import { Suspense, lazy } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ErrorNote, Loading } from '../../components/ui';
import { usePersonnage, jourUTC } from '../../components/avatar/personnage';
import { JaugeEnergie, JaugeNiveau } from '../../components/avatar/Jauges';
import {
  BAS,
  CHEVEUX,
  COIFFURES,
  EXPRESSIONS,
  FONDS,
  HAUTS,
  PEAUX,
  fondDuStudio,
  type Apparence,
} from '../../components/avatar/apparence';
import { NIVEAUX, joursSansJouer, type Emplacement, type ObjetPossede, type Rarete } from '../../lib/avatar';

const Avatar3D = lazy(() => import('../../components/avatar/Avatar3D'));

/**
 * La page du personnage : le héros en grand, ses objets, et l'échelle des
 * niveaux jusqu'à la Légende.
 *
 * Chaque objet non gagné dit ce qu'il faut faire pour l'avoir, et où en est
 * l'enfant : « Valide 10 leçons — 4 sur 10 ». Un objet qu'on voit, avec sa
 * barre qui avance, donne une raison de faire la leçon suivante.
 */

const PLACES: Array<{ cle: Emplacement; nom: string }> = [
  { cle: 'tete', nom: 'Tête' },
  { cle: 'visage', nom: 'Visage' },
  { cle: 'corps', nom: 'Tenue' },
  { cle: 'accessoire', nom: 'Accessoires' },
  { cle: 'dos', nom: 'Dos' },
  { cle: 'main', nom: 'Main' },
  { cle: 'pieds', nom: 'Pieds' },
  { cle: 'compagnon', nom: 'Compagnon' },
  { cle: 'aura', nom: 'Pouvoirs du moment' },
];

const RARETE: Record<Rarete, { nom: string; couleur: string; fond: string }> = {
  commun: { nom: 'Commun', couleur: '#64748b', fond: '#f1f5f9' },
  rare: { nom: 'Rare', couleur: '#2563eb', fond: '#dbeafe' },
  epique: { nom: 'Épique', couleur: '#7c3aed', fond: '#ede9fe' },
  legendaire: { nom: 'Légendaire', couleur: '#b45309', fond: '#fef3c7' },
};

function CarteObjet({ o, porte, onPorter }: { o: ObjetPossede; porte: boolean; onPorter: () => void }) {
  const r = RARETE[o.rarete];
  return (
    <li
      className="rounded-2xl border-2 p-2.5"
      style={{ borderColor: o.gagne ? r.couleur : '#e5e7eb', background: o.gagne ? r.fond : '#fafafa' }}
    >
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <p className={'text-kid-sm font-black leading-tight ' + (o.gagne ? '' : 'text-muted')}>
            {o.gagne ? '' : '🔒 '}
            {o.nom}
          </p>
          <p className="text-[0.72rem] font-black uppercase tracking-wide" style={{ color: r.couleur }}>
            {r.nom}
            {o.temporaire ? ' · pouvoir' : ''}
          </p>
        </div>
        {o.gagne ? (
          <button
            type="button"
            onClick={onPorter}
            className={
              'shrink-0 rounded-full px-2.5 py-1 text-[0.72rem] font-black ' +
              (porte ? 'bg-ink text-white-warm' : 'border-2 border-ink bg-white-warm')
            }
          >
            {porte ? 'Porté' : 'Porter'}
          </button>
        ) : null}
      </div>
      {o.gagne ? (
        o.eteint ? (
          <p className="mt-1 text-[0.72rem] font-bold text-clay-dark">Éteint : recharge ton énergie pour qu’il brille.</p>
        ) : null
      ) : (
        <>
          <p className="mt-1 text-[0.75rem] font-bold leading-tight text-ink-2">{o.condition}</p>
          <div className="mt-1 h-2 overflow-hidden rounded-full bg-line">
            <div className="h-full rounded-full" style={{ width: `${(o.fait / o.but) * 100}%`, background: r.couleur }} />
          </div>
          <p className="mt-0.5 text-right text-[0.7rem] font-black tabular-nums text-muted">
            {o.fait} / {o.but}
          </p>
        </>
      )}
    </li>
  );
}

export default function Personnage() {
  const { childId } = useParams();
  const { chargement, erreur, calcul, reglages, setReglages } = usePersonnage(childId);

  if (chargement) return <Loading label="Ton personnage arrive…" />;
  if (erreur) return <ErrorNote error={erreur} />;
  if (!calcul || !childId) return null;

  const sans = joursSansJouer(calcul.bilan.dernierJour, jourUTC());
  const gagnes = calcul.objets.filter((o) => o.gagne).length;

  const porter = (o: ObjetPossede) => {
    const deja = calcul.porte[o.emplacement]?.id === o.id;
    setReglages({ ...reglages, choix: { ...reglages.choix, [o.emplacement]: deja ? null : o.id } });
  };

  return (
    <main className="enfant ciel min-h-screen pb-16">
      <div className="mx-auto grid max-w-2xl grid-cols-1 gap-4 px-4 pt-4">
        <Link to={`/enfant/${childId}`} className="w-fit rounded-full bg-white-warm/80 px-3 py-1.5 text-kid-sm font-bold">
          ← Ma page
        </Link>

        <section className="overflow-hidden rounded-[var(--radius-card)] border-2 border-ink" style={{ background: fondDuStudio(reglages.apparence.fond) }}>
          <Suspense fallback={<div style={{ height: 360 }} />}>
            <Avatar3D equipement={calcul.porte} energie={calcul.energie} apparence={reglages.apparence} hauteur={360} />
          </Suspense>
          <p className={'pb-2 text-center text-[0.75rem] font-bold ' + (reglages.apparence.fond !== 'clair' ? 'text-white/80' : 'text-ink-2')}>
            Fais-le tourner du doigt · touche-le pour qu’il saute, salue ou tourne
          </p>
        </section>

        <section className="grid gap-3 rounded-[var(--radius-card)] border border-line bg-white-warm p-4">
          <JaugeNiveau niveau={calcul.niveau} />
          <JaugeEnergie energie={calcul.energie} joursSans={Number.isFinite(sans) ? sans : 0} />
        </section>

        <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-4">
          <h2 className="text-kid-sm font-black">Son allure</h2>
          {(() => {
            const changer = (morceau: Partial<Apparence>) =>
              setReglages({ ...reglages, apparence: { ...reglages.apparence, ...morceau } });
            const ap = reglages.apparence;
            const Pastilles = ({ titre, couleurs, valeur, cle }: { titre: string; couleurs: string[]; valeur: string; cle: keyof Apparence }) => (
              <>
                <p className="mt-3 text-[0.75rem] font-black text-muted">{titre}</p>
                <div className="mt-1 flex flex-wrap gap-2">
                  {couleurs.map((c) => (
                    <button
                      key={c}
                      type="button"
                      aria-label={titre}
                      onClick={() => changer({ [cle]: c } as Partial<Apparence>)}
                      className={'h-9 w-9 rounded-full border-4 ' + (valeur === c ? 'border-ink' : 'border-white shadow')}
                      style={{ background: c }}
                    />
                  ))}
                </div>
              </>
            );
            const Choix = <T extends string>({ titre, options, valeur, onChoix }: {
              titre: string; options: Array<{ cle: T; nom: string }>; valeur: T; onChoix: (v: T) => void;
            }) => (
              <>
                <p className="mt-3 text-[0.75rem] font-black text-muted">{titre}</p>
                <div className="mt-1 flex flex-wrap gap-1.5">
                  {options.map((o) => (
                    <button
                      key={o.cle}
                      type="button"
                      onClick={() => onChoix(o.cle)}
                      className={
                        'rounded-full border-2 px-3 py-1 text-kid-xs font-black ' +
                        (valeur === o.cle ? 'border-ink bg-ink text-white-warm' : 'border-line bg-white-warm')
                      }
                    >
                      {o.nom}
                    </button>
                  ))}
                </div>
              </>
            );
            return (
              <>
                <Choix titre="COIFFURE" options={COIFFURES} valeur={ap.coiffure} onChoix={(v) => changer({ coiffure: v })} />
                <Pastilles titre="CHEVEUX" couleurs={CHEVEUX} valeur={ap.cheveux} cle="cheveux" />
                <Pastilles titre="PEAU" couleurs={PEAUX} valeur={ap.peau} cle="peau" />
                <Pastilles titre="CHEMISE (sans tenue gagnée)" couleurs={HAUTS} valeur={ap.haut} cle="haut" />
                <Pastilles titre="PANTALON" couleurs={BAS} valeur={ap.bas} cle="bas" />
                <Choix titre="EXPRESSION" options={EXPRESSIONS} valeur={ap.expression} onChoix={(v) => changer({ expression: v })} />
                <Choix titre="STUDIO" options={FONDS} valeur={ap.fond} onChoix={(v) => changer({ fond: v })} />
              </>
            );
          })()}
        </section>

        <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-4">
          <div className="flex items-baseline justify-between">
            <h2 className="text-kid-sm font-black">Ses objets</h2>
            <span className="text-kid-xs font-bold text-muted">
              {gagnes} sur {calcul.objets.length}
            </span>
          </div>
          {PLACES.map((pl) => {
            const siens = calcul.objets.filter((o) => o.emplacement === pl.cle);
            return (
              <div key={pl.cle} className="mt-3">
                <p className="text-[0.75rem] font-black uppercase tracking-wide text-muted">{pl.nom}</p>
                {pl.cle === 'aura' ? (
                  <p className="text-[0.72rem] font-bold text-ink-2">
                    Ils disparaissent après 7 jours sans travail. Ils se regagnent.
                  </p>
                ) : null}
                <ul className="mt-1 grid grid-cols-2 gap-2">
                  {siens.map((o) => (
                    <CarteObjet key={o.id} o={o} porte={calcul.porte[o.emplacement]?.id === o.id} onPorter={() => porter(o)} />
                  ))}
                </ul>
              </div>
            );
          })}
        </section>

        <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-4">
          <h2 className="text-kid-sm font-black">L’échelle des niveaux</h2>
          <ol className="mt-2 grid gap-1.5">
            {[...NIVEAUX].reverse().map((n) => {
              const atteint = calcul.niveau.actuel.rang >= n.rang;
              const ici = calcul.niveau.actuel.rang === n.rang;
              return (
                <li
                  key={n.rang}
                  className={
                    'flex items-center justify-between gap-2 rounded-xl px-3 py-2 ' +
                    (ici ? 'bg-gold/40 ring-2 ring-ink' : atteint ? 'bg-leaf/15' : 'bg-paper')
                  }
                >
                  <div className="min-w-0">
                    <p className={'text-kid-sm font-black ' + (n.rang === 8 ? 'text-clay-dark' : '')}>
                      {atteint ? '✓ ' : '🔒 '}
                      {n.rang}. {n.nom}
                      {n.rang === 8 ? ' 👑' : ''}
                    </p>
                    {n.exige ? (
                      <p className="text-[0.72rem] font-bold leading-tight text-ink-2">Il faut aussi : {n.exige.texte}</p>
                    ) : null}
                  </div>
                  <span className="shrink-0 text-kid-xs font-black tabular-nums text-muted">{n.seuil} pts</span>
                </li>
              );
            })}
          </ol>
        </section>
      </div>
    </main>
  );
}
