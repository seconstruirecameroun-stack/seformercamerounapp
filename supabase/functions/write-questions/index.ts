/**
 * write-questions — les explications et les questions d'une leçon lue.
 *
 * analyze-document s'arrête aux notions. Sans cette fonction, le parent
 * publiait une leçon que l'enfant pouvait lire mais pas jouer : « Jouer » le
 * déposait directement sur l'écran de fin, sans une seule question.
 *
 * Elle est appelée une fois par leçon, juste après la lecture. Deux appels
 * courts valent mieux qu'un long : une seule requête pour trois leçons
 * dépasserait le temps accordé à une fonction, et une panne au milieu
 * perdrait tout.
 *
 * Elle garantit une chose, et c'est sa raison d'être : chaque notion
 * conservée a de quoi franchir les QUATRE étapes. Une notion sans question à
 * un niveau bloque la leçon pour toujours — elle reste comptée dans le
 * total, n'est jamais posée, et rien à l'écran ne dit pourquoi l'étape ne se
 * termine pas. Une notion qui n'y arrive pas après un second essai est donc
 * écartée plutôt que laissée en travers.
 */

import Anthropic from 'npm:@anthropic-ai/sdk@0.74.0';
import { createClient } from 'npm:@supabase/supabase-js@2.49.4';
import {
  CORS,
  etapesManquantes,
  fauteDeQuestion,
  HONNETETE,
  lireJson,
  TON,
} from './maison.ts';
import type { Item } from './maison.ts';

const REGISTRES = ['simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'];

/**
 * Les quatre étapes, et ce que chacune demande vraiment.
 *
 * Ce ne sont pas quatre niveaux de difficulté : ce sont quatre façons de
 * savoir la même chose. Un enfant peut reconnaître sans savoir restituer, et
 * restituer lentement sans savoir répondre vite.
 */
const ETAPES = `ÉTAPE 1 — Découverte. Reconnaître. La bonne réponse est dans ce qu-on lui
montre : il la choisit. Type : qcm ou vrai_faux.

ÉTAPE 2 — Entraînement. Comprendre. Il doit relier, ranger, ou choisir entre
des réponses qui se ressemblent. Type : qcm, association ou chronologie.

ÉTAPE 3 — Maîtrise. Restituer. Rien ne lui est proposé : il écrit le mot.
Type : texte_a_trous.

ÉTAPE 4 — Défi. Répondre vite et sans aide. Le temps est compté, donc
seulement qcm ou vrai_faux — relier ou ranger des étiquettes y ferait perdre
sur la montre et non sur le savoir. C-est aussi l-étape où l-on pose la
question qui sépare deux choses qu-on confond.`;

const TYPES = `qcm           { "question": "…", "options": ["…", "…", "…"] } + { "index": 0 }
              Trois réponses. La question fait 90 caractères au plus, chaque
              réponse 70 au plus. Les mauvaises réponses doivent être
              plausibles : une réponse absurde ne fait pas réfléchir.
              Elles doivent aussi avoir À PEU PRÈS LA MÊME LONGUEUR que la
              bonne. Une bonne réponse deux fois plus longue se repère sans
              lire la question.

vrai_faux     { "statement": "…" } + { "value": true }
              110 caractères au plus. Vise moitié de vrai, moitié de faux sur
              l-ensemble : toujours vrai se devine sans savoir.

texte_a_trous { "text": "… {{1}} …", "blanks": 1 } + { "values": ["mot"] }
              Un ou deux trous. LA RÉPONSE EST UN SEUL MOT, sans espace : le
              clavier de cet exercice n-a pas de touche espace, et « 3 000 »
              ou « eau de javel » seraient impossibles à taper. Seize lettres
              au plus. Lettres, accents français, chiffres, trait d-union,
              virgule et point uniquement.

association   { "question": "…", "gauche": [...], "droite": [...] } + { "order": [0,1,2] }
              2 à 4 paires. order[i] est l-indice dans "droite" de ce qui va
              avec gauche[i]. Écris les paires en face l-une de l-autre
              (order [0,1,2]) : l-application mélange l-affichage elle-même.

chronologie   { "question": "…", "tokens": [...] } + { "order": [0,1,2] }
              3 à 5 étiquettes, données DANS LE BON ORDRE, order [0,1,2,…].
              Pour un ordre réel : des étapes, des dates, une suite de mots
              d-une phrase. Jamais pour une liste sans ordre.`;

const PIEGES = `CE QUI A DÉJÀ RATÉ, ET QU-ON NE REFAIT PAS.

La réponse toujours à la même place. Sur 277 questions à choix, la bonne
réponse était la première. Les 277. L-application mélange désormais
l-affichage, donc range la bonne réponse où tu veux — mais ne compense pas
en la cachant toujours en dernier.

La réponse reconnaissable à sa forme. La plus longue, la plus précise, la
seule bien rédigée : l-enfant la trouve sans rien savoir.

Les notions qui se confondent, non séparées. Quand deux ou trois notions de
la leçon se ressemblent par les mots — le nom, la nationalité, l-identité —
l-enfant les récite dans l-ordre sans savoir laquelle fait quoi. Chaque fois
que tu interroges l-une, mets les autres dans les mauvaises réponses. C-est
la seule façon de réviser la différence plutôt que la liste.

La question qui porte sur un point douteux. Si le cahier se trompe ou se
contredit, on enseigne ce qu-il dit mais on n-interroge pas dessus.

La réponse impossible à taper. Deux mots, un nombre avec une espace, un
symbole absent du clavier : l-enfant ne peut pas la réussir, quoi qu-il
écrive, et la faute est comptée contre lui.`;

const FORMAT = `Tu réponds par un unique objet JSON, sans texte autour :

{
  "notions": [
    {
      "id": "l-identifiant exact de la notion",
      "explications": [
        { "registre": "simple | analogie | histoire | visuel | pas_a_pas",
          "corps": "une ou deux phrases, 190 caractères au plus" }
      ],
      "questions": [
        { "kind": "qcm | vrai_faux | texte_a_trous | association | chronologie",
          "level": 1,
          "payload": { },
          "answer": { },
          "explain": "pourquoi c-est cette réponse, une phrase courte" }
      ]
    }
  ],
  "avertissements": ["ce qui t-a gêné"]
}

Pour CHAQUE notion : deux ou trois explications de registres différents, et
EXACTEMENT CINQ questions dont au moins une à chacune des étapes 1, 2, 3 et
4. La cinquième est une seconde question d-étape 1 ou 2.`;

function consigne(contexte: string): string {
  return `Tu écris les explications et les questions de révision d-une leçon déjà
transcrite d-un cahier du primaire camerounais.

${contexte}

${HONNETETE}

${TON}

${ETAPES}

LES TYPES DE QUESTION

${TYPES}

LES EXPLICATIONS. Deux ou trois par notion, de registres différents :
- simple    : redire la notion autrement, avec des mots plus courts
- analogie  : la rapprocher de ce que l-enfant connaît déjà chez lui
- visuel    : décrire ce qu-on voit, ce qui se compte, ce qui se montre
- pas_a_pas : la décomposer en gestes ou en moments successifs
- histoire  : une phrase de récit, pour une notion de date
Aucune n-ajoute de savoir : elles redisent la notion, elles ne l-étendent pas.

${PIEGES}

${FORMAT}`;
}

type Sortie = {
  notions: Array<{
    id: string;
    explications: Array<{ registre: string; corps: string }>;
    questions: Item[];
  }>;
  avertissements?: string[];
};

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

  let lessonId: string | undefined;
  try {
    ({ lesson_id: lessonId } = await req.json());
  } catch (_) {
    return repondre({ erreur: 'corps illisible' }, 400);
  }
  if (!lessonId) return repondre({ erreur: 'lesson_id manquant' }, 400);

  const { data: lecon, error: errLecon } = await supabase
    .from('lessons')
    .select('id, title, summary, lang, chapter, class_id, classes(label), subjects(label)')
    .eq('id', lessonId)
    .maybeSingle();
  if (errLecon) return repondre({ erreur: errLecon.message }, 400);
  if (!lecon) return repondre({ erreur: 'leçon introuvable' }, 404);

  const { data: notions } = await supabase
    .from('notions')
    .select('id, kind, statement, sort_order')
    .eq('lesson_id', lessonId)
    .order('sort_order');
  if (!notions || notions.length === 0) return repondre({ erreur: 'leçon sans notion' }, 400);

  // Une notion qui a déjà ses questions n-est pas refaite : la fonction peut
  // être relancée sans tout dupliquer.
  const { data: dejaFaites } = await supabase
    .from('items')
    .select('notion_id')
    .in('notion_id', notions.map((n) => n.id));
  const avec = new Set((dejaFaites ?? []).map((i) => (i as { notion_id: string }).notion_id));
  const aFaire = notions.filter((n) => !avec.has(n.id));
  if (aFaire.length === 0) return repondre({ notions: 0, questions: 0, avertissements: [] });

  const classe = (lecon as { classes?: { label?: string } }).classes?.label ?? '';
  const matiere = (lecon as { subjects?: { label?: string } }).subjects?.label ?? '';

  const contexte =
    `Leçon : « ${lecon.title} »` +
    (lecon.chapter ? `, chapitre « ${lecon.chapter} »` : '') +
    (matiere ? `, matière ${matiere}` : '') +
    (classe ? `, classe ${classe}` : '') +
    `.\nLangue de la leçon : ${lecon.lang === 'en' ? 'anglais' : 'français'}. ` +
    `Tu écris TOUT dans cette langue — questions, explications et justifications.` +
    (lecon.summary ? `\nÀ retenir : ${lecon.summary}` : '');

  const anthropic = new Anthropic({ apiKey: cle });

  async function demander(liste: Array<{ id: string; kind: string; statement: string }>) {
    const params: Record<string, unknown> = {
      model: 'claude-opus-5-5',
      max_tokens: 32000,
      output_config: { effort: 'high' },
      system: consigne(contexte),
      messages: [
        {
          role: 'user',
          content:
            'Voici les notions de la leçon, dans l-ordre.\n\n' +
            liste
              .map((n) => `id: ${n.id}\ntype: ${n.kind}\nénoncé: ${n.statement}`)
              .join('\n\n') +
            '\n\nÉcris les explications et les questions.',
        },
      ],
    };
    // En flux, parce qu-une réponse de cette taille dépasserait le délai
    // d-une requête ordinaire. L-objet est typé largement : « effort » est
    // récent, et un désaccord de types avec la version du SDK installée
    // ferait échouer la construction de la fonction, pas son exécution.
    const flux = anthropic.messages.stream(params as Anthropic.MessageStreamParams);
    const reponse = await flux.finalMessage();
    const texte = reponse.content
      .filter((b): b is Anthropic.TextBlock => b.type === 'text')
      .map((b) => b.text)
      .join('');
    return { sortie: lireJson<Sortie>(texte), usage: reponse.usage };
  }

  try {
    const avertissements: string[] = [];
    const retenues = new Map<string, { explications: Sortie['notions'][0]['explications']; questions: Item[] }>();

    // Premier passage, puis un second pour les seules notions qui n-ont pas
    // abouti. Une question mal formée n-est pas rattrapée à la main : on la
    // jette et on redemande, parce qu-une question réparée au jugé est
    // exactement ce qu-on cherche à éviter.
    let liste = aFaire as Array<{ id: string; kind: string; statement: string }>;
    let usage: unknown = null;
    for (let passage = 0; passage < 2 && liste.length > 0; passage++) {
      const { sortie, usage: u } = await demander(liste);
      usage = u;
      for (const n of sortie.notions ?? []) {
        const cible = liste.find((x) => x.id === n.id);
        if (!cible) continue;
        const bonnes: Item[] = [];
        for (const q of n.questions ?? []) {
          const faute = fauteDeQuestion(q);
          if (faute) {
            if (passage === 1) avertissements.push(`« ${cible.statement.slice(0, 50)} » : ${faute}`);
            continue;
          }
          bonnes.push(q);
        }
        const manque = etapesManquantes(bonnes);
        if (manque.length === 0) {
          const expl = (n.explications ?? [])
            .filter((e) => REGISTRES.includes(e.registre) && e.corps?.trim())
            .slice(0, 3)
            .map((e) => ({ registre: e.registre, corps: e.corps.slice(0, 200) }));
          retenues.set(n.id, { explications: expl, questions: bonnes });
        }
      }
      liste = liste.filter((n) => !retenues.has(n.id));
      if (liste.length > 0 && passage === 0) {
        avertissements.push(
          `Second essai pour ${liste.length} notion(s) dont les questions ne tenaient pas les règles.`,
        );
      }
    }

    // Ce qui n-a pas abouti est écarté, pas laissé en travers : une notion
    // sans ses quatre étapes bloquerait la leçon entière.
    for (const n of liste) {
      await supabase.from('notions').update({ status: 'rejected' }).eq('id', n.id);
      avertissements.push(
        `Notion écartée faute de questions valides : « ${n.statement.slice(0, 60)} ». ` +
        `Elle bloquerait la leçon si elle restait.`,
      );
    }

    let questions = 0;
    for (const [notionId, contenu] of retenues) {
      if (contenu.explications.length > 0) {
        const { error } = await supabase.from('explanations').insert(
          contenu.explications.map((e) => ({
            parent_id: parentId,
            notion_id: notionId,
            register: e.registre,
            body: e.corps,
            status: 'pending',
          })),
        );
        if (error) throw error;
      }
      const { error } = await supabase.from('items').insert(
        contenu.questions.map((q) => ({
          parent_id: parentId,
          notion_id: notionId,
          kind: q.kind,
          level: q.level,
          payload: q.payload,
          answer: q.answer,
          explain: q.explain ?? null,
          status: 'pending',
        })),
      );
      if (error) throw error;
      questions += contenu.questions.length;
    }

    return repondre({
      notions: retenues.size,
      ecartees: liste.length,
      questions,
      avertissements,
      usage,
    });
  } catch (e) {
    const message = e instanceof Error ? e.message : String(e);
    return repondre({ erreur: message }, 500);
  }
});
