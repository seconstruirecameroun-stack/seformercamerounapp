/**
 * Ce que la forme d'une épreuve doit garantir.
 *
 * La situation problème est fabriquée, pas écrite : si une question de
 * l'oral demandait une chose que le texte ne dit pas, l'enfant perdrait un
 * point sur une question sans réponse, et rien à l'écran ne le montrerait.
 * De même pour l'appréciation : une lettre qui ne correspond pas à celle
 * que la maîtresse aurait mise est une note qui ment.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/epreuve.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/epreuve.verif.mjs
 *   node ../work/epreuve.verif.mjs
 */

import {
  POINTS_ORAL,
  appreciation,
  exercices,
  graine,
  matiereDeLEpreuve,
  mention,
  situationProbleme,
  totalDeLEpreuve,
  type LeconDEpreuve,
} from './epreuve';

let echecs = 0;

function verifie(nom: string, condition: boolean) {
  if (condition) {
    console.log('  ok     ' + nom);
  } else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

const L = (id: string, title: string, matiere = 'Français'): LeconDEpreuve => ({ id, title, matiere });

export function verifierEpreuve(): number {
  const deux = [L('a', 'Le féminin des noms'), L('b', 'Le groupe du verbe')];
  const cinq = [
    L('a', 'Le verbe'), L('b', 'Le conte'), L('c', 'La centaine', 'Mathématiques'),
    L('d', 'Le pavé', 'Mathématiques'), L('e', 'La végétation', 'Géographie'),
  ];

  // ── La situation est figée ────────────────────────────────────────────────
  const s1 = situationProbleme('compo-1', 'CE1', deux);
  const s1bis = situationProbleme('compo-1', 'CE1', deux);
  verifie('situation : la même composition raconte la même histoire',
    s1.texte === s1bis.texte && JSON.stringify(s1.oral) === JSON.stringify(s1bis.oral));
  const heros = new Set(
    Array.from({ length: 40 }, (_, i) => situationProbleme('compo-' + i, 'CE1', deux).heros),
  );
  verifie('situation : toutes les compositions n’ont pas le même héros', heros.size >= 4);
  verifie('graine : le même texte donne le même nombre', graine('abc') === graine('abc'));
  verifie('graine : deux textes donnent deux nombres', graine('abc') !== graine('abd'));

  // ── Le texte dit ce qu'il faut ────────────────────────────────────────────
  verifie('texte : il nomme le héros', s1.texte.includes(s1.heros));
  verifie('texte : il nomme la classe', s1.texte.includes('au CE1'));
  verifie('texte : il nomme les leçons annoncées',
    s1.texte.includes('Le féminin des noms') && s1.texte.includes('Le groupe du verbe'));
  verifie('texte : deux leçons se lient par « et »',
    s1.texte.includes('« Le féminin des noms » et « Le groupe du verbe »'));
  const s5 = situationProbleme('compo-5', 'CM1', cinq);
  verifie('texte : au-delà de trois leçons, il n’en cite que trois',
    s5.texte.includes('Le verbe') && s5.texte.includes('La centaine') && !s5.texte.includes('Le pavé'));
  verifie('texte : et il dit qu’il y en a d’autres', s5.texte.includes('d’autres encore'));
  verifie('texte : avec deux leçons, il ne promet rien de plus', !s1.texte.includes('d’autres encore'));
  verifie('texte : une seule leçon s’écrit sans « et »',
    situationProbleme('x', 'CE1', [deux[0]]).texte.includes('portent sur : « Le féminin des noms ».'));
  verifie('texte : il demande de l’aide', s1.texte.includes('Il veut que tu l’aides'));
  verifie('texte : aucune apostrophe droite', !s1.texte.includes("'") && !s5.texte.includes("'"));

  // ── L'oral ne demande rien que le texte ne dise ───────────────────────────
  for (const [nom, s] of [['deux leçons', s1], ['cinq leçons', s5]] as const) {
    verifie(`oral (${nom}) : ${POINTS_ORAL} questions`, s.oral.length === POINTS_ORAL);
    verifie(`oral (${nom}) : trois choix distincts par question`,
      s.oral.every((q) => q.options.length === 3 && new Set(q.options).size === 3));
    verifie(`oral (${nom}) : chaque bonne réponse est écrite dans le texte`,
      s.oral.every((q) => s.texte.toLowerCase().includes(q.options[0].toLowerCase())));
    verifie(`oral (${nom}) : aucune mauvaise réponse n’est écrite dans le texte`,
      s.oral.every((q) => q.options.slice(1).every((o) => !s.texte.toLowerCase().includes(o.toLowerCase()))));
    verifie(`oral (${nom}) : aucune apostrophe droite`,
      s.oral.every((q) => !q.question.includes("'") && q.options.every((o) => !o.includes("'"))));
  }
  verifie('oral : la première question demande de qui parle le texte',
    s1.oral[0].question === 'De qui parle le texte ?' && s1.oral[0].options[0] === s1.heros);
  verifie('oral : la classe demandée est celle de l’enfant', s5.oral[1].options[0] === 'CM1');
  const inconnue = situationProbleme('y', 'Class 3', deux);
  verifie('oral : une classe hors liste garde trois choix distincts',
    new Set(inconnue.oral[1].options).size === 3 && inconnue.oral[1].options[0] === 'Class 3');
  // Sur beaucoup de compositions, jamais un choix en double ni une bonne
  // réponse absente : le tirage des mauvaises réponses ne doit pas retomber
  // sur la bonne.
  let propre = true;
  for (let i = 0; i < 300; i++) {
    const s = situationProbleme('essai-' + i, CLASSE_AU_HASARD[i % CLASSE_AU_HASARD.length], deux);
    for (const q of s.oral) {
      if (new Set(q.options).size !== q.options.length) propre = false;
      if (!s.texte.toLowerCase().includes(q.options[0].toLowerCase())) propre = false;
    }
  }
  verifie('oral : trois cents compositions, aucun choix en double, aucune réponse introuvable', propre);

  // ── Le nom de l'épreuve ───────────────────────────────────────────────────
  verifie('épreuve : une seule matière donne son nom', matiereDeLEpreuve(deux) === 'Français');
  verifie('épreuve : plusieurs matières sont dites telles',
    matiereDeLEpreuve(cinq) === 'Plusieurs matières');
  verifie('épreuve : aucune leçon, aucun nom', matiereDeLEpreuve([]) === '');

  // ── Les exercices ─────────────────────────────────────────────────────────
  const ordre = ['a1', 'b1', 'a2', 'b2', 'a3'];
  const leconDe = new Map([['a1', 'a'], ['a2', 'a'], ['a3', 'a'], ['b1', 'b'], ['b2', 'b']]);
  const ex = exercices(ordre, leconDe, deux);
  verifie('exercices : un par leçon', ex.length === 2);
  verifie('exercices : numérotés à partir de 1', ex[0].numero === 1 && ex[1].numero === 2);
  verifie('exercices : dans l’ordre où les leçons ont été annoncées',
    ex[0].lecon.id === 'a' && ex[1].lecon.id === 'b');
  verifie('exercices : les questions d’une leçon sont regroupées',
    ex[0].questions.join() === 'a1,a2,a3' && ex[1].questions.join() === 'b1,b2');
  verifie('exercices : aucune question perdue, aucune en double',
    ex.flatMap((e) => e.questions).sort().join() === [...ordre].sort().join());
  const inverse = exercices(ordre, leconDe, [deux[1], deux[0]]);
  verifie('exercices : l’ordre suit l’annonce, pas le tirage', inverse[0].lecon.id === 'b');
  verifie('exercices : une leçon sans question ne fait pas d’exercice vide',
    exercices(['a1'], leconDe, deux).length === 1);
  verifie('exercices : une question dont on ignore la leçon est écartée',
    exercices(['a1', 'zz'], leconDe, deux).flatMap((e) => e.questions).join() === 'a1');
  verifie('exercices : rien à poser, aucun exercice', exercices([], leconDe, deux).length === 0);

  // ── Le barème ─────────────────────────────────────────────────────────────
  verifie('barème : 26 questions écrites font une épreuve sur 30', totalDeLEpreuve(26) === 30);
  verifie('barème : 36 questions écrites font une épreuve sur 40', totalDeLEpreuve(36) === 40);

  // ── L'appréciation, contre les copies de l'école ──────────────────────────
  verifie('mention : 28 sur 30 → A+ (copie de français)', mention(28, 30) === 'A+');
  verifie('mention : 37 sur 40 → A+ (copie de TIC)', mention(37, 40) === 'A+');
  verifie('mention : 40 sur 40 → A+ (copie de mathématiques)', mention(40, 40) === 'A+');
  verifie('mention : 27 sur 30 → A+ (révision du 10 novembre)', mention(27, 30) === 'A+');
  verifie('mention : 23 sur 30 → A (devoir de TIC du 6 novembre)', mention(23, 30) === 'A');
  verifie('mention : 20 sur 30 → B', mention(20, 30) === 'B');
  verifie('mention : la moitié → C', mention(15, 30) === 'C');
  verifie('mention : sous la moitié → D', mention(14, 30) === 'D');
  verifie('mention : zéro → D', mention(0, 30) === 'D');
  verifie('mention : une épreuve vide ne divise pas par zéro', mention(0, 0) === 'D');
  verifie('appréciation : chaque lettre a ses mots',
    new Set((['A+', 'A', 'B', 'C', 'D'] as const).map(appreciation)).size === 5);

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
  return echecs;
}

const CLASSE_AU_HASARD = ['SIL', 'CP', 'CE1', 'CE2', 'CM1', 'CM2'];

verifierEpreuve();
