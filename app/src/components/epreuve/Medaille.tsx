import type { Metal } from '../../lib/recompenses';

/**
 * Une médaille : un ruban, un disque, une étoile, et un reflet qui passe.
 *
 * Tracée, comme Niba et Pango : elle reste nette à toutes les tailles, et
 * l'or, l'argent et le bronze ne sont que trois jeux de couleurs.
 */

const METAUX: Record<Metal, { clair: string; fonce: string; ruban: string; nom: string }> = {
  or: { clair: '#ffd84d', fonce: '#c9941a', ruban: '#d7443a', nom: 'Médaille d’or' },
  argent: { clair: '#eef1f5', fonce: '#9aa3ad', ruban: '#2f6db5', nom: 'Médaille d’argent' },
  bronze: { clair: '#f0ac72', fonce: '#a3622e', ruban: '#2f7d32', nom: 'Médaille de bronze' },
};

export function nomDuMetal(m: Metal): string {
  return METAUX[m].nom;
}

export default function Medaille({
  metal,
  taille = 96,
  terne = false,
  className = '',
}: {
  metal: Metal;
  taille?: number;
  /** Une médaille pas encore gagnée : on la montre, en gris, pour donner envie. */
  terne?: boolean;
  className?: string;
}) {
  const c = METAUX[metal];
  const id = 'reflet-' + metal + (terne ? '-terne' : '');
  return (
    <svg
      viewBox="0 0 100 120"
      width={taille}
      height={(taille * 120) / 100}
      className={className + (terne ? ' opacity-40 grayscale' : '')}
      aria-label={c.nom}
      role="img"
    >
      <defs>
        <clipPath id={id}>
          <circle cx={50} cy={72} r={34} />
        </clipPath>
      </defs>
      {/* Le ruban. */}
      <path d="M28 0 L44 44 L56 44 L40 0 Z" fill={c.ruban} />
      <path d="M72 0 L56 44 L44 44 L60 0 Z" fill={c.ruban} opacity={0.82} />
      {/* Le disque. */}
      <circle cx={50} cy={72} r={36} fill={c.fonce} />
      <circle cx={50} cy={72} r={30} fill={c.clair} stroke={c.fonce} strokeWidth={3} />
      <path
        d="M50 52 L56 66 L71 66 L59 75 L63 90 L50 81 L37 90 L41 75 L29 66 L44 66 Z"
        fill={c.fonce}
        opacity={0.85}
      />
      {/* Le reflet qui traverse le disque. */}
      {!terne ? (
        <g clipPath={`url(#${id})`}>
          <rect className="medaille-reflet" x={-40} y={30} width={18} height={90} fill="#fff" opacity={0.55} transform="rotate(20 50 72)" />
        </g>
      ) : null}
    </svg>
  );
}
