import { useState } from 'react';
import Illustration from '../Illustration';
import { useMelange } from '../../lib/melange';
import { Enonce } from './partage';
import type { Props } from './partage';

/**
 * Annoter un schéma : poser un nom en face de chaque numéro du dessin.
 *
 * Le dessin est montré EN GRAND, et non en vignette contre l'énoncé comme
 * pour les autres types. C'est lui l'exercice : une vignette de 56 pixels
 * ne laisse pas lire un numéro, et l'enfant répondrait de mémoire au lieu
 * de regarder, ce qui est exactement ce qu'on veut lui faire faire.
 *
 * Les numéros sont dessinés dans la figure, jamais posés par-dessus : voir
 * lib/annotation.ts pour la raison.
 *
 * On relie par deux touchers successifs, comme pour l'association, et pour
 * la même raison : sur un téléphone partagé, un doigt qui traîne sur l'écran
 * fait défiler la page.
 */
export default function Annotation({ item, onRepondre, verrouille }: Props) {
  const payload = item.payload as { question: string; figure: string; etiquettes: string[] };
  /** ordre[k] = index dans `etiquettes` du nom qui va au repère k + 1. */
  const ordre = (item.answer as { ordre: number[] }).ordre;
  // Les étiquettes sont mélangées : rangées dans l'ordre des numéros, elles
  // donneraient la réponse sans regarder le dessin.
  const vue = useMelange(payload.etiquettes.length);

  const [actif, setActif] = useState<number | null>(null);
  /** poses[k] = index choisi dans `etiquettes` pour le repère k + 1. */
  const [poses, setPoses] = useState<Array<number | null>>(() =>
    payload.etiquettes.map(() => null),
  );

  const prises = new Set(poses.filter((p): p is number => p !== null));

  function poser(etiquette: number) {
    if (actif === null || verrouille) return;
    const suite = [...poses];
    // Une même étiquette ne sert qu'une fois : on libère son ancienne place.
    for (let i = 0; i < suite.length; i++) if (suite[i] === etiquette) suite[i] = null;
    suite[actif] = etiquette;
    setPoses(suite);
    setActif(null);

    if (suite.every((p) => p !== null)) {
      const correct = suite.every((p, i) => p === ordre[i]);
      onRepondre({ correct, donnee: { ordre: suite } });
    }
  }

  return (
    <>
      <Enonce>{payload.question}</Enonce>

      <div className="mt-3 overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm">
        <Illustration
          cle={payload.figure}
          forme="objet"
          alt="Le schéma à annoter, avec ses numéros."
          priorite
          className="mx-auto block h-auto w-full max-w-[320px]"
        />
      </div>

      <p className="mt-2 text-kid-sm text-muted">Touche un numéro, puis touche son nom.</p>

      <div className="mt-3 grid grid-cols-2 gap-3">
        <div className="grid content-start gap-2">
          {poses.map((pose, k) => {
            const juste = verrouille && pose === ordre[k];
            const faux = verrouille && pose !== ordre[k];
            return (
              <button
                key={k}
                type="button"
                disabled={verrouille}
                onClick={() => setActif(actif === k ? null : k)}
                className={
                  'tuile flex min-h-[60px] items-center gap-3 rounded-[var(--radius-tile)] border-2 px-3 py-2 text-left text-kid-sm font-bold shadow-[var(--shadow-tile)] ' +
                  (juste
                    ? 'border-leaf bg-leaf/15'
                    : faux
                      ? 'border-clay bg-clay/12'
                      : actif === k
                        ? 'border-ink bg-sand'
                        : pose !== null
                          ? 'border-line bg-sand/60'
                          : 'border-line bg-white-warm')
                }
              >
                <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-gold text-kid-sm font-black text-ink">
                  {k + 1}
                </span>
                <span className="min-w-0 flex-1">
                  {pose === null ? (
                    <span className="text-muted">…</span>
                  ) : (
                    payload.etiquettes[pose]
                  )}
                </span>
              </button>
            );
          })}
        </div>

        <div className="grid content-start gap-2">
          {vue.map((j) => (
            <button
              key={j}
              type="button"
              disabled={verrouille || actif === null}
              onClick={() => poser(j)}
              className={
                'tuile min-h-[60px] rounded-[var(--radius-tile)] border-2 px-3 py-2 text-left text-kid-sm font-bold shadow-[var(--shadow-tile)] ' +
                (prises.has(j)
                  ? 'border-line bg-sand/60 opacity-60'
                  : actif === null
                    ? 'border-line bg-white-warm opacity-70'
                    : 'border-line bg-white-warm hover:border-ink-2')
              }
            >
              {payload.etiquettes[j]}
            </button>
          ))}
        </div>
      </div>

      {verrouille ? (
        <ul className="mt-4 grid gap-1 text-kid-sm text-ink-2">
          {ordre.map((j, k) => (
            <li key={k}>
              <strong>{k + 1}</strong> → {payload.etiquettes[j]}
            </li>
          ))}
        </ul>
      ) : poses.some((p) => p !== null) ? (
        <button
          type="button"
          className="mt-3 text-kid-sm font-bold text-clay underline"
          onClick={() => {
            setPoses(payload.etiquettes.map(() => null));
            setActif(null);
          }}
        >
          Recommencer
        </button>
      ) : null}
    </>
  );
}
