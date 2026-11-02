import { useEffect, useRef, useState } from 'react';

/** L’apostrophe typographique : celle qu’attendent les corrections. */
const APOS = '’';

/**
 * Le clavier de l'application.
 *
 * Il existe pour une raison qu'on ne peut pas obtenir autrement : **empêcher
 * le téléphone de souffler la réponse**. Depuis une page web, on ne peut pas
 * supprimer de façon fiable la barre de suggestions d'Android — autocomplete,
 * autocorrect et spellcheck sont inégalement respectés d'un clavier à
 * l'autre. Le seul moyen sûr est d'empêcher le clavier système de s'ouvrir
 * (`inputMode="none"`) et de dessiner le nôtre.
 *
 * Ce que cela règle, et qui n'est pas accessoire :
 *
 *   Plus aucune suggestion. Une dictée où le téléphone propose « sablonneux »
 *   au bout de trois lettres ne mesure plus rien.
 *
 *   Plus aucune correction automatique. Elle réparait silencieusement les
 *   fautes — ou en inventait d'autres — et l'enfant ne savait pas laquelle
 *   des deux orthographes était la sienne.
 *
 *   Les lettres accentuées deviennent atteignables. Sur un téléphone, é è ê à
 *   ç sont cachés derrière un appui long : c'est pour cela que la correction
 *   les pardonne aujourd'hui. Avec ce clavier, on pourra cesser de les
 *   pardonner là où ils comptent.
 *
 *   Des touches à la taille d'un doigt de sept ans.
 *
 * L'ordre est **alphabétique**, pas AZERTY. Un enfant de CE1 connaît son
 * alphabet et ne connaît pas la disposition d'un clavier ; la chercher
 * ajouterait à l'exercice une difficulté qui n'est pas celle qu'on enseigne.
 * C'est discutable pour un CM1 qui a des cours de TIC — mais ici on teste ce
 * qu'il a retenu, pas sa dactylographie.
 */

const LIGNES = ['abcdefg', 'hijklmn', 'opqrstu', 'vwxyz'];

/**
 * La première rangée : les accents, et l'apostrophe.
 *
 * L'apostrophe est ici et non derrière la bascule, parce qu'elle n'est pas
 * une ponctuation pour un enfant : elle est dans le mot. « l’eau »,
 * « s’élargit », « l’âge de la pierre taillée » — derrière la bascule, il
 * faudrait changer de page au milieu de chaque mot.
 */
const ACCENTS = ['é', 'è', 'ê', 'à', 'ç', 'ù', APOS];

/**
 * La seconde page, et pourquoi elle existe.
 *
 * On a relevé ce que les exercices réclament réellement, en lisant les
 * énoncés en base : les dictées contiennent des chiffres (« Gutenberg invente
 * l’imprimerie en 1450 »), des virgules et un « œ » ; les textes à trous
 * attendent « sous-multiples » et « 200 ». Sans ces touches, l'enfant ne
 * pouvait pas répondre du tout — un défaut bien pire que les suggestions du
 * téléphone.
 *
 * Elles vivent sur une seconde page plutôt que toutes affichées : trente-six
 * touches tiennent sur un téléphone, soixante non. Et elles sont TOUTES
 * montrées, jamais choisies d'après la réponse attendue — un clavier qui
 * ferait apparaître un trait d'union seulement quand la réponse en contient
 * un soufflerait la réponse, exactement ce qu'on cherche à empêcher.
 */
const CHIFFRES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];
const SIGNES = ['-', ',', '.', 'œ', 'â', 'î', 'ô', 'ë', 'ï', 'ü'];

export type ClavierProps = {
  /** La valeur en cours d'édition. */
  valeur: string;
  onChange: (v: string) => void;
  /** Affiche la touche espace : inutile pour un mot, nécessaire pour une phrase. */
  espace?: boolean;
  /** Affiche la rangée des accents. */
  accents?: boolean;
  /** Le bouton de validation, posé dans le clavier plutôt qu'en dessous. */
  onValider?: () => void;
  validerActif?: boolean;
  libelleValider?: string;
};

function Touche({
  children,
  onPress,
  large = 1,
  ton = 'lettre',
  desactive = false,
  etiquette,
}: {
  children: React.ReactNode;
  onPress: () => void;
  large?: number;
  ton?: 'lettre' | 'gomme' | 'valider';
  desactive?: boolean;
  etiquette?: string;
}) {
  return (
    <button
      type="button"
      aria-label={etiquette}
      disabled={desactive}
      // Le doigt ne doit pas retirer le focus du champ : sans cela, le curseur
      // saute et l'enfant perd le fil de ce qu'il écrit.
      onPointerDown={(e) => e.preventDefault()}
      onClick={onPress}
      style={{ flexGrow: large, flexBasis: `${large * 11}%` }}
      className={
        'tuile h-14 min-w-0 rounded-xl border-2 text-kid font-black shadow-[var(--shadow-tile)] ' +
        'select-none disabled:opacity-40 ' +
        (ton === 'valider'
          ? 'border-leaf bg-leaf text-white-warm'
          : ton === 'gomme'
            ? 'border-clay/60 bg-clay/15 text-clay-dark'
            : 'border-line bg-white-warm text-ink active:bg-sand')
      }
    >
      {children}
    </button>
  );
}

export default function Clavier({
  valeur,
  onChange,
  espace = false,
  accents = false,
  onValider,
  validerActif = true,
  libelleValider = 'Vérifier',
}: ClavierProps) {
  const [majuscule, setMajuscule] = useState(false);
  const [signes, setSignes] = useState(false);

  const taper = (lettre: string) => {
    onChange(valeur + (majuscule ? lettre.toUpperCase() : lettre));
    setMajuscule(false);
  };

  const maj = (
    <Touche
      onPress={() => setMajuscule((m) => !m)}
      large={1.4}
      ton={majuscule ? 'valider' : 'lettre'}
      etiquette="Majuscule"
    >
      ⇧
    </Touche>
  );

  const gomme = (
    <Touche
      onPress={() => onChange(valeur.slice(0, -1))}
      large={1.4}
      ton="gomme"
      desactive={valeur.length === 0}
      etiquette="Effacer la dernière lettre"
    >
      ⌫
    </Touche>
  );

  const bas = (
    <div className="flex gap-1 sm:gap-1.5">
      <Touche
        onPress={() => setSignes((s) => !s)}
        large={1.6}
        etiquette={signes ? 'Revenir aux lettres' : 'Chiffres et signes'}
      >
        {signes ? 'abc' : '123'}
      </Touche>
      {espace ? (
        <Touche onPress={() => taper(' ')} large={3} etiquette="Espace">
          espace
        </Touche>
      ) : null}
      {onValider ? (
        <Touche
          onPress={onValider}
          large={espace ? 2.8 : 5.4}
          ton="valider"
          desactive={!validerActif}
        >
          {libelleValider}
        </Touche>
      ) : null}
    </div>
  );

  const cadre = 'mt-4 grid gap-1 rounded-[var(--radius-card)] border border-line bg-paper p-2 sm:gap-1.5 sm:p-3';

  if (signes) {
    return (
      <div className={cadre}>
        <div className="flex gap-1 sm:gap-1.5">
          {CHIFFRES.map((c) => (
            <Touche key={c} onPress={() => taper(c)} etiquette={c}>
              {c}
            </Touche>
          ))}
        </div>
        <div className="flex gap-1 sm:gap-1.5">
          {SIGNES.map((c) => (
            <Touche key={c} onPress={() => taper(c)} etiquette={c}>
              {majuscule ? c.toUpperCase() : c}
            </Touche>
          ))}
        </div>
        <div className="flex gap-1 sm:gap-1.5">
          {maj}
          <span className="grow" />
          {gomme}
        </div>
        {bas}
      </div>
    );
  }

  return (
    <div className={cadre}>
      {accents ? (
        <div className="flex gap-1 sm:gap-1.5">
          {ACCENTS.map((a) => (
            <Touche key={a} onPress={() => taper(a)} etiquette={a}>
              {majuscule ? a.toUpperCase() : a}
            </Touche>
          ))}
        </div>
      ) : null}

      {LIGNES.map((ligne, i) => (
        <div key={ligne} className="flex gap-1 sm:gap-1.5">
          {i === LIGNES.length - 1 ? maj : null}
          {[...ligne].map((l) => (
            <Touche key={l} onPress={() => taper(l)} etiquette={l}>
              {majuscule ? l.toUpperCase() : l}
            </Touche>
          ))}
          {i === LIGNES.length - 1 ? gomme : null}
        </div>
      ))}

      {bas}
    </div>
  );
}

/**
 * Les attributs à poser sur tout champ que ce clavier alimente.
 *
 * `inputMode="none"` est celui qui compte : il garde le champ focusable, avec
 * son curseur, mais empêche le clavier du système de s'ouvrir. Les trois
 * autres ne coûtent rien et servent là où ils sont respectés.
 */
export const SANS_AIDE = {
  inputMode: 'none' as const,
  autoComplete: 'off',
  autoCorrect: 'off',
  autoCapitalize: 'off',
  spellCheck: false,
};

/**
 * Le champ actif, quand plusieurs se partagent le même clavier.
 *
 * Un texte à trous en a deux : le clavier doit écrire dans celui que l'enfant
 * vient de toucher, et dans aucun autre.
 */
export function useChampActif(nombre: number) {
  const [actif, setActif] = useState(0);
  const refs = useRef<Array<HTMLInputElement | null>>([]);

  useEffect(() => {
    if (actif >= nombre) setActif(0);
  }, [actif, nombre]);

  return {
    actif,
    setActif,
    refs,
    /** À étaler sur chaque champ : il devient actif dès qu'on le touche. */
    liens: (i: number) => ({
      ref: (el: HTMLInputElement | null) => {
        refs.current[i] = el;
      },
      onFocus: () => setActif(i),
      onClick: () => setActif(i),
      ...SANS_AIDE,
    }),
  };
}
