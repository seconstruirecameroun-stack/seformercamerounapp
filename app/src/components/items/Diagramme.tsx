import { useRef, useState } from 'react';
import {
  DEHORS,
  disposition,
  memeRangement,
  posees,
  regionDuPoint,
  type Rangement,
} from '../../lib/diagramme';
import { useMelange } from '../../lib/melange';
import { Enonce } from './partage';
import type { Props } from './partage';

/**
 * Ranger les éléments dans les régions d'un diagramme.
 *
 * C'est l'exercice du cahier, enfin jouable : « draw a venn diagram and
 * represent sets A, B and C ». Jusqu'ici on pouvait lui demander **où** va
 * le 15 ; maintenant il le **pose**, et c'est ce geste-là que ses ratures
 * montrent qu'il rate.
 *
 * On relie par deux touchers, comme pour l'association et pour les lettres
 * mobiles : prendre une étiquette, puis toucher la région. Jamais de
 * glisser-déposer — sur un téléphone, un doigt qui traîne fait défiler la
 * page.
 *
 * La région touchée n'est pas devinée : elle est calculée depuis les
 * disques, dans lib/diagramme.ts, et chaque ancre y est prouvée tomber dans
 * sa propre région. Sans cela, un élément affiché au milieu aurait pu être
 * enregistré ailleurs.
 */
export default function Diagramme({ item, onRepondre, verrouille, visuel }: Props) {
  const payload = item.payload as { question: string; sets: string[]; elements: string[] };
  const attendu = (item.answer as { regions: Rangement }).regions;

  const d = disposition(payload.sets);
  const [range, setRange] = useState<Rangement>({});
  const [pris, setPris] = useState<string | null>(null);
  const svg = useRef<SVGSVGElement | null>(null);

  // Le tiroir sort dans un ordre tiré à chaque fois : rangé dans l-ordre de
  // l-énoncé, il suffirait de le vider de gauche à droite en suivant les
  // régions de gauche à droite.
  const ordre = useMelange(payload.elements.length);
  const dejaPosees = posees(range);
  const tiroir = ordre.map((i) => payload.elements[i]).filter((e) => !dejaPosees.includes(e));

  function poser(region: string) {
    if (verrouille || pris === null) return;
    const suite: Rangement = {};
    for (const [cle, liste] of Object.entries(range)) suite[cle] = liste.filter((e) => e !== pris);
    suite[region] = [...(suite[region] ?? []), pris];
    setPris(null);
    setRange(suite);
    if (posees(suite).length === payload.elements.length) {
      onRepondre({ correct: memeRangement(suite, attendu), donnee: { regions: suite } });
    }
  }

  function reprendre(element: string) {
    if (verrouille) return;
    const suite: Rangement = {};
    for (const [cle, liste] of Object.entries(range)) suite[cle] = liste.filter((e) => e !== element);
    setRange(suite);
    setPris(element);
  }

  function toucher(e: React.MouseEvent<SVGSVGElement>) {
    if (!svg.current || pris === null) return;
    const r = svg.current.getBoundingClientRect();
    const region = regionDuPoint(d, {
      x: ((e.clientX - r.left) / r.width) * d.largeur,
      y: ((e.clientY - r.top) / r.height) * d.hauteur,
    });
    if (region) poser(region);
  }

  /** La région où cet élément aurait dû aller. */
  const bonneRegion = (element: string) =>
    Object.entries(attendu).find(([, liste]) => liste.includes(element))?.[0] ?? DEHORS;

  const pastille = (element: string, region: string, i: number, total: number) => {
    const juste = verrouille ? bonneRegion(element) === region : null;
    const ancre = d.ancres[region];
    const ecart = 23;
    return (
      <button
        key={element}
        type="button"
        disabled={verrouille}
        onClick={(e) => {
          e.stopPropagation();
          reprendre(element);
        }}
        style={{
          left: `${((ancre.x - (ecart * (total - 1)) / 2 + i * ecart) / d.largeur) * 100}%`,
          top: `${(ancre.y / d.hauteur) * 100}%`,
        }}
        className={
          'absolute -translate-x-1/2 -translate-y-1/2 rounded-lg border-2 px-1.5 py-0.5 ' +
          'text-kid-xs font-black shadow-[var(--shadow-tile)] ' +
          (juste === null
            ? 'border-ink bg-white-warm text-ink'
            : juste
              ? 'border-leaf bg-leaf text-white-warm'
              : 'border-clay bg-clay text-white-warm')
        }
      >
        {element}
      </button>
    );
  };

  return (
    <>
      <Enonce visuel={visuel}>{payload.question}</Enonce>
      <p className="mt-1 text-kid-sm text-muted">
        {pris === null
          ? 'Touche une étiquette, puis la région où elle va.'
          : `Où va ${pris} ? Touche la région.`}
      </p>

      <div className="relative mt-4">
        <svg
          ref={svg}
          viewBox={`0 0 ${d.largeur} ${d.hauteur}`}
          className={'w-full ' + (pris === null ? '' : 'cursor-pointer')}
          onClick={toucher}
        >
          <rect
            x={d.cadre.x}
            y={d.cadre.y}
            width={d.cadre.w}
            height={d.cadre.h}
            rx={10}
            className="fill-[var(--color-white-warm)] stroke-[var(--color-ink)]"
            strokeWidth={3}
          />
          <text x={d.cadre.x + 16} y={d.cadre.y + 24} className="fill-[var(--color-ink-2)]" fontSize={17}>
            U
          </text>
          {d.cercles.map((c, i) => (
            <circle
              key={c.nom}
              cx={c.cx}
              cy={c.cy}
              r={c.r}
              className={
                'stroke-[var(--color-ink)] ' +
                ['fill-sky/45', 'fill-gold/40', 'fill-mint/45'][i % 3]
              }
              strokeWidth={3}
            />
          ))}
          {d.etiquettes.map((e, i) => (
            <text
              key={payload.sets[i]}
              x={e.x}
              y={e.y}
              textAnchor="middle"
              className="fill-[var(--color-ink)] font-black"
              fontSize={19}
            >
              {payload.sets[i]}
            </text>
          ))}
        </svg>

        {Object.entries(range).map(([region, liste]) =>
          liste.map((element, i) => pastille(element, region, i, liste.length)),
        )}
      </div>

      {verrouille ? (
        <div className="mt-3 grid gap-1 text-kid-sm text-ink-2">
          {Object.entries(attendu)
            .filter(([, liste]) => liste.length > 0)
            .map(([region, liste]) => (
              <p key={region}>
                <strong>{region === DEHORS ? 'Hors des ovales' : region}</strong> : {liste.join(', ')}
              </p>
            ))}
        </div>
      ) : (
        <>
          <div className="mt-4 flex flex-wrap justify-center gap-2 rounded-[var(--radius-tile)] border-2 border-dashed border-line bg-sand/40 p-3">
            {tiroir.length === 0 && pris === null ? (
              <p className="text-kid-sm text-muted">Tout est posé.</p>
            ) : (
              tiroir.map((element) => (
                <button
                  key={element}
                  type="button"
                  onClick={() => setPris(pris === element ? null : element)}
                  className={
                    'tuile min-h-[44px] rounded-xl border-2 px-3 text-kid font-black shadow-[var(--shadow-tile)] ' +
                    (pris === element
                      ? 'border-ink bg-sand text-ink'
                      : 'border-line bg-white-warm text-ink active:bg-sand')
                  }
                >
                  {element}
                </button>
              ))
            )}
          </div>

          {dejaPosees.length > 0 ? (
            <button
              type="button"
              className="mt-3 text-kid-sm font-bold text-clay underline"
              onClick={() => {
                setRange({});
                setPris(null);
              }}
            >
              Tout remettre
            </button>
          ) : null}
        </>
      )}
    </>
  );
}
