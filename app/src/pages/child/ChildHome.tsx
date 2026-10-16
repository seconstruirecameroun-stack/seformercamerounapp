import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { chargerTableauDeBord } from '../../lib/dashboard';
import { PALIERS } from '../../lib/paliers';
import { phraseDAccueil } from '../../lib/jeu';
import type { Serie } from '../../lib/jeu';
import CarteMatiere from '../../components/CarteMatiere';
import type { Autocollant } from '../../lib/dashboard';
import Illustration from '../../components/Illustration';
import Mascotte from '../../components/jeu/Mascotte';
import type { Humeur } from '../../components/jeu/Mascotte';
import { AnneauObjectif, BandeRang, Flamme } from '../../components/jeu/Compteurs';
import { Quetes, Trophees } from '../../components/jeu/Quetes';
import Duel from '../../components/jeu/Duel';
import { chargerDuel } from '../../lib/duel';
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

function Semaine({ jours, serie }: { jours: string[]; serie: Serie }) {
  const faits = new Set(jours);
  return (
    <div>
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-kid-sm font-extrabold">Ta semaine</h2>
        {serie.pardonUtilise ? (
          // Le pardon est annoncé : sans ça, l'enfant croit que manquer un
          // jour ne coûte rien, et la série cesse de tenir quoi que ce soit.
          <span className="text-kid-xs font-bold text-clay">Un jour rattrapé</span>
        ) : serie.prochainPalier ? (
          <span className="text-kid-xs font-bold text-muted">
            {serie.prochainPalier - serie.jours} jour
            {serie.prochainPalier - serie.jours > 1 ? 's' : ''} → trophée
          </span>
        ) : null}
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
    </div>
  );
}

function Collection({ autocollants }: { autocollants: Autocollant[] }) {
  const avec = autocollants.filter((a) => a.illustration);
  if (avec.length === 0) return null;
  const gagnes = avec.filter((a) => a.acquis).length;
  const reste = avec.length - gagnes;

  return (
    <section>
      <div className="flex items-baseline justify-between gap-3">
        <h2 className="text-kid-lg font-extrabold">Ma collection</h2>
        <span className="text-kid-sm font-bold text-muted">
          {gagnes} sur {avec.length}
        </span>
      </div>
      <p className="mt-1 text-kid-sm text-muted">
        {/* Dire ce qui manque, et à quelle condition : « gagne-les en jouant »
            n'apprend pas à l'enfant comment on les gagne. */}
        {gagnes === 0
          ? 'Monte une leçon jusqu’à l’étape 3 pour gagner ta première image.'
          : reste === 0
            ? 'Collection complète. Bravo !'
            : `Encore ${reste} image${reste > 1 ? 's' : ''} à trouver.`}
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

  const duel = useQuery({
    queryKey: ['duel', childId],
    enabled: Boolean(childId),
    queryFn: () => chargerDuel(childId!),
  });

  if (enfant.isLoading || bord.isLoading) return <Loading />;
  if (bord.error) return <ErrorNote error={bord.error} />;

  const d = bord.data!;
  const prenom = enfant.data?.first_name ?? '';
  const prochaine = d.lecons.find((l) => l.id === d.prochaineLecon);
  const restantes = d.autocollants.filter((a) => a.illustration && !a.acquis).length;

  const accueil = phraseDAccueil({
    serie: d.serie,
    objectif: d.objectif,
    imagesRestantes: restantes,
    reste: d.duesTotal,
    prenom,
  });

  // L'humeur de Niba dit en un coup d'œil ce que la phrase explique.
  const humeur: Humeur = d.objectif.atteint
    ? 'fete'
    : d.serie.jours > 0 && !d.serie.joueAujourdhui
      ? 'encourage'
      : d.jours.length > 0 && !d.serie.joueAujourdhui && d.serie.jours === 0
        ? 'manque'
        : 'content';

  return (
    <main className="enfant ciel min-h-screen pb-12">
      <div className="mx-auto grid max-w-2xl gap-4 px-4 pt-4 sm:px-6">
        <header className="flex items-center justify-between gap-2">
          <Link
            to="/"
            className="flex items-center gap-2 rounded-full bg-white-warm/80 py-1.5 pr-4 pl-1.5 text-kid-sm font-bold"
          >
            <span className="grid h-9 w-9 place-items-center rounded-full bg-lilac text-base">
              {enfant.data?.avatar ?? prenom.slice(0, 1).toUpperCase()}
            </span>
            {prenom}
          </Link>
          <div className="flex items-center gap-2">
            <Flamme serie={d.serie} />
            <span className="flex items-center gap-1.5 rounded-full bg-gold/35 px-4 py-2 text-kid-sm font-black">
              <span aria-hidden="true">★</span>
              {d.points}
            </span>
          </div>
        </header>

        {/* Niba parle en premier : c'est lui qui donne la raison de jouer
            aujourd'hui, avant même de montrer quelle leçon. */}
        <section className="monte flex items-center gap-3 rounded-[var(--radius-card)] border border-line bg-white-warm/85 px-4 py-3">
          <Mascotte humeur={humeur} taille={72} className="shrink-0" />
          <div className="min-w-0">
            <p className="text-kid-base leading-tight font-black text-balance">{accueil.titre}</p>
            <p className="mt-0.5 text-kid-sm text-muted">{accueil.sous}</p>
          </div>
        </section>

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
            {/* La marge à droite réserve la place du gros bouton rond : sans elle,
                le texte passait dessous sur un écran de téléphone. */}
            <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/85 via-ink/45 to-transparent px-5 pt-14 pr-20 pb-4">
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

        {/* L'objectif et la semaine dans la même carte : ce sont deux façons de
            regarder la même habitude, aujourd'hui et sur sept jours. */}
        <section className="rounded-[var(--radius-card)] border border-line bg-white-warm/80 px-4 py-3">
          <div className="flex items-center gap-4">
            <AnneauObjectif objectif={d.objectif} />
            <div className="min-w-0 flex-1">
              <h2 className="text-kid-sm font-extrabold">Objectif du jour</h2>
              <p className="mt-0.5 text-kid-sm text-muted">
                {d.objectif.atteint
                  ? 'Atteint ! Tout le reste est du bonus.'
                  : `Encore ${d.objectif.cible - d.objectif.gagnees} étoiles.`}
              </p>
            </div>
          </div>
          <div className="mt-3 border-t border-line pt-3">
            <Semaine jours={d.jours} serie={d.serie} />
          </div>
        </section>

        {duel.data ? <Duel duel={duel.data} childId={childId!} /> : null}

        <Quetes quetes={d.quetes} />

        <section className="rounded-[var(--radius-card)] border border-line bg-white-warm/80 px-4 py-3">
          <BandeRang rang={d.rang} />
        </section>

        {/* Avec une seule leçon, cette liste répéterait la carte du dessus.
            Elle n'apparaît qu'à partir de la deuxième. */}
        {d.lecons.length > 1 ? (
          <section>
            <h2 className="text-kid-lg font-extrabold">Mes matières</h2>
            {/* Deux colonnes : des tuiles assez grandes pour un doigt, et
                toute la liste visible sans défiler longtemps. */}
            <div className="mt-2 grid grid-cols-2 gap-2 sm:grid-cols-3">
              {d.matieres.map((matiere) => (
                <CarteMatiere key={matiere.id} matiere={matiere} childId={childId!} />
              ))}
            </div>
          </section>
        ) : null}

        <Collection autocollants={d.autocollants} />

        <Trophees trophees={d.trophees} />
      </div>
    </main>
  );
}
