import { useEffect, useRef, useState } from 'react';
import { jouerSon } from '../../lib/sons';

/**
 * Le coffre de fin de séance.
 *
 * Toute la séance tient déjà dans le récapitulatif ; le coffre n'ajoute
 * aucune information. Il ajoute une seconde d'attente, et un geste à faire.
 * C'est exactement ce qui manque à un bilan honnête pour qu'un enfant ait
 * envie d'en gagner un autre : le butin n'est pas affiché, il est ouvert.
 *
 * Il ne s'ouvre jamais tout seul. Un coffre qui s'ouvre sans qu'on y touche
 * n'est plus une récompense, c'est une notification.
 */

export type Butin = { icone: string; texte: string };

export default function Coffre({
  butin,
  titre,
  onOuvert,
}: {
  butin: Butin[];
  titre: string;
  /** Prévenu une fois le couvercle levé : la suite du bilan apparaît alors. */
  onOuvert?: () => void;
}) {
  const [etat, setEtat] = useState<'ferme' | 'ouvre' | 'ouvert'>('ferme');
  const minuteur = useRef<number[]>([]);

  useEffect(() => () => minuteur.current.forEach(clearTimeout), []);

  function ouvrir() {
    if (etat !== 'ferme') return;
    setEtat('ouvre');
    jouerSon('coffre');
    minuteur.current.push(
      window.setTimeout(() => {
        setEtat('ouvert');
        jouerSon('fete');
        onOuvert?.();
      }, 1400),
    );
  }

  if (etat === 'ouvert') {
    return (
      <div className="monte text-center">
        <p className="text-kid-lg font-black">{titre}</p>
        <ul className="mx-auto mt-3 grid max-w-xs gap-2">
          {butin.map((b, i) => (
            <li
              key={i}
              className="grimpe flex items-center gap-3 rounded-2xl bg-gold/20 px-4 py-2.5 text-left"
              style={{ animationDelay: `${i * 120}ms` }}
            >
              <span aria-hidden="true" className="text-xl">
                {b.icone}
              </span>
              <span className="text-kid-sm font-extrabold">{b.texte}</span>
            </li>
          ))}
        </ul>
      </div>
    );
  }

  return (
    <div className="text-center">
      <button
        type="button"
        onClick={ouvrir}
        disabled={etat === 'ouvre'}
        className="tuile mx-auto block rounded-3xl px-6 py-4"
        aria-label="Ouvrir ton coffre"
      >
        <span className="relative block">
          {etat === 'ouvre' ? (
            <span
              aria-hidden="true"
              className="eclate absolute inset-0 rounded-full bg-gold/60"
            />
          ) : null}
          <svg
            viewBox="0 0 120 100"
            width="128"
            height="107"
            className={'relative ' + (etat === 'ouvre' ? 'tremble' : '')}
            aria-hidden="true"
          >
            {/* Le couvercle, posé en premier : il doit passer sous la serrure. */}
            <path d="M14 46 a46 30 0 0 1 92 0 z" fill="var(--color-clay)" />
            <rect x="14" y="46" width="92" height="42" rx="8" fill="var(--color-clay-dark)" />
            <rect x="14" y="42" width="92" height="10" rx="5" fill="var(--color-gold)" />
            <rect x="52" y="38" width="16" height="22" rx="4" fill="var(--color-gold)" />
            <circle cx="60" cy="50" r="4" fill="var(--color-clay-dark)" />
          </svg>
        </span>
        <span className="mt-2 block text-kid-base font-black">
          {etat === 'ouvre' ? '…' : 'Ouvre ton coffre !'}
        </span>
      </button>
    </div>
  );
}

/**
 * Les confettis.
 *
 * Posés en position fixe et sans interception du pouce : ils tombent
 * par-dessus la fenêtre sans jamais empêcher d'appuyer sur le bouton qui est
 * dessous. Trente morceaux suffisent — au-delà, c'est une tempête de neige.
 */
export function Confettis({ nombre = 30 }: { nombre?: number }) {
  const [morceaux] = useState(() =>
    Array.from({ length: nombre }, () => ({
      gauche: Math.random() * 100,
      derive: Math.round((Math.random() - 0.5) * 160),
      duree: 1800 + Math.random() * 1400,
      retard: Math.random() * 500,
      tour: Math.round(360 + Math.random() * 720),
      taille: 6 + Math.random() * 7,
      couleur: ['var(--color-gold)', 'var(--color-clay)', 'var(--color-leaf)', 'var(--color-lilac)'][
        Math.floor(Math.random() * 4)
      ],
    })),
  );

  return (
    <div aria-hidden="true" className="pointer-events-none fixed inset-0 z-50 overflow-hidden">
      {morceaux.map((m, i) => (
        <span
          key={i}
          className="confetti absolute top-0 block"
          style={{
            left: `${m.gauche}%`,
            width: m.taille,
            height: m.taille * 0.6,
            background: m.couleur,
            borderRadius: 2,
            ['--derive' as string]: `${m.derive}px`,
            ['--duree' as string]: `${m.duree}ms`,
            ['--retard' as string]: `${m.retard}ms`,
            ['--tour' as string]: `${m.tour}deg`,
          }}
        />
      ))}
    </div>
  );
}
