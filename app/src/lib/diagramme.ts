/**
 * Placer les éléments dans les régions d'un diagramme.
 *
 * Le cahier de BRAYNE demande « Draw a venn diagram and represent sets A, B
 * and C ». Aucun type de question ne savait le faire : on pouvait lui
 * demander **où** va le 15, pas le lui faire **poser**. Or c'est le geste de
 * l'exercice, et c'est celui qu'il rate — ses ratures portent toutes sur les
 * régions, jamais sur la définition.
 *
 * Tout ce qui est géométrie vit ici et non dans le composant, pour une
 * raison simple : la question « dans quelle région ai-je touché ? » est
 * exacte ou fausse, elle se vérifie hors du navigateur, et une erreur
 * dessus rangerait un élément dans la mauvaise case sans rien dire.
 *
 * On ne découpe pas les lentilles en tracés : on garde des disques, et on
 * demande au point touché **dans quels disques il est**. La liste des
 * disques qui le contiennent EST la région. Sept régions pour trois
 * ensembles, quatre pour deux, et le dehors, sans un seul chemin courbe à
 * écrire.
 */

export type Cercle = { nom: string; cx: number; cy: number; r: number };

export type Point = { x: number; y: number };

export type Disposition = {
  largeur: number;
  hauteur: number;
  cadre: { x: number; y: number; w: number; h: number };
  cercles: Cercle[];
  /** Où poser les étiquettes d'une région, par clé de région. */
  ancres: Record<string, Point>;
  /** Où écrire le nom de chaque ensemble. */
  etiquettes: Point[];
};

/** La région hors de tous les ovales, mais dans le rectangle. */
export const DEHORS = 'dehors';

/**
 * La clé d'une région : les noms des ensembles qui la contiennent, dans
 * l'ordre de l'énoncé. « AB » est l'intersection de A et de B, « A » est la
 * part de A que personne d'autre ne partage, et `dehors` est le reste du
 * rectangle.
 */
export function cleRegion(noms: string[], dedans: boolean[]): string {
  const pris = noms.filter((_, i) => dedans[i]).join('');
  return pris === '' ? DEHORS : pris;
}

/** Toutes les régions d'un diagramme, dehors compris. */
export function toutesLesRegions(noms: string[]): string[] {
  const cles: string[] = [];
  for (let masque = 0; masque < 1 << noms.length; masque += 1) {
    cles.push(cleRegion(noms, noms.map((_, i) => Boolean(masque & (1 << i)))));
  }
  return cles;
}

const CADRE = { x: 6, y: 6, w: 308, h: 196 };

export function disposition(noms: string[]): Disposition {
  const commun = { largeur: 320, hauteur: 230, cadre: CADRE };

  if (noms.length === 2) {
    const r = 62;
    const cercles = [
      { nom: noms[0], cx: 116, cy: 100, r },
      { nom: noms[1], cx: 204, cy: 100, r },
    ];
    return {
      ...commun,
      cercles,
      ancres: {
        [noms[0]]: { x: 84, y: 100 },
        [noms[0] + noms[1]]: { x: 160, y: 100 },
        [noms[1]]: { x: 236, y: 100 },
        [DEHORS]: { x: 46, y: 182 },
      },
      etiquettes: [
        { x: 72, y: 46 },
        { x: 248, y: 46 },
      ],
    };
  }

  // Trois ensembles : un ovale en haut, deux en bas, comme le manuel les
  // dessine. Les ancres des lentilles sont poussées jusqu-au centre du
  // troisième disque opposé — à mi-chemin elles tombaient encore DANS ce
  // troisième disque, et l-étiquette se serait affichée dans la mauvaise
  // région. C-est vérifié, pas supposé : voir diagramme.verif.ts.
  // Rayon 60 et écart 32, mesurés et non choisis : c-est le couple qui ouvre
  // le plus les lentilles — la région commune à B et C passe de deux places à
  // cinq, le centre des trois de trois à huit — sans qu-aucun cercle ne sorte
  // du rectangle. Au-delà, le haut du cercle A dépasse le cadre.
  const r = 60;
  const cercles = [
    { nom: noms[0], cx: 160, cy: 68, r },
    { nom: noms[1], cx: 187.71, cy: 116, r },
    { nom: noms[2], cx: 132.29, cy: 116, r },
  ];
  const [a, b, c] = noms;
  return {
    ...commun,
    cercles,
    ancres: {
      [a]: { x: 160, y: 48 },
      [b]: { x: 213, y: 130 },
      [c]: { x: 107, y: 130 },
      [a + b]: { x: 189, y: 84 },
      [a + c]: { x: 131, y: 84 },
      [b + c]: { x: 160, y: 133 },
      [a + b + c]: { x: 160, y: 100 },
      [DEHORS]: { x: 42, y: 185 },
    },
    // La lettre du haut est DANS son ovale : au-dessus, il ne reste plus
    // rien depuis que les cercles se sont élargis, et elle sortait du cadre.
    // Les deux autres gardent leur place à l-extérieur, à gauche et à droite.
    etiquettes: [
      { x: 160, y: 24 },
      { x: 272, y: 148 },
      { x: 48, y: 148 },
    ],
  };
}

/** Le point est-il dans ce disque ? */
function dansLeCercle(c: Cercle, p: Point): boolean {
  return Math.hypot(p.x - c.cx, p.y - c.cy) <= c.r;
}

/**
 * La région touchée, ou `null` si le doigt est tombé hors du rectangle.
 *
 * Hors du rectangle il n-y a rien : ni ensemble, ni set universel. Mieux
 * vaut ne rien faire que ranger l-élément quelque part au hasard.
 */
export function regionDuPoint(d: Disposition, p: Point): string | null {
  const { x, y, w, h } = d.cadre;
  if (p.x < x || p.x > x + w || p.y < y || p.y > y + h) return null;
  return cleRegion(
    d.cercles.map((c) => c.nom),
    d.cercles.map((c) => dansLeCercle(c, p)),
  );
}

export type Rangement = Record<string, string[]>;

/** Les éléments déjà posés, tous régions confondues. */
export function posees(rangement: Rangement): string[] {
  return Object.values(rangement).flat();
}

/**
 * Deux rangements disent-ils la même chose ?
 *
 * L-ordre à l-intérieur d-une région ne compte pas : écrire « 15 19 » ou
 * « 19 15 » dans le milieu, c-est la même réponse. Une région absente et une
 * région vide non plus ne se distinguent pas — et les régions vides sont
 * justement une réponse, pas un oubli.
 */
export function memeRangement(a: Rangement, b: Rangement): boolean {
  const cles = new Set([...Object.keys(a), ...Object.keys(b)]);
  for (const cle of cles) {
    const ga = [...(a[cle] ?? [])].sort();
    const gb = [...(b[cle] ?? [])].sort();
    if (ga.length !== gb.length || ga.some((v, i) => v !== gb[i])) return false;
  }
  return true;
}

/** La forme attendue d'un item `diagramme`, vérifiée avant tout rendu. */
export function diagrammeJouable(p: Record<string, unknown>, a: Record<string, unknown>): boolean {
  const noms = p.sets;
  const elements = p.elements;
  if (typeof p.question !== 'string') return false;
  if (!Array.isArray(noms) || noms.length < 2 || noms.length > 3) return false;
  if (!noms.every((n) => typeof n === 'string' && n.length >= 1 && n.length <= 2)) return false;
  if (new Set(noms as string[]).size !== noms.length) return false;
  if (!Array.isArray(elements) || elements.length === 0) return false;
  if (!elements.every((e) => typeof e === 'string' && e.trim() !== '')) return false;
  if (new Set(elements as string[]).size !== elements.length) return false;

  const regions = a.regions;
  if (!regions || typeof regions !== 'object' || Array.isArray(regions)) return false;
  const connues = new Set(toutesLesRegions(noms as string[]));
  const vues: string[] = [];
  for (const [cle, valeur] of Object.entries(regions as Record<string, unknown>)) {
    if (!connues.has(cle)) return false;
    if (!Array.isArray(valeur) || !valeur.every((v) => typeof v === 'string')) return false;
    vues.push(...(valeur as string[]));
  }
  // Chaque élément est rangé une fois et une seule : sans cela, la question
  // serait impossible à réussir ou réussie sans tout poser.
  if (vues.length !== elements.length) return false;
  return [...vues].sort().join('\u0000') === [...(elements as string[])].sort().join('\u0000');
}

/* ────────────────────────── où poser les étiquettes ──────────────────────── */

/**
 * Une étiquette posée, en coordonnées du dessin.
 *
 * Les pastilles vivent désormais DANS le svg, dans les mêmes unités que les
 * cercles. En html, elles gardaient leur taille en pixels pendant que le
 * dessin, lui, s-étirait à la largeur de l-écran : la place qu-elles
 * occupaient dans la figure changeait d-un téléphone à l-autre, et le calcul
 * ne pouvait pas être juste partout à la fois.
 */
export type Place = Point & { w: number; h: number };

export const HAUTEUR_PASTILLE = 16;

export function largeurPastille(texte: string): number {
  return Math.max(18, 9 + texte.length * 8);
}

/** Le pas du quadrillage où l-on cherche une place. */
const PAS = 4;

const lattices = new Map<string, Array<Point & { region: string }>>();

function quadrillage(d: Disposition): Array<Point & { region: string }> {
  const cle = d.cercles.map((c) => c.nom).join('|');
  const connu = lattices.get(cle);
  if (connu) return connu;
  const points: Array<Point & { region: string }> = [];
  const { x, y, w, h } = d.cadre;
  for (let py = y + 2; py <= y + h - 2; py += PAS) {
    for (let px = x + 2; px <= x + w - 2; px += PAS) {
      const region = regionDuPoint(d, { x: px, y: py });
      if (region) points.push({ x: px, y: py, region });
    }
  }
  lattices.set(cle, points);
  return points;
}

/** La pastille entière tient-elle dans la région, coins compris ? */
function tientDedans(d: Disposition, region: string, p: Point, w: number, h: number): boolean {
  const dx = w / 2;
  const dy = h / 2;
  const coins = [
    p,
    { x: p.x - dx, y: p.y - dy },
    { x: p.x + dx, y: p.y - dy },
    { x: p.x - dx, y: p.y + dy },
    { x: p.x + dx, y: p.y + dy },
  ];
  return coins.every((c) => regionDuPoint(d, c) === region);
}

/**
 * Où poser les étiquettes d-une région, sans qu-aucune n-en sorte.
 *
 * Elles étaient alignées sur une seule rangée centrée sur l-ancre : à cinq,
 * elles débordaient largement du cercle, et un élément dessiné hors de sa
 * région dit le contraire de ce que l-exercice enseigne.
 *
 * On cherche donc de vraies places : les points du quadrillage qui sont dans
 * la région ET dont la pastille entière y tient, les plus proches du centre
 * d-abord, sans qu-elles se recouvrent. Le groupe se forme alors tout seul,
 * en grappe plutôt qu-en file, et il épouse la forme de la région — large
 * dans un croissant, empilé dans une lentille étroite.
 *
 * Si la région est vraiment trop petite, on empile sur l-ancre plutôt que de
 * ne rien afficher : mieux vaut une pastille serrée qu-un élément invisible.
 */
/**
 * Les tailles essayées, de la plus confortable à la plus serrée.
 *
 * Une lentille de trois ovales est étroite : à taille pleine, deux pastilles
 * n-y tiennent pas côte à côte. Plutôt que de les laisser déborder, on les
 * rétrécit — jusqu-à un plancher, en dessous duquel un enfant de sept ans ne
 * lirait plus le nombre.
 */
const ECHELLES = [1, 0.86, 0.74, 0.62];

/** La place que prend le nom d-un ensemble, et qu-aucune pastille ne doit prendre. */
const BOITE_LETTRE = { w: 26, h: 26 };

function surUneLettre(d: Disposition, p: Point, w: number, h: number): boolean {
  return d.etiquettes.some(
    (e) =>
      Math.abs(e.x - p.x) < (BOITE_LETTRE.w + w) / 2 &&
      Math.abs(e.y - p.y) < (BOITE_LETTRE.h + h) / 2,
  );
}

function essayer(
  d: Disposition,
  region: string,
  nombre: number,
  w: number,
  h: number,
): Place[] | null {
  const ancre = d.ancres[region];
  if (!ancre) return null;
  const candidats = quadrillage(d)
    .filter((p) => p.region === region)
    .sort(
      (a, b) =>
        Math.hypot(a.x - ancre.x, a.y - ancre.y) - Math.hypot(b.x - ancre.x, b.y - ancre.y),
    );
  const places: Place[] = [];
  for (const c of candidats) {
    if (places.length >= nombre) break;
    if (!tientDedans(d, region, c, w, h)) continue;
    if (surUneLettre(d, c, w, h)) continue;
    if (places.some((p) => Math.abs(p.x - c.x) < (p.w + w) / 2 + 2 && Math.abs(p.y - c.y) < h + 2)) {
      continue;
    }
    places.push({ x: c.x, y: c.y, w, h });
  }
  return places.length === nombre ? places : null;
}

/**
 * Où poser les étiquettes d-une région, sans qu-aucune n-en sorte.
 *
 * Elles étaient alignées sur une seule rangée centrée sur l-ancre : à cinq,
 * elles débordaient largement du cercle. Un élément dessiné hors de sa
 * région dit le contraire de ce que l-exercice enseigne — et c-est le père
 * qui l-a vu, sur une capture, avant moi.
 *
 * On cherche donc de vraies places : les points du quadrillage qui sont dans
 * la région et dont la pastille entière y tient, les plus proches du centre
 * d-abord, sans recouvrement. Le groupe se forme alors tout seul, en grappe
 * plutôt qu-en file, et il épouse la forme de la région — étalé dans un
 * croissant, empilé dans une lentille étroite.
 *
 * Si rien ne tient même à la plus petite taille, on empile sur l-ancre : un
 * élément serré reste visible, un élément absent ne l-est pas. Mais ce cas
 * ne doit pas arriver dans une question écrite avec soin, et `capaciteRegion`
 * permet de le vérifier avant.
 */
export function placerEtiquettes(
  d: Disposition,
  region: string,
  etiquettes: string[],
): Place[] {
  if (etiquettes.length === 0) return [];
  const base = Math.max(...etiquettes.map(largeurPastille));
  for (const e of ECHELLES) {
    const trouve = essayer(d, region, etiquettes.length, base * e, HAUTEUR_PASTILLE * e);
    if (trouve) return trouve;
  }
  const ancre = d.ancres[region] ?? { x: d.cadre.x + 20, y: d.cadre.y + 20 };
  const h = HAUTEUR_PASTILLE * ECHELLES[ECHELLES.length - 1];
  return etiquettes.map((_, i) => ({
    x: ancre.x,
    y: ancre.y + (i - (etiquettes.length - 1) / 2) * (h + 1),
    w: base * ECHELLES[ECHELLES.length - 1],
    h,
  }));
}

/**
 * Combien d-étiquettes une région peut porter sans qu-aucune n-en sorte.
 *
 * Sert à écrire les questions en connaissance de cause : une région à
 * laquelle on demande plus que sa capacité donnerait un dessin faux.
 */
export function capaciteRegion(
  d: Disposition,
  region: string,
  // Deux chiffres : le cas courant, et le plus large de nos étiquettes. La
  // mesurer avec une largeur arbitraire annonçait une capacité que le vrai
  // placement ne tenait pas.
  largeur = largeurPastille('10'),
): number {
  const petit = ECHELLES[ECHELLES.length - 1];
  for (let n = 1; n <= 12; n += 1) {
    if (!essayer(d, region, n, largeur * petit, HAUTEUR_PASTILLE * petit)) return n - 1;
  }
  return 12;
}
