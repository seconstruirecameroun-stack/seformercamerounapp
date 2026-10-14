import { useRef, useState } from 'react';
import Illustration, { sourceIllustration } from '../../components/Illustration';
import { lire, peutParler, stopper } from '../../lib/voix';
import { NIVEAU_ACQUIS } from '../../lib/dashboard';
import type { ExplanationRow, NotionRow } from '../../types/db';

/**
 * La leçon, en fiches.
 *
 * Elle était une liste de sept cartes empilées : l'enfant la faisait défiler
 * sans rien regarder. Une fiche à la fois, qu'on fait glisser, tient
 * l'attention et donne un rythme — et le bouton pour jouer reste sous le
 * pouce, parce que l'apprentissage n'est pas une salle d'attente.
 *
 * Le film et le résumé sont les deux premières fiches : c'est la même
 * matière, elle n'a pas à vivre dans des blocs séparés au-dessus. Le lecteur
 * vidéo, surtout, occupait la moitié de l'écran sans rien montrer tant qu'on
 * ne l'avait pas lancé.
 */

const REGISTRES: Record<string, string> = {
  simple: 'En deux mots',
  analogie: 'C’est comme…',
  histoire: 'Une petite histoire',
  visuel: 'À imaginer',
  pas_a_pas: 'Pas à pas',
};

type NotionFiche = NotionRow & { explanations: ExplanationRow[] };

type Film = { url: string; poster: string | null; duree: number | null };

export default function Fiches({
  film,
  resume,
  illustration,
  notions,
  langue,
  niveaux,
  onJouer,
}: {
  film: Film | null;
  resume: string | null;
  illustration: string | null;
  notions: NotionFiche[];
  langue: string;
  niveaux: Map<string, number>;
  onJouer: () => void;
}) {
  type Fiche = 'film' | 'resume' | NotionFiche;
  const fiches: Fiche[] = [
    ...(film ? (['film'] as Fiche[]) : []),
    ...(resume ? (['resume'] as Fiche[]) : []),
    ...notions,
  ];
  const [joue, setJoue] = useState(false);
  const [index, setIndex] = useState(0);
  const [sens, setSens] = useState(18);
  const [registre, setRegistre] = useState(0);
  const depart = useRef<number | null>(null);

  function aller(pas: number) {
    const cible = index + pas;
    if (cible < 0 || cible >= fiches.length) return;
    stopper();
    setSens(pas > 0 ? 18 : -18);
    setRegistre(0);
    setIndex(cible);
  }

  const fiche = fiches[index];
  const notion = typeof fiche === 'string' ? null : fiche;
  const explications = notion?.explanations ?? [];
  const courante = explications.length > 0 ? explications[registre % explications.length] : null;
  const acquise = notion ? (niveaux.get(notion.id) ?? 1) >= NIVEAU_ACQUIS : false;
  const aLire = notion ? notion.statement + '. ' + (courante?.body ?? '') : (resume ?? '');

  // Changer de fiche coupe le film : deux sons ne doivent pas se superposer.
  if (fiche !== 'film' && joue) setJoue(false);

  return (
    <section
      onTouchStart={(e) => (depart.current = e.changedTouches[0].clientX)}
      onTouchEnd={(e) => {
        if (depart.current === null) return;
        const ecart = e.changedTouches[0].clientX - depart.current;
        depart.current = null;
        if (Math.abs(ecart) > 50) aller(ecart < 0 ? 1 : -1);
      }}
    >
      <ol className="mb-3 flex justify-center gap-1.5" aria-label="Fiches de la leçon">
        {fiches.map((_, i) => (
          <li
            key={i}
            className={
              'h-2 rounded-full transition-all duration-300 ' +
              (i === index ? 'w-6 bg-clay' : i < index ? 'w-2 bg-gold' : 'w-2 bg-line')
            }
          />
        ))}
      </ol>

      <article
        key={index}
        className="carte-entre overflow-hidden rounded-[var(--radius-card)] bg-white-warm shadow-[var(--shadow-card)]"
        style={{ ['--sens' as string]: `${sens}px` }}
      >
        {fiche === 'film' && film ? (
          joue ? (
            <video
              autoPlay
              controls
              playsInline
              poster={sourceIllustration(film.poster) ?? undefined}
              src={film.url}
              className="w-full"
            />
          ) : (
            <button
              type="button"
              onClick={() => setJoue(true)}
              className="relative block w-full"
              aria-label="Lancer le film"
            >
              <img
                src={sourceIllustration(film.poster) ?? undefined}
                alt=""
                width={960}
                height={540}
                loading="lazy"
                className="h-48 w-full object-cover"
              />
              <span className="absolute inset-0 grid place-items-center bg-ink/25">
                <span className="grid h-16 w-16 place-items-center rounded-full bg-clay text-2xl text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]">
                  ▶
                </span>
              </span>
              <span className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/80 to-transparent px-4 pt-8 pb-3 text-left text-kid-sm font-black text-white-warm">
                Le film · {film.duree ?? 0} s
              </span>
            </button>
          )
        ) : notion ? (
          <>
            <div className="relative bg-sand/50">
              <Illustration
                cle={notion.illustration}
                forme="objet"
                alt=""
                className="mx-auto h-40 w-40 object-contain"
              />
              {acquise ? (
                <span className="absolute top-3 right-3 grid h-9 w-9 place-items-center rounded-full bg-gold text-base">
                  ★
                </span>
              ) : null}
            </div>
            <div className="px-5 py-5">
              <h2 className="text-kid-lg leading-snug font-black text-balance">
                {notion.statement}
              </h2>
              {courante ? (
                <>
                  <p className="mt-3 text-xs font-black tracking-wide text-clay-dark uppercase">
                    {REGISTRES[courante.register] ?? 'Explication'}
                  </p>
                  <p className="mt-1 text-kid leading-relaxed text-ink-2">{courante.body}</p>
                </>
              ) : null}
            </div>
          </>
        ) : (
          <>
            <Illustration
              cle={illustration}
              forme="scene"
              alt=""
              className="h-36 w-full object-cover"
            />
            <div className="px-5 py-5">
              <p className="text-xs font-black tracking-widest text-clay-dark uppercase">
                À retenir
              </p>
              <p className="mt-2 text-kid leading-relaxed">{resume}</p>
            </div>
          </>
        )}

        <div
          className={
            'flex flex-wrap gap-2 px-5 py-3 ' +
            (fiche === 'film' ? 'hidden' : 'border-t border-line')
          }
        >
          {peutParler() ? (
            <button
              type="button"
              onClick={() => lire(aLire, langue)}
              className="tuile inline-flex min-h-[44px] items-center gap-1.5 rounded-full border-2 border-line px-4 text-kid-sm font-bold"
            >
              <span aria-hidden="true">🔊</span> Écouter
            </button>
          ) : null}
          {explications.length > 1 ? (
            <button
              type="button"
              onClick={() => {
                stopper();
                setRegistre(registre + 1);
              }}
              className="tuile inline-flex min-h-[44px] items-center rounded-full bg-clay/12 px-4 text-kid-sm font-bold text-clay-dark"
            >
              Explique autrement
            </button>
          ) : null}
        </div>
      </article>

      <div className="mt-3 flex items-center gap-2">
        <button
          type="button"
          onClick={() => aller(-1)}
          disabled={index === 0}
          aria-label="Fiche précédente"
          className="tuile grid h-14 w-14 shrink-0 place-items-center rounded-full border-2 border-line bg-white-warm text-xl font-black disabled:opacity-35"
        >
          ←
        </button>

        {index < fiches.length - 1 ? (
          <button
            type="button"
            onClick={() => aller(1)}
            className="tuile min-h-[56px] flex-1 rounded-full bg-ink text-kid font-extrabold text-white-warm"
          >
            Suivant
          </button>
        ) : (
          <button
            type="button"
            onClick={() => {
              stopper();
              onJouer();
            }}
            className="tuile min-h-[56px] flex-1 rounded-full bg-clay text-kid font-extrabold text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]"
          >
            Jouer maintenant
          </button>
        )}
      </div>

      {index < fiches.length - 1 ? (
        <button
          type="button"
          onClick={() => {
            stopper();
            onJouer();
          }}
          className="mx-auto mt-3 block text-kid-sm font-bold text-clay underline"
        >
          Passer et jouer
        </button>
      ) : null}
    </section>
  );
}
