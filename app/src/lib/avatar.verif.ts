/**
 * Ce que le personnage doit garantir.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/avatar.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/avatar.verif.mjs
 *   node ../work/avatar.verif.mjs
 */

import {
  NIVEAUX,
  OBJETS,
  energie,
  equipement,
  joursSansJouer,
  niveauDe,
  objetsDe,
  type Bilan,
} from './avatar';

let echecs = 0;
function verifie(nom: string, condition: boolean) {
  if (condition) console.log('  ok     ' + nom);
  else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

const RIEN: Bilan = {
  etapesFranchies: 0, leconsTerminees: 0, leconsValidees: 0, images: 0, etoiles: 0,
  joursJoues: 0, serieJours: 0, serieManches: 0, or: 0, argent: 0, bronze: 0,
  matieresCompletes: 0, dernierJour: null, joursRecents: 0,
};
const JOUR = '2026-11-16';
const ilYA = (n: number) => new Date(Date.parse(JOUR) - n * 86_400_000).toISOString().slice(0, 10);

// ── Le catalogue ────────────────────────────────────────────────────────────
verifie('catalogue : aucun identifiant en double', new Set(OBJETS.map((o) => o.id)).size === OBJETS.length);
verifie('catalogue : chaque objet dit comment on le gagne', OBJETS.every((o) => o.condition.length > 5));
verifie('catalogue : seules les auras sont temporaires', OBJETS.every((o) => o.temporaire === (o.emplacement === 'aura')));

// ── L'énergie ───────────────────────────────────────────────────────────────
verifie('énergie : pleine le jour où il joue', energie(JOUR, JOUR) === 100);
verifie('énergie : un jour sans jouer, 80', energie(ilYA(1), JOUR) === 80);
verifie('énergie : vide au bout de cinq jours', energie(ilYA(5), JOUR) === 0 && energie(ilYA(9), JOUR) === 0);
verifie('énergie : jamais joué, vide', energie(null, JOUR) === 0);
verifie('jours sans jouer : compte juste', joursSansJouer(ilYA(3), JOUR) === 3);

// ── Rien sans travail ───────────────────────────────────────────────────────
verifie('sans travail : aucun objet', objetsDe(RIEN, JOUR).every((o) => !o.gagne));
verifie('sans travail : niveau Débutant', niveauDe(RIEN).actuel.nom === 'Débutant');

// ── Ce qui est gagné par la maîtrise reste ──────────────────────────────────
const travailleur: Bilan = {
  ...RIEN, etapesFranchies: 20, leconsTerminees: 6, leconsValidees: 4, images: 50,
  joursJoues: 12, serieJours: 4, serieManches: 3, or: 1, argent: 2, dernierJour: JOUR, joursRecents: 6,
};
const aujourdhui = objetsDe(travailleur, JOUR);
const a = (id: string, l = aujourdhui) => l.find((o) => o.id === id)!;
verifie('travail : la casquette, le bandeau, la cape sont gagnés',
  a('casquette').gagne && a('bandeau').gagne && a('cape').gagne);
verifie('travail : les ailes demandent 10 leçons validées', !a('ailes').gagne && a('ailes').fait === 4 && a('ailes').but === 10);
verifie('travail : les pouvoirs du moment sont là', a('flammes').gagne && a('eclairs').gagne && a('arc-en-ciel').gagne);

const absent8 = objetsDe({ ...travailleur, dernierJour: ilYA(8) }, JOUR);
verifie('8 jours d’absence : les objets de maîtrise restent',
  a('casquette', absent8).gagne && a('cape', absent8).gagne && a('trophee', absent8).gagne);
verifie('8 jours d’absence : les pouvoirs du moment disparaissent',
  !a('flammes', absent8).gagne && !a('eclairs', absent8).gagne);
const absent6 = objetsDe({ ...travailleur, dernierJour: ilYA(6) }, JOUR);
verifie('6 jours d’absence : les pouvoirs tiennent encore', a('eclairs', absent6).gagne);

// ── L'énergie éteint le légendaire sans le reprendre ────────────────────────
const legendaire: Bilan = { ...travailleur, images: 220 };
verifie('légendaire : le bébé lion brille quand il joue', !a('lionceau', objetsDe(legendaire, JOUR)).eteint);
const endormi = objetsDe({ ...legendaire, dernierJour: ilYA(3) }, JOUR);
verifie('légendaire : trois jours sans jouer, il est éteint mais toujours à lui',
  a('lionceau', endormi).gagne && a('lionceau', endormi).eteint);

// ── Ce qu'il porte ──────────────────────────────────────────────────────────
const porte = equipement(aujourdhui);
verifie('équipement : le plus rare gagné par défaut', porte.tete?.id === 'bandeau' && porte.dos?.id === 'cape');
verifie('équipement : son choix l’emporte s’il l’a gagné', equipement(aujourdhui, { tete: 'casquette' }).tete?.id === 'casquette');
verifie('équipement : un objet non gagné ne se porte pas', equipement(aujourdhui, { tete: 'couronne' }).tete?.id === 'bandeau');
verifie('équipement : il peut ne rien porter', equipement(aujourdhui, { tete: null }).tete === undefined);

// ── Les niveaux ─────────────────────────────────────────────────────────────
verifie('niveaux : seuils croissants', NIVEAUX.every((n, i) => i === 0 || n.seuil > NIVEAUX[i - 1].seuil));
const n = niveauDe(travailleur);
verifie('niveaux : le travailleur a passé Débutant', n.actuel.rang >= 2);
verifie('niveaux : on dit ce qui manque', n.suivant !== null && n.manquePoints > 0);
const rienQueDesPoints: Bilan = { ...RIEN, etapesFranchies: 2000, joursJoues: 100 };
verifie('Légende : beaucoup de points ne suffisent pas sans maîtrise', niveauDe(rienQueDesPoints).actuel.rang <= 5);
verifie('Légende : la condition est annoncée', niveauDe(rienQueDesPoints).manqueCondition !== null);
const legende: Bilan = { ...rienQueDesPoints, leconsValidees: 40, or: 5, matieresCompletes: 1 };
verifie('Légende : points et maîtrise, la Légende est atteinte', niveauDe(legende).actuel.nom === 'Légende');
verifie('Légende : rien au-dessus', niveauDe(legende).suivant === null);

console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
