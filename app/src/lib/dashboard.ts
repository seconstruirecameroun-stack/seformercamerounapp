import { supabase } from './supabase';
import { etapeCourante, etapeImage, imageGagnee, reussitesParNiveau } from './paliers';
import {
  calculerSerie,
  construireContexte,
  etatRang,
  objectifDuJour,
  quetesDuJour,
  trophees,
} from './jeu';
import type { EtatRang, Objectif, Quete, RepereItem, Serie, Trophee } from './jeu';

/**
 * Ce que l'enfant voit en arrivant.
 *
 * Tout est déduit du journal des tentatives et de la maîtrise : rien n'est
 * stocké en double. Si la formule de progression change un jour, ce tableau
 * change avec elle sans migration.
 */

export type Autocollant = {
  notionId: string;
  matiereId: string | null;
  statement: string;
  illustration: string | null;
  acquis: boolean;
};

export type LeconResume = {
  id: string;
  title: string;
  illustration: string | null;
  matiere: string | null;
  matiereId: string | null;
  /** L'intitulé du cahier : « Éducation à la paix », « Droits et devoirs ». */
  chapitre: string | null;
  /** Le jour écrit en haut de la page, quand le cahier le porte. */
  date: string | null;
  couleur: string | null;
  notions: number;
  acquises: number;
  dues: number;
  /**
   * Notions déjà travaillées dont la date de révision est arrivée.
   *
   * Différent de `dues`, qui compte aussi tout ce qui n'a jamais été vu :
   * c'est ce qu'il faut pour bâtir une mission, mais pas pour une pastille.
   * Annoncer « 3 à revoir » à un enfant qui n'a jamais ouvert la leçon est
   * faux, et ça met du rouge partout dès le premier écran.
   */
  aRevoir: number;
  /** L'étape en cours dans cette leçon, 1 à 3. */
  etape: number;
  /** Les trois étapes sont franchies. */
  etapeTerminee: boolean;
  /** Notions validées à l'étape en cours, et nombre total à y valider. */
  etapeFaites: number;
  etapeTotal: number;
};

/**
 * Une matière, vue comme un dossier.
 *
 * Six leçons tiennent dans une liste ; vingt n'y tiennent pas. L'enfant
 * choisit d'abord la matière, puis la leçon — deux écrans courts valent
 * mieux qu'un écran interminable.
 */
export type MatiereResume = {
  id: string;
  label: string;
  couleur: string | null;
  /** La couverture du dossier : l'image de sa première leçon. */
  illustration: string | null;
  lecons: number;
  /** Leçons dont une étape reste à franchir. */
  enCours: number;
  aRevoir: number;
};

export type TableauDeBord = {
  lecons: LeconResume[];
  matieres: MatiereResume[];
  duesTotal: number;
  points: number;
  serie: Serie;
  rang: EtatRang;
  objectif: Objectif;
  quetes: Quete[];
  trophees: Trophee[];
  /** Jours où l'enfant a répondu, du plus récent au plus ancien. */
  jours: string[];
  autocollants: Autocollant[];
  prochaineLecon: string | null;
};

export async function chargerTableauDeBord(childId: string): Promise<TableauDeBord> {
  // La classe de l'enfant commande ce qu'il voit. Sans ce filtre, un CM1
  // trouvait les leçons de CE1 de son frère dans sa propre liste — et les
  // comptait dans sa progression.
  const { data: enfant, error: erreurEnfant } = await supabase
    .from('children')
    .select('class_id')
    .eq('id', childId)
    .single();
  if (erreurEnfant) throw erreurEnfant;

  // Une leçon sans classe reste visible par tous : c'est le cas d'un document
  // importé avant que le parent ait choisi la classe.
  const classe = (enfant as { class_id: string | null }).class_id;

  const [lecons, maitrise, recompenses, tentatives, justes] = await Promise.all([
    supabase
      .from('lessons')
      .select(
        'id, title, illustration, subject_id, chapter, taught_on, subjects(label, color), ' +
          'notions(id, statement, illustration, status, items(id, level, status))',
      )
      .eq('status', 'approved')
      .or(classe ? `class_id.eq.${classe},class_id.is.null` : 'class_id.is.null')
      .order('sort_order'),
    supabase.from('mastery').select('notion_id, level, next_review').eq('child_id', childId),
    supabase.from('rewards').select('value, created_at').eq('child_id', childId),
    supabase
      .from('attempts')
      .select('item_id, correct, created_at')
      .eq('child_id', childId)
      .order('created_at', { ascending: false })
      .limit(400),
    // Seules les bonnes réponses situent l'étape : la liste reste courte,
    // et elle ne peut pas être tronquée par une limite comme au-dessus.
    supabase
      .from('attempts')
      .select('item_id, created_at')
      .eq('child_id', childId)
      .eq('correct', true),
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
    subject_id: string | null;
    chapter: string | null;
    taught_on: string | null;
    subjects: { label: string; color: string | null } | null;
    notions: Array<{
      id: string;
      statement: string;
      illustration: string | null;
      status: string;
      items: Array<{ id: string; level: number; status: string }>;
    }>;
  }>;

  const resumes: LeconResume[] = [];
  const autocollants: Autocollant[] = [];
  const repere = new Map<string, RepereItem>();
  /** Pour chaque notion gagnée, le jour où son image est tombée. */
  const jourDesImages = new Map<string, string>();

  // Le premier « juste » de chaque question, pour dater les événements du jour.
  const premierJuste = new Map<string, string>();
  for (const j of justes.data ?? []) {
    const jour = String(j.created_at).slice(0, 10);
    const connu = premierJuste.get(j.item_id);
    if (!connu || jour < connu) premierJuste.set(j.item_id, jour);
  }

  for (const lecon of brutes) {
    const notions = lecon.notions.filter((n) => n.status === 'approved');
    let acquises = 0;
    let dues = 0;
    let aRevoir = 0;

    // L'étape se lit avec la règle de la salle de jeu, importée telle quelle.
    const avecItems = notions.map((n) => ({
      id: n.id,
      items: (n.items ?? []).filter((i) => i.status === 'approved'),
    }));
    const reussies = reussitesParNiveau(avecItems, justes.data ?? []);
    const { niveau, termine } = etapeCourante(avecItems, reussies);

    for (const n of avecItems) {
      for (const i of n.items) {
        repere.set(i.id, {
          niveau: i.level,
          notionId: n.id,
          matiereId: lecon.subject_id,
          leconId: lecon.id,
        });
      }
    }

    for (const [rang, notion] of notions.entries()) {
      const m = suivi.get(notion.id);
      // L'image se gagne sur l'escalier, et la maîtrise ne sert plus qu'à
      // espacer les révisions : deux comptes différents, deux rôles.
      const acquis = imageGagnee(avecItems[rang], reussies);
      if (acquis) {
        acquises += 1;
        const niveauImage = etapeImage(avecItems[rang]);
        const jours = avecItems[rang].items
          .filter((i) => i.level === niveauImage)
          .map((i) => premierJuste.get(i.id))
          .filter((j): j is string => Boolean(j))
          .sort();
        if (jours[0]) jourDesImages.set(notion.id, jours[0]);
      }
      if (!m?.next_review || m.next_review <= aujourdhui) dues += 1;
      if (m?.next_review && m.next_review <= aujourdhui) aRevoir += 1;
      autocollants.push({
        notionId: notion.id,
        matiereId: lecon.subject_id,
        statement: notion.statement,
        illustration: notion.illustration,
        acquis,
      });
    }
    const aValider = avecItems.filter((n) => n.items.some((i) => i.level === niveau));

    resumes.push({
      id: lecon.id,
      title: lecon.title,
      illustration: lecon.illustration,
      matiere: lecon.subjects?.label ?? null,
      matiereId: lecon.subject_id,
      chapitre: lecon.chapter,
      date: lecon.taught_on,
      couleur: lecon.subjects?.color ?? null,
      notions: notions.length,
      acquises,
      dues,
      aRevoir,
      etape: niveau,
      etapeTerminee: termine,
      etapeFaites: termine ? aValider.length : (reussies.get(niveau)?.size ?? 0),
      etapeTotal: aValider.length,
    });
  }

  // La leçon mise en avant est celle dont une étape reste à franchir : c'est
  // l'escalier qui tire l'enfant, pas le calendrier. Quand tout est gravi, on
  // repasse la main à la révision espacée, et la leçon la plus due remonte.
  const enCours = resumes.filter((l) => !l.etapeTerminee && l.etapeTotal > 0);
  const prochaine =
    enCours.sort((a, b) => a.etape - b.etape || b.etapeTotal - b.etapeFaites - (a.etapeTotal - a.etapeFaites))[0] ??
    [...resumes].sort((a, b) => b.dues - a.dues)[0];

  const jours = [...new Set((tentatives.data ?? []).map((t) => String(t.created_at).slice(0, 10)))];

  // Les dossiers, dans l'ordre d'apparition des leçons : l'enfant retrouve
  // ses matières à la même place d'une fois sur l'autre.
  const parMatiere = new Map<string, MatiereResume>();
  for (const l of resumes) {
    if (!l.matiereId) continue;
    const dossier = parMatiere.get(l.matiereId) ?? {
      id: l.matiereId,
      label: l.matiere ?? 'Leçons',
      couleur: l.couleur,
      illustration: l.illustration,
      lecons: 0,
      enCours: 0,
      aRevoir: 0,
    };
    dossier.lecons += 1;
    if (!l.etapeTerminee && l.etapeTotal > 0) dossier.enCours += 1;
    dossier.aRevoir += l.aRevoir;
    if (!dossier.illustration) dossier.illustration = l.illustration;
    parMatiere.set(l.matiereId, dossier);
  }

  const etoiles = (recompenses.data ?? []).reduce((somme, r) => somme + (r.value ?? 0), 0);
  const serie = calculerSerie(jours);

  const gains = (recompenses.data ?? []).map((r) => ({
    value: r.value ?? 0,
    jour: String(r.created_at).slice(0, 10),
  }));

  const brutesTentatives = (tentatives.data ?? []) as unknown as Array<{
    item_id: string;
    correct: boolean;
    created_at: string;
  }>;
  const journal = brutesTentatives.map((t) => ({
    itemId: t.item_id,
    correct: t.correct,
    jour: String(t.created_at).slice(0, 10),
    a: String(t.created_at),
  }));

  const imagesDuJour = [...jourDesImages.values()].filter((j) => j === aujourdhui).length;

  // Un album est complet quand toutes les images d'une matière sont gagnées.
  const albums = new Map<string, { total: number; gagnes: number }>();
  for (const a of autocollants) {
    if (!a.illustration || !a.matiereId) continue;
    const album = albums.get(a.matiereId) ?? { total: 0, gagnes: 0 };
    album.total += 1;
    if (a.acquis) album.gagnes += 1;
    albums.set(a.matiereId, album);
  }

  // La plus longue suite de bonnes réponses au chrono, journal remis à
  // l'endroit : il arrive du plus récent au plus ancien.
  let meilleureSerieDefi = 0;
  let suite = 0;
  for (const t of [...journal].reverse()) {
    if (repere.get(t.itemId)?.niveau !== 4) continue;
    suite = t.correct ? suite + 1 : 0;
    if (suite > meilleureSerieDefi) meilleureSerieDefi = suite;
  }

  const avecImage = autocollants.filter((a) => a.illustration);
  const contexte = construireContexte(journal, repere, gains, imagesDuJour);

  return {
    lecons: resumes,
    matieres: [...parMatiere.values()],
    duesTotal: resumes.reduce((n, l) => n + l.dues, 0),
    points: etoiles,
    serie,
    rang: etatRang(etoiles),
    objectif: objectifDuJour(gains),
    quetes: quetesDuJour(contexte),
    trophees: trophees({
      etoiles,
      images: avecImage.filter((a) => a.acquis).length,
      albumsComplets: [...albums.values()].filter((a) => a.total > 0 && a.gagnes === a.total).length,
      leconsTerminees: resumes.filter((l) => l.etapeTerminee).length,
      serie: serie.jours,
      meilleureSerieDefi,
    }),
    jours,
    autocollants,
    prochaineLecon: prochaine?.id ?? resumes[0]?.id ?? null,
  };
}
