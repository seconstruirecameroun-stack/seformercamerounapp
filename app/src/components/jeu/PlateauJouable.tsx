import { useEffect, useRef, useState } from 'react';
import { jouerSon } from '../../lib/sons';
import {
  coupsPossibles,
  estVoisin,
  jouer,
  melangerPlateau,
  nouveauPlateau,
  suggestion as coupSuggere,
  type Coup,
  type Plateau as Grille,
  type Position,
} from '../../lib/bonbons';

/**
 * Le plateau de bonbons, jouable, avec toute son animation.
 *
 * Un enfant de sept ans ne joue pas pour les points : il joue pour ce qui se
 * passe à l'écran quand il réussit. Chaque geste a donc sa réponse visible —
 * le bonbon gonfle avant d'éclater, un anneau s'ouvre dessous, des étoiles
 * partent en gerbe, les bonbons retombent d'en haut avec un rebond, les
 * points montent et s'effacent, et une grosse cascade secoue le plateau.
 *
 * Chaque animation dure moins d'une demi-seconde. Une animation qu'on attend
 * devient une corvée au dixième coup, et il y en aura vingt dans une
 * composition.
 *
 * Le composant porte le plateau ET son animation, pour que la salle de
 * composition et le banc d'essai ne les écrivent pas deux fois — c'est le
 * genre de duplication où les deux versions finissent par diverger.
 */

const LIGNES = 7;
const COLONNES = 7;
/** Le temps du gonflement et de l'éclat. */
const TEMPS_ECLAT = 300;
/** Le temps de la chute, retards compris. */
const TEMPS_CHUTE = 380;
/** Après quoi on montre un coup à l'enfant qui ne joue pas. */
const TEMPS_AVANT_AIDE = 7000;

/** Ce qu'on crie quand la cascade enchaîne. */
const CRIS = ['', 'Bravo !', 'Super !', 'Énorme !', 'Incroyable !'];

const BONBONS = [
  { fond: '#c9703f', forme: 'rond', nom: 'le rond orange' },
  { fond: '#e7ae4a', forme: 'carre', nom: 'le carré doré' },
  { fond: '#7aa46c', forme: 'losange', nom: 'le losange vert' },
  { fond: '#6d9ecb', forme: 'anneau', nom: 'l’anneau bleu' },
  { fond: '#9a7fc4', forme: 'fleur', nom: 'la fleur violette' },
] as const;

/** Une étoile à cinq branches, dessinée une fois pour toutes. */
const ETOILE =
  'polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)';

function Forme({ couleur }: { couleur: number }) {
  const b = BONBONS[couleur % BONBONS.length];
  const ombre = 'inset 0 -3px 0 rgb(0 0 0 / 0.16), inset 0 3px 0 rgb(255 255 255 / 0.3)';
  if (b.forme === 'rond') {
    return (
      <span
        className="block h-full w-full rounded-full"
        style={{ background: b.fond, boxShadow: ombre }}
      />
    );
  }
  if (b.forme === 'carre') {
    return (
      <span
        className="block h-full w-full rounded-[28%]"
        style={{ background: b.fond, boxShadow: ombre }}
      />
    );
  }
  if (b.forme === 'losange') {
    return (
      <span
        className="block h-[80%] w-[80%] rounded-[18%]"
        style={{ background: b.fond, boxShadow: ombre, transform: 'rotate(45deg)' }}
      />
    );
  }
  if (b.forme === 'anneau') {
    return (
      <span
        className="grid h-full w-full place-items-center rounded-full"
        style={{ background: b.fond, boxShadow: ombre }}
      >
        <span className="block h-[38%] w-[38%] rounded-full bg-white-warm" />
      </span>
    );
  }
  return (
    <span className="relative block h-full w-full">
      <span className="absolute inset-0 rounded-[42%]" style={{ background: b.fond }} />
      <span
        className="absolute inset-0 rounded-[42%]"
        style={{ background: b.fond, transform: 'rotate(45deg)', boxShadow: ombre }}
      />
      <span className="absolute inset-[34%] rounded-full bg-white-warm/80" />
    </span>
  );
}

/** La gerbe d'étoiles d'un bonbon qui part. */
function Etincelles({ couleur }: { couleur: number }) {
  const b = BONBONS[couleur % BONBONS.length];
  const branches = [0, 60, 120, 180, 240, 300];
  return (
    <span aria-hidden="true" className="pointer-events-none absolute inset-0">
      <span className="splash absolute inset-0 rounded-full border-4 border-white-warm" />
      {branches.map((angle, i) => {
        const r = (angle * Math.PI) / 180;
        return (
          <span
            key={angle}
            className="etincelle absolute top-1/2 left-1/2 block"
            style={
              {
                width: 9,
                height: 9,
                marginLeft: -4.5,
                marginTop: -4.5,
                background: i % 2 === 0 ? 'var(--color-gold)' : b.fond,
                clipPath: ETOILE,
                '--dx': `${Math.cos(r) * 26}px`,
                '--dy': `${Math.sin(r) * 26}px`,
                '--tour': `${180 + i * 40}deg`,
                '--retard': `${i * 18}ms`,
              } as React.CSSProperties
            }
          />
        );
      })}
    </span>
  );
}

/** Ce qu'un coup a produit, pour qui veut l'afficher. */
export type Gain = { points: number; bonbons: number; vagues: number };

export default function PlateauJouable({
  actif,
  onCoupJoue,
  onRefus,
  onMelange,
}: {
  /** Le plateau n'accepte un coup que si l'enfant en a gagné un. */
  actif: boolean;
  /** Appelé une fois le coup entièrement résolu, animation comprise. */
  onCoupJoue: (gain: Gain) => void;
  onRefus?: () => void;
  onMelange?: () => void;
}) {
  const [grille, setGrille] = useState<Grille>(() => nouveauPlateau(LIGNES, COLONNES, Math.random));
  const [eclats, setEclats] = useState<Set<string>>(new Set());
  const [tombees, setTombees] = useState<Map<string, number>>(new Map());
  const [choisie, setChoisie] = useState<Position | null>(null);
  const [refuses, setRefuses] = useState<Set<string>>(new Set());
  const [aide, setAide] = useState<Coup | null>(null);
  const [secousse, setSecousse] = useState(0);
  const [vole, setVole] = useState<{ cle: number; points: number; cri: string } | null>(null);
  const occupe = useRef(false);

  // Un plateau qui redevient inactif ne garde pas une case sélectionnée :
  // elle resterait allumée pendant la question suivante.
  useEffect(() => {
    if (!actif) setChoisie(null);
  }, [actif]);

  useEffect(() => {
    setAide(null);
    if (!actif) return;
    const t = setTimeout(() => setAide(coupSuggere(grille)), TEMPS_AVANT_AIDE);
    return () => clearTimeout(t);
  }, [actif, grille]);

  const attendre = (ms: number) => new Promise((f) => setTimeout(f, ms));

  async function resoudre(coup: Coup) {
    const r = jouer(grille, coup, Math.random);
    if (!r) {
      // Un échange qui n'aligne rien ne coûte pas le coup : les deux bonbons
      // se repoussent, et l'enfant réessaie. Le plateau refuse, il ne punit
      // pas.
      setRefuses(new Set([coup.a.l + ':' + coup.a.c, coup.b.l + ':' + coup.b.c]));
      jouerSon('faux');
      await attendre(320);
      setRefuses(new Set());
      onRefus?.();
      return;
    }

    occupe.current = true;
    setAide(null);
    let courant = grille;

    for (let i = 0; i < r.etapes.length; i++) {
      const etape = r.etapes[i];
      jouerSon('juste');
      setEclats(new Set(etape.explosions.map((p) => p.l + ':' + p.c)));
      await attendre(TEMPS_ECLAT);
      setEclats(new Set());

      // Ce qui tombe : dans chaque colonne touchée, tout ce qui se trouve
      // au-dessus de l'explosion la plus basse. Le retard se règle par
      // ligne, pour que la chute descende au lieu d'apparaître d'un bloc.
      const parColonne = new Map<number, number>();
      for (const p of etape.explosions) {
        parColonne.set(p.c, Math.max(parColonne.get(p.c) ?? -1, p.l));
      }
      const chute = new Map<string, number>();
      for (const [c, basse] of parColonne) {
        for (let l = basse; l >= 0; l--) chute.set(l + ':' + c, (basse - l) * 26);
      }
      setTombees(chute);
      courant = etape.apres;
      setGrille(courant);

      // Les points de la vague montent au-dessus du plateau, avec le cri qui
      // convient : trois vagues doivent se voir autrement que deux.
      setVole({
        cle: Date.now() + i,
        points: etape.points,
        cri: CRIS[Math.min(i + 1, CRIS.length - 1)] ?? '',
      });
      if (i >= 1) setSecousse(i >= 2 ? 6 : 3);

      await attendre(TEMPS_CHUTE);
      setTombees(new Map());
      setSecousse(0);
    }

    // Plus aucun coup possible : on remue les bonbons présents, sans en
    // créer ni en retirer un seul.
    if (coupsPossibles(courant).length === 0) {
      courant = melangerPlateau(courant, Math.random);
      setGrille(courant);
      onMelange?.();
    }

    // Les points s'effacent d'eux-mêmes, mais le nœud n'a plus rien à faire
    // là : on le retire, pour qu'un coup suivant reparte d'un écran propre.
    setVole(null);
    occupe.current = false;
    onCoupJoue({ points: r.points, bonbons: r.bonbons, vagues: r.etapes.length });
  }

  function toucher(p: Position) {
    if (!actif || occupe.current) return;
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
      void resoudre(coup);
      return;
    }
    // Une case lointaine ne rate pas le coup : elle devient la nouvelle
    // sélection. Un enfant qui vise mal ne doit pas perdre son tour.
    setChoisie(p);
  }

  const montree = aide
    ? new Set([aide.a.l + ':' + aide.a.c, aide.b.l + ':' + aide.b.c])
    : new Set<string>();

  return (
    <div className="relative">
      {vole ? (
        <p
          key={vole.cle}
          aria-hidden="true"
          className="score-vole pointer-events-none absolute inset-x-0 top-1/3 z-20 text-center"
        >
          <span className="rounded-full bg-ink/85 px-3 py-1 text-kid-lg font-black text-gold">
            +{vole.points}
            {vole.cri ? <span className="ml-2 text-white-warm">{vole.cri}</span> : null}
          </span>
        </p>
      ) : null}

      <div
        className={
          'grid gap-1 rounded-[var(--radius-card)] border border-line bg-sand/50 p-1.5 ' +
          (secousse > 0 ? 'plateau-secoue' : '')
        }
        style={
          {
            gridTemplateColumns: `repeat(${COLONNES}, minmax(0, 1fr))`,
            '--force': `${secousse}px`,
          } as React.CSSProperties
        }
      >
        {grille.map((ligne, l) =>
          ligne.map((couleur, c) => {
            const cle = l + ':' + c;
            const prise = choisie?.l === l && choisie?.c === c;
            const eclate = eclats.has(cle);
            const retard = tombees.get(cle);
            return (
              <button
                key={cle}
                type="button"
                disabled={!actif}
                onClick={() => toucher({ l, c })}
                aria-label={BONBONS[couleur % BONBONS.length].nom}
                className={
                  'relative grid aspect-square place-items-center rounded-[26%] p-[7%] ' +
                  (prise
                    ? 'bg-ink/15 ring-2 ring-ink'
                    : montree.has(cle)
                      ? 'bg-gold/35 ring-2 ring-gold'
                      : 'bg-white-warm/70') +
                  (actif ? '' : ' opacity-80')
                }
              >
                <span
                  className={
                    'grid h-full w-full place-items-center ' +
                    (eclate
                      ? 'bonbon-eclate'
                      : refuses.has(cle)
                        ? 'bonbon-refuse'
                        : retard !== undefined
                          ? 'bonbon-tombe'
                          : prise
                            ? 'bonbon-choisi'
                            : '')
                  }
                  style={retard !== undefined ? ({ '--retard': `${retard}ms` } as React.CSSProperties) : undefined}
                >
                  <Forme couleur={couleur} />
                </span>
                {eclate ? <Etincelles couleur={couleur} /> : null}
              </button>
            );
          }),
        )}
      </div>
    </div>
  );
}
