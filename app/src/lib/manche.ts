import { supabase } from './supabase';
import type { NotionAvecItems, Question } from './paliers';

/**
 * La manche de validation.
 *
 * Franchir les quatre étapes fait avancer ; valider la leçon certifie. La
 * validation demande le sans-faute : chaque question doit tomber juste. C'est
 * volontairement dur — une leçon sue ne se récite pas à huit sur dix.
 *
 * Elle se joue en SÉRIES d'une douzaine de questions. La règle du sans-faute
 * ne change pas d'un iota ; c'est la distance sur laquelle on l'exige qui
 * change, et le découpage est expliqué au-dessus de decouperEnSeries.
 *
 * Trois règles de mécanique l'accompagnent, et aucune n'est cosmétique :
 *
 *   La série va jusqu'au bout. Une faute ne l'interrompt pas : l'enfant
 *   répond à tout, voit chaque correction, et le verdict tombe à la fin.
 *   Couper à la première erreur lui retirerait les explications qu'il avait
 *   encore à lire, et le punirait deux fois.
 *
 *   Ce qu'il a raté est ce qu'on lui redonne. Avant de reproposer la série,
 *   on repasse sur les notions fautives seules. Rejouer douze questions
 *   identiques pour une erreur sur les arêtes n'apprend rien sur les arêtes.
 *
 *   La validation se perd. Si une notion d'une série tenue est ratée plus
 *   tard en révision, cette série est à refaire — elle seule, pas la leçon
 *   entière. C'est la seule exception au principe « rater fait revenir, pas
 *   reculer » de toute l'app, et elle est assumée : ce principe protège
 *   l'apprentissage, qui est fragile, tandis que la validation est une
 *   affirmation faite au parent. Une affirmation devenue fausse ne vaut rien.
 *   Seule la validation se perd — les étapes, les images, les étoiles et les
 *   trophées ne bougent pas.
 *
 * Rien de tout cela n'est stocké comme un état. La table manches journalise
 * ce qui a été joué, et l'état s'en déduit, comme l'étape courante se déduit
 * déjà des tentatives. Une colonne « validée » tenue à la main devrait être
 * corrigée à chaque erreur en révision, et finirait par mentir.
 */

/**
 * Ce que rapporte une manche.
 *
 * Elle valait 120 étoiles à plat, et rien du tout en cas de faute. Les
 * quarante premières manches jouées ont montré deux défauts de cette règle :
 *
 *   Une manche de 40 questions rapportait autant qu-une de 15, alors
 *   qu-elle demande près de trois fois le travail.
 *
 *   Vingt-huit manches ont été ratées, dont NEUF par une seule faute —
 *   38/40, 31/32, 29/30. Celui qui manquait une question recevait
 *   exactement ce que recevait celui qui en manquait douze : zéro.
 *
 * D-où les deux règles ci-dessous. Elles ne touchent qu-aux ÉTOILES : la
 * validation, elle, continue d-exiger le sans-faute. On sépare la
 * récompense, qui encourage, du certificat, qui affirme au parent que
 * l-enfant sait sa leçon. Une affirmation ne se donne pas au prorata.
 *
 * Le découpage en séries ne change pas le prix d-une leçon : cinq étoiles
 * par question, série par série, fait exactement le total d-avant.
 */

/** La série gagnée : cinq étoiles par question, donc proportionnelle. */
export const POINTS_PAR_QUESTION = 5;

/**
 * La consolation : deux étoiles par bonne réponse, à partir de 80 %.
 *
 * Elle n-est versée que si le score BAT le meilleur déjà fait sur cette
 * série. Sans cette condition, rejouer indéfiniment la même série à 9/10
 * rapporterait à chaque fois — on paierait la répétition au lieu du progrès,
 * et l-enfant n-aurait plus de raison de chercher la dernière.
 */
export const POINTS_PAR_JUSTE = 2;
export const SEUIL_CONSOLATION = 0.8;

/** Les étoiles d-une série gagnée, proportionnelles à sa longueur. */
export function pointsManche(questions: number): number {
  return POINTS_PAR_QUESTION * questions;
}

/**
 * Les étoiles d-une série ratée mais passée tout près.
 *
 * `meilleurPrecedent` est le plus grand nombre de bonnes réponses déjà
 * obtenu sur cette série. Zéro si c-est la première.
 */
export function pointsConsolation(
  justes: number,
  questions: number,
  meilleurPrecedent: number,
): number {
  if (questions <= 0) return 0;
  if (justes >= questions) return 0; // gagnée : ce n-est pas une consolation
  if (justes / questions < SEUIL_CONSOLATION) return 0;
  if (justes <= meilleurPrecedent) return 0;
  return POINTS_PAR_JUSTE * justes;
}

/**
 * La longueur visée d-une série.
 *
 * Quinze ne sert pas à couper, il sert à COMPTER : le nombre de séries est
 * `arrondi au-dessus de total / 15`, puis les notions sont réparties pour que
 * les séries soient aussi égales que possible. Une leçon de 22 questions fait
 * donc deux séries de onze, et non une de 22.
 *
 * Deux écueils ont été essayés avant d-en arriver là, et tous deux mesurés :
 *
 *   Quinze pris comme CIBLE d-arrondi ordinaire ramenait à une seule manche
 *   les 33 leçons de 15 à 24 questions — le tiers du catalogue, et exactement
 *   ce que le découpage corrige. D-où l-arrondi au-dessus.
 *
 *   Quinze pris comme PLAFOND dur cassait l-appariement : deux notions de
 *   huit questions font seize, donc elles ne pouvaient jamais aller ensemble,
 *   et la leçon la plus longue du catalogue — 85 questions en onze notions —
 *   tombait en DIX séries de huit. Une série a donc le droit de dépasser
 *   quinze d-une notion quand s-arrêter avant l-éloignerait davantage de la
 *   longueur visée.
 *
 * Ce que coûte le passage de dix à quinze, dit honnêtement : à 96 % de
 * justesse par question — la justesse mesurée sur les manches jouées — dix
 * questions passent sans faute deux fois sur trois, treize trois fois sur
 * cinq, quinze un peu plus d-une fois sur deux. C-est le choix du parent,
 * fait en connaissance du chiffre : moins de séries, chacune un peu plus
 * dure, et toujours très loin des trois fois sur dix d-une leçon entière.
 *
 * Une notion n-est jamais coupée en deux : une notion qui porterait à elle
 * seule plus de quinze questions fait donc une série plus longue, et c-est
 * assumé — la couper rendrait la série indicible.
 */
export const VISEE_SERIE = 15;

/**
 * Au-delà de ce nombre de questions, une leçon ne se joue plus d-un seul tenant.
 *
 * Sans ce plancher, les huit leçons de QUINZE questions pile — le minimum du
 * catalogue — restaient une manche unique, puisque quinze sur quinze donne
 * une série. C-est le seul cas où le découpage ne découpait rien, et c-était
 * aussi le pire : à la justesse mesurée, quinze questions d-affilée passent
 * sans faute un peu plus d-une fois sur deux, quand deux séries de sept ou
 * huit passent chacune près de trois fois sur quatre.
 *
 * Il ne s-applique qu-au compte INITIAL, jamais au recompte qui suit une
 * fermeture : une leçon de trente questions doit faire deux séries de quinze,
 * et non trois parce que le reste de quinze se serait recoupé en deux.
 *
 * Quatorze et non quinze, pour que le plancher dise exactement « quinze se
 * coupe » sans décaler les leçons plus longues d-une série.
 */
export const MANCHE_SEULE_MAX = 14;

/** Le strict nécessaire pour découper : un identifiant, un nombre de questions. */
export type NotionComptable = { id: string; items: unknown[] };

/**
 * La leçon découpée en séries, sur les frontières de notions.
 *
 * Pourquoi on ne coupe pas une notion : une série doit pouvoir se dire en une
 * phrase — « ces trois notions, complètement ». Une demi-notion ne se dit pas,
 * et l-enfant qui rate la seconde moitié ne saurait pas quoi réviser.
 *
 * Le nombre de séries est fixé d-abord, à partir du total, puis les notions
 * sont réparties pour que les séries soient aussi égales que possible : à
 * chaque notion on se demande si fermer ici approche la cible davantage que
 * continuer. En cas d-égalité on continue, pour ne pas laisser de moignon de
 * trois questions à la fin.
 *
 * Une notion sans question approuvée est écartée. Elle ne donnerait rien à
 * jouer, et sa présence dans la liste d-une série empêcherait cette série
 * d-être jamais reconnue comme couverte.
 */
export function decouperEnSeries<T extends NotionComptable>(notions: T[]): T[][] {
  const jouables = notions.filter((n) => n.items.length > 0);
  const total = jouables.reduce((n, x) => n + x.items.length, 0);
  if (total === 0) return [];

  const series: T[][] = [];
  let courante: T[] = [];
  let dedans = 0;
  let restant = total;
  // Combien de séries il reste à ouvrir, recalculé à chaque fermeture. Fixé
  // une fois pour toutes, il laissait la dernière série déborder le plafond
  // dès que les notions tombaient mal.
  let aOuvrir =
    total > MANCHE_SEULE_MAX ? Math.max(2, Math.ceil(total / VISEE_SERIE)) : 1;

  for (let i = 0; i < jouables.length; i++) {
    const notion = jouables[i];
    courante.push(notion);
    dedans += notion.items.length;
    restant -= notion.items.length;

    const apres = jouables.length - 1 - i;
    if (apres === 0) continue; // la dernière série prend le reste

    const suivante = jouables[i + 1].items.length;
    // La dernière série à ouvrir prend tout le reste — et comme aOuvrir est
    // recalculé à chaque fermeture, elle ne vaut un que si ce reste tient
    // sous la longueur visée. Il faut aussi garder une notion pour chaque
    // série encore à ouvrir.
    if (aOuvrir <= 1) continue;
    if (apres < aOuvrir - 1) continue;

    const cible = (dedans + restant) / aOuvrir;
    // On ferme ici si s-arrêter approche la longueur visée davantage que
    // continuer. En cas d-égalité on continue, pour ne pas laisser de
    // moignon de trois questions à la fin.
    if (Math.abs(dedans - cible) < Math.abs(dedans + suivante - cible)) {
      series.push(courante);
      courante = [];
      dedans = 0;
      aOuvrir = Math.max(1, Math.ceil(restant / VISEE_SERIE));
    }
  }
  if (courante.length > 0) series.push(courante);
  return series;
}

/**
 * Quand chaque notion est entrée dans la leçon : son identifiant, sa date.
 *
 * Sans cette table, une manche d-avant le découpage couvrirait une notion
 * ajoutée APRÈS qu-elle a été jouée. Le cas s-est produit : deux parties
 * manquaient à la leçon de la lampe à pétrole, on les a ajoutées, et la
 * leçon affichait toujours « validée » alors qu-il n-avait jamais vu ces
 * deux notions-là. L-affirmation faite au parent était devenue fausse.
 */
export type Naissances = Record<string, string>;

/**
 * La série est-elle entièrement couverte par cette manche jouée ?
 *
 * Deux cas, et le second est le délicat. Une manche qui porte la liste de
 * ses notions se lit directement. Une manche d-AVANT le découpage, elle,
 * n-a pas de liste : elle portait toute la leçon — toute la leçon TELLE
 * QU-ELLE ÉTAIT CE JOUR-LÀ. Elle ne couvre donc une notion que si cette
 * notion existait déjà quand elle a été jouée.
 *
 * Une notion dont on ignore la date n-est pas couverte. C-est le sens de
 * prudence : sur-affirmer fait mentir la médaille, sous-affirmer fait
 * seulement rejouer une série. Entre les deux, on rejoue.
 */
function couvre(m: MancheRow, serie: string[], naissances: Naissances): boolean {
  const notions = m.notions ?? [];
  if (notions.length === 0) {
    return serie.every((n) => {
      const nee = naissances[n];
      return nee !== undefined && nee < m.created_at;
    });
  }
  const dans = new Set(notions);
  return serie.every((n) => dans.has(n));
}

/** La manche jouée portait-elle exactement cette série ? */
function memeSerie(m: MancheRow, serie: string[]): boolean {
  const notions = m.notions ?? [];
  if (notions.length !== serie.length) return false;
  const dans = new Set(notions);
  return serie.every((n) => dans.has(n));
}

/**
 * Le meilleur nombre de bonnes réponses déjà obtenu sur une série.
 *
 * Seules les manches portant exactement cette série comptent : comparer les
 * 9 justes d-une série de dix aux 28 justes d-une leçon entière interdirait
 * toute consolation. Les manches d-avant le découpage sont donc écartées, et
 * la première série jouée repart d-un meilleur à zéro — une consolation de
 * plus, une seule fois, et c-est sans conséquence.
 */
export function meilleurJustes(manches: MancheRow[], serie: string[]): number {
  let meilleur = 0;
  for (const m of manches) {
    if (!memeSerie(m, serie)) continue;
    if (m.justes > meilleur) meilleur = m.justes;
  }
  return meilleur;
}

/**
 * La série de manches parfaites en cours, toutes leçons confondues.
 *
 * On compte depuis la plus récente et on s-arrête à la première ratée. Une
 * série se voit, se rompt et se reconstruit : c-est ce qui en fait un
 * encouragement plutôt qu-un total de plus.
 *
 * `manches` arrive de la plus récente à la plus ancienne, comme partout
 * ailleurs dans ce fichier.
 */
export function serieParfaite(manches: MancheRow[]): number {
  let serie = 0;
  for (const m of manches) {
    if (!m.reussie) break;
    serie += 1;
  }
  return serie;
}

/** Au-delà, la reprise devient une séance comme une autre. */
export const TAILLE_REPRISE = 6;

export type EtatValidation = {
  /** La leçon est validée aujourd'hui : toutes ses séries sont tenues. */
  validee: boolean;
  /** Date où la dernière série manquante est tombée, même si perdue depuis. */
  obtenueLe: string | null;
  /** La première réponse fausse qui a fait perdre la validation. */
  perdueLe: string | null;
  /** Les notions à redonner avant de reproposer la série en cours. */
  aReprendre: string[];
  /** La série en cours a déjà été tentée. */
  dejaTentee: boolean;
  /**
   * La série en cours avait été gagnée, puis une faute l'a cassée.
   *
   * L'écran d'annonce ne dit pas la même chose à qui tente une série pour la
   * première fois et à qui vient la regagner. Et ce n'est pas `perdueLe`,
   * qui ne parle que de la leçon entière : une série peut tomber alors que
   * les autres n'ont jamais été gagnées.
   */
  serieARegagner: boolean;
  /** Le rang de la série à jouer, de 1 à seriesTotal. Zéro si tout est tenu. */
  serieEnCours: number;
  /** Les notions de la série à jouer. */
  notionsDeLaSerie: string[];
  /** Combien de séries la leçon compte. */
  seriesTotal: number;
  /** Combien sont tenues aujourd'hui. */
  seriesTenues: number;
};

export type MancheRow = {
  lesson_id: string;
  questions: number;
  justes: number;
  reussie: boolean;
  notions_ratees: string[];
  /** Les notions de la série jouée. Vide = toute la leçon (manches d'avant). */
  notions?: string[] | null;
  created_at: string;
};

export type Reponse = { notion_id: string; correct: boolean; created_at: string };

/**
 * Les notions encore à reprendre, parmi celles qu'on avait notées fautives.
 *
 * Une notion sort de la liste dès que sa réponse la plus récente, depuis le
 * moment de référence, est juste. Sans cette sortie, la reprise ne finirait
 * jamais : la manche ratée garderait pour toujours la trace des notions
 * manquées, et l'enfant rejouerait les mêmes questions à l'infini sans
 * jamais revoir la manche.
 */
function encoreARevoir(
  candidates: string[],
  reponses: Reponse[],
  depuis: string,
): string[] {
  const derniere = new Map<string, Reponse>();
  for (const r of reponses) {
    if (r.created_at <= depuis) continue;
    const connue = derniere.get(r.notion_id);
    if (!connue || r.created_at > connue.created_at) derniere.set(r.notion_id, r);
  }
  // Pas de réponse depuis : la notion reste à revoir, elle n'a pas été reprise.
  return [...new Set(candidates)].filter((n) => !(derniere.get(n)?.correct ?? false));
}

/** L'état d'une série : gagnée quand, cassée par quoi. */
type EtatSerie = {
  notions: string[];
  gagneeLe: string | null;
  fauteDepuis: string | null;
  tenue: boolean;
};

/**
 * L'état de validation, déduit des manches jouées et du journal des réponses.
 *
 * `series` porte les notions de chaque série, dans l'ordre de la leçon. Elle
 * est recalculée par decouperEnSeries à chaque fois, et non stockée : le
 * découpage doit suivre la leçon si une notion y est ajoutée.
 *
 * `reponses` porte les réponses de l'enfant sur les notions de cette leçon,
 * justes et fausses, avec leur date. L'appelant les a déjà lues pour situer
 * l'étape : on ne relit pas le journal une seconde fois.
 *
 * `naissances` donne la date d'entrée de chaque notion dans la leçon. Elle
 * ne sert qu'aux manches d'avant le découpage, et elle leur est
 * indispensable : voir couvre, plus haut.
 */
export function lireValidation(
  series: string[][],
  manches: MancheRow[],
  reponses: Reponse[],
  naissances: Naissances,
): EtatValidation {
  const fausses = reponses.filter((r) => !r.correct);

  // Les manches arrivent de la plus récente à la plus ancienne.
  const etats: EtatSerie[] = series.map((notions) => {
    const dedans = new Set(notions);
    const gagnante = manches.find((m) => m.reussie && couvre(m, notions, naissances)) ?? null;
    const gagneeLe = gagnante?.created_at ?? null;
    // Une faute postérieure à la série gagnée l'annule. On prend la première :
    // c'est elle qui dit quand il a cessé de savoir.
    const faute = gagneeLe
      ? (fausses
          .filter((f) => dedans.has(f.notion_id) && f.created_at > gagneeLe)
          .sort((a, b) => a.created_at.localeCompare(b.created_at))[0] ?? null)
      : null;
    return {
      notions,
      gagneeLe,
      fauteDepuis: faute?.created_at ?? null,
      tenue: gagneeLe !== null && faute === null,
    };
  });

  const validee = etats.length > 0 && etats.every((e) => e.tenue);
  const rang = etats.findIndex((e) => !e.tenue);
  const courante = rang >= 0 ? etats[rang] : null;

  // « Validée le 18, perdue le 25 » ne se dit que si elle l'a vraiment été :
  // il faut que CHAQUE série soit tombée un jour. Une seule série gagnée puis
  // cassée sur trois n'a jamais validé la leçon.
  const toutesTombees = etats.length > 0 && etats.every((e) => e.gagneeLe !== null);
  const obtenueLe = toutesTombees
    ? etats.map((e) => e.gagneeLe!).sort((a, b) => a.localeCompare(b))[etats.length - 1]
    : null;
  const perdueLe =
    toutesTombees && !validee
      ? (etats
          .map((e) => e.fauteDepuis)
          .filter((d): d is string => d !== null)
          .sort((a, b) => a.localeCompare(b))[0] ?? null)
      : null;

  let aReprendre: string[] = [];
  let dejaTentee = false;

  if (courante) {
    const dedans = new Set(courante.notions);
    if (courante.gagneeLe !== null) {
      // Elle était tenue : on redonne ce qui l'a fait tomber.
      dejaTentee = true;
      const depuis = courante.gagneeLe;
      // Une série retentée et ratée depuis la perte dit mieux ce qui reste à
      // revoir que les fautes de révision : elle a reposé TOUTES les
      // questions, donc elle a vu des notions que la révision n'a pas
      // touchées. Sans cette préférence, l'enfant retentait la série en
      // n'ayant revu qu'une des deux notions qu'il venait de manquer.
      const retentee =
        manches.find(
          (m) => !m.reussie && couvre(m, courante.notions, naissances) && m.created_at > depuis,
        ) ?? null;
      aReprendre = retentee
        ? encoreARevoir(
            retentee.notions_ratees.filter((n) => dedans.has(n)),
            reponses,
            retentee.created_at,
          )
        : encoreARevoir(
            fausses
              .filter((f) => dedans.has(f.notion_id) && f.created_at > depuis)
              .map((f) => f.notion_id),
            reponses,
            depuis,
          );
    } else {
      const derniere = manches.find((m) => couvre(m, courante.notions, naissances)) ?? null;
      dejaTentee = derniere !== null;
      if (derniere && !derniere.reussie) {
        aReprendre = encoreARevoir(
          derniere.notions_ratees.filter((n) => dedans.has(n)),
          reponses,
          derniere.created_at,
        );
      }
    }
  }

  return {
    validee,
    obtenueLe,
    perdueLe,
    aReprendre,
    dejaTentee,
    serieARegagner: courante !== null && courante.gagneeLe !== null,
    serieEnCours: rang >= 0 ? rang + 1 : 0,
    notionsDeLaSerie: courante?.notions ?? [],
    seriesTotal: etats.length,
    seriesTenues: etats.filter((e) => e.tenue).length,
  };
}

/**
 * Toutes les questions des notions données, dans l'ordre où elles s'apprennent.
 *
 * Notion par notion, et à l'intérieur d'une notion de l'étape la plus facile à
 * la plus difficile. Un ordre au hasard ferait sauter l'enfant d'une notion à
 * l'autre et d'une forme de question à l'autre dix fois de suite, ce qui est
 * une épreuve de souplesse et non de savoir.
 */
export function questionsDeLaManche(notions: NotionAvecItems[]): Question[] {
  const questions: Question[] = [];
  for (const notion of notions) {
    const items = [...notion.items].sort((a, b) => a.level - b.level || a.id.localeCompare(b.id));
    for (const item of items) questions.push({ notion, item });
  }
  return questions;
}

/** Enregistre la série jouée. Le verdict est le compte, pas une appréciation. */
export async function enregistrerManche(params: {
  parentId: string;
  childId: string;
  lessonId: string;
  questions: number;
  justes: number;
  notionsRatees: string[];
  /** Les notions de la série : sans elles, la ligne ne se déduit plus. */
  notions: string[];
}): Promise<void> {
  const { parentId, childId, lessonId, questions, justes, notionsRatees, notions } = params;
  const { error } = await supabase.from('manches').insert({
    parent_id: parentId,
    child_id: childId,
    lesson_id: lessonId,
    questions,
    justes,
    reussie: justes === questions,
    notions_ratees: [...new Set(notionsRatees)],
    notions: [...new Set(notions)],
  });
  if (error) throw error;
}
