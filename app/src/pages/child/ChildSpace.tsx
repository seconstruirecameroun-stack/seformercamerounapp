import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { useSession } from '../../lib/auth';
import { recordAttempt } from '../../lib/progress';
import { construireMission } from '../../lib/mission';
import { NIVEAU_ACQUIS } from '../../lib/dashboard';
import { stopper } from '../../lib/voix';
import type { EtapeMission } from '../../lib/mission';
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
  subjects: { label: string } | null;
  notions: Array<NotionRow & { explanations: ExplanationRow[] }>;
  videos: VideoRow[];
};

const NIVEAUX = ['Découverte', 'Entraînement', 'Maîtrise', 'Défi'];

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

function Mission({
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
  // Le retour de la dernière réponse : tant qu'il est posé, la fenêtre est
  // ouverte et c'est elle qui porte le passage à la question suivante.
  const [retour, setRetour] = useState<{
    ton: 'juste' | 'faux' | 'fete';
    titre: string;
    texte: string;
    points: number;
    vignette: string | null;
  } | null>(null);
  const [gagnes, setGagnes] = useState(0);
  const [justes, setJustes] = useState(0);
  // Les notions qui viennent de franchir le seuil de maîtrise pendant cette
  // séance : ce sont elles qui se révéleront sur l'écran de fin.
  const [revelees, setRevelees] = useState<Array<{ id: string; illustration: string | null; statement: string }>>([]);
  const [erreur, setErreur] = useState<unknown>(null);

  const mission = useQuery({
    queryKey: ['mission', childId, lessonId],
    queryFn: () => construireMission(childId, lessonId),
    staleTime: 0,
  });

  if (mission.isLoading) return <Loading label="Je prépare ta mission…" />;
  if (mission.error) return <ErrorNote error={mission.error} />;

  const etapes = (mission.data ?? []) as EtapeMission[];

  if (etapes.length === 0) {
    return (
      <div className="rounded-[var(--radius-card)] border border-line bg-white-warm p-6 text-center">
        <Illustration cle="repos" forme="objet" alt="" className="mx-auto h-28 w-28" />
        <h2 className="mt-3 text-kid-lg font-extrabold">Rien à réviser</h2>
        <p className="mt-1 text-kid-sm text-muted">Reviens demain !</p>
      </div>
    );
  }

  if (index >= etapes.length) {
    return (
      <div className="monte overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm text-center shadow-[var(--shadow-card)]">
        <div className="bg-gold/25 px-6 py-7">
          <Illustration cle="medaille" forme="objet" alt="" className="mx-auto h-28 w-28" />
          <h2 className="mt-3 text-kid-2xl font-black">Mission terminée !</h2>
          <p className="mt-1 text-kid font-bold text-ink-2">
            {justes} sur {etapes.length} · +{gagnes} points
          </p>
        </div>
        {revelees.length > 0 ? (
          <div className="border-b border-line px-6 py-5">
            <p className="text-kid-xs font-black tracking-widest text-clay-dark uppercase">
              {revelees.length > 1
                ? `${revelees.length} images gagnées`
                : 'Une image gagnée'}
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
            <p className="mt-3 text-kid-sm text-muted">
              {revelees.length > 1 ? 'Dans ta collection !' : 'Dans ta collection !'}
            </p>
          </div>
        ) : null}
        <div className="px-6 py-5">
          <p className="text-kid-sm text-muted">
            {justes === etapes.length
              ? 'Tout juste ! On revérifie dans quelques jours.'
              : 'On revoit demain ce qui a coincé.'}
          </p>
          <div className="mt-4 flex flex-wrap justify-center gap-2">
            <GrosBouton onClick={() => navigate(`/enfant/${childId}`)}>Mes leçons</GrosBouton>
            <GrosBouton
              variante="douce"
              onClick={() => {
                setIndex(0);
                setVerrouille(false);
                setGagnes(0);
                setJustes(0);
                setRevelees([]);
                setRetour(null);
                mission.refetch();
              }}
            >
              Rejouer
            </GrosBouton>
          </div>
        </div>
      </div>
    );
  }

  const etape = etapes[index];

  async function repondre(reponse: Reponse) {
    if (verrouille) return;
    setVerrouille(true);
    setErreur(null);
    try {
      const bilan = await recordAttempt({
        parentId,
        childId,
        item: etape.item,
        answer: reponse.donnee,
        correct: reponse.correct,
      });
      const acquise = bilan.previousLevel < NIVEAU_ACQUIS && bilan.level >= NIVEAU_ACQUIS;

      const bouts: string[] = [];
      if (etape.item.explain) bouts.push(etape.item.explain);
      if (acquise) bouts.push('Nouvelle image pour ta collection !');
      else if (bilan.leveledUp) bouts.push(`Tu passes en « ${NIVEAUX[bilan.level - 1]} » !`);
      if (bilan.leveledDown) bouts.push('On reprend plus doucement.');

      setRetour({
        ton: acquise ? 'fete' : reponse.correct ? 'juste' : 'faux',
        titre: acquise ? 'Image gagnée !' : reponse.correct ? 'Bravo !' : 'Presque…',
        texte: bouts.join(' ') || (reponse.correct ? 'Bien joué.' : 'Ce sera pour la prochaine fois.'),
        points: bilan.points,
        vignette: acquise ? etape.notion.illustration : null,
      });
      setGagnes(gagnes + bilan.points);
      if (acquise) {
        setRevelees((d) => [
          ...d,
          {
            id: etape.notion.id,
            illustration: etape.notion.illustration,
            statement: etape.notion.statement,
          },
        ]);
      }
      if (reponse.correct) setJustes(justes + 1);
      qc.invalidateQueries({ queryKey: ['points', childId] });
      qc.invalidateQueries({ queryKey: ['tableau', childId] });
    } catch (err) {
      setErreur(err);
      setRetour(null);
      setVerrouille(false);
    }
  }

  function questionSuivante() {
    setRetour(null);
    setIndex(index + 1);
    setVerrouille(false);
  }

  return (
    <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-5 shadow-[var(--shadow-card)] sm:p-6">
      <div className="flex items-center justify-between gap-3">
        <Galets total={etapes.length} faits={index} />
        <span className="rounded-full bg-sand px-3 py-1 text-kid-xs font-black tracking-wide uppercase">
          {NIVEAUX[etape.item.level - 1] ?? 'Niveau ' + etape.item.level}
        </span>
      </div>

      <div className="mt-5">
        <ItemPlayer
          item={etape.item}
          onRepondre={repondre}
          verrouille={verrouille}
          visuel={
            etape.notion.illustration ? (
              <Illustration
                cle={etape.notion.illustration}
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
          action={index + 1 === etapes.length ? 'Voir mon résultat' : 'Question suivante'}
          onFermer={questionSuivante}
          vignette={
            retour.vignette ? (
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
          'id, title, summary, lang, illustration, subjects(label), ' +
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
            to={`/enfant/${childId}`}
            className="tuile flex items-center gap-2 rounded-full bg-white-warm/80 py-2 pr-4 pl-3 text-kid-sm font-bold"
          >
            <span aria-hidden="true">←</span>
            Mes leçons
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
                  <Mission parentId={parentId} childId={childId} lessonId={bundle.id} />
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
