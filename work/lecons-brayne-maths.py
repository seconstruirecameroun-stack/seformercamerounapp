# -*- coding: utf-8 -*-
"""
Unit 3 — Venn diagram, la leçon de mathématiques de BRAYNE (CM1),
lundi 2 novembre 2026.

Tout est en anglais, explications comprises. Son cahier de leçons, son
cahier d’exercices et le manuel (pages 12 et 13) sont en anglais : c’est
dans cette langue qu’il sera interrogé. La matière reste « Mathématiques »
pour rejoindre les leçons déjà en base.

Le programme suit ses fautes. Sur la page d’exercices, les questions 1 à 4
— lister les éléments de U, K, L et M — passent presque sans rature. Les
questions 5 à 10 sont biffées, réécrites, biffées encore : ce sont
exactement celles qui demandent K∩L∩M, les unions, et « set L only ». Ce
n’est donc pas la définition du diagramme qui manque, c’est la **lecture
des régions**. La troisième leçon ne parle que de cela.

Deux prudences sur les sources.

Le diagramme à trois cercles de son cahier d’exercices est photographié de
biais et plusieurs nombres sont ambigus. Rien ici ne le recopie : inventer
la place d’un nombre dans une région reviendrait à lui faire réviser une
fausse réponse. Les questions de lecture s’appuient sur les sets de la
partie B du même exercice, eux parfaitement lisibles :
A = {11, 13, 15, 17, 19}, B = {12, 15, 18, 19}, C = {13, 15, 19, 20}.
Ce sont ses nombres, et c’est justement l’exercice où il fallait placer
les éléments soi-même.

L’exemple de son cahier de leçons est écarté pour la même raison : B et C
y sont recopiés identiques, ce qui ne peut pas être. On ne révise pas sur
une copie fautive.

Une contrainte du clavier commande l’écriture des textes à trous : il n’a
pas de touche espace. Toute réponse à écrire tient donc en un seul mot, et
le script le vérifie plutôt que de s’en souvenir.

Usage :  python work/lecons-brayne-maths.py
"""

import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-venn.py. '

MATIERE = 'Mathématiques'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'en'
CHAPITRE = 'Unit 3 — Venn diagram'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

LECONS = [
    (
        'What a Venn diagram shows', CHAPITRE, '2026-11-02', 20,
        'A Venn diagram is a special diagram used to show the relationship between a universal set '
        'and the working sets. The universal set is represented by a rectangle, and each working '
        'set is represented by an oval drawn inside that rectangle.',
        've-diagramme',
        'Un rectangle marqué epsilon, deux ovales A et B à l’intérieur, qui se chevauchent.',
        [
            (
                'definition',
                'A Venn diagram shows the relationship between a universal set and the working sets.',
                've-relation',
                'Deux ovales qui se chevauchent dans un rectangle, la zone commune teintée.',
                [
                    ('simple',
                     'A Venn diagram is a picture of how sets go together: what they share, and what they do not.'),
                    ('analogie',
                     'It is like a seating plan: the rectangle is the classroom, each oval is a group, and some pupils belong to two groups.'),
                ],
                [
                    ('qcm', 1, {'question': 'What does a Venn diagram show?',
                                'options': ['The relationship between sets', 'The price of each set',
                                            'The name of the teacher']},
                     {'index': 0}, 'It shows the relationship between a universal set and the working sets.'),
                    ('vrai_faux', 1, {'statement': 'A Venn diagram shows how sets are related.'},
                     {'value': True}, 'Yes. That is exactly what it is for.'),
                    ('association', 2, {'question': 'Match each word with what it means.',
                                        'gauche': ['Venn diagram', 'Universal set', 'Working set'],
                                        'droite': ['A picture of how sets are related',
                                                   'All the elements we are working with',
                                                   'One of the sets drawn inside']},
                     {'order': [0, 1, 2]}, 'The diagram shows the relationship; the universal set holds everything.'),
                    ('texte_a_trous', 3,
                     {'text': 'A Venn diagram shows the {{1}} between sets.', 'blanks': 1},
                     {'values': ['relationship']}, 'The relationship: what the sets share and what they do not.'),
                    ('qcm', 4, {'question': 'A Venn diagram is used to show…',
                                'options': ['a relationship', 'a multiplication', 'a measurement']},
                     {'index': 0}, 'A relationship between sets.'),
                ],
            ),
            (
                'definition',
                'The universal set holds every element we are working with. It is represented by a rectangle.',
                've-rectangle',
                'Un rectangle seul, marqué epsilon dans le coin haut gauche, vide à l’intérieur.',
                [
                    ('simple', 'The universal set is everything we are working with. We draw it as a rectangle.'),
                    ('visuel', 'The rectangle is the wall of the room. Nothing in the exercise lives outside it.'),
                    ('pas_a_pas',
                     'Draw the rectangle first. Write epsilon in a corner. Then draw the ovals inside it.'),
                ],
                [
                    ('qcm', 1, {'question': 'How is the universal set drawn?',
                                'options': ['As a rectangle', 'As an oval', 'As a triangle']},
                     {'index': 0}, 'The universal set is drawn as a rectangle.'),
                    ('vrai_faux', 1, {'statement': 'The universal set is drawn as an oval.'},
                     {'value': False}, 'No. The rectangle is the universal set; the ovals are the working sets.'),
                    ('qcm', 2, {'question': 'Which sign stands for the universal set?',
                                'options': ['epsilon', 'plus', 'minus']},
                     {'index': 0}, 'The Greek letter epsilon. Some books write U instead.'),
                    ('texte_a_trous', 3,
                     {'text': 'The universal set is represented by a {{1}}.', 'blanks': 1},
                     {'values': ['rectangle']}, 'A rectangle. The working sets are ovals inside it.'),
                    ('vrai_faux', 4, {'statement': 'The rectangle of a Venn diagram is the universal set.'},
                     {'value': True}, 'True.'),
                ],
            ),
            (
                'definition',
                'Each working set is represented by an oval drawn inside the rectangle.',
                've-ovale',
                'Un rectangle avec trois ovales séparés à l’intérieur, marqués A, B et C.',
                [
                    ('simple', 'Every set we work on gets its own oval, and every oval sits inside the rectangle.'),
                    ('visuel', 'Ovals inside the rectangle, never outside it: the universal set holds them all.'),
                ],
                [
                    ('qcm', 1, {'question': 'How is a working set drawn?',
                                'options': ['As an oval', 'As a rectangle', 'As a straight line']},
                     {'index': 0}, 'Each working set is an oval.'),
                    ('vrai_faux', 1, {'statement': 'The ovals are drawn inside the rectangle.'},
                     {'value': True}, 'Yes. The universal set holds every working set.'),
                    ('association', 2, {'question': 'Match the shape with the set.',
                                        'gauche': ['Rectangle', 'Oval'],
                                        'droite': ['Universal set', 'Working set']},
                     {'order': [0, 1]}, 'Rectangle for the universal set, oval for each working set.'),
                    ('texte_a_trous', 3,
                     {'text': 'The working sets are represented by {{1}}.', 'blanks': 1},
                     {'values': ['ovals']}, 'Ovals, drawn inside the rectangle.'),
                    ('qcm', 4, {'question': 'An oval in a Venn diagram is…',
                                'options': ['a working set', 'the universal set', 'an answer']},
                     {'index': 0}, 'A working set.'),
                ],
            ),
            (
                'relation',
                'To complete a Venn diagram, always start by filling the intersection, the part common to both sets.',
                've-commencer',
                'Deux ovales, la zone commune remplie en premier et numérotée 1, les côtés numérotés 2 et 3.',
                [
                    ('simple',
                     'Start in the middle. Put the common elements there first, then fill what is left on each side.'),
                    ('pas_a_pas',
                     'One: find what is in both sets and write it in the middle. Two: fill the rest of each oval. Three: write what is left outside.'),
                    ('analogie',
                     'Like sharing kola nuts: you first set aside what belongs to both, then each one takes the rest.'),
                ],
                [
                    ('qcm', 1, {'question': 'Where do you start when filling a Venn diagram?',
                                'options': ['In the intersection', 'Outside the rectangle', 'Anywhere at all']},
                     {'index': 0}, 'Always start with the intersection, the common part.'),
                    ('chronologie', 2, {'question': 'Put the steps in the right order.',
                                        'tokens': ['Fill the common part', 'Fill the rest of each oval',
                                                   'Write what is left outside the ovals']},
                     {'order': [0, 1, 2]}, 'Common part first, then each oval, then the outside.'),
                    ('texte_a_trous', 3, {'text': 'Always start by filling the {{1}}.', 'blanks': 1},
                     {'values': ['intersection']}, 'The intersection: the part common to both sets.'),
                    ('vrai_faux', 4, {'statement': 'You should fill the outside of the ovals first.'},
                     {'value': False}, 'No. The common part comes first.'),
                ],
            ),
        ],
    ),
    (
        'Intersection, union, subset and disjoint sets', CHAPITRE, '2026-11-02', 21,
        'Four relationships can be read on a Venn diagram. The intersection is what belongs to both '
        'sets. The union is everything that belongs to one set or the other. A subset is a set drawn '
        'entirely inside another. Disjoint sets have nothing in common, so their ovals never touch.',
        've-quatre',
        'Quatre vignettes : intersection teintée, union teintée, ovale dans un ovale, ovales séparés.',
        [
            (
                'definition',
                'The intersection of two sets is made of the elements that belong to both of them at the same time.',
                've-intersection',
                'Deux ovales P et K, la seule zone commune teintée, le reste pâle.',
                [
                    ('simple', 'The intersection is the middle part: what is in this set AND in that one.'),
                    ('visuel',
                     'In the book, P and K share chair and table. The intersection of P and K is chair and table.'),
                    ('analogie', 'Two friends empty their pockets. The intersection is what they both happen to carry.'),
                ],
                [
                    ('qcm', 1, {'question': 'The intersection of two sets is made of…',
                                'options': ['what is in both sets', 'what is in neither set',
                                            'everything in the rectangle']},
                     {'index': 0}, 'The intersection holds what belongs to both sets.'),
                    ('vrai_faux', 1, {'statement': 'The intersection is the part shared by the two ovals.'},
                     {'value': True}, 'Yes, the part where the ovals overlap.'),
                    ('qcm', 2, {'question': 'Sets P and K share chair and table. So the intersection of P and K is…',
                                'options': ['chair and table', 'pots and plates', 'radio and clock']},
                     {'index': 0}, 'Chair and table, the only two in both ovals.'),
                    ('texte_a_trous', 3, {'text': 'The elements in both sets form the {{1}}.', 'blanks': 1},
                     {'values': ['intersection']}, 'The intersection.'),
                    ('vrai_faux', 4, {'statement': 'An element of the intersection belongs to both sets.'},
                     {'value': True}, 'True, that is what puts it in the middle.'),
                ],
            ),
            (
                'definition',
                'The union of two sets is made of every element of the first set and every element of the second, each written once.',
                've-union',
                'Deux ovales C et D entièrement teintés, bord commun compris.',
                [
                    ('simple', 'The union takes everything: the left side, the middle, and the right side.'),
                    ('pas_a_pas',
                     'Write the elements of the first set. Add those of the second. Write a shared element only once.'),
                ],
                [
                    ('qcm', 1, {'question': 'The union of two sets is made of…',
                                'options': ['everything in one set or the other', 'only what they share',
                                            'only what they do not share']},
                     {'index': 0}, 'The union takes everything from both sets.'),
                    ('vrai_faux', 1, {'statement': 'In a union, a shared element is written twice.'},
                     {'value': False}, 'No. Each element is written once, even when both sets have it.'),
                    ('association', 2, {'question': 'Match each one with what it takes.',
                                        'gauche': ['Intersection', 'Union'],
                                        'droite': ['Only what both sets share', 'Everything in both sets']},
                     {'order': [0, 1]}, 'Intersection takes the middle only; union takes it all.'),
                    ('texte_a_trous', 3,
                     {'text': 'Everything in both sets together forms the {{1}}.', 'blanks': 1},
                     {'values': ['union']}, 'The union.'),
                    ('qcm', 4, {'question': 'Which one is bigger, the union or the intersection?',
                                'options': ['The union', 'The intersection', 'They are always equal']},
                     {'index': 0}, 'The union contains the intersection, and usually more.'),
                ],
            ),
            (
                'definition',
                'A set is a subset of another when every one of its elements is also in that other set. Its oval is drawn inside.',
                've-sous-ensemble',
                'Un petit ovale B entièrement contenu dans un grand ovale A, dans un rectangle.',
                [
                    ('simple', 'If everything in B is also in A, then B is a subset of A.'),
                    ('visuel',
                     'In the book, parlour and garage are rooms of the house: the oval B sits fully inside A.'),
                    ('analogie',
                     'The pupils of your class are a subset of the pupils of the school. All of them, with none left out.'),
                ],
                [
                    ('qcm', 1, {'question': 'When is B a subset of A?',
                                'options': ['When every element of B is in A', 'When B and A share one element',
                                            'When B and A share nothing']},
                     {'index': 0}, 'Every element of B must be in A. Not one left out.'),
                    ('vrai_faux', 1, {'statement': 'A subset is drawn as an oval inside another oval.'},
                     {'value': True}, 'Yes, fully inside.'),
                    ('qcm', 2, {'question': 'The oval B is drawn completely inside the oval A. This shows…',
                                'options': ['a subset', 'disjoint sets', 'an intersection']},
                     {'index': 0}, 'A subset.'),
                    ('texte_a_trous', 3, {'text': 'When all of B is inside A, B is a {{1}} of A.', 'blanks': 1},
                     {'values': ['subset']}, 'A subset.'),
                    ('vrai_faux', 4, {'statement': 'If one element of B is outside A, B is still a subset of A.'},
                     {'value': False}, 'No. One element outside is enough to break it.'),
                ],
            ),
            (
                'definition',
                'Two sets are disjoint when they have nothing in common. Their ovals do not touch.',
                've-disjoints',
                'Deux ovales T et C nettement séparés dans un rectangle, aucun contact.',
                [
                    ('simple', 'Disjoint means no common element at all, so the ovals stay apart.'),
                    ('visuel',
                     'In the book, the toilet things and the things of the yard share nothing. The two ovals are drawn apart.'),
                ],
                [
                    ('qcm', 1, {'question': 'Two sets are disjoint when they…',
                                'options': ['have nothing in common', 'share one element',
                                            'have the same elements']},
                     {'index': 0}, 'Nothing in common at all.'),
                    ('vrai_faux', 1, {'statement': 'The ovals of two disjoint sets overlap.'},
                     {'value': False}, 'No. They are drawn apart, because there is nothing to share.'),
                    ('qcm', 2, {'question': 'The two ovals do not touch. What does the diagram show?',
                                'options': ['Disjoint sets', 'A subset', 'A union']},
                     {'index': 0}, 'Disjoint sets.'),
                    ('texte_a_trous', 3,
                     {'text': 'Sets with nothing in common are called {{1}} sets.', 'blanks': 1},
                     {'values': ['disjoint']}, 'Disjoint sets.'),
                    ('qcm', 4, {'question': 'What is the intersection of two disjoint sets?',
                                'options': ['It is empty', 'It is the whole rectangle', 'It is one element']},
                     {'index': 0}, 'Empty: they share nothing.'),
                ],
            ),
            (
                'relation',
                'Each of the four pictures has a name: ovals that overlap, an oval inside another, ovals drawn apart.',
                've-reconnaitre',
                'Quatre petites vignettes alignées, chacune sous son nom.',
                [
                    ('simple', 'Look at the drawing before looking at the words: how the ovals sit tells you the name.'),
                    ('pas_a_pas',
                     'Do the ovals touch? If not, disjoint. Is one inside the other? Subset. Do they overlap? Then they have an intersection.'),
                ],
                [
                    ('qcm', 1, {'question': 'Which picture shows a subset?',
                                'options': ['One oval inside another', 'Two ovals apart',
                                            'Two ovals that overlap']},
                     {'index': 0}, 'One oval drawn inside the other.'),
                    ('association', 2, {'question': 'Match each picture with its name.',
                                        'gauche': ['Ovals that overlap', 'One oval inside another',
                                                   'Ovals that do not touch'],
                                        'droite': ['Intersection', 'Subset', 'Disjoint sets']},
                     {'order': [0, 1, 2]}, 'The way the ovals sit gives the name.'),
                    ('texte_a_trous', 3, {'text': 'Two ovals drawn apart show {{1}} sets.', 'blanks': 1},
                     {'values': ['disjoint']}, 'Disjoint sets.'),
                    ('qcm', 4, {'question': 'Two ovals overlap. What is the shaded middle called?',
                                'options': ['The intersection', 'The union', 'The subset']},
                     {'index': 0}, 'The intersection.'),
                ],
            ),
        ],
    ),
    (
        'Reading a Venn diagram', CHAPITRE, '2026-11-02', 22,
        'Reading a Venn diagram means naming each region. The elements of a set are everything inside '
        'its oval, the shared parts included. Set A only means inside A and in no other oval. The '
        'middle of three ovals belongs to all three. What is outside every oval still belongs to the '
        'universal set.',
        've-lire',
        'Trois ovales A, B et C qui se chevauchent, chaque région numérotée de 1 à 7.',
        [
            (
                'relation',
                'To list the elements of a set, take everything inside its oval, including the parts shared with other sets.',
                've-lister',
                'Un ovale A teinté en entier, ses chevauchements compris, les voisins pâles.',
                [
                    ('simple', 'Follow the line of the oval with your finger. Everything inside belongs to that set.'),
                    ('pas_a_pas',
                     'Read the part that is A alone. Then the parts A shares. Put them together: that is the set A.'),
                    ('analogie', 'A pupil in two clubs is still a pupil of the first one. Sharing does not take him out.'),
                ],
                [
                    ('vrai_faux', 1, {'statement': 'An element in the middle belongs to both sets.'},
                     {'value': True}, 'Yes. It is inside both ovals, so it counts in both.'),
                    ('qcm', 1, {'question': 'To list set A, what do you take?',
                                'options': ['Everything inside its oval', 'Only the part A does not share',
                                            'Everything in the rectangle']},
                     {'index': 0}, 'Everything inside the oval, shared parts included.'),
                    ('qcm', 2, {'question': 'A is 11, 13, 15, 17, 19 and C is 13, 15, 19, 20. What is in both?',
                                'options': ['13, 15 and 19', '11 and 17', '20 only']},
                     {'index': 0}, '13, 15 and 19 are in the two lists.'),
                    ('texte_a_trous', 3,
                     {'text': 'The set 11, 13, 15, 17, 19 has {{1}} elements.', 'blanks': 1},
                     {'values': ['5']}, 'Five: 11, 13, 15, 17 and 19.'),
                    ('vrai_faux', 4,
                     {'statement': 'An element of the shared part is left out when you list the set.'},
                     {'value': False}, 'No. It is inside the oval, so it belongs to the set.'),
                ],
            ),
            (
                'relation',
                'Set A only means the elements inside A and inside no other oval. The shared parts are left out.',
                've-seulement',
                'Trois ovales, seule la région de A hors de tout chevauchement est teintée.',
                [
                    ('simple', 'Only means alone: in this oval and in no other one.'),
                    ('visuel', 'Shade A, then rub out every part A shares. What stays is A only.'),
                    ('pas_a_pas',
                     'Take the set. Remove what it shares with the second set. Remove what it shares with the third. What is left is A only.'),
                ],
                [
                    ('qcm', 1, {'question': 'Set A only means…',
                                'options': ['in A and in no other set', 'in A and in B', 'everything in A']},
                     {'index': 0}, 'In A alone, outside every other oval.'),
                    ('vrai_faux', 1, {'statement': 'Set A only is the same as set A.'},
                     {'value': False}, 'No. Set A keeps the shared parts; A only drops them.'),
                    ('qcm', 2, {'question': 'A is 11, 13, 15, 17, 19. The others hold 13, 15 and 19. A only is…',
                                'options': ['11 and 17', '13 and 15', '15 and 19']},
                     {'index': 0}, '11 and 17 are in no other set.'),
                    ('texte_a_trous', 3,
                     {'text': 'B is 12, 15, 18, 19. As 15 and 19 are shared, B only is 12 and {{1}}.', 'blanks': 1},
                     {'values': ['18']}, '12 and 18 are in B alone.'),
                    ('qcm', 4, {'question': 'C is 13, 15, 19, 20, and only 20 is in no other set. C only is…',
                                'options': ['20', '13 and 15', '15, 19 and 20']},
                     {'index': 0}, '20 alone.'),
                ],
            ),
            (
                'relation',
                'The middle region of three ovals belongs to all three sets at once.',
                've-centre',
                'Trois ovales qui se chevauchent, la seule région centrale teintée.',
                [
                    ('simple', 'The small part in the very middle is inside the three ovals at the same time.'),
                    ('pas_a_pas', 'Find what is in A and B. Among those, keep what is also in C. That is the middle.'),
                ],
                [
                    ('qcm', 1, {'question': 'The middle of three ovals is made of elements that are…',
                                'options': ['in all three sets', 'in one set only', 'outside the ovals']},
                     {'index': 0}, 'In the three sets at the same time.'),
                    ('qcm', 2, {'question': 'A, B and C all contain 15 and 19. What is in the middle region?',
                                'options': ['15 and 19', '13 and 20', '11, 12 and 17']},
                     {'index': 0}, '15 and 19 are the two in all three sets.'),
                    ('texte_a_trous', 3,
                     {'text': 'The middle region of three ovals belongs to {{1}} of them.', 'blanks': 1},
                     {'values': ['all']}, 'All three.'),
                    ('vrai_faux', 4,
                     {'statement': 'An element in the middle of three ovals is also in the first two.'},
                     {'value': True}, 'True. If it is in the three, it is in any two of them.'),
                ],
            ),
            (
                'relation',
                'An element written outside every oval still belongs to the universal set. It belongs to no working set.',
                've-dehors',
                'Un rectangle, deux ovales, trois nombres posés dans le rectangle hors des ovales.',
                [
                    ('simple',
                     'Outside the ovals but inside the rectangle: it is in the universal set and in no working set.'),
                    ('visuel',
                     'In the book, the dog, the fowls and the fence are written outside the two ovals, but still inside the rectangle.'),
                ],
                [
                    ('qcm', 1, {'question': 'A number outside every oval but inside the rectangle belongs to…',
                                'options': ['the universal set only', 'no set at all', 'every working set']},
                     {'index': 0}, 'The universal set, and no working set.'),
                    ('vrai_faux', 1, {'statement': 'What is outside the ovals belongs to no set at all.'},
                     {'value': False}, 'It still belongs to the universal set, the rectangle.'),
                    ('association', 2, {'question': 'Match the place with what it means.',
                                        'gauche': ['Inside one oval', 'Inside the shared part',
                                                   'Outside every oval'],
                                        'droite': ['In that working set', 'In both working sets',
                                                   'In the universal set only']},
                     {'order': [0, 1, 2]}, 'The place in the drawing says which sets it belongs to.'),
                    ('texte_a_trous', 3,
                     {'text': 'Outside the ovals but inside the rectangle: it is in the {{1}} set.', 'blanks': 1},
                     {'values': ['universal']}, 'The universal set.'),
                    ('qcm', 4, {'question': 'Can an element be written outside the rectangle?',
                                'options': ['No, the rectangle holds them all', 'Yes, if it is large',
                                            'Yes, if it is shared']},
                     {'index': 0}, 'No. The universal set holds every element of the exercise.'),
                ],
            ),
            (
                'relation',
                'The sign n in front of a set means the number of its elements. For the universal set it counts everything, ovals and outside.',
                've-nombre',
                'Un rectangle avec ses éléments, un compteur posé dessous indiquant un total.',
                [
                    ('simple', 'The sign n means how many. Count the elements, do not list them.'),
                    ('pas_a_pas',
                     'Count what is in the ovals. Add what is outside them. The total is n of the universal set.'),
                    ('analogie',
                     'Like counting heads in the classroom: those at the desks and those at the back, nobody left out.'),
                ],
                [
                    ('qcm', 1, {'question': 'What does the sign n in front of a set mean?',
                                'options': ['The number of its elements', 'The name of the set',
                                            'The largest element']},
                     {'index': 0}, 'How many elements the set has.'),
                    ('qcm', 2, {'question': 'A set holds 11, 13, 15, 17 and 19. What is n of that set?',
                                'options': ['5', '19', '75']},
                     {'index': 0}, 'Five elements, so n is 5.'),
                    ('texte_a_trous', 3, {'text': 'The set 12, 15, 18, 19 has n equal to {{1}}.', 'blanks': 1},
                     {'values': ['4']}, 'Four elements.'),
                    ('vrai_faux', 4,
                     {'statement': 'To find n of the universal set, you also count what is outside the ovals.'},
                     {'value': True}, 'True. Everything inside the rectangle counts.'),
                ],
            ),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total = set(), 0
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 400, 'résumé trop long : ' + titre
        assert img not in cles, 'image en double : ' + img
        cles.add(img)
        for kind, phrase, nimg, nprompt, expl, items in notions:
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 180, 'notion trop longue : ' + phrase
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
                # Le Défi est chronométré : seuls les types qui se jouent en un
                # geste y ont leur place.
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, 'question trop longue : ' + payload['question']
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 70, 'option trop longue : ' + o
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, payload
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        # Le clavier de l-app n-a pas de touche espace dans un
                        # texte à trous : une réponse en deux mots serait
                        # impossible à écrire, quoi que l-enfant sache.
                        assert ' ' not in v, 'réponse en plusieurs mots : ' + v
                        assert v.strip() == v and v != '', 'réponse mal cadrée : ' + repr(v)
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))
    return len(cles), total


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
    images, items = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-venn.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    notions = sum(len(l[7]) for l in LECONS)
    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-46s %s  %d notions' % (titre, date, len(ns)))
    print(chemin)
