/**
 * analyze-document — lecture d'un cours photographié et extraction en notions.
 *
 * Reçoit un batch_id (les pages photographiées d'un même cours), lit les
 * fichiers, puis produit un résumé et des notions typées.
 *
 * Trois partis pris :
 *
 * 1. La fonction s'exécute avec le jeton du parent, jamais avec la clé
 *    service_role. La RLS s'applique donc normalement : un parent ne peut
 *    analyser que ses propres documents, et aucune clé d'administration ne
 *    traîne dans l'environnement.
 *
 * 2. Le contenu produit naît en statut « pending ». Rien n'arrive à l'enfant
 *    sans un passage par le parent.
 *
 * 3. Le modèle n'a pas le droit d'ajouter du savoir. Il transcrit, structure
 *    et signale ses doutes. Un programme scolaire varie d'une école à l'autre,
 *    et compléter de mémoire produirait des révisions fausses.
 */

import Anthropic from 'npm:@anthropic-ai/sdk@0.74.0';
import { zodOutputFormat } from 'npm:@anthropic-ai/sdk@0.74.0/helpers/zod';
import { z } from 'npm:zod@3.25.76';
import { createClient } from 'npm:@supabase/supabase-js@2.49.4';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

/**
 * Le style maison, identique à celui de la chaîne vidéo.
 *
 * Deux exigences non négociables dans chaque consigne :
 *  - aucun texte dans l'image : les mots-clés sont superposés par l'app, ce
 *    qui permet de corriger un mot sans repayer une génération, et de servir
 *    un cours en français comme en anglais avec la même image ;
 *  - aucun personnage reconnaissable ni marque.
 */
const STYLE =
  'Pastel flat 2D children illustration, soft gradient sky, sand, mint and ' +
  'lilac palette, no black outlines, rounded friendly shapes, gentle shading, ' +
  'no text, no letters, no numbers, no watermark, no real person, no brand.';

const Extraction = z.object({
  langue: z.enum(['fr', 'en']).describe('Langue du cours, telle qu’elle est écrite.'),
  lisibilite: z.enum(['bonne', 'moyenne', 'mauvaise']),
  titre: z.string().describe('Titre de la leçon, repris du document si présent.'),
  chapitre: z.string().describe('Chapitre ou thème, ou chaîne vide si absent.'),
  matiere_suggeree: z
    .string()
    .describe('Intitulé de la matière tel qu’il apparaît sur le document.'),
  resume: z
    .string()
    .describe(
      'Le résumé à retenir, en deux ou trois phrases courtes. 300 caractères au maximum.',
    ),
  illustration_scene: z
    .string()
    .describe(
      'Consigne d’image en anglais pour la scène d’ouverture de la leçon, ' +
        'format 16:9, sans texte. Décrit un lieu ou une situation, pas un concept.',
    ),
  notions: z
    .array(
      z.object({
        type: z.enum(['definition', 'date', 'liste', 'relation']),
        enonce: z
          .string()
          .describe('Une seule chose à savoir, en une phrase courte. 110 caractères au maximum.'),
        illustration: z
          .string()
          .describe(
            'Consigne d’image en anglais pour une vignette carrée illustrant ' +
              'cette notion : un objet ou un petit groupe d’objets sur fond ' +
              'uni, sans texte.',
          ),
      }),
    )
    .describe('Entre 3 et 10 notions, dans l’ordre du cours.'),
  avertissements: z
    .array(z.string())
    .describe('Passages illisibles, douteux ou pédagogiquement discutables.'),
});

const SYSTEM = `Tu transcris et structures des cours du primaire camerounais pour une application de révision.

Règles absolues :
- N'ajoute aucun savoir qui ne figure pas dans le document. Chaque école a son programme ; compléter de mémoire produirait des révisions fausses.
- Si un passage est illisible ou douteux, ne devine pas : signale-le dans avertissements.
- Si le document contredit ce que tu sais du sujet, transcris quand même ce qu'il dit, et signale l'écart dans avertissements. Le parent tranchera.
- Garde la langue du document. Ne traduis pas.

Une notion est une seule chose à savoir, formulée en une phrase, telle qu'un élève doit pouvoir la restituer. Type :
- definition : ce qu'est une chose
- date : un repère chronologique
- liste : des éléments à retenir ensemble
- relation : un ordre, une cause, une conséquence

Écris court. Le lecteur a entre six et onze ans, lit lentement, et saute tout
paragraphe. Une phrase qu'il lit vaut mieux qu'un paragraphe exact qu'il
ignore. Pas de subordonnées empilées, pas de mot savant sans le dire
autrement, pas de phrase de plus de vingt mots.

Les pages sont fournies dans l'ordre et forment un seul cours.

Pour chaque notion, écris aussi une consigne d'image en anglais. Elle doit
décrire une chose concrète et montrable, jamais une idée abstraite : pour
« l'écriture marque la fin de la Préhistoire », décris une tablette d'argile
gravée et un stylet, pas « la fin d'une époque ». Aucune image ne contient de
texte : les mots sont posés par l'application par-dessus.`;

function base64(bytes: Uint8Array): string {
  let binaire = '';
  const pas = 0x8000; // par tranches, sinon la pile déborde sur un gros fichier
  for (let i = 0; i < bytes.length; i += pas) {
    binaire += String.fromCharCode(...bytes.subarray(i, i + pas));
  }
  return btoa(binaire);
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });

  const repondre = (corps: unknown, status = 200) =>
    new Response(JSON.stringify(corps), {
      status,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });

  const autorisation = req.headers.get('Authorization');
  if (!autorisation) return repondre({ erreur: 'authentification requise' }, 401);

  const cle = Deno.env.get('ANTHROPIC_API_KEY');
  if (!cle) return repondre({ erreur: 'ANTHROPIC_API_KEY absente des secrets' }, 500);

  // Le client porte le jeton du parent : la RLS fait le reste.
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: autorisation } } },
  );

  const { data: auth } = await supabase.auth.getUser();
  const parentId = auth.user?.id;
  if (!parentId) return repondre({ erreur: 'session invalide' }, 401);

  let batchId: string;
  try {
    ({ batch_id: batchId } = await req.json());
  } catch {
    return repondre({ erreur: 'corps JSON attendu' }, 400);
  }
  if (!batchId) return repondre({ erreur: 'batch_id manquant' }, 400);

  const { data: pages, error: errPages } = await supabase
    .from('documents')
    .select('id, storage_path, mime, page_no, child_id, subject_id, kind')
    .eq('batch_id', batchId)
    .order('page_no');

  if (errPages) return repondre({ erreur: errPages.message }, 400);
  if (!pages || pages.length === 0) return repondre({ erreur: 'aucun document' }, 404);

  const ids = pages.map((p) => p.id);
  const marquer = (stage: string, erreur: string | null = null) =>
    supabase.from('documents').update({ stage, stage_error: erreur }).in('id', ids);

  await marquer('en_lecture');

  try {
    const contenu: Anthropic.ContentBlockParam[] = [];
    for (const page of pages) {
      const { data: fichier, error } = await supabase.storage
        .from('cours')
        .download(page.storage_path!);
      if (error) throw error;

      const donnees = base64(new Uint8Array(await fichier.arrayBuffer()));
      const type = page.mime ?? 'image/jpeg';

      if (type === 'application/pdf') {
        contenu.push({
          type: 'document',
          source: { type: 'base64', media_type: 'application/pdf', data: donnees },
        });
      } else {
        contenu.push({
          type: 'image',
          source: {
            type: 'base64',
            media_type: type as 'image/jpeg' | 'image/png' | 'image/webp',
            data: donnees,
          },
        });
      }
    }

    contenu.push({
      type: 'text',
      text:
        `Ces ${pages.length} page(s) forment un seul ${pages[0].kind}. ` +
        `Transcris, puis structure selon le format demandé.`,
    });

    const anthropic = new Anthropic({ apiKey: cle });
    const reponse = await anthropic.messages.parse({
      model: 'claude-opus-5-5',
      max_tokens: 16000,
      system: SYSTEM,
      thinking: { type: 'adaptive' },
      output_config: { effort: 'medium', format: zodOutputFormat(Extraction) },
      messages: [{ role: 'user', content: contenu }],
    });

    if (reponse.stop_reason === 'refusal') {
      throw new Error('Le modèle a refusé de traiter ce document.');
    }

    const extrait = reponse.parsed_output;
    if (!extrait) throw new Error('Réponse illisible du modèle.');

    // La matière suggérée ne s'impose pas : si le parent en avait déjà choisi
    // une à l'import, elle reste. L'intitulé de l'école prime toujours.
    let subjectId = pages[0].subject_id as string | null;
    if (!subjectId && extrait.matiere_suggeree.trim()) {
      const libelle = extrait.matiere_suggeree.trim().slice(0, 60);
      const { data: existante } = await supabase
        .from('subjects')
        .select('id')
        .eq('label', libelle)
        .maybeSingle();
      if (existante) subjectId = existante.id;
      else {
        const { data: creee } = await supabase
          .from('subjects')
          .insert({ parent_id: parentId, label: libelle })
          .select('id')
          .single();
        subjectId = creee?.id ?? null;
      }
    }

    const { data: lecon, error: errLecon } = await supabase
      .from('lessons')
      .insert({
        parent_id: parentId,
        document_id: pages[0].id,
        subject_id: subjectId,
        title: extrait.titre.slice(0, 200),
        summary: extrait.resume,
        illustration_prompt: STYLE + ' ' + extrait.illustration_scene,
        lang: extrait.langue,
        chapter: extrait.chapitre || null,
        status: 'pending',
      })
      .select('id')
      .single();
    if (errLecon) throw errLecon;

    const { error: errNotions } = await supabase.from('notions').insert(
      extrait.notions.map((n, i) => ({
        parent_id: parentId,
        lesson_id: lecon.id,
        kind: n.type,
        statement: n.enonce,
        illustration_prompt: STYLE + ' ' + n.illustration,
        sort_order: i + 1,
        status: 'pending',
      })),
    );
    if (errNotions) throw errNotions;

    await supabase
      .from('documents')
      .update({
        stage: 'a_valider',
        stage_error: null,
        lang: extrait.langue,
        title_guess: extrait.titre.slice(0, 200),
      })
      .in('id', ids);

    return repondre({
      lesson_id: lecon.id,
      notions: extrait.notions.length,
      langue: extrait.langue,
      lisibilite: extrait.lisibilite,
      avertissements: extrait.avertissements,
      usage: reponse.usage,
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    await marquer('echec', message.slice(0, 500));
    return repondre({ erreur: message }, 500);
  }
});
