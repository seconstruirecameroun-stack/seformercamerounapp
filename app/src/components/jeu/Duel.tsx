import type { Duel as DuelData } from '../../lib/duel';

/**
 * Le duel de la semaine.
 *
 * Il se lit en une seconde : deux visages, deux barres, un écart. L'enfant
 * doit savoir s'il mène ou s'il court, et de combien — un classement qu'il
 * faut déchiffrer ne fait courir personne.
 *
 * Le texte ne tombe jamais dans la moquerie du second. « Il te mène de 40 »
 * donne un chiffre à rattraper ; « tu es dernier » n'en donne aucun.
 */
export default function Duel({ duel, childId }: { duel: DuelData; childId: string }) {
  const max = Math.max(1, ...duel.concurrents.map((c) => c.etoiles));

  return (
    <section className="rounded-[var(--radius-card)] border border-line bg-white-warm/80 px-4 py-3">
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-kid-sm font-extrabold">Duel de la semaine</h2>
        <span className="shrink-0 text-kid-xs font-bold text-muted">
          {duel.joursRestants > 1 ? `${duel.joursRestants} jours restants` : 'dernier jour !'}
        </span>
      </div>

      <ul className="mt-2 grid gap-2">
        {duel.concurrents.map((c, rang) => {
          const moi = c.childId === childId;
          return (
            <li key={c.childId} className="flex items-center gap-3">
              <span
                className={
                  'grid h-9 w-9 shrink-0 place-items-center rounded-full text-base ' +
                  (moi ? 'bg-lilac' : 'bg-line/70')
                }
              >
                {c.avatar ?? c.prenom.slice(0, 1).toUpperCase()}
              </span>
              <div className="min-w-0 flex-1">
                <div className="flex items-baseline justify-between gap-2">
                  <p className={'truncate text-kid-sm ' + (moi ? 'font-black' : 'font-bold')}>
                    {c.prenom}
                    {rang === 0 && c.etoiles > 0 ? (
                      <span aria-label="en tête" className="ml-1">
                        👑
                      </span>
                    ) : null}
                  </p>
                  <span className="shrink-0 text-kid-xs font-black tabular-nums">{c.etoiles} ★</span>
                </div>
                <div className="mt-1 h-2.5 overflow-hidden rounded-full bg-line">
                  <div
                    className={
                      'h-full rounded-full transition-[width] duration-700 ' +
                      (moi ? 'bg-clay' : 'bg-gold')
                    }
                    style={{ width: `${Math.round((c.etoiles / max) * 100)}%` }}
                  />
                </div>
              </div>
            </li>
          );
        })}
      </ul>

      <p className="mt-2 text-kid-sm font-bold text-ink-2">
        {duel.exAequo && duel.enTete
          ? 'Vous êtes à égalité !'
          : duel.enTete
            ? 'Tu mènes. Garde ton avance !'
            : duel.ecart > 0
              ? `Il te mène de ${duel.ecart} ★. Rattrapable !`
              : 'La semaine commence. À toi de prendre la tête.'}
      </p>

      {duel.gagnantPasse ? (
        <p className="mt-1 text-kid-xs text-muted">
          La semaine dernière : {duel.gagnantPasse.prenom} avec {duel.gagnantPasse.etoiles} ★.
        </p>
      ) : null}
    </section>
  );
}
