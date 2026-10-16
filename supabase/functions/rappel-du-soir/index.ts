/**
 * rappel-du-soir — le message qui ramène l'enfant.
 *
 * Appelée chaque soir par pg_cron, qui a déjà choisi les destinataires : les
 * enfants qui n'ont pas joué aujourd'hui. Cette fonction ne fait que deux
 * choses — trouver la bonne phrase, puis signer et chiffrer l'envoi.
 *
 * Trois partis pris :
 *
 * 1. Aucune clé d'administration. La fonction ne lit pas la base : tout ce
 *    dont elle a besoin arrive dans le corps de la requête. Elle ne détient
 *    que la clé privée VAPID, qui ne sert qu'à signer des notifications.
 *
 * 2. Une phrase par situation, jamais de reproche. « Tu n'as pas travaillé »
 *    ne fait revenir personne ; « ta série t'attend » donne une raison, et
 *    une chose à faire ce soir.
 *
 * 3. Rien n'est promis que l'app ne tienne. Chaque message renvoie à quelque
 *    chose que l'enfant trouvera en ouvrant : sa série, son duel, sa
 *    première image.
 */

import webpush from 'npm:web-push@3.6.7';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  // supabase-js ajoute authorization, apikey et x-client-info : omis de
  // cette liste, le navigateur refuse l'appel avant même de l'envoyer.
  'Access-Control-Allow-Headers':
    'authorization, apikey, x-client-info, content-type, x-rappel-secret',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

type Rappel = {
  endpoint: string;
  p256dh: string;
  auth: string;
  childId: string;
  prenom: string;
  /** Dernier jour joué, au format AAAA-MM-JJ, ou null s'il n'a jamais joué. */
  dernierJour: string | null;
  reussitesSemaine: number;
  meilleurRival: number;
  prenomRival: string | null;
};

/** La journée d'un enfant se compte au Cameroun, pas à Greenwich. */
function jourLocal(decalage = 0): string {
  const d = new Date(Date.now() - decalage * 86_400_000);
  return new Intl.DateTimeFormat('fr-CA', { timeZone: 'Africa/Douala' }).format(d);
}

/** Le jour de la semaine au Cameroun : 1 pour lundi, 7 pour dimanche. */
function jourSemaineLocal(): number {
  const court = new Intl.DateTimeFormat('en-US', {
    timeZone: 'Africa/Douala',
    weekday: 'short',
  }).format(new Date());
  return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].indexOf(court) + 1;
}

/** Jours d'absence, à partir de la dernière journée jouée. */
function absence(dernierJour: string | null): number {
  if (!dernierJour) return Infinity;
  const hier = new Date(jourLocal(0) + 'T00:00:00Z').getTime();
  const alors = new Date(dernierJour + 'T00:00:00Z').getTime();
  return Math.round((hier - alors) / 86_400_000);
}

export function message(r: Rappel, jourSemaine: number): { titre: string; texte: string } {
  const jours = absence(r.dernierJour);
  const retard = r.meilleurRival - r.reussitesSemaine;

  // Vendredi et samedi, le duel prime : c'est le moment où il se joue encore
  // et où il se perd. Le reste de la semaine, une avance de l'aîné
  // n'inquiète personne.
  if (r.prenomRival && retard > 0 && (jourSemaine === 5 || jourSemaine === 6)) {
    return {
      // « de 1 question » ne se dit pas : un enfant qui lit ses
      // notifications apprend aussi sa langue dedans.
      titre:
        retard > 1
          ? `${r.prenomRival} te mène de ${retard} questions`
          : `${r.prenomRival} te mène d’une question`,
      texte: 'La semaine se termine dimanche soir. Tu peux encore le rattraper !',
    };
  }

  // Une série vivante est ce qu'on perd le plus vite, et ce qu'on protège le
  // plus volontiers : elle passe avant tout le reste.
  if (jours === 1) {
    return {
      titre: `${r.prenom}, ta série t’attend !`,
      texte: 'Une leçon avant ce soir, et elle tient.',
    };
  }

  if (jours === Infinity) {
    return {
      titre: `${r.prenom}, on commence ?`,
      texte: 'Cinq minutes, et tu gagnes ta première image.',
    };
  }

  if (jours >= 3) {
    return {
      titre: `Tu m’as manqué, ${r.prenom} !`,
      texte: 'Niba t’attend pour une leçon.',
    };
  }

  return {
    titre: `${r.prenom}, on joue ?`,
    texte: 'Une leçon de cinq minutes, et une image de plus.',
  };
}

Deno.serve(async (requete) => {
  if (requete.method === 'OPTIONS') return new Response('ok', { headers: CORS });

  const secret = Deno.env.get('RAPPEL_SECRET');
  const prive = Deno.env.get('VAPID_PRIVATE_KEY');
  const publique = Deno.env.get('VAPID_PUBLIC_KEY');
  const contact = Deno.env.get('VAPID_CONTACT') ?? 'mailto:seconstruirecameroun@gmail.com';

  if (!secret || !prive || !publique) {
    return new Response(JSON.stringify({ erreur: 'fonction non configurée' }), {
      status: 500,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });
  }
  // Le secret partagé : sans lui, n'importe qui connaissant l'adresse
  // pourrait faire sonner le téléphone des enfants.
  if (requete.headers.get('x-rappel-secret') !== secret) {
    return new Response('non autorisé', { status: 401, headers: CORS });
  }

  webpush.setVapidDetails(contact, publique, prive);

  const { rappels } = (await requete.json()) as { rappels: Rappel[] };
  const jourSemaine = jourSemaineLocal();

  let envoyes = 0;
  const morts: string[] = [];

  for (const r of rappels ?? []) {
    const { titre, texte } = message(r, jourSemaine);
    try {
      await webpush.sendNotification(
        { endpoint: r.endpoint, keys: { p256dh: r.p256dh, auth: r.auth } },
        JSON.stringify({
          titre,
          texte,
          url: `/enfant/${r.childId}`,
          // Une étiquette par enfant : deux rappels du même soir se
          // remplacent au lieu de s'empiler.
          tag: `rappel-${r.childId}`,
        }),
        { TTL: 10 * 3600 },
      );
      envoyes += 1;
    } catch (err) {
      // 404 et 410 : le navigateur a désinstallé l'app ou vidé ses données.
      const code = (err as { statusCode?: number }).statusCode;
      if (code === 404 || code === 410) morts.push(r.endpoint);
    }
  }

  return new Response(JSON.stringify({ envoyes, morts }), {
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
});
