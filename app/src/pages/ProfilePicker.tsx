import { Link, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import { setCurrentChildId } from '../lib/childSession';
import { ErrorNote, Loading } from '../components/ui';
import Mascotte from '../components/jeu/Mascotte';

/**
 * Le carrefour : qui révise maintenant ?
 *
 * C'est un enfant qui touche cet écran, pas le parent — il hérite donc du
 * registre de l'espace enfant : grandes cibles, Fredoka, fond de lever de
 * jour. L'accès à l'espace parent reste présent mais discret, en bas : un
 * enfant ne doit pas tomber dessus par mégarde, et le code l'arrête de toute
 * façon.
 */

type ChildCard = {
  id: string;
  first_name: string;
  avatar: string | null;
  classes: { code: string } | null;
};

export default function ProfilePicker() {
  const navigate = useNavigate();

  const children = useQuery({
    queryKey: ['children'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('id, first_name, avatar, classes(code)')
        .order('created_at');
      if (error) throw error;
      return data as unknown as ChildCard[];
    },
  });

  const list = children.data ?? [];

  return (
    <main className="enfant ciel flex min-h-screen flex-col">
      <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col justify-center gap-6 px-4 py-8 sm:px-6">
        <header className="text-center">
          <Mascotte taille={76} className="mx-auto" />
          <h1 className="mt-2 text-kid-xl font-black text-balance">Qui révise aujourd’hui ?</h1>
        </header>

        {children.isLoading ? <Loading label="Je cherche les profils…" /> : null}
        {children.error ? <ErrorNote error={children.error} /> : null}

        {list.length > 0 ? (
          <ul className="grid gap-3 sm:grid-cols-2">
            {list.map((child) => (
              <li key={child.id}>
                <button
                  type="button"
                  onClick={() => {
                    setCurrentChildId(child.id);
                    navigate('/enfant/' + child.id);
                  }}
                  className="tuile flex w-full items-center gap-4 rounded-[var(--radius-card)] border-2 border-line bg-white-warm px-5 py-4 text-left shadow-[var(--shadow-tile)]"
                >
                  <span className="grid h-16 w-16 shrink-0 place-items-center rounded-full bg-gold/30 text-3xl">
                    {child.avatar ?? child.first_name.slice(0, 1).toUpperCase()}
                  </span>
                  <span className="min-w-0 flex-1">
                    <strong className="block truncate text-kid-lg font-black">
                      {child.first_name}
                    </strong>
                    <small className="block text-kid-sm text-muted">
                      {child.classes?.code ?? 'Classe à définir'}
                    </small>
                  </span>
                  <span
                    aria-hidden="true"
                    className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-clay text-xl text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]"
                  >
                    ▶
                  </span>
                </button>
              </li>
            ))}
          </ul>
        ) : null}

        {!children.isLoading && list.length === 0 ? (
          <div className="rounded-[var(--radius-card)] border border-line bg-white-warm/85 px-6 py-8 text-center">
            <h2 className="text-kid-lg font-extrabold">Aucun enfant pour l’instant</h2>
            <p className="mx-auto mt-1 max-w-sm text-kid-sm text-muted">
              Ouvrez l’espace parent pour créer un premier profil, puis importez un cours.
            </p>
            <Link
              to="/parent"
              className="tuile mt-5 inline-block rounded-full bg-clay px-6 py-3.5 text-kid font-black text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]"
            >
              Ouvrir l’espace parent
            </Link>
          </div>
        ) : null}
      </div>

      <footer className="px-4 pb-8 text-center sm:px-6">
        <Link
          to="/parent"
          className="tuile inline-block rounded-full border-2 border-line bg-white-warm/80 px-5 py-2.5 text-kid-sm font-bold shadow-[var(--shadow-tile)]"
        >
          Espace parent
        </Link>
      </footer>
    </main>
  );
}
