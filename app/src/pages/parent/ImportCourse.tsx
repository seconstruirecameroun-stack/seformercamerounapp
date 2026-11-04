import { useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { importerCours, TAILLE_MAX, TYPES_ACCEPTES } from '../../lib/import';
import type { FichierRefuse } from '../../lib/import';
import { Button, Card, ErrorNote, Pill } from '../../components/ui';

type ChildOption = { id: string; first_name: string };

/**
 * Un enfant, des photos, un bouton.
 *
 * La version précédente demandait aussi la matière, le jour et le type de
 * document — quatre champs avant d'avoir le droit d'envoyer. Trois d'entre
 * eux sont écrits sur la page que le parent vient de photographier : les
 * demander, c'est faire recopier à la main ce que la lecture sait lire.
 *
 * L'envoi enchaîne donc tout seul :
 *   1. le dépôt des pages,
 *   2. la lecture, qui découpe en leçons et devine matière, jour et titre,
 *   3. l'écriture des questions, leçon par leçon.
 *
 * Ce qui en sort n'est pas publié : tout attend dans « À valider », où le
 * parent voit la photo à côté du texte. Le choix de rendre l'import simple
 * ne déplace pas le contrôle, il le met au seul endroit où il sert — devant
 * le résultat, pas devant un formulaire vide.
 */
export default function ImportCourse({ enfants }: { enfants: ChildOption[] }) {
  const qc = useQueryClient();
  const inputRef = useRef<HTMLInputElement>(null);
  const [childId, setChildId] = useState(enfants.length === 1 ? enfants[0].id : '');
  const [fichiers, setFichiers] = useState<File[]>([]);
  const [avancement, setAvancement] = useState<string | null>(null);
  const [refuses, setRefuses] = useState<FichierRefuse[]>([]);

  type Bilan = {
    lecons: Array<{ titre: string; notions: number; questions: number }>;
    avertissements: string[];
  };
  const [bilan, setBilan] = useState<Bilan | null>(null);

  const envoi = useMutation({
    mutationFn: async (): Promise<Bilan> => {
      const { data: auth } = await supabase.auth.getUser();
      const parentId = auth.user?.id;
      if (!parentId) throw new Error('Session expirée, reconnectez-vous.');

      // « Failed to fetch » ne dit rien au parent : la même phrase sort d'un
      // réseau coupé, d'un envoi trop lourd ou d'une fonction tombée. On dit
      // au moins QUELLE étape a lâché — c'est ce qui manquait au premier
      // essai depuis un téléphone.
      const etape = async <T,>(quoi: string, f: () => Promise<T>): Promise<T> => {
        try {
          return await f();
        } catch (e) {
          const m = e instanceof Error ? e.message : String(e);
          throw new Error(
            /fetch|network|réseau/i.test(m)
              ? `${quoi} : la connexion a été coupée. Réessayez, les pages déjà envoyées ne sont pas perdues.`
              : `${quoi} : ${m}`,
          );
        }
      };

      const depot = await etape('Envoi des pages', () =>
        importerCours({
          parentId,
          childId,
          subjectId: null,
          taughtOn: null,
          kind: 'cours',
          fichiers,
          onProgress: (fait, total, phase) =>
            setAvancement(
              phase === 'reduction'
                ? `Préparation de la page ${fait} sur ${total}…`
                : `Envoi de la page ${fait} sur ${total}…`,
            ),
        }),
      );
      setRefuses(depot.refuses);

      setAvancement('Lecture du cahier…');
      const lu = await etape('Lecture du cahier', () =>
        supabase.functions.invoke('analyze-document', { body: { batch_id: depot.batchId } }),
      );
      if (lu.error) throw lu.error;
      const lecture = lu.data as {
        lecons: Array<{ id: string; titre: string; notions: number }>;
        avertissements?: string[];
      };

      const avertissements = [...(lecture.avertissements ?? [])];
      const lecons: Bilan['lecons'] = [];

      // Une leçon à la fois : un appel court aboutit, et une panne au milieu
      // ne perd que la leçon en cours.
      for (let i = 0; i < lecture.lecons.length; i++) {
        const L = lecture.lecons[i];
        setAvancement(
          `Questions de « ${L.titre} » (${i + 1} sur ${lecture.lecons.length})…`,
        );
        const q = await supabase.functions.invoke('write-questions', {
          body: { lesson_id: L.id },
        });
        if (q.error) {
          avertissements.push(`« ${L.titre} » : questions non écrites (${q.error.message}).`);
          lecons.push({ titre: L.titre, notions: L.notions, questions: 0 });
          continue;
        }
        const res = q.data as { questions: number; notions: number; avertissements?: string[] };
        avertissements.push(...(res.avertissements ?? []));
        lecons.push({ titre: L.titre, notions: res.notions, questions: res.questions });
      }

      return { lecons, avertissements };
    },
    onSuccess: (res) => {
      setFichiers([]);
      setAvancement(null);
      setBilan(res);
      if (inputRef.current) inputRef.current.value = '';
      qc.invalidateQueries({ queryKey: ['documents'] });
      qc.invalidateQueries({ queryKey: ['validation'] });
      qc.invalidateQueries({ queryKey: ['subjects'] });
    },
    onError: () => setAvancement(null),
  });

  function submit(event: FormEvent) {
    event.preventDefault();
    setBilan(null);
    setRefuses([]);
    envoi.mutate();
  }

  const total = fichiers.reduce((n, f) => n + f.size, 0);
  const pret = childId !== '' && fichiers.length > 0 && !envoi.isPending;

  return (
    <Card
      titre="Envoyer un cours"
      sous="Choisissez l’enfant et photographiez les pages. La matière, le jour et le découpage en leçons sont lus sur le cahier."
      actions={<Pill>photos ou PDF</Pill>}
    >
      <form onSubmit={submit} className="grid gap-4">
        <label className="block">
          <span className="mb-1.5 block text-sm font-bold">Pour qui ?</span>
          <select
            value={childId}
            onChange={(e) => setChildId(e.target.value)}
            className="w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink outline-none transition focus:border-clay"
          >
            <option value="">Choisir l’enfant</option>
            {enfants.map((e) => (
              <option key={e.id} value={e.id}>
                {e.first_name}
              </option>
            ))}
          </select>
        </label>

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
              {fichiers.length === 0
                ? 'plusieurs jours à la fois, ce n’est pas grave'
                : 'Toucher pour en choisir d’autres'}
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
            {/* Le poids affiché est celui des photos telles qu'elles sortent du
                téléphone. Sans cette ligne, 38,8 Mo sur une connexion mobile
                font renoncer avant d'avoir essayé. */}
            <li className="text-sm text-muted">
              Réduites avant l’envoi : environ{' '}
              {Math.max(0.1, total / 1024 / 1024 / 7).toFixed(1)} Mo partiront réellement.
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
            {envoi.isPending ? (avancement ?? 'Envoi…') : 'Envoyer'}
          </Button>
          {envoi.isPending ? (
            <span className="text-sm text-muted">
              La lecture prend une à deux minutes. Ne fermez pas la page.
            </span>
          ) : null}
        </div>

        {bilan ? (
          <div className="grid gap-2 rounded-2xl border-2 border-leaf/40 bg-leaf/10 px-4 py-3">
            <strong className="text-base">
              {bilan.lecons.length} leçon{bilan.lecons.length > 1 ? 's' : ''} à relire
            </strong>
            <ul className="grid gap-1 text-sm text-ink-2">
              {bilan.lecons.map((l, i) => (
                <li key={i}>
                  <strong>{l.titre}</strong> — {l.notions} notion{l.notions > 1 ? 's' : ''},{' '}
                  {l.questions} question{l.questions > 1 ? 's' : ''}
                </li>
              ))}
            </ul>
            <span className="text-sm text-muted">
              Rien n’est publié : tout vous attend dans « À valider ».
            </span>
            {bilan.avertissements.length > 0 ? (
              <ul className="mt-1 grid gap-1 rounded-xl bg-gold/25 px-3 py-2 text-sm">
                {bilan.avertissements.map((a, i) => (
                  <li key={i}>⚠ {a}</li>
                ))}
              </ul>
            ) : null}
          </div>
        ) : null}
      </form>
    </Card>
  );
}
