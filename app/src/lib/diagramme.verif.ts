/**
 * Vérifications de la géométrie du diagramme.
 *
 * La plus importante est la dernière : **chaque ancre doit tomber dans la
 * région qu'elle sert**. Une ancre mal placée écrirait « 15 » dans le
 * milieu alors que le toucher au même endroit le rangerait ailleurs, et
 * l'enfant verrait sa bonne réponse refusée sans comprendre. À mi-chemin,
 * les ancres des lentilles tombaient encore dans le troisième disque : ce
 * contrôle l'a trouvé, pas un coup d'œil.
 *
 *   npx esbuild src/lib/diagramme.verif.ts --bundle --platform=node \
 *     --outfile=node_modules/.cache/diagramme.verif.cjs --format=cjs \
 *     && node node_modules/.cache/diagramme.verif.cjs
 */

import {
  DEHORS,
  cleRegion,
  diagrammeJouable,
  disposition,
  memeRangement,
  regionDuPoint,
  toutesLesRegions,
} from './diagramme';

let ko = 0;
const ok = (nom: string, vrai: boolean) => {
  if (!vrai) {
    ko += 1;
    console.log('KO  ' + nom);
  }
};

// Les clés de régions.
ok('clé du dehors', cleRegion(['A', 'B'], [false, false]) === DEHORS);
ok('clé simple', cleRegion(['A', 'B'], [true, false]) === 'A');
ok('clé croisée', cleRegion(['A', 'B', 'C'], [true, false, true]) === 'AC');
ok('quatre régions à deux ensembles', toutesLesRegions(['A', 'B']).length === 4);
ok('huit régions à trois ensembles', toutesLesRegions(['A', 'B', 'C']).length === 8);

// Chaque ancre doit tomber dans sa propre région. C-est tout le contrat.
for (const noms of [['A', 'B'], ['A', 'B', 'C']]) {
  const d = disposition(noms);
  for (const [cle, point] of Object.entries(d.ancres)) {
    const trouvee = regionDuPoint(d, point);
    ok(`ancre ${noms.length} ensembles « ${cle} » → ${trouvee}`, trouvee === cle);
  }
  // Et toutes les régions doivent exister sur le dessin, sinon une réponse
  // attendue serait impossible à composer.
  for (const cle of toutesLesRegions(noms)) {
    ok(`région « ${cle} » dessinée`, d.ancres[cle] !== undefined);
  }
  // Hors du rectangle, on ne range rien.
  ok(`${noms.length} ensembles : hors cadre refusé`, regionDuPoint(d, { x: 2, y: 2 }) === null);
  ok(`${noms.length} ensembles : sous le cadre refusé`, regionDuPoint(d, { x: 160, y: 226 }) === null);
  // Les étiquettes des noms ne doivent pas se poser sur une ancre.
  for (const e of d.etiquettes) {
    ok(`${noms.length} ensembles : étiquette hors des ancres`,
       Object.values(d.ancres).every((a) => Math.hypot(a.x - e.x, a.y - e.y) > 18));
  }
}

// Le milieu des trois ovales doit vraiment appartenir aux trois.
const d3 = disposition(['A', 'B', 'C']);
ok('le centre est bien ABC', regionDuPoint(d3, d3.ancres.ABC) === 'ABC');
ok('le haut est A seul', regionDuPoint(d3, { x: 160, y: 20 }) === 'A');

// Comparaison des rangements.
ok('ordre indifférent dans une région',
   memeRangement({ ABC: ['15', '19'] }, { ABC: ['19', '15'] }));
ok('région absente = région vide', memeRangement({ A: ['11'], AB: [] }, { A: ['11'] }));
ok('un élément déplacé est une autre réponse',
   !memeRangement({ A: ['11'], B: [] }, { A: [], B: ['11'] }));
ok('un élément en trop est une autre réponse',
   !memeRangement({ A: ['11'] }, { A: ['11', '17'] }));

// La garde de forme.
const bon = {
  p: { question: 'Place them.', sets: ['A', 'B', 'C'], elements: ['11', '13', '15'] },
  a: { regions: { A: ['11'], AC: ['13'], ABC: ['15'] } },
};
ok('item valide accepté', diagrammeJouable(bon.p, bon.a));
ok('élément oublié refusé',
   !diagrammeJouable(bon.p, { regions: { A: ['11'], AC: ['13'] } }));
ok('élément rangé deux fois refusé',
   !diagrammeJouable(bon.p, { regions: { A: ['11', '15'], AC: ['13'], ABC: ['15'] } }));
ok('élément inconnu refusé',
   !diagrammeJouable(bon.p, { regions: { A: ['11'], AC: ['13'], ABC: ['99'] } }));
ok('région inconnue refusée',
   !diagrammeJouable(bon.p, { regions: { A: ['11'], AC: ['13'], AD: ['15'] } }));
ok('un seul ensemble refusé',
   !diagrammeJouable({ ...bon.p, sets: ['A'] }, { regions: { A: ['11', '13', '15'] } }));
ok('quatre ensembles refusés',
   !diagrammeJouable({ ...bon.p, sets: ['A', 'B', 'C', 'D'] }, bon.a));
ok('élément en double dans l-énoncé refusé',
   !diagrammeJouable({ ...bon.p, elements: ['11', '11', '15'] }, bon.a));
// Une région vide est une réponse, pas un oubli : elle doit passer.
ok('régions vides acceptées',
   diagrammeJouable({ question: 'x', sets: ['A', 'B'], elements: ['1'] },
                    { regions: { A: ['1'], AB: [], B: [], dehors: [] } }));

if (ko > 0) throw new Error(ko + ' echec(s)');
console.log('diagramme : geometrie et garde verifiees, tout passe');
