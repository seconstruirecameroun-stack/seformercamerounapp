import Illustration from './Illustration';

/**
 * Le guide qui parle à l'enfant.
 *
 * Il n'apparaît que lorsqu'il a quelque chose à dire : une correction, un
 * encouragement, une explication. Un personnage présent en permanence devient
 * un décor qu'on ne lit plus.
 *
 * Le ton suit le fond, jamais l'inverse : on ne félicite pas une erreur avec
 * une couleur de réussite.
 */
export default function Guide({
  ton,
  children,
}: {
  ton: 'juste' | 'faux' | 'neutre';
  children: React.ReactNode;
}) {
  const bulle = {
    juste: 'border-leaf/40 bg-leaf/12',
    faux: 'border-clay/35 bg-clay/10',
    neutre: 'border-line bg-white-warm',
  }[ton];

  return (
    <div className="monte mt-5 flex items-end gap-3">
      <Illustration
        cle="guide"
        forme="portrait"
        alt=""
        className="h-20 w-auto shrink-0 drop-shadow-sm"
      />
      <div
        className={
          'relative flex-1 rounded-[var(--radius-tile)] border px-4 py-3 text-kid-sm leading-relaxed text-ink-2 ' +
          bulle
        }
      >
        <span
          aria-hidden="true"
          className={
            'absolute -left-[7px] bottom-5 h-3 w-3 rotate-45 border-b border-l ' + bulle
          }
        />
        {children}
      </div>
    </div>
  );
}
