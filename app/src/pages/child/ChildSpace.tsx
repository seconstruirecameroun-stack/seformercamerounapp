import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { useSession } from '../../lib/auth';
import { recordAttempt } from '../../lib/progress';
import { construireSeance, estChronometre, PALIERS, SECONDES_DEFI } from '../../lib/paliers';
import { NIVEAU_ACQUIS } from '../../lib/dashboard';
import { stopper } from '../../lib/voix';
import type { Palier } from '../../lib/paliers';
import ItemPlayer from '../../components/items/ItemPlayer';
import type { Reponse } from '../../components/items/ItemPlayer';
import Illustration from '../../components/Illustration';
import Fiches from './Fiches';
import Popup from '../../components/Popup';
import { ErrorNote, Loading } from '../../components/ui';
import type { ExplanationRow, NotionRow, VideoRow } from '../../types/db';

type LessonBundle = {
  id: string;
  title: string;
  summary: string | null;
  lang: string;
  illustration: string | null;
  subject_id: string | null;
  subjects: { label: string } | null;
  notions: Array<NotionRow & { explanations: ExplanationRow[] }>;
  videos: VideoRow[];
};


/** Bouton rond et large : la cible principale de l'espace enfant. */
function GrosBouton({
  children,
  onClick,
  variante = 'clay',
  type = 'button',
  disabled,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  variante?: 'clay' | 'douce';
  type?: 'button' | 'submit';
  disabled?: boolean;
}) {
  const look =
    variante === 'clay'
      ? 'bg-clay text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]'
      : 'bg-white-warm text-ink border-2 border-line shadow-[var(--shadow-tile)]';
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={
        'tuile inline-flex min-h-[54px] items-center justify-center gap-2 rounded-full px-7 text-kid font-extrabold disabled:opacity-45 ' +
        look
      }
    >
      {children}
    </button>
  );
}

/** Les étapes franchies, en galets. Une barre de progression ne dit rien à
    un enfant qui ne sait pas encore lire les pourcentages. */
function Galets({ total, faits }: { total: number; faits: number }) {
  return (
    <div className="flex items-center gap-1.5" aria-label={`${faits} sur ${total}`}>
      {Array.from({ length: total }, (_, i) => (
        <span
          key={i}
          className={
            'h-2.5 rounded-full transition-all duration-300 ' +
            (i < faits ? 'w-7 bg-gold' : i === faits ? 'w-7 bg-gold/35' : 'w-2.5 bg-line')
          }
        />
      ))}
    </div>
  );
}


/**
 * L'étape en cours, en haut de l'écran.
 *
 * C'est la pièce qui manquait : l'enfant jouait sans jamais voir où il en
 * était ni ce qu'il visait. On montre l'escalier entier — les trois étapes,
 * celle où il se trouve — et ce qu'il reste à faire pour franchir celle-ci.
 */
function BarreEtape({
  palier,
  reussies,
  total,
  termine,
}: {
  palier: Palier;
  reussies: number;
  total: number;
  termine: boolean;
}) {
  const part = total === 0 ? 0 : Math.min(1, reussies / total);
  // Au sommet de l'escalier, il n'y a pas d'étape suivante à annoncer.
  const derniere = palier.niveau === PALIERS[PALIERS.length - 1].niveau;
  return (
    <div className="rounded-[var(--radius-card)] border-2 border-line bg-white-warm p-4 shadow-[var(--shadow-tile)]">
      <div className="flex items-center gap-2">
        {PALIERS.map((p) => {
          const franchi = termine || p.niveau < palier.niveau;
          const courant = !termine && p.niveau === palier.niveau;
          return (
            <span
              key={p.niveau}
              title={p.nom}
              className={
                'grid h-9 w-9 shrink-0 place-items-center rounded-full text-kid-sm font-black transition-all duration-300 ' +
                (franchi
                  ? 'bg-leaf text-white-warm'
                  : courant
                    ? 'halo bg-gold text-ink ring-4 ring-gold/30'
                    : 'bg-sand text-muted')
              }
            >
              {franchi ? '★' : p.niveau}
            </span>
          );
        })}
        <span className="ml-1 min-w-0 flex-1">
          <span className="block text-kid-xs font-black tracking-widest text-clay-dark uppercase">
            {termine ? 'Leçon terminée' : `Étape ${palier.niveau} sur ${PALIERS.length}`}
          </span>
          <span className="block truncate text-kid font-extrabold">
            {termine ? 'Tu révises' : palier.nom}
          </span>
        </span>
      </div>

      {/* Le fond doit trancher sur l'or : à la taille d'un téléphone, un
          sable pâle sous une barre dorée se lit comme une barre pleine. */}
      <div className="mt-3 h-4 overflow-hidden rounded-full bg-ink/15 inset-shadow-sm">
        <div
          className="h-full rounded-full bg-gold transition-[width] duration-700 ease-out"
          style={{ width: `${part * 100}%` }}
        />
      </div>
      <p className="mt-1.5 text-kid-sm font-bold text-ink-2">
        {termine
          ? 'Tu peux rejouer autant que tu veux.'
          : reussies >= total
            ? 'Étape réussie !'
            : `Encore ${total - reussies} ${total - reussies > 1 ? 'questions' : 'question'} ${
                derniere ? 'pour terminer la leçon' : `pour passer à l’étape ${palier.niveau + 1}`
              }`}
      </p>
    </div>
  );
}

/**
 * Le sablier de la dernière étape.
 *
 * Il ne sert qu'au Défi : partout ailleurs, presser un enfant qui découvre
 * une notion l'empêche justement de la comprendre. Ici la notion est déjà
 * sue, et c'est la vitesse qu'on vient chercher.
 *
 * Le temps écoulé vaut une réponse manquée — la notion revient, sans drame.
 */
function Chrono({
  cle,
  secondes,
  gele,
  surFin,
}: {
  cle: string;
  secondes: number;
  gele: boolean;
  surFin: () => void;
}) {
  const [reste, setReste] = useState(secondes);
  const fini = useRef(false);
  // La fonction de fin change à chaque rendu du parent. Dans une ref, elle ne
  // relance pas le compte à rebours.
  const fin = useRef(surFin);
  fin.current = surFin;

  useEffect(() => {
    setReste(secondes);
    fini.current = false;
  }, [cle, secondes]);

  useEffect(() => {
    if (gele || fini.current) return;
    if (reste <= 0) {
      fini.current = true;
      fin.current();
      return;
    }
    const t = setTimeout(() => setReste((r) => r - 1), 1000);
    return () => clearTimeout(t);
  }, [reste, gele]);

  const part = Math.max(0, reste / secondes);
  const urgent = reste <= 5;

  return (
    <div className="flex items-center gap-2" aria-label={`${reste} secondes`}>
      <span
        className={
          'grid h-8 w-8 shrink-0 place-items-center rounded-full text-kid-sm font-black tabular-nums ' +
          (urgent ? 'bg-clay text-white-warm' : 'bg-sand text-ink')
        }
      >
        {Math.max(0, reste)}
      </span>
      <span className="h-2.5 flex-1 overflow-hidden rounded-full bg-ink/15">
        <span
          className={'block h-full rounded-full ' + (urgent ? 'bg-clay' : 'bg-leaf')}
          style={{ width: `${part * 100}%`, transition: 'width 1s linear' }}
        />
      </span>
    </div>
  );
}

function Etape({
  parentId,
  childId,
  lessonId,
}: {
  parentId: string;
  childId: string;
  lessonId: string;
}) {
  const qc = useQueryClient();
  const navigate = useNavigate();
  const [index, setIndex] = useState(0);
  const [verrouille, setVerrouille] = useState(false);
  const [retour, setRetour] = useState<{
    ton: 'juste' | 'faux' | 'fete';
    titre: string;
    texte: string;
    points: number;
    vignette: string | null;
    /** Cette réponse vient de franchir l'étape : la fenêtre change de rôle. */
    franchie: boolean;
  } | null>(null);
  const [gagnes, setGagnes] = useState(0);
  const [justes, setJustes] = useState(0);
  /** Notions validées pendant cette séance, pour faire avancer la barre tout de suite. */
  const [validees, setValidees] = useState<Set<string>>(new Set());
  const [revelees, setRevelees] = useState<
    Array<{ id: string; illustration: string | null; statement: string }>
  >([]);
  const [erreur, setErreur] = useState<unknown>(null);

  const seance = useQuery({
    queryKey: ['seance', childId, lessonId],
    queryFn: () => construireSeance(childId, lessonId),
    staleTime: 0,
  });

  /** Nouvelle série de questions, à la suite : l'enfant ne retourne pas au menu. */
  function continuer() {
    setIndex(0);
    setVerrouille(false);
    setGagnes(0);
    setJustes(0);
    setValidees(new Set());
    setRevelees([]);
    setRetour(null);
    seance.refetch();
  }

  if (seance.isLoading) return <Loading label="Je prépare ton étape…" />;
  if (seance.error) return <ErrorNote error={seance.error} />;

  const s = seance.data;

  if (!s || s.questions.length === 0) {
    return (
      <div className="rounded-[var(--radius-card)] border border-line bg-white-warm p-6 text-center">
        <Illustration cle="repos" forme="objet" alt="" className="mx-auto h-28 w-28" />
        <h2 className="mt-3 text-kid-lg font-extrabold">Rien à jouer ici</h2>
        <p className="mt-1 text-kid-sm text-muted">Cette leçon n’a pas encore de questions.</p>
      </div>
    );
  }

  const reussies = s.reussies + validees.size;
  const etapeFranchie = !s.termine && reussies >= s.total;

  if (index >= s.questions.length) {
    const reste = s.total - reussies;
    return (
      <div className="grid gap-3">
        <BarreEtape palier={s.palier} reussies={reussies} total={s.total} termine={s.termine} />

        <div className="monte overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm text-center shadow-[var(--shadow-card)]">
          <div className={'px-6 py-7 ' + (etapeFranchie ? 'bg-leaf/25' : 'bg-gold/25')}>
            <Illustration
              cle='medaille'
              forme="objet"
              alt=""
              className="mx-auto h-28 w-28"
            />
            <h2 className="mt-3 text-kid-2xl font-black">
              {etapeFranchie ? 'Étape réussie !' : 'Bien joué !'}
            </h2>
            <p className="mt-1 text-kid font-bold text-ink-2">
              {justes} sur {s.questions.length} · +{gagnes} points
            </p>
          </div>

          {revelees.length > 0 ? (
            <div className="border-b border-line px-6 py-5">
              <p className="text-kid-xs font-black tracking-widest text-clay-dark uppercase">
                {revelees.length > 1 ? `${revelees.length} images gagnées` : 'Une image gagnée'}
              </p>
              <ul className="mt-3 flex flex-wrap justify-center gap-3">
                {revelees.map((r, i) => (
                  <li key={r.id} className="w-24">
                    <div
                      className="halo revele overflow-hidden rounded-2xl border-2 border-gold"
                      style={{ animationDelay: `${i * 220}ms` }}
                    >
                      <Illustration
                        cle={r.illustration}
                        forme="objet"
                        alt={r.statement}
                        className="h-24 w-24 object-cover"
                      />
                    </div>
                  </li>
                ))}
              </ul>
              <p className="mt-3 text-kid-sm text-muted">Dans ta collection !</p>
            </div>
          ) : null}

          <div className="px-6 py-5">
            <p className="text-kid-sm text-muted">
              {etapeFranchie
                ? PALIERS[s.palier.niveau]
                ? `Tu passes en « ${PALIERS[s.palier.niveau].nom} ».`
                : 'Tu as fini les quatre étapes de cette leçon.'
                : s.termine
                  ? 'Tu connais toute la leçon.'
                  : reste > 0
                    ? `Encore ${reste} ${reste > 1 ? 'questions' : 'question'} à réussir pour l’étape ${s.palier.niveau + 1}.`
                    : 'On continue.'}
            </p>
            <div className="mt-4 flex flex-wrap justify-center gap-2">
              <GrosBouton onClick={continuer}>
                {etapeFranchie ? 'Étape suivante' : 'Continuer'}
              </GrosBouton>
              <GrosBouton variante="douce" onClick={() => navigate(`/enfant/${childId}`)}>
                Mes leçons
              </GrosBouton>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const question = s.questions[index];

  async function repondre(reponse: Reponse) {
    if (verrouille || !s) return;
    setVerrouille(true);
    setErreur(null);
    try {
      const bilan = await recordAttempt({
        parentId,
        childId,
        item: question.item,
        answer: reponse.donnee,
        correct: reponse.correct,
      });

      // La notion tombe pour cette étape : c'est ce qui fait avancer la barre.
      const valide = reponse.correct && !validees.has(question.notion.id);
      const suite = valide ? new Set(validees).add(question.notion.id) : validees;
      if (valide) setValidees(suite);

      const franchie = !s.termine && s.reussies + suite.size >= s.total;
      const acquise = bilan.previousLevel < NIVEAU_ACQUIS && bilan.level >= NIVEAU_ACQUIS;

      const bouts: string[] = [];
      if (question.item.explain) bouts.push(question.item.explain);
      const suivante = PALIERS[s.palier.niveau];
      if (franchie) {
        bouts.push(suivante ? `Tu passes en « ${suivante.nom} » !` : 'Tu connais toute la leçon !');
      }
      else if (acquise) bouts.push('Nouvelle image pour ta collection !');
      else if (!reponse.correct) bouts.push('On la repose tout à l’heure.');

      setRetour({
        ton: franchie || acquise ? 'fete' : reponse.correct ? 'juste' : 'faux',
        titre: franchie
          ? 'Étape réussie !'
          : acquise
            ? 'Image gagnée !'
            : reponse.correct
              ? 'Bravo !'
              : (reponse.donnee as { expire?: boolean })?.expire
                ? 'Trop tard !'
                : 'Presque…',
        texte: bouts.join(' ') || (reponse.correct ? 'Bien joué.' : 'Ce sera pour la prochaine fois.'),
        points: bilan.points,
        vignette: acquise ? question.notion.illustration : null,
        franchie,
      });

      setGagnes((g) => g + bilan.points);
      if (acquise) {
        setRevelees((d) => [
          ...d,
          {
            id: question.notion.id,
            illustration: question.notion.illustration,
            statement: question.notion.statement,
          },
        ]);
      }
      if (reponse.correct) setJustes((j) => j + 1);
      qc.invalidateQueries({ queryKey: ['points', childId] });
      qc.invalidateQueries({ queryKey: ['tableau', childId] });
      qc.invalidateQueries({ queryKey: ['maitrise', childId, lessonId] });
    } catch (err) {
      setErreur(err);
      setRetour(null);
      setVerrouille(false);
    }
  }

  function questionSuivante() {
    // Une étape franchie arrête la série : la suite se joue au niveau du dessus.
    if (retour?.franchie) {
      continuer();
      return;
    }
    setRetour(null);
    setIndex(index + 1);
    setVerrouille(false);
  }

  const derniere = index + 1 === s.questions.length;

  return (
    <div className="grid gap-3">
      <BarreEtape palier={s.palier} reussies={reussies} total={s.total} termine={s.termine} />

      <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-5 shadow-[var(--shadow-card)] sm:p-6">
        <div className="flex items-center justify-between gap-3">
          <Galets total={s.questions.length} faits={index} />
          <span className="rounded-full bg-sand px-3 py-1 text-kid-xs font-black tracking-wide uppercase">
            {s.palier.promesse}
          </span>
        </div>

        {estChronometre(s.niveau) ? (
          <div className="mt-3">
            <Chrono
              cle={question.item.id}
              secondes={SECONDES_DEFI}
              gele={verrouille || retour !== null}
              /* Le temps écoulé vaut une réponse manquée : la notion revient. */
              surFin={() => repondre({ correct: false, donnee: { expire: true } })}
            />
          </div>
        ) : null}

        <div className="mt-5">
          <ItemPlayer
            item={question.item}
            onRepondre={repondre}
            verrouille={verrouille}
            visuel={
              question.notion.illustration ? (
                <Illustration
                  cle={question.notion.illustration}
                  forme="objet"
                  alt=""
                  priorite
                  className="h-14 w-14 shrink-0 rounded-2xl object-cover sm:h-20 sm:w-20"
                />
              ) : null
            }
          />
        </div>

        {erreur ? (
          <div className="mt-4">
            <ErrorNote error={erreur} />
          </div>
        ) : null}

        {retour ? (
          <Popup
            ton={retour.ton}
            titre={retour.titre}
            action={
              retour.franchie ? 'Étape suivante' : derniere ? 'Voir mon résultat' : 'Question suivante'
            }
            onFermer={questionSuivante}
            vignette={
              retour.franchie ? (
                <Illustration cle="medaille" forme="objet" alt="" className="h-28 w-28 object-cover" />
              ) : retour.vignette ? (
                <Illustration
                  cle={retour.vignette}
                  forme="objet"
                  alt=""
                  className="h-28 w-28 object-cover"
                />
              ) : (
                <Illustration cle="guide" forme="portrait" alt="" className="h-28 w-auto" />
              )
            }
          >
            {retour.texte}
            {retour.points > 0 ? (
              <span className="mt-3 block text-kid-lg font-black text-gold">
                +{retour.points} points
              </span>
            ) : null}
          </Popup>
        ) : null}
      </section>
    </div>
  );
}

export default function ChildSpace() {
  const { childId, lessonId } = useParams<{ childId: string; lessonId: string }>();
  const [onglet, setOnglet] = useState<'mission' | 'lecon'>('mission');

  // La voix ne doit pas poursuivre l'enfant d'un écran à l'autre.
  useEffect(() => stopper, []);

  // L'identifiant du parent vient de la session déjà en mémoire. Passer par
  // auth.getUser() ajoutait un aller-retour réseau avant le premier affichage,
  // et l'enfant restait devant un écran vide le temps de la réponse.
  const { session } = useSession();
  const parentId = session?.user.id ?? null;

  const child = useQuery({
    queryKey: ['child', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('id, first_name, avatar')
        .eq('id', childId!)
        .single();
      if (error) throw error;
      return data;
    },
  });

  const lesson = useQuery({
    queryKey: ['lesson-bundle', lessonId],
    enabled: Boolean(lessonId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('lessons')
        .select(
          'id, title, summary, lang, illustration, subject_id, subjects(label), ' +
            'notions(id, kind, statement, sort_order, illustration, parent_id, lesson_id, status, created_at, ' +
            'explanations(id, register, body, notion_id, parent_id, status, created_at)), ' +
            'videos(id, external_url, poster_url, duration_s, status, lesson_id, parent_id, manifest, voice_preset, storage_path, created_at)',
        )
        .eq('id', lessonId!)
        .maybeSingle();
      if (error) throw error;
      return data as unknown as LessonBundle | null;
    },
  });

  const maitrise = useQuery({
    queryKey: ['maitrise', childId, lessonId],
    enabled: Boolean(childId && lessonId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('mastery')
        .select('notion_id, level')
        .eq('child_id', childId!);
      if (error) throw error;
      return new Map((data ?? []).map((m) => [m.notion_id as string, m.level as number]));
    },
  });

  const points = useQuery({
    queryKey: ['points', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('rewards')
        .select('value')
        .eq('child_id', childId!);
      if (error) throw error;
      return (data ?? []).reduce((somme, r) => somme + (r.value ?? 0), 0);
    },
  });

  if (lesson.isLoading || child.isLoading) return <Loading />;
  if (lesson.error) return <ErrorNote error={lesson.error} />;

  const bundle = lesson.data;
  const notions = [...(bundle?.notions ?? [])]
    .filter((n) => n.status === 'approved')
    .sort((a, b) => a.sort_order - b.sort_order);
  const video = bundle?.videos?.[0];

  return (
    <main className="enfant ciel min-h-screen pb-12">
      <div className="mx-auto max-w-2xl px-4 pt-4 sm:px-6">
        <header className="flex items-center justify-between gap-3">
          <Link
            to={
              bundle?.subject_id
                ? `/enfant/${childId}/matiere/${bundle.subject_id}`
                : `/enfant/${childId}`
            }
            className="tuile flex items-center gap-2 rounded-full bg-white-warm/80 py-2 pr-4 pl-3 text-kid-sm font-bold"
          >
            <span aria-hidden="true">←</span>
            <span className="max-w-[11.5rem] truncate">
              {bundle?.subjects?.label ?? 'Mes leçons'}
            </span>
          </Link>
          <span className="flex items-center gap-1.5 rounded-full bg-gold/35 px-4 py-2 text-kid-sm font-black">
            <span aria-hidden="true">★</span>
            {points.data ?? 0}
          </span>
        </header>

        {!bundle ? (
          <div className="mt-8 rounded-[var(--radius-card)] border border-line bg-white-warm p-6 text-center">
            <h1 className="text-kid-lg font-extrabold">Pas encore de leçon</h1>
            <p className="mt-2 text-kid-sm text-muted">
              Un parent doit d’abord en publier une depuis l’espace parent.
            </p>
          </div>
        ) : (
          <>
            <section className="relative mt-4 overflow-hidden rounded-[var(--radius-card)] shadow-[var(--shadow-card)]">
              <Illustration
                cle={bundle.illustration}
                forme="scene"
                alt=""
                priorite
                className={
                  'w-full object-cover transition-[height] duration-300 ' +
                  (onglet === 'lecon' ? 'h-24 sm:h-28' : 'h-40 sm:h-52')
                }
              />
              <div
                className={
                  'absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/80 via-ink/35 to-transparent px-5 pb-3 ' +
                  (onglet === 'lecon' ? 'pt-6' : 'pt-12 pb-4')
                }
              >
                <p className="text-kid-xs font-black tracking-widest text-gold uppercase">
                  {bundle.subjects?.label ?? 'Leçon'}
                </p>
                <h1
                  className={
                    'line-clamp-2 leading-tight font-black text-white-warm text-balance ' +
                    (onglet === 'lecon' || bundle.title.length > 28 ? 'text-kid-lg' : 'text-kid-2xl')
                  }
                >
                  {bundle.title}
                </h1>
              </div>
            </section>

            <nav className="mt-4 flex gap-2" aria-label="Sections">
              {(
                [
                  ['mission', 'Jouer'],
                  ['lecon', 'Apprendre'],
                ] as const
              ).map(([cle, libelle]) => (
                <button
                  key={cle}
                  type="button"
                  onClick={() => setOnglet(cle)}
                  className={
                    'tuile min-h-[46px] flex-1 rounded-full px-4 text-kid font-extrabold ' +
                    (onglet === cle
                      ? 'bg-ink text-white-warm'
                      : 'border-2 border-line bg-white-warm/70 text-ink-2')
                  }
                >
                  {libelle}
                </button>
              ))}
            </nav>

            <div className="mt-4">
              {onglet === 'mission' ? (
                parentId && childId ? (
                  <Etape parentId={parentId} childId={childId} lessonId={bundle.id} />
                ) : (
                  <Loading />
                )
              ) : (
                <div className="grid gap-3">
                  <Fiches
                    film={
                      video?.external_url
                        ? {
                            url: video.external_url,
                            poster: video.poster_url,
                            duree: video.duration_s,
                          }
                        : null
                    }
                    resume={bundle.summary}
                    illustration={bundle.illustration}
                    notions={notions}
                    langue={bundle.lang}
                    niveaux={maitrise.data ?? new Map()}
                    onJouer={() => setOnglet('mission')}
                  />
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </main>
  );
}
