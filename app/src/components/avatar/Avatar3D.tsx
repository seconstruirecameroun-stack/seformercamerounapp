import { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import type { Emplacement, ObjetPossede } from '../../lib/avatar';
import { APPARENCE_DEFAUT, type Apparence } from './apparence';

/**
 * Le personnage en 3D : un héros en blocs, construit dans le code.
 *
 * Aucun modèle n'est téléchargé : chaque partie est une boîte, un cylindre
 * ou une sphère, colorée. Le moteur 3D (three.js) n'est chargé que là où le
 * personnage s'affiche, pour ne pas alourdir le reste de l'app sur un
 * téléphone modeste.
 *
 * Il vit : il respire, cligne des yeux, balance les bras, et on le fait
 * tourner du doigt. Un toucher le fait sauter, le suivant le fait saluer, le
 * troisième tourner sur lui-même. Ses objets ont chacun leur petite vie —
 * la cape flotte, les ailes battent, le compagnon sautille, l'aura monte.
 *
 * L'ÉNERGIE SE VOIT. Pleine, il est vif et lumineux ; basse, il respire
 * lentement, baisse la tête, ses yeux se ferment à moitié et des « Z »
 * s'envolent. L'aura pâlit avec elle.
 *
 * Son allure est à lui : un personnage en blocs, aux couleurs du pays, qui
 * n'est celui d'aucun autre jeu.
 */


type Props = {
  equipement: Partial<Record<Emplacement, ObjetPossede>>;
  energie: number;
  apparence?: Apparence;
  /** Hauteur en pixels ; la largeur suit le conteneur. */
  hauteur?: number;
  /** Sur la page d'accueil, il est plus petit, et ne se fait pas tourner. */
  compact?: boolean;
};

const OR = '#f5c542';

function mat(couleur: string, extra: Partial<THREE.MeshStandardMaterialParameters> = {}) {
  return new THREE.MeshStandardMaterial({ color: couleur, roughness: 0.65, metalness: 0.05, ...extra });
}

function boite(l: number, h: number, p: number, m: THREE.Material) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(l, h, p), m);
  return mesh;
}

/** Le visage, dessiné sur une toile et collé sur la face avant de la tête. */
function dessinerVisage(ctx: CanvasRenderingContext2D, peau: string, ouverture: number, content: boolean) {
  const t = ctx.canvas.width;
  ctx.fillStyle = peau;
  ctx.fillRect(0, 0, t, t);
  // Les joues.
  ctx.fillStyle = 'rgba(240,120,110,0.35)';
  ctx.beginPath();
  ctx.arc(t * 0.22, t * 0.66, t * 0.08, 0, Math.PI * 2);
  ctx.arc(t * 0.78, t * 0.66, t * 0.08, 0, Math.PI * 2);
  ctx.fill();
  // Les yeux : ouverture 1 = grands ouverts, 0 = fermés.
  for (const x of [0.32, 0.68]) {
    const cx = t * x;
    const cy = t * 0.45;
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.ellipse(cx, cy, t * 0.09, t * 0.11 * Math.max(0.08, ouverture), 0, 0, Math.PI * 2);
    ctx.fill();
    if (ouverture > 0.2) {
      ctx.fillStyle = '#1b1b1b';
      ctx.beginPath();
      ctx.arc(cx, cy + t * 0.01, t * 0.055 * Math.min(1, ouverture + 0.2), 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(cx + t * 0.02, cy - t * 0.02, t * 0.018, 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.strokeStyle = '#1b1b1b';
      ctx.lineWidth = t * 0.025;
      ctx.beginPath();
      ctx.moveTo(cx - t * 0.07, cy);
      ctx.lineTo(cx + t * 0.07, cy);
      ctx.stroke();
    }
  }
  // La bouche.
  ctx.strokeStyle = '#3b1a12';
  ctx.lineWidth = t * 0.03;
  ctx.lineCap = 'round';
  ctx.beginPath();
  if (content) ctx.arc(t * 0.5, t * 0.66, t * 0.12, 0.15 * Math.PI, 0.85 * Math.PI);
  else {
    ctx.moveTo(t * 0.42, t * 0.74);
    ctx.lineTo(t * 0.58, t * 0.74);
  }
  ctx.stroke();
}

/** Une petite étoile en volume, pour la couronne, le compagnon, l'aura. */
function etoile(rayon: number, epaisseur: number, m: THREE.Material) {
  const forme = new THREE.Shape();
  for (let i = 0; i < 10; i++) {
    const a = (i / 10) * Math.PI * 2 - Math.PI / 2;
    const r = i % 2 ? rayon * 0.45 : rayon;
    const x = Math.cos(a) * r;
    const y = Math.sin(a) * r;
    if (i === 0) forme.moveTo(x, y);
    else forme.lineTo(x, y);
  }
  return new THREE.Mesh(new THREE.ExtrudeGeometry(forme, { depth: epaisseur, bevelEnabled: false }), m);
}

export default function Avatar3D({ equipement, energie, apparence = APPARENCE_DEFAUT, hauteur = 320, compact = false }: Props) {
  const boiteRef = useRef<HTMLDivElement | null>(null);
  const [sansWebGL, setSansWebGL] = useState(false);
  const geste = useRef<{ genre: 'saut' | 'salut' | 'tour'; debut: number } | null>(null);
  const prochainGeste = useRef(0);
  const angle = useRef({ cible: -0.35, actuel: -0.35, glisse: null as number | null });

  // Les objets portés se lisent par identifiant : la scène se reconstruit
  // quand l'enfant change de tenue, pas à chaque rendu.
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
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    } catch {
      setSansWebGL(true);
      return;
    }
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    conteneur.appendChild(renderer.domElement);
    renderer.domElement.style.display = 'block';
    renderer.domElement.style.touchAction = compact ? 'auto' : 'none';

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50);
    camera.position.set(0, 2.0, compact ? 7.0 : 7.6);
    camera.lookAt(0, 1.5, 0);

    const vif = energie / 100;
    scene.add(new THREE.HemisphereLight('#fff6e8', '#5a4632', 0.9 + 0.5 * vif));
    const soleil = new THREE.DirectionalLight('#ffffff', 1.2 + 0.8 * vif);
    soleil.position.set(3, 6, 5);
    scene.add(soleil);
    const contre = new THREE.DirectionalLight('#9fd3ff', 0.5);
    contre.position.set(-4, 3, -3);
    scene.add(contre);

    const jetables: Array<{ dispose: () => void }> = [];
    const garde = <T extends { dispose: () => void }>(x: T) => {
      jetables.push(x);
      return x;
    };

    // ── Le personnage ─────────────────────────────────────────────────────
    const heros = new THREE.Group();
    scene.add(heros);
    const corps = new THREE.Group();
    heros.add(corps);

    const peau = garde(mat(apparence.peau));
    const corpsObjet = equipement.corps?.id;
    const haut = garde(
      corpsObjet === 'armure'
        ? mat('#b8c0ca', { metalness: 0.45, roughness: 0.3 })
        : corpsObjet === 'tenue-or'
          ? mat(OR, { metalness: 0.3, roughness: 0.3, emissive: '#5a4300', emissiveIntensity: equipement.corps?.eteint ? 0 : 0.35 })
          : corpsObjet === 'maillot'
            ? mat('#2f7d32')
            : mat(apparence.haut),
    );
    const bas = garde(mat(apparence.bas));

    // Les jambes.
    const jambes: THREE.Mesh[] = [];
    for (const x of [-0.24, 0.24]) {
      const j = boite(0.4, 0.95, 0.42, bas);
      j.position.set(x, 0.48, 0);
      corps.add(j);
      jambes.push(j);
      const chaussure = boite(
        0.44, 0.22, 0.56,
        garde(equipement.pieds?.id === 'bottes'
          ? mat('#38bdf8', { emissive: '#0ea5e9', emissiveIntensity: 0.4 * vif })
          : equipement.pieds?.id === 'baskets'
            ? mat('#f8fafc')
            : mat('#3b2a1a')),
      );
      chaussure.position.set(x, 0.08, 0.05);
      corps.add(chaussure);
    }
    // Le torse.
    const torse = boite(1.05, 1.05, 0.55, haut);
    torse.position.y = 1.5;
    corps.add(torse);
    if (corpsObjet === 'maillot') {
      // Une bande jaune et rouge : le maillot des Lions.
      const bande = boite(1.07, 0.16, 0.57, garde(mat('#f5c542')));
      bande.position.y = 1.62;
      corps.add(bande);
      const bande2 = boite(1.07, 0.1, 0.57, garde(mat('#d7443a')));
      bande2.position.y = 1.46;
      corps.add(bande2);
    }
    // Les bras, accrochés à l'épaule pour pouvoir tourner.
    const bras: THREE.Group[] = [];
    for (const cote of [-1, 1]) {
      const epaule = new THREE.Group();
      epaule.position.set(cote * 0.7, 1.98, 0);
      const manche = boite(0.34, 0.5, 0.4, haut);
      manche.position.y = -0.22;
      const main = boite(0.32, 0.5, 0.36, peau);
      main.position.y = -0.7;
      epaule.add(manche, main);
      corps.add(epaule);
      bras.push(epaule);
    }

    // La tête et son visage.
    // La tête se pose sur les épaules : le haut du torse est à 2,025.
    const tete = new THREE.Group();
    tete.position.y = 2.03;
    corps.add(tete);
    const toile = document.createElement('canvas');
    toile.width = toile.height = 128;
    const ctx = toile.getContext('2d')!;
    const texture = garde(new THREE.CanvasTexture(toile));
    texture.colorSpace = THREE.SRGBColorSpace;
    const visage = garde(new THREE.MeshStandardMaterial({ map: texture, roughness: 0.7 }));
    const crane = new THREE.Mesh(
      garde(new THREE.BoxGeometry(0.9, 0.9, 0.9)),
      [peau, peau, peau, peau, visage, peau],
    );
    crane.position.y = 0.45;
    tete.add(crane);
    const fatigue = energie <= 40;
    let ouverture = fatigue ? 0.35 : 1;
    dessinerVisage(ctx, apparence.peau, ouverture, !fatigue);
    texture.needsUpdate = true;

    // ── Les objets ────────────────────────────────────────────────────────
    const enMouvement: Array<(t: number) => void> = [];

    const chapeau = equipement.tete?.id;
    if (chapeau === 'casquette') {
      const c = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.47, 0.47, 0.25, 24)), garde(mat('#d7443a')));
      c.position.y = 0.98;
      const visiere = boite(0.7, 0.06, 0.45, garde(mat('#b8352d')));
      visiere.position.set(0, 0.88, 0.55);
      tete.add(c, visiere);
    } else if (chapeau === 'bandeau') {
      const b = boite(0.94, 0.16, 0.94, garde(mat('#d7443a')));
      b.position.y = 0.78;
      const noeud = boite(0.08, 0.3, 0.3, garde(mat('#d7443a')));
      noeud.position.set(0, 0.7, -0.52);
      tete.add(b, noeud);
    } else if (chapeau === 'chapeau') {
      const bord = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.85, 0.85, 0.06, 28)), garde(mat('#b08a4a')));
      bord.position.y = 0.92;
      const calotte = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.42, 0.5, 0.38, 24)), garde(mat('#c9a35c')));
      calotte.position.y = 1.12;
      const ruban = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.505, 0.505, 0.09, 24)), garde(mat('#5a3b1c')));
      ruban.position.y = 0.99;
      tete.add(bord, calotte, ruban);
    } else if (chapeau === 'couronne') {
      const brille = !equipement.tete?.eteint;
      const m = garde(mat(OR, { metalness: 0.3, roughness: 0.3, emissive: '#7a5a00', emissiveIntensity: brille ? 0.6 : 0 }));
      const anneau = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.47, 0.47, 0.2, 24, 1, true)), m);
      anneau.position.y = 0.98;
      tete.add(anneau);
      for (let i = 0; i < 6; i++) {
        const a = (i / 6) * Math.PI * 2;
        const pointe = new THREE.Mesh(garde(new THREE.ConeGeometry(0.09, 0.26, 8)), m);
        pointe.position.set(Math.cos(a) * 0.44, 1.2, Math.sin(a) * 0.44);
        tete.add(pointe);
      }
      const joyau = new THREE.Mesh(garde(new THREE.OctahedronGeometry(0.1)), garde(mat('#d7443a', { emissive: '#d7443a', emissiveIntensity: brille ? 0.6 : 0 })));
      joyau.position.set(0, 1.0, 0.48);
      tete.add(joyau);
    }

    const dos = equipement.dos?.id;
    if (dos === 'sac') {
      const sac = boite(0.8, 0.85, 0.35, garde(mat('#8b5a2b')));
      sac.position.set(0, 1.5, -0.45);
      corps.add(sac);
    } else if (dos === 'cape') {
      const cape = new THREE.Mesh(garde(new THREE.PlaneGeometry(1.1, 1.6, 1, 6)), garde(mat('#b91c1c', { side: THREE.DoubleSide })));
      cape.position.set(0, 1.25, -0.32);
      corps.add(cape);
      const base = (cape.geometry as THREE.PlaneGeometry).attributes.position.array.slice();
      enMouvement.push((t) => {
        const pos = (cape.geometry as THREE.PlaneGeometry).attributes.position;
        for (let i = 0; i < pos.count; i++) {
          const y = base[i * 3 + 1];
          const prof = (0.8 - y) / 1.6;
          pos.setZ(i, -prof * (0.35 + 0.12 * Math.sin(t * 3 + y * 3)));
        }
        pos.needsUpdate = true;
      });
    } else if (dos === 'ailes' || dos === 'ailes-or') {
      const dorees = dos === 'ailes-or';
      const brille = !equipement.dos?.eteint;
      const m = garde(mat(dorees ? OR : '#f8fafc', {
        side: THREE.DoubleSide, transparent: true, opacity: 0.92,
        metalness: dorees ? 0.3 : 0, emissive: dorees ? '#7a5a00' : '#000000', emissiveIntensity: dorees && brille ? 0.5 : 0,
      }));
      const forme = new THREE.Shape();
      forme.moveTo(0, 0);
      forme.quadraticCurveTo(0.6, 0.9, 1.5, 0.8);
      forme.quadraticCurveTo(1.1, 0.4, 1.3, 0.1);
      forme.quadraticCurveTo(0.8, -0.1, 1.0, -0.45);
      forme.quadraticCurveTo(0.4, -0.3, 0, 0);
      const geo = garde(new THREE.ShapeGeometry(forme));
      const ailes: THREE.Mesh[] = [];
      for (const cote of [-1, 1]) {
        const aile = new THREE.Mesh(geo, m);
        aile.scale.x = cote;
        aile.position.set(cote * 0.15, 1.7, -0.32);
        corps.add(aile);
        ailes.push(aile);
      }
      enMouvement.push((t) => {
        const battement = 0.35 + 0.3 * Math.sin(t * (2 + 3 * vif));
        ailes[0].rotation.y = battement;
        ailes[1].rotation.y = -battement;
      });
    }

    const tenu = equipement.main?.id;
    if (tenu === 'livre') {
      const livre = boite(0.42, 0.55, 0.12, garde(mat('#2f6db5')));
      livre.position.set(0, -0.85, 0.25);
      bras[1].add(livre);
    } else if (tenu === 'trophee') {
      const m = garde(mat(OR, { metalness: 0.3, roughness: 0.3, emissive: '#5a4300', emissiveIntensity: 0.3 * vif }));
      const coupe = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.22, 0.1, 0.3, 16)), m);
      coupe.position.set(0, -0.72, 0.3);
      const pied = new THREE.Mesh(garde(new THREE.CylinderGeometry(0.14, 0.14, 0.08, 16)), m);
      pied.position.set(0, -0.92, 0.3);
      bras[1].add(coupe, pied);
    }

    // Le compagnon, à côté de lui.
    const compagnon = equipement.compagnon?.id;
    if (compagnon) {
      const ami = new THREE.Group();
      ami.position.set(1.45, 0.6, 0.3);
      scene.add(ami);
      if (compagnon === 'balle') {
        ami.add(new THREE.Mesh(garde(new THREE.SphereGeometry(0.28, 20, 16)), garde(mat('#f97316'))));
      } else if (compagnon === 'etoile') {
        const e = etoile(0.35, 0.12, garde(mat('#facc15', { emissive: '#facc15', emissiveIntensity: 0.4 * vif })));
        e.position.z = -0.06;
        ami.add(e);
      } else if (compagnon === 'lionceau') {
        const brille = !equipement.compagnon?.eteint;
        const fauve = garde(mat('#e0a040'));
        const criniere = boite(0.62, 0.62, 0.3, garde(mat('#9a5a1c', { emissive: '#7a3a00', emissiveIntensity: brille ? 0.25 : 0 })));
        criniere.position.set(0, 0.25, -0.05);
        const tetel = boite(0.44, 0.44, 0.4, fauve);
        tetel.position.set(0, 0.25, 0.08);
        const corpsl = boite(0.5, 0.36, 0.7, fauve);
        corpsl.position.set(0, -0.1, -0.3);
        ami.add(criniere, tetel, corpsl);
      }
      enMouvement.push((t) => {
        ami.position.y = 0.6 + Math.abs(Math.sin(t * (2 + 2 * vif))) * 0.35 * (0.4 + vif);
        ami.rotation.y = Math.sin(t * 0.8) * 0.6;
      });
    }

    // L'aura : des particules qui montent autour de lui, plus vives avec l'énergie.
    const aura = equipement.aura?.id;
    if (aura) {
      const n = 60;
      const positions = new Float32Array(n * 3);
      const vitesses: number[] = [];
      for (let i = 0; i < n; i++) {
        const a = Math.random() * Math.PI * 2;
        const r = 0.8 + Math.random() * 0.5;
        positions.set([Math.cos(a) * r, Math.random() * 3, Math.sin(a) * r], i * 3);
        vitesses.push(0.4 + Math.random() * 0.8);
      }
      const geo = garde(new THREE.BufferGeometry());
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      const couleur = aura === 'flammes' ? '#ff7a1a' : aura === 'eclairs' ? '#67e8f9' : '#ff4fd8';
      const pm = garde(new THREE.PointsMaterial({
        color: couleur, size: 0.13, transparent: true, opacity: 0.25 + 0.65 * vif,
        blending: THREE.AdditiveBlending, depthWrite: false,
      }));
      const points = new THREE.Points(geo, pm);
      heros.add(points);
      enMouvement.push((t) => {
        const pos = geo.attributes.position;
        for (let i = 0; i < n; i++) {
          let y = pos.getY(i) + vitesses[i] * 0.016 * (0.5 + vif);
          if (y > 3.2) y = 0;
          pos.setY(i, y);
        }
        pos.needsUpdate = true;
        if (aura === 'arc-en-ciel') pm.color.setHSL((t * 0.15) % 1, 0.9, 0.6);
        if (aura === 'eclairs') pm.opacity = (0.25 + 0.65 * vif) * (0.6 + 0.4 * Math.random());
      });
    }

    // L'ombre au sol.
    const ombre = new THREE.Mesh(
      garde(new THREE.CircleGeometry(0.95, 32)),
      garde(new THREE.MeshBasicMaterial({ color: '#000000', transparent: true, opacity: 0.18 })),
    );
    ombre.rotation.x = -Math.PI / 2;
    ombre.position.y = 0.01;
    scene.add(ombre);

    // Les « Z » d'un personnage fatigué.
    const zzz: THREE.Sprite[] = [];
    if (fatigue) {
      const zt = document.createElement('canvas');
      zt.width = zt.height = 64;
      const zc = zt.getContext('2d')!;
      zc.font = 'bold 48px sans-serif';
      zc.fillStyle = '#ffffff';
      zc.strokeStyle = '#334155';
      zc.lineWidth = 6;
      zc.strokeText('Z', 14, 50);
      zc.fillText('Z', 14, 50);
      const zm = garde(new THREE.SpriteMaterial({ map: garde(new THREE.CanvasTexture(zt)), transparent: true }));
      for (let i = 0; i < 3; i++) {
        const s = new THREE.Sprite(zm);
        s.scale.setScalar(0.35);
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
      // Un toucher, et non un glissé : un geste du personnage.
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
    let prochainClin = performance.now() + 2500;
    const debut = performance.now();
    const boucle = (maintenant: number) => {
      const t = (maintenant - debut) / 1000;
      const lent = 0.45 + 0.55 * vif;

      // Respirer, se balancer, regarder.
      corps.position.y = Math.sin(t * 2 * lent) * 0.03;
      torse.scale.y = 1 + Math.sin(t * 2 * lent) * 0.015;
      bras[0].rotation.x = Math.sin(t * 1.6 * lent) * 0.12;
      bras[1].rotation.x = -Math.sin(t * 1.6 * lent) * 0.12;
      bras[0].rotation.z = -0.05;
      bras[1].rotation.z = 0.05;
      tete.rotation.y = Math.sin(t * 0.7) * 0.15;
      tete.rotation.x = fatigue ? 0.22 : Math.sin(t * 0.9) * 0.04;
      heros.position.y = 0;

      // Un geste demandé par un toucher.
      const g = geste.current;
      if (g) {
        const d = (maintenant - g.debut) / 1000;
        if (g.genre === 'saut') {
          const duree = 0.7;
          heros.position.y = Math.sin(Math.min(1, d / duree) * Math.PI) * 0.9;
          bras[0].rotation.z = -2.6 * Math.sin(Math.min(1, d / duree) * Math.PI);
          bras[1].rotation.z = 2.6 * Math.sin(Math.min(1, d / duree) * Math.PI);
          if (d > duree) geste.current = null;
        } else if (g.genre === 'salut') {
          const duree = 1.4;
          bras[1].rotation.z = 2.7;
          bras[1].rotation.x = Math.sin(d * 14) * 0.35;
          if (d > duree) geste.current = null;
        } else {
          const duree = 0.9;
          heros.rotation.y = angle.current.actuel + Math.min(1, d / duree) * Math.PI * 2;
          if (d > duree) geste.current = null;
        }
      }
      if (!g || g.genre !== 'tour') {
        // Sans glissé, il se tourne doucement d'un côté puis de l'autre.
        if (!depart && !compact) angle.current.cible += 0;
        const cible = compact ? -0.35 + Math.sin(t * 0.4) * 0.35 : angle.current.cible;
        angle.current.actuel += (cible - angle.current.actuel) * 0.12;
        heros.rotation.y = angle.current.actuel;
      }

      // Cligner des yeux.
      if (maintenant > prochainClin) {
        dessinerVisage(ctx, apparence.peau, 0, !fatigue);
        texture.needsUpdate = true;
        if (maintenant > prochainClin + 140) {
          ouverture = fatigue ? 0.35 : 1;
          dessinerVisage(ctx, apparence.peau, ouverture, !fatigue);
          texture.needsUpdate = true;
          prochainClin = maintenant + 2200 + Math.random() * 2800;
        }
      }

      for (const f of enMouvement) f(t);
      zzz.forEach((s, i) => {
        const cycle = (t * 0.5 + i / 3) % 1;
        s.position.set(0.7 + cycle * 0.6, 2.9 + cycle * 1.0, 0);
        s.material.opacity = 1 - cycle;
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
      scene.traverse((o) => {
        const m = o as THREE.Mesh;
        if (m.geometry) m.geometry.dispose();
        const mats = Array.isArray(m.material) ? m.material : m.material ? [m.material] : [];
        mats.forEach((x) => x.dispose());
      });
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
