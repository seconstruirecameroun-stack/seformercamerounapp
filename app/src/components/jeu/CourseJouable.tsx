import { useEffect, useRef, useState } from 'react';
import {
  DUREE_CHOC,
  VOIES,
  avancer,
  changerDeVoie,
  donnerBouclier,
  donnerTurbo,
  etape,
  nouvelEtat,
  paysage,
  type Etat,
  type Evenement,
  type Objet,
  type Paysage,
} from '../../lib/course';
import { jouerSon } from '../../lib/sons';

/**
 * La course, jouable : la route, la voiture, et tout ce qui bouge.
 *
 * La logique vit dans lib/course.ts ; ici on ne fait que dessiner et écouter
 * le doigt. Le dessin est fait au canvas, et pas en éléments de page : il y a
 * soixante images par seconde, des dizaines d'objets qui défilent, et un
 * téléphone d'entrée de gamme doit tenir le rythme.
 *
 * Rien n'est chargé : la voiture, la chèvre, les palmiers sont des formes
 * tracées. Zéro image, zéro crédit, et la course démarre hors connexion.
 *
 * L'enfant touche la moitié gauche ou droite de la route pour changer de
 * voie. S'il ne touche plus rien pendant quelques secondes — ou si `actif`
 * est faux, parce qu'il lit sa question — la voiture conduit seule.
 */

/** Après ce silence du doigt, le pilote reprend le volant. */
const PILOTE_APRES = 4;

type Particule = {
  x: number; y: number; vx: number; vy: number; vie: number; duree: number;
  couleur: string; taille: number;
};
type Texte = { x: number; y: number; texte: string; vie: number; couleur: string };

export type Resume = {
  pieces: number;
  distance: number;
  chocs: number;
  esquives: number;
  pilote: boolean;
  bouclier: boolean;
  turbo: boolean;
};

const DECOR: Record<Paysage, { herbe: string; herbe2: string; nom: string }> = {
  ville: { herbe: '#c9c3b6', herbe2: '#b7b0a2', nom: 'En ville' },
  savane: { herbe: '#e6cf7a', herbe2: '#d8bd62', nom: 'La savane' },
  foret: { herbe: '#5f9a5a', herbe2: '#4f8a4b', nom: 'La forêt' },
  mer: { herbe: '#ecd9a6', herbe2: '#e1cb8f', nom: 'Le bord de mer' },
};

const FONTE = "800 %spx Fredoka, system-ui, sans-serif";

export default function CourseJouable(props: {
  /** Faux pendant une question : la voiture roule seule. */
  actif?: boolean;
  /** Chaque fois que ce nombre monte, un turbo est donné. */
  turbos?: number;
  /** Chaque fois que ce nombre monte, un bouclier est donné. */
  boucliers?: number;
  onResume?: (r: Resume) => void;
}) {
  const actif = props.actif ?? true;
  const toile = useRef<HTMLCanvasElement | null>(null);
  const boite = useRef<HTMLDivElement | null>(null);
  const etat = useRef<Etat>(nouvelEtat());
  const particules = useRef<Particule[]>([]);
  const textes = useRef<Texte[]>([]);
  const actifRef = useRef(actif);
  actifRef.current = actif;
  const onResume = useRef(props.onResume);
  onResume.current = props.onResume;

  const [hud, setHud] = useState(() => ({
    pieces: 0, distance: 0, pilote: false, bouclier: false, turbo: false,
  }));
  const [banniere, setBanniere] = useState<{ cle: number; texte: string; sous?: string } | null>(null);

  // Les bonnes réponses arrivent par ces deux compteurs.
  const turbosVus = useRef(props.turbos ?? 0);
  useEffect(() => {
    const n = props.turbos ?? 0;
    if (n > turbosVus.current) {
      etat.current = donnerTurbo(etat.current);
      jouerSon('turbo');
      setBanniere({ cle: Date.now(), texte: 'TURBO !', sous: 'Bonne réponse' });
    }
    turbosVus.current = n;
  }, [props.turbos]);
  const boucliersVus = useRef(props.boucliers ?? 0);
  useEffect(() => {
    const n = props.boucliers ?? 0;
    if (n > boucliersVus.current) {
      etat.current = donnerBouclier(etat.current);
      jouerSon('bouclier');
      setBanniere({ cle: Date.now(), texte: 'BOUCLIER !', sous: 'Série sans faute' });
    }
    boucliersVus.current = n;
  }, [props.boucliers]);

  // Le doigt et les flèches.
  const geste = (sens: -1 | 1) => {
    if (!actifRef.current) return;
    etat.current = changerDeVoie(etat.current, sens);
  };
  useEffect(() => {
    const touche = (ev: KeyboardEvent) => {
      if (ev.key === 'ArrowLeft') geste(-1);
      if (ev.key === 'ArrowRight') geste(1);
    };
    window.addEventListener('keydown', touche);
    return () => window.removeEventListener('keydown', touche);
  }, []);

  // La boucle.
  useEffect(() => {
    const canvas = toile.current;
    const conteneur = boite.current;
    if (!canvas || !conteneur) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let L = 0;
    let H = 0;
    const dimensionner = () => {
      const dpr = Math.min(2, window.devicePixelRatio || 1);
      L = conteneur.clientWidth;
      H = Math.round(Math.min(560, Math.max(380, L * 1.3)));
      canvas.width = Math.round(L * dpr);
      canvas.height = Math.round(H * dpr);
      canvas.style.height = H + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    dimensionner();
    const observateur = new ResizeObserver(dimensionner);
    observateur.observe(conteneur);

    let avant = performance.now();
    let dernierHud = 0;
    let temps = 0;
    let id = 0;

    const boucle = (maintenant: number) => {
      const dt = Math.min(0.05, (maintenant - avant) / 1000);
      avant = maintenant;
      temps += dt;
      const pilote = !actifRef.current || etat.current.sansGeste > PILOTE_APRES;
      const r = avancer(etat.current, dt, Math.random, pilote);
      etat.current = r.etat;
      reagir(r.evenements, pilote);
      dessiner(ctx, L, H, etat.current, temps, particules.current, textes.current, dt);

      if (maintenant - dernierHud > 120) {
        dernierHud = maintenant;
        const e = etat.current;
        setHud((h) => {
          const n = {
            pieces: e.pieces, distance: Math.floor(e.distance), pilote,
            bouclier: e.bouclier, turbo: e.turbo > 0,
          };
          return h.pieces === n.pieces && h.distance === n.distance && h.pilote === n.pilote &&
            h.bouclier === n.bouclier && h.turbo === n.turbo ? h : n;
        });
        onResume.current?.({
          pieces: e.pieces, distance: e.distance, chocs: e.chocs, esquives: e.esquives,
          pilote, bouclier: e.bouclier, turbo: e.turbo > 0,
        });
      }
      id = requestAnimationFrame(boucle);
    };

    const reagir = (evenements: Evenement[], pilote: boolean) => {
      const e = etat.current;
      const voieX = (v: number) => xDeVoie(L, v);
      const yVoiture = H * 0.78;
      for (const ev of evenements) {
        if (ev.type === 'piece') {
          jouerSon('piece');
          gerbe(particules.current, voieX(ev.voie), yVoiture - 20, '#f2c14e', 9);
          textes.current.push({ x: voieX(ev.voie), y: yVoiture - 40, texte: '+1', vie: 0.8, couleur: '#b9770e' });
        } else if (ev.type === 'choc') {
          jouerSon('choc');
          gerbe(particules.current, voieX(ev.voie), yVoiture - 10, '#ffffff', 14);
          gerbe(particules.current, voieX(ev.voie), yVoiture - 10, '#f2c14e', 6);
          textes.current.push({
            x: voieX(ev.voie), y: yVoiture - 60, vie: 1,
            texte: ev.sorte === 'chevre' ? 'Bêêê !' : ev.sorte === 'flaque' ? 'Splash !' : 'Ouille !',
            couleur: '#c0392b',
          });
          // On ne secoue le téléphone que si c'est l'enfant qui conduit.
          if (!pilote && navigator.vibrate) navigator.vibrate(40);
        } else if (ev.type === 'bouclier') {
          jouerSon('bouclier');
          gerbe(particules.current, voieX(ev.voie), yVoiture - 10, '#7fd3f7', 18);
          textes.current.push({ x: voieX(ev.voie), y: yVoiture - 60, texte: 'Protégé !', vie: 1, couleur: '#1f7aa8' });
        } else if (ev.type === 'ville') {
          jouerSon('fete');
          setBanniere({ cle: Date.now(), texte: 'Bienvenue à ' + ev.nom + ' !', sous: Math.round(e.distance) + ' m parcourus' });
          for (let i = 0; i < 4; i++) gerbe(particules.current, L * (0.2 + i * 0.2), H * 0.3, ['#e74c3c', '#f1c40f', '#2ecc71', '#3498db'][i], 12);
        }
      }
    };

    id = requestAnimationFrame(boucle);
    return () => {
      cancelAnimationFrame(id);
      observateur.disconnect();
    };
  }, []);

  const voyage = etape(hud.distance);

  return (
    <div className="select-none">
      {/* Le voyage : la ville quittée, la suivante, et combien il reste. */}
      <div className="mb-2 flex items-center gap-2">
        <span className="shrink-0 rounded-full bg-gold px-2.5 py-1 text-kid-sm font-black tabular-nums text-ink shadow-[inset_0_-2px_0_rgb(0_0_0/0.12)]">
          ● {hud.pieces}
        </span>
        <div className="min-w-0 flex-1">
          <div className="flex justify-between gap-2 text-kid-xs font-black">
            <span className="truncate">{voyage.depuis.nom}</span>
            <span className="truncate text-clay-dark">{voyage.vers ? voyage.vers.nom : 'Au bout du pays !'}</span>
          </div>
          <div className="relative mt-1 h-3 rounded-full bg-line">
            <div className="h-3 rounded-full bg-leaf" style={{ width: voyage.part * 100 + '%' }} />
            <span
              className="absolute -top-1.5 text-base leading-none"
              style={{ left: `calc(${voyage.part * 100}% - 9px)` }}
              aria-hidden
            >
              🚗
            </span>
          </div>
        </div>
        <span className="shrink-0 text-kid-xs font-black tabular-nums text-ink-2">
          {voyage.vers ? `${voyage.restant} m` : ''}
        </span>
      </div>

      <div
        ref={boite}
        className="relative w-full touch-none overflow-hidden rounded-[var(--radius-card)] border-2 border-ink"
        onPointerDown={(ev) => {
          const r = (ev.currentTarget as HTMLDivElement).getBoundingClientRect();
          geste(ev.clientX - r.left < r.width / 2 ? -1 : 1);
        }}
      >
        <canvas ref={toile} className="block w-full" />

        {banniere ? (
          <div
            key={banniere.cle}
            className="banniere-course pointer-events-none absolute inset-x-0 top-[18%] flex flex-col items-center"
            onAnimationEnd={() => setBanniere(null)}
          >
            <p className="rounded-full border-2 border-ink bg-white-warm px-4 py-1.5 text-center text-kid-lg font-black text-clay-dark shadow-[0_6px_0_oklch(0.3_0.045_205_/_0.25)]">
              {banniere.texte}
            </p>
            {banniere.sous ? (
              <p className="mt-1 rounded-full bg-ink/80 px-3 py-0.5 text-kid-xs font-bold text-white-warm">
                {banniere.sous}
              </p>
            ) : null}
          </div>
        ) : null}

        <div className="pointer-events-none absolute left-2 top-2 flex flex-col gap-1">
          <span className="rounded-full bg-ink/75 px-2 py-0.5 text-kid-xs font-black tabular-nums text-white-warm">
            {(hud.distance / 1000).toFixed(2).replace('.', ',')} km
          </span>
          {hud.bouclier ? (
            <span className="rounded-full bg-sky px-2 py-0.5 text-kid-xs font-black text-ink">🛡 Bouclier</span>
          ) : null}
        </div>
        {hud.pilote && actif ? (
          <span className="pointer-events-none absolute inset-x-0 bottom-2 mx-auto w-fit rounded-full bg-white-warm/85 px-2.5 py-0.5 text-kid-xs font-bold text-ink-2">
            Pilote auto · touche pour conduire
          </span>
        ) : null}
      </div>
    </div>
  );
}

// ─── Le dessin ──────────────────────────────────────────────────────────────

/** La route occupe le milieu, les bas-côtés le reste. */
function geometrie(L: number) {
  const route = Math.min(L * 0.72, 330);
  const gauche = (L - route) / 2;
  return { route, gauche, voie: route / VOIES };
}

function xDeVoie(L: number, v: number) {
  const g = geometrie(L);
  return g.gauche + g.voie * (v + 0.5);
}

/** Combien de pixels pour un mètre de route. */
const pxParMetre = (H: number) => H / 34;

function gerbe(liste: Particule[], x: number, y: number, couleur: string, n: number) {
  for (let i = 0; i < n; i++) {
    const a = Math.random() * Math.PI * 2;
    const v = 60 + Math.random() * 160;
    liste.push({
      x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 60, vie: 0, duree: 0.5 + Math.random() * 0.4,
      couleur, taille: 2 + Math.random() * 3.5,
    });
  }
}

/** Un nombre tiré d'un entier, toujours le même : le décor ne clignote pas. */
function hache(n: number) {
  let h = Math.imul(n ^ 0x9e3779b9, 2654435761);
  h ^= h >>> 15;
  return ((h >>> 0) % 1000) / 1000;
}

function dessiner(
  ctx: CanvasRenderingContext2D,
  L: number,
  H: number,
  e: Etat,
  t: number,
  particules: Particule[],
  textes: Texte[],
  dt: number,
) {
  const g = geometrie(L);
  const ppm = pxParMetre(H);
  const yVoiture = H * 0.78;
  const ecran = (d: number) => yVoiture - (d - e.distance) * ppm;
  const ici = paysage(e.distance);
  const decor = DECOR[ici];

  // Les bas-côtés.
  ctx.fillStyle = decor.herbe;
  ctx.fillRect(0, 0, L, H);
  ctx.fillStyle = decor.herbe2;
  const bande = 3 * ppm;
  const decal = (e.distance * ppm) % (bande * 2);
  for (let y = -bande * 2 + decal; y < H; y += bande * 2) {
    ctx.fillRect(0, y, g.gauche, bande);
    ctx.fillRect(g.gauche + g.route, y, L - g.gauche - g.route, bande);
  }
  if (ici === 'mer') {
    ctx.fillStyle = '#5bb6d6';
    ctx.fillRect(g.gauche + g.route + 18, 0, L, H);
    ctx.fillStyle = 'rgba(255,255,255,0.55)';
    for (let k = 0; k < 6; k++) {
      const y = ((k * H) / 6 + e.distance * ppm * 0.6) % H;
      ctx.fillRect(g.gauche + g.route + 30, y, L, 2);
    }
  }

  // Le décor qui défile : un objet tous les sept mètres, de chaque côté.
  const premier = Math.floor((e.distance - 10) / 7);
  const dernier = Math.ceil((e.distance + H / ppm) / 7);
  for (let k = premier; k <= dernier; k++) {
    const y = ecran(k * 7);
    for (const cote of [0, 1]) {
      if (ici === 'mer' && cote === 1) continue;
      const h = hache(k * 2 + cote);
      if (h < 0.35) continue;
      const largeurCote = cote === 0 ? g.gauche : L - g.gauche - g.route;
      const x = cote === 0 ? largeurCote * (0.25 + h * 0.5) : g.gauche + g.route + largeurCote * (0.25 + h * 0.5);
      decorDe(ctx, ici, x, y, h, Math.min(largeurCote * 0.8, 46));
    }
  }

  // La route.
  ctx.fillStyle = '#4a4f57';
  ctx.fillRect(g.gauche, 0, g.route, H);
  ctx.fillStyle = '#f4f1e8';
  ctx.fillRect(g.gauche, 0, 4, H);
  ctx.fillRect(g.gauche + g.route - 4, 0, 4, H);
  const tiret = 2.2 * ppm;
  const pasTiret = 5 * ppm;
  const dec = (e.distance * ppm) % pasTiret;
  ctx.fillStyle = 'rgba(244,241,232,0.85)';
  for (let v = 1; v < VOIES; v++) {
    const x = g.gauche + g.voie * v - 2;
    for (let y = -pasTiret + dec; y < H; y += pasTiret) ctx.fillRect(x, y, 4, tiret);
  }

  // Le turbo : des traits de vitesse sur la route.
  if (e.turbo > 0) {
    ctx.strokeStyle = 'rgba(255,255,255,0.35)';
    ctx.lineWidth = 2;
    for (let i = 0; i < 9; i++) {
      const x = g.gauche + hache(i + Math.floor(t * 20)) * g.route;
      const y = hache(i * 7 + Math.floor(t * 20)) * H;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x, y + 40);
      ctx.stroke();
    }
  }

  // Les objets.
  for (const o of e.objets) {
    if (o.pris && o.type === 'piece') continue;
    const y = ecran(o.d);
    if (y < -40 || y > H + 40) continue;
    const x = g.gauche + g.voie * (o.voie + 0.5);
    if (o.type === 'piece') piece(ctx, x, y, g.voie * 0.2, t);
    else obstacle(ctx, o, x, y, g.voie * 0.62, o.pris === true);
  }

  // La voiture.
  const xV = g.gauche + g.voie * (e.x + 0.5);
  voiture(ctx, xV, yVoiture, g.voie * 0.56, e, t);

  // Les étincelles et les mots.
  for (const p of particules) {
    p.vie += dt;
    p.x += p.vx * dt;
    p.y += p.vy * dt;
    p.vy += 380 * dt;
    const a = 1 - p.vie / p.duree;
    if (a <= 0) continue;
    ctx.globalAlpha = a;
    ctx.fillStyle = p.couleur;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.taille, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
  for (let i = particules.length - 1; i >= 0; i--) if (particules[i].vie >= particules[i].duree) particules.splice(i, 1);

  ctx.textAlign = 'center';
  for (const m of textes) {
    m.vie -= dt;
    m.y -= 40 * dt;
    if (m.vie <= 0) continue;
    ctx.globalAlpha = Math.min(1, m.vie * 2.5);
    ctx.font = FONTE.replace('%s', '22');
    ctx.lineWidth = 5;
    ctx.strokeStyle = '#ffffff';
    ctx.strokeText(m.texte, m.x, m.y);
    ctx.fillStyle = m.couleur;
    ctx.fillText(m.texte, m.x, m.y);
  }
  ctx.globalAlpha = 1;
  for (let i = textes.length - 1; i >= 0; i--) if (textes[i].vie <= 0) textes.splice(i, 1);
}

function decorDe(ctx: CanvasRenderingContext2D, p: Paysage, x: number, y: number, h: number, t: number) {
  if (p === 'ville') {
    const couleurs = ['#e8a87c', '#85c1e9', '#f7dc6f', '#d98880', '#a9cce3'];
    const l = t * (0.7 + h * 0.3);
    ctx.fillStyle = 'rgba(0,0,0,0.12)';
    ctx.fillRect(x - l / 2 + 3, y - l / 2 + 3, l, l);
    ctx.fillStyle = couleurs[Math.floor(h * 100) % couleurs.length];
    ctx.fillRect(x - l / 2, y - l / 2, l, l);
    ctx.fillStyle = 'rgba(255,255,255,0.7)';
    ctx.fillRect(x - l / 4, y - l / 4, l / 5, l / 5);
    ctx.fillRect(x + l / 10, y - l / 4, l / 5, l / 5);
  } else if (p === 'foret') {
    const r = t * (0.45 + h * 0.25);
    ctx.fillStyle = 'rgba(0,0,0,0.15)';
    ctx.beginPath();
    ctx.arc(x + 4, y + 4, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = h > 0.7 ? '#2e6b34' : '#3d8a43';
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,0.15)';
    ctx.beginPath();
    ctx.arc(x - r / 3, y - r / 3, r / 3, 0, Math.PI * 2);
    ctx.fill();
  } else if (p === 'savane') {
    if (h > 0.75) {
      // Un acacia : une couronne plate.
      ctx.fillStyle = 'rgba(0,0,0,0.12)';
      ctx.beginPath();
      ctx.ellipse(x + 3, y + 3, t * 0.55, t * 0.32, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#6f9a3c';
      ctx.beginPath();
      ctx.ellipse(x, y, t * 0.55, t * 0.32, 0, 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.strokeStyle = '#b8962f';
      ctx.lineWidth = 2;
      for (let i = -2; i <= 2; i++) {
        ctx.beginPath();
        ctx.moveTo(x + i * 3, y + 6);
        ctx.lineTo(x + i * 5, y - 6);
        ctx.stroke();
      }
    }
  } else {
    // Un palmier vu d'en haut.
    ctx.strokeStyle = '#3f8f4a';
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2 + h;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + Math.cos(a) * t * 0.5, y + Math.sin(a) * t * 0.5);
      ctx.stroke();
    }
    ctx.fillStyle = '#8b5a2b';
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fill();
  }
}

function piece(ctx: CanvasRenderingContext2D, x: number, y: number, r: number, t: number) {
  const s = Math.abs(Math.cos(t * 4 + y * 0.01));
  ctx.fillStyle = 'rgba(0,0,0,0.15)';
  ctx.beginPath();
  ctx.ellipse(x + 2, y + 3, r * Math.max(0.25, s), r, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#e5a91f';
  ctx.beginPath();
  ctx.ellipse(x, y, r * Math.max(0.25, s), r, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = '#f7d354';
  ctx.beginPath();
  ctx.ellipse(x, y, r * 0.7 * Math.max(0.25, s), r * 0.7, 0, 0, Math.PI * 2);
  ctx.fill();
}

function obstacle(ctx: CanvasRenderingContext2D, o: Objet, x: number, y: number, l: number, touche: boolean) {
  ctx.save();
  if (touche) ctx.globalAlpha = 0.45;
  switch (o.sorte) {
    case 'trou':
      ctx.fillStyle = '#2b2a28';
      ctx.beginPath();
      ctx.ellipse(x, y, l * 0.48, l * 0.3, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#6b5e4e';
      ctx.lineWidth = 3;
      ctx.stroke();
      break;
    case 'flaque':
      ctx.fillStyle = '#6fb7e6';
      ctx.beginPath();
      ctx.ellipse(x, y, l * 0.5, l * 0.3, 0.2, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,0.6)';
      ctx.beginPath();
      ctx.ellipse(x - l * 0.15, y - l * 0.08, l * 0.14, l * 0.05, 0.2, 0, Math.PI * 2);
      ctx.fill();
      break;
    case 'carton': {
      const c = l * 0.6;
      ctx.fillStyle = 'rgba(0,0,0,0.2)';
      ctx.fillRect(x - c / 2 + 3, y - c / 2 + 3, c, c);
      ctx.fillStyle = '#c8935a';
      ctx.fillRect(x - c / 2, y - c / 2, c, c);
      ctx.fillStyle = '#e9d29a';
      ctx.fillRect(x - c / 2, y - 3, c, 6);
      ctx.fillRect(x - 3, y - c / 2, 6, c);
      break;
    }
    default: {
      // La chèvre, vue d'en haut : le corps, la tête, deux cornes.
      const r = l * 0.3;
      ctx.fillStyle = 'rgba(0,0,0,0.18)';
      ctx.beginPath();
      ctx.ellipse(x + 3, y + 4, r * 1.25, r * 0.8, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#f5f2ea';
      ctx.beginPath();
      ctx.ellipse(x, y, r * 1.25, r * 0.8, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#d8cdb8';
      ctx.beginPath();
      ctx.arc(x + r * 1.35, y - r * 0.2, r * 0.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#7a6a55';
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(x + r * 1.3, y - r * 0.6);
      ctx.lineTo(x + r * 1.1, y - r * 1.0);
      ctx.moveTo(x + r * 1.55, y - r * 0.55);
      ctx.lineTo(x + r * 1.7, y - r * 0.95);
      ctx.stroke();
      ctx.fillStyle = '#2b2a28';
      ctx.beginPath();
      ctx.arc(x + r * 1.55, y - r * 0.25, 2, 0, Math.PI * 2);
      ctx.fill();
    }
  }
  ctx.restore();
}

function voiture(ctx: CanvasRenderingContext2D, x: number, y: number, l: number, e: Etat, t: number) {
  const h = l * 1.7;
  ctx.save();
  ctx.translate(x, y);
  if (e.choc > 0) ctx.rotate((1 - e.choc / DUREE_CHOC) * Math.PI * 2);
  else ctx.rotate((e.voie - e.x) * -0.25);
  // Clignote pendant qu'elle ne peut pas être touchée.
  if (e.invulnerable > 0 && e.choc === 0 && Math.floor(t * 12) % 2 === 0) ctx.globalAlpha = 0.55;

  // Les flammes du turbo.
  if (e.turbo > 0) {
    const f = 0.7 + Math.random() * 0.5;
    for (const [dx, c, s] of [[-l * 0.22, '#f39c12', 1], [l * 0.22, '#f39c12', 1], [-l * 0.22, '#f9e79f', 0.55], [l * 0.22, '#f9e79f', 0.55]] as const) {
      ctx.fillStyle = c;
      ctx.beginPath();
      ctx.moveTo(dx - 6 * s, h / 2);
      ctx.lineTo(dx, h / 2 + 34 * f * s);
      ctx.lineTo(dx + 6 * s, h / 2);
      ctx.fill();
    }
  }

  // L'ombre.
  ctx.fillStyle = 'rgba(0,0,0,0.25)';
  arrondi(ctx, -l / 2 + 4, -h / 2 + 6, l, h, l * 0.3);
  ctx.fill();
  // Les roues.
  ctx.fillStyle = '#1f2326';
  for (const [rx, ry] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
    arrondi(ctx, rx * (l / 2) - (rx > 0 ? 3 : 4), ry * h * 0.28 - 8, 7, 16, 3);
    ctx.fill();
  }
  // La carrosserie.
  ctx.fillStyle = '#d7443a';
  arrondi(ctx, -l / 2, -h / 2, l, h, l * 0.3);
  ctx.fill();
  ctx.fillStyle = '#b8352d';
  arrondi(ctx, -l / 2 + 3, -h * 0.12, l - 6, h * 0.36, l * 0.18);
  ctx.fill();
  // Le pare-brise et la vitre arrière.
  ctx.fillStyle = '#bfe3f2';
  arrondi(ctx, -l * 0.36, -h * 0.3, l * 0.72, h * 0.18, 5);
  ctx.fill();
  arrondi(ctx, -l * 0.32, h * 0.25, l * 0.64, h * 0.1, 4);
  ctx.fill();
  // Une bande blanche : c'est une voiture de course.
  ctx.fillStyle = 'rgba(255,255,255,0.85)';
  ctx.fillRect(-3, -h / 2 + 2, 6, h * 0.18);
  // Les phares.
  ctx.fillStyle = '#fff3b0';
  ctx.beginPath();
  ctx.arc(-l * 0.3, -h / 2 + 4, 3.5, 0, Math.PI * 2);
  ctx.arc(l * 0.3, -h / 2 + 4, 3.5, 0, Math.PI * 2);
  ctx.fill();
  ctx.globalAlpha = 1;

  // Le bouclier : une bulle qui respire.
  if (e.bouclier) {
    const r = h * 0.72 + Math.sin(t * 6) * 3;
    ctx.fillStyle = 'rgba(127,211,247,0.22)';
    ctx.strokeStyle = 'rgba(31,122,168,0.8)';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(0, 0, r, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }
  ctx.restore();
}

function arrondi(ctx: CanvasRenderingContext2D, x: number, y: number, l: number, h: number, r: number) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + l, y, x + l, y + h, r);
  ctx.arcTo(x + l, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + l, y, r);
  ctx.closePath();
}
