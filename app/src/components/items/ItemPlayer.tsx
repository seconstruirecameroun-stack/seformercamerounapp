import { useState } from 'react';
import type { ItemRow } from '../../types/db';
import { Button } from '../ui';

/**
 * Un item, quel que soit son type, se joue de la même façon :
 * l'enfant répond, on dit si c'est juste, on passe.
 *
 * Chaque type a sa forme de payload et de réponse. Les gardes ci-dessous
 * refusent de jouer un item mal formé plutôt que de planter l'écran : un
 * contenu généré peut toujours arriver de travers, et l'enfant n'a pas à en
 * faire les frais.
 */

export type Reponse = { correct: boolean; donnee: unknown };

type Props = { item: ItemRow; onRepondre: (r: Reponse) => void; verrouille: boolean };

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

function Qcm({ item, onRepondre, verrouille }: Props) {
  const payload = item.payload as { question: string; options: string[] };
  const bonne = (item.answer as { index: number }).index;
  const [choisi, setChoisi] = useState<number | null>(null);

  return (
    <>
      <h3 className="text-xl font-bold">{payload.question}</h3>
      <div className="mt-4 grid gap-2">
        {payload.options.map((option, i) => {
          let look = 'border-line bg-white-warm hover:border-ink-2';
          if (verrouille && i === bonne) look = 'border-leaf bg-leaf/15';
          else if (verrouille && i === choisi) look = 'border-clay bg-clay/10';
          return (
            <button
              key={i}
              type="button"
              disabled={verrouille}
              className={'rounded-2xl border px-4 py-3 text-left transition ' + look}
              onClick={() => {
                setChoisi(i);
                onRepondre({ correct: i === bonne, donnee: { index: i } });
              }}
            >
              {option}
            </button>
          );
        })}
      </div>
    </>
  );
}

function Chronologie({ item, onRepondre, verrouille }: Props) {
  const payload = item.payload as { question: string; tokens: string[] };
  const ordre = (item.answer as { order: number[] }).order;
  const [choisis, setChoisis] = useState<number[]>([]);

  const restants = payload.tokens.map((_, i) => i).filter((i) => !choisis.includes(i));

  function ajouter(i: number) {
    const suite = [...choisis, i];
    setChoisis(suite);
    if (suite.length === payload.tokens.length) {
      const correct = suite.every((val, pos) => val === ordre[pos]);
      onRepondre({ correct, donnee: { order: suite } });
    }
  }

  return (
    <>
      <h3 className="text-xl font-bold">{payload.question}</h3>
      <p className="mt-1 text-sm text-muted">Touche les étiquettes dans le bon ordre.</p>

      <ol className="mt-4 grid gap-2">
        {payload.tokens.map((_, position) => {
          const rempli = choisis[position];
          const juste = verrouille && rempli === ordre[position];
          const faux = verrouille && rempli !== undefined && rempli !== ordre[position];
          return (
            <li
              key={position}
              className={
                'flex items-center gap-3 rounded-2xl border px-4 py-3 ' +
                (juste
                  ? 'border-leaf bg-leaf/15'
                  : faux
                    ? 'border-clay bg-clay/10'
                    : 'border-dashed border-line')
              }
            >
              <span className="grid h-7 w-7 place-items-center rounded-full bg-gold/30 text-sm font-bold">
                {position + 1}
              </span>
              <span className={rempli === undefined ? 'text-muted' : ''}>
                {rempli === undefined ? 'à compléter' : payload.tokens[rempli]}
              </span>
              {faux ? (
                <span className="ml-auto text-xs text-clay-dark">
                  → {payload.tokens[ordre[position]]}
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
              className="rounded-full border border-line bg-white-warm px-4 py-2 text-sm hover:border-ink-2"
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
          className="mt-3 text-sm font-semibold text-clay underline"
          onClick={() => setChoisis([])}
        >
          Recommencer
        </button>
      ) : null}
    </>
  );
}

function TexteATrous({ item, onRepondre, verrouille }: Props) {
  const payload = item.payload as { text: string; blanks: number };
  const attendues = (item.answer as { values: string[] }).values;
  const [saisies, setSaisies] = useState<string[]>(() => attendues.map(() => ''));

  const morceaux = payload.text.split(/\{\{\d+\}\}/);
  const complet = saisies.every((s) => s.trim() !== '');

  function valider() {
    const correct = saisies.every((s, i) => memeMot(s, attendues[i] ?? ''));
    onRepondre({ correct, donnee: { values: saisies } });
  }

  return (
    <>
      <h3 className="text-xl font-bold">Complète la phrase</h3>
      <p className="mt-4 text-lg leading-relaxed">
        {morceaux.map((morceau, i) => (
          <span key={i}>
            {morceau}
            {i < saisies.length ? (
              <input
                className={
                  'mx-1 inline-block w-32 rounded-xl border-b-2 bg-transparent px-2 py-1 text-center outline-none ' +
                  (verrouille
                    ? memeMot(saisies[i], attendues[i] ?? '')
                      ? 'border-leaf text-leaf'
                      : 'border-clay text-clay-dark line-through'
                    : 'border-line focus:border-ink-2')
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
        <p className="mt-3 text-sm text-ink-2">
          Réponse : <strong>{attendues.join(' · ')}</strong>
        </p>
      ) : (
        <Button className="mt-4" onClick={valider} disabled={!complet}>
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
    case 'qcm':
      return (
        typeof p.question === 'string' &&
        tableau(p.options) &&
        typeof a.index === 'number' &&
        a.index >= 0 &&
        a.index < (p.options as unknown[]).length
      );
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
      <p className="text-sm text-muted">
        Cette question n’est pas encore jouable ici ({item.kind}). Elle reste en base, rien n’est
        perdu.
      </p>
    );
  }

  switch (item.kind) {
    case 'qcm':
      return <Qcm {...props} />;
    case 'chronologie':
      return <Chronologie {...props} />;
    default:
      return <TexteATrous {...props} />;
  }
}
