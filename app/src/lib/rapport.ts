import { toutLire } from './toutLire';
import { supabase } from './supabase';
import {
  decouperEnSeries,
  lireValidation,
  type MancheRow,
  type Naissances,
} from './manche';
import type { ItemKind, Json, NotionKind } from '../types/db';

/**
 * Le rapport de travail d'un enfant, pour son parent.
 *
 * Un parent ne regarde pas des pourcentages, il regarde son enfant. « 42 % en
 * géométrie » ne lui dit pas quoi faire le soir ; « il confond les arêtes et
 * les sommets » le lui dit. Tout ce fichier sert cette phrase-là.
 *
 * Quatre volets, dans cet ordre, parce que c'est l'ordre dans lequel on
 * comprend quelqu'un : comment il travaille, ce qu'il réussit, ce qui le met
 * en difficulté, et ce qu'il doit travailler beaucoup.
 *
 * Deux règles que le reste du fichier applique sans jamais y déroger :
 *
 *   Le rapport décrit le COMPORTEMENT DE TRAVAIL, jamais l'enfant. « Il
 *   s'arrête après huit minutes » est un fait utile. « Il manque de
 *   concentration » est un jugement que l'app n'a pas à porter, et qu'un
 *   parent lirait sur son fils plutôt que sur une séance.
 *
 *   Rien n'est deviné. Chaque chiffre vient du journal des tentatives, et une
 *   mesure qui n'a pas assez de matière pour être honnête n'est pas affichée
 *   du tout. Trois réponses ne font pas une tendance, et annoncer « il est
 *   faible en français » sur trois questions serait une calomnie calculée.
 *
 * Le rapport est calculé, pas rédigé par un modèle. Des phrases produites à
 * chaque consultation se liraient mieux, coûteraient à chaque ouverture, et
 * pourraient broder. Ici les faits sont bruts et la mise en phrase vit dans
 * l'écran, où elle se relit.
 */

/**
 * Reconnaître, ou produire.
 *
 * Deux QCM et un texte à trous ne demandent pas le même travail : dans l'un
 * la réponse est à l'écran, dans l'autre elle est dans la tête. Mélangés, ils
 * donnent une moyenne qui ment — un enfant à 97 % quand il choisit et à 33 %
 * quand il écrit s'affiche à 82 %, et personne ne voit le trou.
 */
const RECONNAITRE: ItemKind[] = ['qcm', 'vrai_faux'];

/** En deçà, un profil par type de notion n'a pas assez de matière. */
const ASSEZ_POUR_UN_PROFIL = 8;
/** Et chaque versant doit tenir debout tout seul pour qu'on les compare. */
const ASSEZ_PAR_VERSANT = 4;
/** Sous cet écart, reconnaître et produire se valent : rien à signaler. */
const ECART_NOTABLE = 0.25;

/** En deçà, une proportion ne veut rien dire : on ne l'affiche pas. */
const ASSEZ_POUR_UNE_MATIERE = 8;
const ASSEZ_POUR_UN_TYPE = 6;
/** Deux fautes sur une notion font une difficulté ; une seule fait un jour sans. */
const FAUTES_POUR_UNE_PRIORITE = 2;
/** Au-delà, ce n'est plus une priorité, c'est une liste. */
const PRIORITES_MAX = 4;
/** Deux réponses séparées de plus de vingt minutes sont deux séances. */
const COUPURE_SEANCE_MS = 20 * 60 * 1000;
/** Une séance de deux questions est une ouverture, pas un travail. */
const SEANCE_COURTE = 3;
/** Le Cameroun vit à UTC+1 : la journée d'un enfant se compte là-bas. */
const DECALAGE_DOUALA_H = 1;

export type Fenetre = 'semaine' | 'debut';

export type Priorite = {
  notionId: string;
  enonce: string;
  lecon: string;
  matiere: string | null;
  fautes: number;
  essais: number;
  /**
   * Ce qu'il répond quand il se trompe.
   *
   * `habituelle` sépare deux affirmations qui n'ont pas la même force : une
   * réponse donnée plusieurs fois est une habitude, une réponse unique n'est
   * qu'un exemple. Les confondre ferait dire au rapport « il répond toujours
   * X » sur une seule occurrence.
   */
  erreur: { texte: string; habituelle: boolean } | null;
};

export type Part = { label: string; part: number; essais: number };

/**
 * Ce que l'enfant fait d'une famille de notions : dates, définitions, listes,
 * relations.
 *
 * C'est l'axe qui manquait, et c'est pourtant celui dans lequel un parent
 * pense — « il rate les dates », pas « il rate 42 % des questions de niveau
 * 3 ». Il manquait parce que le rapport ne regardait que les matières et les
 * formes de questions ; une faiblesse étalée sur dix notions de dates, une
 * erreur chacune, ne ressortait nulle part.
 */
export type ProfilNotion = {
  kind: NotionKind;
  essais: number;
  part: number;
  /** Quand la réponse est à l'écran : QCM, vrai ou faux. */
  reconnaitre: { part: number; essais: number } | null;
  /** Quand il doit la sortir de sa tête : écrire, dicter, remettre en ordre. */
  produire: { part: number; essais: number } | null;
  /** L'écart entre les deux, quand il est assez grand pour être dit. */
  ecart: number | null;
  /**
   * Ce qu'il écrit à la place, quand la même réponse revient sur plusieurs
   * notions de la famille.
   *
   * C'est le fait le plus utile du rapport entier : une date fausse répétée
   * trois fois sur trois questions différentes n'est pas une étourderie,
   * c'est un repère faux qui s'est installé.
   */
  erreurRecurrente: { texte: string; fois: number } | null;
};

export type Rapport = {
  prenom: string;
  fenetre: Fenetre;
  /** Aucune réponse dans la fenêtre : il n'y a rien à raconter. */
  vide: boolean;

  // ── Comment il travaille ────────────────────────────────────────────────
  questions: number;
  seances: number;
  minutes: number;
  questionsParSeance: number;
  secondesParQuestion: number | null;
  heureHabituelle: number | null;
  joursJoues: number;
  joursPossibles: number;
  seancesCourtes: number;

  // ── Ce qu'il réussit ────────────────────────────────────────────────────
  justes: number;
  duPremierCoup: number;
  questionsVues: number;
  leconsValidees: number;
  matiereForte: Part | null;

  // ── Ce qui le met en difficulté ─────────────────────────────────────────
  matiereFaible: Part | null;
  typeFaible: (Part & { kind: ItemKind }) | null;
  /** Dates, définitions, listes, relations : de la plus fragile à la plus sûre. */
  profils: ProfilNotion[];
  manchesRatees: number;

  // ── Ce qu'il doit beaucoup travailler ───────────────────────────────────
  aTravailler: Priorite[];
};

/** Le jour, à Douala. Une leçon jouée à 23 h appartient à ce jour-là. */
function jourLocal(iso: string): string {
  const d = new Date(iso);
  d.setUTCHours(d.getUTCHours() + DECALAGE_DOUALA_H);
  return d.toISOString().slice(0, 10);
}

function heureLocale(iso: string): number {
  const d = new Date(iso);
  return (d.getUTCHours() + DECALAGE_DOUALA_H) % 24;
}

function mediane(valeurs: number[]): number | null {
  if (valeurs.length === 0) return null;
  const t = [...valeurs].sort((a, b) => a - b);
  const m = Math.floor(t.length / 2);
  return t.length % 2 ? t[m] : (t[m - 1] + t[m]) / 2;
}

/**
 * Ce qu'il a répondu, dit en clair.
 *
 * C'est le cœur du dernier volet. « Il se trompe sur les arêtes » laisse le
 * parent démuni ; « il répond huit arêtes » lui donne la phrase à dire au
 * dîner. Quand la forme de la question ne permet pas de le nommer proprement,
 * on ne dit rien plutôt que d'inventer.
 */
export function direLaReponse(kind: ItemKind, payload: Json, answer: Json): string | null {
  const p = payload as Record<string, unknown>;
  const a = answer as Record<string, unknown>;
  if (kind === 'qcm') {
    const options = p.options as string[] | undefined;
    const i = a.index as number | undefined;
    return options && typeof i === 'number' && options[i] ? options[i] : null;
  }
  if (kind === 'vrai_faux') {
    if (typeof a.value !== 'boolean') return null;
    return a.value ? 'Vrai' : 'Faux';
  }
  if (kind === 'texte_a_trous') {
    const v = a.values as string[] | undefined;
    const ecrit = (v ?? []).filter((x) => typeof x === 'string' && x.trim() !== '');
    return ecrit.length ? ecrit.join(', ') : null;
  }
  if (kind === 'dictee') {
    const phrase = a.phrase as string | undefined;
    return phrase && phrase.trim() !== '' ? phrase : null;
  }
  // Relier et remettre en ordre se répondent par des positions : les écrire
  // donnerait « 2, 0, 1 », qui n'apprend rien à personne.
  return null;
}

/**
 * Ce qu'il répond quand il se trompe : son habitude, ou à défaut son dernier
 * essai.
 *
 * Les deux servent le parent, mais ils ne disent pas la même chose. Une
 * réponse revenue trois fois est une erreur installée, qu'on peut corriger
 * d'une phrase. Une réponse unique n'est qu'un exemple — et pour une dictée,
 * où aucune faute ne se répète jamais à l'identique, c'est le seul exemple
 * qu'on aura. Le taire reviendrait à ne rien dire des dictées.
 */
function erreurDominante(reponses: string[]): { texte: string; habituelle: boolean } | null {
  if (reponses.length === 0) return null;
  const compte = new Map<string, number>();
  for (const r of reponses) compte.set(r, (compte.get(r) ?? 0) + 1);
  const classe = [...compte.entries()].sort((a, b) => b[1] - a[1]);
  if (classe[0][1] >= 2) return { texte: classe[0][0], habituelle: true };
  return { texte: reponses[reponses.length - 1], habituelle: false };
}

type Essai = {
  item_id: string;
  correct: boolean;
  duration_ms: number | null;
  created_at: string;
  answer: Json;
};

type Repere = {
  kind: ItemKind;
  notionKind: NotionKind;
  payload: Json;
  notionId: string;
  enonce: string;
  lecon: string;
  matiere: string | null;
};

/**
 * Le profil de chaque famille de notions : dates, définitions, listes,
 * relations.
 *
 * On y sépare reconnaître de produire, parce que c'est là que se cache ce
 * qu'une moyenne noie. Et on y cherche la réponse fausse qui revient d'une
 * notion à l'autre : trois dates différentes auxquelles l'enfant répond la
 * même année, ce n'est pas trois étourderies, c'est un repère faux installé.
 */
function profilsParNotion(essais: Essai[], reperes: Map<string, Repere>): ProfilNotion[] {
  const familles = new Map<
    NotionKind,
    { bons: number; total: number; rBons: number; rTotal: number; pBons: number; pTotal: number; ecrites: string[] }
  >();

  for (const e of essais) {
    const r = reperes.get(e.item_id);
    if (!r) continue;
    const f = familles.get(r.notionKind) ?? {
      bons: 0, total: 0, rBons: 0, rTotal: 0, pBons: 0, pTotal: 0, ecrites: [],
    };
    f.total += 1;
    if (e.correct) f.bons += 1;
    if (RECONNAITRE.includes(r.kind)) {
      f.rTotal += 1;
      if (e.correct) f.rBons += 1;
    } else {
      f.pTotal += 1;
      if (e.correct) f.pBons += 1;
      if (!e.correct) {
        const dite = direLaReponse(r.kind, r.payload, e.answer);
        // On ne garde que ce qu'il a vraiment écrit : une position dans une
        // liste ne se répète pas d'une notion à l'autre.
        if (dite) for (const bout of dite.split(',')) {
          const net = bout.trim();
          if (net) f.ecrites.push(net);
        }
      }
    }
    familles.set(r.notionKind, f);
  }

  const profils: ProfilNotion[] = [];
  for (const [kind, f] of familles) {
    if (f.total < ASSEZ_POUR_UN_PROFIL) continue;
    const reconnaitre = f.rTotal >= ASSEZ_PAR_VERSANT
      ? { part: f.rBons / f.rTotal, essais: f.rTotal } : null;
    const produire = f.pTotal >= ASSEZ_PAR_VERSANT
      ? { part: f.pBons / f.pTotal, essais: f.pTotal } : null;
    const brut = reconnaitre && produire ? reconnaitre.part - produire.part : null;
    const compte = new Map<string, number>();
    for (const x of f.ecrites) compte.set(x, (compte.get(x) ?? 0) + 1);
    const repetee = [...compte.entries()].sort((a, b) => b[1] - a[1])[0];
    profils.push({
      kind,
      essais: f.total,
      part: f.bons / f.total,
      reconnaitre,
      produire,
      ecart: brut !== null && brut >= ECART_NOTABLE ? brut : null,
      // Deux fois ne suffit pas : c'est la troisième qui fait le repère faux.
      erreurRecurrente: repetee && repetee[1] >= 3 ? { texte: repetee[0], fois: repetee[1] } : null,
    });
  }
  return profils.sort((a, b) => a.part - b.part);
}

/** Les proportions de réussite par étiquette, celles qui ont assez de matière. */
function parts(
  essais: Essai[],
  etiquette: (e: Essai) => string | null,
  minimum: number,
): { meilleure: Part | null; pire: Part | null } {
  const compte = new Map<string, { bons: number; total: number }>();
  for (const e of essais) {
    const cle = etiquette(e);
    if (!cle) continue;
    const c = compte.get(cle) ?? { bons: 0, total: 0 };
    c.total += 1;
    if (e.correct) c.bons += 1;
    compte.set(cle, c);
  }
  const retenues: Part[] = [...compte.entries()]
    .filter(([, c]) => c.total >= minimum)
    .map(([label, c]) => ({ label, part: c.bons / c.total, essais: c.total }))
    .sort((a, b) => b.part - a.part);
  if (retenues.length === 0) return { meilleure: null, pire: null };
  // Une seule matière ne peut pas être à la fois la plus forte et la plus
  // faible : affirmer les deux sur le même mot ne dit rien.
  if (retenues.length === 1) return { meilleure: retenues[0], pire: null };
  return { meilleure: retenues[0], pire: retenues[retenues.length - 1] };
}

export function construireRapport(
  prenom: string,
  fenetre: Fenetre,
  essais: Essai[],
  reperes: Map<string, Repere>,
  manches: Array<{ reussie: boolean; created_at: string }>,
  premiereReponsePar: Map<string, boolean>,
  leconsValidees: number,
): Rapport {
  const vide = essais.length === 0;

  // ── Les séances : des réponses qui se suivent de près ───────────────────
  const tries = [...essais].sort((a, b) => a.created_at.localeCompare(b.created_at));
  const seances: Essai[][] = [];
  for (const e of tries) {
    const courante = seances[seances.length - 1];
    const precedent = courante?.[courante.length - 1];
    if (
      !precedent ||
      new Date(e.created_at).getTime() - new Date(precedent.created_at).getTime() >
        COUPURE_SEANCE_MS
    ) {
      seances.push([e]);
    } else {
      courante.push(e);
    }
  }

  const minutes = seances.reduce((total, s) => {
    const debut = new Date(s[0].created_at).getTime();
    const fin = new Date(s[s.length - 1].created_at).getTime();
    // Une séance d'une seule question dure au moins le temps de la lire.
    return total + Math.max(fin - debut, 20_000);
  }, 0) / 60_000;

  const durees = essais
    .map((e) => e.duration_ms)
    .filter((d): d is number => typeof d === 'number' && d > 500 && d < 180_000);

  const heures = new Map<number, number>();
  for (const e of essais) {
    const h = heureLocale(e.created_at);
    heures.set(h, (heures.get(h) ?? 0) + 1);
  }
  const heureHabituelle =
    heures.size === 0
      ? null
      : [...heures.entries()].sort((a, b) => b[1] - a[1] || a[0] - b[0])[0][0];

  const jours = new Set(essais.map((e) => jourLocal(e.created_at)));
  const joursPossibles =
    fenetre === 'semaine'
      ? 7
      : Math.max(
          1,
          Math.round(
            (Date.now() - new Date(tries[0]?.created_at ?? Date.now()).getTime()) / 86_400_000,
          ) + 1,
        );

  // ── Ce qu'il réussit ────────────────────────────────────────────────────
  const vues = new Set(essais.map((e) => e.item_id));
  const duPremierCoup = [...vues].filter((id) => premiereReponsePar.get(id) === true).length;

  const matieres = parts(essais, (e) => reperes.get(e.item_id)?.matiere ?? null, ASSEZ_POUR_UNE_MATIERE);
  const types = parts(essais, (e) => reperes.get(e.item_id)?.kind ?? null, ASSEZ_POUR_UN_TYPE);

  // ── Ce qu'il doit beaucoup travailler ───────────────────────────────────
  // Les réponses sont parcourues dans l'ordre du temps : `dernieres` garde les
  // deux plus récentes de chaque notion.
  const parNotion = new Map<
    string,
    { fautes: number; essais: number; mauvaises: string[]; dernieres: boolean[] }
  >();
  for (const e of tries) {
    const r = reperes.get(e.item_id);
    if (!r) continue;
    const c = parNotion.get(r.notionId) ?? { fautes: 0, essais: 0, mauvaises: [], dernieres: [] };
    c.essais += 1;
    c.dernieres = [...c.dernieres, e.correct].slice(-2);
    if (!e.correct) {
      c.fautes += 1;
      const dite = direLaReponse(r.kind, r.payload, e.answer);
      if (dite) c.mauvaises.push(dite);
    }
    parNotion.set(r.notionId, c);
  }

  // Une notion RATTRAPÉE n'est plus à travailler : ratée trois fois au début,
  // réussie les deux dernières, l'enfant l'a apprise — c'est même ce que ses
  // étapes affichent. La garder ici faisait dire au rapport le contraire de
  // ce que montre l'espace de l'enfant.
  const aTravailler: Priorite[] = [...parNotion.entries()]
    .filter(([, c]) => c.fautes >= FAUTES_POUR_UNE_PRIORITE)
    .filter(([, c]) => !(c.dernieres.length === 2 && c.dernieres.every(Boolean)))
    .sort((a, b) => b[1].fautes - a[1].fautes || b[1].essais - a[1].essais)
    .slice(0, PRIORITES_MAX)
    .map(([notionId, c]) => {
      const r = [...reperes.values()].find((x) => x.notionId === notionId);
      return {
        notionId,
        enonce: r?.enonce ?? 'Notion',
        lecon: r?.lecon ?? '',
        matiere: r?.matiere ?? null,
        fautes: c.fautes,
        essais: c.essais,
        erreur: erreurDominante(c.mauvaises),
      };
    });

  return {
    prenom,
    fenetre,
    vide,
    questions: essais.length,
    seances: seances.length,
    minutes: Math.round(minutes),
    questionsParSeance: seances.length ? Math.round(essais.length / seances.length) : 0,
    secondesParQuestion: durees.length >= 5 ? Math.round((mediane(durees) ?? 0) / 1000) : null,
    heureHabituelle,
    joursJoues: jours.size,
    joursPossibles,
    seancesCourtes: seances.filter((s) => s.length < SEANCE_COURTE).length,
    justes: essais.filter((e) => e.correct).length,
    duPremierCoup,
    questionsVues: vues.size,
    leconsValidees,
    matiereForte: matieres.meilleure,
    matiereFaible: matieres.pire,
    typeFaible: types.pire ? { ...types.pire, kind: types.pire.label as ItemKind } : null,
    profils: profilsParNotion(essais, reperes),
    manchesRatees: manches.filter((m) => !m.reussie).length,
    aTravailler,
  };
}

/**
 * Les deux rapports d'un enfant : la semaine écoulée, et depuis le début.
 *
 * Une difficulté qui dure n'a pas le même sens qu'une mauvaise soirée, et un
 * parent a besoin des deux pour faire la différence.
 */
export async function chargerRapports(
  childId: string,
): Promise<{ semaine: Rapport; debut: Rapport }> {
  const { data: enfant, error: erreurEnfant } = await supabase
    .from('children')
    .select('first_name')
    .eq('id', childId)
    .single();
  if (erreurEnfant) throw erreurEnfant;
  const prenom = (enfant as { first_name: string }).first_name;

  // Toutes les réponses, page après page. Lues d'un coup, elles s'arrêtaient
  // aux mille plus ANCIENNES : passé ce seuil, le rapport ne voyait plus rien
  // de la semaine en cours.
  const essais = await toutLire<Essai>((de, a) =>
    supabase
      .from('attempts')
      .select('item_id, correct, duration_ms, created_at, answer')
      .eq('child_id', childId)
      .order('created_at')
      .order('id')
      .range(de, a),
  );

  const { data: manchesBrutes, error: erreurManches } = await supabase
    .from('manches')
    .select('lesson_id, questions, justes, reussie, notions_ratees, notions, created_at')
    .eq('child_id', childId)
    .order('created_at', { ascending: false });
  if (erreurManches) throw erreurManches;
  const manches = (manchesBrutes ?? []) as MancheRow[];

  // Les repères des seules questions touchées : inutile de charger le
  // catalogue entier pour raconter ce qu'un enfant a joué.
  const ids = [...new Set(essais.map((e) => e.item_id))];
  const reperes = new Map<string, Repere>();
  for (let i = 0; i < ids.length; i += 200) {
    const tranche = ids.slice(i, i + 200);
    const { data, error } = await supabase
      .from('items')
      .select(
        'id, kind, payload, notion_id, ' +
          'notions(id, kind, statement, lessons(title, subjects(label)))',
      )
      .in('id', tranche);
    if (error) throw error;
    for (const brut of (data ?? []) as unknown as Array<{
      id: string;
      kind: ItemKind;
      payload: Json;
      notion_id: string;
      notions: {
        kind: NotionKind;
        statement: string;
        lessons: { title: string; subjects: { label: string } | null } | null;
      } | null;
    }>) {
      reperes.set(brut.id, {
        kind: brut.kind,
        notionKind: brut.notions?.kind ?? 'definition',
        payload: brut.payload,
        notionId: brut.notion_id,
        enonce: brut.notions?.statement ?? 'Notion',
        lecon: brut.notions?.lessons?.title ?? '',
        matiere: brut.notions?.lessons?.subjects?.label ?? null,
      });
    }
  }

  // La toute première réponse à chaque question : c'est elle qui dit « du
  // premier coup », et elle ne dépend pas de la fenêtre qu'on regarde.
  const premiereReponsePar = new Map<string, boolean>();
  for (const e of essais) {
    if (!premiereReponsePar.has(e.item_id)) premiereReponsePar.set(e.item_id, e.correct);
  }

  // Une leçon validée : TOUTES ses séries tenues. Une série réussie sur trois
  // n'est pas une leçon sue, et c'est le genre de phrase qu'un rapport ne doit
  // pas prononcer à tort — le parent la lit comme un certificat.
  //
  // La règle n'est pas recopiée ici : c'est lireValidation, la même fonction
  // que la salle de jeu et le tableau de bord. Il lui faut le découpage en
  // séries, donc les notions des leçons qui ont une manche — et elles seules,
  // pas le catalogue entier.
  const leconsValidees = new Set<string>();
  const avecManche = [...new Set(manches.map((m) => m.lesson_id))];
  if (avecManche.length > 0) {
    const { data, error } = await supabase
      .from('notions')
      .select('id, lesson_id, status, sort_order, created_at, items(id, status)')
      .in('lesson_id', avecManche)
      .eq('status', 'approved')
      .order('sort_order');
    if (error) throw error;

    const parLecon = new Map<string, Array<{ id: string; items: unknown[] }>>();
    const notionDeItem = new Map<string, string>();
    // La date d-entrée de chaque notion : une manche d-avant le découpage ne
    // couvre pas une notion ajoutée depuis.
    const naissances: Naissances = {};
    for (const brut of (data ?? []) as unknown as Array<{
      id: string;
      lesson_id: string;
      created_at: string;
      items: Array<{ id: string; status: string }> | null;
    }>) {
      const items = (brut.items ?? []).filter((i) => i.status === 'approved');
      for (const i of items) notionDeItem.set(i.id, brut.id);
      naissances[brut.id] = brut.created_at;
      const liste = parLecon.get(brut.lesson_id) ?? [];
      liste.push({ id: brut.id, items });
      parLecon.set(brut.lesson_id, liste);
    }

    for (const [lecon, notions] of parLecon) {
      const siennes = new Set(notions.map((n) => n.id));
      const reponses = essais
        .map((e) => ({
          notion_id: notionDeItem.get(e.item_id) ?? '',
          correct: e.correct,
          created_at: e.created_at,
        }))
        .filter((r) => siennes.has(r.notion_id));
      const etat = lireValidation(
        decouperEnSeries(notions).map((serie) => serie.map((n) => n.id)),
        manches.filter((m) => m.lesson_id === lecon),
        reponses,
        naissances,
      );
      if (etat.validee) leconsValidees.add(lecon);
    }
  }

  const limite = new Date(Date.now() - 7 * 86_400_000).toISOString();
  const fabrique = (fenetre: Fenetre) => {
    const dedans = fenetre === 'semaine' ? essais.filter((e) => e.created_at >= limite) : essais;
    const sesManches =
      fenetre === 'semaine' ? manches.filter((m) => m.created_at >= limite) : manches;
    return construireRapport(
      prenom,
      fenetre,
      dedans,
      reperes,
      sesManches,
      premiereReponsePar,
      leconsValidees.size,
    );
  };

  return { semaine: fabrique('semaine'), debut: fabrique('debut') };
}
