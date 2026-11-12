/**
 * Les sons de l'app.
 *
 * Synthétisés, et non chargés : quatre fichiers audio pèseraient plus que
 * toute l'application, et ils arriveraient en retard sur une connexion
 * camerounaise. Ici le son part au moment exact du geste — c'est ce décalage
 * de zéro milliseconde qui fait qu'un retour paraît juste.
 *
 * Volume bas par principe. L'app sera souvent ouverte dans la même pièce que
 * le reste de la famille, et un enfant qui doit couper le son d'une app finit
 * par ne plus l'ouvrir du tout.
 */

type Son =
  | 'juste' | 'faux' | 'fete' | 'coffre' | 'etape'
  | 'piece' | 'choc' | 'turbo' | 'bouclier' | 'tambour' | 'tampon' | 'serie';

let contexte: AudioContext | null = null;

function obtenirContexte(): AudioContext | null {
  if (typeof window === 'undefined') return null;
  try {
    const Classe = window.AudioContext ?? (window as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
    if (!Classe) return null;
    contexte ??= new Classe();
    // Les navigateurs suspendent le contexte tant que l'enfant n'a rien
    // touché : on le réveille au premier son, qui suit toujours un geste.
    if (contexte.state === 'suspended') void contexte.resume();
    return contexte;
  } catch {
    return null;
  }
}

/** Une note courte, montée et amortie pour ne jamais claquer. */
function note(ctx: AudioContext, frequence: number, depart: number, duree: number, volume: number) {
  const oscillateur = ctx.createOscillator();
  const gain = ctx.createGain();
  oscillateur.type = 'sine';
  oscillateur.frequency.setValueAtTime(frequence, ctx.currentTime + depart);
  gain.gain.setValueAtTime(0, ctx.currentTime + depart);
  gain.gain.linearRampToValueAtTime(volume, ctx.currentTime + depart + 0.012);
  gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + depart + duree);
  oscillateur.connect(gain).connect(ctx.destination);
  oscillateur.start(ctx.currentTime + depart);
  oscillateur.stop(ctx.currentTime + depart + duree + 0.02);
}

/**
 * Les mélodies.
 *
 * Une bonne réponse monte, une erreur descend — sans dissonance : on signale
 * une réponse à revoir, on ne gronde pas. La fête est un arpège majeur, celui
 * que tous les jeux utilisent parce qu'un enfant le reconnaît avant de savoir
 * ce qu'est un accord.
 */
const MELODIES: Record<Son, Array<[number, number, number]>> = {
  juste: [[660, 0, 0.12], [880, 0.08, 0.16]],
  faux: [[320, 0, 0.14], [240, 0.1, 0.2]],
  etape: [[523, 0, 0.12], [659, 0.1, 0.12], [784, 0.2, 0.22]],
  fete: [[523, 0, 0.1], [659, 0.08, 0.1], [784, 0.16, 0.1], [1046, 0.24, 0.3]],
  coffre: [[392, 0, 0.3], [330, 0.18, 0.35]],
  // La course : une pièce tinte, très court, car il y en a beaucoup ; un
  // choc fait « bong », sans rien de grondeur ; le turbo monte vite.
  piece: [[1318, 0, 0.06], [1760, 0.04, 0.08]],
  choc: [[220, 0, 0.12], [165, 0.07, 0.18]],
  turbo: [[392, 0, 0.08], [523, 0.05, 0.08], [659, 0.1, 0.08], [880, 0.15, 0.2]],
  bouclier: [[784, 0, 0.1], [1046, 0.07, 0.18]],
  // La remise du bulletin : un roulement grave, puis le coup sec du tampon.
  tambour: [[110, 0, 0.06], [110, 0.09, 0.06], [117, 0.18, 0.06], [117, 0.27, 0.06], [123, 0.36, 0.06], [131, 0.45, 0.06], [165, 0.56, 0.22]],
  tampon: [[196, 0, 0.12], [98, 0.03, 0.2]],
  // Une série : trois notes qui grimpent, plus vite que l'étape.
  serie: [[659, 0, 0.08], [880, 0.06, 0.08], [1175, 0.12, 0.16]],
};

export function jouerSon(son: Son) {
  const ctx = obtenirContexte();
  if (!ctx) return;
  const volume = son === 'faux' || son === 'piece' ? 0.05 : 0.07;
  for (const [frequence, depart, duree] of MELODIES[son]) {
    note(ctx, frequence, depart, duree, volume);
  }
}
