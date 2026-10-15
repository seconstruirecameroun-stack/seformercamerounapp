import { Link } from 'react-router-dom';
import Illustration from './Illustration';
import type { MatiereResume } from '../lib/dashboard';

/**
 * Une matière, présentée comme un dossier qu'on ouvre.
 *
 * La couleur vient de la matière elle-même : c'est celle que l'enfant
 * retrouvera sur la page de la matière, et elle l'aide à viser la bonne
 * tuile avant même de savoir lire l'intitulé.
 *
 * La couverture est l'image de la première leçon du dossier. Produire une
 * image par matière coûterait trente générations pour un gain nul : l'enfant
 * reconnaît le dossier à la couleur et à la place, pas au dessin.
 */
export default function CarteMatiere({
  matiere,
  childId,
}: {
  matiere: MatiereResume;
  childId: string;
}) {
  const couleur = matiere.couleur ?? 'var(--color-clay)';
  return (
    <Link
      to={`/enfant/${childId}/matiere/${matiere.id}`}
      className="tuile relative flex flex-col overflow-hidden rounded-[var(--radius-card)] border-2 bg-white-warm shadow-[var(--shadow-tile)]"
      style={{ borderColor: couleur }}
    >
      <div className="relative h-24 w-full overflow-hidden sm:h-28">
        <Illustration
          cle={matiere.illustration}
          forme="scene"
          alt=""
          className="h-full w-full object-cover"
        />
        {/* Un voile à la couleur de la matière : les couvertures sont toutes
            pastel, elles se ressembleraient sans lui. */}
        <span
          aria-hidden="true"
          className="absolute inset-0 opacity-30 mix-blend-multiply"
          style={{ backgroundColor: couleur }}
        />
      </div>

      <div className="flex flex-1 flex-col gap-0.5 px-3 py-2.5">
        <h3 className="line-clamp-2 text-kid font-extrabold text-balance">{matiere.label}</h3>
        <p className="text-kid-xs font-bold text-muted">
          {matiere.lecons > 1 ? `${matiere.lecons} leçons` : '1 leçon'}
        </p>
      </div>

      {matiere.aRevoir > 0 ? (
        <span className="absolute top-2 right-2 grid h-7 min-w-7 place-items-center rounded-full bg-clay px-2 text-kid-xs font-black text-white-warm shadow-[var(--shadow-tile)]">
          {matiere.aRevoir}
        </span>
      ) : null}
    </Link>
  );
}
