/**
 * L'image qui s'affiche quand on partage le lien.
 *
 * Au Cameroun, une app de famille circule par WhatsApp. Un lien nu, sans
 * vignette, ressemble à un lien douteux — et personne ne l'ouvre. Cette image
 * est donc le premier contact avec l'app, avant même la page d'accueil.
 *
 * Elle est composée à partir de ce qui existe déjà : Niba, une vraie capture
 * de l'app, et la palette. Rien n'y est redessiné pour la circonstance.
 *
 * Usage :  node scripts/preparer-partage.mjs
 */

import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ici = dirname(fileURLToPath(import.meta.url));
const pub = join(ici, '..', 'public');

/** Le format attendu par WhatsApp, Facebook et les autres. */
const L = 1200;
const H = 630;

const C = { ink: '#1d3c42', ink2: '#3d5257', clay: '#e2813f', sand: '#fae5c8', papier: '#f7f3ea' };

const fond = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${L}" height="${H}">
  <defs>
    <linearGradient id="ciel" x1="0" y1="0" x2="0.3" y2="1">
      <stop offset="0" stop-color="#d7eaf4"/>
      <stop offset="1" stop-color="${C.papier}"/>
    </linearGradient>
    <pattern id="points" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.6" fill="${C.ink}" opacity="0.07"/>
    </pattern>
  </defs>
  <rect width="${L}" height="${H}" fill="url(#ciel)"/>
  <rect width="${L}" height="${H}" fill="url(#points)"/>
</svg>`);

// La police de l'app n'est pas installée sur la machine qui compose l'image :
// on s'en tient à une grotesque système, et on laisse les mots au minimum.
// Ce sont le lionceau et la capture qui doivent parler ici.
const POLICE = 'Segoe UI, Noto Sans, DejaVu Sans, sans-serif';

const texte = Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${L}" height="${H}">
  <text x="80" y="214" font-family="${POLICE}" font-size="34" font-weight="700" fill="${C.clay}">
    SE FORMER CAMEROUN
  </text>
  <text x="80" y="300" font-family="${POLICE}" font-size="62" font-weight="800" fill="${C.ink}">
    Les leçons du cahier,
  </text>
  <text x="80" y="372" font-family="${POLICE}" font-size="62" font-weight="800" fill="${C.ink}">
    révisées en jouant.
  </text>
  <text x="80" y="438" font-family="${POLICE}" font-size="30" font-weight="400" fill="${C.ink2}">
    Vous photographiez le cours.
  </text>
  <text x="80" y="480" font-family="${POLICE}" font-size="30" font-weight="400" fill="${C.ink2}">
    Votre enfant y revient de lui-même.
  </text>
</svg>`);

const niba = readFileSync(join(pub, 'niba.svg'));

// La capture, dans son cadre, posée à droite et débordant légèrement du bas :
// on reconnaît un téléphone sans avoir à en dessiner un entier.
const ecran = await sharp(join(pub, 'apercu', 'accueil.webp')).resize(330).toBuffer();
const cadre = await sharp({
  create: { width: 350, height: 470, channels: 4, background: C.ink },
})
  .composite([{ input: ecran, left: 10, top: 10 }])
  .png()
  .toBuffer();
const cadreArrondi = await sharp(cadre)
  .composite([
    {
      input: Buffer.from(
        `<svg width="350" height="470"><rect width="350" height="470" rx="34" fill="#fff"/></svg>`,
      ),
      blend: 'dest-in',
    },
  ])
  .png()
  .toBuffer();

const info = await sharp(fond)
  .composite([
    { input: texte, left: 0, top: 0 },
    { input: await sharp(niba, { density: 400 }).resize(96, 96).png().toBuffer(), left: 80, top: 86 },
    { input: cadreArrondi, left: 790, top: 120 },
  ])
  .png()
  .toFile(join(pub, 'partage.png'));

console.log(`partage.png  ${L}×${H}  ${(info.size / 1024).toFixed(0)} ko`);
