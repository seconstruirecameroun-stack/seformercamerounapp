import type { niveauDe } from '../../lib/avatar';
import { ENERGIE_POUR_BRILLER, JOURS_AVANT_PERTE } from '../../lib/avatar';

/**
 * Les deux jauges du personnage : son niveau, et son énergie.
 *
 * Elles disent toujours ce qui vient : combien de points jusqu'au niveau
 * suivant, ce qu'il exige en plus ; et ce que coûtera un jour de plus sans
 * travail.
 */

export function JaugeNiveau({ niveau }: { niveau: ReturnType<typeof niveauDe> }) {
  return (
    <div>
      <div className="flex items-baseline justify-between gap-2">
        <p className="text-kid-sm font-black">
          Niveau {niveau.actuel.rang} · {niveau.actuel.nom}
        </p>
        <p className="text-kid-xs font-bold text-muted tabular-nums">{niveau.points} pts</p>
      </div>
      <div className="mt-1 h-3 overflow-hidden rounded-full bg-line">
        <div
          className="h-full rounded-full bg-[linear-gradient(90deg,#f5b335,#f97316)] transition-[width] duration-700"
          style={{ width: `${Math.round(niveau.part * 100)}%` }}
        />
      </div>
      <p className="mt-1 text-[0.78rem] font-bold leading-tight text-ink-2">
        {niveau.suivant
          ? niveau.manquePoints > 0
            ? `Encore ${niveau.manquePoints} points pour devenir ${niveau.suivant.nom}` +
              (niveau.manqueCondition ? `, et ${niveau.manqueCondition}` : '')
            : `Pour devenir ${niveau.suivant.nom} : ${niveau.manqueCondition}`
          : 'Tu es une Légende. Le plus haut niveau !'}
      </p>
    </div>
  );
}

export function JaugeEnergie({ energie, joursSans }: { energie: number; joursSans: number }) {
  const couleur = energie >= ENERGIE_POUR_BRILLER ? '#22c55e' : energie >= 40 ? '#f59e0b' : '#ef4444';
  const message =
    energie === 100
      ? 'Plein d’énergie ! Tous tes objets brillent.'
      : energie > 0
        ? 'Ton personnage s’endort : travaille aujourd’hui pour le recharger.'
        : 'Ton personnage dort. Une séance le réveille !';
  const reste = JOURS_AVANT_PERTE - joursSans;
  return (
    <div>
      <div className="flex items-baseline justify-between gap-2">
        <p className="text-kid-sm font-black">⚡ Énergie</p>
        <p className="text-kid-xs font-black tabular-nums" style={{ color: couleur }}>
          {energie} %
        </p>
      </div>
      <div className="mt-1 h-3 overflow-hidden rounded-full bg-line">
        <div className="h-full rounded-full transition-[width] duration-700" style={{ width: `${energie}%`, background: couleur }} />
      </div>
      <p className="mt-1 text-[0.78rem] font-bold leading-tight text-ink-2">{message}</p>
      {joursSans > 0 && reste > 0 ? (
        <p className="mt-0.5 text-[0.78rem] font-black leading-tight text-clay-dark">
          Encore {reste} jour{reste > 1 ? 's' : ''} sans travail et tes pouvoirs du moment s’envolent.
        </p>
      ) : null}
    </div>
  );
}
