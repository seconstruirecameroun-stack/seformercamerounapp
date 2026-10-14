/**
 * Quel enfant utilise l'appareil en ce moment.
 *
 * Ce choix est local à l'appareil, pas une identité : les profils enfants ne
 * sont pas des comptes. Les données, elles, restent protégées par la RLS du
 * parent connecté.
 */
const KEY = 'sfc-current-child';

export function getCurrentChildId(): string | null {
  try {
    return localStorage.getItem(KEY);
  } catch {
    return null;
  }
}

export function setCurrentChildId(id: string | null) {
  try {
    if (id) localStorage.setItem(KEY, id);
    else localStorage.removeItem(KEY);
  } catch {
    /* navigation privée ou stockage bloqué : on continue sans mémoriser */
  }
}
