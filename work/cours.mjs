#!/usr/bin/env node
/**
 * cours.mjs — la main de la tâche planifiée sur les cours.
 *
 * Les leçons faites à la main sont déposées depuis le navigateur du parent,
 * avec sa session. Une tâche planifiée n-a pas de session : elle passe par
 * la fonction Edge « agent-cours », et cet outil est tout ce qu-elle a le
 * droit d-appeler.
 *
 *   node work/cours.mjs contexte
 *       Les enfants, leur classe, leurs matières, et le dernier rang pris.
 *       À lire en premier : c-est ce qui donne les identifiants.
 *
 *   node work/cours.mjs lister
 *       Les lots de pages qu-un parent a envoyés et que personne n-a encore
 *       traités. Rien à faire s-il n-y en a pas.
 *
 *   node work/cours.mjs pages <lot> [dossier]
 *       Télécharge les photos du lot pour pouvoir les regarder. Par défaut
 *       dans work/lot-<lot>/.
 *
 *   node work/cours.mjs deposer <paquet.json> [--lot <id>] [--statut …] [--stade …]
 *       Dépose les leçons. Le paquet est celui que produisent les scripts
 *       work/lecons-*.py : l-outil résout lui-même l-enfant, la classe et
 *       les matières, pour qu-aucun identifiant ne soit écrit à la main.
 *       Par défaut les leçons arrivent au statut « pending » et le lot au
 *       stade « a_valider » : le parent garde le dernier mot, et rien
 *       n-atteint l-enfant tant que personne n-a regardé.
 *
 * CONFIGURATION — .env.cours.local à la racine, jamais versionné :
 *
 *   AGENT_COURS_URL=https://<projet>.supabase.co/functions/v1/agent-cours
 *   AGENT_COURS_SECRET=<le secret que vous avez généré>
 *
 * Le secret n-est ni une clé Supabase ni un mot de passe : c-est une chaîne
 * au hasard, qui ne donne accès qu-à ces quatre actions et qu-on remplace
 * en une minute si elle fuit.
 */

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const RACINE = dirname(dirname(fileURLToPath(import.meta.url)));
const CONFIG = join(RACINE, '.env.cours.local');

/** Un échec attendu, dont le message suffit : pas de pile à afficher. */
class Souci extends Error {}

async function reglages() {
  if (!existsSync(CONFIG)) {
    throw new Souci(
      `Il manque ${CONFIG}.\n` +
        'Créez-le avec ces deux lignes :\n' +
        '  AGENT_COURS_URL=https://<projet>.supabase.co/functions/v1/agent-cours\n' +
        '  AGENT_COURS_SECRET=<votre secret>',
    );
  }
  const valeurs = {};
  for (const ligne of (await readFile(CONFIG, 'utf8')).split('\n')) {
    const net = ligne.trim();
    if (!net || net.startsWith('#')) continue;
    const coupe = net.indexOf('=');
    if (coupe === -1) continue;
    valeurs[net.slice(0, coupe).trim()] = net.slice(coupe + 1).trim();
  }
  for (const nom of ['AGENT_COURS_URL', 'AGENT_COURS_SECRET']) {
    if (!valeurs[nom]) throw new Souci(`${nom} manque dans ${CONFIG}.`);
  }
  return valeurs;
}

async function appeler(corps) {
  const { AGENT_COURS_URL, AGENT_COURS_SECRET } = await reglages();
  let reponse;
  try {
    reponse = await fetch(AGENT_COURS_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-agent-secret': AGENT_COURS_SECRET },
      body: JSON.stringify(corps),
    });
  } catch (e) {
    throw new Souci(`La fonction n-a pas répondu : ${e.message}\nURL appelée : ${AGENT_COURS_URL}`);
  }

  const texte = await reponse.text();
  let data;
  try {
    data = JSON.parse(texte);
  } catch {
    throw new Souci(`Réponse illisible (${reponse.status}) :\n${texte.slice(0, 400)}`);
  }
  if (!reponse.ok) {
    if (reponse.status === 401) {
      throw new Souci('Secret refusé. Vérifiez AGENT_COURS_SECRET des deux côtés.');
    }
    if (data.code === 'sans_secret') {
      throw new Souci(
        'La fonction est déployée mais pas configurée.\n' +
          'Posez ses deux secrets :  AGENT_COURS_SECRET  et  AGENT_COURS_PARENT',
      );
    }
    const detail = data.pris ? '\n  ' + data.pris.join('\n  ') : '';
    throw new Souci(`${data.erreur ?? 'erreur'} (${reponse.status})${detail}`);
  }
  return data;
}

// --------------------------------------------------------------- contexte

async function contexte({ brut = false } = {}) {
  const d = await appeler({ action: 'contexte' });
  if (brut) return console.log(JSON.stringify(d, null, 2));

  if (!d.enfants.length) return console.log('Aucun enfant enregistré.');
  for (const e of d.enfants) {
    console.log(`\n${e.prenom}  —  ${e.classe ?? 'classe inconnue'}`);
    console.log(`  enfant   ${e.id}`);
    console.log(`  classe   ${e.class_id}`);
    console.log(`  rangs    jusqu-à ${e.dernier_rang} ; la suivante prend ${e.dernier_rang + 1}`);
    const siennes = d.matieres.filter((m) => m.class_id === e.class_id);
    if (siennes.length) {
      console.log('  matières');
      for (const m of siennes) console.log(`    ${m.label.padEnd(30)} ${m.id}`);
    }
  }
}

// ----------------------------------------------------------------- lister

async function lister({ brut = false } = {}) {
  const d = await appeler({ action: 'lister' });
  if (brut) return console.log(JSON.stringify(d, null, 2));

  if (!d.lots.length) return console.log('Aucun lot en attente.');
  console.log(`${d.lots.length} lot(s) en attente :\n`);
  for (const l of d.lots) {
    const quand = new Date(l.depuis).toLocaleString('fr-FR');
    console.log(`  ${l.batch}`);
    console.log(`    ${l.enfant ?? 'enfant inconnu'} — ${l.pages} page(s) — envoyé le ${quand}`);
  }
  console.log('\nPour voir les photos :  node work/cours.mjs pages <lot>');
}

// ------------------------------------------------------------------ pages

async function pages(lot, dossier) {
  if (!lot) throw new Souci('Usage : node work/cours.mjs pages <lot> [dossier]');
  const d = await appeler({ action: 'pages', batch: lot });
  const cible = resolve(dossier ?? join(RACINE, 'work', `lot-${lot}`));
  await mkdir(cible, { recursive: true });

  let total = 0;
  for (const p of d.pages) {
    const reponse = await fetch(p.url);
    if (!reponse.ok) throw new Souci(`page ${p.page} : téléchargement refusé (${reponse.status})`);
    const octets = Buffer.from(await reponse.arrayBuffer());
    const ext = (p.mime ?? '').includes('png') ? 'png' : (p.mime ?? '').includes('pdf') ? 'pdf' : 'jpg';
    const nom = `p${String(p.page).padStart(2, '0')}.${ext}`;
    await writeFile(join(cible, nom), octets);
    total += octets.length;
    console.log(`  ${nom}  ${(octets.length / 1024).toFixed(0)} Ko  ${p.nom ?? ''}`);
  }
  console.log(`\n${d.pages.length} page(s), ${(total / 1024 / 1024).toFixed(1)} Mo`);
  console.log(cible);
}

// ---------------------------------------------------------------- deposer

/**
 * Traduit un paquet de work/lecons-*.py en ce que la fonction attend.
 *
 * Les scripts nomment l-enfant et la matière en clair — « KLEIN »,
 * « Métiers » — parce que c-est ce qu-on lit dans un cahier. La base, elle,
 * veut des identifiants. La traduction se fait ici, contre le contexte réel,
 * pour qu-aucun identifiant ne soit recopié à la main : un uuid tapé de
 * travers ne se voit pas, et il écrit la leçon dans la mauvaise classe.
 */
function traduire(paquet, ctx) {
  const vise = (paquet.enfant ?? '').trim().toLowerCase();
  const enfant = ctx.enfants.find((e) => (e.prenom ?? '').trim().toLowerCase() === vise);
  if (!enfant) {
    const connus = ctx.enfants.map((e) => e.prenom).join(', ') || '(aucun)';
    throw new Souci(`Enfant « ${paquet.enfant} » introuvable. Connus : ${connus}`);
  }

  const siennes = ctx.matieres.filter((m) => m.class_id === enfant.class_id);
  const parNom = new Map(siennes.map((m) => [m.label.trim().toLowerCase(), m.id]));
  const manquantes = new Set();

  const lecons = paquet.lecons.map((L) => {
    const nom = (L.matiere ?? paquet.matiere ?? '').trim();
    const id = parNom.get(nom.toLowerCase());
    if (!id) manquantes.add(nom || '(sans matière)');
    return { ...L, subject_id: id ?? null };
  });

  if (manquantes.size) {
    const dispo = siennes.map((m) => m.label).join(', ') || '(aucune)';
    throw new Souci(
      `Matière(s) introuvable(s) pour ${enfant.prenom} : ${[...manquantes].join(', ')}\n` +
        `Matières de sa classe : ${dispo}`,
    );
  }

  return { class_id: enfant.class_id, lang: paquet.lang ?? 'fr', lecons, enfant };
}

async function deposer(fichier, options) {
  if (!fichier) {
    throw new Souci('Usage : node work/cours.mjs deposer <paquet.json> [--lot <id>]');
  }
  const chemin = resolve(fichier);
  if (!existsSync(chemin)) throw new Souci(`Paquet introuvable : ${chemin}`);

  let paquet;
  try {
    paquet = JSON.parse(await readFile(chemin, 'utf8'));
  } catch (e) {
    throw new Souci(`Paquet illisible : ${e.message}`);
  }
  if (!Array.isArray(paquet.lecons) || !paquet.lecons.length) {
    throw new Souci('Le paquet ne contient aucune leçon.');
  }

  const ctx = await appeler({ action: 'contexte' });
  const { class_id, lang, lecons, enfant } = traduire(paquet, ctx);

  const rangs = lecons.map((l) => l.sort_order);
  console.log(`${enfant.prenom} — ${lecons.length} leçon(s), rangs ${Math.min(...rangs)} à ${Math.max(...rangs)}`);
  if (Math.min(...rangs) <= enfant.dernier_rang) {
    console.log(`  ⚠ le dernier rang occupé est ${enfant.dernier_rang} : la fonction refusera si un rang est déjà pris.`);
  }

  const d = await appeler({
    action: 'deposer',
    batch: options.lot,
    statut: options.statut,
    stade: options.stade,
    paquet: { class_id, lang, lecons },
  });

  const b = d.bilan;
  console.log(`\n${b.lecons} leçon(s), ${b.notions} notion(s), ${b.explications} explication(s), ${b.questions} question(s)`);
  for (const t of b.titres) console.log(`  ${t}`);
  console.log(`\nstatut : ${d.statut}${d.stade ? ` — lot passé au stade ${d.stade}` : ''}`);
}

// ------------------------------------------------------------------ entrée

function options(args) {
  const o = {};
  const restants = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--lot') o.lot = args[++i];
    else if (args[i] === '--statut') o.statut = args[++i];
    else if (args[i] === '--stade') o.stade = args[++i];
    else if (args[i] === '--json') o.brut = true;
    else restants.push(args[i]);
  }
  return { o, restants };
}

const AIDE = `
  node work/cours.mjs contexte              les enfants, leurs matières, les rangs pris
  node work/cours.mjs lister                les lots de pages en attente
  node work/cours.mjs pages <lot> [dossier] télécharge les photos d-un lot
  node work/cours.mjs deposer <paquet.json> [--lot <id>] [--statut pending|approved]

  --json  sur contexte et lister, rend la réponse brute
`;

const [commande, ...reste] = process.argv.slice(2);
const { o, restants } = options(reste);

try {
  if (commande === 'contexte') await contexte(o);
  else if (commande === 'lister') await lister(o);
  else if (commande === 'pages') await pages(restants[0], restants[1]);
  else if (commande === 'deposer') await deposer(restants[0], o);
  else {
    console.log(AIDE);
    process.exit(commande ? 1 : 0);
  }
} catch (e) {
  console.error(e instanceof Souci ? `\n${e.message}\n` : e);
  process.exit(1);
}
