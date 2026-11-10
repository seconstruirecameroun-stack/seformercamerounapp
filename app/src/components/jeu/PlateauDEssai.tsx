import { useEffect, useState } from 'react';
import Plateau from './Plateau';
import {
  coupsPossibles,
  jouer,
  melangerPlateau,
  nouveauPlateau,
  suggestion as coupSuggere,
  type Coup,
  type Plateau as Grille,
  type Position,
} from '../../lib/bonbons';

/**
 * Le plateau de bonbons, librement jouable, sur le banc d'essai.
 *
 * Dans une composition, un coup se gagne par une bonne réponse. Ici tous les
 * coups sont gratuits : c'est fait pour éprouver le jeu lui-même — les
 * cascades, le mélange quand plus rien n'est possible, la lisibilité des
 * cinq formes — sans poser une seule question à un enfant et sans écrire
 * une ligne dans son journal.
 */

const LIGNES = 7;
const COLONNES = 7;
const TEMPS_EXPLOSION = 260;
const TEMPS_AVANT_AIDE = 7000;

export default function PlateauDEssai() {
  const [grille, setGrille] = useState<Grille>(() => nouveauPlateau(LIGNES, COLONNES, Math.random));
  const [explosions, setExplosions] = useState<Position[]>([]);
  const [score, setScore] = useState(0);
  const [coups, setCoups] = useState(0);
  const [melanges, setMelanges] = useState(0);
  const [occupe, setOccupe] = useState(false);
  const [aide, setAide] = useState<Coup | null>(null);
  const [dernier, setDernier] = useState<{ points: number; bonbons: number; vagues: number } | null>(
    null,
  );

  useEffect(() => {
    setAide(null);
    if (occupe) return;
    const t = setTimeout(() => setAide(coupSuggere(grille)), TEMPS_AVANT_AIDE);
    return () => clearTimeout(t);
  }, [grille, occupe]);

  async function jouerCoup(coup: Coup) {
    if (occupe) return;
    const r = jouer(grille, coup, Math.random);
    if (!r) return;
    setOccupe(true);
    setAide(null);
    let courant = grille;
    for (const etape of r.etapes) {
      setExplosions(etape.explosions);
      // eslint-disable-next-line no-await-in-loop
      await new Promise((f) => setTimeout(f, TEMPS_EXPLOSION));
      setExplosions([]);
      courant = etape.apres;
      setGrille(courant);
      // eslint-disable-next-line no-await-in-loop
      await new Promise((f) => setTimeout(f, 90));
    }
    if (coupsPossibles(courant).length === 0) {
      courant = melangerPlateau(courant, Math.random);
      setGrille(courant);
      setMelanges((m) => m + 1);
    }
    setScore((s) => s + r.points);
    setCoups((c) => c + 1);
    setDernier({ points: r.points, bonbons: r.bonbons, vagues: r.etapes.length });
    setOccupe(false);
  }

  return (
    <section className="mt-3">
      <div className="flex items-baseline justify-between gap-3">
        <p className="text-kid-sm font-extrabold tabular-nums">{score} points</p>
        <p className="text-kid-xs text-muted tabular-nums">
          {coups} coup{coups > 1 ? 's' : ''}
          {melanges > 0 ? ` · ${melanges} mélange${melanges > 1 ? 's' : ''}` : ''}
        </p>
      </div>

      <div className="mt-2">
        <Plateau
          grille={grille}
          actif={!occupe}
          explosions={explosions}
          suggestion={aide}
          onCoup={jouerCoup}
        />
      </div>

      <p className="mt-2 text-center text-kid-xs font-bold text-muted">
        {dernier
          ? `+${dernier.points} · ${dernier.bonbons} bonbons · ${dernier.vagues} vague${dernier.vagues > 1 ? 's' : ''}`
          : 'Touche deux bonbons voisins.'}
      </p>

      <button
        type="button"
        onClick={() => {
          setGrille(nouveauPlateau(LIGNES, COLONNES, Math.random));
          setScore(0);
          setCoups(0);
          setMelanges(0);
          setDernier(null);
        }}
        className="mt-3 w-full rounded-full border-2 border-clay px-3 py-2 text-kid-xs font-black text-clay-dark"
      >
        Nouveau plateau
      </button>
    </section>
  );
}
