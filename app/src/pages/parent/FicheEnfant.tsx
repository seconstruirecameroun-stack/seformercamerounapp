import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  chargerRapports,
  type Fenetre,
  type Priorite,
  type ProfilNotion,
  type Rapport,
} from '../../lib/rapport';
import { Button, Card, ErrorNote, Loading, Pill, Vide } from '../../components/ui';
import Mascotte from '../../components/jeu/Mascotte';
import { verrouiller } from '../../components/PinGate';
import { supabase } from '../../lib/supabase';
import type { ItemKind, NotionKind } from '../../types/db';

/**
 * Le rapport de travail, dans le profil de l'enfant.
 *
 * Quatre volets, dans l'ordre où l'on comprend quelqu'un : comment il
 * travaille, ce qu'il réussit, ce qui le met en difficulté, et ce qu'il doit
 * travailler beaucoup. Le dernier est le seul qui compte vraiment pour un
 * parent du soir, et c'est pourquoi il ferme la page au lieu de l'ouvrir —
 * on y arrive après avoir lu de quoi le comprendre.
 *
 * Les chiffres sont calculés dans lib/rapport.ts. Ici on les met en phrases,
 * et la règle est tenue mot à mot : le rapport parle du TRAVAIL, jamais de
 * l'enfant. « Il s'arrête après huit minutes » se dit ; « il manque de
 * concentration » ne se dit pas, parce que l'app n'en sait rien et qu'un
 * parent le lirait sur son fils.
 *
 * Quand une mesure n'a pas assez de matière, elle disparaît au lieu de
 * s'afficher en gris. Une ligne vide invite à deviner ; une ligne absente,
 * non.
 */

const NOM_DU_TYPE: Record<ItemKind, string> = {
  qcm: 'les questions à choix',
  association: 'les exercices où il faut relier',
  chronologie: 'les mots à remettre en ordre',
  texte_a_trous: 'les textes à trous',
  vrai_faux: 'les vrai ou faux',
  dictee: 'les dictées',
  diagramme: 'les éléments à placer dans un diagramme',
  annotation: 'les schémas à annoter',
  restitution_audio: 'les réponses orales',
  defi_chrono: 'les défis chronométrés',
};

/** Les quatre familles de notions, dites comme un parent les dirait. */
const NOM_DE_LA_FAMILLE: Record<NotionKind, string> = {
  date: 'les dates',
  definition: 'les définitions',
  liste: 'les listes à retenir',
  relation: 'les liens entre les choses',
};

/** « vers 19 h », parce qu'un parent ne lit pas « mode horaire = 19 ». */
function versHeure(h: number | null): string | null {
  return h === null ? null : `vers ${h} h`;
}

function Fait({
  valeur,
  libelle,
  ton = 'neutre',
}: {
  valeur: string;
  libelle: string;
  ton?: 'neutre' | 'bon' | 'attention';
}) {
  return (
    <div
      className={
        'rounded-2xl px-3 py-2.5 text-center ' +
        (ton === 'bon' ? 'bg-leaf/15' : ton === 'attention' ? 'bg-clay/10' : 'bg-paper')
      }
    >
      <p className="text-xl leading-tight font-black">{valeur}</p>
      <p className="mt-0.5 text-sm text-muted">{libelle}</p>
    </div>
  );
}

function Phrase({ children }: { children: React.ReactNode }) {
  return <li className="flex gap-2 text-base leading-relaxed">
    <span aria-hidden="true" className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-clay" />
    <span>{children}</span>
  </li>;
}

function CarteTravail({ r }: { r: Rapport }) {
  const heure = versHeure(r.heureHabituelle);
  const phrases: React.ReactNode[] = [];

  if (r.seances > 0) {
    phrases.push(
      <>
        {r.seances} séance{r.seances > 1 ? 's' : ''} de {r.questionsParSeance} question
        {r.questionsParSeance > 1 ? 's' : ''} en moyenne
        {heure ? `, le plus souvent ${heure}` : ''}.
      </>,
    );
  }
  if (r.secondesParQuestion !== null) {
    phrases.push(<>Il prend environ {r.secondesParQuestion} secondes par question.</>);
  }
  phrases.push(
    <>
      Il a joué {r.joursJoues} jour{r.joursJoues > 1 ? 's' : ''} sur {r.joursPossibles}
      {r.fenetre === 'semaine' ? ' cette semaine' : ' depuis le début'}.
    </>,
  );
  if (r.seancesCourtes > 0) {
    // Un fait, pas un verdict : on dit ce qui s'est passé, le parent sait
    // mieux que l'app si c'était l'heure du bain ou le découragement.
    phrases.push(
      <>
        {r.seancesCourtes} fois, il s’est arrêté avant la troisième question.
      </>,
    );
  }

  return (
    <Card titre="Comment il travaille" sous="Le rythme des séances, pas leur résultat.">
      <div className="grid grid-cols-3 gap-2">
        <Fait valeur={String(r.questions)} libelle={r.questions > 1 ? 'questions' : 'question'} />
        <Fait valeur={String(r.seances)} libelle={r.seances > 1 ? 'séances' : 'séance'} />
        <Fait valeur={`${r.minutes} min`} libelle="au total" />
      </div>
      <ul className="mt-4 grid gap-2">
        {phrases.map((p, i) => (
          <Phrase key={i}>{p}</Phrase>
        ))}
      </ul>
    </Card>
  );
}

function CarteForces({ r }: { r: Rapport }) {
  const part = r.questionsVues > 0 ? Math.round((r.duPremierCoup / r.questionsVues) * 100) : 0;
  return (
    <Card titre="Ce qu’il réussit" sous="Ce qui est acquis, et où il avance seul.">
      <div className="grid grid-cols-3 gap-2">
        <Fait
          valeur={`${r.justes}/${r.questions}`}
          libelle="bonnes réponses"
          ton={r.questions > 0 && r.justes / r.questions >= 0.7 ? 'bon' : 'neutre'}
        />
        <Fait valeur={`${part} %`} libelle="du premier coup" ton={part >= 60 ? 'bon' : 'neutre'} />
        <Fait
          valeur={String(r.leconsValidees)}
          libelle={r.leconsValidees > 1 ? 'leçons validées' : 'leçon validée'}
          ton={r.leconsValidees > 0 ? 'bon' : 'neutre'}
        />
      </div>
      <ul className="mt-4 grid gap-2">
        {r.matiereForte ? (
          <Phrase>
            C’est en <strong>{r.matiereForte.label}</strong> qu’il avance le mieux :{' '}
            {Math.round(r.matiereForte.part * 100)} % de bonnes réponses sur{' '}
            {r.matiereForte.essais} questions.
          </Phrase>
        ) : null}
        <Phrase>
          {r.duPremierCoup} question{r.duPremierCoup > 1 ? 's' : ''} sur {r.questionsVues}{' '}
          {r.duPremierCoup > 1 ? 'ont été réussies' : 'a été réussie'} dès la première fois.
        </Phrase>
        {r.leconsValidees > 0 ? (
          <Phrase>
            {r.leconsValidees} leçon{r.leconsValidees > 1 ? 's sont passées' : ' est passée'} par la
            manche sans faute, série par série.
          </Phrase>
        ) : null}
      </ul>
    </Card>
  );
}

/**
 * Une famille de notions, et le trou entre reconnaître et produire.
 *
 * C'est le bloc qui manquait. Un parent voyait son fils buter sur les dates
 * et ne trouvait rien dans le rapport : 82 % de réussite, rien à signaler.
 * La moyenne mélangeait trente et un QCM, où la bonne année est à l'écran,
 * et six textes à trous, où il faut l'écrire — 97 % d'un côté, 33 % de
 * l'autre. Le trou était là ; il n'était simplement affiché nulle part.
 */
function Famille({ p }: { p: ProfilNotion }) {
  const nom = NOM_DE_LA_FAMILLE[p.kind] ?? p.kind;
  return (
    <li className="rounded-2xl bg-paper p-4">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <strong className="text-base">
          {nom.charAt(0).toUpperCase() + nom.slice(1)}
        </strong>
        <span className="text-sm text-muted">
          {Math.round(p.part * 100)} % sur {p.essais} questions
        </span>
      </div>
      {p.ecart !== null && p.reconnaitre && p.produire ? (
        <p className="mt-2 text-base leading-relaxed">
          Il répond juste <strong>{Math.round(p.reconnaitre.part * 100)} %</strong> du temps
          quand la réponse est à l’écran, et <strong>{Math.round(p.produire.part * 100)} %</strong>{' '}
          quand il doit l’écrire lui-même.
        </p>
      ) : null}
      {p.erreurRecurrente ? (
        <p className="mt-2 rounded-xl bg-clay/10 px-3 py-2 text-base">
          Il a écrit <strong>« {p.erreurRecurrente.texte} »</strong> {p.erreurRecurrente.fois} fois,
          sur des questions différentes.
        </p>
      ) : null}
    </li>
  );
}

function CarteDifficultes({ r }: { r: Rapport }) {
  // Les familles qui méritent d'être montrées : celles qui ne vont pas de
  // soi — un trou entre reconnaître et produire, une erreur répétée, ou une
  // réussite nettement basse. Les lister toutes ferait un tableau de plus.
  const familles = r.profils.filter(
    (p) => p.ecart !== null || p.erreurRecurrente !== null || p.part < 0.7,
  );
  const avecEcart = r.profils.filter((p) => p.ecart !== null);
  const rien =
    !r.matiereFaible &&
    !r.typeFaible &&
    familles.length === 0 &&
    r.manchesRatees === 0 &&
    r.aTravailler.length === 0;
  return (
    <Card titre="Ce qui le met en difficulté" sous="Les formes de questions et les matières qui résistent.">
      {rien ? (
        <p className="text-base text-muted">
          Rien ne se détache{r.fenetre === 'semaine' ? ' cette semaine' : ''}. C’est une bonne
          nouvelle, ou le signe qu’il n’a pas encore assez joué pour qu’une tendance apparaisse.
        </p>
      ) : (
        <ul className="grid gap-2">
          {/* Quand le trou se répète sur presque toutes les familles, ce
              n-est plus une faiblesse sur les dates ou sur les listes : c’est
              une seule chose, dite quatre fois. Au parent de la lire d-un
              coup, pas de la recomposer carte par carte. */}
          {avecEcart.length >= 3 ? (
            <Phrase>
              La même chose revient partout : il reconnaît bien, et il produit
              mal. Dans {avecEcart.length} famille{avecEcart.length > 1 ? 's' : ''} de notions sur{' '}
              {r.profils.length}, il répond nettement mieux quand la réponse est à l’écran que
              lorsqu’il doit l’écrire lui-même.
            </Phrase>
          ) : null}
          {r.matiereFaible ? (
            <Phrase>
              La matière qui résiste le plus est <strong>{r.matiereFaible.label}</strong> :{' '}
              {Math.round(r.matiereFaible.part * 100)} % de bonnes réponses sur{' '}
              {r.matiereFaible.essais} questions.
            </Phrase>
          ) : null}
          {r.typeFaible ? (
            <Phrase>
              Ce sont <strong>{NOM_DU_TYPE[r.typeFaible.kind] ?? r.typeFaible.kind}</strong> qui lui
              coûtent le plus : {Math.round(r.typeFaible.part * 100)} % de réussite sur{' '}
              {r.typeFaible.essais} questions.
            </Phrase>
          ) : null}
          {familles.length > 0 ? (
            <li>
              <ul className="my-1 grid gap-2">
                {familles.map((p) => (
                  <Famille key={p.kind} p={p} />
                ))}
              </ul>
            </li>
          ) : null}
          {r.manchesRatees > 0 ? (
            <Phrase>
              {r.manchesRatees} série{r.manchesRatees > 1 ? 's' : ''} de validation{' '}
              {r.manchesRatees > 1 ? 'ont été tentées' : 'a été tentée'} sans aller au bout du
              sans-faute.
            </Phrase>
          ) : null}
        </ul>
      )}
    </Card>
  );
}

function CartePriorite({ p }: { p: Priorite }) {
  return (
    <li className="rounded-2xl border-2 border-clay/40 bg-clay/5 p-4">
      <p className="text-base font-extrabold">{p.enonce}</p>
      <p className="mt-0.5 text-sm text-muted">
        {p.lecon}
        {p.matiere ? ` · ${p.matiere}` : ''}
      </p>
      {/* La phrase que le parent peut dire au dîner. Sans elle, le rapport
          renvoie à un pourcentage et le parent reste démuni. On distingue
          l’habitude de l’exemple : « il répond toujours » sur une seule
          occurrence serait une affirmation que les faits ne portent pas. */}
      {p.erreur ? (
        <p className="mt-2 text-base">
          {p.erreur.habituelle ? 'Quand il se trompe, il répond ' : 'La dernière fois, il a répondu '}
          <strong>« {p.erreur.texte} »</strong>.
        </p>
      ) : null}
      <p className="mt-2 text-sm font-bold text-clay-dark">
        {p.fautes} erreur{p.fautes > 1 ? 's' : ''} sur {p.essais} essai
        {p.essais > 1 ? 's' : ''}
      </p>
    </li>
  );
}

function CarteATravailler({ r }: { r: Rapport }) {
  return (
    <Card
      titre="Ce qu’il doit beaucoup travailler"
      sous="Trois ou quatre notions, nommées. Pas une liste à cocher."
    >
      {r.aTravailler.length === 0 ? (
        <p className="text-base text-muted">
          Aucune notion ne revient assez souvent{r.fenetre === 'semaine' ? ' cette semaine' : ''}{' '}
          pour être une priorité. Il faut au moins deux erreurs sur la même notion pour qu’on la
          nomme ici — une seule, c’est un jour sans.
        </p>
      ) : (
        <ul className="grid gap-3">
          {r.aTravailler.map((p) => (
            <CartePriorite key={p.notionId} p={p} />
          ))}
        </ul>
      )}
    </Card>
  );
}

export default function FicheEnfant() {
  const { childId } = useParams<{ childId: string }>();
  const navigate = useNavigate();
  const [fenetre, setFenetre] = useState<Fenetre>('semaine');

  const rapports = useQuery({
    queryKey: ['rapport', childId],
    queryFn: () => chargerRapports(childId!),
    enabled: Boolean(childId),
  });

  const r = rapports.data?.[fenetre];

  return (
    <main className="min-h-dvh bg-paper px-4 py-8 sm:px-6">
      <div className="mx-auto grid w-full max-w-3xl gap-5">
        <header className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Mascotte taille={44} className="shrink-0" />
            <div>
              <Pill>Rapport de travail</Pill>
              <h1 className="mt-1.5 text-2xl font-black sm:text-3xl">
                {r ? r.prenom : 'Son travail'}
              </h1>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            {childId ? (
              <Link
                to={`/parent/enfant/${childId}/composition`}
                className="tuile rounded-full border-2 border-ink bg-ink px-4 py-2 text-base font-bold text-white-warm"
              >
                Composition
              </Link>
            ) : null}
            {childId ? (
              <Link
                to={`/enfant/${childId}`}
                className="tuile rounded-full border-2 border-line bg-white-warm px-4 py-2 text-base font-bold"
              >
                Son espace
              </Link>
            ) : null}
            <Button variant="secondary" onClick={() => navigate('/parent')}>
              Espace parent
            </Button>
            <Button
              variant="ghost"
              onClick={() => {
                verrouiller();
                supabase.auth.signOut();
              }}
            >
              Se déconnecter
            </Button>
          </div>
        </header>

        {/* Deux échelles, parce qu'une difficulté qui dure n'a pas le même
            sens qu'une mauvaise soirée. */}
        <div className="flex gap-2 rounded-full bg-white-warm/85 p-1.5">
          {(
            [
              ['semaine', 'Cette semaine'],
              ['debut', 'Depuis le début'],
            ] as Array<[Fenetre, string]>
          ).map(([cle, nom]) => (
            <button
              key={cle}
              type="button"
              onClick={() => setFenetre(cle)}
              className={
                'min-h-11 flex-1 rounded-full px-4 py-2 text-base font-bold transition-colors ' +
                (fenetre === cle ? 'bg-ink text-white-warm' : 'text-ink-2 hover:bg-paper')
              }
            >
              {nom}
            </button>
          ))}
        </div>

        {rapports.isLoading ? <Loading label="Je relis ses séances…" /> : null}
        {rapports.error ? <ErrorNote error={rapports.error} /> : null}

        {r && r.vide ? (
          <Vide
            titre={
              fenetre === 'semaine'
                ? `${r.prenom} n’a pas joué cette semaine`
                : `${r.prenom} n’a encore rien joué`
            }
            texte={
              fenetre === 'semaine'
                ? 'Regardez « depuis le début » pour voir ce qu’il a fait avant.'
                : 'Le rapport se remplit dès sa première séance.'
            }
          />
        ) : null}

        {r && !r.vide ? (
          <>
            <CarteTravail r={r} />
            <CarteForces r={r} />
            <CarteDifficultes r={r} />
            <CarteATravailler r={r} />
            <p className="px-1 text-sm text-muted">
              Ce rapport décrit son travail, pas lui. Il compte des réponses et des séances ; il ne
              dit rien de son attention ni de ses efforts, que vous êtes seul à voir.
            </p>
          </>
        ) : null}
      </div>
    </main>
  );
}
