/**
 * Vérifications de la comparaison des mots.
 *
 * Écrites parce qu'un typecheck vert avait laissé passer le défaut qu'elles
 * couvrent : la rangée des accents était facultative, les textes à trous ne
 * la demandaient pas, et la réponse « s’élargit » était donc impossible à
 * écrire. Un test du composant seul ne l'aurait pas vu — il faut tester ce
 * que la correction accepte, et avec quels caractères.
 *
 *   npx esbuild src/components/items/partage.verif.tsx --bundle --platform=node \
 *     --outfile=../../tmp-verif.cjs --format=cjs --external:react && node ../../tmp-verif.cjs
 */

import { ecartMot, memeMot, memePhrase } from './partage';
import { accentsComptent, ETAPE_DEFI, ETAPE_PRODUCTION } from '../../lib/saisie';

const APOS = '’';
let ko = 0;
function ok(nom: string, vrai: boolean) {
  if (!vrai) {
    ko += 1;
    console.log('KO  ' + nom);
  }
}

// Ce que le clavier produit doit être accepté. L’enfant tape l’apostrophe
// typographique, qui est la seule touche disponible.
ok('apostrophe du clavier acceptée', memeMot('s' + APOS + 'élargit', 's' + APOS + 'élargit'));
// Et si la base, elle, contient l’apostrophe droite, la réponse doit passer
// quand même : l’enfant n’a aucun moyen de savoir laquelle est attendue.
ok('apostrophe droite en base', memeMot('s' + APOS + 'élargit', "s'élargit"));
ok('apostrophe droite en base, au défi', memeMot('s' + APOS + 'élargit', "s'élargit", true));
ok('apostrophe tapée, attendue typographique', memeMot("l'eau", 'l' + APOS + 'eau'));

// Avant le défi, l’accent est pardonné.
ok('accent pardonné hors défi', memeMot('eleve', 'élève'));
ok('casse pardonnée', memeMot('ÉLÈVE', 'élève'));
ok('espaces pardonnés', memeMot('  sous-multiples ', 'sous-multiples'));
// Au défi, il compte.
ok('accent compté au défi', !memeMot('eleve', 'élève', true));
ok('accent juste accepté au défi', memeMot('élève', 'élève', true));
ok('casse encore pardonnée au défi', memeMot('Élève', 'élève', true));
// Le clavier compose en NFC ; une réponse en base décomposée doit passer.
ok('NFD en base = NFC au clavier', memeMot('élève', 'e\u0301le\u0300ve', true));

// La ligature n'est pas un accent : « oe » vaut « œ », partout.
ok('ligature : « oeuf » vaut « œuf »', memeMot('oeuf', 'œuf'));
ok('ligature : et dans l’autre sens', memeMot('œuf', 'oeuf'));
ok('ligature : aussi au Défi, où l’accent compte', memeMot('soeur', 'sœur', true));
ok('ligature : « ae » vaut « æ »', memeMot('ex aequo', 'ex æquo'));
ok('ligature : l’accent compte encore au Défi', !memeMot('coeur', 'cœür', true));
ok('dictée : la phrase de KLEIN est acceptée',
  memePhrase('les ovipares pondent des oeufs', 'Les ovipares pondent des œufs.'));
ok('dictée : les accents comptent toujours', !memePhrase('la benoue arrose garoua', 'La Bénoué arrose Garoua.'));
ok('dictée : une vraie faute reste une faute', !memePhrase('les ovipare pondent des oeufs', 'Les ovipares pondent des œufs.'));
// Le trait d’union et les chiffres, qui vivent sur la seconde page.
ok('trait d’union', memeMot('fifty-one', 'fifty-one', true));
ok('chiffres', memeMot('200', '200', true));

// La règle d’étape.
ok('défi strict', accentsComptent(ETAPE_DEFI));
ok('maîtrise indulgente', !accentsComptent(ETAPE_PRODUCTION));
ok('découverte indulgente', !accentsComptent(1));

// L’écart doit montrer l’accent quand il compte, sinon l’enfant voit une
// réponse refusée sans rien qui la distingue de ce qu’il a écrit.
const e = ecartMot('eleve', 'élève', true);
ok('écart montre l’accent', e.ecrit !== e.attendu && (e.debut + e.ecrit + e.fin) === 'eleve');
const n = ecartMot('sabloneux', 'sablonneux');
ok('écart lettre manquante', n.debut === 'sablon' && n.ecrit === '' && n.attendu === 'n' && n.fin === 'eux');
// Hors défi, un simple accent ne crée pas d’écart : le mot est juste.
const z = ecartMot('eleve', 'élève');
ok('pas d’écart sans le défi', z.ecrit === '' && z.attendu === '');

// Un `throw` plutot que process.exit : node rend alors un code non nul sans
// qu'on ait besoin des types node dans le typecheck de l'application.
if (ko > 0) throw new Error(ko + ' echec(s)');
console.log('partage : 21 verifications, tout passe');
