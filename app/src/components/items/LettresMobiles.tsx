import { useMemo, useState } from 'react';

/**
 * Les lettres mobiles : le mot en désordre, à remettre dans l'ordre.
 *
 * C'est l'exercice que la maîtresse fait avec des étiquettes de carton, et
 * il est ici pour une raison précise. KLEIN a écrit « Sabloneux » — un seul
 * n — sur une leçon de sciences qui portait sur la nature du sol, pas sur
 * l'orthographe. On lui comptait zéro pour une faute qui n'était pas la
 * leçon, et il a fini par taper « Hallo » puis par arrêter de jouer.
 *
 * Le tiroir contient **exactement** les lettres du mot, ni plus ni moins.
 * Aucun leurre, et c'est un choix :
 *
 *   Le tiroir porte l'orthographe. « sablonneux » met deux n sur la table ;
 *   l'enfant qui n'en place qu'un se retrouve avec une étiquette dans la
 *   main. Il voit sa faute au lieu de la subir — c'est exactement celle
 *   qu'il faisait.
 *
 *   Des leurres transformeraient l'exercice. Il faudrait alors deviner
 *   quelles lettres n'appartiennent pas au mot, ce qui est un autre jeu que
 *   de savoir l'écrire.
 *
 * Le désordre est tiré une fois par question et ne rebat pas les cartes à
 * chaque geste : des lettres qui sautent sous le doigt rendraient l'exercice
 * impraticable.
 */

/** Une permutation stable, tirée du texte lui-même plutôt que du hasard. */
function melanger(mot: string, graine: string): number[] {
  const indices = [...mot].map((_, i) => i);
  let h = 2166136261;
  for (const c of graine + mot) {
    h ^= c.charCodeAt(0);
    h = Math.imul(h, 16777619) >>> 0;
  }
  for (let i = indices.length - 1; i > 0; i--) {
    h = (Math.imul(h, 48271) + 11) >>> 0;
    const j = h % (i + 1);
    [indices[i], indices[j]] = [indices[j], indices[i]];
  }
  // Un tirage qui rendrait le mot déjà écrit n'est pas un exercice.
  const identique = indices.every((v, i) => mot[v] === mot[i]);
  if (identique && indices.length > 1) [indices[0], indices[1]] = [indices[1], indices[0]];
  return indices;
}

/** Une étiquette : lettre lisible, et l'espace rendu visible. */
function etiquette(c: string) {
  return c === ' ' ? '␣' : c;
}

export default function LettresMobiles({
  attendu,
  graine,
  onChange,
  verrouille = false,
}: {
  /** Le mot à reconstituer : il donne le contenu du tiroir. */
  attendu: string;
  /** De quoi tirer un désordre stable — l'identifiant de la question. */
  graine: string;
  onChange: (v: string) => void;
  verrouille?: boolean;
}) {
  const lettres = useMemo(() => [...attendu], [attendu]);
  const ordre = useMemo(() => melanger(attendu, graine), [attendu, graine]);
  /** Les positions du tiroir déjà posées, dans l'ordre où l'enfant les a prises. */
  const [posees, setPosees] = useState<number[]>([]);

  function ecrire(suite: number[]) {
    setPosees(suite);
    onChange(suite.map((i) => lettres[ordre[i]]).join(''));
  }

  const restantes = ordre.map((_, i) => i).filter((i) => !posees.includes(i));

  return (
    <div className="mt-5">
      {/* Ce qu'il a écrit : une case par lettre, pour qu'on voie d'un coup
          combien il en reste. Toucher une lettre posée la renvoie au tiroir. */}
      <div className="flex flex-wrap justify-center gap-1.5 rounded-[var(--radius-tile)] border-2 border-dashed border-line bg-sand/40 p-3">
        {lettres.map((_, rang) => {
          const i = posees[rang];
          const pleine = i !== undefined;
          return (
            <button
              key={rang}
              type="button"
              disabled={verrouille || !pleine}
              onPointerDown={(e) => e.preventDefault()}
              onClick={() => ecrire(posees.filter((_, r) => r !== rang))}
              aria-label={pleine ? `Retirer ${etiquette(lettres[ordre[i]])}` : 'Case vide'}
              className={
                'grid h-12 w-10 place-items-center rounded-xl border-2 text-kid-lg font-black ' +
                (pleine
                  ? 'border-clay/60 bg-white-warm text-ink shadow-[var(--shadow-tile)]'
                  : 'border-line/70 bg-transparent text-transparent')
              }
            >
              {pleine ? etiquette(lettres[ordre[i]]) : '·'}
            </button>
          );
        })}
      </div>

      {!verrouille ? (
        <>
          <p className="mt-3 text-center text-kid-sm text-muted">
            {restantes.length > 0
              ? `Encore ${restantes.length} ${restantes.length > 1 ? 'lettres' : 'lettre'} à placer`
              : 'Toutes les lettres sont placées'}
          </p>
          <div className="mt-2 flex flex-wrap justify-center gap-2">
            {ordre.map((_, i) =>
              posees.includes(i) ? null : (
                <button
                  key={i}
                  type="button"
                  onPointerDown={(e) => e.preventDefault()}
                  onClick={() => ecrire([...posees, i])}
                  aria-label={etiquette(lettres[ordre[i]])}
                  className="tuile grid h-14 w-12 place-items-center rounded-xl border-2 border-line bg-white-warm text-kid-lg font-black text-ink shadow-[var(--shadow-tile)] active:bg-sand"
                >
                  {etiquette(lettres[ordre[i]])}
                </button>
              ),
            )}
          </div>
          {posees.length > 0 ? (
            <button
              type="button"
              className="mx-auto mt-3 block text-kid-sm font-bold text-clay underline"
              onClick={() => ecrire([])}
            >
              Tout remettre
            </button>
          ) : null}
        </>
      ) : null}
    </div>
  );
}
