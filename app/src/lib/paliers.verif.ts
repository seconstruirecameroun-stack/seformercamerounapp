/**
 * Vérifications de l'escalier des étapes.
 *
 * Écrites après coup, pour un défaut que personne ne pouvait voir à l'écran :
 * l'appui servi au bout de trois échecs ne s'arrêtait jamais. Le compteur
 * d'échecs ne se remettait à zéro que sur une bonne réponse **de l'étape en
 * cours** — or l'appui faisait précisément qu'on n'en servait plus aucune.
 * Le compteur restait figé, l'appui durait pour toujours, et l'étape ne
 * passait plus. KLEIN avait cinq notions mortes ainsi.
 *
 * Le dernier contrôle est le plus important : il joue une vie entière de
 * séances et exige que l'étape finisse par passer.
 *
 *   npx esbuild src/lib/paliers.verif.ts --bundle --platform=node \
 *     --outfile=node_modules/.cache/paliers.verif.cjs --format=cjs \
 *     && node node_modules/.cache/paliers.verif.cjs
 */

import {
  ECHECS_AVANT_APPUI,
  avanceLEtape,
  echecsDAffilee,
  etapeCourante,
  niveauDAppui,
  reussitesParNiveau,
} from './paliers';

let ko = 0;
const ok = (nom: string, vrai: boolean) => {
  if (!vrai) {
    ko += 1;
    console.log('KO  ' + nom);
  }
};

/** Une notion à trois marches : reconnaître, relier, écrire. */
const notion = {
  id: 'n1',
  items: [
    { id: 'i1', level: 1 },
    { id: 'i2', level: 2 },
    { id: 'i3', level: 3 },
  ],
};
const notions = [notion] as never;

let horloge = 0;
const essai = (item_id: string, correct: boolean) => {
  horloge += 1;
  return { item_id, correct, created_at: new Date(Date.UTC(2026, 10, 2, 8, horloge)).toISOString() };
};

const echecs = (journal: ReturnType<typeof essai>[], niveau = 3) =>
  echecsDAffilee(notions, niveau, journal).get('n1') ?? 0;

// L-appui se déclenche au bout de trois échecs, pas avant.
const trois = [essai('i3', false), essai('i3', false), essai('i3', false)];
ok('deux échecs ne déclenchent rien', echecs(trois.slice(0, 2)) < ECHECS_AVANT_APPUI);
ok('trois échecs déclenchent l-appui', echecs(trois) >= ECHECS_AVANT_APPUI);
ok('l-appui redescend d-une marche', niveauDAppui(notion, 3) === 2);

// Le défaut : après l-appui, une bonne réponse en bas doit rendre la main.
const apresAppui = [...trois, essai('i2', true)];
ok('une réussite à l-appui remet le compteur à zéro', echecs(apresAppui) === 0);

// Et elle rend TROIS essais neufs, pas un seul — sinon le premier échec
// renverrait aussitôt en bas, et on tournerait en rond.
ok('un échec après la reprise ne rebloque pas', echecs([...apresAppui, essai('i3', false)]) === 1);
ok('deux échecs après la reprise ne rebloquent pas encore',
   echecs([...apresAppui, essai('i3', false), essai('i3', false)]) === 2);
ok('trois échecs après la reprise rebloquent',
   echecs([...apresAppui, essai('i3', false), essai('i3', false), essai('i3', false)])
     >= ECHECS_AVANT_APPUI);

// Un échec à l-appui ne rend pas la main : il a encore besoin de la marche basse.
ok('un échec à l-appui laisse l-appui', echecs([...trois, essai('i2', false)]) >= ECHECS_AVANT_APPUI);

// Une bonne réponse à l-étape elle-même remet évidemment à zéro.
ok('une réussite à l-étape remet à zéro', echecs([...trois, essai('i3', true)]) === 0);

// Une réussite d-appui ANCIENNE ne doit pas effacer des échecs postérieurs.
ok('la réussite d-appui ne vaut que si elle est récente',
   echecs([essai('i2', true), essai('i3', false), essai('i3', false), essai('i3', false)])
     >= ECHECS_AVANT_APPUI);

// ───────────────────────────────────────────────────────────────────────────
// Le contrôle qui compte : une suite de séances doit FINIR par passer
// l-étape. C-est exactement ce qui ne pouvait plus arriver.

function simuler(reussitAppui: boolean, reussitEtape: boolean, tours: number) {
  // Les deux premières marches sont déjà franchies : c’est la situation de
  // KLEIN, bloqué à l’étape d’écriture d’une leçon dont il reconnaît tout.
  // Cette réussite d’appui est ANCIENNE : elle ne doit pas servir de reprise
  // aux échecs qui suivent, et les contrôles plus haut le vérifient.
  const journal: ReturnType<typeof essai>[] = [essai('i1', true), essai('i2', true)];
  let servisEnHaut = 0;
  for (let t = 0; t < tours; t += 1) {
    const bloque = (echecsDAffilee(notions, 3, journal).get('n1') ?? 0) >= ECHECS_AVANT_APPUI;
    const servi = bloque ? niveauDAppui(notion, 3) : 3;
    if (servi === 3) {
      servisEnHaut += 1;
      journal.push(essai('i3', reussitEtape));
    } else {
      journal.push(essai('i2', reussitAppui));
    }
    const etape = etapeCourante(notions, reussitesParNiveau(
      [{ id: 'n1', items: notion.items }],
      journal.filter((e) => e.correct),
    ));
    if (etape.niveau > 3 || etape.termine) return { passee: true, tours: t + 1, servisEnHaut };
  }
  return { passee: false, tours, servisEnHaut };
}

// Un enfant qui échoue toujours en haut mais réussit l-appui doit malgré tout
// se voir REPROPOSER la question de l-étape, encore et encore.
const entete = simuler(true, false, 40);
ok('la question de l-étape revient après chaque reprise (' + entete.servisEnHaut + ' fois sur 40)',
   entete.servisEnHaut >= 8);

// Et dès qu-il la réussit, l-étape passe.
const fini = simuler(true, true, 40);
ok('l-étape finit par passer', fini.passee);

// Même celui qui échoue partout doit continuer à voir la marche haute
// revenir : sans cela, l-appui est un cul-de-sac.
const jamais = simuler(false, false, 40);
ok('aucun cul-de-sac même en échec total', jamais.servisEnHaut >= 3);

// Une question d-appui réussie ne fait pas avancer l-étape à l-écran. C-était
// le défaut du 12 novembre : « Étape réussie ! », le coffre, cinquante
// étoiles, puis retour à l-étape 2 sur la même question.
ok('appui juste : l’étape n’avance pas', !avanceLEtape({ appui: true }, true));
ok('appui faux : l’étape n’avance pas', !avanceLEtape({ appui: true }, false));
ok('question de l’étape juste : l’étape avance', avanceLEtape({ appui: false }, true));
ok('question sans indication d’appui, juste : l’étape avance', avanceLEtape({}, true));
ok('question de l’étape fausse : rien n’avance', !avanceLEtape({ appui: false }, false));

// Et le journal dit la même chose que l-écran : la bonne réponse d-appui est
// rangée à son niveau, pas à celui de l-étape.
{
  const n = { id: 'n', items: [{ id: 'bas', level: 1 }, { id: 'haut', level: 2 }] };
  const r = reussitesParNiveau([n], [{ item_id: 'bas' }]);
  ok('journal : l’appui réussi valide le niveau 1', r.get(1)?.has('n') === true);
  ok('journal : et pas le niveau 2', !(r.get(2)?.has('n') ?? false));
  ok('journal : l’étape reste donc la 2',
    etapeCourante([n], r).niveau === 2 && !etapeCourante([n], r).termine);
}

if (ko > 0) throw new Error(ko + ' echec(s)');
console.log('paliers : escalier verifie, aucun cul-de-sac');
