import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { Button, Card, ErrorNote, Field, Loading, Pill } from '../../components/ui';
import type { ClassRow } from '../../types/db';

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

export default function ParentSpace() {
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
          <Link to="/">
            <Button variant="secondary">Espace enfant</Button>
          </Link>
          <Button variant="ghost" onClick={() => supabase.auth.signOut()}>
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
      <Library />
      <PinSetup />
    </main>
  );
}
