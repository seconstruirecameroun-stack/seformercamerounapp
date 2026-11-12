// Insère le cahier de sciences humaines de KLEIN et son cahier en anglais
// (octobre 2026, photographiés le 12 novembre) : 23 leçons, en français et
// en anglais. Une même matière peut avoir deux paquets, un par langue.
//
// Même script que pour le cahier de BRAYNE, à l-enfant et aux paquets près :
// tout passe par la session du parent et par RLS, les journaux des enfants ne
// sont pas touchés, et le script REFUSE avant d-écrire si un titre existe
// déjà dans la classe ou si une matière manque. `window.__A_BLANC = true`
// fait tous les contrôles et s-arrête avant la première écriture.

const H = window.__H, BASE = window.__BASE;
const ENFANT = 'b1b14ffe-dc0a-4aab-8f85-3a309b333e2f';
const PAQUETS = [
  ['Droits humains', '/seed-klein-droits-humains-en-nov12.json'],
  ['Histoire', '/seed-klein-histoire-en-nov12.json'],
  ['ICT', '/seed-klein-ict-en-nov12.json'],
  ['Métiers', '/seed-klein-metiers-en-nov12.json'],
  ['Sciences et technologies', '/seed-klein-sciences-et-technologies-en-nov12.json'],
  ['Éducation civique', '/seed-klein-education-civique-en-nov12.json'],
  ['Éducation morale', '/seed-klein-education-morale-en-nov12.json'],
  ['Géographie', '/seed-klein-geographie-fr-nov12.json'],
  ['Histoire', '/seed-klein-histoire-fr-nov12.json'],
  ['Sciences et technologies', '/seed-klein-sciences-et-technologies-fr-nov12.json'],
  ['Éducation civique', '/seed-klein-education-civique-fr-nov12.json'],
];

const sel = async (t, q) => {
  const r = await fetch(BASE + t + '?' + q, { headers: H });
  if (!r.ok) throw new Error('lecture ' + t + ' : ' + (await r.text()));
  return r.json();
};
const ins = async (t, rows) => {
  if (!rows.length) return [];
  const r = await fetch(BASE + t, {
    method: 'POST', headers: { ...H, Prefer: 'return=representation' }, body: JSON.stringify(rows),
  });
  if (!r.ok) throw new Error(t + ' : ' + (await r.text()));
  return r.json();
};

const [enfant] = await sel('children', 'select=id,first_name,class_id,parent_id&id=eq.' + ENFANT);
if (!enfant) throw new Error('enfant introuvable');
const CLASSE = enfant.class_id, PARENT = enfant.parent_id;

const existe = await sel('lessons', 'select=title,sort_order,subject_id&class_id=eq.' + CLASSE + '&limit=1000');
const sujets = await sel('subjects', 'select=*&limit=200');
let rang = Math.max(0, ...existe.map((e) => e.sort_order));

const plan = [];
for (const [matiere, chemin] of PAQUETS) {
  const d = await (await fetch(chemin + '?v=' + Date.now())).json();
  if (d.matiere !== matiere || d.enfant !== 'KLEIN') throw new Error('paquet inattendu : ' + chemin);
  const sujet = sujets.find((s) => s.label === matiere && (s.class_id === CLASSE || s.class_id == null));
  if (!sujet) throw new Error('la matière « ' + matiere + ' » n-existe pas pour cette classe');
  const titres = d.lecons.map((l) => l.title);
  if (new Set(titres).size !== titres.length) throw new Error('titre en double dans ' + chemin);
  const collision = existe.filter((e) => titres.includes(e.title));
  if (collision.length) throw new Error('titres déjà en base : ' + collision.map((c) => c.title).join(', '));
  plan.push({ matiere, sujet, d });
}

const bilan = {
  classe: CLASSE, rangDeDepart: rang + 1, aBlanc: Boolean(window.__A_BLANC),
  matieres: plan.map((p) => p.matiere + ' → ' + p.sujet.id + ' (' + existe.filter((e) => e.subject_id === p.sujet.id).length + ' leçons avant)'),
  lecons: 0, notions: 0, explications: 0, questions: 0, titres: [],
};

for (const { matiere, sujet, d } of plan) {
  for (const L of d.lecons) {
    rang += 1;
    bilan.titres.push(rang + ' ' + matiere + ' · ' + L.title);
    if (window.__A_BLANC) {
      bilan.lecons += 1;
      bilan.notions += L.notions.length;
      bilan.explications += L.notions.reduce((t, n) => t + n.explanations.length, 0);
      bilan.questions += L.notions.reduce((t, n) => t + n.items.length, 0);
      continue;
    }
    const [lec] = await ins('lessons', [{
      parent_id: PARENT, class_id: CLASSE, subject_id: sujet.id,
      title: L.title, summary: L.summary, lang: d.lang, chapter: L.chapter,
      taught_on: L.taught_on, sort_order: rang, status: 'approved',
      illustration: L.illustration, illustration_prompt: L.illustration_prompt,
    }]);
    const notions = await ins('notions', L.notions.map((n, i) => ({
      parent_id: PARENT, lesson_id: lec.id, kind: n.kind, statement: n.statement,
      sort_order: i + 1, status: 'approved',
      illustration: n.illustration, illustration_prompt: n.illustration_prompt,
    })));
    const par = new Map(notions.map((n) => [n.statement, n.id]));
    const expl = [], items = [];
    for (const n of L.notions) {
      const id = par.get(n.statement);
      if (!id) throw new Error('notion non retrouvée : ' + n.statement);
      for (const e of n.explanations) expl.push({ parent_id: PARENT, notion_id: id, register: e.register, body: e.body, status: 'approved' });
      for (const it of n.items) items.push({ parent_id: PARENT, notion_id: id, kind: it.kind, level: it.level, payload: it.payload, answer: it.answer, explain: it.explain, status: 'approved' });
    }
    bilan.lecons += 1;
    bilan.notions += notions.length;
    bilan.explications += (await ins('explanations', expl)).length;
    bilan.questions += (await ins('items', items)).length;
  }
}
bilan;
