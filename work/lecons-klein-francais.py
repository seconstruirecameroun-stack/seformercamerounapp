# -*- coding: utf-8 -*-
"""
Les trois leçons de français du cahier de KLEIN (CE1), octobre 2026.

Les pronoms personnels (mercredi 14 octobre), la phrase et ses constituants
(page sans date), le pluriel des noms en ou et en eu (jeudi 15 octobre).

Rien n'est ajouté au cahier. Un écart est signalé plutôt que corrigé : la
page des pluriels donne six noms en « ou » qui prennent un x — bijou,
caillou, chou, joujou, genou, pou — là où la liste classique en compte sept.
« Hibou » manque. La notion dit donc ce que le cahier dit, et l'explication
le précise, parce qu'un enfant interrogé sur sept exceptions n'a pas à être
pris en défaut par son propre cahier.

Les trois pages portent des en-têtes différents — Conjugaison, Grammaire,
Orthographe — qui sont tous des chapitres de la même matière au programme de
CE1 : Français. L'en-tête du cahier devient le chapitre.

Les illustrations d'une leçon de langue ne peuvent pas montrer la règle. Elles
montrent donc ce qui se compte et ce qui se remplace : un caillou puis des
cailloux, une femme puis sa silhouette, un collier enfilé contre des perles en
tas. Et quand la phrase du cahier parle des femmes qui travaillent la terre,
c'est une terre de latérite rouge.

Usage :  python work/lecons-klein-francais.py
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, '
    'no numbers, no watermark, no real person, no brand. '
)

MATIERE = 'Français'
COULEUR = '#4f7fae'

LECONS = [
    (
        'Les pronoms personnels', 'Conjugaison', '2026-10-14', 10,
        'Le pronom est un mot qui remplace le nom. Maman va au champ devient elle va au champ. '
        'Les pronoms personnels sont je, tu, il, elle, nous, vous, ils, elles.',
        'pp-pronoms',
        'Two rounded cards side by side on a plain background: on the left a woman walking with a hoe, '
        'on the right the very same shape drawn as a simple soft silhouette.',
        [
            (
                'definition',
                'Le pronom est un mot qui remplace le nom.',
                'pp-remplace',
                'One rounded card holding a small figure, and an arrow pointing to a second identical card '
                'holding a plain soft silhouette of the same figure.',
                [
                    ('simple', 'Le pronom prend la place du nom pour ne pas le répéter.'),
                    ('analogie', 'C’est comme un remplaçant au football : il entre, et il joue au même poste.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le pronom remplace…',
                                'options': ['le nom', 'le point', 'la page']},
                     {'index': 0}, 'Il remplace le nom.'),
                    ('qcm', 1, {'question': 'À quoi sert un pronom ?',
                                'options': ['À ne pas répéter le nom', 'À compter', 'À dessiner']},
                     {'index': 0}, 'Il évite de répéter le nom.'),
                    ('qcm', 2, {'question': 'Dans « Paul mange », que peut remplacer un pronom ?',
                                'options': ['Paul', 'mange', 'le point', 'rien du tout']},
                     {'index': 0}, 'Paul est le nom : il peut devenir « il ».'),
                    ('texte_a_trous', 3, {'text': 'Le {{1}} est un mot qui remplace le {{2}}.', 'blanks': 2},
                     {'values': ['pronom', 'nom']}, 'Le pronom remplace le nom.'),
                    ('vrai_faux', 4, {'statement': 'Un pronom remplace un nom.'},
                     {'value': True}, 'C’est sa définition.'),
                ],
            ),
            (
                'relation',
                'Maman va au champ devient elle va au champ : le pronom remplace Maman.',
                'pp-maman',
                'A mother walking along a red laterite path towards a green field, a hoe on her shoulder, '
                'warm morning light.',
                [
                    ('simple', 'On dit Maman une fois, puis elle. On parle de la même personne.'),
                    ('pas_a_pas', 'On trouve le nom : Maman. On cherche qui c’est : une femme. On dit elle.'),
                ],
                [
                    ('qcm', 1, {'question': 'Maman va au champ. On peut dire…',
                                'options': ['Elle va au champ', 'Il va au champ', 'Nous allons au champ']},
                     {'index': 0}, 'Maman est une femme : elle.'),
                    ('qcm', 1, {'question': 'Dans « elle va au champ », elle remplace…',
                                'options': ['Maman', 'le champ', 'la route']},
                     {'index': 0}, 'Elle remplace Maman.'),
                    ('qcm', 2, {'question': 'Papa va au champ. On peut dire…',
                                'options': ['Il va au champ', 'Elle va au champ',
                                            'Ils vont au champ', 'Tu vas au champ']},
                     {'index': 0}, 'Papa est un homme : il.'),
                    ('dictee', 3, {'phrase': 'Elle va au champ.', 'langue': 'fr'},
                     {'phrase': 'Elle va au champ.'}, 'Elle prend deux l.'),
                    ('qcm', 4, {'question': 'Les enfants jouent. On peut dire…',
                                'options': ['Ils jouent', 'Il joue', 'Elle joue']},
                     {'index': 0}, 'Plusieurs garçons et filles : ils.'),
                ],
            ),
            (
                'liste',
                'Les pronoms personnels sont je, tu, il, elle, nous, vous, ils, elles.',
                'pp-huit',
                'Eight small rounded figures in a row on a plain background: one alone, one facing the viewer, '
                'a boy, a girl, a group of three, a group facing the viewer, a group of boys, a group of girls.',
                [
                    ('simple', 'Il y a huit pronoms personnels. Quatre pour un seul, quatre pour plusieurs.'),
                    ('visuel', 'Je, tu, il, elle : une seule personne. Nous, vous, ils, elles : plusieurs.'),
                ],
                [
                    ('qcm', 1, {'question': 'Lequel est un pronom personnel ?',
                                'options': ['nous', 'champ', 'rouge']},
                     {'index': 0}, 'Nous est un pronom personnel.'),
                    ('qcm', 1, {'question': 'Combien y a-t-il de pronoms personnels ?',
                                'options': ['Huit', 'Trois', 'Vingt']},
                     {'index': 0}, 'Huit, dans l’ordre du cahier.'),
                    ('association', 2, {'question': 'Relie chaque pronom à qui il désigne.',
                                        'gauche': ['je', 'tu', 'ils'],
                                        'droite': ['Celui qui parle', 'Celui à qui on parle', 'Plusieurs garçons']},
                     {'order': [0, 1, 2]}, 'Je parle, tu écoutes, ils sont plusieurs.'),
                    ('chronologie', 3, {'question': 'Remets les quatre premiers pronoms dans l’ordre.',
                                        'tokens': ['je', 'tu', 'il', 'elle'],
                                        'consigne': 'Touche les mots dans l’ordre du cahier.'},
                     {'order': [0, 1, 2, 3]}, 'Je, tu, il, elle.'),
                    ('vrai_faux', 4, {'statement': 'Vous est un pronom personnel.'},
                     {'value': True}, 'Il est dans la liste du cahier.'),
                ],
            ),
        ],
    ),
    (
        'La phrase et ses constituants', 'Grammaire', None, 11,
        'La phrase est un ensemble de mots ayant un sens. Elle commence par une lettre majuscule et '
        'se termine par un point. Ses constituants sont un groupe nominal et un groupe verbal.',
        'ph-phrase',
        'A neat row of coloured wooden beads threaded on a string, laid on a plain surface, and beside it '
        'a small loose heap of the very same beads.',
        [
            (
                'definition',
                'La phrase est un ensemble de mots qui a un sens.',
                'ph-sens',
                'A threaded string of coloured beads lying in a neat line, next to a scattered heap of the '
                'same beads, plain soft background.',
                [
                    ('simple', 'Des mots mis ensemble dans le bon ordre : on comprend. C’est une phrase.'),
                    ('analogie', 'Des perles enfilées font un collier. En tas, ce ne sont que des perles.'),
                ],
                [
                    ('qcm', 1, {'question': 'Une phrase est un ensemble de…',
                                'options': ['mots', 'images', 'chiffres']},
                     {'index': 0}, 'Un ensemble de mots.'),
                    ('qcm', 1, {'question': 'Pour être une phrase, les mots doivent…',
                                'options': ['avoir un sens', 'être nombreux', 'être rouges']},
                     {'index': 0}, 'Ils doivent avoir un sens.'),
                    ('qcm', 2, {'question': 'Laquelle est une phrase ?',
                                'options': ['Les femmes travaillent la terre.', 'terre les femmes',
                                            'la la la', 'champ champ']},
                     {'index': 0}, 'Celle-là seule a un sens.'),
                    ('texte_a_trous', 3, {'text': 'La phrase est un ensemble de {{1}} ayant un {{2}}.', 'blanks': 2},
                     {'values': ['mots', 'sens']}, 'Des mots, et un sens.'),
                    ('vrai_faux', 4, {'statement': 'Des mots mis dans le désordre forment une phrase.'},
                     {'value': False}, 'Sans sens, ce n’est pas une phrase.'),
                ],
            ),
            (
                'relation',
                'La phrase commence par une lettre majuscule et se termine par un point.',
                'ph-majuscule',
                'A threaded string of beads where the very first bead is clearly taller than the others and the '
                'very last one is a small round dot, plain soft background.',
                [
                    ('simple', 'Une grande lettre au début, un point à la fin. Les deux bornes de la phrase.'),
                    ('visuel', 'La majuscule ouvre la phrase, le point la ferme.'),
                ],
                [
                    ('qcm', 1, {'question': 'La phrase commence par…',
                                'options': ['une lettre majuscule', 'un point', 'un chiffre']},
                     {'index': 0}, 'Par une majuscule.'),
                    ('qcm', 1, {'question': 'La phrase se termine par…',
                                'options': ['un point', 'une majuscule', 'une virgule']},
                     {'index': 0}, 'Par un point.'),
                    ('qcm', 2, {'question': 'Quelle phrase est bien écrite ?',
                                'options': ['Les enfants jouent.', 'les enfants jouent.',
                                            'Les enfants jouent', 'les enfants jouent']},
                     {'index': 0}, 'Majuscule au début, point à la fin.'),
                    ('chronologie', 3, {'question': 'Remets la phrase dans le bon ordre.',
                                        'tokens': ['La phrase', 'commence', 'par une majuscule'],
                                        'consigne': 'Touche les mots dans l’ordre.'},
                     {'order': [0, 1, 2]}, 'La phrase commence par une majuscule.'),
                    ('vrai_faux', 4, {'statement': 'On peut finir une phrase sans point.'},
                     {'value': False}, 'Le point ferme la phrase.'),
                ],
            ),
            (
                'liste',
                'La phrase a deux constituants : le groupe nominal et le groupe verbal.',
                'ph-deux',
                'Two rounded blocks side by side on a plain background: the left one holds a small group of '
                'people, the right one holds a hoe and a patch of tilled red earth.',
                [
                    ('simple', 'Deux morceaux : qui c’est, et ce qu’il fait.'),
                    ('pas_a_pas', 'On cherche de qui on parle : le groupe nominal. Puis ce qu’il fait : le groupe verbal.'),
                ],
                [
                    ('qcm', 1, {'question': 'Combien la phrase a-t-elle de constituants ?',
                                'options': ['Deux', 'Quatre', 'Dix']},
                     {'index': 0}, 'Deux : le GN et le GV.'),
                    ('qcm', 1, {'question': 'GN veut dire…',
                                'options': ['groupe nominal', 'grand nombre', 'groupe nouveau']},
                     {'index': 0}, 'Groupe nominal.'),
                    ('association', 2, {'question': 'Relie chaque sigle à son nom.',
                                        'gauche': ['GN', 'GV'],
                                        'droite': ['Groupe nominal', 'Groupe verbal']},
                     {'order': [0, 1]}, 'GN et GV.'),
                    ('texte_a_trous', 3, {'text': 'La phrase a un groupe {{1}} et un groupe {{2}}.', 'blanks': 2},
                     {'values': ['nominal', 'verbal']}, 'Nominal et verbal.'),
                    ('vrai_faux', 4, {'statement': 'Le groupe verbal dit ce que l’on fait.'},
                     {'value': True}, 'Il porte le verbe.'),
                ],
            ),
            (
                'definition',
                'Dans « Les femmes travaillent la terre », le groupe nominal est « les femmes ».',
                'ph-femmes',
                'Cameroonian women hoeing a field of red laterite earth, bent over their work, a few young '
                'plants in the rows, warm morning light.',
                [
                    ('simple', 'Les femmes : c’est de qui on parle. Travaillent la terre : ce qu’elles font.'),
                    ('visuel', 'Le verbe est travaillent, et la terre est encore un groupe nominal.'),
                ],
                [
                    ('qcm', 1, {'question': 'Dans « Les femmes travaillent la terre », le GN est…',
                                'options': ['les femmes', 'travaillent', 'la']},
                     {'index': 0}, 'Les femmes.'),
                    ('qcm', 1, {'question': 'Quel est le verbe de cette phrase ?',
                                'options': ['travaillent', 'femmes', 'terre']},
                     {'index': 0}, 'Travaillent.'),
                    ('qcm', 2, {'question': 'Quel est le groupe verbal de cette phrase ?',
                                'options': ['travaillent la terre', 'les femmes',
                                            'la terre seulement', 'les femmes travaillent']},
                     {'index': 0}, 'Le verbe et ce qui le suit.'),
                    ('dictee', 3, {'phrase': 'Les femmes travaillent la terre.', 'langue': 'fr'},
                     {'phrase': 'Les femmes travaillent la terre.'}, 'Travaillent prend deux l.'),
                    ('qcm', 4, {'question': 'Dans « Les enfants aident leurs parents », le GN est…',
                                'options': ['les enfants', 'aident', 'leurs parents']},
                     {'index': 0}, 'C’est de qui on parle.'),
                ],
            ),
        ],
    ),
    (
        'Le pluriel des noms en ou et en eu', 'Orthographe', '2026-10-15', 12,
        'Les noms terminés par ou prennent un s au pluriel, sauf bijou, caillou, chou, joujou, genou et pou '
        'qui prennent un x. Les noms terminés par eu prennent un x au pluriel, sauf pneu, bleu et émeu.',
        'pl-pluriel',
        'A single smooth pebble on pale sand, and beside it a small heap of the very same pebbles, '
        'plain soft background.',
        [
            (
                'relation',
                'Les noms terminés par ou prennent un s au pluriel.',
                'pl-ou',
                'One small round fruit on a plain surface, and beside it several identical fruits grouped '
                'together, soft warm light.',
                [
                    ('simple', 'Un trou, des trous. On ajoute un s, comme presque partout.'),
                    ('visuel', 'La règle est la règle ordinaire : au pluriel, on ajoute un s.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les noms en ou prennent au pluriel…',
                                'options': ['un s', 'un x', 'rien']},
                     {'index': 0}, 'Un s, sauf six exceptions.'),
                    ('qcm', 1, {'question': 'Le pluriel de trou est…',
                                'options': ['trous', 'troux', 'troues']},
                     {'index': 0}, 'Trou suit la règle : trous.'),
                    ('qcm', 2, {'question': 'Lequel prend un s au pluriel ?',
                                'options': ['clou', 'chou', 'genou', 'caillou']},
                     {'index': 0}, 'Clou n’est pas dans les exceptions.'),
                    ('texte_a_trous', 3, {'text': 'Les noms en ou prennent un {{1}} au {{2}}.', 'blanks': 2},
                     {'values': ['s', 'pluriel']}, 'Un s au pluriel.'),
                    ('vrai_faux', 4, {'statement': 'Le pluriel de kangourou est kangourous.'},
                     {'value': True}, 'Il suit la règle ordinaire.'),
                ],
            ),
            (
                'liste',
                'Six noms en ou prennent un x : bijou, caillou, chou, joujou, genou, pou.',
                'pl-ou-exceptions',
                'Six small objects in a row on a plain background: a gold bead, a smooth pebble, a green '
                'cabbage, a small cloth doll, a child bent knee, and one tiny insect.',
                [
                    ('simple', 'Six mots font exception. Ils prennent un x et non un s.'),
                    ('histoire', 'Le cahier en donne six. La liste complète en compte sept : hibou en fait aussi partie.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le pluriel de caillou est…',
                                'options': ['cailloux', 'caillous', 'cailloues']},
                     {'index': 0}, 'Caillou est une exception.'),
                    ('qcm', 1, {'question': 'Combien d’exceptions le cahier donne-t-il ?',
                                'options': ['Six', 'Deux', 'Douze']},
                     {'index': 0}, 'Six noms sont cités.'),
                    ('qcm', 2, {'question': 'Lequel prend un x au pluriel ?',
                                'options': ['genou', 'clou', 'trou', 'kangourou']},
                     {'index': 0}, 'Genou est dans la liste.'),
                    ('dictee', 3, {'phrase': 'Des bijoux et des cailloux.', 'langue': 'fr'},
                     {'phrase': 'Des bijoux et des cailloux.'}, 'Les deux prennent un x.'),
                    ('vrai_faux', 4, {'statement': 'Le pluriel de chou est chous.'},
                     {'value': False}, 'C’est choux, avec un x.'),
                ],
            ),
            (
                'relation',
                'Les noms terminés par eu prennent un x au pluriel.',
                'pl-eu',
                'One small campfire on red earth, and beside it two more identical small fires, soft evening light.',
                [
                    ('simple', 'Un feu, des feux. Ici le pluriel prend un x, pas un s.'),
                    ('analogie', 'C’est le contraire des noms en ou : eu prend un x presque toujours.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les noms en eu prennent au pluriel…',
                                'options': ['un x', 'un s', 'rien']},
                     {'index': 0}, 'Un x, sauf trois exceptions.'),
                    ('qcm', 1, {'question': 'Le pluriel de feu est…',
                                'options': ['feux', 'feus', 'feues']},
                     {'index': 0}, 'Feu prend un x.'),
                    ('qcm', 2, {'question': 'Lequel prend un x au pluriel ?',
                                'options': ['cheveu', 'pneu', 'bleu', 'émeu']},
                     {'index': 0}, 'Les trois autres sont les exceptions.'),
                    ('texte_a_trous', 3, {'text': 'Les noms en eu prennent un {{1}} au {{2}}.', 'blanks': 2},
                     {'values': ['x', 'pluriel']}, 'Un x au pluriel.'),
                    ('vrai_faux', 4, {'statement': 'Le pluriel de jeu est jeux.'},
                     {'value': True}, 'Il suit la règle.'),
                ],
            ),
            (
                'liste',
                'Trois noms en eu prennent un s : pneu, bleu, émeu.',
                'pl-eu-exceptions',
                'Three objects in a row on a plain background: a bicycle tyre, a folded piece of blue cloth, '
                'and one tall flightless bird.',
                [
                    ('simple', 'Trois mots font exception. Ils prennent un s comme les autres noms.'),
                    ('visuel', 'Un pneu, des pneus. Un bleu, des bleus. Un émeu, des émeus.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le pluriel de pneu est…',
                                'options': ['pneus', 'pneux', 'pneues']},
                     {'index': 0}, 'Pneu est une exception.'),
                    ('qcm', 1, {'question': 'Combien y a-t-il d’exceptions en eu ?',
                                'options': ['Trois', 'Six', 'Dix']},
                     {'index': 0}, 'Pneu, bleu, émeu.'),
                    ('association', 2, {'question': 'Relie chaque mot à son pluriel.',
                                        'gauche': ['pneu', 'feu', 'bleu'],
                                        'droite': ['pneus', 'feux', 'bleus']},
                     {'order': [0, 1, 2]}, 'Deux exceptions et un mot ordinaire.'),
                    ('texte_a_trous', 3, {'text': 'Un {{1}}, des pneus. Un feu, des {{2}}.', 'blanks': 2},
                     {'values': ['pneu', 'feux']}, 'Pneu fait exception, feu non.'),
                    ('vrai_faux', 4, {'statement': 'Le pluriel de bleu est bleux.'},
                     {'value': False}, 'C’est bleus, avec un s.'),
                ],
            ),
        ],
    ),
]

NIVEAUX_ATTENDUS = {1, 2, 3, 4}


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total = set(), 0
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 320, 'résumé trop long : ' + titre
        assert img not in cles, 'image en double : ' + img
        cles.add(img)
        for kind, phrase, nimg, nprompt, expl, items in notions:
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 150, 'notion trop longue : ' + phrase
            assert nimg not in cles, 'image en double : ' + nimg
            cles.add(nimg)
            for registre, corps in expl:
                assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), registre
                assert len(corps) <= 200, 'explication trop longue : ' + corps
            niveaux = set()
            for ikind, niveau, payload, answer, explain in items:
                total += 1
                niveaux.add(niveau)
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                if ikind == 'qcm':
                    assert len(payload['question']) <= 80, 'question trop longue : ' + payload['question']
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 60, 'option trop longue pour un CE1 : ' + o
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 90, payload
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous pour un CE1 : ' + payload['text']
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                elif ikind == 'dictee':
                    assert payload['phrase'] == answer['phrase'], payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))
    return len(cles), total


def paquet():
    return {
        'matiere': MATIERE, 'couleur': COULEUR, 'classe': 'CE1', 'enfant': 'KLEIN',
        'lecons': [
            {
                'title': titre, 'chapter': chapitre, 'taught_on': date, 'sort_order': ordre,
                'summary': resume, 'illustration': img, 'illustration_prompt': STYLE + prompt,
                'notions': [
                    {
                        'kind': k, 'statement': p, 'illustration': ni,
                        'illustration_prompt': STYLE + npr,
                        'explanations': [{'register': r, 'body': b} for r, b in ex],
                        'items': [{'kind': ik, 'level': lv, 'payload': pl,
                                   'answer': an, 'explain': exp}
                                  for ik, lv, pl, an, exp in it],
                    }
                    for k, p, ni, npr, ex, it in notions
                ],
            }
            for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS
        ],
    }


if __name__ == '__main__':
    images, items = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Servi par le serveur de développement le temps de l'insertion, puis
    # retiré : rien de tout cela n'a à vivre dans le dossier public.
    chemin = os.path.join(racine, 'app', 'public', 'seed-francais.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    notions = sum(len(l[7]) for l in LECONS)
    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-36s %-14s %-10s %d notions'
              % (titre, chapitre, date or 'sans date', len(ns)))
    print(chemin)
