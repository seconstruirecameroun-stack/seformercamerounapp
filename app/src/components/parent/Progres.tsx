import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { chargerTableauDeBord } from '../../lib/dashboard';
import { PALIERS } from '../../lib/paliers';
import { ErrorNote, Loading } from '../ui';

/**
 * Où en est chaque enfant.
 *
 * C'est ce qui manquait à l'espace parent : on pouvait y importer des cours,
 * les valider, régler un code — mais pas savoir si l'enfant jouait. Un parent
 * ouvre cette page pour deux raisons, et celle-ci passait à la trappe.
 *
 * Rien n'est calculé ici : tout vient du même tableau de bord que l'enfant
 * voit de son côté, sous la même clé de cache. Le parent et l'enfant lisent
 * donc exactement les mêmes chiffres — il n'y a pas une version pour chacun.
 */

type Enfant = { id: string; first_name: string; avatar: string | null; classes?: { code: string } | null };

/** Le dernier jour joué, dit comme on le dirait à voix haute. */
function derniereFois(jours: string[]): { texte: string; alerte: boolean } {
  if (jours.length === 0) return { texte: 'n’a jamais joué', alerte: true };

  const aujourdhui = new Date();
  const jour = (d: number) => {
    const x = new Date(aujourdhui);
    x.setDate(x.getDate() - d);
    return x.toISOString().slice(0, 10);
  };

  const dernier = [...jours].sort().reverse()[0];
  if (dernier === jour(0)) return { texte: 'a joué aujourd’hui', alerte: false };
  if (dernier === jour(1)) return { texte: 'a joué hier', alerte: false };
  for (let d = 2; d <= 14; d++) {
    if (dernier === jour(d)) return { texte: `a joué il y a ${d} jours`, alerte: d >= 3 };
  }
  return { texte: 'n’a pas joué depuis deux semaines', alerte: true };
}

function Chiffre({ valeur, libelle }: { valeur: string; libelle: string }) {
  return (
    <div className="rounded-2xl bg-paper px-3 py-2 text-center">
      <p className="text-xl leading-tight font-black">{valeur}</p>
      <p className="text-sm text-muted">{libelle}</p>
    </div>
  );
}

function CarteEnfant({ enfant }: { enfant: Enfant }) {
  // Même clé que l'espace enfant : le chiffre affiché ici est celui qu'il
  // voit, pas une seconde version qui pourrait en diverger.
  const bord = useQuery({
    queryKey: ['tableau', enfant.id],
    queryFn: () => chargerTableauDeBord(enfant.id),
  });

  const d = bord.data;
  const avecImage = d?.autocollants.filter((a) => a.illustration) ?? [];
  const gagnees = avecImage.filter((a) => a.acquis).length;
  const terminees = d?.lecons.filter((l) => l.etapeTerminee).length ?? 0;
  const enCours = d?.lecons.filter((l) => !l.etapeTerminee && l.etapeTotal > 0).length ?? 0;
  const aRevoir = d?.lecons.reduce((n, l) => n + l.aRevoir, 0) ?? 0;
  const courante = d?.lecons.find((l) => l.id === d.prochaineLecon);
  const vu = derniereFois(d?.jours ?? []);

  return (
    <article className="rounded-[var(--radius-card)] border border-line bg-white-warm/85 p-5">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex min-w-0 items-center gap-3">
          <span className="grid h-12 w-12 shrink-0 place-items-center rounded-full bg-gold/30 text-2xl">
            {enfant.avatar ?? enfant.first_name.slice(0, 1).toUpperCase()}
          </span>
          <div className="min-w-0">
            <strong className="block truncate text-lg">{enfant.first_name}</strong>
            <small className="block text-muted">
              {enfant.classes?.code ?? 'Classe à définir'}
            </small>
          </div>
        </div>
        <Link
          to={`/enfant/${enfant.id}`}
          className="tuile shrink-0 rounded-full border-2 border-line bg-white-warm px-4 py-2 text-base font-bold"
        >
          Voir son espace
        </Link>
      </header>

      {bord.isLoading ? <Loading label="Je rassemble sa progression…" /> : null}
      {bord.error ? (
        <div className="mt-3">
          <ErrorNote error={bord.error} />
        </div>
      ) : null}

      {d ? (
        <>
          <p
            className={
              'mt-4 rounded-2xl px-4 py-2.5 text-base font-bold ' +
              (vu.alerte ? 'bg-clay/10 text-clay-dark' : 'bg-leaf/15 text-leaf')
            }
          >
            {enfant.first_name} {vu.texte}.
          </p>

          <div className="mt-3 grid grid-cols-3 gap-2">
            <Chiffre
              valeur={String(d.serie.jours)}
              libelle={d.serie.jours > 1 ? 'jours de suite' : 'jour de suite'}
            />
            <Chiffre valeur={String(d.points)} libelle="étoiles" />
            <Chiffre valeur={`${gagnees}/${avecImage.length}`} libelle="images" />
          </div>

          <dl className="mt-3 grid min-w-0 gap-1.5 text-base">
            <div className="flex min-w-0 justify-between gap-3">
              <dt className="text-muted">Rang</dt>
              <dd className="font-bold">{d.rang.rang.nom}</dd>
            </div>
            <div className="flex min-w-0 justify-between gap-3">
              <dt className="text-muted">Leçons</dt>
              <dd className="min-w-0 text-right font-bold">
                {terminees} terminée{terminees > 1 ? 's' : ''}
                {enCours > 0 ? `, ${enCours} en cours` : ''}
              </dd>
            </div>
            {courante && !courante.etapeTerminee ? (
              <div className="flex min-w-0 justify-between gap-3">
                <dt className="text-muted">En ce moment</dt>
                <dd className="min-w-0 text-right font-bold">
                  <span className="block truncate">{courante.title}</span>
                  <span className="block text-sm font-normal text-muted">
                    Étape {courante.etape} · {PALIERS[courante.etape - 1]?.nom ?? ''}
                  </span>
                </dd>
              </div>
            ) : null}
            {aRevoir > 0 ? (
              <div className="flex min-w-0 justify-between gap-3">
                <dt className="text-muted">À revoir</dt>
                <dd className="font-bold">
                  {aRevoir} notion{aRevoir > 1 ? 's' : ''}
                </dd>
              </div>
            ) : null}
          </dl>
        </>
      ) : null}
    </article>
  );
}

export default function Progres({ enfants }: { enfants: Enfant[] }) {
  if (enfants.length === 0) return null;
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {enfants.map((e) => (
        <CarteEnfant key={e.id} enfant={e} />
      ))}
    </div>
  );
}
