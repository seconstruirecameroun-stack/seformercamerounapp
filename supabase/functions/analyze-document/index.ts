/**
 * analyze-document — lecture d'un cahier photographié.
 *
 * Reçoit un batch_id : les pages photographiées envoyées ensemble. Le parent
 * n'a rien d'autre à remplir que l'enfant. Tout le reste — la matière, le
 * jour, le titre, le chapitre, le découpage — est lu sur la page.
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
 * 3. Un envoi peut contenir PLUSIEURS leçons. C'est le cas courant : on
 *    photographie un cahier d'un coup, et il porte trois jours et trois
 *    matières. La première version en faisait une seule leçon, dont le titre
 *    était les trois titres collés. Elle sait maintenant les séparer.
 *
 * Elle écrit la classe de l'enfant sur chaque leçon. Sans elle, la leçon est
 * montrée à TOUS les enfants de la famille — le CM1 retrouvait les leçons de
 * CE1 de son frère dans sa liste.
 *
 * Elle ne pose pas les questions : c'est le travail de write-questions,
 * appelée ensuite pour chaque leçon. Deux appels courts valent mieux qu'un
 * long, qui dépasserait le temps accordé à une fonction.
 */

import Anthropic from 'npm:@anthropic-ai/sdk@0.74.0';
import { createClient } from 'npm:@supabase/supabase-js@2.49.4';
import { base64, CORS, HONNETETE, lireJson, TON } from './maison.ts';

/**
 * Le style maison, identique à celui de la chaîne vidéo.
 *
 * Aucun texte dans l'image : les mots sont superposés par l'app, ce qui
 * permet de corriger un mot sans refaire l'image, et de servir un cours en
 * français comme en anglais avec la même illustration.
 */
const STYLE =
  'Pastel flat 2D children illustration, soft gradient sky, sand, mint and ' +
  'lilac palette, no black outlines, rounded friendly shapes, gentle shading, ' +
  'no text, no letters, no numbers, no watermark, no real person, no brand.';

const FORMAT = `Tu réponds par un unique objet JSON, sans texte autour :

{
  "lisibilite": "bonne, moyenne ou mauvaise",
  "lecons": [
    {
      "langue": "fr ou en, la langue dans laquelle CETTE leçon est écrite",
      "titre": "le titre, repris du cahier s-il y figure",
      "chapitre": "le chapitre, le thème ou l-unité, chaîne vide si absent",
      "matiere": "l-intitulé de la matière, repris de la liste fournie si l-un convient",
      "jour": "la date écrite en haut de la page, au format AAAA-MM-JJ, chaîne vide si absente",
      "resume": "ce qu-il faut retenir, deux ou trois phrases courtes, 380 caractères au plus",
      "illustration_scene": "consigne d-image EN ANGLAIS pour la scène d-ouverture, 16:9, sans texte : un lieu ou une situation, jamais un concept",
      "pages": [1, 2],
      "notions": [
        {
          "type": "definition | date | liste | relation",
          "enonce": "une seule chose à savoir, une phrase, 150 caractères au plus",
          "illustration": "consigne d-image EN ANGLAIS pour une vignette carrée : un objet ou un petit groupe d-objets sur fond uni, sans texte"
        }
      ]
    }
  ],
  "avertissements": ["ce qui est illisible, douteux, incomplet ou pédagogiquement discutable"]
}`;

type Lecon = {
  langue: string;
  titre: string;
  chapitre: string;
  matiere: string;
  jour: string;
  resume: string;
  illustration_scene: string;
  pages: number[];
  notions: Array<{ type: string; enonce: string; illustration: string }>;
};

type Extraction = { lisibilite: string; lecons: Lecon[]; avertissements: string[] };

const TYPES = ['definition', 'date', 'liste', 'relation'];

function consigne(matieres: string[]): string {
  return `Tu lis des pages de cahier du primaire camerounais, photographiées par un
parent, et tu les structures pour une application de révision.

${HONNETETE}

${TON}

DÉCOUPAGE. Les pages arrivent dans l-ordre, mais elles ne forment pas
forcément un seul cours. Une nouvelle leçon commence à chaque fois que change
l-une de ces trois choses : la date écrite en haut, la matière, ou le titre
souligné. Rends une entrée par leçon, et dis dans "pages" quelles pages la
composent. Un cahier photographié d-un coup en contient souvent trois.

NOTIONS. Une notion est une seule chose à savoir, formulée en une phrase,
telle qu-un élève doit pouvoir la restituer. Son type :
- definition : ce qu-est une chose
- date : un repère chronologique
- liste : des éléments à retenir ensemble
- relation : un ordre, une cause, une conséquence

Entre 3 et 6 notions par leçon, dans l-ordre du cours. Au-delà de six, la
leçon est trop longue à réviser d-une traite : coupe-la en deux leçons.

Découpe aussi une notion en deux quand elle demande deux choses différentes.
« Le nom relie l-enfant à une famille » et « la nationalité le rattache à un
pays » sont deux notions, pas une.

MATIÈRE. Voici les matières déjà connues pour cette classe :
${matieres.length ? matieres.map((m) => '- ' + m).join('\n') : '- (aucune pour l-instant)'}
Reprends l-intitulé exact de cette liste dès que l-un convient. N-en propose
un nouveau que si aucun ne correspond vraiment.

IMAGES. Pour chaque notion, écris une consigne d-image en anglais. Elle décrit
une chose concrète et montrable, jamais une idée abstraite : pour
« l-écriture marque la fin de la Préhistoire », décris une tablette d-argile
gravée et un stylet, pas « la fin d-une époque ». Aucune image ne contient de
texte.

` + FORMAT;
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

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: autorisation } } },
  );

  const { data: utilisateur } = await supabase.auth.getUser();
  const parentId = utilisateur?.user?.id;
  if (!parentId) return repondre({ erreur: 'session invalide' }, 401);

  let batchId: string | undefined;
  try {
    ({ batch_id: batchId } = await req.json());
  } catch (_) {
    return repondre({ erreur: 'corps illisible' }, 400);
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
    // La classe de l-enfant : elle commande les matières proposées, et elle
    // sera écrite sur chaque leçon.
    const { data: enfant } = await supabase
      .from('children')
      .select('class_id')
      .eq('id', pages[0].child_id)
      .maybeSingle();
    const classId = (enfant as { class_id: string | null } | null)?.class_id ?? null;

    const { data: matieres } = await supabase
      .from('subjects')
      .select('id, label')
      .eq('parent_id', parentId)
      .eq('class_id', classId ?? '00000000-0000-0000-0000-000000000000');
    const catalogue = (matieres ?? []) as Array<{ id: string; label: string }>;

    const contenu: Anthropic.ContentBlockParam[] = [];
    for (const page of pages) {
      const { data: fichier, error } = await supabase.storage
        .from('cours')
        .download(page.storage_path!);
      if (error) throw error;

      const donnees = base64(new Uint8Array(await fichier.arrayBuffer()));
      const type = page.mime ?? 'image/jpeg';

      contenu.push({ type: 'text', text: `Page ${page.page_no} :` });
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
        `Ces ${pages.length} page(s) forment un ou plusieurs ${pages[0].kind}. ` +
        `Transcris, découpe en leçons, puis structure selon le format demandé.`,
    });

    const anthropic = new Anthropic({ apiKey: cle });
    // En flux, parce qu-une réponse de cette taille dépasserait le délai
    // d-une requête ordinaire. L-objet est typé largement : « effort » est
    // récent, et un désaccord de types avec la version du SDK installée
    // ferait échouer la construction de la fonction, pas son exécution.
    const params: Record<string, unknown> = {
      model: 'claude-opus-5-5',
      max_tokens: 32000,
      output_config: { effort: 'high' },
      system: consigne(catalogue.map((m) => m.label)),
      messages: [{ role: 'user', content: contenu }],
    };
    const flux = anthropic.messages.stream(params as Anthropic.MessageStreamParams);
    const reponse = await flux.finalMessage();

    const texte = reponse.content
      .filter((b): b is Anthropic.TextBlock => b.type === 'text')
      .map((b) => b.text)
      .join('');
    const extrait = lireJson<Extraction>(texte);

    if (!Array.isArray(extrait?.lecons) || extrait.lecons.length === 0) {
      throw new Error('Lecture sans leçon exploitable.');
    }
    const avertissements = Array.isArray(extrait.avertissements) ? extrait.avertissements : [];

    // Les leçons se rangent après les leçons existantes de la classe.
    const { data: dernieres } = await supabase
      .from('lessons')
      .select('sort_order')
      .order('sort_order', { ascending: false })
      .limit(1);
    let rang = ((dernieres?.[0] as { sort_order: number } | undefined)?.sort_order ?? 0) + 1;

    const faites: Array<{ id: string; titre: string; notions: number }> = [];

    for (const L of extrait.lecons) {
      const notions = (L.notions ?? []).filter(
        (n) => n && typeof n.enonce === 'string' && n.enonce.trim(),
      );
      if (notions.length === 0) {
        avertissements.push('Une leçon lue sans notion exploitable a été ignorée : ' + (L.titre ?? ''));
        continue;
      }

      // La matière du parent prime s-il en a choisi une à l-import ; sinon
      // celle du cahier, rattachée à la classe de l-enfant.
      let subjectId = pages[0].subject_id as string | null;
      if (!subjectId && L.matiere?.trim()) {
        const libelle = L.matiere.trim().slice(0, 60);
        const connue = catalogue.find((m) => m.label.toLowerCase() === libelle.toLowerCase());
        if (connue) subjectId = connue.id;
        else {
          const { data: creee } = await supabase
            .from('subjects')
            .insert({ parent_id: parentId, class_id: classId, label: libelle })
            .select('id, label')
            .single();
          if (creee) {
            catalogue.push(creee as { id: string; label: string });
            subjectId = (creee as { id: string }).id;
          }
        }
      }

      const jour = /^\d{4}-\d{2}-\d{2}$/.test(L.jour ?? '') ? L.jour : null;
      const premiere = pages.find((p) => (L.pages ?? []).includes(p.page_no)) ?? pages[0];

      const { data: lecon, error: errLecon } = await supabase
        .from('lessons')
        .insert({
          parent_id: parentId,
          class_id: classId,
          document_id: premiere.id,
          subject_id: subjectId,
          title: String(L.titre ?? '').slice(0, 200) || 'Leçon sans titre',
          summary: String(L.resume ?? '').slice(0, 400),
          illustration_prompt: STYLE + ' ' + (L.illustration_scene ?? ''),
          lang: L.langue === 'en' ? 'en' : 'fr',
          chapter: L.chapitre?.trim() || null,
          taught_on: jour,
          sort_order: rang++,
          status: 'pending',
        })
        .select('id')
        .single();
      if (errLecon) throw errLecon;

      const { error: errNotions } = await supabase.from('notions').insert(
        notions.map((n, i) => ({
          parent_id: parentId,
          lesson_id: lecon.id,
          kind: TYPES.includes(n.type) ? n.type : 'definition',
          statement: String(n.enonce).slice(0, 180),
          illustration_prompt: STYLE + ' ' + (n.illustration ?? ''),
          sort_order: i + 1,
          status: 'pending',
        })),
      );
      if (errNotions) throw errNotions;

      faites.push({ id: lecon.id, titre: String(L.titre ?? ''), notions: notions.length });
    }

    if (faites.length === 0) throw new Error('Aucune leçon n-a pu être enregistrée.');

    await supabase
      .from('documents')
      .update({ stage: 'a_valider', stage_error: null, lang: extrait.lecons[0].langue === 'en' ? 'en' : 'fr' })
      .in('id', ids);

    return repondre({
      lecons: faites,
      notions: faites.reduce((n, l) => n + l.notions, 0),
      lisibilite: extrait.lisibilite ?? null,
      avertissements,
      usage: reponse.usage,
    });
  } catch (e) {
    const message = e instanceof Error ? e.message : String(e);
    await marquer('echec', message.slice(0, 500));
    return repondre({ erreur: message }, 500);
  }
});
