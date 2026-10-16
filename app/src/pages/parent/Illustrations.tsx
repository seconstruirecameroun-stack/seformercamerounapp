import { useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { supabase } from '../../lib/supabase';
import { preparerIllustration } from '../../lib/image';
import type { FormeImage } from '../../lib/image';
import { Card, ErrorNote, Loading, Pill, Vide } from '../../components/ui';
import { sourceIllustration } from '../../components/Illustration';

/**
 * Les illustrations des cours importés.
 *
 * L'extraction écrit une consigne d'image par leçon et par notion. Le parent
 * la copie dans son générateur, regarde ce qui sort, et dépose l'image s'il
 * la juge bonne.
 *
 * Cette boucle passe par un humain à dessein : une illustration hors sujet ou
 * malheureuse atteindrait l'enfant sans que personne ne l'ait vue. C'est la
 * même règle que pour le texte généré.
 */

const BUCKET = 'illustrations';

type NotionIllu = {
  id: string;
  statement: string;
  sort_order: number;
  illustration: string | null;
  illustration_prompt: string | null;
};

type LeconIllu = {
  id: string;
  title: string;
  status: string;
  illustration: string | null;
  illustration_prompt: string | null;
  notions: NotionIllu[];
};

function Consigne({ texte }: { texte: string }) {
  const [copie, setCopie] = useState(false);
  return (
    <div className="mt-2 rounded-2xl bg-paper px-3 py-2">
      <p className="text-sm leading-relaxed break-words text-muted">{texte}</p>
      <button
        type="button"
        className="mt-1 text-sm font-bold text-clay underline"
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(texte);
            setCopie(true);
            setTimeout(() => setCopie(false), 2000);
          } catch {
            setCopie(false);
          }
        }}
      >
        {copie ? 'Consigne copiée' : 'Copier la consigne'}
      </button>
    </div>
  );
}

function Depot({
  cible,
  forme,
  lessonId,
  actuelle,
}: {
  cible: { table: 'lessons' | 'notions'; id: string };
  forme: FormeImage;
  lessonId: string;
  actuelle: string | null;
}) {
  const qc = useQueryClient();
  const input = useRef<HTMLInputElement>(null);

  const envoi = useMutation({
    mutationFn: async (fichier: File) => {
      const { data: auth } = await supabase.auth.getUser();
      const parentId = auth.user?.id;
      if (!parentId) throw new Error('Session expirée, reconnectez-vous.');

      const blob = await preparerIllustration(fichier, forme);
      const nom = cible.table === 'lessons' ? 'scene' : cible.id;
      const chemin = `${parentId}/${lessonId}/${nom}.webp`;

      const { error: errDepot } = await supabase.storage
        .from(BUCKET)
        .upload(chemin, blob, { contentType: blob.type, upsert: true });
      if (errDepot) throw errDepot;

      const { data } = supabase.storage.from(BUCKET).getPublicUrl(chemin);
      // L'horodatage force le navigateur et le cache à reprendre l'image
      // quand le parent en dépose une meilleure au même endroit.
      const url = `${data.publicUrl}?v=${Date.now()}`;

      const { error } = await supabase.from(cible.table).update({ illustration: url }).eq('id', cible.id);
      if (error) throw error;
      return { poids: blob.size };
    },
    onSuccess: () => {
      if (input.current) input.current.value = '';
      qc.invalidateQueries({ queryKey: ['illustrations'] });
      qc.invalidateQueries({ queryKey: ['lesson-bundle'] });
    },
  });

  // L'illustration est tantôt une adresse complète — celles déposées ici —
  // tantôt une clé courte livrée avec l'app. Posée telle quelle dans un
  // `src`, la clé donnait une image cassée : c'est la même traduction que
  // partout ailleurs qu'il faut appliquer.
  const apercu = sourceIllustration(actuelle);

  return (
    <div className="mt-3 flex flex-wrap items-center gap-3">
      {apercu ? (
        <img
          src={apercu}
          alt="L’illustration actuelle"
          className={
            'rounded-xl border-2 border-line object-cover ' +
            (forme === 'scene' ? 'h-16 w-28' : 'h-16 w-16')
          }
        />
      ) : (
        <span
          aria-hidden="true"
          className={
            'grid place-items-center rounded-xl border-2 border-dashed border-line text-sm text-muted ' +
            (forme === 'scene' ? 'h-16 w-28' : 'h-16 w-16')
          }
        >
          vide
        </span>
      )}

      {/* Le sélecteur natif affiche « Aucun fichier choisi » dans la langue
          du navigateur et ne ressemble à rien d'autre dans l'app : on le
          cache derrière un bouton rond, qui dit ce qu'il fait. */}
      <label className="tuile inline-flex cursor-pointer items-center gap-2 rounded-full border-2 border-line bg-white-warm px-5 py-2.5 text-base font-bold">
        {apercu ? 'Remplacer l’image' : 'Déposer une image'}
        <input
          ref={input}
          type="file"
          accept="image/*"
          className="sr-only"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) envoi.mutate(f);
          }}
        />
      </label>

      {envoi.isPending ? <span className="text-sm text-muted">Préparation…</span> : null}
      {envoi.isSuccess ? (
        <span className="text-sm text-leaf">
          Déposée · {(envoi.data.poids / 1024).toFixed(0)} ko
        </span>
      ) : null}
      {envoi.error ? <ErrorNote error={envoi.error} /> : null}
    </div>
  );
}

export default function Illustrations() {
  const lecons = useQuery({
    queryKey: ['illustrations'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('lessons')
        .select(
          'id, title, status, illustration, illustration_prompt, ' +
            'notions(id, statement, sort_order, illustration, illustration_prompt)',
        )
        .order('created_at', { ascending: false });
      if (error) throw error;
      return data as unknown as LeconIllu[];
    },
  });

  if (lecons.isLoading) return <Loading />;
  if (lecons.error) return <ErrorNote error={lecons.error} />;

  // Seules les leçons issues d'un import portent des consignes : la leçon de
  // démonstration est déjà illustrée par les images livrées avec l'app.
  const aIllustrer = (lecons.data ?? []).filter(
    (l) => l.illustration_prompt || l.notions.some((n) => n.illustration_prompt),
  );

  if (aIllustrer.length === 0) {
    return (
      <Card titre="Illustrations" sous="Les consignes d’image, à produire puis à déposer.">
        <Vide
          titre="Rien à illustrer pour l’instant"
          texte="Chaque cours importé puis lu reçoit une consigne d’image par leçon et par notion ; elles apparaîtront ici."
        />
      </Card>
    );
  }

  return (
    <section className="grid gap-4">
      <div className="rounded-[var(--radius-card)] border border-line bg-white-warm/85 px-5 py-4 sm:px-6">
        <h2 className="text-lg font-extrabold">Illustrations à produire</h2>
        <p className="mt-0.5 text-sm text-muted">
          Copiez la consigne dans votre générateur d’images, puis déposez le résultat. L’image est
          réduite et convertie avant l’envoi, pour rester légère chez l’enfant.
        </p>
      </div>

      {aIllustrer.map((lecon) => (
        <Card key={lecon.id}>
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h3 className="text-lg font-bold">{lecon.title}</h3>
            <Pill>{lecon.status === 'approved' ? 'publiée' : lecon.status}</Pill>
          </div>

          {lecon.illustration_prompt ? (
            <div className="mt-4 rounded-2xl border border-line p-3">
              <p className="text-sm font-bold text-muted">
                Scène d’ouverture · 16:9
              </p>
              <Consigne texte={lecon.illustration_prompt} />
              <Depot
                cible={{ table: 'lessons', id: lecon.id }}
                forme="scene"
                lessonId={lecon.id}
                actuelle={lecon.illustration}
              />
            </div>
          ) : null}

          <ul className="mt-3 grid gap-3">
            {[...lecon.notions]
              .sort((a, b) => a.sort_order - b.sort_order)
              .filter((n) => n.illustration_prompt)
              .map((notion) => (
                <li key={notion.id} className="rounded-2xl border border-line p-3">
                  <p className="text-sm font-semibold">{notion.statement}</p>
                  <Consigne texte={notion.illustration_prompt!} />
                  <Depot
                    cible={{ table: 'notions', id: notion.id }}
                    forme="objet"
                    lessonId={lecon.id}
                    actuelle={notion.illustration}
                  />
                </li>
              ))}
          </ul>
        </Card>
      ))}
    </section>
  );
}
