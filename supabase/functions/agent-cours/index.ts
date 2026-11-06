/**
 * agent-cours — la porte par laquelle une tâche planifiée voit les cours.
 *
 * POURQUOI ELLE EXISTE
 *
 * Les leçons faites à la main sont déposées depuis le navigateur du parent,
 * avec sa session : rien ne circule, aucune clé ne traîne. Mais une tâche
 * planifiée démarre à neuf, sans mémoire et sans session. Elle ne peut donc
 * ni voir les photos du compartiment privé, ni écrire les leçons.
 *
 * Cette fonction est la seule porte qu-on lui ouvre, et elle est étroite :
 * trois actions, pas une de plus, et aucune ne supprime quoi que ce soit.
 *
 *   contexte  les enfants, leur classe, leurs matières, les rangs pris
 *   lister    les lots de pages encore au stade « importe »
 *   pages     des liens signés, valables une heure, vers les photos d-un lot
 *   deposer   les leçons finies, et le lot passe au stade demandé
 *
 * « contexte » n-est pas un confort. Une tâche planifiée démarre sans
 * mémoire : elle ne connaît ni l-identifiant de l-enfant, ni celui de la
 * matière, ni le rang où reprendre. Sans cette action elle ne pourrait
 * rien déposer du tout. Elle ne rend que ce que le parent voit déjà dans
 * son propre espace.
 *
 * CE QUI LA PROTÈGE
 *
 * 1. Un secret partagé, que le parent génère lui-même et dépose dans les
 *    secrets de la fonction. Ce n-est ni une clé Supabase ni son mot de
 *    passe : s-il fuit, on le change en une minute sans rien casser
 *    d-autre. La comparaison est à temps constant, pour ne pas laisser
 *    deviner le secret octet par octet.
 *
 * 2. La fonction ne sert qu-UN parent, nommé dans AGENT_COURS_PARENT. Même
 *    avec le secret en main, on ne peut pas s-en servir pour atteindre la
 *    famille d-un autre. Tout ce qui est lu ou écrit est filtré sur ce
 *    seul identifiant, y compris ce qui vient du paquet déposé.
 *
 * 3. Elle n-expose aucune requête libre. Pas de table en paramètre, pas de
 *    filtre fourni par l-appelant : les trois actions sont écrites en dur.
 *
 * 4. Elle refuse un dépôt dont un sort_order existe déjà dans la classe.
 *    C-est ce qui rend un deuxième appel sans danger : si la tâche a été
 *    relancée après une coupure, elle est arrêtée au lieu de créer des
 *    doublons que personne ne verrait avant que l-enfant les rencontre.
 *
 * SUR LA CLÉ DE SERVICE
 *
 * Supabase injecte SUPABASE_SERVICE_ROLE_KEY dans l-environnement de toute
 * fonction Edge : personne n-a à la copier, ni à la voir. C-est elle qui
 * permet d-écrire sans la session du parent, et c-est exactement pour la
 * tenir enfermée ici que les quatre protections ci-dessus existent. Elle ne
 * sort jamais de ce fichier et ne figure dans aucune réponse.
 *
 * Déploiement :  supabase functions deploy agent-cours --no-verify-jwt
 * Secrets :      AGENT_COURS_SECRET, AGENT_COURS_PARENT
 */

import { createClient } from 'npm:@supabase/supabase-js@2.49.4';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'content-type, x-agent-secret',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

const JSON_ENTETES = { ...CORS, 'Content-Type': 'application/json' };

/**
 * Les stades qu-un lot peut recevoir, recopiés de l-enum doc_stage du
 * schéma. Une valeur inventée ne serait pas refusée ici : elle serait
 * refusée par Postgres, au milieu du dépôt, une fois les leçons écrites.
 */
const STADES = new Set(['importe', 'en_lecture', 'a_valider', 'publie', 'echec']);

/**
 * Les statuts qu-une leçon peut porter, recopiés de l-enum content_status.
 *
 * Il n-y en a que trois, et « a_valider » n-en fait PAS partie — c-est un
 * stade de document, pas un statut de contenu. Le statut qui veut dire
 * « le parent n-a pas encore tranché » est « pending », et c-est d-ailleurs
 * le défaut de la colonne.
 */
const STATUTS = new Set(['pending', 'approved', 'rejected']);

function repondre(corps: unknown, status = 200) {
  return new Response(JSON.stringify(corps), { status, headers: JSON_ENTETES });
}

/**
 * Comparaison à temps constant.
 *
 * Un `===` sur des chaînes s-arrête au premier octet qui diffère, et le
 * temps de réponse laisse alors deviner le secret lettre par lettre. Le
 * coût de faire autrement est nul ; le coût de ne pas le faire est un
 * secret qui se devine en quelques milliers d-appels.
 */
function memeSecret(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let ecart = 0;
  for (let i = 0; i < a.length; i++) ecart |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return ecart === 0;
}

type Explication = { register: string; body: string };
type Question = {
  kind: string;
  level: number;
  payload: Record<string, unknown>;
  answer: Record<string, unknown>;
  explain?: string | null;
};
type Notion = {
  kind: string;
  statement: string;
  illustration?: string | null;
  illustration_prompt?: string | null;
  explanations: Explication[];
  items: Question[];
};
type Lecon = {
  title: string;
  summary: string;
  chapter?: string | null;
  sort_order: number;
  taught_on?: string | null;
  lang?: string | null;
  subject_id?: string | null;
  matiere?: string | null;
  illustration?: string | null;
  illustration_prompt?: string | null;
  notions: Notion[];
};

Deno.serve(async (requete) => {
  if (requete.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (requete.method !== 'POST') return repondre({ erreur: 'POST attendu' }, 405);

  const secret = Deno.env.get('AGENT_COURS_SECRET');
  const parent = Deno.env.get('AGENT_COURS_PARENT');
  if (!secret || !parent) {
    // Sans ces deux secrets la fonction serait ouverte : elle refuse de
    // servir plutôt que de servir mal.
    return repondre({ erreur: 'agent non configuré', code: 'sans_secret' }, 503);
  }

  const donne = requete.headers.get('x-agent-secret') ?? '';
  if (!memeSecret(donne, secret)) return repondre({ erreur: 'secret refusé' }, 401);

  let corps: { action?: string; batch?: string; stade?: string; statut?: string; paquet?: unknown };
  try {
    corps = await requete.json();
  } catch {
    return repondre({ erreur: 'corps illisible' }, 400);
  }

  const db = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
    { auth: { persistSession: false } },
  );

  // -------------------------------------------------------------- contexte
  if (corps.action === 'contexte') {
    const [enfants, matieres] = await Promise.all([
      db.from('children').select('id, first_name, class_id, avatar').eq('parent_id', parent),
      db.from('subjects').select('id, label, class_id').eq('parent_id', parent),
    ]);
    if (enfants.error) return repondre({ erreur: enfants.error.message }, 500);
    if (matieres.error) return repondre({ erreur: matieres.error.message }, 500);

    const classes = [...new Set((enfants.data ?? []).map((e) => e.class_id).filter(Boolean))];
    const { data: libelles } = classes.length
      ? await db.from('classes').select('id, code, subsystem').in('id', classes as string[])
      : { data: [] };
    const nomClasse = new Map((libelles ?? []).map((c) => [c.id, c.code]));

    // Le rang le plus haut déjà pris, par classe : c-est là que la
    // prochaine leçon doit commencer. Le calculer ici évite que la tâche
    // le devine, et un rang deviné finit en doublon.
    const rangs: Record<string, number> = {};
    for (const classe of classes as string[]) {
      const { data: haut } = await db
        .from('lessons')
        .select('sort_order')
        .eq('parent_id', parent)
        .eq('class_id', classe)
        .order('sort_order', { ascending: false })
        .limit(1)
        .maybeSingle();
      rangs[classe] = haut?.sort_order ?? 0;
    }

    return repondre({
      enfants: (enfants.data ?? []).map((e) => ({
        id: e.id,
        prenom: e.first_name,
        class_id: e.class_id,
        classe: nomClasse.get(e.class_id ?? '') ?? null,
        dernier_rang: rangs[e.class_id ?? ''] ?? 0,
      })),
      matieres: (matieres.data ?? []).map((m) => ({
        id: m.id,
        label: m.label,
        class_id: m.class_id,
      })),
    });
  }

  // ---------------------------------------------------------------- lister
  if (corps.action === 'lister') {
    const { data, error } = await db
      .from('documents')
      .select('batch_id, page_no, storage_path, created_at, child_id, subject_id, taught_on')
      .eq('parent_id', parent)
      .eq('stage', 'importe')
      .order('created_at', { ascending: true });
    if (error) return repondre({ erreur: error.message }, 500);

    const enfants = new Map<string, { prenom: string; class_id: string }>();
    const ids = [...new Set((data ?? []).map((d) => d.child_id).filter(Boolean))] as string[];
    if (ids.length) {
      const { data: cs } = await db
        .from('children')
        .select('id, first_name, class_id')
        .eq('parent_id', parent)
        .in('id', ids);
      for (const c of cs ?? []) enfants.set(c.id, { prenom: c.first_name, class_id: c.class_id });
    }

    const lots = new Map<string, Record<string, unknown>>();
    for (const d of data ?? []) {
      const lot = lots.get(d.batch_id) ?? {
        batch: d.batch_id,
        child_id: d.child_id,
        enfant: enfants.get(d.child_id ?? '')?.prenom ?? null,
        class_id: enfants.get(d.child_id ?? '')?.class_id ?? null,
        subject_id: d.subject_id,
        taught_on: d.taught_on,
        depuis: d.created_at,
        pages: 0,
      };
      (lot.pages as number)++;
      lots.set(d.batch_id, lot);
    }
    return repondre({ lots: [...lots.values()] });
  }

  // ----------------------------------------------------------------- pages
  if (corps.action === 'pages') {
    if (!corps.batch) return repondre({ erreur: 'batch manquant' }, 400);
    const { data, error } = await db
      .from('documents')
      .select('page_no, storage_path, mime, original_name')
      .eq('parent_id', parent)
      .eq('batch_id', corps.batch)
      .order('page_no', { ascending: true });
    if (error) return repondre({ erreur: error.message }, 500);
    if (!data?.length) return repondre({ erreur: 'lot introuvable' }, 404);

    const pages = [];
    for (const d of data) {
      // Une heure : le temps de télécharger et de travailler, pas celui
      // d-oublier un lien actif dans un journal.
      const { data: signe, error: eS } = await db.storage
        .from('cours')
        .createSignedUrl(d.storage_path, 3600);
      if (eS) return repondre({ erreur: 'lien refusé : ' + eS.message }, 500);
      pages.push({ page: d.page_no, nom: d.original_name, mime: d.mime, url: signe.signedUrl });
    }
    return repondre({ batch: corps.batch, pages });
  }

  // --------------------------------------------------------------- deposer
  if (corps.action === 'deposer') {
    const paquet = corps.paquet as
      | { class_id?: string; lang?: string; lecons?: Lecon[] }
      | undefined;
    if (!paquet?.class_id || !Array.isArray(paquet.lecons) || !paquet.lecons.length) {
      return repondre({ erreur: 'paquet incomplet : class_id et lecons sont requis' }, 400);
    }
    // Par défaut le parent garde le dernier mot : la leçon arrive en
    // « pending » et le lot en « a_valider ». Rien n-atteint l-enfant tant
    // que personne n-a regardé.
    const statut = corps.statut ?? 'pending';
    if (!STATUTS.has(statut)) {
      return repondre({ erreur: 'statut inconnu : ' + statut, connus: [...STATUTS] }, 400);
    }
    const stade = corps.stade ?? 'a_valider';
    if (!STADES.has(stade)) {
      return repondre({ erreur: 'stade inconnu : ' + stade, connus: [...STADES] }, 400);
    }

    // La classe doit être celle d-un enfant de CE parent.
    //
    // Attention : « classes » est une table de référence GLOBALE — SIL, CP,
    // CE1 sont les mêmes lignes pour toutes les familles, et elle ne porte
    // pas de parent_id. Chercher la classe du parent n-aurait donc rien
    // trouvé et aurait refusé tous les dépôts. Le lien d-appartenance
    // passe par l-enfant : c-est lui qui est inscrit dans une classe.
    const { data: enfant } = await db
      .from('children')
      .select('id')
      .eq('parent_id', parent)
      .eq('class_id', paquet.class_id)
      .limit(1)
      .maybeSingle();
    if (!enfant) return repondre({ erreur: 'aucun enfant de ce parent dans cette classe' }, 403);

    // Les matières, elles, appartiennent bien à un parent. Une leçon qui
    // pointerait vers la matière d-une autre famille serait invisible chez
    // elle et parasite chez l-autre : on refuse avant d-écrire.
    const matieres = [...new Set(paquet.lecons.map((l) => l.subject_id).filter(Boolean))] as string[];
    if (matieres.length) {
      const { data: ok } = await db
        .from('subjects')
        .select('id')
        .eq('parent_id', parent)
        .in('id', matieres);
      const connues = new Set((ok ?? []).map((m) => m.id));
      const etrangeres = matieres.filter((m) => !connues.has(m));
      if (etrangeres.length) {
        return repondre({ erreur: 'matière inconnue pour ce parent', matieres: etrangeres }, 403);
      }
    }

    // Un deuxième appel après une coupure ne doit pas doubler les leçons.
    //
    // Le filtre sur parent_id n-est pas décoratif : la classe étant
    // partagée, sans lui on verrait les rangs d-une autre famille et on
    // refuserait un dépôt parfaitement légitime.
    const ordres = paquet.lecons.map((l) => l.sort_order);
    const { data: deja } = await db
      .from('lessons')
      .select('sort_order, title')
      .eq('parent_id', parent)
      .eq('class_id', paquet.class_id)
      .in('sort_order', ordres);
    if (deja?.length) {
      return repondre(
        {
          erreur: 'ces rangs existent déjà dans la classe',
          code: 'rangs_pris',
          pris: deja.map((l) => `${l.sort_order} ${l.title}`),
        },
        409,
      );
    }

    const bilan = { lecons: 0, notions: 0, explications: 0, questions: 0, titres: [] as string[] };
    for (const L of paquet.lecons) {
      const { data: lec, error: eL } = await db
        .from('lessons')
        .insert({
          parent_id: parent,
          class_id: paquet.class_id,
          subject_id: L.subject_id ?? null,
          title: L.title,
          summary: L.summary,
          lang: L.lang ?? paquet.lang ?? 'fr',
          chapter: L.chapter ?? null,
          sort_order: L.sort_order,
          status: statut,
          illustration: L.illustration ?? null,
          illustration_prompt: L.illustration_prompt ?? null,
          taught_on: L.taught_on ?? null,
        })
        .select('id')
        .single();
      if (eL) return repondre({ erreur: `leçon « ${L.title} » : ${eL.message}`, bilan }, 500);
      bilan.lecons++;
      bilan.titres.push(`${L.sort_order} ${L.title}`);

      for (const [rang, N] of (L.notions ?? []).entries()) {
        const { data: no, error: eN } = await db
          .from('notions')
          .insert({
            parent_id: parent,
            lesson_id: lec.id,
            kind: N.kind,
            statement: N.statement,
            sort_order: rang,
            status: statut,
            illustration: N.illustration ?? null,
            illustration_prompt: N.illustration_prompt ?? null,
          })
          .select('id')
          .single();
        if (eN) return repondre({ erreur: `notion : ${eN.message}`, bilan }, 500);
        bilan.notions++;

        if (N.explanations?.length) {
          const { error: eE } = await db.from('explanations').insert(
            N.explanations.map((x) => ({
              parent_id: parent,
              notion_id: no.id,
              register: x.register,
              body: x.body,
              status: statut,
            })),
          );
          if (eE) return repondre({ erreur: `explications : ${eE.message}`, bilan }, 500);
          bilan.explications += N.explanations.length;
        }

        if (N.items?.length) {
          const { error: eI } = await db.from('items').insert(
            N.items.map((x) => ({
              parent_id: parent,
              notion_id: no.id,
              kind: x.kind,
              level: x.level,
              payload: x.payload,
              answer: x.answer,
              explain: x.explain ?? null,
              status: statut,
            })),
          );
          if (eI) return repondre({ erreur: `questions : ${eI.message}`, bilan }, 500);
          bilan.questions += N.items.length;
        }
      }
    }

    // Le lot ne change de stade qu-une fois tout le reste écrit : une
    // coupure en cours laisse le lot à faire, jamais un lot marqué fini
    // dont les leçons manquent.
    if (corps.batch) {
      const { error: eD } = await db
        .from('documents')
        .update({ stage: stade })
        .eq('parent_id', parent)
        .eq('batch_id', corps.batch);
      if (eD) return repondre({ erreur: `stade du lot : ${eD.message}`, bilan }, 500);
    }

    return repondre({ bilan, statut, stade: corps.batch ? stade : null });
  }

  return repondre({ erreur: 'action inconnue : ' + (corps.action ?? '(vide)') }, 400);
});
