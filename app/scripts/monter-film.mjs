/**
 * Monte le film d'une leçon à partir des scènes et de la narration.
 *
 * Le montage se fait en local, avec ffmpeg. C'est ce qui permet de refaire le
 * film à l'identique, et de corriger un mot-clé sans repayer une génération :
 * seules les scènes et la voix coûtent des crédits.
 *
 * Chaque plan dure exactement sa phrase, plus une courte respiration. La durée
 * du film n'est donc pas décidée à l'avance : elle découle du texte.
 *
 * Usage :  node scripts/monter-film.mjs <dossier>
 *   le dossier contient scene1..N.png, vo1..N.mp3 et script_manifest.json
 */

import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join, resolve } from 'node:path';
import ffmpeg from 'ffmpeg-static';

const dossier = process.argv[2];
if (!dossier) {
  console.error('Usage : node scripts/monter-film.mjs <dossier>');
  process.exit(1);
}

const LARGEUR = 1280;
const HAUTEUR = 720;
const FPS = 25;
/** Respiration après chaque phrase : l'enfant a besoin d'un temps pour voir. */
const PAUSE = 0.6;
const POLICE = 'C\\:/Windows/Fonts/arialbd.ttf';

const manifeste = JSON.parse(readFileSync(join(dossier, 'script_manifest.json'), 'utf8'));
const temp = join(dossier, '.montage');
rmSync(temp, { recursive: true, force: true });
mkdirSync(temp, { recursive: true });

const ff = (args) => execFileSync(ffmpeg, ['-y', '-hide_banner', '-loglevel', 'error', ...args]);

function duree(fichier) {
  const sortie = execFileSync(ffmpeg, ['-i', fichier], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] })
    .toString();
  return lireDuree(sortie);
}

function lireDuree(texte) {
  const m = texte.match(/Duration: (\d+):(\d+):(\d+\.\d+)/);
  if (!m) throw new Error('durée illisible');
  return Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3]);
}

// ffmpeg écrit les métadonnées sur stderr et sort en erreur sans -o : on lit
// la sortie de l'exception plutôt que d'ajouter ffprobe.
function dureeMp3(fichier) {
  try {
    duree(fichier);
  } catch (e) {
    return lireDuree(String(e.stderr || e.stdout || ''));
  }
  throw new Error('durée introuvable pour ' + fichier);
}

const plans = manifeste.blocks.map((bloc, i) => {
  const n = i + 1;
  const voix = join(dossier, `vo${n}.mp3`);
  const d = dureeMp3(voix) + PAUSE;
  return { n, bloc, voix, duree: d, scene: join(dossier, `scene${n}.png`) };
});

console.log('Plans :');
for (const p of plans) console.log(`  ${p.n}. ${p.duree.toFixed(2)}s  ${p.bloc.keywords.join(' · ')}`);
const total = plans.reduce((s, p) => s + p.duree, 0);
console.log(`Durée totale : ${total.toFixed(1)}s\n`);

// ───────────────────────── 1. les plans ─────────────────────────
for (const p of plans) {
  const images = Math.round(p.duree * FPS);
  // Un lent rapprochement : l'image fixe respire sans attirer l'attention sur
  // le mouvement lui-même.
  const kenBurns =
    `scale=${LARGEUR * 2}:-2,` +
    `zoompan=z='min(1+0.0009*on,1.12)':d=${images}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':` +
    `s=${LARGEUR}x${HAUTEUR}:fps=${FPS}`;

  const motsFichier = join(temp, `mots${p.n}.txt`);
  writeFileSync(motsFichier, p.bloc.keywords.join('   ·   '), 'utf8');

  // Le mot-clé arrive une demi-seconde après la phrase et reste jusqu'au bout.
  const texte =
    `drawtext=fontfile='${POLICE}':textfile='${motsFichier.replace(/\\/g, '/').replace(/:/g, '\\:')}':` +
    `fontcolor=white:fontsize=44:borderw=3:bordercolor=0x1b3b3fcc:` +
    `x=(w-text_w)/2:y=h-120:enable='gte(t,0.5)':alpha='min((t-0.5)/0.4,1)'`;

  ff([
    '-loop', '1', '-framerate', String(FPS), '-i', p.scene,
    '-t', p.duree.toFixed(2),
    '-vf', `${kenBurns},${texte},format=yuv420p`,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
    join(temp, `plan${p.n}.mp4`),
  ]);
  console.log(`  plan ${p.n} rendu`);
}

// ───────────────────────── 2. la bande son ─────────────────────────
// Chaque phrase est suivie de sa respiration, pour rester calée sur l'image.
const morceaux = [];
for (const p of plans) {
  const padded = join(temp, `voix${p.n}.wav`);
  ff(['-i', p.voix, '-af', `apad=pad_dur=${PAUSE}`, '-ar', '44100', '-ac', '2', padded]);
  morceaux.push(padded);
}
writeFileSync(
  join(temp, 'voix.txt'),
  // ffmpeg résout les chemins d'une liste depuis le dossier de la liste, et
  // non depuis le dossier courant. Un dossier passé en relatif donnait donc
  // une liste illisible : on écrit en absolu.
  morceaux.map((m) => `file '${resolve(m).replace(/\\/g, '/')}'`).join('\n'),
  'utf8',
);
ff(['-f', 'concat', '-safe', '0', '-i', join(temp, 'voix.txt'), '-c', 'copy', join(temp, 'voix.wav')]);

// ───────────────────────── 3. assemblage ─────────────────────────
writeFileSync(
  join(temp, 'plans.txt'),
  plans.map((p) => `file '${resolve(join(temp, `plan${p.n}.mp4`)).replace(/\\/g, '/')}'`).join('\n'),
  'utf8',
);
ff(['-f', 'concat', '-safe', '0', '-i', join(temp, 'plans.txt'), '-c', 'copy', join(temp, 'muet.mp4')]);

const sortie = join(dossier, 'film.mp4');
ff([
  '-i', join(temp, 'muet.mp4'),
  '-i', join(temp, 'voix.wav'),
  '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest',
  // L'index en tête du fichier : la lecture démarre avant la fin du
  // téléchargement, ce qui change tout sur une connexion lente.
  '-movflags', '+faststart',
  sortie,
]);

console.log(`\nFilm monté : ${sortie}`);
