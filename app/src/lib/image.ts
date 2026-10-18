/**
 * Prépare une illustration avant dépôt.
 *
 * Les images sorties d'un générateur font 1 à 2 Mo. Les envoyer telles quelles
 * reviendrait à faire payer une dizaine de méga-octets par leçon à une famille
 * facturée au volume. La réduction se fait donc ici, dans le navigateur du
 * parent, avant même que l'octet parte sur le réseau.
 *
 * Mêmes formats que les illustrations livrées avec l'app, pour que rien ne
 * détonne : voir DESIGN.md.
 */

export const FORMATS = {
  scene: { width: 960, height: 540 },
  objet: { width: 320, height: 320 },
} as const;

export type FormeImage = keyof typeof FORMATS;

export const POIDS_MAX_SOURCE = 12 * 1024 * 1024;

/** Recadre au centre, à la façon d'un object-fit: cover. */
function cadrage(sw: number, sh: number, dw: number, dh: number) {
  const echelle = Math.max(dw / sw, dh / sh);
  const w = sw * echelle;
  const h = sh * echelle;
  return { x: (dw - w) / 2, y: (dh - h) / 2, w, h };
}

export async function preparerIllustration(fichier: File, forme: FormeImage): Promise<Blob> {
  if (!fichier.type.startsWith('image/')) {
    throw new Error('Ce fichier n’est pas une image.');
  }
  if (fichier.size > POIDS_MAX_SOURCE) {
    throw new Error('Image trop lourde : 12 Mo au maximum.');
  }

  const { width, height } = FORMATS[forme];
  const source = await createImageBitmap(fichier);
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;

  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Le navigateur ne sait pas préparer l’image.');
  ctx.imageSmoothingQuality = 'high';

  const { x, y, w, h } = cadrage(source.width, source.height, width, height);
  ctx.drawImage(source, x, y, w, h);
  source.close();

  const blob = await new Promise<Blob | null>((resolve) =>
    canvas.toBlob(resolve, 'image/webp', 0.72),
  );
  // Un navigateur qui ignore WebP rend un PNG : il est plus lourd, mais mieux
  // vaut une image lourde qu'un dépôt impossible.
  if (!blob) throw new Error('Conversion impossible sur ce navigateur.');
  return blob;
}

/**
 * L'adresse d'un film de leçon.
 *
 * Deux colonnes peuvent la porter, pour une raison d'histoire : les premiers
 * films vivaient sur un CDN extérieur et ont gardé leur `external_url` en
 * passant dans le compartiment du projet, tandis que les suivants n'ont qu'un
 * `storage_path`.
 *
 * Le lecteur ne lisait que `external_url`. Un film correctement déposé mais
 * référencé par son chemin restait donc invisible dans la leçon — sans la
 * moindre erreur, ce qui est la pire façon de disparaître. Le chemin passe
 * d'abord : c'est la forme qui survit à un changement d'hébergement.
 */
export function urlFilm(
  video: { storage_path?: string | null; external_url?: string | null } | null | undefined,
  urlPublique: (chemin: string) => string,
): string | null {
  if (!video) return null;
  if (video.storage_path) return urlPublique(video.storage_path);
  return video.external_url ?? null;
}
