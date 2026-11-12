import { useState } from 'react';
import Ceremonie from './Ceremonie';
import Palmares from './Palmares';
import DialogueJeu, { momentFort, type Dialogue } from '../jeu/DialogueJeu';
import type { CompositionRow } from '../../lib/composition';

/**
 * Les récompenses des compositions, sur le banc d'essai.
 *
 * La cérémonie du bulletin avec quatre notes au choix, les moments forts de
 * Niba à la demande, et une vitrine de médailles faite de copies inventées.
 * Rien n'est lu ni écrit dans la base.
 */

const NOTES = [
  { nom: '28/30 · or', points: 28 },
  { nom: '23/30 · argent', points: 23 },
  { nom: '18/30 · bronze', points: 18 },
  { nom: '12/30 · rien', points: 12 },
];

const MOMENTS: Array<{ nom: string; fabrique: () => Dialogue }> = [
  { nom: 'Série de 3', fabrique: () => momentFort('serie', 'SÉRIE DE 3 !', 'Tes points du plateau comptent double !') },
  { nom: 'Exercice parfait', fabrique: () => momentFort('parfait', 'EXERCICE PARFAIT !', '5 sur 5 : un coup bonus pour toi !') },
  { nom: 'Mention assurée', fabrique: () => momentFort('mention', 'A ASSURÉ !', 'Personne ne peut plus te l’enlever. Vise plus haut !') },
  { nom: 'Plus que 3', fabrique: () => momentFort('fin', 'PLUS QUE 3 !', 'Dernière ligne droite : garde ta série !') },
];

const fausseCopie = (id: string, justes: number, jour: number): CompositionRow => ({
  id, parent_id: '', child_id: '', titre: 'Essai ' + id, lessons: [],
  questions: Array.from({ length: 26 }, (_, i) => 'q' + i),
  commencee_le: null, finie_le: `2026-11-${String(jour).padStart(2, '0')}T10:00:00Z`, justes,
  created_at: '2026-11-12T10:00:00Z',
});

export default function RecompensesDEssai() {
  const [choix, setChoix] = useState(0);
  const [tour, setTour] = useState(0);
  const [moment, setMoment] = useState<Dialogue | null>(null);
  const exercices = [
    { numero: 1, titre: 'Le féminin des noms', eus: 7, sur: 7 },
    { numero: 2, titre: 'Le groupe du verbe', eus: 6, sur: 8 },
    { numero: 3, titre: 'Les homonymes', eus: 0, sur: 11 },
  ];
  // Les lignes suivent la note choisie : l'oral plein, le reste réparti.
  const pts = NOTES[choix].points;
  const ecrit = pts - 4;
  let reste = ecrit;
  const lignes = exercices.map((e) => {
    const eus = Math.max(0, Math.min(e.sur, reste));
    reste -= eus;
    return { ...e, eus };
  });

  return (
    <section className="mt-3 grid gap-4">
      <DialogueJeu dernier={moment} />

      <div>
        <h2 className="text-kid-sm font-black">Les moments forts de Niba</h2>
        <div className="mt-2 grid grid-cols-2 gap-2">
          {MOMENTS.map((m) => (
            <button
              key={m.nom}
              type="button"
              onClick={() => setMoment(m.fabrique())}
              className="min-h-11 rounded-full bg-ink px-3 py-2 text-kid-xs font-black text-white-warm"
            >
              {m.nom}
            </button>
          ))}
        </div>
      </div>

      <div>
        <h2 className="text-kid-sm font-black">La remise du bulletin</h2>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {NOTES.map((n, i) => (
            <button
              key={n.nom}
              type="button"
              onClick={() => { setChoix(i); setTour((t) => t + 1); }}
              className={
                'rounded-full border-2 px-3 py-1 text-kid-xs font-black ' +
                (i === choix ? 'border-ink bg-ink text-white-warm' : 'border-line bg-white-warm')
              }
            >
              {n.nom}
            </button>
          ))}
        </div>
        <div className="mt-3">
          <Ceremonie key={tour} oral={4} surOral={4} exercices={lignes} points={pts} total={30} />
        </div>
      </div>

      <div>
        <h2 className="text-kid-sm font-black">La vitrine, sur la page de l’enfant</h2>
        <div className="mt-2">
          <Palmares
            compositions={[fausseCopie('a', 23, 1), fausseCopie('b', 28, 2), fausseCopie('c', 25, 3)]}
          />
        </div>
      </div>
    </section>
  );
}
