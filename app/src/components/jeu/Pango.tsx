/**
 * Pango, le pangolin de KLEIN.
 *
 * Un animal des forêts du Cameroun, qui en vrai se roule en boule pour se
 * protéger — c'est ce qu'il fait ici quand il fonce. Il est tracé, pas
 * dessiné à la main dans un fichier : il tient en quelques formes, pèse
 * quelques centaines d'octets, et change d'humeur par une seule propriété.
 *
 * Son allure est à lui : écailles cuivrées, museau crème, joues roses. Ce
 * n'est le personnage d'aucun autre jeu.
 */

export type Humeur = 'joie' | 'surpris' | 'fier' | 'boule';

const ECAILLE = '#c9793a';
const ECAILLE_FONCEE = '#8f4f1f';
const ECAILLE_CLAIRE = '#e7a564';
const CREME = '#f3d6aa';
const ENCRE = '#3b2615';

/** Une rangée d'écailles : de petits arcs qui se chevauchent. */
function Ecailles({ y, de, a, pas }: { y: number; de: number; a: number; pas: number }) {
  const arcs = [];
  for (let x = de; x <= a; x += pas) {
    arcs.push(
      <path
        key={x}
        d={`M${x - pas / 2} ${y} q${pas / 2} ${-pas * 0.9} ${pas} 0`}
        fill={ECAILLE_CLAIRE}
        stroke={ECAILLE_FONCEE}
        strokeWidth={2}
        strokeLinejoin="round"
      />,
    );
  }
  return <>{arcs}</>;
}

function Boule() {
  return (
    <g>
      <circle cx={60} cy={62} r={40} fill={ECAILLE} stroke={ECAILLE_FONCEE} strokeWidth={3} />
      {/* La spirale d'écailles qui dit qu'il tourne. */}
      {[34, 26, 18, 10].map((r, i) => (
        <circle
          key={r}
          cx={60 + i * 2}
          cy={62 - i}
          r={r}
          fill="none"
          stroke={i % 2 ? ECAILLE_CLAIRE : ECAILLE_FONCEE}
          strokeWidth={4}
          strokeDasharray="10 7"
        />
      ))}
      <ellipse cx={46} cy={44} rx={12} ry={7} fill="#fff" opacity={0.35} />
    </g>
  );
}

export default function Pango({ humeur = 'joie', className }: { humeur?: Humeur; className?: string }) {
  return (
    <svg viewBox="0 0 120 120" className={className} aria-hidden>
      {humeur === 'boule' ? (
        <Boule />
      ) : (
        <g>
          {/* La queue, longue et écailleuse, qui s'enroule derrière. */}
          <path
            d="M30 82 C10 86 4 70 12 60 C16 55 22 58 20 64"
            fill="none"
            stroke={ECAILLE}
            strokeWidth={14}
            strokeLinecap="round"
          />
          <path
            d="M30 82 C10 86 4 70 12 60"
            fill="none"
            stroke={ECAILLE_FONCEE}
            strokeWidth={2}
            strokeDasharray="5 5"
          />
          {/* Les pattes. */}
          <ellipse cx={44} cy={100} rx={9} ry={6} fill={ECAILLE_FONCEE} />
          <ellipse cx={74} cy={100} rx={9} ry={6} fill={ECAILLE_FONCEE} />
          {/* Le corps, couvert d'écailles. */}
          <ellipse cx={58} cy={74} rx={36} ry={27} fill={ECAILLE} stroke={ECAILLE_FONCEE} strokeWidth={3} />
          <Ecailles y={62} de={36} a={80} pas={11} />
          <Ecailles y={74} de={30} a={86} pas={11} />
          <Ecailles y={86} de={38} a={78} pas={11} />
          {/* La tête et le museau. */}
          <ellipse cx={90} cy={58} rx={19} ry={16} fill={CREME} stroke={ECAILLE_FONCEE} strokeWidth={2.5} />
          <ellipse cx={107} cy={63} rx={10} ry={6.5} fill={CREME} stroke={ECAILLE_FONCEE} strokeWidth={2.5} />
          <circle cx={115} cy={62} r={3} fill={ENCRE} />
          <path d="M80 44 q4 -8 9 -2" fill={CREME} stroke={ECAILLE_FONCEE} strokeWidth={2.5} />
          {/* Les joues. */}
          <circle cx={96} cy={66} r={4.5} fill="#f29c86" opacity={0.75} />
          {/* L'œil et la bouche, selon l'humeur. */}
          {humeur === 'joie' ? (
            <>
              <path d="M86 54 q5 -7 10 0" fill="none" stroke={ENCRE} strokeWidth={3.5} strokeLinecap="round" />
              <path d="M98 69 q6 7 12 -1" fill="#8a2d2d" stroke={ENCRE} strokeWidth={2} />
            </>
          ) : humeur === 'surpris' ? (
            <>
              <circle cx={91} cy={53} r={6.5} fill="#fff" stroke={ENCRE} strokeWidth={2} />
              <circle cx={92} cy={54} r={3.5} fill={ENCRE} />
              <circle cx={93} cy={52} r={1.3} fill="#fff" />
              <ellipse cx={103} cy={71} rx={3.5} ry={4.5} fill="#8a2d2d" stroke={ENCRE} strokeWidth={2} />
            </>
          ) : (
            <>
              {/* Fier : un clin d'œil et un grand sourire. */}
              <path d="M86 54 h10" stroke={ENCRE} strokeWidth={3.5} strokeLinecap="round" />
              <path d="M97 68 q7 6 13 -2" fill="none" stroke={ENCRE} strokeWidth={3} strokeLinecap="round" />
            </>
          )}
          {/* Le bras levé : il salue, il célèbre. */}
          {humeur !== 'surpris' ? (
            <path
              d="M70 64 q10 -18 18 -24"
              fill="none"
              stroke={ECAILLE_FONCEE}
              strokeWidth={7}
              strokeLinecap="round"
            />
          ) : (
            <path
              d="M70 66 q8 4 14 -2"
              fill="none"
              stroke={ECAILLE_FONCEE}
              strokeWidth={7}
              strokeLinecap="round"
            />
          )}
        </g>
      )}
    </svg>
  );
}
