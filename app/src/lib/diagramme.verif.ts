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
  capaciteRegion,
  placerEtiquettes,
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
  // La lettre elle-même doit rester dans le rectangle : en élargissant les
  // cercles, le K du haut est passé sous le bord du cadre, et c-est le père
  // qui l-aurait vu avant moi.
  for (const e of d.etiquettes) {
    ok(`${noms.length} ensembles : lettre dans le cadre`,
       e.x - 13 >= d.cadre.x && e.x + 13 <= d.cadre.x + d.cadre.w &&
       e.y - 13 >= d.cadre.y && e.y + 13 <= d.cadre.y + d.cadre.h);
  }
  // Les étiquettes des noms ne doivent pas se poser sur une ancre.
  for (const e of d.etiquettes) {
    ok(`${noms.length} ensembles : étiquette hors des ancres`,
       Object.values(d.ancres).every((a) => Math.hypot(a.x - e.x, a.y - e.y) > 18));
  }
}

// Le milieu des trois ovales doit vraiment appartenir aux trois.
const d3 = disposition(['A', 'B', 'C']);
ok('le centre est bien ABC', regionDuPoint(d3, d3.ancres.ABC) === 'ABC');
ok('le haut est A seul', regionDuPoint(d3, { x: 160, y: 24 }) === 'A');

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

// ───────────────────────────────────────────────────────────────────────────
// Les places des étiquettes.
//
// Elles étaient posées sur une seule rangée centrée sur l-ancre : à cinq,
// elles sortaient franchement du cercle. Un élément dessiné hors de sa
// région dit le contraire de ce que l-exercice enseigne — et le père l-a vu
// avant moi, sur une capture.

// Ce que chaque région peut porter, et qui ne doit pas rétrécir sans qu-on
// le sache : une géométrie retouchée pourrait fermer une lentille en
// silence, et une question parfaitement écrite deviendrait illisible.
const MINIMUM = { lentille: 4, large: 8 };

for (const noms of [['A', 'B'], ['A', 'B', 'C']]) {
  const d = disposition(noms);
  for (const region of toutesLesRegions(noms)) {
    const capacite = capaciteRegion(d, region);
    const lentille = region !== DEHORS && region.length > 1;
    ok(`${noms.length} ensembles, ${region} : capacité ${capacite}`,
       capacite >= (lentille ? MINIMUM.lentille : MINIMUM.large));

    // Jusqu-à sa capacité, une région doit poser proprement : dedans, et
    // sans recouvrement. Au-delà, le dessin serait de toute façon illisible
    // et la question n-aurait pas dû être écrite ainsi.
    for (let combien = 1; combien <= capacite; combien += 1) {
      const etiquettes = Array.from({ length: combien }, (_, i) => String(10 + i));
      const places = placerEtiquettes(d, region, etiquettes);
      ok(`${region} × ${combien} : autant de places que d-étiquettes`,
         places.length === combien);

      // Chaque pastille, coins compris, doit être dans sa région.
      const dehors = places.filter((p) => {
        const dx = p.w / 2;
        const dy = p.h / 2;
        return [
          { x: p.x - dx, y: p.y - dy }, { x: p.x + dx, y: p.y - dy },
          { x: p.x - dx, y: p.y + dy }, { x: p.x + dx, y: p.y + dy },
        ].some((c) => regionDuPoint(d, c) !== region);
      });
      ok(`${region} × ${combien} : aucune pastille hors de sa région (${dehors.length})`,
         dehors.length === 0);

      // Et elles ne doivent pas se recouvrir.
      let collisions = 0;
      for (let i = 0; i < places.length; i += 1) {
        for (let j = i + 1; j < places.length; j += 1) {
          if (Math.abs(places[i].x - places[j].x) < (places[i].w + places[j].w) / 2 &&
              Math.abs(places[i].y - places[j].y) < places[i].h) collisions += 1;
        }
      }
      ok(`${region} × ${combien} : aucune pastille sur une autre`, collisions === 0);
    }
  }
}

// Le cas qui a déclenché tout cela : dix éléments, le rangement attendu de
// la question réellement en base.
const d2 = disposition(['C', 'D']);
for (const [region, liste] of Object.entries({
  C: ['1', '2', '3'], CD: ['4', '5'], D: ['6', '7'], dehors: ['8', '9', '10'],
})) {
  const places = placerEtiquettes(d2, region, liste);
  const toutesDedans = places.every((p) =>
    regionDuPoint(d2, { x: p.x - p.w / 2, y: p.y }) === region &&
    regionDuPoint(d2, { x: p.x + p.w / 2, y: p.y }) === region);
  ok(`question en base, région ${region} : tout tient dedans`, toutesDedans);
}

if (ko > 0) throw new Error(ko + ' echec(s)');
console.log('diagramme : geometrie et garde verifiees, tout passe');
