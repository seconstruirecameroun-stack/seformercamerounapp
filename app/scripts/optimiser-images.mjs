/**
 * Prépare pour le web un dossier d'images générées.
 *
 * Les sorties de Higgsfield pèsent 1 à 2 Mo chacune. Servies telles quelles,
 * une leçon coûterait une dizaine de méga-octets à l'enfant — rédhibitoire
 * sur une connexion camerounaise facturée au volume.
 *
 * Contrairement au premier script, celui-ci ne porte aucune table de
 * correspondance : le fichier s'appelle déjà comme la clé stockée en base
 * (« so-argileux.png » → « so-argileux.webp »), et le format se déduit de la
 * forme de l'image. Un import suivant n'a donc rien à modifier ici.
 *
 *   image en paysage → scène de leçon, 960 px de large
 *   image carrée     → vignette de notion, 320 px
 *
 * Usage :  node scripts/optimiser-images.mjs <dossier-source>
 *
 * Les sources restent hors du dépôt ; seules les sorties sont versionnées.
 */

import sharp from 'sharp';
import { readdir, stat } from 'node:fs/promises';
import { join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const ici = dirname(fileURLToPath(import.meta.url));
const SORTIE = join(ici, '..', 'public', 'illustrations');

const source = process.argv[2];
if (!source) {
  console.error('Usage : node scripts/optimiser-images.mjs <dossier-source>');
  process.exit(1);
}

const fichiers = (await readdir(source)).filter((f) => /\.(png|jpe?g|webp)$/i.test(f));
if (fichiers.length === 0) {
  console.error('Aucune image dans ' + source);
  process.exit(1);
}

let avant = 0;
let apres = 0;

for (const fichier of fichiers.sort()) {
  const cle = basename(fichier).replace(/\.[^.]+$/, '');
  if (!/^[a-z0-9-]+$/.test(cle)) {
    console.error(`  ${fichier} ignoré : le nom doit être la clé stockée en base`);
    continue;
  }

  const chemin = join(source, fichier);
  const image = sharp(chemin);
  const { width, height } = await image.metadata();
  const paysage = width / height > 1.2;

  // Le recadrage est centré : les modèles placent le sujet au milieu, et une
  // vignette qui coupe une tête est pire qu'une vignette un peu large.
  const sortie = join(SORTIE, cle + '.webp');
  await image
    .resize(
      paysage ? { width: 960, height: 540, fit: 'cover', position: 'centre' }
              : { width: 320, height: 320, fit: 'cover', position: 'centre' },
    )
    .webp({ quality: 82 })
    .toFile(sortie);

  avant += (await stat(chemin)).size;
  apres += (await stat(sortie)).size;
  console.log(`  ${cle.padEnd(18)} ${paysage ? 'scène ' : 'objet '} → ${(await stat(sortie)).size / 1024 | 0} ko`);
}

const ko = (n) => (n / 1024).toFixed(0) + ' ko';
console.log(`\n${fichiers.length} images : ${ko(avant)} → ${ko(apres)}`);
