import { useState } from 'react';
import CourseJouable, { type Resume } from './CourseJouable';

/**
 * La course de KLEIN, sur le banc d'essai.
 *
 * Aucune question n'est posée ici : trois boutons font ce que feront plus
 * tard les réponses — un turbo pour une réponse juste, un choc pour une
 * erreur, un bouclier pour une série sans faute. L'enfant, lui, ne touchera
 * jamais la route. On éprouve le jeu sans écrire une ligne dans le journal
 * d'un enfant.
 */

export default function CourseDEssai() {
  const [numero, setNumero] = useState(0);
  const [turbos, setTurbos] = useState(0);
  const [boucliers, setBoucliers] = useState(0);
  const [erreurs, setErreurs] = useState(0);
  const [resume, setResume] = useState<Resume | null>(null);

  return (
    <section className="mt-3">
      <CourseJouable
        key={numero}
        turbos={turbos}
        erreurs={erreurs}
        boucliers={boucliers}
        onResume={setResume}
      />

      <p className="mt-2 text-center text-kid-xs font-bold text-muted tabular-nums">
        {resume
          ? `${resume.pieces} pièce${resume.pieces > 1 ? 's' : ''} · ${resume.esquives} obstacle${resume.esquives > 1 ? 's' : ''} évité${resume.esquives > 1 ? 's' : ''} · ${resume.chocs} choc${resume.chocs > 1 ? 's' : ''}`
          : 'La voiture roule seule. Les boutons jouent les réponses.'}
      </p>

      <div className="mt-3 grid grid-cols-2 gap-2">
        <button
          type="button"
          onClick={() => setTurbos((n) => n + 1)}
          className="min-h-12 rounded-full bg-leaf px-3 py-2 text-kid-sm font-black text-white-warm shadow-[inset_0_-3px_0_rgb(0_0_0/0.18)]"
        >
          Bonne réponse → turbo
        </button>
        <button
          type="button"
          onClick={() => setErreurs((n) => n + 1)}
          className="min-h-12 rounded-full bg-clay px-3 py-2 text-kid-sm font-black text-white-warm shadow-[inset_0_-3px_0_rgb(0_0_0/0.18)]"
        >
          Mauvaise réponse → choc
        </button>
      </div>
      <button
        type="button"
        onClick={() => setBoucliers((n) => n + 1)}
        className="mt-2 min-h-12 w-full rounded-full bg-sky px-3 py-2 text-kid-sm font-black text-ink shadow-[inset_0_-3px_0_rgb(0_0_0/0.12)]"
      >
        Série sans faute → bouclier
      </button>

      <button
        type="button"
        onClick={() => {
          setNumero((n) => n + 1);
          setTurbos(0);
          setBoucliers(0);
          setErreurs(0);
          setResume(null);
        }}
        className="mt-3 w-full rounded-full border-2 border-clay px-3 py-2 text-kid-xs font-black text-clay-dark"
      >
        Nouvelle route
      </button>
    </section>
  );
}
