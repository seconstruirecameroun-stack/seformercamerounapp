import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { chargerTableauDeBord } from '../../lib/dashboard';
import { PALIERS } from '../../lib/paliers';
import type { Autocollant, LeconResume } from '../../lib/dashboard';
import Illustration from '../../components/Illustration';
import { ErrorNote, Loading } from '../../components/ui';

const JOURS = ['D', 'L', 'M', 'M', 'J', 'V', 'S'];

/** Les sept derniers jours, du plus ancien à aujourd'hui. */
function derniersJours(): Array<{ cle: string; lettre: string; aujourdhui: boolean }> {
  const sortie = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    sortie.push({
      cle: d.toISOString().slice(0, 10),
      lettre: JOURS[d.getDay()],
      aujourdhui: i === 0,
    });
  }
  return sortie;
}

function Semaine({ jours, serie }: { jours: string[]; serie: number }) {
  const faits = new Set(jours);
  return (
    <section className="rounded-[var(--radius-card)] border border-line bg-white-warm/80 px-4 py-3">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-kid-sm font-extrabold">Ta semaine</h2>
        <span className="text-kid-sm font-bold text-muted">
          {serie > 0 ? `${serie} jour${serie > 1 ? 's' : ''} !` : 'À toi de jouer'}
        </span>
      </div>
      <ol className="mt-2 flex justify-between gap-1">
        {derniersJours().map((jour) => {
          const fait = faits.has(jour.cle);
          return (
            <li key={jour.cle} className="flex flex-1 flex-col items-center gap-1">
              <span
                className={
                  'grid h-9 w-full max-w-11 place-items-center rounded-xl text-kid-sm font-black ' +
                  (fait
                    ? 'bg-gold text-ink'
                    : jour.aujourdhui
                      ? 'border-2 border-dashed border-gold/70 text-muted'
                      : 'bg-line/60 text-muted')
                }
              >
                {fait ? '★' : jour.lettre}
              </span>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

/**
 * Où en est l'enfant dans cette leçon : l'escalier, et la marche en cours.
 *
 * Le pourcentage de notions acquises qui figurait ici ne disait rien à un
 * enfant — il ne voyait ni où il était, ni ce qu'il visait.
 */
function CarteLecon({ lecon, childId }: { lecon: LeconResume; childId: string }) {
  const part =
    lecon.etapeTotal > 0 ? Math.round((lecon.etapeFaites / lecon.etapeTotal) * 100) : 0;
  return (
    <Link
      to={`/enfant/${childId}/lecon/${lecon.id}`}
      className="tuile flex items-center gap-3 overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm p-2 pr-4 shadow-[var(--shadow-tile)]"
    >
      <Illustration
        cle={lecon.illustration}
        forme="scene"
        alt=""
        className="h-20 w-28 shrink-0 rounded-2xl object-cover"
      />
      <div className="min-w-0 flex-1">
        <p className="text-kid-xs font-black tracking-wide text-muted uppercase">
          {lecon.matiere ?? 'Leçon'}
        </p>
        <h3 className="line-clamp-2 text-kid font-extrabold">{lecon.title}</h3>
        <div className="mt-1.5 flex items-center gap-2">
          <span className="flex shrink-0 items-center gap-1" aria-hidden="true">
            {[1, 2, 3].map((n) => (
              <span
                key={n}
                className={
                  'grid h-5 w-5 place-items-center rounded-full text-[0.7rem] font-black ' +
                  (lecon.etapeTerminee || n < lecon.etape
                    ? 'bg-leaf text-white-warm'
                    : n === lecon.etape
                      ? 'bg-gold text-ink'
                      : 'bg-line text-muted')
                }
              >
                {lecon.etapeTerminee || n < lecon.etape ? '★' : n}
              </span>
            ))}
          </span>
          <span className="h-2 flex-1 overflow-hidden rounded-full bg-ink/15">
            <span
              className="block h-full rounded-full bg-gold transition-all duration-500"
              style={{ width: `${part}%` }}
            />
          </span>
        </div>
        <p className="mt-1 text-kid-xs font-bold text-muted">
          {lecon.etapeTerminee
            ? 'Leçon terminée — tu révises'
            : `Étape ${lecon.etape} · ${lecon.etapeFaites}/${lecon.etapeTotal}`}
        </p>
      </div>
      {lecon.dues > 0 ? (
        <span className="grid h-7 min-w-7 shrink-0 place-items-center rounded-full bg-clay px-2 text-kid-xs font-black text-white-warm">
          {lecon.dues}
        </span>
      ) : null}
    </Link>
  );
}

function Collection({ autocollants }: { autocollants: Autocollant[] }) {
  const avec = autocollants.filter((a) => a.illustration);
  if (avec.length === 0) return null;
  const gagnes = avec.filter((a) => a.acquis).length;

  return (
    <section>
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-kid-lg font-extrabold">Ma collection</h2>
        <span className="text-kid-sm font-bold text-muted">
          {gagnes} sur {avec.length}
        </span>
      </div>
      <p className="mt-1 text-kid-sm text-muted">
        Gagne-les en jouant.
      </p>
      <ul className="mt-3 grid grid-cols-4 gap-2 sm:grid-cols-6">
        {avec.map((a) => (
          <li key={a.notionId}>
            <div
              title={a.statement}
              className={
                'relative aspect-square overflow-hidden rounded-2xl border-2 ' +
                (a.acquis ? 'border-gold bg-white-warm' : 'border-line bg-line/40')
              }
            >
              <Illustration
                cle={a.illustration}
                forme="objet"
                alt={a.acquis ? a.statement : ''}
                className={
                  'h-full w-full object-cover transition ' +
                  (a.acquis ? '' : 'opacity-35 grayscale')
                }
              />
              {!a.acquis ? (
                <span aria-hidden="true" className="absolute inset-0 grid place-items-center">
                  <span className="grid h-7 w-7 place-items-center rounded-full bg-white-warm/90 text-kid-sm font-black text-ink-2">
                    ?
                  </span>
                </span>
              ) : null}
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default function ChildHome() {
  const { childId } = useParams<{ childId: string }>();

  const enfant = useQuery({
    queryKey: ['child', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        .select('id, first_name, avatar')
        .eq('id', childId!)
        .single();
      if (error) throw error;
      return data;
    },
  });

  const bord = useQuery({
    queryKey: ['tableau', childId],
    enabled: Boolean(childId),
    queryFn: () => chargerTableauDeBord(childId!),
  });

  if (enfant.isLoading || bord.isLoading) return <Loading />;
  if (bord.error) return <ErrorNote error={bord.error} />;

  const d = bord.data!;
  const prenom = enfant.data?.first_name ?? '';
  const prochaine = d.lecons.find((l) => l.id === d.prochaineLecon);

  return (
    <main className="enfant ciel min-h-screen pb-12">
      <div className="mx-auto grid max-w-2xl gap-4 px-4 pt-4 sm:px-6">
        <header className="flex items-center justify-between gap-3">
          <Link
            to="/"
            className="flex items-center gap-2 rounded-full bg-white-warm/80 py-1.5 pr-4 pl-1.5 text-kid-sm font-bold"
          >
            <span className="grid h-9 w-9 place-items-center rounded-full bg-lilac text-base">
              {enfant.data?.avatar ?? prenom.slice(0, 1).toUpperCase()}
            </span>
            {prenom}
          </Link>
          <span className="flex items-center gap-1.5 rounded-full bg-gold/35 px-4 py-2 text-kid-sm font-black">
            <span aria-hidden="true">★</span>
            {d.points}
          </span>
        </header>

        {prochaine ? (
          <Link
            to={`/enfant/${childId}/lecon/${prochaine.id}`}
            className="tuile relative block overflow-hidden rounded-[var(--radius-card)] shadow-[var(--shadow-card)]"
          >
            <Illustration
              cle={prochaine.illustration}
              forme="scene"
              alt=""
              priorite
              className="h-44 w-full object-cover sm:h-56"
            />
            <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/85 via-ink/45 to-transparent px-5 pt-14 pb-4">
              <p className="text-kid-xs font-black tracking-widest text-gold uppercase">
                {!prochaine.etapeTerminee
                  ? `Étape ${prochaine.etape} · ${PALIERS[prochaine.etape - 1]?.nom ?? ''}`
                  : d.duesTotal > 0
                    ? 'Ta mission du jour'
                    : 'Tout est à jour'}
              </p>
              <h1
                className={
                  'line-clamp-2 leading-tight font-black text-white-warm text-balance ' +
                  (prochaine.title.length > 28 ? 'text-kid-lg' : 'text-kid-2xl')
                }
              >
                {prochaine.title}
              </h1>
              <p className="mt-1 text-kid-sm font-bold text-white-warm/90">
                {!prochaine.etapeTerminee
                  ? `Encore ${prochaine.etapeTotal - prochaine.etapeFaites} ${
                      prochaine.etapeTotal - prochaine.etapeFaites > 1 ? 'questions' : 'question'
                    } pour l’étape ${prochaine.etape + 1}`
                  : d.duesTotal > 0
                    ? `${d.duesTotal} à revoir`
                    : 'Rejoue quand tu veux'}
              </p>
            </div>
            <span className="absolute right-4 bottom-4 grid h-12 w-12 place-items-center rounded-full bg-clay text-xl text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]">
              ▶
            </span>
          </Link>
        ) : (
          <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-6 text-center">
            <Illustration cle="repos" forme="objet" alt="" className="mx-auto h-28 w-28" />
            <h1 className="mt-3 text-kid-lg font-extrabold">Rien à faire</h1>
            <p className="mt-1 text-kid-sm text-muted">Demande à un parent.</p>
          </section>
        )}

        <Semaine jours={d.jours} serie={d.serie} />

        {/* Avec une seule leçon, cette liste répéterait la carte du dessus.
            Elle n'apparaît qu'à partir de la deuxième. */}
        {d.lecons.length > 1 ? (
          <section>
            <h2 className="text-kid-lg font-extrabold">Mes leçons</h2>
            <div className="mt-2 grid gap-2">
              {d.lecons.map((lecon) => (
                <CarteLecon key={lecon.id} lecon={lecon} childId={childId!} />
              ))}
            </div>
          </section>
        ) : null}

        <Collection autocollants={d.autocollants} />
      </div>
    </main>
  );
}
