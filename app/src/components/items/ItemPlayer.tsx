import { useState } from 'react';
import type { ItemRow } from '../../types/db';
import { Button } from '../ui';
import Illustration from '../Illustration';
import { Enonce, LETTRES, memeMot } from './partage';
import type { Props } from './partage';
import VraiFaux from './VraiFaux';
import Association from './Association';
import Dictee from './Dictee';

export type { Reponse } from './partage';
export { memeMot } from './partage';

/**
 * Un item, quel que soit son type, se joue de la même façon :
 * l'enfant répond, on dit si c'est juste, on passe.
 *
 * Tout est dimensionné pour un doigt sur un téléphone partagé : cibles d'au
 * moins 60 px de haut, texte large, et aucun glisser-déposer.
 */

function Qcm({ item, onRepondre, verrouille, visuel }: Props) {
  const payload = item.payload as { question: string; options?: string[]; images?: string[] };
  const bonne = (item.answer as { index: number }).index;
  const [choisi, setChoisi] = useState<number | null>(null);

  // Quand les réponses sont des images, on les montre en grand plutôt que
  // d'écrire leur nom : à sept ans, reconnaître une terre rouge est plus sûr
  // que lire « ferralitique ».
  if (payload.images) {
    return (
      <>
        <Enonce visuel={visuel}>{payload.question}</Enonce>
        <div className="mt-5 grid grid-cols-2 gap-3">
          {payload.images.map((cle, i) => {
            const estBonne = verrouille && i === bonne;
            const estRate = verrouille && i === choisi && i !== bonne;
            return (
              <button
                key={i}
                type="button"
                disabled={verrouille}
                onClick={() => {
                  setChoisi(i);
                  onRepondre({ correct: i === bonne, donnee: { index: i } });
                }}
                className={
                  'tuile relative overflow-hidden rounded-[var(--radius-tile)] border-[3px] shadow-[var(--shadow-tile)] ' +
                  (estBonne
                    ? 'border-leaf'
                    : estRate
                      ? 'border-clay'
                      : verrouille
                        ? 'border-line opacity-55'
                        : 'border-line hover:border-ink-2')
                }
              >
                <Illustration cle={cle} forme="objet" alt="" className="h-28 w-full object-cover sm:h-36" />
                <span
                  aria-hidden="true"
                  className={
                    'absolute top-1.5 left-1.5 grid h-8 w-8 place-items-center rounded-full text-kid-sm font-black ' +
                    (estBonne
                      ? 'bg-leaf text-white-warm'
                      : estRate
                        ? 'bg-clay text-white-warm'
                        : 'bg-white-warm/90 text-ink')
                  }
                >
                  {estBonne ? '✓' : estRate ? '✗' : LETTRES[i]}
                </span>
              </button>
            );
          })}
        </div>
      </>
    );
  }

  const options = payload.options ?? [];

  return (
    <>
      <Enonce visuel={visuel}>{payload.question}</Enonce>
      <div className="mt-5 grid gap-3">
        {options.map((option, i) => {
          const estBonne = verrouille && i === bonne;
          const estRate = verrouille && i === choisi && i !== bonne;
          return (
            <button
              key={i}
              type="button"
              disabled={verrouille}
              onClick={() => {
                setChoisi(i);
                onRepondre({ correct: i === bonne, donnee: { index: i } });
              }}
              className={
                'tuile flex min-h-[60px] items-center gap-3 rounded-[var(--radius-tile)] border-2 px-4 py-3 text-left text-kid shadow-[var(--shadow-tile)] ' +
                (estBonne
                  ? 'border-leaf bg-leaf/15'
                  : estRate
                    ? 'border-clay bg-clay/12'
                    : verrouille
                      ? 'border-line bg-white-warm opacity-55'
                      : 'border-line bg-white-warm hover:border-ink-2')
              }
            >
              <span
                aria-hidden="true"
                className={
                  'grid h-9 w-9 shrink-0 place-items-center rounded-full text-kid-sm font-black ' +
                  (estBonne
                    ? 'bg-leaf text-white-warm'
                    : estRate
                      ? 'bg-clay text-white-warm'
                      : 'bg-sand text-ink')
                }
              >
                {estBonne ? '✓' : estRate ? '✗' : LETTRES[i]}
              </span>
              <span className="flex-1">{option}</span>
            </button>
          );
        })}
      </div>
    </>
  );
}

function Chronologie({ item, onRepondre, verrouille, visuel }: Props) {
  const payload = item.payload as { question: string; tokens: string[]; consigne?: string };
  const ordre = (item.answer as { order: number[] }).order;
  const [choisis, setChoisis] = useState<number[]>([]);

  const restants = payload.tokens.map((_, i) => i).filter((i) => !choisis.includes(i));

  function ajouter(i: number) {
    const suite = [...choisis, i];
    setChoisis(suite);
    if (suite.length === payload.tokens.length) {
      onRepondre({ correct: suite.every((v, pos) => v === ordre[pos]), donnee: { order: suite } });
    }
  }

  return (
    <>
      <Enonce visuel={visuel}>{payload.question}</Enonce>
      <p className="mt-1 text-kid-sm text-muted">
        {payload.consigne ?? 'Touche les étiquettes dans le bon ordre.'}
      </p>

      <ol className="mt-5 grid gap-2">
        {payload.tokens.map((_, position) => {
          const rempli = choisis[position];
          const juste = verrouille && rempli === ordre[position];
          const faux = verrouille && rempli !== undefined && rempli !== ordre[position];
          return (
            <li
              key={position}
              className={
                'flex min-h-[56px] items-center gap-3 rounded-[var(--radius-tile)] border-2 px-4 py-3 text-kid ' +
                (juste
                  ? 'border-leaf bg-leaf/15'
                  : faux
                    ? 'border-clay bg-clay/12'
                    : 'border-dashed border-line bg-white-warm/60')
              }
            >
              <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-sand text-kid-sm font-black">
                {position + 1}
              </span>
              <span className={rempli === undefined ? 'text-muted' : 'font-semibold'}>
                {rempli === undefined ? 'à compléter' : payload.tokens[rempli]}
              </span>
              {faux ? (
                <span className="ml-auto text-right text-kid-sm text-clay-dark">
                  {payload.tokens[ordre[position]]}
                </span>
              ) : null}
            </li>
          );
        })}
      </ol>

      {!verrouille && restants.length > 0 ? (
        <div className="mt-4 flex flex-wrap gap-2">
          {restants.map((i) => (
            <button
              key={i}
              type="button"
              className="tuile min-h-[48px] rounded-full border-2 border-line bg-white-warm px-5 text-kid font-semibold shadow-[var(--shadow-tile)] hover:border-ink-2"
              onClick={() => ajouter(i)}
            >
              {payload.tokens[i]}
            </button>
          ))}
        </div>
      ) : null}

      {!verrouille && choisis.length > 0 ? (
        <button
          type="button"
          className="mt-3 text-kid-sm font-bold text-clay underline"
          onClick={() => setChoisis([])}
        >
          Recommencer
        </button>
      ) : null}
    </>
  );
}

function TexteATrous({ item, onRepondre, verrouille, visuel }: Props) {
  const payload = item.payload as { text: string; blanks: number };
  const attendues = (item.answer as { values: string[] }).values;
  const [saisies, setSaisies] = useState<string[]>(() => attendues.map(() => ''));

  const morceaux = payload.text.split(/\{\{\d+\}\}/);
  const complet = saisies.every((s) => s.trim() !== '');

  return (
    <>
      <Enonce visuel={visuel}>Complète la phrase</Enonce>
      <p className="mt-5 text-kid leading-[2.3]">
        {morceaux.map((morceau, i) => (
          <span key={i}>
            {morceau}
            {i < saisies.length ? (
              <input
                aria-label={`Mot ${i + 1}`}
                className={
                  'mx-1 inline-block w-28 max-w-[42vw] rounded-xl border-b-[3px] bg-sand/50 px-2 py-1 text-center font-bold outline-none ' +
                  (verrouille
                    ? memeMot(saisies[i], attendues[i] ?? '')
                      ? 'border-leaf text-leaf'
                      : 'border-clay text-clay-dark'
                    : 'border-line focus:border-clay')
                }
                value={saisies[i]}
                disabled={verrouille}
                onChange={(e) => {
                  const copie = [...saisies];
                  copie[i] = e.target.value;
                  setSaisies(copie);
                }}
              />
            ) : null}
          </span>
        ))}
      </p>

      {verrouille ? (
        <p className="mt-4 text-kid-sm text-ink-2">
          Réponse : <strong>{attendues.join(' · ')}</strong>
        </p>
      ) : (
        <Button
          className="mt-5"
          onClick={() =>
            onRepondre({
              correct: saisies.every((s, i) => memeMot(s, attendues[i] ?? '')),
              donnee: { values: saisies },
            })
          }
          disabled={!complet}
        >
          Vérifier
        </Button>
      )}
    </>
  );
}

const tableau = (v: unknown) => Array.isArray(v) && v.length > 0;

/**
 * Un item est jouable si sa forme correspond à son type.
 *
 * La vérification a lieu ici, avant le rendu : un composant qui lirait un
 * payload de travers planterait l'écran entier, et React n'attrape pas cela
 * depuis le parent.
 */
export function estJouable(item: ItemRow): boolean {
  const p = item.payload as Record<string, unknown> | null;
  const a = item.answer as Record<string, unknown> | null;
  if (!p || !a) return false;

  switch (item.kind) {
    case 'qcm': {
      // Les réponses sont des textes ou des images, jamais les deux.
      const choix = (p.images ?? p.options) as unknown[];
      return (
        typeof p.question === 'string' &&
        tableau(choix) &&
        typeof a.index === 'number' &&
        a.index >= 0 &&
        a.index < choix.length
      );
    }
    case 'vrai_faux':
      return typeof p.statement === 'string' && typeof a.value === 'boolean';
    case 'association':
      return (
        typeof p.question === 'string' &&
        tableau(p.gauche) &&
        tableau(p.droite) &&
        tableau(a.order) &&
        (a.order as unknown[]).length === (p.gauche as unknown[]).length &&
        (a.order as number[]).every(
          (j) => Number.isInteger(j) && j >= 0 && j < (p.droite as unknown[]).length,
        ) &&
        new Set(a.order as number[]).size === (a.order as unknown[]).length
      );
    case 'dictee':
      return typeof p.phrase === 'string' && (p.phrase as string).trim().length > 0;
    case 'chronologie':
      return (
        typeof p.question === 'string' &&
        tableau(p.tokens) &&
        tableau(a.order) &&
        (a.order as unknown[]).length === (p.tokens as unknown[]).length
      );
    case 'texte_a_trous':
      return (
        typeof p.text === 'string' &&
        tableau(a.values) &&
        p.text.split(/\{\{\d+\}\}/).length - 1 === (a.values as unknown[]).length
      );
    default:
      return false;
  }
}

export default function ItemPlayer(props: Props) {
  const { item } = props;

  if (!estJouable(item)) {
    return (
      <p className="text-kid-sm text-muted">
        Cette question n’est pas encore jouable ici ({item.kind}). Elle reste en base, rien n’est
        perdu.
      </p>
    );
  }

  switch (item.kind) {
    case 'qcm':
      return <Qcm {...props} />;
    case 'vrai_faux':
      return <VraiFaux {...props} />;
    case 'association':
      return <Association {...props} />;
    case 'dictee':
      return <Dictee {...props} />;
    case 'chronologie':
      return <Chronologie {...props} />;
    default:
      return <TexteATrous {...props} />;
  }
}
