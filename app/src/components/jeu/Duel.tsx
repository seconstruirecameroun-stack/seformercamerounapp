import { BONUS_MANCHE_DUEL, type Duel as DuelData } from '../../lib/duel';

/**
 * Le duel de la semaine.
 *
 * Il se lit en une seconde : deux visages, deux barres, un écart. L'enfant
 * doit savoir s'il mène ou s'il court, et de combien — un classement qu'il
 * faut déchiffrer ne fait courir personne.
 *
 * L'écart est annoncé en questions, l'unité que l'enfant peut rattraper :
 * « il te mène de 4 questions » dit exactement quoi faire ce soir, ce qu'un
 * écart en points ne dit pas.
 *
 * Le texte ne tombe jamais dans la moquerie du second. Un chiffre à
 * rattraper appelle ; « tu es dernier » n'appelle à rien.
 *
 * Le détail du total est montré dès qu'une série sans faute y entre. Un
 * bonus qui tombe sans explication ne récompense rien : l'enfant doit voir
 * d'où vient son avance pour savoir comment la refaire.
 */
export default function Duel({ duel, childId }: { duel: DuelData; childId: string }) {
  const max = Math.max(1, ...duel.concurrents.map((c) => c.reussites));

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
                    {rang === 0 && c.reussites > 0 ? (
                      <span aria-label="en tête" className="ml-1">
                        👑
                      </span>
                    ) : null}
                  </p>
                  <span className="shrink-0 text-kid-xs font-black tabular-nums">
                    {c.reussites}{' '}
                    <span className="font-bold text-muted">
                      réussie{c.reussites > 1 ? 's' : ''}
                    </span>
                  </span>
                </div>
                <div className="mt-1 h-2.5 overflow-hidden rounded-full bg-line">
                  <div
                    className={
                      'h-full rounded-full transition-[width] duration-700 ' +
                      (moi ? 'bg-clay' : 'bg-gold')
                    }
                    style={{ width: `${Math.round((c.reussites / max) * 100)}%` }}
                  />
                </div>
                {c.manches > 0 ? (
                  <p className="mt-0.5 text-kid-xs text-muted">
                    {c.questions} question{c.questions > 1 ? 's' : ''} et {c.manches} série
                    {c.manches > 1 ? 's' : ''} sans faute
                  </p>
                ) : null}
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
              ? `Il te mène de ${duel.ecart} question${duel.ecart > 1 ? 's' : ''}. Rattrapable !`
              : 'La semaine commence. À toi de prendre la tête.'}
      </p>

      {duel.concurrents.some((c) => c.manches > 0) ? (
        <p className="mt-1 text-kid-xs text-muted">
          Une série sans faute vaut {BONUS_MANCHE_DUEL} questions.
        </p>
      ) : null}

      {duel.gagnantPasse ? (
        <p className="mt-1 text-kid-xs text-muted">
          La semaine dernière : {duel.gagnantPasse.prenom}, {duel.gagnantPasse.reussites} question
          {duel.gagnantPasse.reussites > 1 ? 's' : ''} réussie
          {duel.gagnantPasse.reussites > 1 ? 's' : ''}.
        </p>
      ) : null}
    </section>
  );
}
