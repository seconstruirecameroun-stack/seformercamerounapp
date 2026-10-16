import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { BUCKET } from '../../lib/import';
import { Button, Card, ErrorNote, Loading, Pill, Vide } from '../../components/ui';

/**
 * La file de validation.
 *
 * C'est le point de contrôle du produit : rien de ce que la machine a écrit
 * n'atteint l'enfant sans être passé ici. Un cahier mal photographié ou une
 * lecture approximative produirait des révisions fausses, et l'enfant
 * réviserait l'erreur.
 *
 * Le défaut de la première version n'était pas son allure : on demandait au
 * parent de vérifier une transcription **sans lui montrer la page du cahier**.
 * Relire de mémoire une leçon écrite en classe la veille ne vérifie rien. La
 * photo est donc à côté du texte, et c'est elle qui fait de cet écran un
 * contrôle plutôt qu'une formalité.
 *
 * Deux autres corrections tenaient à la même idée — rendre visible ce qui
 * engage :
 *
 *   · les énoncés étaient des zones de saisie sans bordure ni fond. On
 *     pouvait les corriger, mais rien ne le disait ;
 *   · « Tout rejeter » touchait « Valider et publier ». Un doigt qui glisse
 *     détruisait un import. Il demande maintenant une confirmation, et il est
 *     posé loin.
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

/**
 * Les pages photographiées de l'envoi dont cette leçon est sortie.
 *
 * Le compartiment est privé : on signe chaque adresse pour une heure, ce qui
 * couvre largement une relecture sans laisser d'adresse publique traîner.
 */
function usePages(documentId: string | null) {
  return useQuery({
    queryKey: ['pages-source', documentId],
    enabled: Boolean(documentId),
    staleTime: 50 * 60 * 1000,
    queryFn: async () => {
      const { data: tete, error: errTete } = await supabase
        .from('documents')
        .select('batch_id')
        .eq('id', documentId!)
        .maybeSingle();
      if (errTete) throw errTete;

      const requete = supabase
        .from('documents')
        .select('id, page_no, storage_path, original_name')
        .order('page_no');
      const { data, error } = tete?.batch_id
        ? await requete.eq('batch_id', tete.batch_id)
        : await requete.eq('id', documentId!);
      if (error) throw error;

      const pages = (data ?? []) as Array<{
        id: string;
        page_no: number;
        storage_path: string | null;
        original_name: string | null;
      }>;

      return Promise.all(
        pages.map(async (p) => {
          if (!p.storage_path) return { ...p, url: null, pdf: false };
          const { data: signe } = await supabase.storage
            .from(BUCKET)
            .createSignedUrl(p.storage_path, 3600);
          return {
            ...p,
            url: signe?.signedUrl ?? null,
            pdf: p.storage_path.toLowerCase().endsWith('.pdf'),
          };
        }),
      );
    },
  });
}

function PagesSource({ documentId }: { documentId: string | null }) {
  const pages = usePages(documentId);
  const [agrandie, setAgrandie] = useState<string | null>(null);

  if (!documentId) {
    return (
      <p className="rounded-2xl border border-dashed border-line px-4 py-6 text-center text-sm text-muted">
        Aucune page d’origine rattachée à cette leçon.
      </p>
    );
  }
  if (pages.isLoading) return <Loading label="J’ouvre les pages…" />;
  if (pages.error) return <ErrorNote error={pages.error} />;

  const liste = pages.data ?? [];

  return (
    <div>
      <p className="mb-2 text-sm font-bold">
        La page du cahier
        <span className="ml-2 font-normal text-muted">
          {liste.length} page{liste.length > 1 ? 's' : ''}
        </span>
      </p>
      <ul className="grid gap-3">
        {liste.map((p) =>
          p.url && !p.pdf ? (
            <li key={p.id}>
              {/* Un appui agrandit : sur un téléphone, une photo de cahier
                  réduite à la largeur d'une colonne ne se relit pas. */}
              <button
                type="button"
                onClick={() => setAgrandie(p.url)}
                className="tuile block w-full overflow-hidden rounded-2xl border-2 border-line bg-white-warm"
              >
                <img
                  src={p.url}
                  alt={`Page ${p.page_no} du cahier`}
                  loading="lazy"
                  className="block w-full"
                />
              </button>
            </li>
          ) : (
            <li key={p.id}>
              <a
                href={p.url ?? '#'}
                target="_blank"
                rel="noreferrer"
                className="tuile flex items-center justify-between gap-2 rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-sm font-bold"
              >
                Page {p.page_no} · {p.pdf ? 'PDF' : 'fichier'}
                <span aria-hidden="true">↗</span>
              </a>
            </li>
          ),
        )}
      </ul>

      {agrandie ? (
        <div
          role="dialog"
          aria-label="Page agrandie"
          className="fixed inset-0 z-50 grid place-items-center bg-ink/80 p-4"
          onClick={() => setAgrandie(null)}
        >
          <img src={agrandie} alt="" className="max-h-full max-w-full rounded-2xl object-contain" />
          <p className="absolute bottom-6 text-sm font-bold text-white-warm">
            Touchez l’image pour refermer
          </p>
        </div>
      ) : null}
    </div>
  );
}

function LessonCard({ lecon }: { lecon: LessonPending }) {
  const qc = useQueryClient();
  const [titre, setTitre] = useState(lecon.title);
  const [chapitre, setChapitre] = useState(lecon.chapter ?? '');
  const [resume, setResume] = useState(lecon.summary ?? '');
  const [notions, setNotions] = useState<NotionEdit[]>(
    [...lecon.notions].sort((a, b) => a.sort_order - b.sort_order),
  );
  const [retirees, setRetirees] = useState<string[]>([]);
  const [confirmeRejet, setConfirmeRejet] = useState(false);

  const publier = useMutation({
    mutationFn: async () => {
      const { error: errLecon } = await supabase
        .from('lessons')
        .update({
          title: titre.trim(),
          chapter: chapitre.trim() || null,
          summary: resume.trim(),
          status: 'approved',
        })
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
  const champ =
    'w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink ' +
    'outline-none transition focus:border-clay';

  return (
    <Card>
      <div className="grid gap-6 lg:grid-cols-[minmax(0,22rem)_minmax(0,1fr)]">
        {/* La source à gauche, et elle reste à vue pendant qu'on fait défiler
            la transcription : c'est elle qu'on compare, ligne à ligne. */}
        <div className="lg:sticky lg:top-6 lg:self-start">
          <PagesSource documentId={lecon.document_id} />
        </div>

        <div>
          <div className="flex flex-wrap items-center gap-2">
            <Pill>
              {lecon.subjects?.label ?? 'Matière à définir'} · {lecon.lang.toUpperCase()}
            </Pill>
            <span className="text-sm text-muted">
              {notions.length} notion{notions.length > 1 ? 's' : ''} extraite
              {notions.length > 1 ? 's' : ''}
            </span>
          </div>

          <div className="mt-4 grid gap-4">
            <label className="block">
              <span className="mb-1.5 block text-sm font-bold">Titre de la leçon</span>
              <input
                className={champ + ' text-lg font-bold'}
                value={titre}
                onChange={(e) => setTitre(e.target.value)}
              />
            </label>

            <label className="block">
              <span className="mb-1.5 block text-sm font-bold">Chapitre</span>
              <input
                className={champ}
                value={chapitre}
                onChange={(e) => setChapitre(e.target.value)}
                placeholder="Par exemple : Éducation à la paix"
              />
              <span className="mt-1 block text-sm text-muted">
                Il range la leçon dans le dossier de la matière, chez l’enfant.
              </span>
            </label>

            <label className="block">
              <span className="mb-1.5 block text-sm font-bold">Résumé à retenir</span>
              <textarea
                className={champ}
                rows={4}
                value={resume}
                onChange={(e) => setResume(e.target.value)}
              />
            </label>
          </div>

          <div className="mt-6 flex items-baseline justify-between gap-3">
            <h3 className="text-base font-extrabold">Les notions</h3>
            <span className="text-sm font-bold text-muted">
              {gardees} gardée{gardees > 1 ? 's' : ''} sur {notions.length}
            </span>
          </div>

          <ul className="mt-2 grid gap-2">
            {notions.map((n, i) => {
              const retiree = retirees.includes(n.id);
              return (
                <li
                  key={n.id}
                  className={
                    'rounded-2xl border-2 px-4 py-3 transition ' +
                    (retiree ? 'border-line bg-paper' : 'border-line bg-white-warm')
                  }
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-sm font-bold text-muted">
                      {TYPES[n.kind] ?? n.kind}
                    </span>
                    <button
                      type="button"
                      aria-pressed={!retiree}
                      className={
                        'rounded-full px-3 py-1 text-sm font-bold transition ' +
                        (retiree
                          ? 'bg-line text-ink-2'
                          : 'bg-leaf/15 text-leaf')
                      }
                      onClick={() =>
                        setRetirees(
                          retiree ? retirees.filter((x) => x !== n.id) : [...retirees, n.id],
                        )
                      }
                    >
                      {retiree ? '✕ Retirée' : '✓ Gardée'}
                    </button>
                  </div>
                  {/* La bordure est visible : une zone de saisie transparente
                      ne dit pas qu'on peut corriger le mot mal lu. */}
                  <textarea
                    className={
                      'mt-2 w-full resize-y rounded-xl border-2 px-3 py-2 text-base outline-none transition ' +
                      (retiree
                        ? 'border-transparent bg-transparent text-muted line-through'
                        : 'border-line bg-white-warm focus:border-clay')
                    }
                    rows={2}
                    value={n.statement}
                    disabled={retiree}
                    aria-label={`Énoncé de la notion ${i + 1}`}
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

          {publier.error ? (
            <div className="mt-4">
              <ErrorNote error={publier.error} />
            </div>
          ) : null}
          {rejeter.error ? (
            <div className="mt-4">
              <ErrorNote error={rejeter.error} />
            </div>
          ) : null}

          <div className="mt-6 border-t border-line pt-4">
            <Button
              onClick={() => publier.mutate()}
              disabled={publier.isPending || gardees === 0 || titre.trim() === ''}
            >
              {publier.isPending ? 'Publication…' : 'Valider et publier'}
            </Button>
            <p className="mt-2 text-sm text-muted">
              {gardees === 0
                ? 'Gardez au moins une notion pour pouvoir publier.'
                : 'Après publication, la leçon apparaît chez l’enfant.'}
            </p>

            {/* L'action destructrice est séparée par un filet, et demande un
                second geste : un doigt qui glisse ne doit pas défaire un
                import. */}
            <div className="mt-5 border-t border-dashed border-line pt-4">
              {confirmeRejet ? (
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-sm font-bold">Rejeter toute la leçon ?</span>
                  <Button
                    variant="danger"
                    onClick={() => rejeter.mutate()}
                    disabled={rejeter.isPending}
                  >
                    {rejeter.isPending ? 'Rejet…' : 'Oui, rejeter'}
                  </Button>
                  <Button variant="ghost" onClick={() => setConfirmeRejet(false)}>
                    Annuler
                  </Button>
                </div>
              ) : (
                <Button variant="ghost" onClick={() => setConfirmeRejet(true)}>
                  Tout rejeter
                </Button>
              )}
            </div>
          </div>
        </div>
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

  if (attente.isLoading) {
    return (
      <Card titre="À valider" sous="Ce que la lecture a tiré de vos photos, avant publication.">
        <Loading />
      </Card>
    );
  }
  if (attente.error) {
    return (
      <Card titre="À valider" sous="Ce que la lecture a tiré de vos photos, avant publication.">
        <ErrorNote error={attente.error} />
      </Card>
    );
  }

  const liste = attente.data ?? [];

  if (liste.length === 0) {
    return (
      <Card titre="À valider" sous="Ce que la lecture a tiré de vos photos, avant publication.">
        <Vide
          titre="Rien n’attend votre relecture"
          texte="Les leçons extraites d’un cours importé apparaissent ici. L’enfant ne verra que ce que vous aurez validé."
        />
      </Card>
    );
  }

  return (
    <section className="grid gap-4">
      <div className="rounded-[var(--radius-card)] border-2 border-gold bg-white-warm/85 px-5 py-4 sm:px-6">
        <h2 className="text-lg font-extrabold">
          À valider · {liste.length} leçon{liste.length > 1 ? 's' : ''}
        </h2>
        <p className="mt-0.5 text-sm text-muted">
          Comparez avec la page du cahier, corrigez ce qui a été mal lu, retirez ce qui n’a rien à
          y faire. L’enfant ne verra que ce que vous aurez validé.
        </p>
      </div>
      {liste.map((l) => (
        <LessonCard key={l.id} lecon={l} />
      ))}
    </section>
  );
}
