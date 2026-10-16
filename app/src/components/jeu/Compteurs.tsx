import type { EtatRang, Objectif, Serie } from '../../lib/jeu';

/**
 * Les trois compteurs qui tirent l'enfant : la série, l'objectif du jour, le
 * rang.
 *
 * Ils partagent un même principe : montrer ce qui manque, pas ce qui est
 * fait. « 3 jours de suite » n'appelle à rien ; « encore une leçon et ta
 * série tient » fait ouvrir l'app. Chaque compteur affiche donc un reste,
 * jamais un total seul.
 */

/** La flamme de la série. Éteinte, elle réclame ; allumée, elle se protège. */
export function Flamme({ serie, compact = false }: { serie: Serie; compact?: boolean }) {
  const vive = serie.joueAujourdhui && serie.jours > 0;
  return (
    <span
      className={
        'flex items-center gap-1.5 rounded-full px-3 py-2 text-kid-sm font-black ' +
        (vive ? 'bg-clay/20 text-clay-dark' : 'bg-line/60 text-muted')
      }
      title={
        vive
          ? `${serie.jours} jours de suite`
          : serie.jours > 0
            ? 'Joue aujourd’hui pour garder ta série'
            : 'Joue aujourd’hui pour démarrer ta série'
      }
    >
      <svg viewBox="0 0 24 24" width="18" height="18" className={vive ? 'flamme' : ''} aria-hidden="true">
        <path
          d="M12 2c3 4 5 6 5 10a5 5 0 0 1-10 0c0-1.6.6-2.8 1.4-3.8C9 10 10.5 8 12 2z"
          fill={vive ? 'var(--color-clay)' : 'var(--color-line)'}
        />
        <path
          d="M12 11c1.4 1.8 2.2 2.8 2.2 4.2a2.2 2.2 0 0 1-4.4 0c0-1.2.9-2.3 2.2-4.2z"
          fill={vive ? 'var(--color-gold)' : 'var(--color-white-warm)'}
        />
      </svg>
      {serie.jours}
      {compact ? null : <span className="sr-only"> jours de suite</span>}
    </span>
  );
}

/** L'anneau de l'objectif du jour : un cercle qu'on veut fermer. */
export function AnneauObjectif({ objectif, taille = 76 }: { objectif: Objectif; taille?: number }) {
  const r = 32;
  const tour = 2 * Math.PI * r;
  const reste = tour * (1 - objectif.part);

  return (
    <div className="relative shrink-0" style={{ width: taille, height: taille }}>
      <svg viewBox="0 0 80 80" width={taille} height={taille} aria-hidden="true">
        <circle cx="40" cy="40" r={r} fill="none" stroke="var(--color-line)" strokeWidth="8" />
        <circle
          cx="40"
          cy="40"
          r={r}
          fill="none"
          stroke={objectif.atteint ? 'var(--color-leaf)' : 'var(--color-gold)'}
          strokeWidth="8"
          strokeLinecap="round"
          strokeDasharray={tour}
          strokeDashoffset={reste}
          transform="rotate(-90 40 40)"
          className="anneau-actif"
          style={{ ['--depart' as string]: `${tour}` }}
        />
      </svg>
      <span className="absolute inset-0 grid place-items-center text-center leading-none">
        {objectif.atteint ? (
          <span className="text-kid-lg font-black text-leaf">✓</span>
        ) : (
          <span>
            <span className="block text-kid-base font-black">{objectif.gagnees}</span>
            <span className="block text-kid-xs font-bold text-muted">/ {objectif.cible}</span>
          </span>
        )}
      </span>
    </div>
  );
}

/** Le rang : la seule progression qui ne se perd jamais. */
export function BandeRang({ rang }: { rang: EtatRang }) {
  return (
    <div className="flex items-center gap-3">
      <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-gold/30 text-lg">
        🦁
      </span>
      <div className="min-w-0 flex-1">
        <div className="flex items-baseline justify-between gap-2">
          <p className="truncate text-kid-sm font-extrabold">{rang.rang.nom}</p>
          {rang.suivant ? (
            <p className="shrink-0 text-kid-xs font-bold text-muted">
              encore {rang.reste} ★
            </p>
          ) : (
            <p className="shrink-0 text-kid-xs font-bold text-gold">rang maximum</p>
          )}
        </div>
        <div className="mt-1.5 h-2.5 overflow-hidden rounded-full bg-line">
          <div
            className="h-full rounded-full bg-gold transition-[width] duration-700"
            style={{ width: `${Math.round(rang.part * 100)}%` }}
          />
        </div>
        {rang.suivant ? (
          <p className="mt-1 text-kid-xs text-muted">puis {rang.suivant.nom}</p>
        ) : null}
      </div>
    </div>
  );
}
