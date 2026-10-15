import { Link } from 'react-router-dom';
import Illustration from './Illustration';
import type { LeconResume } from '../lib/dashboard';

/**
 * Où en est l'enfant dans cette leçon : l'escalier, et la marche en cours.
 *
 * Le pourcentage de notions acquises qui figurait ici ne disait rien à un
 * enfant — il ne voyait ni où il était, ni ce qu'il visait.
 */
export default function CarteLecon({
  lecon,
  childId,
  montrerMatiere = true,
}: {
  lecon: LeconResume;
  childId: string;
  /** Inutile dans le dossier d'une matière : il la porte déjà en titre. */
  montrerMatiere?: boolean;
}) {
  const part =
    lecon.etapeTotal > 0 ? Math.round((lecon.etapeFaites / lecon.etapeTotal) * 100) : 0;
  return (
    <Link
      to={`/enfant/${childId}/lecon/${lecon.id}`}
      className="tuile flex items-center gap-3 overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm p-2 pr-4 shadow-[var(--shadow-tile)]"
    >
      <Illustration
        cle={lecon.illustration}
        forme="scene"
        alt=""
        className="h-20 w-28 shrink-0 rounded-2xl object-cover"
      />
      <div className="min-w-0 flex-1">
        {montrerMatiere ? (
          <p className="text-kid-xs font-black tracking-wide text-muted uppercase">
            {lecon.matiere ?? 'Leçon'}
          </p>
        ) : null}
        <h3 className="line-clamp-2 text-kid font-extrabold">{lecon.title}</h3>
        <div className="mt-1.5 flex items-center gap-2">
          <span className="flex shrink-0 items-center gap-1" aria-hidden="true">
            {[1, 2, 3].map((n) => (
              <span
                key={n}
                className={
                  'grid h-5 w-5 place-items-center rounded-full text-[0.7rem] font-black ' +
                  (lecon.etapeTerminee || n < lecon.etape
                    ? 'bg-leaf text-white-warm'
                    : n === lecon.etape
                      ? 'bg-gold text-ink'
                      : 'bg-line text-muted')
                }
              >
                {lecon.etapeTerminee || n < lecon.etape ? '★' : n}
              </span>
            ))}
          </span>
          <span className="h-2 flex-1 overflow-hidden rounded-full bg-ink/15">
            <span
              className="block h-full rounded-full bg-gold transition-all duration-500"
              style={{ width: `${part}%` }}
            />
          </span>
        </div>
        <p className="mt-1 text-kid-xs font-bold text-muted">
          {lecon.etapeTerminee
            ? 'Leçon terminée — tu révises'
            : `Étape ${lecon.etape} · ${lecon.etapeFaites}/${lecon.etapeTotal}`}
        </p>
      </div>
      {lecon.aRevoir > 0 ? (
        <span className="grid h-7 min-w-7 shrink-0 place-items-center rounded-full bg-clay px-2 text-kid-xs font-black text-white-warm">
          {lecon.aRevoir}
        </span>
      ) : null}
    </Link>
  );
}
