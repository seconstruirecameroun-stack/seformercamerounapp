import { Suspense, lazy } from 'react';
import { Link, useParams } from 'react-router-dom';
import { ErrorNote, Loading } from '../../components/ui';
import { usePersonnage, jourUTC } from '../../components/avatar/personnage';
import { JaugeEnergie, JaugeNiveau } from '../../components/avatar/Jauges';
import { HAUTS, PEAUX } from '../../components/avatar/apparence';
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
  { cle: 'corps', nom: 'Tenue' },
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

        <section className="overflow-hidden rounded-[var(--radius-card)] border-2 border-ink bg-[radial-gradient(circle_at_50%_35%,#fff8e6_0%,#ffe2b0_55%,#f6c27a_100%)]">
          <Suspense fallback={<div style={{ height: 360 }} />}>
            <Avatar3D equipement={calcul.porte} energie={calcul.energie} apparence={reglages.apparence} hauteur={360} />
          </Suspense>
          <p className="pb-2 text-center text-[0.75rem] font-bold text-ink-2">
            Fais-le tourner du doigt · touche-le pour qu’il saute, salue ou tourne
          </p>
        </section>

        <section className="grid gap-3 rounded-[var(--radius-card)] border border-line bg-white-warm p-4">
          <JaugeNiveau niveau={calcul.niveau} />
          <JaugeEnergie energie={calcul.energie} joursSans={Number.isFinite(sans) ? sans : 0} />
        </section>

        <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-4">
          <h2 className="text-kid-sm font-black">Son allure</h2>
          <p className="mt-2 text-[0.75rem] font-black text-muted">PEAU</p>
          <div className="mt-1 flex gap-2">
            {PEAUX.map((c) => (
              <button
                key={c}
                type="button"
                aria-label="Couleur de peau"
                onClick={() => setReglages({ ...reglages, apparence: { ...reglages.apparence, peau: c } })}
                className={'h-9 w-9 rounded-full border-4 ' + (reglages.apparence.peau === c ? 'border-ink' : 'border-white')}
                style={{ background: c }}
              />
            ))}
          </div>
          <p className="mt-2 text-[0.75rem] font-black text-muted">HAUT (quand il ne porte pas de tenue gagnée)</p>
          <div className="mt-1 flex flex-wrap gap-2">
            {HAUTS.map((c) => (
              <button
                key={c}
                type="button"
                aria-label="Couleur du haut"
                onClick={() => setReglages({ ...reglages, apparence: { ...reglages.apparence, haut: c } })}
                className={'h-9 w-9 rounded-xl border-4 ' + (reglages.apparence.haut === c ? 'border-ink' : 'border-white')}
                style={{ background: c }}
              />
            ))}
          </div>
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
