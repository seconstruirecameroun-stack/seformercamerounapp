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
  /**
   * La place de la classe dans l’école, de 1 (SIL) à 6 (CM2).
   *
   * Elle décide de la façon d’écrire une réponse : étiquettes aux petites
   * classes, clavier ensuite. La règle vit dans lib/saisie.ts.
   */
  rang?: number | null;
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

/**
 * La même lettre, à la casse près — et aux accents près seulement si on le
 * demande. Au Défi, « eleve » contre « élève » doit montrer DEUX fautes :
 * sans cela l'écart ne trouve aucune divergence et l'enfant voit une réponse
 * refusée sans rien qui la distingue de ce qu'il a écrit.
 */
function memeLettre(a: string, b: string, accentsComptent = false) {
  const net = (c: string) =>
    accentsComptent
      ? c.toLowerCase()
      : c.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  return net(a) === net(b);
}

export type Ecart = {
  /** Le début commun aux deux mots. */
  debut: string;
  /** Ce que l'enfant a écrit de trop ou de travers, au milieu. */
  ecrit: string;
  /** Ce qu'il aurait fallu écrire à la place. */
  attendu: string;
  /** La fin commune aux deux mots. */
  fin: string;
};

/**
 * Où exactement le mot diverge.
 *
 * On pèle le début puis la fin communs, et ce qui reste au milieu est la
 * faute. Pour « sabloneux » contre « sablonneux » : début « sablon », fin
 * « eux », et au milieu rien d'écrit contre un « n » attendu. L'enfant lit
 * alors « il manque un n » au lieu de « Réponse : sablonneux », qui ne lui
 * dit pas ce qu'il a raté.
 */
export function ecartMot(ecrit: string, attendu: string, accentsComptent = false): Ecart {
  const a = ecrit.trim();
  const b = attendu.trim();
  let debut = 0;
  while (
    debut < a.length &&
    debut < b.length &&
    memeLettre(a[debut], b[debut], accentsComptent)
  ) {
    debut += 1;
  }
  let fin = 0;
  while (
    fin < a.length - debut &&
    fin < b.length - debut &&
    memeLettre(a[a.length - 1 - fin], b[b.length - 1 - fin], accentsComptent)
  ) {
    fin += 1;
  }
  return {
    debut: b.slice(0, debut),
    ecrit: a.slice(debut, a.length - fin),
    attendu: b.slice(debut, b.length - fin),
    fin: fin > 0 ? b.slice(b.length - fin) : '',
  };
}

/**
 * Comparaison d'un mot : la casse et les espaces ne comptent jamais, les
 * accents comptent si on le demande.
 *
 * Ils ne comptaient nulle part, et pour une bonne raison : sur un téléphone,
 * é è ê à ç sont cachés derrière un appui long. Punir un accent qu'on ne
 * peut pas atteindre, c'est noter le clavier et non l'enfant. Le clavier de
 * l'app les met en première rangée, donc l'excuse est tombée — mais
 * seulement au Défi, la dernière étape, celle qu'on n'atteint qu'en ayant
 * déjà franchi les trois autres sur cette notion.
 *
 * L'apostrophe, elle, est toujours normalisée : droite ou typographique,
 * c'est la même apostrophe. Ce n'est pas ce qu'on enseigne, et l'enfant n'a
 * aucun moyen de savoir laquelle des deux la base attend.
 */
export function memeMot(a: string, b: string, accentsComptent = false) {
  const net = (s: string) => {
    const brut = s.trim().toLowerCase().replace(/['‘’ʼ]/g, '’').replace(/\s+/g, ' ');
    return accentsComptent
      ? brut.normalize('NFC')
      : brut.normalize('NFD').replace(/[̀-ͯ]/g, '');
  };
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
