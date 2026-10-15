import { supabase } from './supabase';

export const BUCKET = 'cours';

/** 20 Mo, comme la limite posée sur le compartiment. */
export const TAILLE_MAX = 20 * 1024 * 1024;

export const TYPES_ACCEPTES = [
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/heic',
  'application/pdf',
];

/**
 * Le chemin de stockage porte la sécurité : son premier segment est
 * l'identifiant du parent, et les politiques du compartiment le comparent à
 * auth.uid(). Changer cette forme casserait l'isolation entre familles.
 */
export function cheminStockage(parentId: string, batchId: string, page: number, nom: string) {
  const sain = nom
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-zA-Z0-9._-]/g, '-')
    .slice(-60);
  return `${parentId}/${batchId}/${String(page).padStart(2, '0')}-${sain}`;
}

export type FichierRefuse = { nom: string; raison: string };

export function trierFichiers(fichiers: File[]) {
  const acceptes: File[] = [];
  const refuses: FichierRefuse[] = [];
  for (const f of fichiers) {
    if (!TYPES_ACCEPTES.includes(f.type)) {
      refuses.push({ nom: f.name, raison: 'format non pris en charge' });
    } else if (f.size > TAILLE_MAX) {
      refuses.push({ nom: f.name, raison: 'dépasse 20 Mo' });
    } else {
      acceptes.push(f);
    }
  }
  return { acceptes, refuses };
}

/**
 * Trouve une matière dans le catalogue de la classe, ou l'y ajoute.
 *
 * L'emploi du temps de l'école fournit la liste, mais il ne dit pas tout :
 * un cahier peut porter un intitulé qui n'y figure pas. On ne fige donc
 * rien — on rattache la nouvelle matière à la classe, pour qu'elle soit
 * proposée la prochaine fois au lieu d'être réinventée.
 */
export async function matiereDeClasse(
  parentId: string,
  classId: string,
  libelle: string,
): Promise<string> {
  const label = libelle.trim();
  const { data: existante } = await supabase
    .from('subjects')
    .select('id')
    .eq('parent_id', parentId)
    .eq('class_id', classId)
    .eq('label', label)
    .maybeSingle();
  if (existante) return existante.id;

  const { data, error } = await supabase
    .from('subjects')
    .insert({ parent_id: parentId, class_id: classId, label })
    .select('id')
    .single();
  if (error) throw error;
  return data.id;
}

export type ResultatImport = {
  batchId: string;
  documents: string[];
  refuses: FichierRefuse[];
};

/**
 * Dépose les fichiers puis enregistre un document par fichier.
 *
 * Plusieurs photos forment souvent un seul cours : elles partagent un batch_id
 * et sont ordonnées par page_no. Le découpage réel en leçons est décidé à
 * l'extraction, puis corrigé par le parent.
 */
export async function importerCours(params: {
  parentId: string;
  childId: string;
  /** Une matière du catalogue de la classe. L'import n'en invente plus. */
  subjectId: string | null;
  kind: 'cours' | 'devoir' | 'autre';
  fichiers: File[];
  onProgress?: (fait: number, total: number) => void;
}): Promise<ResultatImport> {
  const { parentId, childId, subjectId, kind, fichiers, onProgress } = params;
  const { acceptes, refuses } = trierFichiers(fichiers);
  if (acceptes.length === 0) {
    throw new Error('Aucun fichier exploitable : ' + (refuses[0]?.raison ?? 'liste vide'));
  }

  const batchId = crypto.randomUUID();
  const documents: string[] = [];

  for (let i = 0; i < acceptes.length; i++) {
    const fichier = acceptes[i];
    const page = i + 1;
    const chemin = cheminStockage(parentId, batchId, page, fichier.name);

    const { error: upErr } = await supabase.storage
      .from(BUCKET)
      .upload(chemin, fichier, { contentType: fichier.type, upsert: false });
    if (upErr) throw upErr;

    const { data, error } = await supabase
      .from('documents')
      .insert({
        parent_id: parentId,
        child_id: childId,
        subject_id: subjectId,
        kind,
        storage_path: chemin,
        original_name: fichier.name,
        mime: fichier.type,
        size_bytes: fichier.size,
        page_no: page,
        batch_id: batchId,
        stage: 'importe',
      })
      .select('id')
      .single();
    if (error) throw error;

    documents.push(data.id);
    onProgress?.(page, acceptes.length);
  }

  return { batchId, documents, refuses };
}
