/**
 * Vérifications du mélange des choix.
 *
 *   npx esbuild src/lib/melange.verif.ts --bundle --platform=node \
 *     --outfile=node_modules/.cache/melange.verif.cjs --format=cjs \
 *     && node node_modules/.cache/melange.verif.cjs
 */

import { melanger } from './melange';

let ko = 0;
const ok = (nom: string, vrai: boolean) => {
  if (!vrai) {
    ko += 1;
    console.log('KO  ' + nom);
  }
};

// Une permutation, et rien d'autre : aucun choix perdu, aucun en double.
for (const n of [1, 2, 3, 4, 8]) {
  let bon = true;
  for (let essai = 0; essai < 2000; essai++) {
    const o = melanger(n);
    if (o.length !== n) bon = false;
    if (new Set(o).size !== n) bon = false;
    if (o.some((v) => v < 0 || v >= n || !Number.isInteger(v))) bon = false;
  }
  ok('permutation valide pour n=' + n, bon);
}

// Le point de départ : la bonne réponse est l'index 0 dans toute la base.
// Elle doit tomber à peu près aussi souvent à chaque place, sinon on a
// simplement déplacé l'habitude.
for (const n of [2, 3, 4]) {
  const places = new Array<number>(n).fill(0);
  const tirages = 60000;
  for (let i = 0; i < tirages; i++) places[melanger(n).indexOf(0)] += 1;
  const attendu = tirages / n;
  const pire = Math.max(...places.map((p) => Math.abs(p - attendu) / attendu));
  ok('n=' + n + ' : la bonne réponse se répartit (écart max ' + (100 * pire).toFixed(1) + '%)', pire < 0.05);
}

// Et elle ne doit pas non plus éviter la première place : « jamais celle du
// dessus » serait une habitude de plus.
const premiere = Array.from({ length: 20000 }, () => melanger(4)).filter((o) => o[0] === 0).length;
ok('la première place reste possible', premiere > 20000 / 4 - 500 && premiere < 20000 / 4 + 500);

// Deux questions de suite ne doivent pas sortir le même ordre.
const differents = new Set(Array.from({ length: 200 }, () => melanger(4).join(''))).size;
ok("l'ordre change d'une question à l'autre", differents > 10);

if (ko > 0) throw new Error(ko + ' echec(s)');
console.log('melange : 10 verifications, tout passe');
