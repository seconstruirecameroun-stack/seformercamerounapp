import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { Button, Card, ErrorNote, Field, Loading, Pill } from '../../components/ui';
import ImportCourse from './ImportCourse';
import Validation from './Validation';
import { verrouiller } from '../../components/PinGate';
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
  classes: { code: string; subsystem: string } | null;
};

function AddChild({ classes }: { classes: ClassRow[] }) {
  const qc = useQueryClient();
  const [firstName, setFirstName] = useState('');
  const [classId, setClassId] = useState('');
  const [avatar, setAvatar] = useState('');

  const add = useMutation({
    mutationFn: async () => {
      const { data: auth } = await supabase.auth.getUser();
      const parentId = auth.user?.id;
      if (!parentId) throw new Error('Session expirée, reconnectez-vous.');
      const { error } = await supabase.from('children').insert({
        parent_id: parentId,
        first_name: firstName.trim(),
        class_id: classId || null,
        avatar: avatar.trim() || null,
      });
      if (error) throw error;
    },
    onSuccess: () => {
      setFirstName('');
      setClassId('');
      setAvatar('');
      qc.invalidateQueries({ queryKey: ['children'] });
    },
  });

  function submit(event: FormEvent) {
    event.preventDefault();
    add.mutate();
  }

  const francophone = classes.filter((c) => c.subsystem === 'francophone');
  const anglophone = classes.filter((c) => c.subsystem === 'anglophone');

  return (
    <Card>
      <h2 className="text-xl font-bold">Ajouter un enfant</h2>
      <form onSubmit={submit} className="mt-4 grid gap-4 sm:grid-cols-3">
        <Field
          label="Prénom"
          required
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
        />
        <label className="block">
          <span className="mb-1 block text-xs font-bold tracking-wide text-muted uppercase">
            Classe
          </span>
          <select
            className="w-full rounded-2xl border border-line bg-white-warm px-4 py-3 text-ink outline-none focus:border-ink-2"
            value={classId}
            onChange={(e) => setClassId(e.target.value)}
          >
            <option value="">À définir</option>
            <optgroup label="Francophone">
              {francophone.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.code}
                </option>
              ))}
            </optgroup>
            <optgroup label="Anglophone">
              {anglophone.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.code}
                </option>
              ))}
            </optgroup>
          </select>
        </label>
        <Field
          label="Avatar"
          value={avatar}
          onChange={(e) => setAvatar(e.target.value)}
          hint="Un emoji, par exemple 🦁"
          maxLength={4}
        />
        <div className="sm:col-span-3">
          {add.error ? <ErrorNote error={add.error} /> : null}
          <Button type="submit" disabled={add.isPending || firstName.trim().length === 0}>
            {add.isPending ? 'Enregistrement…' : 'Ajouter'}
          </Button>
        </div>
      </form>
    </Card>
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
    <Card>
      <h2 className="text-xl font-bold">Code de l’espace parent</h2>
      <p className="mt-2 text-sm text-muted">
        {isSet.data
          ? 'Un code est défini. Vous pouvez le remplacer ci-dessous.'
          : 'Aucun code pour l’instant : l’espace parent est accessible à tous sur cet appareil.'}
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
    <Card>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-bold">Bibliothèque</h2>
        <Button variant="secondary" onClick={() => seed.mutate()} disabled={seed.isPending}>
          {seed.isPending ? 'Chargement…' : 'Charger la leçon de démonstration'}
        </Button>
      </div>

      {seed.error ? <div className="mt-3"><ErrorNote error={seed.error} /></div> : null}

      {lessons.isLoading ? <Loading /> : null}
      {lessons.error ? <ErrorNote error={lessons.error} /> : null}

      <ul className="mt-4 grid gap-3">
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
        <p className="mt-4 text-sm text-muted">
          Aucune leçon. L’import de cours arrive au lot 1 ; en attendant, chargez la leçon de
          démonstration.
        </p>
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
    <Card>
      <h2 className="text-xl font-bold">Documents importés</h2>
      {docs.isLoading ? <Loading /> : null}
      {docs.error ? <ErrorNote error={docs.error} /> : null}

      {envois.size === 0 && !docs.isLoading ? (
        <p className="mt-3 text-sm text-muted">
          Rien d’importé pour l’instant. Les photos envoyées apparaîtront ici avec leur état
          d’avancement.
        </p>
      ) : null}

      <ul className="mt-4 grid gap-3">
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
              <ol className="mt-2 grid gap-1 text-xs text-muted">
                {pages.map((p) => (
                  <li key={p.id}>
                    {p.page_no}. {p.original_name ?? 'sans nom'}
                  </li>
                ))}
              </ol>
              {enEchec?.stage_error ? (
                <p className="mt-2 text-xs text-clay-dark">{enEchec.stage_error}</p>
              ) : null}
              {tete.stage === 'importe' || tete.stage === 'echec' ? (
                <BoutonLecture batchId={tete.batch_id} stage={tete.stage} />
              ) : null}
            </li>
          );
        })}
      </ul>

      <p className="mt-4 text-xs text-muted">
        La lecture appelle la fonction d’extraction : elle transcrit les pages, en tire un résumé
        et des notions, puis dépose le tout dans « À valider ». Rien n’atteint l’enfant avant
        votre relecture.
      </p>
    </Card>
  );
}

export default function ParentSpace() {
  const navigate = useNavigate();
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
        .select('id, first_name, avatar, class_id, classes(code, subsystem)')
        .order('created_at');
      if (error) throw error;
      return data as unknown as ChildWithClass[];
    },
  });

  return (
    <main className="mx-auto grid max-w-4xl gap-6 p-6">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <Pill>Espace parent</Pill>
          <h1 className="mt-2 text-3xl font-black">Mes enfants et leurs cours</h1>
        </div>
        <div className="flex gap-2">
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

      <Card>
        <h2 className="text-xl font-bold">Profils</h2>
        {children.isLoading ? <Loading /> : null}
        {children.error ? <ErrorNote error={children.error} /> : null}
        <ul className="mt-4 grid gap-3 sm:grid-cols-2">
          {(children.data ?? []).map((child) => (
            <li
              key={child.id}
              className="flex items-center gap-3 rounded-2xl border border-line px-4 py-3"
            >
              <span className="grid h-10 w-10 place-items-center rounded-full bg-gold/30">
                {child.avatar ?? child.first_name.slice(0, 1).toUpperCase()}
              </span>
              <div>
                <strong>{child.first_name}</strong>
                <small className="block text-muted">
                  {child.classes ? child.classes.code : 'Classe à définir'}
                </small>
              </div>
            </li>
          ))}
        </ul>
        {children.data && children.data.length === 0 ? (
          <p className="mt-4 text-sm text-muted">Aucun profil enregistré.</p>
        ) : null}
      </Card>

      {classes.data ? <AddChild classes={classes.data} /> : null}
      <ImportCourse enfants={children.data ?? []} />
      <Documents />
      <Validation />
      <Library />
      <PinSetup />
    </main>
  );
}
