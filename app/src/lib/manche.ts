import { supabase } from './supabase';
import type { NotionAvecItems, Question } from './paliers';

/**
 * La manche de validation.
 *
 * Franchir les quatre étapes fait avancer ; valider la leçon certifie. La
 * validation demande la note sur note : TOUTES les questions de la leçon,
 * toutes justes. Vingt pour « Le cube ». C'est volontairement dur — une leçon
 * sue ne se récite pas à huit sur dix.
 *
 * Trois règles de mécanique l'accompagnent, et aucune n'est cosmétique :
 *
 *   La manche va jusqu'au bout. Une faute ne l'interrompt pas : l'enfant
 *   répond à tout, voit chaque correction, et le verdict tombe à la fin.
 *   Couper à la première erreur lui retirerait les dix-neuf explications
 *   qu'il avait encore à lire, et le punirait deux fois.
 *
 *   Ce qu'il a raté est ce qu'on lui redonne. Avant de reproposer la manche,
 *   on repasse sur les notions fautives seules. Rejouer vingt questions
 *   identiques pour une erreur sur les arêtes n'apprend rien sur les arêtes.
 *
 *   La validation se perd. Si une notion d'une leçon validée est ratée plus
 *   tard en révision, la manche est à refaire. C'est la seule exception au
 *   principe « rater fait revenir, pas reculer » de toute l'app, et elle est
 *   assumée : ce principe protège l'apprentissage, qui est fragile, tandis
 *   que la validation est une affirmation faite au parent. Une affirmation
 *   devenue fausse ne vaut rien. Seule la validation se perd — les étapes,
 *   les images, les étoiles et les trophées ne bougent pas.
 *
 * Rien de tout cela n'est stocké comme un état. La table manches journalise
 * ce qui a été joué, et l'état s'en déduit, comme l'étape courante se déduit
 * déjà des tentatives. Une colonne « validée » tenue à la main devrait être
 * corrigée à chaque erreur en révision, et finirait par mentir.
 */

/**
 * Ce que rapporte une manche.
 *
 * Elle valait 120 étoiles à plat, et rien du tout en cas de faute. Les
 * quarante premières manches jouées ont montré deux défauts de cette règle :
 *
 *   Une manche de 40 questions rapportait autant qu-une de 15, alors
 *   qu-elle demande près de trois fois le travail.
 *
 *   Vingt-huit manches ont été ratées, dont NEUF par une seule faute —
 *   38/40, 31/32, 29/30. Celui qui manquait une question recevait
 *   exactement ce que recevait celui qui en manquait douze : zéro.
 *
 * D-où les deux règles ci-dessous. Elles ne touchent qu-aux ÉTOILES : la
 * validation, elle, continue d-exiger le sans-faute. On sépare la
 * récompense, qui encourage, du certificat, qui affirme au parent que
 * l-enfant sait sa leçon. Une affirmation ne se donne pas au prorata.
 */

/** La manche gagnée : cinq étoiles par question, donc proportionnelle. */
export const POINTS_PAR_QUESTION = 5;

/**
 * La consolation : deux étoiles par bonne réponse, à partir de 80 %.
 *
 * Elle n-est versée que si le score BAT le meilleur déjà fait sur cette
 * leçon. Sans cette condition, rejouer indéfiniment la même manche à 24/25
 * rapporterait à chaque fois — on paierait la répétition au lieu du
 * progrès, et l-enfant n-aurait plus de raison de chercher la vingt-cinquième.
 */
export const POINTS_PAR_JUSTE = 2;
export const SEUIL_CONSOLATION = 0.8;

/** Les étoiles d-une manche gagnée, proportionnelles à sa longueur. */
export function pointsManche(questions: number): number {
  return POINTS_PAR_QUESTION * questions;
}

/**
 * Les étoiles d-une manche ratée mais passée tout près.
 *
 * `meilleurPrecedent` est le plus grand nombre de bonnes réponses déjà
 * obtenu sur cette leçon, manches gagnées comprises. Zéro si c-est la
 * première.
 */
export function pointsConsolation(
  justes: number,
  questions: number,
  meilleurPrecedent: number,
): number {
  if (questions <= 0) return 0;
  if (justes >= questions) return 0; // gagnée : ce n-est pas une consolation
  if (justes / questions < SEUIL_CONSOLATION) return 0;
  if (justes <= meilleurPrecedent) return 0;
  return POINTS_PAR_JUSTE * justes;
}

/** Le meilleur nombre de bonnes réponses déjà obtenu sur une leçon. */
export function meilleurJustes(manches: MancheRow[]): number {
  let meilleur = 0;
  for (const m of manches) if (m.justes > meilleur) meilleur = m.justes;
  return meilleur;
}

/**
 * La série de manches parfaites en cours, toutes leçons confondues.
 *
 * On compte depuis la plus récente et on s-arrête à la première ratée. Une
 * série se voit, se rompt et se reconstruit : c-est ce qui en fait un
 * encouragement plutôt qu-un total de plus.
 *
 * `manches` arrive de la plus récente à la plus ancienne, comme partout
 * ailleurs dans ce fichier.
 */
export function serieParfaite(manches: MancheRow[]): number {
  let serie = 0;
  for (const m of manches) {
    if (!m.reussie) break;
    serie += 1;
  }
  return serie;
}

/** Au-delà, la reprise devient une séance comme une autre. */
export const TAILLE_REPRISE = 6;

export type EtatValidation = {
  /** La leçon est validée aujourd'hui. */
  validee: boolean;
  /** Date de la manche réussie, même si la validation a été perdue depuis. */
  obtenueLe: string | null;
  /** La première réponse fausse qui a fait perdre la validation. */
  perdueLe: string | null;
  /** Les notions à redonner avant de reproposer la manche. */
  aReprendre: string[];
  /** Une manche a déjà été tentée et ratée. */
  dejaTentee: boolean;
};

export type MancheRow = {
  lesson_id: string;
  questions: number;
  justes: number;
  reussie: boolean;
  notions_ratees: string[];
  created_at: string;
};

export type Reponse = { notion_id: string; correct: boolean; created_at: string };

/**
 * Les notions encore à reprendre, parmi celles qu'on avait notées fautives.
 *
 * Une notion sort de la liste dès que sa réponse la plus récente, depuis le
 * moment de référence, est juste. Sans cette sortie, la reprise ne finirait
 * jamais : la manche ratée garderait pour toujours la trace des notions
 * manquées, et l'enfant rejouerait les mêmes questions à l'infini sans
 * jamais revoir la manche.
 */
function encoreARevoir(
  candidates: string[],
  reponses: Reponse[],
  depuis: string,
): string[] {
  const derniere = new Map<string, Reponse>();
  for (const r of reponses) {
    if (r.created_at <= depuis) continue;
    const connue = derniere.get(r.notion_id);
    if (!connue || r.created_at > connue.created_at) derniere.set(r.notion_id, r);
  }
  // Pas de réponse depuis : la notion reste à revoir, elle n'a pas été reprise.
  return [...new Set(candidates)].filter((n) => !(derniere.get(n)?.correct ?? false));
}

/**
 * L'état de validation, déduit des manches jouées et du journal des réponses.
 *
 * `reponses` porte les réponses de l'enfant sur les notions de cette leçon,
 * justes et fausses, avec leur date. L'appelant les a déjà lues pour situer
 * l'étape : on ne relit pas le journal une seconde fois.
 */
export function lireValidation(manches: MancheRow[], reponses: Reponse[]): EtatValidation {
  const fausses = reponses.filter((r) => !r.correct);
  // Les manches arrivent de la plus récente à la plus ancienne.
  const derniere = manches[0] ?? null;
  const reussie = manches.find((m) => m.reussie) ?? null;

  if (!reussie) {
    return {
      validee: false,
      obtenueLe: null,
      perdueLe: null,
      aReprendre: derniere
        ? encoreARevoir(derniere.notions_ratees, reponses, derniere.created_at)
        : [],
      dejaTentee: derniere !== null,
    };
  }

  // Une faute postérieure à la manche réussie annule la validation. On prend
  // la première : c'est elle qui dit quand il a cessé de savoir.
  const depuis = fausses
    .filter((f) => f.created_at > reussie.created_at)
    .sort((a, b) => a.created_at.localeCompare(b.created_at));
  const perdue = depuis[0] ?? null;

  if (!perdue) {
    return {
      validee: true,
      obtenueLe: reussie.created_at,
      perdueLe: null,
      aReprendre: [],
      dejaTentee: true,
    };
  }

  // Validation perdue : on redonne d'abord ce qui a été raté depuis. Une
  // manche ratée plus récente que la perte dit mieux ce qui reste à revoir.
  const apres = manches.find((m) => !m.reussie && m.created_at > reussie.created_at);
  const aReprendre = apres
    ? encoreARevoir(apres.notions_ratees, reponses, apres.created_at)
    : encoreARevoir(
        depuis.map((f) => f.notion_id),
        reponses,
        reussie.created_at,
      );

  return {
    validee: false,
    obtenueLe: reussie.created_at,
    perdueLe: perdue.created_at,
    aReprendre,
    dejaTentee: true,
  };
}

/**
 * Toutes les questions de la leçon, dans l'ordre où elle s'apprend.
 *
 * Notion par notion, et à l'intérieur d'une notion de l'étape la plus facile à
 * la plus difficile. Un ordre au hasard ferait sauter l'enfant d'une notion à
 * l'autre et d'une forme de question à l'autre vingt fois de suite, ce qui est
 * une épreuve de souplesse et non de savoir.
 */
export function questionsDeLaManche(notions: NotionAvecItems[]): Question[] {
  const questions: Question[] = [];
  for (const notion of notions) {
    const items = [...notion.items].sort((a, b) => a.level - b.level || a.id.localeCompare(b.id));
    for (const item of items) questions.push({ notion, item });
  }
  return questions;
}

/** Enregistre la manche jouée. Le verdict est le compte, pas une appréciation. */
export async function enregistrerManche(params: {
  parentId: string;
  childId: string;
  lessonId: string;
  questions: number;
  justes: number;
  notionsRatees: string[];
}): Promise<void> {
  const { parentId, childId, lessonId, questions, justes, notionsRatees } = params;
  const { error } = await supabase.from('manches').insert({
    parent_id: parentId,
    child_id: childId,
    lesson_id: lessonId,
    questions,
    justes,
    reussie: justes === questions,
    notions_ratees: [...new Set(notionsRatees)],
  });
  if (error) throw error;
}
