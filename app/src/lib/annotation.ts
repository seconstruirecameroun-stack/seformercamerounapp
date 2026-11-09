/**
 * Annoter un schéma.
 *
 * La révision du 9 novembre demande deux fois le même geste : des numéros
 * posés sur un dessin, et une liste à compléter en face. C'est la forme la
 * plus fréquente des épreuves de sciences de sa classe, et aucun type ne
 * savait la poser — on pouvait lui demander ce que fait le réservoir, pas
 * lui faire RECONNAÎTRE le réservoir sur le dessin.
 *
 * POURQUOI LES REPÈRES NE SONT PAS EN BASE. On aurait pu stocker des
 * coordonnées et poser les numéros par-dessus l'image au moment du rendu.
 * Ils sont au contraire dessinés DANS la figure, par le script qui dessine
 * la figure, et la base ne porte que les noms à mettre en face.
 *
 * La raison est qu'une coordonnée stockée se décale. La figure est redessinée
 * quand une leçon change, et deux fichiers qui doivent rester d'accord sur la
 * position d'un point finissent toujours par ne plus l'être — le numéro 3 se
 * retrouve dans le vide, et l'enfant répond à une question qui ne montre
 * rien. Le numéro gravé dans l'image ne peut pas se désaligner de l'image.
 *
 * En échange, c'est le script de figures qui porte la vérité des positions,
 * et c'est lui qui doit vérifier que ses numéros vont bien de 1 à n.
 */

/** La forme attendue d'un item `annotation`, vérifiée avant tout rendu. */
export function annotationJouable(
  p: Record<string, unknown>,
  a: Record<string, unknown>,
): boolean {
  if (typeof p.question !== 'string' || p.question.trim() === '') return false;

  // La figure est une clé d'illustration livrée avec l'app. Une URL n'est pas
  // acceptée : une figure annotée est dessinée, jamais générée, et le contrôle
  // des numéros vit dans le script qui la dessine.
  if (typeof p.figure !== 'string' || !/^[a-z0-9-]+$/.test(p.figure)) return false;

  const etiquettes = p.etiquettes;
  if (!Array.isArray(etiquettes) || etiquettes.length < 2 || etiquettes.length > 8) return false;
  if (!etiquettes.every((e) => typeof e === 'string' && e.trim() !== '')) return false;
  if (new Set(etiquettes as string[]).size !== etiquettes.length) return false;

  // ordre[k] = l'étiquette du repère k + 1. C'est une permutation complète :
  // chaque numéro reçoit un nom, et chaque nom sert une fois. Sans cela, la
  // question serait impossible à réussir, ou réussie sans tout poser.
  const ordre = a.ordre;
  if (!Array.isArray(ordre) || ordre.length !== etiquettes.length) return false;
  if (!ordre.every((j) => Number.isInteger(j) && j >= 0 && j < etiquettes.length)) return false;
  return new Set(ordre as number[]).size === ordre.length;
}

/** Les deux réponses disent-elles la même chose ? */
export function memeAnnotation(a: Array<number | null>, attendu: number[]): boolean {
  return a.length === attendu.length && a.every((v, i) => v === attendu[i]);
}
