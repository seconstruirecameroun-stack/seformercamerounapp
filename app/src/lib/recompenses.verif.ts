/**
 * Ce que les récompenses doivent garantir.
 *
 * Usage :
 *   cd app
 *   node_modules/.bin/esbuild src/lib/recompenses.verif.ts --bundle \
 *     --platform=node --format=esm --outfile=../work/recompenses.verif.mjs
 *   node ../work/recompenses.verif.mjs
 */

import { mention } from './epreuve';
import {
  SEUILS,
  medailleDe,
  mentionAssuree,
  multiplicateur,
  palierAtteint,
  palmares,
  pointsPour,
  prochaineMedaille,
  prochaineMention,
  prochainPalier,
} from './recompenses';

let echecs = 0;
function verifie(nom: string, condition: boolean) {
  if (condition) console.log('  ok     ' + nom);
  else {
    echecs += 1;
    console.log('  ECHEC  ' + nom);
  }
}

// ── Les séries ──────────────────────────────────────────────────────────────
verifie('série : sans série, les points comptent une fois', multiplicateur(0) === 1 && multiplicateur(2) === 1);
verifie('série : trois de suite, double', multiplicateur(3) === 2 && multiplicateur(4) === 2);
verifie('série : cinq de suite, triple', multiplicateur(5) === 3);
verifie('série : dix de suite, quadruple', multiplicateur(12) === 4);
verifie('série : on annonce le prochain palier', prochainPalier(2)?.dans === 1 && prochainPalier(2)?.multiplicateur === 2);
verifie('série : à quatre, le triple est à une réponse', prochainPalier(4)?.dans === 1 && prochainPalier(4)?.multiplicateur === 3);
verifie('série : au-delà de dix, plus rien à annoncer', prochainPalier(10) === null);
verifie('série : 3, 5 et 10 sont des moments forts', palierAtteint(3) && palierAtteint(5) && palierAtteint(10) && !palierAtteint(4));

// ── La mention ──────────────────────────────────────────────────────────────
// Les seuils doivent dire la même chose que la lettre du bulletin, sur tous
// les barèmes et tous les scores.
let accord = true;
for (const total of [20, 24, 30, 34, 40]) {
  for (let p = 0; p <= total; p++) {
    for (const s of SEUILS) {
      const atteint = p >= pointsPour(s.lettre, total);
      const lettre = mention(p, total);
      const rang = ['D', 'C', 'B', 'A', 'A+'];
      if (atteint !== rang.indexOf(lettre) >= rang.indexOf(s.lettre)) accord = false;
    }
  }
}
verifie('mention : les seuils annoncés sont ceux du bulletin, sur tous les barèmes', accord);
verifie('mention : 27 sur 30, A+ assuré', mentionAssuree(27, 30) === 'A+');
verifie('mention : 15 sur 30, C assuré', mentionAssuree(15, 30) === 'C');
verifie('mention : 14 sur 30, rien d’assuré', mentionAssuree(14, 30) === null);
verifie('mention : 20 sur 30, il manque 3 points pour l’A', JSON.stringify(prochaineMention(20, 30, 10)) === JSON.stringify({ lettre: 'A', manque: 3 }));
verifie('mention : on n’annonce pas ce qui n’est plus possible', prochaineMention(5, 30, 4) === null);
verifie('mention : à l’A+, plus rien à annoncer', prochaineMention(28, 30, 2) === null);

// ── Les médailles ───────────────────────────────────────────────────────────
verifie('médaille : A+ vaut l’or', medailleDe(28, 30) === 'or');
verifie('médaille : A vaut l’argent', medailleDe(23, 30) === 'argent');
verifie('médaille : B vaut le bronze', medailleDe(18, 30) === 'bronze');
verifie('médaille : sous B, pas de médaille', medailleDe(15, 30) === null);
verifie('médaille : de l’argent, il manque 4 points pour l’or (sur 30)',
  JSON.stringify(prochaineMedaille(23, 30)) === JSON.stringify({ metal: 'or', manque: 4 }));
verifie('médaille : à l’or, plus rien à viser', prochaineMedaille(30, 30) === null);

const c = (id: string, points: number, total: number, jour: number) => ({
  id, titre: 'Copie ' + id, points, total, finie_le: `2026-11-${String(jour).padStart(2, '0')}`,
});
const p = palmares([c('a', 28, 30, 3), c('b', 23, 30, 1), c('c', 36, 40, 2), c('d', 12, 30, 4)]);
verifie('palmarès : on compte les métaux', p.compte.or === 2 && p.compte.argent === 1 && p.compte.bronze === 0);
verifie('palmarès : trois A de suite, dans l’ordre des dates', p.trophees.find((t) => t.cle === 'trois-a')?.gagne === true);
verifie('palmarès : pas encore de copie parfaite', p.trophees.find((t) => t.cle === 'parfaite')?.gagne === false);
verifie('palmarès : la plus récente d’abord', p.copies[0].id === 'd');
verifie('palmarès : sans copie, aucun trophée', palmares([]).trophees.every((t) => !t.gagne));

console.log(echecs === 0 ? '\nTout passe.' : '\n' + echecs + ' échec(s).');
