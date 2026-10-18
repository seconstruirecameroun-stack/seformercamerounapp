# -*- coding: utf-8 -*-
"""
Les trois leçons de mathématiques du cahier de KLEIN (CE1), octobre 2026.

Les nombres de 101 à 999 (mardi 13 octobre), le cube (mercredi 14 octobre),
les sous-multiples (jeudi 15 octobre). Une quatrième page, « Comparer et
ordonner les nombres de 101 à 999 » (vendredi 16 octobre), ne porte aucun
« Je retiens » : elle n'est pas ici, parce qu'en faire une leçon demanderait
d'inventer la règle que la page ne donne pas.

Un écart est signalé plutôt que recopié. La page des nombres écrit
« 340 = trois cents quarante », avec un s, alors que sa propre règle dit que
cent ne prend pas de s quand un nombre le suit. L'écart n'est pas une
omission comme « hibou » : c'est une faute que la règle du cahier réfute
elle-même. La notion applique donc la règle — trois cent quarante — et
l'explication dit que le cahier a écrit un s de trop, pour que KLEIN ne soit
pris en défaut ni par sa leçon ni par sa page.

Les illustrations ne sont pas générées : en mathématiques la figure doit être
exacte, et un générateur produit volontiers un cube à sept arêtes. Elles sont
dessinées par work/figures-maths.py. Le champ illustration_prompt décrit donc
ce que le dessin doit contenir, pas ce qu'un modèle doit imaginer.

Usage :  python work/lecons-klein-maths.py
"""

import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-maths.py. '

MATIERE = 'Mathématiques'
COULEUR = '#3f7d6a'

LECONS = [
    (
        'Les nombres de 101 à 999', 'Nombres et calculs', '2026-10-13', 13,
        'Pour écrire un nombre en lettres, je mets un s à cent lorsqu’il est multiplié et qu’aucun '
        'autre nombre ne le suit. 100 s’écrit cent, 200 deux cents, 340 trois cent quarante. '
        '999 est le plus grand nombre à trois chiffres.',
        'nb-nombres',
        'Trois tuiles pastel portant 9, 9 et 9, surmontées des mots centaines, dizaines, unités.',
        [
            (
                'relation',
                'Cent prend un s quand il est multiplié et qu’aucun nombre ne le suit.',
                'nb-regle',
                'Le mot cents en grand, le s final détaché en terre cuite, et une case vide derrière lui.',
                [
                    ('simple', 'Deux conditions, pas une : cent doit être multiplié, et rien ne doit le suivre.'),
                    ('pas_a_pas', 'Je regarde devant cent : y a-t-il un nombre ? Je regarde derrière : y a-t-il un nombre ? S’il n’y a rien derrière, je mets le s.'),
                ],
                [
                    ('qcm', 1, {'question': 'Cent prend un s quand il est…',
                                'options': ['multiplié', 'tout seul', 'au début']},
                     {'index': 0}, 'Il faut qu’il soit multiplié.'),
                    ('qcm', 1, {'question': 'Cent prend un s si aucun nombre ne le…',
                                'options': ['suit', 'précède', 'compte']},
                     {'index': 0}, 'Rien ne doit venir après lui.'),
                    ('qcm', 2, {'question': 'Dans quel cas cent prend-il un s ?',
                                'options': ['Multiplié et rien après', 'Tout seul',
                                            'Suivi d’un nombre', 'Jamais']},
                     {'index': 0}, 'Les deux conditions ensemble.'),
                    ('texte_a_trous', 3, {'text': 'Cent prend un {{1}} quand il est {{2}}.', 'blanks': 2},
                     {'values': ['s', 'multiplié']}, 'Un s, et seulement s’il est multiplié.'),
                    ('vrai_faux', 4, {'statement': 'Cent prend un s quand un nombre le suit.'},
                     {'value': False}, 'Au contraire : s’il est suivi, il perd le s.'),
                ],
            ),
            (
                'definition',
                '100 s’écrit cent, sans s : cent n’est pas multiplié.',
                'nb-cent',
                'La tuile 100 et le mot cent, avec une case vide devant le mot.',
                [
                    ('simple', 'Il n’y a qu’une centaine. Cent n’est multiplié par rien, donc pas de s.'),
                    ('visuel', 'Devant cent, il n’y a aucun nombre écrit : la première condition manque.'),
                ],
                [
                    ('qcm', 1, {'question': '100 s’écrit…',
                                'options': ['cent', 'cents', 'centre']},
                     {'index': 0}, 'Cent, sans s.'),
                    ('qcm', 1, {'question': 'Dans 100, cent est-il multiplié ?',
                                'options': ['Non', 'Oui', 'Parfois']},
                     {'index': 0}, 'Aucun nombre ne le multiplie.'),
                    ('qcm', 2, {'question': 'Pourquoi cent ne prend pas de s dans 100 ?',
                                'options': ['Il n’est pas multiplié', 'Il est suivi',
                                            'Il est trop petit', 'Il est au pluriel']},
                     {'index': 0}, 'La première condition manque.'),
                    ('dictee', 3, {'phrase': 'Cent enfants.', 'langue': 'fr'},
                     {'phrase': 'Cent enfants.'}, 'Cent tout seul ne prend pas de s.'),
                    ('vrai_faux', 4, {'statement': '100 s’écrit cents.'},
                     {'value': False}, 'C’est cent, sans s.'),
                ],
            ),
            (
                'definition',
                '200 s’écrit deux cents, avec un s : cent est multiplié et rien ne le suit.',
                'nb-deux-cents',
                'Deux disques pastel portant chacun 100, et dessous le mot deux cents, le s mis en relief.',
                [
                    ('simple', 'Deux fois cent, et plus rien derrière : le s arrive.'),
                    ('analogie', 'Deux paquets de cent. On dit deux cents comme on dirait deux paquets.'),
                ],
                [
                    ('qcm', 1, {'question': '200 s’écrit…',
                                'options': ['deux cents', 'deux cent', 'deux centes']},
                     {'index': 0}, 'Avec un s : rien ne suit cent.'),
                    ('qcm', 1, {'question': 'Dans 200, cent est multiplié par…',
                                'options': ['deux', 'dix', 'cent']},
                     {'index': 0}, 'Par deux.'),
                    ('qcm', 2, {'question': 'Lequel est bien écrit ?',
                                'options': ['trois cents', 'trois cent', 'troi cents', 'trois centes']},
                     {'index': 0}, '300 : cent est multiplié et rien ne suit.'),
                    ('dictee', 3, {'phrase': 'Deux cents francs.', 'langue': 'fr'},
                     {'phrase': 'Deux cents francs.'}, 'Cents prend un s ici.'),
                    ('vrai_faux', 4, {'statement': '400 s’écrit quatre cents.'},
                     {'value': True}, 'Multiplié, et rien derrière.'),
                ],
            ),
            (
                'definition',
                '340 s’écrit trois cent quarante, sans s : quarante suit cent.',
                'nb-340',
                'La tuile 340 et le mot trois cent quarante, une flèche partant de cent vers quarante.',
                [
                    ('simple', 'Cent est bien multiplié par trois, mais quarante vient après : le s tombe.'),
                    ('histoire', 'Le cahier a écrit « trois cents quarante », avec un s de trop. Sa propre règle dit le contraire : ici cent est suivi de quarante, donc pas de s.'),
                ],
                [
                    ('qcm', 1, {'question': '340 s’écrit…',
                                'options': ['trois cent quarante', 'trois cents quarante',
                                            'trois cent quarantes']},
                     {'index': 0}, 'Sans s : quarante suit cent.'),
                    ('qcm', 1, {'question': 'Dans 340, qu’y a-t-il après cent ?',
                                'options': ['quarante', 'rien', 'trois']},
                     {'index': 0}, 'Quarante le suit.'),
                    ('qcm', 2, {'question': 'Lequel est bien écrit ?',
                                'options': ['deux cent dix', 'deux cents dix',
                                            'deux cent dixs', 'deux centes dix']},
                     {'index': 0}, '210 : dix suit cent, donc pas de s.'),
                    ('texte_a_trous', 3, {'text': '340 s’écrit trois {{1}} {{2}}.', 'blanks': 2},
                     {'values': ['cent', 'quarante']}, 'Cent sans s, puis quarante.'),
                    ('vrai_faux', 4, {'statement': 'On écrit cinq cents douze.'},
                     {'value': False}, 'C’est cinq cent douze : douze suit cent.'),
                ],
            ),
            (
                'liste',
                '999 est le plus grand nombre à trois chiffres.',
                'nb-999',
                'Trois tuiles portant 9, 9, 9, et une quatrième tuile barrée derrière elles.',
                [
                    ('simple', 'Neuf centaines, neuf dizaines, neuf unités : on ne peut pas mettre plus.'),
                    ('pas_a_pas', 'Si j’ajoute un à 999, j’obtiens 1000, qui a quatre chiffres. 999 est donc le dernier à trois.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le plus grand nombre à trois chiffres est…',
                                'options': ['999', '100', '990']},
                     {'index': 0}, '999, trois fois neuf.'),
                    ('qcm', 1, {'question': 'Combien de chiffres a 999 ?',
                                'options': ['Trois', 'Deux', 'Neuf']},
                     {'index': 0}, 'Trois chiffres.'),
                    ('qcm', 2, {'question': 'Que vient juste après 999 ?',
                                'options': ['1000', '998', '900', '9910']},
                     {'index': 0}, 'Mille, qui a quatre chiffres.'),
                    ('chronologie', 3, {'question': 'Range ces nombres du plus petit au plus grand.',
                                        'tokens': ['101', '500', '999'],
                                        'consigne': 'Touche les nombres dans l’ordre.'},
                     {'order': [0, 1, 2]}, 'Du premier au dernier de la leçon.'),
                    ('vrai_faux', 4, {'statement': '1000 a trois chiffres.'},
                     {'value': False}, 'Il en a quatre.'),
                ],
            ),
        ],
    ),
    (
        'Le cube', 'Géométrie', '2026-10-14', 14,
        'Le cube est un solide. Il a six faces carrées, huit sommets et douze arêtes.',
        'cu-cube',
        'Un cube en perspective, faces pastel, sommets et arêtes visibles, posé avec une ombre douce.',
        [
            (
                'definition',
                'Le cube est un solide.',
                'cu-solide',
                'Le cube seul, en perspective, avec son ombre portée sur le fond.',
                [
                    ('simple', 'Un solide prend de la place dans l’espace. On peut le tenir dans la main.'),
                    ('analogie', 'Un carré se dessine sur la feuille. Un cube, lui, se pose dessus.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le cube est…',
                                'options': ['un solide', 'une ligne', 'un point']},
                     {'index': 0}, 'C’est un solide.'),
                    ('qcm', 1, {'question': 'Un cube a-t-il une épaisseur ?',
                                'options': ['Oui', 'Non', 'Parfois']},
                     {'index': 0}, 'Il occupe de l’espace.'),
                    ('qcm', 2, {'question': 'Lequel est un solide ?',
                                'options': ['le cube', 'le carré', 'le triangle', 'le cercle']},
                     {'index': 0}, 'Les trois autres sont plats.'),
                    ('association', 3, {'question': 'Relie chaque forme à ce qu’elle est.',
                                        'gauche': ['le cube', 'le carré'],
                                        'droite': ['Un solide', 'Une figure plate']},
                     {'order': [0, 1]}, 'Le cube est en volume, le carré est plat.'),
                    ('vrai_faux', 4, {'statement': 'Le cube est une figure plate.'},
                     {'value': False}, 'C’est un solide.'),
                ],
            ),
            (
                'liste',
                'Le cube a six faces carrées.',
                'cu-faces',
                'Le cube avec ses trois faces visibles teintées et un petit 6 posé à côté.',
                [
                    ('simple', 'Six faces, et toutes les six sont des carrés de la même taille.'),
                    ('visuel', 'On en voit trois à la fois. Les trois autres sont derrière.'),
                ],
                [
                    ('qcm', 1, {'question': 'Combien de faces a le cube ?',
                                'options': ['Six', 'Huit', 'Douze']},
                     {'index': 0}, 'Six faces.'),
                    ('qcm', 1, {'question': 'Les faces du cube sont des…',
                                'options': ['carrés', 'cercles', 'triangles']},
                     {'index': 0}, 'Des carrés.'),
                    ('qcm', 2, {'question': 'Quelle est la forme d’une face du cube ?',
                                'options': ['Un carré', 'Un rectangle long', 'Un triangle', 'Un rond']},
                     {'index': 0}, 'Un carré.'),
                    ('texte_a_trous', 3, {'text': 'Le cube a {{1}} faces {{2}}.', 'blanks': 2},
                     {'values': ['six', 'carrées']}, 'Six faces carrées.'),
                    ('vrai_faux', 4, {'statement': 'Le cube a six faces rondes.'},
                     {'value': False}, 'Elles sont carrées.'),
                ],
            ),
            (
                'liste',
                'Le cube a huit sommets.',
                'cu-sommets',
                'Le cube avec ses huit sommets marqués de pastilles en terre cuite, numérotées.',
                [
                    ('simple', 'Un sommet est un coin. Le cube en a huit : quatre en haut, quatre en bas.'),
                    ('pas_a_pas', 'Je compte les quatre coins du dessus, puis les quatre du dessous. Quatre et quatre font huit.'),
                ],
                [
                    ('qcm', 1, {'question': 'Combien de sommets a le cube ?',
                                'options': ['Huit', 'Six', 'Douze']},
                     {'index': 0}, 'Huit sommets.'),
                    ('qcm', 1, {'question': 'Un sommet est…',
                                'options': ['un coin', 'un côté', 'une face']},
                     {'index': 0}, 'C’est un coin.'),
                    ('qcm', 2, {'question': 'Où se trouvent les sommets du cube ?',
                                'options': ['Aux coins', 'Au milieu des faces',
                                            'Au milieu des arêtes', 'À l’intérieur']},
                     {'index': 0}, 'Aux coins.'),
                    ('chronologie', 3, {'question': 'Range les trois comptes dans l’ordre du cahier.',
                                        'tokens': ['6 faces', '8 sommets', '12 arêtes'],
                                        'consigne': 'Touche-les dans l’ordre de la leçon.'},
                     {'order': [0, 1, 2]}, 'Faces, sommets, arêtes.'),
                    ('vrai_faux', 4, {'statement': 'Le cube a huit sommets.'},
                     {'value': True}, 'Quatre en haut, quatre en bas.'),
                ],
            ),
            (
                'liste',
                'Le cube a douze arêtes.',
                'cu-aretes',
                'Le cube avec ses douze arêtes épaissies en terre cuite, numérotées une à une.',
                [
                    ('simple', 'Une arête est un bord, là où deux faces se rencontrent. Il y en a douze.'),
                    ('pas_a_pas', 'Quatre arêtes en haut, quatre en bas, et quatre debout qui relient les deux. Douze en tout.'),
                ],
                [
                    ('qcm', 1, {'question': 'Combien d’arêtes a le cube ?',
                                'options': ['Douze', 'Huit', 'Six']},
                     {'index': 0}, 'Douze arêtes.'),
                    ('qcm', 1, {'question': 'Une arête est…',
                                'options': ['un bord', 'un coin', 'une face']},
                     {'index': 0}, 'C’est un bord.'),
                    ('qcm', 2, {'question': 'L’arête est la ligne où se rencontrent…',
                                'options': ['deux faces', 'deux cubes',
                                            'deux sommets opposés', 'deux ombres']},
                     {'index': 0}, 'Deux faces voisines.'),
                    ('association', 3, {'question': 'Relie chaque élément à son nombre.',
                                        'gauche': ['les faces', 'les sommets', 'les arêtes'],
                                        'droite': ['Six', 'Huit', 'Douze']},
                     {'order': [0, 1, 2]}, 'Six, huit, douze.'),
                    ('vrai_faux', 4, {'statement': 'Le cube a dix arêtes.'},
                     {'value': False}, 'Il en a douze.'),
                ],
            ),
        ],
    ),
    (
        'Les mesures de grandeurs : les sous-multiples', 'Mesures et grandeurs', '2026-10-15', 15,
        'Pour convertir une mesure de longueur, j’utilise le tableau des sous-multiples : mètre, '
        'décimètre, centimètre, millimètre. 2 m = 200 cm. 120 cm = 1 m 2 dm 0 cm. 3 dm 4 mm = 304 mm.',
        'me-mesures',
        'Le tableau à quatre colonnes m, dm, cm, mm, avec une règle graduée posée dessous.',
        [
            (
                'relation',
                'Pour convertir une mesure, j’utilise le tableau des sous-multiples.',
                'me-tableau',
                'Le tableau vide à quatre colonnes m, dm, cm, mm, une seule case en attente par colonne.',
                [
                    ('simple', 'Une colonne, un chiffre. Le tableau fait le travail à ma place.'),
                    ('pas_a_pas', 'J’écris le nombre en plaçant son dernier chiffre dans la colonne de son unité, puis je lis la colonne que je cherche.'),
                ],
                [
                    ('qcm', 1, {'question': 'Pour convertir, j’utilise…',
                                'options': ['le tableau', 'la gomme', 'le dessin']},
                     {'index': 0}, 'Le tableau des sous-multiples.'),
                    ('qcm', 1, {'question': 'Le tableau sert à…',
                                'options': ['convertir', 'colorier', 'compter les jours']},
                     {'index': 0}, 'À convertir les mesures.'),
                    ('qcm', 2, {'question': 'Que met-on dans une colonne du tableau ?',
                                'options': ['Un seul chiffre', 'Deux chiffres', 'Un mot', 'Un dessin']},
                     {'index': 0}, 'Un chiffre par colonne.'),
                    ('texte_a_trous', 3, {'text': 'Pour convertir j’utilise le {{1}} des {{2}}.', 'blanks': 2},
                     {'values': ['tableau', 'sous-multiples']}, 'Le tableau des sous-multiples.'),
                    ('vrai_faux', 4, {'statement': 'Chaque colonne du tableau reçoit un seul chiffre.'},
                     {'value': True}, 'Un chiffre, une colonne.'),
                ],
            ),
            (
                'definition',
                'Les sous-multiples du mètre sont le décimètre, le centimètre et le millimètre.',
                'me-sous-multiples',
                'Quatre segments pastel de longueurs décroissantes, étiquetés m, dm, cm, mm.',
                [
                    ('simple', 'Trois unités plus petites que le mètre, de la plus grande à la plus petite.'),
                    ('visuel', 'Chaque fois qu’on descend d’une colonne, la mesure est dix fois plus petite.'),
                ],
                [
                    ('qcm', 1, {'question': 'Lequel est le plus petit ?',
                                'options': ['le millimètre', 'le mètre', 'le décimètre']},
                     {'index': 0}, 'Le millimètre.'),
                    ('qcm', 1, {'question': 'dm veut dire…',
                                'options': ['décimètre', 'demi-mètre', 'double mètre']},
                     {'index': 0}, 'Décimètre.'),
                    ('qcm', 2, {'question': 'Lequel est un sous-multiple du mètre ?',
                                'options': ['le centimètre', 'le kilomètre', 'le gramme', 'le litre']},
                     {'index': 0}, 'Le centimètre est plus petit que le mètre.'),
                    ('chronologie', 3, {'question': 'Range ces unités du plus grand au plus petit.',
                                        'tokens': ['m', 'dm', 'cm', 'mm'],
                                        'consigne': 'Touche-les dans l’ordre du tableau.'},
                     {'order': [0, 1, 2, 3]}, 'C’est l’ordre des colonnes.'),
                    ('vrai_faux', 4, {'statement': 'Le mètre est plus petit que le décimètre.'},
                     {'value': False}, 'Le mètre est le plus grand des quatre.'),
                ],
            ),
            (
                'definition',
                '2 m = 200 cm.',
                'me-2m',
                'Le tableau avec 2 en colonne m, puis 0 et 0 qui tombent en dm et cm, et 200 cm écrit dessous.',
                [
                    ('simple', 'Un mètre fait cent centimètres. Deux mètres en font deux cents.'),
                    ('pas_a_pas', 'Je pose le 2 dans la colonne m, je complète jusqu’à la colonne cm avec deux zéros, et je lis 200.'),
                ],
                [
                    ('qcm', 1, {'question': '2 m font…',
                                'options': ['200 cm', '20 cm', '2 cm']},
                     {'index': 0}, 'Deux cents centimètres.'),
                    ('qcm', 1, {'question': '1 m fait…',
                                'options': ['100 cm', '10 cm', '1000 cm']},
                     {'index': 0}, 'Cent centimètres.'),
                    ('qcm', 2, {'question': '3 m font…',
                                'options': ['300 cm', '30 cm', '3 cm', '3000 cm']},
                     {'index': 0}, 'Trois fois cent.'),
                    ('texte_a_trous', 3, {'text': '2 m = {{1}} cm et 1 m = {{2}} cm.', 'blanks': 2},
                     {'values': ['200', '100']}, 'Deux cents, et cent.'),
                    ('vrai_faux', 4, {'statement': '2 m = 20 cm.'},
                     {'value': False}, 'C’est 200 cm.'),
                ],
            ),
            (
                'definition',
                '120 cm = 1 m 2 dm 0 cm.',
                'me-120',
                'Le tableau avec 1, 2, 0 dans les colonnes m, dm, cm, et 120 cm écrit dessous.',
                [
                    ('simple', 'Cent vingt centimètres, c’est un mètre et deux décimètres.'),
                    ('pas_a_pas', 'Je place le dernier chiffre de 120 dans la colonne cm : il reste 1 en m et 2 en dm.'),
                ],
                [
                    ('qcm', 1, {'question': '120 cm font…',
                                'options': ['1 m 2 dm', '1 m 20 dm', '12 m']},
                     {'index': 0}, 'Un mètre et deux décimètres.'),
                    ('qcm', 1, {'question': 'Dans 120 cm, combien de mètres entiers ?',
                                'options': ['Un', 'Deux', 'Zéro']},
                     {'index': 0}, 'Un seul mètre.'),
                    ('qcm', 2, {'question': 'Que reste-t-il après le mètre dans 120 cm ?',
                                'options': ['2 dm', '2 cm', '20 dm', '12 cm']},
                     {'index': 0}, 'Vingt centimètres, donc deux décimètres.'),
                    ('texte_a_trous', 3, {'text': '120 cm = {{1}} m {{2}} dm.', 'blanks': 2},
                     {'values': ['1', '2']}, 'Un mètre, deux décimètres.'),
                    ('vrai_faux', 4, {'statement': '120 cm font plus d’un mètre.'},
                     {'value': True}, 'Un mètre et vingt centimètres.'),
                ],
            ),
            (
                'definition',
                '3 dm 4 mm = 304 mm.',
                'me-304',
                'Le tableau avec 3 en dm, 0 en cm, 4 en mm, et 304 mm écrit dessous.',
                [
                    ('simple', 'Trois décimètres font trois cents millimètres. Avec quatre de plus, 304.'),
                    ('pas_a_pas', 'Je pose 3 en dm et 4 en mm. La colonne cm reste vide : j’y mets un zéro, et je lis 304.'),
                ],
                [
                    ('qcm', 1, {'question': '3 dm 4 mm font…',
                                'options': ['304 mm', '34 mm', '340 mm']},
                     {'index': 0}, 'Trois cent quatre millimètres.'),
                    ('qcm', 1, {'question': '1 dm fait…',
                                'options': ['100 mm', '10 mm', '1000 mm']},
                     {'index': 0}, 'Cent millimètres.'),
                    ('qcm', 2, {'question': '3 dm font…',
                                'options': ['300 mm', '30 mm', '3 mm', '3000 mm']},
                     {'index': 0}, 'Trois fois cent millimètres.'),
                    ('texte_a_trous', 3, {'text': '3 dm 4 mm = {{1}} mm car 3 dm = {{2}} mm.', 'blanks': 2},
                     {'values': ['304', '300']}, 'Trois cents, plus quatre.'),
                    ('vrai_faux', 4, {'statement': '3 dm 4 mm font 34 mm.'},
                     {'value': False}, 'Il manque le zéro des centimètres : 304 mm.'),
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
                'summary': resume, 'illustration': img, 'illustration_prompt': FIGURE + prompt,
                'notions': [
                    {
                        'kind': k, 'statement': p, 'illustration': ni,
                        'illustration_prompt': FIGURE + npr,
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
    chemin = os.path.join(racine, 'app', 'public', 'seed-maths.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    notions = sum(len(l[7]) for l in LECONS)
    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-46s %-20s %-10s %d notions'
              % (titre, chapitre, date or 'sans date', len(ns)))
    print(chemin)
