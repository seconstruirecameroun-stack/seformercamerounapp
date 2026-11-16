import type { TableauDeBord } from './dashboard';
import { PALIERS } from './paliers';
import { totalDe, type CompositionRow } from './composition';
import { palmares } from './recompenses';
import type { Bilan } from './avatar';

/**
 * Le bilan du personnage, lu dans le tableau de bord et les copies rendues.
 *
 * Le tableau de bord est celui que l'enfant et le parent voient déjà : le
 * personnage ne recompte rien de son côté, il ne peut donc pas annoncer un
 * travail que l'espace de l'enfant ne montre pas.
 */
export function bilanDe(d: TableauDeBord, compositions: CompositionRow[], aujourdhui: string): Bilan {
  const etapesFranchies = d.lecons.reduce(
    (total, l) => total + (l.etapeTerminee ? PALIERS.length : Math.max(0, l.etape - 1)),
    0,
  );

  // Une matière complète : toutes ses leçons validées, et au moins une.
  const parMatiere = new Map<string, { total: number; validees: number }>();
  for (const l of d.lecons) {
    if (!l.matiereId) continue;
    const m = parMatiere.get(l.matiereId) ?? { total: 0, validees: 0 };
    m.total += 1;
    if (l.validee) m.validees += 1;
    parMatiere.set(l.matiereId, m);
  }
  const matieresCompletes = [...parMatiere.values()].filter((m) => m.total > 0 && m.validees === m.total).length;

  const copies = compositions
    .filter((c) => c.finie_le && c.justes !== null)
    .map((c) => ({ id: c.id, titre: c.titre, points: c.justes ?? 0, total: totalDe(c), finie_le: c.finie_le! }));
  const { compte } = palmares(copies);

  const jours = [...d.jours].sort();
  const dernierJour = jours.length ? jours[jours.length - 1] : null;
  const ilYA7 = new Date(Date.parse(aujourdhui + 'T00:00:00Z') - 6 * 86_400_000).toISOString().slice(0, 10);

  return {
    etapesFranchies,
    leconsTerminees: d.lecons.filter((l) => l.etapeTerminee).length,
    leconsValidees: d.lecons.filter((l) => l.validee).length,
    images: d.autocollants.filter((a) => a.acquis).length,
    etoiles: d.points,
    joursJoues: jours.length,
    serieJours: d.serie.jours,
    serieManches: d.serieManches,
    or: compte.or,
    argent: compte.argent,
    bronze: compte.bronze,
    matieresCompletes,
    dernierJour,
    joursRecents: jours.filter((j) => j >= ilYA7 && j <= aujourdhui).length,
  };
}
