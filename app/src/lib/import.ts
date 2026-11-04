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

/**
 * Le plus grand côté qu'une image garde avant l'envoi.
 *
 * Ce n'est pas un réglage de confort : c'est la résolution maximale que le
 * modèle utilise. Au-delà, il réduit lui-même avant de lire. Envoyer une
 * photo de 4 080 px, c'est donc faire voyager des pixels qu'on jette à
 * l'arrivée — et les faire voyager sur la 4G du parent.
 *
 * Dix pages de cahier pesaient 38,8 Mo. Le premier envoi a échoué avant la
 * moindre ligne en base. Réduites, les mêmes dix pages pèsent environ 5 Mo,
 * et le modèle voit exactement la même chose.
 */
export const COTE_MAX = 2576;

/**
 * Réduit une photo avant l'envoi, sans jamais faire échouer l'import.
 *
 * Tout ce qui n'est pas une image qu'on sait décoder — un PDF, un HEIC que
 * le navigateur refuse — repart tel quel. Une réduction est un gain, pas
 * une condition : la perdre ne doit pas coûter la page.
 */
export async function reduire(fichier: File): Promise<File> {
  if (!fichier.type.startsWith('image/')) return fichier;
  try {
    const source = await createImageBitmap(fichier);
    const cote = Math.max(source.width, source.height);
    const echelle = Math.min(1, COTE_MAX / cote);
    const w = Math.round(source.width * echelle);
    const h = Math.round(source.height * echelle);

    const canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    if (!ctx) return fichier;
    ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(source, 0, 0, w, h);
    source.close();

    const blob = await new Promise<Blob | null>((r) => canvas.toBlob(r, 'image/jpeg', 0.82));
    if (!blob || blob.size >= fichier.size) return fichier;

    const nom = fichier.name.replace(/\.[^.]+$/, '') + '.jpg';
    return new File([blob], nom, { type: 'image/jpeg', lastModified: fichier.lastModified });
  } catch (_) {
    // HEIC que le navigateur ne décode pas, image corrompue, mémoire courte :
    // on envoie l'original plutôt que de refuser la page.
    return fichier;
  }
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
  /**
   * Le jour écrit en haut de la page du cahier.
   *
   * Nullable : toutes les pages n'en portent pas, et deviner le jour d'un
   * cours serait pire que de l'ignorer.
   */
  taughtOn: string | null;
  kind: 'cours' | 'devoir' | 'autre';
  fichiers: File[];
  onProgress?: (fait: number, total: number, etape: 'reduction' | 'envoi') => void;
}): Promise<ResultatImport> {
  const { parentId, childId, subjectId, taughtOn, kind, fichiers, onProgress } = params;

  // La réduction passe AVANT le tri : une photo de 24 Mo serait refusée pour
  // son poids alors qu'elle pèse 500 Ko une fois ramenée à la taille que le
  // modèle utilise.
  const reduits: File[] = [];
  for (let i = 0; i < fichiers.length; i++) {
    onProgress?.(i + 1, fichiers.length, 'reduction');
    reduits.push(await reduire(fichiers[i]));
  }

  const { acceptes, refuses } = trierFichiers(reduits);
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
        taught_on: taughtOn,
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
    onProgress?.(page, acceptes.length, 'envoi');
  }

  return { batchId, documents, refuses };
}
