import { toutLire } from './toutLire';
import { supabase } from './supabase';
import {
  decouperEnSeries,
  lireValidation,
  type Naissances,
  meilleurJustes as meilleurDesManches,
  questionsDeLaManche,
  TAILLE_REPRISE,
  type EtatValidation,
  type MancheRow,
} from './manche';
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

/**
 * L'étape qui fait gagner l'image de la notion.
 *
 * « Maîtrise » : l'enfant a reconnu, compris, puis écrit la notion. C'est le
 * moment juste — plus tôt l'image se donnerait sans effort, plus tard elle
 * arriverait après le chronomètre, qui joue la vitesse et non le savoir.
 *
 * Cette règle est volontairement la même que celle de l'escalier. L'image a
 * longtemps dépendu d'un autre compte, caché, qui demandait six bonnes
 * réponses sur la même notion : un enfant pouvait gravir les quatre étapes
 * d'une leçon et garder une collection vide.
 */
export const ETAPE_IMAGE = 3;

/**
 * L'étape à laquelle cette notion donne son image.
 *
 * Normalement la troisième. Mais une leçon importée peut n'avoir que deux
 * niveaux de questions : l'image se gagne alors à la plus haute étape qu'elle
 * porte, sinon elle resterait hors d'atteinte.
 */
export function etapeImage(notion: NotionNiveaux): number | null {
  const niveaux = notion.items.map((i) => i.level);
  if (niveaux.length === 0) return null;
  const jusqua = niveaux.filter((n) => n <= ETAPE_IMAGE);
  return jusqua.length > 0 ? Math.max(...jusqua) : Math.min(...niveaux);
}

/** L'image de cette notion est-elle gagnée, d'après le journal ? */
export function imageGagnee(
  notion: NotionNiveaux,
  reussiesParNiveau: Map<number, Set<string>>,
): boolean {
  const etape = etapeImage(notion);
  return etape !== null && (reussiesParNiveau.get(etape)?.has(notion.id) ?? false);
}

export type NotionAvecItems = NotionRow & { items: ItemRow[] };

export type Question = {
  notion: NotionAvecItems;
  item: ItemRow;
  /**
   * La question est servie une marche plus bas, pour reprendre appui.
   *
   * L'enfant a buté trois fois de suite sur cette notion à l'étape en cours.
   * On ne lui repose pas la même question une quatrième fois : on redescend
   * à une étape qu'il franchit, et on remontera après.
   */
  appui?: boolean;
};

/**
 * Ce que la séance demande à l'enfant.
 *
 *   etapes   l'escalier ordinaire, ou la révision d'une leçon validée
 *   reprise  les notions ratées à la dernière manche, et elles seules
 *   manche   toutes les questions de la leçon, pour la valider sans faute
 */
export type ModeSeance = 'etapes' | 'reprise' | 'manche';

export type Seance = {
  mode: ModeSeance;
  /** Où en est la validation de la leçon, d'après les manches jouées. */
  validation: EtatValidation;
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
  /**
   * Le meilleur nombre de bonnes réponses déjà obtenu sur cette leçon.
   *
   * Il sert à décider de la consolation d-une manche ratée de peu : elle
   * n-est versée que si le score progresse. Il est calculé ici parce que
   * les manches de la leçon sont déjà lues à cet endroit, et nulle part
   * ailleurs.
   */
  meilleurJustes: number;
  /**
   * Où en est la manche, série par série.
   *
   * `rang` est la série à jouer, `tenues` celles déjà acquises aujourd-hui.
   * Quand `tenues` vaut `total - 1`, la série en cours est la dernière : la
   * gagner valide la leçon, et l-écran le dit.
   */
  serie: { rang: number; total: number; tenues: number };
  /** Les notions de la série en cours : c-est ce que le journal doit porter. */
  notionsDeLaSerie: string[];
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
 * Les questions d'une reprise : les notions ratées, et elles seules.
 *
 * Un tour par notion avant d'en approfondir aucune. Donner d'abord cinq
 * questions sur les arêtes puis rien sur les sommets laisserait la moitié du
 * travail de côté — et c'est justement la moitié qu'il a ratée.
 *
 * À l'intérieur d'une notion, le plus difficile d'abord : l'enfant a déjà
 * gravi les quatre étapes, ce n'est pas la reconnaissance qui lui manque.
 */
export function questionsDeReprise(
  notions: NotionAvecItems[],
  vus: Map<string, number>,
  taille: number,
): Question[] {
  const files = notions.map((notion) => ({
    notion,
    items: [...notion.items].sort(
      (a, b) => b.level - a.level || (vus.get(a.id) ?? 0) - (vus.get(b.id) ?? 0),
    ),
  }));

  const questions: Question[] = [];
  for (let tour = 0; questions.length < taille; tour++) {
    if (!files.some((f) => f.items.length > tour)) break;
    for (const f of files) {
      if (questions.length >= taille) break;
      const item = f.items[tour];
      if (item) questions.push({ notion: f.notion, item });
    }
  }
  return questions;
}

/**
 * Une bonne réponse fait-elle avancer l'étape en cours ?
 *
 * Pas celle d'une question d'appui. L'appui est servi une marche plus bas,
 * pour que l'enfant reprenne pied ; il ne valide pas la marche du dessus.
 * Le journal le savait déjà — `reussitesParNiveau` range chaque bonne réponse
 * à SON niveau —, mais l'écran de la leçon, lui, comptait toute bonne réponse
 * comme une notion validée.
 *
 * Ce que l'enfant vivait : trois fautes sur une notion d'étape 2, la question
 * plus facile réussie, et l'écran annonçait « Étape réussie ! Tu passes en
 * Maîtrise », avec le coffre et cinquante étoiles. Puis « Étape suivante »
 * relisait le journal… et le remettait à l'étape 2, sur la même question. Le
 * père l'a décrit d'une phrase : ça ne traverse plus l'étape 2. KLEIN a fait
 * ce tour trois fois de suite sur la souris de l'ordinateur, BRAYNE cinq fois
 * sur les lampes.
 */
export function avanceLEtape(question: Pick<Question, 'appui'>, correct: boolean): boolean {
  return correct && !question.appui;
}

/** Au bout de trois échecs de suite sur une notion, on redescend d'une marche. */
export const ECHECS_AVANT_APPUI = 3;

/**
 * Les échecs consécutifs de chaque notion, à une étape donnée.
 *
 * Deux choses remettent le compteur à zéro : une bonne réponse **à cette
 * étape**, et une bonne réponse **à l’étape d’appui**.
 *
 * La seconde n’était pas là, et elle manquait gravement. L’appui sert une
 * question plus facile au bout de trois échecs — mais comme on ne servait
 * plus aucune question de l’étape en cours, plus aucun échec ni aucune
 * réussite ne pouvait s’y inscrire : le compteur restait figé au-dessus de
 * trois, l’appui durait pour toujours, et la notion ne pouvait plus jamais
 * être validée. KLEIN avait cinq notions dans cet état, dont deux bloquées à
 * l’étape 2 le jour même. L’escalier censé l’aider devenait un cul-de-sac.
 *
 * Avec la reprise d’appui, le cycle se referme : trois échecs, une marche
 * plus bas, et dès qu’il retrouve pied la question de l’étape revient — avec
 * trois essais neufs, et non un seul qui le renverrait aussitôt en bas.
 */
export function echecsDAffilee(
  notions: NotionAvecItems[],
  niveau: number,
  essais: Array<{ item_id: string; correct: boolean; created_at: string }>,
): Map<string, number> {
  const recents = [...essais].sort((a, b) => b.created_at.localeCompare(a.created_at));
  const sortie = new Map<string, number>();
  for (const notion of notions) {
    const siens = new Set(notion.items.filter((i) => i.level === niveau).map((i) => i.id));
    if (siens.size === 0) continue;
    const appui = niveauDAppui(notion, niveau);
    const ceuxDAppui = new Set(
      appui < niveau ? notion.items.filter((i) => i.level === appui).map((i) => i.id) : [],
    );
    let suite = 0;
    for (const e of recents) {
      if (ceuxDAppui.has(e.item_id) && e.correct) break;
      if (!siens.has(e.item_id)) continue;
      if (e.correct) break;
      suite += 1;
    }
    sortie.set(notion.id, suite);
  }
  return sortie;
}

/**
 * L'étape où reprendre appui : la plus haute en dessous de celle qui bloque.
 *
 * Reconnaître avant de produire. Un enfant qui échoue à écrire « sablonneux »
 * sait souvent le reconnaître parmi trois propositions — c'est là qu'il
 * retrouve pied, et une bonne réponse à l'étape basse ne valide pas pour
 * autant l'étape haute : chaque niveau garde son compte.
 */
export function niveauDAppui(notion: NotionNiveaux, niveau: number): number {
  const dessous = notion.items.map((i) => i.level).filter((n) => n < niveau);
  return dessous.length > 0 ? Math.max(...dessous) : niveau;
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

  const [essaisRes, manchesRes] = await Promise.all([
    toutLire<{ item_id: string; correct: boolean; created_at: string }>((de, a) =>
      supabase
        .from('attempts')
        .select('item_id, correct, created_at')
        .eq('child_id', childId)
        .in('item_id', idsItems)
        .order('created_at')
        .order('id')
        .range(de, a),
    ).then((data) => ({ data, error: null })),
    supabase
      .from('manches')
      .select('lesson_id, questions, justes, reussie, notions_ratees, created_at')
      .eq('child_id', childId)
      .eq('lesson_id', lessonId)
      .order('created_at', { ascending: false }),
  ]);
  if (essaisRes.error) throw essaisRes.error;
  if (manchesRes.error) throw manchesRes.error;
  const essais = essaisRes.data ?? [];

  // Trois lectures du même journal : ce qui est validé, ce qui a déjà été vu,
  // et les fautes datées — ce sont elles qui font perdre une validation.
  const reussiesParNiveau = reussitesParNiveau(notions, essais.filter((e) => e.correct));
  const vus = new Map<string, number>();
  for (const e of essais) vus.set(e.item_id, (vus.get(e.item_id) ?? 0) + 1);

  const notionDeItem = new Map<string, string>();
  for (const n of notions) for (const i of n.items) notionDeItem.set(i.id, n.id);
  const reponses = essais
    .map((e) => ({
      notion_id: notionDeItem.get(e.item_id) ?? '',
      correct: e.correct,
      created_at: e.created_at,
    }))
    .filter((r) => r.notion_id !== '');

  const manches = (manchesRes.data ?? []) as MancheRow[];
  // Le découpage se recalcule à chaque séance, et ne se stocke pas : une
  // notion ajoutée à la leçon doit entrer dans une série, pas rester dehors.
  const series = decouperEnSeries(notions);
  // La date d-entrée de chaque notion : une manche d-avant le découpage ne
  // couvre pas une notion ajoutée depuis.
  const naissances: Naissances = {};
  for (const n of notions) naissances[n.id] = n.created_at;
  const validation = lireValidation(
    series.map((s) => s.map((n) => n.id)),
    manches,
    reponses,
    naissances,
  );
  const meilleur = meilleurDesManches(manches, validation.notionsDeLaSerie);
  const rangSerie = {
    rang: validation.serieEnCours,
    total: validation.seriesTotal,
    tenues: validation.seriesTenues,
  };

  const { niveau, termine } = etapeCourante(notions, reussiesParNiveau);
  const palier = PALIERS.find((p) => p.niveau === niveau) ?? PALIERS[0];
  const aFaire = concernees(notions, niveau);
  const ok = reussiesParNiveau.get(niveau) ?? new Set<string>();

  // L'escalier gravi, la leçon n'est pas finie : il reste à la valider. Tant
  // qu'elle ne l'est pas, la séance sert la manche — ou, s'il a raté la
  // précédente, les notions fautives seules.
  const aReprendre = notions.filter((n) => validation.aReprendre.includes(n.id));
  const mode: ModeSeance =
    !termine || validation.validee ? 'etapes' : aReprendre.length > 0 ? 'reprise' : 'manche';

  if (mode === 'manche') {
    // Une seule série : celle qui n-est pas tenue. Rejouer les trente
    // questions de la leçon pour une faute sur les arêtes était justement ce
    // qui rendait la validation inatteignable.
    const aJouer = series[validation.serieEnCours - 1] ?? notions;
    const questions = questionsDeLaManche(aJouer);
    return {
      mode,
      validation,
      niveau,
      palier,
      termine,
      total: questions.length,
      reussies: 0,
      questions,
      restantAprès: 0,
      meilleurJustes: meilleur,
      serie: rangSerie,
      notionsDeLaSerie: aJouer.map((n) => n.id),
    };
  }

  if (mode === 'reprise') {
    const questions = questionsDeReprise(aReprendre, vus, TAILLE_REPRISE);
    return {
      mode,
      validation,
      niveau,
      palier,
      termine,
      total: aReprendre.length,
      reussies: 0,
      questions,
      restantAprès: 0,
      meilleurJustes: meilleur,
      serie: rangSerie,
      notionsDeLaSerie: validation.notionsDeLaSerie,
    };
  }

  // Une étape franchie : on repasse sur tout, pour entretenir.
  const restantes = termine ? aFaire : aFaire.filter((n) => !ok.has(n.id));

  const echecs = echecsDAffilee(notions, niveau, essais);

  const questions: Question[] = [];
  for (const notion of restantes.slice(0, TAILLE_SEANCE)) {
    // Trois échecs de suite : on arrête de reposer la même question. KLEIN a
    // reçu « sablonneux » cinq fois dans la journée, et son orthographe s'est
    // dégradée à chaque essai — il ne révisait plus, il se noyait.
    const bloque = (echecs.get(notion.id) ?? 0) >= ECHECS_AVANT_APPUI;
    const servi = bloque ? niveauDAppui(notion, niveau) : niveau;
    const item = choisirQuestion(notion, servi, vus);
    if (item) questions.push({ notion, item, appui: servi < niveau });
  }

  return {
    mode,
    validation,
    niveau,
    palier,
    termine,
    total: aFaire.length,
    reussies: termine ? aFaire.length : ok.size,
    questions,
    restantAprès: Math.max(0, restantes.length - questions.length),
    meilleurJustes: meilleur,
    serie: rangSerie,
    notionsDeLaSerie: validation.notionsDeLaSerie,
  };
}
