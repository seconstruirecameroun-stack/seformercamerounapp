/**
 * Lecture à voix haute, par la synthèse du navigateur.
 *
 * Un enfant de primaire lit lentement, et certains cours arrivent dans une
 * langue qui n'est pas celle qu'il parle à la maison. Entendre la phrase aide,
 * et ne coûte ni octet de réseau ni génération.
 *
 * La voix est celle du système : elle n'a pas la qualité de la narration des
 * vidéos, mais elle est disponible hors-ligne et immédiatement.
 */

const LANGUES: Record<string, string> = { fr: 'fr-FR', en: 'en-US' };

export function peutParler(): boolean {
  return typeof window !== 'undefined' && 'speechSynthesis' in window;
}

export function lire(texte: string, langue = 'fr') {
  if (!peutParler()) return;
  window.speechSynthesis.cancel();
  const phrase = new SpeechSynthesisUtterance(texte);
  phrase.lang = LANGUES[langue] ?? LANGUES.fr;
  // Un peu plus lent que la normale : on lit pour comprendre, pas pour aller
  // vite.
  phrase.rate = 0.9;
  window.speechSynthesis.speak(phrase);
}

export function stopper() {
  if (peutParler()) window.speechSynthesis.cancel();
}
