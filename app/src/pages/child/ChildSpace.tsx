import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { recordAttempt } from '../../lib/progress';
import { construireMission, TAILLE_MISSION } from '../../lib/mission';
import type { EtapeMission } from '../../lib/mission';
import ItemPlayer from '../../components/items/ItemPlayer';
import type { Reponse } from '../../components/items/ItemPlayer';
import { Button, Card, ErrorNote, Loading, Pill } from '../../components/ui';
import type { ExplanationRow, NotionRow, VideoRow } from '../../types/db';

type LessonBundle = {
  id: string;
  title: string;
  summary: string | null;
  lang: string;
  notions: Array<NotionRow & { explanations: ExplanationRow[] }>;
  videos: VideoRow[];
};

const NIVEAUX = ['Découverte', 'Entraînement', 'Maîtrise', 'Défi'];

/** Fait tourner les registres d’explication : c’est « Explique autrement ». */
function NotionCard({ notion }: { notion: LessonBundle['notions'][number] }) {
  const [montre, setMontre] = useState(0);
  const explications = notion.explanations ?? [];
  const courante = explications.length > 0 ? explications[montre % explications.length] : null;

  return (
    <article className="rounded-2xl border border-line bg-white-warm p-5">
      <Pill>{notion.kind}</Pill>
      <h3 className="mt-2 font-bold">{notion.statement}</h3>
      {courante ? (
        <>
          <p className="mt-3 text-sm text-ink-2">{courante.body}</p>
          {explications.length > 1 ? (
            <button
              type="button"
              className="mt-3 text-sm font-semibold text-clay underline"
              onClick={() => setMontre(montre + 1)}
            >
              Explique autrement ({(montre % explications.length) + 1}/{explications.length})
            </button>
          ) : null}
        </>
      ) : (
        <p className="mt-3 text-sm text-muted">Pas encore d’explication pour cette notion.</p>
      )}
    </article>
  );
}

/**
 * La séance du jour.
 *
 * Une question par notion, au niveau de maîtrise de l'enfant, les notions
 * dues en premier. Chaque réponse est journalisée et met à jour la maîtrise ;
 * c'est elle qui décide de la séance du lendemain.
 */
function Mission({ parentId, childId, lessonId }: { parentId: string; childId: string; lessonId: string }) {
  const qc = useQueryClient();
  const [index, setIndex] = useState(0);
  const [verrouille, setVerrouille] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [gagnes, setGagnes] = useState(0);
  const [justes, setJustes] = useState(0);
  const [erreur, setErreur] = useState<unknown>(null);

  const mission = useQuery({
    queryKey: ['mission', childId, lessonId],
    queryFn: () => construireMission(childId, lessonId),
    staleTime: 0,
  });

  if (mission.isLoading) return <Loading label="Préparation de ta mission…" />;
  if (mission.error) return <ErrorNote error={mission.error} />;

  const etapes = (mission.data ?? []) as EtapeMission[];

  if (etapes.length === 0) {
    return (
      <Card>
        <h3 className="text-xl font-bold">Rien à réviser pour l’instant</h3>
        <p className="mt-2 text-sm text-muted">
          Cette leçon n’a pas encore de questions validées. Reviens quand un parent en aura publié.
        </p>
      </Card>
    );
  }

  if (index >= etapes.length) {
    return (
      <Card className="text-center">
        <div className="mx-auto grid h-16 w-16 place-items-center rounded-full bg-gold/30 text-3xl">
          ★
        </div>
        <h3 className="mt-3 text-2xl font-black">Mission terminée !</h3>
        <p className="mt-2 text-ink-2">
          {justes} bonne{justes > 1 ? 's' : ''} réponse{justes > 1 ? 's' : ''} sur {etapes.length} ·{' '}
          <strong>+{gagnes} points</strong>
        </p>
        <p className="mt-2 text-sm text-muted">
          Ta progression est enregistrée. Les notions ratées reviendront demain.
        </p>
        <Button
          className="mt-4"
          variant="secondary"
          onClick={() => {
            setIndex(0);
            setVerrouille(false);
            setMessage(null);
            setGagnes(0);
            setJustes(0);
            mission.refetch();
          }}
        >
          Rejouer une séance
        </Button>
      </Card>
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
      const bouts: string[] = [reponse.correct ? 'Bravo !' : 'À retenir :'];
      if (etape.item.explain) bouts.push(etape.item.explain);
      if (bilan.points > 0) bouts.push(`+${bilan.points} points`);
      if (bilan.leveledUp) bouts.push(`Tu passes en « ${NIVEAUX[bilan.level - 1]} » !`);
      if (bilan.leveledDown) bouts.push('On reprend plus doucement : relis l’explication.');
      setMessage(bouts.join(' '));
      setGagnes(gagnes + bilan.points);
      if (reponse.correct) setJustes(justes + 1);
      qc.invalidateQueries({ queryKey: ['points', childId] });
    } catch (err) {
      setErreur(err);
      setMessage(null);
    }
  }

  return (
    <Card>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs font-bold tracking-wide text-muted uppercase">
          Question {index + 1} sur {etapes.length}
        </p>
        <Pill>{NIVEAUX[etape.item.level - 1] ?? 'Niveau ' + etape.item.level}</Pill>
      </div>
      <div className="mt-2 h-2 overflow-hidden rounded-full bg-line">
        <div
          className="h-full rounded-full bg-gold transition-all"
          style={{ width: `${(index / etapes.length) * 100}%` }}
        />
      </div>

      <div className="mt-5">
        <ItemPlayer item={etape.item} onRepondre={repondre} verrouille={verrouille} />
      </div>

      {erreur ? (
        <div className="mt-3">
          <ErrorNote error={erreur} />
        </div>
      ) : null}
      {message ? <p className="mt-4 text-sm font-semibold text-ink-2">{message}</p> : null}

      {verrouille ? (
        <Button
          className="mt-4"
          onClick={() => {
            setIndex(index + 1);
            setVerrouille(false);
            setMessage(null);
          }}
        >
          {index + 1 === etapes.length ? 'Voir mon résultat' : 'Question suivante'}
        </Button>
      ) : null}
    </Card>
  );
}

export default function ChildSpace() {
  const { childId } = useParams<{ childId: string }>();
  const [onglet, setOnglet] = useState<'mission' | 'lecon'>('mission');

  const me = useQuery({
    queryKey: ['me'],
    queryFn: async () => {
      const { data } = await supabase.auth.getUser();
      return data.user?.id ?? null;
    },
  });

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
    queryKey: ['lesson-bundle'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('lessons')
        .select(
          'id, title, summary, lang, ' +
            'notions(id, kind, statement, sort_order, parent_id, lesson_id, status, created_at, ' +
            'explanations(id, register, body, notion_id, parent_id, status, created_at)), ' +
            'videos(id, external_url, poster_url, duration_s, status, lesson_id, parent_id, manifest, voice_preset, storage_path, created_at)',
        )
        .eq('status', 'approved')
        .order('sort_order')
        .limit(1)
        .maybeSingle();
      if (error) throw error;
      return data as unknown as LessonBundle | null;
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
    <main className="mx-auto max-w-3xl p-6">
      <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <Pill>Bonjour {child.data?.first_name ?? ''}</Pill>
          <h1 className="mt-2 text-2xl font-black">{bundle?.title ?? 'Pas encore de leçon'}</h1>
        </div>
        <div className="flex items-center gap-3">
          <span className="rounded-full bg-gold/30 px-4 py-2 text-sm font-bold">
            {points.data ?? 0} points
          </span>
          <Link to="/">
            <Button variant="secondary">Changer de profil</Button>
          </Link>
        </div>
      </header>

      {!bundle ? (
        <Card>
          <p className="text-sm text-muted">
            Aucune leçon publiée pour l’instant. Un parent peut en publier une depuis l’espace
            parent.
          </p>
        </Card>
      ) : (
        <>
          <nav className="mb-4 flex gap-2">
            <Button
              variant={onglet === 'mission' ? 'primary' : 'secondary'}
              onClick={() => setOnglet('mission')}
            >
              Ma mission du jour
            </Button>
            <Button
              variant={onglet === 'lecon' ? 'primary' : 'secondary'}
              onClick={() => setOnglet('lecon')}
            >
              Ma leçon
            </Button>
          </nav>

          {onglet === 'mission' ? (
            me.data && childId ? (
              <Mission parentId={me.data} childId={childId} lessonId={bundle.id} />
            ) : (
              <Loading />
            )
          ) : (
            <div className="grid gap-4">
              {video?.external_url ? (
                <Card>
                  <video
                    controls
                    playsInline
                    preload="metadata"
                    poster={video.poster_url ?? undefined}
                    src={video.external_url}
                    className="w-full rounded-2xl"
                  />
                  <p className="mt-3 text-xs text-muted">
                    Film animé · {video.duration_s ?? 0} secondes
                  </p>
                </Card>
              ) : null}

              {bundle.summary ? (
                <Card>
                  <h2 className="text-lg font-bold">Le résumé à retenir</h2>
                  <p className="mt-2 text-ink-2">{bundle.summary}</p>
                </Card>
              ) : null}

              <div className="grid gap-3">
                {notions.map((notion) => (
                  <NotionCard key={notion.id} notion={notion} />
                ))}
              </div>

              <p className="text-center text-xs text-muted">
                Ta mission du jour pose {TAILLE_MISSION} questions au maximum, une par notion.
              </p>
            </div>
          )}
        </>
      )}
    </main>
  );
}
