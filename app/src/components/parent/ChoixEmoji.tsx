/**
 * Le choix de l'emoji d'un enfant.
 *
 * Il fallait l'écrire dans un champ texte. Sur un téléphone, cela veut dire
 * ouvrir le clavier emoji, chercher dans six cents dessins, et espérer n'en
 * coller qu'un — le champ acceptait quatre caractères, donc deux emojis et un
 * espace passaient sans rien dire. Sur un ordinateur, la plupart des parents
 * ne savent simplement pas comment faire.
 *
 * Trente choix suffisent, et ils sont là pour que l'enfant se reconnaisse :
 * des animaux d'abord, parce que c'est ce qu'un enfant choisit en premier.
 */

const FAMILLES: Array<{ nom: string; emojis: string[] }> = [
  {
    nom: 'Animaux',
    emojis: ['🦁', '🐯', '🐘', '🦒', '🦓', '🐼', '🐨', '🦊', '🐢', '🦜', '🐝', '🦋'],
  },
  {
    nom: 'Visages',
    emojis: ['😀', '😎', '🤓', '🥳', '😺', '🤖', '👧', '👦', '🧒'],
  },
  {
    nom: 'Choses',
    emojis: ['⚽', '🏀', '🎨', '🎸', '🚀', '⭐', '🌍', '📚', '🏆'],
  },
];

export default function ChoixEmoji({
  valeur,
  onChange,
}: {
  valeur: string;
  onChange: (emoji: string) => void;
}) {
  return (
    <div>
      <div className="flex items-center gap-4">
        <span
          aria-hidden="true"
          className="grid h-20 w-20 shrink-0 place-items-center rounded-full bg-gold/30 text-5xl"
        >
          {valeur}
        </span>
        <p className="text-sm text-muted">
          C’est le visage qu’il verra sur son écran, et vous aussi dans la liste de vos enfants.
        </p>
      </div>

      <div className="mt-4 grid gap-4">
        {FAMILLES.map((famille) => (
          <div key={famille.nom}>
            <p className="mb-2 text-sm font-bold text-muted">{famille.nom}</p>
            <div
              role="radiogroup"
              aria-label={`Emojis — ${famille.nom}`}
              className="flex flex-wrap gap-2"
            >
              {famille.emojis.map((e) => {
                const choisi = e === valeur;
                return (
                  <button
                    key={e}
                    type="button"
                    role="radio"
                    aria-checked={choisi}
                    aria-label={e}
                    onClick={() => onChange(e)}
                    className={
                      'tuile grid h-12 w-12 place-items-center rounded-2xl border-2 text-2xl transition ' +
                      (choisi
                        ? 'border-clay bg-gold/25'
                        : 'border-line bg-white-warm hover:border-ink-2')
                    }
                  >
                    {e}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
