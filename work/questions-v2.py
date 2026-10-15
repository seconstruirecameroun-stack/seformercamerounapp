# -*- coding: utf-8 -*-
"""
Les nouveaux types de questions, et la quatrième étape.

Avant : 183 questions dont 139 QCM. L'enfant répondait presque toujours de
la même façon — on mesurait sa capacité à reconnaître la bonne case plus que
ce qu'il savait.

Ce fichier ajoute quatre façons d'interroger et une marche :

  relier        les leçons sont faites de listes (quatre sols, trois époques,
                des inventions et leurs inventeurs). Un QCM les découpe et
                perd justement le lien.
  vrai / faux   rapide, en série ; seul il laisse une chance sur deux.
  image         on génère déjà une illustration par notion : « clique sur le
                sol ferralitique » convient mieux à un CE1 qu'un mot à lire.
  dictée        le navigateur parle sans réseau, et l'école a ses créneaux
                de dictée.
  mots en ordre reconstruire la phrase du résumé (même moteur que la
                chronologie, autre consigne).

L'étape 4 « Défi » se joue au chronomètre : vingt secondes par question. On
n'y pose donc que du court, et on y demande du transfert — appliquer ce
qu'on sait à un cas qu'on n'a pas vu.

Usage :  python work/questions-v2.py
"""

import io
import json
import os

# (lecon, rang de la notion, kind, niveau, payload, answer, explain)
Q = []


def q(lecon, rang, kind, niveau, payload, answer, explain):
    Q.append({'lecon': lecon, 'rang': rang, 'kind': kind, 'level': niveau,
              'payload': payload, 'answer': answer, 'explain': explain})


def qcm(lecon, rang, niveau, question, options, bonne, explain):
    q(lecon, rang, 'qcm', niveau, {'question': question, 'options': options}, {'index': bonne}, explain)


def images(lecon, rang, niveau, question, cles, bonne, explain):
    q(lecon, rang, 'qcm', niveau, {'question': question, 'images': cles}, {'index': bonne}, explain)


def vf(lecon, rang, niveau, phrase, valeur, explain):
    q(lecon, rang, 'vrai_faux', niveau, {'statement': phrase}, {'value': valeur}, explain)


def relier(lecon, rang, niveau, question, gauche, droite, explain):
    """gauche[i] va avec droite[i] : on mélange l'affichage, pas les données."""
    q(lecon, rang, 'association', niveau, {'question': question, 'gauche': gauche, 'droite': droite},
      {'order': list(range(len(gauche)))}, explain)


def dictee(lecon, rang, niveau, phrase, explain, langue='fr'):
    q(lecon, rang, 'dictee', niveau, {'phrase': phrase, 'langue': langue}, {'phrase': phrase}, explain)


def mots(lecon, rang, niveau, jetons, explain):
    q(lecon, rang, 'chronologie', niveau,
      {'question': 'Remets la phrase dans le bon ordre.', 'tokens': jetons,
       'consigne': 'Touche les mots dans l’ordre de la phrase.'},
      {'order': list(range(len(jetons)))}, explain)


PRE = 'La Préhistoire'
GD = 'Les grandes inventions et les grandes découvertes'
OB = 'L’obéissance'
ID = 'Le droit à l’identité'
IN = 'L’intégration nationale'
FI = 'Les techniques de filtrage de l’eau'
PA = 'La paix'
SO = 'Le sol'

# ═══════════════════════ La Préhistoire (CM1, 7 notions) ═══════════════════════

relier(PRE, 7, 2, 'Relie chaque époque à ce qu’on y fabrique.',
       ['Paléolithique', 'Néolithique', 'Âge des métaux'],
       ['La pierre taillée', 'La pierre polie', 'Le cuivre et le fer'],
       'Taillée, polie, puis les métaux.')
images(PRE, 3, 2, 'Clique sur l’outil du Paléolithique.',
       ['biface', 'hache-ble', 'metaux', 'tablette-ecriture'], 0,
       'Le biface est une pierre taillée.')
images(PRE, 6, 2, 'Clique sur ce qu’on fabrique à l’âge des métaux.',
       ['metaux', 'biface', 'chasse-peche-cueillette', 'tablette-ecriture'], 0,
       'Des outils et des bijoux en métal.')
dictee(PRE, 3, 3, 'Le Paléolithique est l’âge de la pierre taillée.', 'Pierre taillée.')
dictee(PRE, 5, 3, 'Au Néolithique, les humains commencent l’agriculture.', 'Le Néolithique et l’agriculture.')
mots(PRE, 2, 3, ['L’écriture', 'marque', 'la fin', 'de la Préhistoire'], 'L’écriture clôt la Préhistoire.')
mots(PRE, 1, 3, ['La Préhistoire', 'commence', 'avec les premiers', 'humains'], 'Elle commence avec eux.')

vf(PRE, 1, 4, 'La Préhistoire se termine quand on invente l’écriture.', True, 'Oui, vers 3 000 avant J.-C.')
vf(PRE, 2, 4, 'L’écriture est inventée après l’âge des métaux.', False,
   'Non : elle arrive à la fin de la Préhistoire, après l’âge des métaux dans le temps mais c’est elle qui la termine.')
qcm(PRE, 3, 4, 'On trouve une pierre cassée en pointe. Quelle époque ?',
    ['Le Paléolithique', 'Le Néolithique', 'L’âge des métaux'], 0, 'Pierre taillée : Paléolithique.')
qcm(PRE, 4, 4, 'Un campement déplacé chaque mois. Que mangent-ils ?',
    ['Ce qu’ils chassent et cueillent', 'Le blé de leurs champs', 'Des animaux d’élevage'], 0,
    'Ils suivent leur nourriture.')
qcm(PRE, 5, 4, 'On trouve des grains de blé et une meule. Quelle époque ?',
    ['Le Néolithique', 'Le Paléolithique', 'La Préhistoire n’en a pas'], 0, 'L’agriculture, donc le Néolithique.')
qcm(PRE, 6, 4, 'Un bracelet en bronze sort de terre. Quelle époque ?',
    ['L’âge des métaux', 'Le Paléolithique', 'Le Néolithique'], 0, 'Le bronze est un métal.')
qcm(PRE, 7, 4, 'Quelle époque vient entre les deux autres ?',
    ['Le Néolithique', 'Le Paléolithique', 'L’âge des métaux'], 0, 'Paléolithique, Néolithique, métaux.')

# ═══════════════ Les grandes inventions (CM1, 11 notions) ═══════════════

relier(GD, 6, 2, 'Relie chaque invention à son peuple.',
       ['Le papier', 'La caravelle', 'L’imprimerie'],
       ['Les Chinois', 'Les Portugais', 'L’Allemand Gutenberg'],
       'Chine, Portugal, Allemagne.')
relier(GD, 9, 2, 'Relie chaque navigateur à sa découverte.',
       ['Bartholomeu Dias', 'Christophe Colomb', 'Vasco de Gama'],
       ['Le cap de Bonne-Espérance', 'L’Amérique', 'La route des Indes'],
       '1487, 1492, 1498.')
relier(GD, 11, 3, 'Relie chaque voyage à son année.',
       ['Dias', 'Colomb', 'Vasco de Gama', 'Magellan'],
       ['1487', '1492', '1498', '1519'],
       'Dans l’ordre : 1487, 1492, 1498, 1519.')
images(GD, 3, 2, 'Clique sur la boussole.',
       ['gd-boussole', 'gd-gouvernail', 'gd-caravelle', 'gd-imprimerie'], 0,
       'Elle montre le nord.')
images(GD, 5, 2, 'Clique sur la caravelle.',
       ['gd-caravelle', 'gd-boussole', 'gd-papier-poudre', 'gd-imprimerie'], 0,
       'Le bateau portugais de 1440.')
dictee(GD, 1, 3, 'Une invention crée un objet qui n’existait pas.', 'Créer ce qui n’existait pas.')
dictee(GD, 6, 3, 'Gutenberg invente l’imprimerie en 1450.', 'Gutenberg, 1450.')
mots(GD, 7, 3, ['Ces inventions', 'ont favorisé', 'la navigation'], 'Elles ont aidé les marins.')

vf(GD, 1, 4, 'Découvrir l’Amérique, c’est l’inventer.', False, 'On découvre une terre, on ne l’invente pas.')
vf(GD, 2, 4, 'Le papier vient de Chine.', True, 'Oui, au 1ᵉʳ siècle.')
vf(GD, 3, 4, 'La boussole sert à faire avancer le bateau.', False, 'Elle donne la direction, pas la force.')
vf(GD, 4, 4, 'Le gouvernail sert à diriger le bateau.', True, 'Oui, il le dirige.')
vf(GD, 5, 4, 'La caravelle est inventée après l’imprimerie.', False, 'Caravelle 1440, imprimerie 1450.')
vf(GD, 7, 4, 'Sans la boussole, les marins seraient allés aussi loin.', False,
   'Sans direction en pleine mer, on ne s’éloigne pas des côtes.')
qcm(GD, 6, 4, 'Grâce à quoi un même livre existe en mille exemplaires ?',
    ['L’imprimerie', 'La boussole', 'La caravelle'], 0, 'L’imprimerie copie vite.')
qcm(GD, 8, 4, 'Un marin contourne le sud de l’Afrique. Qui est-ce ?',
    ['Bartholomeu Dias', 'Christophe Colomb', 'Magellan'], 0, 'Dias, au cap de Bonne-Espérance.')
qcm(GD, 9, 4, 'Il part vers l’ouest chercher les Indes et trouve une autre terre.',
    ['Christophe Colomb', 'Vasco de Gama', 'Dias'], 0, 'Colomb, en 1492.')
qcm(GD, 10, 4, 'Il rapporte des épices par la mer, en passant au sud de l’Afrique.',
    ['Vasco de Gama', 'Colomb', 'Gutenberg'], 0, 'Vasco de Gama, en 1498.')
qcm(GD, 11, 4, 'Un bateau part à l’ouest et revient par l’est. Qu’a-t-il fait ?',
    ['Le tour du monde', 'Un aller-retour', 'Un naufrage'], 0, 'C’est Magellan.')

# ═══════════════════════ L’obéissance (CE1, 3 notions) ═══════════════════════

vf(OB, 1, 2, 'Obéir, c’est discuter avant de faire.', False, 'Obéir, c’est faire sans discuter.')
vf(OB, 2, 2, 'Un enfant obéissant est aimé de tout le monde.', True, 'Oui, c’est ce que dit la leçon.')
relier(OB, 1, 2, 'Relie chaque mot à ce qu’il veut dire.',
       ['Obéir', 'Un aîné', 'Une consigne'],
       ['Faire ce qu’on demande', 'Un plus grand que moi', 'Ce qu’on me demande de faire'],
       'Trois mots de la leçon.')
dictee(OB, 2, 3, 'Un enfant obéissant est aimé de tout le monde.', 'La phrase du cahier.')
mots(OB, 3, 3, ['Pour réussir', 'dans la vie', 'il faut obéir'], 'La leçon finit là-dessus.')

qcm(OB, 1, 4, 'Ton maître te demande de ranger. Tu fais quoi ?',
    ['Je range tout de suite', 'Je demande pourquoi', 'Je range demain'], 0, 'Sans discuter.')
qcm(OB, 2, 4, 'Pourquoi aime-t-on un enfant obéissant ?',
    ['Il fait ce qu’on lui demande', 'Il crie fort', 'Il court vite'], 0, 'Parce qu’il écoute.')
vf(OB, 3, 4, 'Obéir aujourd’hui aide à réussir plus tard.', True, 'C’est ce que dit la leçon.')

# ═══════════════════ Le droit à l’identité (CE1, 2 notions) ═══════════════════

vf(ID, 1, 2, 'Seuls les grands ont droit à une identité.', False, 'Chaque enfant y a droit.')
relier(ID, 2, 2, 'Relie chaque chose à ce qu’elle est.',
       ['Mon nom', 'Ma nationalité'],
       ['Comment on m’appelle', 'Le pays qui est le mien'],
       'Les deux font l’identité.')
dictee(ID, 1, 3, 'Chaque enfant a droit à une identité.', 'La phrase du cahier.')
mots(ID, 2, 3, ['L’identité', 'donne un nom', 'et une nationalité'], 'Un nom et une nationalité.')

qcm(ID, 1, 4, 'Un bébé qui vient de naître a-t-il droit à une identité ?',
    ['Oui, dès sa naissance', 'Non, à six ans', 'Seulement à l’école'], 0, 'Chaque enfant, dès le début.')
qcm(ID, 2, 4, 'Être camerounais, c’est quelle partie de mon identité ?',
    ['Ma nationalité', 'Mon nom', 'Mon âge'], 0, 'C’est la nationalité.')

# ═══════════════ L’intégration nationale (CE1, 3 notions) ═══════════════

vf(IN, 2, 2, 'Au Cameroun, il y a moins de dix ethnies.', False, 'Il y en a plus de 250.')
relier(IN, 3, 2, 'Relie chaque moyen à ce qu’il rapproche.',
       ['Le mariage interethnique', 'La cohabitation', 'L’affectation'],
       ['Deux familles', 'Des voisins', 'Un travailleur et une région'],
       'Trois façons de se rapprocher.')
images(IN, 2, 2, 'Clique sur le village où vivent plusieurs peuples.',
       ['in-ethnies', 'in-melange', 'in-moyens'], 0, 'Beaucoup de maisons différentes, côte à côte.')
dictee(IN, 1, 3, 'L’intégration nationale mélange les cultures.', 'Un mélange de cultures.')
mots(IN, 2, 3, ['Au Cameroun', 'les ethnies', 'vivent en paix'], 'Plus de 250, en paix.')

qcm(IN, 1, 4, 'Deux familles de régions différentes fêtent ensemble. C’est quoi ?',
    ['De l’intégration nationale', 'Une dispute', 'Un voyage'], 0, 'Les cultures se mélangent.')
qcm(IN, 2, 4, 'Combien d’ethnies au Cameroun ?',
    ['Plus de 250', 'Environ 20', 'Une seule'], 0, 'Plus de 250.')
vf(IN, 3, 4, 'Refuser les gens d’une autre ethnie aide l’intégration.', False, 'Cela sépare au lieu de rassembler.')

# ═══════════ Les techniques de filtrage de l’eau (CE1, 3 notions) ═══════════

relier(FI, 1, 2, 'Relie chaque matière à son rôle.',
       ['Le gravier', 'Le charbon', 'Le coton'],
       ['Il arrête les gros morceaux', 'Il nettoie l’eau', 'Il retient les petites saletés'],
       'Chacun fait son travail.')
images(FI, 2, 2, 'Clique sur le filtre et ses couches.',
       ['fi-couches', 'fi-materiel', 'fi-eau-potable'], 0, 'Gravier, charbon, sable, coton.')
dictee(FI, 3, 3, 'L’eau sale entre et l’eau propre sort.', 'Entrée sale, sortie propre.')
mots(FI, 2, 3, ['Le gravier', 'puis le charbon', 'puis le sable', 'puis le coton'],
     'L’ordre des couches, de haut en bas.')

qcm(FI, 1, 4, 'Il te manque le charbon. Ton filtre marchera-t-il aussi bien ?',
    ['Non, il nettoie moins bien', 'Oui, c’est pareil', 'Oui, il ira plus vite'], 0,
    'Chaque couche sert à quelque chose.')
qcm(FI, 2, 4, 'Tu mets le coton tout en haut. Que se passe-t-il ?',
    ['L’eau n’est pas bien filtrée', 'Rien ne change', 'L’eau devient sucrée'], 0,
    'L’ordre compte : le coton est en bas.')
vf(FI, 3, 4, 'L’eau du puits est toujours potable.', False, 'Pas toujours : c’est pour ça qu’on filtre.')

# ═══════════════════════ La paix (CE1, 2 notions) ═══════════════════════

relier(PA, 2, 2, 'Relie chaque geste à son mot.',
       ['Je porte le panier de mon voisin', 'Je joue avec un enfant d’ailleurs', 'On construit ensemble'],
       ['Assister', 'Accepter', 'Collaborer'],
       'Trois gestes du vivre-ensemble.')
vf(PA, 1, 2, 'On vit ensemble seulement au village.', False, 'Au village ou en ville.')
dictee(PA, 1, 3, 'Je vis bien avec les autres.', 'La paix commence là.')
mots(PA, 2, 3, ['Accepter', 'aider', 'et collaborer'], 'Les gestes du vivre-ensemble.')

qcm(PA, 1, 4, 'Deux camarades se disputent. Que fais-tu pour la paix ?',
    ['Je les aide à se parler', 'Je prends un camp', 'Je m’en vais'], 0, 'On rapproche, on ne sépare pas.')
qcm(PA, 2, 4, 'Un nouvel élève ne parle pas ta langue. Tu fais quoi ?',
    ['Je l’accepte et je l’aide', 'Je me moque', 'Je l’ignore'], 0, 'Accepter, c’est le premier geste.')

# ═══════════════════════ Le sol (CE1, 6 notions) ═══════════════════════

relier(SO, 2, 2, 'Relie chaque sol à ce qui le reconnaît.',
       ['Sablonneux', 'Ferralitique', 'Basaltique', 'Argileux'],
       ['Des grains de roche', 'Rouge, riche en fer', 'Noir et fertile', 'Mou, pas fertile'],
       'Les quatre sols du cahier.')
images(SO, 4, 2, 'Clique sur le sol ferralitique.',
       ['so-ferralitique', 'so-basaltique', 'so-sablonneux', 'so-argileux'], 0, 'Il est rouge.')
images(SO, 5, 2, 'Clique sur le sol basaltique.',
       ['so-basaltique', 'so-ferralitique', 'so-argileux', 'so-sablonneux'], 0, 'Il est noir.')
images(SO, 3, 2, 'Clique sur le sol sablonneux.',
       ['so-sablonneux', 'so-argileux', 'so-basaltique', 'so-ferralitique'], 0, 'Fait de grains de roche.')
dictee(SO, 1, 3, 'Le sol est la partie du dessus de la terre.', 'La couche du dessus.')
dictee(SO, 4, 3, 'Le sol ferralitique est rouge.', 'Rouge, riche en fer.')
mots(SO, 6, 3, ['Le sol argileux', 'est mou', 'et pas fertile'], 'Mou et pas fertile.')

vf(SO, 1, 4, 'Le sol est la partie profonde de la terre.', False, 'C’est la partie du dessus.')
vf(SO, 2, 4, 'Tous les sols se ressemblent.', False, 'Ils diffèrent par leur structure.')
qcm(SO, 3, 4, 'Tu marches sur une terre qui coule entre les doigts. Lequel ?',
    ['Sablonneux', 'Argileux', 'Basaltique'], 0, 'Des grains de roche.')
qcm(SO, 4, 4, 'Une terre très rouge après la pluie. Lequel ?',
    ['Ferralitique', 'Basaltique', 'Sablonneux'], 0, 'Rouge : riche en fer.')
qcm(SO, 5, 4, 'Dans quel sol le maïs poussera-t-il le mieux ?',
    ['Le basaltique', 'L’argileux', 'Le sablonneux'], 0, 'Noir et fertile.')
qcm(SO, 6, 4, 'Un paysan évite une terre molle où rien ne pousse. Laquelle ?',
    ['L’argileuse', 'La basaltique', 'La ferralitique'], 0, 'Molle et pas fertile.')


# ─────────────────────────── vérifications ───────────────────────────

NOTIONS = {PRE: 7, GD: 11, OB: 3, ID: 2, IN: 3, FI: 3, PA: 2, SO: 6}


def verifier():
    for r in Q:
        textes = json.dumps([r['payload'], r['answer'], r['explain']], ensure_ascii=False)
        assert "'" not in textes, 'apostrophe droite : ' + textes
        assert 1 <= r['rang'] <= NOTIONS[r['lecon']], 'rang hors leçon : ' + str(r)
        assert 1 <= r['level'] <= 4, r

        k, p, a = r['kind'], r['payload'], r['answer']
        if k == 'qcm' and 'images' in p:
            assert 2 <= len(p['images']) <= 4 and len(set(p['images'])) == len(p['images']), p
            assert 0 <= a['index'] < len(p['images'])
        elif k == 'qcm':
            assert 2 <= len(p['options']) <= 4 and len(set(p['options'])) == len(p['options']), p
            assert 0 <= a['index'] < len(p['options'])
            assert len(p['question']) <= 80, p['question']
        elif k == 'vrai_faux':
            assert isinstance(a['value'], bool) and len(p['statement']) <= 90, p
        elif k == 'association':
            assert len(p['gauche']) == len(p['droite']) == len(a['order']), p
            assert 2 <= len(p['gauche']) <= 4, p
            assert sorted(a['order']) == list(range(len(p['gauche'])))
        elif k == 'dictee':
            assert p['phrase'] == a['phrase']
            assert len(p['phrase'].split()) <= 10, 'dictée trop longue : ' + p['phrase']
        elif k == 'chronologie':
            assert sorted(a['order']) == list(range(len(p['tokens'])))
        else:
            raise AssertionError('type inconnu ' + k)

        # L'étape 4 se joue en vingt secondes : rien de long.
        if r['level'] == 4:
            assert k in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + k

    # Chaque notion doit avoir de quoi franchir l'étape 4.
    defis = {(r['lecon'], r['rang']) for r in Q if r['level'] == 4}
    manquantes = [(l, n) for l, total in NOTIONS.items() for n in range(1, total + 1)
                  if (l, n) not in defis]
    assert not manquantes, 'notions sans question de Défi : %s' % manquantes


if __name__ == '__main__':
    verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    io.open(os.path.join(racine, 'work', 'questions-v2.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(Q, ensure_ascii=False, indent=1))

    par_type, par_niveau = {}, {}
    for r in Q:
        cle = 'image' if (r['kind'] == 'qcm' and 'images' in r['payload']) else (
            'mots en ordre' if (r['kind'] == 'chronologie' and 'consigne' in r['payload']) else r['kind'])
        par_type[cle] = par_type.get(cle, 0) + 1
        par_niveau['N%d' % r['level']] = par_niveau.get('N%d' % r['level'], 0) + 1
    print('%d questions' % len(Q))
    print('  par type   : ' + ', '.join('%s %d' % (k, v) for k, v in sorted(par_type.items())))
    print('  par niveau : ' + ', '.join('%s %d' % (k, par_niveau[k]) for k in sorted(par_niveau)))
