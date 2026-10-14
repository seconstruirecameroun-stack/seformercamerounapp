/**
 * Une illustration de leçon ou de notion.
 *
 * La valeur stockée en base prend deux formes :
 *   'prehistoire-grotte'   → livrée avec l'app, servie depuis /illustrations
 *   'https://…'            → générée pour cette leçon, servie depuis le
 *                            stockage
 *
 * Les dimensions sont toujours posées pour que la page ne saute pas pendant
 * le chargement : sur une connexion lente, un bloc qui se décale fait rater
 * son clic à l'enfant.
 */

const FORMATS = {
  scene: { width: 960, height: 540 },
  objet: { width: 320, height: 320 },
  portrait: { width: 360, height: 540 },
} as const;

export type FormeIllustration = keyof typeof FORMATS;

export function sourceIllustration(cle: string | null | undefined): string | null {
  if (!cle) return null;
  if (cle.startsWith('http://') || cle.startsWith('https://')) return cle;
  if (!/^[a-z0-9-]+$/.test(cle)) return null;
  return `/illustrations/${cle}.webp`;
}

export default function Illustration({
  cle,
  forme,
  alt,
  className = '',
  priorite = false,
}: {
  cle: string | null | undefined;
  forme: FormeIllustration;
  alt: string;
  className?: string;
  priorite?: boolean;
}) {
  const src = sourceIllustration(cle);
  if (!src) return null;
  const { width, height } = FORMATS[forme];

  return (
    <img
      src={src}
      alt={alt}
      width={width}
      height={height}
      loading={priorite ? 'eager' : 'lazy'}
      decoding="async"
      className={className}
    />
  );
}
