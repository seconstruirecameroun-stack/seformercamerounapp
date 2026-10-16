/**
 * lire-fiche-enfant — un bulletin photographié remplit la fiche.
 *
 * Un parent qui inscrit son enfant a presque toujours un papier sous la main :
 * un bulletin, une carte scolaire, un reçu de scolarité. Tout y est déjà —
 * le prénom tel que l'école l'écrit, la classe, l'établissement, souvent la
 * date de naissance. Le retaper au clavier d'un téléphone est une corvée, et
 * une corvée fait abandonner.
 *
 * Trois partis pris, les mêmes que pour la lecture des cours :
 *
 * 1. La fonction s'exécute avec le jeton du parent, jamais avec une clé
 *    d'administration. Elle ne peut donc lire que les fichiers de ce parent.
 *
 * 2. Le modèle n'a pas le droit d'ajouter du savoir. Il transcrit ce qui est
 *    écrit, et laisse vide ce qu'il ne lit pas. Une date de naissance devinée
 *    serait pire que pas de date du tout.
 *
 * 3. Rien n'est enregistré ici. La fonction répond, l'assistant pré-remplit,
 *    et c'est le parent qui valide. Un prénom mal lu doit pouvoir être
 *    corrigé avant d'exister.
 */

import Anthropic from 'npm:@anthropic-ai/sdk@0.74.0';
import { createClient } from 'npm:@supabase/supabase-js@2.49.4';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, apikey, x-client-info, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};

const CONSIGNE = `Tu lis la photo d'un document scolaire camerounais : bulletin,
carte scolaire, reçu de scolarité, fiche d'inscription ou emploi du temps.

Tu en extrais uniquement ce qui concerne L'ÉLÈVE, et uniquement ce qui est
écrit noir sur blanc. Tu réponds en JSON strict, sans aucun texte autour :

{
  "prenom": "le prénom usuel seul, sans le nom de famille, ou null",
  "naissance": "AAAA-MM-JJ, ou null",
  "genre": "fille | garcon | null",
  "ecole": "le nom de l'établissement, ou null",
  "classe": "le libellé exact de la classe tel qu'écrit, par exemple CM1, CE2, Class 5, ou null",
  "doutes": ["ce que tu as lu avec hésitation, en une phrase chacun"]
}

Règles absolues :
- Tu ne devines jamais. Un champ illisible ou absent vaut null.
- Tu ne complètes jamais de mémoire : si le document ne porte pas la date de
  naissance, elle reste null, même si tu pourrais l'estimer par la classe.
- Le genre ne se déduit pas du prénom. Il ne vient que d'une mention explicite
  (Sexe, M/F, Masculin/Féminin, fils/fille de).
- Un prénom composé reste entier. Tu ne traduis rien, tu ne corriges pas
  l'orthographe de l'école.`;

Deno.serve(async (requete) => {
  if (requete.method === 'OPTIONS') return new Response('ok', { headers: CORS });

  const cle = Deno.env.get('ANTHROPIC_API_KEY');
  if (!cle) {
    return new Response(
      JSON.stringify({ erreur: 'lecture non configurée', code: 'sans_cle' }),
      { status: 503, headers: { ...CORS, 'Content-Type': 'application/json' } },
    );
  }

  const autorisation = requete.headers.get('Authorization');
  if (!autorisation) {
    return new Response(JSON.stringify({ erreur: 'session requise' }), {
      status: 401,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });
  }

  const { chemin } = (await requete.json()) as { chemin?: string };
  if (!chemin) {
    return new Response(JSON.stringify({ erreur: 'chemin manquant' }), {
      status: 400,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });
  }

  // Le client porte le jeton du parent : la RLS du compartiment s'applique,
  // et il ne peut donc atteindre que ses propres fichiers.
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: autorisation } } },
  );

  const { data: fichier, error } = await supabase.storage.from('cours').download(chemin);
  if (error || !fichier) {
    return new Response(JSON.stringify({ erreur: 'document introuvable' }), {
      status: 404,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });
  }

  const octets = new Uint8Array(await fichier.arrayBuffer());
  let binaire = '';
  for (const o of octets) binaire += String.fromCharCode(o);
  const base64 = btoa(binaire);
  const type = fichier.type === 'image/png' ? 'image/png' : 'image/jpeg';

  const anthropic = new Anthropic({ apiKey: cle });
  const reponse = await anthropic.messages.create({
    model: 'claude-sonnet-5-5',
    max_tokens: 1000,
    messages: [
      {
        role: 'user',
        content: [
          { type: 'image', source: { type: 'base64', media_type: type, data: base64 } },
          { type: 'text', text: CONSIGNE },
        ],
      },
    ],
  });

  const texte = reponse.content
    .map((bloc) => (bloc.type === 'text' ? bloc.text : ''))
    .join('')
    .trim();

  // Le modèle entoure parfois son JSON d'une clôture de code : on prend ce
  // qui va de la première accolade à la dernière plutôt que d'échouer.
  const debut = texte.indexOf('{');
  const fin = texte.lastIndexOf('}');
  let fiche: unknown = null;
  try {
    fiche = JSON.parse(texte.slice(debut, fin + 1));
  } catch {
    return new Response(JSON.stringify({ erreur: 'lecture illisible', brut: texte.slice(0, 400) }), {
      status: 422,
      headers: { ...CORS, 'Content-Type': 'application/json' },
    });
  }

  return new Response(JSON.stringify({ fiche }), {
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
});
