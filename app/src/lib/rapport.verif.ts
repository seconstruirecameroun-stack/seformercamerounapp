/**
 * Ce que le rapport du parent doit garantir.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/rapport.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/rapport.verif.mjs \
 *     --define:import.meta.env='{"VITE_SUPABASE_URL":"http://x","VITE_SUPABASE_PUBLISHABLE_KEY":"x"}'
 *   node ../work/rapport.verif.mjs
 */

import { construireRapport } from './rapport';

let echecs = 0;
function verifie(nom: string, condition: boolean) {
  if (condition) console.log('  ok     ' + nom);
  else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

// Trois notions d'une même leçon, une question chacune.
const reperes = new Map(
  ['a', 'b', 'c'].map((n) => [
    'q-' + n,
    {
      kind: 'qcm' as const,
      notionKind: 'definition' as const,
      payload: { question: 'Q ' + n, options: ['x', 'y'] },
      notionId: 'n-' + n,
      enonce: 'Notion ' + n.toUpperCase(),
      lecon: 'La leçon',
      matiere: 'Sciences',
    },
  ]),
);

let minute = 0;
const essai = (notion: string, correct: boolean) => ({
  item_id: 'q-' + notion,
  correct,
  duration_ms: 4000,
  created_at: new Date(Date.UTC(2026, 10, 10, 9, minute++)).toISOString(),
  answer: { index: correct ? 0 : 1 },
});

const essais = [
  // A : trois fautes, puis deux réussites — rattrapée.
  essai('a', false), essai('a', false), essai('a', false), essai('a', true), essai('a', true),
  // B : trois fautes, une réussite, puis encore une faute — toujours fragile.
  essai('b', false), essai('b', false), essai('b', true), essai('b', false),
  // C : deux fautes, rien d'autre.
  essai('c', false), essai('c', false),
];

const r = construireRapport('BRAYNE', 'debut', essais, reperes, [], new Map(), 0);
const ids = r.aTravailler.map((p) => p.notionId);
verifie('une notion rattrapée (deux dernières justes) n’est plus à travailler', !ids.includes('n-a'));
verifie('une notion ratée à la dernière réponse reste à travailler', ids.includes('n-b'));
verifie('une notion jamais réussie reste à travailler', ids.includes('n-c'));
verifie('les questions sont toutes comptées', r.questions === essais.length);
verifie('les bonnes réponses sont comptées', r.justes === 3);

// Les réponses arrivent dans le désordre : le rapport doit les remettre dans
// l'ordre du temps avant de juger « les deux dernières ».
const melangees = [...essais].reverse();
const r2 = construireRapport('BRAYNE', 'debut', melangees, reperes, [], new Map(), 0);
verifie('l’ordre d’arrivée ne change rien', !r2.aTravailler.some((p) => p.notionId === 'n-a')
  && r2.aTravailler.some((p) => p.notionId === 'n-b'));

const vide = construireRapport('BRAYNE', 'semaine', [], reperes, [], new Map(), 0);
verifie('une semaine sans réponse : un rapport vide, sans priorité', vide.vide && vide.aTravailler.length === 0);

console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
