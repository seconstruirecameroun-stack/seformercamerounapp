/**
 * Ce que le garde de l'annotation doit refuser.
 *
 * Une question d'annotation mal formée ne plante pas : elle s'affiche avec
 * un numéro sans nom possible, ou un nom qui ne va nulle part, et l'enfant
 * perd une manche sans avoir rien raté. Le garde tourne donc avant le
 * rendu, et ces vérifications tournent avant la mise en ligne.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/annotation.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/annotation.verif.mjs
 *   node ../work/annotation.verif.mjs
 */

import { annotationJouable, memeAnnotation } from './annotation';

let echecs = 0;

function verifie(nom: string, condition: boolean) {
  if (condition) {
    console.log('  ok     ' + nom);
  } else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

const bon = {
  p: {
    question: 'Annote le schéma de la lampe à pétrole.',
    figure: 'br-la-schema',
    etiquettes: ['le réservoir', 'la molette', 'la mèche', 'le verre', 'la grille d’aération'],
  },
  a: { ordre: [0, 1, 2, 3, 4] },
};

export function verifierAnnotation(): number {
  verifie('annotation : la forme attendue passe', annotationJouable(bon.p, bon.a));

  // La figure est une clé livrée avec l'app. Une figure annotée est
  // dessinée, jamais générée : son script est ce qui garantit que les
  // numéros vont de 1 à n, et une URL n'a pas de script.
  verifie(
    'annotation : une URL de figure est refusée',
    !annotationJouable({ ...bon.p, figure: 'https://ailleurs/figure.webp' }, bon.a),
  );
  verifie(
    'annotation : une clé avec majuscule est refusée',
    !annotationJouable({ ...bon.p, figure: 'BR-la-schema' }, bon.a),
  );
  verifie('annotation : sans figure, refusée', !annotationJouable({ ...bon.p, figure: '' }, bon.a));
  verifie(
    'annotation : sans énoncé, refusée',
    !annotationJouable({ ...bon.p, question: '   ' }, bon.a),
  );

  // Chaque numéro reçoit un nom, chaque nom sert une fois.
  verifie(
    'annotation : un ordre trop court est refusé',
    !annotationJouable(bon.p, { ordre: [0, 1, 2, 3] }),
  );
  verifie(
    'annotation : un nom servi deux fois est refusé',
    !annotationJouable(bon.p, { ordre: [0, 0, 2, 3, 4] }),
  );
  verifie(
    'annotation : un index hors liste est refusé',
    !annotationJouable(bon.p, { ordre: [0, 1, 2, 3, 9] }),
  );
  verifie(
    'annotation : un index non entier est refusé',
    !annotationJouable(bon.p, { ordre: [0, 1, 2, 3, 4.5] }),
  );
  verifie('annotation : sans ordre, refusée', !annotationJouable(bon.p, {}));

  // Deux étiquettes identiques rendraient une réponse juste indiscernable
  // d'une fausse.
  verifie(
    'annotation : deux étiquettes identiques sont refusées',
    !annotationJouable(
      { ...bon.p, etiquettes: ['le verre', 'le verre', 'la mèche'] },
      { ordre: [0, 1, 2] },
    ),
  );
  verifie(
    'annotation : un seul repère est refusé',
    !annotationJouable({ ...bon.p, etiquettes: ['le verre'] }, { ordre: [0] }),
  );
  verifie(
    'annotation : neuf repères sont refusés',
    !annotationJouable(
      { ...bon.p, etiquettes: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'] },
      { ordre: [0, 1, 2, 3, 4, 5, 6, 7, 8] },
    ),
  );
  verifie(
    'annotation : une étiquette vide est refusée',
    !annotationJouable({ ...bon.p, etiquettes: ['le verre', '  '] }, { ordre: [0, 1] }),
  );

  // La comparaison des réponses.
  verifie('réponse : la même suite est juste', memeAnnotation([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]));
  verifie('réponse : une place échangée est fausse', !memeAnnotation([1, 0, 2, 3, 4], [0, 1, 2, 3, 4]));
  verifie('réponse : un trou est faux', !memeAnnotation([0, 1, 2, 3, null], [0, 1, 2, 3, 4]));

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
  return echecs;
}

verifierAnnotation();
