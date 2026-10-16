import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { useSession } from '../../lib/auth';
import { Button, Card, ErrorNote, Field, Loading, Pill, Vide } from '../../components/ui';
import ImportCourse from './ImportCourse';
import Validation from './Validation';
import Illustrations from './Illustrations';
import Rappels from '../../components/parent/Rappels';
import Progres from '../../components/parent/Progres';
import NouvelEnfant from '../../components/parent/NouvelEnfant';
import { verrouiller } from '../../components/PinGate';
import Mascotte from '../../components/jeu/Mascotte';
import type { ClassRow } from '../../types/db';

const ETAPES: Record<string, string> = {
  importe: 'Importé',
  en_lecture: 'Lecture en cours',
  a_valider: 'À valider',
  publie: 'Publié',
  echec: 'Échec',
};

type ChildWithClass = {
  id: string;
  first_name: string;
  avatar: string | null;
  class_id: string | null;
  school: string | null;
  classes: { code: string; subsystem: string } | null;
};

/**
 * Les enfants : la liste et l'ajout au même endroit.
 *
 * C'étaient deux cartes voisines, « Profils » puis « Ajouter un enfant ». Un
 * parent qui vient d'en ajouter un cherchait ensuite où il était passé. Le
 * formulaire est maintenant replié sous la liste : on le déplie quand on en a
 * besoin, et le résultat apparaît juste au-dessus.
 */
/**
 * Les enfants : leur avancement, et de quoi en ajouter un.
 *
 * La liste des prénoms a cédé la place aux cartes de progression — c'est la
 * première chose qu'un parent vient voir, et c'était justement ce qui
 * manquait. Le formulaire d'ajout reste replié dessous : on l'ouvre deux fois
 * dans la vie de l'app.
 */
/**
 * Les enfants : leur avancement, et de quoi en ajouter un.
 *
 * La liste des prénoms a cédé la place aux cartes de progression — c'est la
 * première chose qu'un parent vient voir. L'ajout, lui, est passé d'un
 * formulaire de trois champs à un assistant : on n'ajoute un enfant que deux
 * fois dans la vie de l'app, autant poser les bonnes questions ce jour-là.
 */
function Enfants({
  classes,
  enfants,
  chargement,
  erreur,
}: {
  classes: ClassRow[];
  enfants: ChildWithClass[];
  chargement: boolean;
  erreur: unknown;
}) {
  const [assistant, setAssistant] = useState(false);

  // Presque toujours la même école d'un enfant à l'autre : on la propose.
  const ecoleConnue = enfants.map((e) => e.school).find((s) => s && s.trim()) ?? null;

  return (
    <section className="grid gap-4">
      <div>
        <h2 className="text-lg font-extrabold">Vos enfants</h2>
        <p className="mt-0.5 text-sm text-muted">Où ils en sont, et depuis quand.</p>
      </div>

      {chargement ? <Loading /> : null}
      {erreur ? <ErrorNote error={erreur} /> : null}

      <Progres enfants={enfants} />

      {!chargement && enfants.length === 0 && !assistant ? (
        <Vide
          titre="Aucun profil pour l’instant"
          texte="Ajoutez un premier enfant : c’est lui qui recevra les cours que vous importerez."
          action={<Button onClick={() => setAssistant(true)}>Ajouter un enfant</Button>}
        />
      ) : null}

      {assistant ? (
        <NouvelEnfant
          classes={classes}
          ecoleConnue={ecoleConnue}
          onFini={() => setAssistant(false)}
        />
      ) : enfants.length > 0 ? (
        <Button
          variant="secondary"
          className="justify-self-start"
          onClick={() => setAssistant(true)}
        >
          + Ajouter un enfant
        </Button>
      ) : null}
    </section>
  );
}

function PinSetup() {
  const [pin, setPin] = useState('');
  const [done, setDone] = useState(false);

  const isSet = useQuery({
    queryKey: ['pin-set'],
    queryFn: async () => {
      const { data, error } = await supabase.rpc('parent_pin_is_set');
      if (error) throw error;
      return data as boolean;
    },
  });

  const save = useMutation({
    mutationFn: async () => {
      const { error } = await supabase.rpc('set_parent_pin', { new_pin: pin });
      if (error) throw error;
    },
    onSuccess: () => {
      setPin('');
      setDone(true);
      isSet.refetch();
    },
  });

  return (
    <Card
      titre="Code de l’espace parent"
      sous="Quatre chiffres qui protègent l’import, la validation et les réglages."
    >
      <p
        className={
          'rounded-2xl px-4 py-3 text-sm font-semibold ' +
          (isSet.data ? 'bg-leaf/15 text-leaf' : 'bg-gold/25 text-ink-2')
        }
      >
        {isSet.data
          ? 'Un code est défini. Vous pouvez le remplacer ci-dessous.'
          : 'Aucun code pour l’instant : sur cet appareil, l’espace parent est ouvert à tous — y compris à vos enfants.'}
      </p>
      <form
        className="mt-4 flex flex-wrap items-end gap-3"
        onSubmit={(e) => {
          e.preventDefault();
          save.mutate();
        }}
      >
        <Field
          label="Nouveau code"
          inputMode="numeric"
          maxLength={4}
          value={pin}
          onChange={(e) => setPin(e.target.value.replace(/\D/g, ''))}
        />
        <Button type="submit" disabled={pin.length !== 4 || save.isPending}>
          Enregistrer
        </Button>
      </form>
      {save.error ? <ErrorNote error={save.error} /> : null}
      {done ? <p className="mt-3 text-sm text-leaf">Code enregistré.</p> : null}
    </Card>
  );
}

function Library() {
  const qc = useQueryClient();

  const lessons = useQuery({
    queryKey: ['lessons'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('lessons')
        .select('id, title, lang, chapter, status, subjects(label), notions(count)')
        .order('sort_order');
      if (error) throw error;
      return data as unknown as Array<{
        id: string;
        title: string;
        lang: string;
        chapter: string | null;
        status: string;
        subjects: { label: string } | null;
        notions: Array<{ count: number }>;
      }>;
    },
  });

  const seed = useMutation({
    mutationFn: async () => {
      const { error } = await supabase.rpc('seed_demo_prehistoire');
      if (error) throw error;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['lessons'] }),
  });

  return (
    <Card
      titre="Bibliothèque"
      sous="Tout ce que vos enfants peuvent déjà jouer."
      actions={
        <Button variant="secondary" onClick={() => seed.mutate()} disabled={seed.isPending}>
          {seed.isPending ? 'Chargement…' : 'Leçon de démonstration'}
        </Button>
      }
    >
      {seed.error ? <div className="mb-3"><ErrorNote error={seed.error} /></div> : null}

      {lessons.isLoading ? <Loading /> : null}
      {lessons.error ? <ErrorNote error={lessons.error} /> : null}

      <ul className="grid gap-3">
        {(lessons.data ?? []).map((lesson) => (
          <li
            key={lesson.id}
            className="flex flex-wrap items-center justify-between gap-2 rounded-2xl border border-line px-4 py-3"
          >
            <div>
              <strong>{lesson.title}</strong>
              <small className="ml-2 text-muted">
                {lesson.subjects?.label ?? 'Matière à définir'} · {lesson.lang.toUpperCase()} ·{' '}
                {lesson.notions?.[0]?.count ?? 0} notions
              </small>
            </div>
            <Pill>{lesson.status === 'approved' ? 'publiée' : lesson.status}</Pill>
          </li>
        ))}
      </ul>

      {lessons.data && lessons.data.length === 0 ? (
        <Vide
          titre="Aucune leçon publiée"
          texte="Importez un cours photographié, ou chargez la leçon de démonstration pour voir à quoi ressemble le jeu."
        />
      ) : null}
    </Card>
  );
}

/**
 * Les documents importés, regroupés par envoi.
 *
 * Un envoi (batch_id) correspond à ce que le parent a photographié d'un coup.
 * C'est le candidat naturel pour « une leçon », mais rien n'est figé : le
 * découpage réel se décide à l'extraction, puis se corrige à la validation.
 */
function BoutonLecture({ batchId, stage }: { batchId: string | null; stage: string }) {
  const qc = useQueryClient();
  const lire = useMutation({
    mutationFn: async () => {
      const { data, error } = await supabase.functions.invoke('analyze-document', {
        body: { batch_id: batchId },
      });
      if (error) throw error;
      return data as { notions?: number; avertissements?: string[] };
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['documents'] });
      qc.invalidateQueries({ queryKey: ['validation'] });
    },
  });

  if (!batchId) return null;

  return (
    <div className="mt-2">
      <Button
        variant="secondary"
        onClick={() => lire.mutate()}
        disabled={lire.isPending || stage === 'en_lecture'}
      >
        {lire.isPending ? 'Lecture en cours…' : stage === 'echec' ? 'Relancer la lecture' : 'Lire ce cours'}
      </Button>
      {lire.error ? (
        <div className="mt-2">
          <ErrorNote error={lire.error} />
        </div>
      ) : null}
      {lire.data ? (
        <p className="mt-2 text-sm text-leaf">
          {lire.data.notions} notions extraites. À relire dans « À valider ».
        </p>
      ) : null}
      {lire.data?.avertissements && lire.data.avertissements.length > 0 ? (
        <ul className="mt-2 rounded-2xl bg-gold/20 px-4 py-3 text-sm">
          {lire.data.avertissements.map((a, i) => (
            <li key={i}>⚠ {a}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

function Documents() {
  const docs = useQuery({
    queryKey: ['documents'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('documents')
        .select(
          'id, batch_id, page_no, original_name, kind, stage, stage_error, lang, created_at, ' +
            'children(first_name), subjects(label)',
        )
        .order('created_at', { ascending: false })
        .order('page_no');
      if (error) throw error;
      return data as unknown as Array<{
        id: string;
        batch_id: string | null;
        page_no: number;
        original_name: string | null;
        kind: string;
        stage: string;
        stage_error: string | null;
        lang: string | null;
        created_at: string;
        children: { first_name: string } | null;
        subjects: { label: string } | null;
      }>;
    },
  });

  const envois = new Map<string, NonNullable<typeof docs.data>>();
  for (const d of docs.data ?? []) {
    const cle = d.batch_id ?? d.id;
    if (!envois.has(cle)) envois.set(cle, []);
    envois.get(cle)!.push(d);
  }

  return (
    <Card
      titre="Documents importés"
      sous="Chaque envoi, et où il en est de sa lecture."
    >
      {docs.isLoading ? <Loading /> : null}
      {docs.error ? <ErrorNote error={docs.error} /> : null}

      {envois.size === 0 && !docs.isLoading ? (
        <Vide
          titre="Rien d’importé pour l’instant"
          texte="Les pages que vous photographiez apparaîtront ici, groupées par envoi, avec leur état d’avancement."
        />
      ) : null}

      <ul className="grid gap-3">
        {[...envois.values()].map((pages) => {
          const tete = pages[0];
          const enEchec = pages.find((p) => p.stage === 'echec');
          return (
            <li key={tete.batch_id ?? tete.id} className="rounded-2xl border border-line px-4 py-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <strong>{tete.subjects?.label ?? 'Matière à définir'}</strong>
                  <small className="ml-2 text-muted">
                    {tete.children?.first_name ?? 'Enfant supprimé'} · {tete.kind} · {pages.length}{' '}
                    page{pages.length > 1 ? 's' : ''}
                    {tete.lang ? ' · ' + tete.lang.toUpperCase() : ''}
                  </small>
                </div>
                <Pill>{ETAPES[tete.stage] ?? tete.stage}</Pill>
              </div>
              <ol className="mt-2 grid gap-1 text-sm text-muted">
                {pages.map((p) => (
                  <li key={p.id}>
                    {p.page_no}. {p.original_name ?? 'sans nom'}
                  </li>
                ))}
              </ol>
              {enEchec?.stage_error ? (
                <p className="mt-2 text-sm font-semibold text-clay-dark">{enEchec.stage_error}</p>
              ) : null}
              {tete.stage === 'importe' || tete.stage === 'echec' ? (
                <BoutonLecture batchId={tete.batch_id} stage={tete.stage} />
              ) : null}
            </li>
          );
        })}
      </ul>

      <p className="mt-4 text-sm text-muted">
        La lecture appelle la fonction d’extraction : elle transcrit les pages, en tire un résumé
        et des notions, puis dépose le tout dans « À valider ». Rien n’atteint l’enfant avant
        votre relecture.
      </p>
    </Card>
  );
}

export default function ParentSpace() {
  const navigate = useNavigate();
  const { session } = useSession();
  const classes = useQuery({
    queryKey: ['classes'],
    queryFn: async () => {
      const { data, error } = await supabase.from('classes').select('*').order('rank');
      if (error) throw error;
      return data as ClassRow[];
    },
  });

  const children = useQuery({
    queryKey: ['children'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('id, first_name, avatar, class_id, school, classes(code, subsystem)')
        .order('created_at');
      if (error) throw error;
      return data as unknown as ChildWithClass[];
    },
  });

  return (
    <main className="ciel min-h-screen pb-16">
      <div className="mx-auto grid max-w-4xl gap-5 px-4 py-6 sm:px-6">
        {/* L'en-tête porte le lionceau en petit : c'est la même maison que
            l'espace enfant, vue depuis le bureau du parent. */}
        <header className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Mascotte taille={44} className="shrink-0" />
            <div>
              <Pill>Espace parent</Pill>
              <h1 className="mt-1.5 text-2xl font-black sm:text-3xl">Les cours de vos enfants</h1>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button
              variant="secondary"
              onClick={() => {
                // Quitter l'espace parent le referme : sinon le verrou ne
                // protegerait que la premiere visite de l'onglet.
                verrouiller();
                navigate('/');
              }}
            >
              Espace enfant
            </Button>
            <Button
              variant="ghost"
              onClick={() => {
                verrouiller();
                supabase.auth.signOut();
              }}
            >
              Se déconnecter
            </Button>
          </div>
        </header>

        {/* Trois blocs visibles, et le reste dans un tiroir. L'espace parent
            empilait huit sections de même poids : on y cherchait longtemps ce
            qu'on vient y faire presque chaque jour — voir où en sont les
            enfants, et ajouter le cours du soir. */}
        <Enfants
          classes={classes.data ?? []}
          enfants={children.data ?? []}
          chargement={children.isLoading}
          erreur={children.error}
        />

        <ImportCourse enfants={children.data ?? []} />
        <Validation />

        <details className="rounded-[var(--radius-card)] border border-line bg-white-warm/70 px-5 py-4 sm:px-6">
          <summary className="cursor-pointer list-none marker:content-['']">
            <span className="flex items-center justify-between gap-3">
              <span>
                <strong className="block text-lg font-extrabold">Réglages et outils</strong>
                <span className="mt-0.5 block text-sm text-muted">
                  Documents importés, rappels du soir, bibliothèque, illustrations, code d’accès.
                </span>
              </span>
              <span aria-hidden="true" className="shrink-0 text-xl text-clay">
                <span className="group-open:hidden">+</span>
              </span>
            </span>
          </summary>

          <div className="mt-5 grid gap-5">
            <Documents />
            {session?.user.id ? (
              <Rappels parentId={session.user.id} enfants={children.data ?? []} />
            ) : null}
            <Library />
            <Illustrations />
            <PinSetup />
          </div>
        </details>

      </div>
    </main>
  );
}
