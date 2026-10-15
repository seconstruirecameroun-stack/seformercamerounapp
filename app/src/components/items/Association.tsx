import { useState } from 'react';
import { Enonce } from './partage';
import type { Props } from './partage';

/**
 * Relier deux colonnes.
 *
 * Le type que ces leçons réclamaient le plus : elles sont faites de listes —
 * quatre sols et leurs couleurs, trois époques et leurs outils, des
 * inventions et leurs inventeurs. Un QCM les découpe en questions séparées
 * et perd justement ce qui compte, le lien.
 *
 * On relie par deux touchers successifs, jamais par glisser-déposer : sur un
 * téléphone partagé, un doigt qui traîne sur l'écran fait défiler la page.
 */
export default function Association({ item, onRepondre, verrouille, visuel }: Props) {
  const payload = item.payload as { question: string; gauche: string[]; droite: string[] };
  /** ordre[i] = index dans `droite` de ce qui va avec gauche[i]. */
  const ordre = (item.answer as { order: number[] }).order;

  const [actif, setActif] = useState<number | null>(null);
  /** paires[i] = index choisi dans `droite` pour gauche[i]. */
  const [paires, setPaires] = useState<Array<number | null>>(() => payload.gauche.map(() => null));

  const prises = new Set(paires.filter((p): p is number => p !== null));

  function relier(droiteIndex: number) {
    if (actif === null || verrouille) return;
    const suite = [...paires];
    // Un même élément de droite ne sert qu'une fois : on libère son ancien lien.
    for (let i = 0; i < suite.length; i++) if (suite[i] === droiteIndex) suite[i] = null;
    suite[actif] = droiteIndex;
    setPaires(suite);
    setActif(null);

    if (suite.every((p) => p !== null)) {
      const correct = suite.every((p, i) => p === ordre[i]);
      onRepondre({ correct, donnee: { order: suite } });
    }
  }

  return (
    <>
      <Enonce visuel={visuel}>{payload.question}</Enonce>
      <p className="mt-1 text-kid-sm text-muted">
        Touche à gauche, puis touche ce qui va avec.
      </p>

      <div className="mt-5 grid grid-cols-2 gap-3">
        <div className="grid content-start gap-2">
          {payload.gauche.map((texte, i) => {
            const lie = paires[i] !== null;
            const juste = verrouille && paires[i] === ordre[i];
            const faux = verrouille && paires[i] !== ordre[i];
            return (
              <button
                key={i}
                type="button"
                disabled={verrouille}
                onClick={() => setActif(actif === i ? null : i)}
                className={
                  'tuile min-h-[60px] rounded-[var(--radius-tile)] border-2 px-3 py-2 text-left text-kid-sm font-bold shadow-[var(--shadow-tile)] ' +
                  (juste
                    ? 'border-leaf bg-leaf/15'
                    : faux
                      ? 'border-clay bg-clay/12'
                      : actif === i
                        ? 'border-ink bg-sand'
                        : lie
                          ? 'border-line bg-sand/60'
                          : 'border-line bg-white-warm')
                }
              >
                {texte}
                {paires[i] !== null ? (
                  <span className="mt-1 block text-kid-xs font-semibold text-muted">
                    → {payload.droite[paires[i]!]}
                  </span>
                ) : null}
              </button>
            );
          })}
        </div>

        <div className="grid content-start gap-2">
          {payload.droite.map((texte, j) => (
            <button
              key={j}
              type="button"
              disabled={verrouille || actif === null}
              onClick={() => relier(j)}
              className={
                'tuile min-h-[60px] rounded-[var(--radius-tile)] border-2 px-3 py-2 text-left text-kid-sm font-bold shadow-[var(--shadow-tile)] ' +
                (prises.has(j)
                  ? 'border-line bg-sand/60 opacity-60'
                  : actif === null
                    ? 'border-line bg-white-warm opacity-70'
                    : 'border-line bg-white-warm hover:border-ink-2')
              }
            >
              {texte}
            </button>
          ))}
        </div>
      </div>

      {verrouille ? (
        <ul className="mt-4 grid gap-1 text-kid-sm text-ink-2">
          {payload.gauche.map((texte, i) => (
            <li key={i}>
              <strong>{texte}</strong> → {payload.droite[ordre[i]]}
            </li>
          ))}
        </ul>
      ) : paires.some((p) => p !== null) ? (
        <button
          type="button"
          className="mt-3 text-kid-sm font-bold text-clay underline"
          onClick={() => {
            setPaires(payload.gauche.map(() => null));
            setActif(null);
          }}
        >
          Recommencer
        </button>
      ) : null}
    </>
  );
}
