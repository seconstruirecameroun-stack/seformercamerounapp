/**
 * Comment l'enfant écrit sa réponse, selon sa classe et l'étape.
 *
 * L'escalier vient d'un constat, pas d'une intuition. KLEIN, CE1, a répondu
 * « Sabloneux » pour « sablonneux » — un seul n manquant — puis « Stuture »
 * pour « structure », puis a tapé « J », « F », « Hallo », et a cessé de
 * jouer. Il connaissait les mots. C'est de les écrire qui l'a mis dehors.
 *
 * Or la leçon portait sur la nature du sol, pas sur l'orthographe de
 * « sablonneux ». On mesurait autre chose que ce qu'on enseignait.
 *
 *   lettres-mobiles  les lettres du mot, en désordre, à remettre dans
 *                    l'ordre. C'est l'exercice que la maîtresse fait avec
 *                    des étiquettes. Il teste le mot ET son orthographe, et
 *                    il retire la seule chose qui n'est pas la leçon :
 *                    savoir taper.
 *
 *   clavier          la frappe libre, sur le clavier de l'application.
 *
 * Ce n'est pas une facilité, c'est une marche. Les lettres mobiles ne
 * pardonnent rien : le tiroir contient deux n, et il faut les placer tous
 * les deux. Un enfant qui écrit « Sabloneux » au clavier passe à côté sans
 * le voir ; avec les étiquettes, il lui reste un n sur les bras.
 */

import type { ClassRow } from '../types/db';

export type ModeSaisie = 'lettres-mobiles' | 'clavier';

/**
 * Jusqu'à cette place dans l'école, l'étape « Maîtrise » se joue aux lettres
 * mobiles : SIL, CP et CE1 côté francophone, Class 1 à 3 côté anglophone.
 * `rank` sert de clé plutôt que le libellé, pour que les deux sous-systèmes
 * suivent la même règle sans la réécrire.
 */
export const DERNIERE_CLASSE_AUX_ETIQUETTES = 3;

/** L'étape où l'on produit la réponse au lieu de la reconnaître. */
export const ETAPE_PRODUCTION = 3;

export function modeSaisie(rang: number | null, niveau: number): ModeSaisie {
  if (rang === null) return 'clavier';
  // Au Défi, tout le monde tape : la vitesse et la frappe font partie de
  // l'épreuve, et l'enfant a déjà franchi la Maîtrise sur cette notion.
  if (niveau !== ETAPE_PRODUCTION) return 'clavier';
  return rang <= DERNIERE_CLASSE_AUX_ETIQUETTES ? 'lettres-mobiles' : 'clavier';
}

type ClasseJointe = Pick<ClassRow, 'rank'>;

/**
 * Le rang de la classe d'un enfant, quand on le connaît.
 *
 * La jointure accepte les deux formes : PostgREST renvoie un objet pour une
 * relation vers un seul parent, là où les types générés annoncent un
 * tableau. Trancher ici évite de répéter le doute à chaque appel.
 */
export function rangDeLaClasse(
  classe: ClasseJointe | ClasseJointe[] | null | undefined,
): number | null {
  const un = Array.isArray(classe) ? classe[0] : classe;
  return un && typeof un.rank === 'number' ? un.rank : null;
}
