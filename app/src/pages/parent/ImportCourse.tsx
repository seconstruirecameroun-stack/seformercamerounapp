import { useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { importerCours, matiereDeClasse, TAILLE_MAX, TYPES_ACCEPTES } from '../../lib/import';
import type { FichierRefuse } from '../../lib/import';
import { Button, Card, ErrorNote, Pill } from '../../components/ui';

type ChildOption = { id: string; first_name: string };

export default function ImportCourse({ enfants }: { enfants: ChildOption[] }) {
  const qc = useQueryClient();
  const inputRef = useRef<HTMLInputElement>(null);
  const [childId, setChildId] = useState('');
  const [matiere, setMatiere] = useState('');
  /** L'intitulé saisi quand la matière du cahier n'est pas au tableau. */
  const [nouvelle, setNouvelle] = useState('');
  /** Le jour écrit en haut de la page. Vide tant que le parent ne l'a pas lu. */
  const [date, setDate] = useState('');
  const [kind, setKind] = useState<'cours' | 'devoir' | 'autre'>('cours');
  const [fichiers, setFichiers] = useState<File[]>([]);
  const [avancement, setAvancement] = useState<string | null>(null);
  const [refuses, setRefuses] = useState<FichierRefuse[]>([]);

  // La classe de l'enfant commande les matières proposées. Sans ce filtre,
  // l'import inventait sa matière à chaque cahier — six en une seule fois,
  // dont deux qui n'existaient pas au tableau de l'école.
  const classe = useQuery({
    queryKey: ['classe-enfant', childId],
    enabled: childId !== '',
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('class_id')
        .eq('id', childId)
        .single();
      if (error) throw error;
      return (data as { class_id: string | null }).class_id;
    },
  });

  const matieres = useQuery({
    queryKey: ['subjects', classe.data],
    enabled: Boolean(classe.data),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('subjects')
        .select('id, label, official_fr')
        .eq('class_id', classe.data!)
        .order('label');
      if (error) throw error;
      return data as Array<{ id: string; label: string; official_fr: string | null }>;
    },
  });

  /**
   * Les matières du jour, d'après l'emploi du temps.
   *
   * Un parent photographie le cahier le soir même : les trois ou quatre
   * matières de la journée couvrent presque toujours ce qu'il envoie, et
   * elles lui évitent de parcourir seize lignes.
   */
  const duJour = useQuery({
    queryKey: ['matieres-du-jour', classe.data],
    enabled: Boolean(classe.data),
    queryFn: async () => {
      const jour = new Date().getDay();
      if (jour < 1 || jour > 5) return [] as string[];
      const { data, error } = await supabase
        .from('timetable_slots')
        .select('subject_id, debut')
        .eq('class_id', classe.data!)
        .eq('day', jour)
        .eq('kind', 'cours')
        .order('debut');
      if (error) throw error;
      const vus = new Set<string>();
      for (const c of (data ?? []) as Array<{ subject_id: string | null }>) {
        if (c.subject_id) vus.add(c.subject_id);
      }
      return [...vus];
    },
  });

  const envoi = useMutation({
    mutationFn: async () => {
      const { data: auth } = await supabase.auth.getUser();
      const parentId = auth.user?.id;
      if (!parentId) throw new Error('Session expirée, reconnectez-vous.');
      // « Une autre matière » : on l'ajoute au catalogue de la classe, pour
      // qu'elle soit proposée au prochain import.
      let subjectId: string | null = matiere || null;
      if (matiere === 'autre') {
        if (!classe.data) throw new Error('Classe de l’enfant inconnue.');
        if (!nouvelle.trim()) throw new Error('Donnez l’intitulé de la matière.');
        subjectId = await matiereDeClasse(parentId, classe.data, nouvelle);
      }

      return importerCours({
        parentId,
        childId,
        subjectId,
        taughtOn: date || null,
        kind,
        fichiers,
        onProgress: (fait, total) => setAvancement(`Envoi ${fait} / ${total}`),
      });
    },
    onSuccess: (res) => {
      setFichiers([]);
      setNouvelle('');
      setDate('');
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
    <Card
      titre="Importer un cours"
      sous="Photographiez chaque page du cahier. Plusieurs photos envoyées ensemble forment un seul cours, dans l’ordre où vous les choisissez."
      actions={<Pill>photos ou PDF</Pill>}
    >
      <form onSubmit={submit} className="grid gap-4">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <label className="block">
            <span className="mb-1.5 block text-sm font-bold">
              Pour quel enfant
            </span>
            <select
              className="w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink outline-none transition focus:border-clay"
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

          <label className="block">
            <span className="mb-1.5 block text-sm font-bold">
              Matière
            </span>
            <select
              className="w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink outline-none transition focus:border-clay disabled:opacity-50"
              value={matiere}
              onChange={(e) => setMatiere(e.target.value)}
              disabled={!classe.data}
            >
              <option value="">{classe.data ? 'Choisir…' : 'Choisissez l’enfant d’abord'}</option>
              {(matieres.data ?? []).map((m) => (
                <option key={m.id} value={m.id}>
                  {m.label}
                </option>
              ))}
              {/* L'emploi du temps ne dit pas tout : le cahier de KLEIN porte
                  une « éducation à la paix » qui n'y figure pas. La liste
                  guide, elle n'enferme pas. */}
              <option value="autre">Une autre matière…</option>
            </select>
            {matiere === 'autre' ? (
              <input
                className="mt-2 w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink outline-none transition focus:border-clay"
                value={nouvelle}
                onChange={(e) => setNouvelle(e.target.value)}
                placeholder="Intitulé du cahier"
                autoFocus
              />
            ) : null}
            <span className="mt-1 block text-sm text-muted">
              {matiere === 'autre'
                ? 'Elle sera ajoutée aux matières de cette classe.'
                : 'Les matières de la classe, telles que l’école les nomme.'}
            </span>
          </label>

          <label className="block">
            <span className="mb-1.5 block text-sm font-bold">
              Date du cours
            </span>
            <input
              type="date"
              className="w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink outline-none transition focus:border-clay"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              max={new Date().toISOString().slice(0, 10)}
            />
            <span className="mt-1 block text-sm text-muted">
              Celle du cahier. Laissez vide si la page n’en porte pas.
            </span>
          </label>

          <label className="block">
            <span className="mb-1.5 block text-sm font-bold">
              Type
            </span>
            <select
              className="w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink outline-none transition focus:border-clay"
              value={kind}
              onChange={(e) => setKind(e.target.value as 'cours' | 'devoir' | 'autre')}
            >
              <option value="cours">Cours</option>
              <option value="devoir">Devoir</option>
              <option value="autre">Autre</option>
            </select>
          </label>
        </div>

        {(duJour.data ?? []).length > 0 ? (
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-bold text-muted">
              Au programme aujourd’hui
            </span>
            {(duJour.data ?? []).map((id) => {
              const m = (matieres.data ?? []).find((x) => x.id === id);
              if (!m) return null;
              return (
                <button
                  key={id}
                  type="button"
                  onClick={() => setMatiere(id)}
                  className={
                    'rounded-full border px-3 py-1.5 text-sm font-semibold transition-colors ' +
                    (matiere === id
                      ? 'border-ink bg-ink text-white-warm'
                      : 'border-line bg-white-warm text-ink-2 hover:border-ink-2')
                  }
                >
                  {m.label}
                </button>
              );
            })}
          </div>
        ) : null}

        {/* Le sélecteur natif annonce « Aucun fichier choisi » dans la langue
            du navigateur, au milieu d'une interface qui ne ressemble à rien de
            tel. On le cache, et la zone dit elle-même ce qu'elle attend. */}
        <label className="block">
          <span className="mb-1.5 block text-sm font-bold">Les pages du cahier</span>
          <span className="tuile flex cursor-pointer flex-col items-center gap-1 rounded-2xl border-2 border-dashed border-line bg-white-warm px-4 py-6 text-center">
            <strong className="text-base">
              {fichiers.length === 0
                ? 'Choisir les photos'
                : `${fichiers.length} page${fichiers.length > 1 ? 's' : ''} choisie${fichiers.length > 1 ? 's' : ''}`}
            </strong>
            <span className="text-sm text-muted">
              {fichiers.length === 0 ? 'ou le PDF du cours' : 'Toucher pour en choisir d’autres'}
            </span>
            <input
              ref={inputRef}
              type="file"
              multiple
              accept={TYPES_ACCEPTES.join(',')}
              onChange={(e) => setFichiers([...(e.target.files ?? [])])}
              className="sr-only"
            />
          </span>
          <span className="mt-1 block text-sm text-muted">
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
            <li className="mt-1 text-sm text-muted">
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
