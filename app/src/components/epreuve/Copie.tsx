import { note } from '../../lib/composition';
import { appreciation, mention } from '../../lib/epreuve';

/**
 * Les trois morceaux d'une copie : l'en-tête, la situation problème, le
 * bulletin.
 *
 * Ils sont sortis de la salle de composition pour pouvoir se regarder sur le
 * banc d'essai, sans composition en base et sans écrire une ligne dans le
 * journal d'un enfant. La salle et le banc montrent donc exactement la même
 * copie.
 */

function Ligne({ nom, valeur }: { nom: string; valeur: string }) {
  return (
    <div className="flex items-baseline gap-3 border-b border-line py-1.5 last:border-b-0">
      <dt className="w-24 shrink-0 text-kid-xs font-black tracking-wide text-muted">{nom}</dt>
      <dd className="min-w-0 flex-1 text-kid-sm font-bold break-words">{valeur}</dd>
    </div>
  );
}

/** Le cartouche du haut de la copie : nom, date, classe, épreuve. */
export function EnTeteDeCopie(props: {
  nom: string;
  date: string;
  classe: string;
  epreuve: string;
}) {
  return (
    <dl className="rounded-[var(--radius-tile)] border-2 border-ink bg-white-warm px-3 py-1">
      <Ligne nom="NOM" valeur={props.nom} />
      <Ligne nom="DATE" valeur={props.date} />
      <Ligne nom="CLASSE" valeur={props.classe} />
      <Ligne nom="ÉPREUVE" valeur={props.epreuve} />
    </dl>
  );
}

/** Le texte à lire avant de répondre, et ce que vaut chaque partie. */
export function SituationProbleme(props: { texte: string; oral: number; ecrit: number }) {
  return (
    <>
      <section className="rounded-[var(--radius-card)] border border-line bg-white-warm/80 p-4">
        <h2 className="text-kid-sm font-black underline decoration-2 underline-offset-4">
          Situation problème
        </h2>
        <p className="mt-2 text-kid leading-relaxed">{props.texte}</p>
      </section>

      <section className="mt-4 grid grid-cols-2 gap-2">
        <div className="rounded-[var(--radius-tile)] bg-sand px-3 py-2 text-center">
          <p className="text-kid-xs font-black tracking-wide text-muted">ORAL</p>
          <p className="text-kid-lg font-black tabular-nums">{props.oral} pts</p>
        </div>
        <div className="rounded-[var(--radius-tile)] bg-sand px-3 py-2 text-center">
          <p className="text-kid-xs font-black tracking-wide text-muted">ÉCRIT</p>
          <p className="text-kid-lg font-black tabular-nums">{props.ecrit} pts</p>
        </div>
      </section>
    </>
  );
}

export type LigneDeBulletin = { numero: number; titre: string; eus: number; sur: number };

/** La note, l'appréciation, et le détail par partie et par exercice. */
export function Bulletin(props: {
  oral: number;
  surOral: number;
  ecrit: number;
  surEcrit: number;
  exercices: LigneDeBulletin[];
}) {
  const obtenus = props.oral + props.ecrit;
  const total = props.surOral + props.surEcrit;
  const lettre = mention(obtenus, total);
  return (
    <>
      <section className="rounded-[var(--radius-card)] border-2 border-ink bg-white-warm p-4 text-center">
        <p className="text-5xl font-black tabular-nums">{note(obtenus, total)}</p>
        <p className="mt-2 inline-flex flex-wrap items-center justify-center gap-x-2 rounded-full border-2 border-clay px-4 py-1 text-kid-lg font-black text-clay-dark">
          {lettre}
          <span className="text-kid-sm font-bold text-ink-2">{appreciation(lettre)}</span>
        </p>
      </section>

      <section className="mt-4 rounded-[var(--radius-card)] border border-line bg-white-warm/80 p-4">
        <div className="flex items-baseline justify-between gap-3">
          <h2 className="text-kid-sm font-black">Oral</h2>
          <span className="text-kid-sm font-black tabular-nums">
            {note(props.oral, props.surOral)}
          </span>
        </div>
        <div className="mt-3 flex items-baseline justify-between gap-3 border-t border-line pt-3">
          <h2 className="text-kid-sm font-black">Écrit</h2>
          <span className="text-kid-sm font-black tabular-nums">
            {note(props.ecrit, props.surEcrit)}
          </span>
        </div>
        <ul className="mt-2 grid grid-cols-1 gap-2">
          {props.exercices.map((ex) => (
            <li key={ex.numero} className="flex items-baseline justify-between gap-3">
              <span className="min-w-0 text-kid-xs font-bold text-ink-2">
                {ex.numero}. {ex.titre}
              </span>
              <span
                className={
                  'shrink-0 text-kid-xs font-black tabular-nums ' +
                  (ex.eus === ex.sur ? 'text-leaf' : 'text-clay-dark')
                }
              >
                {note(ex.eus, ex.sur)}
              </span>
            </li>
          ))}
        </ul>
      </section>
    </>
  );
}
