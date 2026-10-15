import type { ItemRow } from '../../types/db';

/**
 * Ce que tous les types de questions partagent.
 *
 * Chaque type vit dans son propre fichier — ils n'ont rien en commun sauf
 * ceci : la forme de la réponse, l'énoncé, et la façon de comparer deux
 * mots. Le reste diffère assez pour que les mélanger rende chaque type
 * moins lisible.
 */

export type Reponse = { correct: boolean; donnee: unknown };

export type Props = {
  item: ItemRow;
  onRepondre: (r: Reponse) => void;
  verrouille: boolean;
  /** Vignette de la notion, posée contre l'énoncé et non contre l'exercice :
      les réponses gardent ainsi toute la largeur, ce qui compte sur un
      téléphone où une option sur deux lignes devient pénible à viser. */
  visuel?: React.ReactNode;
};

export const LETTRES = ['A', 'B', 'C', 'D', 'E'];

export function Enonce({
  visuel,
  children,
}: {
  visuel?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="flex items-start gap-3">
      {visuel}
      <h2 className="flex-1 text-kid-xl leading-snug font-extrabold text-balance">{children}</h2>
    </div>
  );
}

/** Comparaison indulgente : la casse, les accents et les espaces ne comptent pas. */
export function memeMot(a: string, b: string) {
  const net = (s: string) =>
    s
      .trim()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .replace(/\s+/g, ' ');
  return net(a) === net(b);
}

/**
 * Comparaison d'une phrase dictée.
 *
 * Contrairement à `memeMot`, les accents comptent : une dictée sert
 * précisément à les apprendre. On pardonne en revanche la casse, les espaces
 * en trop et le point final, qui ne sont pas l'objet de l'exercice.
 */
export function memePhrase(a: string, b: string) {
  const net = (s: string) =>
    s
      .trim()
      .toLowerCase()
      .replace(/\s+/g, ' ')
      // L'espace avant le point d'exclamation est la règle en français : on
      // la retire avec la ponctuation, sinon « rouge ! » serait refusé.
      .replace(/\s*[.!?]+$/, '')
      .replace(/[’']/g, '’')
      .trim();
  return net(a) === net(b);
}
