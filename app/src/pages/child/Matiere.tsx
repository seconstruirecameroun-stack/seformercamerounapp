import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { chargerTableauDeBord } from '../../lib/dashboard';
import CarteLecon from '../../components/CarteLecon';
import Illustration from '../../components/Illustration';
import { ErrorNote, Loading } from '../../components/ui';

/**
 * Le dossier d'une matière, ouvert.
 *
 * On réutilise le tableau de bord plutôt que de refaire une requête : il est
 * déjà en cache quand l'enfant arrive d'ici, l'ouverture est donc immédiate.
 * Sur une connexion lente, une page qui s'affiche sans attendre vaut mieux
 * qu'une requête parfaitement taillée.
 */
export default function Matiere() {
  const { childId, subjectId } = useParams<{ childId: string; subjectId: string }>();

  const bord = useQuery({
    queryKey: ['tableau', childId],
    enabled: Boolean(childId),
    queryFn: () => chargerTableauDeBord(childId!),
  });

  if (bord.isLoading) return <Loading />;
  if (bord.error) return <ErrorNote error={bord.error} />;

  const d = bord.data!;
  const matiere = d.matieres.find((m) => m.id === subjectId);
  const lecons = d.lecons.filter((l) => l.matiereId === subjectId);
  const couleur = matiere?.couleur ?? 'var(--color-clay)';

  return (
    <main className="enfant ciel min-h-screen pb-12">
      <div className="mx-auto grid max-w-2xl gap-4 px-4 pt-4 sm:px-6">
        <header className="flex items-center justify-between gap-3">
          <Link
            to={`/enfant/${childId}`}
            className="tuile flex items-center gap-2 rounded-full bg-white-warm/80 py-2 pr-4 pl-3 text-kid-sm font-bold"
          >
            <span aria-hidden="true">←</span>
            Mes matières
          </Link>
          <span className="flex items-center gap-1.5 rounded-full bg-gold/35 px-4 py-2 text-kid-sm font-black">
            <span aria-hidden="true">★</span>
            {d.points}
          </span>
        </header>

        <section
          className="relative overflow-hidden rounded-[var(--radius-card)] border-2 shadow-[var(--shadow-card)]"
          style={{ borderColor: couleur }}
        >
          <Illustration
            cle={matiere?.illustration}
            forme="scene"
            alt=""
            priorite
            className="h-28 w-full object-cover sm:h-36"
          />
          <span
            aria-hidden="true"
            className="absolute inset-0 opacity-35 mix-blend-multiply"
            style={{ backgroundColor: couleur }}
          />
          <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/80 to-transparent px-5 pt-10 pb-3">
            <h1 className="text-kid-xl leading-tight font-black text-white-warm text-balance">
              {matiere?.label ?? 'Mes leçons'}
            </h1>
            <p className="text-kid-sm font-bold text-white-warm/90">
              {lecons.length > 1 ? `${lecons.length} leçons` : `${lecons.length} leçon`}
            </p>
          </div>
        </section>

        {lecons.length === 0 ? (
          <div className="rounded-[var(--radius-card)] border border-line bg-white-warm p-6 text-center">
            <Illustration cle="repos" forme="objet" alt="" className="mx-auto h-24 w-24" />
            <p className="mt-2 text-kid-sm text-muted">Pas encore de leçon ici.</p>
          </div>
        ) : (
          <div className="grid gap-2">
            {lecons.map((lecon) => (
              <CarteLecon key={lecon.id} lecon={lecon} childId={childId!} montrerMatiere={false} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
