/**
 * Ce que le tirage d'une composition doit garantir.
 *
 * Une épreuve mal tirée mesure mal : trois questions sur la même notion et
 * rien sur une autre, ou vingt questions prises dans la première leçon des
 * quatre annoncées. L'enfant ne peut pas le voir, le parent non plus, et la
 * note ment sans que personne ne s'en aperçoive. D'où ces vérifications.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/composition.verif.ts --bundle \
 *     --platform=node --format=esm \
 *     --define:import.meta.env='{"VITE_SUPABASE_URL":"https://x.test",
 *     "VITE_SUPABASE_PUBLISHABLE_KEY":"x"}' --outfile=../work/composition.verif.mjs
 *   node ../work/composition.verif.mjs
 */

import {
  EPREUVE_DEPUIS,
  etatDeLaComposition,
  note,
  pointsOralDe,
  questionsEcritesPour,
  tirerQuestions,
  totalDe,
  type CompositionRow,
  type LeconPourTirage,
} from './composition';

let echecs = 0;

function verifie(nom: string, condition: boolean) {
  if (condition) {
    console.log('  ok     ' + nom);
  } else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

/** Une leçon de `notions` notions, chacune avec ses quatre étapes. */
const lecon = (id: string, notions: number, etapes = [1, 2, 3, 4]): LeconPourTirage => ({
  id,
  notions: Array.from({ length: notions }, (_, n) => ({
    id: id + '-n' + n,
    items: etapes.map((niveau) => ({ id: id + '-n' + n + '-e' + niveau, level: niveau })),
  })),
});

/** À quelle notion appartient une question, d'après son identifiant. */
const notionDe = (item: string) => item.split('-e')[0];
const leconDe = (item: string) => item.split('-n')[0];

export function verifierComposition(): number {
  const trois = [lecon('A', 3), lecon('B', 3), lecon('C', 3)];

  // ── La taille ────────────────────────────────────────────────────────────
  verifie('taille : vingt questions demandées, vingt tirées',
    tirerQuestions(trois, 20).length === 20);
  verifie('taille : dix questions demandées, dix tirées',
    tirerQuestions(trois, 10).length === 10);
  verifie('taille : rien demandé, rien tiré', tirerQuestions(trois, 0).length === 0);
  verifie('taille : aucune leçon, aucune question', tirerQuestions([], 20).length === 0);

  // Trois leçons de trois notions à quatre étapes font 36 questions. En
  // demander 50 doit en rendre 36, et non répéter.
  const tout = tirerQuestions(trois, 50);
  verifie('taille : on ne rend jamais plus que ce qui existe', tout.length === 36);
  verifie('taille : et jamais deux fois la même question',
    new Set(tout).size === tout.length);

  // ── Les leçons ───────────────────────────────────────────────────────────
  const dix = tirerQuestions(trois, 10);
  const lecons = new Set(dix.map(leconDe));
  verifie('leçons : les trois sont représentées', lecons.size === 3);
  const parLecon = ['A', 'B', 'C'].map((l) => dix.filter((q) => leconDe(q) === l).length);
  verifie('leçons : l’écart entre elles ne dépasse pas une question',
    Math.max(...parLecon) - Math.min(...parLecon) <= 1);

  // Une leçon n'épuise pas les autres : les trois premières questions
  // viennent de trois leçons différentes.
  verifie('leçons : les trois premières questions viennent de trois leçons',
    new Set(dix.slice(0, 3).map(leconDe)).size === 3);

  // ── Les notions ──────────────────────────────────────────────────────────
  // Neuf notions en tout : les neuf premières questions doivent venir de
  // neuf notions différentes. Revenir sur une notion avant que toutes aient
  // été interrogées serait mesurer deux fois la même chose.
  const neuf = tirerQuestions(trois, 9);
  verifie('notions : les neuf premières questions touchent neuf notions',
    new Set(neuf.map(notionDe)).size === 9);

  const douze = tirerQuestions(trois, 12);
  const compteNotions: Record<string, number> = {};
  for (const q of douze) compteNotions[notionDe(q)] = (compteNotions[notionDe(q)] ?? 0) + 1;
  const compte = Object.values(compteNotions);
  verifie('notions : douze questions se répartissent sur les neuf notions',
    Object.keys(compteNotions).length === 9);
  verifie('notions : aucune notion n’est posée trois fois quand d’autres le sont une',
    Math.max(...compte) - Math.min(...compte) <= 1);

  // ── Les étapes ───────────────────────────────────────────────────────────
  const etapeDe = (item: string) => Number(item.split('-e')[1]);
  const vingt = tirerQuestions(trois, 20);
  const etapes = new Set(vingt.map(etapeDe));
  verifie('étapes : les quatre sont présentes', etapes.size === 4);
  const parEtape = [1, 2, 3, 4].map((e) => vingt.filter((q) => etapeDe(q) === e).length);
  verifie('étapes : elles sont servies également, à une près',
    Math.max(...parEtape) - Math.min(...parEtape) <= 1);

  // Une notion sans question de Défi ne doit pas bloquer le tour : on prend
  // l'étape la plus proche, et la composition garde sa taille.
  const bancales = [lecon('D', 2, [1, 2]), lecon('E', 2)];
  const mixte = tirerQuestions(bancales, 8);
  verifie('étapes : une notion sans Défi ne fait pas sauter son tour',
    mixte.length === 8 && new Set(mixte).size === 8);

  // ── Les notions vides ────────────────────────────────────────────────────
  const avecVide: LeconPourTirage[] = [
    { id: 'F', notions: [{ id: 'F-n0', items: [] }, ...lecon('F', 1).notions] },
    lecon('G', 1),
  ];
  const sansVide = tirerQuestions(avecVide, 8);
  verifie('notions vides : elles sont écartées sans rien casser',
    sansVide.length === 8 && new Set(sansVide).size === 8);

  // ── La note et l’état ────────────────────────────────────────────────────
  verifie('note : elle se lit juste sur posées', note(14, 20) === '14 / 20');

  const base: CompositionRow = {
    id: 'c', parent_id: 'p', child_id: 'e', titre: 'Séquence 2',
    lessons: ['L'], questions: ['q'], commencee_le: null, finie_le: null,
    justes: null, created_at: '2026-11-11T08:00:00Z',
  };
  verifie('état : jamais ouverte, elle est à faire',
    etatDeLaComposition(base) === 'a_faire');
  verifie('état : commencée et pas finie, elle est en cours',
    etatDeLaComposition({ ...base, commencee_le: '2026-11-11T09:00:00Z' }) === 'en_cours');
  verifie('état : finie, elle est finie',
    etatDeLaComposition({
      ...base, commencee_le: '2026-11-11T09:00:00Z', finie_le: '2026-11-11T09:20:00Z',
    }) === 'finie');

  // ── Les anciennes compositions gardent leur note ─────────────────────────
  // Trois ont été passées avant la forme d'épreuve : 18 sur 20, 19 sur 30,
  // 22 sur 30. Elles n'ont jamais eu d'oral, et leur total ne doit pas
  // grossir de quatre points.
  const vingtQuestions = Array.from({ length: 20 }, (_, i) => 'q' + i);
  const ancienne = { created_at: '2026-11-10T22:24:00+00:00', questions: vingtQuestions };
  const derniereAncienne = { created_at: '2026-11-11T18:31:00+00:00', questions: vingtQuestions };
  const nouvelle = { created_at: '2026-11-11T19:22:00+00:00', questions: vingtQuestions.slice(0, 16) };
  verifie('ancienne : une composition du 10 novembre n’a pas d’oral', pointsOralDe(ancienne) === 0);
  verifie('ancienne : elle reste notée sur ses vingt questions', totalDe(ancienne) === 20);
  verifie('ancienne : la dernière d’avant le changement aussi', totalDe(derniereAncienne) === 20);
  verifie('nouvelle : une composition d’après a ses quatre points d’oral',
    pointsOralDe(nouvelle) === 4);
  verifie('nouvelle : seize questions écrites font une épreuve sur 20', totalDe(nouvelle) === 20);
  verifie('nouvelle : la date pivot elle-même est du nouveau format',
    pointsOralDe({ created_at: EPREUVE_DEPUIS }) === 4);
  verifie('nouvelle : le fuseau de la date ne change rien',
    pointsOralDe({ created_at: '2026-11-11T20:30:00+01:00' }) === 4 &&
      pointsOralDe({ created_at: '2026-11-11T19:30:00+01:00' }) === 0);
  verifie('barème : une épreuve sur 30 tire 26 questions écrites', questionsEcritesPour(30) === 26);
  verifie('barème : une épreuve sur 20 en tire 16', questionsEcritesPour(20) === 16);

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
  return echecs;
}

verifierComposition();
