# -*- coding: utf-8 -*-
"""
Huit leçons sur les nombres décimaux pour BRAYNE (CM1) — fiche de révision
« CM1 - MATHEMATICS - REVISION SHEET - DECIMAL NUMBERS », 3 pages, donnée
par le père le 8 novembre 2026.

RIEN DE CE SUJET N-ÉTAIT EN BASE. Les douze sections de la fiche sont donc
toutes reprises, en huit leçons :

  section 1       la place des chiffres : dixièmes, centièmes, millièmes
  section 2       lire et écrire un décimal
  sections 3-4    comparer et ranger
  section 5       arrondir
  section 6       les chiffres significatifs
  section 7       passer du décimal à la fraction, et l-inverse
  section 8       additionner et soustraire
  sections 9-10   multiplier et diviser
  section 11      les problèmes

TOUTES LES FAUTES DE CE CHAPITRE SONT DES FAUTES DE COLONNE : comparer
2.05 à 2.5 sans aligner, poser une addition sans aligner les virgules,
arrondir en regardant le mauvais chiffre. Les leçons sont donc écrites
autour de la colonne, et les figures montrent la colonne.

LES EXEMPLES SONT CEUX DE LA FICHE, aux chiffres près : 34.728, 2.5 et
2.05, 3.276, 526.8, 0.004025, 7/20, 4.006 + 2.940, 64.80 - 5.63,
0.08 × 4.2, 2.4 ÷ 0.08, 48.5 kg - 20.2 kg. Chaque calcul a été refait à la
main avant d-être écrit ici.

LE POINT DÉCIMAL EST ÉCRIT « . » ET NON « , » : c-est la notation de sa
fiche, qui est anglophone, et c-est celle qu-on lui demandera. Le clavier
de l-application a le point, donc une réponse comme 0.35 se tape.

Usage :  python work/lecons-brayne-decimaux.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-decimaux.py. ')

MATIERE = 'Mathématiques'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'en'
CHAPITRE = 'Decimal numbers'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

LECONS = [
    # ------------------------------------------------------------------ 44
    (
        'Decimal place value', CHAPITRE, None, 44,
        'The decimal point separates the whole number from the parts. The first digit after the '
        'point is the tenths, the second the hundredths, the third the thousandths. In 34.728: '
        '3 is tens, 4 is units, 7 is tenths, 2 is hundredths and 8 is thousandths.',
        'bd-pv-couv',
        'Le tableau de position avec 34.728 posé dedans, la colonne des dixièmes allumée.',
        [
            ('relation',
             'The decimal point separates the whole number on its left from the parts of a '
             'whole on its right.',
             'bd-pv-point',
             'Le tableau de position, la colonne du point allumée.',
             [('simple', 'Left of the point: whole things. Right of the point: pieces of a '
                         'thing.'),
              ('visuel', 'The point is not a digit. It is a fence between two kinds of '
                         'columns.')],
             [('qcm', 1, {'question': 'What does the decimal point separate?',
                          'options': ['The whole number from the parts',
                                      'The tens from the hundreds',
                                      'The answer from the question']},
               {'index': 0}, 'The whole number on the left, the parts on the right.'),
              ('vrai_faux', 1, {'statement': 'In 34.728, the whole number is 34.'},
               {'value': True}, 'Yes: what is written left of the point.'),
              ('texte_a_trous', 2,
               {'text': 'Left of the point is the {{1}} number.', 'blanks': 1},
               {'values': ['whole']}, 'The whole number.'),
              ('qcm', 3, {'question': 'In 7.25, what is the whole number?',
                          'options': ['7', '25', '725']},
               {'index': 0}, 'Seven, on the left of the point.'),
              ('vrai_faux', 4, {'statement': 'The decimal point is itself a digit.'},
               {'value': False}, 'No. It only marks where the parts begin.')]),

            ('definition',
             'The first digit after the decimal point is the tenths digit.',
             'bd-pv-dixiemes',
             'Le tableau de position, la colonne des dixièmes allumée sur le 7.',
             [('simple', 'In 34.728, the tenths digit is 7: the whole is cut into ten parts, '
                         'and seven are taken.'),
              ('pas_a_pas', 'Find the point. Move one place to the right. That is the tenths.')],
             [('qcm', 1, {'question': 'Which digit comes just after the point?',
                          'options': ['The tenths', 'The hundredths', 'The units']},
               {'index': 0}, 'The tenths.'),
              ('vrai_faux', 1, {'statement': 'In 34.728, the tenths digit is 7.'},
               {'value': True}, 'Yes: the first one after the point.'),
              ('texte_a_trous', 2,
               {'text': 'The first digit after the point is the {{1}} digit.', 'blanks': 1},
               {'values': ['tenths']}, 'The tenths digit.'),
              ('qcm', 3, {'question': 'In 0.46, what is the tenths digit?',
                          'options': ['4', '6', '0']},
               {'index': 0}, 'The first one after the point.'),
              ('vrai_faux', 4, {'statement': 'The tenths digit is written before the point.'},
               {'value': False}, 'No. It is the first one after it.')]),

            ('definition',
             'The second digit after the point is the hundredths, and the third is the '
             'thousandths.',
             'bd-pv-centiemes',
             'Le tableau de position, les colonnes des centièmes et des millièmes allumées.',
             [('simple', 'In 34.728, 2 is the hundredths digit and 8 is the thousandths digit.'),
              ('visuel', 'The further right you go, the smaller the parts become.')],
             [('qcm', 1, {'question': 'Which is the third digit after the point?',
                          'options': ['The thousandths', 'The hundredths', 'The tenths']},
               {'index': 0}, 'The thousandths.'),
              ('vrai_faux', 1, {'statement': 'In 34.728, the hundredths digit is 2.'},
               {'value': True}, 'Yes: the second one after the point.'),
              ('texte_a_trous', 2,
               {'text': 'The second digit after the point is the {{1}} digit.', 'blanks': 1},
               {'values': ['hundredths']}, 'The hundredths digit.'),
              ('qcm', 3, {'question': 'In 0.149, what is the thousandths digit?',
                          'options': ['9', '1', '4']},
               {'index': 0}, 'The third one after the point.'),
              ('vrai_faux', 4,
               {'statement': 'Hundredths are bigger parts than tenths.'},
               {'value': False}, 'No. The further right, the smaller.')]),

            ('relation',
             'In 34.728, each digit has its own column: 3 tens, 4 units, 7 tenths, 2 hundredths '
             'and 8 thousandths.',
             'bd-pv-nombre',
             'Le nombre 34.728 posé colonne par colonne.',
             [('simple', 'A digit means nothing by itself. Its column gives it its value.'),
              ('pas_a_pas', 'Write the columns first, then drop each digit into its own.')],
             [('qcm', 1, {'question': 'In 34.728, which digit is in the tens column?',
                          'options': ['3', '4', '7']},
               {'index': 0}, 'Three tens.'),
              ('vrai_faux', 1, {'statement': 'In 34.728, the units digit is 4.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each digit of 34.728 with its column.',
                                  'gauche': ['3', '4', '7'],
                                  'droite': ['tens', 'units', 'tenths']},
               {'order': [0, 1, 2]}, 'Tens, units, then tenths after the point.'),
              ('qcm', 3, {'question': 'In 34.728, which digit is in the thousandths column?',
                          'options': ['8', '2', '7']},
               {'index': 0}, 'The last one.'),
              ('vrai_faux', 4,
               {'statement': 'A digit has the same value in every column.'},
               {'value': False}, 'No. Its column gives it its value.')]),

            ('relation',
             'A decimal is read digit by digit after the point: 4.5 is four point five, and '
             '12.304 is twelve point three zero four.',
             'bd-pv-lecture',
             'Trois lectures : 4.5, 0.07 et 12.304, écrites en toutes lettres.',
             [('simple', 'Before the point, read the number. After the point, name the digits '
                         'one by one.'),
              ('visuel', 'You never say twelve point three hundred and four. Each digit is said '
                         'on its own.')],
             [('qcm', 1, {'question': 'How is 4.5 read?',
                          'options': ['four point five', 'four and five',
                                      'forty-five point']},
               {'index': 0}, 'Four point five.'),
              ('vrai_faux', 1, {'statement': 'The number 0.07 is read zero point zero seven.'},
               {'value': True}, 'Yes, digit by digit.'),
              ('texte_a_trous', 2,
               {'text': 'After the point, the digits are read one by {{1}}.', 'blanks': 1},
               {'values': ['one']}, 'One by one.'),
              ('qcm', 3, {'question': 'How do you write seven point three?',
                          'options': ['7.3', '73', '0.73']},
               {'index': 0}, 'Seven, the point, then three.'),
              ('vrai_faux', 4,
               {'statement': 'The number 12.304 is read twelve point three hundred and four.'},
               {'value': False}, 'No: twelve point three zero four.')]),
        ],
    ),

    # ------------------------------------------------------------------ 45
    (
        'Comparing and ordering decimals', CHAPITRE, None, 45,
        'To compare two decimals, look at the digits from left to right, column by column. Zeros '
        'may be added at the end without changing the number: 2.5 = 2.500. So 2.500 is bigger '
        'than 2.050, which means 2.5 is bigger than 2.05.',
        'bd-cp-couv',
        'Le cadre portant 2.500 est plus grand que 2.050.',
        [
            ('relation',
             'To compare two decimals, read the digits from left to right and stop at the first '
             'column where they differ.',
             'bd-cp-gauche',
             'Les trois temps : les unités, puis les dixièmes, puis les centièmes.',
             [('simple', 'The first column where they differ decides. The rest does not '
                         'matter.'),
              ('pas_a_pas', 'Compare the units. If they are equal, compare the tenths. Then the '
                            'hundredths.')],
             [('qcm', 1, {'question': 'In which direction do you compare decimals?',
                          'options': ['From left to right', 'From right to left',
                                      'From the point outwards']},
               {'index': 0}, 'From left to right, column by column.'),
              ('vrai_faux', 1,
               {'statement': 'The first column where two decimals differ decides.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Decimals are compared from {{1}} to right.', 'blanks': 1},
               {'values': ['left']}, 'From left to right.'),
              ('qcm', 3, {'question': 'Which is the bigger, 3.41 or 3.52?',
                          'options': ['3.52', '3.41', 'They are equal']},
               {'index': 0}, 'Same units, but 5 tenths beat 4 tenths.'),
              ('vrai_faux', 4,
               {'statement': 'The decimal with the most digits is always the bigger.'},
               {'value': False}, 'No. 2.05 has more digits than 2.5 and is smaller.')]),

            ('relation',
             'Zeros may be added at the end of a decimal without changing it: 2.5 = 2.500 and '
             '0.75 = 0.750.',
             'bd-cp-zeros',
             '2.5 s’écrit aussi 2.500 : le nombre ne change pas, les colonnes s’alignent.',
             [('simple', 'Adding a zero at the end adds no part at all. It only fills the '
                         'column.'),
              ('pas_a_pas', 'Give both numbers the same number of digits after the point. Then '
                            'compare.')],
             [('qcm', 1, {'question': 'What happens if you write 2.5 as 2.500?',
                          'options': ['Nothing changes', 'It becomes bigger',
                                      'It becomes smaller']},
               {'index': 0}, 'It is the same number.'),
              ('vrai_faux', 1, {'statement': 'The numbers 0.75 and 0.750 are equal.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Adding a {{1}} at the end does not change a decimal.', 'blanks': 1},
               {'values': ['zero']}, 'A zero.'),
              ('qcm', 3, {'question': 'Written with three decimal places, what is 2.5?',
                          'options': ['2.500', '2.005', '2.050']},
               {'index': 0}, 'The zeros go after the 5.'),
              ('vrai_faux', 4, {'statement': 'The numbers 2.5 and 2.05 are equal.'},
               {'value': False}, 'No. 2.5 is 2.50, which is bigger.')]),

            ('relation',
             'Once the zeros are added, the comparison is plain: 2.500 is bigger than 2.050, so '
             '2.5 is bigger than 2.05.',
             'bd-cp-exemple',
             '2.500 et 2.050 posés l’un sous l’autre, les points alignés.',
             [('simple', 'Five tenths against zero tenths: the first one wins at once.'),
              ('visuel', 'Written one under the other with the points aligned, the answer is '
                         'read off the page.')],
             [('qcm', 1, {'question': 'Which is the bigger, 2.5 or 2.05?',
                          'options': ['2.5', '2.05', 'They are equal']},
               {'index': 0}, '2.5 is 2.50, and 50 hundredths beat 5.'),
              ('vrai_faux', 1, {'statement': 'The number 2.5 is bigger than 2.05.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Written with three places, 2.05 becomes {{1}}.', 'blanks': 1},
               {'values': ['2.050']}, 'Two point zero five zero.'),
              ('qcm', 3, {'question': 'Which is the bigger, 0.6 or 0.59?',
                          'options': ['0.6', '0.59', 'They are equal']},
               {'index': 0}, '0.60 is bigger than 0.59.'),
              ('vrai_faux', 4, {'statement': 'The number 0.09 is bigger than 0.1.'},
               {'value': False}, 'No. 0.10 is bigger than 0.09.')]),

            ('relation',
             'Ascending order goes from the smallest to the greatest; descending order goes the '
             'other way: 0.07, 0.077, 0.7, 0.707 is ascending.',
             'bd-cp-ordre',
             'La suite 0.07, 0.077, 0.7, 0.707 rangée du plus petit au plus grand.',
             [('simple', 'Ascending climbs. Descending comes down.'),
              ('pas_a_pas', 'Give them all the same number of decimal places, then put them in '
                            'order.')],
             [('qcm', 1, {'question': 'What does ascending order mean?',
                          'options': ['From smallest to greatest',
                                      'From greatest to smallest', 'In any order']},
               {'index': 0}, 'From the smallest to the greatest.'),
              ('vrai_faux', 1,
               {'statement': 'Descending order goes from the greatest to the smallest.'},
               {'value': True}, 'Yes.'),
              ('chronologie', 2, {'question': 'Put these in ascending order.',
                                  'tokens': ['0.07', '0.077', '0.7', '0.707']},
               {'order': [0, 1, 2, 3]}, 'Written with three places: 0.070, 0.077, 0.700, 0.707.'),
              ('qcm', 3, {'question': 'Which one is the smallest?',
                          'options': ['0.07', '0.7', '0.707']},
               {'index': 0}, 'Seven hundredths is the smallest of the three.'),
              ('vrai_faux', 4,
               {'statement': 'In ascending order, the greatest number comes first.'},
               {'value': False}, 'No. It comes last.')]),
        ],
    ),

    # ------------------------------------------------------------------ 46
    (
        'Rounding decimals', CHAPITRE, None, 46,
        'To round, look at the digit just after the place you are keeping. If it is 5 or more, '
        'add 1. If it is less than 5, keep the digit as it is. To the nearest whole number check '
        'the tenths; to the nearest tenth check the hundredths; to the nearest hundredth check '
        'the thousandths.',
        'bd-ro-couv',
        'Le cadre portant 3.276 arrondi au centième : 3.28.',
        [
            ('relation',
             'The rule for rounding: if the digit just after is 5 or more, add 1. If it is less '
             'than 5, keep the digit as it is.',
             'bd-ro-regle',
             'La règle en trois lignes : regarder le chiffre d’après, 5 ou plus, moins de 5.',
             [('simple', 'One digit decides, and only one: the one straight after the place you '
                         'keep.'),
              ('pas_a_pas', 'Underline the place you keep. Look at the next digit. Then decide.')],
             [('qcm', 1, {'question': 'When do you add 1 when rounding?',
                          'options': ['When the next digit is 5 or more',
                                      'When the next digit is 4 or less',
                                      'When the number is big']},
               {'index': 0}, 'When the checking digit is 5 or more.'),
              ('vrai_faux', 1,
               {'statement': 'If the checking digit is less than 5, the digit is kept.'},
               {'value': True}, 'Yes, unchanged.'),
              ('texte_a_trous', 2,
               {'text': 'If the checking digit is 5 or more, you add {{1}}.', 'blanks': 1},
               {'values': ['1']}, 'You add one.'),
              ('qcm', 3, {'question': 'The checking digit is 4. What do you do?',
                          'options': ['Keep the digit', 'Add 1 to it', 'Remove it']},
               {'index': 0}, '4 is less than 5, so nothing changes.'),
              ('vrai_faux', 4,
               {'statement': 'All the digits after the place you keep decide the rounding.'},
               {'value': False}, 'No. Only the first one after it.')]),

            ('relation',
             'To round to the nearest whole number, look at the tenths digit.',
             'bd-ro-entier',
             'Le tableau de position, la colonne des dixièmes allumée.',
             [('simple', 'In 34.728, the tenths digit is 7, which is 5 or more, so 34 becomes '
                         '35.'),
              ('pas_a_pas', 'Keep the units. Check the tenths. Decide. Drop everything after the '
                            'point.')],
             [('qcm', 1, {'question': 'Rounding to the nearest whole number: which digit?',
                          'options': ['The tenths digit', 'The hundredths digit',
                                      'The units digit']},
               {'index': 0}, 'The tenths digit decides.'),
              ('vrai_faux', 1, {'statement': 'To the nearest whole number, 34.728 gives 35.'},
               {'value': True}, 'Yes: the tenths digit is 7.'),
              ('texte_a_trous', 2,
               {'text': 'For the nearest whole number, check the {{1}} digit.', 'blanks': 1},
               {'values': ['tenths']}, 'The tenths digit.'),
              ('qcm', 3, {'question': 'To the nearest whole number, what is 6.3?',
                          'options': ['6', '7', '6.3']},
               {'index': 0}, '3 is less than 5, so 6 stays 6.'),
              ('vrai_faux', 4, {'statement': 'To the nearest whole number, 2.5 gives 2.'},
               {'value': False}, 'No: 5 or more, so it gives 3.')]),

            ('relation',
             'To round to the nearest tenth, look at the hundredths digit. One digit is kept '
             'after the point.',
             'bd-ro-dixieme',
             'Le tableau de position, la colonne des centièmes allumée.',
             [('simple', 'In 34.728, the hundredths digit is 2, which is less than 5, so the '
                         'answer is 34.7.'),
              ('pas_a_pas', 'Keep one digit after the point. Check the next one. Decide.')],
             [('qcm', 1, {'question': 'Rounding to the nearest tenth: which digit decides?',
                          'options': ['The hundredths digit', 'The tenths digit',
                                      'The thousandths digit']},
               {'index': 0}, 'The hundredths digit.'),
              ('vrai_faux', 1, {'statement': 'To the nearest tenth, 34.728 gives 34.7.'},
               {'value': True}, 'Yes: the hundredths digit is 2.'),
              ('texte_a_trous', 2,
               {'text': 'To the nearest tenth, you keep {{1}} digit after the point.',
                'blanks': 1},
               {'values': ['one']}, 'One digit.'),
              ('qcm', 3, {'question': 'To the nearest tenth, what is 0.48?',
                          'options': ['0.5', '0.4', '0.48']},
               {'index': 0}, '8 is 5 or more, so 4 becomes 5.'),
              ('vrai_faux', 4, {'statement': 'To the nearest tenth, 0.42 gives 0.5.'},
               {'value': False}, 'No: 2 is less than 5, so it gives 0.4.')]),

            ('relation',
             'To round to the nearest hundredth, look at the thousandths digit: 3.276 gives '
             '3.28, because 6 is 5 or more.',
             'bd-ro-centieme',
             'Les trois temps : regarder le millième 6, 6 est plus grand que 5, 3.276 devient 3.28.',
             [('simple', 'Two digits are kept after the point, and the third one decides.'),
              ('pas_a_pas', 'Keep 3.27. Look at the 6. It is 5 or more, so 7 becomes 8: 3.28.')],
             [('qcm', 1, {'question': 'Rounding to the nearest hundredth: which digit decides?',
                          'options': ['The thousandths digit', 'The hundredths digit',
                                      'The tenths digit']},
               {'index': 0}, 'The thousandths digit.'),
              ('vrai_faux', 1, {'statement': 'To the nearest hundredth, 3.276 gives 3.28.'},
               {'value': True}, 'Yes: the thousandths digit is 6.'),
              ('texte_a_trous', 2,
               {'text': 'To the nearest hundredth, 3.276 gives {{1}}.', 'blanks': 1},
               {'values': ['3.28']}, 'Three point two eight.'),
              ('qcm', 3, {'question': 'To the nearest hundredth, what is 0.512?',
                          'options': ['0.51', '0.52', '0.5']},
               {'index': 0}, '2 is less than 5, so 1 stays 1.'),
              ('vrai_faux', 4, {'statement': 'To the nearest hundredth, 3.276 gives 3.27.'},
               {'value': False}, 'No: the 6 makes the 7 become 8.')]),
        ],
    ),

    # ------------------------------------------------------------------ 47
    (
        'Significant figures', CHAPITRE, None, 47,
        'Counting significant figures starts at the first digit that is not a zero. Keep as many '
        'digits as you are asked for, and use the next digit to round. So 526.8 to three '
        'significant figures is 527, and 0.004025 to three significant figures is 0.00403.',
        'bd-sf-couv',
        'Le cadre portant 526.8 arrondi à trois chiffres significatifs : 527.',
        [
            ('relation',
             'Counting significant figures starts at the first digit that is not a zero. The '
             'zeros written before it do not count.',
             'bd-sf-premier',
             'Dans 0.004025, on commence à compter au 4.',
             [('simple', 'In 0.004025, the first significant figure is 4. The zeros in front '
                         'only show where the number sits.'),
              ('pas_a_pas', 'Read from the left. Skip the zeros until the first digit that is '
                            'not one. Start counting there.')],
             [('qcm', 1, {'question': 'Where does the counting start?',
                          'options': ['At the first digit that is not zero',
                                      'At the first digit after the point',
                                      'At the last digit']},
               {'index': 0}, 'At the first digit that is not a zero.'),
              ('vrai_faux', 1,
               {'statement': 'In 0.004025, the first significant figure is 4.'},
               {'value': True}, 'Yes: the zeros in front do not count.'),
              ('texte_a_trous', 2,
               {'text': 'Counting starts at the first digit that is not a {{1}}.', 'blanks': 1},
               {'values': ['zero']}, 'Not a zero.'),
              ('qcm', 3, {'question': 'In 0.0307, what is the first significant figure?',
                          'options': ['3', '0', '7']},
               {'index': 0}, 'The first digit that is not a zero.'),
              ('vrai_faux', 4,
               {'statement': 'The zeros written in front of a number are significant.'},
               {'value': False}, 'No. They only show where the number sits.')]),

            ('relation',
             'Keep exactly as many significant figures as you are asked for, and no more.',
             'bd-sf-garder',
             'Trois chiffres significatifs demandés : on en garde trois.',
             [('simple', 'Three significant figures means three digits counted from the first '
                         'one that is not a zero.'),
              ('visuel', 'Count them on your fingers as you read the number from the left.')],
             [('qcm', 1, {'question': 'How many digits do you keep for 3 significant figures?',
                          'options': ['Three', 'Four', 'As many as you like']},
               {'index': 0}, 'Three, counted from the first one that is not a zero.'),
              ('vrai_faux', 1,
               {'statement': 'Three significant figures means keeping three digits.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Keep exactly the number of figures you are {{1}} for.', 'blanks': 1},
               {'values': ['asked']}, 'Asked for.'),
              ('qcm', 3, {'question': 'In 526.8, which are the first three figures?',
                          'options': ['5, 2 and 6', '5, 2 and 8', '2, 6 and 8']},
               {'index': 0}, 'Counting from the left: 5, 2, 6.'),
              ('vrai_faux', 4,
               {'statement': 'You may keep four figures when three are asked for.'},
               {'value': False}, 'No. Exactly three.')]),

            ('relation',
             'The digit that comes just after the ones you keep does the rounding, by the usual '
             'rule.',
             'bd-sf-arrondir',
             '526.8 à trois chiffres : le suivant est 8, donc 527.',
             [('simple', 'In 526.8, you keep 526, and the next digit is 8: five or more, so 526 '
                         'becomes 527.'),
              ('pas_a_pas', 'Keep your figures. Look at the next one. Apply the rounding rule.')],
             [('qcm', 1, {'question': 'Which digit does the rounding?',
                          'options': ['The one just after those kept',
                                      'The last digit of the number',
                                      'The first digit of the number']},
               {'index': 0}, 'The one just after the figures you keep.'),
              ('vrai_faux', 1,
               {'statement': 'To three significant figures, 526.8 gives 527.'},
               {'value': True}, 'Yes: the next digit is 8.'),
              ('texte_a_trous', 2,
               {'text': 'To three significant figures, 526.8 gives {{1}}.', 'blanks': 1},
               {'values': ['527']}, 'Five hundred and twenty-seven.'),
              ('qcm', 3, {'question': 'To two significant figures, what is 3.46?',
                          'options': ['3.5', '3.4', '3.46']},
               {'index': 0}, 'Keep 3.4, and the 6 makes the 4 become 5.'),
              ('vrai_faux', 4,
               {'statement': 'To three significant figures, 526.8 gives 526.'},
               {'value': False}, 'No: the 8 rounds it up to 527.')]),

            ('relation',
             'Two worked examples: 526.8 to three significant figures is 527, and 0.004025 to '
             'three significant figures is 0.00403.',
             'bd-sf-exemples',
             'Les deux exemples de la fiche : 526.8 donne 527, 0.004025 donne 0.00403.',
             [('simple', 'In 0.004025, the three figures are 4, 0 and 2; the next one is 5, so '
                         'the 2 becomes 3.'),
              ('visuel', 'The zeros in front stay in place: they are not figures, but they hold '
                         'the number where it is.')],
             [('qcm', 1, {'question': 'To three significant figures, what is 0.004025?',
                          'options': ['0.00403', '0.00402', '0.004']},
               {'index': 0}, 'The figures are 4, 0, 2, and the next one is 5.'),
              ('vrai_faux', 1,
               {'statement': 'To three significant figures, 0.004025 gives 0.00403.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The zeros written in front are {{1}} in the answer.', 'blanks': 1},
               {'values': ['kept']}, 'They are kept.'),
              ('qcm', 3, {'question': 'In 0.004025, which digit does the rounding?',
                          'options': ['5', '4', '2']},
               {'index': 0}, 'The one just after the three figures kept.'),
              ('vrai_faux', 4,
               {'statement': 'Rounding 0.004025 removes the zeros written in front.'},
               {'value': False}, 'No. They hold the number where it is.')]),
        ],
    ),

    # ------------------------------------------------------------------ 48
    (
        'Decimals and fractions', CHAPITRE, None, 48,
        'A decimal can be written as a fraction and back again: 0.5 = 5/10 = 1/2, 0.25 = 1/4 and '
        '0.75 = 3/4. A fraction in tenths is read straight off: 3/10 = 0.3. Others are changed '
        'into hundredths first: 7/20 = 35/100 = 0.35.',
        'bd-fr-couv',
        'Le cadre portant 0.75 = 75/100 = 3/4.',
        [
            ('relation',
             'The decimal 0.5 is five tenths, which is 5/10, which is one half.',
             'bd-fr-moitie',
             '0.5 = 5/10, puis 5/10 = 1/2.',
             [('simple', 'One digit after the point means tenths. Five tenths is a half.'),
              ('pas_a_pas', 'Write the digits after the point over 10, then simplify.')],
             [('qcm', 1, {'question': 'What fraction is 0.5?',
                          'options': ['1/2', '1/5', '5/1']},
               {'index': 0}, 'Five tenths, which is a half.'),
              ('vrai_faux', 1, {'statement': 'The decimal 0.5 is equal to 5/10.'},
               {'value': True}, 'Yes: five tenths.'),
              ('texte_a_trous', 2,
               {'text': 'One digit after the point means {{1}}.', 'blanks': 1},
               {'values': ['tenths']}, 'Tenths.'),
              ('qcm', 3, {'question': 'What is 0.5 of 60?',
                          'options': ['30', '12', '50']},
               {'index': 0}, 'Half of 60.'),
              ('vrai_faux', 4, {'statement': 'The decimal 0.5 is equal to 1/5.'},
               {'value': False}, 'No. It is one half.')]),

            ('relation',
             'Two digits after the point mean hundredths: 0.25 = 25/100 = 1/4, and '
             '0.75 = 75/100 = 3/4.',
             'bd-fr-quarts',
             'Les deux quarts décimaux : 0.25 = 1/4 et 0.75 = 3/4.',
             [('simple', 'Twenty-five hundredths is a quarter; seventy-five hundredths is three '
                         'quarters.'),
              ('visuel', 'These two come back so often that they are worth knowing by heart.')],
             [('qcm', 1, {'question': 'What fraction is 0.25?',
                          'options': ['1/4', '1/2', '3/4']},
               {'index': 0}, 'Twenty-five hundredths, which is a quarter.'),
              ('vrai_faux', 1, {'statement': 'The decimal 0.75 is equal to 3/4.'},
               {'value': True}, 'Yes: three quarters.'),
              ('texte_a_trous', 2,
               {'text': 'Two digits after the point mean {{1}}.', 'blanks': 1},
               {'values': ['hundredths']}, 'Hundredths.'),
              ('qcm', 3, {'question': 'What is 0.75 of 40?',
                          'options': ['30', '10', '34']},
               {'index': 0}, 'Three quarters of 40.'),
              ('vrai_faux', 4, {'statement': 'The decimal 0.25 is equal to 3/4.'},
               {'value': False}, 'No. It is one quarter.')]),

            ('relation',
             'A fraction in tenths is read straight off as a decimal: 3/10 = 0.3.',
             'bd-fr-versdecimal',
             '3/10, trois dixièmes, donc 0.3.',
             [('simple', 'The numerator goes just after the point when the denominator is 10.'),
              ('pas_a_pas', 'Check the denominator is 10. Write the numerator one place after '
                            'the point.')],
             [('qcm', 1, {'question': 'What decimal is 3/10?',
                          'options': ['0.3', '3.0', '0.03']},
               {'index': 0}, 'Three tenths.'),
              ('vrai_faux', 1, {'statement': 'The fraction 3/10 is equal to 0.3.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The fraction 7/10 is written {{1}} as a decimal.', 'blanks': 1},
               {'values': ['0.7']}, 'Zero point seven.'),
              ('qcm', 3, {'question': 'What decimal is 9/10?',
                          'options': ['0.9', '9.0', '0.09']},
               {'index': 0}, 'Nine tenths.'),
              ('vrai_faux', 4, {'statement': 'The fraction 3/10 is equal to 0.03.'},
               {'value': False}, 'No. That would be three hundredths.')]),

            ('relation',
             'A fraction whose denominator is not 10 or 100 is changed first: 7/20 becomes '
             '35/100, which is 0.35.',
             'bd-fr-vingtieme',
             '7/20 : on multiplie par 5 en haut et en bas, donc 35/100, donc 0.35.',
             [('simple', 'Twenty goes into a hundred five times, so multiply the top by five '
                         'too.'),
              ('pas_a_pas', 'Find what turns the denominator into 100. Multiply top and bottom '
                            'by it. Then read the decimal.')],
             [('qcm', 1, {'question': 'To change 7/20, what do you multiply by?',
                          'options': ['5', '2', '10']},
               {'index': 0}, '20 × 5 = 100.'),
              ('vrai_faux', 1, {'statement': 'The fraction 7/20 is equal to 35/100.'},
               {'value': True}, 'Yes: 7 × 5 and 20 × 5.'),
              ('texte_a_trous', 2,
               {'text': 'The fraction 7/20 is written {{1}} as a decimal.', 'blanks': 1},
               {'values': ['0.35']}, 'Zero point three five.'),
              ('qcm', 3, {'question': 'What decimal is 3/4?',
                          'options': ['0.75', '0.34', '0.25']},
               {'index': 0}, '3/4 = 75/100 = 0.75.'),
              ('vrai_faux', 4,
               {'statement': 'You multiply only the denominator to reach 100.'},
               {'value': False}, 'No. Top and bottom, by the same number.')]),
        ],
    ),

    # ------------------------------------------------------------------ 49
    (
        'Adding and subtracting decimals', CHAPITRE, None, 49,
        'Line up the decimal points one under the other, add zeros if a column is empty, and '
        'then add or subtract as usual. So 4.006 + 2.940 = 6.946, and 64.80 - 5.63 = 59.17. The '
        'point of the answer sits under the others.',
        'bd-as-couv',
        'Le cadre portant 4.006 + 2.940 = 6.946.',
        [
            ('relation',
             'The decimal points are lined up one under the other before anything is added or '
             'subtracted.',
             'bd-as-aligner',
             '4.006 et 2.940 posés, les points l’un sous l’autre.',
             [('simple', 'Tenths must sit under tenths, and hundredths under hundredths. The '
                         'point is what lines them up.'),
              ('visuel', 'Align on the point, never on the right-hand edge. That is the whole '
                         'difference.')],
             [('qcm', 1, {'question': 'What do you line up before adding decimals?',
                          'options': ['The decimal points', 'The last digits',
                                      'The first digits']},
               {'index': 0}, 'The decimal points, one under the other.'),
              ('vrai_faux', 1, {'statement': 'Decimals are lined up on their right-hand edge.'},
               {'value': False}, 'No. They are lined up on the point.'),
              ('texte_a_trous', 2,
               {'text': 'Before adding, line up the decimal {{1}}.', 'blanks': 1},
               {'values': ['points']}, 'The decimal points.'),
              ('qcm', 3, {'question': 'Why are the points lined up?',
                          'options': ['So each column meets its own kind',
                                      'To make the numbers look nice',
                                      'To make the answer bigger']},
               {'index': 0}, 'So that tenths meet tenths, and hundredths hundredths.'),
              ('vrai_faux', 4,
               {'statement': 'The point of the answer sits under the other points.'},
               {'value': True}, 'Yes, in the same column.')]),

            ('relation',
             'If a column is empty, fill it with a zero: 64.8 is written 64.80 before 5.63 is '
             'taken away from it.',
             'bd-as-zeros',
             '64.8 s’écrit 64.80 : les colonnes sont pleines, on peut soustraire.',
             [('simple', 'An empty column cannot be subtracted from. A zero fills it without '
                         'changing the number.'),
              ('pas_a_pas', 'Count the decimal places of the longest number. Give the same '
                            'number of places to the others.')],
             [('qcm', 1, {'question': 'What do you write in an empty column?',
                          'options': ['A zero', 'A one', 'Nothing at all']},
               {'index': 0}, 'A zero, which changes nothing.'),
              ('vrai_faux', 1, {'statement': 'Before subtracting 5.63, you write 64.8 as 64.80.'},
               {'value': True}, 'Yes, so that every column is full.'),
              ('texte_a_trous', 2,
               {'text': 'An empty column is filled with a {{1}}.', 'blanks': 1},
               {'values': ['zero']}, 'A zero.'),
              ('qcm', 3, {'question': 'With two decimal places, how is 7.5 written?',
                          'options': ['7.50', '7.05', '0.75']},
               {'index': 0}, 'The zero goes after the 5.'),
              ('vrai_faux', 4, {'statement': 'Writing 64.8 as 64.80 makes it bigger.'},
               {'value': False}, 'No. It is the same number.')]),

            ('relation',
             'A worked addition: 4.006 + 2.940 = 6.946. The columns are added as usual, and the '
             'point stays in its column.',
             'bd-as-addition',
             'L’addition 4.006 + 2.940 = 6.946 posée, les points alignés.',
             [('simple', 'Once the points are lined up, it is an ordinary addition.'),
              ('pas_a_pas', 'Add the thousandths, then the hundredths, then the tenths, then the '
                            'units.')],
             [('qcm', 1, {'question': 'What is 4.006 + 2.940?',
                          'options': ['6.946', '6.046', '7.946']},
               {'index': 0}, 'Column by column: 6.946.'),
              ('vrai_faux', 1, {'statement': 'The sum 4.006 + 2.940 is equal to 6.946.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'In the answer, the point stays in its own {{1}}.', 'blanks': 1},
               {'values': ['column']}, 'Its own column.'),
              ('qcm', 3, {'question': 'What is 1.5 + 2.25?',
                          'options': ['3.75', '3.3', '2.4']},
               {'index': 0}, '1.50 + 2.25 = 3.75.'),
              ('vrai_faux', 4, {'statement': 'The sum 1.5 + 2.25 is equal to 2.40.'},
               {'value': False}, 'No. It is 3.75.')]),

            ('relation',
             'A worked subtraction: 64.80 - 5.63 = 59.17. The zero added to 64.8 is what makes '
             'the hundredths column workable.',
             'bd-as-soustraction',
             'La soustraction 64.80 – 5.63 = 59.17 posée, les points alignés.',
             [('simple', 'Without the zero, there would be nothing to take 3 hundredths from.'),
              ('pas_a_pas', 'Fill the columns. Line up the points. Subtract from the right.')],
             [('qcm', 1, {'question': 'What is 64.80 - 5.63?',
                          'options': ['59.17', '58.17', '59.23']},
               {'index': 0}, 'Column by column: 59.17.'),
              ('vrai_faux', 1, {'statement': 'The difference 64.80 - 5.63 is equal to 59.17.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The zero of 64.80 fills the {{1}} column.', 'blanks': 1},
               {'values': ['hundredths']}, 'The hundredths column.'),
              ('qcm', 3, {'question': 'What is 9.5 - 2.25?',
                          'options': ['7.25', '7.3', '6.75']},
               {'index': 0}, '9.50 - 2.25 = 7.25.'),
              ('vrai_faux', 4,
               {'statement': 'A subtraction of decimals starts from the left.'},
               {'value': False}, 'No. It starts from the right, as usual.')]),
        ],
    ),

    # ------------------------------------------------------------------ 50
    (
        'Multiplying and dividing decimals', CHAPITRE, None, 50,
        'To multiply, multiply as if the numbers were whole, count all the decimal places of '
        'both, and put the point there: 0.08 × 4.2 = 0.336. To divide, make the divisor a whole '
        'number by multiplying both numbers by 10 or 100: 2.4 ÷ 0.08 = 240 ÷ 8 = 30.',
        'bd-md-couv',
        'Le cadre portant 3.6 × 2.5 = 9.0.',
        [
            ('relation',
             'To multiply decimals, multiply as if they were whole numbers, then count the '
             'decimal places of both factors and put the point there.',
             'bd-md-multiplier',
             'Les trois temps : multiplier sans les points, compter les décimales, poser le point.',
             [('simple', 'The point is forgotten while you multiply, and put back at the end.'),
              ('pas_a_pas', 'Multiply without the points. Count the decimal places in both '
                            'numbers. Count that many from the right of the answer.')],
             [('qcm', 1, {'question': 'What do you count to place the point?',
                          'options': ['The decimal places of both numbers',
                                      'The digits of the answer',
                                      'The zeros of the answer']},
               {'index': 0}, 'All the decimal places of the two factors.'),
              ('vrai_faux', 1,
               {'statement': 'While multiplying, the points are left aside.'},
               {'value': True}, 'Yes, and put back at the end.'),
              ('texte_a_trous', 2,
               {'text': 'Count the decimal {{1}} of both numbers.', 'blanks': 1},
               {'values': ['places']}, 'The decimal places.'),
              ('qcm', 3, {'question': 'What is 3.6 × 2.5?',
                          'options': ['9.0', '90', '0.9']},
               {'index': 0}, '36 × 25 = 900, and two decimal places give 9.00.'),
              ('vrai_faux', 4,
               {'statement': 'Decimals are multiplied with a common denominator.'},
               {'value': False}, 'No. That rule belongs to fractions.')]),

            ('relation',
             'A worked multiplication: 0.08 × 4.2. Without the points, 8 × 42 = 336. There are '
             'three decimal places in all, so the answer is 0.336.',
             'bd-md-exemple',
             'Les trois temps de 0.08 × 4.2 : 8 × 42 = 336, trois décimales, 0.336.',
             [('simple', 'Two places in 0.08 and one in 4.2 make three places in the answer.'),
              ('visuel', 'Count three digits from the right of 336, and the point goes there.')],
             [('qcm', 1, {'question': 'How many decimal places are there in 0.08 and 4.2?',
                          'options': ['Three', 'Two', 'Four']},
               {'index': 0}, 'Two in 0.08 and one in 4.2.'),
              ('vrai_faux', 1, {'statement': 'The product 0.08 × 4.2 is equal to 0.336.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Without the points, 8 × 42 gives {{1}}.', 'blanks': 1},
               {'values': ['336']}, 'Three hundred and thirty-six.'),
              ('qcm', 3, {'question': 'What is 0.3 × 0.2?',
                          'options': ['0.06', '0.6', '6']},
               {'index': 0}, '3 × 2 = 6, and two decimal places give 0.06.'),
              ('vrai_faux', 4, {'statement': 'The product 0.3 × 0.2 is equal to 0.6.'},
               {'value': False}, 'No: two decimal places give 0.06.')]),

            ('relation',
             'To divide by a decimal, make the divisor a whole number by multiplying both '
             'numbers by 10, by 100, or by whatever it takes.',
             'bd-md-diviser',
             'Les trois temps : le diviseur doit être entier, on multiplie les deux par 10 ou 100.',
             [('simple', 'Multiplying both numbers by the same thing does not change the '
                         'answer.'),
              ('pas_a_pas', 'Look at the divisor. Count its decimal places. Multiply both '
                            'numbers by 10 for one place, by 100 for two.')],
             [('qcm', 1, {'question': 'What must the divisor become?',
                          'options': ['A whole number', 'A decimal', 'A fraction']},
               {'index': 0}, 'A whole number.'),
              ('vrai_faux', 1,
               {'statement': 'Both numbers are multiplied, not just the divisor.'},
               {'value': True}, 'Yes, otherwise the answer would change.'),
              ('texte_a_trous', 2,
               {'text': 'The divisor must be made a {{1}} number.', 'blanks': 1},
               {'values': ['whole']}, 'A whole number.'),
              ('qcm', 3, {'question': 'What is 7.5 ÷ 0.5?',
                          'options': ['15', '1.5', '3.75']},
               {'index': 0}, '75 ÷ 5 = 15.'),
              ('vrai_faux', 4,
               {'statement': 'Only the divisor is multiplied by 10.'},
               {'value': False}, 'No. Both numbers, or the answer changes.')]),

            ('relation',
             'A worked division: 2.4 ÷ 0.08. Both numbers are multiplied by 100, which gives '
             '240 ÷ 8 = 30.',
             'bd-md-exemple2',
             'Les trois temps de 2.4 ÷ 0.08 : les deux × 100, puis 240 ÷ 8, donc 30.',
             [('simple', 'The divisor 0.08 has two decimal places, so both numbers are '
                         'multiplied by 100.'),
              ('pas_a_pas', '0.08 × 100 = 8, and 2.4 × 100 = 240. Then divide as usual.')],
             [('qcm', 1, {'question': 'In 2.4 ÷ 0.08, what do you multiply both numbers by?',
                          'options': ['100', '10', '1 000']},
               {'index': 0}, '0.08 has two decimal places.'),
              ('vrai_faux', 1, {'statement': 'The quotient 2.4 ÷ 0.08 is equal to 30.'},
               {'value': True}, 'Yes: 240 ÷ 8 = 30.'),
              ('texte_a_trous', 2,
               {'text': 'Multiplied by 100, the number 2.4 becomes {{1}}.', 'blanks': 1},
               {'values': ['240']}, 'Two hundred and forty.'),
              ('qcm', 3, {'question': 'What is 1.2 ÷ 0.4?',
                          'options': ['3', '0.3', '30']},
               {'index': 0}, '12 ÷ 4 = 3.'),
              ('vrai_faux', 4, {'statement': 'The quotient 2.4 ÷ 0.08 is equal to 3.'},
               {'value': False}, 'No. It is 30.')]),
        ],
    ),

    # ------------------------------------------------------------------ 51
    (
        'Decimal word problems', CHAPITRE, None, 51,
        'The key words give the operation: altogether means add, left means subtract, each and '
        'share mean divide, times means multiply. Write the operation down before calculating, '
        'and always give the answer its unit: 48.5 kg - 20.2 kg = 28.3 kg.',
        'bd-pb-couv',
        'Le cadre portant 48.5 kg – 20.2 kg = 28.3 kg.',
        [
            ('relation',
             'Altogether means add. Left or remaining means subtract.',
             'bd-pb-motscles',
             'Deux mots qui commandent : altogether, et left.',
             [('simple', 'The word of the question tells you the operation before you think.'),
              ('pas_a_pas', 'Underline the key word first. Then write the operation.')],
             [('qcm', 1, {'question': 'What operation does altogether call for?',
                          'options': ['Adding', 'Subtracting', 'Dividing']},
               {'index': 0}, 'Adding.'),
              ('vrai_faux', 1, {'statement': 'The word left calls for a subtraction.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The word altogether means you must {{1}}.', 'blanks': 1},
               {'values': ['add']}, 'Add.'),
              ('qcm', 3, {'question': 'He had 9.5 kg and used 2.5 kg. What is left?',
                          'options': ['7 kg', '12 kg', '7.5 kg']},
               {'index': 0}, '9.5 - 2.5 = 7 kg.'),
              ('vrai_faux', 4, {'statement': 'The word remaining calls for an addition.'},
               {'value': False}, 'No. It calls for a subtraction.')]),

            ('relation',
             'Each and share mean divide. Times means multiply.',
             'bd-pb-partage',
             'Deux mots qui commandent : each ou share, et times.',
             [('simple', 'Sharing between people is a division; so many times is a '
                         'multiplication.'),
              ('visuel', 'Four key words, four operations. There is nothing else to choose '
                         'from.')],
             [('qcm', 1, {'question': 'What operation does share call for?',
                          'options': ['Dividing', 'Multiplying', 'Adding']},
               {'index': 0}, 'Dividing.'),
              ('vrai_faux', 1, {'statement': 'The word times calls for a multiplication.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each key word with its operation.',
                                  'gauche': ['altogether', 'left', 'share'],
                                  'droite': ['add', 'subtract', 'divide']},
               {'order': [0, 1, 2]}, 'Add, subtract, divide.'),
              ('qcm', 3, {'question': '7.5 litres shared between 3 jars. How much in each?',
                          'options': ['2.5 litres', '22.5 litres', '4.5 litres']},
               {'index': 0}, '7.5 ÷ 3 = 2.5 litres.'),
              ('vrai_faux', 4, {'statement': 'The word each often calls for a division.'},
               {'value': True}, 'Yes, when something is being shared.')]),

            ('relation',
             'The operation is written down before it is calculated. A problem solved in the '
             'head leaves nothing to check.',
             'bd-pb-operation',
             'Les trois temps : lire ce qu’on cherche, écrire l’opération, calculer.',
             [('simple', 'Write the operation first. Then do it. Two separate moments.'),
              ('pas_a_pas', 'Read what is asked. Write the operation. Calculate. Write the '
                            'answer with its unit.')],
             [('qcm', 1, {'question': 'What do you write before calculating?',
                          'options': ['The operation', 'The answer', 'The unit']},
               {'index': 0}, 'The operation.'),
              ('vrai_faux', 1, {'statement': 'The operation is written before it is done.'},
               {'value': True}, 'Yes, so that it can be checked.'),
              ('chronologie', 2, {'question': 'Put the three steps in the right order.',
                                  'tokens': ['Read what is asked', 'Write the operation',
                                             'Calculate']},
               {'order': [0, 1, 2]}, 'Read, write, calculate.'),
              ('qcm', 3, {'question': 'Why write the operation first?',
                          'options': ['So the work can be checked',
                                      'To make the page longer',
                                      'To make the answer bigger']},
               {'index': 0}, 'So that the work can be checked.'),
              ('vrai_faux', 4,
               {'statement': 'A problem done in the head leaves nothing to check.'},
               {'value': True}, 'Yes, which is why it is written.')]),

            ('relation',
             'The answer always carries its unit: 48.5 kg - 20.2 kg = 28.3 kg, and not 28.3 on '
             'its own.',
             'bd-pb-unite',
             'La soustraction 48.5 – 20.2 posée, et la réponse 28.3 kg.',
             [('simple', 'Kilograms were asked for, so kilograms are answered.'),
              ('visuel', 'Write the unit straight after the number, before you put your pen '
                         'down.')],
             [('qcm', 1, {'question': 'What is 48.5 kg - 20.2 kg?',
                          'options': ['28.3 kg', '28.3', '68.7 kg']},
               {'index': 0}, 'Twenty-eight point three kilograms.'),
              ('vrai_faux', 1, {'statement': 'Writing 28.3 without its unit is a full answer.'},
               {'value': False}, 'No. 28.3 what?'),
              ('texte_a_trous', 2,
               {'text': 'The answer always carries its {{1}}.', 'blanks': 1},
               {'values': ['unit']}, 'Its unit.'),
              ('qcm', 3, {'question': 'He buys 2.5 litres and 1.75 litres. How much altogether?',
                          'options': ['4.25 litres', '4.25', '0.75 litres']},
               {'index': 0}, '2.50 + 1.75 = 4.25 litres.'),
              ('vrai_faux', 4, {'statement': 'The unit may be left out when the answer is big.'},
               {'value': False}, 'No. It is part of the answer, always.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues, trous = set(), 0, 0, 0
    titres = [l[0] for l in LECONS]
    assert len(set(titres)) == len(titres), 'titre en double'

    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 400, 'résumé trop long (%d) : %s' % (len(resume), titre)
        assert date is None or len(date) == 10, date
        assert img not in cles, 'image en double : ' + img
        cles.add(img)
        for kind, phrase, nimg, nprompt, expl, items in notions:
            notions_vues += 1
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 180, 'notion trop longue (%d) : %s' % (len(phrase), phrase)
            assert nimg not in cles, 'image en double : ' + nimg
            cles.add(nimg)
            for registre, corps in expl:
                assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), \
                    registre
                assert len(corps) <= 200, 'explication trop longue : ' + corps
            niveaux = set()
            for ikind, niveau, payload, answer, explain in items:
                total += 1
                niveaux.add(niveau)
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, \
                        'question trop longue (%d) : %s' % (len(payload['question']),
                                                            payload['question'])
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 70, 'option trop longue : ' + o
                    bonne = len(options[answer['index']])
                    autres = [len(o) for k, o in enumerate(options) if k != answer['index']]
                    assert bonne <= max(autres) * 2, \
                        'bonne réponse bien plus longue que les autres : ' + payload['question']
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']),
                                                               payload['statement'])
                elif ikind == 'texte_a_trous':
                    trous += 1
                    n = payload['text'].count('{{')
                    assert n == len(answer['values']) == payload['blanks'], payload
                    assert n <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        assert v == v.strip() != '', 'réponse mal cadrée : ' + repr(v)
                        assert set(v) <= TAPABLE, 'réponse non tapable au clavier : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie'
                                   else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'chronologie':
                        assert len(set(payload['tokens'])) == longueur, \
                            'jeton en double : ' + str(payload['tokens'])
                    else:
                        assert len(payload['gauche']) == len(payload['droite']), payload
                        assert len(set(payload['droite'])) == len(payload['droite']), \
                            'deux étiquettes identiques à droite : ' + str(payload['droite'])
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-brayne-decimaux.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    manquantes = cles - dessinees
    inutiles = dessinees - cles
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(
        sorted(manquantes))
    assert not inutiles, 'images dessinées mais jamais utilisées : ' + ', '.join(sorted(inutiles))
    return len(cles), total, notions_vues, trous


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
    images, items, notions, trous = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-decimaux.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-38s %d notions  %d questions'
              % (ordre, titre, len(ns), sum(len(n[5]) for n in ns)))
    print(chemin)
