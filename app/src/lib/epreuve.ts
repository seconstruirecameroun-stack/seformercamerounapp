/**
 * L'épreuve : la forme que prend une composition à l'école.
 *
 * Le père a apporté trois copies de son fils — français, TIC, mathématiques,
 * « évaluation de fin de mois de septembre ». Elles ont toutes la même
 * charpente, et la composition de l'app ne l'avait pas :
 *
 *   une SITUATION PROBLÈME en tête — un enfant a manqué l'école, il ne peut
 *   pas faire ses devoirs sur telles notions, « il veut que tu l'aides » ;
 *
 *   un ORAL, quelques questions sur ce petit texte : de qui parle-t-il,
 *   dans quelle classe est-il, pourquoi a-t-il besoin d'aide ;
 *
 *   un ÉCRIT, fait d'EXERCICES : chaque exercice porte sur une notion, et
 *   affiche ses points ;
 *
 *   une NOTE sur 30 ou sur 40, et une appréciation en lettre.
 *
 * Rien de tout cela n'est stocké. La situation se déduit de la composition
 * elle-même : le même identifiant donne toujours le même héros et la même
 * histoire, si bien qu'un enfant qui revient retrouve le texte qu'il a lu.
 * C'est la règle de la maison — ce qui se déduit ne s'écrit pas.
 *
 * Ce que l'app ne note pas : le « savoir-être » des copies (propreté,
 * respect des consignes). Un écran ne se salit pas, et donner ces points
 * d'office reviendrait à gonfler toutes les notes de la même quantité.
 */

/** Les questions de l'oral : une par point, comme sur la copie de TIC. */
export const POINTS_ORAL = 4;

/** Les épreuves de l'école sont sur 30 ou sur 40 ; vingt points font une petite épreuve. */
export const BAREMES = [20, 30, 40] as const;

export type LeconDEpreuve = { id: string; title: string; matiere: string };

export type QuestionOrale = {
  question: string;
  /** La bonne réponse est la première ; l'écran mélange avant de montrer. */
  options: string[];
};

export type Situation = {
  heros: string;
  texte: string;
  oral: QuestionOrale[];
};

/** Les prénoms des copies de l'école, et quelques autres du même pays. */
const HEROS = ['Olama', 'Mbamba', 'Njoya', 'Onana', 'Etoundi', 'Zogo', 'Fouda', 'Atangana'];

const CAUSES = [
  { texte: 'à cause de la varicelle', courte: 'À cause de la varicelle' },
  { texte: 'à cause du paludisme', courte: 'À cause du paludisme' },
  { texte: 'à cause d’une forte grippe', courte: 'À cause d’une forte grippe' },
];

const DUREES = ['une semaine', 'deux semaines', 'trois semaines'];

const CLASSES = ['SIL', 'CP', 'CE1', 'CE2', 'CM1', 'CM2'];

/**
 * Un nombre tiré d'un texte, toujours le même pour le même texte.
 *
 * Le hasard d'une épreuve doit être figé : deux ouvertures de la même
 * composition ne peuvent pas raconter deux histoires.
 */
export function graine(texte: string): number {
  let h = 2166136261;
  for (let i = 0; i < texte.length; i++) {
    h ^= texte.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

function choisir<T>(liste: T[], g: number, decalage: number): T {
  return liste[(g >>> decalage) % liste.length];
}

/** Trois autres éléments de la liste, jamais celui qu'on écarte. */
function autres<T>(liste: T[], sauf: T, g: number, combien: number): T[] {
  const reste = liste.filter((x) => x !== sauf);
  const depart = g % Math.max(1, reste.length);
  const sortie: T[] = [];
  for (let i = 0; i < reste.length && sortie.length < combien; i++) {
    sortie.push(reste[(depart + i) % reste.length]);
  }
  return sortie;
}

function enumerer(titres: string[]): string {
  if (titres.length <= 1) return titres[0] ?? '';
  return titres.slice(0, -1).join(', ') + ' et ' + titres[titres.length - 1];
}

/**
 * La situation problème et son oral.
 *
 * Le texte nomme les leçons annoncées — au plus trois, comme la copie qui
 * dit « les notions du nom, des groupes de verbes et même d'écriture » —
 * et les questions de l'oral ne demandent rien qui ne soit écrit dedans.
 */
export function situationProbleme(
  cle: string,
  classe: string,
  lecons: LeconDEpreuve[],
): Situation {
  const g = graine(cle);
  const heros = choisir(HEROS, g, 0);
  const cause = choisir(CAUSES, g, 5);
  const duree = choisir(DUREES, g, 9);
  // Les titres sont cités entre guillemets : beaucoup contiennent eux-mêmes
  // un « et », et « le féminin des noms et l'infinitif et les trois groupes »
  // ne laisse plus voir où finit une leçon et où commence la suivante.
  const citees = lecons.slice(0, 3).map((l) => `« ${l.title} »`);
  const suite = lecons.length > citees.length ? ', et d’autres encore' : '';

  const texte =
    `${heros} est élève au ${classe}. Il a passé ${duree} à la maison ${cause.texte}. ` +
    `Il ne peut pas faire ses devoirs, qui portent sur : ${enumerer(citees)}${suite}. ` +
    'Il veut que tu l’aides. Sers-toi de ce que tu as appris pour répondre à ces questions.';

  const oral: QuestionOrale[] = [
    {
      question: 'De qui parle le texte ?',
      options: [heros, ...autres(HEROS, heros, g >>> 3, 2)],
    },
    {
      question: `Dans quelle classe est ${heros} ?`,
      options: [classe, ...autres(CLASSES, classe, g >>> 7, 2)],
    },
    {
      question: `Pourquoi ${heros} est-il resté à la maison ?`,
      options: [cause.courte, 'Parce que c’étaient les vacances', 'Parce qu’il était en voyage'],
    },
    {
      question: `Combien de temps ${heros} a-t-il passé à la maison ?`,
      options: [duree, ...autres(DUREES, duree, g >>> 11, 2)],
    },
  ];

  return { heros, texte, oral: oral.slice(0, POINTS_ORAL) };
}

/**
 * Le nom de l'épreuve, comme dans l'en-tête de la copie.
 *
 * Une épreuve de l'école porte sur une matière. Si le parent en a coché
 * plusieurs, l'app le dit plutôt que d'en nommer une au hasard.
 */
export function matiereDeLEpreuve(lecons: LeconDEpreuve[]): string {
  const matieres = [...new Set(lecons.map((l) => l.matiere))];
  if (matieres.length === 0) return '';
  if (matieres.length === 1) return matieres[0];
  return 'Plusieurs matières';
}

export type Exercice = {
  numero: number;
  lecon: LeconDEpreuve;
  /** Les questions de l'exercice, dans l'ordre où elles seront posées. */
  questions: string[];
};

/**
 * Les exercices de l'écrit : les questions regroupées par leçon.
 *
 * Le tirage alterne les leçons pour n'en oublier aucune ; l'épreuve, elle,
 * se PASSE exercice par exercice, comme sur la copie — toutes les questions
 * sur le féminin des noms, puis toutes celles sur le groupe du verbe. Passer
 * d'une notion à l'autre à chaque question est une difficulté que l'école
 * n'impose pas.
 *
 * L'ordre des exercices est celui où le parent a annoncé les leçons, et
 * l'ordre des questions dans un exercice est celui du tirage.
 */
export function exercices(
  ordre: string[],
  leconDe: Map<string, string>,
  lecons: LeconDEpreuve[],
): Exercice[] {
  const parLecon = new Map<string, string[]>();
  for (const id of ordre) {
    const lecon = leconDe.get(id);
    if (!lecon) continue;
    const liste = parLecon.get(lecon) ?? [];
    liste.push(id);
    parLecon.set(lecon, liste);
  }
  const sortie: Exercice[] = [];
  for (const lecon of lecons) {
    const questions = parLecon.get(lecon.id);
    if (!questions || questions.length === 0) continue;
    sortie.push({ numero: sortie.length + 1, lecon, questions });
  }
  return sortie;
}

/** Sur combien l'épreuve est notée : un point par question, oral compris. */
export function totalDeLEpreuve(questionsEcrites: number): number {
  return questionsEcrites + POINTS_ORAL;
}

export type Mention = 'A+' | 'A' | 'B' | 'C' | 'D';

/**
 * L'appréciation en lettre.
 *
 * Deux seuils viennent des copies : 27 sur 30 et 37 sur 40 ont reçu A+,
 * 23 sur 30 a reçu A. Les seuils du dessous ne figurent sur aucune copie
 * que le père a montrée ; ils sont posés ici par quarts, et se corrigent en
 * une ligne si l'école note autrement.
 */
export function mention(points: number, total: number): Mention {
  if (total <= 0) return 'D';
  const part = points / total;
  if (part >= 0.9) return 'A+';
  if (part >= 0.75) return 'A';
  if (part >= 0.6) return 'B';
  if (part >= 0.5) return 'C';
  return 'D';
}

/** Ce que la lettre veut dire, en mots qu'un parent lit sans barème. */
export function appreciation(m: Mention): string {
  switch (m) {
    case 'A+':
      return 'Très bien acquis';
    case 'A':
      return 'Acquis';
    case 'B':
      return 'En cours d’acquisition';
    case 'C':
      return 'Tout juste la moyenne';
    default:
      return 'À reprendre';
  }
}
