import { supabase } from './supabase';
import type { ItemRow, NotionRow } from '../types/db';

/**
 * La mission du jour.
 *
 * Trois règles, dans cet ordre :
 *
 * 1. Les notions dues reviennent d'abord. C'est le calendrier de révision
 *    espacée qui décide, pas le dernier score.
 * 2. Une seule question par notion. Enchaîner cinq questions sur la même
 *    chose fatigue sans rien consolider.
 * 3. Chaque question est posée au niveau de maîtrise de l'enfant pour cette
 *    notion, et à défaut au niveau disponible le plus proche en dessous.
 *
 * On s'arrête à cinq : c'est la taille d'une séance qu'un enfant de primaire
 * termine sans se décourager.
 */

export const TAILLE_MISSION = 5;

export type NotionAvecItems = NotionRow & { items: ItemRow[] };

export type EtapeMission = {
  notion: NotionAvecItems;
  item: ItemRow;
  niveau: number;
  due: boolean;
};

/**
 * L'item posé à l'enfant pour cette notion.
 *
 * Au niveau de l'enfant ou en dessous, on prend le plus haut disponible : il
 * est prêt pour celui-là. Si la notion n'a aucun item à sa portée, on prend le
 * plus bas qui existe, jamais le plus haut — lui servir un défi avant même
 * l'entraînement n'apprend rien et décourage.
 */
export function choisirItem(items: ItemRow[], niveau: number): ItemRow | null {
  if (items.length === 0) return null;
  const aSaPortee = items.filter((i) => i.level <= niveau);
  const niveauVise =
    aSaPortee.length > 0
      ? Math.max(...aSaPortee.map((i) => i.level))
      : Math.min(...items.map((i) => i.level));
  const auNiveau = items.filter((i) => i.level === niveauVise);
  return auNiveau[Math.floor(Math.random() * auNiveau.length)];
}

export async function construireMission(childId: string, lessonId: string) {
  const { data, error } = await supabase
    .from('notions')
    .select(
      'id, lesson_id, kind, statement, sort_order, illustration, parent_id, status, created_at, ' +
        'items(id, notion_id, kind, level, payload, answer, explain, parent_id, status, created_at)',
    )
    .eq('lesson_id', lessonId)
    .eq('status', 'approved')
    .order('sort_order');
  if (error) throw error;

  const notions = (data ?? []) as unknown as NotionAvecItems[];
  if (notions.length === 0) return [];

  const { data: maitrise } = await supabase
    .from('mastery')
    .select('notion_id, level, next_review')
    .eq('child_id', childId)
    .in(
      'notion_id',
      notions.map((n) => n.id),
    );

  const parNotion = new Map<string, { level: number; next_review: string | null }>();
  for (const m of maitrise ?? []) {
    parNotion.set(m.notion_id, { level: m.level, next_review: m.next_review });
  }

  const aujourdhui = new Date().toISOString().slice(0, 10);

  const etapes: EtapeMission[] = [];
  for (const notion of notions) {
    const suivi = parNotion.get(notion.id);
    const niveau = suivi?.level ?? 1;
    // Jamais révisée, ou dont la date est arrivée.
    const due = !suivi?.next_review || suivi.next_review <= aujourdhui;
    const jouables = (notion.items ?? []).filter((i) => i.status === 'approved');
    const item = choisirItem(jouables, niveau);
    if (item) etapes.push({ notion, item, niveau, due });
  }

  // Les notions dues passent devant ; le reste comble la séance.
  etapes.sort((a, b) => Number(b.due) - Number(a.due));
  return etapes.slice(0, TAILLE_MISSION);
}

export async function totalPoints(childId: string): Promise<number> {
  const { data, error } = await supabase.from('rewards').select('value').eq('child_id', childId);
  if (error) throw error;
  return (data ?? []).reduce((somme, r) => somme + (r.value ?? 0), 0);
}
