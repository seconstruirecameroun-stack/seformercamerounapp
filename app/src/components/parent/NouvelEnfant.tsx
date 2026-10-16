import { useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { Button, ErrorNote, Field } from '../ui';
import ChoixEmoji from './ChoixEmoji';
import type { ClassRow } from '../../types/db';

/**
 * L'ajout d'un enfant, en quatre temps.
 *
 * C'était un formulaire de trois champs en ligne : prénom, classe, emoji. On
 * y ajoutait un enfant sans savoir qu'on venait de décider de son programme,
 * et sans jamais renseigner ce qui servira plus tard.
 *
 * Quatre écrans courts valent mieux qu'un long : chacun pose une question à
 * la fois, on voit où l'on en est, et on peut revenir. C'est la même règle
 * que pour l'enfant — une chose à la fois.
 *
 * Tout est facultatif sauf le prénom et la classe. Un parent pressé passe en
 * trois touches ; celui qui a le bulletin sous la main remplit le reste une
 * fois pour toutes.
 */

const ETAPES = ['L’enfant', 'Son école', 'Son emploi du temps', 'C’est prêt'];

/** L'âge, en années révolues. */
function age(naissance: string): number | null {
  if (!naissance) return null;
  const n = new Date(naissance);
  if (Number.isNaN(n.getTime())) return null;
  const aujourdhui = new Date();
  let ans = aujourdhui.getFullYear() - n.getFullYear();
  const mois = aujourdhui.getMonth() - n.getMonth();
  if (mois < 0 || (mois === 0 && aujourdhui.getDate() < n.getDate())) ans -= 1;
  return ans >= 0 && ans < 30 ? ans : null;
}

export default function NouvelEnfant({
  classes,
  ecoleConnue,
  onFini,
}: {
  classes: ClassRow[];
  /** L'école des enfants déjà enregistrés : presque toujours la même. */
  ecoleConnue: string | null;
  onFini: () => void;
}) {
  const qc = useQueryClient();
  const [etape, setEtape] = useState(0);

  const [prenom, setPrenom] = useState('');
  const [emoji, setEmoji] = useState('🦁');
  const [naissance, setNaissance] = useState('');
  const [genre, setGenre] = useState<'fille' | 'garcon' | ''>('');
  const [ecole, setEcole] = useState(ecoleConnue ?? '');
  const [sousSysteme, setSousSysteme] = useState<'francophone' | 'anglophone'>('francophone');
  const [classId, setClassId] = useState('');

  const niveaux = useMemo(
    () => classes.filter((c) => c.subsystem === sousSysteme).sort((a, b) => a.rank - b.rank),
    [classes, sousSysteme],
  );
  const classeChoisie = classes.find((c) => c.id === classId) ?? null;

  // Ce que l'app sait déjà de cette classe : les matières relevées sur un
  // emploi du temps, et les créneaux. S'ils existent, le nouvel enfant en
  // hérite sans rien faire.
  const dejaConnu = useQuery({
    queryKey: ['classe-connue', classId],
    enabled: Boolean(classId),
    queryFn: async () => {
      const [matieres, creneaux] = await Promise.all([
        supabase.from('subjects').select('label').eq('class_id', classId),
        supabase.from('timetable_slots').select('id', { count: 'exact', head: true }).eq('class_id', classId),
      ]);
      if (matieres.error) throw matieres.error;
      return {
        matieres: (matieres.data ?? []).map((m) => m.label as string),
        creneaux: creneaux.count ?? 0,
      };
    },
  });

  const creer = useMutation({
    mutationFn: async () => {
      const { data: auth } = await supabase.auth.getUser();
      const parentId = auth.user?.id;
      if (!parentId) throw new Error('Session expirée, reconnectez-vous.');
      const { error } = await supabase.from('children').insert({
        parent_id: parentId,
        first_name: prenom.trim(),
        avatar: emoji,
        class_id: classId || null,
        birth_date: naissance || null,
        sex: genre || null,
        school: ecole.trim() || null,
      });
      if (error) throw error;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['children'] });
      onFini();
    },
  });

  const peutAvancer = [prenom.trim().length > 0, classId !== '', true, true][etape];
  const ans = age(naissance);

  const bouton =
    'tuile rounded-2xl border-2 px-4 py-3 text-base font-bold transition ';
  const choisi = 'border-clay bg-gold/25';
  const libre = 'border-line bg-white-warm hover:border-ink-2';

  return (
    <div className="rounded-[var(--radius-card)] border-2 border-clay/30 bg-white-warm p-5 sm:p-6">
      {/* Où l'on en est : quatre galets, comme dans la salle de jeu. */}
      <ol className="flex items-center gap-2" aria-label="Étapes">
        {ETAPES.map((nom, i) => (
          <li key={nom} className="flex flex-1 items-center gap-2">
            <span
              className={
                'grid h-8 w-8 shrink-0 place-items-center rounded-full text-sm font-black transition ' +
                (i < etape
                  ? 'bg-leaf text-white-warm'
                  : i === etape
                    ? 'bg-clay text-white-warm'
                    : 'bg-line text-muted')
              }
            >
              {i < etape ? '✓' : i + 1}
            </span>
            {i < ETAPES.length - 1 ? (
              <span className={'h-0.5 flex-1 ' + (i < etape ? 'bg-leaf' : 'bg-line')} />
            ) : null}
          </li>
        ))}
      </ol>
      <h3 className="mt-4 text-lg font-extrabold">{ETAPES[etape]}</h3>

      {/* ───────── 1. L'enfant ───────── */}
      {etape === 0 ? (
        <div className="mt-4 grid gap-5">
          <Field
            label="Son prénom"
            required
            autoFocus
            value={prenom}
            onChange={(e) => setPrenom(e.target.value)}
          />

          <div>
            <p className="mb-2 text-sm font-bold">Son emoji</p>
            <ChoixEmoji valeur={emoji} onChange={setEmoji} />
          </div>

          <div>
            <Field
              label="Sa date de naissance"
              type="date"
              value={naissance}
              onChange={(e) => setNaissance(e.target.value)}
              hint={ans !== null ? `${ans} ans` : 'Facultative.'}
            />
          </div>

          <div>
            <p className="mb-2 text-sm font-bold">
              Fille ou garçon <span className="font-normal text-muted">· facultatif</span>
            </p>
            <div className="flex flex-wrap gap-2">
              {(
                [
                  ['fille', 'Une fille'],
                  ['garcon', 'Un garçon'],
                ] as const
              ).map(([valeur, libelle]) => (
                <button
                  key={valeur}
                  type="button"
                  aria-pressed={genre === valeur}
                  onClick={() => setGenre(genre === valeur ? '' : valeur)}
                  className={bouton + (genre === valeur ? choisi : libre)}
                >
                  {libelle}
                </button>
              ))}
            </div>
            <p className="mt-1 text-sm text-muted">
              Sert aux accords : « tu es prêt » ou « tu es prête ».
            </p>
          </div>
        </div>
      ) : null}

      {/* ───────── 2. L'école ───────── */}
      {etape === 1 ? (
        <div className="mt-4 grid gap-5">
          <Field
            label="Son école"
            value={ecole}
            onChange={(e) => setEcole(e.target.value)}
            placeholder="New Century Bilingual School"
            hint={
              ecoleConnue
                ? 'Reprise de vos autres enfants. Modifiez-la si ce n’est pas la même.'
                : 'Facultative.'
            }
          />

          <div>
            <p className="mb-2 text-sm font-bold">Sous-système</p>
            <div className="flex flex-wrap gap-2">
              {(
                [
                  ['francophone', 'Francophone'],
                  ['anglophone', 'Anglophone'],
                ] as const
              ).map(([valeur, libelle]) => (
                <button
                  key={valeur}
                  type="button"
                  aria-pressed={sousSysteme === valeur}
                  onClick={() => {
                    setSousSysteme(valeur);
                    setClassId('');
                  }}
                  className={bouton + (sousSysteme === valeur ? choisi : libre)}
                >
                  {libelle}
                </button>
              ))}
            </div>
          </div>

          <div>
            <p className="mb-2 text-sm font-bold">Sa classe</p>
            {/* Des pastilles plutôt qu'une liste déroulante : six niveaux se
                montrent d'un coup, et se touchent du pouce. */}
            <div className="flex flex-wrap gap-2">
              {niveaux.map((c) => (
                <button
                  key={c.id}
                  type="button"
                  aria-pressed={classId === c.id}
                  onClick={() => setClassId(c.id)}
                  className={bouton + (classId === c.id ? choisi : libre)}
                >
                  {c.code}
                </button>
              ))}
            </div>
            <p className="mt-1 text-sm text-muted">
              Elle décide des leçons qu’il verra : un CM1 ne reçoit pas celles du CE1.
            </p>
          </div>
        </div>
      ) : null}

      {/* ───────── 3. L'emploi du temps ───────── */}
      {etape === 2 ? (
        <div className="mt-4 grid gap-4">
          {dejaConnu.isLoading ? <p className="text-sm text-muted">Je regarde…</p> : null}

          {dejaConnu.data && dejaConnu.data.matieres.length > 0 ? (
            <>
              <p className="rounded-2xl bg-leaf/15 px-4 py-3 text-base font-bold text-leaf">
                L’emploi du temps du {classeChoisie?.code} est déjà enregistré.
              </p>
              <p className="text-sm text-muted">
                {dejaConnu.data.matieres.length} matières
                {dejaConnu.data.creneaux > 0 ? ` et ${dejaConnu.data.creneaux} créneaux` : ''} —
                {prenom.trim() ? ` ${prenom.trim()}` : ' cet enfant'} en hérite sans rien faire.
              </p>
              <ul className="flex flex-wrap gap-1.5">
                {dejaConnu.data.matieres.slice(0, 14).map((m) => (
                  <li
                    key={m}
                    className="rounded-full border border-line bg-paper px-3 py-1 text-sm"
                  >
                    {m}
                  </li>
                ))}
              </ul>
            </>
          ) : null}

          {dejaConnu.data && dejaConnu.data.matieres.length === 0 ? (
            <>
              <p className="rounded-2xl bg-gold/25 px-4 py-3 text-base font-semibold text-ink-2">
                Aucun emploi du temps pour cette classe, pour l’instant.
              </p>
              <p className="text-sm text-muted">
                Ce n’est pas bloquant : vous choisirez la matière à chaque import de cours, et vous
                pourrez ajouter l’emploi du temps plus tard. Les matières se créent au fur et à
                mesure — la liste n’est figée par aucun référentiel.
              </p>
            </>
          ) : null}
        </div>
      ) : null}

      {/* ───────── 4. Le récapitulatif ───────── */}
      {etape === 3 ? (
        <div className="mt-4">
          <div className="flex items-center gap-4 rounded-2xl border border-line bg-paper px-4 py-4">
            <span aria-hidden="true" className="grid h-16 w-16 shrink-0 place-items-center rounded-full bg-gold/30 text-4xl">
              {emoji}
            </span>
            <div className="min-w-0">
              <strong className="block truncate text-lg">{prenom.trim() || 'Sans prénom'}</strong>
              <small className="block text-muted">
                {[
                  classeChoisie?.code,
                  ans !== null ? `${ans} ans` : null,
                  genre === 'fille' ? 'fille' : genre === 'garcon' ? 'garçon' : null,
                ]
                  .filter(Boolean)
                  .join(' · ')}
              </small>
              {ecole.trim() ? (
                <small className="block truncate text-muted">{ecole.trim()}</small>
              ) : null}
            </div>
          </div>

          <p className="mt-3 text-sm text-muted">
            Tout se modifie plus tard. Dès que le profil existe, vous pouvez lui importer son
            premier cours.
          </p>

          {creer.error ? (
            <div className="mt-3">
              <ErrorNote error={creer.error} />
            </div>
          ) : null}
        </div>
      ) : null}

      {/* ───────── La barre de navigation ───────── */}
      <div className="mt-6 flex flex-wrap items-center justify-between gap-2 border-t border-line pt-4">
        <Button
          variant="ghost"
          onClick={() => (etape === 0 ? onFini() : setEtape(etape - 1))}
          disabled={creer.isPending}
        >
          {etape === 0 ? 'Annuler' : 'Retour'}
        </Button>

        {etape < ETAPES.length - 1 ? (
          <Button onClick={() => setEtape(etape + 1)} disabled={!peutAvancer}>
            Continuer
          </Button>
        ) : (
          <Button onClick={() => creer.mutate()} disabled={creer.isPending || !prenom.trim()}>
            {creer.isPending ? 'Création…' : 'Créer le profil'}
          </Button>
        )}
      </div>
    </div>
  );
}
