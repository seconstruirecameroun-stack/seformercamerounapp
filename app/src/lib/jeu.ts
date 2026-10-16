/**
 * Ce qui donne envie de revenir demain.
 *
 * Un enfant de sept ans ne revient pas pour réviser. Il revient pour une
 * série qu'il ne veut pas casser, un objectif à quelques étoiles près, un
 * coffre qu'il n'a pas encore ouvert. Tout ce fichier sert à ça, et à rien
 * d'autre : transformer le travail déjà fait en raisons d'y retourner.
 *
 * Règle du projet tenue ici aussi : rien n'est stocké. La série, l'objectif,
 * les quêtes et les trophées se déduisent du journal des tentatives et des
 * récompenses. Aucune colonne à tenir à jour, donc aucun compteur qui puisse
 * mentir sur ce que l'enfant a réellement fait.
 */

/**
 * L'objectif du jour, en étoiles.
 *
 * Calibré sur une dizaine de questions : assez pour que la journée compte,
 * assez peu pour qu'un soir chargé n'y suffise pas de justesse. Un objectif
 * qu'on atteint sans s'en apercevoir ne retient personne ; un objectif qu'on
 * rate trois soirs de suite non plus.
 */
import type { NomIcone } from '../components/jeu/Icone';

export const OBJECTIF_JOUR = 100;

/** Ce qu'on sait d'une question jouée, sans charger son énoncé. */
export type RepereItem = {
  niveau: number;
  notionId: string;
  matiereId: string | null;
  leconId: string;
};

export type Tentative = { itemId: string; correct: boolean; jour: string; a: string };

export type Gain = { value: number; jour: string };

// ───────────────────────── la série ─────────────────────────

export type Serie = {
  jours: number;
  /** La série tient aujourd'hui, ou elle attend d'être nourrie. */
  joueAujourdhui: boolean;
  /** Un jour manqué a été pardonné : on le dit, ça vaut un avertissement. */
  pardonUtilise: boolean;
  /** Le prochain palier qui déclenche une fête. */
  prochainPalier: number | null;
};

export const PALIERS_SERIE = [3, 7, 14, 30, 100];

function jourDecale(decalage: number): string {
  const d = new Date();
  d.setDate(d.getDate() - decalage);
  return d.toISOString().slice(0, 10);
}

/**
 * La série, avec un jour de pardon.
 *
 * Une série qui tombe à zéro pour un dimanche de baptême ne motive plus
 * personne : l'enfant qui vient de perdre trente jours n'a plus de raison de
 * revenir lundi. On autorise donc un seul trou, et seulement si la série
 * valait déjà la peine d'être sauvée — trois jours au moins. Le trou est
 * annoncé à l'enfant : le pardon n'est pas une permission.
 */
export function calculerSerie(jours: string[]): Serie {
  const vus = new Set(jours);
  const joueAujourdhui = vus.has(jourDecale(0));

  // Une série reste vivante jusqu'à la fin de la journée du lendemain : à
  // 7 h du matin, l'enfant n'a pas encore « cassé » quoi que ce soit.
  let i = joueAujourdhui ? 0 : vus.has(jourDecale(1)) ? 1 : -1;
  if (i === -1) return { jours: 0, joueAujourdhui, pardonUtilise: false, prochainPalier: PALIERS_SERIE[0] };

  let compte = 0;
  let pardonUtilise = false;
  for (;;) {
    if (vus.has(jourDecale(i))) {
      compte += 1;
      i += 1;
      continue;
    }
    // Le trou n'est pardonné qu'une fois, et qu'au-delà de trois jours tenus.
    if (!pardonUtilise && compte >= 3 && vus.has(jourDecale(i + 1))) {
      pardonUtilise = true;
      i += 1;
      continue;
    }
    break;
  }

  return {
    jours: compte,
    joueAujourdhui,
    pardonUtilise,
    prochainPalier: PALIERS_SERIE.find((p) => p > compte) ?? null,
  };
}

// ───────────────────────── les rangs ─────────────────────────

export type Rang = {
  nom: string;
  seuil: number;
  /** La clé de l'emblème dans la banque d'illustrations. */
  embleme: string;
};

/**
 * Les rangs portent le lion : au Cameroun, un enfant sait ce qu'est un Lion
 * indomptable avant de savoir lire. Le dernier rang se mérite sur une année
 * scolaire entière — une échelle qu'on épuise en un mois ne tire plus rien.
 */
export const RANGS: Rang[] = [
  { nom: 'Lionceau', seuil: 0, embleme: 'rang-lionceau' },
  { nom: 'Petite griffe', seuil: 250, embleme: 'rang-griffe' },
  { nom: 'Griffe d’or', seuil: 750, embleme: 'rang-griffe-or' },
  { nom: 'Jeune crinière', seuil: 1800, embleme: 'rang-criniere' },
  { nom: 'Grande crinière', seuil: 3500, embleme: 'rang-grande-criniere' },
  { nom: 'Lion indomptable', seuil: 7000, embleme: 'rang-indomptable' },
];

export type EtatRang = {
  rang: Rang;
  suivant: Rang | null;
  /** Part du chemin parcouru vers le rang suivant, de 0 à 1. */
  part: number;
  /** Étoiles restantes avant le rang suivant. */
  reste: number;
};

export function etatRang(etoiles: number): EtatRang {
  let index = 0;
  for (let i = 0; i < RANGS.length; i++) if (etoiles >= RANGS[i].seuil) index = i;
  const rang = RANGS[index];
  const suivant = RANGS[index + 1] ?? null;
  if (!suivant) return { rang, suivant: null, part: 1, reste: 0 };
  const part = (etoiles - rang.seuil) / (suivant.seuil - rang.seuil);
  return { rang, suivant, part: Math.min(1, Math.max(0, part)), reste: suivant.seuil - etoiles };
}

// ───────────────────────── l'objectif du jour ─────────────────────────

export type Objectif = { gagnees: number; cible: number; part: number; atteint: boolean };

export function objectifDuJour(gains: Gain[], cible = OBJECTIF_JOUR): Objectif {
  const aujourdhui = jourDecale(0);
  const gagnees = gains.filter((g) => g.jour === aujourdhui).reduce((s, g) => s + g.value, 0);
  return {
    gagnees,
    cible,
    part: Math.min(1, gagnees / cible),
    atteint: gagnees >= cible,
  };
}

// ───────────────────────── les quêtes du jour ─────────────────────────

export type Quete = {
  id: string;
  texte: string;
  icone: NomIcone;
  fait: number;
  cible: number;
};

type Mesure = (ctx: ContexteJour) => number;

type ContexteJour = {
  /** Les tentatives d'aujourd'hui, dans l'ordre où elles ont été jouées. */
  duJour: Tentative[];
  repere: Map<string, RepereItem>;
  /** Notions dont l'image a été gagnée aujourd'hui. */
  imagesDuJour: number;
  etoilesDuJour: number;
};

const CATALOGUE: Array<{
  id: string;
  texte: string;
  icone: NomIcone;
  cible: number;
  mesure: Mesure;
}> = [
  {
    id: 'reussir',
    texte: 'Réussis 12 questions',
    icone: 'coche',
    cible: 12,
    mesure: (c) => c.duJour.filter((t) => t.correct).length,
  },
  {
    id: 'image',
    texte: 'Gagne une image',
    icone: 'image',
    cible: 1,
    mesure: (c) => c.imagesDuJour,
  },
  {
    id: 'affilee',
    texte: 'Réussis 5 questions d’affilée',
    icone: 'eclair',
    cible: 5,
    mesure: (c) => {
      let max = 0;
      let suite = 0;
      for (const t of c.duJour) {
        suite = t.correct ? suite + 1 : 0;
        if (suite > max) max = suite;
      }
      return max;
    },
  },
  {
    id: 'matieres',
    texte: 'Joue dans 2 matières',
    icone: 'livres',
    cible: 2,
    mesure: (c) =>
      new Set(
        c.duJour
          .map((t) => c.repere.get(t.itemId)?.matiereId)
          .filter((m): m is string => Boolean(m)),
      ).size,
  },
  {
    id: 'etoiles',
    texte: 'Gagne 60 étoiles',
    icone: 'etoile',
    cible: 60,
    mesure: (c) => c.etoilesDuJour,
  },
  {
    id: 'defi',
    texte: 'Réussis 3 questions du Défi',
    icone: 'chrono',
    cible: 3,
    mesure: (c) =>
      c.duJour.filter((t) => t.correct && c.repere.get(t.itemId)?.niveau === 4).length,
  },
];

/**
 * Trois quêtes par jour, tirées de la date.
 *
 * Tirer au hasard à chaque chargement donnerait des quêtes qui changent sous
 * les yeux de l'enfant ; les figer une fois pour toutes les rendrait vite
 * lassantes. La date sert donc de graine : les mêmes trois quêtes toute la
 * journée, d'autres demain, et les mêmes sur le téléphone du parent.
 */
export function quetesDuJour(ctx: ContexteJour, aujourdhui = jourDecale(0)): Quete[] {
  const graine = [...aujourdhui].reduce((n, c) => n + c.charCodeAt(0), 0);
  const choisies: typeof CATALOGUE = [];
  for (let i = 0; choisies.length < 3 && i < CATALOGUE.length; i++) {
    const q = CATALOGUE[(graine + i * 2 + 1) % CATALOGUE.length];
    if (!choisies.includes(q)) choisies.push(q);
  }
  return choisies.map((q) => ({
    id: q.id,
    texte: q.texte,
    icone: q.icone,
    cible: q.cible,
    fait: Math.min(q.cible, q.mesure(ctx)),
  }));
}

export function construireContexte(
  tentatives: Tentative[],
  repere: Map<string, RepereItem>,
  gains: Gain[],
  imagesDuJour: number,
): ContexteJour {
  const aujourdhui = jourDecale(0);
  return {
    duJour: tentatives.filter((t) => t.jour === aujourdhui).sort((a, b) => a.a.localeCompare(b.a)),
    repere,
    imagesDuJour,
    etoilesDuJour: gains.filter((g) => g.jour === aujourdhui).reduce((s, g) => s + g.value, 0),
  };
}

// ───────────────────────── les trophées ─────────────────────────

export type Trophee = {
  id: string;
  nom: string;
  /** Ce qu'il a fallu faire, dit à l'enfant et non au développeur. */
  condition: string;
  icone: NomIcone;
  obtenu: boolean;
};

export type EtatJeu = {
  etoiles: number;
  images: number;
  albumsComplets: number;
  leconsTerminees: number;
  serie: number;
  meilleureSerieDefi: number;
};

export function trophees(e: EtatJeu): Trophee[] {
  const liste: Array<[string, string, string, string, boolean]> = [
    ['premiere-image', 'Première image', 'Gagner sa première image', 'image', e.images >= 1],
    ['dix-images', 'Collectionneur', 'Gagner 10 images', 'collection', e.images >= 10],
    ['album', 'Album terminé', 'Toutes les images d’une matière', 'album', e.albumsComplets >= 1],
    ['lecon', 'Leçon au complet', 'Monter les 4 étapes d’une leçon', 'echelle', e.leconsTerminees >= 1],
    ['serie-3', 'Trois jours', 'Jouer 3 jours de suite', 'flamme', e.serie >= 3],
    ['serie-7', 'Une semaine', 'Jouer 7 jours de suite', 'flamme', e.serie >= 7],
    ['serie-30', 'Un mois entier', 'Jouer 30 jours de suite', 'flamme', e.serie >= 30],
    ['mille', 'Mille étoiles', 'Gagner 1 000 étoiles', 'etoile', e.etoiles >= 1000],
    ['defi', 'Défi parfait', '5 bonnes réponses d’affilée au chrono', 'chrono', e.meilleureSerieDefi >= 5],
  ];
  return liste.map(([id, nom, condition, icone, obtenu]) => ({
    id,
    nom,
    condition,
    icone: icone as NomIcone,
    obtenu,
  }));
}

// ───────────────────────── ce qu'on dit à l'enfant ─────────────────────────

/**
 * La phrase d'accueil.
 *
 * Elle ne décrit pas l'état de l'app : elle donne une raison de toucher le
 * bouton tout de suite. L'ordre compte — on sert d'abord ce qui se perd (la
 * série), puis ce qui est à portée (l'objectif, une image), et seulement
 * ensuite l'encouragement général.
 */
export function phraseDAccueil(a: {
  serie: Serie;
  objectif: Objectif;
  imagesRestantes: number;
  reste: number;
  prenom: string;
}): { titre: string; sous: string } {
  const { serie, objectif, imagesRestantes, prenom } = a;

  if (serie.jours > 0 && !serie.joueAujourdhui) {
    return {
      titre: `Ta série de ${serie.jours} jour${serie.jours > 1 ? 's' : ''} t’attend`,
      sous: 'Une seule leçon suffit à la garder.',
    };
  }
  if (objectif.atteint) {
    return { titre: 'Objectif du jour atteint !', sous: 'Tout ce que tu joues maintenant est du bonus.' };
  }
  if (objectif.gagnees > 0) {
    return {
      titre: `Plus que ${objectif.cible - objectif.gagnees} étoiles`,
      sous: 'Et l’objectif du jour est à toi.',
    };
  }
  if (serie.jours >= 3) {
    return { titre: `${serie.jours} jours de suite !`, sous: 'On continue aujourd’hui ?' };
  }
  if (imagesRestantes > 0 && imagesRestantes <= 3) {
    return {
      titre: `Encore ${imagesRestantes} image${imagesRestantes > 1 ? 's' : ''}`,
      sous: 'Et ta collection est complète.',
    };
  }
  return { titre: `À toi de jouer, ${prenom} !`, sous: 'Une leçon, et ta série démarre.' };
}
