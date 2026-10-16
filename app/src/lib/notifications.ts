import { supabase } from './supabase';

/**
 * Les rappels du soir.
 *
 * Toute la gamification de l'app suppose que l'enfant l'ouvre. Or un enfant
 * de sept ans ne pense pas à ouvrir une application de révision : c'est à
 * elle d'aller le chercher. Un rappel par jour, le soir, et jamais s'il a
 * déjà joué.
 *
 * Deux règles tenues ici :
 *
 * 1. L'abonnement appartient à un couple (appareil, enfant). Les deux frères
 *    partagent souvent le même téléphone ; chacun doit recevoir son message,
 *    avec son prénom.
 *
 * 2. On ne demande jamais la permission au chargement de la page. Un
 *    navigateur qui réclame l'autorisation avant qu'on ait rien vu se fait
 *    refuser, et le refus est définitif — il faut alors passer par les
 *    réglages du système pour revenir en arrière. La demande part d'un geste
 *    du parent, dans son espace, une fois qu'il sait ce qu'il accepte.
 */

const CLE_PUBLIQUE = import.meta.env.VITE_VAPID_PUBLIC_KEY as string | undefined;

export type EtatRappel = 'impossible' | 'non-configure' | 'refuse' | 'inactif' | 'actif';

/** Le navigateur sait-il recevoir un push ? */
export function supporte(): boolean {
  return (
    typeof window !== 'undefined' &&
    'serviceWorker' in navigator &&
    'PushManager' in window &&
    'Notification' in window
  );
}

export function etatGeneral(): EtatRappel {
  if (!supporte()) return 'impossible';
  if (!CLE_PUBLIQUE) return 'non-configure';
  if (Notification.permission === 'denied') return 'refuse';
  return 'inactif';
}

/** La clé VAPID voyage en base64url ; l'API, elle, veut des octets. */
function enOctets(base64url: string): Uint8Array {
  const base64 = (base64url + '='.repeat((4 - (base64url.length % 4)) % 4))
    .replace(/-/g, '+')
    .replace(/_/g, '/');
  const brut = atob(base64);
  return Uint8Array.from(brut, (c) => c.charCodeAt(0));
}

function enBase64(buffer: ArrayBuffer | null): string {
  if (!buffer) return '';
  const octets = new Uint8Array(buffer);
  let brut = '';
  for (const o of octets) brut += String.fromCharCode(o);
  return btoa(brut).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export async function enregistrerServiceWorker(): Promise<ServiceWorkerRegistration | null> {
  if (!supporte()) return null;
  return navigator.serviceWorker.register('/sw.js');
}

/**
 * Active les rappels pour un enfant sur cet appareil.
 *
 * Renvoie l'état atteint : le refus n'est pas une erreur, c'est une réponse.
 */
export async function activer(parentId: string, childId: string): Promise<EtatRappel> {
  if (!supporte()) return 'impossible';
  if (!CLE_PUBLIQUE) return 'non-configure';

  const permission = await Notification.requestPermission();
  if (permission !== 'granted') return permission === 'denied' ? 'refuse' : 'inactif';

  const inscription = (await enregistrerServiceWorker()) ?? (await navigator.serviceWorker.ready);
  await navigator.serviceWorker.ready;

  // Un abonnement déjà pris est réutilisé : en redemander un produirait une
  // seconde adresse, et l'enfant recevrait le rappel en double.
  const abonnement =
    (await inscription.pushManager.getSubscription()) ??
    (await inscription.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: enOctets(CLE_PUBLIQUE) as BufferSource,
    }));

  const { error } = await supabase.from('push_subscriptions').upsert(
    {
      parent_id: parentId,
      child_id: childId,
      endpoint: abonnement.endpoint,
      p256dh: enBase64(abonnement.getKey('p256dh')),
      auth: enBase64(abonnement.getKey('auth')),
      appareil: navigator.userAgent.slice(0, 200),
      echecs: 0,
    },
    { onConflict: 'endpoint,child_id' },
  );
  if (error) throw error;

  return 'actif';
}

/**
 * Coupe les rappels d'un enfant sur cet appareil.
 *
 * L'abonnement du navigateur n'est annulé que si plus aucun enfant ne s'en
 * sert : sur le téléphone du père, couper ceux de KLEIN ne doit pas couper
 * ceux de BRAYNE.
 */
export async function desactiver(childId: string): Promise<EtatRappel> {
  if (!supporte()) return 'impossible';
  const inscription = await navigator.serviceWorker.getRegistration();
  const abonnement = await inscription?.pushManager.getSubscription();
  if (!abonnement) return 'inactif';

  const { error } = await supabase
    .from('push_subscriptions')
    .delete()
    .eq('child_id', childId)
    .eq('endpoint', abonnement.endpoint);
  if (error) throw error;

  const { count } = await supabase
    .from('push_subscriptions')
    .select('id', { count: 'exact', head: true })
    .eq('endpoint', abonnement.endpoint);
  if ((count ?? 0) === 0) await abonnement.unsubscribe();

  return 'inactif';
}

/** Les enfants déjà abonnés sur cet appareil. */
export async function abonnesIci(): Promise<Set<string>> {
  if (!supporte()) return new Set();
  const inscription = await navigator.serviceWorker.getRegistration();
  const abonnement = await inscription?.pushManager.getSubscription();
  if (!abonnement) return new Set();

  const { data } = await supabase
    .from('push_subscriptions')
    .select('child_id')
    .eq('endpoint', abonnement.endpoint);
  return new Set((data ?? []).map((r) => r.child_id as string));
}

/**
 * Un rappel d'essai, affiché tout de suite sur cet appareil.
 *
 * Il ne passe pas par le serveur de push : il sert au parent à voir à quoi
 * ressemble le message, et à vérifier que son téléphone laisse bien passer
 * les notifications de l'app.
 */
export async function essai(prenom: string): Promise<boolean> {
  if (!supporte() || Notification.permission !== 'granted') return false;
  const inscription = (await navigator.serviceWorker.getRegistration()) ?? null;
  if (!inscription) return false;
  await inscription.showNotification(`${prenom}, Niba t’attend !`, {
    body: 'Une leçon de cinq minutes, et tu gardes ta série.',
    icon: '/icone-192.png',
    badge: '/icone-192.png',
    lang: 'fr',
    tag: 'essai',
    data: { url: '/' },
  });
  return true;
}
