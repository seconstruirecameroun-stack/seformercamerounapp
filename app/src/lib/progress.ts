import { supabase } from './supabase';
import type { ItemRow, MasteryRow } from '../types/db';

/**
 * Les règles de progression du document de structure, en un seul endroit.
 *
 *   3 bonnes réponses d’affilée  → niveau + 1
 *   2 erreurs d’affilée          → niveau − 1, et l’interface propose une
 *                                  autre explication
 *
 * streak est signé : positif pour les réussites consécutives, négatif pour les
 * erreurs. Cela évite une seconde colonne et rend les deux règles symétriques.
 */

/** Intervalles de révision espacée, en jours, indexés par niveau 1 à 4. */
const REVIEW_DAYS = [1, 3, 7, 21];

export const POINTS_PER_LEVEL = 10;
export const POINTS_LEVEL_UP = 50;

export type ProgressOutcome = {
  level: number;
  previousLevel: number;
  score: number;
  leveledUp: boolean;
  leveledDown: boolean;
  points: number;
};

function nextReviewDate(level: number): string {
  const days = REVIEW_DAYS[Math.min(Math.max(level, 1), 4) - 1];
  const date = new Date();
  date.setDate(date.getDate() + days);
  return date.toISOString().slice(0, 10);
}

export function computeNext(
  current: Pick<MasteryRow, 'level' | 'score' | 'streak'>,
  correct: boolean,
): { level: number; score: number; streak: number; leveledUp: boolean; leveledDown: boolean } {
  let { level, score, streak } = current;
  const previousLevel = level;

  if (correct) {
    streak = streak > 0 ? streak + 1 : 1;
    score = Math.min(100, score + POINTS_PER_LEVEL * level);
    if (streak >= 3 && level < 4) {
      level += 1;
      streak = 0;
    }
  } else {
    streak = streak < 0 ? streak - 1 : -1;
    score = Math.max(0, score - 5);
    if (streak <= -2 && level > 1) {
      level -= 1;
      streak = 0;
    }
  }

  return {
    level,
    score,
    streak,
    leveledUp: level > previousLevel,
    leveledDown: level < previousLevel,
  };
}

/**
 * Enregistre une tentative et met à jour la maîtrise.
 *
 * attempts est un journal en ajout seul : on y écrit toujours, même quand la
 * mise à jour de mastery échoue. C’est la source de vérité, mastery n’en est
 * que la vue agrégée.
 */
export async function recordAttempt(params: {
  parentId: string;
  childId: string;
  item: Pick<ItemRow, 'id' | 'notion_id'>;
  answer: unknown;
  correct: boolean;
  durationMs?: number;
}): Promise<ProgressOutcome> {
  const { parentId, childId, item, answer, correct, durationMs } = params;

  const { error: attemptError } = await supabase.from('attempts').insert({
    parent_id: parentId,
    child_id: childId,
    item_id: item.id,
    answer: answer as never,
    correct,
    duration_ms: durationMs ?? null,
  });
  if (attemptError) throw attemptError;

  const { data: existing } = await supabase
    .from('mastery')
    .select('level, score, streak')
    .eq('child_id', childId)
    .eq('notion_id', item.notion_id)
    .maybeSingle();

  const current = existing ?? { level: 1, score: 0, streak: 0 };
  const next = computeNext(current, correct);

  const { error: masteryError } = await supabase.from('mastery').upsert(
    {
      child_id: childId,
      notion_id: item.notion_id,
      parent_id: parentId,
      level: next.level,
      score: next.score,
      streak: next.streak,
      next_review: nextReviewDate(next.level),
      updated_at: new Date().toISOString(),
    },
    { onConflict: 'child_id,notion_id' },
  );
  if (masteryError) throw masteryError;

  // Les points récompensent le niveau joué, pas le simple clic : rejouer le
  // niveau 1 en boucle ne rapporte presque rien.
  let points = 0;
  if (correct) points += POINTS_PER_LEVEL * current.level;
  if (next.leveledUp) points += POINTS_LEVEL_UP;

  if (points > 0) {
    await supabase.from('rewards').insert({
      parent_id: parentId,
      child_id: childId,
      kind: 'points',
      value: points,
    });
  }

  return {
    level: next.level,
    previousLevel: current.level,
    score: next.score,
    leveledUp: next.leveledUp,
    leveledDown: next.leveledDown,
    points,
  };
}
