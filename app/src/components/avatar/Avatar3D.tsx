import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import type { Emplacement, ObjetPossede } from '../../lib/avatar';
import { APPARENCE_DEFAUT, type Apparence } from './apparence';

/**
 * Le personnage en 3D.
 *
 * Un ado de jeu vidéo, habillé à la mode de la rue : chemise à col et
 * manches courtes, pantalon large, baskets épaisses, mèches en bataille — et
 * par-dessus, tout ce qu'il a gagné : lunettes, bretelles et cravate,
 * porte-clés peluche, chaîne, chapeaux, cape, ailes, compagnon, aura.
 * Construit dans le code : aucun modèle n'est téléchargé, et le moteur 3D ne
 * se charge que là où il s'affiche.
 *
 * CE QUI LUI DONNE SA QUALITÉ :
 *
 *   des formes arrondies et des vêtements superposés ; un visage peint —
 *   yeux à double reflet, sourcils, joues — avec des paupières qui clignent,
 *   et deux expressions, souriant ou « cool » ;
 *
 *   un éclairage de studio, sombre ou clair : une lumière principale qui
 *   porte une ombre douce, un contre-jour qui détache la silhouette, et des
 *   reflets vrais sur l'or et le métal ;
 *
 *   des animations qui ont du poids : il arrive en rebondissant, respire,
 *   regarde autour de lui, s'accroupit avant de sauter et s'écrase en
 *   retombant ; sa peluche se balance à sa ceinture.
 *
 * L'ÉNERGIE SE VOIT : pleine, il est vif et son podium s'allume ; basse, il
 * baisse la tête, ses paupières tombent et des « Z » s'envolent.
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

type Humeur = 'joie' | 'calme' | 'cool' | 'sommeil';

// ── Le visage ───────────────────────────────────────────────────────────────

/**
 * Le visage, sur une toile transparente : seuls les traits sont peints, la
 * peau est celle de la tête. `ouverture` va de 0 (fermé) à 1 (grand ouvert).
 */
function dessinerVisage(ctx: CanvasRenderingContext2D, peau: string, ouverture: number, humeur: Humeur) {
  const t = ctx.canvas.width;
  ctx.clearRect(0, 0, t, t);

  for (const x of [0.2, 0.8]) {
    const g = ctx.createRadialGradient(t * x, t * 0.66, 0, t * x, t * 0.66, t * 0.11);
    g.addColorStop(0, 'rgba(255,120,110,0.45)');
    g.addColorStop(1, 'rgba(255,120,110,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, t, t);
  }

  // Les sourcils : arqués quand il sourit, droits et un peu bas quand il est cool.
  ctx.strokeStyle = '#1e140d';
  ctx.lineCap = 'round';
  ctx.lineWidth = t * 0.026;
  for (const [i, x] of [0.32, 0.68].entries()) {
    ctx.beginPath();
    const haut = humeur === 'sommeil' ? 0.33 : humeur === 'cool' ? 0.31 : 0.27;
    const pente = humeur === 'cool' ? (i === 0 ? 0.012 : -0.012) : 0;
    ctx.moveTo(t * (x - 0.07), t * (haut + 0.015 - pente));
    ctx.quadraticCurveTo(t * x, t * (haut - (humeur === 'cool' ? 0 : 0.025)), t * (x + 0.07), t * (haut + 0.015 + pente));
    ctx.stroke();
  }

  for (const x of [0.32, 0.68]) {
    const cx = t * x;
    const cy = t * 0.45;
    const rx = t * 0.072;
    const ry = t * 0.095;
    if (ouverture < 0.12) {
      ctx.strokeStyle = '#1b120c';
      ctx.lineWidth = t * 0.028;
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

  if (humeur === 'joie') {
    ctx.fillStyle = '#5a1a14';
    ctx.beginPath();
    ctx.moveTo(t * 0.41, t * 0.67);
    ctx.quadraticCurveTo(t * 0.5, t * 0.79, t * 0.59, t * 0.67);
    ctx.closePath();
    ctx.fill();
    ctx.fillStyle = '#f07a7a';
    ctx.beginPath();
    ctx.ellipse(t * 0.5, t * 0.735, t * 0.04, t * 0.022, 0, 0, Math.PI * 2);
    ctx.fill();
  } else {
    ctx.strokeStyle = '#4a1a12';
    ctx.lineWidth = t * 0.024;
    ctx.beginPath();
    if (humeur === 'sommeil') ctx.ellipse(t * 0.5, t * 0.7, t * 0.025, t * 0.03, 0, 0, Math.PI * 2);
    else if (humeur === 'cool') {
      // Une petite moue en coin.
      ctx.moveTo(t * 0.45, t * 0.7);
      ctx.quadraticCurveTo(t * 0.5, t * 0.685, t * 0.56, t * 0.69);
    } else ctx.arc(t * 0.5, t * 0.63, t * 0.07, 0.2 * Math.PI, 0.8 * Math.PI);
    ctx.stroke();
  }
}

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
/** Un nombre tiré d'un entier, toujours le même : la coiffure ne change pas d'une fois sur l'autre. */
const graine = (i: number) => {
  const s = Math.sin(i * 12.9898) * 43758.5453;
  return s - Math.floor(s);
};

export default function Avatar3D({ equipement, energie, apparence = APPARENCE_DEFAUT, hauteur = 320, compact = false }: Props) {
  const boiteRef = useRef<HTMLDivElement | null>(null);
  const [sansWebGL, setSansWebGL] = useState(false);
  const geste = useRef<{ genre: 'saut' | 'salut' | 'tour'; debut: number } | null>(null);
  const prochainGeste = useRef(0);
  const angle = useRef({ cible: -0.3, actuel: -0.3 });
  const a = { ...APPARENCE_DEFAUT, ...apparence };

  const cle = JSON.stringify([
    Object.values(equipement).map((o) => o && o.id + (o.eteint ? '-eteint' : '')),
    a,
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
    renderer.toneMappingExposure = a.fond !== 'clair' ? 1.15 : 1.05;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    conteneur.appendChild(renderer.domElement);
    renderer.domElement.style.display = 'block';
    renderer.domElement.style.touchAction = compact ? 'auto' : 'none';

    const scene = new THREE.Scene();
    const pmrem = new THREE.PMREMGenerator(renderer);
    const studio = new RoomEnvironment();
    const envTex = pmrem.fromScene(studio, 0.04).texture;
    scene.environment = envTex;

    const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 50);
    camera.position.set(0, compact ? 1.9 : 1.95, compact ? 6.3 : 6.8);
    camera.lookAt(0, 1.5, 0);

    const vif = energie / 100;
    const fatigue = energie <= 40;
    const sombre = a.fond !== 'clair';

    scene.add(new THREE.HemisphereLight('#fff4e0', sombre ? '#22242a' : '#6b4a2a', (sombre ? 0.45 : 0.55) + 0.35 * vif));
    const principale = new THREE.DirectionalLight('#fff3e0', 1.8 + 0.8 * vif);
    principale.position.set(1.2, 6, 2.8);
    principale.castShadow = true;
    principale.shadow.mapSize.set(512, 512);
    principale.shadow.camera.left = -2;
    principale.shadow.camera.right = 2;
    principale.shadow.camera.top = 3.5;
    principale.shadow.camera.bottom = -1;
    principale.shadow.radius = 4;
    principale.shadow.bias = -0.0015;
    scene.add(principale);
    const contreJour = new THREE.DirectionalLight(sombre ? '#cfe4ff' : '#9fd8ff', sombre ? 2.2 : 1.4);
    contreJour.position.set(-3, 3.5, -4);
    scene.add(contreJour);

    const jetables: Array<{ dispose: () => void }> = [envTex, pmrem];
    const garde = <T extends { dispose: () => void }>(x: T) => {
      jetables.push(x);
      return x;
    };
    const mat = (couleur: string, extra: Partial<THREE.MeshPhysicalMaterialParameters> = {}) =>
      garde(new THREE.MeshPhysicalMaterial({ color: couleur, roughness: 0.6, metalness: 0, ...extra }));
    const arrondi = (l: number, h: number, p: number, r: number) => garde(new RoundedBoxGeometry(l, h, p, 4, r));
    const sphere = (r: number) => garde(new THREE.SphereGeometry(r, 28, 20));
    const capsule = (r: number, l: number) => garde(new THREE.CapsuleGeometry(r, l, 8, 16));
    const or = (brille = true) =>
      mat(OR, { metalness: 0.9, roughness: 0.22, emissive: '#6b4a00', emissiveIntensity: brille ? 0.35 : 0, clearcoat: 0.6 });

    // ── Le podium ───────────────────────────────────────────────────────────
    const sol = new THREE.Mesh(garde(new THREE.CircleGeometry(1.05, 48)), garde(new THREE.ShadowMaterial({ opacity: sombre ? 0.4 : 0.22 })));
    sol.rotation.x = -Math.PI / 2;
    sol.position.y = 0.002;
    sol.receiveShadow = true;
    scene.add(sol);
    const podium = new THREE.Mesh(
      garde(new THREE.CylinderGeometry(1.05, 1.15, 0.14, 48)),
      mat(a.fond === 'gris' ? '#5d6066' : sombre ? '#3a3d45' : '#fff3dc', { roughness: 0.35, clearcoat: 0.5 }),
    );
    podium.position.y = -0.07;
    podium.receiveShadow = true;
    scene.add(podium);
    const halo = new THREE.Mesh(
      garde(new THREE.TorusGeometry(1.1, 0.03, 12, 64)),
      mat(energie >= 60 ? '#ffd166' : energie > 0 ? '#ff9f43' : '#9aa3ad', {
        emissive: energie >= 60 ? '#ffb000' : '#ff7a00', emissiveIntensity: 1.3 * vif,
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

    const peau = mat(a.peau, { roughness: 0.55, sheen: 0.3, sheenColor: new THREE.Color('#ffd9c0') });
    const corpsObjet = equipement.corps?.id;
    const haut =
      corpsObjet === 'armure' ? mat('#c9d1db', { metalness: 0.85, roughness: 0.28, clearcoat: 0.5 })
        : corpsObjet === 'tenue-or' ? or(!equipement.corps?.eteint)
          : corpsObjet === 'maillot' ? mat('#17803d', { roughness: 0.7 })
            : mat(a.haut, { roughness: 0.7, sheen: 0.6, sheenColor: new THREE.Color('#ffffff') });
    const bas = mat(a.bas, { roughness: 0.85, sheen: 0.5, sheenColor: new THREE.Color('#6b7280') });

    // Les baskets, épaisses.
    const pieds = equipement.pieds?.id;
    for (const x of [-0.2, 0.2]) {
      const chaussure = new THREE.Mesh(
        arrondi(0.34, pieds === 'bottes' ? 0.4 : 0.22, 0.52, 0.1),
        pieds === 'bottes'
          ? mat('#1d9bf0', { emissive: '#38bdf8', emissiveIntensity: 0.5 * vif, clearcoat: 0.8 })
          : pieds === 'baskets' ? mat('#f8fafc', { clearcoat: 0.6 }) : mat('#eef0f3', { roughness: 0.5 }),
      );
      chaussure.position.set(x, pieds === 'bottes' ? 0.2 : 0.13, 0.06);
      const semelle = new THREE.Mesh(arrondi(0.36, 0.07, 0.54, 0.03), mat(pieds === 'baskets' ? '#e63946' : '#d1d5db'));
      semelle.position.set(x, 0.035, 0.06);
      corps.add(chaussure, semelle);
    }
    // Le pantalon très large : il tombe droit, puis s'entasse en plis sur
    // les baskets ; une poche cargo sur le côté de chaque jambe.
    for (const cote of [-1, 1]) {
      const x = cote * 0.21;
      const haut_ = new THREE.Mesh(arrondi(0.41, 0.62, 0.48, 0.09), bas);
      haut_.position.set(x, 0.8, 0);
      const tas = new THREE.Mesh(arrondi(0.47, 0.32, 0.55, 0.12), bas);
      tas.position.set(x, 0.36, 0.01);
      corps.add(haut_, tas);
      for (const [y, l] of [[0.52, 0.47], [0.3, 0.5]] as const) {
        const pli = new THREE.Mesh(arrondi(l, 0.05, l + 0.08, 0.025), bas);
        pli.position.set(x, y, 0.01);
        pli.rotation.z = cote * 0.04;
        corps.add(pli);
      }
      const poche = new THREE.Mesh(arrondi(0.05, 0.24, 0.26, 0.02), bas);
      poche.position.set(x + cote * 0.225, 0.74, 0);
      const rabat = new THREE.Mesh(arrondi(0.06, 0.06, 0.28, 0.02), bas);
      rabat.position.set(x + cote * 0.23, 0.87, 0);
      corps.add(poche, rabat);
    }
    const bassin = new THREE.Mesh(arrondi(0.82, 0.3, 0.46, 0.08), bas);
    bassin.position.y = 1.16;
    corps.add(bassin);
    // La ceinture, ses passants et sa boucle : elle fait partie de la tenue.
    const noirCeinture = mat('#141414', { roughness: 0.45, clearcoat: 0.3 });
    const ceinture = new THREE.Mesh(arrondi(0.86, 0.08, 0.5, 0.03), noirCeinture);
    ceinture.position.y = 1.29;
    corps.add(ceinture);
    for (const x of [-0.3, -0.12, 0.12, 0.3]) {
      const passant = new THREE.Mesh(arrondi(0.04, 0.11, 0.02, 0.008), bas);
      passant.position.set(x, 1.29, 0.255);
      corps.add(passant);
    }
    const boucleCeinture = new THREE.Mesh(arrondi(0.11, 0.08, 0.03, 0.012), mat('#d1d5db', { metalness: 0.9, roughness: 0.25 }));
    boucleCeinture.position.set(0, 1.29, 0.262);
    corps.add(boucleCeinture);

    // Le torse : un bloc carré aux angles arrondis, large aux épaules.
    const torse = new THREE.Mesh(arrondi(0.9, 0.82, 0.46, 0.1), haut);
    torse.position.y = 1.62;
    corps.add(torse);
    if (!corpsObjet) {
      // Le col de chemise, la patte de boutonnage et ses boutons.
      for (const s of [-1, 1]) {
        const pan = new THREE.Mesh(arrondi(0.2, 0.13, 0.04, 0.02), haut);
        pan.position.set(s * 0.1, 1.98, 0.22);
        pan.rotation.z = s * 0.55;
        corps.add(pan);
      }
      const patte = new THREE.Mesh(arrondi(0.07, 0.7, 0.02, 0.008), mat('#e5e7eb'));
      patte.position.set(0, 1.62, 0.232);
      corps.add(patte);
      for (let i = 0; i < 4; i++) {
        const bouton = new THREE.Mesh(sphere(0.02), mat('#9ca3af', { clearcoat: 1 }));
        bouton.position.set(0, 1.88 - i * 0.17, 0.245);
        corps.add(bouton);
      }
    } else if (corpsObjet === 'maillot') {
      const jaune = new THREE.Mesh(arrondi(0.92, 0.1, 0.48, 0.04), mat('#ffc93c'));
      jaune.position.y = 1.7;
      const rouge = new THREE.Mesh(arrondi(0.92, 0.07, 0.48, 0.03), mat('#e63946'));
      rouge.position.y = 1.6;
      corps.add(jaune, rouge);
    } else if (corpsObjet === 'armure') {
      const plastron = new THREE.Mesh(arrondi(0.62, 0.52, 0.1, 0.06), mat('#e2e8f0', { metalness: 0.9, roughness: 0.2, clearcoat: 1 }));
      plastron.position.set(0, 1.64, 0.24);
      const embleme = new THREE.Mesh(garde(new THREE.ExtrudeGeometry(etoileForme(0.11), { depth: 0.03, bevelEnabled: false })), or());
      embleme.position.set(0, 1.64, 0.29);
      corps.add(plastron, embleme);
    }

    // Les bras en blocs : une manche courte, le bras, et une main en bloc
    // avec son pouce.
    const bras: THREE.Group[] = [];
    for (const cote of [-1, 1]) {
      const epaule = new THREE.Group();
      epaule.position.set(cote * 0.6, 1.94, 0);
      const manche = new THREE.Mesh(arrondi(0.3, 0.34, 0.4, 0.08), haut);
      manche.position.y = -0.13;
      const avantBras = new THREE.Mesh(arrondi(0.27, 0.5, 0.3, 0.07), corpsObjet ? haut : peau);
      avantBras.position.y = -0.5;
      if (corpsObjet === 'armure') {
        const epauliere = new THREE.Mesh(arrondi(0.36, 0.14, 0.44, 0.06), mat('#e2e8f0', { metalness: 0.9, roughness: 0.2 }));
        epauliere.position.y = 0.04;
        epaule.add(epauliere);
      }
      const main = new THREE.Group();
      main.position.set(0, -0.88, 0.02);
      const paume = new THREE.Mesh(arrondi(0.27, 0.27, 0.3, 0.09), peau);
      const pouce = new THREE.Mesh(arrondi(0.09, 0.15, 0.11, 0.04), peau);
      pouce.position.set(-cote * 0.13, 0.03, 0.08);
      pouce.rotation.z = cote * 0.35;
      main.add(paume, pouce);
      epaule.add(manche, avantBras, main);
      corps.add(epaule);
      bras.push(epaule);
    }

    // La tête.
    const tete = new THREE.Group();
    tete.position.y = 2.02;
    corps.add(tete);
    const cou = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.15, 0.15, 0.12, 20)), peau);
    cou.position.y = 0.02;
    tete.add(cou);
    const crane = new THREE.Mesh(arrondi(0.86, 0.8, 0.78, 0.22), peau);
    crane.position.y = 0.42;
    tete.add(crane);
    for (const cote of [-1, 1]) {
      const oreille = new THREE.Mesh(sphere(0.1), peau);
      oreille.scale.set(0.6, 1, 0.9);
      oreille.position.set(cote * 0.44, 0.42, 0);
      tete.add(oreille);
    }
    const toile = document.createElement('canvas');
    toile.width = toile.height = 256;
    const ctx = toile.getContext('2d')!;
    const texture = garde(new THREE.CanvasTexture(toile));
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.anisotropy = 4;
    const visage = new THREE.Mesh(
      garde(new THREE.PlaneGeometry(0.74, 0.68)),
      garde(new THREE.MeshStandardMaterial({ map: texture, transparent: true, roughness: 0.5, polygonOffset: true, polygonOffsetFactor: -2 })),
    );
    visage.position.set(0, 0.4, 0.392);
    tete.add(visage);
    const humeur: Humeur = fatigue ? 'sommeil' : a.expression === 'cool' ? 'cool' : vif >= 0.8 ? 'joie' : 'calme';
    const ouvertureRepos = fatigue ? 0.35 : humeur === 'cool' ? 0.68 : 1;
    dessinerVisage(ctx, a.peau, ouvertureRepos, humeur);
    texture.needsUpdate = true;

    // ── Les cheveux ─────────────────────────────────────────────────────────
    const chapeau = equipement.tete?.id;
    const couvreChef = chapeau === 'casquette' || chapeau === 'chapeau' || chapeau === 'capuche';
    // Mats : un reflet trop vif sur des cheveux sombres les fait paraître gris.
    const cheveux = mat(a.cheveux, { roughness: 0.85, sheen: 0.25, sheenColor: new THREE.Color('#3a2a1e') });
    const coiffure = new THREE.Group();
    tete.add(coiffure);
    if (a.coiffure === 'meches') {
      // Une tignasse : un volume de touffes au-dessus de la tête, des
      // dizaines de mèches fines et pointues qui partent dans tous les sens,
      // et une longue frange qui tombe sur le front.
      const haut3 = new THREE.Vector3(0, 1, 0);
      const meche = garde(new THREE.ConeGeometry(0.065, 1, 10));
      meche.translate(0, 0.5, 0); // la base à l'origine : la mèche pousse depuis sa racine
      const pousser = (x: number, y: number, z: number, dir: THREE.Vector3, longueur: number, epais = 1) => {
        const m = new THREE.Mesh(meche, cheveux);
        m.position.set(x, y, z);
        m.quaternion.setFromUnitVectors(haut3, dir.clone().normalize());
        m.scale.set(epais, longueur, epais);
        coiffure.add(m);
      };
      if (!couvreChef) {
        const calotte = new THREE.Mesh(sphere(0.47), cheveux);
        calotte.scale.set(1.08, 0.82, 1.08);
        calotte.position.set(0, 0.68, -0.04);
        coiffure.add(calotte);
        const touffe = garde(new THREE.SphereGeometry(0.1, 14, 10));
        for (let i = 0; i < 16; i++) {
          const az = (i / 16) * Math.PI * 2;
          const el = 0.35 + graine(i + 100) * 0.9;
          // Pas de touffe basse sur le devant : le visage reste dégagé.
          if (Math.sin(az) > 0.6 && el < 0.7) continue;
          const t = new THREE.Mesh(touffe, cheveux);
          t.position.set(Math.cos(el) * Math.cos(az) * 0.5, 0.66 + Math.sin(el) * 0.38, Math.cos(el) * Math.sin(az) * 0.48 - 0.04);
          t.scale.set(2.1, 1.5, 2.1);
          coiffure.add(t);
        }
        // Les pointes en bataille, sur tout le volume.
        for (let i = 0; i < 30; i++) {
          const az = graine(i + 200) * Math.PI * 2;
          const el = 0.15 + graine(i + 300) * 1.3;
          if (Math.sin(az) > 0.55 && el < 0.55) continue;
          const nx = Math.cos(el) * Math.cos(az);
          const ny = Math.sin(el);
          const nz = Math.cos(el) * Math.sin(az);
          // Les mèches du dessus se dressent, celles des côtés retombent.
          const dir = new THREE.Vector3(nx + (graine(i) - 0.5) * 0.6, ny - (1 - ny) * 0.9, nz + (graine(i + 1) - 0.5) * 0.6);
          pousser(nx * 0.46, 0.66 + ny * 0.34, nz * 0.44 - 0.04, dir, 0.28 + graine(i + 400) * 0.24, 0.9 + graine(i + 500) * 0.5);
        }
      }
      // La frange : de longues mèches qui tombent sur le front, de travers,
      // jusqu'au ras des yeux — une plus longue d'un côté.
      for (let i = 0; i < 8; i++) {
        const x = -0.33 + i * 0.094;
        const longue = i === 5;
        pousser(
          x, couvreChef ? 0.7 : 0.78, couvreChef ? 0.37 : 0.33,
          new THREE.Vector3((graine(i + 600) - 0.5) * 0.7 + (x > 0 ? 0.15 : -0.15), -1, 0.28),
          (couvreChef ? (longue ? 0.22 : 0.15) : longue ? 0.42 : 0.3) + graine(i + 700) * 0.06,
          1.3,
        );
      }
      // Les côtés, qui couvrent le haut des oreilles, et la nuque — sauf
      // sous une capuche, qui les cache.
      for (const cote of chapeau === 'capuche' ? [] : [-1, 1]) {
        for (let i = 0; i < 4; i++) {
          pousser(cote * 0.44, 0.74, 0.18 - i * 0.14, new THREE.Vector3(cote * 0.25, -1, (graine(i + cote * 9) - 0.5) * 0.3), 0.32 + graine(i + 800) * 0.1, 1.4);
        }
      }
      for (let i = 0; i < (chapeau === 'capuche' ? 0 : 6); i++) {
        pousser(-0.3 + i * 0.12, 0.72, -0.4, new THREE.Vector3((graine(i + 900) - 0.5) * 0.4, -1, -0.3), 0.36 + graine(i + 950) * 0.1, 1.5);
      }
    } else if (a.coiffure === 'boucles') {
      for (let ix = -2; ix <= 2; ix++) {
        for (let iz = -2; iz <= 1; iz++) {
          if (couvreChef) continue;
          const n = (ix + 3) * 10 + iz;
          const b = new THREE.Mesh(sphere(0.16 + graine(n) * 0.03), cheveux);
          b.position.set(ix * 0.165, 0.8 + graine(n + 1) * 0.04 - Math.abs(ix) * 0.02, iz * 0.165 - 0.02);
          coiffure.add(b);
        }
      }
      for (let ix = -2; ix <= 2; ix++) {
        if (!couvreChef) {
          const f = new THREE.Mesh(sphere(0.11), cheveux);
          f.position.set(ix * 0.165, 0.76, 0.27);
          coiffure.add(f);
        }
        const nuque = new THREE.Mesh(sphere(0.14), cheveux);
        nuque.position.set(ix * 0.165, 0.6, -0.32);
        coiffure.add(nuque);
      }
    } else {
      const ras = new THREE.Mesh(sphere(0.44), cheveux);
      ras.scale.set(1, 0.6, 1);
      ras.position.set(0, 0.62, -0.04);
      coiffure.add(ras);
    }

    // ── Les objets ────────────────────────────────────────────────────────
    const enMouvement: Array<(t: number) => void> = [];

    // La tête.
    if (chapeau === 'casquette') {
      const dome = new THREE.Mesh(garde(new THREE.SphereGeometry(0.46, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2)), mat('#e63946', { roughness: 0.6 }));
      dome.scale.set(1, 0.75, 1);
      dome.position.y = 0.62;
      const visiere = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.3, 0.3, 0.04, 32)), mat('#c1121f'));
      visiere.scale.set(1.15, 1, 0.9);
      visiere.position.set(0, 0.65, 0.4);
      visiere.rotation.x = 0.12;
      const bouton = new THREE.Mesh(sphere(0.045), mat('#c1121f'));
      bouton.position.y = 0.97;
      tete.add(dome, visiere, bouton);
    } else if (chapeau === 'bandeau') {
      const b = new THREE.Mesh(garde(new THREE.TorusGeometry(0.42, 0.05, 12, 40)), mat('#e63946'));
      b.rotation.x = Math.PI / 2;
      b.scale.set(1, 0.92, 1);
      b.position.y = 0.66;
      tete.add(b);
      for (const s of [-1, 1]) {
        const pan = new THREE.Mesh(arrondi(0.07, 0.28, 0.04, 0.02), mat('#e63946'));
        pan.position.set(s * 0.07, 0.52, -0.42);
        pan.rotation.z = s * 0.4;
        tete.add(pan);
        enMouvement.push((t) => {
          pan.rotation.x = 0.3 + Math.sin(t * 4 + s) * 0.15;
        });
      }
    } else if (chapeau === 'chapeau') {
      const bord = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.72, 0.75, 0.05, 48)), mat('#b88a4a', { roughness: 0.85 }));
      bord.position.y = 0.76;
      const calotteC = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.36, 0.43, 0.32, 40)), mat('#cfa463', { roughness: 0.85 }));
      calotteC.position.y = 0.94;
      const ruban = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.435, 0.435, 0.08, 40)), mat('#5a3b1c'));
      ruban.position.y = 0.82;
      tete.add(bord, calotteC, ruban);
    } else if (chapeau === 'couronne') {
      const brille = !equipement.tete?.eteint;
      const m = or(brille);
      const anneau = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.36, 0.38, 0.16, 40, 1, true)), m);
      anneau.position.y = 1.0;
      tete.add(anneau);
      const gemmes = ['#e63946', '#3a86ff', '#2ec4b6', '#e63946', '#8338ec'];
      for (let i = 0; i < 5; i++) {
        const ang = (i / 5) * Math.PI * 2 + Math.PI / 2;
        const pointe = new THREE.Mesh(garde(new THREE.ConeGeometry(0.075, 0.22, 12)), m);
        pointe.position.set(Math.cos(ang) * 0.36, 1.18, Math.sin(ang) * 0.36);
        const gemme = new THREE.Mesh(sphere(0.05), mat(gemmes[i], { roughness: 0.05, clearcoat: 1, emissive: gemmes[i], emissiveIntensity: brille ? 0.6 : 0 }));
        gemme.position.set(Math.cos(ang) * 0.36, 1.3, Math.sin(ang) * 0.36);
        tete.add(pointe, gemme);
      }
    }

    if (chapeau === 'capuche') {
      // Une capuche ouverte sur le visage, et deux oreilles pointues.
      const tissu = mat('#1c1c20', { roughness: 0.45, clearcoat: 0.35, side: THREE.DoubleSide });
      const capuche = new THREE.Mesh(
        garde(new THREE.SphereGeometry(0.64, 40, 28, Math.PI * 0.8, Math.PI * 1.4, 0, Math.PI * 0.84)),
        tissu,
      );
      capuche.scale.set(1.04, 1.06, 1.02);
      capuche.position.set(0, 0.44, -0.06);
      tete.add(capuche);
      for (const cote of [-1, 1]) {
        const oreille = new THREE.Mesh(garde(new THREE.ConeGeometry(0.13, 0.32, 4)), tissu);
        oreille.position.set(cote * 0.32, 1.1, -0.06);
        oreille.rotation.set(0, Math.PI / 4, cote * -0.35);
        const dedans = new THREE.Mesh(garde(new THREE.ConeGeometry(0.07, 0.2, 4)), mat('#3a3a40'));
        dedans.position.set(cote * 0.32, 1.08, 0.02);
        dedans.rotation.set(0, Math.PI / 4, cote * -0.35);
        tete.add(oreille, dedans);
      }
    }

    // Le visage : des lunettes rondes, ou de soleil, ou un cache-cou.
    const lunettes = equipement.visage?.id;
    if (lunettes === 'cache-cou') {
      // Il couvre la bouche et le menton, comme sur les tenues de rue.
      const masque = new THREE.Mesh(
        garde(new THREE.CylinderGeometry(0.47, 0.48, 0.34, 40, 1, true, -0.95, 1.9)),
        mat('#18181b', { roughness: 0.6, side: THREE.DoubleSide, sheen: 0.4 }),
      );
      masque.position.set(0, 0.24, -0.04);
      tete.add(masque);
      const couture = new THREE.Mesh(arrondi(0.015, 0.3, 0.02, 0.006), mat('#2a2a2e'));
      couture.position.set(0, 0.24, 0.435);
      tete.add(couture);
    } else if (lunettes) {
      const soleil = lunettes === 'lunettes-soleil';
      const monture = mat(soleil ? '#111827' : '#1f1f1f', { metalness: 0.6, roughness: 0.3 });
      for (const s of [-1, 1]) {
        const cercle = new THREE.Mesh(garde(new THREE.TorusGeometry(0.1, 0.014, 10, 32)), monture);
        cercle.position.set(s * 0.13, 0.43, 0.41);
        tete.add(cercle);
        const verre = new THREE.Mesh(
          garde(new THREE.CircleGeometry(0.1, 32)),
          soleil
            ? mat('#0b1220', { metalness: 0.3, roughness: 0.05, clearcoat: 1, transparent: true, opacity: 0.92 })
            : mat('#ffffff', { roughness: 0.02, transparent: true, opacity: 0.12, clearcoat: 1 }),
        );
        verre.position.set(s * 0.13, 0.43, 0.412);
        tete.add(verre);
        const branche = new THREE.Mesh(arrondi(0.02, 0.02, 0.36, 0.008), monture);
        branche.position.set(s * 0.235, 0.44, 0.22);
        tete.add(branche);
      }
      const pont = new THREE.Mesh(arrondi(0.06, 0.015, 0.015, 0.006), monture);
      pont.position.set(0, 0.45, 0.415);
      tete.add(pont);
    }

    // Les accessoires.
    const accessoire = equipement.accessoire?.id;
    if (accessoire === 'bretelles') {
      const noir = mat('#111111', { roughness: 0.45, clearcoat: 0.3 });
      for (const s of [-1, 1]) {
        const devant = new THREE.Mesh(arrondi(0.07, 0.62, 0.03, 0.012), noir);
        devant.position.set(s * 0.2, 1.62, 0.262);
        devant.rotation.z = s * 0.06;
        const derriere = devant.clone();
        derriere.position.z = -0.262;
        const boucle = new THREE.Mesh(arrondi(0.09, 0.06, 0.03, 0.01), mat('#cbd5e1', { metalness: 0.9, roughness: 0.25 }));
        boucle.position.set(s * 0.2, 1.42, 0.27);
        corps.add(devant, derriere, boucle);
      }
      const cravate = new THREE.Mesh(arrondi(0.07, 0.42, 0.025, 0.01), noir);
      cravate.position.set(0, 1.74, 0.262);
      const noeud = new THREE.Mesh(arrondi(0.09, 0.07, 0.04, 0.015), noir);
      noeud.position.set(0, 1.95, 0.262);
      corps.add(cravate, noeud);
    } else if (accessoire === 'bandouliere') {
      // Une sangle en travers, de l'épaule à la hanche, devant et derrière,
      // avec sa boucle carrée.
      const sangle = mat('#121212', { roughness: 0.4, clearcoat: 0.4 });
      const argent = mat('#d1d5db', { metalness: 0.9, roughness: 0.25 });
      for (const z of [0.25, -0.25]) {
        const bande = new THREE.Mesh(arrondi(0.09, 1.0, 0.03, 0.012), sangle);
        bande.position.set(0.02, 1.62, z);
        bande.rotation.z = z > 0 ? 0.62 : -0.62;
        corps.add(bande);
      }
      const epaule = new THREE.Mesh(arrondi(0.1, 0.04, 0.52, 0.015), sangle);
      epaule.position.set(-0.3, 2.04, 0);
      corps.add(epaule);
      const cadre = new THREE.Mesh(arrondi(0.13, 0.13, 0.03, 0.02), argent);
      cadre.position.set(-0.08, 1.72, 0.27);
      cadre.rotation.z = 0.62;
      const trou = new THREE.Mesh(arrondi(0.07, 0.07, 0.035, 0.01), sangle);
      trou.position.set(-0.08, 1.72, 0.275);
      trou.rotation.z = 0.62;
      corps.add(cadre, trou);
    } else if (accessoire === 'chaine-or') {
      const brille = !equipement.accessoire?.eteint;
      const chaine = new THREE.Mesh(garde(new THREE.TorusGeometry(0.24, 0.018, 8, 40)), or(brille));
      chaine.rotation.x = Math.PI / 2 - 0.35;
      chaine.position.set(0, 1.86, 0.08);
      const pendentif = new THREE.Mesh(
        garde(new THREE.ExtrudeGeometry(etoileForme(0.07), { depth: 0.02, bevelEnabled: true, bevelSize: 0.01, bevelThickness: 0.01 })),
        or(brille),
      );
      pendentif.position.set(0, 1.72, 0.27);
      corps.add(chaine, pendentif);
    }
    if (accessoire === 'porte-cles' || accessoire === 'bretelles') {
      // La peluche pend à la ceinture, sur la hanche, et se balance.
      const attache = new THREE.Group();
      attache.position.set(0.3, 1.24, 0.27);
      corps.add(attache);
      const anneau = new THREE.Mesh(garde(new THREE.TorusGeometry(0.035, 0.008, 8, 16)), mat('#cbd5e1', { metalness: 0.9, roughness: 0.25 }));
      attache.add(anneau);
      const ours = new THREE.Group();
      ours.position.y = -0.17;
      attache.add(ours);
      const blanc = mat('#fbfbfb', { roughness: 0.9, sheen: 1, sheenColor: new THREE.Color('#ffffff') });
      const teteO = new THREE.Mesh(sphere(0.075), blanc);
      teteO.position.y = 0.04;
      const corpsO = new THREE.Mesh(sphere(0.06), blanc);
      corpsO.scale.set(1, 1.1, 0.9);
      corpsO.position.y = -0.06;
      ours.add(teteO, corpsO);
      for (const s of [-1, 1]) {
        const oreille = new THREE.Mesh(sphere(0.028), blanc);
        oreille.position.set(s * 0.05, 0.1, 0);
        const oeil = new THREE.Mesh(sphere(0.011), mat('#111111'));
        oeil.position.set(s * 0.026, 0.05, 0.068);
        ours.add(oreille, oeil);
      }
      enMouvement.push((t) => {
        attache.rotation.z = Math.sin(t * 3.2) * 0.25;
        attache.rotation.x = Math.sin(t * 2.1) * 0.12;
      });
    }

    // Le dos.
    const dos = equipement.dos?.id;
    if (dos === 'sac') {
      const sac = new THREE.Mesh(arrondi(0.62, 0.66, 0.28, 0.12), mat('#a0642e', { roughness: 0.8 }));
      sac.position.set(0, 1.6, -0.4);
      const poche = new THREE.Mesh(arrondi(0.42, 0.22, 0.1, 0.05), mat('#8b5524'));
      poche.position.set(0, 1.45, -0.56);
      corps.add(sac, poche);
      if (accessoire !== 'bretelles') {
        for (const s of [-1, 1]) {
          const bretelle = new THREE.Mesh(arrondi(0.08, 0.6, 0.05, 0.02), mat('#8b5524'));
          bretelle.position.set(s * 0.25, 1.65, 0.265);
          corps.add(bretelle);
        }
      }
    } else if (dos === 'cape') {
      const geo = garde(new THREE.PlaneGeometry(0.92, 1.4, 8, 10));
      const cape = new THREE.Mesh(geo, mat('#c1121f', { side: THREE.DoubleSide, roughness: 0.65, sheen: 0.8, sheenColor: new THREE.Color('#ff8a8a') }));
      cape.position.set(0, 1.3, -0.28);
      corps.add(cape);
      for (const s of [-1, 1]) {
        const agrafe = new THREE.Mesh(sphere(0.05), or());
        agrafe.position.set(s * 0.18, 1.98, 0.17);
        corps.add(agrafe);
      }
      const base = geo.attributes.position.array.slice();
      enMouvement.push((t) => {
        const pos = geo.attributes.position;
        for (let i = 0; i < pos.count; i++) {
          const x = base[i * 3];
          const y = base[i * 3 + 1];
          const versLeBas = (0.7 - y) / 1.4;
          pos.setZ(i, -versLeBas * (0.3 + 0.1 * Math.sin(t * 2.5 + y * 4 + x * 2)));
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
        aile.position.set(cote * 0.18, 1.75, -0.28);
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

    // La main.
    const tenu = equipement.main?.id;
    if (tenu === 'livre') {
      const livre = new THREE.Group();
      const couverture = new THREE.Mesh(arrondi(0.32, 0.42, 0.09, 0.03), mat('#3a86ff', { clearcoat: 0.6 }));
      const pages = new THREE.Mesh(arrondi(0.28, 0.38, 0.07, 0.01), mat('#fffaf0'));
      pages.position.x = 0.025;
      const etoile = new THREE.Mesh(garde(new THREE.ExtrudeGeometry(etoileForme(0.07), { depth: 0.01, bevelEnabled: false })), or());
      etoile.position.set(0, 0, 0.05);
      livre.add(pages, couverture, etoile);
      livre.position.set(0, -0.95, 0.2);
      bras[1].add(livre);
    } else if (tenu === 'trophee') {
      const profil = [
        [0, 0], [0.12, 0], [0.12, 0.03], [0.05, 0.06], [0.04, 0.15], [0.08, 0.19], [0.16, 0.27], [0.19, 0.43], [0.18, 0.44], [0, 0.29],
      ].map(([x, y]) => new THREE.Vector2(x, y));
      const coupe = new THREE.Mesh(garde(new THREE.LatheGeometry(profil, 32)), or());
      coupe.position.set(0, -1.08, 0.18);
      bras[1].add(coupe);
    }

    // Le compagnon.
    const compagnon = equipement.compagnon?.id;
    if (compagnon) {
      const ami = new THREE.Group();
      ami.position.set(1.2, 0.55, 0.3);
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
        ami.add(new THREE.Mesh(sphere(0.22), garde(new THREE.MeshPhysicalMaterial({ map: tex, roughness: 0.3, clearcoat: 0.8 }))));
      } else if (compagnon === 'etoile') {
        const e = new THREE.Mesh(
          garde(new THREE.ExtrudeGeometry(etoileForme(0.28), { depth: 0.08, bevelEnabled: true, bevelSize: 0.04, bevelThickness: 0.04, bevelSegments: 3 })),
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
          const ang = (i / 10) * Math.PI * 2;
          const touffe = new THREE.Mesh(sphere(0.1), criniere);
          touffe.position.set(Math.cos(ang) * 0.2, 0.3 + Math.sin(ang) * 0.2, -0.04);
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
        ami.scale.setScalar(1.15);
      }
      enMouvement.push((t) => {
        ami.position.y = 0.45 + Math.abs(Math.sin(t * (2 + 2 * vif))) * 0.3 * (0.4 + vif);
        ami.rotation.y = -0.5 + Math.sin(t * 0.8) * 0.4;
      });
      ami.traverse((o) => {
        if ((o as THREE.Mesh).isMesh) o.castShadow = true;
      });
    }

    // L'aura.
    const aura = equipement.aura?.id;
    if (aura) {
      const nb = 70;
      const positions = new Float32Array(nb * 3);
      const vitesses: number[] = [];
      const angles: number[] = [];
      for (let i = 0; i < nb; i++) {
        const ang = Math.random() * Math.PI * 2;
        angles.push(ang);
        const r = 0.75 + Math.random() * 0.35;
        positions.set([Math.cos(ang) * r, Math.random() * 3, Math.sin(ang) * r], i * 3);
        vitesses.push(0.5 + Math.random() * 0.9);
      }
      const geo = garde(new THREE.BufferGeometry());
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      const couleur = aura === 'flammes' ? '#ff8c1a' : aura === 'eclairs' ? '#7df9ff' : '#ff5ce1';
      const pm = garde(new THREE.PointsMaterial({
        color: couleur, size: 0.2, map: garde(texturePoint()), transparent: true,
        opacity: 0.3 + 0.65 * vif, blending: THREE.AdditiveBlending, depthWrite: false,
      }));
      heros.add(new THREE.Points(geo, pm));
      enMouvement.push((t) => {
        const pos = geo.attributes.position;
        for (let i = 0; i < nb; i++) {
          let y = pos.getY(i) + vitesses[i] * 0.014 * (0.5 + vif);
          if (y > 3.1) y = 0;
          pos.setY(i, y);
          const r = (0.8 + 0.3 * Math.sin(i)) * (1 - y / 5);
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

      const entree = Math.min(1, t / 0.7);
      const rebond = entree < 1 ? 1 + Math.sin(entree * Math.PI * 2.2) * (1 - entree) * 0.35 : 1;
      const echelle = Math.max(0.001, doux(entree) * rebond);

      const souffle = Math.sin(t * 2.2 * lent);
      let sx = 1 - souffle * 0.01;
      let sy = 1 + souffle * 0.018;
      let y = 0;
      bras[0].rotation.set(Math.sin(t * 1.6 * lent) * 0.08, 0, -0.1);
      bras[1].rotation.set(-Math.sin(t * 1.6 * lent) * 0.08, 0, 0.1);

      if (maintenant > prochainRegard) {
        regardCible = (Math.random() - 0.5) * 0.7;
        prochainRegard = maintenant + 2000 + Math.random() * 3000;
      }
      regard += (regardCible - regard) * 0.05;
      tete.rotation.y = regard;
      tete.rotation.x = fatigue ? 0.25 + Math.sin(t * 0.8) * 0.04 : Math.sin(t * 1.1) * 0.03;
      tete.rotation.z = Math.sin(t * 0.9 * lent) * 0.03;

      let g = geste.current;
      if (!g && vif >= 0.8 && maintenant > prochainHop) {
        geste.current = { genre: 'saut', debut: maintenant };
        g = geste.current;
        prochainHop = maintenant + 6000 + Math.random() * 5000;
      }

      if (g) {
        const d = (maintenant - g.debut) / 1000;
        if (g.genre === 'saut') {
          if (d < 0.14) {
            const k = d / 0.14;
            sy *= 1 - 0.15 * k;
            sx *= 1 + 0.08 * k;
          } else if (d < 0.66) {
            const k = (d - 0.14) / 0.52;
            y = Math.sin(k * Math.PI) * 0.8;
            sy *= 1 + 0.06 * Math.sin(k * Math.PI);
            bras[0].rotation.z = -2.4 * Math.sin(k * Math.PI);
            bras[1].rotation.z = 2.4 * Math.sin(k * Math.PI);
          } else if (d < 0.86) {
            const k = (d - 0.66) / 0.2;
            const ecrase = Math.sin(k * Math.PI);
            sy *= 1 - 0.13 * ecrase;
            sx *= 1 + 0.08 * ecrase;
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
      halo.scale.setScalar(1 - y * 0.15);

      if (maintenant > prochainClin && finClin === 0) {
        dessinerVisage(ctx, a.peau, 0, humeur);
        texture.needsUpdate = true;
        finClin = maintenant + 130;
      } else if (finClin && maintenant > finClin) {
        dessinerVisage(ctx, a.peau, ouvertureRepos, humeur);
        texture.needsUpdate = true;
        finClin = 0;
        prochainClin = maintenant + 2000 + Math.random() * 3000;
      }

      for (const f of enMouvement) f(t);
      zzz.forEach((s, i) => {
        const cycle = (t * 0.45 + i / 3) % 1;
        s.position.set(0.5 + cycle * 0.5, 3.0 + cycle * 0.9, 0.2);
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
