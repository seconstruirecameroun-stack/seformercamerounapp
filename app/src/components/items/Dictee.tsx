import { useEffect, useRef, useState } from 'react';
import { Button } from '../ui';
import { Enonce, memePhrase } from './partage';
import type { Props } from './partage';
import { lire, peutParler, stopper } from '../../lib/voix';

/**
 * La dictée : on entend, on écrit.
 *
 * Les deux emplois du temps de l'école réservent des créneaux à la dictée —
 * « spelling and dictation », « Français (NCBS dictée) ». La synthèse du
 * navigateur permet de la faire ici sans réseau et sans un centime.
 *
 * La phrase se répète autant de fois que l'enfant le demande : une dictée
 * d'école se relit aussi, et refuser la répétition ne mesurerait que la
 * mémoire immédiate.
 *
 * La correction pardonne la casse, les espaces et le point final, mais pas
 * les accents : c'est justement ce qu'on apprend.
 */
export default function Dictee({ item, onRepondre, verrouille, visuel }: Props) {
  const payload = item.payload as { phrase: string; langue?: string };
  const [saisie, setSaisie] = useState('');
  const [ecoutes, setEcoutes] = useState(0);
  const champ = useRef<HTMLTextAreaElement>(null);

  const dire = () => {
    lire(payload.phrase, payload.langue ?? 'fr');
    setEcoutes((n) => n + 1);
  };

  // La phrase est dite en arrivant : sans cela, l'enfant regarde un champ
  // vide sans savoir qu'il doit appuyer sur un bouton.
  useEffect(() => {
    dire();
    return stopper;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [item.id]);

  if (!peutParler()) {
    return (
      <p className="text-kid-sm text-muted">
        Cet appareil ne sait pas lire à voix haute. La dictée reviendra sur un autre écran.
      </p>
    );
  }

  return (
    <>
      <Enonce visuel={visuel}>Écoute, puis écris la phrase</Enonce>

      <button
        type="button"
        onClick={dire}
        disabled={verrouille}
        className="tuile mt-5 flex min-h-[72px] w-full items-center justify-center gap-3 rounded-[var(--radius-tile)] border-2 border-line bg-white-warm text-kid-lg font-extrabold shadow-[var(--shadow-tile)] disabled:opacity-50"
      >
        <span aria-hidden="true" className="text-kid-2xl">
          🔊
        </span>
        {ecoutes <= 1 ? 'Écouter' : 'Réécouter'}
      </button>

      <textarea
        ref={champ}
        className="mt-3 w-full rounded-[var(--radius-tile)] border-2 border-line bg-sand/40 px-4 py-3 text-kid leading-relaxed outline-none focus:border-clay disabled:opacity-70"
        rows={2}
        value={saisie}
        disabled={verrouille}
        onChange={(e) => setSaisie(e.target.value)}
        placeholder="Écris ici…"
        aria-label="La phrase entendue"
      />

      {verrouille ? (
        <p className="mt-3 text-kid-sm text-ink-2">
          La phrase était : <strong>{payload.phrase}</strong>
        </p>
      ) : (
        <Button
          className="mt-3"
          disabled={saisie.trim() === ''}
          onClick={() =>
            onRepondre({
              correct: memePhrase(saisie, payload.phrase),
              donnee: { phrase: saisie.trim(), ecoutes },
            })
          }
        >
          Vérifier
        </Button>
      )}
    </>
  );
}
