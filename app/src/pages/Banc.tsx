import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import ItemPlayer from '../components/items/ItemPlayer';
import PlateauDEssai from '../components/jeu/PlateauDEssai';
import CopieDEssai from '../components/epreuve/CopieDEssai';
import { supabase } from '../lib/supabase';
import type { ItemRow } from '../types/db';

/**
 * Banc d'essai — page locale, jamais poussée en ligne.
 *
 * Elle sert à éprouver une question sans la gagner : rien de ce qui se passe
 * ici n'est enregistré. Aucun appel à recordAttempt, aucune écriture, aucun
 * point. Les journaux de BRAYNE et de KLEIN ne bougent pas.
 *
 * Les questions « poser les éléments » sont lues en base telles qu'elles
 * seront servies ; les deux autres sont écrites ici pour isoler ce qu'il y a
 * à regarder — le clavier, et l'ordre des réponses.
 */

const fabriquer = (kind: string, level: number, payload: unknown, answer: unknown): ItemRow =>
  ({
    id: 'banc-' + kind + level, notion_id: 'banc', parent_id: 'banc', status: 'approved',
    kind, level, payload, answer, explain: null, created_at: '',
  }) as unknown as ItemRow;

const CLAVIER = fabriquer(
  'texte_a_trous', 4,
  { text: 'Le fleuve {{1}} vers la mer, puis l’eau {{2}}.', blanks: 2 },
  { values: ['s’élargit', 'déborde'] },
);

const CLAVIER_DOUX = fabriquer(
  'texte_a_trous', 2,
  { text: 'À l’étape 2, l’accent est pardonné : écris {{1}}.', blanks: 1 },
  { values: ['élève'] },
);

const MELANGE = fabriquer(
  'qcm', 1,
  { question: 'Quelle est la capitale du Cameroun ?',
    options: ['Yaoundé', 'Douala', 'Bafoussam', 'Garoua'] },
  { index: 0 },
);

const ORDRE = fabriquer(
  'chronologie', 2,
  { question: 'Remets la phrase dans le bon ordre.',
    tokens: ['Le', 'fleuve', 'rejoint', 'la', 'mer'] },
  { order: [0, 1, 2, 3, 4] },
);

/**
 * Deux associations de tailles différentes, à jouer l'une après l'autre.
 *
 * C'est le couple exact de la leçon des cultures vivrières : une question à
 * deux paires, puis une à trois. Sans clé de remontage, la seconde hérite du
 * mélange de la première et n'affiche que deux étiquettes à droite pour
 * trois à gauche — et le lecteur conclut après deux liens, sur une question
 * que l'enfant n'a pas finie.
 */
const ASSO_2 = fabriquer(
  'association', 2,
  { question: 'Relie chaque mot à ce qu’il veut dire.',
    gauche: ['Culture vivrière', 'Population locale'],
    droite: ['Elle nourrit les gens du pays', 'Les gens qui vivent ici'] },
  { order: [0, 1] },
);

const ASSO_3 = fabriquer(
  'association', 2,
  { question: 'Relie chaque culture à sa région.',
    gauche: ['Le manioc', 'Les ignames', 'Le sorgho'],
    droite: ['Le Centre, le Sud et le Littoral', 'L’Ouest', 'Le Nord'] },
  { order: [0, 1, 2] },
);

/**
 * Les trois schémas à annoter, lus en base.
 *
 * Ils se regardent ici parce que c'est le seul type dont le DESSIN est
 * l'exercice : une vignette ne suffit pas à juger, il faut voir si les
 * numéros se lisent et si les noms tiennent à côté.
 */
const ONGLETS = [
  { cle: 'probleme', titre: 'Les problemes',
    note: 'Les enonces rediges, lus en base. Une situation, puis le resultat a ecrire.' },
  { cle: 'suite', titre: 'Deux questions de suite',
    note: 'Deux paires, puis trois. Décoche la clé pour revoir le défaut.' },
  { cle: 'diagramme', titre: 'Poser les éléments', note: 'Les 3 questions lues en base.' },
  { cle: 'annotation', titre: 'Annoter un schéma',
    note: 'Les schémas lus en base : les numéros doivent se lire, et chaque nom trouver sa place.' },
  { cle: 'bonbons', titre: 'Plateau de bonbons',
    note: 'Le plateau de la salle de composition, libre : ici chaque coup est gratuit. Dans une composition, il faut une bonne réponse pour en gagner un.' },
  { cle: 'copie', titre: 'Copie de composition',
    note: 'L’en-tête, la situation problème et le bulletin d’une épreuve sur 30, avec des points inventés.' },
  { cle: 'clavier', titre: 'Clavier · Défi', note: 'Étape 4 : l’accent et l’apostrophe comptent. Réponses : s’élargit · déborde.' },
  { cle: 'clavier2', titre: 'Clavier · étape 2', note: 'Même clavier, mais « eleve » est accepté ici.' },
  { cle: 'melange', titre: 'Ordre des choix', note: 'Rejoue : la bonne réponse change de place.' },
  { cle: 'ordre', titre: 'Étiquettes', note: 'Elles ne sortent plus déjà rangées.' },
];

export default function Banc() {
  const [onglet, setOnglet] = useState('probleme');
  const [avecCle, setAvecCle] = useState(true);
  const [n, setN] = useState(0);
  const [etat, setEtat] = useState<{ correct: boolean } | null>(null);

  // Les problemes : on lit les textes a trous les plus longs, ceux qui
  // portent une situation et non une operation posee.
  const problemes = useQuery({
    queryKey: ['banc-probleme'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('items').select('*').eq('kind', 'texte_a_trous').order('level');
      if (error) throw error;
      return (data as ItemRow[]).filter(
        (i) => String((i.payload as { text?: string }).text ?? '').length >= 180,
      );
    },
  });

  const schemas = useQuery({
    queryKey: ['banc-annotation'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('items').select('*').eq('kind', 'annotation').order('level');
      if (error) throw error;
      return data as ItemRow[];
    },
  });

  const live = useQuery({
    queryKey: ['banc-diagramme'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('items').select('*').eq('kind', 'diagramme').order('level');
      if (error) throw error;
      return data as ItemRow[];
    },
  });

  const rejouer = () => { setN((x) => x + 1); setEtat(null); };
  const actif = ONGLETS.find((o) => o.cle === onglet)!;

  if (onglet === 'bonbons' || onglet === 'copie') {
    return (
      <main className="mx-auto max-w-md p-4 pb-24">
        <p className="rounded-xl bg-sand/70 px-3 py-2 text-kid-xs font-bold text-ink">
          Banc d’essai — rien n’est enregistré ici. Les journaux des enfants ne bougent pas.
        </p>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {ONGLETS.map((o) => (
            <button
              key={o.cle}
              type="button"
              onClick={() => { setOnglet(o.cle); setN(0); setEtat(null); }}
              className={
                'rounded-full border-2 px-3 py-1 text-kid-xs font-black ' +
                (o.cle === onglet
                  ? 'border-ink bg-ink text-white-warm'
                  : 'border-line bg-white-warm text-ink')
              }
            >
              {o.titre}
            </button>
          ))}
        </div>
        <p className="mt-2 text-kid-xs text-muted">{actif.note}</p>
        {actif.cle === 'copie' ? <CopieDEssai /> : <PlateauDEssai />}
      </main>
    );
  }

  let item: ItemRow | null = null;
  if (onglet === 'probleme') {
    item = problemes.data?.[n % Math.max(1, problemes.data.length)] ?? null;
  } else if (onglet === 'suite') item = n % 2 === 0 ? ASSO_2 : ASSO_3;
  else if (onglet === 'diagramme') item = live.data?.[n % Math.max(1, live.data.length)] ?? null;
  else if (onglet === 'annotation')
    item = schemas.data?.[n % Math.max(1, schemas.data.length)] ?? null;
  else if (onglet === 'clavier') item = CLAVIER;
  else if (onglet === 'clavier2') item = CLAVIER_DOUX;
  else if (onglet === 'melange') item = MELANGE;
  else item = ORDRE;

  return (
    <main className="mx-auto max-w-md p-4 pb-24">
      <p className="rounded-xl bg-sand/70 px-3 py-2 text-kid-xs font-bold text-ink">
        Banc d’essai — rien n’est enregistré ici. Les journaux des enfants ne bougent pas.
      </p>

      <div className="mt-3 flex flex-wrap gap-1.5">
        {ONGLETS.map((o) => (
          <button
            key={o.cle}
            type="button"
            onClick={() => { setOnglet(o.cle); setN(0); setEtat(null); }}
            className={
              'rounded-full border-2 px-3 py-1 text-kid-xs font-black ' +
              (o.cle === onglet
                ? 'border-ink bg-ink text-white-warm'
                : 'border-line bg-white-warm text-ink')
            }
          >
            {o.titre}
          </button>
        ))}
      </div>

      <p className="mt-2 text-kid-xs text-muted">{actif.note}</p>

      <div className="mt-2 flex items-center gap-3">
        <button
          type="button"
          onClick={rejouer}
          className="rounded-full border-2 border-clay px-3 py-1 text-kid-xs font-black text-clay-dark"
        >
          {onglet === 'diagramme' || onglet === 'annotation' || onglet === 'suite' ||
          onglet === 'probleme'
            ? 'Question suivante'
            : 'Rejouer'}
        </button>
        {onglet === 'suite' ? (
          <label className="flex items-center gap-1.5 text-kid-xs font-bold text-ink">
            <input
              type="checkbox"
              checked={avecCle}
              onChange={(e) => setAvecCle(e.target.checked)}
            />
            clé de remontage
          </label>
        ) : null}
        {etat ? (
          <span
            className={
              'text-kid-sm font-black ' + (etat.correct ? 'text-leaf' : 'text-clay-dark')
            }
          >
            {etat.correct ? '✓ juste' : '✗ faux'}
          </span>
        ) : null}
      </div>

      <div className="mt-4 rounded-[var(--radius-card)] border-2 border-line bg-white-warm p-4">
        {item ? (
          <ItemPlayer
            key={avecCle ? onglet + n + item.id : 'sans-cle'}
            item={item}
            verrouille={etat !== null}
            rang={5}
            onRepondre={(r) => setEtat({ correct: r.correct })}
          />
        ) : (
          <p className="text-kid-sm text-muted">Chargement…</p>
        )}
      </div>
    </main>
  );
}
