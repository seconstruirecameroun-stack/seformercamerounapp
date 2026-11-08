# -*- coding: utf-8 -*-
"""
Cinq leçons sur les ensembles pour BRAYNE (CM1) — fiche de révision
« CM1 - MATHEMATICS - REVISION SHEET - SETS AND VENN DIAGRAMS », 3 pages,
donnée par le père le 8 novembre 2026.

CE QUI EST DÉJÀ FAIT N-EST PAS REFAIT. Quatre leçons existent en base sous
le chapitre « Unit 3 — Venn diagram » : ce que montre un diagramme,
intersection / union / sous-ensemble / disjoints, la lecture des régions,
et les questions du cahier. Elles couvrent les sections 5 et 6 de la fiche.
Un contrôle refuse ce fichier si l-un de ces quatre titres y revenait.

CE QUE LA FICHE AJOUTE, et qui n-était nulle part :

  section 1    ce qu-est un ensemble, et ce qu-est un élément
  section 2    les cinq types : unité, fini, infini, vide, universel
  section 3    le tableau des signes, qu-il faut savoir LIRE
  section 4    lister : pairs, premiers, facteurs, multiples
  sections 7-8 compter : n(A∪B), n(A’), « at least one », « none »

L-ANGLAIS EST CELUI DE LA FICHE. Les quatre leçons de l-unité 3 sont déjà
en anglais, c-est la langue de son épreuve, et les mots à retenir sont des
mots anglais — subset, factor, multiple. Traduire les énoncés lui ferait
réviser un vocabulaire qu-on ne lui demandera pas.

DEUX CONTRAINTES D-ÉCRITURE, toutes deux vérifiées plus bas.

Les signes d-ensembles s-écrivent dans les énoncés — le navigateur va
chercher la lettre manquante dans la police du système — mais JAMAIS dans
une réponse à taper : le clavier de l-application n-a ni ces signes, ni la
barre de fraction, ni la touche espace. Toute réponse à écrire est donc un
mot unique, en minuscules, tapable sur ce clavier-là.

Les quatre étapes sont obligatoires sur chaque notion, et le Défi étant
chronométré, il ne porte que des questions qui se jouent en un geste.

Usage :  python work/lecons-brayne-sets.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-sets.py. ')

MATIERE = 'Mathématiques'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'en'
CHAPITRE = 'Sets and Venn diagrams'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

# Les touches que le clavier de l-application offre réellement.
TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

# Les quatre leçons de l-unité 3, déjà en base, qui ne doivent pas revenir.
DEJA = (
    'What a Venn diagram shows',
    'Intersection, union, subset and disjoint sets',
    'Reading a Venn diagram',
    'Questions on a Venn diagram',
)

LECONS = [
    # ------------------------------------------------------------------ 48
    (
        'What a set is', CHAPITRE, None, 48,
        'A set is a collection of objects or things that are alike. The objects of a set are '
        'called its elements. A set is written inside braces, with its elements separated by '
        'commas: A = { 2, 4, 6, 8 }. And n(A) is the number of elements in the set A.',
        'bs-se-couv',
        'Un cadre blanc portant A = { 2, 4, 6, 8 }, accolades et virgules comprises.',
        [
            ('definition',
             'A set is a collection of objects or things that are alike.',
             'bs-se-def',
             'L’ensemble A = { 2, 4, 6, 8 } écrit dans son cadre.',
             [('simple', 'Things that go together make a set: the even numbers, the days of the '
                         'week, the pupils of your class.'),
              ('analogie', 'A basket is a set: what you put in it belongs together. One stone '
                           'among the mangoes does not belong to that basket.')],
             [('qcm', 1, {'question': 'What is a set?',
                          'options': ['A collection of things that are alike',
                                      'A way of dividing numbers', 'A kind of ruler']},
               {'index': 0}, 'A collection of objects or things that are alike.'),
              ('vrai_faux', 1, {'statement': 'A set is a collection of objects that are alike.'},
               {'value': True}, 'Yes. That is the definition.'),
              ('texte_a_trous', 2,
               {'text': 'A set is a collection of objects that are {{1}}.', 'blanks': 1},
               {'values': ['alike']}, 'Alike: they go together.'),
              ('qcm', 3, {'question': 'Which one of these is a set?',
                          'options': ['The even numbers less than 10',
                                      'A number chosen with no rule',
                                      'A word and a drawing']},
               {'index': 0}, 'The even numbers less than 10: they are alike.'),
              ('vrai_faux', 4, {'statement': 'Objects with nothing in common still make a set.'},
               {'value': False}, 'No. The objects of a set are alike.')]),

            ('definition',
             'The objects that make up a set are called its elements.',
             'bs-se-elements',
             'Les quatre éléments de A = { 2, 4, 6, 8 }, nommés un par un.',
             [('simple', 'In A = { 2, 4, 6, 8 }, the elements are 2, 4, 6 and 8. Each one is an '
                         'element of A.'),
              ('pas_a_pas', 'To name the elements, read what is inside the braces, one by one.')],
             [('qcm', 1, {'question': 'What are the objects of a set called?',
                          'options': ['Its elements', 'Its corners', 'Its rules']},
               {'index': 0}, 'Its elements.'),
              ('texte_a_trous', 1,
               {'text': 'The objects of a set are called its {{1}}.', 'blanks': 1},
               {'values': ['elements']}, 'Its elements.'),
              ('qcm', 2, {'question': 'In A = { 2, 4, 6, 8 }, how many elements are there?',
                          'options': ['4', '2', '8']},
               {'index': 0}, 'Four: 2, 4, 6 and 8.'),
              ('association', 3, {'question': 'Match each set with its number of elements.',
                                  'gauche': ['{ 7 }', '{ 1, 2 }', '{ 1, 2, 3 }'],
                                  'droite': ['one element', 'two elements', 'three elements']},
               {'order': [0, 1, 2]}, 'Count what is inside the braces.'),
              ('vrai_faux', 4,
               {'statement': 'In B = { Monday, Tuesday }, Monday is an element of B.'},
               {'value': True}, 'Yes. It is written inside the braces.')]),

            ('relation',
             'A set is written inside braces, and its elements are separated by commas: '
             'A = { 2, 4, 6, 8 }.',
             'bs-se-accolades',
             'B = { Monday, Tuesday, Sunday } : les accolades ouvrent et ferment l’ensemble.',
             [('visuel', 'The braces hold the set together. Without them, it is only a line of '
                         'numbers.'),
              ('pas_a_pas', 'Write the name, the equals sign, the open brace, the elements with '
                            'their commas, and the close brace.')],
             [('qcm', 1, {'question': 'How is a set written?',
                          'options': ['Inside braces, elements separated by commas',
                                      'Inside a circle, with no sign',
                                      'On two lines, one word a line']},
               {'index': 0}, 'Inside braces, with commas between the elements.'),
              ('vrai_faux', 1, {'statement': 'The elements of a set are separated by commas.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2, {'text': 'A set is written inside {{1}}.', 'blanks': 1},
               {'values': ['braces']}, 'Inside braces.'),
              ('qcm', 3, {'question': 'Which one is written correctly?',
                          'options': ['A = { 1, 2, 3 }', 'A = 1, 2, 3', 'A = ( 1 2 3 )']},
               {'index': 0}, 'Braces, and commas between the elements.'),
              ('vrai_faux', 4, {'statement': 'A = ( 2, 4, 6 ) is the correct way to write a set.'},
               {'value': False}, 'No. A set takes braces, not brackets.')]),

            ('definition',
             'n(A) is the number of elements in the set A. If A = { 2, 4, 6, 8 }, then n(A) = 4.',
             'bs-se-nombre',
             'n(A) écrit en grand, avec sa lecture dessous.',
             [('simple', 'n(A) does not ask what is inside. It asks how many.'),
              ('pas_a_pas', 'Count the elements one by one, and write that number.')],
             [('qcm', 1, {'question': 'What does n(A) mean?',
                          'options': ['The number of elements in A', 'The name of the set A',
                                      'The biggest element of A']},
               {'index': 0}, 'The number of elements in A.'),
              ('texte_a_trous', 1, {'text': 'n(A) is the {{1}} of elements in A.', 'blanks': 1},
               {'values': ['number']}, 'The number of elements.'),
              ('qcm', 2, {'question': 'If A = { 2, 4, 6, 8 }, what is n(A)?',
                          'options': ['4', '8', '2']},
               {'index': 0}, 'Four elements, so n(A) = 4.'),
              ('qcm', 3, {'question': 'If B = { Monday, Tuesday, Sunday }, what is n(B)?',
                          'options': ['3', '7', '2']},
               {'index': 0}, 'Three elements, so n(B) = 3.'),
              ('vrai_faux', 4,
               {'statement': 'If a set has seven elements, then n of that set is 7.'},
               {'value': True}, 'Yes. n counts the elements.')]),
        ],
    ),

    # ------------------------------------------------------------------ 49
    (
        'The types of sets', CHAPITRE, None, 49,
        'Sets take their name from what they hold. A unit set has one element only. A finite set '
        'can be counted to the end. An infinite set never ends. The empty set has no element at '
        'all. And the universal set U holds every element being considered.',
        'bs-ty-couv',
        'Cinq cartes alignées : unit, finite, infinite, empty, universal.',
        [
            ('definition',
             'A unit set, also called a singleton, has only one element. Example: { 7 }.',
             'bs-ty-unite',
             'A = { 7 } : un seul élément dans les accolades.',
             [('simple', 'One element, and one only. { 7 } is a unit set; { 7, 8 } is not.'),
              ('analogie', 'A singleton is a house with one person in it. Let a second one in, '
                           'and it is no longer a singleton.')],
             [('qcm', 1, {'question': 'How many elements has a unit set?',
                          'options': ['One', 'Two', 'None']},
               {'index': 0}, 'One element only.'),
              ('vrai_faux', 1, {'statement': '{ 7 } is a unit set.'},
               {'value': True}, 'Yes: one element.'),
              ('qcm', 2, {'question': 'Which one is a singleton?',
                          'options': ['{ 5 }', '{ 5, 6 }', '{ }']},
               {'index': 0}, '{ 5 } holds one element.'),
              ('texte_a_trous', 3,
               {'text': 'A set with only one element is a unit set, or a {{1}}.', 'blanks': 1},
               {'values': ['singleton']}, 'A singleton.'),
              ('vrai_faux', 4, {'statement': '{ 3, 9 } is a unit set.'},
               {'value': False}, 'No. It has two elements.')]),

            ('definition',
             'A finite set has a limited number of elements: you can count them and stop. '
             'Example: { 1, 2, 3, 4 }.',
             'bs-ty-fini',
             'B = { 1, 2, 3, 4 } : on peut les compter, et s’arrêter.',
             [('simple', 'If the counting comes to an end, the set is finite.'),
              ('pas_a_pas', 'Count the elements. If you reach the last one, the set is finite.')],
             [('qcm', 1, {'question': 'What is a finite set?',
                          'options': ['A set with a limited number of elements',
                                      'A set that never ends', 'A set with no element']},
               {'index': 0}, 'Its elements can be counted to the end.'),
              ('vrai_faux', 1, {'statement': '{ 1, 2, 3, 4 } is a finite set.'},
               {'value': True}, 'Yes: four elements, and it stops.'),
              ('texte_a_trous', 2,
               {'text': 'A set you can finish counting is a {{1}} set.', 'blanks': 1},
               {'values': ['finite']}, 'A finite set.'),
              ('qcm', 3, {'question': 'Which one of these sets is finite?',
                          'options': ['The days of the week', 'The whole numbers',
                                      'The multiples of 3']},
               {'index': 0}, 'Seven days, and no more.'),
              ('vrai_faux', 4, {'statement': 'A finite set can always be counted to the end.'},
               {'value': True}, 'Yes. That is what finite means.')]),

            ('definition',
             'An infinite set has an unlimited number of elements: the counting never ends. '
             'Example: { 1, 2, 3, … }.',
             'bs-ty-infini',
             'C = { 1, 2, 3, … } : les points disent que cela continue.',
             [('simple', 'The three dots mean: go on in the same way, for ever.'),
              ('visuel', 'You can write the first elements, never the last one. There is none.')],
             [('qcm', 1, {'question': 'What is an infinite set?',
                          'options': ['A set whose elements never end',
                                      'A set with four elements', 'A set with one element']},
               {'index': 0}, 'Its elements never end.'),
              ('vrai_faux', 1, {'statement': 'The set { 1, 2, 3, … } is an infinite set.'},
               {'value': True}, 'Yes. The dots say it goes on.'),
              ('texte_a_trous', 2,
               {'text': 'A set whose counting never ends is an {{1}} set.', 'blanks': 1},
               {'values': ['infinite']}, 'An infinite set.'),
              ('qcm', 3, {'question': 'Which one of these sets is infinite?',
                          'options': ['The whole numbers', 'The days of the week',
                                      'The months of the year']},
               {'index': 0}, 'The whole numbers never end.'),
              ('vrai_faux', 4, {'statement': 'An infinite set has a last element.'},
               {'value': False}, 'No. That is exactly what it has not.')]),

            ('definition',
             'The empty set has no element at all. It is written ∅, or with two braces and '
             'nothing between them: { }.',
             'bs-ty-vide',
             'Un rond barré : le signe de l’ensemble vide.',
             [('simple', 'Nothing inside. The set of the pupils taller than a house is empty.'),
              ('visuel', 'Careful: { 0 } is not empty. It holds one element, the number zero.')],
             [('qcm', 1, {'question': 'How many elements has the empty set?',
                          'options': ['None', 'One', 'Two']},
               {'index': 0}, 'None at all.'),
              ('vrai_faux', 1, {'statement': 'The empty set can be written { }.'},
               {'value': True}, 'Yes: two braces, nothing between them.'),
              ('texte_a_trous', 2,
               {'text': 'A set with no element at all is called the {{1}} set.', 'blanks': 1},
               {'values': ['empty']}, 'The empty set.'),
              ('qcm', 3, {'question': 'Which one of these is the empty set?',
                          'options': ['{ }', '{ 0 }', '{ 1 }']},
               {'index': 0}, 'Nothing between the braces.'),
              ('vrai_faux', 4, {'statement': 'The set { 0 } is the empty set.'},
               {'value': False}, 'No. It holds one element: the number zero.')]),

            ('definition',
             'The universal set, written U, holds every element being considered. In a Venn '
             'diagram it is the rectangle drawn around the ovals.',
             'bs-ty-universel',
             'Le rectangle U avec ses deux ovales à l’intérieur.',
             [('simple', 'U is the whole of what we are talking about. Nothing in the exercise '
                         'lives outside it.'),
              ('analogie', 'U is the school yard: every group plays inside it, and nobody is '
                           'outside the fence.')],
             [('qcm', 1, {'question': 'What does the universal set hold?',
                          'options': ['Every element being considered',
                                      'Only the even numbers', 'Only one element']},
               {'index': 0}, 'Everything we are working with.'),
              ('vrai_faux', 1,
               {'statement': 'In a Venn diagram, the universal set is the rectangle.'},
               {'value': True}, 'Yes, and the sets are the ovals inside it.'),
              ('texte_a_trous', 2,
               {'text': 'The rectangle drawn around the ovals is the {{1}} set.', 'blanks': 1},
               {'values': ['universal']}, 'The universal set.'),
              ('qcm', 3, {'question': 'Which one is drawn as a rectangle?',
                          'options': ['The universal set', 'A unit set', 'The empty set']},
               {'index': 0}, 'The universal set.'),
              ('vrai_faux', 4,
               {'statement': 'An element outside every oval is still in the universal set.'},
               {'value': True}, 'Yes. It is inside the rectangle.')]),
        ],
    ),

    # ------------------------------------------------------------------ 50
    (
        'The signs of sets', CHAPITRE, None, 50,
        'Four signs come back in every exercise. ∈ means is an element of, and ∉ means is not. '
        '⊂ means is a subset of. ∩ is the intersection, what is common, and ∪ is the union, all '
        'together. A’ is the complement of A: everything in U that is not in A.',
        'bs-si-couv',
        'Quatre signes tracés côte à côte : appartenance, inclusion, intersection, union.',
        [
            ('definition',
             'The sign ∈ means is an element of, and ∉ means is not an element of. A bar across '
             'a sign always means no.',
             'bs-si-appartient',
             'Le signe d’appartenance et le même signe barré, chacun nommé.',
             [('simple', 'The sentence 2 ∈ A is read: 2 is an element of A.'),
              ('visuel', 'The bar is the same on every sign: it turns the sentence into its '
                         'contrary.')],
             [('qcm', 1, {'question': 'What does the sign ∈ mean?',
                          'options': ['is an element of', 'is not an element of',
                                      'is a subset of']},
               {'index': 0}, 'It means: is an element of.'),
              ('vrai_faux', 1, {'statement': 'A bar across a sign means no.'},
               {'value': True}, 'Yes, on every sign.'),
              ('texte_a_trous', 2,
               {'text': 'The sign ∈ is read: is an {{1}} of.', 'blanks': 1},
               {'values': ['element']}, 'Is an element of.'),
              ('qcm', 3, {'question': 'If A = { 2, 4, 6 }, which sentence is true?',
                          'options': ['2 ∈ A', '5 ∈ A', '2 ∉ A']},
               {'index': 0}, '2 is written inside A.'),
              ('vrai_faux', 4, {'statement': 'The sign ∉ means is not an element of.'},
               {'value': True}, 'Yes: the barred sign.')]),

            ('definition',
             'The sign ⊂ means is a subset of: every element of the first set is also in the '
             'second one. The sign ⊄ means it is not.',
             'bs-si-inclus',
             'Le signe d’inclusion et le même signe barré, chacun nommé.',
             [('simple', 'The sentence { 2, 4 } ⊂ { 2, 4, 6 } is true: both elements are there.'),
              ('pas_a_pas', 'Take each element of the small set and look for it in the big one. '
                            'If one is missing, it is not a subset.')],
             [('qcm', 1, {'question': 'What does the sign ⊂ mean?',
                          'options': ['is a subset of', 'is an element of', 'is the union of']},
               {'index': 0}, 'It means: is a subset of.'),
              ('vrai_faux', 1, {'statement': 'The sentence { 2, 4 } ⊂ { 2, 4, 6 } is true.'},
               {'value': True}, 'Yes: 2 and 4 are both in the second set.'),
              ('texte_a_trous', 2,
               {'text': 'A set whose elements are all in another set is a {{1}} of it.',
                'blanks': 1},
               {'values': ['subset']}, 'A subset.'),
              ('qcm', 3, {'question': 'Which one is a subset of { 1, 2, 3 }?',
                          'options': ['{ 1, 3 }', '{ 1, 4 }', '{ 4, 5 }']},
               {'index': 0}, '1 and 3 are both in { 1, 2, 3 }.'),
              ('vrai_faux', 4, {'statement': 'The set { 1, 5 } is a subset of { 1, 2, 3 }.'},
               {'value': False}, 'No. 5 is missing from the second set.')]),

            ('relation',
             'The sign ∩ is the intersection: what the sets have in common. The sign ∪ is the '
             'union: all their elements together, each written once.',
             'bs-si-inter',
             'L’arche de l’intersection et le récipient de l’union, chacun nommé.',
             [('simple', 'Intersection means common. Union means all together. That is the whole '
                         'memory rule.'),
              ('visuel', 'The arch of the intersection keeps the middle only; the cup of the '
                         'union holds everything.')],
             [('qcm', 1, {'question': 'What does the sign ∩ mean?',
                          'options': ['intersection', 'union', 'subset']},
               {'index': 0}, 'Intersection: what is common.'),
              ('vrai_faux', 1, {'statement': 'The sign ∪ means all the elements together.'},
               {'value': True}, 'Yes: the union.'),
              ('texte_a_trous', 2,
               {'text': 'The sign ∩ gives what the two sets have in {{1}}.', 'blanks': 1},
               {'values': ['common']}, 'In common.'),
              ('qcm', 3, {'question': 'If A = { 2, 4, 6 } and B = { 2, 7 }, what is A ∩ B?',
                          'options': ['{ 2 }', '{ 2, 7 }', '{ 4, 6 }']},
               {'index': 0}, 'Only 2 is in both sets.'),
              ('qcm', 4, {'question': 'If A = { 1, 2 } and B = { 2, 3 }, what is A ∪ B?',
                          'options': ['{ 1, 2, 3 }', '{ 2 }', '{ 1, 3 }']},
               {'index': 0}, 'Everything, each element written once.')]),

            ('definition',
             'A’ is the complement of A: every element of the universal set U that is not in A.',
             'bs-si-complement',
             'A’ écrit en grand, avec sa lecture dessous.',
             [('simple', 'If U = { 1, 2, 3, 4 } and A = { 1, 2 }, then A’ = { 3, 4 }.'),
              ('pas_a_pas', 'Write U, cross out everything that is in A, and what is left is A’.')],
             [('qcm', 1, {'question': 'What is A’?',
                          'options': ['Everything in U that is not in A', 'Everything in A',
                                      'The number of elements in A']},
               {'index': 0}, 'What is in U but not in A.'),
              ('vrai_faux', 1, {'statement': 'A’ is read: the complement of A.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2, {'text': 'A’ is called the {{1}} of A.', 'blanks': 1},
               {'values': ['complement']}, 'The complement of A.'),
              ('qcm', 3, {'question': 'If U = { 1, 2, 3, 4 } and A = { 1, 2 }, what is A’?',
                          'options': ['{ 3, 4 }', '{ 1, 2 }', '{ }']},
               {'index': 0}, 'What is left in U once A is taken away.'),
              ('vrai_faux', 4, {'statement': 'A’ holds the elements of A.'},
               {'value': False}, 'No. It holds the others.')]),
        ],
    ),

    # ------------------------------------------------------------------ 51
    (
        'Listing the elements of a set', CHAPITRE, None, 51,
        'Many questions begin by asking for a list: the even numbers less than 12, the prime '
        'numbers less than 20, the factors of 18, the multiples of 5 up to 30. Each list has its '
        'own rule, and it is the rule that has to be known.',
        'bs-li-couv',
        'Un cadre portant { 2, 3, 5, 7, 11, 13, 17, 19 }, les nombres premiers.',
        [
            ('relation',
             'Even numbers can be divided by 2. The even numbers less than 12 are '
             '{ 2, 4, 6, 8, 10 }.',
             'bs-li-pairs',
             'E = { 2, 4, 6, 8, 10 } dans son cadre.',
             [('simple', 'An even number ends in 0, 2, 4, 6 or 8.'),
              ('pas_a_pas', 'Count by twos, and stop before the limit you were given.')],
             [('qcm', 1, {'question': 'An even number can be divided by which number?',
                          'options': ['2', '3', '5']},
               {'index': 0}, 'By 2.'),
              ('vrai_faux', 1, {'statement': 'The number 10 is an even number.'},
               {'value': True}, 'Yes: it can be divided by 2.'),
              ('texte_a_trous', 2,
               {'text': 'A number that can be divided by two is an {{1}} number.', 'blanks': 1},
               {'values': ['even']}, 'An even number.'),
              ('qcm', 3, {'question': 'What are the even numbers less than 12?',
                          'options': ['{ 2, 4, 6, 8, 10 }', '{ 2, 4, 6, 8, 10, 12 }',
                                      '{ 1, 3, 5, 7, 9 }']},
               {'index': 0}, '12 is not less than 12, so it stays out.'),
              ('vrai_faux', 4, {'statement': 'The number 7 is an even number.'},
               {'value': False}, 'No. 7 cannot be divided by 2.')]),

            ('relation',
             'A prime number has exactly two factors: 1 and itself. The prime numbers less than '
             '20 are { 2, 3, 5, 7, 11, 13, 17, 19 }.',
             'bs-li-premiers',
             'P = { 2, 3, 5, 7, 11, 13, 17, 19 } dans son cadre.',
             [('simple', 'The number 1 is not prime: it has one factor only. And 2 is prime, the '
                         'only even one.'),
              ('pas_a_pas', 'Try to divide by 2, then 3, then 5, then 7. If none of them works, '
                            'the number is prime.')],
             [('qcm', 1, {'question': 'How many factors has a prime number?',
                          'options': ['Exactly two', 'Exactly one', 'Three']},
               {'index': 0}, 'Two: 1 and itself.'),
              ('vrai_faux', 1, {'statement': 'The number 7 is a prime number.'},
               {'value': True}, 'Yes: only 1 and 7 divide it.'),
              ('qcm', 2, {'question': 'Which one of these numbers is not prime?',
                          'options': ['9', '11', '13']},
               {'index': 0}, '9 can be divided by 3.'),
              ('texte_a_trous', 3,
               {'text': 'A number with exactly two factors is a {{1}} number.', 'blanks': 1},
               {'values': ['prime']}, 'A prime number.'),
              ('vrai_faux', 4, {'statement': 'The number 1 is a prime number.'},
               {'value': False}, 'No. It has one factor only.')]),

            ('relation',
             'The factors of a number divide it exactly. The factors of 18 are '
             '{ 1, 2, 3, 6, 9, 18 }.',
             'bs-li-facteurs',
             'Les multiplications 1 × 18, 2 × 9, 3 × 6, puis la liste des facteurs.',
             [('simple', 'Factors go in pairs: 2 × 9 = 18, so 2 and 9 are both factors of 18.'),
              ('pas_a_pas', 'Try 1, then 2, then 3. Each time it divides exactly, write down both '
                            'numbers of the multiplication.')],
             [('qcm', 1, {'question': 'What is a factor of a number?',
                          'options': ['A number that divides it exactly',
                                      'A number bigger than it', 'The number of its elements']},
               {'index': 0}, 'A number that divides it exactly.'),
              ('vrai_faux', 1, {'statement': 'The number 3 is a factor of 18.'},
               {'value': True}, 'Yes: 3 × 6 = 18.'),
              ('qcm', 2, {'question': 'Which one is not a factor of 18?',
                          'options': ['4', '6', '9']},
               {'index': 0}, '18 divided by 4 does not come out exactly.'),
              ('texte_a_trous', 3,
               {'text': 'A number that divides 18 exactly is a {{1}} of 18.', 'blanks': 1},
               {'values': ['factor']}, 'A factor of 18.'),
              ('vrai_faux', 4, {'statement': 'The number 18 is a factor of 18.'},
               {'value': True}, 'Yes: 1 × 18 = 18.')]),

            ('relation',
             'The multiples of a number are what you find in its times table. The multiples of 5 '
             'up to 30 are { 5, 10, 15, 20, 25, 30 }.',
             'bs-li-multiples',
             'La table de 5 jusqu’à 30, puis la liste des multiples.',
             [('simple', 'A multiple is the number multiplied by 1, then 2, then 3, and so on.'),
              ('visuel', 'Factors are smaller than the number; multiples are bigger. Do not mix '
                         'the two words.')],
             [('qcm', 1, {'question': 'Where do you find the multiples of 5?',
                          'options': ['In the times table of 5', 'In the factors of 5',
                                      'In the even numbers']},
               {'index': 0}, 'In its times table.'),
              ('vrai_faux', 1, {'statement': 'The number 20 is a multiple of 5.'},
               {'value': True}, 'Yes: 5 × 4 = 20.'),
              ('qcm', 2, {'question': 'Which one is not a multiple of 5?',
                          'options': ['12', '15', '25']},
               {'index': 0}, '12 is not in the times table of 5.'),
              ('texte_a_trous', 3,
               {'text': 'The numbers of the times table of 5 are its {{1}}.', 'blanks': 1},
               {'values': ['multiples']}, 'Its multiples.'),
              ('vrai_faux', 4,
               {'statement': 'The multiples of a number are always smaller than it.'},
               {'value': False}, 'No. They are bigger. The factors are the smaller ones.')]),
        ],
    ),

    # ------------------------------------------------------------------ 52
    (
        'Counting with sets', CHAPITRE, None, 52,
        'Some questions ask how many, not which. Then n(A ∪ B) = n(A) + n(B) - n(A ∩ B), because '
        'the common elements would be counted twice. And n(A’) = n(U) - n(A). At least one means '
        'everything inside the ovals; none is what is left in U.',
        'bs-co-couv',
        'La formule n(A ∪ B) = n(A) + n(B) - n(A ∩ B), les signes tracés.',
        [
            ('relation',
             'n(A ∪ B) = n(A) + n(B) - n(A ∩ B). The elements in both sets would be counted '
             'twice, so they are taken away once.',
             'bs-co-union',
             'Deux ovales, l’union teintée et le milieu en doré : la part comptée deux fois.',
             [('simple', 'Add the two counts, then take the middle away once: it was counted in '
                         'both of them.'),
              ('analogie', 'Two teams of eleven with three players in both make nineteen '
                           'children, not twenty-two.')],
             [('qcm', 1, {'question': 'Why do you take away the intersection?',
                          'options': ['Those elements were counted twice',
                                      'Those elements are too small',
                                      'Those elements are outside U']},
               {'index': 0}, 'They belong to both sets, so they were counted twice.'),
              ('vrai_faux', 1,
               {'statement': 'n(A ∪ B) = n(A) + n(B) - n(A ∩ B).'},
               {'value': True}, 'Yes, that is the formula.'),
              ('qcm', 2, {'question': 'n(A) = 8, n(B) = 5, n(A ∩ B) = 2. What is n(A ∪ B)?',
                          'options': ['11', '13', '15']},
               {'index': 0}, '8 + 5 = 13, then 13 - 2 = 11.'),
              ('qcm', 3, {'question': 'n(A) = 10, n(B) = 7, n(A ∩ B) = 3. What is n(A ∪ B)?',
                          'options': ['14', '17', '20']},
               {'index': 0}, '10 + 7 = 17, then 17 - 3 = 14.'),
              ('vrai_faux', 4,
               {'statement': 'To find n(A ∪ B), you only add n(A) and n(B).'},
               {'value': False}, 'No. You must take the intersection away once.')]),

            ('relation',
             'n(A’) = n(U) - n(A). What is not in A is everything else in the universal set.',
             'bs-co-complement',
             'Le rectangle teinté partout sauf dans les ovales : le complément.',
             [('simple', 'Count the whole of U, take away what is in A, and the rest is A’.'),
              ('pas_a_pas', 'Write n(U). Write n(A). Subtract. That is the answer.')],
             [('qcm', 1, {'question': 'What is n(A’) equal to?',
                          'options': ['n(U) - n(A)', 'n(U) + n(A)', 'n(A) - n(U)']},
               {'index': 0}, 'The whole of U, less what is in A.'),
              ('vrai_faux', 1, {'statement': 'n(A’) = n(U) - n(A).'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'To find n(A’), you {{1}} n(A) from n(U).', 'blanks': 1},
               {'values': ['subtract']}, 'You subtract it.'),
              ('qcm', 3, {'question': 'n(U) = 30 and n(A) = 12. What is n(A’)?',
                          'options': ['18', '42', '12']},
               {'index': 0}, '30 - 12 = 18.'),
              ('vrai_faux', 4,
               {'statement': 'If every element of U is in A, then n(A’) = 0.'},
               {'value': True}, 'Yes: nothing is left outside A.')]),

            ('relation',
             'At least one means everything inside the ovals: the parts that belong to one set '
             'only, and the parts that are shared.',
             'bs-co-aumoins',
             'Les deux ovales teintés entièrement : « at least one ».',
             [('simple', 'At least one does not mean one only. It means one or more.'),
              ('visuel', 'Colour the whole of both ovals. What you coloured is the answer.')],
             [('qcm', 1, {'question': 'What does at least one mean?',
                          'options': ['One or more', 'One only', 'None']},
               {'index': 0}, 'One or more.'),
              ('vrai_faux', 1,
               {'statement': 'At least one is everything inside the ovals.'},
               {'value': True}, 'Yes, shared parts included.'),
              ('qcm', 2, {'question': '7 are in A only, 4 in both, 6 in B only. How many in all?',
                          'options': ['17', '11', '13']},
               {'index': 0}, '7 + 4 + 6 = 17.'),
              ('texte_a_trous', 3, {'text': 'At least one means one or {{1}}.', 'blanks': 1},
               {'values': ['more']}, 'One or more.'),
              ('vrai_faux', 4,
               {'statement': 'At least one leaves out the part shared by the two sets.'},
               {'value': False}, 'No. The shared part is counted too.')]),

            ('relation',
             'None means what is left in U once the ovals are counted: n(U) less the total '
             'inside the ovals.',
             'bs-co-aucun',
             'n(U) = 30, 22 dans les ovales, 30 - 22 = 8 dans aucun ensemble.',
             [('simple', 'They are written outside the ovals, but still inside the rectangle.'),
              ('pas_a_pas', 'Add everything inside the ovals. Take that away from n(U). The rest '
                            'belongs to no set.')],
             [('qcm', 1, {'question': 'Where are the elements that belong to no set?',
                          'options': ['Outside the ovals, inside U', 'Inside the two ovals',
                                      'Outside the rectangle']},
               {'index': 0}, 'Outside the ovals, but inside the rectangle.'),
              ('vrai_faux', 1,
               {'statement': 'None is n(U) less the total inside the ovals.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'n(U) = 30 and 22 are inside the ovals. How many in none?',
                          'options': ['8', '22', '52']},
               {'index': 0}, '30 - 22 = 8.'),
              ('qcm', 3, {'question': 'n(U) = 40 and 31 are inside the ovals. How many in none?',
                          'options': ['9', '31', '71']},
               {'index': 0}, '40 - 31 = 9.'),
              ('vrai_faux', 4,
               {'statement': 'An element in no set at all is written outside the rectangle.'},
               {'value': False}, 'No. It stays inside the rectangle, which is U.')]),

            ('relation',
             'In a word problem, the number given for both sets goes in the middle first. The '
             'number given for one set includes that middle, so take the middle away.',
             'bs-co-etapes',
             'Les quatre temps : le milieu, les parts à deux, les parts seules, le total.',
             [('simple', 'If 20 play football and 8 play both games, then 12 play football only.'),
              ('pas_a_pas', 'Write the middle. Then, for each set, subtract the middle from its '
                            'total. What is left goes in the part that is alone.')],
             [('qcm', 1, {'question': 'In a word problem, what goes in the middle first?',
                          'options': ['The number belonging to both sets', 'The biggest number',
                                      'The number of the universal set']},
               {'index': 0}, 'The number that belongs to both sets.'),
              ('vrai_faux', 1,
               {'statement': 'The number given for one set already includes the middle.'},
               {'value': True}, 'Yes, which is why the middle is taken away.'),
              ('chronologie', 2, {'question': 'Put the four steps in the right order.',
                                  'tokens': ['The middle first', 'The parts shared by two',
                                             'The parts that are alone', 'Check the total']},
               {'order': [0, 1, 2, 3]}, 'Middle, shared parts, lone parts, then the check.'),
              ('qcm', 3, {'question': '20 play football and 8 play both. How many play football only?',
                          'options': ['12', '28', '8']},
               {'index': 0}, '20 - 8 = 12.'),
              ('vrai_faux', 4,
               {'statement': 'If 20 play football and 8 play both, then 20 play football only.'},
               {'value': False}, 'No. The 8 are inside the 20, so 12 play football only.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues, trous = set(), 0, 0, 0
    titres = [l[0] for l in LECONS]
    assert len(set(titres)) == len(titres), 'titre en double'
    for deja in DEJA:
        assert deja not in titres, 'cette leçon existe déjà en base : ' + deja

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
                # Le Défi est chronométré : seuls les types qui se jouent en
                # un geste y ont leur place.
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
                    # Une bonne réponse bien plus longue que les autres se
                    # devine sans rien savoir de la leçon.
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
                        # Le clavier de l-application n-a ni touche espace, ni
                        # barre de fraction, ni signe d-ensemble. Une réponse
                        # qu-il ne peut pas taper serait perdue d-avance.
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
        'fig', os.path.join(ici, 'figures-brayne-sets.py'))
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
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-sets.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-34s %d notions  %d questions'
              % (ordre, titre, len(ns), sum(len(n[5]) for n in [x for x in ns])))
    print(chemin)
