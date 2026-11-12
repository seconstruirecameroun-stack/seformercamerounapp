/**
 * Lire tout le journal, même quand le serveur tronque.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/toutLire.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/toutLire.verif.mjs
 *   node ../work/toutLire.verif.mjs
 */

import { toutLire } from './toutLire';

let echecs = 0;
function verifie(nom: string, condition: boolean) {
  if (condition) console.log('  ok     ' + nom);
  else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

/** Un serveur qui ne rend jamais plus de `plafond` lignes, comme Supabase. */
function serveur(lignes: number, plafond: number) {
  const table = Array.from({ length: lignes }, (_, i) => ({ id: i }));
  let appels = 0;
  const page = (de: number, a: number) => {
    appels += 1;
    const fin = Math.min(a + 1, de + plafond, table.length);
    return Promise.resolve({ data: table.slice(de, fin), error: null });
  };
  return { page, appels: () => appels };
}

async function lancer() {
  const s1 = serveur(2731, 1000);
  const t1 = await toutLire<{ id: number }>(s1.page);
  verifie('2 731 réponses, plafond 1 000 : tout est lu', t1.length === 2731);
  verifie('aucune réponse en double ni sautée', t1.every((x, i) => x.id === i));

  const s2 = serveur(2731, 300);
  const t2 = await toutLire<{ id: number }>(s2.page);
  verifie('serveur plus avare (300) : rien n’est sauté', t2.length === 2731 && t2.every((x, i) => x.id === i));

  const s3 = serveur(0, 1000);
  verifie('journal vide : liste vide', (await toutLire(s3.page)).length === 0);

  const s4 = serveur(1000, 1000);
  const t4 = await toutLire(s4.page);
  verifie('pile mille : mille, et une page vide pour s’en assurer', t4.length === 1000 && s4.appels() === 2);

  let leve = false;
  try {
    await toutLire(() => Promise.resolve({ data: null, error: new Error('refusé') }));
  } catch {
    leve = true;
  }
  verifie('une erreur du serveur remonte', leve);

  console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
}

void lancer();
