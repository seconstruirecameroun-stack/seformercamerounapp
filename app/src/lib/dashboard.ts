import { supabase } from './supabase';

/**
 * Ce que l'enfant voit en arrivant.
 *
 * Tout est déduit du journal des tentatives et de la maîtrise : rien n'est
 * stocké en double. Si la formule de progression change un jour, ce tableau
 * change avec elle sans migration.
 */

/** Une notion est « acquise » à partir du niveau 3, celui où l'on produit. */
export const NIVEAU_ACQUIS = 3;

export type Autocollant = {
  notionId: string;
  statement: string;
  illustration: string | null;
  acquis: boolean;
};

export type LeconResume = {
  id: string;
  title: string;
  illustration: string | null;
  matiere: string | null;
  notions: number;
  acquises: number;
  dues: number;
};

export type TableauDeBord = {
  lecons: LeconResume[];
  duesTotal: number;
  points: number;
  serie: number;
  /** Jours où l'enfant a répondu, du plus récent au plus ancien. */
  jours: string[];
  autocollants: Autocollant[];
  prochaineLecon: string | null;
};

/**
 * La série, en jours consécutifs de révision.
 *
 * Elle se calcule à partir des jours où l'enfant a réellement répondu. Une
 * série qui compterait les jours d'ouverture de l'app, sans réponse, serait
 * une flatterie : elle doit récompenser l'effort.
 *
 * Le jour en cours ne casse rien tant qu'il n'est pas fini : on part
 * d'aujourd'hui, et à défaut d'hier.
 */
export function calculerSerie(jours: string[]): number {
  if (jours.length === 0) return 0;
  const uniques = [...new Set(jours)].sort().reverse();

  const jour = (decalage: number) => {
    const d = new Date();
    d.setDate(d.getDate() - decalage);
    return d.toISOString().slice(0, 10);
  };

  const depart = uniques[0] === jour(0) ? 0 : uniques[0] === jour(1) ? 1 : -1;
  if (depart === -1) return 0;

  let serie = 0;
  for (let i = depart; ; i++) {
    if (uniques.includes(jour(i))) serie += 1;
    else break;
  }
  return serie;
}

export async function chargerTableauDeBord(childId: string): Promise<TableauDeBord> {
  const [lecons, maitrise, recompenses, tentatives] = await Promise.all([
    supabase
      .from('lessons')
      .select('id, title, illustration, subjects(label), notions(id, statement, illustration, status)')
      .eq('status', 'approved')
      .order('sort_order'),
    supabase.from('mastery').select('notion_id, level, next_review').eq('child_id', childId),
    supabase.from('rewards').select('value').eq('child_id', childId),
    supabase
      .from('attempts')
      .select('created_at')
      .eq('child_id', childId)
      .order('created_at', { ascending: false })
      .limit(400),
  ]);

  if (lecons.error) throw lecons.error;

  const suivi = new Map<string, { level: number; next_review: string | null }>();
  for (const m of maitrise.data ?? []) {
    suivi.set(m.notion_id, { level: m.level, next_review: m.next_review });
  }

  const aujourdhui = new Date().toISOString().slice(0, 10);
  const brutes = (lecons.data ?? []) as unknown as Array<{
    id: string;
    title: string;
    illustration: string | null;
    subjects: { label: string } | null;
    notions: Array<{ id: string; statement: string; illustration: string | null; status: string }>;
  }>;

  const resumes: LeconResume[] = [];
  const autocollants: Autocollant[] = [];

  for (const lecon of brutes) {
    const notions = lecon.notions.filter((n) => n.status === 'approved');
    let acquises = 0;
    let dues = 0;

    for (const notion of notions) {
      const m = suivi.get(notion.id);
      const acquis = (m?.level ?? 1) >= NIVEAU_ACQUIS;
      if (acquis) acquises += 1;
      if (!m?.next_review || m.next_review <= aujourdhui) dues += 1;
      autocollants.push({
        notionId: notion.id,
        statement: notion.statement,
        illustration: notion.illustration,
        acquis,
      });
    }

    resumes.push({
      id: lecon.id,
      title: lecon.title,
      illustration: lecon.illustration,
      matiere: lecon.subjects?.label ?? null,
      notions: notions.length,
      acquises,
      dues,
    });
  }

  // La leçon proposée en premier est celle qui a le plus de notions dues :
  // c'est là que la révision sert le plus.
  const prochaine = [...resumes].sort((a, b) => b.dues - a.dues)[0];

  const jours = [...new Set((tentatives.data ?? []).map((t) => String(t.created_at).slice(0, 10)))];

  return {
    lecons: resumes,
    duesTotal: resumes.reduce((n, l) => n + l.dues, 0),
    points: (recompenses.data ?? []).reduce((somme, r) => somme + (r.value ?? 0), 0),
    serie: calculerSerie(jours),
    jours,
    autocollants,
    prochaineLecon: prochaine && prochaine.dues > 0 ? prochaine.id : (resumes[0]?.id ?? null),
  };
}
