/**
 * Ce que la course doit garantir.
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
  changerDeVoie,
  choixDuPilote,
  donnerBouclier,
  donnerTurbo,
  etape,
  nouvelEtat,
  paysage,
  rangee,
  type Etat,
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

function rouler(e: Etat, secondes: number, a: () => number, pilote: boolean) {
  const evenements = [];
  for (let t = 0; t < secondes; t += 1 / 60) {
    const r = avancer(e, 1 / 60, a, pilote);
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

// ── Les gestes ──────────────────────────────────────────────────────────────
const e0 = nouvelEtat();
verifie('départ : au milieu', e0.voie === 1);
verifie('geste : à gauche', changerDeVoie(e0, -1).voie === 0);
verifie('geste : pas plus loin que la route', changerDeVoie(changerDeVoie(e0, -1), -1).voie === 0);
verifie('geste : à droite, pas plus loin que la route',
  changerDeVoie(changerDeVoie(changerDeVoie(e0, 1), 1), 1).voie === 2);

// ── La voiture avance seule, et ne s'arrête jamais ──────────────────────────
const seule = rouler(nouvelEtat(), 60, alea(3), true);
verifie('pilote : une minute seule, elle avance', seule.e.distance > 60 * 10);
verifie('pilote : elle ramasse des pièces', seule.e.pieces > 5);
verifie('pilote : elle évite presque tout', seule.e.chocs <= 2);
const sansPilote = rouler(nouvelEtat(), 60, alea(3), false);
verifie('sans pilote : les chocs ne l’arrêtent pas', sansPilote.e.distance > 60 * 8);
verifie('sans pilote : la vitesse revient toujours', sansPilote.e.vitesse > VITESSE_CHOC_MAX());

function VITESSE_CHOC_MAX() {
  return 3;
}

// ── Le turbo et le bouclier ─────────────────────────────────────────────────
const t = donnerTurbo(nouvelEtat());
verifie('turbo : la voiture file', t.vitesse === VITESSE_TURBO);
const apres = rouler(t, 5, alea(1), true).e;
verifie('turbo : il retombe', Math.abs(apres.vitesse - VITESSE_NORMALE) < 0.01);

// Un obstacle posé droit devant, dans la voie de la voiture.
function devantUnObstacle(e: Etat): Etat {
  return {
    ...e, voie: 1, x: 1, prochaineRangee: 10_000,
    objets: [{ id: 999, type: 'obstacle', sorte: 'chevre', voie: 1, d: e.distance + 1 }],
  };
}
const choc = avancer(devantUnObstacle(nouvelEtat()), 1 / 60, alea(2), false);
verifie('choc : il est signalé', choc.evenements.some((v) => v.type === 'choc'));
verifie('choc : la voiture tourne', choc.etat.choc === DUREE_CHOC || choc.etat.choc > 0.7);
const protege = avancer(devantUnObstacle(donnerBouclier(nouvelEtat())), 1 / 60, alea(2), false);
verifie('bouclier : l’obstacle est traversé', protege.evenements.some((v) => v.type === 'bouclier'));
verifie('bouclier : pas de choc', protege.etat.choc === 0 && protege.etat.chocs === 0);
verifie('bouclier : il ne sert qu’une fois', protege.etat.bouclier === false);
const fonce = avancer(devantUnObstacle(donnerTurbo(nouvelEtat())), 1 / 60, alea(2), false);
verifie('turbo : il traverse aussi', fonce.etat.chocs === 0);

// ── Le pilote ───────────────────────────────────────────────────────────────
const piege: Etat = {
  ...nouvelEtat(),
  objets: [{ id: 1, type: 'obstacle', sorte: 'trou', voie: 1, d: 12 }],
};
verifie('pilote : il quitte la voie d’un obstacle', choixDuPilote(piege) !== 1);
const appat: Etat = {
  ...nouvelEtat(),
  objets: [{ id: 1, type: 'piece', voie: 2, d: 12 }, { id: 2, type: 'piece', voie: 2, d: 15 }],
};
verifie('pilote : il va chercher les pièces', choixDuPilote(appat) === 2);
const bord: Etat = {
  ...nouvelEtat(), voie: 0, x: 0,
  objets: [{ id: 1, type: 'piece', voie: 2, d: 12 }],
};
verifie('pilote : une voie à la fois', choixDuPilote(bord) === 1);

// ── Le voyage ───────────────────────────────────────────────────────────────
verifie('voyage : on part de Yaoundé', etape(0).depuis.nom === 'Yaoundé');
verifie('voyage : la prochaine ville est Mbalmayo', etape(10).vers?.nom === 'Mbalmayo');
verifie('voyage : à mi-chemin, la moitié', Math.abs(etape(350).part - 0.5) < 0.001);
verifie('voyage : au bout, plus de prochaine ville', etape(1e9).vers === null);
const arrivee = rouler({ ...nouvelEtat(), distance: VILLES[1].d - 3 }, 1, alea(4), true);
verifie('voyage : arriver dans une ville est un événement',
  arrivee.evenements.some((v) => v.type === 'ville' && v.nom === 'Mbalmayo'));
verifie('décor : il change en route', paysage(0) !== paysage(500));

console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
