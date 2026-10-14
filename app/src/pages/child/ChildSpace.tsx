import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { recordAttempt } from '../../lib/progress';
import { Button, Card, ErrorNote, Loading, Pill } from '../../components/ui';
import type { ExplanationRow, ItemRow, NotionRow, VideoRow } from '../../types/db';

type LessonBundle = {
  id: string;
  title: string;
  summary: string | null;
  lang: string;
  notions: Array<NotionRow & { explanations: ExplanationRow[]; items: ItemRow[] }>;
  videos: VideoRow[];
};

type QcmPayload = { question: string; options: string[] };

function isQcm(item: ItemRow): item is ItemRow & { payload: QcmPayload } {
  const p = item.payload as Partial<QcmPayload> | null;
  return item.kind === 'qcm' && Array.isArray(p?.options) && typeof p?.question === 'string';
}

function answerIndex(item: ItemRow): number | null {
  const a = item.answer as { index?: number } | null;
  return typeof a?.index === 'number' ? a.index : null;
}

/** Fait tourner les registres d’explication : c’est « Explique autrement ». */
function NotionCard({ notion }: { notion: LessonBundle['notions'][number] }) {
  const [shown, setShown] = useState(0);
  const explanations = notion.explanations;
  const current = explanations[shown % Math.max(explanations.length, 1)];

  return (
    <article className="rounded-2xl border border-line bg-white-warm p-5">
      <Pill>{notion.kind}</Pill>
      <h3 className="mt-2 font-bold">{notion.statement}</h3>
      {current ? (
        <>
          <p className="mt-3 text-sm text-ink-2">{current.body}</p>
          {explanations.length > 1 ? (
            <button
              type="button"
              className="mt-3 text-sm font-semibold text-clay underline"
              onClick={() => setShown(shown + 1)}
            >
              Explique autrement ({(shown % explanations.length) + 1}/{explanations.length})
            </button>
          ) : null}
        </>
      ) : (
        <p className="mt-3 text-sm text-muted">Pas encore d’explication pour cette notion.</p>
      )}
    </article>
  );
}

function Games({
  items,
  parentId,
  childId,
}: {
  items: ItemRow[];
  parentId: string;
  childId: string;
}) {
  const qc = useQueryClient();
  const [index, setIndex] = useState(0);
  const [picked, setPicked] = useState<number | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);

  const playable = useMemo(() => items.filter(isQcm), [items]);
  const item = playable[index];

  if (playable.length === 0) {
    return (
      <Card>
        <p className="text-sm text-muted">
          Aucun jeu disponible pour cette leçon. Le moteur complet arrive au lot 3.
        </p>
      </Card>
    );
  }

  if (!item) {
    return (
      <Card className="text-center">
        <h3 className="text-xl font-bold">C’est terminé pour aujourd’hui.</h3>
        <p className="mt-2 text-sm text-muted">Ta progression est enregistrée.</p>
        <Button
          className="mt-4"
          variant="secondary"
          onClick={() => {
            setIndex(0);
            setPicked(null);
            setFeedback(null);
          }}
        >
          Recommencer
        </Button>
      </Card>
    );
  }

  const correctIndex = answerIndex(item);

  async function choose(option: number) {
    if (picked !== null || busy) return;
    setPicked(option);
    setBusy(true);
    setError(null);
    const correct = option === correctIndex;
    try {
      const outcome = await recordAttempt({
        parentId,
        childId,
        item,
        answer: { index: option },
        correct,
      });
      const bits: string[] = [];
      bits.push(correct ? 'Bravo !' : 'À retenir :');
      if (item.explain) bits.push(item.explain);
      if (outcome.points > 0) bits.push('+' + outcome.points + ' points');
      if (outcome.leveledUp) bits.push('Tu passes au niveau ' + outcome.level + ' !');
      if (outcome.leveledDown) bits.push('On reprend plus doucement, lis une autre explication.');
      setFeedback(bits.join(' '));
      qc.invalidateQueries({ queryKey: ['points', childId] });
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card>
      <p className="text-xs font-bold tracking-wide text-muted uppercase">
        Question {index + 1} sur {playable.length} · niveau {item.level}
      </p>
      <h3 className="mt-2 text-xl font-bold">{(item.payload as QcmPayload).question}</h3>

      <div className="mt-4 grid gap-2">
        {(item.payload as QcmPayload).options.map((option, i) => {
          const isAnswer = i === correctIndex;
          const chosen = picked === i;
          let look = 'border-line bg-white-warm hover:border-ink-2';
          if (picked !== null && isAnswer) look = 'border-leaf bg-leaf/15';
          else if (chosen) look = 'border-clay bg-clay/10';
          return (
            <button
              key={i}
              type="button"
              disabled={picked !== null}
              onClick={() => choose(i)}
              className={'rounded-2xl border px-4 py-3 text-left transition ' + look}
            >
              {option}
            </button>
          );
        })}
      </div>

      {error ? <div className="mt-3"><ErrorNote error={error} /></div> : null}
      {feedback ? <p className="mt-4 text-sm font-semibold text-ink-2">{feedback}</p> : null}

      {picked !== null ? (
        <Button
          className="mt-4"
          onClick={() => {
            setIndex(index + 1);
            setPicked(null);
            setFeedback(null);
          }}
        >
          {index + 1 === playable.length ? 'Voir le résultat' : 'Question suivante'}
        </Button>
      ) : null}
    </Card>
  );
}

export default function ChildSpace() {
  const { childId } = useParams<{ childId: string }>();
  const [tab, setTab] = useState<'lecon' | 'jeux'>('lecon');

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
            'explanations(id, register, body, notion_id, parent_id, status, created_at), ' +
            'items(id, kind, level, payload, answer, explain, notion_id, parent_id, status, created_at)), ' +
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
      return (data ?? []).reduce((sum, row) => sum + (row.value ?? 0), 0);
    },
  });

  if (lesson.isLoading || child.isLoading) return <Loading />;
  if (lesson.error) return <ErrorNote error={lesson.error} />;

  const bundle = lesson.data;
  const notions = (bundle?.notions ?? []).slice().sort((a, b) => a.sort_order - b.sort_order);
  const items = notions.flatMap((n) => n.items ?? []).sort((a, b) => a.level - b.level);
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
            Aucune leçon publiée pour l’instant. Un parent peut en charger une depuis l’espace
            parent.
          </p>
        </Card>
      ) : (
        <>
          <nav className="mb-4 flex gap-2">
            <Button variant={tab === 'lecon' ? 'primary' : 'secondary'} onClick={() => setTab('lecon')}>
              Ma leçon
            </Button>
            <Button variant={tab === 'jeux' ? 'primary' : 'secondary'} onClick={() => setTab('jeux')}>
              Mes jeux
            </Button>
          </nav>

          {tab === 'lecon' ? (
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
            </div>
          ) : me.data && childId ? (
            <Games items={items} parentId={me.data} childId={childId} />
          ) : (
            <Loading />
          )}
        </>
      )}
    </main>
  );
}
