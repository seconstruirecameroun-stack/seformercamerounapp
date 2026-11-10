/**
 * Ce que le plateau de bonbons doit garantir.
 *
 * Une règle de jeu qui se trompe est une injustice que l'enfant subit sans
 * pouvoir la nommer : il voit des bonbons disparaître sans points, ou un
 * coup refusé sans raison, et il croit que c'est lui. Tout se vérifie donc
 * ici, hors du navigateur, avec un hasard tenu à la main.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/bonbons.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/bonbons.verif.mjs
 *   node ../work/bonbons.verif.mjs
 */

import {
  alignements,
  coupsPossibles,
  estVoisin,
  jouer,
  melangerPlateau,
  nouveauPlateau,
  objectifDuPlateau,
  pointsDeLExplosion,
  suggestion,
  VIDE,
  type Plateau,
} from './bonbons';

let echecs = 0;

function verifie(nom: string, condition: boolean) {
  if (condition) {
    console.log('  ok     ' + nom);
  } else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

/** Un hasard tenu à la main : la même suite à chaque exécution. */
function graine(n: number) {
  let etat = n >>> 0;
  return () => {
    etat = (etat * 1664525 + 1013904223) >>> 0;
    return etat / 4294967296;
  };
}

/** Un plateau écrit à la main, ligne par ligne, pour que le cas se lise. */
const P = (lignes: string[]): Plateau =>
  lignes.map((l) => [...l].map((c) => (c === '.' ? VIDE : Number(c))));

export function verifierBonbons(): number {
  // ── Les alignements ──────────────────────────────────────────────────────
  verifie(
    'alignement : trois en ligne sont pris',
    alignements(P(['11123', '21234', '32341'])).length === 3,
  );
  verifie(
    'alignement : deux en ligne ne suffisent pas',
    alignements(P(['11234', '21234', '32341'])).length === 0,
  );
  verifie(
    'alignement : trois en colonne sont pris',
    alignements(P(['12345', '12345', '12345'])).length === 15,
  );
  verifie(
    'alignement : cinq en ligne font cinq cases',
    alignements(P(['11111', '23452', '34523'])).length === 5,
  );

  // Un L : une ligne de trois et une colonne de trois qui se croisent. La
  // case du coin ne doit être comptée qu'une fois - sinon elle paie double.
  const enL = P(['111', '100', '100']);
  verifie('alignement : un L compte cinq cases, pas six', alignements(enL).length === 5);

  verifie(
    'alignement : les cases vides ne s’alignent pas',
    alignements(P(['...', '123', '231'])).length === 0,
  );

  // ── Le voisinage ─────────────────────────────────────────────────────────
  verifie('voisin : côte à côte', estVoisin({ l: 1, c: 1 }, { l: 1, c: 2 }));
  verifie('voisin : l’un sur l’autre', estVoisin({ l: 1, c: 1 }, { l: 2, c: 1 }));
  verifie('voisin : en diagonale, non', !estVoisin({ l: 1, c: 1 }, { l: 2, c: 2 }));
  verifie('voisin : la même case, non', !estVoisin({ l: 1, c: 1 }, { l: 1, c: 1 }));

  // ── Les coups ────────────────────────────────────────────────────────────
  // Échanger le 2 et le 1 de la première ligne aligne trois 1 en colonne 0.
  const avecCoup = P(['21345', '13452', '14523']);
  verifie('coup : un échange qui aligne est trouvé', coupsPossibles(avecCoup).length > 0);

  // Un plateau SANS AUCUN COUP, trouvé par recherche exhaustive sur quatre
  // lignes et cinq couleurs. Le damier à deux couleurs du premier jet n-en
  // était pas un : échanger deux cases voisines y aligne trois bonbons, et
  // le test échouait - à juste titre.
  const sansCoup = P(['3042', '2013', '3142', '2420']);
  verifie('coup : ce plateau-là n’offre aucun coup', coupsPossibles(sansCoup).length === 0);
  verifie('coup : et rien n’y est déjà aligné', alignements(sansCoup).length === 0);
  verifie('suggestion : rien à suggérer sans coup', suggestion(sansCoup) === null);
  verifie('suggestion : la même à chaque appel', JSON.stringify(suggestion(avecCoup)) ===
    JSON.stringify(suggestion(avecCoup)));

  // ── Jouer ────────────────────────────────────────────────────────────────
  const refuse = jouer(sansCoup, { a: { l: 0, c: 0 }, b: { l: 0, c: 1 } }, graine(1));
  verifie('jouer : un échange qui n’aligne rien est refusé', refuse === null);

  const loin = jouer(avecCoup, { a: { l: 0, c: 0 }, b: { l: 2, c: 4 } }, graine(1));
  verifie('jouer : deux cases qui ne se touchent pas, refusé', loin === null);

  // Un cas écrit pour être lisible : les trois 1 du haut s'alignent en
  // colonne 0 dès qu'on échange le 2 et le 1 de la première ligne.
  const simple = P(['21444', '13232', '14343', '23234', '34342']);
  const coup = { a: { l: 0, c: 0 }, b: { l: 0, c: 1 } };
  const joue = jouer(simple, coup, graine(7));
  verifie('jouer : le coup est accepté', joue !== null);
  if (joue) {
    verifie('jouer : au moins trois bonbons sautent', joue.bonbons >= 3);
    verifie('jouer : des points sont marqués', joue.points > 0);
    verifie('jouer : au moins une étape d’animation', joue.etapes.length >= 1);
    verifie(
      'jouer : le plateau rendu n’a plus aucun alignement',
      alignements(joue.plateau).length === 0,
    );
    verifie(
      'jouer : aucune case vide ne reste',
      joue.plateau.every((l) => l.every((c) => c !== VIDE)),
    );
    verifie(
      'jouer : le plateau garde sa taille',
      joue.plateau.length === simple.length && joue.plateau[0].length === simple[0].length,
    );
    verifie(
      'jouer : les points annoncés sont la somme des étapes',
      joue.points === joue.etapes.reduce((t, e) => t + e.points, 0),
    );
  }

  // ── Les points ───────────────────────────────────────────────────────────
  verifie('points : trois bonbons, première vague', pointsDeLExplosion(3, 1) === 30);
  verifie('points : la deuxième vague vaut double', pointsDeLExplosion(3, 2) === 60);
  verifie('points : cinq bonbons valent plus que trois',
    pointsDeLExplosion(5, 1) > pointsDeLExplosion(3, 1));

  // ── Le plateau de départ ─────────────────────────────────────────────────
  let sains = 0;
  for (let n = 0; n < 200; n++) {
    const p = nouveauPlateau(7, 7, graine(n + 1));
    if (alignements(p).length === 0 && coupsPossibles(p).length > 0) sains += 1;
  }
  verifie('départ : 200 plateaux sans alignement et tous jouables', sains === 200);

  const p0 = nouveauPlateau(7, 7, graine(42));
  verifie('départ : la taille demandée', p0.length === 7 && p0[0].length === 7);
  verifie(
    'départ : aucune case vide',
    p0.every((l) => l.every((c) => c !== VIDE)),
  );

  // ── Le mélange ───────────────────────────────────────────────────────────
  const compte = (p: Plateau) => {
    const n: Record<number, number> = {};
    for (const l of p) for (const c of l) n[c] = (n[c] ?? 0) + 1;
    return JSON.stringify(Object.entries(n).sort());
  };
  const remue = melangerPlateau(sansCoup, graine(3));
  verifie('mélange : aucun bonbon créé ni perdu', compte(remue) === compte(sansCoup));
  verifie('mélange : un coup redevient possible', coupsPossibles(remue).length > 0);
  verifie('mélange : rien n’est déjà aligné', alignements(remue).length === 0);

  // ── L’objectif ───────────────────────────────────────────────────────────
  verifie('objectif : dix questions valent 500', objectifDuPlateau(10) === 500);
  verifie('objectif : il monte avec les questions',
    objectifDuPlateau(30) > objectifDuPlateau(20));

  // ── Une partie entière, pour voir que rien ne se bloque ──────────────────
  const alea = graine(99);
  let partie = nouveauPlateau(7, 7, alea);
  let total = 0;
  let melanges = 0;
  for (let coups = 0; coups < 60; coups++) {
    let possibles = coupsPossibles(partie);
    if (possibles.length === 0) {
      partie = melangerPlateau(partie, alea);
      melanges += 1;
      possibles = coupsPossibles(partie);
    }
    const choisi = possibles[Math.floor(alea() * possibles.length)];
    const r = jouer(partie, choisi, alea);
    if (!r) break;
    partie = r.plateau;
    total += r.points;
  }
  verifie('partie : soixante coups sans blocage', total > 0);
  verifie('partie : le plateau tient toujours debout',
    alignements(partie).length === 0 && coupsPossibles(partie).length > 0);
  verifie('partie : les mélanges restent rares', melanges <= 5);

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
  return echecs;
}

verifierBonbons();
