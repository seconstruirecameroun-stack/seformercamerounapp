import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { useSession } from '../../lib/auth';
import {
  POINTS_ETAPE,
  POINTS_IMAGE,
  POINTS_NOTION,
  POINTS_PAR_ETAPE,
  recordAttempt,
} from '../../lib/progress';
import {
  construireSeance,
  estChronometre,
  etapeImage,
  imageGagnee,
  PALIERS,
  reussitesParNiveau,
  SECONDES_DEFI,
} from '../../lib/paliers';
import {
  enregistrerManche,
  pointsConsolation,
  pointsManche,
  serieParfaite,
  type MancheRow,
} from '../../lib/manche';
import { rangDeLaClasse } from '../../lib/saisie';
import { stopper } from '../../lib/voix';
import type { Palier } from '../../lib/paliers';
import ItemPlayer from '../../components/items/ItemPlayer';
import type { Reponse } from '../../components/items/ItemPlayer';
import Illustration from '../../components/Illustration';
import { urlFilm } from '../../lib/image';
import Fiches from './Fiches';
import Popup from '../../components/Popup';
import Coffre, { Confettis } from '../../components/jeu/Coffre';
import type { Butin } from '../../components/jeu/Coffre';
import Mascotte from '../../components/jeu/Mascotte';
import type { Humeur } from '../../components/jeu/Mascotte';
import { jouerSon } from '../../lib/sons';
import { etatRang } from '../../lib/jeu';
import { ErrorNote, Loading } from '../../components/ui';
import type { ExplanationRow, NotionRow, VideoRow } from '../../types/db';

type LessonBundle = {
  id: string;
  title: string;
  summary: string | null;
  lang: string;
  illustration: string | null;
  subject_id: string | null;
  subjects: { label: string } | null;
  notions: Array<NotionRow & { explanations: ExplanationRow[] }>;
  videos: VideoRow[];
};


/** Bouton rond et large : la cible principale de l'espace enfant. */
function GrosBouton({
  children,
  onClick,
  variante = 'clay',
  type = 'button',
  disabled,
}: {
  children: React.ReactNode;
  onClick?: () => void;
  variante?: 'clay' | 'douce';
  type?: 'button' | 'submit';
  disabled?: boolean;
}) {
  const look =
    variante === 'clay'
      ? 'bg-clay text-white-warm shadow-[0_3px_0_var(--color-clay-dark)]'
      : 'bg-white-warm text-ink border-2 border-line shadow-[var(--shadow-tile)]';
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={
        'tuile inline-flex min-h-[54px] items-center justify-center gap-2 rounded-full px-7 text-kid font-extrabold disabled:opacity-45 ' +
        look
      }
    >
      {children}
    </button>
  );
}

/** Les étapes franchies, en galets. Une barre de progression ne dit rien à
    un enfant qui ne sait pas encore lire les pourcentages. */
function Galets({ total, faits }: { total: number; faits: number }) {
  return (
    <div className="flex items-center gap-1.5" aria-label={`${faits} sur ${total}`}>
      {Array.from({ length: total }, (_, i) => (
        <span
          key={i}
          className={
            'h-2.5 rounded-full transition-all duration-300 ' +
            (i < faits ? 'w-7 bg-gold' : i === faits ? 'w-7 bg-gold/35' : 'w-2.5 bg-line')
          }
        />
      ))}
    </div>
  );
}


/**
 * L'étape en cours, en haut de l'écran.
 *
 * C'est la pièce qui manquait : l'enfant jouait sans jamais voir où il en
 * était ni ce qu'il visait. On montre l'escalier entier — les trois étapes,
 * celle où il se trouve — et ce qu'il reste à faire pour franchir celle-ci.
 */
function BarreEtape({
  palier,
  reussies,
  total,
  termine,
}: {
  palier: Palier;
  reussies: number;
  total: number;
  termine: boolean;
}) {
  const part = total === 0 ? 0 : Math.min(1, reussies / total);
  // Au sommet de l'escalier, il n'y a pas d'étape suivante à annoncer.
  const derniere = palier.niveau === PALIERS[PALIERS.length - 1].niveau;
  return (
    <div className="rounded-[var(--radius-card)] border-2 border-line bg-white-warm p-4 shadow-[var(--shadow-tile)]">
      {/* Le titre occupe sa propre ligne. Posé à côté des quatre pastilles,
          « ÉTAPE 1 SUR 4 » se cassait en deux sur un écran de téléphone, et
          le 4 se retrouvait seul sous le reste. */}
      <div className="flex items-baseline justify-between gap-2">
        <span className="shrink-0 text-kid-xs font-black tracking-widest text-clay-dark uppercase">
          {termine ? 'Leçon terminée' : `Étape ${palier.niveau} sur ${PALIERS.length}`}
        </span>
        <span className="truncate text-kid font-extrabold">
          {termine ? 'Tu révises' : palier.nom}
        </span>
      </div>

      <div className="mt-2 flex items-center gap-2">
        {PALIERS.map((p) => {
          const franchi = termine || p.niveau < palier.niveau;
          const courant = !termine && p.niveau === palier.niveau;
          return (
            <span
              key={p.niveau}
              title={p.nom}
              className={
                'grid h-9 w-9 shrink-0 place-items-center rounded-full text-kid-sm font-black transition-all duration-300 ' +
                (franchi
                  ? 'bg-leaf text-white-warm'
                  : courant
                    ? 'halo bg-gold text-ink ring-4 ring-gold/30'
                    : 'bg-sand text-muted')
              }
            >
              {franchi ? '★' : p.niveau}
            </span>
          );
        })}
      </div>

      {/* Le fond doit trancher sur l'or : à la taille d'un téléphone, un
          sable pâle sous une barre dorée se lit comme une barre pleine. */}
      <div className="mt-3 h-4 overflow-hidden rounded-full bg-ink/15 inset-shadow-sm">
        <div
          className="h-full rounded-full bg-gold transition-[width] duration-700 ease-out"
          style={{ width: `${part * 100}%` }}
        />
      </div>
      <p className="mt-1.5 text-kid-sm font-bold text-ink-2">
        {termine
          ? 'Tu peux rejouer autant que tu veux.'
          : reussies >= total
            ? 'Étape réussie !'
            : `Encore ${total - reussies} ${total - reussies > 1 ? 'questions' : 'question'} ${
                derniere ? 'pour terminer la leçon' : `pour passer à l’étape ${palier.niveau + 1}`
              }`}
      </p>
    </div>
  );
}

/**
 * La barre de la manche de validation.
 *
 * Elle ne montre pas une progression mais un capital : les fautes restantes,
 * et il n'y en a aucune. Une barre qui se remplit dirait « tu avances » alors
 * que la seule chose qui compte est de n'avoir rien raté.
 *
 * Le rang de la série y figure, parce que la distance à tenir a changé : une
 * faute coûte une douzaine de questions et non trente, et il doit le savoir pendant
 * qu'il joue, pas seulement dans l'annonce.
 */
function BarreManche({
  faites,
  total,
  fautes,
  serie,
}: {
  faites: number;
  total: number;
  fautes: number;
  serie: { rang: number; total: number };
}) {
  return (
    <div
      className={
        'rounded-[var(--radius-card)] border-2 p-4 shadow-[var(--shadow-tile)] ' +
        (fautes > 0 ? 'border-clay/50 bg-clay/10' : 'border-leaf/50 bg-white-warm')
      }
    >
      <div className="flex items-baseline justify-between gap-2">
        <span className="shrink-0 text-kid-xs font-black tracking-widest text-clay-dark uppercase">
          {serie.total > 1 ? `Série ${serie.rang}/${serie.total}` : 'La manche'}
        </span>
        <span className="truncate text-kid font-extrabold">
          Question {Math.min(faites + 1, total)} sur {total}
        </span>
      </div>
      <p className="mt-2 text-kid-sm font-bold text-ink-2">
        {fautes === 0
          ? 'Sans faute pour l’instant. Continue !'
          : `${fautes} ${fautes > 1 ? 'fautes' : 'faute'} : ${serie.total > 1 ? 'cette série' : 'la manche'} sera à refaire. Va jusqu’au bout, tu apprends à chaque question.`}
      </p>
    </div>
  );
}

/**
 * Le sablier de la dernière étape.
 *
 * Il ne sert qu'au Défi : partout ailleurs, presser un enfant qui découvre
 * une notion l'empêche justement de la comprendre. Ici la notion est déjà
 * sue, et c'est la vitesse qu'on vient chercher.
 *
 * Le temps écoulé vaut une réponse manquée — la notion revient, sans drame.
 */
function Chrono({
  cle,
  secondes,
  gele,
  surFin,
}: {
  cle: string;
  secondes: number;
  gele: boolean;
  surFin: () => void;
}) {
  const [reste, setReste] = useState(secondes);
  const fini = useRef(false);
  // La fonction de fin change à chaque rendu du parent. Dans une ref, elle ne
  // relance pas le compte à rebours.
  const fin = useRef(surFin);
  fin.current = surFin;

  useEffect(() => {
    setReste(secondes);
    fini.current = false;
  }, [cle, secondes]);

  useEffect(() => {
    if (gele || fini.current) return;
    if (reste <= 0) {
      fini.current = true;
      fin.current();
      return;
    }
    const t = setTimeout(() => setReste((r) => r - 1), 1000);
    return () => clearTimeout(t);
  }, [reste, gele]);

  const part = Math.max(0, reste / secondes);
  const urgent = reste <= 5;

  return (
    <div className="flex items-center gap-2" aria-label={`${reste} secondes`}>
      <span
        className={
          'grid h-8 w-8 shrink-0 place-items-center rounded-full text-kid-sm font-black tabular-nums ' +
          (urgent ? 'bg-clay text-white-warm' : 'bg-sand text-ink')
        }
      >
        {Math.max(0, reste)}
      </span>
      <span className="h-2.5 flex-1 overflow-hidden rounded-full bg-ink/15">
        <span
          className={'block h-full rounded-full ' + (urgent ? 'bg-clay' : 'bg-leaf')}
          style={{ width: `${part * 100}%`, transition: 'width 1s linear' }}
        />
      </span>
    </div>
  );
}

/**
 * Une nouvelle à annoncer, et une seule.
 *
 * Une bonne réponse peut en déclencher trois d'un coup : l'image de la
 * notion, l'étape franchie, le rang atteint. Entassées dans un même message,
 * elles se noyaient — l'enfant lisait la dernière et ne voyait pas qu'il
 * avait changé de rang. Elles défilent donc une par une, de la plus
 * ordinaire à la plus rare, chacune avec son titre, son image et les étoiles
 * qu'elle a values.
 */
type Fenetre = {
  ton: 'juste' | 'faux' | 'fete';
  son: 'juste' | 'faux' | 'fete' | 'etape';
  titre: string;
  texte: string;
  /** Les étoiles de ce moment-là, pas le total de la réponse. */
  points: number;
  /** L'illustration à montrer ; sans elle, c'est Niba qui paraît. */
  vignette: string | null;
  humeur: Humeur | null;
};

function Etape({
  parentId,
  childId,
  lessonId,
  rang,
}: {
  parentId: string;
  childId: string;
  lessonId: string;
  /** La place de la classe dans l'école : elle choisit la façon d'écrire. */
  rang: number | null;
}) {
  const qc = useQueryClient();
  const navigate = useNavigate();
  const [index, setIndex] = useState(0);
  const [verrouille, setVerrouille] = useState(false);
  const [file, setFile] = useState<Fenetre[]>([]);
  /** La réponse en cours vient de franchir l'étape : la dernière fenêtre
      rendra la main au bilan, et non à la question suivante. */
  const [franchieMaintenant, setFranchieMaintenant] = useState(false);
  const [gagnes, setGagnes] = useState(0);
  const [justes, setJustes] = useState(0);
  /** Notions validées pendant cette séance, pour faire avancer la barre tout de suite. */
  const [validees, setValidees] = useState<Set<string>>(new Set());
  const [revelees, setRevelees] = useState<
    Array<{ id: string; illustration: string | null; statement: string }>
  >([]);
  const [erreur, setErreur] = useState<unknown>(null);
  /** Le bilan ne se montre qu'une fois le coffre ouvert. */
  const [coffreOuvert, setCoffreOuvert] = useState(false);
  /** Les notions ratées pendant la manche en cours. */
  const [ratees, setRatees] = useState<Set<string>>(new Set());
  /** La manche ne démarre pas toute seule : on annonce l'enjeu d'abord. */
  const [mancheLancee, setMancheLancee] = useState(false);
  /**
   * Le moment où la question est apparue.
   *
   * Le temps passé par question est l'un des quatre faits que le rapport du
   * parent promet, et il n'était enregistré nulle part : recordAttempt
   * acceptait une durée depuis le début, personne ne la lui passait, et la
   * colonne restait vide. Une promesse qui ne se remplit jamais vaut moins
   * qu'une promesse qu'on ne fait pas.
   */
  const apparue = useRef<number>(Date.now());

  // La séance ne bouge pas sous les yeux de l'enfant : elle est rechargée au
  // seul moment où on le décide, par « Continuer ». Laissée fraîche, elle se
  // rechargeait au retour sur l'onglet — et le bilan d'une étape annonçait
  // alors l'étape suivante, qui n'était pas encore jouée.
  const seance = useQuery({
    queryKey: ['seance', childId, lessonId],
    queryFn: () => construireSeance(childId, lessonId),
    staleTime: Infinity,
    refetchOnWindowFocus: false,
    refetchOnMount: 'always',
  });

  // Chaque fenêtre sonne quand elle arrive, et non toutes au moment de la
  // réponse : c'est ce qui fait qu'une bonne nouvelle s'entend.
  useEffect(() => {
    if (file.length > 0) jouerSon(file[0].son);
  }, [file]);

  // Le chronomètre du temps de réflexion repart à chaque question. Il ne
  // compte donc pas le temps passé à lire la correction de la précédente.
  useEffect(() => {
    apparue.current = Date.now();
  }, [index, mancheLancee]);

  /** Nouvelle série de questions, à la suite : l'enfant ne retourne pas au menu. */
  function continuer() {
    setIndex(0);
    setVerrouille(false);
    setGagnes(0);
    setJustes(0);
    setValidees(new Set());
    setRevelees([]);
    setFile([]);
    setFranchieMaintenant(false);
    setCoffreOuvert(false);
    setRatees(new Set());
    setMancheLancee(false);
    seance.refetch();
  }

  if (seance.isLoading) return <Loading label="Je prépare ton étape…" />;
  if (seance.error) return <ErrorNote error={seance.error} />;

  const s = seance.data;

  if (!s || s.questions.length === 0) {
    return (
      <div className="rounded-[var(--radius-card)] border border-line bg-white-warm p-6 text-center">
        <Illustration cle="repos" forme="objet" alt="" className="mx-auto h-28 w-28" />
        <h2 className="mt-3 text-kid-lg font-extrabold">Rien à jouer ici</h2>
        <p className="mt-1 text-kid-sm text-muted">Cette leçon n’a pas encore de questions.</p>
      </div>
    );
  }

  const estManche = s.mode === 'manche';
  const estReprise = s.mode === 'reprise';

  // L'enjeu s'annonce avant la première question. Lancer douze questions sans
  // prévenir qu'une seule faute les annule serait un piège : l'enfant doit
  // savoir dans quoi il entre, et pouvoir y entrer quand il se sent prêt.
  //
  // Et il doit savoir que ce qu'il gagne ne se rejoue pas. C'est la promesse
  // du découpage en séries : sans elle, « une faute et c'est à refaire »
  // s'entend encore comme les trente questions d'avant.
  if (estManche && !mancheLancee) {
    const aRegagner = s.validation.serieARegagner;
    const plusieurs = s.serie.total > 1;
    const derniere = plusieurs && s.serie.tenues + 1 === s.serie.total;
    const restantes = s.serie.total - s.serie.tenues;
    return (
      <div className="grid gap-3">
        <div className="monte overflow-hidden rounded-[var(--radius-card)] border-2 border-gold bg-white-warm text-center shadow-[var(--shadow-card)]">
          <div className="bg-gold/25 px-6 py-7">
            <Mascotte humeur="encourage" taille={96} className="mx-auto" />
            <p className="mt-2 text-kid-xs font-black tracking-widest text-clay-dark uppercase">
              {/* « Dernière épreuve » au-dessus de « Série 1 sur 9 » se
                  contredit tout seul : l'épreuve n'est dernière que pour la
                  leçon, et l'enfant lit le titre juste en dessous. */}
              {aRegagner
                ? 'À regagner'
                : derniere
                  ? 'Dernière série'
                  : plusieurs
                    ? 'La validation'
                    : 'Dernière épreuve'}
            </p>
            <h2 className="mt-1 text-kid-2xl font-black">
              {plusieurs ? `Série ${s.serie.rang} sur ${s.serie.total}` : 'La manche'}
            </h2>
          </div>
          <div className="px-6 py-6">
            <p className="text-kid font-bold">
              {aRegagner
                ? 'Tu avais gagné cette série, puis tu as raté une notion. Il faut la regagner.'
                : derniere
                  ? 'Plus qu’une série, et la leçon est validée !'
                  : plusieurs
                    ? `Tu as gravi les quatre étapes. La leçon se valide en ${s.serie.total} séries, chacune sans faute.`
                    : 'Tu as gravi les quatre étapes. Il reste à valider la leçon.'}
            </p>
            <ul className="mx-auto mt-4 grid max-w-sm gap-2 text-left text-kid-sm text-ink-2">
              <li className="flex gap-2">
                <span className="font-black text-clay-dark">{s.questions.length}</span>
                <span>
                  {plusieurs
                    ? `questions : ${s.notionsDeLaSerie.length} ${s.notionsDeLaSerie.length > 1 ? 'notions' : 'notion'} de la leçon, complètement.`
                    : 'questions : toute la leçon, du début à la fin.'}
                </span>
              </li>
              <li className="flex gap-2">
                <span className="font-black text-clay-dark">0</span>
                <span>
                  faute permise. Une seule, et {plusieurs ? 'cette série' : 'la manche'} est à
                  refaire.
                </span>
              </li>
              {plusieurs ? (
                <li className="flex gap-2">
                  <span className="font-black text-leaf">★</span>
                  <span>
                    Une série gagnée reste gagnée : tu ne la rejoues pas.{' '}
                    {/* « Il en reste 9 » juste après se lit « 9 APRÈS
                        celle-ci ». On dit donc ce qu'il tient déjà, qui est
                        de toute façon ce qu'on veut lui montrer. */}
                    {restantes === 1
                      ? 'Celle-ci est la dernière.'
                      : s.serie.tenues > 0
                        ? `Tu en as déjà ${s.serie.tenues} ; il t’en reste ${restantes}.`
                        : `Il y en a ${s.serie.total} à gagner en tout.`}
                  </span>
                </li>
              ) : null}
              <li className="flex gap-2">
                <span className="font-black text-clay-dark">✓</span>
                <span>
                  Tu vas jusqu’au bout même si tu te trompes : tu verras toutes les réponses.
                </span>
              </li>
            </ul>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              <GrosBouton onClick={() => setMancheLancee(true)}>Je suis prêt</GrosBouton>
              <GrosBouton variante="douce" onClick={() => navigate(`/enfant/${childId}`)}>
                Plus tard
              </GrosBouton>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const reussies = s.reussies + validees.size;
  const etapeFranchie = !s.termine && reussies >= s.total;

  if (index >= s.questions.length) {
    // Le bilan de la manche ne ressemble à aucun autre : il ne dit pas ce qui
    // a été gagné, il dit si la leçon est validée. Le coffre n'a pas sa place
    // ici quand elle ne l'est pas — il annoncerait une récompense à qui vient
    // d'échouer.
    if (estManche) {
      const gagnee = justes === s.questions.length;
      const manquantes = s.questions.length - justes;
      // La série gagnée ne valide la leçon que si c'était la dernière qui
      // manquait. Les autres sont déjà tenues : on le sait sans rien relire.
      const plusieurs = s.serie.total > 1;
      const valideeMaintenant = gagnee && s.serie.tenues + 1 === s.serie.total;
      const restantes = s.serie.total - s.serie.tenues - (gagnee ? 1 : 0);
      // Recalculée ici, et non passée depuis la réponse : la fonction est
      // pure, donc les deux endroits disent forcément la même chose.
      const consolation = gagnee
        ? 0
        : pointsConsolation(justes, s.questions.length, s.meilleurJustes);
      return (
        <div className="grid gap-3">
          {gagnee ? <Confettis /> : null}
          <div className="monte overflow-hidden rounded-[var(--radius-card)] border-2 border-line bg-white-warm text-center shadow-[var(--shadow-card)]">
            <div className={'px-6 py-7 ' + (gagnee ? 'bg-leaf/25' : 'bg-clay/15')}>
              <Mascotte humeur={gagnee ? 'fete' : 'encourage'} taille={96} className="mx-auto" />
              <h2 className="mt-2 text-kid-2xl font-black">
                {valideeMaintenant
                  ? 'Leçon validée !'
                  : gagnee
                    ? `Série ${s.serie.rang} gagnée !`
                    : 'Pas encore'}
              </h2>
              <p className="mt-1 text-kid font-bold text-ink-2">
                {justes} bonnes réponses sur {s.questions.length}
              </p>
              {gagnee ? (
                <p className="grimpe mt-3 text-kid-lg font-black text-gold">
                  +{pointsManche(s.questions.length)} ★
                </p>
              ) : consolation > 0 ? (
                <p className="grimpe mt-3 text-kid-lg font-black text-gold">+{consolation} ★</p>
              ) : null}
            </div>
            <div className="px-6 py-6">
              <p className="text-kid-sm text-muted">
                {valideeMaintenant
                  ? 'Toute la leçon, sans une faute. Tu la sais.'
                  : gagnee
                    ? `Sans une faute : cette série est acquise, tu ne la rejoues pas. Il en reste ${restantes} pour valider la leçon.`
                    : consolation > 0
                      ? `C’est ton meilleur score sur cette série. Il te manque ${manquantes} ${manquantes > 1 ? 'questions' : 'question'} : on va les revoir.`
                      : `Il te manque ${manquantes} ${manquantes > 1 ? 'questions' : 'question'}. On va revoir ce que tu as raté, puis tu retenteras ${plusieurs ? 'la série' : 'la manche'}.`}
              </p>
              <div className="mt-5 flex flex-wrap justify-center gap-2">
                <GrosBouton onClick={continuer}>
                  {valideeMaintenant
                    ? 'Continuer'
                    : gagnee
                      ? 'La série suivante'
                      : 'Revoir ce que j’ai raté'}
                </GrosBouton>
                <GrosBouton variante="douce" onClick={() => navigate(`/enfant/${childId}`)}>
                  Mes leçons
                </GrosBouton>
              </div>
            </div>
          </div>
        </div>
      );
    }

    const reste = s.total - reussies;

    // Le butin dit la même chose que l'ancien récapitulatif. La différence
    // tient au geste : l'enfant ouvre, au lieu de lire ce qui est déjà là.
    const butin: Butin[] = [
      { icone: '★', texte: `+${gagnes} étoiles` },
      ...(revelees.length > 0
        ? [
            {
              icone: '🖼',
              texte:
                revelees.length > 1
                  ? `${revelees.length} images pour ta collection`
                  : 'Une image pour ta collection',
            },
          ]
        : []),
      ...(etapeFranchie ? [{ icone: '🪜', texte: `Étape ${s.palier.niveau} franchie` }] : []),
      { icone: '✓', texte: `${justes} bonnes réponses sur ${s.questions.length}` },
    ];

    return (
      <div className="grid gap-3">
        {coffreOuvert && (etapeFranchie || revelees.length > 0) ? <Confettis /> : null}
        <BarreEtape palier={s.palier} reussies={reussies} total={s.total} termine={s.termine} />

        <div className="monte overflow-hidden rounded-[var(--radius-card)] border border-line bg-white-warm text-center shadow-[var(--shadow-card)]">
          <div className={'px-6 py-7 ' + (etapeFranchie ? 'bg-leaf/25' : 'bg-gold/25')}>
            <Mascotte humeur="fete" taille={88} className="mx-auto" />
            <h2 className="mt-2 text-kid-2xl font-black">
              {etapeFranchie ? 'Étape réussie !' : 'Bien joué !'}
            </h2>
            <div className="mt-4">
              <Coffre
                butin={butin}
                titre={etapeFranchie ? 'Ton coffre d’étape' : 'Ton coffre'}
                onOuvert={() => setCoffreOuvert(true)}
              />
            </div>
          </div>

          {coffreOuvert && revelees.length > 0 ? (
            <div className="border-b border-line px-6 py-5">
              <p className="text-kid-xs font-black tracking-widest text-clay-dark uppercase">
                {revelees.length > 1 ? `${revelees.length} images gagnées` : 'Une image gagnée'}
              </p>
              <ul className="mt-3 flex flex-wrap justify-center gap-3">
                {revelees.map((r, i) => (
                  <li key={r.id} className="w-24">
                    <div
                      className="halo revele overflow-hidden rounded-2xl border-2 border-gold"
                      style={{ animationDelay: `${i * 220}ms` }}
                    >
                      <Illustration
                        cle={r.illustration}
                        forme="objet"
                        alt={r.statement}
                        className="h-24 w-24 object-cover"
                      />
                    </div>
                  </li>
                ))}
              </ul>
              <p className="mt-3 text-kid-sm text-muted">Dans ta collection !</p>
            </div>
          ) : null}

          {coffreOuvert ? (
            <div className="monte px-6 py-5">
              <p className="text-kid-sm text-muted">
                {etapeFranchie
                  ? PALIERS[s.palier.niveau]
                  ? `Tu passes en « ${PALIERS[s.palier.niveau].nom} ».`
                  : 'Tu as fini les quatre étapes de cette leçon.'
                  : s.termine
                    ? 'Tu connais toute la leçon.'
                    : reste > 0
                      ? `Encore ${reste} ${reste > 1 ? 'questions' : 'question'} à réussir pour l’étape ${s.palier.niveau + 1}.`
                      : 'On continue.'}
              </p>
              <div className="mt-4 flex flex-wrap justify-center gap-2">
                <GrosBouton onClick={continuer}>
                  {etapeFranchie ? 'Étape suivante' : 'Continuer'}
                </GrosBouton>
                <GrosBouton variante="douce" onClick={() => navigate(`/enfant/${childId}`)}>
                  Mes leçons
                </GrosBouton>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    );
  }

  const question = s.questions[index];

  async function repondre(reponse: Reponse) {
    if (verrouille || !s) return;
    setVerrouille(true);
    setErreur(null);
    try {
      // La notion tombe pour cette étape : c'est ce qui fait avancer la barre.
      const valide = reponse.correct && !validees.has(question.notion.id);
      const suite = valide ? new Set(validees).add(question.notion.id) : validees;
      if (valide) setValidees(suite);

      const franchie = !s.termine && s.reussies + suite.size >= s.total;

      // La manche se juge à la fin, et seulement à la fin. Elle n'est pas
      // interrompue par une faute : l'enfant doit voir les corrections des
      // questions qui lui restaient.
      const ratee = estManche && !reponse.correct;
      const toutesRatees = ratee ? new Set(ratees).add(question.notion.id) : ratees;
      if (ratee) setRatees(toutesRatees);
      const derniereDeLaManche = estManche && index + 1 === s.questions.length;
      const justesFinal = justes + (reponse.correct ? 1 : 0);
      const mancheGagnee = derniereDeLaManche && justesFinal === s.questions.length;
      // L'image tombe quand la notion est validée à son étape « Maîtrise » :
      // le même geste que celui qui fait avancer la barre, donc visible.
      const acquise = valide && s.palier.niveau === etapeImage(question.notion);

      // Les trois bonus partent avec la tentative : une seule écriture, et
      // le total affiché est celui qui est réellement en base.
      // La manche ratée de peu rapporte quand même, à deux conditions :
      // avoir dépassé 80 %, et avoir fait mieux que la dernière fois sur
      // cette leçon. C-est le progrès qu-on paie, pas la répétition.
      const consolation =
        derniereDeLaManche && !mancheGagnee
          ? pointsConsolation(justesFinal, s.questions.length, s.meilleurJustes)
          : 0;

      const bonus =
        (valide ? POINTS_NOTION : 0) +
        (acquise ? POINTS_IMAGE : 0) +
        (franchie ? POINTS_ETAPE : 0) +
        (mancheGagnee ? pointsManche(s.questions.length) : 0) +
        consolation;

      // Le total d'étoiles avant la réponse, lu dans le cache : il sert à
      // savoir si cette réponse-là fait franchir un rang.
      const etoilesAvant = qc.getQueryData<number>(['points', childId]) ?? 0;

      const bilan = await recordAttempt({
        parentId,
        childId,
        item: question.item,
        answer: reponse.donnee,
        correct: reponse.correct,
        durationMs: Date.now() - apparue.current,
        bonus,
      });

      const avant = etatRang(etoilesAvant).rang;
      const apres = etatRang(etoilesAvant + bilan.points).rang;
      const rangMonte = apres.nom !== avant.nom ? apres : null;

      // Une fenêtre par nouvelle, de la plus ordinaire à la plus rare.
      // Entassées dans un seul message, les trois se noyaient : l'enfant
      // lisait « tu passes en Défi » et ne voyait pas qu'il avait changé de
      // rang. Chacune a maintenant son titre, son image et ses étoiles.
      const suivante = PALIERS[s.palier.niveau];
      const fenetres: Fenetre[] = [
        {
          ton: reponse.correct ? 'juste' : 'faux',
          son: reponse.correct ? 'juste' : 'faux',
          titre: reponse.correct
            ? 'Bravo !'
            : (reponse.donnee as { expire?: boolean })?.expire
              ? 'Trop tard !'
              : 'Presque…',
          texte:
            question.item.explain ??
            (reponse.correct ? 'Bien joué.' : 'On la repose tout à l’heure.'),
          // Les étoiles de la réponse elle-même : le reste arrive avec les
          // fenêtres qui l'ont mérité.
          points: (reponse.correct ? POINTS_PAR_ETAPE * question.item.level : 0) +
            (valide ? POINTS_NOTION : 0),
          vignette: null,
          humeur: reponse.correct ? 'fete' : 'encourage',
        },
      ];

      if (acquise) {
        fenetres.push({
          ton: 'fete',
          son: 'fete',
          titre: 'Image gagnée !',
          texte: 'Elle rejoint ta collection.',
          points: POINTS_IMAGE,
          vignette: question.notion.illustration,
          humeur: null,
        });
      }

      if (franchie) {
        fenetres.push({
          ton: 'fete',
          son: 'etape',
          titre: 'Étape réussie !',
          texte: suivante
            ? `Tu passes en « ${suivante.nom} » !`
            : 'Tu connais toute la leçon !',
          points: POINTS_ETAPE,
          vignette: 'medaille',
          humeur: null,
        });
      }

      if (rangMonte) {
        fenetres.push({
          ton: 'fete',
          son: 'etape',
          titre: 'Nouveau rang !',
          texte: `Tu es maintenant ${rangMonte.nom} !`,
          // Le rang ne rapporte rien : il récompense le chemin déjà payé.
          points: 0,
          vignette: rangMonte.embleme,
          humeur: null,
        });
      }

      // La série jouée est écrite une fois sa dernière question répondue.
      // C'est elle qui porte la validation, et les notions à redonner si
      // l'enfant ferme l'app avant la reprise. `notions` dit ce qu'elle
      // couvrait : sans cette liste, la ligne ne se déduit plus.
      if (derniereDeLaManche) {
        await enregistrerManche({
          parentId,
          childId,
          lessonId,
          questions: s.questions.length,
          justes: justesFinal,
          notionsRatees: [...toutesRatees],
          notions: s.notionsDeLaSerie,
        });
        if (mancheGagnee) {
          // La médaille n'est pas pour la série : elle est pour la leçon. Une
          // série gagnée sur trois ne se célèbre pas comme une leçon sue.
          const derniereSerie = s.serie.tenues + 1 === s.serie.total;
          fenetres.push({
            ton: 'fete',
            son: 'etape',
            titre: derniereSerie ? 'Leçon validée !' : 'Série sans faute !',
            texte: derniereSerie
              ? 'Toute la leçon, sans une faute.'
              : `Série ${s.serie.rang} sur ${s.serie.total}. Elle est acquise.`,
            points: pointsManche(s.questions.length),
            vignette: derniereSerie ? 'medaille' : null,
            humeur: null,
          });
        } else if (consolation > 0) {
          // Pas de médaille et pas de confettis : la leçon n-est pas validée.
          // Mais le progrès est nommé, parce qu-il a eu lieu.
          fenetres.push({
            ton: 'juste',
            son: 'juste',
            titre: 'Ton meilleur score !',
            texte: `${justesFinal} bonnes réponses sur ${s.questions.length}.`,
            points: consolation,
            vignette: null,
            humeur: 'encourage',
          });
        }
        qc.invalidateQueries({ queryKey: ['manches', childId] });
      }

      setFile(fenetres);
      setFranchieMaintenant(franchie);

      setGagnes((g) => g + bilan.points);
      if (acquise) {
        setRevelees((d) => [
          ...d,
          {
            id: question.notion.id,
            illustration: question.notion.illustration,
            statement: question.notion.statement,
          },
        ]);
      }
      if (reponse.correct) setJustes((j) => j + 1);
      qc.invalidateQueries({ queryKey: ['points', childId] });
      qc.invalidateQueries({ queryKey: ['tableau', childId] });
      qc.invalidateQueries({ queryKey: ['duel'] });
      qc.invalidateQueries({ queryKey: ['images', childId, lessonId] });
    } catch (err) {
      setErreur(err);
      setFile([]);
      setVerrouille(false);
    }
  }

  /**
   * Le bouton de la fenêtre affichée.
   *
   * Tant qu'il reste des nouvelles à annoncer, il passe simplement à la
   * suivante. C'est la dernière qui rend la main au jeu.
   */
  function fenetreSuivante() {
    if (file.length > 1) {
      setFile((f) => f.slice(1));
      return;
    }
    setFile([]);
    // Une étape franchie arrête la série : la suite se joue au niveau du
    // dessus. On passe d'abord par le bilan — c'est là qu'est le coffre, et
    // c'est le moment de la séance où il a le plus de valeur. Enchaîner
    // directement sur l'étape suivante priverait l'enfant de sa récompense.
    setIndex(franchieMaintenant ? (seance.data?.questions.length ?? 0) : index + 1);
    setVerrouille(false);
  }

  const derniere = index + 1 === s.questions.length;

  return (
    <div className="grid gap-3">
      {estManche ? (
        <BarreManche
          faites={index}
          total={s.questions.length}
          fautes={ratees.size}
          serie={s.serie}
        />
      ) : estReprise ? (
        <div className="rounded-[var(--radius-card)] border-2 border-clay/50 bg-clay/10 p-4 shadow-[var(--shadow-tile)]">
          <span className="text-kid-xs font-black tracking-widest text-clay-dark uppercase">
            Ce que tu as raté
          </span>
          <p className="mt-1 text-kid-sm font-bold text-ink-2">
            On revoit {s.total} {s.total > 1 ? 'notions' : 'notion'}, puis tu retentes
            {s.serie.total > 1 ? ` la série ${s.serie.rang}` : ' la manche'}.
          </p>
        </div>
      ) : (
        <BarreEtape palier={s.palier} reussies={reussies} total={s.total} termine={s.termine} />
      )}

      <section className="rounded-[var(--radius-card)] border border-line bg-white-warm p-5 shadow-[var(--shadow-card)] sm:p-6">
        <div className="flex items-center justify-between gap-3">
          <Galets total={s.questions.length} faits={index} />
          <span className="rounded-full bg-sand px-3 py-1 text-kid-xs font-black tracking-wide uppercase">
            {estManche ? 'Sans faute' : estReprise ? 'On reprend' : s.palier.promesse}
          </span>
        </div>

        {/* Le sablier suit le niveau de la QUESTION, pas celui de la séance.
            Dans une série, les questions de toutes les étapes se suivent :
            chronométrer une question de Découverte parce que la séance est
            au sommet de l’escalier n’aurait aucun sens. */}
        {estChronometre(question.item.level) ? (
          <div className="mt-3">
            <Chrono
              cle={question.item.id}
              secondes={SECONDES_DEFI}
              gele={verrouille || file.length > 0}
              /* Le temps écoulé vaut une réponse manquée : la notion revient. */
              surFin={() => repondre({ correct: false, donnee: { expire: true } })}
            />
          </div>
        ) : null}

        <div className="mt-5">
          {/* La clé force un lecteur neuf à chaque question. Sans elle, React
              gardait le même composant d'une question à la suivante et, avec
              lui, tout son état : l'ordre tiré au sort et les liens déjà
              posés. Une association à trois paires qui suivait une question à
              deux n'affichait que deux étiquettes à droite — la troisième
              n'existait pas — et se concluait toute seule après deux liens,
              comptée fausse. 32 des 45 leçons enchaînent des questions d'un
              même type et de tailles différentes. */}
          <ItemPlayer
            key={index + ':' + question.item.id}
            item={question.item}
            onRepondre={repondre}
            verrouille={verrouille}
            rang={rang}
            visuel={
              question.notion.illustration ? (
                <Illustration
                  cle={question.notion.illustration}
                  forme="objet"
                  alt=""
                  priorite
                  className="h-14 w-14 shrink-0 rounded-2xl object-cover sm:h-20 sm:w-20"
                />
              ) : null
            }
          />
        </div>

        {erreur ? (
          <div className="mt-4">
            <ErrorNote error={erreur} />
          </div>
        ) : null}

        {/* Les confettis n'accompagnent que la fête : sortis à chaque bonne
            réponse, ils ne voudraient plus rien dire au bout de dix minutes. */}
        {file[0]?.ton === 'fete' ? <Confettis key={file.length} /> : null}

        {file[0] ? (
          <Popup
            // La clé force une nouvelle fenêtre à chaque nouvelle : sans
            // elle, React réutiliserait la même et l'animation d'entrée ne
            // rejouerait pas — les trois annonces se succéderaient sans qu'on
            // voie le changement.
            key={file.length}
            ton={file[0].ton}
            titre={file[0].titre}
            action={
              file.length > 1
                ? 'Super !'
                : franchieMaintenant
                  ? 'Étape suivante'
                  : derniere
                    ? estManche
                      ? 'Voir si c’est validé'
                      : 'Voir mon résultat'
                    : 'Question suivante'
            }
            onFermer={fenetreSuivante}
            vignette={
              file[0].vignette ? (
                <Illustration
                  cle={file[0].vignette}
                  forme="objet"
                  alt=""
                  className="halo h-28 w-28 rounded-2xl object-cover"
                />
              ) : (
                <Mascotte humeur={file[0].humeur ?? 'fete'} taille={112} />
              )
            }
          >
            {file[0].texte}
            {file[0].points > 0 ? (
              <span className="grimpe mt-3 block text-kid-lg font-black text-gold">
                +{file[0].points} ★
              </span>
            ) : null}
          </Popup>
        ) : null}
      </section>
    </div>
  );
}

export default function ChildSpace() {
  const { childId, lessonId } = useParams<{ childId: string; lessonId: string }>();
  const [onglet, setOnglet] = useState<'mission' | 'lecon'>('mission');

  // La voix ne doit pas poursuivre l'enfant d'un écran à l'autre.
  useEffect(() => stopper, []);

  // L'identifiant du parent vient de la session déjà en mémoire. Passer par
  // auth.getUser() ajoutait un aller-retour réseau avant le premier affichage,
  // et l'enfant restait devant un écran vide le temps de la réponse.
  const { session } = useSession();
  const parentId = session?.user.id ?? null;

  const child = useQuery({
    queryKey: ['child', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('children')
        // Le rang de la classe décide de la façon d’écrire une réponse —
        // étiquettes aux petites classes, clavier ensuite. Le charger ici
        // évite une requête de plus au moment de poser la question.
        .select('id, first_name, avatar, classes(rank)')
        .eq('id', childId!)
        .single();
      if (error) throw error;
      return data;
    },
  });

  const lesson = useQuery({
    queryKey: ['lesson-bundle', lessonId],
    enabled: Boolean(lessonId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('lessons')
        .select(
          'id, title, summary, lang, illustration, subject_id, subjects(label), ' +
            'notions(id, kind, statement, sort_order, illustration, parent_id, lesson_id, status, created_at, ' +
            'explanations(id, register, body, notion_id, parent_id, status, created_at)), ' +
            'videos(id, external_url, poster_url, duration_s, status, lesson_id, parent_id, manifest, voice_preset, storage_path, created_at)',
        )
        .eq('id', lessonId!)
        .maybeSingle();
      if (error) throw error;
      return data as unknown as LessonBundle | null;
    },
  });

  // Les notions dont l'image est gagnée, lues au même endroit que la
  // collection : le paquet de fiches et le tableau de bord ne peuvent pas
  // afficher deux vérités différentes de la même leçon.
  const images = useQuery({
    queryKey: ['images', childId, lessonId],
    enabled: Boolean(childId && lessonId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('notions')
        .select('id, items(id, level, status)')
        .eq('lesson_id', lessonId!)
        .eq('status', 'approved');
      if (error) throw error;
      const notions = ((data ?? []) as unknown as Array<{
        id: string;
        items: Array<{ id: string; level: number; status: string }>;
      }>).map((n) => ({ id: n.id, items: (n.items ?? []).filter((i) => i.status === 'approved') }));

      const justes = await supabase
        .from('attempts')
        .select('item_id')
        .eq('child_id', childId!)
        .eq('correct', true);
      if (justes.error) throw justes.error;

      const reussies = reussitesParNiveau(notions, justes.data ?? []);
      return new Set(notions.filter((n) => imageGagnee(n, reussies)).map((n) => n.id));
    },
  });

  /**
   * Les séries sans faute enchaînées, toutes leçons confondues.
   *
   * Elle se lit sur toutes les manches de l-enfant, et pas sur celles de la
   * leçon ouverte : un compteur qui se remettrait à zéro en changeant de
   * leçon ne voudrait rien dire. Les cinquante dernières suffisent — une
   * suite plus longue que cinquante séries sans faute n-a jamais existé.
   */
  const serie = useQuery({
    queryKey: ['manches', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('manches')
        .select('lesson_id, questions, justes, reussie, notions_ratees, created_at')
        .eq('child_id', childId!)
        .order('created_at', { ascending: false })
        .limit(50);
      if (error) throw error;
      return serieParfaite((data ?? []) as MancheRow[]);
    },
  });

  const points = useQuery({
    queryKey: ['points', childId],
    enabled: Boolean(childId),
    queryFn: async () => {
      const { data, error } = await supabase
        .from('rewards')
        .select('value')
        .eq('child_id', childId!);
      if (error) throw error;
      return (data ?? []).reduce((somme, r) => somme + (r.value ?? 0), 0);
    },
  });

  if (lesson.isLoading || child.isLoading) return <Loading />;
  if (lesson.error) return <ErrorNote error={lesson.error} />;

  const bundle = lesson.data;
  const notions = [...(bundle?.notions ?? [])]
    .filter((n) => n.status === 'approved')
    .sort((a, b) => a.sort_order - b.sort_order);
  const video = bundle?.videos?.[0];
  const filmUrl = urlFilm(video, (chemin) =>
    supabase.storage.from('films').getPublicUrl(chemin).data.publicUrl,
  );

  return (
    <main className="enfant ciel min-h-screen pb-12">
      <div className="mx-auto max-w-2xl px-4 pt-4 sm:px-6">
        <header className="flex items-center justify-between gap-3">
          <Link
            to={
              bundle?.subject_id
                ? `/enfant/${childId}/matiere/${bundle.subject_id}`
                : `/enfant/${childId}`
            }
            className="tuile flex items-center gap-2 rounded-full bg-white-warm/80 py-2 pr-4 pl-3 text-kid-sm font-bold"
          >
            <span aria-hidden="true">←</span>
            <span className="max-w-[11.5rem] truncate">
              {bundle?.subjects?.label ?? 'Mes leçons'}
            </span>
          </Link>
          <div className="flex items-center gap-2">
            {serie.data ? (
              <span
                className="flex items-center gap-1.5 rounded-full bg-leaf/30 px-3 py-2 text-kid-sm font-black"
                title={`${serie.data} série${serie.data > 1 ? 's' : ''} sans faute de suite`}
              >
                <span aria-hidden="true">🎯</span>
                {serie.data}
              </span>
            ) : null}
            <span className="flex items-center gap-1.5 rounded-full bg-gold/35 px-4 py-2 text-kid-sm font-black">
              <span aria-hidden="true">★</span>
              {points.data ?? 0}
            </span>
          </div>
        </header>

        {!bundle ? (
          <div className="mt-8 rounded-[var(--radius-card)] border border-line bg-white-warm p-6 text-center">
            <h1 className="text-kid-lg font-extrabold">Pas encore de leçon</h1>
            <p className="mt-2 text-kid-sm text-muted">
              Un parent doit d’abord en publier une depuis l’espace parent.
            </p>
          </div>
        ) : (
          <>
            <section className="relative mt-4 overflow-hidden rounded-[var(--radius-card)] shadow-[var(--shadow-card)]">
              <Illustration
                cle={bundle.illustration}
                forme="scene"
                alt=""
                priorite
                className={
                  'w-full object-cover transition-[height] duration-300 ' +
                  (onglet === 'lecon' ? 'h-24 sm:h-28' : 'h-40 sm:h-52')
                }
              />
              <div
                className={
                  'absolute inset-x-0 bottom-0 bg-gradient-to-t from-ink/80 via-ink/35 to-transparent px-5 pb-3 ' +
                  (onglet === 'lecon' ? 'pt-6' : 'pt-12 pb-4')
                }
              >
                <p className="text-kid-xs font-black tracking-widest text-gold uppercase">
                  {bundle.subjects?.label ?? 'Leçon'}
                </p>
                <h1
                  className={
                    'line-clamp-2 leading-tight font-black text-white-warm text-balance ' +
                    (onglet === 'lecon' || bundle.title.length > 28 ? 'text-kid-lg' : 'text-kid-2xl')
                  }
                >
                  {bundle.title}
                </h1>
              </div>
            </section>

            <nav className="mt-4 flex gap-2" aria-label="Sections">
              {(
                [
                  ['mission', 'Jouer'],
                  ['lecon', 'Apprendre'],
                ] as const
              ).map(([cle, libelle]) => (
                <button
                  key={cle}
                  type="button"
                  onClick={() => setOnglet(cle)}
                  className={
                    'tuile min-h-[46px] flex-1 rounded-full px-4 text-kid font-extrabold ' +
                    (onglet === cle
                      ? 'bg-ink text-white-warm'
                      : 'border-2 border-line bg-white-warm/70 text-ink-2')
                  }
                >
                  {libelle}
                </button>
              ))}
            </nav>

            <div className="mt-4">
              {onglet === 'mission' ? (
                parentId && childId ? (
                  <Etape
                    parentId={parentId}
                    childId={childId}
                    lessonId={bundle.id}
                    rang={rangDeLaClasse(child.data?.classes ?? null)}
                  />
                ) : (
                  <Loading />
                )
              ) : (
                <div className="grid gap-3">
                  <Fiches
                    film={
                      filmUrl && video
                        ? {
                            url: filmUrl,
                            poster: video.poster_url,
                            duree: video.duration_s,
                          }
                        : null
                    }
                    resume={bundle.summary}
                    illustration={bundle.illustration}
                    notions={notions}
                    langue={bundle.lang}
                    acquises={images.data ?? new Set()}
                    onJouer={() => setOnglet('mission')}
                  />
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </main>
  );
}
