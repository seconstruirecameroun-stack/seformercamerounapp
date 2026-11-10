import { Link } from 'react-router-dom';
import Illustration from './Illustration';
import type { LeconResume } from '../lib/dashboard';
import { PALIERS } from '../lib/paliers';
import { jourCourt } from '../lib/rangement';

/**
 * Où en est l'enfant dans cette leçon : l'escalier, et la marche en cours.
 *
 * Le pourcentage de notions acquises qui figurait ici ne disait rien à un
 * enfant — il ne voyait ni où il était, ni ce qu'il visait.
 */
export default function CarteLecon({
  lecon,
  childId,
  montrerMatiere = true,
}: {
  lecon: LeconResume;
  childId: string;
  /** Inutile dans le dossier d'une matière : il la porte déjà en titre. */
  montrerMatiere?: boolean;
}) {
  const part =
    lecon.etapeTotal > 0 ? Math.round((lecon.etapeFaites / lecon.etapeTotal) * 100) : 0;
  return (
    <Link
      to={`/enfant/${childId}/lecon/${lecon.id}`}
      className="tuile flex items-center gap-3 overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm p-2 pr-4 shadow-[var(--shadow-tile)]"
    >
      <Illustration
        cle={lecon.illustration}
        forme="scene"
        alt=""
        className="h-20 w-28 shrink-0 rounded-2xl object-cover"
      />
      <div className="min-w-0 flex-1">
        {montrerMatiere ? (
          <p className="text-kid-xs font-black tracking-wide text-muted uppercase">
            {lecon.matiere ?? 'Leçon'}
          </p>
        ) : null}
        <h3 className="line-clamp-2 text-kid font-extrabold">{lecon.title}</h3>
        <div className="mt-1.5 flex items-center gap-2">
          <span className="flex shrink-0 items-center gap-1" aria-hidden="true">
            {/* L'escalier se compte depuis PALIERS, jamais à la main : le jour
                où une marche est ajoutée — le Défi l'a été — une liste écrite
                en dur fait mentir la carte sur ce qu'il reste à franchir. */}
            {PALIERS.map(({ niveau: n }) => (
              <span
                key={n}
                className={
                  // 14 px dans une pastille de 24 : à 11 px le numéro de l'étape
                  // se devinait plus qu'il ne se lisait, sur une carte dont
                  // c'est pourtant l'information principale.
                  'grid h-6 w-6 place-items-center rounded-full text-sm leading-none font-black ' +
                  (lecon.etapeTerminee || n < lecon.etape
                    ? 'bg-leaf text-white-warm'
                    : n === lecon.etape
                      ? 'bg-gold text-ink'
                      : 'bg-line text-muted')
                }
              >
                {lecon.etapeTerminee || n < lecon.etape ? '★' : n}
              </span>
            ))}
          </span>
          <span className="h-2 flex-1 overflow-hidden rounded-full bg-ink/15">
            <span
              className="block h-full rounded-full bg-gold transition-all duration-500"
              style={{ width: `${part}%` }}
            />
          </span>
        </div>
        <p className="mt-1 flex items-center gap-2 text-kid-xs font-bold text-muted">
          {/* L'escalier gravi n'est pas la leçon sue : tant que la manche
              n'est pas passée, la carte annonce ce qu'il reste à faire plutôt
              qu'une révision tranquille.

              Le rang de la série y est, et il compte : « la manche t'attend »
              laissait croire qu'il fallait reprendre les trente questions
              alors qu'il en avait déjà tenu deux tiers. Ce qui reste à faire
              doit se lire sans ouvrir la leçon. */}
          <span className={lecon.validee ? 'font-black text-leaf' : undefined}>
            {lecon.validee
              ? '✓ Leçon validée'
              : lecon.validationPerdue
                ? `À revalider · série ${lecon.seriesTenues + 1}/${lecon.seriesTotal}`
                : lecon.etapeTerminee
                  ? lecon.seriesTotal > 1
                    ? `Série ${lecon.seriesTenues + 1}/${lecon.seriesTotal} t’attend`
                    : 'La manche t’attend'
                  : `Étape ${lecon.etape} · ${lecon.etapeFaites}/${lecon.etapeTotal}`}
          </span>
          {/* Le jour du cahier : ce n'est pas ce que l'enfant vient chercher,
              mais c'est ce qui l'aide à reconnaître « le cours de mardi ». */}
          {jourCourt(lecon.date) ? (
            <span className="shrink-0 font-semibold opacity-70">{jourCourt(lecon.date)}</span>
          ) : null}
        </p>
      </div>
      {lecon.aRevoir > 0 ? (
        <span className="grid h-7 min-w-7 shrink-0 place-items-center rounded-full bg-clay px-2 text-kid-xs font-black text-white-warm">
          {lecon.aRevoir}
        </span>
      ) : null}
    </Link>
  );
}
