import { useState } from 'react';
import type { ItemRow } from '../../types/db';
import Illustration from '../Illustration';
import { Button } from '../ui';
import { ecartMot, Enonce, LETTRES, memeMot } from './partage';
import Clavier, { useChampActif } from './Clavier';
import LettresMobiles from './LettresMobiles';
import { accentsComptent, modeSaisie } from '../../lib/saisie';
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

/**
 * La faute, montrée à l’endroit où elle est.
 *
 * « Réponse : sablonneux » ne dit pas à un enfant ce qu’il a raté. On lui
 * met ses deux mots l’un sous l’autre, avec la seule lettre qui diffère en
 * couleur — il voit qu’il lui manquait un n, et c’est ce qu’il retiendra.
 */
function Faute({
  ecrit,
  attendu,
  accents = false,
}: {
  ecrit: string;
  attendu: string;
  accents?: boolean;
}) {
  const e = ecartMot(ecrit, attendu, accents);
  if (ecrit.trim() === '') return null;
  // Rien de commun : les deux mots n’ont pas de rapport, le détail de la
  // divergence n’apprendrait rien. On se tait plutôt que de bricoler.
  if (e.debut === '' && e.fin === '') return null;

  return (
    <div className="rounded-2xl bg-clay/10 px-4 py-3">
      <p className="text-kid-xs font-black tracking-widest text-clay-dark uppercase">
        Tu as écrit
      </p>
      <p className="mt-0.5 text-kid font-extrabold">
        <span>{e.debut}</span>
        <span className="rounded bg-clay/30 px-0.5 text-clay-dark line-through">{e.ecrit}</span>
        <span>{e.fin}</span>
      </p>
      <p className="mt-2 text-kid-xs font-black tracking-widest text-leaf uppercase">
        Il fallait écrire
      </p>
      <p className="mt-0.5 text-kid font-extrabold">
        <span>{e.debut}</span>
        <span className="rounded bg-leaf/30 px-0.5 text-leaf">{e.attendu}</span>
        <span>{e.fin}</span>
      </p>
    </div>
  );
}

function TexteATrous({ item, onRepondre, verrouille, visuel, rang }: Props) {
  const payload = item.payload as { text: string; blanks: number };
  const attendues = (item.answer as { values: string[] }).values;
  const [saisies, setSaisies] = useState<string[]>(() => attendues.map(() => ''));
  // Le clavier de l’app écrit dans le trou que l’enfant vient de toucher.
  const champs = useChampActif(attendues.length);
  // Aux petites classes, l’étape Maîtrise se joue aux étiquettes : la règle
  // vit dans lib/saisie.ts, avec le constat qui l’a fait écrire.
  const etiquettes = modeSaisie(rang ?? null, item.level) === 'lettres-mobiles';
  // Aux étiquettes, « rempli » ne suffit pas : il faut avoir posé toutes les
  // lettres, sinon on valide un mot tronqué sans rien en dire.
  const entier = saisies.every((s, i) => s.length === (attendues[i] ?? '').length);
  // Au Défi, l'accent compte. La règle et son pourquoi vivent dans lib/saisie.ts.
  const accents = accentsComptent(item.level);
  const juste = (i: number) => memeMot(saisies[i] ?? '', attendues[i] ?? '', accents);

  const morceaux = payload.text.split(/\{\{\d+\}\}/);
  const complet = saisies.every((s) => s.trim() !== '');

  function ecrire(v: string) {
    const copie = [...saisies];
    copie[champs.actif] = v;
    setSaisies(copie);
  }

  function valider() {
    onRepondre({
      correct: saisies.every((_s, i) => juste(i)),
      donnee: { values: saisies },
    });
  }

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
                    ? juste(i)
                      ? 'border-leaf text-leaf'
                      : 'border-clay text-clay-dark'
                    : 'border-line focus:border-clay')
                }
                value={saisies[i]}
                disabled={verrouille}
                {...champs.liens(i)}
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
        <div className="mt-4 grid gap-2">
          {attendues.map((mot, i) =>
            juste(i) ? null : (
              <Faute key={i} ecrit={saisies[i] ?? ''} attendu={mot} accents={accents} />
            ),
          )}
          <p className="text-kid-sm text-ink-2">
            Réponse : <strong>{attendues.join(' · ')}</strong>
          </p>
        </div>
      ) : etiquettes ? (
        <>
          {attendues.map((mot, i) => (
            <div key={i} className="mt-4">
              {attendues.length > 1 ? (
                <p className="text-kid-xs font-black tracking-widest text-clay-dark uppercase">
                  Trou {i + 1}
                </p>
              ) : null}
              <LettresMobiles
                attendu={mot}
                graine={item.id + ':' + i}
                onChange={(v) => {
                  setSaisies((avant) => {
                    const copie = [...avant];
                    copie[i] = v;
                    return copie;
                  });
                }}
              />
            </div>
          ))}
          <Button className="mt-5" onClick={valider} disabled={!entier}>
            Vérifier
          </Button>
        </>
      ) : (
        <>
          {attendues.length > 1 ? (
            <p className="mt-3 text-kid-sm text-muted">
              Touche un trou pour y écrire. Trou {champs.actif + 1} sur {attendues.length}.
            </p>
          ) : null}
          <Clavier
            valeur={saisies[champs.actif] ?? ''}
            onChange={ecrire}
            onValider={valider}
            validerActif={complet}
          />
        </>
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
