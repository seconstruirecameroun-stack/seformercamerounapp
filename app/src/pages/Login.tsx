import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { ErrorNote } from '../components/ui';
import Mascotte from '../components/jeu/Mascotte';

/**
 * L'entrée de l'espace parent.
 *
 * Elle était correcte et froide : un titre, deux champs, un bouton gris. Or
 * c'est le premier écran d'un parent qui arrive de la page d'accueil, et il
 * doit reconnaître la même maison — même fond, même lionceau, mêmes boutons
 * ronds.
 *
 * Le choix entre se connecter et créer un compte est un interrupteur visible,
 * et non un lien perdu sous le formulaire : la moitié des arrivants viennent
 * pour créer, et l'adresse qui les amène le dit déjà (`?mode=creation`).
 */
export default function LoginPage() {
  const navigate = useNavigate();
  const [parametres] = useSearchParams();
  const [mode, setMode] = useState<'in' | 'up'>(
    parametres.get('mode') === 'creation' ? 'up' : 'in',
  );
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    setNotice(null);
    try {
      if (mode === 'in') {
        const { error: signInError } = await supabase.auth.signInWithPassword({ email, password });
        if (signInError) throw signInError;
        navigate('/', { replace: true });
      } else {
        const { data, error: signUpError } = await supabase.auth.signUp({ email, password });
        if (signUpError) throw signUpError;
        // Selon le réglage du projet, la session est immédiate ou il faut
        // confirmer l’adresse par courriel.
        if (data.session) navigate('/', { replace: true });
        else setNotice('Compte créé. Vérifiez votre boîte mail pour confirmer l’adresse.');
      }
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }

  function basculer(vers: 'in' | 'up') {
    setMode(vers);
    setError(null);
    setNotice(null);
  }

  const champ =
    'w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3.5 text-kid ' +
    'outline-none transition focus:border-clay';

  return (
    <main className="enfant ciel flex min-h-screen flex-col">
      <header className="mx-auto w-full max-w-5xl px-4 py-4 sm:px-6">
        <Link to="/" className="inline-flex items-center gap-2">
          <Mascotte taille={36} />
          <strong className="text-kid-sm font-black">Se Former Cameroun</strong>
        </Link>
      </header>

      <div className="mx-auto flex w-full max-w-md flex-1 flex-col justify-center gap-5 px-4 pb-10 sm:px-6">
        <div className="text-center">
          <Mascotte humeur={mode === 'up' ? 'fete' : 'content'} taille={84} className="mx-auto" />
          <h1 className="mt-2 text-kid-xl font-black text-balance">
            {mode === 'in' ? 'Content de vous revoir' : 'Bienvenue'}
          </h1>
          <p className="mt-1 text-kid-sm text-ink-2">
            {mode === 'in'
              ? 'Entrez pour retrouver les leçons de vos enfants.'
              : 'Quelques secondes, et vous pourrez importer un premier cours.'}
          </p>
        </div>

        {/* L'interrupteur : deux moitiés, celle qui est active porte le fond. */}
        <div
          role="tablist"
          aria-label="Se connecter ou créer un compte"
          className="grid grid-cols-2 gap-1 rounded-full border-2 border-line bg-white-warm p-1"
        >
          {(
            [
              ['in', 'Se connecter'],
              ['up', 'Créer un compte'],
            ] as const
          ).map(([valeur, libelle]) => (
            <button
              key={valeur}
              type="button"
              role="tab"
              aria-selected={mode === valeur}
              onClick={() => basculer(valeur)}
              className={
                'rounded-full py-2.5 text-kid-sm font-bold transition ' +
                (mode === valeur ? 'bg-ink text-white-warm' : 'text-ink-2')
              }
            >
              {libelle}
            </button>
          ))}
        </div>

        <form
          onSubmit={submit}
          className="grid gap-4 rounded-[var(--radius-card)] border border-line bg-white-warm/90 p-5 shadow-[var(--shadow-card)]"
        >
          <label className="grid gap-1.5">
            <span className="text-kid-sm font-bold">Adresse e-mail</span>
            <input
              type="email"
              autoComplete="email"
              required
              className={champ}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="vous@exemple.com"
            />
          </label>

          <label className="grid gap-1.5">
            <span className="text-kid-sm font-bold">Mot de passe</span>
            <input
              type="password"
              autoComplete={mode === 'in' ? 'current-password' : 'new-password'}
              required
              minLength={8}
              className={champ}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            {mode === 'up' ? (
              <small className="text-kid-xs text-muted">Huit caractères au minimum.</small>
            ) : null}
          </label>

          {error ? <ErrorNote error={error} /> : null}
          {notice ? (
            <p className="rounded-2xl bg-leaf/15 px-4 py-3 text-kid-sm font-bold text-leaf">
              {notice}
            </p>
          ) : null}

          <button
            type="submit"
            disabled={busy}
            className="tuile rounded-full bg-clay py-4 text-kid font-black text-white-warm shadow-[0_3px_0_var(--color-clay-dark)] disabled:opacity-60"
          >
            {busy ? 'Un instant…' : mode === 'in' ? 'Se connecter' : 'Créer mon compte'}
          </button>
        </form>

        <p className="text-center text-kid-xs text-muted text-balance">
          L’espace parent est protégé par un code à quatre chiffres. Les cahiers de vos enfants ne
          servent qu’à leurs révisions.
        </p>
      </div>
    </main>
  );
}
