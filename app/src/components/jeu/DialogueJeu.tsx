import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import Pango, { type Humeur } from './Pango';

/**
 * Les dialogues de la course : Pango surgit, parle, et repart.
 *
 * Une case de bande dessinée posée sur tout l'écran : un soleil de couleur
 * qui tourne, Pango qui entre d'un bond, une bulle qui éclate, des étoiles
 * qui volent — et, sur un choc, l'écran qui tremble. C'est ce qui donne du
 * poids à une bonne réponse : l'enfant ne voit pas seulement la voiture
 * accélérer, quelqu'un le félicite.
 *
 * TROIS RÈGLES, pour que ce soit une fête et pas une gêne :
 *
 *   le dialogue ne bloque rien — il laisse passer le doigt, l'enfant peut
 *   déjà répondre à la question suivante ;
 *
 *   il est court — moins de deux secondes, une seconde et demie pour le
 *   turbo, qui revient à chaque bonne réponse ;
 *
 *   un seul à la fois — les autres attendent leur tour, sans se chevaucher.
 *
 * Les phrases changent d'une fois à l'autre : la même phrase à chaque bonne
 * réponse ne serait plus entendue à la cinquième.
 */

export type GenreDialogue = 'turbo' | 'bouclier' | 'choc' | 'ville';

export type Dialogue = {
  cle: number;
  genre: GenreDialogue;
  titre: string;
  phrase: string;
};

const STYLE: Record<GenreDialogue, { soleil: string; titre: string; humeur: Humeur; duree: number }> = {
  turbo: { soleil: '#f5b335', titre: '#c2410c', humeur: 'boule', duree: 1500 },
  bouclier: { soleil: '#7fd3f7', titre: '#0e6a96', humeur: 'fier', duree: 1900 },
  choc: { soleil: '#f3a5a0', titre: '#b42318', humeur: 'surpris', duree: 1700 },
  ville: { soleil: '#9ad48a', titre: '#2f7d32', humeur: 'joie', duree: 2100 },
};

const PHRASES: Record<GenreDialogue, string[]> = {
  turbo: ['Accroche-toi !', 'On décolle !', 'Trop rapide !', 'Bonne réponse, plein gaz !', 'Fiiiiiouuu !'],
  bouclier: ['Trois de suite : tu es protégé !', 'Rien ne peut nous arrêter !', 'La carapace d’or est à toi !'],
  choc: ['Pas grave, on repart !', 'On se relève et on fonce !', 'La prochaine, on l’aura !'],
  ville: ['Quel voyage !', 'Encore une ville de gagnée !', 'On continue la route ?'],
};

const TITRES_CHOC: Record<string, string> = {
  chevre: 'Bêêê ! Une chèvre !',
  trou: 'Boum ! Un trou !',
  flaque: 'Splash ! Tout mouillé !',
  carton: 'Patatras !',
};

let compteur = 0;

/** Fabrique un dialogue, avec une phrase tirée au sort. */
export function dialogue(genre: GenreDialogue, detail?: string): Dialogue {
  const phrases = PHRASES[genre];
  const titre =
    genre === 'turbo' ? 'TURBO !'
      : genre === 'bouclier' ? 'BOUCLIER !'
        : genre === 'choc' ? TITRES_CHOC[detail ?? ''] ?? 'Aïe !'
          : 'Bienvenue à ' + (detail ?? '') + ' !';
  compteur += 1;
  // L'espace avant « ! » est insécable : sur un téléphone, un point
  // d'exclamation seul en début de ligne casse l'effet.
  const insecable = (t: string) => t.replace(/ ([!?:])/g, ' $1');
  return {
    cle: Date.now() * 10 + (compteur % 10),
    genre,
    titre: insecable(titre),
    phrase: insecable(phrases[Math.floor(Math.random() * phrases.length)]),
  };
}

/** Le soleil de bande dessinée : seize rayons, alternés. */
function Soleil({ couleur }: { couleur: string }) {
  const points: string[] = [];
  for (let i = 0; i < 32; i++) {
    const a = (i / 32) * Math.PI * 2;
    const r = i % 2 ? 34 : 50;
    points.push(`${50 + Math.cos(a) * r},${50 + Math.sin(a) * r}`);
  }
  return (
    <svg viewBox="0 0 100 100" className="dialogue-soleil absolute inset-0 h-full w-full" aria-hidden>
      <polygon points={points.join(' ')} fill={couleur} />
      <circle cx={50} cy={50} r={30} fill="#fff" opacity={0.35} />
    </svg>
  );
}

/** Les étoiles qui partent du personnage, chacune dans sa direction. */
function Etoiles({ couleur }: { couleur: string }) {
  return (
    <>
      {Array.from({ length: 10 }, (_, i) => {
        const a = (i / 10) * Math.PI * 2;
        return (
          <span
            key={i}
            className="dialogue-etoile absolute left-1/2 top-1/2 text-xl"
            style={
              {
                color: i % 2 ? couleur : '#ffd84d',
                '--dx': `${Math.cos(a) * 110}px`,
                '--dy': `${Math.sin(a) * 90}px`,
                animationDelay: `${120 + (i % 3) * 40}ms`,
              } as React.CSSProperties
            }
          >
            ★
          </span>
        );
      })}
    </>
  );
}

export default function DialogueJeu({ dernier }: { dernier: Dialogue | null }) {
  const [file, setFile] = useState<Dialogue[]>([]);
  const vus = useRef(new Set<number>());

  useEffect(() => {
    if (!dernier || vus.current.has(dernier.cle)) return;
    vus.current.add(dernier.cle);
    // Au plus deux en attente : un enfant qui enchaîne les bonnes réponses ne
    // doit pas regarder défiler des dialogues en retard.
    setFile((f) => [...f, dernier].slice(-2));
  }, [dernier]);

  const actuel = file[0];
  useEffect(() => {
    if (!actuel) return;
    const t = setTimeout(() => setFile((f) => f.slice(1)), STYLE[actuel.genre].duree);
    return () => clearTimeout(t);
  }, [actuel]);

  if (!actuel || typeof document === 'undefined') return null;
  const s = STYLE[actuel.genre];

  return createPortal(
    <div
      key={actuel.cle}
      className={
        'pointer-events-none fixed inset-0 z-50 flex items-start justify-center pt-[16vh] ' +
        (actuel.genre === 'choc' ? 'dialogue-secousse' : '')
      }
      style={{ '--duree': s.duree + 'ms' } as React.CSSProperties}
      aria-live="polite"
    >
      {/* Un voile doux qui fait ressortir la case sans cacher la page. */}
      <div className="dialogue-voile absolute inset-0 bg-[radial-gradient(circle_at_50%_30%,transparent_20%,rgb(30_20_10/0.35)_80%)]" />
      {actuel.genre === 'choc' ? <div className="dialogue-eclair absolute inset-0 bg-white" /> : null}

      <div className="dialogue-case relative flex w-full max-w-md items-center gap-2 px-4">
        <div className="dialogue-perso relative h-32 w-32 shrink-0">
          <Soleil couleur={s.soleil} />
          <Etoiles couleur={s.titre} />
          <Pango
            humeur={s.humeur}
            className={'absolute inset-2 h-28 w-28 drop-shadow-lg ' + (s.humeur === 'boule' ? 'dialogue-roule' : 'dialogue-sautille')}
          />
        </div>

        <div className="dialogue-bulle relative min-w-0 flex-1 rounded-[26px] border-[3px] border-ink bg-white-warm px-4 py-3 shadow-[0_8px_0_rgb(30_20_10/0.25)]">
          {/* La pointe de la bulle, vers Pango. */}
          <span className="absolute -left-[13px] top-1/2 h-0 w-0 -translate-y-1/2 border-y-[11px] border-r-[13px] border-y-transparent border-r-ink" />
          <span className="absolute -left-[8px] top-1/2 h-0 w-0 -translate-y-1/2 border-y-[8px] border-r-[10px] border-y-transparent border-r-white-warm" />
          <p
            className="dialogue-titre text-kid-xl font-black leading-tight [text-shadow:0_2px_0_rgb(255_255_255)]"
            style={{ color: s.titre }}
          >
            {actuel.titre}
          </p>
          <p className="mt-0.5 text-kid-sm font-bold text-ink">{actuel.phrase}</p>
        </div>
      </div>
    </div>,
    document.body,
  );
}
