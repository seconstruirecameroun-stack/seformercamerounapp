import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { chargerTableauDeBord } from '../../lib/dashboard';
import { compositionsDeLEnfant } from '../../lib/composition';
import { bilanDe } from '../../lib/bilanAvatar';
import { energie, equipement, niveauDe, objetsDe, type Emplacement } from '../../lib/avatar';
import { APPARENCE_DEFAUT, type Apparence } from './apparence';

/**
 * Le personnage d'un enfant : son travail, ses objets, son niveau, son
 * énergie, et ce qu'il a choisi de porter.
 *
 * Le travail vient des mêmes requêtes que sa page d'accueil, sous les mêmes
 * clés : rien n'est relu deux fois, et le personnage ne peut pas dire autre
 * chose que les étapes affichées.
 *
 * Ses réglages — la couleur de sa peau, celle de son haut, l'objet porté à
 * chaque place — sont des choix de goût, pas du travail : ils se gardent
 * sur l'appareil. S'ils se perdent, le personnage porte simplement ses plus
 * beaux objets.
 */

export type Reglages = {
  apparence: Apparence;
  choix: Partial<Record<Emplacement, string | null>>;
};

const cle = (childId: string) => 'personnage-' + childId;

function lire(childId: string): Reglages {
  try {
    const brut = JSON.parse(localStorage.getItem(cle(childId)) ?? 'null') as Reglages | null;
    if (brut?.apparence) return { apparence: { ...APPARENCE_DEFAUT, ...brut.apparence }, choix: brut.choix ?? {} };
  } catch {
    // navigation privée : les réglages par défaut
  }
  return { apparence: APPARENCE_DEFAUT, choix: {} };
}

export function jourUTC(d = new Date()): string {
  return d.toISOString().slice(0, 10);
}

export function usePersonnage(childId: string | undefined) {
  const bord = useQuery({
    queryKey: ['tableau', childId],
    enabled: Boolean(childId),
    queryFn: () => chargerTableauDeBord(childId!),
  });
  const compositions = useQuery({
    queryKey: ['compositions', childId],
    enabled: Boolean(childId),
    queryFn: () => compositionsDeLEnfant(childId!),
  });
  const [reglages, setReglagesBrut] = useState<Reglages>(() =>
    childId ? lire(childId) : { apparence: APPARENCE_DEFAUT, choix: {} },
  );

  const setReglages = (r: Reglages) => {
    setReglagesBrut(r);
    try {
      if (childId) localStorage.setItem(cle(childId), JSON.stringify(r));
    } catch {
      // rien : le choix vaut pour cette visite
    }
  };

  const aujourdhui = jourUTC();
  const calcul = useMemo(() => {
    if (!bord.data) return null;
    const bilan = bilanDe(bord.data, compositions.data ?? [], aujourdhui);
    const objets = objetsDe(bilan, aujourdhui);
    return {
      bilan,
      objets,
      porte: equipement(objets, reglages.choix),
      niveau: niveauDe(bilan),
      energie: energie(bilan.dernierJour, aujourdhui),
    };
  }, [bord.data, compositions.data, reglages.choix, aujourdhui]);

  return { chargement: bord.isLoading, erreur: bord.error, calcul, reglages, setReglages };
}
