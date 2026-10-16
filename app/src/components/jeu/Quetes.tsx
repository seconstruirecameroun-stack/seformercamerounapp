import type { Quete, Trophee } from '../../lib/jeu';

/**
 * Les quêtes du jour et les trophées.
 *
 * Trois quêtes, pas plus : une liste qu'on ne finit jamais décourage au lieu
 * d'appeler. Elles sont toutes atteignables en une séance de dix minutes, et
 * elles changent chaque matin — c'est ce qui fait qu'un enfant ouvre l'app
 * pour voir ce qu'on lui demande aujourd'hui.
 *
 * Les trophées, eux, ne tournent pas : ils restent sur l'étagère. Les cases
 * vides comptent autant que les pleines — c'est la case vide qui donne envie.
 */

export function Quetes({ quetes }: { quetes: Quete[] }) {
  if (quetes.length === 0) return null;
  const finies = quetes.filter((q) => q.fait >= q.cible).length;

  return (
    <section className="rounded-[var(--radius-card)] border border-line bg-white-warm/80 px-4 py-3">
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-kid-sm font-extrabold">Tes défis du jour</h2>
        <span className="text-kid-xs font-bold text-muted">
          {finies} sur {quetes.length}
        </span>
      </div>
      <ul className="mt-2 grid gap-2">
        {quetes.map((q) => {
          const fini = q.fait >= q.cible;
          return (
            <li key={q.id} className="flex items-center gap-3">
              <span
                aria-hidden="true"
                className={
                  'grid h-8 w-8 shrink-0 place-items-center rounded-lg text-kid-sm ' +
                  (fini ? 'bg-leaf/25' : 'bg-line/60')
                }
              >
                {fini ? '✓' : q.icone}
              </span>
              <div className="min-w-0 flex-1">
                <p
                  className={
                    'truncate text-kid-sm font-bold ' + (fini ? 'text-muted line-through' : '')
                  }
                >
                  {q.texte}
                </p>
                <div
                  className={
                    'mt-1 h-2 overflow-hidden rounded-full bg-line ' + (fini ? 'pulse-or' : '')
                  }
                >
                  <div
                    className={
                      'h-full rounded-full transition-[width] duration-500 ' +
                      (fini ? 'bg-leaf' : 'bg-clay')
                    }
                    style={{ width: `${Math.round((q.fait / q.cible) * 100)}%` }}
                  />
                </div>
              </div>
              <span className="shrink-0 text-kid-xs font-black text-muted tabular-nums">
                {q.fait}/{q.cible}
              </span>
            </li>
          );
        })}
      </ul>
    </section>
  );
}

export function Trophees({ trophees }: { trophees: Trophee[] }) {
  const gagnes = trophees.filter((t) => t.obtenu).length;

  return (
    <section>
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-kid-lg font-extrabold">Mes trophées</h2>
        <span className="text-kid-sm font-bold text-muted">
          {gagnes} sur {trophees.length}
        </span>
      </div>
      <ul className="mt-3 grid grid-cols-3 gap-2 sm:grid-cols-5">
        {trophees.map((t) => (
          <li
            key={t.id}
            title={t.condition}
            className={
              'rounded-2xl border-2 px-2 py-3 text-center ' +
              (t.obtenu ? 'border-gold bg-gold/15' : 'border-line bg-line/25')
            }
          >
            <span
              aria-hidden="true"
              className={'block text-2xl ' + (t.obtenu ? '' : 'opacity-30 grayscale')}
            >
              {t.icone}
            </span>
            <p
              className={
                'mt-1 text-kid-xs leading-tight font-extrabold ' +
                (t.obtenu ? '' : 'text-muted')
              }
            >
              {t.obtenu ? t.nom : t.condition}
            </p>
          </li>
        ))}
      </ul>
    </section>
  );
}
