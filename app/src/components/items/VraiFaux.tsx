import { useState } from 'react';
import { Enonce } from './partage';
import type { Props } from './partage';

/**
 * Vrai ou faux.
 *
 * Deux cibles énormes, une décision immédiate : c'est le type le plus rapide
 * à jouer, et celui qui tient le mieux dans une série.
 *
 * Son défaut est connu : une chance sur deux au hasard. On ne le pose donc
 * qu'en compagnie d'autres types dans la même séance, jamais seul pour
 * valider une notion.
 */
export default function VraiFaux({ item, onRepondre, verrouille, visuel }: Props) {
  const payload = item.payload as { statement: string };
  const attendu = (item.answer as { value: boolean }).value;
  const [choisi, setChoisi] = useState<boolean | null>(null);

  const cases = [
    { valeur: true, libelle: 'VRAI', icone: '✓' },
    { valeur: false, libelle: 'FAUX', icone: '✗' },
  ];

  return (
    <>
      <Enonce visuel={visuel}>{payload.statement}</Enonce>

      <div className="mt-6 grid grid-cols-2 gap-3">
        {cases.map((c) => {
          const estBonne = verrouille && c.valeur === attendu;
          const estRate = verrouille && c.valeur === choisi && c.valeur !== attendu;
          return (
            <button
              key={c.libelle}
              type="button"
              disabled={verrouille}
              onClick={() => {
                setChoisi(c.valeur);
                onRepondre({ correct: c.valeur === attendu, donnee: { value: c.valeur } });
              }}
              className={
                'tuile flex min-h-[96px] flex-col items-center justify-center gap-1 rounded-[var(--radius-tile)] border-2 text-kid-xl font-black shadow-[var(--shadow-tile)] ' +
                (estBonne
                  ? 'border-leaf bg-leaf/20 text-leaf'
                  : estRate
                    ? 'border-clay bg-clay/15 text-clay-dark'
                    : verrouille
                      ? 'border-line bg-white-warm opacity-55'
                      : 'border-line bg-white-warm hover:border-ink-2')
              }
            >
              <span aria-hidden="true" className="text-kid-2xl">
                {c.icone}
              </span>
              {c.libelle}
            </button>
          );
        })}
      </div>
    </>
  );
}
