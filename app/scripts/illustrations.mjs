/**
 * Prépare les illustrations de leçon pour le web.
 *
 * Les images sorties de Higgsfield pèsent 1,3 à 2 Mo chacune. Servies telles
 * quelles, une seule leçon coûterait une dizaine de méga-octets à l'enfant.
 * Sur une connexion camerounaise facturée au volume, c'est rédhibitoire.
 *
 * Ce script les redimensionne et les convertit en WebP :
 *   scènes 16:9  → 960 px de large
 *   objets  1:1  → 320 px, recadrés au centre si la source ne l'est pas
 *
 * Usage :  node scripts/illustrations.mjs <dossier-source>
 *
 * Les sources restent hors du dépôt ; seules les sorties optimisées sont
 * versionnées, dans public/illustrations.
 */

import sharp from 'sharp';
import { mkdir, readdir, stat } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ici = dirname(fileURLToPath(import.meta.url));
const SORTIE = join(ici, '..', 'public', 'illustrations');

/** nom de sortie → fragment reconnaissable du fichier source, et format. */
const PLAN = {
  // Scènes : bandeau de leçon.
  'prehistoire-grotte': { src: '42632d', forme: 'scene' },
  'prehistoire-village': { src: '2f72f6', forme: 'scene' },
  'prehistoire-metaux': { src: 'e5a3d7', forme: 'scene' },
  'prehistoire-ecriture': { src: 'a988b7', forme: 'scene' },
  // L'affiche du film : 22,8 Mo à la source, montrée avant même qu'on le lance.
  'prehistoire-film': { src: 'e508850', forme: 'scene' },

  // Objets : vignette de notion.
  'roue-memoire': { src: 'ba4191', forme: 'objet' },
  'biface': { src: '2197cd', forme: 'objet' },
  'chasse-peche-cueillette': { src: '6af4c6', forme: 'objet' },
  'hache-ble': { src: '43ff82', forme: 'objet' },
  'metaux': { src: '903ca4', forme: 'objet' },
  'tablette-ecriture': { src: 'a988b7', forme: 'objet' },
  'trois-epoques': { src: 'e21f749f', forme: 'objet' },

  // Récompense et repos : elles remplacent la roue-mémoire, qui servait
  // partout à défaut de mieux.
  'medaille': { src: '3d6a0df8', forme: 'objet' },
  'repos': { src: '2b149718', forme: 'objet' },

  // Le guide qui accompagne l'enfant.
  'guide': { src: '8ae114', forme: 'portrait' },
};

const TAILLES = {
  scene: { width: 960, height: 540 },
  objet: { width: 320, height: 320 },
  portrait: { width: 360, height: 540 },
};

const source = process.argv[2];
if (!source) {
  console.error('Usage : node scripts/illustrations.mjs <dossier-source>');
  process.exit(1);
}

await mkdir(SORTIE, { recursive: true });
const fichiers = (await readdir(source)).filter((f) => f.endsWith('.png'));

let total = 0;
for (const [nom, { src, forme }] of Object.entries(PLAN)) {
  const fichier = fichiers.find((f) => f.includes(src));
  if (!fichier) {
    console.warn(`  ! source introuvable pour ${nom} (${src})`);
    continue;
  }
  const dest = join(SORTIE, nom + '.webp');
  await sharp(join(source, fichier))
    .resize({ ...TAILLES[forme], fit: 'cover', position: 'attention' })
    .webp({ quality: 72, effort: 6 })
    .toFile(dest);
  const { size } = await stat(dest);
  total += size;
  console.log(`  ${nom.padEnd(26)} ${(size / 1024).toFixed(0).padStart(4)} ko`);
}

console.log(`\n${Object.keys(PLAN).length} illustrations · ${(total / 1024).toFixed(0)} ko au total`);
