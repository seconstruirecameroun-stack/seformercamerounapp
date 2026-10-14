import { useState } from 'react';
import type { FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Button, Card, ErrorNote, Field, Pill } from '../components/ui';

export default function LoginPage() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<'in' | 'up'>('in');
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

  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col justify-center gap-6 p-6">
      <div className="text-center">
        <Pill>Espace parent</Pill>
        <h1 className="mt-3 text-3xl font-black">Se Former Cameroun</h1>
        <p className="mt-2 text-sm text-muted">
          Les cours de vos enfants, transformés en révisions.
        </p>
      </div>

      <Card>
        <form onSubmit={submit} className="grid gap-4">
          <Field
            label="Adresse e-mail"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Field
            label="Mot de passe"
            type="password"
            autoComplete={mode === 'in' ? 'current-password' : 'new-password'}
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            hint={mode === 'up' ? 'Huit caractères au minimum.' : undefined}
          />
          {error ? <ErrorNote error={error} /> : null}
          {notice ? <p className="text-sm text-leaf">{notice}</p> : null}
          <Button type="submit" disabled={busy}>
            {busy ? 'Un instant…' : mode === 'in' ? 'Se connecter' : 'Créer mon compte'}
          </Button>
        </form>
      </Card>

      <p className="text-center text-sm text-muted">
        {mode === 'in' ? 'Pas encore de compte ?' : 'Déjà un compte ?'}{' '}
        <button
          type="button"
          className="font-semibold text-ink underline"
          onClick={() => {
            setMode(mode === 'in' ? 'up' : 'in');
            setError(null);
            setNotice(null);
          }}
        >
          {mode === 'in' ? 'En créer un' : 'Se connecter'}
        </button>
      </p>
    </main>
  );
}
