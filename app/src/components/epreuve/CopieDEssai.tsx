import { Bulletin, EnTeteDeCopie, SituationProbleme } from './Copie';
import { matiereDeLEpreuve, situationProbleme, type LeconDEpreuve } from '../../lib/epreuve';

/**
 * Une copie d'essai, sur le banc.
 *
 * L'en-tête, la situation problème et le bulletin d'une épreuve sur 30, avec
 * des leçons et des points inventés : de quoi regarder la copie sans qu'une
 * composition existe et sans qu'un enfant y ait répondu. La situation est
 * fabriquée par le même code que dans la salle.
 */

const LECONS: LeconDEpreuve[] = [
  { id: 'a', title: 'Les noms propres et les noms communs', matiere: 'Français' },
  { id: 'b', title: 'Le féminin des noms', matiere: 'Français' },
  { id: 'c', title: 'L’infinitif et les trois groupes de verbes', matiere: 'Français' },
  { id: 'd', title: 'Le champ lexical de la ville et du village', matiere: 'Français' },
];

export default function CopieDEssai() {
  const situation = situationProbleme('banc-d-essai', 'CE1', LECONS);
  return (
    <section className="mt-3">
      <p className="text-center text-kid-xs font-black tracking-wide text-clay-dark">
        COMPOSITION · SUR 30 POINTS
      </p>
      <div className="mt-3">
        <EnTeteDeCopie
          nom="KLEIN"
          date="12 novembre 2026"
          classe="CE1"
          epreuve={matiereDeLEpreuve(LECONS)}
        />
      </div>
      <div className="mt-4">
        <SituationProbleme texte={situation.texte} oral={situation.oral.length} ecrit={26} />
      </div>

      <p className="mt-6 text-center text-kid-xs font-black tracking-wide text-clay-dark">
        À LA FIN : LE BULLETIN
      </p>
      <div className="mt-3">
        <Bulletin
          oral={4}
          surOral={4}
          ecrit={24}
          surEcrit={26}
          exercices={[
            { numero: 1, titre: LECONS[0].title, eus: 7, sur: 7 },
            { numero: 2, titre: LECONS[1].title, eus: 7, sur: 7 },
            { numero: 3, titre: LECONS[2].title, eus: 4, sur: 6 },
            { numero: 4, titre: LECONS[3].title, eus: 6, sur: 6 },
          ]}
        />
      </div>
    </section>
  );
}
