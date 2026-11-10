import { useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { useSession } from '../../lib/auth';
import { ErrorNote, Loading } from '../../components/ui';
import {
  TAILLES,
  compositionsDeLEnfant,
  creerComposition,
  etatDeLaComposition,
  note,
  supprimerComposition,
  tirerQuestions,
  type LeconPourTirage,
} from '../../lib/composition';

/**
 * Préparer une composition.
 *
 * Le parent fait ici ce que fait un maître le vendredi : il annonce les
 * leçons sur lesquelles on composera, et combien de questions. Rien d'autre
 * ne lui est demandé — le tirage, la répartition entre les leçons et entre
 * les quatre étapes sont l'affaire de l'app, et ils se vérifient dans
 * lib/composition.verif.ts.
 *
 * Les leçons sont présentées PAR MATIÈRE et dans l'ordre du cahier, parce
 * que c'est ainsi que le parent les connaît. Celles qui n'ont aucune
 * question n'y figurent pas : les cocher ne donnerait rien à composer.
 */

type LeconCochable = {
  id: string;
  title: string;
  chapter: string | null;
  taught_on: string | null;
  matiere: string;
  questions: number;
  pourTirage: LeconPourTirage;
};

export default function NouvelleComposition() {
  const { childId } = useParams();
  const { session } = useSession();
  const parentId = session?.user.id ?? null;

  const [cochees, setCochees] = useState<Set<string>>(new Set());
  const [taille, setTaille] = useState<number>(20);
  const [titre, setTitre] = useState('');
  const [erreur, setErreur] = useState<unknown>(null);
  const [envoi, setEnvoi] = useState(false);

  const enfant = useQuery({
    queryKey: ['child', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('id, first_name, class_id')
        .eq('id', childId!)
        .single();
      if (error) throw error;
      return data;
    },
  });

  const lecons = useQuery({
    queryKey: ['lecons-composables', enfant.data?.class_id],
    enabled: Boolean(enfant.data),
    queryFn: async (): Promise<LeconCochable[]> => {
      const { data, error } = await supabase
        .from('lessons')
        .select(
          'id, title, chapter, taught_on, sort_order, subjects(label), ' +
            'notions(id, status, items(id, level, status))',
        )
        .eq('status', 'approved')
        .eq('class_id', enfant.data!.class_id!)
        .order('sort_order');
      if (error) throw error;
      type Brut = {
        id: string;
        title: string;
        chapter: string | null;
        taught_on: string | null;
        subjects: { label: string } | { label: string }[] | null;
        notions: Array<{
          id: string;
          status: string;
          items: Array<{ id: string; level: number; status: string }> | null;
        }> | null;
      };
      return ((data ?? []) as unknown as Brut[])
        .map((l) => {
          const sujet = Array.isArray(l.subjects) ? l.subjects[0] : l.subjects;
          const notions = (l.notions ?? [])
            .filter((n) => n.status === 'approved')
            .map((n) => ({
              id: n.id,
              items: (n.items ?? []).filter((i) => i.status === 'approved'),
            }))
            .filter((n) => n.items.length > 0);
          return {
            id: l.id,
            title: l.title,
            chapter: l.chapter,
            taught_on: l.taught_on,
            matiere: sujet?.label ?? 'Sans matière',
            questions: notions.reduce((t, n) => t + n.items.length, 0),
            pourTirage: { id: l.id, notions },
          };
        })
        .filter((l) => l.questions > 0);
    },
  });

  const faites = useQuery({
    queryKey: ['compositions', childId],
    enabled: Boolean(childId),
    queryFn: () => compositionsDeLEnfant(childId!),
  });

  const parMatiere = useMemo(() => {
    const groupes = new Map<string, LeconCochable[]>();
    for (const l of lecons.data ?? []) {
      const liste = groupes.get(l.matiere) ?? [];
      liste.push(l);
      groupes.set(l.matiere, liste);
    }
    return [...groupes.entries()];
  }, [lecons.data]);

  const choisies = (lecons.data ?? []).filter((l) => cochees.has(l.id));
  const disponibles = choisies.reduce((t, l) => t + l.questions, 0);
  // Ce que l'app tirera vraiment : inutile d'annoncer trente questions
  // quand les leçons cochées n'en portent que dix-huit.
  const vraiment = Math.min(taille, disponibles);

  function basculer(id: string) {
    const suite = new Set(cochees);
    if (suite.has(id)) suite.delete(id);
    else suite.add(id);
    setCochees(suite);
  }

  async function creer() {
    if (!parentId || !childId || choisies.length === 0) return;
    setEnvoi(true);
    setErreur(null);
    try {
      const questions = tirerQuestions(
        choisies.map((l) => l.pourTirage),
        taille,
      );
      if (questions.length === 0) throw new Error('Ces leçons ne portent aucune question.');
      const quand = new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long' });
      await creerComposition({
        parentId,
        childId,
        titre: titre.trim() || `Composition du ${quand}`,
        lessons: choisies.map((l) => l.id),
        questions,
      });
      await faites.refetch();
      setCochees(new Set());
      setTitre('');
    } catch (e) {
      setErreur(e);
    } finally {
      setEnvoi(false);
    }
  }

  if (enfant.isLoading || lecons.isLoading) return <Loading label="Les leçons arrivent…" />;
  if (lecons.error) return <ErrorNote error={lecons.error} />;

  return (
    <main className="mx-auto max-w-md p-4 pb-28">
      <Link
        to={`/parent/enfant/${childId}`}
        className="inline-flex min-h-11 items-center text-kid-xs font-bold text-clay-dark"
      >
        ← {enfant.data?.first_name}
      </Link>
      <h1 className="mt-2 text-kid-xl font-extrabold">Préparer une composition</h1>
      <p className="mt-1 text-kid-sm text-muted">
        Cochez les leçons annoncées. L’app tire les questions, réparties entre les leçons et
        sur les quatre étapes.
      </p>

      {faites.data && faites.data.length > 0 ? (
        <section className="mt-4 grid gap-2">
          {faites.data.slice(0, 4).map((c) => (
            <div
              key={c.id}
              className="flex items-center justify-between gap-3 rounded-[var(--radius-card)] border border-line bg-white-warm/80 px-3 py-2"
            >
              <div className="min-w-0">
                <p className="truncate text-kid-sm font-bold">{c.titre}</p>
                <p className="text-kid-xs text-muted">
                  {etatDeLaComposition(c) === 'finie'
                    ? `Finie · ${note(c.justes ?? 0, c.questions.length)}`
                    : etatDeLaComposition(c) === 'en_cours'
                      ? 'Commencée'
                      : `À faire · ${c.questions.length} questions`}
                </p>
              </div>
              {etatDeLaComposition(c) === 'a_faire' ? (
                <button
                  type="button"
                  className="shrink-0 text-kid-xs font-bold text-clay-dark underline"
                  onClick={async () => {
                    await supprimerComposition(c.id);
                    await faites.refetch();
                  }}
                >
                  Retirer
                </button>
              ) : null}
            </div>
          ))}
        </section>
      ) : null}

      <section className="mt-5">
        <h2 className="text-kid-sm font-extrabold">Combien de questions</h2>
        <div className="mt-2 flex gap-2">
          {TAILLES.map((n) => (
            <button
              key={n}
              type="button"
              onClick={() => setTaille(n)}
              className={
                'flex-1 rounded-full border-2 px-3 py-2 text-kid-sm font-black ' +
                (taille === n ? 'border-ink bg-ink text-white-warm' : 'border-line bg-white-warm')
              }
            >
              {n}
            </button>
          ))}
        </div>
      </section>

      <section className="mt-5">
        <label className="text-kid-sm font-extrabold" htmlFor="titre">
          Le titre, si vous en voulez un
        </label>
        <input
          id="titre"
          value={titre}
          onChange={(e) => setTitre(e.target.value)}
          placeholder="Composition de la 2e séquence"
          className="mt-2 w-full rounded-[var(--radius-tile)] border-2 border-line bg-white-warm px-3 py-2 text-kid-sm"
        />
      </section>

      <section className="mt-5">
        <h2 className="text-kid-sm font-extrabold">Les leçons</h2>
        {parMatiere.map(([matiere, liste]) => (
          <div key={matiere} className="mt-3">
            <p className="text-kid-xs font-black tracking-wide text-muted">
              {matiere.toUpperCase()}
            </p>
            <div className="mt-1 grid gap-1.5">
              {liste.map((l) => {
                const prise = cochees.has(l.id);
                return (
                  <button
                    key={l.id}
                    type="button"
                    onClick={() => basculer(l.id)}
                    className={
                      'flex items-center gap-3 rounded-[var(--radius-tile)] border-2 px-3 py-2 text-left ' +
                      (prise ? 'border-ink bg-sand' : 'border-line bg-white-warm')
                    }
                  >
                    <span
                      className={
                        'grid h-6 w-6 shrink-0 place-items-center rounded-md border-2 text-kid-xs font-black ' +
                        (prise ? 'border-ink bg-ink text-white-warm' : 'border-line')
                      }
                    >
                      {prise ? '✓' : ''}
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className="block truncate text-kid-sm font-bold">{l.title}</span>
                      <span className="block text-kid-xs text-muted">
                        {l.questions} questions
                        {l.chapter ? ` · ${l.chapter}` : ''}
                      </span>
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </section>

      {erreur ? <ErrorNote error={erreur} /> : null}

      <div className="fixed inset-x-0 bottom-0 border-t border-line bg-paper/95 p-3 backdrop-blur">
        <div className="mx-auto flex max-w-md items-center gap-3">
          <p className="min-w-0 flex-1 text-kid-xs font-bold text-ink-2">
            {choisies.length === 0
              ? 'Cochez au moins une leçon.'
              : `${choisies.length} leçon${choisies.length > 1 ? 's' : ''} · ${vraiment} question${vraiment > 1 ? 's' : ''}`}
            {choisies.length > 0 && vraiment < taille ? (
              <span className="block text-muted">
                Ces leçons n’en portent pas {taille}.
              </span>
            ) : null}
          </p>
          <button
            type="button"
            disabled={choisies.length === 0 || envoi}
            onClick={creer}
            className="shrink-0 rounded-full bg-ink px-5 py-3 text-kid-sm font-black text-white-warm disabled:opacity-40"
          >
            {envoi ? 'Un instant…' : 'Donner la composition'}
          </button>
        </div>
      </div>
    </main>
  );
}
