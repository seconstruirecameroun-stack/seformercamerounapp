/**
 * Ce que la course doit garantir.
 *
 * L'enfant ne conduit pas : ce sont ses réponses qui décident. Il faut donc
 * vérifier que la course dit vrai — que les bonnes réponses font avancer,
 * qu'une erreur coûte un choc et un seul, et que sans erreur la voiture ne
 * touche jamais rien.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/course.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/course.verif.mjs
 *   node ../work/course.verif.mjs
 */

import {
  DUREE_CHOC,
  VITESSE_NORMALE,
  VITESSE_TURBO,
  VILLES,
  avancer,
  choixDuPilote,
  donnerBouclier,
  donnerErreur,
  donnerTurbo,
  etape,
  nouvelEtat,
  paysage,
  rangee,
  type Etat,
  type Evenement,
} from './course';

let echecs = 0;
function verifie(nom: string, condition: boolean) {
  if (condition) console.log('  ok     ' + nom);
  else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

/** Un hasard figé : la même graine rejoue la même route. */
function alea(graine: number) {
  let s = graine >>> 0;
  return () => {
    s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

function rouler(e: Etat, secondes: number, a: () => number) {
  const evenements: Evenement[] = [];
  for (let t = 0; t < secondes; t += 1 / 60) {
    const r = avancer(e, 1 / 60, a);
    e = r.etat;
    evenements.push(...r.evenements);
  }
  return { e, evenements };
}

// ── La route laisse toujours une voie libre ─────────────────────────────────
let libre = true;
const a = alea(7);
for (let i = 0; i < 3000; i++) {
  const r = rangee(100 + i * 20, 5000, a, 1);
  const bloquees = new Set(r.filter((o) => o.type === 'obstacle').map((o) => o.voie));
  if (bloquees.size >= 3) libre = false;
  if (r.some((o) => o.type === 'piece' && bloquees.has(o.voie))) libre = false;
}
verifie('route : jamais trois obstacles de front', libre);
verifie('route : jamais une pièce derrière un obstacle de sa rangée', libre);

// ── Sans erreur, aucun choc ─────────────────────────────────────────────────
let jamais = true;
let pieces = true;
for (const g of [1, 2, 3, 4, 5, 6, 7, 8]) {
  const r = rouler(nouvelEtat(), 90, alea(g));
  if (r.e.chocs > 0) jamais = false;
  if (r.e.pieces < 10) pieces = false;
}
verifie('sans erreur : huit routes d’une minute et demie, aucun choc', jamais);
verifie('sans erreur : le pilote ramasse des pièces', pieces);

// ── Les réponses font la course ─────────────────────────────────────────────
const lente = rouler(nouvelEtat(), 30, alea(2)).e;
let e = nouvelEtat();
const ar = alea(2);
for (let i = 0; i < 6; i++) {
  e = donnerTurbo(e);
  e = rouler(e, 5, ar).e;
}
verifie('réponses : six bonnes réponses font bien plus de route que rien',
  e.distance > lente.distance * 1.8);
let f = nouvelEtat();
const af = alea(2);
for (let i = 0; i < 6; i++) {
  f = donnerErreur(f);
  f = rouler(f, 5, af).e;
}
verifie('réponses : six erreurs font moins de route que rien', f.distance < lente.distance);
verifie('réponses : six erreurs, six chocs', f.chocs === 6);

// ── Une erreur, un choc, et un seul ─────────────────────────────────────────
const apresErreur = rouler(donnerErreur(nouvelEtat()), 12, alea(5));
verifie('erreur : le pilote heurte un obstacle',
  apresErreur.evenements.filter((v) => v.type === 'choc').length === 1);
verifie('erreur : la maladresse est effacée après le choc', apresErreur.e.maladroit === false);
const turboArrete = donnerErreur(donnerTurbo(nouvelEtat()));
verifie('erreur : elle arrête le turbo', turboArrete.turbo === 0);
verifie('turbo : une bonne réponse efface une erreur en attente',
  donnerTurbo(donnerErreur(nouvelEtat())).maladroit === false);

// ── Le bouclier encaisse l'erreur ───────────────────────────────────────────
const protege = rouler(donnerErreur(donnerBouclier(nouvelEtat())), 12, alea(5));
verifie('bouclier : l’erreur est encaissée', protege.evenements.some((v) => v.type === 'bouclier'));
verifie('bouclier : aucun choc', protege.e.chocs === 0);
verifie('bouclier : il ne sert qu’une fois', protege.e.bouclier === false);
verifie('bouclier : la maladresse est effacée', protege.e.maladroit === false);

// ── Le turbo ────────────────────────────────────────────────────────────────
const t = donnerTurbo(nouvelEtat());
verifie('turbo : la voiture file', t.vitesse === VITESSE_TURBO);
const retombe = rouler(t, 6, alea(1)).e;
verifie('turbo : il retombe', Math.abs(retombe.vitesse - VITESSE_NORMALE) < 0.01);

// Un obstacle posé droit devant, dans la voie de la voiture.
function devantUnObstacle(e0: Etat): Etat {
  return {
    ...e0, voie: 1, x: 1, prochaineRangee: 10_000,
    objets: [{ id: 999, type: 'obstacle', sorte: 'chevre', voie: 1, d: e0.distance + 1 }],
  };
}
const choc = avancer(devantUnObstacle(donnerErreur(nouvelEtat())), 1 / 60, alea(2));
verifie('choc : la voiture tourne', choc.etat.choc > DUREE_CHOC - 0.1);
const adroit = avancer(devantUnObstacle(nouvelEtat()), 1 / 60, alea(2));
verifie('choc : sans erreur, même un obstacle collé ne touche pas', adroit.etat.chocs === 0);

// ── Le pilote ───────────────────────────────────────────────────────────────
const piege: Etat = {
  ...nouvelEtat(),
  objets: [{ id: 1, type: 'obstacle', sorte: 'trou', voie: 1, d: 12 }],
};
verifie('pilote : il quitte la voie d’un obstacle', choixDuPilote(piege) !== 1);
verifie('pilote maladroit : il y va', choixDuPilote({ ...piege, voie: 0, x: 0, maladroit: true }) === 1);
const appat: Etat = {
  ...nouvelEtat(),
  objets: [{ id: 1, type: 'piece', voie: 2, d: 12 }, { id: 2, type: 'piece', voie: 2, d: 15 }],
};
verifie('pilote : il va chercher les pièces', choixDuPilote(appat) === 2);
const bord: Etat = { ...nouvelEtat(), voie: 0, x: 0, objets: [{ id: 1, type: 'piece', voie: 2, d: 12 }] };
verifie('pilote : une voie à la fois', choixDuPilote(bord) === 1);

// ── Le voyage ───────────────────────────────────────────────────────────────
verifie('voyage : on part de Yaoundé', etape(0).depuis.nom === 'Yaoundé');
verifie('voyage : la prochaine ville est Mbalmayo', etape(10).vers?.nom === 'Mbalmayo');
verifie('voyage : à mi-chemin, la moitié', Math.abs(etape(350).part - 0.5) < 0.001);
verifie('voyage : au bout, plus de prochaine ville', etape(1e9).vers === null);
const arrivee = rouler({ ...nouvelEtat(), distance: VILLES[1].d - 3 }, 1, alea(4));
verifie('voyage : arriver dans une ville est un événement',
  arrivee.evenements.some((v) => v.type === 'ville' && v.nom === 'Mbalmayo'));
verifie('décor : il change en route', paysage(0) !== paysage(500));

console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
