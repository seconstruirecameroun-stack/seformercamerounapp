import { Suspense, lazy, useState } from 'react';
import { energie, equipement, joursSansJouer, niveauDe, objetsDe, type Bilan, type Emplacement } from '../../lib/avatar';
import { JaugeEnergie, JaugeNiveau } from './Jauges';
import { APPARENCE_DEFAUT, fondDuStudio, type Apparence } from './apparence';

const Avatar3D = lazy(() => import('./Avatar3D'));

/**
 * Le personnage sur le banc d'essai : quatre enfants inventés, du débutant à
 * la légende, et un qui ne joue plus depuis trois jours. Rien n'est lu en
 * base : on juge le dessin, les animations et les jauges.
 */

const JOUR = new Date().toISOString().slice(0, 10);
const ilYA = (n: number) => new Date(Date.now() - n * 86_400_000).toISOString().slice(0, 10);

const BASE: Bilan = {
  etapesFranchies: 0, leconsTerminees: 0, leconsValidees: 0, images: 0, etoiles: 0, joursJoues: 0,
  serieJours: 0, serieManches: 0, or: 0, argent: 0, bronze: 0, matieresCompletes: 0,
  dernierJour: JOUR, joursRecents: 1,
};

const PROFILS: Array<{ nom: string; bilan: Bilan; choix?: Partial<Record<Emplacement, string | null>>; apparence?: Partial<Apparence> }> = [
  { nom: 'Débutant', bilan: { ...BASE, etapesFranchies: 1, images: 2, joursJoues: 2, serieJours: 2 } },
  { nom: 'Travailleur', bilan: {
    ...BASE, etapesFranchies: 30, leconsTerminees: 12, leconsValidees: 5, images: 60, joursJoues: 20,
    serieJours: 4, serieManches: 1, argent: 2, bronze: 1, joursRecents: 5,
  } },
  { nom: 'Endormi (3 jours)', bilan: {
    ...BASE, etapesFranchies: 30, leconsTerminees: 12, leconsValidees: 5, images: 60, joursJoues: 20,
    serieJours: 0, argent: 2, bronze: 1, dernierJour: ilYA(3), joursRecents: 3,
  } },
  { nom: 'Légende', bilan: {
    ...BASE, etapesFranchies: 400, leconsTerminees: 90, leconsValidees: 60, images: 260, joursJoues: 120,
    serieJours: 30, serieManches: 4, or: 6, argent: 4, bronze: 2, matieresCompletes: 2, joursRecents: 7,
  } },
  { nom: 'Tenue de rue', bilan: {
    ...BASE, etapesFranchies: 30, leconsTerminees: 12, leconsValidees: 5, images: 60, joursJoues: 20,
    serieJours: 4, serieManches: 1, argent: 2, bronze: 1, joursRecents: 5,
  }, choix: { tete: null, visage: 'lunettes', accessoire: 'bretelles', corps: null, dos: null, main: null, compagnon: null, aura: null },
  apparence: { peau: '#e0ac69' } },
  { nom: 'Capuche', bilan: {
    ...BASE, etapesFranchies: 30, leconsTerminees: 12, leconsValidees: 5, images: 60, joursJoues: 20,
    serieJours: 4, serieManches: 1, argent: 2, bronze: 1, joursRecents: 5,
  }, choix: { tete: 'capuche', visage: 'cache-cou', accessoire: null, corps: null, dos: null, main: null, compagnon: null, aura: null },
  apparence: { peau: '#e0ac69', haut: '#141416', cheveux: '#e8e8ec' } },
];

export default function PersonnageDEssai() {
  const [choix, setChoix] = useState(1);
  const b = PROFILS[choix].bilan;
  const porte = equipement(objetsDe(b, JOUR), PROFILS[choix].choix);
  const e = energie(b.dernierJour, JOUR);
  const sans = joursSansJouer(b.dernierJour, JOUR);
  return (
    <section className="mt-3 grid gap-3">
      <div className="flex flex-wrap gap-1.5">
        {PROFILS.map((p, i) => (
          <button
            key={p.nom}
            type="button"
            onClick={() => setChoix(i)}
            className={
              'rounded-full border-2 px-3 py-1 text-kid-xs font-black ' +
              (i === choix ? 'border-ink bg-ink text-white-warm' : 'border-line bg-white-warm')
            }
          >
            {p.nom}
          </button>
        ))}
      </div>
      <div className="overflow-hidden rounded-[var(--radius-card)] border-2 border-ink" style={{ background: fondDuStudio(APPARENCE_DEFAUT.fond) }}>
        <Suspense fallback={<div style={{ height: 360 }} />}>
          <Avatar3D equipement={porte} energie={e} hauteur={360} apparence={{ ...APPARENCE_DEFAUT, ...PROFILS[choix].apparence }} />
        </Suspense>
      </div>
      <div className="grid gap-3 rounded-[var(--radius-card)] border border-line bg-white-warm p-4">
        <JaugeNiveau niveau={niveauDe(b)} />
        <JaugeEnergie energie={e} joursSans={Number.isFinite(sans) ? sans : 0} />
        <p className="text-kid-xs font-bold text-ink-2">
          Porte : {Object.values(porte).map((o) => o?.nom).join(', ') || 'rien encore'}
        </p>
      </div>
    </section>
  );
}
