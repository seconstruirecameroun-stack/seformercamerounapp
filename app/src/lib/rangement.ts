import type { Autocollant, LeconResume, MatiereResume } from './dashboard';

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


/* ────────────────────────────────────────────────────────────────────────── */

export type GroupeMois = {
  /** « novembre 2026 », ou « Sans date » pour les pages qui n-en portent pas. */
  titre: string;
  /** « 2026-11 », ou la chaîne vide : sert de clé React et de tri. */
  cle: string;
  lecons: LeconResume[];
};

/**
 * Les leçons rangées par mois, toutes matières confondues.
 *
 * C-est la seconde façon de chercher une leçon, et elle répond à une autre
 * question que le dossier de matière. « Où est la leçon sur le vent ? » se
 * cherche par matière. « Qu-est-ce qu-on a fait la semaine du 19 ? » se
 * cherche par date — et c-est cette question-là qu-on se pose la veille
 * d-un contrôle.
 *
 * Les leçons sans date ferment la marche plutôt que d-être rangées sous un
 * mois inventé. Toutes les pages de cahier ne portent pas de jour.
 */
export function grouperParMois(lecons: LeconResume[]): GroupeMois[] {
  const groupes = new Map<string, LeconResume[]>();
  for (const l of lecons) {
    const cle = l.date ? l.date.slice(0, 7) : '';
    const liste = groupes.get(cle) ?? [];
    liste.push(l);
    groupes.set(cle, liste);
  }

  return [...groupes.entries()]
    .map(([cle, liste]) => ({
      cle,
      titre: cle ? nomDuMois(cle) : 'Sans date',
      lecons: liste.sort(parDate),
    }))
    // Du mois le plus récent au plus ancien ; les sans-date tout à la fin.
    .sort((a, b) => {
      if (!a.cle) return 1;
      if (!b.cle) return -1;
      return b.cle.localeCompare(a.cle);
    });
}

/** « 2026-11 » devient « Novembre 2026 ». */
function nomDuMois(cle: string): string {
  const d = new Date(cle + '-01T12:00:00');
  if (Number.isNaN(d.getTime())) return cle;
  const nom = new Intl.DateTimeFormat('fr-FR', { month: 'long', year: 'numeric' }).format(d);
  return nom.charAt(0).toUpperCase() + nom.slice(1);
}

export type Album = {
  matiereId: string | null;
  titre: string;
  couleur: string | null;
  total: number;
  gagnes: number;
  images: Autocollant[];
};

/**
 * La collection rangée en albums, un par matière.
 *
 * Elle était une seule grille. À deux cents images — c-est le compte réel
 * de BRAYNE — elle faisait trente rangées qu-aucun enfant ne parcourt, et
 * on n-y voyait ni ce qu-on avait presque fini, ni où aller chercher ce qui
 * manque.
 *
 * Un album par matière répond aux deux : la barre dit où on en est, et le
 * titre dit dans quel dossier aller jouer pour la remplir. C-est aussi la
 * forme que les enfants connaissent déjà des albums d-images.
 *
 * L-ordre des images à l-intérieur d-un album est celui où elles ont été
 * poussées, c-est-à-dire leçon par leçon : elles suivent l-ordre où
 * l-enfant les a apprises, et non un ordre alphabétique qui ne dirait rien.
 */
export function grouperEnAlbums(
  autocollants: Autocollant[],
  matieres: MatiereResume[],
): Album[] {
  const avec = autocollants.filter((a) => a.illustration);
  if (avec.length === 0) return [];

  const groupes = new Map<string, Autocollant[]>();
  for (const a of avec) {
    const cle = a.matiereId ?? '';
    const liste = groupes.get(cle) ?? [];
    liste.push(a);
    groupes.set(cle, liste);
  }

  const rang = new Map(matieres.map((m, i) => [m.id, i]));
  return [...groupes.entries()]
    .map(([cle, images]) => {
      const matiere = matieres.find((m) => m.id === cle);
      return {
        matiereId: cle || null,
        titre: matiere?.label ?? 'Autres images',
        couleur: matiere?.couleur ?? null,
        total: images.length,
        gagnes: images.filter((a) => a.acquis).length,
        images,
      };
    })
    // Le même ordre que les dossiers de matières, pour qu-un enfant retrouve
    // son album là où il a l-habitude de voir sa matière. Les images sans
    // matière, s-il y en a, ferment la marche.
    .sort((a, b) => (rang.get(a.matiereId ?? '') ?? 99) - (rang.get(b.matiereId ?? '') ?? 99));
}
