import { supabase } from './supabase';

/**
 * Le duel de la semaine, entre frères.
 *
 * C'est le ressort le plus puissant du lot, et le plus délicat : deux enfants
 * de classes différentes ne peuvent pas être comparés sur ce qu'ils savent.
 * Le duel ne porte donc pas sur le savoir mais sur l'effort de la semaine —
 * les questions réussies, remises à zéro chaque lundi. Un CE1 qui travaille
 * plus bat un CM1 qui travaille moins, et c'est tout l'intérêt.
 *
 * On compte des questions et non des étoiles, parce qu'une question du Défi
 * vaut quatre fois une question de Découverte : l'aîné, qui a fini ses
 * leçons et rejoue au chronomètre, aurait creusé un écart que le cadet ne
 * pouvait pas combler en travaillant. Une question reste une question, quelle
 * que soit l'étape — c'est la seule mesure qui compare vraiment l'effort.
 *
 * La remise à zéro hebdomadaire est la deuxième protection : celui qui perd
 * ne perd que sept jours, jamais son avance cumulée. Un classement à vie
 * décourage définitivement le second.
 *
 * UNE EXCEPTION, ET UNE SEULE : la manche gagnée.
 *
 * Valider une leçon demande le sans-faute sur toutes ses questions, et c'est
 * le seul acte du jeu qui vaille autant pour un CE1 que pour un CM1 — la
 * difficulté est celle de SA leçon à lui. Elle compte donc pour vingt
 * questions, le même nombre pour les deux, quel que soit leur niveau.
 *
 * Le bonus est FIXE, et c'est ce qui le rend acceptable. Le payer au prorata
 * de la longueur de la manche rouvrirait exactement l'écart que la règle des
 * questions évite : l'aîné, dont les leçons sont plus longues, gagnerait
 * davantage à chaque validation sans travailler davantage.
 *
 * Tout se déduit du journal des tentatives et des manches, comme le reste.
 */

/** Ce que vaut une manche gagnée dans le duel, en questions. */
export const BONUS_MANCHE_DUEL = 20;

export type Concurrent = {
  childId: string;
  prenom: string;
  avatar: string | null;
  /** Le total qui classe : questions réussies plus le bonus des manches. */
  reussites: number;
  /** Questions réussies depuis lundi, sans le bonus. */
  questions: number;
  /** Manches gagnées depuis lundi. */
  manches: number;
};

export type Duel = {
  concurrents: Concurrent[];
  /** L'écart avec celui qui mène, pour l'enfant qui regarde. */
  ecart: number;
  enTete: boolean;
  exAequo: boolean;
  /** Jours restants avant la remise à zéro, dimanche inclus. */
  joursRestants: number;
  /** Le gagnant de la semaine passée, s'il y en a eu un. */
  gagnantPasse: { prenom: string; reussites: number } | null;
};

/** Le lundi de la semaine en cours, en date ISO. Le décalage recule d'une semaine. */
export function lundi(decalageSemaines = 0): string {
  const d = new Date();
  // getDay() rend 0 pour dimanche : au Cameroun comme en France, la semaine
  // scolaire commence le lundi, et le dimanche clôt la précédente.
  const depuisLundi = (d.getDay() + 6) % 7;
  d.setDate(d.getDate() - depuisLundi + decalageSemaines * 7);
  return d.toISOString().slice(0, 10);
}

export async function chargerDuel(childId: string): Promise<Duel | null> {
  const [enfants, justes, gagnees] = await Promise.all([
    supabase.from('children').select('id, first_name, avatar'),
    supabase
      .from('attempts')
      .select('child_id, created_at')
      .eq('correct', true)
      .gte('created_at', lundi(-1)),
    supabase
      .from('manches')
      .select('child_id, created_at')
      .eq('reussie', true)
      .gte('created_at', lundi(-1)),
  ]);
  if (enfants.error) throw enfants.error;
  if (justes.error) throw justes.error;
  if (gagnees.error) throw gagnees.error;

  const liste = (enfants.data ?? []) as Array<{
    id: string;
    first_name: string;
    avatar: string | null;
  }>;
  // Un enfant seul n'a personne à défier : la carte n'a alors pas lieu d'être.
  if (liste.length < 2) return null;

  const debut = lundi();
  const cette = new Map<string, number>();
  const passee = new Map<string, number>();
  const manchesCette = new Map<string, number>();
  for (const t of justes.data ?? []) {
    const jour = String(t.created_at).slice(0, 10);
    const panier = jour >= debut ? cette : passee;
    panier.set(t.child_id, (panier.get(t.child_id) ?? 0) + 1);
  }
  // Les manches de la semaine passée entrent dans son total, comme les
  // questions : le gagnant annoncé doit être celui qui a vraiment gagné.
  for (const m of gagnees.data ?? []) {
    const jour = String(m.created_at).slice(0, 10);
    if (jour >= debut) {
      manchesCette.set(m.child_id, (manchesCette.get(m.child_id) ?? 0) + 1);
    } else {
      passee.set(m.child_id, (passee.get(m.child_id) ?? 0) + BONUS_MANCHE_DUEL);
    }
  }

  const concurrents: Concurrent[] = liste
    .map((e) => {
      const questions = cette.get(e.id) ?? 0;
      const manches = manchesCette.get(e.id) ?? 0;
      return {
        childId: e.id,
        prenom: e.first_name,
        avatar: e.avatar,
        questions,
        manches,
        reussites: questions + manches * BONUS_MANCHE_DUEL,
      };
    })
    .sort((a, b) => b.reussites - a.reussites || a.prenom.localeCompare(b.prenom));

  const moi = concurrents.find((c) => c.childId === childId);
  const tete = concurrents[0];
  const ecart = moi ? tete.reussites - moi.reussites : 0;

  // Dimanche compte encore : la semaine ne se termine qu'à la fin du
  // septième jour, et c'est souvent le jour où l'on rattrape.
  const aujourdhui = new Date();
  const joursRestants = 7 - ((aujourdhui.getDay() + 6) % 7);

  const meilleurPasse = [...passee.entries()].sort((a, b) => b[1] - a[1])[0];
  const gagnantPasse =
    meilleurPasse && meilleurPasse[1] > 0
      ? {
          prenom: liste.find((e) => e.id === meilleurPasse[0])?.first_name ?? '',
          reussites: meilleurPasse[1],
        }
      : null;

  return {
    concurrents,
    ecart,
    enTete: Boolean(moi && moi.reussites === tete.reussites && tete.reussites > 0),
    exAequo: concurrents.length > 1 && concurrents[0].reussites === concurrents[1].reussites,
    joursRestants,
    gagnantPasse,
  };
}
