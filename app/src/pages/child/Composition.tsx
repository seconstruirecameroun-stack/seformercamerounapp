import { useCallback, useEffect, useRef, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { useSession } from '../../lib/auth';
import { recordAttempt } from '../../lib/progress';
import { rangDeLaClasse } from '../../lib/saisie';
import { jouerSon } from '../../lib/sons';
import { ErrorNote, Loading } from '../../components/ui';
import ItemPlayer from '../../components/items/ItemPlayer';
import type { Reponse } from '../../components/items/ItemPlayer';
import Plateau from '../../components/jeu/Plateau';
import {
  commencerComposition,
  finirComposition,
  lireComposition,
  note,
  questionsDeLaComposition,
} from '../../lib/composition';
import {
  coupsPossibles,
  jouer,
  melangerPlateau,
  nouveauPlateau,
  objectifDuPlateau,
  suggestion as coupSuggere,
  type Coup,
  type Plateau as Grille,
  type Position,
} from '../../lib/bonbons';

/**
 * La salle de composition.
 *
 * Elle est faite d'une seule idée : CHAQUE BONNE RÉPONSE DONNE UN COUP. La
 * question est en bas, le plateau en haut, et rien ne se passe sur le
 * plateau tant que l'enfant n'a pas gagné son coup. Une composition de vingt
 * questions est longue ; le plateau lui donne, question après question, une
 * conséquence visible et une raison de continuer.
 *
 * Le jeu ne corrige rien et ne juge rien. La note est le compte des bonnes
 * réponses, et elle ne dépend pas du score du plateau : un enfant qui répond
 * juste et joue mal a la même note que celui qui répond juste et joue bien.
 * Sans cela, la note ne dirait plus ce qu'il sait.
 *
 * Une faute ne coûte rien sur le plateau. Elle coûte un coup qu'il n'aura
 * pas, ce qui suffit : ajouter une pénalité ferait d'une erreur une double
 * punition, et l'app a déjà tranché cela pour la manche.
 */

const LIGNES = 7;
const COLONNES = 7;
/** Le temps d'une explosion, puis de la chute : assez pour la voir. */
const TEMPS_EXPLOSION = 260;
/** Après quoi on montre un coup à l'enfant qui ne joue pas. */
const TEMPS_AVANT_AIDE = 7000;

type Phase = 'question' | 'corrige' | 'plateau' | 'bilan';

export default function Composition() {
  const { childId, compositionId } = useParams();
  const navigate = useNavigate();
  const { session } = useSession();
  const parentId = session?.user.id ?? null;

  const enfant = useQuery({
    queryKey: ['child', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('id, first_name, avatar, classes(rank)')
        .eq('id', childId!)
        .single();
      if (error) throw error;
      return data;
    },
  });

  const compo = useQuery({
    queryKey: ['composition', compositionId],
    enabled: Boolean(compositionId),
    queryFn: async () => {
      const c = await lireComposition(compositionId!);
      if (!c) return null;
      const questions = await questionsDeLaComposition(c);
      return { composition: c, questions };
    },
  });

  const [index, setIndex] = useState(0);
  const [justes, setJustes] = useState(0);
  /**
   * Le compte des bonnes réponses, tenu à part.
   *
   * `justes` sert à l-affichage ; cette référence sert à la note. La mise à
   * jour d-un état React n-est pas appliquée quand la dernière question
   * appelle finirComposition, et la note partait alors en base avec une
   * réponse de retard.
   */
  const justesRef = useRef(0);
  /** Vrai si la dernière réponse était juste : le plateau en dépend. */
  const justesDeLaDerniere = useRef(false);
  const [phase, setPhase] = useState<Phase>('question');
  const [grille, setGrille] = useState<Grille | null>(null);
  const [explosions, setExplosions] = useState<Position[]>([]);
  const [score, setScore] = useState(0);
  const [aide, setAide] = useState<Coup | null>(null);
  const [erreur, setErreur] = useState<unknown>(null);
  const [dernierGain, setDernierGain] = useState(0);
  const commence = useRef(false);

  const total = compo.data?.questions.length ?? 0;
  const objectif = objectifDuPlateau(total);

  // Le plateau de départ est tiré une fois, à l'ouverture.
  useEffect(() => {
    if (!grille && compo.data) setGrille(nouveauPlateau(LIGNES, COLONNES, Math.random));
  }, [compo.data, grille]);

  // La composition est marquée commencée au premier affichage, et une seule
  // fois : la requête ne touche la ligne que si la date est encore vide.
  useEffect(() => {
    if (compo.data?.composition && !commence.current) {
      commence.current = true;
      if (!compo.data.composition.commencee_le) {
        commencerComposition(compo.data.composition.id).catch(() => undefined);
      }
    }
  }, [compo.data]);

  // Le coup suggéré ne paraît qu'après une longue hésitation, et seulement
  // quand c'est à l'enfant de jouer.
  useEffect(() => {
    setAide(null);
    if (phase !== 'plateau' || !grille) return;
    const t = setTimeout(() => setAide(coupSuggere(grille)), TEMPS_AVANT_AIDE);
    return () => clearTimeout(t);
  }, [phase, grille]);

  const suivante = useCallback(() => {
    if (index + 1 >= total) {
      setPhase('bilan');
      if (compositionId) finirComposition(compositionId, justesRef.current).catch(() => undefined);
      return;
    }
    setIndex((i) => i + 1);
    setPhase('question');
  }, [index, total, compositionId]);

  async function repondre(reponse: Reponse) {
    if (phase !== 'question' || !compo.data || !parentId || !childId) return;
    const item = compo.data.questions[index];
    setPhase('corrige');
    setErreur(null);
    try {
      // Tout compte, comme en révision : étoiles, maîtrise, étapes. C'est le
      // choix du père, et le seul qui garde vraie l'affirmation faite au
      // parent — une leçon ratée en composition n'est plus une leçon sue.
      await recordAttempt({
        parentId,
        childId,
        item,
        answer: reponse.donnee,
        correct: reponse.correct,
      });
    } catch (e) {
      setErreur(e);
    }
    jouerSon(reponse.correct ? 'juste' : 'faux');
    if (reponse.correct) {
      justesRef.current += 1;
      setJustes(justesRef.current);
    }
  }

  /** Une bonne réponse ouvre le plateau ; une faute passe à la suite. */
  function apresCorrection() {
    if (phase !== 'corrige') return;
    if (justesDeLaDerniere.current) setPhase('plateau');
    else suivante();
  }

  async function jouerCoup(coup: Coup) {
    if (phase !== 'plateau' || !grille) return;
    const r = jouer(grille, coup, Math.random);
    if (!r) {
      // Un échange qui n'aligne rien ne coûte pas le coup : l'enfant
      // réessaie. Le plateau refuse, il ne punit pas.
      jouerSon('faux');
      return;
    }
    setPhase('corrige');
    setAide(null);
    jouerSon('juste');
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
    // Plus aucun coup possible : on remue les bonbons présents, sans en
    // créer ni en retirer un seul.
    if (coupsPossibles(courant).length === 0) {
      courant = melangerPlateau(courant, Math.random);
      setGrille(courant);
    }
    setScore((s) => s + r.points);
    setDernierGain(r.points);
    suivante();
  }

  if (compo.isLoading || enfant.isLoading) return <Loading label="La salle s’ouvre…" />;
  if (compo.error) return <ErrorNote error={compo.error} />;
  if (!compo.data?.composition) {
    return (
      <main className="mx-auto max-w-md p-4">
        <p className="text-kid-sm text-muted">Cette composition n’existe plus.</p>
      </main>
    );
  }

  const { composition, questions } = compo.data;
  const rang = rangDeLaClasse(enfant.data?.classes);
  const item = questions[index];

  if (phase === 'bilan') {
    const gagne = score >= objectif;
    return (
      <main className="mx-auto max-w-md p-4 pb-24">
        <section className="rounded-[var(--radius-card)] border border-line bg-white-warm/80 p-5 text-center">
          <p className="text-kid-xs font-black tracking-wide text-clay-dark">COMPOSITION FINIE</p>
          <h1 className="mt-1 text-kid-xl font-extrabold">{composition.titre}</h1>
          <p className="mt-4 text-5xl font-black tabular-nums">{note(justes, total)}</p>
          <p className="mt-1 text-kid-sm text-muted">
            {justes === total
              ? 'Pas une seule faute.'
              : justes * 2 >= total
                ? 'Plus de la moitié de juste.'
                : 'Il y a de quoi réviser.'}
          </p>
          <p className="mt-4 text-kid-sm font-bold">
            Plateau : {score} points {gagne ? '— objectif atteint !' : `sur ${objectif}`}
          </p>
          <button
            type="button"
            onClick={() => navigate(`/enfant/${childId}`)}
            className="mt-6 w-full rounded-full bg-ink px-4 py-3 text-kid-sm font-black text-white-warm"
          >
            Revenir chez moi
          </button>
        </section>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-md p-3 pb-24">
      <header className="flex items-baseline justify-between gap-3">
        <h1 className="truncate text-kid-sm font-extrabold">{composition.titre}</h1>
        <span className="shrink-0 text-kid-xs font-bold text-muted tabular-nums">
          Question {index + 1} / {total}
        </span>
      </header>

      <div className="mt-2 flex items-center gap-2">
        <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-line">
          <div
            className="h-full rounded-full bg-gold transition-[width] duration-500"
            style={{ width: `${Math.min(100, Math.round((score / objectif) * 100))}%` }}
          />
        </div>
        <span className="shrink-0 text-kid-xs font-black tabular-nums">{score}</span>
      </div>

      {grille ? (
        <div className="mt-2">
          <Plateau
            grille={grille}
            actif={phase === 'plateau'}
            explosions={explosions}
            suggestion={aide}
            onCoup={jouerCoup}
          />
        </div>
      ) : null}

      <p className="mt-2 text-center text-kid-xs font-bold text-muted">
        {phase === 'plateau'
          ? 'À toi de jouer : touche deux bonbons voisins.'
          : dernierGain > 0
            ? `+${dernierGain} points`
            : 'Réponds juste, et tu gagnes un coup.'}
      </p>

      {erreur ? <ErrorNote error={erreur} /> : null}

      {phase !== 'plateau' && item ? (
        <section className="mt-3 rounded-[var(--radius-card)] border border-line bg-white-warm/80 p-4">
          <ItemPlayer
            key={item.id}
            item={item}
            rang={rang}
            verrouille={phase === 'corrige'}
            onRepondre={(r) => {
              justesDeLaDerniere.current = r.correct;
              void repondre(r);
            }}
          />
          {phase === 'corrige' ? (
            <button
              type="button"
              onClick={apresCorrection}
              className="mt-4 w-full rounded-full bg-ink px-4 py-3 text-kid-sm font-black text-white-warm"
            >
              {justesDeLaDerniere.current ? 'Jouer mon coup' : 'Question suivante'}
            </button>
          ) : null}
        </section>
      ) : null}
    </main>
  );
}
