import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import { setCurrentChildId } from '../lib/childSession';
import { Button, Card, ErrorNote, Field, Loading, Pill } from '../components/ui';

/**
 * Le verrou de l’espace parent.
 *
 * Quatre chiffres ne protègent pas d’un adulte déterminé, et ce n’est pas le
 * but : il s’agit d’empêcher l’enfant d’aller lire les réponses ou de modifier
 * sa progression. La vérification se fait en base, le hash ne descend jamais
 * jusqu’au navigateur.
 */
function PinDialog({ onClose }: { onClose: () => void }) {
  const navigate = useNavigate();
  const [pin, setPin] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    const { data, error: rpcError } = await supabase.rpc('verify_parent_pin', { candidate: pin });
    setBusy(false);
    if (rpcError) {
      setError(rpcError.message);
      return;
    }
    if (data === true) navigate('/parent');
    else setError('Code incorrect.');
  }

  return (
    <div className="fixed inset-0 grid place-items-center bg-ink/40 p-6">
      <Card className="w-full max-w-sm">
        <form onSubmit={submit} className="grid gap-4">
          <h2 className="text-xl font-bold">Code parent</h2>
          <Field
            label="Quatre chiffres"
            inputMode="numeric"
            maxLength={4}
            autoFocus
            value={pin}
            onChange={(e) => setPin(e.target.value.replace(/\D/g, ''))}
          />
          {error ? <ErrorNote error={new Error(error)} /> : null}
          <div className="flex gap-2">
            <Button type="submit" disabled={busy || pin.length !== 4}>
              Entrer
            </Button>
            <Button type="button" variant="secondary" onClick={onClose}>
              Annuler
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}

type ChildCard = {
  id: string;
  first_name: string;
  avatar: string | null;
  classes: { code: string } | null;
};

export default function ProfilePicker() {
  const navigate = useNavigate();
  const [askPin, setAskPin] = useState(false);

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

  async function openParentSpace() {
    const { data } = await supabase.rpc('parent_pin_is_set');
    if (data === true) setAskPin(true);
    else navigate('/parent');
  }

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
        <Button variant="secondary" onClick={openParentSpace}>
          Espace parent
        </Button>
      </div>

      {askPin ? <PinDialog onClose={() => setAskPin(false)} /> : null}
    </main>
  );
}
