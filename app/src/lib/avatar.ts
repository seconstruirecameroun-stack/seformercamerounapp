/**
 * Le personnage de l'enfant : ce qu'il gagne, ce qu'il garde, ce qui s'éteint.
 *
 * TOUT SE LIT DANS LE JOURNAL. Rien n'est enregistré à part : les objets, le
 * niveau et l'énergie se déduisent du travail réel de l'enfant — étapes
 * franchies, leçons maîtrisées et validées, images, médailles, jours joués.
 * Un objet ne peut donc pas être gagné sans le travail qui le mérite, ni
 * perdu sans raison.
 *
 * TROIS RÈGLES, choisies par le père :
 *
 *   CE QUI EST GAGNÉ PAR LA MAÎTRISE RESTE. Un chapeau gagné en franchissant
 *   dix étapes est à l'enfant pour toujours : son travail ne lui est jamais
 *   repris.
 *
 *   L'ÉNERGIE BAISSE SANS TRAVAIL. Chaque jour sans jouer, elle descend ;
 *   une séance la remet au maximum. Basse, elle éteint l'aura, et les objets
 *   légendaires ne brillent plus — l'enfant les a toujours, mais ils
 *   attendent qu'il revienne.
 *
 *   LES OBJETS TEMPORAIRES DISPARAISSENT après sept jours sans travail. Ce
 *   sont les pouvoirs de l'élan du moment — des flammes pour une série de
 *   jours, des éclairs pour des manches parfaites. Ils se regagnent.
 *
 * Le dernier niveau, Légende, est fait pour être difficile : beaucoup de
 * travail ET une matière entière validée ET des médailles d'or.
 *
 * Tout ce fichier est pur, et vérifié par avatar.verif.ts.
 */

export type Emplacement =
  | 'tete' | 'visage' | 'corps' | 'accessoire' | 'dos' | 'main' | 'pieds' | 'compagnon' | 'aura';
export type Rarete = 'commun' | 'rare' | 'epique' | 'legendaire';

/** Le travail de l'enfant, tel que le tableau de bord le connaît. */
export type Bilan = {
  etapesFranchies: number;
  leconsTerminees: number;
  leconsValidees: number;
  images: number;
  etoiles: number;
  joursJoues: number;
  /** Jours joués d'affilée, jusqu'à aujourd'hui. */
  serieJours: number;
  /** Manches parfaites d'affilée. */
  serieManches: number;
  or: number;
  argent: number;
  bronze: number;
  /** Matières dont toutes les leçons sont validées. */
  matieresCompletes: number;
  /** Le dernier jour joué (AAAA-MM-JJ), ou null s'il n'a jamais joué. */
  dernierJour: string | null;
  /** Jours joués pendant les sept derniers jours. */
  joursRecents: number;
};

export type Objet = {
  id: string;
  nom: string;
  emplacement: Emplacement;
  rarete: Rarete;
  /** Disparaît après sept jours sans travail. */
  temporaire: boolean;
  /** Ce qu'il faut faire pour l'avoir, dit à l'enfant. */
  condition: string;
  /** La progression vers l'objet : où il en est, et le but. */
  progres: (b: Bilan) => { fait: number; but: number };
};

const p = (fait: number, but: number) => ({ fait: Math.min(fait, but), but });

/** Le catalogue. L'ordre compte : du plus facile au plus difficile, par emplacement. */
export const OBJETS: Objet[] = [
  // ── La tête ──
  { id: 'casquette', nom: 'Casquette', emplacement: 'tete', rarete: 'commun', temporaire: false,
    condition: 'Franchis ta première étape', progres: (b) => p(b.etapesFranchies, 1) },
  { id: 'bandeau', nom: 'Bandeau de champion', emplacement: 'tete', rarete: 'rare', temporaire: false,
    condition: 'Franchis 15 étapes', progres: (b) => p(b.etapesFranchies, 15) },
  { id: 'chapeau', nom: 'Chapeau d’explorateur', emplacement: 'tete', rarete: 'epique', temporaire: false,
    condition: 'Gravis 10 leçons jusqu’en haut', progres: (b) => p(b.leconsTerminees, 10) },
  { id: 'capuche', nom: 'Capuche à oreilles', emplacement: 'tete', rarete: 'epique', temporaire: false,
    condition: 'Valide 5 leçons', progres: (b) => p(b.leconsValidees, 5) },
  { id: 'couronne', nom: 'Couronne', emplacement: 'tete', rarete: 'legendaire', temporaire: false,
    condition: 'Valide 15 leçons', progres: (b) => p(b.leconsValidees, 15) },

  // ── Le visage ──
  { id: 'lunettes', nom: 'Lunettes rondes', emplacement: 'visage', rarete: 'rare', temporaire: false,
    condition: 'Gravis 3 leçons jusqu’en haut', progres: (b) => p(b.leconsTerminees, 3) },
  { id: 'cache-cou', nom: 'Cache-cou', emplacement: 'visage', rarete: 'rare', temporaire: false,
    condition: 'Franchis 20 étapes', progres: (b) => p(b.etapesFranchies, 20) },
  { id: 'lunettes-soleil', nom: 'Lunettes de soleil', emplacement: 'visage', rarete: 'epique', temporaire: false,
    condition: 'Joue 20 jours', progres: (b) => p(b.joursJoues, 20) },

  // ── Les accessoires ──
  { id: 'porte-cles', nom: 'Porte-clés peluche', emplacement: 'accessoire', rarete: 'commun', temporaire: false,
    condition: 'Gagne 10 images', progres: (b) => p(b.images, 10) },
  { id: 'bretelles', nom: 'Harnais et écouteurs', emplacement: 'accessoire', rarete: 'rare', temporaire: false,
    condition: 'Franchis 10 étapes', progres: (b) => p(b.etapesFranchies, 10) },
  { id: 'bandouliere', nom: 'Bandoulière à boucle', emplacement: 'accessoire', rarete: 'epique', temporaire: false,
    condition: 'Gravis 5 leçons jusqu’en haut', progres: (b) => p(b.leconsTerminees, 5) },
  { id: 'chaine-or', nom: 'Chaîne en or', emplacement: 'accessoire', rarete: 'legendaire', temporaire: false,
    condition: 'Gagne 3 médailles d’or', progres: (b) => p(b.or, 3) },

  // ── Le corps ──
  { id: 'maillot', nom: 'Maillot des Lions', emplacement: 'corps', rarete: 'rare', temporaire: false,
    condition: 'Franchis 25 étapes', progres: (b) => p(b.etapesFranchies, 25) },
  { id: 'armure', nom: 'Armure du savoir', emplacement: 'corps', rarete: 'epique', temporaire: false,
    condition: 'Gravis 25 leçons jusqu’en haut', progres: (b) => p(b.leconsTerminees, 25) },
  { id: 'tenue-or', nom: 'Tenue dorée', emplacement: 'corps', rarete: 'legendaire', temporaire: false,
    condition: 'Gagne 5 médailles d’or en composition', progres: (b) => p(b.or, 5) },

  // ── Le dos ──
  { id: 'sac', nom: 'Sac d’aventure', emplacement: 'dos', rarete: 'commun', temporaire: false,
    condition: 'Gravis une leçon jusqu’en haut', progres: (b) => p(b.leconsTerminees, 1) },
  { id: 'cape', nom: 'Cape', emplacement: 'dos', rarete: 'rare', temporaire: false,
    condition: 'Valide 3 leçons', progres: (b) => p(b.leconsValidees, 3) },
  { id: 'ailes', nom: 'Ailes', emplacement: 'dos', rarete: 'epique', temporaire: false,
    condition: 'Valide 10 leçons', progres: (b) => p(b.leconsValidees, 10) },
  { id: 'ailes-or', nom: 'Ailes dorées', emplacement: 'dos', rarete: 'legendaire', temporaire: false,
    condition: 'Valide une matière entière', progres: (b) => p(b.matieresCompletes, 1) },

  // ── La main ──
  { id: 'livre', nom: 'Livre magique', emplacement: 'main', rarete: 'rare', temporaire: false,
    condition: 'Gagne une médaille en composition', progres: (b) => p(b.or + b.argent + b.bronze, 1) },
  { id: 'trophee', nom: 'Trophée', emplacement: 'main', rarete: 'epique', temporaire: false,
    condition: 'Gagne une médaille d’or', progres: (b) => p(b.or, 1) },

  // ── Les pieds ──
  { id: 'baskets', nom: 'Baskets', emplacement: 'pieds', rarete: 'commun', temporaire: false,
    condition: 'Joue 7 jours', progres: (b) => p(b.joursJoues, 7) },
  { id: 'bottes', nom: 'Bottes éclair', emplacement: 'pieds', rarete: 'epique', temporaire: false,
    condition: 'Joue 40 jours', progres: (b) => p(b.joursJoues, 40) },

  // ── Le compagnon ──
  { id: 'balle', nom: 'Petite balle', emplacement: 'compagnon', rarete: 'commun', temporaire: false,
    condition: 'Gagne ta première image', progres: (b) => p(b.images, 1) },
  { id: 'etoile', nom: 'Étoile filante', emplacement: 'compagnon', rarete: 'rare', temporaire: false,
    condition: 'Gagne 40 images', progres: (b) => p(b.images, 40) },
  { id: 'lionceau', nom: 'Bébé lion', emplacement: 'compagnon', rarete: 'legendaire', temporaire: false,
    condition: 'Gagne 200 images', progres: (b) => p(b.images, 200) },

  // ── Les pouvoirs du moment : ils disparaissent après sept jours sans travail ──
  { id: 'flammes', nom: 'Aura de flammes', emplacement: 'aura', rarete: 'rare', temporaire: true,
    condition: 'Joue 3 jours de suite', progres: (b) => p(b.serieJours, 3) },
  { id: 'eclairs', nom: 'Aura d’éclairs', emplacement: 'aura', rarete: 'epique', temporaire: true,
    condition: 'Réussis 3 manches parfaites d’affilée', progres: (b) => p(b.serieManches, 3) },
  { id: 'arc-en-ciel', nom: 'Aura arc-en-ciel', emplacement: 'aura', rarete: 'legendaire', temporaire: true,
    condition: 'Joue 6 des 7 derniers jours', progres: (b) => p(b.joursRecents, 6) },
];

export const RANG_RARETE: Record<Rarete, number> = { commun: 0, rare: 1, epique: 2, legendaire: 3 };

// ── L'énergie ───────────────────────────────────────────────────────────────

/** Les jours écoulés depuis le dernier jour joué. */
export function joursSansJouer(dernierJour: string | null, aujourdhui: string): number {
  if (!dernierJour) return Infinity;
  const ms = Date.parse(aujourdhui + 'T00:00:00Z') - Date.parse(dernierJour + 'T00:00:00Z');
  return Math.max(0, Math.round(ms / 86_400_000));
}

/**
 * L'énergie, de 0 à 100 : pleine le jour où il joue, un cinquième de moins
 * par jour sans travail, vide au bout de cinq jours.
 */
export function energie(dernierJour: string | null, aujourdhui: string): number {
  const j = joursSansJouer(dernierJour, aujourdhui);
  if (!Number.isFinite(j)) return 0;
  return Math.max(0, 100 - 20 * j);
}

/** Les objets légendaires ne brillent qu'au-dessus de cette énergie. */
export const ENERGIE_POUR_BRILLER = 60;
/** Les pouvoirs du moment s'éteignent après ce nombre de jours sans travail. */
export const JOURS_AVANT_PERTE = 7;

// ── Les objets de l'enfant ──────────────────────────────────────────────────

export type ObjetPossede = Objet & {
  /** Il l'a. */
  gagne: boolean;
  /** Il l'a, mais l'énergie est trop basse pour qu'il brille. */
  eteint: boolean;
  fait: number;
  but: number;
};

export function objetsDe(b: Bilan, aujourdhui: string): ObjetPossede[] {
  const sans = joursSansJouer(b.dernierJour, aujourdhui);
  const e = energie(b.dernierJour, aujourdhui);
  return OBJETS.map((o) => {
    const { fait, but } = o.progres(b);
    const atteint = fait >= but;
    // Un pouvoir du moment se perd après sept jours sans travail.
    const gagne = atteint && (!o.temporaire || sans < JOURS_AVANT_PERTE);
    const eteint = gagne && o.rarete === 'legendaire' && e < ENERGIE_POUR_BRILLER;
    return { ...o, gagne, eteint, fait, but };
  });
}

/**
 * Ce que porte le personnage : dans chaque emplacement, le choix de
 * l'enfant s'il l'a gagné, sinon le plus rare de ce qu'il a.
 */
export function equipement(
  objets: ObjetPossede[],
  choix: Partial<Record<Emplacement, string | null>> = {},
): Partial<Record<Emplacement, ObjetPossede>> {
  const sortie: Partial<Record<Emplacement, ObjetPossede>> = {};
  const emplacements = [...new Set(objets.map((o) => o.emplacement))];
  for (const em of emplacements) {
    const siens = objets.filter((o) => o.emplacement === em && o.gagne);
    if (choix[em] === null) continue; // il a choisi de ne rien porter là
    const voulu = siens.find((o) => o.id === choix[em]);
    const meilleur = [...siens].sort((a, z) => RANG_RARETE[z.rarete] - RANG_RARETE[a.rarete])[0];
    const porte = voulu ?? meilleur;
    if (porte) sortie[em] = porte;
  }
  return sortie;
}

// ── Les niveaux ─────────────────────────────────────────────────────────────

/** Les points d'évolution : ce que vaut chaque morceau de travail. */
export function pointsDEvolution(b: Bilan): number {
  return (
    b.etapesFranchies * 10 +
    b.leconsTerminees * 30 +
    b.leconsValidees * 60 +
    b.images * 3 +
    b.joursJoues * 5 +
    b.or * 80 +
    b.argent * 40 +
    b.bronze * 20
  );
}

export type Niveau = {
  rang: number;
  nom: string;
  seuil: number;
  /** Ce qu'il faut EN PLUS des points, pour les plus hauts niveaux. */
  exige?: { texte: string; ok: (b: Bilan) => boolean };
};

export const NIVEAUX: Niveau[] = [
  { rang: 1, nom: 'Débutant', seuil: 0 },
  { rang: 2, nom: 'Apprenti', seuil: 150 },
  { rang: 3, nom: 'Explorateur', seuil: 450 },
  { rang: 4, nom: 'Aventurier', seuil: 1000 },
  { rang: 5, nom: 'Champion', seuil: 2000 },
  { rang: 6, nom: 'Héros', seuil: 3500,
    exige: { texte: '10 leçons validées', ok: (b) => b.leconsValidees >= 10 } },
  { rang: 7, nom: 'Maître', seuil: 5500,
    exige: { texte: '25 leçons validées et 2 médailles d’or', ok: (b) => b.leconsValidees >= 25 && b.or >= 2 } },
  { rang: 8, nom: 'Légende', seuil: 9000,
    exige: {
      texte: 'une matière entière validée et 5 médailles d’or',
      ok: (b) => b.matieresCompletes >= 1 && b.or >= 5,
    } },
];

/**
 * Le niveau atteint, et ce qui manque pour le suivant.
 *
 * Un niveau exige ses points ET sa condition : on ne devient pas Légende
 * en répondant beaucoup, il faut avoir maîtrisé.
 */
export function niveauDe(b: Bilan) {
  const points = pointsDEvolution(b);
  let actuel = NIVEAUX[0];
  for (const n of NIVEAUX) {
    if (points >= n.seuil && (!n.exige || n.exige.ok(b))) actuel = n;
    else break;
  }
  const suivant = NIVEAUX.find((n) => n.rang === actuel.rang + 1) ?? null;
  const part = suivant
    ? Math.max(0, Math.min(1, (points - actuel.seuil) / (suivant.seuil - actuel.seuil)))
    : 1;
  return {
    points,
    actuel,
    suivant,
    part,
    manquePoints: suivant ? Math.max(0, suivant.seuil - points) : 0,
    manqueCondition: suivant?.exige && !suivant.exige.ok(b) ? suivant.exige.texte : null,
  };
}
