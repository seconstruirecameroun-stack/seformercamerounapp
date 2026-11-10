import { useState } from 'react';
import PlateauJouable, { type Gain } from './PlateauJouable';

/**
 * Le plateau de bonbons, librement jouable, sur le banc d'essai.
 *
 * Dans une composition, un coup se gagne par une bonne réponse. Ici tous les
 * coups sont gratuits : c'est fait pour éprouver le jeu lui-même — les
 * cascades, les animations, le mélange quand plus rien n'est possible, la
 * lisibilité des cinq formes — sans poser une seule question à un enfant et
 * sans écrire une ligne dans son journal.
 *
 * Le plateau et son animation vivent dans PlateauJouable : le banc et la
 * salle de composition montrent exactement le même jeu, et une animation
 * corrigée ici se corrige là.
 */

export default function PlateauDEssai() {
  const [numero, setNumero] = useState(0);
  const [score, setScore] = useState(0);
  const [coups, setCoups] = useState(0);
  const [melanges, setMelanges] = useState(0);
  const [refus, setRefus] = useState(0);
  const [dernier, setDernier] = useState<Gain | null>(null);
  // Dans la salle, le plateau se fait petit pendant la question : le banc
  // permet de le voir se réduire sans poser de question à personne.
  const [petit, setPetit] = useState(false);

  return (
    <section className="mt-3">
      <div className="flex items-baseline justify-between gap-3">
        <p className="text-kid-sm font-extrabold tabular-nums">{score} points</p>
        <p className="text-kid-xs text-muted tabular-nums">
          {coups} coup{coups > 1 ? 's' : ''}
          {melanges > 0 ? ` · ${melanges} mélange${melanges > 1 ? 's' : ''}` : ''}
          {refus > 0 ? ` · ${refus} refus` : ''}
        </p>
      </div>

      <div className="mt-2">
        <PlateauJouable
          key={numero}
          actif={!petit}
          compact={petit}
          bordABord
          onCoupJoue={(g) => {
            setScore((s) => s + g.points);
            setCoups((c) => c + 1);
            setDernier(g);
          }}
          onRefus={() => setRefus((r) => r + 1)}
          onMelange={() => setMelanges((m) => m + 1)}
        />
      </div>

      <p className="mt-2 text-center text-kid-xs font-bold text-muted">
        {dernier
          ? `+${dernier.points} · ${dernier.bonbons} bonbons · ${dernier.vagues} vague${dernier.vagues > 1 ? 's' : ''}`
          : 'Touche deux bonbons voisins.'}
      </p>

      <button
        type="button"
        onClick={() => setPetit((p) => !p)}
        className="mt-3 min-h-11 w-full rounded-full border-2 border-line px-3 py-2 text-kid-xs font-black text-ink-2"
      >
        {petit ? 'Agrandir : c’est à moi de jouer' : 'Réduire : comme pendant une question'}
      </button>

      <button
        type="button"
        onClick={() => {
          setNumero((n) => n + 1);
          setScore(0);
          setCoups(0);
          setMelanges(0);
          setRefus(0);
          setDernier(null);
        }}
        className="mt-3 w-full rounded-full border-2 border-clay px-3 py-2 text-kid-xs font-black text-clay-dark"
      >
        Nouveau plateau
      </button>
    </section>
  );
}
