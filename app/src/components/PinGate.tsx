import { useState } from 'react';
import type { FormEvent, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import { Button, Card, ErrorNote, Field, Loading } from './ui';

/**
 * Verrou de l'espace parent, posé sur la route et non sur un bouton.
 *
 * Première version : la vérification vivait dans l'écran de choix de profil.
 * Taper /parent dans la barre d'adresse suffisait alors à passer outre — un
 * enfant de CM1 sait faire cela. Le contrôle appartient donc à la route.
 *
 * Le déverrouillage tient dans sessionStorage : il dure le temps de l'onglet,
 * et se referme à sa fermeture. localStorage le rendrait permanent, ce qui
 * viderait le verrou de son sens.
 */
const CLE = 'sfc-parent-ouvert';

export function estDeverrouille(): boolean {
  try {
    return sessionStorage.getItem(CLE) === '1';
  } catch {
    return false;
  }
}

export function deverrouiller() {
  try {
    sessionStorage.setItem(CLE, '1');
  } catch {
    /* stockage bloqué : le code sera redemandé, ce qui est le bon défaut */
  }
}

export function verrouiller() {
  try {
    sessionStorage.removeItem(CLE);
  } catch {
    /* sans effet, le verrou reste fermé par défaut */
  }
}

export default function PinGate({ children }: { children: ReactNode }) {
  const navigate = useNavigate();
  const [pin, setPin] = useState('');
  const [erreur, setErreur] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [ouvert, setOuvert] = useState(estDeverrouille());

  const codeDefini = useQuery({
    queryKey: ['pin-set'],
    queryFn: async () => {
      const { data, error } = await supabase.rpc('parent_pin_is_set');
      if (error) throw error;
      return data as boolean;
    },
  });

  if (codeDefini.isLoading) return <Loading label="Vérification du verrou…" />;
  if (codeDefini.error) return <ErrorNote error={codeDefini.error} />;

  // Aucun code défini : l'espace reste ouvert, et les réglages invitent à en
  // créer un. Refuser l'accès ici enfermerait le parent dehors.
  if (codeDefini.data !== true || ouvert) return <>{children}</>;

  async function soumettre(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setErreur(null);
    const { data, error } = await supabase.rpc('verify_parent_pin', { candidate: pin });
    setBusy(false);
    if (error) {
      setErreur(error.message);
      return;
    }
    if (data === true) {
      deverrouiller();
      setOuvert(true);
    } else {
      setErreur('Code incorrect.');
      setPin('');
    }
  }

  return (
    <main className="mx-auto grid min-h-screen max-w-sm place-items-center p-6">
      <Card className="w-full">
        <form onSubmit={soumettre} className="grid gap-4">
          <div>
            <h1 className="text-xl font-bold">Espace parent</h1>
            <p className="mt-1 text-sm text-muted">Entre le code à quatre chiffres.</p>
          </div>
          <Field
            label="Code"
            inputMode="numeric"
            maxLength={4}
            autoFocus
            value={pin}
            onChange={(e) => setPin(e.target.value.replace(/\D/g, ''))}
          />
          {erreur ? <ErrorNote error={new Error(erreur)} /> : null}
          <div className="flex gap-2">
            <Button type="submit" disabled={busy || pin.length !== 4}>
              Entrer
            </Button>
            <Button type="button" variant="secondary" onClick={() => navigate('/')}>
              Retour
            </Button>
          </div>
        </form>
      </Card>
    </main>
  );
}
