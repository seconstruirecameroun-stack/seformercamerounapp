import { supabase } from './supabase';
import type { ItemRow, NotionRow } from '../types/db';

/**
 * Les étapes d'une leçon.
 *
 * Une leçon se franchit comme les niveaux d'un jeu : trois étapes, dans
 * l'ordre, et on ne passe pas à la suivante tant que la précédente n'est pas
 * nette. C'est la règle que l'enfant comprend sans explication — il l'a déjà
 * vue partout ailleurs.
 *
 * Ce qui valide une étape : avoir répondu juste, à ce niveau, sur CHAQUE
 * notion de la leçon. Pas un score moyen, pas un pourcentage. Une moyenne
 * laisse passer un enfant qui ignore trois notions sur dix ; ici, chaque
 * notion doit tomber.
 *
 * Tant qu'il reste des notions à valider, la séance suivante repose des
 * questions sur celles-là, et sur celles-là seulement — avec une autre
 * formulation quand elle existe. Rater ne fait pas reculer : ça fait revenir.
 * Pour un enfant de primaire, perdre un acquis décourage bien plus que ça ne
 * motive.
 *
 * Tout se déduit du journal des tentatives. Aucune colonne « étape en cours »
 * à tenir à jour, donc rien qui puisse mentir sur l'état réel.
 */

export type Palier = {
  niveau: number;
  nom: string;
  /** Ce que l'enfant doit savoir faire à cette étape, dit en mots d'enfant. */
  promesse: string;
};

export const PALIERS: Palier[] = [
  { niveau: 1, nom: 'Découverte', promesse: 'Reconnaître' },
  { niveau: 2, nom: 'Entraînement', promesse: 'Bien comprendre' },
  { niveau: 3, nom: 'Maîtrise', promesse: 'Savoir écrire' },
  { niveau: 4, nom: 'Défi', promesse: 'Vite et juste' },
];

/**
 * La dernière étape se joue au chronomètre.
 *
 * Vingt secondes par question : assez pour lire et réfléchir à cet âge, trop
 * peu pour aller chercher la réponse dans la leçon. Le temps écoulé compte
 * comme une erreur — on ne punit pas, la notion revient simplement.
 */
export const SECONDES_DEFI = 20;

export function estChronometre(niveau: number): boolean {
  return niveau === 4;
}

export const TAILLE_SEANCE = 6;

export type NotionAvecItems = NotionRow & { items: ItemRow[] };

export type Question = {
  notion: NotionAvecItems;
  item: ItemRow;
};

export type Seance = {
  /** L'étape en cours, 1 à 3. */
  niveau: number;
  palier: Palier;
  /** Les trois étapes sont franchies : la leçon passe en révision. */
  termine: boolean;
  /** Notions concernées par cette étape. */
  total: number;
  /** Notions déjà validées à cette étape, avant la séance. */
  reussies: number;
  /** Les questions à poser maintenant. */
  questions: Question[];
  /** Notions encore à valider après cette séance, si elle est parfaite. */
  restantAprès: number;
};

/**
 * Le strict nécessaire pour situer une étape : un identifiant, des niveaux.
 * Le tableau de bord applique ainsi la même règle que la salle de jeu, sans
 * charger les énoncés ni en recopier le calcul.
 */
export type NotionNiveaux = { id: string; items: Array<{ level: number }> };

/** Les notions qui ont au moins une question à ce niveau. */
function concernees<T extends NotionNiveaux>(notions: T[], niveau: number): T[] {
  return notions.filter((n) => n.items.some((i) => i.level === niveau));
}

/**
 * La question posée à une notion, à ce niveau.
 *
 * On sert d'abord ce que l'enfant n'a jamais vu : reposer mot pour mot la
 * question qu'il vient de rater lui apprend la réponse, pas la notion. À
 * défaut, celle qu'il a vue le moins souvent.
 */
export function choisirQuestion(
  notion: NotionAvecItems,
  niveau: number,
  vus: Map<string, number>,
): ItemRow | null {
  const candidats = notion.items.filter((i) => i.level === niveau);
  if (candidats.length === 0) return null;

  const moins = Math.min(...candidats.map((i) => vus.get(i.id) ?? 0));
  const frais = candidats.filter((i) => (vus.get(i.id) ?? 0) === moins);
  return frais[Math.floor(Math.random() * frais.length)];
}

/**
 * Les notions déjà validées, niveau par niveau, d'après les bonnes réponses.
 *
 * Une seule bonne réponse suffit à valider une notion pour une étape. Deux
 * dans la foulée seraient plus sûres, mais à ce rythme un enfant de CM1
 * passerait trois séances sur la même étape sans rien voir bouger — et c'est
 * exactement ce qu'il reprochait au jeu.
 */
export function reussitesParNiveau(
  notions: Array<{ id: string; items: Array<{ id: string; level: number }> }>,
  justes: Array<{ item_id: string }>,
): Map<number, Set<string>> {
  const repere = new Map<string, { notion: string; niveau: number }>();
  for (const n of notions) {
    for (const i of n.items) repere.set(i.id, { notion: n.id, niveau: i.level });
  }

  const sortie = new Map<number, Set<string>>();
  for (const e of justes) {
    const r = repere.get(e.item_id);
    if (!r) continue;
    if (!sortie.has(r.niveau)) sortie.set(r.niveau, new Set());
    sortie.get(r.niveau)!.add(r.notion);
  }
  return sortie;
}

/**
 * L'étape en cours : la première qui n'est pas entièrement validée.
 *
 * Une notion sans question à ce niveau ne bloque personne — elle est comptée
 * hors de l'étape. Une leçon importée peut très bien n'avoir que deux niveaux
 * sur trois ; elle doit rester jouable.
 */
export function etapeCourante(
  notions: NotionNiveaux[],
  reussiesParNiveau: Map<number, Set<string>>,
): { niveau: number; termine: boolean } {
  for (const palier of PALIERS) {
    const aFaire = concernees(notions, palier.niveau);
    if (aFaire.length === 0) continue;
    const ok = reussiesParNiveau.get(palier.niveau) ?? new Set<string>();
    if (aFaire.some((n) => !ok.has(n.id))) return { niveau: palier.niveau, termine: false };
  }
  // Tout est franchi : on reste sur la dernière étape pour les révisions.
  const dernier = [...PALIERS].reverse().find((p) => concernees(notions, p.niveau).length > 0);
  return { niveau: dernier?.niveau ?? 1, termine: true };
}

export async function construireSeance(childId: string, lessonId: string): Promise<Seance | null> {
  const { data, error } = await supabase
    .from('notions')
    .select(
      'id, lesson_id, kind, statement, sort_order, illustration, parent_id, status, created_at, ' +
        'items(id, notion_id, kind, level, payload, answer, explain, parent_id, status, created_at)',
    )
    .eq('lesson_id', lessonId)
    .eq('status', 'approved')
    .order('sort_order');
  if (error) throw error;

  const notions = ((data ?? []) as unknown as NotionAvecItems[]).map((n) => ({
    ...n,
    items: (n.items ?? []).filter((i) => i.status === 'approved'),
  }));
  if (notions.length === 0) return null;

  const idsItems = notions.flatMap((n) => n.items.map((i) => i.id));
  if (idsItems.length === 0) return null;

  const { data: essais, error: erreurEssais } = await supabase
    .from('attempts')
    .select('item_id, correct')
    .eq('child_id', childId)
    .in('item_id', idsItems);
  if (erreurEssais) throw erreurEssais;

  // Deux lectures du même journal : ce qui est validé, et ce qui a déjà été vu.
  const reussiesParNiveau = reussitesParNiveau(notions, (essais ?? []).filter((e) => e.correct));
  const vus = new Map<string, number>();
  for (const e of essais ?? []) vus.set(e.item_id, (vus.get(e.item_id) ?? 0) + 1);

  const { niveau, termine } = etapeCourante(notions, reussiesParNiveau);
  const palier = PALIERS.find((p) => p.niveau === niveau) ?? PALIERS[0];
  const aFaire = concernees(notions, niveau);
  const ok = reussiesParNiveau.get(niveau) ?? new Set<string>();

  // Une étape franchie : on repasse sur tout, pour entretenir.
  const restantes = termine ? aFaire : aFaire.filter((n) => !ok.has(n.id));

  const questions: Question[] = [];
  for (const notion of restantes.slice(0, TAILLE_SEANCE)) {
    const item = choisirQuestion(notion, niveau, vus);
    if (item) questions.push({ notion, item });
  }

  return {
    niveau,
    palier,
    termine,
    total: aFaire.length,
    reussies: termine ? aFaire.length : ok.size,
    questions,
    restantAprès: Math.max(0, restantes.length - questions.length),
  };
}
