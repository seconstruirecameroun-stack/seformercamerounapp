import { useState } from 'react';
import CourseJouable, { type Resume } from './CourseJouable';

/**
 * La course de KLEIN, sur le banc d'essai.
 *
 * Aucune question n'est posée ici : deux boutons font ce que feront plus tard
 * les bonnes réponses — un turbo pour une réponse juste, un bouclier pour une
 * série sans faute. On éprouve le jeu lui-même, sur un vrai téléphone, sans
 * écrire une ligne dans le journal d'un enfant.
 */

export default function CourseDEssai() {
  const [numero, setNumero] = useState(0);
  const [turbos, setTurbos] = useState(0);
  const [boucliers, setBoucliers] = useState(0);
  const [question, setQuestion] = useState(false);
  const [resume, setResume] = useState<Resume | null>(null);

  return (
    <section className="mt-3">
      <CourseJouable
        key={numero}
        actif={!question}
        turbos={turbos}
        boucliers={boucliers}
        onResume={setResume}
      />

      <p className="mt-2 text-center text-kid-xs font-bold text-muted tabular-nums">
        {resume
          ? `${resume.pieces} pièces · ${resume.esquives} obstacles évités · ${resume.chocs} choc${resume.chocs > 1 ? 's' : ''}`
          : 'Touche à gauche ou à droite de la route.'}
      </p>

      <div className="mt-3 grid grid-cols-2 gap-2">
        <button
          type="button"
          onClick={() => setTurbos((n) => n + 1)}
          className="min-h-12 rounded-full bg-clay px-3 py-2 text-kid-sm font-black text-white-warm shadow-[inset_0_-3px_0_rgb(0_0_0/0.18)]"
        >
          Bonne réponse → turbo
        </button>
        <button
          type="button"
          onClick={() => setBoucliers((n) => n + 1)}
          className="min-h-12 rounded-full bg-sky px-3 py-2 text-kid-sm font-black text-ink shadow-[inset_0_-3px_0_rgb(0_0_0/0.12)]"
        >
          Série sans faute → bouclier
        </button>
      </div>

      <button
        type="button"
        onClick={() => setQuestion((q) => !q)}
        className="mt-3 min-h-11 w-full rounded-full border-2 border-line px-3 py-2 text-kid-xs font-black text-ink-2"
      >
        {question ? 'Fin de la question : c’est à moi de conduire' : 'Pendant une question : la voiture roule seule'}
      </button>

      <button
        type="button"
        onClick={() => {
          setNumero((n) => n + 1);
          setTurbos(0);
          setBoucliers(0);
          setResume(null);
        }}
        className="mt-3 w-full rounded-full border-2 border-clay px-3 py-2 text-kid-xs font-black text-clay-dark"
      >
        Nouvelle route
      </button>
    </section>
  );
}
