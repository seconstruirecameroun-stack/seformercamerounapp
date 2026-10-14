import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import { setCurrentChildId } from '../lib/childSession';
import { Button, Card, ErrorNote, Loading, Pill } from '../components/ui';

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

  if (children.isLoading) return <Loading />;
  if (children.error) return <ErrorNote error={children.error} />;

  const list = children.data ?? [];

  return (
    <main className="mx-auto max-w-3xl p-6">
      <header className="mb-8 text-center">
        <Pill>Qui révise aujourd’hui ?</Pill>
        <h1 className="mt-3 text-3xl font-black">Se Former Cameroun</h1>
      </header>

      {list.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-3">
          {list.map((child) => (
            <button
              key={child.id}
              onClick={() => {
                setCurrentChildId(child.id);
                navigate('/enfant/' + child.id);
              }}
              className="rounded-[var(--radius-card)] bg-white-warm p-6 text-center shadow-[var(--shadow-card)] transition hover:-translate-y-1"
            >
              <span className="mx-auto grid h-16 w-16 place-items-center rounded-full bg-gold/30 text-2xl">
                {child.avatar ?? child.first_name.slice(0, 1).toUpperCase()}
              </span>
              <strong className="mt-3 block text-lg">{child.first_name}</strong>
              <small className="text-muted">{child.classes?.code ?? 'Classe à définir'}</small>
            </button>
          ))}
        </div>
      ) : (
        <Card className="text-center">
          <h2 className="text-xl font-bold">Aucun enfant pour l’instant</h2>
          <p className="mt-2 text-sm text-muted">
            Ouvrez l’espace parent pour ajouter un premier profil.
          </p>
        </Card>
      )}

      <div className="mt-8 text-center">
        <Button variant="secondary" onClick={() => navigate('/parent')}>
          Espace parent
        </Button>
      </div>
    </main>
  );
}
