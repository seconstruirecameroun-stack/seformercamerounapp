# -*- coding: utf-8 -*-
"""
Sept leçons sur les fractions pour BRAYNE (CM1) — fiche de révision
« CM1 - MATHEMATICS - REVISION SHEET - FRACTIONS », 4 pages, donnée par le
père le 8 novembre 2026.

RIEN DE CE SUJET N-ÉTAIT EN BASE. Ses neuf leçons de mathématiques
portaient les diagrammes de Venn, les capacités, la moyenne, le
pourcentage, les problèmes et les angles. Les treize sections de cette
fiche sont donc toutes reprises, et réparties en sept leçons :

  sections 1        ce qu-est une fraction, numérateur et dénominateur
  section 2         les quatre types : propre, impropre, mixte, unitaire
  sections 3-4      fractions équivalentes, et comparer
  section 5         passer de l-impropre au mixte, et l-inverse
  sections 6-7      additionner et soustraire
  sections 8-9      multiplier et diviser
  sections 10-11    la fraction d-une quantité, et les problèmes

LES EXEMPLES SONT CEUX DE LA FICHE, aux chiffres près : 3/5, 7/4, 11/4,
3/8 + 2/8, 1/2 + 1/3, 2/3 × 5/7, 2/3 ÷ 4/5, 3/5 de 40. Un enfant qui
révise reconnaît ses propres nombres ; en changer n-apporterait rien et
lui ferait croire à une autre leçon.

LA FICHE LAISSE 3/9 ET 10/12 SANS LES SIMPLIFIER. On ne corrige pas sa
fiche — ce sont ses réponses attendues — mais la simplification est dite
dans une explication, parce qu-elle est au programme de la section 3 de
cette même fiche.

DEUX CONTRAINTES D-ÉCRITURE, toutes deux vérifiées plus bas.

Le clavier de l-application n-a pas de barre de fraction, ni de touche
espace. Aucune réponse à taper n-est donc une fraction : ce sont des mots,
et le script vérifie chaque caractère contre les touches qui existent.

Les quatre étapes sont obligatoires sur chaque notion, et le Défi étant
chronométré, il ne porte que des questions qui se jouent en un geste.

Usage :  python work/lecons-brayne-fractions.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-fractions.py. ')

MATIERE = 'Mathématiques'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'en'
CHAPITRE = 'Fractions'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

LECONS = [
    # ------------------------------------------------------------------ 53
    (
        'What a fraction is', CHAPITRE, None, 53,
        'A fraction shows one or more equal parts of a whole. The numerator is the top number: '
        'it tells how many parts are taken. The denominator is the bottom number: it tells how '
        'many equal parts make the whole. In 3/5, 3 is the numerator and 5 is the denominator.',
        'bf-wh-couv',
        'Une barre partagée en cinq parts égales, trois coloriées.',
        [
            ('definition',
             'A fraction shows one or more equal parts of a whole.',
             'bf-wh-def',
             'Trois parts prises sur cinq parts égales.',
             [('simple', 'The whole is cut into equal parts, and the fraction says how many of '
                         'them you take.'),
              ('analogie', 'A mango cut into five equal pieces: take three, and you have taken '
                           'three fifths of the mango.')],
             [('qcm', 1, {'question': 'What does a fraction show?',
                          'options': ['Equal parts of a whole', 'The biggest number',
                                      'A times table']},
               {'index': 0}, 'One or more equal parts of a whole.'),
              ('vrai_faux', 1, {'statement': 'A fraction shows parts of a whole.'},
               {'value': True}, 'Yes, and the parts are equal.'),
              ('texte_a_trous', 2,
               {'text': 'A fraction shows one or more equal {{1}} of a whole.', 'blanks': 1},
               {'values': ['parts']}, 'Equal parts.'),
              ('qcm', 3, {'question': 'A cake is cut into 4 equal parts. You take 1. What do you take?',
                          'options': ['1/4 of the cake', '4/1 of the cake', '1/3 of the cake']},
               {'index': 0}, 'One part out of four: 1/4.'),
              ('vrai_faux', 4, {'statement': 'The parts of a fraction may be of different sizes.'},
               {'value': False}, 'No. The parts must be equal.')]),

            ('definition',
             'The numerator is the top number of a fraction. It tells how many parts are taken.',
             'bf-wh-num',
             'La fraction 3/5 écrite en grand, trait de fraction tracé.',
             [('simple', 'In 3/5, the numerator is 3: three parts are taken.'),
              ('visuel', 'The numerator sits on top, like the part you lift off the plate.')],
             [('qcm', 1, {'question': 'Where is the numerator?',
                          'options': ['On top', 'At the bottom', 'On the left']},
               {'index': 0}, 'The top number.'),
              ('vrai_faux', 1, {'statement': 'In 3/5, the numerator is 3.'},
               {'value': True}, 'Yes: the top number.'),
              ('texte_a_trous', 2,
               {'text': 'The top number of a fraction is the {{1}}.', 'blanks': 1},
               {'values': ['numerator']}, 'The numerator.'),
              ('qcm', 3, {'question': 'In 7/8, what is the numerator?',
                          'options': ['7', '8', '15']},
               {'index': 0}, 'The top number: 7.'),
              ('vrai_faux', 4, {'statement': 'The numerator says how many parts are taken.'},
               {'value': True}, 'Yes.')]),

            ('definition',
             'The denominator is the bottom number of a fraction. It tells how many equal parts '
             'make the whole.',
             'bf-wh-den',
             'La fraction 3/5, numérateur et dénominateur nommés.',
             [('simple', 'In 3/5, the denominator is 5: the whole was cut into five parts.'),
              ('pas_a_pas', 'Read the bottom number first: it tells you how to cut. Then read '
                            'the top one: it tells you how many to take.')],
             [('qcm', 1, {'question': 'What does the denominator tell you?',
                          'options': ['How many equal parts make the whole',
                                      'How many parts are taken', 'The name of the fraction']},
               {'index': 0}, 'How many equal parts the whole is cut into.'),
              ('vrai_faux', 1, {'statement': 'In 3/5, the denominator is 5.'},
               {'value': True}, 'Yes: the bottom number.'),
              ('texte_a_trous', 2,
               {'text': 'The bottom number of a fraction is the {{1}}.', 'blanks': 1},
               {'values': ['denominator']}, 'The denominator.'),
              ('qcm', 3, {'question': 'In 7/8, what is the denominator?',
                          'options': ['8', '7', '1']},
               {'index': 0}, 'The bottom number: 8.'),
              ('vrai_faux', 4,
               {'statement': 'The denominator says how many parts are taken.'},
               {'value': False}, 'No. That is the numerator.')]),

            ('relation',
             'The parts of a fraction must be equal. Four parts of different sizes are not '
             'quarters, whatever their number.',
             'bf-wh-egales',
             'Une barre en quatre parts numérotées, toutes de même longueur.',
             [('simple', 'Cut into four equal parts, each one is a quarter.'),
              ('visuel', 'If one part is bigger than the others, no fraction can name it.')],
             [('qcm', 1, {'question': 'How must the parts of a fraction be?',
                          'options': ['Equal', 'Different', 'Coloured']},
               {'index': 0}, 'Equal.'),
              ('vrai_faux', 1,
               {'statement': 'A whole cut into four equal parts gives quarters.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The parts of a fraction are always {{1}}.', 'blanks': 1},
               {'values': ['equal']}, 'Equal.'),
              ('association', 3, {'question': 'Match each cut with the name of one part.',
                                  'gauche': ['into 2', 'into 3', 'into 4'],
                                  'droite': ['a half', 'a third', 'a quarter']},
               {'order': [0, 1, 2]}, 'Two parts: halves. Three: thirds. Four: quarters.'),
              ('vrai_faux', 4,
               {'statement': 'Four parts of different sizes can still be called quarters.'},
               {'value': False}, 'No. Quarters are equal parts.')]),
        ],
    ),

    # ------------------------------------------------------------------ 54
    (
        'The types of fractions', CHAPITRE, None, 54,
        'A proper fraction has a numerator smaller than its denominator, like 3/5. An improper '
        'fraction has a numerator as big or bigger, like 7/4. A mixed number is a whole number '
        'and a fraction, like 2 and 1/3. A unit fraction has 1 as its numerator, like 1/7.',
        'bf-ty-couv',
        'Trois fractions écrites côte à côte : 3/5, 7/4, 1/7.',
        [
            ('definition',
             'A proper fraction has a numerator smaller than its denominator. It is worth less '
             'than one whole. Example: 3/5.',
             'bf-ty-propre',
             'Une barre de cinq parts, trois coloriées : moins que le tout.',
             [('simple', 'The top is smaller than the bottom, so you have not taken the whole.'),
              ('visuel', 'On the bar, some parts are still white. That is a proper fraction.')],
             [('qcm', 1, {'question': 'In a proper fraction, the numerator is…',
                          'options': ['smaller than the denominator',
                                      'bigger than the denominator', 'always 1']},
               {'index': 0}, 'Smaller than the denominator.'),
              ('vrai_faux', 1, {'statement': 'The fraction 3/5 is a proper fraction.'},
               {'value': True}, 'Yes: 3 is smaller than 5.'),
              ('texte_a_trous', 2,
               {'text': 'A fraction worth less than one whole is a {{1}} fraction.', 'blanks': 1},
               {'values': ['proper']}, 'A proper fraction.'),
              ('qcm', 3, {'question': 'Which one is a proper fraction?',
                          'options': ['2/9', '9/2', '9/9']},
               {'index': 0}, '2 is smaller than 9.'),
              ('vrai_faux', 4, {'statement': 'A proper fraction is worth more than one whole.'},
               {'value': False}, 'No. It is worth less than one.')]),

            ('definition',
             'An improper fraction has a numerator as big as, or bigger than, its denominator. '
             'It is worth one or more. Example: 7/4.',
             'bf-ty-impropre',
             'Improper fraction 7/4 : le haut plus grand que le bas, donc plus que 1.',
             [('simple', 'The top is bigger, so you have more than one whole.'),
              ('analogie', '7/4 is seven quarters: one whole cake and three quarters of a '
                           'second one.')],
             [('qcm', 1, {'question': 'In an improper fraction, the numerator is…',
                          'options': ['as big or bigger than the denominator',
                                      'always smaller than the denominator',
                                      'always the number 1 exactly']},
               {'index': 0}, 'As big as, or bigger than, the denominator.'),
              ('vrai_faux', 1, {'statement': 'The fraction 7/4 is an improper fraction.'},
               {'value': True}, 'Yes: 7 is bigger than 4.'),
              ('texte_a_trous', 2,
               {'text': 'A fraction whose top is bigger than its bottom is {{1}}.', 'blanks': 1},
               {'values': ['improper']}, 'Improper.'),
              ('qcm', 3, {'question': 'Which one is an improper fraction?',
                          'options': ['9/2', '2/9', '1/9']},
               {'index': 0}, '9 is bigger than 2.'),
              ('vrai_faux', 4, {'statement': 'An improper fraction is worth less than one.'},
               {'value': False}, 'No. It is worth one or more.')]),

            ('definition',
             'A mixed number is a whole number written with a fraction. Example: 2 and 1/3.',
             'bf-ty-mixte',
             'Mixed number 2 et 1/3 : un entier et une fraction, écrits ensemble.',
             [('simple', 'Two whole cakes and one third of a third cake: 2 and 1/3.'),
              ('visuel', 'The whole number is written first, then the fraction beside it.')],
             [('qcm', 1, {'question': 'What is a mixed number?',
                          'options': ['A whole number and a fraction', 'Two fractions',
                                      'A fraction with 1 on top']},
               {'index': 0}, 'A whole number written with a fraction.'),
              ('vrai_faux', 1, {'statement': 'The number 2 and 1/3 is a mixed number.'},
               {'value': True}, 'Yes: a whole number and a fraction.'),
              ('texte_a_trous', 2,
               {'text': 'A whole number written with a fraction is a {{1}} number.', 'blanks': 1},
               {'values': ['mixed']}, 'A mixed number.'),
              ('qcm', 3, {'question': 'Which one is a mixed number?',
                          'options': ['3 and 1/2', '3 over 2', '1 over 2']},
               {'index': 0}, 'A whole number and a fraction together.'),
              ('vrai_faux', 4, {'statement': 'A mixed number is always smaller than one.'},
               {'value': False}, 'No. It holds at least one whole.')]),

            ('definition',
             'A unit fraction has 1 as its numerator. It is one single part of the whole. '
             'Example: 1/7.',
             'bf-ty-unitaire',
             'Une barre de sept parts, une seule coloriée.',
             [('simple', 'One part, and one only, out of all the parts.'),
              ('visuel', 'On the bar, exactly one cell is coloured.')],
             [('qcm', 1, {'question': 'What is the numerator of a unit fraction?',
                          'options': ['1', '7', 'The denominator']},
               {'index': 0}, 'Always 1.'),
              ('vrai_faux', 1, {'statement': 'The fraction 1/7 is a unit fraction.'},
               {'value': True}, 'Yes: its numerator is 1.'),
              ('texte_a_trous', 2,
               {'text': 'A fraction whose numerator is 1 is a {{1}} fraction.', 'blanks': 1},
               {'values': ['unit']}, 'A unit fraction.'),
              ('qcm', 3, {'question': 'Which one is a unit fraction?',
                          'options': ['1/9', '2/9', '9/1']},
               {'index': 0}, 'Its numerator is 1.'),
              ('vrai_faux', 4, {'statement': 'The fraction 2/7 is a unit fraction.'},
               {'value': False}, 'No. Its numerator is 2.')]),
        ],
    ),

    # ------------------------------------------------------------------ 55
    (
        'Equivalent fractions and comparing', CHAPITRE, None, 55,
        'Equivalent fractions have the same value: 1/2 = 2/4 = 3/6. You find them by multiplying '
        'or dividing the numerator and the denominator by the same number. To compare: with the '
        'same denominator, look at the numerators; with the same numerator, the smaller '
        'denominator wins.',
        'bf-eq-couv',
        'Deux barres de même longueur : une moitié, et deux quarts.',
        [
            ('definition',
             'Equivalent fractions have the same value, written in different ways: '
             '1/2 = 2/4 = 3/6.',
             'bf-eq-equivalent',
             'Une barre 1/2 et une barre 2/4 : la même longueur coloriée.',
             [('simple', 'Different numbers, same amount. Half a cake is also two quarters of '
                         'that cake.'),
              ('visuel', 'On two bars of the same length, the coloured parts end at the same '
                         'place.')],
             [('qcm', 1, {'question': 'What do equivalent fractions have?',
                          'options': ['The same value', 'The same numerator',
                                      'The same number of digits']},
               {'index': 0}, 'The same value, written differently.'),
              ('vrai_faux', 1, {'statement': 'The fractions 1/2 and 2/4 are equivalent.'},
               {'value': True}, 'Yes: both are a half.'),
              ('texte_a_trous', 2,
               {'text': 'Fractions with the same value are called {{1}}.', 'blanks': 1},
               {'values': ['equivalent']}, 'Equivalent fractions.'),
              ('qcm', 3, {'question': 'Which fraction is equivalent to 1/2?',
                          'options': ['3/6', '2/5', '1/4']},
               {'index': 0}, '3 × 2 = 6, so 3/6 is a half.'),
              ('vrai_faux', 4, {'statement': 'The fractions 1/3 and 1/4 are equivalent.'},
               {'value': False}, 'No. A third is bigger than a quarter.')]),

            ('relation',
             'To find an equivalent fraction, multiply or divide the numerator and the '
             'denominator by the same number.',
             'bf-eq-methode',
             '1 × 2 = 2, puis 2 × 2 = 4, donc 1/2 = 2/4.',
             [('simple', 'What you do on top, you do at the bottom. Both, or neither.'),
              ('pas_a_pas', 'Choose a number. Multiply the top by it. Multiply the bottom by the '
                            'same one. The value has not changed.')],
             [('qcm', 1, {'question': 'What do you multiply to find an equivalent fraction?',
                          'options': ['Top and bottom by the same number',
                                      'Only the top of the fraction',
                                      'Only the bottom of the fraction']},
               {'index': 0}, 'Both, by the same number.'),
              ('vrai_faux', 1,
               {'statement': 'Multiplying only the numerator keeps the same value.'},
               {'value': False}, 'No. You must multiply the denominator too.'),
              ('texte_a_trous', 2,
               {'text': 'Multiply the top and the bottom by the {{1}} number.', 'blanks': 1},
               {'values': ['same']}, 'By the same number.'),
              ('qcm', 3, {'question': 'Multiply 2/3 by 4 on top and bottom. What do you get?',
                          'options': ['8/12', '8/3', '6/12']},
               {'index': 0}, '2 × 4 = 8 and 3 × 4 = 12.'),
              ('vrai_faux', 4,
               {'statement': 'Dividing top and bottom by the same number also works.'},
               {'value': True}, 'Yes: 3/9 divided by 3 gives 1/3.')]),

            ('relation',
             'When two fractions have the same denominator, the one with the bigger numerator is '
             'the bigger fraction.',
             'bf-eq-memedenom',
             'Deux barres de huit parts : trois coloriées, puis cinq.',
             [('simple', 'Same size of parts, so the one with more parts is bigger.'),
              ('visuel', 'Five eighths cover more of the bar than three eighths.')],
             [('qcm', 1, {'question': 'Same denominator: how do you compare?',
                          'options': ['Look at the numerators', 'Look at the denominators',
                                      'Add them first']},
               {'index': 0}, 'The bigger numerator wins.'),
              ('vrai_faux', 1, {'statement': 'The fraction 5/8 is bigger than 3/8.'},
               {'value': True}, 'Yes: five parts beat three of the same size.'),
              ('texte_a_trous', 2,
               {'text': 'With the same denominator, compare the {{1}}.', 'blanks': 1},
               {'values': ['numerators']}, 'The numerators.'),
              ('qcm', 3, {'question': 'Which one is the biggest?',
                          'options': ['7/9', '4/9', '2/9']},
               {'index': 0}, 'Same bottom, so the biggest top wins.'),
              ('vrai_faux', 4, {'statement': 'The fraction 2/7 is bigger than 6/7.'},
               {'value': False}, 'No: 2 is smaller than 6.')]),

            ('relation',
             'When two fractions have the same numerator, the one with the smaller denominator '
             'is the bigger fraction.',
             'bf-eq-memenum',
             'Une barre 1/3 et une barre 1/6 : le tiers est plus long.',
             [('simple', 'Fewer parts means bigger parts. A third is bigger than a sixth.'),
              ('analogie', 'One cake shared between three children, or between six: with three, '
                           'each one gets more.')],
             [('qcm', 1, {'question': 'Same numerator: which fraction is bigger?',
                          'options': ['The one with the smaller denominator',
                                      'The one with the bigger denominator',
                                      'They are equal']},
               {'index': 0}, 'Fewer parts, so bigger parts.'),
              ('vrai_faux', 1, {'statement': 'The fraction 1/3 is bigger than 1/6.'},
               {'value': True}, 'Yes: a third is a bigger part.'),
              ('texte_a_trous', 2,
               {'text': 'With the same numerator, the {{1}} denominator wins.', 'blanks': 1},
               {'values': ['smaller']}, 'The smaller denominator.'),
              ('qcm', 3, {'question': 'Which one is the biggest?',
                          'options': ['2/3', '2/5', '2/9']},
               {'index': 0}, 'Same top, smallest bottom.'),
              ('vrai_faux', 4, {'statement': 'The fraction 1/10 is bigger than 1/2.'},
               {'value': False}, 'No. A tenth is a very small part.')]),

            ('relation',
             'When the denominators are different, change the fractions so that they share a '
             'common denominator, then compare the numerators.',
             'bf-eq-commun',
             '1/2 et 1/3 deviennent 3/6 et 2/6 : le dénominateur commun est 6.',
             [('simple', 'You cannot compare thirds with halves. Turn both into sixths first.'),
              ('pas_a_pas', 'Find a number both denominators divide into. Change each fraction '
                            'into that denominator. Then compare the tops.')],
             [('qcm', 1, {'question': 'Different denominators: what do you do first?',
                          'options': ['Find a common denominator', 'Add the denominators',
                                      'Take the biggest numerator']},
               {'index': 0}, 'Find a common denominator.'),
              ('vrai_faux', 1, {'statement': 'A common denominator for 1/2 and 1/3 is 6.'},
               {'value': True}, 'Yes: 2 and 3 both divide into 6.'),
              ('texte_a_trous', 2,
               {'text': 'With different denominators, look for a {{1}} denominator.', 'blanks': 1},
               {'values': ['common']}, 'A common denominator.'),
              ('qcm', 3, {'question': 'Changed into sixths, what does 1/2 become?',
                          'options': ['3/6', '2/6', '1/6']},
               {'index': 0}, '1 × 3 = 3 and 2 × 3 = 6.'),
              ('vrai_faux', 4, {'statement': 'Thirds and halves can be compared as they are.'},
               {'value': False}, 'No. Their parts are not the same size.')]),
        ],
    ),

    # ------------------------------------------------------------------ 56
    (
        'Improper fractions and mixed numbers', CHAPITRE, None, 56,
        'To change an improper fraction into a mixed number, divide the numerator by the '
        'denominator: 11/4 = 2 remainder 3 = 2 and 3/4. To go back, multiply the whole number by '
        'the denominator and add the numerator: 3 and 2/5 = 17/5. Both write the same amount.',
        'bf-im-couv',
        '11/4 = 2 et 3/4, les deux écritures côte à côte.',
        [
            ('relation',
             'To change an improper fraction into a mixed number, divide the numerator by the '
             'denominator: 11/4 = 2 remainder 3 = 2 and 3/4.',
             'bf-im-versmixte',
             'La division 11 ÷ 4, le quotient 2, le reste 3 sur 4.',
             [('simple', 'The quotient gives the whole number; the remainder goes on top of the '
                         'same denominator.'),
              ('pas_a_pas', 'Divide. Write the quotient. Write the remainder over the '
                            'denominator, which never changes.')],
             [('qcm', 1, {'question': 'To change 11/4 into a mixed number, what do you do?',
                          'options': ['Divide 11 by 4', 'Multiply 11 by 4', 'Add 11 and 4']},
               {'index': 0}, 'Divide the numerator by the denominator.'),
              ('vrai_faux', 1, {'statement': 'The fraction 11/4 is the same as 2 and 3/4.'},
               {'value': True}, 'Yes: 11 ÷ 4 = 2 remainder 3.'),
              ('texte_a_trous', 2,
               {'text': 'The {{1}} of the division goes over the denominator.', 'blanks': 1},
               {'values': ['remainder']}, 'The remainder.'),
              ('qcm', 3, {'question': 'What is 7/2 as a mixed number?',
                          'options': ['3 and 1/2', '2 and 3/2', '3 and 1/3']},
               {'index': 0}, '7 ÷ 2 = 3 remainder 1.'),
              ('vrai_faux', 4, {'statement': 'The denominator changes when you divide.'},
               {'value': False}, 'No. It stays the same.')]),

            ('relation',
             'To change a mixed number into an improper fraction, multiply the whole number by '
             'the denominator and add the numerator: 3 and 2/5 = 17/5.',
             'bf-im-versimpropre',
             '3 × 5 = 15, puis 15 + 2 = 17, donc 17/5.',
             [('simple', 'Three whole cakes cut into fifths make fifteen fifths; add the two '
                         'you had, and that is seventeen.'),
              ('pas_a_pas', 'Multiply, then add, then write the answer over the same '
                            'denominator.')],
             [('qcm', 1, {'question': 'In 3 and 2/5, what do you multiply first?',
                          'options': ['3 by 5', '3 by 2', '2 by 5']},
               {'index': 0}, 'The whole number by the denominator.'),
              ('vrai_faux', 1, {'statement': 'The number 3 and 2/5 is the same as 17/5.'},
               {'value': True}, 'Yes: 3 × 5 + 2 = 17.'),
              ('texte_a_trous', 2,
               {'text': 'Multiply the whole by the denominator, then {{1}} the numerator.',
                'blanks': 1},
               {'values': ['add']}, 'Then add the numerator.'),
              ('qcm', 3, {'question': 'What is 2 and 1/3 as an improper fraction?',
                          'options': ['7/3', '6/3', '5/3']},
               {'index': 0}, '2 × 3 + 1 = 7.'),
              ('vrai_faux', 4, {'statement': 'In 2 and 1/3, you add before you multiply.'},
               {'value': False}, 'No: multiply first, then add.')]),

            ('relation',
             'An improper fraction and its mixed number are the same amount, written in two '
             'ways: 11/4 is two whole ones and three quarters.',
             'bf-im-memequantite',
             'Deux barres pleines et une barre aux trois quarts : 11/4.',
             [('simple', 'Nothing is gained or lost in the change. Only the writing changes.'),
              ('visuel', 'Two full bars, then three parts out of four: that is 11/4.')],
             [('qcm', 1, {'question': 'How many whole ones are there in 11/4?',
                          'options': ['2', '3', '11']},
               {'index': 0}, 'Two whole ones, and three quarters left.'),
              ('vrai_faux', 1,
               {'statement': 'An improper fraction and its mixed number are the same amount.'},
               {'value': True}, 'Yes: only the writing changes.'),
              ('texte_a_trous', 2,
               {'text': 'The two writings show the same {{1}}.', 'blanks': 1},
               {'values': ['amount']}, 'The same amount.'),
              ('qcm', 3, {'question': 'How many whole ones are there in 9/4?',
                          'options': ['2', '4', '9']},
               {'index': 0}, '9 ÷ 4 = 2 remainder 1.'),
              ('vrai_faux', 4, {'statement': 'Changing 11/4 into 2 and 3/4 makes it bigger.'},
               {'value': False}, 'No. It is the very same amount.')]),

            ('relation',
             'Before multiplying or dividing, a mixed number must be changed into an improper '
             'fraction. Otherwise the calculation cannot be done.',
             'bf-im-avantcalcul',
             'Trois temps : un nombre mixte ne se calcule pas, on le change, puis on calcule.',
             [('simple', 'You cannot multiply a whole number and a fraction at the same time.'),
              ('pas_a_pas', 'Change first, calculate afterwards. Always in that order.')],
             [('qcm', 1, {'question': 'What do you do with a mixed number before multiplying?',
                          'options': ['Change it into an improper fraction',
                                      'Leave it as it is', 'Take away the whole number']},
               {'index': 0}, 'Change it into an improper fraction.'),
              ('vrai_faux', 1,
               {'statement': 'A mixed number can be multiplied just as it is written.'},
               {'value': False}, 'No. Change it into an improper fraction first.'),
              ('texte_a_trous', 2,
               {'text': 'Before multiplying, change a mixed number into an {{1}} fraction.',
                'blanks': 1},
               {'values': ['improper']}, 'An improper fraction.'),
              ('qcm', 3, {'question': 'To multiply 2 and 1/3 by 4, what do you write first?',
                          'options': ['7/3', '2/3', '3/7']},
               {'index': 0}, '2 × 3 + 1 = 7, so 7/3.'),
              ('vrai_faux', 4,
               {'statement': 'The same rule holds for dividing mixed numbers.'},
               {'value': True}, 'Yes: change them first.')]),
        ],
    ),

    # ------------------------------------------------------------------ 57
    (
        'Adding and subtracting fractions', CHAPITRE, None, 57,
        'With the same denominator, keep the denominator and add or subtract the numerators '
        'only: 3/8 + 2/8 = 5/8. With different denominators, find a common denominator first, '
        'change each fraction, then add: 1/2 + 1/3 = 3/6 + 2/6 = 5/6.',
        'bf-ad-couv',
        'Le calcul 3/8 + 2/8 = 5/8 posé en fractions.',
        [
            ('relation',
             'With the same denominator, keep the denominator and add or subtract the numerators '
             'only: 3/8 + 2/8 = 5/8.',
             'bf-ad-memedenom',
             '3/8 + 2/8 = 5/8 : le bas ne change pas, on ajoute les hauts.',
             [('simple', 'Three eighths and two eighths make five eighths. The size of the part '
                         'has not changed.'),
              ('analogie', 'Three mangoes and two mangoes make five mangoes, not five of '
                           'something else.')],
             [('qcm', 1, {'question': 'Same denominator: what do you add?',
                          'options': ['The numerators only', 'The denominators only',
                                      'Both of them']},
               {'index': 0}, 'The numerators. The denominator does not change.'),
              ('vrai_faux', 1, {'statement': 'The sum 3/8 + 2/8 is equal to 5/8.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'With the same denominator, you {{1}} the denominator.', 'blanks': 1},
               {'values': ['keep']}, 'You keep it.'),
              ('qcm', 3, {'question': 'What is 7/9 - 4/9?',
                          'options': ['3/9', '3/0', '11/9']},
               {'index': 0}, '7 - 4 = 3, and the denominator stays 9. (3/9 is also 1/3.)'),
              ('vrai_faux', 4, {'statement': 'The sum 3/8 + 2/8 is equal to 5/16.'},
               {'value': False}, 'No. The denominators are not added.')]),

            ('relation',
             'With different denominators, find a common denominator, change each fraction into '
             'an equivalent one, and only then add or subtract.',
             'bf-ad-commun',
             'Les trois temps : chercher le commun, changer, ajouter.',
             [('simple', 'Halves and thirds cannot be added. Turn both into sixths, and they '
                         'can.'),
              ('pas_a_pas', 'Find the common denominator. Change each fraction. Add the '
                            'numerators. The denominator stays the common one.')],
             [('qcm', 1, {'question': 'Different denominators: what comes first?',
                          'options': ['Finding a common denominator',
                                      'Adding the numerators', 'Adding the denominators']},
               {'index': 0}, 'Finding a common denominator.'),
              ('vrai_faux', 1,
               {'statement': 'Fractions with different denominators are added as they are.'},
               {'value': False}, 'No. They must share a denominator first.'),
              ('chronologie', 2, {'question': 'Put the three steps in the right order.',
                                  'tokens': ['Find the common denominator',
                                             'Change each fraction',
                                             'Add the numerators']},
               {'order': [0, 1, 2]}, 'Common denominator, change, then add.'),
              ('qcm', 3, {'question': 'What is the common denominator of 1/4 and 1/6?',
                          'options': ['12', '10', '24']},
               {'index': 0}, '4 and 6 both divide into 12.'),
              ('vrai_faux', 4,
               {'statement': 'The common denominator is usually the LCM of the two.'},
               {'value': True}, 'Yes, the lowest common multiple.')]),

            ('relation',
             'A worked example: 1/2 + 1/3 = 3/6 + 2/6 = 5/6. The common denominator is 6, and '
             'each fraction is changed before the numerators are added.',
             'bf-ad-exemple',
             'Le calcul 1/2 + 1/3, puis 3/6 + 2/6, puis 5/6.',
             [('simple', 'A half is three sixths; a third is two sixths; together, five '
                         'sixths.'),
              ('visuel', 'Write the three lines one under the other, as at school.')],
             [('qcm', 1, {'question': 'In 1/2 + 1/3, what is the common denominator?',
                          'options': ['6', '5', '2']},
               {'index': 0}, 'Six: both 2 and 3 divide into it.'),
              ('vrai_faux', 1, {'statement': 'Changed into sixths, 1/2 becomes 3/6.'},
               {'value': True}, 'Yes: 1 × 3 and 2 × 3.'),
              ('texte_a_trous', 2,
               {'text': 'The sum of 3/6 and 2/6 has {{1}} for its numerator.', 'blanks': 1},
               {'values': ['5']}, 'Five sixths.'),
              ('qcm', 3, {'question': 'What is 1/2 + 1/3?',
                          'options': ['5/6', '2/5', '1/5']},
               {'index': 0}, '3/6 + 2/6 = 5/6.'),
              ('vrai_faux', 4, {'statement': 'The answer to 1/2 + 1/3 is 2/5.'},
               {'value': False}, 'No. That adds the tops and the bottoms, which is wrong.')]),

            ('relation',
             'The denominators are never added. In 3/8 + 2/8, the answer is 5/8, never 5/16.',
             'bf-ad-piege',
             'Le piège : 3/8 + 2/8 = 5/8, et jamais 5/16.',
             [('simple', 'The denominator says the size of the part. That size does not change '
                         'because you take more parts.'),
              ('visuel', 'If 5/16 were right, taking more parts would make each part smaller. '
                         'That cannot be.')],
             [('qcm', 1, {'question': 'What happens to the denominator when you add?',
                          'options': ['It stays the same', 'It is added too', 'It is doubled']},
               {'index': 0}, 'It stays the same.'),
              ('vrai_faux', 1, {'statement': 'Adding fractions means adding the denominators.'},
               {'value': False}, 'No. Only the numerators are added.'),
              ('texte_a_trous', 2,
               {'text': 'The denominators are {{1}} added together.', 'blanks': 1},
               {'values': ['never']}, 'Never.'),
              ('qcm', 3, {'question': 'What is 1/5 + 2/5?',
                          'options': ['3/5', '3/10', '2/10']},
               {'index': 0}, 'Three fifths. The denominator stays 5.'),
              ('vrai_faux', 4, {'statement': 'The sum 1/5 + 2/5 is equal to 3/10.'},
               {'value': False}, 'No. It is 3/5.')]),
        ],
    ),

    # ------------------------------------------------------------------ 58
    (
        'Multiplying and dividing fractions', CHAPITRE, None, 58,
        'To multiply, multiply numerator by numerator and denominator by denominator: '
        '2/3 × 5/7 = 10/21. A whole number is written over 1. To divide: keep the first fraction, '
        'change the sign to times, and turn the second one upside down: 2/3 ÷ 4/5 = 2/3 × 5/4.',
        'bf-mu-couv',
        'Le calcul 2/3 × 5/7 = 10/21 posé en fractions.',
        [
            ('relation',
             'To multiply two fractions, multiply numerator by numerator and denominator by '
             'denominator: 2/3 × 5/7 = 10/21.',
             'bf-mu-multiplier',
             'Haut × haut : 2 × 5 = 10. Bas × bas : 3 × 7 = 21.',
             [('simple', 'Straight across, top with top and bottom with bottom. No common '
                         'denominator is needed here.'),
              ('visuel', 'Multiplying is the easy one: nothing has to be changed first.')],
             [('qcm', 1, {'question': 'How do you multiply two fractions?',
                          'options': ['Top by top, bottom by bottom',
                                      'Top by bottom', 'With a common denominator']},
               {'index': 0}, 'Numerator by numerator, denominator by denominator.'),
              ('vrai_faux', 1, {'statement': 'The product 2/3 × 5/7 is equal to 10/21.'},
               {'value': True}, 'Yes: 2 × 5 = 10 and 3 × 7 = 21.'),
              ('texte_a_trous', 2,
               {'text': 'To multiply, go straight {{1}}: top with top, bottom with bottom.',
                'blanks': 1},
               {'values': ['across']}, 'Straight across.'),
              ('qcm', 3, {'question': 'What is 1/2 × 3/5?',
                          'options': ['3/10', '4/7', '3/7']},
               {'index': 0}, '1 × 3 = 3 and 2 × 5 = 10.'),
              ('vrai_faux', 4,
               {'statement': 'A common denominator is needed to multiply fractions.'},
               {'value': False}, 'No. That is for adding and subtracting.')]),

            ('relation',
             'To multiply a whole number by a fraction, write the whole number over 1: '
             '4 becomes 4/1.',
             'bf-mu-entier',
             '4 s’écrit 4/1, puis 4/1 × 2/3 = 8/3.',
             [('simple', 'Four whole ones are four over one. Then the rule is the usual one.'),
              ('pas_a_pas', 'Write the whole number over 1. Multiply top by top and bottom by '
                            'bottom.')],
             [('qcm', 1, {'question': 'How do you write the whole number 4 as a fraction?',
                          'options': ['4/1', '1/4', '4/4']},
               {'index': 0}, 'Over 1: four over one.'),
              ('vrai_faux', 1, {'statement': 'The whole number 4 can be written 4/1.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'A whole number is written over the number {{1}}.', 'blanks': 1},
               {'values': ['1']}, 'Over 1.'),
              ('qcm', 3, {'question': 'What is 4 × 2/3?',
                          'options': ['8/3', '8/12', '6/3']},
               {'index': 0}, '4/1 × 2/3 = 8/3.'),
              ('vrai_faux', 4, {'statement': 'The whole number 4 is written 1/4.'},
               {'value': False}, 'No. That is a quarter.')]),

            ('relation',
             'To divide by a fraction: keep the first one, change the sign to times, and turn '
             'the second one upside down. 2/3 ÷ 4/5 = 2/3 × 5/4 = 10/12.',
             'bf-mu-diviser',
             'Keep, change, flip : garder 2/3, changer le signe, retourner 5/4.',
             [('simple', 'Keep, change, flip. Three words, three gestures, in that order.'),
              ('pas_a_pas', 'Keep 2/3. Change the division sign into a times sign. Turn 4/5 into '
                            '5/4. Then multiply as usual.')],
             [('qcm', 1, {'question': 'What are the three words for dividing fractions?',
                          'options': ['Keep, change, flip', 'Add, change, flip',
                                      'Keep, add, turn']},
               {'index': 0}, 'Keep, change, flip.'),
              ('vrai_faux', 1, {'statement': 'To divide, you turn the second fraction over.'},
               {'value': True}, 'Yes, and the sign becomes a times sign.'),
              ('texte_a_trous', 2,
               {'text': 'Keep, change, {{1}}: the three words for dividing.', 'blanks': 1},
               {'values': ['flip']}, 'Keep, change, flip.'),
              ('qcm', 3, {'question': 'What does 2/3 ÷ 4/5 become?',
                          'options': ['2/3 × 5/4', '3/2 × 4/5', '2/3 × 4/5']},
               {'index': 0}, 'Keep 2/3, change the sign, flip 4/5 into 5/4.'),
              ('vrai_faux', 4, {'statement': 'To divide, you turn the first fraction over.'},
               {'value': False}, 'No. The second one is turned over.')]),

            ('relation',
             'Mixed numbers must be changed into improper fractions before they are multiplied '
             'or divided: 2 and 1/3 becomes 7/3.',
             'bf-mu-mixte',
             'Un nombre mixte se change en 7/3, puis seulement on multiplie.',
             [('simple', 'The rule of the fractions only works on fractions.'),
              ('pas_a_pas', 'Multiply the whole by the denominator, add the numerator, then '
                            'multiply or divide as usual.')],
             [('qcm', 1, {'question': 'What do you do with 2 and 1/3 before multiplying?',
                          'options': ['Write it as 7/3', 'Write it as 3/7',
                                      'Multiply it as it is']},
               {'index': 0}, '2 × 3 + 1 = 7, so 7/3.'),
              ('vrai_faux', 1,
               {'statement': 'A mixed number is changed into an improper fraction first.'},
               {'value': True}, 'Yes, always.'),
              ('texte_a_trous', 2,
               {'text': 'A mixed number becomes an {{1}} fraction before you multiply.',
                'blanks': 1},
               {'values': ['improper']}, 'An improper fraction.'),
              ('qcm', 3, {'question': 'What is 1 and 1/2 as an improper fraction?',
                          'options': ['3/2', '2/3', '1/2']},
               {'index': 0}, '1 × 2 + 1 = 3, so 3/2.'),
              ('vrai_faux', 4,
               {'statement': 'You may divide a mixed number without changing it.'},
               {'value': False}, 'No. Change it first.')]),
        ],
    ),

    # ------------------------------------------------------------------ 59
    (
        'A fraction of a quantity', CHAPITRE, None, 59,
        'To find a fraction of a quantity, divide by the denominator and multiply by the '
        'numerator: 3/5 of 40 = 40 ÷ 5 × 3 = 24. What is left is 1 whole less the fraction used. '
        'Of the remainder means: first find what is left, then take that fraction of it.',
        'bf-qu-couv',
        'Le calcul 3/5 of 40 = 24 posé dans son cadre.',
        [
            ('relation',
             'To find a fraction of a quantity, divide by the denominator, then multiply by the '
             'numerator: 3/5 of 40 = 40 ÷ 5 × 3 = 24.',
             'bf-qu-quantite',
             '40 ÷ 5 = 8, puis 8 × 3 = 24.',
             [('simple', 'Divide to find one part, then take as many parts as the numerator '
                         'says.'),
              ('pas_a_pas', 'Divide the quantity by the bottom number. Multiply the answer by '
                            'the top number.')],
             [('qcm', 1, {'question': 'What do you divide by first?',
                          'options': ['The denominator', 'The numerator', 'The quantity']},
               {'index': 0}, 'By the denominator, to find one part.'),
              ('vrai_faux', 1, {'statement': 'Three fifths of 40 is equal to 24.'},
               {'value': True}, 'Yes: 40 ÷ 5 = 8, and 8 × 3 = 24.'),
              ('texte_a_trous', 2,
               {'text': 'Divide by the denominator, then {{1}} by the numerator.', 'blanks': 1},
               {'values': ['multiply']}, 'Then multiply.'),
              ('qcm', 3, {'question': 'What is 2/3 of 30?',
                          'options': ['20', '10', '45']},
               {'index': 0}, '30 ÷ 3 = 10, and 10 × 2 = 20.'),
              ('vrai_faux', 4, {'statement': 'To find 3/5 of 40, you multiply 40 by 5.'},
               {'value': False}, 'No. You divide by 5 first.')]),

            ('relation',
             'What is left is one whole less the fraction used: if 2/5 is taken, 3/5 is left.',
             'bf-qu-reste',
             'Une barre de cinq parts, deux prises : il en reste trois.',
             [('simple', 'The whole is 5/5. Take 2/5 away and 3/5 stay.'),
              ('visuel', 'On the bar, count the white cells: they are what is left.')],
             [('qcm', 1, {'question': 'If 2/5 is used, what fraction is left?',
                          'options': ['3/5', '2/5', '7/5']},
               {'index': 0}, '5/5 - 2/5 = 3/5.'),
              ('vrai_faux', 1, {'statement': 'One whole can be written 5/5.'},
               {'value': True}, 'Yes, with any denominator you like.'),
              ('texte_a_trous', 2,
               {'text': 'What is left is one {{1}} less the fraction used.', 'blanks': 1},
               {'values': ['whole']}, 'One whole.'),
              ('qcm', 3, {'question': 'If 3/8 of the money is spent, what fraction is left?',
                          'options': ['5/8', '3/8', '11/8']},
               {'index': 0}, '8/8 - 3/8 = 5/8.'),
              ('vrai_faux', 4, {'statement': 'If 1/4 is used, then 3/4 is left.'},
               {'value': True}, 'Yes: 4/4 - 1/4 = 3/4.')]),

            ('relation',
             'Of the remainder means: first find what is left, then take that fraction of the '
             'remainder, and not of the first quantity.',
             'bf-qu-deloreste',
             '1/4 de 40 fait 10, il reste 30, et 1/3 du reste fait 10.',
             [('simple', 'The second fraction is taken from what is left, not from the start.'),
              ('pas_a_pas', 'Take the first fraction away. Write down what is left. Only then '
                            'take the next fraction, of that remainder.')],
             [('qcm', 1, {'question': 'Of the remainder means a fraction of what?',
                          'options': ['Of what is left', 'Of the first quantity',
                                      'Of the answer']},
               {'index': 0}, 'Of what is left.'),
              ('vrai_faux', 1,
               {'statement': 'Of the remainder means a fraction of the first quantity.'},
               {'value': False}, 'No: of what is left after the first part is taken.'),
              ('texte_a_trous', 2,
               {'text': 'Of the remainder means a fraction of what is {{1}}.', 'blanks': 1},
               {'values': ['left']}, 'Of what is left.'),
              ('qcm', 3, {'question': 'Of 40, 1/4 is taken. What is the remainder?',
                          'options': ['30', '10', '36']},
               {'index': 0}, '40 ÷ 4 = 10, and 40 - 10 = 30.'),
              ('vrai_faux', 4,
               {'statement': 'The remainder must be found before the next fraction is taken.'},
               {'value': True}, 'Yes, in that order.')]),

            ('relation',
             'A fraction of a sum of money is found in the same way: 2/5 of 3 000 F is '
             '3 000 ÷ 5 × 2 = 1 200 F.',
             'bf-qu-argent',
             '2/5 de 3 000 F : 3 000 ÷ 5 = 600, puis 600 × 2 = 1 200 F.',
             [('simple', 'Money is a quantity like any other. The rule does not change.'),
              ('pas_a_pas', 'Divide the sum by the denominator, multiply by the numerator, and '
                            'write the F at the end.')],
             [('qcm', 1, {'question': 'What is 2/5 of 3 000 F?',
                          'options': ['1 200 F', '600 F', '7 500 F']},
               {'index': 0}, '3 000 ÷ 5 = 600, and 600 × 2 = 1 200 F.'),
              ('vrai_faux', 1,
               {'statement': 'A fraction of money is found like a fraction of anything else.'},
               {'value': True}, 'Yes, the rule is the same.'),
              ('texte_a_trous', 2,
               {'text': 'A sum of money is a {{1}} like any other.', 'blanks': 1},
               {'values': ['quantity']}, 'A quantity.'),
              ('qcm', 3, {'question': 'What is 3/4 of 2 000 F?',
                          'options': ['1 500 F', '500 F', '2 500 F']},
               {'index': 0}, '2 000 ÷ 4 = 500, and 500 × 3 = 1 500 F.'),
              ('vrai_faux', 4, {'statement': 'To find 2/5 of 3 000 F, you multiply 3 000 by 5.'},
               {'value': False}, 'No. You divide by 5 first.')]),

            ('relation',
             'The answer to a word problem always carries its unit: 24 mangoes, 1 200 F, '
             '3 litres. A bare number is not an answer.',
             'bf-qu-unite',
             'La réponse se termine par son unité : 24 mangues, 1 200 F.',
             [('simple', 'The question asked for mangoes, so the answer is in mangoes.'),
              ('visuel', 'Write the unit straight after the number, before you put your pen '
                         'down.')],
             [('qcm', 1, {'question': 'What must the answer to a word problem carry?',
                          'options': ['Its unit', 'Its fraction', 'Its denominator']},
               {'index': 0}, 'Its unit.'),
              ('vrai_faux', 1, {'statement': 'Writing 24 alone is a complete answer.'},
               {'value': False}, 'No. 24 what? The unit is missing.'),
              ('texte_a_trous', 2,
               {'text': 'A complete answer ends with its {{1}}.', 'blanks': 1},
               {'values': ['unit']}, 'Its unit.'),
              ('qcm', 3, {'question': 'He spends 1 200 of his money. What is the full answer?',
                          'options': ['1 200 F', '1 200', 'F']},
               {'index': 0}, 'The number and its unit.'),
              ('vrai_faux', 4, {'statement': 'The unit is part of the answer.'},
               {'value': True}, 'Yes, always.')]),
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
                        # Pas de barre de fraction sur le clavier : une réponse
                        # comme « 3/5 » serait impossible à taper.
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
        'fig', os.path.join(ici, 'figures-brayne-fractions.py'))
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
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-fractions.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-42s %d notions  %d questions'
              % (ordre, titre, len(ns), sum(len(n[5]) for n in ns)))
    print(chemin)
