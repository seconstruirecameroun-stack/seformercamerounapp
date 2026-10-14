import { useEffect, useRef } from 'react';
import type { ReactNode } from 'react';

/**
 * La fenêtre de retour, à la manière des jeux.
 *
 * Elle occupe l'écran une seconde, dit ce qui vient de se passer, puis rend la
 * main. Un message posé en bas de page se lit distraitement ; une fenêtre qui
 * s'ouvre se regarde.
 *
 * Trois règles de tenue :
 *  - un seul bouton, large, sous le pouce : il n'y a jamais de choix à faire ;
 *  - le fond se ferme aussi, et Échap également, pour ne jamais coincer ;
 *  - la couleur vient du résultat, pas de la décoration.
 */

export type TonPopup = 'juste' | 'faux' | 'fete';

export default function Popup({
  ton,
  titre,
  vignette,
  action = 'Continuer',
  onFermer,
  children,
}: {
  ton: TonPopup;
  titre: string;
  vignette?: ReactNode;
  action?: string;
  onFermer: () => void;
  children?: ReactNode;
}) {
  const bouton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    bouton.current?.focus();
    const auClavier = (e: KeyboardEvent) => {
      if (e.key === 'Escape' || e.key === 'Enter') onFermer();
    };
    window.addEventListener('keydown', auClavier);
    return () => window.removeEventListener('keydown', auClavier);
  }, [onFermer]);

  const couleurs = {
    juste: { bandeau: 'bg-leaf', texte: 'text-white-warm', bouton: 'bg-leaf shadow-[0_3px_0_oklch(0.5_0.09_150)]' },
    faux: { bandeau: 'bg-clay', texte: 'text-white-warm', bouton: 'bg-clay shadow-[0_3px_0_var(--color-clay-dark)]' },
    fete: { bandeau: 'bg-gold', texte: 'text-ink', bouton: 'bg-clay shadow-[0_3px_0_var(--color-clay-dark)]' },
  }[ton];

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center bg-ink/55 p-4 sm:items-center"
      onClick={onFermer}
      role="presentation"
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={titre}
        onClick={(e) => e.stopPropagation()}
        className="surgit w-full max-w-sm overflow-hidden rounded-[28px] bg-white-warm shadow-[0_24px_60px_oklch(0.3_0.045_205_/_0.35)]"
      >
        {vignette ? (
          <div className="flex justify-center bg-sand/70 pt-5">
            <div className="halo revele overflow-hidden rounded-3xl border-4 border-white-warm">
              {vignette}
            </div>
          </div>
        ) : null}

        <div className={'px-5 py-3 text-center ' + couleurs.bandeau}>
          <p className={'text-kid-xl font-black ' + couleurs.texte}>{titre}</p>
        </div>

        {children ? (
          <div className="px-5 py-4 text-center text-kid-sm leading-relaxed text-ink-2">
            {children}
          </div>
        ) : null}

        <div className="px-5 pb-5">
          <button
            ref={bouton}
            type="button"
            onClick={onFermer}
            className={
              'tuile min-h-[54px] w-full rounded-full text-kid font-extrabold text-white-warm ' +
              couleurs.bouton
            }
          >
            {action}
          </button>
        </div>
      </div>
    </div>
  );
}
