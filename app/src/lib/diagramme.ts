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
  const r = 56;
  const cercles = [
    { nom: noms[0], cx: 160, cy: 67, r },
    { nom: noms[1], cx: 188.6, cy: 116.5, r },
    { nom: noms[2], cx: 131.4, cy: 116.5, r },
  ];
  const [a, b, c] = noms;
  return {
    ...commun,
    cercles,
    ancres: {
      [a]: { x: 160, y: 39 },
      [b]: { x: 213, y: 130 },
      [c]: { x: 107, y: 130 },
      [a + b]: { x: 189, y: 84 },
      [a + c]: { x: 131, y: 84 },
      [b + c]: { x: 160, y: 133 },
      [a + b + c]: { x: 160, y: 100 },
      [DEHORS]: { x: 42, y: 185 },
    },
    etiquettes: [
      { x: 160, y: 18 },
      { x: 268, y: 150 },
      { x: 52, y: 150 },
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
