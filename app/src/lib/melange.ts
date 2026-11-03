import { useState } from 'react';

/**
 * L'ordre dans lequel les choix sont montrés.
 *
 * Il a fallu l'écrire après un constat net : sur les **277 QCM** de la base,
 * la bonne réponse était en position 1. Les 277. Et ce n'était pas propre à
 * ce type — les associations rangeaient la colonne de droite exactement en
 * face de la gauche, et les chronologies affichaient les étiquettes déjà
 * dans l'ordre. Trois types d'exercices sur quatre se résolvaient sans rien
 * lire : toucher la première tuile, relier ligne à ligne, prendre les
 * étiquettes de haut en bas.
 *
 * Un enfant n'a pas besoin de le formuler pour en prendre l'habitude. Il
 * suffit que ça marche. Et la manche de validation, qui exige un sans-faute,
 * devenait alors un sans-faute sur rien.
 *
 * On corrige **à l'affichage** et non dans les données, pour deux raisons.
 * La première est que mélanger une fois en base laisserait une position
 * fixe par question : l'enfant qui la revoit s'en souviendrait. Ici l'ordre
 * est retiré à chaque fois que la question revient. La seconde est que les
 * scripts qui écrivent les leçons n'ont plus à y penser — ils rangent la
 * bonne réponse en premier si ça les arrange, c'est devenu sans effet.
 *
 * Ce qui est **enregistré** reste l'index d'origine. L'ordre affiché ne
 * sort pas du composant : le journal des tentatives et le rapport aux
 * parents continuent de parler de la même réponse d'une séance à l'autre.
 */

/** Une permutation de [0, n[ : `ordre[place affichée] = index d'origine`. */
export function melanger(n: number): number[] {
  const ordre = Array.from({ length: n }, (_, i) => i);
  // Fisher-Yates. Le tirage est uniforme, donc la bonne réponse tombe aussi
  // souvent en première place qu'ailleurs — y compris, parfois, dans l'ordre
  // d'origine. C'est voulu : « jamais celle du dessus » serait une habitude
  // de plus, simplement inversée.
  for (let i = n - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [ordre[i], ordre[j]] = [ordre[j], ordre[i]];
  }
  return ordre;
}

/**
 * Le mélange d'une question, tiré une fois pour toute sa durée.
 *
 * `useState` et non `useMemo` : React peut recalculer un mémo quand il veut,
 * et les tuiles se mettraient à sauter sous le doigt de l'enfant au milieu
 * de la question. Chaque question monte son propre lecteur — c'est la clé
 * posée sur `ItemPlayer` qui le garantit — donc un tirage au montage vaut
 * un tirage par question.
 *
 * Le tirage est refait quand `n` change. Cette ligne n'est pas une
 * précaution de style : pendant une version, le lecteur n'avait pas de clé
 * et gardait son mélange d'une question à la suivante. Une association à
 * trois paires qui suivait une question à deux n'affichait que deux
 * étiquettes, la troisième réponse n'existait nulle part à l'écran, et la
 * question se concluait toute seule — comptée fausse. Rendre un tableau
 * trop court sans rien dire est une arête : elle est ôtée ici, et la clé
 * reste la vraie correction.
 */
export function useMelange(n: number): number[] {
  const [etat, setEtat] = useState(() => ({ n, ordre: melanger(n) }));
  if (etat.n !== n) {
    const suivant = { n, ordre: melanger(n) };
    setEtat(suivant);
    return suivant.ordre;
  }
  return etat.ordre;
}
