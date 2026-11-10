import { useEffect, useState } from 'react';
import { estVoisin, type Coup, type Plateau as Grille, type Position } from '../../lib/bonbons';

/**
 * Le plateau de bonbons de la salle de composition.
 *
 * On joue par DEUX TOUCHERS successifs, jamais par glisser-déposer — la même
 * raison que pour les associations : sur un téléphone, un doigt qui traîne
 * sur l'écran fait défiler la page, et l'enfant perd son coup.
 *
 * Chaque couleur a sa FORME en plus de sa teinte. Un plateau qui ne se
 * distingue qu'à la couleur est injouable pour un enfant qui les confond, et
 * illisible au soleil sur un écran de téléphone.
 *
 * Le coup suggéré n'est montré qu'après une longue hésitation, et il montre
 * les DEUX cases à échanger : une flèche sur une seule case ne dit pas quoi
 * faire. La suggestion est toujours la même pour un plateau donné, sans quoi
 * elle se lirait comme un clignotement et non comme un conseil.
 */

/** Les cinq bonbons : une teinte, une forme, un nom pour les lecteurs d'écran. */
const BONBONS = [
  { fond: '#c9703f', forme: 'rond', nom: 'le rond orange' },
  { fond: '#e7ae4a', forme: 'carre', nom: 'le carré doré' },
  { fond: '#7aa46c', forme: 'losange', nom: 'le losange vert' },
  { fond: '#6d9ecb', forme: 'anneau', nom: 'l’anneau bleu' },
  { fond: '#9a7fc4', forme: 'fleur', nom: 'la fleur violette' },
] as const;

function Bonbon({ couleur, saute }: { couleur: number; saute: boolean }) {
  const b = BONBONS[couleur % BONBONS.length];
  const base: React.CSSProperties = {
    background: b.fond,
    transition: 'transform 180ms ease, opacity 180ms ease',
    transform: saute ? 'scale(0.1) rotate(25deg)' : 'scale(1)',
    opacity: saute ? 0 : 1,
  };
  if (b.forme === 'rond') {
    return <span className="block h-full w-full rounded-full" style={base} />;
  }
  if (b.forme === 'carre') {
    return <span className="block h-full w-full rounded-[28%]" style={base} />;
  }
  if (b.forme === 'losange') {
    return (
      <span
        className="block h-[78%] w-[78%] rounded-[18%]"
        style={{ ...base, transform: `${base.transform} rotate(45deg)` }}
      />
    );
  }
  if (b.forme === 'anneau') {
    return (
      <span
        className="grid h-full w-full place-items-center rounded-full"
        style={base}
      >
        <span className="block h-[38%] w-[38%] rounded-full bg-white-warm" />
      </span>
    );
  }
  return (
    <span className="relative block h-full w-full" style={base}>
      <span className="absolute inset-0 rounded-[40%]" style={{ background: b.fond }} />
      <span
        className="absolute inset-0 rounded-[40%]"
        style={{ background: b.fond, transform: 'rotate(45deg)' }}
      />
    </span>
  );
}

export default function Plateau({
  grille,
  actif,
  explosions,
  suggestion,
  onCoup,
}: {
  grille: Grille;
  /** Le plateau n'accepte un coup que si l'enfant en a gagné un. */
  actif: boolean;
  /** Les cases qui disparaissent en ce moment. */
  explosions: Position[];
  /** Le coup à montrer quand il hésite, ou null. */
  suggestion: Coup | null;
  onCoup: (coup: Coup) => void;
}) {
  const [choisie, setChoisie] = useState<Position | null>(null);

  // Un plateau qui redevient inactif ne garde pas une case sélectionnée :
  // elle resterait allumée pendant la question suivante.
  useEffect(() => {
    if (!actif) setChoisie(null);
  }, [actif]);

  const colonnes = grille[0]?.length ?? 0;
  const saute = new Set(explosions.map((p) => p.l + ':' + p.c));
  const montree = suggestion
    ? new Set([
        suggestion.a.l + ':' + suggestion.a.c,
        suggestion.b.l + ':' + suggestion.b.c,
      ])
    : new Set<string>();

  function toucher(p: Position) {
    if (!actif) return;
    if (!choisie) {
      setChoisie(p);
      return;
    }
    if (choisie.l === p.l && choisie.c === p.c) {
      setChoisie(null);
      return;
    }
    if (estVoisin(choisie, p)) {
      const coup = { a: choisie, b: p };
      setChoisie(null);
      onCoup(coup);
      return;
    }
    // Une case lointaine ne rate pas le coup : elle devient la nouvelle
    // sélection. Un enfant qui vise mal ne doit pas perdre son tour.
    setChoisie(p);
  }

  return (
    <div
      className="grid gap-1 rounded-[var(--radius-card)] border border-line bg-sand/50 p-1.5"
      style={{ gridTemplateColumns: `repeat(${colonnes}, minmax(0, 1fr))` }}
    >
      {grille.map((ligne, l) =>
        ligne.map((couleur, c) => {
          const cle = l + ':' + c;
          const prise = choisie?.l === l && choisie?.c === c;
          return (
            <button
              key={cle}
              type="button"
              disabled={!actif}
              onClick={() => toucher({ l, c })}
              aria-label={BONBONS[couleur % BONBONS.length].nom}
              className={
                'relative grid aspect-square place-items-center rounded-[26%] p-[6%] ' +
                (prise
                  ? 'bg-ink/15 ring-2 ring-ink'
                  : montree.has(cle)
                    ? 'bg-gold/35 ring-2 ring-gold'
                    : 'bg-white-warm/70') +
                (actif ? '' : ' opacity-80')
              }
            >
              <Bonbon couleur={couleur} saute={saute.has(cle)} />
            </button>
          );
        }),
      )}
    </div>
  );
}
