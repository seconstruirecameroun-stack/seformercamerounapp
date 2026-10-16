import { Link } from 'react-router-dom';
import Mascotte from '../components/jeu/Mascotte';
import Illustration from '../components/Illustration';
import { PALIERS } from '../lib/paliers';

/**
 * La page qu'un parent voit avant d'avoir un compte.
 *
 * Elle n'a qu'un travail : faire comprendre en dix secondes ce que l'app fait
 * du cahier de son enfant, et donner envie d'essayer. Trois règles tenues
 * d'un bout à l'autre :
 *
 * 1. On montre l'app telle qu'elle est. Les captures sont de vraies parties,
 *    jouées sur un téléphone — aucune maquette, aucun écran redessiné pour
 *    l'occasion. Un parent qui s'inscrit doit retrouver exactement ça.
 *
 * 2. Aucun chiffre inventé. Pas de « 10 000 familles », pas de témoignage
 *    fabriqué. Tout ce qui est annoncé ici existe dans l'app aujourd'hui.
 *
 * 3. Aucun prénom d'enfant. Les captures ont été choisies et rognées pour
 *    qu'aucune n'en porte : une page publique n'a pas à nommer un élève.
 */

const ETAPES_IMPORT = [
  {
    titre: 'Vous photographiez la page du cahier',
    texte:
      'Le cours tel qu’il a été écrit en classe, dans sa langue — l’école est bilingue, l’app aussi.',
    illustration: 'tablette-ecriture',
  },
  {
    titre: 'Elle devient une leçon, un film et des questions',
    texte:
      'Vous relisez ce qui en est tiré, vous corrigez, vous publiez. Rien n’arrive à l’enfant sans ce passage.',
    illustration: 'gd-film',
  },
  {
    titre: 'L’enfant joue, et il revient',
    texte:
      'Une série à ne pas casser, des images à gagner, un coffre à ouvrir, et un rappel le soir s’il n’a pas joué.',
    illustration: 'medaille',
  },
];

const RESSORTS = [
  {
    cle: 'defis',
    titre: 'Un objectif, trois défis, chaque jour',
    texte:
      'Cent étoiles à gagner, et trois défis tirés de la date : les mêmes toute la journée, d’autres demain.',
  },
  {
    cle: 'collection',
    titre: 'Une image par notion, à collectionner',
    texte:
      'Chaque notion porte une image. Elle se gagne en montant la leçon jusqu’à l’étape « Maîtrise » — jamais avant.',
  },
  {
    cle: 'coffre',
    titre: 'Un coffre à ouvrir en fin de séance',
    texte:
      'Il n’ajoute aucune information. Il ajoute une seconde d’attente et un geste à faire, et ça change tout.',
  },
  {
    cle: 'image',
    titre: 'Les bonnes nouvelles, une par une',
    texte:
      'L’image, l’étape franchie, le rang atteint : chacune a sa fenêtre, son illustration et ses étoiles.',
  },
];

const QUESTIONS = [
  {
    q: 'Combien ça coûte ?',
    r: 'Rien, pour l’instant. L’app est jeune — elle a d’abord été écrite pour deux enfants d’une école de Yaoundé — et tout ce qu’elle sait faire est ouvert. Si un tarif apparaît un jour, il sera écrit sur cette page.',
  },
  {
    q: 'Comment une leçon entre-t-elle dans l’app ?',
    r: 'Vous photographiez les pages du cahier depuis l’espace parent. Vous relisez ce qui en est tiré, vous corrigez ce qui doit l’être, et vous publiez. Rien n’arrive à l’enfant sans ce passage par vous.',
  },
  {
    q: 'Mes enfants n’ont pas de téléphone.',
    r: 'Un seul appareil suffit. Chaque enfant a son profil, sa progression, sa collection et ses rappels — sur le même téléphone, celui du parent.',
  },
  {
    q: 'Et si le programme de notre école est différent ?',
    r: 'La liste des matières n’est pas figée. Vous choisissez celle de votre école au moment d’importer un cours, et vous en ajoutez une si elle manque.',
  },
  {
    q: 'Est-ce que ça marche en anglais ?',
    r: 'Oui. Chaque cours reste dans la langue où il a été écrit, et les questions suivent. Un cours de science en anglais se révise en anglais.',
  },
  {
    q: 'Qu’est-ce que l’enfant peut faire sans moi ?',
    r: 'Jouer, revoir ses leçons, regarder les films. L’espace parent — l’import, la validation, les réglages — est derrière un code à quatre chiffres.',
  },
];

function Bandeau() {
  const mots = [
    'Fait à Yaoundé',
    'Pour l’école camerounaise',
    'Du CE1 au CM2',
    'Français et anglais',
    'Les leçons de votre cahier',
  ];
  return (
    <div className="overflow-hidden border-b border-line bg-mint/50 py-2">
      <div className="defile flex w-max gap-8 text-kid-xs font-bold whitespace-nowrap text-ink-2">
        {[0, 1].map((tour) => (
          <div key={tour} className="flex gap-8" aria-hidden={tour === 1}>
            {mots.map((m) => (
              <span key={m} className="flex items-center gap-8">
                {m}
                <span className="text-gold">◆</span>
              </span>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

function Telephone({ source, alt, className = '' }: { source: string; alt: string; className?: string }) {
  return (
    <div className={'telephone mx-auto w-full max-w-[300px] ' + className}>
      <img src={source} alt={alt} loading="lazy" decoding="async" className="block w-full" />
    </div>
  );
}

export default function Landing() {
  return (
    <main className="enfant ciel min-h-screen">
      <Bandeau />

      <header className="mx-auto flex max-w-5xl items-center justify-between gap-3 px-4 py-4 sm:px-6">
        {/* Le nom se raccourcit avant le bouton : sur un écran de 360 px,
            c'est l'action qu'il faut garder entière, pas l'enseigne. */}
        <span className="flex min-w-0 items-center gap-2">
          <Mascotte taille={40} className="shrink-0" />
          <strong className="truncate text-kid-sm font-black sm:text-kid">
            Se Former Cameroun
          </strong>
        </span>
        <Link
          to="/connexion"
          className="tuile shrink-0 rounded-full border-2 border-line bg-white-warm px-4 py-2 text-kid-sm font-bold whitespace-nowrap shadow-[var(--shadow-tile)]"
        >
          Se connecter
        </Link>
      </header>

      {/* ───────── Le héros ───────── */}
      <section className="pointille mx-auto max-w-5xl px-4 pt-4 pb-12 sm:px-6">
        <div className="grid items-center gap-8 md:grid-cols-2">
          <div>
            <span className="inline-flex items-center gap-2 rounded-full bg-gold/35 px-4 py-1.5 text-kid-xs font-black">
              ◆ Du cahier à l’écran
            </span>
            <h1 className="mt-4 text-kid-2xl leading-[1.1] font-black text-balance sm:text-[3rem]">
              Les leçons du cahier, révisées en jouant.
            </h1>
            <p className="mt-4 text-kid leading-snug text-ink-2 text-balance">
              Vous photographiez le cours de la journée. L’app en fait une leçon illustrée, un film
              court et un jeu qui monte en difficulté — et votre enfant y revient de lui-même.
            </p>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link
                to="/connexion?mode=creation"
                className="tuile rounded-full bg-clay px-7 py-4 text-kid font-black text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]"
              >
                Créer mon compte
              </Link>
              <a
                href="#methode"
                className="tuile rounded-full border-2 border-line bg-white-warm px-7 py-4 text-kid font-bold shadow-[var(--shadow-tile)]"
              >
                Voir la méthode
              </a>
            </div>
          </div>
          <Telephone source="/apercu/accueil.webp" alt="L’écran d’accueil d’un enfant dans l’app" />
        </div>
      </section>

      {/* ───────── Comment ça marche ───────── */}
      <section id="methode" className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <h2 className="text-kid-xl font-black text-balance">Trois gestes, et la leçon est prête</h2>
        <ol className="mt-6 grid gap-4 md:grid-cols-3">
          {ETAPES_IMPORT.map((e, i) => (
            <li
              key={e.titre}
              className="rounded-[var(--radius-card)] border border-line bg-white-warm/85 p-5"
            >
              <div className="flex items-center gap-3">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-clay text-kid font-black text-white-warm">
                  {i + 1}
                </span>
                <Illustration
                  cle={e.illustration}
                  forme="objet"
                  alt=""
                  className="h-14 w-14 rounded-2xl object-cover"
                />
              </div>
              <h3 className="mt-3 text-kid font-extrabold text-balance">{e.titre}</h3>
              <p className="mt-1 text-kid-sm text-ink-2">{e.texte}</p>
            </li>
          ))}
        </ol>
      </section>

      {/* ───────── L'escalier ───────── */}
      <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <div className="grid items-center gap-8 md:grid-cols-2">
          <Telephone source="/apercu/question.webp" alt="Une question de l’étape Découverte" />
          <div>
            <h2 className="text-kid-xl font-black text-balance">
              Une leçon se gravit comme un jeu : quatre étapes
            </h2>
            <ol className="mt-5 grid gap-2">
              {PALIERS.map((p) => (
                <li
                  key={p.niveau}
                  className="flex items-center gap-3 rounded-2xl border border-line bg-white-warm/85 px-4 py-3"
                >
                  <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-gold text-kid-sm font-black">
                    {p.niveau}
                  </span>
                  <span className="min-w-0">
                    <strong className="block text-kid-sm font-extrabold">{p.nom}</strong>
                    <small className="block text-kid-xs text-muted">{p.promesse}</small>
                  </span>
                </li>
              ))}
            </ol>
            <p className="mt-4 text-kid-sm text-ink-2">
              On ne passe à l’étape suivante que lorsque <strong>chaque notion</strong> de la leçon
              est tombée à ce niveau. Pas une moyenne : une moyenne laisse passer un enfant qui
              ignore trois notions sur dix. Rater ne fait pas reculer — ça fait revenir, avec une
              autre formulation.
            </p>
          </div>
        </div>
      </section>

      {/* ───────── Ce qui le fait revenir ───────── */}
      <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <h2 className="text-kid-xl font-black text-balance">Ce qui lui donne envie de revenir</h2>
        <p className="mt-2 max-w-2xl text-kid-sm text-ink-2">
          Un enfant de sept ans ne revient pas pour réviser. Il revient pour une série qu’il ne veut
          pas casser, un objectif à vingt étoiles près, et un coffre qu’il n’a pas encore ouvert.
        </p>
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {RESSORTS.map((r) => (
            <article
              key={r.cle}
              className="overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm/85"
            >
              <div className="p-5">
                <h3 className="text-kid font-extrabold text-balance">{r.titre}</h3>
                <p className="mt-1 text-kid-sm text-ink-2">{r.texte}</p>
              </div>
              <img
                src={`/apercu/${r.cle}.webp`}
                alt=""
                loading="lazy"
                decoding="async"
                className="block w-full border-t border-line"
              />
            </article>
          ))}
        </div>
      </section>

      {/* ───────── L'école d'ici ───────── */}
      <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <div className="grid items-center gap-8 rounded-[var(--radius-card)] border border-line bg-white-warm/85 p-6 md:grid-cols-2">
          <div>
            <h2 className="text-kid-xl font-black text-balance">Pour l’école d’ici</h2>
            <p className="mt-3 text-kid-sm text-ink-2">
              Les matières viennent de l’emploi du temps de votre école, en français comme en
              anglais. Et parce que chaque école a son programme, <strong>la liste n’est pas
              figée</strong> : vous ajoutez la vôtre au moment d’importer un cours.
            </p>
            <p className="mt-3 text-kid-sm text-ink-2">
              Les illustrations montrent ce que l’enfant connaît : un village, un canari, la Bénoué,
              un marché. Pas une salle de classe d’ailleurs.
            </p>
          </div>
          <Illustration
            cle="in-cameroun"
            forme="scene"
            alt=""
            className="w-full rounded-[var(--radius-card)] object-cover"
          />
        </div>
      </section>

      {/* ───────── Côté parent ───────── */}
      <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <h2 className="text-kid-xl font-black text-balance">Ce que vous gardez en main</h2>
        <ul className="mt-6 grid gap-4 md:grid-cols-3">
          {[
            ['Rien ne passe sans vous', 'Chaque leçon tirée d’une photo attend votre relecture avant d’atteindre l’enfant.'],
            ['Un code pour l’espace parent', 'L’import, la validation et les réglages sont derrière quatre chiffres.'],
            ['Ni publicité, ni revente', 'Les cahiers de vos enfants ne servent qu’à leurs révisions.'],
          ].map(([titre, texte]) => (
            <li key={titre} className="rounded-[var(--radius-card)] border border-line bg-white-warm/85 p-5">
              <h3 className="text-kid font-extrabold text-balance">{titre}</h3>
              <p className="mt-1 text-kid-sm text-ink-2">{texte}</p>
            </li>
          ))}
        </ul>
      </section>

      {/* ───────── Le prix ───────── */}
      <section className="mx-auto max-w-3xl px-4 py-12 sm:px-6">
        <div className="rounded-[var(--radius-card)] border-2 border-gold bg-white-warm/90 p-6 text-center shadow-[var(--shadow-card)]">
          <span className="inline-flex items-center gap-2 rounded-full bg-gold/35 px-4 py-1.5 text-kid-xs font-black">
            ◆ Gratuit pour l’instant
          </span>
          <p className="mt-4 text-[3.5rem] leading-none font-black">0 FCFA</p>
          <p className="mx-auto mt-3 max-w-lg text-kid-sm text-ink-2">
            L’app est jeune : elle a d’abord été écrite pour deux enfants d’une école de Yaoundé.
            Tout ce qu’elle sait faire est ouvert, sans limite de leçons ni d’enfants. Si un tarif
            apparaît un jour, il sera écrit sur cette page.
          </p>
          <ul className="mx-auto mt-5 grid max-w-lg gap-2 text-left sm:grid-cols-2">
            {[
              'Les cours du cahier, importés',
              'Les films et les illustrations',
              'Les quatre étapes et les six types de questions',
              'La collection, les rangs et les trophées',
              'Le duel entre frères et sœurs',
              'Les rappels du soir',
            ].map((ligne) => (
              <li key={ligne} className="flex items-start gap-2 text-kid-sm">
                <span aria-hidden="true" className="mt-0.5 font-black text-leaf">
                  ✓
                </span>
                {ligne}
              </li>
            ))}
          </ul>
          <p className="mt-5 text-kid-xs text-muted">Ni publicité, ni revente de données.</p>
        </div>
      </section>

      {/* ───────── Questions ───────── */}
      <section className="mx-auto max-w-3xl px-4 py-12 sm:px-6">
        <h2 className="text-kid-xl font-black">Les questions qu’on nous pose</h2>
        <div className="mt-6 grid gap-3">
          {QUESTIONS.map((item) => (
            <details
              key={item.q}
              className="group rounded-[var(--radius-card)] border border-line bg-white-warm/85 px-5 py-4"
            >
              <summary className="cursor-pointer list-none text-kid font-extrabold marker:content-['']">
                <span className="flex items-start justify-between gap-3">
                  {item.q}
                  <span aria-hidden="true" className="shrink-0 text-clay group-open:hidden">
                    +
                  </span>
                  <span aria-hidden="true" className="hidden shrink-0 text-clay group-open:block">
                    −
                  </span>
                </span>
              </summary>
              <p className="mt-2 text-kid-sm text-ink-2">{item.r}</p>
            </details>
          ))}
        </div>
      </section>

      {/* ───────── L'appel final ───────── */}
      <section className="mx-auto max-w-5xl px-4 pb-16 sm:px-6">
        <div className="rounded-[var(--radius-card)] bg-ink px-6 py-10 text-center shadow-[var(--shadow-card)]">
          <Mascotte humeur="fete" taille={88} className="mx-auto" />
          <h2 className="mt-3 text-kid-xl font-black text-white-warm text-balance">
            Le cahier de ce soir peut devenir sa leçon de demain.
          </h2>
          <p className="mx-auto mt-2 max-w-md text-kid-sm text-white-warm/80">
            Créez votre compte, ajoutez un enfant, photographiez une page. La première leçon prend
            quelques minutes.
          </p>
          <Link
            to="/connexion?mode=creation"
            className="tuile mt-6 inline-block rounded-full bg-gold px-8 py-4 text-kid font-black text-ink shadow-[0_3px_0_var(--color-clay-dark)]"
          >
            Créer mon compte
          </Link>
        </div>
      </section>

      <footer className="border-t border-line px-4 py-8 text-center text-kid-xs text-muted sm:px-6">
        <p>
          <strong>Se Former Cameroun</strong> · Yaoundé
        </p>
        <p className="mt-1">
          Déjà un compte ?{' '}
          <Link to="/connexion" className="font-bold text-ink-2 underline">
            Se connecter
          </Link>
        </p>
      </footer>
    </main>
  );
}
