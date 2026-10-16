/**
 * Les icônes du jeu.
 *
 * Dessinées ici plutôt que prises dans les émojis du système : un émoji
 * change de dessin d'un téléphone à l'autre, ne connaît pas la palette de
 * l'app, et sur certains appareils ne s'affiche pas du tout — un trophée
 * remplacé par un carré vide ne récompense rien.
 *
 * Toutes partagent la même grammaire : un trait épais, des bouts arrondis,
 * deux couleurs au plus, et aucun détail en dessous de deux pixels. C'est ce
 * qui les rend lisibles à la taille d'une vignette.
 */

export type NomIcone =
  | 'image'
  | 'collection'
  | 'album'
  | 'echelle'
  | 'flamme'
  | 'etoile'
  | 'chrono'
  | 'eclair'
  | 'livres'
  | 'coche';

export default function Icone({
  nom,
  taille = 24,
  className = '',
}: {
  nom: NomIcone;
  taille?: number;
  className?: string;
}) {
  const commun = {
    width: taille,
    height: taille,
    viewBox: '0 0 32 32',
    className,
    'aria-hidden': true as const,
  };
  const trait = {
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 2.4,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
  };

  switch (nom) {
    case 'image':
      return (
        <svg {...commun}>
          <rect x="4" y="6" width="24" height="20" rx="4" {...trait} />
          <circle cx="12" cy="13" r="2.4" fill="currentColor" />
          <path d="M6 22l6-6 5 5 4-3 5 4" {...trait} />
        </svg>
      );
    case 'collection':
      // Un canari : le pot à images, et un objet que l'enfant reconnaît chez lui.
      return (
        <svg {...commun}>
          <path d="M10 8h12l-1.5 4a8 8 0 1 1-9 0z" {...trait} />
          <path d="M9 8h14" {...trait} />
          <path d="M13 19h6" {...trait} />
        </svg>
      );
    case 'album':
      return (
        <svg {...commun}>
          <path d="M6 6h16a4 4 0 0 1 4 4v16H10a4 4 0 0 1-4-4z" {...trait} />
          <path d="M6 22a4 4 0 0 1 4-4h16" {...trait} />
          <path d="M14 11h6" {...trait} />
        </svg>
      );
    case 'echelle':
      return (
        <svg {...commun}>
          <path d="M10 28V4M22 28V4" {...trait} />
          <path d="M10 10h12M10 16h12M10 22h12" {...trait} />
        </svg>
      );
    case 'flamme':
      return (
        <svg {...commun}>
          <path d="M16 3c4 5 7 8 7 12a7 7 0 0 1-14 0c0-2.2.9-3.9 2-5.2 1.6 1 2.3 2.2 2.3 2.2C13 8 14.5 6 16 3z" {...trait} />
        </svg>
      );
    case 'etoile':
      return (
        <svg {...commun}>
          <path d="M16 4l3.7 7.6 8.3 1.2-6 5.9 1.4 8.3L16 23l-7.4 4 1.4-8.3-6-5.9 8.3-1.2z" {...trait} />
        </svg>
      );
    case 'chrono':
      return (
        <svg {...commun}>
          <circle cx="16" cy="18" r="11" {...trait} />
          <path d="M16 12v6l4 3" {...trait} />
          <path d="M12 4h8" {...trait} />
        </svg>
      );
    case 'eclair':
      return (
        <svg {...commun}>
          <path d="M18 3L7 18h8l-2 11 11-15h-8z" {...trait} />
        </svg>
      );
    case 'livres':
      return (
        <svg {...commun}>
          <path d="M5 7h8a3 3 0 0 1 3 3v15a3 3 0 0 0-3-3H5z" {...trait} />
          <path d="M27 7h-8a3 3 0 0 0-3 3v15a3 3 0 0 1 3-3h8z" {...trait} />
        </svg>
      );
    case 'coche':
      return (
        <svg {...commun}>
          <path d="M6 17l6 6L26 9" {...trait} />
        </svg>
      );
  }
}
