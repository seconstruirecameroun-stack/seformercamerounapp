import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import type { Emplacement, ObjetPossede } from '../../lib/avatar';
import { APPARENCE_DEFAUT, type Apparence } from './apparence';

/**
 * Le personnage en 3D.
 *
 * Un héros aux proportions de jeu d'enfant — une grande tête, un petit corps
 * arrondi — construit dans le code : aucun modèle n'est téléchargé. Le moteur
 * 3D ne se charge que là où il s'affiche.
 *
 * CE QUI LUI DONNE SA QUALITÉ :
 *
 *   des formes arrondies, jamais de cube brut ; un visage dessiné — grands
 *   yeux à double reflet, sourcils, joues, sourire — posé sur la tête comme
 *   un décalque, avec des paupières qui se ferment pour cligner ;
 *
 *   un éclairage de studio : une lumière principale qui porte une ombre
 *   douce au sol, un contre-jour qui détache la silhouette, et un
 *   environnement qui donne de vrais reflets à l'or et au métal ;
 *
 *   des animations qui ont du poids : il arrive en rebondissant, respire en
 *   s'écrasant un peu, regarde autour de lui, s'accroupit avant de sauter et
 *   s'écrase en retombant.
 *
 * L'ÉNERGIE SE VOIT. Pleine, il est vif, saute de joie de temps en temps et
 * son podium s'allume ; basse, il respire lentement, baisse la tête, ses
 * paupières tombent et des « Z » s'envolent.
 *
 * Son allure est à lui : il n'est le personnage d'aucun autre jeu.
 */

type Props = {
  equipement: Partial<Record<Emplacement, ObjetPossede>>;
  energie: number;
  apparence?: Apparence;
  /** Hauteur en pixels ; la largeur suit le conteneur. */
  hauteur?: number;
  /** Sur la page d'accueil : plus petit, et il ne se fait pas tourner. */
  compact?: boolean;
};

const OR = '#ffc93c';
const CHEVEUX = '#1e130c';

// ── Le visage ───────────────────────────────────────────────────────────────

/**
 * Le visage, sur une toile transparente : seuls les traits sont peints, la
 * peau est celle de la tête. `ouverture` va de 0 (fermé) à 1 (grand ouvert).
 */
function dessinerVisage(ctx: CanvasRenderingContext2D, peau: string, ouverture: number, humeur: 'joie' | 'calme' | 'sommeil') {
  const t = ctx.canvas.width;
  ctx.clearRect(0, 0, t, t);

  // Les joues, en dégradé doux.
  for (const x of [0.2, 0.8]) {
    const g = ctx.createRadialGradient(t * x, t * 0.64, 0, t * x, t * 0.64, t * 0.12);
    g.addColorStop(0, 'rgba(255,120,110,0.55)');
    g.addColorStop(1, 'rgba(255,120,110,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, t, t);
  }

  // Les sourcils.
  ctx.strokeStyle = '#2a1a10';
  ctx.lineCap = 'round';
  ctx.lineWidth = t * 0.028;
  for (const x of [0.32, 0.68]) {
    ctx.beginPath();
    const haut = humeur === 'sommeil' ? 0.33 : 0.27;
    ctx.moveTo(t * (x - 0.07), t * (haut + 0.015));
    ctx.quadraticCurveTo(t * x, t * (haut - 0.025), t * (x + 0.07), t * (haut + 0.015));
    ctx.stroke();
  }

  // Les yeux : grands, sombres, avec deux reflets.
  for (const x of [0.32, 0.68]) {
    const cx = t * x;
    const cy = t * 0.45;
    const rx = t * 0.075;
    const ry = t * 0.1;
    if (ouverture < 0.12) {
      // Fermés : un arc.
      ctx.strokeStyle = '#1b120c';
      ctx.lineWidth = t * 0.03;
      ctx.beginPath();
      ctx.arc(cx, cy - ry * 0.2, rx, 0.15 * Math.PI, 0.85 * Math.PI);
      ctx.stroke();
      continue;
    }
    ctx.save();
    ctx.beginPath();
    ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
    ctx.clip();
    const iris = ctx.createRadialGradient(cx, cy + ry * 0.3, ry * 0.1, cx, cy, ry * 1.1);
    iris.addColorStop(0, '#6b3d1f');
    iris.addColorStop(0.55, '#2a160b');
    iris.addColorStop(1, '#0b0603');
    ctx.fillStyle = iris;
    ctx.fillRect(cx - rx, cy - ry, rx * 2, ry * 2);
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.ellipse(cx + rx * 0.3, cy - ry * 0.4, rx * 0.34, ry * 0.28, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(cx - rx * 0.35, cy + ry * 0.35, rx * 0.15, 0, Math.PI * 2);
    ctx.fill();
    // La paupière qui descend, couleur de peau.
    if (ouverture < 1) {
      ctx.fillStyle = peau;
      ctx.fillRect(cx - rx, cy - ry, rx * 2, ry * 2 * (1 - ouverture));
      ctx.strokeStyle = '#1b120c';
      ctx.lineWidth = t * 0.018;
      ctx.beginPath();
      ctx.moveTo(cx - rx, cy - ry + ry * 2 * (1 - ouverture));
      ctx.lineTo(cx + rx, cy - ry + ry * 2 * (1 - ouverture));
      ctx.stroke();
    }
    ctx.restore();
  }

  // La bouche.
  if (humeur === 'joie') {
    ctx.fillStyle = '#5a1a14';
    ctx.beginPath();
    ctx.moveTo(t * 0.4, t * 0.66);
    ctx.quadraticCurveTo(t * 0.5, t * 0.8, t * 0.6, t * 0.66);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#f07a7a';
    ctx.beginPath();
    ctx.ellipse(t * 0.5, t * 0.735, t * 0.045, t * 0.025, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.strokeStyle = '#4a1a12';
    ctx.lineWidth = t * 0.025;
    ctx.beginPath();
    if (humeur === 'sommeil') ctx.ellipse(t * 0.5, t * 0.7, t * 0.025, t * 0.03, 0, 0, Math.PI * 2);
    else ctx.arc(t * 0.5, t * 0.63, t * 0.07, 0.2 * Math.PI, 0.8 * Math.PI);
    ctx.stroke();
  }
}

/** Une texture ronde et douce, pour les particules : jamais de carrés. */
function texturePoint(): THREE.CanvasTexture {
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const x = c.getContext('2d')!;
  const g = x.createRadialGradient(32, 32, 0, 32, 32, 32);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.35, 'rgba(255,255,255,0.8)');
  g.addColorStop(1, 'rgba(255,255,255,0)');
  x.fillStyle = g;
  x.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}

function etoileForme(rayon: number): THREE.Shape {
  const s = new THREE.Shape();
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2 + Math.PI / 2;
    const r = i % 2 ? rayon * 0.45 : rayon;
    if (i === 0) s.moveTo(Math.cos(a) * r, Math.sin(a) * r);
    else s.lineTo(Math.cos(a) * r, Math.sin(a) * r);
  }
  return s;
}

const doux = (x: number) => x * x * (3 - 2 * x);

export default function Avatar3D({ equipement, energie, apparence = APPARENCE_DEFAUT, hauteur = 320, compact = false }: Props) {
  const boiteRef = useRef<HTMLDivElement | null>(null);
  const [sansWebGL, setSansWebGL] = useState(false);
  const geste = useRef<{ genre: 'saut' | 'salut' | 'tour'; debut: number } | null>(null);
  const prochainGeste = useRef(0);
  const angle = useRef({ cible: -0.3, actuel: -0.3 });

  const cle = JSON.stringify([
    Object.values(equipement).map((o) => o && o.id + (o.eteint ? '-eteint' : '')),
    apparence,
    Math.round(energie / 20),
  ]);

  useEffect(() => {
    const conteneur = boiteRef.current;
    if (!conteneur) return;
    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    } catch {
      setSansWebGL(true);
      return;
    }
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    conteneur.appendChild(renderer.domElement);
    renderer.domElement.style.display = 'block';
    renderer.domElement.style.touchAction = compact ? 'auto' : 'none';

    const scene = new THREE.Scene();
    // L'environnement de studio : de vrais reflets sur l'or et le métal.
    const pmrem = new THREE.PMREMGenerator(renderer);
    const studio = new RoomEnvironment();
    const envTex = pmrem.fromScene(studio, 0.04).texture;
    scene.environment = envTex;

    const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 50);
    camera.position.set(0, compact ? 1.55 : 1.6, compact ? 6.0 : 6.6);
    camera.lookAt(0, 1.2, 0);

    const vif = energie / 100;
    const fatigue = energie <= 40;

    scene.add(new THREE.HemisphereLight('#fff4e0', '#6b4a2a', 0.55 + 0.35 * vif));
    const principale = new THREE.DirectionalLight('#fff3e0', 1.7 + 0.8 * vif);
    principale.position.set(1.2, 6, 2.5);
    principale.castShadow = true;
    principale.shadow.mapSize.set(512, 512);
    principale.shadow.camera.left = -2;
    principale.shadow.camera.right = 2;
    principale.shadow.camera.top = 3;
    principale.shadow.camera.bottom = -1;
    principale.shadow.radius = 4;
    principale.shadow.bias = -0.0015;
    scene.add(principale);
    const contreJour = new THREE.DirectionalLight('#9fd8ff', 1.4);
    contreJour.position.set(-3, 3, -4);
    scene.add(contreJour);

    const jetables: Array<{ dispose: () => void }> = [envTex, pmrem];
    const garde = <T extends { dispose: () => void }>(x: T) => {
      jetables.push(x);
      return x;
    };
    const mat = (couleur: string, extra: Partial<THREE.MeshPhysicalMaterialParameters> = {}) =>
      garde(new THREE.MeshPhysicalMaterial({ color: couleur, roughness: 0.6, metalness: 0, ...extra }));
    const arrondi = (l: number, h: number, p: number, r: number) =>
      garde(new RoundedBoxGeometry(l, h, p, 4, r));
    const sphere = (r: number) => garde(new THREE.SphereGeometry(r, 28, 20));
    const capsule = (r: number, l: number) => garde(new THREE.CapsuleGeometry(r, l, 8, 16));
    const or = (brille = true) =>
      mat(OR, { metalness: 0.9, roughness: 0.22, emissive: '#6b4a00', emissiveIntensity: brille ? 0.35 : 0, clearcoat: 0.6 });

    // ── Le podium ───────────────────────────────────────────────────────────
    // L'ombre ne tombe que sur le podium : au-delà, elle flotterait dans le vide.
    const sol = new THREE.Mesh(garde(new THREE.CircleGeometry(1.05, 48)), garde(new THREE.ShadowMaterial({ opacity: 0.22 })));
    sol.rotation.x = -Math.PI / 2;
    sol.position.y = 0.002;
    sol.receiveShadow = true;
    scene.add(sol);
    const podium = new THREE.Mesh(garde(new THREE.CylinderGeometry(1.05, 1.15, 0.14, 48)), mat('#fff3dc', { roughness: 0.4, clearcoat: 0.4 }));
    podium.position.y = -0.07;
    podium.receiveShadow = true;
    scene.add(podium);
    const halo = new THREE.Mesh(
      garde(new THREE.TorusGeometry(1.1, 0.035, 12, 64)),
      mat(energie >= 60 ? '#ffd166' : energie > 0 ? '#ff9f43' : '#9aa3ad', {
        emissive: energie >= 60 ? '#ffb000' : '#ff7a00', emissiveIntensity: 1.2 * vif,
      }),
    );
    halo.rotation.x = Math.PI / 2;
    halo.position.y = 0.005;
    scene.add(halo);

    // ── Le personnage ─────────────────────────────────────────────────────
    const heros = new THREE.Group();
    scene.add(heros);
    const corps = new THREE.Group();
    heros.add(corps);

    const peau = mat(apparence.peau, { roughness: 0.55, sheen: 0.3, sheenColor: new THREE.Color('#ffd9c0') });
    const corpsObjet = equipement.corps?.id;
    const haut =
      corpsObjet === 'armure' ? mat('#c9d1db', { metalness: 0.85, roughness: 0.28, clearcoat: 0.5 })
        : corpsObjet === 'tenue-or' ? or(!equipement.corps?.eteint)
          : corpsObjet === 'maillot' ? mat('#17803d', { roughness: 0.7 })
            : mat(apparence.haut, { roughness: 0.75, sheen: 0.5 });
    const bas = mat(apparence.bas, { roughness: 0.8, sheen: 0.4 });

    // Les chaussures.
    const pieds = equipement.pieds?.id;
    for (const x of [-0.19, 0.19]) {
      const chaussure = new THREE.Mesh(
        arrondi(0.32, pieds === 'bottes' ? 0.36 : 0.2, 0.46, 0.09),
        pieds === 'bottes'
          ? mat('#1d9bf0', { emissive: '#38bdf8', emissiveIntensity: 0.5 * vif, clearcoat: 0.8 })
          : pieds === 'baskets' ? mat('#f8fafc', { clearcoat: 0.5 }) : mat('#4a3020'),
      );
      chaussure.position.set(x, pieds === 'bottes' ? 0.18 : 0.1, 0.05);
      corps.add(chaussure);
      if (pieds === 'baskets') {
        const semelle = new THREE.Mesh(arrondi(0.34, 0.06, 0.48, 0.03), mat('#e63946'));
        semelle.position.set(x, 0.03, 0.05);
        corps.add(semelle);
      }
    }
    // Les jambes.
    for (const x of [-0.19, 0.19]) {
      const jambe = new THREE.Mesh(capsule(0.14, 0.32), bas);
      jambe.position.set(x, 0.42, 0);
      corps.add(jambe);
    }
    // Le bassin, puis le torse.
    const bassin = new THREE.Mesh(arrondi(0.78, 0.3, 0.5, 0.13), bas);
    bassin.position.y = 0.7;
    corps.add(bassin);
    const torse = new THREE.Mesh(arrondi(0.88, 0.72, 0.56, 0.2), haut);
    torse.position.y = 1.08;
    corps.add(torse);
    if (corpsObjet === 'maillot') {
      // Le maillot des Lions : une bande jaune, une rouge.
      const jaune = new THREE.Mesh(arrondi(0.9, 0.1, 0.58, 0.05), mat('#ffc93c'));
      jaune.position.y = 1.16;
      const rouge = new THREE.Mesh(arrondi(0.9, 0.07, 0.58, 0.035), mat('#e63946'));
      rouge.position.y = 1.05;
      corps.add(jaune, rouge);
    } else if (corpsObjet === 'armure') {
      const plastron = new THREE.Mesh(arrondi(0.6, 0.48, 0.12, 0.08), mat('#e2e8f0', { metalness: 0.9, roughness: 0.2, clearcoat: 1 }));
      plastron.position.set(0, 1.1, 0.27);
      const embleme = new THREE.Mesh(garde(new THREE.ExtrudeGeometry(etoileForme(0.11), { depth: 0.03, bevelEnabled: false })), or());
      embleme.position.set(0, 1.1, 0.33);
      corps.add(plastron, embleme);
    }
    // Le col.
    const col = new THREE.Mesh(garde(new THREE.TorusGeometry(0.2, 0.05, 10, 24)), haut);
    col.rotation.x = Math.PI / 2;
    col.position.y = 1.44;
    corps.add(col);

    // Les bras, accrochés à l'épaule.
    const bras: THREE.Group[] = [];
    for (const cote of [-1, 1]) {
      const epaule = new THREE.Group();
      epaule.position.set(cote * 0.52, 1.32, 0);
      const manche = new THREE.Mesh(capsule(0.12, 0.3), haut);
      manche.position.y = -0.22;
      if (corpsObjet === 'armure') {
        const epauliere = new THREE.Mesh(sphere(0.17), mat('#e2e8f0', { metalness: 0.9, roughness: 0.2 }));
        epauliere.scale.set(1, 0.7, 1);
        epauliere.position.y = 0.02;
        epaule.add(epauliere);
      }
      const main = new THREE.Mesh(sphere(0.13), peau);
      main.position.y = -0.5;
      epaule.add(manche, main);
      corps.add(epaule);
      bras.push(epaule);
    }

    // La tête.
    const tete = new THREE.Group();
    tete.position.y = 1.47;
    corps.add(tete);
    const crane = new THREE.Mesh(arrondi(1.0, 0.9, 0.86, 0.3), peau);
    crane.position.y = 0.45;
    tete.add(crane);
    for (const cote of [-1, 1]) {
      const oreille = new THREE.Mesh(sphere(0.12), peau);
      oreille.scale.set(0.6, 1, 0.9);
      oreille.position.set(cote * 0.5, 0.45, 0);
      tete.add(oreille);
    }
    const toile = document.createElement('canvas');
    toile.width = toile.height = 256;
    const ctx = toile.getContext('2d')!;
    const texture = garde(new THREE.CanvasTexture(toile));
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.anisotropy = 4;
    const visage = new THREE.Mesh(
      garde(new THREE.PlaneGeometry(0.86, 0.78)),
      garde(new THREE.MeshStandardMaterial({ map: texture, transparent: true, roughness: 0.5, polygonOffset: true, polygonOffsetFactor: -2 })),
    );
    visage.position.set(0, 0.42, 0.432);
    tete.add(visage);
    const humeur = fatigue ? 'sommeil' : vif >= 0.8 ? 'joie' : 'calme';
    const ouvertureRepos = fatigue ? 0.35 : 1;
    dessinerVisage(ctx, apparence.peau, ouvertureRepos, humeur);
    texture.needsUpdate = true;

    // Les cheveux : une coupe courte et bouclée, faite de petites sphères.
    const chapeau = equipement.tete?.id;
    const couvreChef = chapeau === 'casquette' || chapeau === 'chapeau';
    const cheveux = mat(CHEVEUX, { roughness: 0.95, sheen: 0.6, sheenColor: new THREE.Color('#5a3a22') });
    const boucles = new THREE.Group();
    const graine = (i: number) => {
      const s = Math.sin(i * 12.9898) * 43758.5453;
      return s - Math.floor(s);
    };
    let n = 0;
    for (let ix = -2; ix <= 2; ix++) {
      for (let iz = -2; iz <= 1; iz++) {
        // Sous un chapeau, le dessus de la tête est caché : pas de boucles.
        if (couvreChef) continue;
        const b = new THREE.Mesh(sphere(0.19 + graine(n++) * 0.04), cheveux);
        b.position.set(ix * 0.2, 0.86 + graine(n++) * 0.05 - Math.abs(ix) * 0.025, iz * 0.2 - 0.02);
        boucles.add(b);
      }
    }
    // Le bord des cheveux : sur le front (sans chapeau), et toujours sur la
    // nuque et aux tempes, là où il dépasse d'un chapeau.
    for (let ix = -2; ix <= 2; ix++) {
      if (!couvreChef) {
        const f = new THREE.Mesh(sphere(0.13), cheveux);
        f.position.set(ix * 0.2, 0.82, 0.3);
        boucles.add(f);
      }
      const nuque = new THREE.Mesh(sphere(0.16), cheveux);
      nuque.position.set(ix * 0.2, couvreChef ? 0.68 : 0.62, -0.36);
      boucles.add(nuque);
    }
    for (const cote of [-1, 1]) {
      const tempe = new THREE.Mesh(sphere(0.13), cheveux);
      tempe.position.set(cote * 0.44, 0.74, -0.12);
      boucles.add(tempe);
    }
    tete.add(boucles);

    // ── Les objets ────────────────────────────────────────────────────────
    const enMouvement: Array<(t: number) => void> = [];

    if (chapeau === 'casquette') {
      const dome = new THREE.Mesh(garde(new THREE.SphereGeometry(0.54, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2)), mat('#e63946', { roughness: 0.6 }));
      dome.scale.set(1, 0.72, 1);
      dome.position.y = 0.66;
      const visiere = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.36, 0.36, 0.05, 32)), mat('#c1121f'));
      visiere.scale.set(1.15, 1, 0.9);
      visiere.position.set(0, 0.7, 0.46);
      visiere.rotation.x = 0.12;
      const bouton = new THREE.Mesh(sphere(0.05), mat('#c1121f'));
      bouton.position.y = 1.05;
      tete.add(dome, visiere, bouton);
    } else if (chapeau === 'bandeau') {
      const b = new THREE.Mesh(garde(new THREE.TorusGeometry(0.5, 0.06, 12, 40)), mat('#e63946'));
      b.rotation.x = Math.PI / 2;
      b.scale.set(1, 0.92, 1);
      b.position.y = 0.74;
      tete.add(b);
      for (const s of [-1, 1]) {
        const pan = new THREE.Mesh(arrondi(0.08, 0.3, 0.05, 0.02), mat('#e63946'));
        pan.position.set(s * 0.08, 0.6, -0.48);
        pan.rotation.z = s * 0.4;
        tete.add(pan);
        enMouvement.push((t) => {
          pan.rotation.x = 0.3 + Math.sin(t * 4 + s) * 0.15;
        });
      }
    } else if (chapeau === 'chapeau') {
      const bord = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.85, 0.88, 0.05, 48)), mat('#b88a4a', { roughness: 0.85 }));
      bord.position.y = 0.8;
      const calotte = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.42, 0.5, 0.36, 40)), mat('#cfa463', { roughness: 0.85 }));
      calotte.position.y = 1.0;
      const ruban = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.505, 0.505, 0.09, 40)), mat('#5a3b1c'));
      ruban.position.y = 0.87;
      tete.add(bord, calotte, ruban);
    } else if (chapeau === 'couronne') {
      const brille = !equipement.tete?.eteint;
      const m = or(brille);
      const anneau = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.42, 0.44, 0.18, 40, 1, true)), m);
      // Elle se pose SUR les boucles, pas dedans.
      anneau.position.y = 1.06;
      tete.add(anneau);
      const gemmes = ['#e63946', '#3a86ff', '#2ec4b6', '#e63946', '#8338ec'];
      for (let i = 0; i < 5; i++) {
        const a = (i / 5) * Math.PI * 2 + Math.PI / 2;
        const pointe = new THREE.Mesh(garde(new THREE.ConeGeometry(0.085, 0.24, 12)), m);
        pointe.position.set(Math.cos(a) * 0.42, 1.26, Math.sin(a) * 0.42);
        const gemme = new THREE.Mesh(sphere(0.055), mat(gemmes[i], {
          roughness: 0.05, clearcoat: 1, emissive: gemmes[i], emissiveIntensity: brille ? 0.6 : 0,
        }));
        gemme.position.set(Math.cos(a) * 0.42, 1.39, Math.sin(a) * 0.42);
        tete.add(pointe, gemme);
      }
    }

    const dos = equipement.dos?.id;
    if (dos === 'sac') {
      const sac = new THREE.Mesh(arrondi(0.66, 0.66, 0.3, 0.12), mat('#a0642e', { roughness: 0.8 }));
      sac.position.set(0, 1.05, -0.42);
      const poche = new THREE.Mesh(arrondi(0.44, 0.24, 0.1, 0.05), mat('#8b5524'));
      poche.position.set(0, 0.9, -0.6);
      corps.add(sac, poche);
      for (const s of [-1, 1]) {
        const bretelle = new THREE.Mesh(arrondi(0.08, 0.6, 0.06, 0.02), mat('#8b5524'));
        bretelle.position.set(s * 0.26, 1.12, 0.29);
        corps.add(bretelle);
      }
    } else if (dos === 'cape') {
      const geo = garde(new THREE.PlaneGeometry(0.95, 1.25, 8, 10));
      const cape = new THREE.Mesh(geo, mat('#c1121f', { side: THREE.DoubleSide, roughness: 0.65, sheen: 0.8, sheenColor: new THREE.Color('#ff8a8a') }));
      cape.position.set(0, 0.82, -0.32);
      corps.add(cape);
      for (const s of [-1, 1]) {
        const agrafe = new THREE.Mesh(sphere(0.06), or());
        agrafe.position.set(s * 0.2, 1.42, 0.18);
        corps.add(agrafe);
      }
      const base = geo.attributes.position.array.slice();
      enMouvement.push((t) => {
        const pos = geo.attributes.position;
        for (let i = 0; i < pos.count; i++) {
          const x = base[i * 3];
          const y = base[i * 3 + 1];
          const versLeBas = (0.625 - y) / 1.25;
          pos.setZ(i, -versLeBas * (0.28 + 0.1 * Math.sin(t * 2.5 + y * 4 + x * 2)));
        }
        pos.needsUpdate = true;
        geo.computeVertexNormals();
      });
    } else if (dos === 'ailes' || dos === 'ailes-or') {
      const dorees = dos === 'ailes-or';
      const brille = !equipement.dos?.eteint;
      const m = dorees
        ? mat(OR, { metalness: 0.7, roughness: 0.3, side: THREE.DoubleSide, emissive: '#7a5200', emissiveIntensity: brille ? 0.45 : 0 })
        : mat('#ffffff', { side: THREE.DoubleSide, roughness: 0.5, sheen: 1, sheenColor: new THREE.Color('#cfe8ff') });
      const plume = new THREE.Shape();
      plume.absellipse(0, 0, 0.5, 0.14, 0, Math.PI * 2, false, 0);
      const geoPlume = garde(new THREE.ShapeGeometry(plume, 16));
      const ailes: THREE.Group[] = [];
      for (const cote of [-1, 1]) {
        const aile = new THREE.Group();
        aile.position.set(cote * 0.18, 1.2, -0.32);
        for (let i = 0; i < 4; i++) {
          const p = new THREE.Mesh(geoPlume, m);
          p.position.set(cote * (0.42 + i * 0.03), 0.15 - i * 0.14, -i * 0.01);
          p.rotation.z = cote * (0.55 - i * 0.28);
          p.scale.setScalar(1 - i * 0.12);
          aile.add(p);
        }
        corps.add(aile);
        ailes.push(aile);
      }
      enMouvement.push((t) => {
        const b = 0.25 + 0.3 * Math.sin(t * (1.5 + 3 * vif));
        ailes[0].rotation.y = b;
        ailes[1].rotation.y = -b;
      });
    }

    const tenu = equipement.main?.id;
    if (tenu === 'livre') {
      const livre = new THREE.Group();
      const couverture = new THREE.Mesh(arrondi(0.34, 0.44, 0.1, 0.03), mat('#3a86ff', { clearcoat: 0.6 }));
      const pages = new THREE.Mesh(arrondi(0.3, 0.4, 0.08, 0.01), mat('#fffaf0'));
      pages.position.x = 0.025;
      const etoile = new THREE.Mesh(garde(new THREE.ExtrudeGeometry(etoileForme(0.07), { depth: 0.01, bevelEnabled: false })), or());
      etoile.position.set(0, 0, 0.055);
      livre.add(pages, couverture, etoile);
      livre.position.set(0, -0.6, 0.2);
      bras[1].add(livre);
    } else if (tenu === 'trophee') {
      const profil = [
        [0, 0], [0.13, 0], [0.13, 0.03], [0.05, 0.06], [0.04, 0.16], [0.08, 0.2], [0.17, 0.28], [0.2, 0.45], [0.19, 0.46], [0, 0.3],
      ].map(([x, y]) => new THREE.Vector2(x, y));
      const coupe = new THREE.Mesh(garde(new THREE.LatheGeometry(profil, 32)), or());
      coupe.position.set(0, -0.78, 0.22);
      bras[1].add(coupe);
    }

    // Le compagnon.
    const compagnon = equipement.compagnon?.id;
    if (compagnon) {
      const ami = new THREE.Group();
      ami.position.set(1.25, 0.55, 0.3);
      scene.add(ami);
      if (compagnon === 'balle') {
        const c = document.createElement('canvas');
        c.width = 128;
        c.height = 64;
        const x = c.getContext('2d')!;
        ['#e63946', '#ffffff', '#3a86ff', '#ffffff', '#ffc93c', '#ffffff'].forEach((couleur, i) => {
          x.fillStyle = couleur;
          x.fillRect(i * (128 / 6), 0, 128 / 6 + 1, 64);
        });
        const tex = garde(new THREE.CanvasTexture(c));
        tex.colorSpace = THREE.SRGBColorSpace;
        ami.add(new THREE.Mesh(sphere(0.24), garde(new THREE.MeshPhysicalMaterial({ map: tex, roughness: 0.3, clearcoat: 0.8 }))));
      } else if (compagnon === 'etoile') {
        const e = new THREE.Mesh(
          garde(new THREE.ExtrudeGeometry(etoileForme(0.3), { depth: 0.08, bevelEnabled: true, bevelSize: 0.04, bevelThickness: 0.04, bevelSegments: 3 })),
          mat('#ffd60a', { emissive: '#ffb703', emissiveIntensity: 0.5 * vif, clearcoat: 1, roughness: 0.25 }),
        );
        e.position.z = -0.04;
        ami.add(e);
        for (const s of [-1, 1]) {
          const oeil = new THREE.Mesh(sphere(0.03), mat('#1b120c'));
          oeil.position.set(s * 0.06, 0.04, 0.1);
          ami.add(oeil);
        }
      } else if (compagnon === 'lionceau') {
        const brille = !equipement.compagnon?.eteint;
        const fauve = mat('#e8a33d', { roughness: 0.7, sheen: 0.6 });
        const criniere = mat('#8a4b14', { roughness: 0.9, emissive: '#7a3a00', emissiveIntensity: brille ? 0.25 : 0 });
        for (let i = 0; i < 10; i++) {
          const a = (i / 10) * Math.PI * 2;
          const touffe = new THREE.Mesh(sphere(0.1), criniere);
          touffe.position.set(Math.cos(a) * 0.2, 0.3 + Math.sin(a) * 0.2, -0.04);
          ami.add(touffe);
        }
        const tetel = new THREE.Mesh(sphere(0.2), fauve);
        tetel.position.y = 0.3;
        const museau = new THREE.Mesh(sphere(0.08), mat('#ffe5b4'));
        museau.position.set(0, 0.25, 0.17);
        const nez = new THREE.Mesh(sphere(0.03), mat('#3a1a0a'));
        nez.position.set(0, 0.29, 0.24);
        ami.add(tetel, museau, nez);
        for (const s of [-1, 1]) {
          const oeil = new THREE.Mesh(sphere(0.03), mat('#120a05', { roughness: 0.1, clearcoat: 1 }));
          oeil.position.set(s * 0.07, 0.35, 0.17);
          const oreille = new THREE.Mesh(sphere(0.06), fauve);
          oreille.position.set(s * 0.14, 0.47, 0);
          ami.add(oeil, oreille);
        }
        const corpsl = new THREE.Mesh(capsule(0.13, 0.22), fauve);
        corpsl.rotation.x = Math.PI / 2;
        corpsl.position.set(0, 0.05, -0.18);
        const queue = new THREE.Mesh(capsule(0.025, 0.25), fauve);
        queue.position.set(0, 0.12, -0.42);
        queue.rotation.x = -0.8;
        const pompon = new THREE.Mesh(sphere(0.05), criniere);
        pompon.position.set(0, 0.24, -0.52);
        ami.add(corpsl, queue, pompon);
        ami.scale.setScalar(1.2);
      }
      enMouvement.push((t) => {
        ami.position.y = 0.45 + Math.abs(Math.sin(t * (2 + 2 * vif))) * 0.3 * (0.4 + vif);
        ami.rotation.y = -0.5 + Math.sin(t * 0.8) * 0.4;
      });
      ami.traverse((o) => {
        if ((o as THREE.Mesh).isMesh) o.castShadow = true;
      });
    }

    // L'aura : des points de lumière ronds qui montent en tournant.
    const aura = equipement.aura?.id;
    if (aura) {
      const nb = 70;
      const positions = new Float32Array(nb * 3);
      const vitesses: number[] = [];
      const angles: number[] = [];
      for (let i = 0; i < nb; i++) {
        const a = Math.random() * Math.PI * 2;
        angles.push(a);
        const r = 0.75 + Math.random() * 0.35;
        positions.set([Math.cos(a) * r, Math.random() * 2.6, Math.sin(a) * r], i * 3);
        vitesses.push(0.5 + Math.random() * 0.9);
      }
      const geo = garde(new THREE.BufferGeometry());
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      const couleur = aura === 'flammes' ? '#ff8c1a' : aura === 'eclairs' ? '#7df9ff' : '#ff5ce1';
      const pm = garde(new THREE.PointsMaterial({
        color: couleur, size: 0.2, map: garde(texturePoint()), transparent: true,
        opacity: 0.3 + 0.65 * vif, blending: THREE.AdditiveBlending, depthWrite: false,
      }));
      const points = new THREE.Points(geo, pm);
      heros.add(points);
      enMouvement.push((t) => {
        const pos = geo.attributes.position;
        for (let i = 0; i < nb; i++) {
          let y = pos.getY(i) + vitesses[i] * 0.014 * (0.5 + vif);
          if (y > 2.7) y = 0;
          pos.setY(i, y);
          // Elles se resserrent en montant, comme une flamme.
          const r = (0.8 + 0.3 * Math.sin(i)) * (1 - y / 4.5);
          pos.setX(i, Math.cos(angles[i] + t * 0.6) * r);
          pos.setZ(i, Math.sin(angles[i] + t * 0.6) * r);
        }
        pos.needsUpdate = true;
        if (aura === 'arc-en-ciel') pm.color.setHSL((t * 0.12) % 1, 0.95, 0.62);
        if (aura === 'eclairs') pm.opacity = (0.3 + 0.65 * vif) * (0.55 + 0.45 * Math.random());
      });
    }

    heros.traverse((o) => {
      if ((o as THREE.Mesh).isMesh && o !== visage) o.castShadow = true;
    });

    // Les « Z » d'un personnage endormi.
    const zzz: THREE.Sprite[] = [];
    if (fatigue) {
      const zt = document.createElement('canvas');
      zt.width = zt.height = 64;
      const zc = zt.getContext('2d')!;
      zc.font = '900 50px Fredoka, sans-serif';
      zc.lineWidth = 7;
      zc.strokeStyle = '#334155';
      zc.fillStyle = '#ffffff';
      zc.strokeText('Z', 14, 52);
      zc.fillText('Z', 14, 52);
      const zm = garde(new THREE.SpriteMaterial({ map: garde(new THREE.CanvasTexture(zt)), transparent: true, depthWrite: false }));
      for (let i = 0; i < 3; i++) {
        const s = new THREE.Sprite(zm);
        scene.add(s);
        zzz.push(s);
      }
    }

    // ── La taille, le doigt, la boucle ────────────────────────────────────
    const dimensionner = () => {
      const l = conteneur.clientWidth || 300;
      renderer.setSize(l, hauteur);
      camera.aspect = l / hauteur;
      camera.updateProjectionMatrix();
    };
    dimensionner();
    const observateur = new ResizeObserver(dimensionner);
    observateur.observe(conteneur);

    const toile3d = renderer.domElement;
    let depart: { x: number; angle: number; t: number } | null = null;
    const appui = (e: PointerEvent) => {
      depart = { x: e.clientX, angle: angle.current.cible, t: performance.now() };
    };
    const deplace = (e: PointerEvent) => {
      if (!depart || compact) return;
      angle.current.cible = depart.angle + (e.clientX - depart.x) * 0.012;
    };
    const lache = (e: PointerEvent) => {
      if (!depart) return;
      const bouge = Math.abs(e.clientX - depart.x);
      const court = performance.now() - depart.t < 350;
      depart = null;
      if (bouge < 8 && court && !geste.current) {
        const genres = ['saut', 'salut', 'tour'] as const;
        geste.current = { genre: genres[prochainGeste.current % 3], debut: performance.now() };
        prochainGeste.current += 1;
      }
    };
    toile3d.addEventListener('pointerdown', appui);
    window.addEventListener('pointermove', deplace);
    window.addEventListener('pointerup', lache);

    let id = 0;
    let prochainClin = performance.now() + 1800;
    let finClin = 0;
    let regard = 0;
    let regardCible = 0;
    let prochainRegard = performance.now() + 2500;
    let prochainHop = performance.now() + 4000;
    const debut = performance.now();

    const boucle = (maintenant: number) => {
      const t = (maintenant - debut) / 1000;
      const lent = 0.45 + 0.55 * vif;

      // L'arrivée : il surgit en rebondissant.
      const entree = Math.min(1, t / 0.7);
      const rebond = entree < 1 ? 1 + Math.sin(entree * Math.PI * 2.2) * (1 - entree) * 0.35 : 1;
      const echelle = Math.max(0.001, doux(entree) * rebond);

      // Respirer : s'étirer un peu, s'écraser un peu.
      const souffle = Math.sin(t * 2.2 * lent);
      let sx = 1 - souffle * 0.012;
      let sy = 1 + souffle * 0.022;
      let y = 0;
      bras[0].rotation.set(Math.sin(t * 1.6 * lent) * 0.1, 0, -0.12);
      bras[1].rotation.set(-Math.sin(t * 1.6 * lent) * 0.1, 0, 0.12);

      // Regarder autour de lui.
      if (maintenant > prochainRegard) {
        regardCible = (Math.random() - 0.5) * 0.7;
        prochainRegard = maintenant + 2000 + Math.random() * 3000;
      }
      regard += (regardCible - regard) * 0.05;
      tete.rotation.y = regard;
      tete.rotation.x = fatigue ? 0.25 + Math.sin(t * 0.8) * 0.04 : Math.sin(t * 1.1) * 0.03;
      tete.rotation.z = Math.sin(t * 0.9 * lent) * 0.03;

      // De temps en temps, un petit saut de joie quand il est en forme.
      let g = geste.current;
      if (!g && vif >= 0.8 && maintenant > prochainHop) {
        geste.current = { genre: 'saut', debut: maintenant };
        g = geste.current;
        prochainHop = maintenant + 6000 + Math.random() * 5000;
      }

      if (g) {
        const d = (maintenant - g.debut) / 1000;
        if (g.genre === 'saut') {
          // S'accroupir, s'envoler, retomber en s'écrasant.
          if (d < 0.14) {
            const k = d / 0.14;
            sy *= 1 - 0.18 * k;
            sx *= 1 + 0.1 * k;
          } else if (d < 0.66) {
            const k = (d - 0.14) / 0.52;
            y = Math.sin(k * Math.PI) * 0.85;
            sy *= 1 + 0.08 * Math.sin(k * Math.PI);
            bras[0].rotation.z = -2.4 * Math.sin(k * Math.PI);
            bras[1].rotation.z = 2.4 * Math.sin(k * Math.PI);
          } else if (d < 0.86) {
            const k = (d - 0.66) / 0.2;
            const ecrase = Math.sin(k * Math.PI);
            sy *= 1 - 0.16 * ecrase;
            sx *= 1 + 0.1 * ecrase;
          } else geste.current = null;
        } else if (g.genre === 'salut') {
          bras[1].rotation.z = 2.6;
          bras[1].rotation.x = Math.sin(d * 14) * 0.35;
          tete.rotation.z = 0.12;
          if (d > 1.5) geste.current = null;
        } else {
          const k = Math.min(1, d / 0.85);
          heros.rotation.y = angle.current.actuel + doux(k) * Math.PI * 2;
          y = Math.sin(k * Math.PI) * 0.25;
          if (d > 0.85) geste.current = null;
        }
      }
      if (!g || g.genre !== 'tour') {
        const cible = compact ? -0.3 + Math.sin(t * 0.35) * 0.3 : angle.current.cible;
        angle.current.actuel += (cible - angle.current.actuel) * 0.1;
        heros.rotation.y = angle.current.actuel;
      }

      heros.scale.set(echelle * sx, echelle * sy, echelle * sx);
      heros.position.y = y;
      // Le halo se resserre quand il est en l'air : c'est lui qui fait sentir le saut.
      halo.scale.setScalar(1 - y * 0.15);

      // Cligner des yeux.
      if (maintenant > prochainClin && finClin === 0) {
        dessinerVisage(ctx, apparence.peau, 0, humeur);
        texture.needsUpdate = true;
        finClin = maintenant + 130;
      } else if (finClin && maintenant > finClin) {
        dessinerVisage(ctx, apparence.peau, ouvertureRepos, humeur);
        texture.needsUpdate = true;
        finClin = 0;
        prochainClin = maintenant + 2000 + Math.random() * 3000;
      }

      for (const f of enMouvement) f(t);
      zzz.forEach((s, i) => {
        const cycle = (t * 0.45 + i / 3) % 1;
        s.position.set(0.55 + cycle * 0.5, 2.55 + cycle * 0.9, 0.2);
        s.scale.setScalar(0.18 + cycle * 0.2);
        s.material.opacity = Math.sin(cycle * Math.PI);
      });

      renderer.render(scene, camera);
      id = requestAnimationFrame(boucle);
    };
    id = requestAnimationFrame(boucle);

    return () => {
      cancelAnimationFrame(id);
      observateur.disconnect();
      toile3d.removeEventListener('pointerdown', appui);
      window.removeEventListener('pointermove', deplace);
      window.removeEventListener('pointerup', lache);
      const vider = (racine: THREE.Object3D) =>
        racine.traverse((o) => {
          const m = o as THREE.Mesh;
          if (m.geometry) m.geometry.dispose();
          const mats = Array.isArray(m.material) ? m.material : m.material ? [m.material] : [];
          mats.forEach((x) => x.dispose());
        });
      vider(scene);
      vider(studio);
      jetables.forEach((x) => x.dispose());
      renderer.dispose();
      toile3d.remove();
    };
  }, [cle, hauteur, compact]); // eslint-disable-line react-hooks/exhaustive-deps

  if (sansWebGL) {
    return (
      <div style={{ height: hauteur }} className="grid place-items-center rounded-[var(--radius-card)] bg-sand text-kid-sm font-bold text-ink-2">
        Ton personnage a besoin d’un téléphone plus récent pour s’afficher en 3D.
      </div>
    );
  }
  return <div ref={boiteRef} style={{ height: hauteur }} className="w-full select-none" />;
}
