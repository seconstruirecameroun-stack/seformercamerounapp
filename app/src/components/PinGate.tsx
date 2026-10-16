import { useEffect, useRef, useState } from 'react';
import type { FormEvent, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../lib/supabase';
import { ErrorNote, Loading } from './ui';
import Mascotte from './jeu/Mascotte';

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
  const champ = useRef<HTMLInputElement>(null);

  // Quatre chiffres posés : on vérifie sans attendre le bouton. Sur un
  // téléphone, le clavier cache justement ce bouton.
  useEffect(() => {
    if (pin.length === 4 && !busy) champ.current?.form?.requestSubmit();
  }, [pin, busy]);

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
    <main className="enfant ciel flex min-h-screen flex-col items-center justify-center px-4 py-8">
      <div className="w-full max-w-sm text-center">
        <Mascotte humeur={erreur ? 'encourage' : 'content'} taille={76} className="mx-auto" />
        <h1 className="mt-2 text-kid-xl font-black">Espace parent</h1>
        <p className="mt-1 text-kid-sm text-ink-2">Entrez votre code à quatre chiffres.</p>

        <form onSubmit={soumettre} className={'mt-6 ' + (erreur ? 'secoue' : '')}>
          {/* Quatre pastilles, et un champ invisible par-dessus : l'enfant qui
              regarde par-dessus l'épaule ne lit rien, et le parent voit tout
              de suite combien de chiffres il a posés. */}
          <label className="relative block">
            <span className="sr-only">Code à quatre chiffres</span>
            <span aria-hidden="true" className="flex justify-center gap-3">
              {[0, 1, 2, 3].map((i) => (
                <span
                  key={i}
                  className={
                    'grid h-16 w-14 place-items-center rounded-2xl border-2 text-kid-xl font-black transition ' +
                    (pin.length === i && !erreur
                      ? 'border-clay bg-white-warm'
                      : pin.length > i
                        ? 'border-line bg-white-warm'
                        : 'border-line bg-white-warm/60')
                  }
                >
                  {pin.length > i ? '•' : ''}
                </span>
              ))}
            </span>
            <input
              ref={champ}
              type="password"
              inputMode="numeric"
              autoComplete="off"
              maxLength={4}
              autoFocus
              value={pin}
              onChange={(e) => {
                setErreur(null);
                setPin(e.target.value.replace(/\D/g, '').slice(0, 4));
              }}
              className="absolute inset-0 h-full w-full cursor-pointer rounded-2xl bg-transparent text-transparent caret-transparent outline-none"
            />
          </label>

          {erreur ? (
            <p className="mt-4 text-kid-sm font-bold text-clay-dark" role="alert">
              {erreur}
            </p>
          ) : null}

          <div className="mt-6 flex flex-wrap justify-center gap-2">
            <button
              type="submit"
              disabled={busy || pin.length !== 4}
              className="tuile rounded-full bg-clay px-7 py-3.5 text-kid font-black text-white-warm shadow-[0_3px_0_var(--color-clay-dark)] disabled:opacity-50"
            >
              {busy ? 'Un instant…' : 'Entrer'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/')}
              className="tuile rounded-full border-2 border-line bg-white-warm px-7 py-3.5 text-kid font-bold shadow-[var(--shadow-tile)]"
            >
              Retour
            </button>
          </div>
        </form>

        <p className="mt-6 text-kid-xs text-muted text-balance">
          Ce code protège l’import des cours, la validation et les réglages. Il se redemande à
          chaque nouvel onglet.
        </p>
      </div>
    </main>
  );
}
