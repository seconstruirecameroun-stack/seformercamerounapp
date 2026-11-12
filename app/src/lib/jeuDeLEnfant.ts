import { DERNIERE_CLASSE_AUX_ETIQUETTES } from './saisie';

/**
 * Le jeu de chaque enfant.
 *
 * Les plus petits ont la COURSE : une voiture qui roule seule, et que leurs
 * réponses font avancer. Ils n'ont rien à jouer — leur attention reste sur la
 * question. Les grands gardent le PLATEAU de bonbons, qu'une bonne réponse
 * leur donne le droit de jouer.
 *
 * La frontière est celle des lettres mobiles : jusqu'au CE1 (et Class 3 côté
 * anglophone). Elle se lit sur le rang de la classe, comme la façon d'écrire,
 * et rien n'est à régler par enfant.
 */
export type Jeu = 'course' | 'bonbons';

export function jeuDeLaClasse(rang: number | null): Jeu {
  return rang !== null && rang <= DERNIERE_CLASSE_AUX_ETIQUETTES ? 'course' : 'bonbons';
}

/** Combien de bonnes réponses d'affilée valent un bouclier. */
export const SERIE_POUR_BOUCLIER = 3;

export type CompteursDeCourse = { turbos: number; erreurs: number; boucliers: number; serie: number };

export const COMPTEURS_VIDES: CompteursDeCourse = { turbos: 0, erreurs: 0, boucliers: 0, serie: 0 };

/**
 * Ce qu'une réponse fait à la course : un turbo si elle est juste, un choc si
 * elle est fausse, et un bouclier toutes les trois bonnes réponses d'affilée.
 */
export function apresReponse(c: CompteursDeCourse, correct: boolean): CompteursDeCourse {
  if (!correct) return { ...c, erreurs: c.erreurs + 1, serie: 0 };
  const serie = c.serie + 1;
  return {
    turbos: c.turbos + 1,
    erreurs: c.erreurs,
    serie,
    boucliers: c.boucliers + (serie % SERIE_POUR_BOUCLIER === 0 ? 1 : 0),
  };
}
