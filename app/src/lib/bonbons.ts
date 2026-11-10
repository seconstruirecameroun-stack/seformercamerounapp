/**
 * Le plateau de bonbons de la salle de composition.
 *
 * POURQUOI UN JEU AU-DESSUS DES QUESTIONS. Une composition est longue — dix,
 * vingt ou trente questions d'affilée, sans la progression d'une leçon pour
 * porter l'enfant. Le plateau donne à chaque bonne réponse une conséquence
 * immédiate et visible : un coup à jouer, des bonbons qui explosent, un score
 * qui monte. Le jeu ne lui apprend rien ; il le paie. C'est exactement ce que
 * font déjà les étoiles, en beaucoup plus engageant.
 *
 * CE QUE LE JEU NE FAIT PAS. Il ne juge pas, il ne corrige pas, et il ne
 * décide de rien : la note de la composition est le compte des bonnes
 * réponses, et elle ne dépend pas du score du plateau. Un enfant qui répond
 * juste et joue mal a la même note qu'un enfant qui répond juste et joue
 * bien. Sans quoi la note ne dirait plus ce qu'il sait.
 *
 * TOUT EST PUR ET SANS HASARD CACHÉ. Le hasard entre par un paramètre, ce qui
 * rend chaque règle vérifiable hors du navigateur — et une règle de jeu qui
 * se trompe est une injustice que l'enfant subit sans pouvoir la nommer.
 */

/** Une case vide, le temps que les bonbons tombent. */
export const VIDE = -1;

/** Cinq couleurs. Six rendraient les alignements trop rares sur 7 colonnes. */
export const COULEURS = 5;

export type Case = number;
/** Le plateau, ligne par ligne, la ligne 0 en haut. */
export type Plateau = Case[][];
export type Position = { l: number; c: number };
export type Coup = { a: Position; b: Position };
/** Une source de hasard, injectée pour que tout se vérifie. */
export type Alea = () => number;

/** Une étape d'animation : ce qui explose, puis le plateau après la chute. */
export type Etape = { explosions: Position[]; apres: Plateau; points: number };

export type Resultat = {
  plateau: Plateau;
  etapes: Etape[];
  /** Les points gagnés par ce coup, cascades comprises. */
  points: number;
  /** Combien de bonbons ont disparu en tout. */
  bonbons: number;
};

const copie = (p: Plateau): Plateau => p.map((ligne) => [...ligne]);

export function estVoisin(a: Position, b: Position): boolean {
  return Math.abs(a.l - b.l) + Math.abs(a.c - b.c) === 1;
}

/**
 * Toutes les cases prises dans un alignement de trois ou plus.
 *
 * Les lignes et les colonnes sont parcourues séparément, et une case comptée
 * deux fois — le croisement d'un alignement horizontal et d'un vertical — ne
 * figure qu'une fois dans le résultat. Sans cette déduplication, un coup en
 * forme de L paierait deux fois la même case.
 */
export function alignements(p: Plateau): Position[] {
  const prises = new Set<string>();
  const lignes = p.length;
  const colonnes = p[0]?.length ?? 0;

  const retenir = (suite: Position[]) => {
    if (suite.length >= 3) for (const q of suite) prises.add(q.l + ':' + q.c);
  };

  for (let l = 0; l < lignes; l++) {
    let suite: Position[] = [];
    for (let c = 0; c < colonnes; c++) {
      const v = p[l][c];
      if (v !== VIDE && suite.length > 0 && p[suite[0].l][suite[0].c] === v) {
        suite.push({ l, c });
      } else {
        retenir(suite);
        suite = v === VIDE ? [] : [{ l, c }];
      }
    }
    retenir(suite);
  }

  for (let c = 0; c < colonnes; c++) {
    let suite: Position[] = [];
    for (let l = 0; l < lignes; l++) {
      const v = p[l][c];
      if (v !== VIDE && suite.length > 0 && p[suite[0].l][suite[0].c] === v) {
        suite.push({ l, c });
      } else {
        retenir(suite);
        suite = v === VIDE ? [] : [{ l, c }];
      }
    }
    retenir(suite);
  }

  return [...prises].map((cle) => {
    const [l, c] = cle.split(':').map(Number);
    return { l, c };
  });
}

/** Le plateau après un échange, sans rien résoudre. */
function echanger(p: Plateau, a: Position, b: Position): Plateau {
  const q = copie(p);
  const garde = q[a.l][a.c];
  q[a.l][a.c] = q[b.l][b.c];
  q[b.l][b.c] = garde;
  return q;
}

/**
 * Les bonbons tombent, et le haut se recharge.
 *
 * On compacte colonne par colonne vers le bas, puis on remplit ce qui reste
 * en haut. Les nouveaux bonbons peuvent eux-mêmes former un alignement : la
 * boucle de `jouer` s'en occupe, et c'est ce qu-on appelle une cascade.
 */
function tomber(p: Plateau, alea: Alea, couleurs: number): Plateau {
  const lignes = p.length;
  const colonnes = p[0].length;
  const q = copie(p);
  for (let c = 0; c < colonnes; c++) {
    const restants: Case[] = [];
    for (let l = lignes - 1; l >= 0; l--) if (q[l][c] !== VIDE) restants.push(q[l][c]);
    for (let l = lignes - 1; l >= 0; l--) {
      const i = lignes - 1 - l;
      q[l][c] = i < restants.length ? restants[i] : Math.floor(alea() * couleurs);
    }
  }
  return q;
}

/**
 * Ce que rapporte une explosion.
 *
 * Dix points par bonbon, multipliés par le rang de la cascade : la deuxième
 * vague vaut double, la troisième triple. C'est ce qui rend un bon coup
 * nettement meilleur qu'un coup quelconque, et donc ce qui fait réfléchir.
 */
export function pointsDeLExplosion(bonbons: number, cascade: number): number {
  return 10 * bonbons * cascade;
}

/**
 * Joue un échange et résout tout ce qu'il entraîne.
 *
 * Renvoie `null` si l'échange ne forme aucun alignement : ce n'est pas un
 * coup. L'interface ne devrait pas le proposer, et le refuser ici garantit
 * qu'aucun chemin ne peut faire disparaître un bonbon pour rien.
 */
export function jouer(
  p: Plateau,
  coup: Coup,
  alea: Alea,
  couleurs = COULEURS,
): Resultat | null {
  if (!estVoisin(coup.a, coup.b)) return null;
  let plateau = echanger(p, coup.a, coup.b);
  if (alignements(plateau).length === 0) return null;

  const etapes: Etape[] = [];
  let points = 0;
  let bonbons = 0;
  let cascade = 1;

  for (;;) {
    const touches = alignements(plateau);
    if (touches.length === 0) break;
    const gagne = pointsDeLExplosion(touches.length, cascade);
    points += gagne;
    bonbons += touches.length;
    const vide = copie(plateau);
    for (const q of touches) vide[q.l][q.c] = VIDE;
    plateau = tomber(vide, alea, couleurs);
    etapes.push({ explosions: touches, apres: copie(plateau), points: gagne });
    cascade += 1;
  }

  return { plateau, etapes, points, bonbons };
}

/** Tous les échanges qui forment au moins un alignement. */
export function coupsPossibles(p: Plateau): Coup[] {
  const trouves: Coup[] = [];
  const lignes = p.length;
  const colonnes = p[0]?.length ?? 0;
  for (let l = 0; l < lignes; l++) {
    for (let c = 0; c < colonnes; c++) {
      for (const b of [
        { l, c: c + 1 },
        { l: l + 1, c },
      ]) {
        if (b.l >= lignes || b.c >= colonnes) continue;
        const a = { l, c };
        if (alignements(echanger(p, a, b)).length > 0) trouves.push({ a, b });
      }
    }
  }
  return trouves;
}

/**
 * Un coup à montrer à l'enfant qui hésite.
 *
 * Toujours le même pour un plateau donné : une suggestion qui change d'une
 * seconde à l'autre se lit comme un clignotement, et non comme un conseil.
 */
export function suggestion(p: Plateau): Coup | null {
  return coupsPossibles(p)[0] ?? null;
}

/**
 * Rebat les bonbons sans en changer aucun.
 *
 * Quand plus aucun coup n'existe, on ne recharge pas le plateau — on remue
 * ceux qui sont là. L'enfant retrouve ses couleurs, et le jeu ne lui vole
 * rien. On réessaie jusqu'à obtenir un plateau jouable et sans alignement
 * déjà formé, puis on rend le meilleur essai.
 */
export function melangerPlateau(p: Plateau, alea: Alea, essais = 60): Plateau {
  const bonbons: Case[] = p.flat();
  const lignes = p.length;
  const colonnes = p[0].length;
  let dernier = p;
  for (let n = 0; n < essais; n++) {
    const melange = [...bonbons];
    for (let i = melange.length - 1; i > 0; i--) {
      const j = Math.floor(alea() * (i + 1));
      [melange[i], melange[j]] = [melange[j], melange[i]];
    }
    const q: Plateau = [];
    for (let l = 0; l < lignes; l++) q.push(melange.slice(l * colonnes, (l + 1) * colonnes));
    dernier = q;
    if (alignements(q).length === 0 && coupsPossibles(q).length > 0) return q;
  }
  return dernier;
}

/**
 * Un plateau de départ : aucun alignement déjà fait, et au moins un coup.
 *
 * Un alignement offert à l'ouverture donnerait des points sans qu'il ait rien
 * joué ; un plateau sans coup possible lui demanderait de jouer un coup qui
 * n'existe pas. Les deux se vérifient ici plutôt que de se corriger après.
 */
export function nouveauPlateau(
  lignes: number,
  colonnes: number,
  alea: Alea,
  couleurs = COULEURS,
): Plateau {
  for (let essai = 0; essai < 200; essai++) {
    const p: Plateau = [];
    for (let l = 0; l < lignes; l++) {
      const ligne: Case[] = [];
      for (let c = 0; c < colonnes; c++) {
        // On tire en écartant les couleurs qui feraient un alignement tout
        // de suite : deux à gauche, ou deux au-dessus, de la même couleur.
        const interdites = new Set<number>();
        if (c >= 2 && ligne[c - 1] === ligne[c - 2]) interdites.add(ligne[c - 1]);
        if (l >= 2 && p[l - 1][c] === p[l - 2][c]) interdites.add(p[l - 1][c]);
        const libres = [];
        for (let k = 0; k < couleurs; k++) if (!interdites.has(k)) libres.push(k);
        ligne.push(libres[Math.floor(alea() * libres.length)]);
      }
      p.push(ligne);
    }
    if (alignements(p).length === 0 && coupsPossibles(p).length > 0) return p;
  }
  // Inatteignable en pratique : 200 tirages sans plateau jouable supposerait
  // un hasard dégénéré. On rend tout de même quelque chose de jouable.
  const secours: Plateau = [];
  for (let l = 0; l < lignes; l++) {
    const ligne: Case[] = [];
    for (let c = 0; c < colonnes; c++) ligne.push((l + c) % couleurs);
    secours.push(ligne);
  }
  return melangerPlateau(secours, alea);
}

/**
 * Le score à atteindre pour que le plateau soit gagné.
 *
 * Cinquante points par question posée. Un coup ordinaire en rapporte trente
 * à cinquante, un bon coup bien plus : l'objectif demande donc de répondre
 * juste à la plupart des questions, sans exiger la perfection — le
 * sans-faute, lui, est l'affaire de la manche de validation, pas de la
 * composition.
 */
export function objectifDuPlateau(questions: number): number {
  return 50 * questions;
}
