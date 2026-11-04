# -*- coding: utf-8 -*-
"""
Cinq leçons de mathématiques pour BRAYNE (CM1) — contrôle hebdomadaire du
vendredi 30 octobre et remédiation du mercredi 4 novembre 2026.

Tout vient de son cahier : les conversions du contrôle, les notes de Jores,
les 300 candidats au permis, le champ de Baleng, les 70 moutons, les angles
et les droites du triangle. Les nombres ne sont pas inventés — un problème
dont il reconnaît les chiffres est un problème qu-il a déjà vu corriger.

LA DIFFICULTÉ EST DANS LE CALCUL, PAS DANS LA FORME. Le père a demandé du
simple et du très difficile. Les quatre étapes ne changent pas de forme
pour autant : l-étape 4 reste un choix ou un vrai/faux, parce qu-elle est
chronométrée. Ce qui change, c-est ce qu-il faut faire AVANT de répondre.
À l-étape 1 la réponse est dans l-énoncé ; à l-étape 4 il faut mener deux
ou trois opérations de tête et les mauvaises réponses sont exactement les
résultats des fautes probables — l-oubli d-un zéro, la division par le
mauvais nombre, la somme au lieu du produit.

TROIS FAUTES DU CAHIER, et ce qui en a été fait.

1. Au contrôle du 30 octobre, « 2 hl 5 l » est écrit 250 dl au lieu de
   2 050. La maîtresse a corrigé. La leçon enseigne la colonne : le 2 est
   dans les hectolitres, pas dans les litres, et une case sautée décale
   tout le nombre. Une question de l-étape 4 propose 250 comme fausse
   réponse, parce que c-est SA faute.

2. Le problème de l-épicier porte « 600 F la barre » dans l-énoncé mais
   l-opération est faite à 400 F. Le cahier se contredit, donc on ne peut
   pas le suivre : la leçon retient 400 F, qui est le prix avec lequel le
   résultat corrigé en rouge tombe juste. À vérifier avec la maîtresse.

3. Le partage du champ de Baleng est écrit « 34 500 ÷ 3 = 1 815 00 » avant
   d-être repris à 11 500. Seul 11 500 est enseigné.

Usage :  python work/lecons-brayne-maths-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-brayne-maths-nov.py. '

MATIERE = 'Mathématiques'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'fr'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

MESURES = 'Mesures et grandeurs'
CALCUL = 'Nombres et calculs'
GEOMETRIE = 'Géométrie'

# Ce que le clavier d-un texte à trous sait taper. Pas d-espace : « 2 050 »
# serait impossible, et c-est pour ça que les nombres s-y écrivent collés.
TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü’0123456789-,.')
TAPABLE |= {c.upper() for c in TAPABLE}

LECONS = [
    # ----------------------------------------------------------------- 27
    (
        'Les mesures de capacité', MESURES, '2026-10-30', 27,
        'Les unités de capacité vont du kilolitre au millilitre : kl, hl, dal, l, dl, cl, ml. '
        'Chaque case vaut dix fois la suivante. Pour convertir, on écrit le nombre dans '
        'l’échelle, une case par unité, et on complète avec des zéros jusqu’à l’unité demandée.',
        'bm-cap-couv',
        'Les sept unités de capacité alignées, le litre mis en valeur.',
        [
            ('liste',
             'Les unités de capacité sont, de la plus grande à la plus petite : kl, hl, dal, l, dl, cl, ml.',
             'bm-cap-echelle', 'L’échelle des sept unités, le litre repéré comme unité.',
             [('simple', 'Sept cases, dans l’ordre. Le litre est au milieu : c’est l’unité.'),
              ('pas_a_pas', 'On descend d’une case, on multiplie par dix. On monte d’une case, on divise par dix.'),
              ('visuel', 'Sur la figure, chaque case est une unité, et elles se suivent toujours dans le même ordre.')],
             [('qcm', 1, {'question': 'Quelle unité vient juste après le litre, vers le plus petit ?',
                          'options': ['le décilitre', 'le décalitre', 'le centilitre']},
               {'index': 0}, 'Le décilitre, puis le centilitre, puis le millilitre.'),
              ('vrai_faux', 1, {'statement': 'Le millilitre est la plus petite des unités de l’échelle.'},
               {'value': True}, 'Oui, elle est tout à droite.'),
              ('chronologie', 2, {'question': 'Range ces unités de la plus grande à la plus petite.',
                                  'tokens': ['hl', 'dal', 'l', 'dl']},
               {'order': [0, 1, 2, 3]}, 'Hectolitre, décalitre, litre, décilitre.'),
              ('texte_a_trous', 3, {'text': 'Entre le litre et le centilitre se trouve le {{1}}.', 'blanks': 1},
               {'values': ['décilitre']}, 'Le décilitre.'),
              ('qcm', 4, {'question': 'Combien de millilitres y a-t-il dans un litre ?',
                          'options': ['1 000', '100', '10']},
               {'index': 0}, 'Trois cases plus bas, donc trois zéros : 1 000.')]),

            ('relation', '2 hl 5 l s’écrivent 205 l, c’est-à-dire 2 050 dl.',
             'bm-cap-litre', 'L’échelle avec 2 aux hectolitres, 0 aux décalitres, 5 aux litres, 0 aux décilitres.',
             [('pas_a_pas', 'Le 2 va dans la case hl. Rien aux dal, donc un zéro. Le 5 va dans la case l.'),
              ('simple', 'La case dit la valeur du chiffre. Un chiffre mal placé, et le nombre change.'),
              ('visuel', 'Sur la figure, les deux cases allumées sont hl et dl : c’est entre elles qu’on lit.')],
             [('qcm', 1, {'question': 'Dans quelle case va le 2 de « 2 hl 5 l » ?',
                          'options': ['les hectolitres', 'les litres', 'les décilitres']},
               {'index': 0}, 'Dans les hectolitres.'),
              ('vrai_faux', 1, {'statement': '2 hl 5 l font 205 l.'},
               {'value': True}, 'Oui : 200 l et 5 l.'),
              ('qcm', 2, {'question': 'Combien de décilitres font 2 hl 5 l ?',
                          'options': ['2 050 dl', '250 dl', '25 dl']},
               {'index': 0}, 'On descend d’une case depuis les litres : 205 devient 2 050.'),
              ('texte_a_trous', 3, {'text': '2 hl 5 l = {{1}} dl.', 'blanks': 1},
               {'values': ['2050']}, 'Deux mille cinquante décilitres.'),
              ('vrai_faux', 4, {'statement': '2 hl 5 l font 250 dl.'},
               {'value': False}, 'Non. 250 oublie la case des décalitres. La réponse est 2 050 dl.')]),

            ('relation', '120 ml font 12 cl : en remontant d’une case, on enlève un zéro.',
             'bm-cap-petites', 'L’échelle avec 1 aux décilitres, 2 aux centilitres, 0 aux millilitres.',
             [('simple', 'Vers la gauche on enlève un zéro, vers la droite on en ajoute un.'),
              ('pas_a_pas', '120 ml. Une case à gauche : 12 cl. Encore une : 1,2 dl.')],
             [('qcm', 1, {'question': 'Combien de centilitres font 120 ml ?',
                          'options': ['12 cl', '120 cl', '1 200 cl']},
               {'index': 0}, 'On remonte d’une case, donc on enlève un zéro.'),
              ('vrai_faux', 1, {'statement': 'Pour passer des millilitres aux centilitres, on enlève un zéro.'},
               {'value': True}, 'Oui, une case vers la gauche.'),
              ('qcm', 2, {'question': 'Combien de millilitres font 3 cl ?',
                          'options': ['30 ml', '3 ml', '300 ml']},
               {'index': 0}, 'Une case vers la droite ajoute un zéro.'),
              ('texte_a_trous', 3, {'text': '120 ml = {{1}} cl.', 'blanks': 1},
               {'values': ['12']}, 'Douze centilitres.'),
              ('qcm', 4, {'question': 'Combien de millilitres font 2 dl 5 cl ?',
                          'options': ['250 ml', '25 ml', '205 ml']},
               {'index': 0}, '2 dl 5 cl font 25 cl, donc 250 ml.')]),

            ('relation', '560 l et 440 l font ensemble 1 000 l, c’est-à-dire 100 dal.',
             'bm-cap-somme', 'L’addition des deux quantités du fût, puis sa conversion en décalitres.',
             [('pas_a_pas', 'On additionne d’abord, on convertit ensuite. Jamais l’inverse.'),
              ('simple', 'Mille litres, c’est cent décalitres : une case plus haut, un zéro en moins.')],
             [('qcm', 1, {'question': 'Un fût contient 560 l. On y verse 440 l. Combien contient-il ?',
                          'options': ['1 000 l', '900 l', '1 100 l']},
               {'index': 0}, '560 + 440 = 1 000.'),
              ('vrai_faux', 1, {'statement': '1 000 l font 100 dal.'},
               {'value': True}, 'Oui, une case plus haut.'),
              ('qcm', 2, {'question': 'Combien de décalitres font 1 000 l ?',
                          'options': ['100 dal', '10 dal', '1 000 dal']},
               {'index': 0}, 'Cent décalitres.'),
              ('texte_a_trous', 3,
               {'text': 'Dans la réserve de l’école, un fût contient déjà 560 l d’huile. '
                        'Le magasinier y verse encore 440 l apportés le matin même. Quelle '
                        'quantité de liquide le fût contient-il maintenant ? Donne ta '
                        'réponse en litres. Le fût contient {{1}} l.', 'blanks': 1},
               {'values': ['1000']}, '560 + 440 = 1 000 litres.'),
              ('qcm', 4, {'question': 'Un fût de 2 hl est rempli de 85 l. Combien de litres manque-t-il ?',
                          'options': ['115 l', '15 l', '185 l']},
               {'index': 0}, '2 hl font 200 l, et 200 − 85 = 115.')]),

            ('relation', '5 hl 28 l font 528 l, c’est-à-dire 528 000 ml.',
             'bm-cap-zero', 'L’échelle avec 5, 2, 8 puis trois zéros jusqu’aux millilitres.',
             [('pas_a_pas', '5 aux hl, 2 aux dal, 8 aux l. Puis trois cases jusqu’aux ml : trois zéros.'),
              ('simple', 'Chaque case franchie vers la droite ajoute exactement un zéro.')],
             [('qcm', 1, {'question': 'Combien de litres font 5 hl 28 l ?',
                          'options': ['528 l', '5 028 l', '58 l']},
               {'index': 0}, '500 l et 28 l.'),
              ('vrai_faux', 1, {'statement': '5 hl 28 l font 528 000 ml.'},
               {'value': True}, 'Oui : trois cases, donc trois zéros.'),
              ('qcm', 2, {'question': 'Combien de zéros ajoute-t-on pour passer des litres aux millilitres ?',
                          'options': ['trois', 'deux', 'un']},
               {'index': 0}, 'l, dl, cl, ml : trois cases.'),
              ('texte_a_trous', 3, {'text': '5 hl 28 l = {{1}} l.', 'blanks': 1},
               {'values': ['528']}, 'Cinq cent vingt-huit litres.'),
              ('qcm', 4, {'question': 'Combien de centilitres font 3 dal 6 dl ?',
                          'options': ['3 006 cl', '36 cl', '360 cl']},
               {'index': 0}, '3 dal font 30 l, plus 6 dl : 30,6 l, soit 3 006 cl.')]),
        ],
    ),

    # ----------------------------------------------------------------- 28
    (
        'La moyenne', CALCUL, '2026-11-04', 28,
        'La moyenne de plusieurs notes s’obtient en trois gestes : on additionne toutes les '
        'notes, on compte combien il y en a, puis on divise la somme par ce nombre. '
        'Avec 15, 18, 10, 12 et 10, la somme fait 65 et la moyenne 13.',
        'bm-moy-couv',
        'Les cinq notes de Jores alignées, et la moyenne au-dessous.',
        [
            ('relation', 'La moyenne de 15, 18, 10, 12 et 10 est 13.',
             'bm-moy-table', 'Les cinq notes, leur somme, et la division qui donne la moyenne.',
             [('simple', 'La moyenne est la note que Jores aurait eue partout si toutes étaient pareilles.'),
              ('pas_a_pas', '15 + 18 + 10 + 12 + 10 = 65. Cinq notes. 65 ÷ 5 = 13.'),
              ('visuel', 'Sur la figure, les cinq notes sont en haut et la moyenne en bas.')],
             [('qcm', 1, {'question': 'Quelle est la moyenne de 15, 18, 10, 12 et 10 ?',
                          'options': ['13', '15', '11']},
               {'index': 0}, '65 divisé par 5.'),
              ('vrai_faux', 1, {'statement': 'La somme des notes 15, 18, 10, 12 et 10 est 65.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Par combien divise-t-on la somme de ces cinq notes ?',
                          'options': ['par 5', 'par 65', 'par 20']},
               {'index': 0}, 'Par le nombre de notes, donc par 5.'),
              ('texte_a_trous', 3,
               {'text': 'Lors d’une évaluation, Jores a eu les notes suivantes : 15 sur 20, '
                        '18 sur 20, 10 sur 20, 12 sur 20 et 10 sur 20. Calcule sa note '
                        'moyenne. La somme fait {{1}}, et sa moyenne est de {{2}}.', 'blanks': 2},
               {'values': ['65', '13']}, 'La somme fait 65, et 65 ÷ 5 = 13.'),
              ('qcm', 4, {'question': 'Un élève a 12, 14 et 16. Quelle est sa moyenne ?',
                          'options': ['14', '42', '13']},
               {'index': 0}, '12 + 14 + 16 = 42, et 42 ÷ 3 = 14.')]),

            ('liste',
             'Pour trouver une moyenne : additionner les notes, compter combien il y en a, puis diviser.',
             'bm-moy-somme', 'Les trois gestes de la moyenne, l’un sous l’autre.',
             [('pas_a_pas', 'Additionner. Compter. Diviser. Toujours dans cet ordre.'),
              ('simple', 'L’erreur la plus fréquente est de diviser par la note la plus grande au lieu du nombre de notes.')],
             [('qcm', 1, {'question': 'Que fait-on en premier pour trouver une moyenne ?',
                          'options': ['on additionne les notes', 'on divise', 'on cherche la plus grande']},
               {'index': 0}, 'On additionne d’abord.'),
              ('vrai_faux', 1, {'statement': 'On divise la somme par le nombre de notes.'},
               {'value': True}, 'Oui.'),
              ('chronologie', 2, {'question': 'Range les trois gestes dans l’ordre.',
                                  'tokens': ['additionner les notes', 'compter les notes', 'diviser']},
               {'order': [0, 1, 2]}, 'Additionner, compter, diviser.'),
              ('texte_a_trous', 3, {'text': 'On divise la somme par le {{1}} de notes.', 'blanks': 1},
               {'values': ['nombre']}, 'Par le nombre de notes.'),
              ('vrai_faux', 4, {'statement': 'Pour la moyenne de 10 et 20, on divise 30 par 20.'},
               {'value': False}, 'Non : par 2, le nombre de notes. La moyenne est 15.')]),

            ('relation',
             'Si le total des cinq notes est 70 et que quatre d’entre elles font 57, la cinquième est 13.',
             'bm-moy-manque', 'Le total, les notes connues, et la soustraction qui donne celle qui manque.',
             [('pas_a_pas', 'On additionne les notes connues, puis on les retire du total.'),
              ('simple', 'Chercher une note qui manque, c’est une soustraction, pas une division.')],
             [('qcm', 1, {'question': 'Le total fait 70 et quatre notes font 57. Quelle est la cinquième ?',
                          'options': ['13', '17', '127']},
               {'index': 0}, '70 − 57 = 13.'),
              ('vrai_faux', 1, {'statement': 'Pour trouver la note qui manque, on fait une soustraction.'},
               {'value': True}, 'Oui : le total moins les notes connues.'),
              ('qcm', 2, {'question': 'Dictée 14, maths 12, sciences 15, anglais 16. Combien font-elles ?',
                          'options': ['57', '47', '67']},
               {'index': 0}, '14 + 12 + 15 + 16 = 57.'),
              ('texte_a_trous', 3,
               {'text': 'Au bulletin, le total des cinq notes est 70. La dictée fait 14, '
                        'les maths 12, les sciences 15 et l’anglais 16. La note de TIC a été '
                        'effacée. Les quatre notes connues font {{1}}, donc celle de TIC '
                        'vaut {{2}}.', 'blanks': 2},
               {'values': ['57', '13']}, '14 + 12 + 15 + 16 = 57, et 70 − 57 = 13.'),
              ('qcm', 4, {'question': 'Quatre notes font 48. Le total doit faire 62. Que vaut la cinquième ?',
                          'options': ['14', '110', '12']},
               {'index': 0}, '62 − 48 = 14.')]),

            ('relation', 'La moyenne de 14, 12, 15, 13 et 16 est 14, car leur somme est 70.',
             'bm-moy-sens', 'Les cinq notes du bulletin, leur somme et leur moyenne.',
             [('pas_a_pas', '14 + 12 + 15 + 13 + 16 = 70. Cinq notes. 70 ÷ 5 = 14.'),
              ('analogie', 'La moyenne tombe toujours entre la plus petite note et la plus grande.')],
             [('qcm', 1, {'question': 'Quelle est la moyenne de 14, 12, 15, 13 et 16 ?',
                          'options': ['14', '70', '15']},
               {'index': 0}, '70 ÷ 5 = 14.'),
              ('vrai_faux', 1, {'statement': 'Une moyenne peut être plus grande que la plus grande des notes.'},
               {'value': False}, 'Non. Elle tombe toujours entre la plus petite et la plus grande.'),
              ('qcm', 2, {'question': 'Combien font 14 + 12 + 15 + 13 + 16 ?',
                          'options': ['70', '60', '80']},
               {'index': 0}, 'Soixante-dix.'),
              ('texte_a_trous', 3, {'text': '70 ÷ 5 = {{1}}.', 'blanks': 1},
               {'values': ['14']}, 'Quatorze.'),
              ('qcm', 4, {'question': 'Six notes ont pour moyenne 12. Combien fait leur somme ?',
                          'options': ['72', '18', '2']},
               {'index': 0}, 'La moyenne fois le nombre de notes : 12 × 6 = 72.')]),
        ],
    ),

    # ----------------------------------------------------------------- 29
    (
        'Le pourcentage', CALCUL, '2026-11-04', 29,
        'Un pourcentage dit combien il y en aurait sur cent. On le calcule en multipliant '
        'l’effectif par 100 puis en divisant par l’effectif total. Sur 300 candidats, '
        '240 reçus font 80 % de réussite et 60 recalés font 20 % d’échec.',
        'bm-pc-couv',
        'Une rangée de carrés dont la plupart sont colorés, et le pourcentage au-dessous.',
        [
            ('definition', 'Un pourcentage dit combien il y en aurait si le total était cent.',
             'bm-pc-barre', 'Cent carrés, dont quatre-vingts colorés.',
             [('simple', 'Pour cent, cela veut dire : sur cent.'),
              ('visuel', 'La figure a cent carrés. Il suffit de compter ceux qui sont colorés.'),
              ('analogie', '240 sur 300 ne se sent pas. 80 carrés sur 100 se voient.')],
             [('qcm', 1, {'question': 'Que veut dire « pour cent » ?',
                          'options': ['sur cent', 'cent fois', 'plus de cent']},
               {'index': 0}, 'Sur cent.'),
              ('vrai_faux', 1, {'statement': 'Un pourcentage ramène toujours le total à cent.'},
               {'value': True}, 'Oui, c’est à quoi il sert.'),
              ('qcm', 2, {'question': 'Sur la figure, 80 carrés sur 100 sont colorés. Cela fait…',
                          'options': ['80 %', '8 %', '800 %']},
               {'index': 0}, '80 pour cent.'),
              ('texte_a_trous', 3, {'text': 'Un pourcentage dit combien il y en aurait sur {{1}}.', 'blanks': 1},
               {'values': ['cent']}, 'Sur cent.'),
              ('vrai_faux', 4, {'statement': '50 élèves sur 200 font 50 % de l’effectif.'},
               {'value': False}, 'Non : 50 × 100 ÷ 200 = 25 %.')]),

            ('relation', 'Le pourcentage s’obtient en multipliant l’effectif par 100 puis en divisant par le total.',
             'bm-pc-formule', 'La règle écrite en trois lignes : multiplier, diviser, lire le résultat.',
             [('pas_a_pas', 'On multiplie d’abord par 100, on divise ensuite par le total.'),
              ('simple', 'L’effectif total passe toujours en bas, jamais en haut.')],
             [('qcm', 1, {'question': 'Par combien multiplie-t-on l’effectif pour trouver un pourcentage ?',
                          'options': ['par 100', 'par 10', 'par le total']},
               {'index': 0}, 'Par cent.'),
              ('vrai_faux', 1, {'statement': 'On divise par l’effectif total.'},
               {'value': True}, 'Oui, le total passe en bas.'),
              ('qcm', 2, {'question': 'Sur 300 candidats, 240 sont reçus. Quel calcul donne le pourcentage ?',
                          'options': ['240 × 100 ÷ 300', '300 × 100 ÷ 240', '240 ÷ 300 ÷ 100']},
               {'index': 0}, 'L’effectif reçu fois cent, divisé par le total.'),
              ('texte_a_trous', 3,
               {'text': 'Sur 300 candidats qui se sont présentés à l’examen du permis de '
                        'conduire, 240 ont réussi l’épreuve et tous les autres ont été '
                        'recalés. Quel est le pourcentage de réussite à cet examen ? '
                        'Le pourcentage de réussite est de {{1}} %.', 'blanks': 1},
               {'values': ['80']}, '240 × 100 ÷ 300 = 80.'),
              ('qcm', 4, {'question': 'Sur 250 élèves, 150 sont reçus. Quel est le pourcentage de réussite ?',
                          'options': ['60 %', '40 %', '15 %']},
               {'index': 0}, '150 × 100 ÷ 250 = 60.')]),

            ('relation', 'Sur 300 candidats, les 60 recalés font 20 % d’échec.',
             'bm-pc-echec', 'Cent carrés, dont vingt colorés.',
             [('pas_a_pas', '60 × 100 = 6 000, et 6 000 ÷ 300 = 20.'),
              ('simple', 'L’échec se calcule exactement comme la réussite, avec l’autre effectif.')],
             [('qcm', 1, {'question': 'Sur 300 candidats, 60 sont recalés. Quel est le pourcentage d’échec ?',
                          'options': ['20 %', '60 %', '6 %']},
               {'index': 0}, '60 × 100 ÷ 300 = 20.'),
              ('vrai_faux', 1, {'statement': 'Sur 300 candidats dont 240 reçus, 60 ont échoué.'},
               {'value': True}, 'Oui : 300 − 240 = 60.'),
              ('qcm', 2, {'question': 'Combien font 60 × 100 ?',
                          'options': ['6 000', '600', '60 000']},
               {'index': 0}, 'Six mille.'),
              ('texte_a_trous', 3, {'text': '6 000 ÷ 300 = {{1}}.', 'blanks': 1},
               {'values': ['20']}, 'Vingt pour cent.'),
              ('qcm', 4, {'question': 'Sur 400 candidats, 320 réussissent. Quel est le pourcentage d’échec ?',
                          'options': ['20 %', '80 %', '8 %']},
               {'index': 0}, '400 − 320 = 80, et 80 × 100 ÷ 400 = 20.')]),

            ('relation', 'La réussite et l’échec font toujours 100 % ensemble.',
             'bm-pc-cent', 'Les deux pourcentages et leur total, qui fait cent.',
             [('simple', 'Chacun est soit reçu, soit recalé. Les deux parts remplissent le tout.'),
              ('pas_a_pas', 'Si tu connais l’un, tu trouves l’autre : cent moins le premier.')],
             [('qcm', 1, {'question': 'La réussite est de 80 %. Quel est le pourcentage d’échec ?',
                          'options': ['20 %', '80 %', '100 %']},
               {'index': 0}, '100 − 80 = 20.'),
              ('vrai_faux', 1, {'statement': 'La réussite et l’échec font 100 % ensemble.'},
               {'value': True}, 'Oui, il n’y a pas de troisième cas.'),
              ('qcm', 2, {'question': 'La réussite est de 75 %. Quel est l’échec ?',
                          'options': ['25 %', '75 %', '50 %']},
               {'index': 0}, '100 − 75 = 25.'),
              ('texte_a_trous', 3, {'text': 'Si la réussite est de 20 %, l’échec est de {{1}} %.', 'blanks': 1},
               {'values': ['80']}, 'Quatre-vingts.'),
              ('vrai_faux', 4, {'statement': 'Une classe peut avoir 60 % de réussite et 50 % d’échec.'},
               {'value': False}, 'Non : les deux feraient 110 %, ce qui est impossible.')]),

            ('relation', 'À Bangang, 600 reçus sur 800 candidats font 75 % de réussite.',
             'bm-pc-autre', 'Cent carrés, dont soixante-quinze colorés.',
             [('pas_a_pas', '600 × 100 = 60 000, et 60 000 ÷ 800 = 75.'),
              ('simple', 'Trois élèves sur quatre, cela fait bien soixante-quinze sur cent.')],
             [('qcm', 1, {'question': 'Sur 800 candidats, 600 réussissent. Quel est le pourcentage ?',
                          'options': ['75 %', '60 %', '80 %']},
               {'index': 0}, '600 × 100 ÷ 800 = 75.'),
              ('vrai_faux', 1, {'statement': 'À Bangang, 200 candidats ont été recalés.'},
               {'value': True}, 'Oui : 800 − 600 = 200.'),
              ('qcm', 2, {'question': 'Quel est le pourcentage d’échec à Bangang ?',
                          'options': ['25 %', '20 %', '75 %']},
               {'index': 0}, '200 × 100 ÷ 800 = 25.'),
              ('texte_a_trous', 3,
               {'text': 'L’école publique de Bangang a présenté 800 candidats au concours '
                        'd’entrée en sixième. À la publication des résultats, 600 ont réussi '
                        'et tous les autres ont été recalés. Calcule le pourcentage de '
                        'réussite, puis celui d’échec. La réussite est de {{1}} %, et '
                        'l’échec de {{2}} %.', 'blanks': 2},
               {'values': ['75', '25']}, '600 × 100 ÷ 800 = 75, et 100 − 75 = 25.'),
              ('qcm', 4, {'question': 'Une école a 90 % de réussite sur 200 candidats. Combien ont réussi ?',
                          'options': ['180', '90', '110']},
               {'index': 0}, '200 × 90 ÷ 100 = 180.')]),
        ],
    ),

    # ----------------------------------------------------------------- 30
    (
        'Les problèmes', CALCUL, '2026-11-04', 30,
        'Un problème se résout en quatre temps : lire ce qu’on cherche, poser l’opération, '
        'calculer, puis écrire la phrase-réponse. Partager, acheter, peser : chaque situation '
        'a son opération, et c’est la lecture de l’énoncé qui la désigne.',
        'bm-pb-couv',
        'Les trois gains du champ de Baleng, chacun sur sa carte.',
        [
            ('liste',
             'Un problème se fait en quatre temps : lire ce qu’on cherche, poser, calculer, répondre.',
             'bm-pb-etapes', 'Les quatre temps du problème, numérotés.',
             [('pas_a_pas', 'D’abord ce qu’on cherche. Ensuite seulement l’opération.'),
              ('simple', 'La phrase-réponse n’est pas une politesse : elle oblige à vérifier qu’on a répondu à la question posée.')],
             [('qcm', 1, {'question': 'Que fait-on en premier devant un problème ?',
                          'options': ['lire ce qu’on cherche', 'poser l’opération', 'calculer']},
               {'index': 0}, 'On lit d’abord ce qu’on cherche.'),
              ('vrai_faux', 1, {'statement': 'La phrase-réponse s’écrit en dernier.'},
               {'value': True}, 'Oui, après le calcul.'),
              ('chronologie', 2, {'question': 'Range les quatre temps du problème.',
                                  'tokens': ['lire', 'poser', 'calculer', 'répondre']},
               {'order': [0, 1, 2, 3]}, 'Lire, poser, calculer, répondre.'),
              ('texte_a_trous', 3,
               {'text': 'Un maçon construit le mur d’une case. Il pose 125 briques chaque '
                        'jour et il travaille pendant 8 jours de suite. Avant de calculer, '
                        'demande-toi ce qu’on cherche : le nombre total de briques posées. '
                        'Il en a posé {{1}} en tout.', 'blanks': 1},
               {'values': ['1000']}, '125 × 8 = 1 000 briques.'),
              ('qcm', 4, {'question': 'Un problème demande un partage équitable. Quelle opération ?',
                          'options': ['une division', 'une addition', 'une multiplication']},
               {'index': 0}, 'Partager également, c’est diviser.')]),

            ('relation', 'Les gains du champ de Baleng — 7 500 F, 6 000 F et 21 000 F — font 34 500 F.',
             'bm-pb-partage', 'Les trois gains et leur total.',
             [('pas_a_pas', '7 500 + 6 000 = 13 500. Puis 13 500 + 21 000 = 34 500.'),
              ('simple', 'Avant de partager, il faut savoir ce qu’on partage : on additionne d’abord.')],
             [('qcm', 1, {'question': 'Combien font 7 500 F, 6 000 F et 21 000 F ensemble ?',
                          'options': ['34 500 F', '33 500 F', '35 400 F']},
               {'index': 0}, 'Trente-quatre mille cinq cents francs.'),
              ('vrai_faux', 1, {'statement': 'Pour connaître le gain total, on additionne les trois récoltes.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Combien font 7 500 + 6 000 ?',
                          'options': ['13 500', '12 500', '14 500']},
               {'index': 0}, 'Treize mille cinq cents.'),
              ('texte_a_trous', 3,
               {'text': 'À Baleng, trois femmes cultivent ensemble un champ communautaire. '
                        'Cette année, les arachides ont rapporté 7 500 F, le maïs 6 000 F et '
                        'les pistaches 21 000 F. Quel est le gain total du champ ? '
                        'Le gain total est de {{1}} F.', 'blanks': 1},
               {'values': ['34500']}, '7 500 + 6 000 + 21 000 = 34 500 F.'),
              ('qcm', 4, {'question': 'Les pistaches rapportent le double du maïs. Le maïs fait 6 000 F. Et elles ?',
                          'options': ['12 000 F', '21 000 F', '3 000 F']},
               {'index': 0}, 'Le double de 6 000, donc 12 000 F.')]),

            ('relation', '34 500 F partagés équitablement entre 3 femmes donnent 11 500 F à chacune.',
             'bm-pb-division', 'La somme à partager, le nombre de parts, et la part de chacune.',
             [('pas_a_pas', '34 500 ÷ 3. Trois dans 34, onze fois. Il reste 1. On abaisse le 5…'),
              ('simple', 'Équitablement veut dire : des parts égales. C’est une division.'),
              ('analogie', 'Pour vérifier, on remonte : 11 500 × 3 doit redonner 34 500.')],
             [('qcm', 1, {'question': 'Que signifie partager équitablement ?',
                          'options': ['en parts égales', 'au hasard', 'en donnant plus à l’aînée']},
               {'index': 0}, 'En parts égales.'),
              ('vrai_faux', 1, {'statement': '34 500 F partagés entre 3 donnent 11 500 F chacune.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Quelle opération partage 34 500 F entre 3 femmes ?',
                          'options': ['34 500 ÷ 3', '34 500 × 3', '34 500 − 3']},
               {'index': 0}, 'Une division.'),
              ('texte_a_trous', 3,
               {'text': 'Les trois femmes de Baleng ont gagné 34 500 F en tout avec leur '
                        'champ. Elles décident de partager cette somme équitablement entre '
                        'elles. Quelle somme aura chacune ? Chacune aura {{1}} F.', 'blanks': 1},
               {'values': ['11500']}, '34 500 ÷ 3 = 11 500 F pour chacune.'),
              ('qcm', 4, {'question': 'Si elles étaient 5 au lieu de 3, combien recevrait chacune ?',
                          'options': ['6 900 F', '11 500 F', '8 625 F']},
               {'index': 0}, '34 500 ÷ 5 = 6 900 F.')]),

            ('relation', '28 barres à 400 F et 15 kg de riz à 200 F font 14 200 F en tout.',
             'bm-pb-achat', 'Les deux achats, chacun avec son produit, et la somme reçue.',
             [('pas_a_pas', '28 × 400 = 11 200. 15 × 200 = 3 000. 11 200 + 3 000 = 14 200.'),
              ('simple', 'Un prix à l’unité et une quantité : c’est une multiplication, jamais une addition.')],
             [('qcm', 1, {'question': 'Combien coûtent 28 barres de chocolat à 400 F la barre ?',
                          'options': ['11 200 F', '10 200 F', '1 120 F']},
               {'index': 0}, '28 × 400 = 11 200.'),
              ('vrai_faux', 1, {'statement': '15 kg de riz à 200 F le kilo coûtent 3 000 F.'},
               {'value': True}, 'Oui : 15 × 200.'),
              ('qcm', 2, {'question': 'Quelle opération donne le prix de 15 kg de riz à 200 F le kg ?',
                          'options': ['15 × 200', '15 + 200', '200 ÷ 15']},
               {'index': 0}, 'Une multiplication.'),
              ('texte_a_trous', 3,
               {'text': 'Un épicier a vendu 28 barres de chocolat à 400 F la barre, puis '
                        '15 kg de riz à 200 F le kilo. Quelle somme a-t-il reçue en tout ? '
                        'Le chocolat rapporte {{1}} F, et il a reçu {{2}} F en tout.',
                'blanks': 2},
               {'values': ['11200', '14200']},
               '28 × 400 = 11 200, plus 15 × 200 = 3 000, donc 14 200 F.'),
              ('qcm', 4, {'question': 'L’épicier rend la monnaie sur 20 000 F. Combien rend-il ?',
                          'options': ['5 800 F', '6 800 F', '4 200 F']},
               {'index': 0}, '20 000 − 14 200 = 5 800 F.')]),

            ('relation', '70 moutons pesant chacun 75 kg pèsent ensemble 5 250 kg.',
             'bm-pb-masse', 'Le nombre de moutons, la masse de chacun, et la masse totale.',
             [('pas_a_pas', '70 × 75. Sept fois soixante-quinze font 525, et on ajoute le zéro : 5 250.'),
              ('simple', 'Même masse pour chacun et plusieurs bêtes : on multiplie.')],
             [('qcm', 1, {'question': 'Quelle est la masse de 70 moutons de 75 kg chacun ?',
                          'options': ['5 250 kg', '525 kg', '145 kg']},
               {'index': 0}, '70 × 75 = 5 250.'),
              ('vrai_faux', 1, {'statement': 'Pour trouver la masse totale, on multiplie.'},
               {'value': True}, 'Oui, car tous pèsent la même chose.'),
              ('qcm', 2, {'question': 'Combien font 7 × 75 ?',
                          'options': ['525', '515', '535']},
               {'index': 0}, 'Cinq cent vingt-cinq.'),
              ('texte_a_trous', 3,
               {'text': 'Une camionnette emmène des moutons au marché. Elle en charge 70, '
                        'et chacun de ces moutons pèse 75 kg. Calcule la masse totale des '
                        'moutons qu’elle transporte, puis donne cette masse en kilogrammes. '
                        'La masse totale est de {{1}} kg.', 'blanks': 1},
               {'values': ['5250']}, '70 × 75 = 5 250 kg.'),
              ('qcm', 4, {'question': 'La camionnette porte 6 tonnes au plus. Peut-elle prendre les 70 moutons ?',
                          'options': ['oui, 5 250 kg tiennent', 'non, c’est trop lourd',
                                      'non, il faut deux voyages']},
               {'index': 0}, '6 tonnes font 6 000 kg, et 5 250 kg y tiennent.')]),
        ],
    ),

    # ----------------------------------------------------------------- 31
    (
        'Les angles et les droites du triangle', GEOMETRIE, '2026-11-04', 31,
        'Un angle aigu mesure moins de 90°, un angle droit exactement 90°, un angle obtus plus '
        'de 90°, et un angle plat 180°. Dans un triangle, la médiane va d’un sommet au milieu '
        'du côté opposé, tandis que la hauteur y tombe à angle droit.',
        'bm-geo-couv',
        'Les quatre sortes d’angles dessinées à leur vraie mesure.',
        [
            ('definition', 'Un angle aigu mesure moins de 90°.',
             'bm-geo-aigu', 'Un angle de 45 degrés, nommé et mesuré.',
             [('simple', 'Aigu veut dire pointu : ses deux côtés sont serrés.'),
              ('visuel', 'Sur la figure, l’ouverture est plus petite que le coin d’une feuille.')],
             [('qcm', 1, {'question': 'Que mesure un angle aigu ?',
                          'options': ['moins de 90°', 'exactement 90°', 'plus de 90°']},
               {'index': 0}, 'Moins de quatre-vingt-dix degrés.'),
              ('vrai_faux', 1, {'statement': 'Un angle de 45° est un angle aigu.'},
               {'value': True}, 'Oui, 45 est plus petit que 90.'),
              ('qcm', 2, {'question': 'Lequel de ces angles est aigu ?',
                          'options': ['30°', '95°', '180°']},
               {'index': 0}, '30° est plus petit que 90°.'),
              ('texte_a_trous', 3, {'text': 'Un angle aigu mesure moins de {{1}} degrés.', 'blanks': 1},
               {'values': ['90']}, 'Quatre-vingt-dix.'),
              ('vrai_faux', 4, {'statement': 'Un angle de 89° est un angle droit.'},
               {'value': False}, 'Non. 89° est aigu : il manque un degré.')]),

            ('definition', 'Un angle droit mesure exactement 90°.',
             'bm-geo-droit', 'Un angle de 90 degrés, marqué par son petit carré.',
             [('simple', 'C’est le coin d’une feuille, d’une table, d’une porte.'),
              ('visuel', 'On le reconnaît au petit carré qu’on dessine dans le coin.')],
             [('qcm', 1, {'question': 'Que mesure un angle droit ?',
                          'options': ['90°', '45°', '180°']},
               {'index': 0}, 'Exactement quatre-vingt-dix degrés.'),
              ('vrai_faux', 1, {'statement': 'Le coin d’une feuille est un angle droit.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Comment marque-t-on un angle droit sur un dessin ?',
                          'options': ['par un petit carré', 'par une flèche', 'par un point']},
               {'index': 0}, 'Par un petit carré dans le coin.'),
              ('texte_a_trous', 3, {'text': 'Un angle droit mesure {{1}} degrés.', 'blanks': 1},
               {'values': ['90']}, 'Quatre-vingt-dix.'),
              ('qcm', 4, {'question': 'Combien mesure la moitié d’un angle droit ?',
                          'options': ['45°', '180°', '90°']},
               {'index': 0}, '90 ÷ 2 = 45°. C’est ce que trace la bissectrice.')]),

            ('definition', 'Un angle obtus mesure plus de 90° et moins de 180°.',
             'bm-geo-obtus', 'Un angle de 130 degrés, nommé et mesuré.',
             [('simple', 'Plus ouvert que le coin d’une feuille, mais pas encore tout plat.'),
              ('pas_a_pas', 'Compare toujours à 90°. Au-dessus, c’est obtus. En dessous, c’est aigu.')],
             [('qcm', 1, {'question': 'Que mesure un angle obtus ?',
                          'options': ['plus de 90°', 'moins de 90°', 'exactement 180°']},
               {'index': 0}, 'Plus de quatre-vingt-dix degrés.'),
              ('vrai_faux', 1, {'statement': 'Un angle de 130° est obtus.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Lequel de ces angles est obtus ?',
                          'options': ['120°', '60°', '90°']},
               {'index': 0}, '120° est plus grand que 90° et plus petit que 180°.'),
              ('texte_a_trous', 3, {'text': 'Un angle obtus mesure plus de 90 et moins de {{1}} degrés.',
                                    'blanks': 1},
               {'values': ['180']}, 'Cent quatre-vingts.'),
              ('qcm', 4, {'question': 'Un angle mesure 175°. Comment s’appelle-t-il ?',
                          'options': ['obtus', 'plat', 'droit']},
               {'index': 0}, 'Obtus : il est très ouvert, mais pas encore plat.')]),

            ('definition', 'Un angle plat mesure 180° : ses deux côtés forment une droite.',
             'bm-geo-plat', 'Un angle de 180 degrés, dont les deux côtés sont alignés.',
             [('simple', 'Les deux côtés sont dans le prolongement l’un de l’autre : cela fait une ligne droite.'),
              ('pas_a_pas', 'Un angle plat vaut deux angles droits mis bout à bout.')],
             [('qcm', 1, {'question': 'Que mesure un angle plat ?',
                          'options': ['180°', '90°', '360°']},
               {'index': 0}, 'Cent quatre-vingts degrés.'),
              ('vrai_faux', 1, {'statement': 'Les deux côtés d’un angle plat forment une droite.'},
               {'value': True}, 'Oui.'),
              ('chronologie', 2, {'question': 'Range ces angles du plus petit au plus grand.',
                                  'tokens': ['aigu', 'droit', 'obtus', 'plat']},
               {'order': [0, 1, 2, 3]}, 'Aigu, droit, obtus, plat.'),
              ('texte_a_trous', 3, {'text': 'Un angle plat mesure {{1}} degrés.', 'blanks': 1},
               {'values': ['180']}, 'Cent quatre-vingts.'),
              ('qcm', 4, {'question': 'Combien d’angles droits faut-il pour faire un angle plat ?',
                          'options': ['deux', 'trois', 'quatre']},
               {'index': 0}, '90 + 90 = 180, donc deux.')]),

            ('relation', 'Une médiane part d’un sommet et va au milieu du côté opposé.',
             'bm-geo-mediane', 'Un triangle quelconque et sa médiane, qui rejoint le milieu du côté.',
             [('simple', 'La médiane vise le MILIEU. Elle coupe le côté en deux parts égales.'),
              ('visuel', 'Sur la figure, le point au bas de la médiane est marqué « milieu ».'),
              ('pas_a_pas', 'On cherche d’abord le milieu du côté, puis on trace le trait depuis le sommet.')],
             [('qcm', 1, {'question': 'Où arrive une médiane ?',
                          'options': ['au milieu du côté opposé', 'à angle droit sur le côté',
                                      'sur un autre sommet']},
               {'index': 0}, 'Au milieu du côté opposé.'),
              ('vrai_faux', 1, {'statement': 'Une médiane part d’un sommet du triangle.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Que faut-il trouver avant de tracer une médiane ?',
                          'options': ['le milieu du côté', 'l’angle droit', 'la plus grande longueur']},
               {'index': 0}, 'Le milieu du côté opposé.'),
              ('texte_a_trous', 3, {'text': 'La médiane va du sommet au {{1}} du côté opposé.', 'blanks': 1},
               {'values': ['milieu']}, 'Au milieu.'),
              ('qcm', 4, {'question': 'Combien de médianes un triangle a-t-il ?',
                          'options': ['trois', 'une', 'deux']},
               {'index': 0}, 'Une par sommet, donc trois.')]),

            ('relation', 'Une hauteur part d’un sommet et tombe à angle droit sur le côté opposé.',
             'bm-geo-hauteur', 'Le même triangle et sa hauteur, marquée par son angle droit.',
             [('simple', 'La hauteur vise l’angle DROIT. Elle ne vise pas le milieu.'),
              ('visuel', 'Sur la figure, le petit carré au pied de la hauteur dit l’angle droit.'),
              ('pas_a_pas', 'Médiane : le milieu. Hauteur : l’angle droit. C’est là toute la différence.')],
             [('qcm', 1, {'question': 'Comment une hauteur tombe-t-elle sur le côté opposé ?',
                          'options': ['à angle droit', 'au milieu', 'en diagonale']},
               {'index': 0}, 'À angle droit.'),
              ('vrai_faux', 1, {'statement': 'Une hauteur tombe toujours au milieu du côté opposé.'},
               {'value': False}, 'Non, c’est la médiane qui vise le milieu.'),
              ('association', 2, {'question': 'Relie chaque droite à ce qu’elle vise.',
                                  'gauche': ['La médiane', 'La hauteur'],
                                  'droite': ['le milieu du côté', 'l’angle droit']},
               {'order': [0, 1]}, 'La médiane vise le milieu, la hauteur vise l’angle droit.'),
              ('texte_a_trous', 3, {'text': 'La hauteur tombe à angle {{1}} sur le côté opposé.', 'blanks': 1},
               {'values': ['droit']}, 'À angle droit.'),
              ('qcm', 4, {'question': 'Dans un triangle quelconque, médiane et hauteur d’un sommet sont…',
                          'options': ['deux droites différentes', 'la même droite',
                                      'toujours perpendiculaires']},
               {'index': 0}, 'Différentes : l’une vise le milieu, l’autre l’angle droit.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues = set(), 0, 0
    durs = 0
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 400, 'résumé trop long (%d) : %s' % (len(resume), titre)
        assert img not in cles, 'image en double : ' + img
        cles.add(img)
        for kind, phrase, nimg, nprompt, expl, items in notions:
            notions_vues += 1
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 180, 'notion trop longue (%d) : %s' % (len(phrase), phrase)
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
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
                    durs += 1
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, \
                        'question trop longue (%d) : %s' % (len(payload['question']), payload['question'])
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 70, 'option trop longue : ' + o
                    # La bonne réponse ne doit pas se reconnaître à sa taille.
                    bonne = len(options[answer['index']])
                    autres = [len(o) for i, o in enumerate(options) if i != answer['index']]
                    assert bonne <= max(autres) * 2, \
                        'bonne réponse bien plus longue : ' + str(payload)
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']), payload['statement'])
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        # Le clavier de cet exercice a les chiffres mais PAS
                        # d-espace : « 2 050 » serait impossible à taper,
                        # d-où les nombres écrits collés.
                        for c in v:
                            assert c in TAPABLE, 'caractère absent du clavier : « %s » dans %s' % (c, v)
                        assert len(v) <= 16, 'réponse trop longue : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    # Le père a demandé du très difficile. Une question de Défi qui se
    # contente de répéter l-énoncé n-en est pas une : à cette étape, il
    # faut CALCULER quelque chose qui n-est écrit nulle part. On vérifie
    # qu-il y en a au moins une par notion.
    assert durs >= notions_vues, 'il manque des questions de Défi : %d pour %d notions' % (durs, notions_vues)

    # UN PROBLÈME EST UN TEXTE, PAS UNE OPÉRATION POSÉE.
    #
    # La première version de ces leçons n-en contenait aucun : le plus long
    # énoncé de la leçon « Les problèmes » faisait 76 signes, et les
    # questions portaient SUR les problèmes au lieu d-en être. La cause
    # était une de mes propres règles — la question d-un choix tient en
    # 90 signes, ce qui est juste pour un enfant de neuf ans, mais interdit
    # précisément ce qu-est un problème : une situation à lire avant de
    # calculer.
    #
    # Un vrai problème vit donc dans un texte à trous, dont le texte n-est
    # pas limité. On exige ici qu-il y en ait un par notion de la leçon des
    # problèmes, et au moins dix en tout.
    enonces = 0
    for titre, _c, _d, _o, _r, _i, _p, notions in LECONS:
        for _k, phrase, _ni, _np, _ex, items in notions:
            longs = [it for it in items
                     if it[0] == 'texte_a_trous' and len(it[2]['text']) >= 180]
            enonces += len(longs)
            if titre == 'Les problèmes':
                assert longs, \
                    ('« %s » n-a pas de problème rédigé. Un énoncé de moins de 180 signes '
                     'est une opération posée, pas un problème.' % phrase[:60])
    assert enonces >= 10, 'trop peu de problèmes rédigés : %d' % enonces

    # Et les clés d-images doivent être exactement celles que le module dessine.
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-brayne-maths-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    manquantes = cles - dessinees
    inutiles = dessinees - cles
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(sorted(manquantes))
    assert not inutiles, 'images dessinées mais jamais utilisées : ' + ', '.join(sorted(inutiles))
    return len(cles), total, notions_vues, durs


def paquet():
    return {
        'matiere': MATIERE, 'classe': CLASSE, 'enfant': ENFANT, 'lang': LANGUE,
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
    images, items, notions, durs = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-maths-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d de Defi - %d images'
          % (len(LECONS), notions, items, durs, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-38s %-22s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
