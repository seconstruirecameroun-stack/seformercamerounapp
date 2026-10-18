import { lireValidation, questionsDeLaManche, type MancheRow, type Reponse } from './manche';
import type { NotionAvecItems } from './paliers';

/**
 * La règle de validation, vérifiée cas par cas.
 *
 * Elle ne vit que dans lireValidation, et elle décide de ce qu'on affirme au
 * parent : « il sait cette leçon ». Une erreur ici ne casse rien à l'écran,
 * elle ment — c'est pourquoi elle se vérifie à part, et pourquoi chaque cas
 * porte le nom de la situation réelle qu'il représente.
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

/** Une manche jouée : vingt questions, et celles qui ont été ratées. */
const manche = (iso: string, reussie: boolean, ratees: string[] = []): MancheRow => ({
  lesson_id: 'L',
  questions: 20,
  justes: reussie ? 20 : 20 - ratees.length,
  reussie,
  notions_ratees: ratees,
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

export function verifierManche(): number {
  // ── Avant toute manche ──────────────────────────────────────────────────
  let v = lireValidation([], []);
  verifie('jamais tentée : la leçon n’est pas validée', !v.validee && !v.dejaTentee);
  verifie('jamais tentée : rien à reprendre', v.aReprendre.length === 0);

  // ── Une manche ratée ────────────────────────────────────────────────────
  v = lireValidation([manche('2026-10-18T10:00:00Z', false, ['n1', 'n3'])], [
    faux('n1', '2026-10-18T10:00:00Z'),
  ]);
  verifie('manche ratée : non validée', !v.validee && v.dejaTentee);
  verifie('manche ratée : on redonne ses notions fautives', v.aReprendre.join() === 'n1,n3');

  // ── La reprise se termine ───────────────────────────────────────────────
  // Sans cette sortie, la manche ratée garderait pour toujours la trace des
  // notions manquées, et l’enfant rejouerait les mêmes questions à l’infini.
  v = lireValidation([manche('2026-10-18T10:00:00Z', false, ['n1', 'n3'])], [
    faux('n1', '2026-10-18T10:00:00Z'),
    juste('n1', '2026-10-18T10:30:00Z'),
  ]);
  verifie('reprise : la notion réussie sort de la liste', v.aReprendre.join() === 'n3');

  v = lireValidation([manche('2026-10-18T10:00:00Z', false, ['n1', 'n3'])], [
    juste('n1', '2026-10-18T10:30:00Z'),
    juste('n3', '2026-10-18T10:31:00Z'),
  ]);
  verifie('reprise finie : la manche revient', v.aReprendre.length === 0 && !v.validee);

  v = lireValidation([manche('2026-10-18T10:00:00Z', false, ['n1'])], [
    juste('n1', '2026-10-18T10:30:00Z'),
    faux('n1', '2026-10-18T10:40:00Z'),
  ]);
  verifie('reprise : ratée de nouveau, la notion reste', v.aReprendre.join() === 'n1');

  // ── Une manche réussie ──────────────────────────────────────────────────
  v = lireValidation([manche('2026-10-18T11:00:00Z', true)], [faux('n1', '2026-10-18T09:00:00Z')]);
  verifie('réussie : validée malgré une faute antérieure', v.validee && v.perdueLe === null);
  verifie('réussie : rien à reprendre', v.aReprendre.length === 0);

  // ── La validation se perd ───────────────────────────────────────────────
  v = lireValidation([manche('2026-10-18T11:00:00Z', true)], [faux('n2', '2026-10-25T08:00:00Z')]);
  verifie('faute postérieure : validation perdue', !v.validee);
  verifie('faute postérieure : datée', v.perdueLe === '2026-10-25T08:00:00Z');
  verifie('faute postérieure : on sait qu’il l’avait sue', v.obtenueLe === '2026-10-18T11:00:00Z');
  verifie('faute postérieure : on redonne la notion ratée', v.aReprendre.join() === 'n2');

  v = lireValidation(
    [manche('2026-10-18T11:00:00Z', true)],
    [faux('n4', '2026-11-02T08:00:00Z'), faux('n2', '2026-10-25T08:00:00Z')],
  );
  verifie('fautes multiples : on date la première', v.perdueLe === '2026-10-25T08:00:00Z');
  verifie('fautes multiples : on redonne les deux', [...v.aReprendre].sort().join() === 'n2,n4');

  v = lireValidation([manche('2026-10-18T11:00:00Z', true)], [
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
    [manche('2026-11-10T09:00:00Z', true), manche('2026-10-18T11:00:00Z', true)],
    [faux('n2', '2026-10-25T08:00:00Z')],
  );
  verifie('revalidée : la manche la plus récente fait foi', v.validee && v.perdueLe === null);

  v = lireValidation(
    [manche('2026-11-01T09:00:00Z', false, ['n2', 'n5']), manche('2026-10-18T11:00:00Z', true)],
    [faux('n2', '2026-10-25T08:00:00Z')],
  );
  verifie(
    'perte puis échec : la manche ratée dit ce qui reste',
    [...v.aReprendre].sort().join() === 'n2,n5',
  );

  // ── L’ordre des questions ────────────────────────────────────────────────
  const notions = [
    { id: 'a', items: [{ id: 'a4', level: 4 }, { id: 'a1', level: 1 }] },
    { id: 'b', items: [{ id: 'b2', level: 2 }] },
  ] as unknown as NotionAvecItems[];
  const q = questionsDeLaManche(notions);
  verifie('manche : toutes les questions de la leçon', q.length === 3);
  verifie(
    'manche : notion par notion, du plus facile au plus dur',
    q.map((x) => x.item.id).join() === 'a1,a4,b2',
  );

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
  return echecs;
}

verifierManche();
