import { useEffect, useRef, useState } from 'react';
import { note } from '../../lib/composition';
import { appreciation, mention } from '../../lib/epreuve';
import { medailleDe, prochaineMedaille } from '../../lib/recompenses';
import { jouerSon } from '../../lib/sons';
import Medaille, { nomDuMetal } from './Medaille';
import type { LigneDeBulletin } from './Copie';

/**
 * La remise du bulletin.
 *
 * À l'école, la maîtresse rend la copie, et l'enfant cherche la note des
 * yeux. Ici, ce moment se joue en quatre temps, en moins de cinq secondes :
 *
 *   un roulement de tambour ;
 *   les exercices qui s'additionnent, un par un ;
 *   le total qui monte, puis la LETTRE qui tombe et le tampon qui s'écrase ;
 *   la MÉDAILLE qui se révèle — or, argent ou bronze — et, s'il en manquait
 *   une, ce qu'il aurait fallu pour la suivante.
 *
 * Un toucher passe directement à la fin : la cérémonie est un plaisir, pas
 * une attente imposée.
 */

const ETAPES = { tambour: 0, lignes: 1, total: 2, lettre: 3, medaille: 4 } as const;

function Confettis() {
  const couleurs = ['#e74c3c', '#f1c40f', '#2ecc71', '#3498db', '#9b59b6', '#ff8a3d'];
  return (
    <div className="pointer-events-none fixed inset-0 z-40 overflow-hidden" aria-hidden>
      {Array.from({ length: 36 }, (_, i) => (
        <span
          key={i}
          className="confetti absolute top-0 block h-3 w-2 rounded-sm"
          style={{
            left: `${(i * 37) % 100}%`,
            background: couleurs[i % couleurs.length],
            animationDelay: `${(i % 9) * 90}ms`,
            animationDuration: `${1600 + (i % 5) * 260}ms`,
          }}
        />
      ))}
    </div>
  );
}

export default function Ceremonie(props: {
  oral: number;
  surOral: number;
  exercices: LigneDeBulletin[];
  points: number;
  total: number;
}) {
  const [etape, setEtape] = useState<number>(ETAPES.tambour);
  const [lignes, setLignes] = useState(0);
  const [compteur, setCompteur] = useState(0);
  const passe = useRef(false);

  const lettre = mention(props.points, props.total);
  const metal = medailleDe(props.points, props.total);
  const suivante = prochaineMedaille(props.points, props.total);
  const toutes = [
    ...(props.surOral > 0 ? [{ numero: 0, titre: 'Oral', eus: props.oral, sur: props.surOral }] : []),
    ...props.exercices,
  ];

  // Le déroulé : chaque temps lance le suivant.
  useEffect(() => {
    if (passe.current) return;
    let t: number;
    if (etape === ETAPES.tambour) {
      jouerSon('tambour');
      t = window.setTimeout(() => setEtape(ETAPES.lignes), 900);
    } else if (etape === ETAPES.lignes) {
      if (lignes < toutes.length) {
        t = window.setTimeout(() => {
          jouerSon('piece');
          setLignes((n) => n + 1);
        }, 330);
      } else {
        t = window.setTimeout(() => setEtape(ETAPES.total), 200);
      }
    } else if (etape === ETAPES.total) {
      if (compteur < props.points) {
        const pas = Math.max(1, Math.ceil(props.points / 18));
        t = window.setTimeout(() => setCompteur((c) => Math.min(props.points, c + pas)), 45);
      } else {
        t = window.setTimeout(() => setEtape(ETAPES.lettre), 250);
      }
    } else if (etape === ETAPES.lettre) {
      jouerSon('tampon');
      if (navigator.vibrate) navigator.vibrate(30);
      t = window.setTimeout(() => setEtape(ETAPES.medaille), 900);
    } else if (etape === ETAPES.medaille && metal) {
      jouerSon('fete');
    }
    return () => window.clearTimeout(t);
  }, [etape, lignes, compteur]); // eslint-disable-line react-hooks/exhaustive-deps

  const toutVoir = () => {
    if (etape === ETAPES.medaille) return;
    passe.current = true;
    setLignes(toutes.length);
    setCompteur(props.points);
    setEtape(ETAPES.medaille);
  };

  return (
    <section
      onClick={toutVoir}
      className="relative overflow-hidden rounded-[var(--radius-card)] border-2 border-ink bg-white-warm p-4 text-center"
    >
      {etape === ETAPES.medaille && metal === 'or' ? <Confettis /> : null}

      {etape === ETAPES.tambour ? (
        <p className="ceremonie-tambour py-8 text-kid-lg font-black text-clay-dark">
          Roulement de tambour…
        </p>
      ) : (
        <>
          <ul className="grid grid-cols-1 gap-1.5 text-left">
            {toutes.slice(0, lignes).map((ex) => (
              <li key={ex.numero} className="ceremonie-ligne flex items-baseline justify-between gap-3">
                <span className="min-w-0 truncate text-kid-xs font-bold text-ink-2">
                  {ex.numero > 0 ? `${ex.numero}. ` : ''}
                  {ex.titre}
                </span>
                <span
                  className={
                    'shrink-0 text-kid-sm font-black tabular-nums ' +
                    (ex.eus === ex.sur ? 'text-leaf' : 'text-clay-dark')
                  }
                >
                  {note(ex.eus, ex.sur)} {ex.eus === ex.sur ? '★' : ''}
                </span>
              </li>
            ))}
          </ul>

          {etape >= ETAPES.total ? (
            <p className="mt-4 text-5xl font-black tabular-nums">{note(compteur, props.total)}</p>
          ) : null}

          {etape >= ETAPES.lettre ? (
            <div className="relative mt-2 flex justify-center">
              <p className="ceremonie-tampon inline-flex flex-col items-center rounded-2xl border-[5px] border-clay px-6 py-1 text-clay-dark">
                <span className="text-6xl font-black leading-none">{lettre}</span>
                <span className="text-kid-xs font-black tracking-wide uppercase">{appreciation(lettre)}</span>
              </p>
            </div>
          ) : null}

          {etape >= ETAPES.medaille ? (
            <div className="mt-4 flex flex-col items-center">
              {metal ? (
                <>
                  <div className="ceremonie-medaille">
                    <Medaille metal={metal} taille={110} />
                  </div>
                  <p className="mt-1 text-kid-lg font-black text-ink">{nomDuMetal(metal)} !</p>
                </>
              ) : (
                <p className="text-kid-sm font-bold text-ink-2">Pas de médaille cette fois. La prochaine est à portée !</p>
              )}
              {suivante ? (
                <div className="mt-3 flex items-center gap-3 rounded-full bg-sand px-4 py-2">
                  <Medaille metal={suivante.metal} taille={34} terne />
                  <p className="text-left text-kid-xs font-bold text-ink-2">
                    La prochaine fois : {suivante.manque} point{suivante.manque > 1 ? 's' : ''} de plus,
                    et c’est la {nomDuMetal(suivante.metal).toLowerCase()}.
                  </p>
                </div>
              ) : (
                <p className="mt-2 text-kid-xs font-bold text-leaf">La plus belle des médailles. Bravo !</p>
              )}
            </div>
          ) : null}
        </>
      )}

      {etape < ETAPES.medaille ? (
        <p className="mt-3 text-kid-xs text-muted">Touche pour tout voir</p>
      ) : null}
    </section>
  );
}
