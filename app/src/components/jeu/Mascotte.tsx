import { useEffect, useState } from 'react';

/**
 * Niba, le lionceau.
 *
 * Un enfant ne s'attache pas à une barre de progression ; il s'attache à
 * quelqu'un. Niba est le seul élément de l'app qui s'adresse à l'enfant à la
 * première personne, et le seul qui change d'humeur selon ce qui vient de se
 * passer. C'est lui qui dit « tu m'as manqué » après trois jours d'absence —
 * une phrase qu'aucune statistique ne peut remplacer.
 *
 * Le lion, parce qu'au Cameroun un enfant sait ce qu'est un Lion indomptable
 * avant de savoir lire. Un lionceau, parce qu'il grandit avec lui.
 *
 * Dessiné en SVG et non généré en image : il doit cligner des yeux, changer
 * d'expression et rester net du pouce au grand écran, sans peser un octet de
 * réseau ni coûter une génération à chaque nouvelle humeur.
 */

export type Humeur = 'content' | 'fete' | 'encourage' | 'manque' | 'dort';

export default function Mascotte({
  humeur = 'content',
  taille = 96,
  className = '',
}: {
  humeur?: Humeur;
  taille?: number;
  className?: string;
}) {
  const [cligne, setCligne] = useState(false);

  // Un clignement irrégulier : à intervalle fixe, l'œil devient un métronome
  // et le personnage a l'air mécanique.
  useEffect(() => {
    if (humeur === 'dort' || humeur === 'fete') return;
    let timer: number;
    const programmer = () => {
      timer = window.setTimeout(
        () => {
          setCligne(true);
          window.setTimeout(() => setCligne(false), 140);
          programmer();
        },
        2600 + Math.random() * 3200,
      );
    };
    programmer();
    return () => window.clearTimeout(timer);
  }, [humeur]);

  const yeuxFermes = cligne || humeur === 'dort' || humeur === 'fete';

  return (
    <svg
      viewBox="0 0 120 120"
      width={taille}
      height={taille}
      className={className}
      role="img"
      aria-label="Niba, le lionceau"
    >
      {/* La crinière : neuf pétales arrondis, décalés pour ne pas faire roue. */}
      <g>
        {Array.from({ length: 9 }, (_, i) => {
          const angle = (i / 9) * Math.PI * 2 - Math.PI / 2;
          const r = 36;
          return (
            <circle
              key={i}
              cx={60 + Math.cos(angle) * r}
              cy={62 + Math.sin(angle) * r}
              r={16}
              fill={i % 2 === 0 ? 'var(--color-clay)' : 'var(--color-gold)'}
            />
          );
        })}
      </g>

      {/* Les oreilles. Posées assez loin du centre pour dépasser de la face,
          qui est dessinée juste après : plus près, il n'en resterait qu'un
          croissant invisible à la taille d'une vignette. */}
      <circle cx="28" cy="33" r="12" fill="var(--color-clay-dark)" />
      <circle cx="92" cy="33" r="12" fill="var(--color-clay-dark)" />
      <circle cx="28" cy="33" r="6" fill="var(--color-sand)" />
      <circle cx="92" cy="33" r="6" fill="var(--color-sand)" />

      <circle cx="60" cy="62" r="34" fill="var(--color-sand)" />

      {/* Les yeux. Fermés, ce sont deux arcs tournés vers le haut : c'est la
          différence entre un personnage qui dort et un personnage qui rit. */}
      {yeuxFermes ? (
        <>
          <path
            d={humeur === 'dort' ? 'M40 58 q7 5 14 0' : 'M40 60 q7 -8 14 0'}
            stroke="var(--color-ink)"
            strokeWidth="3.5"
            strokeLinecap="round"
            fill="none"
          />
          <path
            d={humeur === 'dort' ? 'M66 58 q7 5 14 0' : 'M66 60 q7 -8 14 0'}
            stroke="var(--color-ink)"
            strokeWidth="3.5"
            strokeLinecap="round"
            fill="none"
          />
        </>
      ) : (
        <>
          <circle cx="47" cy="58" r="5" fill="var(--color-ink)" />
          <circle cx="73" cy="58" r="5" fill="var(--color-ink)" />
          <circle cx="48.8" cy="56.2" r="1.8" fill="var(--color-white-warm)" />
          <circle cx="74.8" cy="56.2" r="1.8" fill="var(--color-white-warm)" />
        </>
      )}

      {/* Les sourcils ne servent qu'à l'inquiétude : ailleurs, ils durcissent
          le visage sans rien ajouter. */}
      {humeur === 'manque' ? (
        <>
          <path d="M40 47 q7 -4 13 -1" stroke="var(--color-ink-2)" strokeWidth="3" strokeLinecap="round" fill="none" />
          <path d="M67 46 q6 -3 13 1" stroke="var(--color-ink-2)" strokeWidth="3" strokeLinecap="round" fill="none" />
        </>
      ) : null}

      {/* Museau */}
      <ellipse cx="60" cy="72" rx="13" ry="9" fill="var(--color-white-warm)" />
      <path d="M55 69 q5 -4 10 0 q-5 5 -10 0" fill="var(--color-clay-dark)" />

      {/* La bouche porte l'humeur à elle seule. */}
      <path
        d={
          humeur === 'manque'
            ? 'M52 83 q8 -5 16 0'
            : humeur === 'fete'
              ? 'M50 78 q10 12 20 0 q-10 5 -20 0'
              : humeur === 'dort'
                ? 'M55 80 q5 3 10 0'
                : 'M52 78 q8 7 16 0'
        }
        fill={humeur === 'fete' ? 'var(--color-clay-dark)' : 'none'}
        stroke="var(--color-ink)"
        strokeWidth="3"
        strokeLinecap="round"
      />

      {/* Les moustaches : trois traits qui suffisent à dire « félin ». */}
      <g stroke="var(--color-ink-2)" strokeWidth="2" strokeLinecap="round" opacity="0.55">
        <path d="M34 68 h10" />
        <path d="M34 75 h10" />
        <path d="M86 68 h-10" />
        <path d="M86 75 h-10" />
      </g>

      {humeur === 'dort' ? (
        <text x="92" y="30" fontSize="16" fontWeight="800" fill="var(--color-ink-2)">
          z
        </text>
      ) : null}
    </svg>
  );
}
