// COPIE GÉNÉRÉE — NE PAS ÉDITER.
// La source est supabase/functions/_shared/maison.ts ; cette copie existe
// parce que l-éditeur du tableau de bord range les fichiers à plat sous la
// fonction et n-y connaît pas « ../_shared/ ».
// Régénérer avec :  python work/plier-fonctions.py

/**
 * Les règles de la maison, écrites une seule fois pour les deux fonctions.
 *
 * Tout ce qui est ici a été appris en construisant des leçons à la main, et
 * chaque ligne corrige une faute constatée — pas une préférence de style.
 * Les commentaires disent laquelle : sans eux, la prochaine personne qui
 * relâche une contrainte ne saura pas ce qu'elle rouvre.
 */

export const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

export function base64(bytes: Uint8Array): string {
  let binaire = '';
  const pas = 0x8000; // par tranches, sinon la pile déborde sur un gros fichier
  for (let i = 0; i < bytes.length; i += pas) {
    binaire += String.fromCharCode(...bytes.subarray(i, i + pas));
  }
  return btoa(binaire);
}

/** Extrait le premier objet JSON d'une réponse, même entourée de texte. */
export function lireJson<T>(texte: string): T {
  const net = texte.trim().replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/, '');
  const debut = net.indexOf('{');
  const fin = net.lastIndexOf('}');
  if (debut === -1 || fin === -1) throw new Error('réponse sans JSON');
  return JSON.parse(net.slice(debut, fin + 1)) as T;
}

/**
 * Ce que le clavier d'un texte à trous sait taper.
 *
 * Il n'a PAS de touche espace — elle n'apparaît que pour une phrase entière.
 * Une réponse en deux mots, ou un nombre écrit « 3 000 », est donc
 * impossible à saisir : l'enfant ne peut pas la réussir, quoi qu'il tape.
 * Un seul cas de ce genre existait dans la base, et il y est resté
 * longtemps sans que personne le voie.
 */
export const TAPABLE = new Set(
  [...('abcdefghijklmnopqrstuvwxyz' + 'éèêàçùœâîôëïü’' + '0123456789' + '-,.')].flatMap((c) => [
    c,
    c.toUpperCase(),
  ]),
);

export const NIVEAUX = [1, 2, 3, 4];

export type Item = {
  kind: string;
  level: number;
  payload: Record<string, unknown>;
  answer: Record<string, unknown>;
  explain?: string | null;
};

/**
 * Vérifie une question, et dit en clair ce qui ne va pas.
 *
 * Rien de ce qui sort d'ici n'est « presque bon » : une question mal formée
 * n'est pas une question moins bonne, c'est une question qu'un enfant de
 * sept ans ne peut pas réussir, et qui comptera contre lui.
 */
export function fauteDeQuestion(it: Item): string | null {
  const p = it.payload ?? {};
  const a = it.answer ?? {};
  const txt = JSON.stringify([p, a, it.explain ?? '']);

  if (!NIVEAUX.includes(it.level)) return 'niveau hors de 1 à 4';
  // L'apostrophe droite se tape autrement que la courbe, et la comparaison
  // des réponses ne les confond pas : une seule suffit à rendre un texte à
  // trous impossible.
  if (txt.includes("'")) return 'apostrophe droite interdite, utiliser ’';
  // L'étape 4 est chronométrée. Relier ou ranger des étiquettes y est trop
  // lent : l'enfant perd sur le temps, pas sur le savoir.
  if (it.level === 4 && it.kind !== 'qcm' && it.kind !== 'vrai_faux') {
    return 'à l’étape 4, seulement qcm ou vrai_faux';
  }

  if (it.kind === 'qcm') {
    const q = String(p.question ?? '');
    const o = p.options as string[] | undefined;
    if (!q.trim()) return 'question vide';
    if (q.length > 90) return 'question de plus de 90 caractères';
    if (!Array.isArray(o) || o.length < 2 || o.length > 4) return 'il faut 2 à 4 réponses';
    if (new Set(o).size !== o.length) return 'deux réponses identiques';
    if (o.some((x) => !String(x).trim())) return 'une réponse vide';
    if (o.some((x) => String(x).length > 70)) return 'une réponse de plus de 70 caractères';
    const i = a.index;
    if (!Number.isInteger(i) || (i as number) < 0 || (i as number) >= o.length) {
      return 'index de bonne réponse invalide';
    }
    // La bonne réponse ne doit pas être reconnaissable à sa forme. Quand
    // elle est la plus longue de beaucoup, l'enfant la trouve sans lire le
    // sujet — et la manche de validation ne valide plus rien.
    const bonne = String(o[i as number]).length;
    const autres = o.filter((_, k) => k !== i).map((x) => String(x).length);
    if (bonne > Math.max(...autres) * 2) return 'la bonne réponse est bien plus longue que les autres';
    return null;
  }

  if (it.kind === 'vrai_faux') {
    const s = String(p.statement ?? '');
    if (!s.trim()) return 'affirmation vide';
    if (s.length > 110) return 'affirmation de plus de 110 caractères';
    if (typeof a.value !== 'boolean') return 'la réponse doit être vrai ou faux';
    return null;
  }

  if (it.kind === 'texte_a_trous') {
    const t = String(p.text ?? '');
    const v = a.values as string[] | undefined;
    const trous = t.split('{{').length - 1;
    if (trous < 1 || trous > 2) return 'il faut un ou deux trous';
    if (!Array.isArray(v) || v.length !== trous) return 'autant de réponses que de trous';
    if (p.blanks !== undefined && p.blanks !== trous) return 'blanks ne correspond pas aux trous';
    for (const mot of v) {
      const m = String(mot);
      if (!m.trim()) return 'réponse vide';
      if (/\s/.test(m)) return 'réponse en plusieurs mots : le clavier n’a pas d’espace';
      if (m.length > 16) return 'réponse de plus de 16 lettres';
      for (const c of m) if (!TAPABLE.has(c)) return 'caractère absent du clavier : ' + c;
    }
    return null;
  }

  if (it.kind === 'association') {
    const g = p.gauche as string[] | undefined;
    const d = p.droite as string[] | undefined;
    const o = a.order as number[] | undefined;
    if (!Array.isArray(g) || !Array.isArray(d)) return 'colonnes manquantes';
    if (g.length !== d.length) return 'les deux colonnes doivent avoir le même nombre';
    if (g.length < 2 || g.length > 4) return 'il faut 2 à 4 paires';
    if (!Array.isArray(o) || o.length !== g.length) return 'ordre de la mauvaise longueur';
    if (JSON.stringify([...o].sort((x, y) => x - y)) !== JSON.stringify(g.map((_, k) => k))) {
      return 'ordre invalide';
    }
    if ([...g, ...d].some((x) => !String(x).trim() || String(x).length > 48)) {
      return 'étiquette vide ou de plus de 48 caractères';
    }
    return null;
  }

  if (it.kind === 'chronologie') {
    const t = p.tokens as string[] | undefined;
    const o = a.order as number[] | undefined;
    if (!Array.isArray(t) || t.length < 3 || t.length > 5) return 'il faut 3 à 5 étiquettes';
    if (!Array.isArray(o) || JSON.stringify([...o].sort((x, y) => x - y)) !== JSON.stringify(t.map((_, k) => k))) {
      return 'ordre invalide';
    }
    if (t.some((x) => !String(x).trim() || String(x).length > 40)) {
      return 'étiquette vide ou de plus de 40 caractères';
    }
    return null;
  }

  return 'type de question inconnu : ' + it.kind;
}

/**
 * Une notion n'est jouable que si elle a de quoi franchir les quatre étapes.
 *
 * Sans question à un niveau, l'étape ne peut jamais être franchie : la
 * notion reste comptée dans le total, n'est jamais posée, et la leçon se
 * bloque sans rien afficher d'anormal.
 */
export function etapesManquantes(items: Item[]): number[] {
  const vus = new Set(items.map((i) => i.level));
  return NIVEAUX.filter((n) => !vus.has(n));
}

/** Les règles de rédaction, communes aux deux fonctions. */
export const TON = `Tu écris pour un enfant du primaire camerounais, entre six et onze ans.
Il lit lentement et saute tout paragraphe. Une phrase qu-il lit vaut mieux
qu-un paragraphe exact qu-il ignore. Pas de subordonnées empilées, pas de mot
savant sans le dire autrement, pas de phrase de plus de vingt mots.

Tu écris dans la langue du cours, sans jamais traduire.

Tu utilises l-apostrophe courbe ’ et jamais l-apostrophe droite.`;

export const HONNETETE = `Trois règles qui priment sur tout le reste :

1. N-ajoute aucun savoir absent du document. Chaque école a son programme ;
   compléter de mémoire produit des révisions fausses.

2. Si le document contredit ce que tu sais, transcris quand même ce qu-il dit
   et signale l-écart dans avertissements. Le parent tranchera avec
   l-enseignant. Exemple vécu : un cahier donnait les roches magmatiques
   « de couleur noire » avec le granite en exemple, qui est clair.

3. Si le document se contredit LUI-MÊME, le suivre est impossible : dis-le
   dans avertissements et retiens la version cohérente. Exemple vécu : un
   cahier écrivait « those montre des noms proches » puis, trois lignes plus
   bas, « that montre un nom éloigné » — those étant le pluriel de that, les
   deux ne peuvent pas être vrais.

Et une règle de prudence : n-interroge jamais sur un point que tu viens de
signaler comme douteux. Là où la classe et le savoir divergent, on enseigne
le cahier mais on ne pose pas la question.`;
