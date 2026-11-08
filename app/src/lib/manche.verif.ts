import {
  decouperEnSeries,
  lireValidation,
  meilleurJustes,
  pointsConsolation,
  pointsManche,
  questionsDeLaManche,
  serieParfaite,
  type MancheRow,
  type Reponse,
} from './manche';
import type { NotionAvecItems } from './paliers';

/**
 * La règle de validation, vérifiée cas par cas.
 *
 * Elle ne vit que dans lireValidation, et elle décide de ce qu'on affirme au
 * parent : « il sait cette leçon ». Une erreur ici ne casse rien à l'écran,
 * elle ment — c'est pourquoi elle se vérifie à part, et pourquoi chaque cas
 * porte le nom de la situation réelle qu'il représente.
 *
 * Depuis le découpage en séries, trois choses de plus se jouent ici :
 *
 *   Le découpage lui-même. Une notion coupée en deux, ou une série de trois
 *   questions laissée en moignon, et la règle du sans-faute perd son sens.
 *
 *   Ce qu'une manche COUVRE. Une série n'est tenue que par une manche qui
 *   portait au moins ses notions. Si cette règle se relâche, l'app affirme
 *   une leçon sue sur la foi d'une série voisine.
 *
 *   Les manches d'avant. Elles n'ont pas de liste de notions, et elles
 *   portaient toute la leçon : elles doivent donc tenir chaque série, sans
 *   qu'on réécrive quoi que ce soit en base.
 *
 * Le projet n'a pas de lanceur de tests. Celui-ci se construit et se joue :
 *
 *   cd app
 *   node_modules/.bin/esbuild src/lib/manche.verif.ts --bundle --platform=node \
 *     --format=esm --define:import.meta.env='{"VITE_SUPABASE_URL":"https://x.test",
 *     "VITE_SUPABASE_PUBLISHABLE_KEY":"x"}' --outfile=../work/manche.verif.mjs
 *   node ../work/manche.verif.mjs
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

/** La leçon des cas d'avant : une seule série, qui est toute la leçon. */
const TOUT = [['n1', 'n2', 'n3', 'n4', 'n5']];

/**
 * Une manche d'avant le découpage : vingt questions, sans liste de notions.
 *
 * C'est exactement ce que porte la base aujourd'hui, et le but est que ces
 * lignes continuent de valider ce qu'elles validaient.
 */
const manche = (iso: string, reussie: boolean, ratees: string[] = []): MancheRow => ({
  lesson_id: 'L',
  questions: 20,
  justes: reussie ? 20 : 20 - ratees.length,
  reussie,
  notions_ratees: ratees,
  created_at: iso,
});

/** Une série jouée, avec les notions qu'elle couvrait. */
const serie = (
  iso: string,
  notions: string[],
  justes: number,
  questions = 10,
  ratees: string[] = [],
): MancheRow => ({
  lesson_id: 'L',
  questions,
  justes,
  reussie: justes === questions,
  notions_ratees: ratees,
  notions,
  created_at: iso,
});

const faux = (notion: string, iso: string): Reponse => ({
  notion_id: notion,
  correct: false,
  created_at: iso,
});
const juste = (notion: string, iso: string): Reponse => ({
  notion_id: notion,
  correct: true,
  created_at: iso,
});

/** Une notion de n questions, pour éprouver le découpage. */
const n = (id: string, questions: number) => ({ id, items: Array(questions).fill(0) });
const tailles = (series: Array<{ items: unknown[] }[]>) =>
  series.map((s) => s.reduce((t, x) => t + x.items.length, 0)).join();

export function verifierManche(): number {
  // ── Le découpage en séries ───────────────────────────────────────────────
  // Quinze fixe le NOMBRE de séries — arrondi au-dessus — puis les notions
  // sont réparties aussi également que possible. Une notion n'est jamais
  // coupée en deux, donc une série peut dépasser quinze d'une notion.

  const dixDeTrois = decouperEnSeries(Array.from({ length: 10 }, (_, i) => n('n' + i, 3)));
  verifie('découpage : 30 questions font deux séries', dixDeTrois.length === 2);
  verifie('découpage : 30 questions en 15, 15', tailles(dixDeTrois) === '15,15');
  verifie(
    'découpage : aucune notion perdue',
    dixDeTrois.flat().map((x) => x.id).join() === 'n0,n1,n2,n3,n4,n5,n6,n7,n8,n9',
  );

  const septDeQuatre = decouperEnSeries(Array.from({ length: 7 }, (_, i) => n('n' + i, 4)));
  verifie('découpage : 28 questions en 16, 12', tailles(septDeQuatre) === '16,12');

  // La leçon la plus longue du catalogue : onze notions, 85 questions. Elle
  // était inatteignable d'une traite — trois sans-faute sur cent.
  const grande = decouperEnSeries([
    ...Array.from({ length: 10 }, (_, i) => n('n' + i, 8)),
    n('derniere', 5),
  ]);
  verifie('découpage : 85 questions font six séries', grande.length === 6);
  verifie(
    'découpage : 85 questions en 16, 16, 16, 16, 8, 13',
    tailles(grande) === '16,16,16,16,8,13',
  );
  // Le plafond dur, essayé puis abandonné, donnait ici DIX séries de huit :
  // deux notions de huit font seize, donc elles ne s'appariaient jamais.
  verifie('découpage : 85 questions ne tombent pas en dix séries', grande.length < 10);

  // Le dépassement existe, mais il ne vaut jamais plus d'une notion : sans
  // cette borne, « quinze questions » ne voudrait plus rien dire.
  verifie(
    'découpage : jamais plus de quinze, à une notion près',
    [dixDeTrois, septDeQuatre, grande].every((series) =>
      series.every((s) => {
        const total = s.reduce((t, x) => t + x.items.length, 0);
        const derniere = s[s.length - 1].items.length;
        return total <= 15 || total - derniere < 15;
      }),
    ),
  );

  // Pas de moignon : le pire défaut d'un découpage glouton est de laisser
  // trois questions à la fin, qui se gagnent sans rien prouver.
  verifie(
    'découpage : aucune série de moins de six questions',
    [...dixDeTrois, ...septDeQuatre].every(
      (s) => s.reduce((t, x) => t + x.items.length, 0) >= 6,
    ),
  );

  // Le tiers du catalogue tient entre 15 et 24 questions. Pris comme cible,
  // quinze les ramènerait à une seule manche : c'est tout l'objet du plafond.
  verifie(
    'découpage : 22 questions font deux séries, et non une',
    tailles(decouperEnSeries(Array.from({ length: 11 }, (_, i) => n('n' + i, 2)))) === '12,10',
  );
  verifie(
    'découpage : 16 questions font deux séries',
    tailles(decouperEnSeries(Array.from({ length: 8 }, (_, i) => n('n' + i, 2)))) === '8,8',
  );
  // Quinze questions pile, le minimum du catalogue : le seul cas où le
  // découpage ne découpait rien, parce que quinze sur quinze fait une série.
  // C'était aussi le pire — quinze d'affilée passent sans faute un peu plus
  // d'une fois sur deux. D'où le plancher de deux séries.
  verifie(
    'découpage : une leçon de quinze fait deux séries',
    tailles(decouperEnSeries([n('a', 5), n('b', 5), n('c', 5)])) === '10,5',
  );
  verifie(
    'découpage : quinze en quatre notions se coupe par le milieu',
    tailles(decouperEnSeries([n('a', 4), n('b', 4), n('c', 4), n('d', 3)])) === '8,7',
  );
  // Le plancher ne s'applique qu'au compte initial : sinon le reste de quinze
  // d'une leçon de trente se recouperait, et trente ferait trois séries.
  verifie(
    'découpage : trente questions font deux séries, pas trois',
    tailles(decouperEnSeries([n('a', 15), n('b', 15)])) === '15,15',
  );
  // Quatorze reste d'un seul tenant : le plancher dit « quinze se coupe », pas
  // « tout se coupe ». Une leçon courte jouée en deux moitiés de sept ne
  // prouverait rien de plus et ferait deux annonces pour rien.
  verifie(
    'découpage : quatorze questions restent une seule manche',
    tailles(decouperEnSeries([n('a', 5), n('b', 5), n('c', 4)])) === '14',
  );
  // Une notion ne se coupe jamais : une leçon de quinze questions portées par
  // UNE notion ne peut pas faire deux séries, et le plancher ne la force pas.
  verifie(
    'découpage : quinze en une seule notion restent une manche',
    tailles(decouperEnSeries([n('a', 15)])) === '15',
  );
  verifie(
    'découpage : une notion ne se coupe pas, même à 40 questions',
    tailles(decouperEnSeries([n('a', 40)])) === '40',
  );
  verifie('découpage : une leçon vide ne donne rien', decouperEnSeries([]).length === 0);
  verifie(
    'découpage : une notion sans question est écartée',
    tailles(decouperEnSeries([n('a', 5), n('vide', 0), n('b', 5)])) === '10',
  );

  // ── Avant toute manche ──────────────────────────────────────────────────
  let v = lireValidation(TOUT, [], []);
  verifie('jamais tentée : la leçon n’est pas validée', !v.validee && !v.dejaTentee);
  verifie('jamais tentée : rien à reprendre', v.aReprendre.length === 0);
  verifie('jamais tentée : on joue la première série', v.serieEnCours === 1);
  verifie('jamais tentée : rien de tenu', v.seriesTenues === 0 && v.seriesTotal === 1);

  // ── Une manche ratée ────────────────────────────────────────────────────
  v = lireValidation(TOUT, [manche('2026-10-18T10:00:00Z', false, ['n1', 'n3'])], [
    faux('n1', '2026-10-18T10:00:00Z'),
  ]);
  verifie('manche ratée : non validée', !v.validee && v.dejaTentee);
  verifie('manche ratée : on redonne ses notions fautives', v.aReprendre.join() === 'n1,n3');
  verifie('manche ratée : ce n’est pas une série à regagner', !v.serieARegagner);

  // ── La reprise se termine ───────────────────────────────────────────────
  // Sans cette sortie, la manche ratée garderait pour toujours la trace des
  // notions manquées, et l’enfant rejouerait les mêmes questions à l’infini.
  v = lireValidation(TOUT, [manche('2026-10-18T10:00:00Z', false, ['n1', 'n3'])], [
    faux('n1', '2026-10-18T10:00:00Z'),
    juste('n1', '2026-10-18T10:30:00Z'),
  ]);
  verifie('reprise : la notion réussie sort de la liste', v.aReprendre.join() === 'n3');

  v = lireValidation(TOUT, [manche('2026-10-18T10:00:00Z', false, ['n1', 'n3'])], [
    juste('n1', '2026-10-18T10:30:00Z'),
    juste('n3', '2026-10-18T10:31:00Z'),
  ]);
  verifie('reprise finie : la manche revient', v.aReprendre.length === 0 && !v.validee);

  v = lireValidation(TOUT, [manche('2026-10-18T10:00:00Z', false, ['n1'])], [
    juste('n1', '2026-10-18T10:30:00Z'),
    faux('n1', '2026-10-18T10:40:00Z'),
  ]);
  verifie('reprise : ratée de nouveau, la notion reste', v.aReprendre.join() === 'n1');

  // ── Une manche réussie ──────────────────────────────────────────────────
  v = lireValidation(TOUT, [manche('2026-10-18T11:00:00Z', true)], [
    faux('n1', '2026-10-18T09:00:00Z'),
  ]);
  verifie('réussie : validée malgré une faute antérieure', v.validee && v.perdueLe === null);
  verifie('réussie : rien à reprendre', v.aReprendre.length === 0);
  verifie('réussie : plus de série à jouer', v.serieEnCours === 0 && v.seriesTenues === 1);

  // ── La validation se perd ───────────────────────────────────────────────
  v = lireValidation(TOUT, [manche('2026-10-18T11:00:00Z', true)], [
    faux('n2', '2026-10-25T08:00:00Z'),
  ]);
  verifie('faute postérieure : validation perdue', !v.validee);
  verifie('faute postérieure : datée', v.perdueLe === '2026-10-25T08:00:00Z');
  verifie('faute postérieure : on sait qu’il l’avait sue', v.obtenueLe === '2026-10-18T11:00:00Z');
  verifie('faute postérieure : on redonne la notion ratée', v.aReprendre.join() === 'n2');
  verifie('faute postérieure : la série est à regagner', v.serieARegagner);

  v = lireValidation(
    TOUT,
    [manche('2026-10-18T11:00:00Z', true)],
    [faux('n4', '2026-11-02T08:00:00Z'), faux('n2', '2026-10-25T08:00:00Z')],
  );
  verifie('fautes multiples : on date la première', v.perdueLe === '2026-10-25T08:00:00Z');
  verifie('fautes multiples : on redonne les deux', [...v.aReprendre].sort().join() === 'n2,n4');

  v = lireValidation(TOUT, [manche('2026-10-18T11:00:00Z', true)], [
    faux('n2', '2026-10-25T08:00:00Z'),
    juste('n2', '2026-10-25T08:05:00Z'),
  ]);
  verifie('perte reprise : plus rien à revoir', !v.validee && v.aReprendre.length === 0);
  verifie(
    'perte reprise : toujours à revalider tant que la manche n’est pas refaite',
    v.perdueLe === '2026-10-25T08:00:00Z',
  );

  // ── On revalide ─────────────────────────────────────────────────────────
  v = lireValidation(
    TOUT,
    [manche('2026-11-10T09:00:00Z', true), manche('2026-10-18T11:00:00Z', true)],
    [faux('n2', '2026-10-25T08:00:00Z')],
  );
  verifie('revalidée : la manche la plus récente fait foi', v.validee && v.perdueLe === null);

  v = lireValidation(
    TOUT,
    [manche('2026-11-01T09:00:00Z', false, ['n2', 'n5']), manche('2026-10-18T11:00:00Z', true)],
    [faux('n2', '2026-10-25T08:00:00Z')],
  );
  verifie(
    'perte puis échec : la manche ratée dit ce qui reste',
    [...v.aReprendre].sort().join() === 'n2,n5',
  );

  // ── La leçon en plusieurs séries ─────────────────────────────────────────
  // C'est tout l'objet du découpage : le sans-faute se tient sur dix
  // questions, et ce qui est tenu ne se rejoue pas.
  const DEUX = [
    ['a', 'b'],
    ['c', 'd'],
  ];

  v = lireValidation(DEUX, [], []);
  verifie('deux séries : on commence par la première', v.serieEnCours === 1);
  verifie('deux séries : la leçon n’est pas validée', !v.validee && v.seriesTotal === 2);

  v = lireValidation(DEUX, [serie('2026-11-08T10:00:00Z', ['a', 'b'], 10)], []);
  verifie('série 1 tenue : on passe à la deuxième', v.serieEnCours === 2 && v.seriesTenues === 1);
  verifie('série 1 tenue : la leçon ne l’est pas pour autant', !v.validee);
  verifie('série 1 tenue : rien de « validé le », la leçon n’a jamais été sue',
    v.obtenueLe === null && v.perdueLe === null);
  verifie('série 1 tenue : la deuxième n’a jamais été tentée', !v.dejaTentee);

  v = lireValidation(
    DEUX,
    [serie('2026-11-08T11:00:00Z', ['c', 'd'], 10), serie('2026-11-08T10:00:00Z', ['a', 'b'], 10)],
    [],
  );
  verifie('deux séries tenues : la leçon est validée', v.validee && v.seriesTenues === 2);
  verifie('deux séries tenues : datée de la dernière', v.obtenueLe === '2026-11-08T11:00:00Z');
  verifie('deux séries tenues : plus rien à jouer', v.serieEnCours === 0);

  // Une faute sur la première série ne renvoie QUE la première série. C'est
  // la raison d'être du découpage : il ne rejoue pas les trente questions.
  v = lireValidation(
    DEUX,
    [serie('2026-11-08T11:00:00Z', ['c', 'd'], 10), serie('2026-11-08T10:00:00Z', ['a', 'b'], 10)],
    [faux('a', '2026-11-12T08:00:00Z')],
  );
  verifie('faute sur la série 1 : elle seule revient', v.serieEnCours === 1 && !v.validee);
  verifie('faute sur la série 1 : la série 2 reste tenue', v.seriesTenues === 1);
  verifie('faute sur la série 1 : la validation est perdue, et datée',
    v.perdueLe === '2026-11-12T08:00:00Z' && v.obtenueLe === '2026-11-08T11:00:00Z');
  verifie('faute sur la série 1 : on redonne la notion ratée', v.aReprendre.join() === 'a');
  verifie('faute sur la série 1 : elle est à regagner', v.serieARegagner);

  // Une faute sur une notion d'une autre série ne casse rien.
  v = lireValidation(
    DEUX,
    [serie('2026-11-08T11:00:00Z', ['c', 'd'], 10), serie('2026-11-08T10:00:00Z', ['a', 'b'], 10)],
    [faux('c', '2026-11-12T08:00:00Z')],
  );
  verifie('faute sur la série 2 : la série 1 n’est pas touchée', v.serieEnCours === 2);

  // Une série ratée ne dit rien d'une autre série.
  v = lireValidation(
    DEUX,
    [serie('2026-11-08T10:00:00Z', ['c', 'd'], 8, 10, ['c'])],
    [faux('c', '2026-11-08T10:00:00Z')],
  );
  verifie('série 2 ratée : la série 1 reste à jouer', v.serieEnCours === 1);
  verifie('série 2 ratée : la série 1 n’est pas « déjà tentée »', !v.dejaTentee);
  verifie('série 2 ratée : rien à reprendre sur la série 1', v.aReprendre.length === 0);

  // ── Les manches d'avant le découpage ─────────────────────────────────────
  // Elles portaient toute la leçon, donc elles tiennent chaque série. Ce
  // n'est pas une indulgence : c'est exactement ce qui s'est passé.
  v = lireValidation(DEUX, [manche('2026-10-18T11:00:00Z', true)], []);
  verifie('manche d’avant : elle tient toutes les séries', v.validee && v.seriesTenues === 2);

  v = lireValidation(DEUX, [manche('2026-10-18T11:00:00Z', false, ['a', 'c'])], []);
  verifie('manche d’avant ratée : la série 1 est déjà tentée', v.dejaTentee);
  verifie(
    'manche d’avant ratée : on ne redonne que ce qui est dans la série',
    v.aReprendre.join() === 'a',
  );

  // Une manche portant les quatre notions tient les deux séries : la règle
  // est la couverture, et non l'égalité stricte.
  v = lireValidation(DEUX, [serie('2026-11-08T10:00:00Z', ['a', 'b', 'c', 'd'], 20, 20)], []);
  verifie('couverture : une série plus large tient les deux', v.validee);

  // ── L’ordre des questions ────────────────────────────────────────────────
  const notions = [
    { id: 'a', items: [{ id: 'a4', level: 4 }, { id: 'a1', level: 1 }] },
    { id: 'b', items: [{ id: 'b2', level: 2 }] },
  ] as unknown as NotionAvecItems[];
  const q = questionsDeLaManche(notions);
  verifie('manche : toutes les questions des notions données', q.length === 3);
  verifie(
    'manche : notion par notion, du plus facile au plus dur',
    q.map((x) => x.item.id).join() === 'a1,a4,b2',
  );

  // ── Le barème ────────────────────────────────────────────────────────────
  // Il décide de ce que l'enfant reçoit. Les scores cités sont ceux que
  // BRAYNE et KLEIN ont réellement obtenus sur les quarante premières manches.

  verifie('gain : proportionnel à la longueur', pointsManche(40) === 200);
  verifie('gain : une série courte rapporte moins', pointsManche(10) === 50);
  verifie(
    'gain : le découpage ne change pas le prix de la leçon',
    pointsManche(16) + pointsManche(12) === pointsManche(28),
  );

  verifie('consolation : 12/13 au premier essai', pointsConsolation(12, 13, 0) === 24);
  verifie('consolation : 38/40, le vrai score de BRAYNE', pointsConsolation(38, 40, 0) === 76);
  verifie(
    'consolation : refaire le même score ne rapporte rien',
    pointsConsolation(9, 10, 9) === 0,
  );
  verifie('consolation : progresser rapporte', pointsConsolation(9, 10, 8) === 18);
  verifie('consolation : sous 80 %, rien', pointsConsolation(7, 10, 0) === 0);
  verifie('consolation : à 80 % pile, elle est versée', pointsConsolation(8, 10, 0) === 16);
  verifie(
    'consolation : une série gagnée n’est pas une consolation',
    pointsConsolation(10, 10, 0) === 0,
  );
  verifie('consolation : une série vide ne rapporte rien', pointsConsolation(0, 0, 0) === 0);

  // Le meilleur score se compte SÉRIE PAR SÉRIE. Comparer les 9 justes d'une
  // série de dix aux 20 justes d'une leçon entière interdirait toute
  // consolation, à jamais.
  const jouees = [
    serie('2026-11-08T11:00:00Z', ['a', 'b'], 9, 10, ['a']),
    serie('2026-11-08T10:00:00Z', ['a', 'b'], 7, 10, ['a', 'b']),
    serie('2026-11-07T10:00:00Z', ['c', 'd'], 10),
    manche('2026-10-18T11:00:00Z', true),
  ];
  verifie('meilleur score : la plus haute de CETTE série', meilleurJustes(jouees, ['a', 'b']) === 9);
  verifie(
    'meilleur score : une autre série ne compte pas',
    meilleurJustes(jouees, ['e', 'f']) === 0,
  );
  verifie('meilleur score : aucune série jouée', meilleurJustes([], ['a']) === 0);

  verifie('suite : aucune manche', serieParfaite([]) === 0);
  verifie(
    'suite : deux sans faute puis une ratée',
    serieParfaite([
      manche('2026-11-03', true),
      manche('2026-11-02', true),
      manche('2026-11-01', false, ['n1']),
      manche('2026-10-31', true),
    ]) === 2,
  );
  verifie(
    'suite : la dernière est ratée, la suite est rompue',
    serieParfaite([manche('2026-11-03', false, ['n1']), manche('2026-11-02', true)]) === 0,
  );

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
  return echecs;
}

verifierManche();
