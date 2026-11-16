import { Suspense, lazy, useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { joursSansJouer, OBJETS } from '../../lib/avatar';
import DialogueJeu, { momentFort, type Dialogue } from '../jeu/DialogueJeu';
import { JaugeEnergie, JaugeNiveau } from './Jauges';
import { jourUTC, usePersonnage } from './personnage';
import { fondDuStudio } from './apparence';

const Avatar3D = lazy(() => import('./Avatar3D'));

/**
 * Le personnage, sur la page d'accueil de l'enfant : la première chose qu'il
 * voit en arrivant.
 *
 * Il y a son héros en 3D, son niveau, son énergie, et le PROCHAIN objet à
 * gagner — celui dont il est le plus près — pour qu'il sache toujours ce que
 * sa séance va lui rapporter.
 *
 * Quand un objet nouveau est arrivé depuis sa dernière visite, ou qu'il a
 * changé de niveau, Niba le lui annonce.
 */
export default function CartePersonnage({ childId }: { childId: string }) {
  const { calcul, reglages } = usePersonnage(childId);
  const [moment, setMoment] = useState<Dialogue | null>(null);
  const annonce = useRef(false);

  // Ce qui est nouveau depuis la dernière visite, sur cet appareil.
  useEffect(() => {
    if (!calcul || annonce.current) return;
    annonce.current = true;
    const gagnes = calcul.objets.filter((o) => o.gagne).map((o) => o.id);
    const cle = 'personnage-vu-' + childId;
    try {
      const vu = JSON.parse(localStorage.getItem(cle) ?? 'null') as { objets: string[]; niveau: number } | null;
      if (vu) {
        const nouveaux = gagnes.filter((id) => !vu.objets.includes(id));
        if (calcul.niveau.actuel.rang > vu.niveau) {
          setMoment(momentFort('mention', `NIVEAU ${calcul.niveau.actuel.rang} !`, `Te voilà ${calcul.niveau.actuel.nom} !`));
        } else if (nouveaux.length > 0) {
          const o = OBJETS.find((x) => x.id === nouveaux[0]);
          setMoment(momentFort('parfait', 'NOUVEL OBJET !', `${o?.nom ?? ''} : va le voir sur ton personnage !`));
        }
      }
      localStorage.setItem(cle, JSON.stringify({ objets: gagnes, niveau: calcul.niveau.actuel.rang }));
    } catch {
      // navigation privée : pas d'annonce
    }
  }, [calcul, childId]);

  if (!calcul) return null;
  const sans = joursSansJouer(calcul.bilan.dernierJour, jourUTC());

  // Le prochain objet : celui dont il est le plus près, parmi ceux qui manquent.
  const prochain = calcul.objets
    .filter((o) => !o.gagne)
    .map((o) => ({ o, part: o.fait / o.but }))
    .sort((a, b) => b.part - a.part)[0]?.o;

  return (
    <Link
      to={`/enfant/${childId}/personnage`}
      className="tuile relative block overflow-hidden rounded-[var(--radius-card)] border-2 border-ink shadow-[var(--shadow-card)]"
      style={{ background: fondDuStudio(reglages.apparence.fond) }}
    >
      <DialogueJeu dernier={moment} />
      <div className="grid grid-cols-[minmax(0,44%)_minmax(0,1fr)] items-center gap-2">
        <Suspense fallback={<div style={{ height: 210 }} />}>
          <Avatar3D
            equipement={calcul.porte}
            energie={calcul.energie}
            apparence={reglages.apparence}
            hauteur={210}
            compact
          />
        </Suspense>
        <div className="my-2 mr-2 grid gap-2 rounded-2xl bg-white-warm/90 p-2.5">
          <JaugeNiveau niveau={calcul.niveau} />
          <JaugeEnergie energie={calcul.energie} joursSans={Number.isFinite(sans) ? sans : 0} />
          {prochain ? (
            <p className="rounded-xl bg-white-warm/80 px-2 py-1 text-[0.78rem] font-bold leading-tight">
              🎁 Prochain : <span className="font-black">{prochain.nom}</span> — {prochain.condition.toLowerCase()} ({prochain.fait}/{prochain.but})
            </p>
          ) : null}
        </div>
      </div>
    </Link>
  );
}
