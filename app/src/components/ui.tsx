import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode } from 'react';

/**
 * Les pièces communes de l'espace parent.
 *
 * Trois registres cohabitent dans l'app, et c'est voulu :
 *
 *   la porte d'entrée — accueil public et connexion — accueille ;
 *   l'espace parent sert une tâche ;
 *   l'espace enfant donne envie d'ouvrir l'app.
 *
 * Ces primitives tiennent le deuxième. Elles restent en police système et en
 * densité normale — un parent lit vite et cherche une ligne précise — mais
 * elles empruntent à la porte d'entrée ses surfaces : même rayon, même filet,
 * même fond crème, mêmes boutons ronds. L'app doit rester une seule maison.
 *
 * Une règle a changé ici : plus aucune étiquette en petites capitales de
 * 12 px. Le parent lit sur le même téléphone que l'enfant, dans le même salon
 * au soleil. Rien ne descend sous 14 px.
 */

export function Card({
  titre,
  sous,
  actions,
  children,
  className = '',
}: {
  /** Le titre de la section. Omis, la carte n'est qu'une surface. */
  titre?: string;
  /** Une ligne qui dit à quoi sert la section : sans elle, un parent
      découvre la fonction en cliquant. */
  sous?: string;
  /** Ce qui se pose à droite du titre : un bouton, un compteur. */
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`rounded-[var(--radius-card)] border border-line bg-white-warm/85 p-5 sm:p-6 ${className}`}
    >
      {titre ? (
        <header className="mb-4 flex flex-wrap items-start justify-between gap-3">
          <div className="min-w-0">
            <h2 className="text-lg font-extrabold">{titre}</h2>
            {sous ? <p className="mt-0.5 text-sm text-muted">{sous}</p> : null}
          </div>
          {actions ? <div className="flex shrink-0 gap-2">{actions}</div> : null}
        </header>
      ) : null}
      {children}
    </section>
  );
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
};

export function Button({ variant = 'primary', className = '', ...rest }: ButtonProps) {
  const base =
    'tuile inline-flex items-center justify-center gap-2 rounded-full px-5 py-3 text-base ' +
    'font-bold transition disabled:cursor-not-allowed disabled:opacity-50';
  // Le relief n'est posé que sur l'action principale : s'il était partout,
  // il ne désignerait plus rien.
  const look = {
    primary: 'bg-clay text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]',
    secondary: 'border-2 border-line bg-white-warm text-ink hover:border-ink-2',
    ghost: 'px-3 text-ink-2 underline underline-offset-2 hover:text-ink',
    danger: 'border-2 border-clay/40 bg-clay/10 text-clay-dark hover:border-clay',
  }[variant];
  return <button className={`${base} ${look} ${className}`} {...rest} />;
}

export function Field({
  label,
  hint,
  className = '',
  ...rest
}: InputHTMLAttributes<HTMLInputElement> & { label: string; hint?: string }) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-bold">{label}</span>
      <input
        className={
          'w-full rounded-2xl border-2 border-line bg-white-warm px-4 py-3 text-base text-ink ' +
          'outline-none transition focus:border-clay ' +
          className
        }
        {...rest}
      />
      {hint ? <span className="mt-1 block text-sm text-muted">{hint}</span> : null}
    </label>
  );
}

/** Un libellé posé au-dessus d'un titre : il situe, il n'informe pas. */
export function Pill({ children }: { children: ReactNode }) {
  return (
    <span className="inline-block rounded-full bg-gold/30 px-3.5 py-1.5 text-sm font-bold text-ink">
      {children}
    </span>
  );
}

/**
 * L'attente.
 *
 * Trois points qui respirent plutôt qu'un mot seul : sur une connexion lente,
 * un texte figé laisse croire que l'écran est cassé.
 */
export function Loading({ label = 'Chargement…' }: { label?: string }) {
  return (
    <p className="flex items-center gap-2 p-6 text-sm text-muted" role="status">
      <span aria-hidden="true" className="flex gap-1">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="flamme inline-block h-1.5 w-1.5 rounded-full bg-muted"
            style={{ animationDelay: `${i * 160}ms`, animationDuration: '1200ms' }}
          />
        ))}
      </span>
      {label}
    </p>
  );
}

/**
 * Le vide, dit comme une étape et non comme un manque.
 *
 * « Aucun document » laisse le parent sans suite ; « importez un premier
 * cours » lui dit où aller.
 */
export function Vide({
  titre,
  texte,
  action,
}: {
  titre: string;
  texte: string;
  action?: ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-dashed border-line px-5 py-8 text-center">
      <p className="font-bold">{titre}</p>
      <p className="mx-auto mt-1 max-w-sm text-sm text-muted">{texte}</p>
      {action ? <div className="mt-4 flex justify-center">{action}</div> : null}
    </div>
  );
}

export function ErrorNote({ error }: { error: unknown }) {
  const message = error instanceof Error ? error.message : String(error);
  return (
    <p
      className="rounded-2xl border-2 border-clay/30 bg-clay/10 px-4 py-3 text-sm font-semibold text-clay-dark"
      role="alert"
    >
      {message}
    </p>
  );
}
