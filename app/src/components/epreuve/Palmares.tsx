import { totalDe, type CompositionRow } from '../../lib/composition';
import { palmares } from '../../lib/recompenses';
import Medaille from './Medaille';

/**
 * Mes médailles : ce que les compositions ont rapporté, et ce qui reste à
 * gagner.
 *
 * Tout se lit dans les copies rendues — rien n'est enregistré à part. Les
 * trophées pas encore gagnés restent visibles, en gris : un enfant vise
 * mieux ce qu'il voit.
 */
export default function Palmares({ compositions }: { compositions: CompositionRow[] }) {
  const copies = compositions
    .filter((c) => c.finie_le && c.justes !== null)
    .map((c) => ({
      id: c.id,
      titre: c.titre,
      points: c.justes ?? 0,
      total: totalDe(c),
      finie_le: c.finie_le!,
    }));
  if (copies.length === 0) return null;
  const { compte, trophees } = palmares(copies);
  const gagnes = trophees.filter((t) => t.gagne).length;

  return (
    <section className="rounded-[var(--radius-card)] border-2 border-gold bg-white-warm px-4 py-3">
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-kid-sm font-extrabold">Mes médailles</h2>
        <span className="text-kid-xs font-bold text-muted">
          {gagnes} trophée{gagnes > 1 ? 's' : ''} sur {trophees.length}
        </span>
      </div>

      <div className="mt-2 flex items-end justify-around">
        {(['or', 'argent', 'bronze'] as const).map((m) => (
          <div key={m} className="flex flex-col items-center">
            <Medaille metal={m} taille={m === 'or' ? 52 : 44} terne={compte[m] === 0} />
            <span className="mt-0.5 text-kid-sm font-black tabular-nums">× {compte[m]}</span>
          </div>
        ))}
      </div>

      <ul className="mt-3 flex flex-wrap gap-1.5">
        {trophees.map((t) => (
          <li
            key={t.cle}
            title={t.detail}
            className={
              'rounded-full px-2.5 py-1 text-kid-xs font-black ' +
              (t.gagne ? 'bg-gold text-ink' : 'border border-dashed border-line text-muted')
            }
          >
            {t.gagne ? '🏆 ' : '🔒 '}
            {t.titre}
          </li>
        ))}
      </ul>
    </section>
  );
}
