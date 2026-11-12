import { mention, type Mention } from './epreuve';

/**
 * Les récompenses d'une composition : ce qu'on gagne en continuant à bien
 * répondre, et ce qu'on garde une fois la copie rendue.
 *
 * DEUX RÈGLES :
 *
 *   LA NOTE NE BOUGE PAS. Elle reste le compte des bonnes réponses, comme sur
 *   la copie de l'école. Les récompenses agissent sur le JEU — les points du
 *   plateau, un coup en plus — et sur ce qu'on collectionne, jamais sur la
 *   note.
 *
 *   ON VOIT TOUJOURS CE QUI VIENT. « Encore une bonne réponse, et tes points
 *   comptent double » : un enfant qui sait ce qu'il va gagner a une raison
 *   de rester concentré à la question suivante.
 *
 * Tout ici est pur, et vérifié par recompenses.verif.ts.
 */

// ── Les séries ──────────────────────────────────────────────────────────────

/** Les paliers d'une série de bonnes réponses d'affilée. */
export const PALIERS_DE_SERIE = [
  { serie: 3, multiplicateur: 2 },
  { serie: 5, multiplicateur: 3 },
  { serie: 10, multiplicateur: 4 },
] as const;

/** Combien comptent les points du plateau, pour une série donnée. */
export function multiplicateur(serie: number): number {
  let m = 1;
  for (const p of PALIERS_DE_SERIE) if (serie >= p.serie) m = p.multiplicateur;
  return m;
}

/** Le prochain palier de série, et combien de bonnes réponses y mènent. */
export function prochainPalier(serie: number): { dans: number; multiplicateur: number } | null {
  const p = PALIERS_DE_SERIE.find((x) => x.serie > serie);
  return p ? { dans: p.serie - serie, multiplicateur: p.multiplicateur } : null;
}

/** Vrai si cette série vient d'atteindre un palier : c'est un moment fort. */
export function palierAtteint(serie: number): boolean {
  return PALIERS_DE_SERIE.some((p) => p.serie === serie);
}

// ── La mention ──────────────────────────────────────────────────────────────

/**
 * Les seuils des lettres, en part du total.
 *
 * Ils doivent rester ceux de `mention` (epreuve.ts) : le test le vérifie.
 */
export const SEUILS: Array<{ lettre: Mention; part: number }> = [
  { lettre: 'C', part: 0.5 },
  { lettre: 'B', part: 0.6 },
  { lettre: 'A', part: 0.75 },
  { lettre: 'A+', part: 0.9 },
];

/** Les points qu'il faut pour une lettre, sur un total donné. */
export function pointsPour(lettre: Mention, total: number): number {
  const s = SEUILS.find((x) => x.lettre === lettre);
  return s ? Math.ceil(s.part * total - 1e-9) : 0;
}

/**
 * La mention ASSURÉE : celle qu'on ne peut plus perdre.
 *
 * Les points ne font que monter pendant une épreuve. Dès qu'on a de quoi
 * faire un B, ce B est acquis, quoi qu'il arrive ensuite — c'est ce qui rend
 * l'annonce juste, et c'est ce qui donne envie de viser le suivant.
 */
export function mentionAssuree(points: number, total: number): Mention | null {
  let m: Mention | null = null;
  for (const s of SEUILS) if (points >= pointsPour(s.lettre, total)) m = s.lettre;
  return m;
}

/**
 * La prochaine lettre à gagner, et combien de points y mènent — seulement si
 * elle est encore possible avec les questions qui restent.
 */
export function prochaineMention(
  points: number,
  total: number,
  restantes: number,
): { lettre: Mention; manque: number } | null {
  for (const s of SEUILS) {
    const besoin = pointsPour(s.lettre, total);
    if (points < besoin) {
      const manque = besoin - points;
      return manque <= restantes ? { lettre: s.lettre, manque } : null;
    }
  }
  return null;
}

// ── Les médailles ───────────────────────────────────────────────────────────

export type Metal = 'or' | 'argent' | 'bronze';

/** La médaille d'une copie rendue : l'or pour un A+, l'argent pour un A, le bronze pour un B. */
export function medailleDe(points: number, total: number): Metal | null {
  const m = mention(points, total);
  if (m === 'A+') return 'or';
  if (m === 'A') return 'argent';
  if (m === 'B') return 'bronze';
  return null;
}

/** Ce qu'il manquait pour la médaille du dessus : de quoi viser la prochaine fois. */
export function prochaineMedaille(points: number, total: number): { metal: Metal; manque: number } | null {
  const actuelle = medailleDe(points, total);
  const cible: { metal: Metal; lettre: Mention } | null =
    actuelle === 'or' ? null
      : actuelle === 'argent' ? { metal: 'or', lettre: 'A+' }
        : actuelle === 'bronze' ? { metal: 'argent', lettre: 'A' }
          : { metal: 'bronze', lettre: 'B' };
  if (!cible) return null;
  return { metal: cible.metal, manque: pointsPour(cible.lettre, total) - points };
}

export type CopieRendue = { id: string; titre: string; points: number; total: number; finie_le: string };

export type Trophee = { cle: string; titre: string; detail: string; gagne: boolean };

/**
 * Les médailles et les trophées d'un enfant, lus dans ses copies rendues.
 *
 * Rien n'est enregistré à part : tout se déduit des notes. Une copie
 * supprimée par le parent emporte sa médaille, et rien ne peut se
 * contredire.
 */
export function palmares(copies: CopieRendue[]) {
  const triees = [...copies].sort((a, b) => a.finie_le.localeCompare(b.finie_le));
  const compte = { or: 0, argent: 0, bronze: 0 };
  for (const c of triees) {
    const m = medailleDe(c.points, c.total);
    if (m) compte[m] += 1;
  }
  let meilleureSuite = 0;
  let suite = 0;
  for (const c of triees) {
    const m = mention(c.points, c.total);
    suite = m === 'A' || m === 'A+' ? suite + 1 : 0;
    meilleureSuite = Math.max(meilleureSuite, suite);
  }
  const parfaite = triees.some((c) => c.total > 0 && c.points === c.total);
  const trophees: Trophee[] = [
    { cle: 'premiere', titre: 'Première copie', detail: 'Rendre sa première composition', gagne: triees.length >= 1 },
    { cle: 'premier-or', titre: 'Premier or', detail: 'Une copie notée A+', gagne: compte.or >= 1 },
    { cle: 'trois-a', titre: 'Trois A de suite', detail: 'Trois copies A ou A+ d’affilée', gagne: meilleureSuite >= 3 },
    { cle: 'parfaite', titre: 'Copie parfaite', detail: 'Toutes les réponses justes', gagne: parfaite },
    { cle: 'cinq-or', titre: 'Cinq ors', detail: 'Cinq copies notées A+', gagne: compte.or >= 5 },
  ];
  return { compte, trophees, copies: triees.reverse() };
}
