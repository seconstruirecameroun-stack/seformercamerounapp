import { supabase } from './supabase';
import type { ItemRow } from '../types/db';

/**
 * La composition : l'épreuve que le parent annonce.
 *
 * Au Cameroun, composer, c'est passer l'épreuve de fin de séquence sur les
 * leçons annoncées par le maître. L'app savait faire réviser une leçon et la
 * valider ; elle ne savait pas faire composer SUR PLUSIEURS LEÇONS À LA
 * FOIS, qui est pourtant la forme que prend l'évaluation à l'école.
 *
 * Ce qu'une composition n'est pas : une manche de validation. La manche
 * exige le sans-faute sur une leçon et certifie au parent qu'elle est sue.
 * La composition, elle, porte sur plusieurs leçons, accepte les fautes, et
 * rend une NOTE. Les deux cohabitent sans se gêner.
 *
 * Ce que le père a tranché, et qui se lit dans tout ce fichier : les
 * réponses d'une composition comptent comme les autres. Étoiles, étapes,
 * images — et une faute sur une leçon déjà validée la remet à valider,
 * exactement comme en révision. C'est le choix exigeant, et le seul qui
 * garde vraie l'affirmation faite au parent.
 */

export type CompositionRow = {
  id: string;
  parent_id: string;
  child_id: string;
  titre: string;
  lessons: string[];
  questions: string[];
  commencee_le: string | null;
  finie_le: string | null;
  justes: number | null;
  created_at: string;
};

/** Le strict nécessaire pour tirer : des leçons, des notions, des questions. */
export type NotionPourTirage = { id: string; items: Array<{ id: string; level: number }> };
export type LeconPourTirage = { id: string; notions: NotionPourTirage[] };

/** Les tailles que le parent peut demander. */
export const TAILLES = [10, 20, 30] as const;

/**
 * Les notions de toutes les leçons, entrelacées.
 *
 * Leçon A, leçon B, leçon C, puis la deuxième notion de A, et ainsi de
 * suite. Prendre les leçons l'une après l'autre donnerait une composition
 * qui épuise la première avant de toucher la deuxième — et un enfant qui
 * abandonne en route n'aurait composé que sur une leçon.
 */
function entrelacer(lecons: LeconPourTirage[]): Array<{ lecon: string; notion: NotionPourTirage }> {
  const sortie: Array<{ lecon: string; notion: NotionPourTirage }> = [];
  const profondeur = Math.max(0, ...lecons.map((l) => l.notions.length));
  for (let i = 0; i < profondeur; i++) {
    for (const l of lecons) {
      const n = l.notions[i];
      if (n) sortie.push({ lecon: l.id, notion: n });
    }
  }
  return sortie;
}

/**
 * Une question de cette notion, à l'étape demandée si elle existe.
 *
 * À défaut, la plus proche : une notion qui n'a pas de question de Défi ne
 * doit pas faire sauter son tour à la leçon entière.
 */
function choisir(
  notion: NotionPourTirage,
  niveau: number,
  pris: Set<string>,
): string | null {
  const libres = notion.items.filter((i) => !pris.has(i.id));
  if (libres.length === 0) return null;
  const tries = [...libres].sort(
    (a, b) => Math.abs(a.level - niveau) - Math.abs(b.level - niveau) || a.id.localeCompare(b.id),
  );
  return tries[0].id;
}

/**
 * Les questions de la composition, tirées des leçons annoncées.
 *
 * Trois règles, et elles sont dans cet ordre de priorité :
 *
 *   on alterne les LEÇONS, pour que la composition porte sur tout ce que le
 *   parent a coché et non sur la première leçon seulement ;
 *
 *   on alterne les NOTIONS, et on ne revient sur une notion déjà
 *   interrogée que lorsque toutes les autres l'ont été. Deux questions sur
 *   la même notion quand une autre n'a rien eu, c'est une épreuve qui
 *   mesure mal ;
 *
 *   on fait tourner les QUATRE ÉTAPES, pour que l'épreuve aille du
 *   reconnaître au transférer, comme une vraie composition.
 *
 * Le tirage est figé à la création : il est écrit dans la ligne, et
 * l'enfant retrouvera les mêmes questions s'il revient.
 */
export function tirerQuestions(lecons: LeconPourTirage[], combien: number): string[] {
  const notions = entrelacer(lecons).filter((n) => n.notion.items.length > 0);
  if (notions.length === 0 || combien <= 0) return [];

  const pris = new Set<string>();
  const sortie: string[] = [];

  for (let tour = 0; sortie.length < combien; tour++) {
    let ajoutes = 0;
    for (const { notion } of notions) {
      if (sortie.length >= combien) break;
      // L'étape tourne avec le RANG de la question posée : la première est
      // de Découverte, la deuxième d'Entraînement, et ainsi de suite.
      const niveau = 1 + (sortie.length % 4);
      const choix = choisir(notion, niveau, pris);
      if (choix) {
        pris.add(choix);
        sortie.push(choix);
        ajoutes += 1;
      }
    }
    // Plus rien à prendre : la composition sera plus courte que demandée,
    // et c'est honnête — mieux vaut quinze questions que quinze questions
    // dont cinq répétées.
    if (ajoutes === 0) break;
  }

  return sortie;
}

/** La note se lit en un coup d'œil : juste sur posées. */
export function note(justes: number, posees: number): string {
  return justes + ' / ' + posees;
}

/**
 * Où en est une composition.
 *
 * Trois états, et aucun n'est stocké comme tel : ils se lisent sur les deux
 * dates. Une colonne « statut » tenue à la main finirait par mentir, comme
 * la colonne « validée » qu'on a refusée pour la manche.
 */
export type EtatComposition = 'a_faire' | 'en_cours' | 'finie';

export function etatDeLaComposition(c: CompositionRow): EtatComposition {
  if (c.finie_le) return 'finie';
  if (c.commencee_le) return 'en_cours';
  return 'a_faire';
}

/** Les compositions d'un enfant, la plus récente d'abord. */
export async function compositionsDeLEnfant(childId: string): Promise<CompositionRow[]> {
  const { data, error } = await supabase
    .from('compositions')
    .select('*')
    .eq('child_id', childId)
    .order('created_at', { ascending: false });
  if (error) throw error;
  return (data ?? []) as CompositionRow[];
}

export async function lireComposition(id: string): Promise<CompositionRow | null> {
  const { data, error } = await supabase.from('compositions').select('*').eq('id', id).single();
  if (error) throw error;
  return (data ?? null) as CompositionRow | null;
}

/** Les questions d'une composition, dans l'ordre où elles ont été tirées. */
export async function questionsDeLaComposition(c: CompositionRow): Promise<ItemRow[]> {
  if (c.questions.length === 0) return [];
  const { data, error } = await supabase.from('items').select('*').in('id', c.questions);
  if (error) throw error;
  const par = new Map((data as ItemRow[]).map((i) => [i.id, i]));
  // L'ordre du tirage fait foi : PostgREST ne promet rien sur l'ordre d'un
  // `in`, et une composition dont les questions changeraient d'ordre entre
  // deux ouvertures ne serait plus la même épreuve.
  return c.questions.map((id) => par.get(id)).filter((i): i is ItemRow => Boolean(i));
}

export async function creerComposition(params: {
  parentId: string;
  childId: string;
  titre: string;
  lessons: string[];
  questions: string[];
}): Promise<CompositionRow> {
  const { data, error } = await supabase
    .from('compositions')
    .insert({
      parent_id: params.parentId,
      child_id: params.childId,
      titre: params.titre,
      lessons: params.lessons,
      questions: params.questions,
    })
    .select('*')
    .single();
  if (error) throw error;
  return data as CompositionRow;
}

export async function commencerComposition(id: string): Promise<void> {
  const { error } = await supabase
    .from('compositions')
    .update({ commencee_le: new Date().toISOString() })
    .eq('id', id)
    .is('commencee_le', null);
  if (error) throw error;
}

export async function finirComposition(id: string, justes: number): Promise<void> {
  const { error } = await supabase
    .from('compositions')
    .update({ finie_le: new Date().toISOString(), justes })
    .eq('id', id)
    .is('finie_le', null);
  if (error) throw error;
}

export async function supprimerComposition(id: string): Promise<void> {
  const { error } = await supabase.from('compositions').delete().eq('id', id);
  if (error) throw error;
}
