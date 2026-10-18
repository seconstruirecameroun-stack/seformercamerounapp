import { supabase } from './supabase';
import type { ItemKind, Json } from '../types/db';

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
  payload: Json;
  notionId: string;
  enonce: string;
  lecon: string;
  matiere: string | null;
};

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
  const parNotion = new Map<string, { fautes: number; essais: number; mauvaises: string[] }>();
  for (const e of essais) {
    const r = reperes.get(e.item_id);
    if (!r) continue;
    const c = parNotion.get(r.notionId) ?? { fautes: 0, essais: 0, mauvaises: [] };
    c.essais += 1;
    if (!e.correct) {
      c.fautes += 1;
      const dite = direLaReponse(r.kind, r.payload, e.answer);
      if (dite) c.mauvaises.push(dite);
    }
    parNotion.set(r.notionId, c);
  }

  const aTravailler: Priorite[] = [...parNotion.entries()]
    .filter(([, c]) => c.fautes >= FAUTES_POUR_UNE_PRIORITE)
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

  const { data: essaisBruts, error: erreurEssais } = await supabase
    .from('attempts')
    .select('item_id, correct, duration_ms, created_at, answer')
    .eq('child_id', childId)
    .order('created_at');
  if (erreurEssais) throw erreurEssais;
  const essais = (essaisBruts ?? []) as Essai[];

  const { data: manchesBrutes, error: erreurManches } = await supabase
    .from('manches')
    .select('lesson_id, questions, justes, reussie, notions_ratees, created_at')
    .eq('child_id', childId)
    .order('created_at', { ascending: false });
  if (erreurManches) throw erreurManches;
  const manches = (manchesBrutes ?? []) as Array<{
    lesson_id: string;
    reussie: boolean;
    created_at: string;
  }>;

  // Les repères des seules questions touchées : inutile de charger le
  // catalogue entier pour raconter ce qu'un enfant a joué.
  const ids = [...new Set(essais.map((e) => e.item_id))];
  const reperes = new Map<string, Repere>();
  for (let i = 0; i < ids.length; i += 200) {
    const tranche = ids.slice(i, i + 200);
    const { data, error } = await supabase
      .from('items')
      .select(
        'id, kind, payload, notion_id, notions(id, statement, lessons(title, subjects(label)))',
      )
      .in('id', tranche);
    if (error) throw error;
    for (const brut of (data ?? []) as unknown as Array<{
      id: string;
      kind: ItemKind;
      payload: Json;
      notion_id: string;
      notions: {
        statement: string;
        lessons: { title: string; subjects: { label: string } | null } | null;
      } | null;
    }>) {
      reperes.set(brut.id, {
        kind: brut.kind,
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

  // Une leçon validée : une manche réussie, et aucune faute depuis. La règle
  // complète vit dans lib/manche.ts ; ici on ne compte que les leçons.
  const leconsValidees = new Set<string>();
  for (const m of manches) {
    if (!m.reussie || leconsValidees.has(m.lesson_id)) continue;
    const fauteDepuis = essais.some(
      (e) => !e.correct && e.created_at > m.created_at && reperes.has(e.item_id),
    );
    if (!fauteDepuis) leconsValidees.add(m.lesson_id);
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
