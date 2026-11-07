import {
  grouperEnAlbums,
  grouperParChapitre,
  grouperParMois,
  jourCourt,
} from './rangement';
import type { Autocollant, LeconResume, MatiereResume } from './dashboard';

/**
 * Le rangement des leçons et de la collection, vérifié cas par cas.
 *
 * Ces fonctions décident de ce qu'un enfant TROUVE. Une leçon rangée sous le
 * mauvais mois n'est pas perdue en base, elle est perdue à l'écran — et
 * c'est pareil pour lui.
 *
 * Deux pièges se cachent ici, et les deux ont leur cas :
 *
 *   Les leçons sans date. Toutes les pages de cahier n'en portent pas. Les
 *   ranger sous le mois en cours serait un mensonge commode ; elles ferment
 *   la marche sous leur propre titre.
 *
 *   L'ordre des albums. Il doit suivre celui des dossiers de matières, pour
 *   qu'un enfant retrouve son album là où il a l'habitude de voir sa
 *   matière. Un tri par nom ou par avancement le déplacerait à chaque image
 *   gagnée.
 *
 * Le projet n'a pas de lanceur de tests. Celui-ci se construit et se joue :
 *
 *   cd app
 *   node_modules/.bin/esbuild src/lib/rangement.verif.ts --bundle --platform=node \
 *     --format=esm --define:import.meta.env='{"VITE_SUPABASE_URL":"https://x.test",
 *     "VITE_SUPABASE_PUBLISHABLE_KEY":"x"}' --outfile=../work/rangement.verif.mjs
 *   node ../work/rangement.verif.mjs
 */

let echecs = 0;

function verifie(nom: string, condition: boolean) {
  if (condition) {
    console.log('  ok     ' + nom);
  } else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

const lecon = (id: string, date: string | null, chapitre: string | null = null) =>
  ({ id, title: id, date, chapitre, matiereId: 'm1' }) as unknown as LeconResume;

const image = (id: string, matiereId: string | null, acquis: boolean) =>
  ({ notionId: id, matiereId, statement: id, illustration: 'img-' + id, acquis }) as Autocollant;

const matiere = (id: string, label: string) =>
  ({ id, label, couleur: '#123456' }) as MatiereResume;

function verifierRangement() {
  console.log('\nRangement');

  // ── Par mois ─────────────────────────────────────────────────────────────
  const mois = grouperParMois([
    lecon('oct-12', '2026-10-12'),
    lecon('nov-04', '2026-11-04'),
    lecon('sans', null),
    lecon('oct-30', '2026-10-30'),
  ]);
  verifie('mois : trois groupes', mois.length === 3);
  verifie('mois : le plus récent en premier', mois[0].cle === '2026-11');
  verifie('mois : le titre est écrit en toutes lettres', mois[0].titre === 'Novembre 2026');
  verifie('mois : octobre vient ensuite', mois[1].cle === '2026-10');
  verifie('mois : les sans-date ferment la marche', mois[2].titre === 'Sans date');
  verifie(
    'mois : dans un mois, du plus récent au plus ancien',
    mois[1].lecons.map((l) => l.id).join() === 'oct-30,oct-12',
  );
  verifie('mois : aucune leçon perdue', mois.reduce((n, g) => n + g.lecons.length, 0) === 4);
  verifie('mois : liste vide', grouperParMois([]).length === 0);

  // Une seule leçon sans date ne doit pas inventer un mois.
  const seule = grouperParMois([lecon('x', null)]);
  verifie('mois : une seule sans date reste sans date', seule[0].titre === 'Sans date');

  // ── Par chapitre, qui existait déjà ──────────────────────────────────────
  const unSeul = grouperParChapitre([lecon('a', '2026-10-01', 'Grammaire')]);
  verifie('chapitre : un seul chapitre ne met pas de titre', unSeul[0].titre === null);
  const deux = grouperParChapitre([
    lecon('a', '2026-10-01', 'Grammaire'),
    lecon('b', '2026-10-20', 'Conjugaison'),
  ]);
  verifie('chapitre : deux chapitres, deux titres', deux.length === 2);
  verifie('chapitre : le plus récent en premier', deux[0].titre === 'Conjugaison');

  // ── Les albums ───────────────────────────────────────────────────────────
  const matieres = [matiere('m1', 'Sciences'), matiere('m2', 'Anglais')];
  const albums = grouperEnAlbums(
    [
      image('a', 'm2', true),
      image('b', 'm1', true),
      image('c', 'm1', false),
      image('d', 'm2', false),
      image('e', null, true),
    ],
    matieres,
  );
  verifie('albums : un par matière, plus les orphelines', albums.length === 3);
  verifie("albums : l'ordre est celui des dossiers de matières", albums[0].titre === 'Sciences');
  verifie('albums : les images sans matière ferment la marche', albums[2].titre === 'Autres images');
  verifie('albums : le compte par album', albums[0].total === 2 && albums[0].gagnes === 1);
  verifie(
    "albums : l'ordre des images est celui où elles arrivent",
    albums[0].images.map((i) => i.notionId).join() === 'b,c',
  );
  verifie(
    'albums : une image sans dessin ne compte pas',
    grouperEnAlbums(
      [{ notionId: 'z', matiereId: 'm1', statement: 'z', illustration: null, acquis: true }],
      matieres,
    ).length === 0,
  );
  verifie('albums : collection vide', grouperEnAlbums([], matieres).length === 0);

  // ── Le jour écrit en court ───────────────────────────────────────────────
  verifie('jour : une date absente ne rend rien', jourCourt(null) === null);
  verifie('jour : une date illisible ne rend rien', jourCourt('pas-une-date') === null);
  verifie('jour : une vraie date est rendue', (jourCourt('2026-10-13') ?? '').includes('13'));

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
  return echecs;
}

verifierRangement();
