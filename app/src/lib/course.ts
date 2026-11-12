/**
 * La course : la voiture de KLEIN, sans dessin.
 *
 * L'ENFANT NE CONDUIT PAS. Son attention va aux questions ; la voiture roule
 * seule, sur trois voies, conduite par un pilote qui ramasse les pièces et
 * évite les obstacles. Ce sont les RÉPONSES qui décident de la course :
 *
 *   une bonne réponse donne un TURBO — la voiture file, et c'est là que se
 *   gagne l'essentiel de la route ;
 *
 *   une mauvaise réponse rend le pilote MALADROIT — il va heurter le prochain
 *   obstacle, fait un tête-à-queue, ralentit, et perd du terrain ;
 *
 *   une série sans faute donne un BOUCLIER — la prochaine maladresse est
 *   encaissée par la bulle, sans choc.
 *
 * La vitesse de croisière est lente exprès : sans bonnes réponses, la voiture
 * avance peu. Le chemin parcouru dit donc comment la séance s'est passée.
 *
 * UN CHOC NE FAIT JAMAIS PERDRE. Ni vie, ni fin de partie : la voiture repart
 * toujours. On signale une réponse à revoir, on ne punit pas.
 *
 * Tout ce fichier est pur : le temps et le hasard lui sont donnés. Il se
 * vérifie donc sans écran (course.verif.ts), et l'écran ne fait que dessiner.
 */

export const VOIES = 3;

/** En mètres par seconde. */
export const VITESSE_NORMALE = 8;
export const VITESSE_TURBO = 28;
export const VITESSE_CHOC = 3;
/** La vitesse revient à la normale à ce rythme, en m/s chaque seconde. */
const REPRISE = 9;

export const DUREE_TURBO = 3.5;
export const DUREE_CHOC = 1;
/** Après un choc, la voiture ne peut pas être touchée de nouveau tout de suite. */
const DUREE_INVULNERABLE = 1.4;

/** La distance entre deux rangées d'objets sur la route. */
const ECART_RANGEES = 22;
/** Ce que la voiture voit devant elle : on crée les objets jusque-là. */
export const HORIZON = 60;
/** La longueur, en mètres, sur laquelle un objet touche la voiture. */
const PORTEE = 1.7;
/** Le pilote ne regarde pas plus loin. */
const REGARD_PILOTE = 26;

export type SorteObstacle = 'trou' | 'chevre' | 'flaque' | 'carton';
export const SORTES: SorteObstacle[] = ['trou', 'chevre', 'flaque', 'carton'];

export type Objet = {
  id: number;
  type: 'piece' | 'obstacle';
  sorte?: SorteObstacle;
  voie: number;
  /** La distance à laquelle il se trouve sur la route. */
  d: number;
  pris?: boolean;
};

export type Etat = {
  /** La voie visée. */
  voie: number;
  /** La position réelle, qui glisse vers la voie visée. */
  x: number;
  distance: number;
  vitesse: number;
  pieces: number;
  objets: Objet[];
  prochaineRangee: number;
  prochainId: number;
  turbo: number;
  choc: number;
  invulnerable: number;
  bouclier: boolean;
  /** Après une mauvaise réponse : le pilote va heurter le prochain obstacle. */
  maladroit: boolean;
  chocs: number;
  esquives: number;
};

export type Evenement =
  | { type: 'piece'; voie: number }
  | { type: 'choc'; sorte: SorteObstacle; voie: number }
  | { type: 'bouclier'; sorte: SorteObstacle; voie: number }
  | { type: 'ville'; nom: string };

/** Le voyage : la voiture traverse le pays, ville après ville. */
export const VILLES = [
  { nom: 'Yaoundé', d: 0 },
  { nom: 'Mbalmayo', d: 700 },
  { nom: 'Ebolowa', d: 1700 },
  { nom: 'Kribi', d: 3000 },
  { nom: 'Douala', d: 4600 },
  { nom: 'Buea', d: 6400 },
  { nom: 'Bafoussam', d: 8600 },
  { nom: 'Ngaoundéré', d: 11200 },
  { nom: 'Garoua', d: 14200 },
  { nom: 'Maroua', d: 17600 },
] as const;

/** Où en est le voyage : la dernière ville passée et la prochaine. */
export function etape(distance: number) {
  let i = 0;
  while (i + 1 < VILLES.length && VILLES[i + 1].d <= distance) i += 1;
  const depuis = VILLES[i];
  const vers = VILLES[i + 1] ?? null;
  const part = vers ? (distance - depuis.d) / (vers.d - depuis.d) : 1;
  return { depuis, vers, part: Math.max(0, Math.min(1, part)), restant: vers ? vers.d - distance : 0 };
}

export type Paysage = 'ville' | 'savane' | 'foret' | 'mer';
const PAYSAGES: Paysage[] = ['ville', 'savane', 'foret', 'mer'];

/** Le décor change tous les 450 mètres. */
export function paysage(distance: number): Paysage {
  return PAYSAGES[Math.floor(Math.max(0, distance) / 450) % PAYSAGES.length];
}

export function nouvelEtat(): Etat {
  return {
    voie: 1, x: 1, distance: 0, vitesse: VITESSE_NORMALE, pieces: 0, objets: [],
    prochaineRangee: 30, prochainId: 1, turbo: 0, choc: 0, invulnerable: 0,
    bouclier: false, maladroit: false, chocs: 0, esquives: 0,
  };
}

/** Une bonne réponse. Elle efface aussi une maladresse en attente. */
export function donnerTurbo(e: Etat): Etat {
  return { ...e, turbo: DUREE_TURBO, maladroit: false, vitesse: Math.max(e.vitesse, VITESSE_TURBO) };
}

/** Une mauvaise réponse : le turbo s'arrête, et le prochain obstacle sera touché. */
export function donnerErreur(e: Etat): Etat {
  return { ...e, turbo: 0, maladroit: true };
}

export function donnerBouclier(e: Etat): Etat {
  return { ...e, bouclier: true };
}

/**
 * Une rangée d'objets : au plus un obstacle par rangée au début, deux plus
 * loin — mais JAMAIS trois. Une voie reste toujours libre, sinon l'enfant
 * serait puni sans avoir rien pu faire.
 */
export function rangee(d: number, distance: number, alea: () => number, id: number): Objet[] {
  const voies = [0, 1, 2].sort(() => alea() - 0.5);
  const nbObstacles = distance > 900 && alea() < 0.35 ? 2 : 1;
  const sortie: Objet[] = [];
  for (let i = 0; i < nbObstacles; i++) {
    sortie.push({
      id: id++, type: 'obstacle', voie: voies[i], d,
      sorte: SORTES[Math.floor(alea() * SORTES.length)],
    });
  }
  // Les pièces vont dans une voie libre, en petite file.
  const libre = voies[nbObstacles];
  const nbPieces = alea() < 0.75 ? 3 : 0;
  for (let i = 0; i < nbPieces; i++) {
    sortie.push({ id: id++, type: 'piece', voie: libre, d: d + 4 + i * 3 });
  }
  return sortie;
}

/**
 * Le pilote.
 *
 * D'ordinaire il évite les obstacles et va chercher les pièces. Maladroit,
 * il va droit sur le prochain obstacle qu'il a le temps d'atteindre. Il ne
 * change de voie que d'une case à la fois.
 */
export function choixDuPilote(e: Etat): number {
  const devant = e.objets.filter(
    (o) => !o.pris && o.d > e.distance - 1 && o.d - e.distance < REGARD_PILOTE,
  );
  if (e.maladroit) {
    const vise = devant
      .filter((o) => o.type === 'obstacle' && o.d - e.distance > 4)
      .sort((a, b) => a.d - b.d)[0];
    if (vise) return e.voie + Math.sign(vise.voie - e.voie);
    return e.voie;
  }
  const danger = (v: number) => devant.some((o) => o.type === 'obstacle' && o.voie === v);
  const gain = (v: number) => devant.filter((o) => o.type === 'piece' && o.voie === v).length;
  // Le pilote choisit la meilleure voie de toute la route, puis s'y rend une
  // voie à la fois. Changer de voie est rapide : traverser une voie dont
  // l'obstacle est encore loin ne fait pas de mal.
  let cible = e.voie;
  let note = -Infinity;
  for (let v = 0; v < VOIES; v++) {
    const n = (danger(v) ? -10 : 0) + gain(v) - 0.3 * Math.abs(v - e.voie);
    if (n > note) {
      note = n;
      cible = v;
    }
  }
  return e.voie + Math.sign(cible - e.voie);
}

/** Le pas du jeu : `dt` secondes passent. */
export function avancer(
  e0: Etat,
  dt: number,
  alea: () => number,
): { etat: Etat; evenements: Evenement[] } {
  const evenements: Evenement[] = [];
  const e: Etat = { ...e0, objets: e0.objets };
  const pas = Math.min(dt, 0.05);

  e.voie = choixDuPilote(e);

  // La voiture glisse vers sa voie, sans sauter.
  const ecart = e.voie - e.x;
  e.x += Math.sign(ecart) * Math.min(Math.abs(ecart), pas * 7);

  e.turbo = Math.max(0, e.turbo - pas);
  e.choc = Math.max(0, e.choc - pas);
  e.invulnerable = Math.max(0, e.invulnerable - pas);
  const cible = e.choc > 0 ? VITESSE_CHOC : e.turbo > 0 ? VITESSE_TURBO : VITESSE_NORMALE;
  if (e.vitesse < cible) e.vitesse = Math.min(cible, e.vitesse + REPRISE * pas);
  else e.vitesse = Math.max(cible, e.vitesse - REPRISE * 2 * pas);

  const avant = e.distance;
  e.distance += e.vitesse * pas;

  // Les villes passées.
  for (const v of VILLES) {
    if (v.d > 0 && avant < v.d && e.distance >= v.d) evenements.push({ type: 'ville', nom: v.nom });
  }

  // De nouveaux objets à l'horizon.
  let objets = e.objets;
  while (e.prochaineRangee < e.distance + HORIZON) {
    const r = rangee(e.prochaineRangee, e.prochaineRangee, alea, e.prochainId);
    e.prochainId += r.length;
    objets = [...objets, ...r];
    e.prochaineRangee += ECART_RANGEES + Math.floor(alea() * 8);
  }

  // Ce que la voiture touche. Elle occupe une voie quand elle en est proche.
  const voieOccupee = Math.round(e.x);
  const proche = Math.abs(e.x - voieOccupee) < 0.35;
  objets = objets.map((o) => {
    if (o.pris || !proche || o.voie !== voieOccupee) return o;
    // Un obstacle déjà dépassé ne touche plus : entrer dans une voie juste
    // derrière lui serait puni sans que l'enfant ait rien pu voir.
    if (o.d - e.distance > PORTEE || o.d - e.distance < (o.type === 'piece' ? -PORTEE : -0.4)) return o;
    if (o.type === 'piece') {
      e.pieces += 1;
      evenements.push({ type: 'piece', voie: o.voie });
      return { ...o, pris: true };
    }
    // Le pilote adroit n'est jamais puni d'un obstacle qu'il n'a pas pu
    // éviter : seule une mauvaise réponse fait toucher.
    if (!e.maladroit || e.invulnerable > 0 || e.turbo > 0) return o;
    const sorte = o.sorte ?? 'trou';
    e.maladroit = false;
    if (e.bouclier) {
      e.bouclier = false;
      e.invulnerable = DUREE_INVULNERABLE;
      evenements.push({ type: 'bouclier', sorte, voie: o.voie });
      return { ...o, pris: true };
    }
    e.choc = DUREE_CHOC;
    e.invulnerable = DUREE_INVULNERABLE;
    e.chocs += 1;
    evenements.push({ type: 'choc', sorte, voie: o.voie });
    return { ...o, pris: true };
  });

  // Ce qui est passé derrière ne compte plus. Un obstacle dépassé sans être
  // touché est une esquive.
  e.objets = objets.filter((o) => {
    const derriere = o.d < e.distance - 8;
    if (derriere && o.type === 'obstacle' && !o.pris) e.esquives += 1;
    return !derriere;
  });

  return { etat: e, evenements };
}
