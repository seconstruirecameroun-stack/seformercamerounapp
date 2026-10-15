import type { LeconResume } from './dashboard';

/**
 * Le rangement des leçons à l'intérieur d'un dossier de matière.
 *
 * Deux axes, dans cet ordre : le chapitre, puis la date.
 *
 * Le chapitre est l'intitulé du cahier — « Éducation à la paix », « Droits
 * et devoirs ». C'est sous ce mot que l'enfant a entendu la leçon en classe,
 * donc c'est sous ce mot qu'il la cherche.
 *
 * La date est celle écrite en haut de la page. Toutes les pages n'en portent
 * pas : on ne range par date que ce qui en a une, et le reste suit sans
 * mentir sur un jour qu'on ignorerait.
 */

export type GroupeLecons = {
  /** Le titre de section, ou null quand il n'y a rien à annoncer. */
  titre: string | null;
  lecons: LeconResume[];
};

/** Du plus récent au plus ancien ; les leçons sans date ferment la marche. */
function parDate(a: LeconResume, b: LeconResume) {
  if (a.date && b.date) return b.date.localeCompare(a.date);
  if (a.date) return -1;
  if (b.date) return 1;
  return 0;
}

/**
 * Regroupe les leçons d'une matière.
 *
 * Quand toutes partagent le même chapitre — le cas tant qu'une matière n'a
 * qu'un seul sujet — on ne montre aucun titre : une seule section intitulée
 * comme le dossier n'apprend rien et occupe un écran déjà petit.
 */
export function grouperParChapitre(lecons: LeconResume[]): GroupeLecons[] {
  if (lecons.length === 0) return [];

  const chapitres = new Set(lecons.map((l) => l.chapitre ?? ''));
  if (chapitres.size <= 1) return [{ titre: null, lecons: [...lecons].sort(parDate) }];

  const groupes = new Map<string, LeconResume[]>();
  for (const l of lecons) {
    const cle = l.chapitre ?? '';
    const liste = groupes.get(cle) ?? [];
    liste.push(l);
    groupes.set(cle, liste);
  }

  return [...groupes.entries()]
    .map(([cle, liste]) => ({
      titre: cle || 'Autres leçons',
      lecons: liste.sort(parDate),
    }))
    // Le chapitre le plus récent en premier : c'est celui de cette semaine.
    .sort((a, b) => parDate(a.lecons[0], b.lecons[0]));
}

/** « mar. 13 oct. » — court, lisible, sans l'année qui n'apprend rien ici. */
export function jourCourt(date: string | null): string | null {
  if (!date) return null;
  const d = new Date(date + 'T12:00:00');
  if (Number.isNaN(d.getTime())) return null;
  return new Intl.DateTimeFormat('fr-FR', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
  }).format(d);
}
