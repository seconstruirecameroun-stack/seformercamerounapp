/**
 * Lire TOUTES les lignes d'une requête, page après page.
 *
 * Supabase ne renvoie jamais plus d'un nombre fixe de lignes par requête
 * (mille, par défaut), et il le fait SANS ERREUR : la liste arrive
 * simplement tronquée. Pour le journal d'un enfant qui répond tous les
 * jours, c'est une question de semaines. Passé ce seuil :
 *
 *   le rapport du parent, qui lit les réponses de la plus ancienne à la plus
 *   récente, ne voyait plus que les mille premières — toute l'activité
 *   récente disparaissait ;
 *
 *   le tableau de bord comptait mal les bonnes réponses, et une étape
 *   franchie pouvait s'afficher comme à faire ;
 *
 *   le total d'étoiles, fait de la somme des récompenses, plafonnait.
 *
 * `page` reçoit les bornes de la tranche à lire (incluses) et rend la
 * requête bornée par `.range(de, a)`. La requête doit être TRIÉE sur une
 * clé stable : sans ordre, deux pages peuvent se recouvrir ou laisser un
 * trou.
 *
 * On avance du nombre de lignes réellement reçues, et non de la taille
 * demandée : si le serveur plafonne plus bas, aucune ligne n'est sautée. On
 * s'arrête sur une page vide.
 */
export async function toutLire<T>(
  page: (de: number, a: number) => PromiseLike<{ data: unknown; error: unknown }>,
  taille = 1000,
): Promise<T[]> {
  const sortie: T[] = [];
  let de = 0;
  // Une borne de sécurité : jamais plus de cent pages, quoi qu'il arrive.
  for (let tour = 0; tour < 100; tour++) {
    const { data, error } = await page(de, de + taille - 1);
    if (error) throw error;
    const lot = (data ?? []) as T[];
    if (lot.length === 0) return sortie;
    sortie.push(...lot);
    de += lot.length;
  }
  return sortie;
}
