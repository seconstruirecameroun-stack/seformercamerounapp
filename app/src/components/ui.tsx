import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode } from 'react';

export function Card({ children, className = '' }: { children: ReactNode; className?: string }) {
  return (
    <section
      className={`rounded-[var(--radius-card)] bg-white-warm p-6 shadow-[var(--shadow-card)] ${className}`}
    >
      {children}
    </section>
  );
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost';
};

export function Button({ variant = 'primary', className = '', ...rest }: ButtonProps) {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-full px-5 py-3 text-sm font-semibold ' +
    'transition disabled:cursor-not-allowed disabled:opacity-50';
  const look = {
    primary: 'bg-clay text-white-warm hover:bg-clay-dark',
    secondary: 'border border-line bg-white-warm text-ink hover:border-ink-2',
    ghost: 'text-ink-2 underline hover:text-ink',
  }[variant];
  return <button className={`${base} ${look} ${className}`} {...rest} />;
}

export function Field({
  label,
  hint,
  ...rest
}: InputHTMLAttributes<HTMLInputElement> & { label: string; hint?: string }) {
  return (
    <label className="block">
      <span className="mb-1 block text-xs font-bold tracking-wide text-muted uppercase">
        {label}
      </span>
      <input
        className="w-full rounded-2xl border border-line bg-white-warm px-4 py-3 text-ink outline-none focus:border-ink-2"
        {...rest}
      />
      {hint && <span className="mt-1 block text-xs text-muted">{hint}</span>}
    </label>
  );
}

export function Pill({ children }: { children: ReactNode }) {
  return (
    <span className="inline-block rounded-full bg-gold/25 px-3 py-1 text-xs font-bold tracking-wide text-ink uppercase">
      {children}
    </span>
  );
}

export function Loading({ label = 'Chargement…' }: { label?: string }) {
  return <p className="p-6 text-sm text-muted">{label}</p>;
}

export function ErrorNote({ error }: { error: unknown }) {
  const message = error instanceof Error ? error.message : String(error);
  return (
    <p className="rounded-2xl bg-clay/10 px-4 py-3 text-sm text-clay-dark" role="alert">
      {message}
    </p>
  );
}
