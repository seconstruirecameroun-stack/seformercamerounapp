import { useEffect, useMemo, useRef, useState } from 'react';
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
import PlateauJouable from '../../components/jeu/PlateauJouable';
import CourseJouable from '../../components/jeu/CourseJouable';
import { COMPTEURS_VIDES, apresReponse, jeuDeLaClasse } from '../../lib/jeuDeLEnfant';
import { EnTeteDeCopie, SituationProbleme } from '../../components/epreuve/Copie';
import Ceremonie from '../../components/epreuve/Ceremonie';
import Medaille from '../../components/epreuve/Medaille';
import DialogueJeu, { momentFort, type Dialogue } from '../../components/jeu/DialogueJeu';
import {
  PALIERS_DE_SERIE,
  mentionAssuree,
  multiplicateur,
  palierAtteint,
  prochaineMention,
  prochainPalier,
} from '../../lib/recompenses';
import {
  commencerComposition,
  epreuveDeLaComposition,
  finirComposition,
  lireComposition,
  pointsOralDe,
} from '../../lib/composition';
import { matiereDeLEpreuve, situationProbleme, type Exercice } from '../../lib/epreuve';
import { objectifDuPlateau } from '../../lib/bonbons';
import type { ItemRow } from '../../types/db';

/**
 * La salle de composition.
 *
 * Elle se déroule comme une copie de l'école, parce que c'est à cette
 * épreuve-là que l'enfant se prépare : un EN-TÊTE à son nom, une SITUATION
 * PROBLÈME à lire, un ORAL sur ce petit texte, puis l'ÉCRIT, exercice par
 * exercice, chacun avec ses points. À la fin, la note sur 20, 30 ou 40 et
 * une appréciation en lettre, comme sur la copie que la maîtresse rend.
 *
 * Le plateau reste ce qu'il était : CHAQUE BONNE RÉPONSE DONNE UN COUP. Une
 * épreuve de trente points est longue ; le plateau lui donne, question après
 * question, une conséquence visible et une raison de continuer.
 *
 * Les petits (jusqu'au CE1) n'ont pas de plateau mais la COURSE : leur
 * voiture roule en haut de l'épreuve, et chaque réponse agit sur elle — un
 * turbo si elle est juste, un choc si elle est fausse. Il n'y a rien à jouer
 * entre deux questions : l'épreuve s'enchaîne, et l'attention reste sur elle.
 *
 * LES RÉCOMPENSES, pour les grands. Une série de bonnes réponses fait
 * compter double, triple, quadruple les points du plateau ; un exercice sans
 * faute donne un coup bonus ; une mention qu'on ne peut plus perdre est
 * annoncée. Niba le lionceau surgit à ces moments forts, et l'enfant voit
 * toujours ce qu'il gagnera à la prochaine bonne réponse. À la fin, le
 * bulletin se remet en cérémonie, avec sa médaille.
 *
 * Le jeu ne corrige rien et ne juge rien. La note est le compte des bonnes
 * réponses, et elle ne dépend pas du score du plateau : un enfant qui répond
 * juste et joue mal a la même note que celui qui répond juste et joue bien.
 *
 * Les réponses de l'écrit comptent comme en révision — étoiles, maîtrise,
 * étapes. Celles de l'oral ne sont écrites nulle part : elles portent sur
 * l'histoire d'un enfant inventé, pas sur une notion du cahier.
 */

type Phase = 'entete' | 'question' | 'corrige' | 'plateau' | 'bilan';

type Etape =
  | { genre: 'oral'; item: ItemRow; rang: number }
  | { genre: 'ecrit'; item: ItemRow; exercice: Exercice; rang: number };

/** Une question de l'oral, sous la forme que l'écran sait déjà jouer. */
function itemOral(i: number, question: string, options: string[]): ItemRow {
  return {
    id: 'oral-' + i,
    parent_id: '',
    notion_id: '',
    kind: 'qcm',
    level: 1,
    payload: { question, options },
    answer: { index: 0 },
    explain: null,
    status: 'approved',
    created_at: '',
  } as ItemRow;
}

export default function Composition() {
  const { childId, compositionId } = useParams();
  const navigate = useNavigate();
  const { session } = useSession();
  const parentId = session?.user.id ?? null;

  const enfant = useQuery({
    queryKey: ['child-epreuve', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('id, first_name, avatar, classes(rank, code)')
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
      return { composition: c, epreuve: await epreuveDeLaComposition(c) };
    },
  });

  const classeJointe = enfant.data?.classes as
    | { rank: number; code: string }
    | Array<{ rank: number; code: string }>
    | null
    | undefined;
  const classe = (Array.isArray(classeJointe) ? classeJointe[0] : classeJointe)?.code ?? '';

  const situation = useMemo(
    () =>
      compo.data
        ? situationProbleme(compo.data.composition.id, classe, compo.data.epreuve.lecons)
        : null,
    [compo.data, classe],
  );

  // Toute l'épreuve, dans l'ordre où elle se passe : l'oral, puis chaque
  // exercice de l'écrit.
  const etapes = useMemo<Etape[]>(() => {
    if (!compo.data || !situation) return [];
    // Une composition d'avant la forme d'épreuve n'a pas d'oral : elle se
    // rejoue comme elle a été créée, et sa note reste sur ses seules
    // questions.
    const oral = situation.oral.slice(0, pointsOralDe(compo.data.composition));
    const sortie: Etape[] = oral.map((q, i) => ({
      genre: 'oral' as const,
      item: itemOral(i, q.question, q.options),
      rang: i + 1,
    }));
    for (const exercice of compo.data.epreuve.exercices) {
      exercice.questions.forEach((id, i) => {
        const item = compo.data!.epreuve.items.get(id);
        if (item) sortie.push({ genre: 'ecrit', item, exercice, rang: i + 1 });
      });
    }
    return sortie;
  }, [compo.data, situation]);

  const [index, setIndex] = useState(0);
  const [phase, setPhase] = useState<Phase>('entete');
  const [score, setScore] = useState(0);
  const [erreur, setErreur] = useState<unknown>(null);
  const [dernierGain, setDernierGain] = useState(0);
  const [course, setCourse] = useState(COMPTEURS_VIDES);
  /** La série de bonnes réponses d'affilée, et ce qu'elle rapporte au plateau. */
  const serie = useRef(0);
  const multiplicateurDuCoup = useRef(1);
  /** Les coups en plus, gagnés par un exercice sans faute. */
  const coupsBonus = useRef(0);
  const [enBonus, setEnBonus] = useState(false);
  /** Le moment fort que Niba annoncera quand l'écran remontera vers le plateau. */
  const momentEnAttente = useRef<Dialogue | null>(null);
  const [moment, setMoment] = useState<Dialogue | null>(null);
  /** La route faite pendant l'épreuve : la distance au départ, puis le gain. */
  const routeAuDepart = useRef<number | null>(null);
  const routeFaite = useRef(0);
  /**
   * Les points, tenus dans une référence.
   *
   * La mise à jour d'un état React n'est pas appliquée quand la dernière
   * question appelle finirComposition : la note partait en base avec une
   * réponse de retard. La référence, elle, est à jour tout de suite.
   */
  const points = useRef({ oral: 0, ecrit: 0, parExercice: new Map<number, number>() });
  const [, redessiner] = useState(0);
  /** Vrai si la dernière réponse était juste : le plateau en dépend. */
  const justeALaDerniere = useRef(false);
  const commence = useRef(false);
  /**
   * Une question ne reçoit qu'UNE réponse.
   *
   * La phase passe à « corrigé » par un état React, qui n'est appliqué
   * qu'au rendu suivant. Deux doigts posés au même instant sur deux choix
   * envoyaient donc deux réponses, et si la seconde était la bonne, le
   * point était compté — et, à l'écrit, deux tentatives partaient au
   * journal. Trouvé en rejouant l'oral : un bulletin à 2 sur 4 pour une
   * seule bonne réponse. La référence, elle, se ferme tout de suite.
   */
  const dejaRepondu = useRef(false);

  const total = etapes.length;
  const objectif = objectifDuPlateau(total);
  const jeu = jeuDeLaClasse(rangDeLaClasse(enfant.data?.classes));

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

  function suivante() {
    if (index + 1 >= total) {
      setPhase('bilan');
      window.scrollTo({ top: 0 });
      if (compositionId) {
        finirComposition(compositionId, points.current.oral + points.current.ecrit).catch(
          () => undefined,
        );
      }
      return;
    }
    dejaRepondu.current = false;
    setIndex((i) => i + 1);
    setPhase('question');
  }

  async function repondre(reponse: Reponse) {
    const etape = etapes[index];
    if (phase !== 'question' || !etape || !parentId || !childId) return;
    if (dejaRepondu.current) return;
    dejaRepondu.current = true;
    justeALaDerniere.current = reponse.correct;
    setPhase('corrige');

    setErreur(null);
    if (etape.genre === 'ecrit') {
      try {
        // Tout compte, comme en révision : étoiles, maîtrise, étapes. C'est
        // le choix du père, et le seul qui garde vraie l'affirmation faite
        // au parent — une leçon ratée en composition n'est plus une leçon
        // sue.
        await recordAttempt({
          parentId,
          childId,
          item: etape.item,
          answer: reponse.donnee,
          correct: reponse.correct,
        });
      } catch (e) {
        setErreur(e);
      }
    }
    jouerSon(reponse.correct ? 'juste' : 'faux');
    const avant = points.current.oral + points.current.ecrit;
    if (reponse.correct) {
      if (etape.genre === 'oral') {
        points.current.oral += 1;
      } else {
        points.current.ecrit += 1;
        const n = etape.exercice.numero;
        points.current.parExercice.set(n, (points.current.parExercice.get(n) ?? 0) + 1);
      }
    }
    // Les récompenses. Un seul moment fort par réponse, le plus beau : un
    // exercice parfait vaut plus qu'une mention, qui vaut plus qu'une série.
    serie.current = reponse.correct ? serie.current + 1 : 0;
    multiplicateurDuCoup.current = multiplicateur(serie.current);
    const apres = points.current.oral + points.current.ecrit;
    const mentionAvant = mentionAssuree(avant, total);
    const mentionApres = mentionAssuree(apres, total);
    const parfait =
      reponse.correct &&
      etape.genre === 'ecrit' &&
      etape.rang === etape.exercice.questions.length &&
      points.current.parExercice.get(etape.exercice.numero) === etape.exercice.questions.length;
    if (parfait) coupsBonus.current += 1;
    const restantes = total - index - 1;
    const FOIS = ['', '', 'double', 'triple', 'quadruple'];
    momentEnAttente.current = parfait
      ? momentFort('parfait', 'EXERCICE PARFAIT !',
        `${etape.exercice.questions.length} sur ${etape.exercice.questions.length} : un coup bonus pour toi !`)
      : mentionApres && mentionApres !== mentionAvant
        ? momentFort('mention', `${mentionApres === 'C' ? 'LA MOYENNE' : mentionApres} ASSURÉ${mentionApres === 'C' ? 'E' : ''} !`,
          'Personne ne peut plus te l’enlever. Vise plus haut !')
        : reponse.correct && palierAtteint(serie.current)
          ? momentFort('serie', `SÉRIE DE ${serie.current} !`,
            `Tes points du plateau comptent ${FOIS[multiplicateurDuCoup.current] ?? 'quatre fois'} !`)
          : restantes === 3
            ? momentFort('fin', 'PLUS QUE 3 !', 'Dernière ligne droite : garde ta série !')
            : null;
    redessiner((x) => x + 1);
  }

  /**
   * Une bonne réponse ouvre le plateau ; une faute passe à la suite. La
   * course, elle, a déjà reçu la réponse : on enchaîne toujours.
   */
  function apresCorrection() {
    if (phase !== 'corrige') return;
    // L'enfant a fait défiler pour répondre : le plateau, comme la question
    // suivante, est en haut. On l'y ramène plutôt que de le laisser chercher.
    window.scrollTo({ top: 0, behavior: 'smooth' });
    // La course reçoit la réponse maintenant, quand l'écran remonte vers elle :
    // au moment du corrigé, l'enfant est en bas, et il ne verrait rien.
    if (jeu === 'course') setCourse((c) => apresReponse(c, justeALaDerniere.current));
    if (jeu === 'bonbons' && momentEnAttente.current) setMoment(momentEnAttente.current);
    momentEnAttente.current = null;
    if (justeALaDerniere.current && jeu === 'bonbons') setPhase('plateau');
    else suivante();
  }

  /**
   * Le coup est fini, animation comprise : on encaisse et on enchaîne.
   *
   * Le score du plateau n'entre pas dans la note : il paie l'effort, il ne
   * le mesure pas.
   */
  function coupJoue(gain: number) {
    const vrai = gain * multiplicateurDuCoup.current;
    setScore((s) => s + vrai);
    setDernierGain(vrai);
    if (coupsBonus.current > 0) {
      // Un exercice parfait : on rejoue, sans question, tout de suite.
      coupsBonus.current -= 1;
      setEnBonus(true);
      jouerSon('serie');
      return;
    }
    setEnBonus(false);
    suivante();
  }

  if (compo.isLoading || enfant.isLoading) return <Loading label="La salle s’ouvre…" />;
  if (compo.error) return <ErrorNote error={compo.error} />;
  if (!compo.data?.composition || !situation) {
    return (
      <main className="mx-auto max-w-md p-4">
        <p className="text-kid-sm text-muted">Cette composition n’existe plus.</p>
      </main>
    );
  }

  const { composition, epreuve } = compo.data;
  const rang = rangDeLaClasse(enfant.data?.classes);
  const matiere = matiereDeLEpreuve(epreuve.lecons);
  const nbOral = pointsOralDe(composition);
  const nbEcrit = total - nbOral;
  const quand = new Date().toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });

  const enTete = (
    <EnTeteDeCopie
      nom={enfant.data?.first_name ?? ''}
      date={quand}
      classe={classe}
      epreuve={matiere}
    />
  );

  // ── L'en-tête et la situation problème ──────────────────────────────────
  if (phase === 'entete') {
    return (
      <main className="mx-auto max-w-md p-4 pb-28">
        <p className="text-center text-kid-xs font-black tracking-wide text-clay-dark">
          COMPOSITION · SUR {total} POINTS
        </p>
        <h1 className="mt-1 text-center text-kid-xl font-extrabold">{composition.titre}</h1>

        <div className="mt-4">{enTete}</div>

        <div className="mt-4">
          <SituationProbleme texte={situation.texte} oral={nbOral} ecrit={nbEcrit} />
        </div>

        {jeu === 'bonbons' ? (
          // Ce qu'il y a à gagner, dit AVANT de commencer : on ne vise bien
          // que ce qu'on connaît.
          <section className="mt-4 rounded-[var(--radius-card)] border-2 border-gold bg-white-warm p-4">
            <h2 className="text-kid-sm font-black">Ce que tu peux gagner</h2>
            <div className="mt-3 flex items-end justify-around">
              {(['or', 'argent', 'bronze'] as const).map((m, i) => (
                <div key={m} className="flex flex-col items-center">
                  <Medaille metal={m} taille={i === 0 ? 54 : 44} />
                  <span className="mt-1 text-kid-xs font-black">{['A+', 'A', 'B'][i]}</span>
                </div>
              ))}
            </div>
            <ul className="mt-3 grid grid-cols-1 gap-1 text-kid-xs font-bold text-ink-2">
              {PALIERS_DE_SERIE.map((p) => (
                <li key={p.serie}>🔥 {p.serie} bonnes réponses de suite : points du plateau ×{p.multiplicateur}</li>
              ))}
              <li>⭐ Un exercice sans faute : un coup bonus</li>
            </ul>
          </section>
        ) : null}

        <div className="fixed inset-x-0 bottom-0 border-t border-line bg-paper/95 p-3 backdrop-blur">
          <button
            type="button"
            onClick={() => {
              window.scrollTo({ top: 0 });
              setPhase('question');
            }}
            className="mx-auto block min-h-12 w-full max-w-md rounded-full bg-ink px-4 py-3 text-kid-sm font-black text-white-warm"
          >
            Commencer l’épreuve
          </button>
        </div>
      </main>
    );
  }

  // ── Le bulletin ──────────────────────────────────────────────────────────
  if (phase === 'bilan') {
    const gagne = score >= objectif;
    return (
      <main className="mx-auto max-w-md p-4 pb-24">
        <p className="text-center text-kid-xs font-black tracking-wide text-clay-dark">
          COMPOSITION FINIE
        </p>
        <h1 className="mt-1 text-center text-kid-xl font-extrabold">{composition.titre}</h1>

        <div className="mt-4">{enTete}</div>

        <div className="mt-4">
          <Ceremonie
            oral={points.current.oral}
            surOral={nbOral}
            points={points.current.oral + points.current.ecrit}
            total={total}
            exercices={epreuve.exercices.map((ex) => ({
              numero: ex.numero,
              titre: ex.lecon.title,
              eus: points.current.parExercice.get(ex.numero) ?? 0,
              sur: ex.questions.length,
            }))}
          />
        </div>

        <p className="mt-4 text-center text-kid-sm font-bold">
          {jeu === 'course'
            ? `Pendant l’épreuve, ta voiture a roulé ${Math.round(routeFaite.current)} mètres.`
            : `Plateau : ${score} points ${gagne ? '— objectif atteint !' : `sur ${objectif}`}`}
        </p>

        <button
          type="button"
          onClick={() => navigate(`/enfant/${childId}`)}
          className="mt-5 min-h-12 w-full rounded-full bg-ink px-4 py-3 text-kid-sm font-black text-white-warm"
        >
          Revenir chez moi
        </button>
      </main>
    );
  }

  // ── L'épreuve ────────────────────────────────────────────────────────────
  const etape = etapes[index];
  const partie =
    etape.genre === 'oral'
      ? `Oral · ${etape.rang} / ${nbOral}`
      : `Exercice ${etape.exercice.numero} · ${etape.rang} / ${etape.exercice.questions.length}`;

  return (
    <main className="mx-auto max-w-md p-3 pb-24">
      <header className="flex items-baseline justify-between gap-3">
        <h1 className="truncate text-kid-sm font-extrabold">{partie}</h1>
        <span className="shrink-0 text-kid-xs font-bold text-muted tabular-nums">
          {index + 1} / {total}
        </span>
      </header>

      {jeu === 'course' ? (
        // La voiture roule pendant toute l'épreuve ; c'est le seul jeu de la
        // salle, et il ne demande rien à l'enfant.
        <div className="mt-2">
          <CourseJouable
            compact
            cle={childId ? 'course-' + childId : undefined}
            turbos={course.turbos}
            erreurs={course.erreurs}
            boucliers={course.boucliers}
            onResume={(r) => {
              if (routeAuDepart.current === null) routeAuDepart.current = r.distance;
              routeFaite.current = r.distance - routeAuDepart.current;
            }}
          />
        </div>
      ) : (
        <>
        <div className="mt-2 flex items-center gap-2">
          <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-line">
            <div
              className="h-full rounded-full bg-gold transition-[width] duration-500"
              style={{ width: `${Math.min(100, Math.round((score / objectif) * 100))}%` }}
            />
          </div>
          <span className="shrink-0 text-kid-xs font-black tabular-nums">{score}</span>
        </div>

        {/* Ce que rapporte la prochaine bonne réponse : la série, et la
            mention qu'on peut encore aller chercher. */}
        {(() => {
          const pts = points.current.oral + points.current.ecrit;
          const restantes = total - index - (phase === 'question' ? 0 : 1);
          const palier = prochainPalier(serie.current);
          const m = multiplicateur(serie.current);
          const assuree = mentionAssuree(pts, total);
          const visee = prochaineMention(pts, total, restantes);
          return (
            <div className="mt-2 grid grid-cols-2 gap-2">
              <div
                key={'serie-' + serie.current}
                className={
                  'recompense-palpite rounded-2xl border-2 px-3 py-1.5 ' +
                  (m > 1 ? 'border-clay bg-clay/10' : 'border-line bg-white-warm')
                }
              >
                <p className="text-kid-xs font-black">
                  🔥 Série {serie.current}
                  {m > 1 ? <span className="text-clay-dark"> · ×{m}</span> : null}
                </p>
                <p className="text-[0.72rem] font-bold leading-tight text-ink-2">
                  {palier
                    ? `Encore ${palier.dans} → points ×${palier.multiplicateur}`
                    : 'Série maximale !'}
                </p>
              </div>
              <div
                key={'mention-' + (assuree ?? '-')}
                className="recompense-palpite rounded-2xl border-2 border-lilac bg-white-warm px-3 py-1.5"
              >
                <p className="text-kid-xs font-black">🏅 Assuré : {assuree ?? '—'}</p>
                <p className="text-[0.72rem] font-bold leading-tight text-ink-2">
                  {visee
                    ? `Encore ${visee.manque} point${visee.manque > 1 ? 's' : ''} → ${visee.lettre}`
                    : assuree === 'A+'
                      ? 'L’or est à toi !'
                      : 'Donne tout jusqu’au bout !'}
                </p>
              </div>
            </div>
          );
        })()}

        {/* Pendant la question, la consigne se range À CÔTÉ du petit plateau,
            dans la place qu'il laisse vide. Quand le coup est gagné, le plateau
            reprend toute la largeur et la consigne repasse dessous, centrée. */}
        <div className="mt-2 flex flex-wrap items-center gap-x-3">
          <div
            className="shrink-0 transition-[width] duration-300 ease-out motion-reduce:transition-none"
            style={{ width: phase === 'plateau' ? '100%' : '44%' }}
          >
            <PlateauJouable
              actif={phase === 'plateau'}
              bordABord={phase === 'plateau'}
              onCoupJoue={(g) => coupJoue(g.points)}
            />
          </div>
          <p
            className={
              'min-w-[40%] flex-1 text-kid-xs font-bold text-muted ' +
              (phase === 'plateau' ? 'mt-2 text-center' : 'text-left')
            }
          >
            {phase === 'plateau'
              ? enBonus
                ? 'COUP BONUS ! Rejoue, c’est cadeau.'
                : multiplicateurDuCoup.current > 1
                  ? `À toi de jouer : ce coup compte ×${multiplicateurDuCoup.current} !`
                  : 'À toi de jouer : touche deux bonbons voisins.'
              : dernierGain > 0
                ? `+${dernierGain} points`
                : 'Réponds juste, et tu gagnes un coup.'}
          </p>
        </div>
        </>
      )}

      <DialogueJeu dernier={moment} />

      {erreur ? <ErrorNote error={erreur} /> : null}

      {phase !== 'plateau' ? (
        <section className="mt-3 rounded-[var(--radius-card)] border border-line bg-white-warm/80 p-4">
          {etape.genre === 'oral' ? (
            // L'oral interroge sur le texte : il reste sous la main, replié
            // pour ne pas pousser les réponses sous le pli.
            <details className="mb-3 rounded-[var(--radius-tile)] bg-sand px-3 py-2">
              <summary className="min-h-8 cursor-pointer text-kid-xs font-black text-clay-dark">
                Relire la situation problème
              </summary>
              <p className="mt-2 text-kid-sm leading-relaxed">{situation.texte}</p>
            </details>
          ) : (
            // Le titre de l'exercice et ses points, comme sur la copie.
            <p className="mb-3 flex items-baseline justify-between gap-3 border-b border-line pb-2">
              <span className="min-w-0 text-kid-xs font-black text-clay-dark">
                {etape.exercice.lecon.title}
              </span>
              <span className="shrink-0 text-kid-xs font-bold text-muted tabular-nums">
                {etape.exercice.questions.length} pt{etape.exercice.questions.length > 1 ? 's' : ''}
              </span>
            </p>
          )}

          <ItemPlayer
            key={etape.item.id}
            item={etape.item}
            rang={rang}
            verrouille={phase === 'corrige'}
            onRepondre={(r) => void repondre(r)}
          />
          {phase === 'corrige' ? (
            <button
              type="button"
              onClick={apresCorrection}
              className="sticky bottom-3 z-10 mt-4 min-h-12 w-full rounded-full bg-ink px-4 py-3 text-kid-sm font-black text-white-warm shadow-lg"
            >
              {justeALaDerniere.current && jeu === 'bonbons' ? 'Jouer mon coup' : 'Question suivante'}
            </button>
          ) : null}
        </section>
      ) : null}
    </main>
  );
}
