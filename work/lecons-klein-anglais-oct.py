# -*- coding: utf-8 -*-
"""
Dix leçons d-anglais pour KLEIN (CE1) — cahier du 26 octobre au 2 novembre
2026.

Tout est rangé sous Anglais, y compris les mois, la tricherie et le sol :
ces pages-là sont écrites en anglais et c-est en anglais qu-elles seront
interrogées. Les chapitres les séparent.

TROIS ENDROITS OÙ LE CAHIER SE TROMPE, et ce qui a été fait.

1. Les démonstratifs. Le cahier écrit « Those: it shows plural of nouns
   that are close », puis trois lignes plus bas « That: it shows singular
   for nouns that are far away ». Les deux ne peuvent pas être vrais à la
   fois : those est le pluriel de that. Le cahier se contredit lui-même,
   donc le suivre est impossible. La leçon enseigne la règle standard —
   this/these près, that/those loin — et une figure la montre en grille.

2. Les mois de 31 jours. Le cahier liste « January, March, May, August,
   October, December » : six mois. July manque. Avec quatre mois de 30
   jours et février, cela ne fait que onze mois sur douze. July est
   rétabli, et un contrôle vérifie que les trois groupes couvrent les
   douze mois exactement une fois.

3. Les irréguliers. Le cahier de KLEIN porte « bad / worse / worse » et
   « little / less / beast ». Ce sont des fautes de recopie — la colonne
   superlative répète le comparatif dans un cas, et « beast » n-est pas un
   mot de la langue. La leçon enseigne worst et least.

Le cas 1 n-est pas du même ordre que les deux autres : il porte sur ce que
la maîtresse a dicté, pas sur ce que l-enfant a mal copié. Il est signalé
au père pour qu-il tranche avec elle.

Usage :  python work/lecons-klein-anglais-oct.py
"""

import importlib.util
import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-anglais-oct.py. '

MATIERE = 'Anglais'
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

JUMBLED = 'Jumbled words and sentences'
DEMO = 'Demonstrative adjectives'
COMP = 'Comparison of adjectives'
MOIS = 'The months of the year'
CONDUITE = 'Good behaviour'
SOL = 'The soil'

LECONS = [
    # ----------------------------------------------------------------- 19
    (
        'Jumbled words', JUMBLED, '2026-10-26', 19,
        'Jumbled words are words wrongly placed that need to be put in order. Read them, find '
        'the word that begins the sentence, then write the sentence so that it makes sense.',
        'an-jw-couv',
        'Les mots en désordre en haut, une flèche, et la phrase remise en bas.',
        [
            ('definition', 'Jumbled words are words wrongly placed and need to be put in order.',
             'an-jw-def', 'Trois mots en désordre, une flèche, et les mêmes trois mots remis.',
             [('simple', 'Jumbled means mixed up. Every word is there, but not in the right place.'),
              ('analogie', 'Like beads from a broken necklace: nothing is lost, everything is out of order.')],
             [('qcm', 1, {'question': 'What are jumbled words?',
                          'options': ['Words wrongly placed', 'Words that are missing',
                                      'Words that are too long']},
               {'index': 0}, 'Words wrongly placed.'),
              ('vrai_faux', 1, {'statement': 'Jumbled words have to be put in order.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'To unjumble words you must…',
                          'options': ['put them in the right order', 'take one word away',
                                      'add a new word']},
               {'index': 0}, 'Put them in order. Nothing is added, nothing is taken away.'),
              ('texte_a_trous', 3,
               {'text': 'Jumbled words are words wrongly placed and need to be put in {{1}}.',
                'blanks': 1}, {'values': ['order']}, 'In order.'),
              ('vrai_faux', 4, {'statement': 'When you unjumble words you may leave one word out.'},
               {'value': False}, 'No. Every word must be used.')]),

            ('relation', 'The jumbled words “class am in I” become “I am in class”.',
             'an-jw-class', 'Les quatre mots mélangés, puis la phrase I am in class.',
             [('pas_a_pas', 'Who? I. Doing what? am. Where? in class. That gives: I am in class.'),
              ('visuel', 'On the picture the mixed words are at the top and the right sentence at the bottom.')],
             [('chronologie', 1, {'question': 'Put the words in order.',
                                  'tokens': ['I', 'am', 'in', 'class']},
               {'order': [0, 1, 2, 3]}, 'I am in class.'),
              ('qcm', 1, {'question': '“class am in I” put in order gives…',
                          'options': ['I am in class', 'Class I am in', 'In I am class']},
               {'index': 0}, 'I am in class.'),
              ('qcm', 2, {'question': 'Which word begins the sentence “… am in class”?',
                          'options': ['I', 'class', 'in']},
               {'index': 0}, 'I am in class.'),
              ('texte_a_trous', 3, {'text': 'I am in {{1}}.', 'blanks': 1},
               {'values': ['class']}, 'In class.'),
              ('vrai_faux', 4, {'statement': '“class am in I” is already in the right order.'},
               {'value': False}, 'No, that is why we call it jumbled.')]),

            ('relation', 'The jumbled words “clean is classroom my” become “my classroom is clean”.',
             'an-jw-clean', 'Les quatre mots mélangés, puis la phrase my classroom is clean.',
             [('pas_a_pas', 'What are we talking about? My classroom. What about it? It is clean.'),
              ('simple', 'The thing we talk about comes first, then what we say about it.')],
             [('chronologie', 1, {'question': 'Put the words in order.',
                                  'tokens': ['my', 'classroom', 'is', 'clean']},
               {'order': [0, 1, 2, 3]}, 'My classroom is clean.'),
              ('vrai_faux', 1, {'statement': '“my classroom is clean” is in the right order.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which word comes first in “… classroom is clean”?',
                          'options': ['my', 'clean', 'is']},
               {'index': 0}, 'My classroom is clean.'),
              ('texte_a_trous', 3, {'text': 'My {{1}} is clean.', 'blanks': 1},
               {'values': ['classroom']}, 'Classroom.'),
              ('qcm', 4, {'question': '“clean is classroom my” put in order gives…',
                          'options': ['my classroom is clean', 'classroom my is clean',
                                      'clean my classroom is']},
               {'index': 0}, 'My classroom is clean.')]),

            ('relation', 'In the exercise, “Is today Monday” was put in order as “Monday is today”.',
             'an-jw-monday', 'Les trois mots mélangés, puis la phrase Monday is today.',
             [('simple', 'The day comes first, then what we say about it: Monday is today.'),
              ('visuel', 'The picture shows the three words before and after.')],
             [('qcm', 1, {'question': 'In the exercise, “Is today Monday” was put in order as…',
                          'options': ['Monday is today', 'Today Monday is', 'Is Monday today']},
               {'index': 0}, 'Monday is today.'),
              ('vrai_faux', 1, {'statement': 'The answer written in the exercise was “Monday is today”.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which word begins the answer “… is today”?',
                          'options': ['Monday', 'today', 'is']},
               {'index': 0}, 'Monday is today.'),
              ('texte_a_trous', 3, {'text': 'Monday is {{1}}.', 'blanks': 1},
               {'values': ['today']}, 'Today.'),
              ('vrai_faux', 4, {'statement': '“Is today Monday” was already in the right order.'},
               {'value': False}, 'No, the words had to be moved.')]),
        ],
    ),

    # ----------------------------------------------------------------- 20
    (
        'Jumbled sentences', JUMBLED, '2026-10-26', 20,
        'Jumbled sentences are sentences that have been mixed up and do not make sense. Read '
        'them slowly, put numbers in the order the story should go, read again to verify, then '
        'copy them in the correct order.',
        'an-js-couv',
        'Trois moments d’une matinée en désordre, puis remis dans l’ordre.',
        [
            ('definition',
             'Jumbled sentences are sentences that have been mixed up, that do not make sense, and should be arranged.',
             'an-js-def', 'Trois phrases courtes en désordre, une flèche, et les mêmes remises.',
             [('simple', 'The sentences are all there, but the story does not hold together.'),
              ('analogie', 'Like the pages of a story put back in the wrong order.')],
             [('qcm', 1, {'question': 'What is a jumbled sentence?',
                          'options': ['A sentence that has been mixed up', 'A sentence that is too long',
                                      'A sentence with no verb']},
               {'index': 0}, 'One that has been mixed up.'),
              ('vrai_faux', 1, {'statement': 'Jumbled sentences should be arranged to make sense.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'A jumbled sentence does not…',
                          'options': ['make sense', 'have words', 'have letters']},
               {'index': 0}, 'It does not make sense yet.'),
              ('texte_a_trous', 3,
               {'text': 'Jumbled sentences should be arranged to make {{1}}.', 'blanks': 1},
               {'values': ['sense']}, 'Sense.'),
              ('vrai_faux', 4, {'statement': 'A jumbled sentence already makes sense.'},
               {'value': False}, 'No. That is the whole point of arranging it.')]),

            ('liste',
             'To arrange jumbled sentences: read slowly, put numbers, read again to verify, then copy in order.',
             'an-js-steps', 'Les quatre étapes numérotées, l’une sous l’autre.',
             [('pas_a_pas', 'Read. Number. Read again to check the numbers. Copy.'),
              ('simple', 'The numbers are written before you copy, so that you copy only once.')],
             [('qcm', 1, {'question': 'What do you do first with jumbled sentences?',
                          'options': ['Read them slowly', 'Copy them', 'Number them']},
               {'index': 0}, 'You read them slowly first.'),
              ('vrai_faux', 1, {'statement': 'The last step is to copy the sentences in the correct order.'},
               {'value': True}, 'Yes, copying comes last.'),
              ('chronologie', 2, {'question': 'Put the four steps in order.',
                                  'tokens': ['Read slowly', 'Put numbers', 'Read to verify',
                                             'Copy in order']},
               {'order': [0, 1, 2, 3]}, 'Read, number, verify, copy.'),
              ('texte_a_trous', 3, {'text': 'Read again to {{1}} following the numbers.', 'blanks': 1},
               {'values': ['verify']}, 'To verify.'),
              ('qcm', 4, {'question': 'Why do you read a third time?',
                          'options': ['To check the numbers', 'To add a sentence',
                                      'To make the story shorter']},
               {'index': 0}, 'To verify that the numbers are right.')]),

            ('relation',
             'In the morning story the order is: wake up, make the bed, greet the parents, take breakfast.',
             'an-js-morning', 'Les quatre moments de la matinée, numérotés dans l’ordre.',
             [('pas_a_pas', 'You get out of bed, you make it, you greet your parents, then you eat.'),
              ('simple', 'The story follows the real morning, so ask yourself what happens first.')],
             [('chronologie', 1, {'question': 'Put the morning story in order.',
                                  'tokens': ['I wake up at 6 am', 'I make my bed',
                                             'I greet my parents', 'I take my breakfast']},
               {'order': [0, 1, 2, 3]}, 'Wake up, bed, parents, breakfast.'),
              ('qcm', 1, {'question': 'What comes first in the morning story?',
                          'options': ['I wake up at 6 am', 'I take my breakfast',
                                      'I greet my parents']},
               {'index': 0}, 'Waking up comes first.'),
              ('qcm', 2, {'question': 'What comes just after “I make my bed”?',
                          'options': ['I greet my parents', 'I wake up at 6 am',
                                      'I go to school']},
               {'index': 0}, 'Greeting the parents.'),
              ('texte_a_trous', 3, {'text': 'I make my {{1}}.', 'blanks': 1},
               {'values': ['bed']}, 'My bed.'),
              ('vrai_faux', 4, {'statement': 'In the story, breakfast comes before greeting the parents.'},
               {'value': False}, 'No, you greet your parents first.')]),

            ('relation',
             'The last sentence of the morning story is “I say goodbye to my parents and go to school”.',
             'an-js-last', 'Les deux dernières phrases de la matinée.',
             [('simple', 'The story ends when you leave for school.'),
              ('pas_a_pas', 'Breakfast first, then goodbye, then school.')],
             [('qcm', 1, {'question': 'What is the last sentence of the morning story?',
                          'options': ['I say goodbye and go to school', 'I wake up at 6 am',
                                      'I make my bed']},
               {'index': 0}, 'Saying goodbye and going to school.'),
              ('vrai_faux', 1, {'statement': 'The morning story ends with going to school.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'What comes just before going to school?',
                          'options': ['I take my breakfast', 'I make my bed', 'I wake up at 6 am']},
               {'index': 0}, 'Breakfast comes just before.'),
              ('texte_a_trous', 3,
               {'text': 'I say goodbye to my parents and go to {{1}}.', 'blanks': 1},
               {'values': ['school']}, 'To school.'),
              ('vrai_faux', 4, {'statement': 'The morning story ends with “I wake up at 6 am”.'},
               {'value': False}, 'No, that is how it begins.')]),
        ],
    ),

    # ----------------------------------------------------------------- 21
    (
        'Demonstrative adjectives', DEMO, '2026-11-02', 21,
        'Demonstrative adjectives are words used to show the position of nouns. This and these '
        'are for what is near; that and those are for what is far away. This and that are '
        'singular; these and those are plural.',
        'an-dm-couv',
        'Les quatre démonstratifs alignés : this, these, that, those.',
        [
            ('definition',
             'Demonstrative adjectives are words used to show the position of nouns. They can be singular or plural.',
             'an-dm-def', 'La grille près / loin croisée avec un / plusieurs.',
             [('simple', 'They answer two questions at once: is it near or far, and is it one or many?'),
              ('visuel', 'The picture is a square cut in four: near on top, far below, one on the left.')],
             [('qcm', 1, {'question': 'What do demonstrative adjectives show?',
                          'options': ['The position of nouns', 'The colour of nouns',
                                      'The number of letters']},
               {'index': 0}, 'Where the noun is.'),
              ('vrai_faux', 1, {'statement': 'Demonstrative adjectives show where a noun is.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which one is a demonstrative adjective?',
                          'options': ['those', 'quickly', 'green']},
               {'index': 0}, 'Those shows position. Green shows colour.'),
              ('texte_a_trous', 3,
               {'text': 'Demonstrative adjectives show the {{1}} of nouns.', 'blanks': 1},
               {'values': ['position']}, 'The position.'),
              ('vrai_faux', 4, {'statement': '“beautiful” is a demonstrative adjective.'},
               {'value': False}, 'No, it describes the noun, it does not place it.')]),

            ('relation', 'This shows one noun that is near. Example: This is a cap on my head.',
             'an-dm-this', 'La grille, la case près et un, celle de this, allumée.',
             [('simple', 'Near, and only one: this.'),
              ('visuel', 'On the grid, this sits top left: near and one.')],
             [('qcm', 1, {'question': 'Which word is used for one thing that is near?',
                          'options': ['this', 'these', 'those']},
               {'index': 0}, 'This.'),
              ('vrai_faux', 1, {'statement': '“This” is used for one noun that is near.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': '… is a cap on my head.',
                          'options': ['This', 'These', 'Those']},
               {'index': 0}, 'One cap, and it is on my head, so it is near.'),
              ('texte_a_trous', 3, {'text': '{{1}} is a cap on my head.', 'blanks': 1},
               {'values': ['This']}, 'This.'),
              ('vrai_faux', 4, {'statement': '“This” is used for many nouns.'},
               {'value': False}, 'No, this is for one. These is for many.')]),

            ('relation', 'These shows many nouns that are near. Example: These are cups on the table.',
             'an-dm-these', 'La grille, la case près et plusieurs, celle de these, allumée.',
             [('simple', 'Near, and more than one: these.'),
              ('pas_a_pas', 'One cup near me: this cup. Several cups near me: these cups.')],
             [('qcm', 1, {'question': 'Which word is used for many things that are near?',
                          'options': ['these', 'this', 'that']},
               {'index': 0}, 'These.'),
              ('vrai_faux', 1, {'statement': '“These” is plural.'},
               {'value': True}, 'Yes, it is used for more than one.'),
              ('qcm', 2, {'question': '… are cups on the table.',
                          'options': ['These', 'This', 'That']},
               {'index': 0}, 'Many cups, and they are near.'),
              ('texte_a_trous', 3, {'text': '{{1}} are cups on the table.', 'blanks': 1},
               {'values': ['These']}, 'These.'),
              ('vrai_faux', 4, {'statement': '“These” is used for one noun only.'},
               {'value': False}, 'No, these is plural.')]),

            ('relation', 'That shows one noun that is far away. Example: That is a house over there.',
             'an-dm-that', 'La grille, la case loin et un, celle de that, allumée.',
             [('simple', 'Far away, and only one: that.'),
              ('pas_a_pas', 'If you have to point far away, and there is only one thing, say that.')],
             [('qcm', 1, {'question': 'Which word is used for one thing that is far away?',
                          'options': ['that', 'this', 'these']},
               {'index': 0}, 'That.'),
              ('vrai_faux', 1, {'statement': '“That” is used for a noun that is far away.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': '… is a house over there.',
                          'options': ['That', 'These', 'This']},
               {'index': 0}, 'One house, and “over there” means far away.'),
              ('texte_a_trous', 3, {'text': '{{1}} is a house over there.', 'blanks': 1},
               {'values': ['That']}, 'That.'),
              ('vrai_faux', 4, {'statement': '“That” is used for a noun that is near.'},
               {'value': False}, 'No. This is for near, that is for far away.')]),

            ('relation', 'Those shows many nouns that are far away. Example: Those are caps over there.',
             'an-dm-those', 'La grille, la case loin et plusieurs, celle de those, allumée.',
             [('simple', 'Those is the plural of that: far away, and more than one.'),
              ('pas_a_pas', 'One house far away: that house. Several houses far away: those houses.'),
              ('visuel', 'On the grid, those sits at the bottom right: far and many.')],
             [('qcm', 1, {'question': 'Which word is used for many things that are far away?',
                          'options': ['those', 'these', 'that']},
               {'index': 0}, 'Those.'),
              ('vrai_faux', 1, {'statement': '“Those” is the plural of “that”.'},
               {'value': True}, 'Yes, so it is used for things that are far away.'),
              ('qcm', 2, {'question': '… pupils write very well.',
                          'options': ['Those', 'This', 'That']},
               {'index': 0}, 'Many pupils, so it is those.'),
              ('texte_a_trous', 3, {'text': '{{1}} are caps over there.', 'blanks': 1},
               {'values': ['Those']}, 'Those.'),
              ('vrai_faux', 4, {'statement': '“Those” is used for things that are near.'},
               {'value': False}, 'No. Near and many is these. Far and many is those.')]),

            ('relation',
             'This and these are for what is near; that and those are for what is far. This and that are singular.',
             'an-dm-grid', 'La grille complète : près ou loin, un ou plusieurs.',
             [('pas_a_pas', 'Ask two questions: near or far? one or many? The two answers give the word.'),
              ('visuel', 'The grid holds all four words at once, each in its own corner.')],
             [('qcm', 1, {'question': 'Which two words are used for things that are far away?',
                          'options': ['that and those', 'this and these', 'this and that']},
               {'index': 0}, 'That and those.'),
              ('association', 2, {'question': 'Match each word with what it shows.',
                                  'gauche': ['this', 'these', 'that', 'those'],
                                  'droite': ['one, near', 'many, near', 'one, far', 'many, far']},
               {'order': [0, 1, 2, 3]}, 'Near on top, far below; one on the left, many on the right.'),
              ('qcm', 2, {'question': 'Which two words are plural?',
                          'options': ['these and those', 'this and that', 'this and these']},
               {'index': 0}, 'These and those.'),
              ('texte_a_trous', 3, {'text': 'She gave us {{1}} kolanuts.', 'blanks': 1},
               {'values': ['these']}, 'These: many, and she gives them to us, so they are near.'),
              ('qcm', 4, {'question': 'In “That man over there”, why “that”?',
                          'options': ['one man, far away', 'many men, far away', 'one man, near']},
               {'index': 0}, 'One man, and “over there” means far away.')]),
        ],
    ),

    # ----------------------------------------------------------------- 22
    (
        'Comparing with -er and -est', COMP, '2026-10-27', 22,
        'Adjectives change their form to show one thing compared to another. An adjective has '
        'three forms: the positive, the comparative and the superlative. For regular adjectives '
        'we add -er for the comparative and -est for the superlative: small, smaller, smallest.',
        'an-cr-couv',
        'Small, smaller, smallest alignés comme au tableau.',
        [
            ('definition',
             'An adjective has three forms: the positive, the comparative and the superlative.',
             'an-cr-three', 'Les trois en-têtes du tableau : positive, comparative, superlative.',
             [('simple', 'Positive is the plain word. Comparative compares two. Superlative beats all.'),
              ('pas_a_pas', 'Small is the positive. Smaller compares two. Smallest is the smallest of all.')],
             [('qcm', 1, {'question': 'How many forms does an adjective have?',
                          'options': ['Three', 'Two', 'Five']},
               {'index': 0}, 'Positive, comparative and superlative.'),
              ('vrai_faux', 1, {'statement': 'Adjectives change their form to compare one thing with another.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each word with its form.',
                                  'gauche': ['small', 'smaller', 'smallest'],
                                  'droite': ['positive', 'comparative', 'superlative']},
               {'order': [0, 1, 2]}, 'Small, smaller, smallest.'),
              ('texte_a_trous', 3,
               {'text': 'Adjectives change their {{1}} to compare one thing to another.', 'blanks': 1},
               {'values': ['form']}, 'Their form.'),
              ('qcm', 4, {'question': '“smallest” is the…',
                          'options': ['superlative', 'comparative', 'positive']},
               {'index': 0}, 'The superlative.')]),

            ('relation',
             'For regular adjectives we add -er for the comparative and -est for the superlative.',
             'an-cr-rule', 'Small, smaller, smallest, les deux dernières colonnes allumées.',
             [('simple', 'Short word? Add -er, then -est. No more, no most.'),
              ('visuel', 'On the picture the two endings are highlighted.')],
             [('qcm', 1, {'question': 'What do we add to make the comparative of a short adjective?',
                          'options': ['-er', '-est', 'more']},
               {'index': 0}, 'We add -er.'),
              ('vrai_faux', 1, {'statement': 'We add -est to make the superlative.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'The comparative of “long” is…',
                          'options': ['longer', 'longest', 'more long']},
               {'index': 0}, 'Longer.'),
              ('texte_a_trous', 3, {'text': 'Old, {{1}}, oldest.', 'blanks': 1},
               {'values': ['older']}, 'Older.'),
              ('qcm', 4, {'question': 'The superlative of “short” is…',
                          'options': ['shortest', 'shorter', 'most short']},
               {'index': 0}, 'Shortest.')]),

            ('liste',
             'Small, old, young, long and short all take -er and -est: smaller, older, younger, longer, shorter.',
             'an-cr-table', 'Les cinq adjectifs réguliers et leurs trois colonnes.',
             [('simple', 'Five short words, one single rule.'),
              ('visuel', 'The picture is the table of the exercise book, column by column.')],
             [('qcm', 1, {'question': 'The superlative of “young” is…',
                          'options': ['youngest', 'younger', 'most young']},
               {'index': 0}, 'Youngest.'),
              ('vrai_faux', 1, {'statement': '“smaller” is the comparative of “small”.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each adjective with its comparative.',
                                  'gauche': ['long', 'short', 'young'],
                                  'droite': ['longer', 'shorter', 'younger']},
               {'order': [0, 1, 2]}, 'Each one takes -er.'),
              ('texte_a_trous', 3, {'text': 'Small, smaller, {{1}}.', 'blanks': 1},
               {'values': ['smallest']}, 'Smallest.'),
              ('vrai_faux', 4, {'statement': 'The comparative of “old” is “oldest”.'},
               {'value': False}, 'No. Older compares two; oldest is the superlative.')]),

            ('relation', 'In fat and big the last letter doubles: fatter, fattest; bigger, biggest.',
             'an-cr-double', 'Fat et big avec leurs formes doublées, mises en valeur.',
             [('simple', 'One short vowel, one last letter: that letter doubles before -er and -est.'),
              ('pas_a_pas', 'Big. Double the g: bigg. Then add -er: bigger. Then -est: biggest.')],
             [('qcm', 1, {'question': 'The comparative of “big” is…',
                          'options': ['bigger', 'biger', 'more big']},
               {'index': 0}, 'Bigger, with two g.'),
              ('vrai_faux', 1, {'statement': '“fat” gives “fatter” and “fattest”.'},
               {'value': True}, 'Yes, the t doubles.'),
              ('qcm', 2, {'question': 'What happens to the last letter of “big”?',
                          'options': ['It doubles', 'It disappears', 'It becomes i']},
               {'index': 0}, 'It doubles: bigger, biggest.'),
              ('texte_a_trous', 3, {'text': 'Fat, fatter, {{1}}.', 'blanks': 1},
               {'values': ['fattest']}, 'Fattest, with two t.'),
              ('vrai_faux', 4, {'statement': 'The superlative of “big” is written “bigest”.'},
               {'value': False}, 'No, it is biggest, with two g.')]),

            ('relation', 'In happy and lazy the y becomes i: happier, happiest; lazier, laziest.',
             'an-cr-yi', 'Happy et lazy avec leurs formes en i, mises en valeur.',
             [('simple', 'A word ending in y changes that y into i before -er and -est.'),
              ('pas_a_pas', 'Happy. Change the y into i: happi. Add -er: happier. Add -est: happiest.')],
             [('qcm', 1, {'question': 'The comparative of “happy” is…',
                          'options': ['happier', 'happyer', 'more happy']},
               {'index': 0}, 'Happier: the y becomes i.'),
              ('vrai_faux', 1, {'statement': 'In “lazy” the y becomes i: lazier, laziest.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'What happens to the y of “happy”?',
                          'options': ['It becomes i', 'It doubles', 'It stays y']},
               {'index': 0}, 'It becomes i.'),
              ('texte_a_trous', 3, {'text': 'Lazy, lazier, {{1}}.', 'blanks': 1},
               {'values': ['laziest']}, 'Laziest.'),
              ('vrai_faux', 4, {'statement': 'We write “happyier”.'},
               {'value': False}, 'No. The y becomes i: happier.')]),
        ],
    ),

    # ----------------------------------------------------------------- 23
    (
        'Comparing with more and most', COMP, '2026-10-27', 23,
        'Long adjectives do not take -er and -est. We put more before the comparative and most '
        'before the superlative: beautiful, more beautiful, most beautiful.',
        'an-cm-couv',
        'Beautiful, more beautiful, most beautiful alignés.',
        [
            ('relation',
             'Long adjectives take more for the comparative and most for the superlative.',
             'an-cm-rule', 'Beautiful et ses deux formes longues, mises en valeur.',
             [('simple', 'A long word would be hard to say with -est. So we put a word in front.'),
              ('pas_a_pas', 'Beautiful. To compare two: more beautiful. To beat them all: most beautiful.')],
             [('qcm', 1, {'question': 'What do we put before a long adjective to compare two things?',
                          'options': ['more', '-er', 'most']},
               {'index': 0}, 'More.'),
              ('vrai_faux', 1, {'statement': 'Long adjectives do not take -er and -est.'},
               {'value': True}, 'Yes, they take more and most.'),
              ('qcm', 2, {'question': 'The superlative of “beautiful” is…',
                          'options': ['most beautiful', 'beautifullest', 'more beautiful']},
               {'index': 0}, 'Most beautiful.'),
              ('texte_a_trous', 3, {'text': 'Beautiful, {{1}} beautiful, most beautiful.', 'blanks': 1},
               {'values': ['more']}, 'More beautiful.'),
              ('vrai_faux', 4, {'statement': 'We say “beautifuller”.'},
               {'value': False}, 'No. We say more beautiful.')]),

            ('liste', 'Beautiful, handsome and careful take more and most.',
             'an-cm-list', 'Les trois adjectifs longs et leurs formes en more et most.',
             [('simple', 'Three long words, the same rule for all three.'),
              ('visuel', 'The picture shows the three rows of the table.')],
             [('qcm', 1, {'question': 'The comparative of “careful” is…',
                          'options': ['more careful', 'carefuller', 'most careful']},
               {'index': 0}, 'More careful.'),
              ('vrai_faux', 1, {'statement': '“handsome” takes more and most.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each adjective with its comparative.',
                                  'gauche': ['beautiful', 'handsome', 'careful'],
                                  'droite': ['more beautiful', 'more handsome', 'more careful']},
               {'order': [0, 1, 2]}, 'Each one takes more.'),
              ('texte_a_trous', 3, {'text': 'Careful, more careful, {{1}} careful.', 'blanks': 1},
               {'values': ['most']}, 'Most careful.'),
              ('qcm', 4, {'question': 'Which one is written correctly?',
                          'options': ['most handsome', 'handsomest', 'more most handsome']},
               {'index': 0}, 'Most handsome.')]),

            ('liste', 'Wonderful and gracious take more and most.',
             'an-cm-list2', 'Wonderful et gracious avec leurs formes en more et most.',
             [('simple', 'Two more long words that follow the same rule.'),
              ('pas_a_pas', 'Wonderful. More wonderful. Most wonderful.')],
             [('qcm', 1, {'question': 'The superlative of “wonderful” is…',
                          'options': ['most wonderful', 'wonderfullest', 'more wonderful']},
               {'index': 0}, 'Most wonderful.'),
              ('vrai_faux', 1, {'statement': '“gracious” takes more and most.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'The comparative of “gracious” is…',
                          'options': ['more gracious', 'graciouser', 'most gracious']},
               {'index': 0}, 'More gracious.'),
              ('texte_a_trous', 3, {'text': 'Wonderful, more wonderful, {{1}} wonderful.', 'blanks': 1},
               {'values': ['most']}, 'Most wonderful.'),
              ('vrai_faux', 4, {'statement': 'We say “graciouser”.'},
               {'value': False}, 'No. We say more gracious.')]),

            ('liste', 'Intelligent and expensive take more and most.',
             'an-cm-list3', 'Intelligent et expensive avec leurs formes en more et most.',
             [('simple', 'The longer the word, the surer the rule.'),
              ('analogie', 'Nobody would say “intelligentest”: it would not even be easy to say.')],
             [('qcm', 1, {'question': 'The comparative of “intelligent” is…',
                          'options': ['more intelligent', 'intelligenter', 'most intelligent']},
               {'index': 0}, 'More intelligent.'),
              ('vrai_faux', 1, {'statement': '“expensive” takes more and most.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'The superlative of “expensive” is…',
                          'options': ['most expensive', 'expensivest', 'more expensive']},
               {'index': 0}, 'Most expensive.'),
              ('texte_a_trous', 3, {'text': 'Intelligent, more intelligent, {{1}} intelligent.', 'blanks': 1},
               {'values': ['most']}, 'Most intelligent.'),
              ('vrai_faux', 4, {'statement': 'We say “expensiver”.'},
               {'value': False}, 'No. We say more expensive.')]),

            ('relation', 'Great is a short adjective: it gives greater and greatest, not more great.',
             'an-cm-great', 'Great, greater, greatest, les deux dernières colonnes allumées.',
             [('simple', 'More and most are only for long words. Great is short, so it takes -er and -est.'),
              ('pas_a_pas', 'Count the parts of the word: great has one. One part means -er and -est.')],
             [('qcm', 1, {'question': 'The comparative of “great” is…',
                          'options': ['greater', 'more great', 'greatest']},
               {'index': 0}, 'Greater.'),
              ('vrai_faux', 1, {'statement': 'We say “more great”.'},
               {'value': False}, 'No. Great is short, so it is greater.'),
              ('qcm', 2, {'question': 'Why does “great” not take more?',
                          'options': ['It is a short adjective', 'It is a noun', 'It is irregular']},
               {'index': 0}, 'Because it is short.'),
              ('texte_a_trous', 3, {'text': 'Great, greater, {{1}}.', 'blanks': 1},
               {'values': ['greatest']}, 'Greatest.'),
              ('vrai_faux', 4, {'statement': 'The superlative of “great” is “most great”.'},
               {'value': False}, 'No, it is greatest.')]),
        ],
    ),

    # ----------------------------------------------------------------- 24
    (
        'Irregular adjectives', COMP, '2026-10-29', 24,
        'Some adjectives follow no rule at all: they take neither -er and -est nor more and most. '
        'Their comparative and superlative have to be learnt: good, better, best; bad, worse, worst.',
        'an-ci-couv',
        'Good, better, best alignés.',
        [
            ('relation',
             'Some adjectives are irregular: they take neither -er and -est nor more and most. Their forms must be learnt.',
             'an-ci-rule', 'Good, better, best, les deux dernières colonnes allumées.',
             [('simple', 'These words change completely. There is nothing to work out, only to remember.'),
              ('analogie', 'Like the names of people: you cannot guess them, you learn them.')],
             [('qcm', 1, {'question': 'What is an irregular adjective?',
                          'options': ['One that follows no rule', 'One that is very long',
                                      'One that is a noun']},
               {'index': 0}, 'One that follows no rule.'),
              ('vrai_faux', 1, {'statement': 'Irregular adjectives have to be learnt by heart.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': '“good, better, best” is…',
                          'options': ['irregular', 'regular', 'a long adjective']},
               {'index': 0}, 'Irregular: better does not come from good by a rule.'),
              ('texte_a_trous', 3, {'text': 'Good, better, {{1}}.', 'blanks': 1},
               {'values': ['best']}, 'Best.'),
              ('vrai_faux', 4, {'statement': 'The comparative of “good” is “gooder”.'},
               {'value': False}, 'No, it is better.')]),

            ('liste', 'Good gives better and best. Bad gives worse and worst.',
             'an-ci-good', 'Les deux lignes good et bad avec leurs formes.',
             [('simple', 'Good goes up to best. Bad goes down to worst.'),
              ('pas_a_pas', 'Bad, worse, worst: the last one ends in -st, like best.')],
             [('qcm', 1, {'question': 'The superlative of “bad” is…',
                          'options': ['worst', 'worse', 'baddest']},
               {'index': 0}, 'Worst.'),
              ('vrai_faux', 1, {'statement': 'The comparative of “bad” is “worse”.'},
               {'value': True}, 'Yes: bad, worse, worst.'),
              ('association', 2, {'question': 'Match each adjective with its comparative.',
                                  'gauche': ['good', 'bad'], 'droite': ['better', 'worse']},
               {'order': [0, 1]}, 'Good gives better, bad gives worse.'),
              ('texte_a_trous', 3, {'text': 'Bad, worse, {{1}}.', 'blanks': 1},
               {'values': ['worst']}, 'Worst, with a t at the end.'),
              ('vrai_faux', 4, {'statement': 'The superlative of “bad” is “worse”.'},
               {'value': False}, 'No. Worse compares two; worst is the superlative.')]),

            ('liste', 'Little gives less and least. Many and much both give more and most.',
             'an-ci-little', 'Les lignes little et many, much avec leurs formes.',
             [('simple', 'Little goes down to least. Many and much go up to most.'),
              ('pas_a_pas', 'Little, less, least: all three begin with the letter l.')],
             [('qcm', 1, {'question': 'The superlative of “little” is…',
                          'options': ['least', 'less', 'littlest']},
               {'index': 0}, 'Least.'),
              ('vrai_faux', 1, {'statement': '“many” and “much” both give “more”.'},
               {'value': True}, 'Yes, they share the same forms.'),
              ('qcm', 2, {'question': 'The comparative of “much” is…',
                          'options': ['more', 'most', 'mucher']},
               {'index': 0}, 'More.'),
              ('texte_a_trous', 3, {'text': 'Little, less, {{1}}.', 'blanks': 1},
               {'values': ['least']}, 'Least.'),
              ('vrai_faux', 4, {'statement': 'The superlative of “little” is “less”.'},
               {'value': False}, 'No. Less compares two; least is the superlative.')]),

            ('liste', 'Far gives farther or further, and farthest or furthest.',
             'an-ci-far', 'Les deux lignes de far : farther et further.',
             [('simple', 'Far has two sets of forms, and both are correct.'),
              ('pas_a_pas', 'Farther goes with farthest. Further goes with furthest. Keep the pairs together.')],
             [('qcm', 1, {'question': 'The comparative of “far” is…',
                          'options': ['farther', 'farer', 'farthest']},
               {'index': 0}, 'Farther, or further.'),
              ('vrai_faux', 1, {'statement': '“far” has two comparatives: farther and further.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'The superlative that goes with “further” is…',
                          'options': ['furthest', 'farthest', 'furtherest']},
               {'index': 0}, 'Furthest.'),
              ('texte_a_trous', 3, {'text': 'Far, farther, {{1}}.', 'blanks': 1},
               {'values': ['farthest']}, 'Farthest.'),
              ('vrai_faux', 4, {'statement': 'We say “farer”.'},
               {'value': False}, 'No. We say farther or further.')]),

            ('liste', 'Old gives older or elder, and oldest or eldest.',
             'an-ci-old', 'Les deux lignes de old : older et elder.',
             [('simple', 'Old is regular with older and oldest, but it also has elder and eldest.'),
              ('pas_a_pas', 'Elder goes with eldest, as older goes with oldest.')],
             [('qcm', 1, {'question': 'Besides “older”, what is the other comparative of “old”?',
                          'options': ['elder', 'olderer', 'more old']},
               {'index': 0}, 'Elder.'),
              ('vrai_faux', 1, {'statement': '“old” has two superlatives: oldest and eldest.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'The superlative that goes with “elder” is…',
                          'options': ['eldest', 'oldest', 'elderest']},
               {'index': 0}, 'Eldest.'),
              ('texte_a_trous', 3, {'text': 'Old, elder, {{1}}.', 'blanks': 1},
               {'values': ['eldest']}, 'Eldest.'),
              ('vrai_faux', 4, {'statement': '“elder” is the superlative of “old”.'},
               {'value': False}, 'No, elder is a comparative. Eldest is the superlative.')]),
        ],
    ),

    # ----------------------------------------------------------------- 25
    (
        'The months of the year', MOIS, '2026-10-28', 25,
        'There are twelve months in a year: January, February, March, April, May, June, July, '
        'August, September, October, November and December. The first month of the year is '
        'January while the last month is December.',
        'an-mo-couv',
        'Les douze mois, janvier et décembre allumés.',
        [
            ('definition', 'There are twelve months in a year.',
             'an-mo-twelve', 'Le calendrier des douze mois.',
             [('simple', 'Twelve months, one after the other, and then the year begins again.'),
              ('visuel', 'The picture holds all twelve at once, in three columns of four.')],
             [('qcm', 1, {'question': 'How many months are there in a year?',
                          'options': ['Twelve', 'Ten', 'Seven']},
               {'index': 0}, 'Twelve.'),
              ('vrai_faux', 1, {'statement': 'There are twelve months in a year.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which one of these is a month?',
                          'options': ['August', 'Monday', 'Morning']},
               {'index': 0}, 'August. Monday is a day.'),
              ('texte_a_trous', 3, {'text': 'There are twelve {{1}} in a year.', 'blanks': 1},
               {'values': ['months']}, 'Months.'),
              ('vrai_faux', 4, {'statement': 'There are ten months in a year.'},
               {'value': False}, 'No, there are twelve.')]),

            ('liste', 'The first six months are January, February, March, April, May and June.',
             'an-mo-six', 'Le calendrier, les six premiers mois allumés.',
             [('simple', 'The first half of the year: January to June.'),
              ('pas_a_pas', 'January, February, March, April, May, June. Then the year is half gone.')],
             [('qcm', 1, {'question': 'Which month comes just after January?',
                          'options': ['February', 'March', 'December']},
               {'index': 0}, 'February.'),
              ('vrai_faux', 1, {'statement': 'March comes before April.'},
               {'value': True}, 'Yes.'),
              ('chronologie', 2, {'question': 'Put these months in order.',
                                  'tokens': ['March', 'April', 'May', 'June']},
               {'order': [0, 1, 2, 3]}, 'March, April, May, June.'),
              ('texte_a_trous', 3, {'text': 'January, February, {{1}}, April.', 'blanks': 1},
               {'values': ['March']}, 'March.'),
              ('qcm', 4, {'question': 'Which month comes just before June?',
                          'options': ['May', 'July', 'April']},
               {'index': 0}, 'May.')]),

            ('liste', 'The last six months are July, August, September, October, November and December.',
             'an-mo-rest', 'Le calendrier, les six derniers mois allumés.',
             [('simple', 'The second half of the year: July to December.'),
              ('pas_a_pas', 'July, August, September, October, November, December. Then the year ends.')],
             [('qcm', 1, {'question': 'Which month comes just after July?',
                          'options': ['August', 'September', 'June']},
               {'index': 0}, 'August.'),
              ('vrai_faux', 1, {'statement': 'October comes before November.'},
               {'value': True}, 'Yes.'),
              ('chronologie', 2, {'question': 'Put these months in order.',
                                  'tokens': ['September', 'October', 'November', 'December']},
               {'order': [0, 1, 2, 3]}, 'September, October, November, December.'),
              ('texte_a_trous', 3, {'text': 'October, November, {{1}}.', 'blanks': 1},
               {'values': ['December']}, 'December.'),
              ('qcm', 4, {'question': 'Which month comes just before September?',
                          'options': ['August', 'October', 'July']},
               {'index': 0}, 'August.')]),

            ('relation', 'The first month of the year is January.',
             'an-mo-first', 'Le calendrier, janvier allumé.',
             [('simple', 'The year begins with January.'),
              ('visuel', 'On the picture only January is lit: it is the one that opens the year.')],
             [('qcm', 1, {'question': 'Which is the first month of the year?',
                          'options': ['January', 'December', 'June']},
               {'index': 0}, 'January.'),
              ('vrai_faux', 1, {'statement': 'The year begins with January.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which month has no month before it?',
                          'options': ['January', 'February', 'December']},
               {'index': 0}, 'January: it is the first.'),
              ('texte_a_trous', 3, {'text': 'The first month of the year is {{1}}.', 'blanks': 1},
               {'values': ['January']}, 'January.'),
              ('vrai_faux', 4, {'statement': 'The first month of the year is December.'},
               {'value': False}, 'No. December is the last one.')]),

            ('relation', 'The last month of the year is December.',
             'an-mo-last', 'Le calendrier, décembre allumé.',
             [('simple', 'The year ends with December.'),
              ('visuel', 'On the picture only December is lit: it is the one that closes the year.')],
             [('qcm', 1, {'question': 'Which is the last month of the year?',
                          'options': ['December', 'January', 'November']},
               {'index': 0}, 'December.'),
              ('vrai_faux', 1, {'statement': 'The year ends with December.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which month has no month after it?',
                          'options': ['December', 'November', 'January']},
               {'index': 0}, 'December: it is the last.'),
              ('texte_a_trous', 3, {'text': 'The last month of the year is {{1}}.', 'blanks': 1},
               {'values': ['December']}, 'December.'),
              ('vrai_faux', 4, {'statement': 'The last month of the year is November.'},
               {'value': False}, 'No. November is followed by December.')]),
        ],
    ),

    # ----------------------------------------------------------------- 26
    (
        'The number of days in each month', MOIS, '2026-10-28', 26,
        'Four months have 30 days: April, June, September and November. Seven months have 31 '
        'days: January, March, May, July, August, October and December. February has 28 days in '
        'a normal year and 29 days in a leap year.',
        'an-jo-couv',
        'Trois cartes : 31 jours, 30 jours, 28 ou 29 jours.',
        [
            ('liste', 'Four months have 30 days: April, June, September and November.',
             'an-jo-30', 'Le calendrier, les quatre mois de 30 jours allumés.',
             [('simple', 'Only four months have 30 days. All four are lit on the picture.'),
              ('pas_a_pas', 'April, June, September, November. Four months, no more.')],
             [('qcm', 1, {'question': 'How many days has September?',
                          'options': ['30', '31', '28']},
               {'index': 0}, '30 days.'),
              ('vrai_faux', 1, {'statement': 'April has 30 days.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which one of these months has 30 days?',
                          'options': ['November', 'August', 'March']},
               {'index': 0}, 'November. August and March have 31.'),
              ('texte_a_trous', 3,
               {'text': 'April, {{1}}, September and November have 30 days.', 'blanks': 1},
               {'values': ['June']}, 'June.'),
              ('vrai_faux', 4, {'statement': 'June has 31 days.'},
               {'value': False}, 'No, June has 30.')]),

            ('liste',
             'Seven months have 31 days: January, March, May, July, August, October and December.',
             'an-jo-31', 'Le calendrier, les sept mois de 31 jours allumés.',
             [('simple', 'Seven months have 31 days. Count them on the picture: there are seven.'),
              ('pas_a_pas', 'January, March, May, July, August, October, December.'),
              ('visuel', 'July is lit with the others: it has 31 days too.')],
             [('qcm', 1, {'question': 'How many days has July?',
                          'options': ['31', '30', '28']},
               {'index': 0}, '31 days.'),
              ('vrai_faux', 1, {'statement': 'January, March and May have 31 days.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which one of these months has 31 days?',
                          'options': ['October', 'April', 'February']},
               {'index': 0}, 'October.'),
              ('texte_a_trous', 3,
               {'text': 'May, {{1}}, August, October and December have 31 days.', 'blanks': 1},
               {'values': ['July']}, 'July.'),
              ('vrai_faux', 4, {'statement': 'July has 30 days.'},
               {'value': False}, 'No, July has 31 days.')]),

            ('relation', 'February has 28 days in a normal year and 29 days in a leap year.',
             'an-jo-feb', 'Le calendrier, février seul allumé.',
             [('simple', 'February is the only month that changes from one year to another.'),
              ('pas_a_pas', 'Most years: 28 days. Every fourth year, a leap year: 29 days.')],
             [('qcm', 1, {'question': 'How many days has February in a normal year?',
                          'options': ['28', '29', '30']},
               {'index': 0}, '28 days.'),
              ('vrai_faux', 1, {'statement': 'February has 29 days in a leap year.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'In a leap year February has…',
                          'options': ['29 days', '28 days', '31 days']},
               {'index': 0}, '29 days.'),
              ('texte_a_trous', 3, {'text': 'February has 29 days in a {{1}} year.', 'blanks': 1},
               {'values': ['leap']}, 'A leap year.'),
              ('vrai_faux', 4, {'statement': 'February always has 28 days.'},
               {'value': False}, 'No: 29 in a leap year.')]),

            ('relation',
             'Seven months have 31 days, four months have 30 days, and one month has 28 or 29 days.',
             'an-jo-count', 'Les trois groupes et leur compte : sept, quatre, un.',
             [('simple', 'Seven and four and one make twelve: every month is in one group.'),
              ('pas_a_pas', 'Count the lit months each time. Seven, then four, then February alone.')],
             [('qcm', 1, {'question': 'How many months have 31 days?',
                          'options': ['Seven', 'Four', 'Six']},
               {'index': 0}, 'Seven.'),
              ('vrai_faux', 1, {'statement': 'Four months have 30 days.'},
               {'value': True}, 'Yes: April, June, September, November.'),
              ('association', 2, {'question': 'Match each group with how many months it holds.',
                                  'gauche': ['31 days', '30 days', '28 or 29 days'],
                                  'droite': ['Seven months', 'Four months', 'One month']},
               {'order': [0, 1, 2]}, 'Seven, four and one.'),
              ('texte_a_trous', 3, {'text': '{{1}} months have 30 days.', 'blanks': 1},
               {'values': ['Four']}, 'Four.'),
              ('qcm', 4, {'question': 'Seven plus four plus one makes…',
                          'options': ['twelve months', 'eleven months', 'ten months']},
               {'index': 0}, 'Twelve: all the months of the year.')]),
        ],
    ),

    # ----------------------------------------------------------------- 27
    (
        'Cheating and truancy', CONDUITE, None, 27,
        'Cheating is acting dishonestly to gain something. It leads to failure in exams, lack of '
        'trust and respect, and hatred and stress. Truancy is the act of staying away from school '
        'without permission, and someone who does it is called a truant.',
        'an-ch-couv',
        'Une copie regardée en douce, et un pupitre vide.',
        [
            ('definition', 'Cheating is acting dishonestly to gain something.',
             'an-ch-def', 'Un regard qui passe d’une copie à l’autre.',
             [('simple', 'Dishonestly means not honestly: taking what you have not earned.'),
              ('analogie', 'Winning a race by starting before the others: you arrive first, but you did not run it.')],
             [('qcm', 1, {'question': 'What is cheating?',
                          'options': ['Acting dishonestly to gain something', 'Working very hard',
                                      'Asking the teacher a question']},
               {'index': 0}, 'Acting dishonestly to gain something.'),
              ('vrai_faux', 1, {'statement': 'Cheating means acting dishonestly.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'A pupil who copies his friend in an exam is…',
                          'options': ['cheating', 'working', 'reading']},
               {'index': 0}, 'He is cheating.'),
              ('texte_a_trous', 3,
               {'text': 'Cheating is acting {{1}} to gain something.', 'blanks': 1},
               {'values': ['dishonestly']}, 'Dishonestly.'),
              ('vrai_faux', 4, {'statement': 'Cheating is a way of working honestly.'},
               {'value': False}, 'No, it is the opposite of honest.')]),

            ('liste',
             'Cheating leads to failure in exams, to lack of trust and respect, and to hatred and stress.',
             'an-ch-leads', 'Les trois conséquences, numérotées.',
             [('simple', 'Three things follow from cheating, and none of them is good.'),
              ('pas_a_pas', 'First you fail. Then nobody trusts you. Then come hatred and stress.')],
             [('qcm', 1, {'question': 'What does cheating lead to?',
                          'options': ['Failure in exams', 'Good marks', 'More friends']},
               {'index': 0}, 'Failure in exams.'),
              ('vrai_faux', 1, {'statement': 'Cheating leads to lack of trust and respect.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Cheating also leads to…',
                          'options': ['hatred and stress', 'peace and rest', 'trust']},
               {'index': 0}, 'Hatred and stress.'),
              ('texte_a_trous', 3, {'text': 'Cheating leads to failure in {{1}}.', 'blanks': 1},
               {'values': ['exams']}, 'In exams.'),
              ('vrai_faux', 4, {'statement': 'Cheating brings trust and respect.'},
               {'value': False}, 'No, it takes them away.')]),

            ('definition', 'Truancy is the act of staying away from school without permission.',
             'an-ch-truancy', 'Un pupitre vide avec un point d’interrogation.',
             [('simple', 'Not every absence is truancy. What makes it truancy is the missing permission.'),
              ('pas_a_pas', 'Away from school, and nobody allowed it: that is truancy.')],
             [('qcm', 1, {'question': 'What is truancy?',
                          'options': ['Staying away from school without permission',
                                      'Coming to school early', 'Being ill at home']},
               {'index': 0}, 'Staying away without permission.'),
              ('vrai_faux', 1, {'statement': 'Truancy means staying away from school without permission.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'A pupil who stays at home and tells nobody is…',
                          'options': ['playing truant', 'on holiday', 'at school']},
               {'index': 0}, 'He is playing truant.'),
              ('texte_a_trous', 3,
               {'text': 'Truancy is staying away from school without {{1}}.', 'blanks': 1},
               {'values': ['permission']}, 'Without permission.'),
              ('vrai_faux', 4, {'statement': 'A pupil who is absent with permission is a truant.'},
               {'value': False}, 'No. With permission, it is not truancy.')]),

            ('definition',
             'Someone who stays away from school without permission is called a truant.',
             'an-ch-truant', 'Le pupitre vide et le mot truant.',
             [('simple', 'Truancy is the act; a truant is the person.'),
              ('pas_a_pas', 'The act has a name: truancy. The pupil has a name too: a truant.')],
             [('qcm', 1, {'question': 'What do we call a pupil who stays away from school?',
                          'options': ['A truant', 'A teacher', 'A prefect']},
               {'index': 0}, 'A truant.'),
              ('vrai_faux', 1, {'statement': 'A truant stays away from school without permission.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'A truant is a pupil who…',
                          'options': ['misses school without permission', 'comes to school early',
                                      'is always first in class']},
               {'index': 0}, 'He misses school without permission.'),
              ('texte_a_trous', 3,
               {'text': 'Someone who stays away from school is called a {{1}}.', 'blanks': 1},
               {'values': ['truant']}, 'A truant.'),
              ('vrai_faux', 4, {'statement': 'A truant is a pupil who never misses school.'},
               {'value': False}, 'No, it is the opposite.')]),
        ],
    ),

    # ----------------------------------------------------------------- 28
    (
        'Uses of the soil', SOL, None, 28,
        'Soil is used to plant crops and flowers, to build houses, to make things and objects '
        'like pots and statues, and as a home for animals.',
        'an-so-couv',
        'Une plante, une maison, un pot et un animal : les quatre usages du sol.',
        [
            ('liste',
             'Soil is used to plant crops and flowers, to build houses, to make pots and statues, and as a home for animals.',
             'an-so-uses', 'Les quatre usages du sol, numérotés.',
             [('simple', 'Four uses: we grow on it, we build with it, we shape it, and animals live in it.'),
              ('visuel', 'The picture lists the four, one under the other.')],
             [('qcm', 1, {'question': 'How many uses of the soil does the lesson give?',
                          'options': ['Four', 'Two', 'Six']},
               {'index': 0}, 'Four.'),
              ('vrai_faux', 1, {'statement': 'Soil is used to plant crops and to build houses.'},
               {'value': True}, 'Yes, two of the four uses.'),
              ('association', 2, {'question': 'Match each thing with what we do with it.',
                                  'gauche': ['Crops', 'Houses', 'Pots'],
                                  'droite': ['We plant them', 'We build them', 'We make them']},
               {'order': [0, 1, 2]}, 'Plant, build, make.'),
              ('texte_a_trous', 3, {'text': 'Soil is used to plant crops and {{1}}.', 'blanks': 1},
               {'values': ['flowers']}, 'And flowers.'),
              ('qcm', 4, {'question': 'Soil is a home for…',
                          'options': ['animals', 'cars', 'books']},
               {'index': 0}, 'For animals.')]),

            ('relation', 'Soil is used to plant crops and flowers.',
             'an-so-plant', 'Une plante qui pousse dans la terre.',
             [('simple', 'Roots go down into the soil and find their food there.'),
              ('analogie', 'Maize, beans and cassava all start in the soil.')],
             [('qcm', 1, {'question': 'What do we plant in the soil?',
                          'options': ['Crops and flowers', 'Pots and statues', 'Houses']},
               {'index': 0}, 'Crops and flowers.'),
              ('vrai_faux', 1, {'statement': 'We plant crops in the soil.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Maize and beans are…',
                          'options': ['crops', 'pots', 'animals']},
               {'index': 0}, 'They are crops.'),
              ('texte_a_trous', 3, {'text': 'We plant {{1}} and flowers in the soil.', 'blanks': 1},
               {'values': ['crops']}, 'Crops.'),
              ('vrai_faux', 4, {'statement': 'Flowers grow without soil.'},
               {'value': False}, 'No, they need the soil.')]),

            ('relation', 'Soil is used to build houses.',
             'an-so-house', 'Une maison aux murs de terre.',
             [('simple', 'Mud bricks are made of soil, dried and laid one on the other.'),
              ('analogie', 'Many houses in the village are built from the soil of the village itself.')],
             [('qcm', 1, {'question': 'What do we build with soil?',
                          'options': ['Houses', 'Rivers', 'Clouds']},
               {'index': 0}, 'Houses.'),
              ('vrai_faux', 1, {'statement': 'Soil is used to build houses.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Mud bricks are made from…',
                          'options': ['soil', 'water only', 'paper']},
               {'index': 0}, 'From soil.'),
              ('texte_a_trous', 3, {'text': 'Soil is used to build {{1}}.', 'blanks': 1},
               {'values': ['houses']}, 'Houses.'),
              ('vrai_faux', 4, {'statement': 'Houses are never built with soil.'},
               {'value': False}, 'No, many are.')]),

            ('relation', 'Soil is used to make things and objects like pots and statues.',
             'an-so-pot', 'Un pot de terre cuite.',
             [('simple', 'Wet soil can be shaped by hand, then left to dry hard.'),
              ('pas_a_pas', 'Dig the clay. Shape the pot. Dry it. Fire it.')],
             [('qcm', 1, {'question': 'What objects do we make from soil?',
                          'options': ['Pots and statues', 'Shoes and socks', 'Books']},
               {'index': 0}, 'Pots and statues.'),
              ('vrai_faux', 1, {'statement': 'Statues can be made from soil.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'A clay pot is made from…',
                          'options': ['soil', 'glass', 'iron']},
               {'index': 0}, 'From soil.'),
              ('texte_a_trous', 3, {'text': 'We make pots and {{1}} from soil.', 'blanks': 1},
               {'values': ['statues']}, 'Statues.'),
              ('vrai_faux', 4, {'statement': 'Pots are made from water.'},
               {'value': False}, 'No, from soil.')]),

            ('relation', 'Soil is a home for animals.',
             'an-so-home', 'Un animal posé sur la terre.',
             [('simple', 'Some animals live in the soil, others live on it.'),
              ('analogie', 'Earthworms and ants have their house under your feet.')],
             [('qcm', 1, {'question': 'Which animals live in the soil?',
                          'options': ['Earthworms', 'Birds in the sky', 'Fish in the sea']},
               {'index': 0}, 'Earthworms live in the soil.'),
              ('vrai_faux', 1, {'statement': 'Soil is a home for some animals.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Soil is a home for…',
                          'options': ['animals', 'clouds', 'stars']},
               {'index': 0}, 'For animals.'),
              ('texte_a_trous', 3, {'text': 'Soil is a {{1}} for animals.', 'blanks': 1},
               {'values': ['home']}, 'A home.'),
              ('vrai_faux', 4, {'statement': 'No animal lives in the soil.'},
               {'value': False}, 'No, many do.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues = set(), 0, 0
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
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, \
                        'question trop longue (%d) : %s' % (len(payload['question']), payload['question'])
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 70, 'option trop longue : ' + o
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']), payload['statement'])
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        # Le clavier d-un texte à trous n-a ni espace ni
                        # chiffre : une réponse en deux mots ou un nombre
                        # serait impossible à taper.
                        assert ' ' not in v, 'réponse en plusieurs mots : ' + v
                        assert v.isalpha(), 'réponse non tapable au clavier : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    # Les trois corrections apportées au cahier doivent être DANS la leçon,
    # et pas seulement dans le commentaire en tête de fichier.
    tout = json.dumps(LECONS, ensure_ascii=False, default=str)
    assert 'Those is the plural of that' in tout, 'la correction des démonstratifs a disparu'
    assert 'July' in tout and 'seven' in tout.lower(), 'July doit être dans les mois de 31 jours'
    assert 'worst' in tout and 'least' in tout, 'les superlatifs irréguliers doivent être enseignés'

    # Et les clés d-images doivent être EXACTEMENT celles que le module de
    # dessin produit. Une clé mal tapée ne casse rien ici : elle casse plus
    # tard, dans l-application, par une image absente que personne ne voit
    # tant que l-enfant n-ouvre pas cette notion-là.
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location('fig', os.path.join(ici, 'figures-anglais-oct.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    manquantes = cles - dessinees
    inutiles = dessinees - cles
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(sorted(manquantes))
    assert not inutiles, 'images dessinées mais jamais utilisées : ' + ', '.join(sorted(inutiles))
    return len(cles), total, notions_vues


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
    images, items, notions = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-anglais-oct.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-32s %-30s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
