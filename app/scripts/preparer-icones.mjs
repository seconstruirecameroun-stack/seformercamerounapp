/**
 * Les icônes de l'app, dessinées à partir de Niba.
 *
 * L'icône posée sur l'écran d'accueil du téléphone est le premier rappel,
 * celui qui agit sans notification : un enfant qui voit le lionceau entre
 * deux applications y pense. Elle mérite donc le même personnage que l'app,
 * et non un logo de plus.
 *
 * Les couleurs sont écrites en hexadécimal et non en OKLCH comme la feuille
 * de style : le moteur de rendu des SVG ne connaît pas encore OKLCH, et une
 * icône muette vaut mieux qu'une icône noire.
 *
 * Usage :  node scripts/preparer-icones.mjs
 */

import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const ici = dirname(fileURLToPath(import.meta.url));
const cible = join(ici, '..', 'public');

const C = {
  clay: '#e2813f',
  gold: '#f2c14e',
  clayDark: '#c2652f',
  sand: '#fae5c8',
  ink: '#1d3c42',
  blanc: '#fffcf6',
};

/** `marge` réserve le bord que les lanceurs Android rognent sur une icône maskable. */
function niba(marge) {
  const petales = Array.from({ length: 9 }, (_, i) => {
    const a = (i / 9) * Math.PI * 2 - Math.PI / 2;
    return `<circle cx="${(60 + Math.cos(a) * 36).toFixed(2)}" cy="${(62 + Math.sin(a) * 36).toFixed(2)}" r="16" fill="${i % 2 ? C.gold : C.clay}"/>`;
  }).join('\n    ');

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="512" height="512">
  <defs><linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#cfe6f2"/><stop offset="1" stop-color="#f7e9d2"/>
  </linearGradient></defs>
  <rect width="120" height="120" fill="url(#ciel)"/>
  <g transform="translate(60 61) scale(${(1 - marge).toFixed(2)}) translate(-60 -62)">
    ${petales}
    <circle cx="28" cy="33" r="12" fill="${C.clayDark}"/><circle cx="92" cy="33" r="12" fill="${C.clayDark}"/>
    <circle cx="28" cy="33" r="6" fill="${C.sand}"/><circle cx="92" cy="33" r="6" fill="${C.sand}"/>
    <circle cx="60" cy="62" r="34" fill="${C.sand}"/>
    <path d="M40 60 q7 -8 14 0" stroke="${C.ink}" stroke-width="3.5" stroke-linecap="round" fill="none"/>
    <path d="M66 60 q7 -8 14 0" stroke="${C.ink}" stroke-width="3.5" stroke-linecap="round" fill="none"/>
    <ellipse cx="60" cy="72" rx="13" ry="9" fill="${C.blanc}"/>
    <path d="M55 69 q5 -4 10 0 q-5 5 -10 0" fill="${C.clayDark}"/>
    <path d="M50 78 q10 12 20 0 q-10 5 -20 0" fill="${C.clayDark}" stroke="${C.ink}" stroke-width="3" stroke-linecap="round"/>
    <g stroke="${C.ink}" stroke-width="2" stroke-linecap="round" opacity="0.5">
      <path d="M34 68 h10"/><path d="M34 75 h10"/><path d="M86 68 h-10"/><path d="M86 75 h-10"/>
    </g>
  </g>
</svg>`;
}

for (const [nom, taille, marge] of [
  ['icone-192', 192, 0],
  ['icone-512', 512, 0],
  ['icone-maskable', 512, 0.22],
]) {
  const info = await sharp(Buffer.from(niba(marge)), { density: 600 })
    .resize(taille, taille)
    .png()
    .toFile(join(cible, nom + '.png'));
  console.log(`${nom}.png`.padEnd(22) + `${(info.size / 1024).toFixed(1)} ko`);
}

writeFileSync(join(cible, 'niba.svg'), niba(0) + '\n');
console.log('niba.svg'.padEnd(22) + 'pour la notification');
