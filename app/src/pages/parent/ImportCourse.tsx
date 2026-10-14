import { useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { importerCours, TAILLE_MAX, TYPES_ACCEPTES } from '../../lib/import';
import type { FichierRefuse } from '../../lib/import';
import { Button, Card, ErrorNote, Field, Pill } from '../../components/ui';

type ChildOption = { id: string; first_name: string };

export default function ImportCourse({ enfants }: { enfants: ChildOption[] }) {
  const qc = useQueryClient();
  const inputRef = useRef<HTMLInputElement>(null);
  const [childId, setChildId] = useState('');
  const [matiere, setMatiere] = useState('');
  const [kind, setKind] = useState<'cours' | 'devoir' | 'autre'>('cours');
  const [fichiers, setFichiers] = useState<File[]>([]);
  const [avancement, setAvancement] = useState<string | null>(null);
  const [refuses, setRefuses] = useState<FichierRefuse[]>([]);

  const matieres = useQuery({
    queryKey: ['subjects'],
    queryFn: async () => {
      const { data, error } = await supabase.from('subjects').select('id, label').order('label');
      if (error) throw error;
      return data as Array<{ id: string; label: string }>;
    },
  });

  const envoi = useMutation({
    mutationFn: async () => {
      const { data: auth } = await supabase.auth.getUser();
      const parentId = auth.user?.id;
      if (!parentId) throw new Error('Session expirée, reconnectez-vous.');
      return importerCours({
        parentId,
        childId,
        subjectLabel: matiere,
        kind,
        fichiers,
        onProgress: (fait, total) => setAvancement(`Envoi ${fait} / ${total}`),
      });
    },
    onSuccess: (res) => {
      setFichiers([]);
      setAvancement(null);
      setRefuses(res.refuses);
      if (inputRef.current) inputRef.current.value = '';
      qc.invalidateQueries({ queryKey: ['documents'] });
      qc.invalidateQueries({ queryKey: ['subjects'] });
    },
    onError: () => setAvancement(null),
  });

  function submit(event: FormEvent) {
    event.preventDefault();
    envoi.mutate();
  }

  const total = fichiers.reduce((n, f) => n + f.size, 0);
  const pret = childId !== '' && fichiers.length > 0 && !envoi.isPending;

  return (
    <Card>
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-xl font-bold">Importer un cours</h2>
        <Pill>photos ou PDF</Pill>
      </div>
      <p className="mt-2 text-sm text-muted">
        Photographiez chaque page du cahier. Plusieurs photos envoyées ensemble forment un seul
        cours, dans l’ordre où vous les choisissez.
      </p>

      <form onSubmit={submit} className="mt-4 grid gap-4">
        <div className="grid gap-4 sm:grid-cols-3">
          <label className="block">
            <span className="mb-1 block text-xs font-bold tracking-wide text-muted uppercase">
              Pour quel enfant
            </span>
            <select
              className="w-full rounded-2xl border border-line bg-white-warm px-4 py-3 text-ink outline-none focus:border-ink-2"
              value={childId}
              onChange={(e) => setChildId(e.target.value)}
              required
            >
              <option value="">Choisir…</option>
              {enfants.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.first_name}
                </option>
              ))}
            </select>
          </label>

          <div>
            <Field
              label="Matière"
              list="liste-matieres"
              value={matiere}
              onChange={(e) => setMatiere(e.target.value)}
              placeholder="Histoire, Science, ECM…"
              hint="L’intitulé de l’école. Créé s’il n’existe pas."
            />
            <datalist id="liste-matieres">
              {(matieres.data ?? []).map((m) => (
                <option key={m.id} value={m.label} />
              ))}
            </datalist>
          </div>

          <label className="block">
            <span className="mb-1 block text-xs font-bold tracking-wide text-muted uppercase">
              Type
            </span>
            <select
              className="w-full rounded-2xl border border-line bg-white-warm px-4 py-3 text-ink outline-none focus:border-ink-2"
              value={kind}
              onChange={(e) => setKind(e.target.value as 'cours' | 'devoir' | 'autre')}
            >
              <option value="cours">Cours</option>
              <option value="devoir">Devoir</option>
              <option value="autre">Autre</option>
            </select>
          </label>
        </div>

        <label className="block">
          <span className="mb-1 block text-xs font-bold tracking-wide text-muted uppercase">
            Fichiers
          </span>
          <input
            ref={inputRef}
            type="file"
            multiple
            accept={TYPES_ACCEPTES.join(',')}
            onChange={(e) => setFichiers([...(e.target.files ?? [])])}
            className="w-full rounded-2xl border border-dashed border-line bg-white-warm px-4 py-6 text-sm"
          />
          <span className="mt-1 block text-xs text-muted">
            JPEG, PNG, WebP, HEIC ou PDF · 20 Mo maximum par fichier
          </span>
        </label>

        {fichiers.length > 0 ? (
          <ul className="grid gap-1 text-sm">
            {fichiers.map((f, i) => (
              <li key={f.name + i} className="flex justify-between gap-3 text-ink-2">
                <span>
                  {i + 1}. {f.name}
                </span>
                <span className={f.size > TAILLE_MAX ? 'text-clay-dark' : 'text-muted'}>
                  {(f.size / 1024 / 1024).toFixed(1)} Mo
                </span>
              </li>
            ))}
            <li className="mt-1 text-xs text-muted">
              {fichiers.length} fichier{fichiers.length > 1 ? 's' : ''} ·{' '}
              {(total / 1024 / 1024).toFixed(1)} Mo au total
            </li>
          </ul>
        ) : null}

        {envoi.error ? <ErrorNote error={envoi.error} /> : null}
        {refuses.length > 0 ? (
          <ul className="rounded-2xl bg-gold/20 px-4 py-3 text-sm">
            {refuses.map((r) => (
              <li key={r.nom}>
                <strong>{r.nom}</strong> écarté : {r.raison}
              </li>
            ))}
          </ul>
        ) : null}

        <div className="flex items-center gap-3">
          <Button type="submit" disabled={!pret}>
            {envoi.isPending ? (avancement ?? 'Envoi…') : 'Importer'}
          </Button>
          {envoi.isSuccess && refuses.length === 0 ? (
            <span className="text-sm text-leaf">Import enregistré.</span>
          ) : null}
        </div>
      </form>
    </Card>
  );
}
