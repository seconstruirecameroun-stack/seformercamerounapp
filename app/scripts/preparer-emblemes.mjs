/**
 * Prépare les emblèmes de rang pour l'app.
 *
 * Les médaillons sortent de la génération sur un fond carré, et chacun sur
 * une teinte légèrement différente. Posés tels quels dans l'app, on verrait
 * six carrés pastel qui jurent entre eux et avec la carte qui les porte.
 *
 * On découpe donc le disque et on jette le fond : un emblème détouré se pose
 * aussi bien sur une carte claire que dans une fenêtre de fête, et il garde
 * sa forme ronde quel que soit le conteneur.
 *
 * Usage :  node scripts/preparer-emblemes.mjs
 */

import { readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ici = dirname(fileURLToPath(import.meta.url));
const source = join(ici, '..', '..', 'work', 'rangs');
const cible = join(ici, '..', 'public', 'illustrations');

/** Côté final. 256 suffit : l'emblème ne dépasse jamais 112 px à l'écran. */
const COTE = 256;
/** Le disque occupe presque tout le carré, mais pas tout à fait : la
    génération laisse une marge fine qu'il vaut mieux ne pas rogner. */
const RAYON = 0.495;

const masque = Buffer.from(
  `<svg width="${COTE}" height="${COTE}">` +
    `<circle cx="${COTE / 2}" cy="${COTE / 2}" r="${COTE * RAYON}" fill="#fff"/>` +
    `</svg>`,
);

const fichiers = readdirSync(source).filter((f) => f.startsWith('rang-') && f.endsWith('.png'));
if (fichiers.length === 0) {
  console.error('Aucun emblème dans ' + source);
  process.exit(1);
}

for (const fichier of fichiers.sort()) {
  const sortie = join(cible, fichier.replace(/\.png$/, '.webp'));
  const info = await sharp(join(source, fichier))
    .resize(COTE, COTE, { fit: 'cover' })
    .composite([{ input: masque, blend: 'dest-in' }])
    .webp({ quality: 88 })
    .toFile(sortie);
  console.log(`${fichier.padEnd(26)} → ${(info.size / 1024).toFixed(1)} ko`);
}

console.log(`\n${fichiers.length} emblèmes prêts.`);
