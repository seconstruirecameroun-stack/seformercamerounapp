import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { Button, Card, ErrorNote, Loading, Pill } from '../../components/ui';

/**
 * La file de validation.
 *
 * C'est le point de contrôle du produit : rien de ce que la machine a écrit
 * n'atteint l'enfant sans être passé ici. Un cahier mal photographié ou une
 * lecture approximative produirait des révisions fausses, et l'enfant
 * réviserait l'erreur.
 *
 * Le parent peut corriger chaque notion avant de publier : c'est plus utile
 * que de tout rejeter pour une phrase bancale.
 */

type NotionEdit = {
  id: string;
  kind: string;
  statement: string;
  sort_order: number;
};

type LessonPending = {
  id: string;
  document_id: string | null;
  title: string;
  summary: string | null;
  lang: string;
  chapter: string | null;
  created_at: string;
  subjects: { label: string } | null;
  notions: NotionEdit[];
};

const TYPES: Record<string, string> = {
  definition: 'Définition',
  date: 'Date',
  liste: 'Liste',
  relation: 'Relation',
};

function LessonCard({ lecon }: { lecon: LessonPending }) {
  const qc = useQueryClient();
  const [titre, setTitre] = useState(lecon.title);
  const [resume, setResume] = useState(lecon.summary ?? '');
  const [notions, setNotions] = useState<NotionEdit[]>(
    [...lecon.notions].sort((a, b) => a.sort_order - b.sort_order),
  );
  const [retirees, setRetirees] = useState<string[]>([]);

  const publier = useMutation({
    mutationFn: async () => {
      const { error: errLecon } = await supabase
        .from('lessons')
        .update({ title: titre.trim(), summary: resume.trim(), status: 'approved' })
        .eq('id', lecon.id);
      if (errLecon) throw errLecon;

      for (const n of notions) {
        const { error } = await supabase
          .from('notions')
          .update({
            statement: n.statement.trim(),
            status: retirees.includes(n.id) ? 'rejected' : 'approved',
          })
          .eq('id', n.id);
        if (error) throw error;
      }

      // Les documents suivent l'état de ce qu'ils ont produit. La leçon ne
      // pointe que vers la première page, on remonte donc à l'envoi entier
      // par son batch_id avant de marquer toutes les pages.
      if (lecon.document_id) {
        const { data: source } = await supabase
          .from('documents')
          .select('batch_id')
          .eq('id', lecon.document_id)
          .maybeSingle();
        if (source?.batch_id) {
          await supabase
            .from('documents')
            .update({ stage: 'publie' })
            .eq('batch_id', source.batch_id);
        } else {
          await supabase.from('documents').update({ stage: 'publie' }).eq('id', lecon.document_id);
        }
      }
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['validation'] });
      qc.invalidateQueries({ queryKey: ['lessons'] });
    },
  });

  const rejeter = useMutation({
    mutationFn: async () => {
      const { error } = await supabase
        .from('lessons')
        .update({ status: 'rejected' })
        .eq('id', lecon.id);
      if (error) throw error;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['validation'] }),
  });

  const gardees = notions.filter((n) => !retirees.includes(n.id)).length;

  return (
    <Card>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <Pill>
            {lecon.subjects?.label ?? 'Matière à définir'} · {lecon.lang.toUpperCase()}
          </Pill>
          <input
            className="mt-2 w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-2.5 text-xl font-bold outline-none transition focus:border-clay"
            value={titre}
            onChange={(e) => setTitre(e.target.value)}
            aria-label="Titre de la leçon"
          />
        </div>
      </div>

      <label className="mt-4 block">
        <span className="mb-1.5 block text-sm font-bold">
          Résumé à retenir
        </span>
        <textarea
          className="w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink outline-none transition focus:border-clay"
          rows={4}
          value={resume}
          onChange={(e) => setResume(e.target.value)}
        />
      </label>

      <p className="mt-4 text-sm font-bold text-muted">
        {gardees} notion{gardees > 1 ? 's' : ''} sur {notions.length}
      </p>

      <ul className="mt-2 grid gap-2">
        {notions.map((n, i) => {
          const retiree = retirees.includes(n.id);
          return (
            <li
              key={n.id}
              className={
                'rounded-2xl border px-4 py-3 ' +
                (retiree ? 'border-line bg-paper opacity-50' : 'border-line bg-white-warm')
              }
            >
              <div className="flex items-center justify-between gap-2">
                <span className="text-sm font-bold text-muted">
                  {TYPES[n.kind] ?? n.kind}
                </span>
                <button
                  type="button"
                  className="text-sm font-semibold text-clay underline"
                  onClick={() =>
                    setRetirees(retiree ? retirees.filter((x) => x !== n.id) : [...retirees, n.id])
                  }
                >
                  {retiree ? 'Remettre' : 'Retirer'}
                </button>
              </div>
              <textarea
                className="mt-1 w-full resize-none rounded-xl border border-transparent bg-transparent text-ink outline-none focus:border-line"
                rows={2}
                value={n.statement}
                disabled={retiree}
                onChange={(e) => {
                  const copie = [...notions];
                  copie[i] = { ...n, statement: e.target.value };
                  setNotions(copie);
                }}
              />
            </li>
          );
        })}
      </ul>

      {publier.error ? <ErrorNote error={publier.error} /> : null}
      {rejeter.error ? <ErrorNote error={rejeter.error} /> : null}

      <div className="mt-4 flex flex-wrap gap-2">
        <Button
          onClick={() => publier.mutate()}
          disabled={publier.isPending || gardees === 0 || titre.trim() === ''}
        >
          {publier.isPending ? 'Publication…' : 'Valider et publier'}
        </Button>
        <Button variant="secondary" onClick={() => rejeter.mutate()} disabled={rejeter.isPending}>
          Tout rejeter
        </Button>
      </div>
    </Card>
  );
}

export default function Validation() {
  const attente = useQuery({
    queryKey: ['validation'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('lessons')
        .select(
          'id, document_id, title, summary, lang, chapter, created_at, subjects(label), ' +
            'notions(id, kind, statement, sort_order)',
        )
        .eq('status', 'pending')
        .order('created_at', { ascending: false });
      if (error) throw error;
      return data as unknown as LessonPending[];
    },
  });

  if (attente.isLoading) return <Loading />;
  if (attente.error) return <ErrorNote error={attente.error} />;

  const liste = attente.data ?? [];

  if (liste.length === 0) {
    return (
      <Card>
        <h2 className="text-xl font-bold">À valider</h2>
        <p className="mt-2 text-sm text-muted">
          Rien n’attend votre relecture. Les leçons extraites d’un cours importé apparaissent ici
          avant d’être visibles par l’enfant.
        </p>
      </Card>
    );
  }

  return (
    <section className="grid gap-4">
      <div>
        <h2 className="text-xl font-bold">
          À valider · {liste.length} leçon{liste.length > 1 ? 's' : ''}
        </h2>
        <p className="mt-1 text-sm text-muted">
          Relisez avant publication : l’enfant ne verra que ce que vous aurez validé.
        </p>
      </div>
      {liste.map((l) => (
        <LessonCard key={l.id} lecon={l} />
      ))}
    </section>
  );
}
