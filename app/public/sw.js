/**
 * Le service worker.
 *
 * Il ne sert qu'à une chose : recevoir le rappel du soir et l'afficher, même
 * quand l'app est fermée. C'est le seul moyen, sur le web, d'aller chercher
 * un enfant qui ne pense pas à ouvrir une application de révision.
 *
 * Pas de cache ici. Une mise en cache mal faite sert de vieilles leçons sans
 * qu'on s'en aperçoive ; elle viendra avec le mode hors-ligne, pensé pour
 * elle-même.
 */

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));

self.addEventListener('push', (e) => {
  // Un push sans contenu lisible ne doit pas laisser une notification vide :
  // mieux vaut une phrase générique que « site web » affiché par le système.
  let message = { titre: 'Se Former Cameroun', texte: 'Niba t’attend !', url: '/' };
  try {
    if (e.data) message = { ...message, ...e.data.json() };
  } catch (err) {
    message.texte = e.data ? e.data.text() : message.texte;
  }

  e.waitUntil(
    self.registration.showNotification(message.titre, {
      body: message.texte,
      icon: '/icone-192.png',
      badge: '/icone-192.png',
      lang: 'fr',
      // Une étiquette par enfant : deux rappels du même soir se remplacent
      // au lieu de s'empiler.
      tag: message.tag || 'rappel',
      renotify: true,
      data: { url: message.url || '/' },
    }),
  );
});

self.addEventListener('notificationclick', (e) => {
  e.notification.close();
  const cible = (e.notification.data && e.notification.data.url) || '/';
  e.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((fenetres) => {
      // Si l'app est déjà ouverte, on l'amène au bon endroit plutôt que
      // d'ouvrir un deuxième onglet par-dessus.
      for (const f of fenetres) {
        if ('focus' in f) {
          f.navigate(cible).catch(() => {});
          return f.focus();
        }
      }
      return self.clients.openWindow(cible);
    }),
  );
});
