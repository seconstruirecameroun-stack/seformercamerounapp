# -*- coding: utf-8 -*-
"""
Quatre leçons d-anglais pour KLEIN (CE1) — pages démêlées du lot du
5 novembre 2026 (cahier de septembre et d-octobre).

UNE FAUTE DU CAHIER, CORRIGÉE ICI.

La page sur les pluriels en f/fe illustre la règle par « chief →
chieves ». C-est faux : le pluriel de chief est chiefs. Le mot fait
partie du petit groupe qui garde son f et ajoute simplement un s —
chief, roof, belief, proof, chef. Recopier le cahier aurait appris une
faute à KLEIN. La leçon enseigne donc la règle ET son groupe
d-exceptions, et une notion entière est consacrée au piège, figure
barrée à l-appui.

CE QUE LA DICTÉE DU 19 OCTOBRE A MONTRÉ.

Six sur dix. Les deux mots barrés sont « plaies » et « pays » : le même
son, écrit avec les mauvaises lettres. Ce n-est pas un problème de
mémoire, c-est un problème de choix entre ai et ay. La dernière notion
de la leçon sur le magic e travaille exactement ce choix-là, parce que
c-est là qu-il perd ses points et nulle part ailleurs.

DEUX DATES MANQUANTES.

Les pages sur le pluriel ne portent pas de date lisible. Plutôt que
d-en inventer une, taught_on reste vide pour ces deux leçons : une
date fausse vaut moins que pas de date.

Usage :  python work/lecons-klein-anglais-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-klein-anglais-nov.py. ')

MATIERE = 'Anglais'
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

PLURIEL = 'Plural of nouns'
MOTS = 'Building words'
SONS = 'Phonics and spelling'

LECONS = [
    # ------------------------------------------------------------------ 29
    (
        'Plural of nouns ending in f or fe', PLURIEL, None, 29,
        'Most nouns that end in f or fe change that ending to ves when they mean more than '
        'one: knife becomes knives. But a small group keeps the f and only adds s: chief '
        'becomes chiefs, never chieves. Learn the rule, then learn the group that escapes it.',
        'kn-pf-couv',
        'Le mot knife à gauche, une flèche, le mot knives à droite, la terminaison en couleur.',
        [
            ('definition',
             'A noun ending in f or fe usually changes that ending to ves when it means more '
             'than one.',
             'kn-pf-regle',
             'Quatre lignes : thief/thieves, leaf/leaves, knife/knives, wife/wives.',
             [('simple', 'You take away the f or the fe at the end, and you put ves instead.'),
              ('analogie', 'Like changing shoes at the door: the foot is the same, only what '
                           'is at the end changes.')],
             [('qcm', 1, {'question': 'What is the plural of knife?',
                          'options': ['knives', 'knifes', 'knife']},
               {'index': 0}, 'Knives. The fe becomes ves.'),
              ('qcm', 1, {'question': 'What is the plural of thief?',
                          'options': ['thieves', 'thiefs', 'thievs']},
               {'index': 0}, 'Thieves.'),
              ('association', 2, {'question': 'Match each noun with its plural.',
                                  'gauche': ['leaf', 'wife', 'knife'],
                                  'droite': ['leaves', 'wives', 'knives']},
               {'order': [0, 1, 2]}, 'Each one ends in ves.'),
              ('texte_a_trous', 3,
               {'text': 'A noun ending in f or fe changes that ending to {{1}}.', 'blanks': 1},
               {'values': ['ves']}, 'To ves.'),
              ('vrai_faux', 4, {'statement': 'The plural of wife is wifes.'},
               {'value': False}, 'No. It is wives.')]),

            ('liste',
             'Life becomes lives, half becomes halves, loaf becomes loaves and shelf becomes '
             'shelves.',
             'kn-pf-plus',
             'Quatre lignes de plus : life/lives, half/halves, loaf/loaves, shelf/shelves.',
             [('simple', 'The same rule again, on four more words you already know.'),
              ('visuel', 'Look at the right column: every word ends in the same three letters, '
                         'v, e, s.')],
             [('qcm', 1, {'question': 'What is the plural of loaf?',
                          'options': ['loaves', 'loafs', 'loafes']},
               {'index': 0}, 'Loaves.'),
              ('qcm', 2, {'question': 'Mother bought two … of bread.',
                          'options': ['loaves', 'loafs', 'loaf']},
               {'index': 0}, 'Two loaves of bread.'),
              ('association', 2, {'question': 'Match each noun with its plural.',
                                  'gauche': ['half', 'shelf', 'life'],
                                  'droite': ['halves', 'shelves', 'lives']},
               {'order': [0, 1, 2]}, 'All three take ves.'),
              ('texte_a_trous', 3, {'text': 'Put the books on the {{1}}.', 'blanks': 1},
               {'values': ['shelves']}, 'On the shelves.'),
              ('vrai_faux', 4, {'statement': 'The plural of half is halves.'},
               {'value': True}, 'Yes.')]),

            ('relation',
             'The f at the end goes away and ves comes in its place: wolf becomes wolves.',
             'kn-pf-wolf',
             'Le mot wolf en haut, une flèche, le mot wolves en bas.',
             [('pas_a_pas', 'Say the word. Find the f at the end. Take it off. Write ves. '
                            'Read the new word to check it sounds right.'),
              ('simple', 'Nothing else in the word moves. Only the end changes.')],
             [('qcm', 1, {'question': 'What is the plural of wolf?',
                          'options': ['wolves', 'wolfs', 'wolfes']},
               {'index': 0}, 'Wolves.'),
              ('qcm', 2, {'question': 'In wolves, which letters replaced the f?',
                          'options': ['ves', 'es', 's']},
               {'index': 0}, 'The f became ves.'),
              ('texte_a_trous', 3, {'text': 'One wolf, two {{1}}.', 'blanks': 1},
               {'values': ['wolves']}, 'Two wolves.'),
              ('texte_a_trous', 3, {'text': 'One calf, two {{1}}.', 'blanks': 1},
               {'values': ['calves']}, 'Two calves. The same rule works on calf.'),
              ('vrai_faux', 4, {'statement': 'When f becomes ves, the start of the word '
                                             'changes too.'},
               {'value': False}, 'No. Only the ending changes.')]),

            ('definition',
             'A small group keeps the f and only adds s: chief, roof, belief, proof and chef.',
             'kn-pf-exception',
             'Quatre lignes : chief/chiefs, roof/roofs, belief/beliefs, chef/chefs.',
             [('simple', 'These words did not read the rule. They just take an s, like most '
                         'other nouns.'),
              ('histoire', 'Think of the chief of the village: he keeps what is his. His f '
                           'stays with him, and he only takes an s.')],
             [('qcm', 1, {'question': 'What is the plural of roof?',
                          'options': ['roofs', 'rooves', 'roofes']},
               {'index': 0}, 'Roofs. This word only adds s.'),
              ('qcm', 2, {'question': 'Which word does NOT take ves?',
                          'options': ['chief', 'knife', 'leaf']},
               {'index': 0}, 'Chief. It takes chiefs.'),
              ('association', 2, {'question': 'Match each noun with its plural.',
                                  'gauche': ['roof', 'belief', 'chef'],
                                  'droite': ['roofs', 'beliefs', 'chefs']},
               {'order': [0, 1, 2]}, 'All three only add s.'),
              ('texte_a_trous', 3, {'text': 'The village has two {{1}}.', 'blanks': 1},
               {'values': ['chiefs']}, 'Two chiefs.'),
              ('vrai_faux', 4, {'statement': 'Every noun ending in f changes to ves.'},
               {'value': False}, 'No. Chief, roof, belief, proof and chef only add s.')]),

            ('relation',
             'Chieves is not an English word. The plural of chief is chiefs, written with f '
             'and s.',
             'kn-pf-piege',
             'Le mot chieves barré en rouge, et en dessous le mot chiefs accepté.',
             [('simple', 'Chief keeps its f. You only put an s after it.'),
              ('visuel', 'The crossed word is the one to forget. The word under it is the '
                         'one to write.')],
             [('qcm', 1, {'question': 'Which one is correct?',
                          'options': ['chiefs', 'chieves', 'chievs']},
               {'index': 0}, 'Chiefs.'),
              ('vrai_faux', 1, {'statement': 'Chieves is the plural of chief.'},
               {'value': False}, 'No. The plural of chief is chiefs.'),
              ('qcm', 2, {'question': 'Chief keeps which letter in the plural?',
                          'options': ['f', 'v', 'e']},
               {'index': 0}, 'It keeps the f.'),
              ('texte_a_trous', 3, {'text': 'The plural of chief is {{1}}.', 'blanks': 1},
               {'values': ['chiefs']}, 'Chiefs.'),
              ('vrai_faux', 4, {'statement': 'Chief belongs to the group that keeps its f.'},
               {'value': True}, 'Yes, with roof, belief, proof and chef.')]),

            ('relation',
             'In a sentence, the plural is used when there is more than one: the tree has '
             'green leaves.',
             'kn-pf-phrase',
             'La phrase avec leaf en haut, et la même phrase avec leaves en bas.',
             [('simple', 'One leaf, many leaves. The sentence tells you which one to write.'),
              ('pas_a_pas', 'Read the sentence. Ask how many there are. If there is more than '
                            'one, write the plural.')],
             [('qcm', 1, {'question': 'The tree has green … .',
                          'options': ['leaves', 'leafs', 'leaf']},
               {'index': 0}, 'Green leaves, because a tree has many.'),
              ('chronologie', 1, {'question': 'Put the words in order.',
                                  'tokens': ['The', 'tree', 'has', 'green', 'leaves']},
               {'order': [0, 1, 2, 3, 4]}, 'The tree has green leaves.'),
              ('qcm', 2, {'question': 'My mother bought three … .',
                          'options': ['knives', 'knifes', 'knife']},
               {'index': 0}, 'Three knives.'),
              ('texte_a_trous', 3, {'text': 'The thieves ran away with two {{1}}.', 'blanks': 1},
               {'values': ['loaves']}, 'Two loaves.'),
              ('vrai_faux', 4, {'statement': 'You write leaves when there is only one leaf.'},
               {'value': False}, 'No. One leaf, many leaves.')]),
        ],
    ),

    # ------------------------------------------------------------------ 30
    (
        'Nouns with a special plural', PLURIEL, None, 30,
        'Some nouns do not take s at all. Their letters change inside the word: foot becomes '
        'feet, mouse becomes mice, child becomes children. A few do not change at all: one '
        'sheep, many sheep. These words are learnt one by one, like faces.',
        'kn-sp-couv',
        'Le mot foot à gauche, une flèche, le mot feet à droite.',
        [
            ('definition',
             'In some nouns the two letters oo become ee: foot becomes feet, tooth becomes '
             'teeth, goose becomes geese.',
             'kn-sp-oo',
             'Trois lignes : foot/feet, tooth/teeth, goose/geese.',
             [('simple', 'No s is added at all. The change happens inside the word.'),
              ('visuel', 'The two round letters oo open up and become two straight ones, ee.')],
             [('qcm', 1, {'question': 'What is the plural of foot?',
                          'options': ['feet', 'foots', 'feets']},
               {'index': 0}, 'Feet.'),
              ('qcm', 1, {'question': 'What is the plural of tooth?',
                          'options': ['teeth', 'tooths', 'teeths']},
               {'index': 0}, 'Teeth.'),
              ('association', 2, {'question': 'Match each noun with its plural.',
                                  'gauche': ['foot', 'tooth', 'goose'],
                                  'droite': ['feet', 'teeth', 'geese']},
               {'order': [0, 1, 2]}, 'In all three, oo becomes ee.'),
              ('texte_a_trous', 3, {'text': 'My two {{1}} are paining me.', 'blanks': 1},
               {'values': ['feet']}, 'My two feet.'),
              ('vrai_faux', 4, {'statement': 'The plural of tooth is tooths.'},
               {'value': False}, 'No. It is teeth.')]),

            ('relation',
             'In mouse and louse, the ending ouse becomes ice: mouse becomes mice, louse '
             'becomes lice.',
             'kn-sp-ouse',
             'Deux lignes : mouse/mice et louse/lice.',
             [('simple', 'Only two common words do this, so they are easy to remember '
                         'together.'),
              ('analogie', 'Mouse and louse are a pair: whatever one does, the other does too.')],
             [('qcm', 1, {'question': 'What is the plural of mouse?',
                          'options': ['mice', 'mouses', 'mices']},
               {'index': 0}, 'Mice.'),
              ('qcm', 2, {'question': 'What is the plural of louse?',
                          'options': ['lice', 'louses', 'lices']},
               {'index': 0}, 'Lice.'),
              ('association', 2, {'question': 'Match each noun with its plural.',
                                  'gauche': ['mouse', 'louse'],
                                  'droite': ['mice', 'lice']},
               {'order': [0, 1]}, 'Ouse becomes ice in both.'),
              ('texte_a_trous', 3, {'text': 'There are many {{1}} in our house.', 'blanks': 1},
               {'values': ['mice']}, 'Many mice.'),
              ('vrai_faux', 4, {'statement': 'The plural of mouse is mouses.'},
               {'value': False}, 'No. It is mice.')]),

            ('liste',
             'Some nouns change almost completely: child becomes children, man becomes men, '
             'woman becomes women, ox becomes oxen.',
             'kn-sp-change',
             'Quatre lignes : child/children, man/men, woman/women, ox/oxen.',
             [('simple', 'These are the oldest words in the language, and they kept their old '
                         'plurals.'),
              ('pas_a_pas', 'There is no rule to apply here. You read the word, you remember '
                            'its partner, you write it.')],
             [('qcm', 1, {'question': 'What is the plural of child?',
                          'options': ['children', 'childs', 'childrens']},
               {'index': 0}, 'Children.'),
              ('qcm', 1, {'question': 'What is the plural of man?',
                          'options': ['men', 'mans', 'mens']},
               {'index': 0}, 'Men.'),
              ('association', 2, {'question': 'Match each noun with its plural.',
                                  'gauche': ['child', 'woman', 'ox'],
                                  'droite': ['children', 'women', 'oxen']},
               {'order': [0, 1, 2]}, 'Each one has its own plural.'),
              ('texte_a_trous', 3, {'text': 'The {{1}} are dancing in the yard.', 'blanks': 1},
               {'values': ['women']}, 'The women.'),
              ('vrai_faux', 4, {'statement': 'The plural of child is childs.'},
               {'value': False}, 'No. It is children.')]),

            ('relation',
             'Person becomes people. The plural is a completely different word.',
             'kn-sp-person',
             'Le mot person en haut, une flèche, le mot people en bas.',
             [('simple', 'One person, two people. Nothing of the first word stays.'),
              ('histoire', 'One person walks into the market. Soon there are twenty of them, '
                           'and now you call them people.')],
             [('qcm', 1, {'question': 'What is the plural of person?',
                          'options': ['people', 'persons', 'peoples']},
               {'index': 0}, 'People.'),
              ('vrai_faux', 1, {'statement': 'One person, many people.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'How many letters of person stay in people?',
                          'options': ['almost none', 'all of them', 'only the s']},
               {'index': 0}, 'Almost none. It is a different word.'),
              ('texte_a_trous', 3, {'text': 'Many {{1}} came to the meeting.', 'blanks': 1},
               {'values': ['people']}, 'Many people.'),
              ('vrai_faux', 4, {'statement': 'People is the plural of person.'},
               {'value': True}, 'Yes.')]),

            ('liste',
             'A few nouns do not change at all: one sheep and many sheep, one deer and many '
             'deer, one fish and many fish.',
             'kn-sp-meme',
             'Trois lignes où le mot de gauche et celui de droite sont identiques.',
             [('simple', 'The word stays the same. Only the words around it tell you how many.'),
              ('visuel', 'Both columns are the same. That is the whole lesson of this notion.')],
             [('qcm', 1, {'question': 'What is the plural of sheep?',
                          'options': ['sheep', 'sheeps', 'sheepes']},
               {'index': 0}, 'Sheep. It does not change.'),
              ('vrai_faux', 1, {'statement': 'The plural of deer is deers.'},
               {'value': False}, 'No. It stays deer.'),
              ('qcm', 2, {'question': 'The farmer keeps seventy … .',
                          'options': ['sheep', 'sheeps', 'sheepen']},
               {'index': 0}, 'Seventy sheep.'),
              ('texte_a_trous', 3, {'text': 'He caught three {{1}} in the river.', 'blanks': 1},
               {'values': ['fish']}, 'Three fish.'),
              ('vrai_faux', 4, {'statement': 'Sheep is written the same for one and for many.'},
               {'value': True}, 'Yes.')]),

            ('relation',
             'In a sentence, the word many or a number warns you that the plural is needed.',
             'kn-sp-phrase',
             'La phrase avec mouse en haut, et la même phrase avec mice en bas.',
             [('simple', 'Words like many, two, several or some are the signal.'),
              ('pas_a_pas', 'Find the word that counts. If it counts more than one, write the '
                            'plural, even when the plural is a strange word.')],
             [('qcm', 1, {'question': 'There are many … in our house.',
                          'options': ['mice', 'mouses', 'mouse']},
               {'index': 0}, 'Many mice.'),
              ('chronologie', 1, {'question': 'Put the words in order.',
                                  'tokens': ['There', 'are', 'many', 'mice', 'here']},
               {'order': [0, 1, 2, 3, 4]}, 'There are many mice here.'),
              ('qcm', 2, {'question': 'Which word tells you to use a plural?',
                          'options': ['many', 'here', 'are']},
               {'index': 0}, 'Many.'),
              ('texte_a_trous', 3, {'text': 'Two {{1}} are standing at the door.', 'blanks': 1},
               {'values': ['men']}, 'Two men.'),
              ('vrai_faux', 4, {'statement': 'After the word many you write the singular.'},
               {'value': False}, 'No. After many you write the plural.')]),
        ],
    ),

    # ------------------------------------------------------------------ 31
    (
        'Jumbled letters', MOTS, '2026-10-21', 31,
        'Jumbled letters are the letters of one word, mixed up. Every letter is there and '
        'none is missing: your work is to put them back in order so that the word means '
        'something. Find the vowels first, then try a beginning, then read it to check.',
        'kn-jl-couv',
        'Les lettres s c o o h l en désordre en haut, et school remis en ordre en dessous.',
        [
            ('definition',
             'Jumbled letters are a set of letters that have been mixed up and need to be put '
             'back in order to form a word.',
             'kn-jl-def',
             'Les lettres n g i s en désordre, une flèche, et sing remis en ordre.',
             [('simple', 'Every letter you need is already there. Not one more, not one less.'),
              ('analogie', 'Like beads from a broken necklace: nothing is lost, everything is '
                           'out of order.')],
             [('qcm', 1, {'question': 'What are jumbled letters?',
                          'options': ['letters mixed up', 'letters that are missing',
                                      'letters that are too big']},
               {'index': 0}, 'Letters mixed up.'),
              ('qcm', 1, {'question': 'The letters n g i s give which word?',
                          'options': ['sing', 'snig', 'gins']},
               {'index': 0}, 'Sing.'),
              ('chronologie', 2, {'question': 'Put the letters in order.',
                                  'tokens': ['s', 'i', 'n', 'g']},
               {'order': [0, 1, 2, 3]}, 'Sing.'),
              ('texte_a_trous', 3,
               {'text': 'Jumbled letters must be put back in {{1}}.', 'blanks': 1},
               {'values': ['order']}, 'In order.'),
              ('vrai_faux', 4, {'statement': 'When you unjumble letters you may leave one out.'},
               {'value': False}, 'No. Every letter must be used.')]),

            ('relation',
             'The letters s c o o h l give the word school. The two letters oo stay together.',
             'kn-jl-school',
             'Les lettres s c o o h l en désordre, et school en dessous.',
             [('simple', 'Look for the letters that like to travel in pairs, such as oo or ch.'),
              ('visuel', 'In school the ch comes first, then oo, then l. Three pieces, not six '
                         'letters.')],
             [('qcm', 1, {'question': 'The letters s c o o h l give which word?',
                          'options': ['school', 'cholos', 'schoool']},
               {'index': 0}, 'School.'),
              ('qcm', 2, {'question': 'In school, which two letters stay together?',
                          'options': ['oo', 'sl', 'hs']},
               {'index': 0}, 'The two letters oo.'),
              ('qcm', 2, {'question': 'How many letters are in school?',
                          'options': ['six', 'five', 'seven']},
               {'index': 0}, 'Six letters.'),
              ('texte_a_trous', 3, {'text': 'I go to {{1}} every morning.', 'blanks': 1},
               {'values': ['school']}, 'To school.'),
              ('vrai_faux', 4, {'statement': 'School has two letters o side by side.'},
               {'value': True}, 'Yes, s c h o o l.')]),

            ('liste',
             'Four steps: read all the letters, find the vowels, try a beginning, then read '
             'the word to check it.',
             'kn-jl-steps',
             'Une liste numérotée de quatre étapes pour remettre des lettres en ordre.',
             [('pas_a_pas', 'Read every letter out loud. Pick out a, e, i, o and u. A word '
                            'almost always needs one of them. Then try a first letter.'),
              ('simple', 'The last step is the one people forget: read the word you made and '
                         'ask yourself if it exists.')],
             [('qcm', 1, {'question': 'What is the first step?',
                          'options': ['read all the letters', 'write the answer',
                                      'count the letters']},
               {'index': 0}, 'Read all the letters first.'),
              ('qcm', 1, {'question': 'Which letters do you look for first?',
                          'options': ['the vowels', 'the last letters', 'the big letters']},
               {'index': 0}, 'The vowels.'),
              ('chronologie', 2, {'question': 'Put the four steps in order.',
                                  'tokens': ['Read the letters', 'Find the vowels',
                                             'Try a beginning', 'Read it to check']},
               {'order': [0, 1, 2, 3]}, 'Read, find, try, check.'),
              ('texte_a_trous', 3, {'text': 'The letters a, e, i, o and u are the {{1}}.',
                                    'blanks': 1},
               {'values': ['vowels']}, 'The vowels.'),
              ('vrai_faux', 4, {'statement': 'The last step is to read the word and check it.'},
               {'value': True}, 'Yes.')]),

            ('relation',
             'The letters o b k o give the word book. A word can have the same letter twice.',
             'kn-jl-book',
             'Les lettres o b k o en désordre, et book en dessous.',
             [('simple', 'Two letters o are given, so the word needs two letters o.'),
              ('visuel', 'Count the letters before you start: four letters in, four letters '
                         'out.')],
             [('qcm', 1, {'question': 'The letters o b k o give which word?',
                          'options': ['book', 'kobo', 'boko']},
               {'index': 0}, 'Book.'),
              ('qcm', 2, {'question': 'How many letters o are in book?',
                          'options': ['two', 'one', 'three']},
               {'index': 0}, 'Two.'),
              ('qcm', 2, {'question': 'Can a word use the same letter twice?',
                          'options': ['yes', 'no', 'only at the end']},
               {'index': 0}, 'Yes, like book.'),
              ('texte_a_trous', 3, {'text': 'I read a {{1}} before I sleep.', 'blanks': 1},
               {'values': ['book']}, 'A book.'),
              ('vrai_faux', 4, {'statement': 'A jumbled word may use one letter twice.'},
               {'value': True}, 'Yes, if that letter is given twice.')]),

            ('relation',
             'The letters r a m f give the word farm. Trying a first letter is often what '
             'opens the word.',
             'kn-jl-farm',
             'Les lettres r a m f en désordre, et farm en dessous.',
             [('pas_a_pas', 'Put f first and read: f, a, r, m. It makes farm, a word you know. '
                            'The word is found.'),
              ('simple', 'If the first letter you try gives nothing, try another one. There '
                         'are not many to try.')],
             [('qcm', 1, {'question': 'The letters r a m f give which word?',
                          'options': ['farm', 'fram', 'marf']},
               {'index': 0}, 'Farm.'),
              ('chronologie', 2, {'question': 'Put the letters in order.',
                                  'tokens': ['f', 'a', 'r', 'm']},
               {'order': [0, 1, 2, 3]}, 'Farm.'),
              ('qcm', 2, {'question': 'Which letter begins the word farm?',
                          'options': ['f', 'r', 'm']},
               {'index': 0}, 'The letter f.'),
              ('texte_a_trous', 3, {'text': 'My father works on his {{1}}.', 'blanks': 1},
               {'values': ['farm']}, 'His farm.'),
              ('vrai_faux', 4, {'statement': 'Only one order of these letters makes a real '
                                             'word.'},
               {'value': True}, 'Yes, farm.')]),
        ],
    ),

    # ------------------------------------------------------------------ 32
    (
        'The magic e', SONS, '2026-10-22', 32,
        'A silent e at the end of a word changes the vowel before it: cap becomes cape, hat '
        'becomes hate, kit becomes kite. The e itself is never said. And the same sound can '
        'sometimes be written another way, with ai or ay, which is where mistakes happen.',
        'kn-me-couv',
        'Le mot cap à gauche, une flèche, le mot cape à droite avec le e en couleur.',
        [
            ('definition',
             'When a silent e is added at the end, the vowel before it says its own name: cap '
             'becomes cape.',
             'kn-me-regle',
             'Trois paires : cap/cape, hat/hate, kit/kite, avec le e ajouté en couleur.',
             [('simple', 'The e at the end wakes up the vowel in the middle and makes it say '
                         'its letter name.'),
              ('analogie', 'The e is like a torch at the back of the word: it does not make a '
                           'sound, it lights up the vowel in front of it.')],
             [('qcm', 1, {'question': 'What does cap become when you add e?',
                          'options': ['cape', 'capp', 'caep']},
               {'index': 0}, 'Cape.'),
              ('qcm', 1, {'question': 'What does kit become when you add e?',
                          'options': ['kite', 'kitt', 'keit']},
               {'index': 0}, 'Kite.'),
              ('association', 2, {'question': 'Match each short word with its magic e word.',
                                  'gauche': ['cap', 'hat', 'kit'],
                                  'droite': ['cape', 'hate', 'kite']},
               {'order': [0, 1, 2]}, 'Each one gains a silent e.'),
              ('texte_a_trous', 3, {'text': 'The letter added at the end is {{1}}.',
                                    'blanks': 1},
               {'values': ['e']}, 'The letter e.'),
              ('vrai_faux', 4, {'statement': 'Adding the magic e changes how the vowel '
                                             'sounds.'},
               {'value': True}, 'Yes, the vowel then says its own name.')]),

            ('liste',
             'Not becomes note, cub becomes cube, rid becomes ride. The rule works on every '
             'vowel.',
             'kn-me-plus',
             'Trois paires : not/note, cub/cube, rid/ride.',
             [('simple', 'The same trick works whether the vowel is a, e, i, o or u.'),
              ('visuel', 'The left word is short and quick. The right word is longer in the '
                         'mouth.')],
             [('qcm', 1, {'question': 'What does not become when you add e?',
                          'options': ['note', 'nott', 'noet']},
               {'index': 0}, 'Note.'),
              ('qcm', 1, {'question': 'What does cub become when you add e?',
                          'options': ['cube', 'cubb', 'cueb']},
               {'index': 0}, 'Cube.'),
              ('association', 2, {'question': 'Match each short word with its magic e word.',
                                  'gauche': ['not', 'cub', 'rid'],
                                  'droite': ['note', 'cube', 'ride']},
               {'order': [0, 1, 2]}, 'Each one takes a silent e.'),
              ('texte_a_trous', 3, {'text': 'I like to {{1}} my bicycle.', 'blanks': 1},
               {'values': ['ride']}, 'To ride.'),
              ('vrai_faux', 4, {'statement': 'The magic e works only on the vowel a.'},
               {'value': False}, 'No. It works on a, e, i, o and u.')]),

            ('relation',
             'The magic e is never pronounced. You write it, but you do not say it.',
             'kn-me-silence',
             'Le mot cube avec son e final en gris, marqué silent.',
             [('simple', 'Say cube out loud. You hear cub, then a long u. You never hear the e '
                         'at the end.'),
              ('histoire', 'The e stands at the door of the word without speaking. It is there '
                           'to open the door for the vowel, nothing more.')],
             [('qcm', 1, {'question': 'Do you say the e at the end of cube?',
                          'options': ['no, never', 'yes, always', 'only sometimes']},
               {'index': 0}, 'No, it is silent.'),
              ('vrai_faux', 1, {'statement': 'The magic e is written but not said.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Why is the e written if it is not said?',
                          'options': ['to change the vowel', 'to make the word longer',
                                      'to look nice']},
               {'index': 0}, 'To change the vowel before it.'),
              ('texte_a_trous', 3, {'text': 'The magic e is {{1}}, you never say it.',
                                    'blanks': 1},
               {'values': ['silent']}, 'Silent.'),
              ('vrai_faux', 4, {'statement': 'You must pronounce the e at the end of kite.'},
               {'value': False}, 'No. It is silent.')]),

            ('liste',
             'There are five families of magic e: a_e as in grade, e_e as in scene, i_e as in '
             'shine, o_e as in vote and u_e as in cute.',
             'kn-me-familles',
             'Cinq lignes : le motif a_e, e_e, i_e, o_e, u_e et un exemple pour chacun.',
             [('simple', 'One family for each vowel, and one word to remember each family by.'),
              ('visuel', 'Read the pattern on the left as a vowel, a gap, then the e. The word '
                         'on the right fills the gap.')],
             [('qcm', 1, {'question': 'Which family does grade belong to?',
                          'options': ['a_e', 'e_e', 'o_e']},
               {'index': 0}, 'The a_e family.'),
              ('qcm', 1, {'question': 'How many families of magic e are there?',
                          'options': ['five', 'three', 'ten']},
               {'index': 0}, 'Five, one for each vowel.'),
              ('association', 2, {'question': 'Match each word with its family.',
                                  'gauche': ['shine', 'vote', 'cute'],
                                  'droite': ['i_e', 'o_e', 'u_e']},
               {'order': [0, 1, 2]}, 'Look at the vowel before the e.'),
              ('texte_a_trous', 3, {'text': 'The word vote belongs to the family o_{{1}}.',
                                    'blanks': 1},
               {'values': ['e']}, 'The family o_e.'),
              ('vrai_faux', 4, {'statement': 'Every vowel has its own magic e family.'},
               {'value': True}, 'Yes, all five of them.')]),

            ('relation',
             'The same long a sound can be written three ways: a_e as in made, ai as in maid, '
             'and ay as in may.',
             'kn-me-ai-ay',
             'Trois mots made, maid, may, avec les lettres du son en rouge dans chacun.',
             [('simple', 'Your ear hears one sound. Your hand must choose between three '
                         'spellings.'),
              ('pas_a_pas', 'If the sound is at the very end of the word, write ay. If it is '
                            'inside the word, it is usually ai, or a with a magic e.')],
             [('qcm', 1, {'question': 'Which three spellings give the long a sound?',
                          'options': ['a_e, ai, ay', 'a, e, i', 'ee, oo, ea']},
               {'index': 0}, 'A_e, ai and ay.'),
              ('qcm', 1, {'question': 'Do made, maid and may sound the same?',
                          'options': ['yes', 'no', 'only two of them']},
               {'index': 0}, 'Yes, the same long a.'),
              ('association', 2, {'question': 'Match each word with its spelling.',
                                  'gauche': ['made', 'maid', 'may'],
                                  'droite': ['a_e', 'ai', 'ay']},
               {'order': [0, 1, 2]}, 'Three spellings for one sound.'),
              ('texte_a_trous', 3, {'text': 'When the sound comes at the end, write {{1}}.',
                                    'blanks': 1},
               {'values': ['ay']}, 'Write ay.'),
              ('vrai_faux', 4, {'statement': 'One sound can have more than one spelling.'},
               {'value': True}, 'Yes, that is why you must look as well as listen.')]),

            ('relation',
             'At the end of a word the long a sound is written ay: plays, pays, days. Plaies '
             'is not a word.',
             'kn-me-plays',
             'Le mot plaies barré en rouge, et en dessous le mot plays accepté.',
             [('simple', 'Plays, pays, days, says. They all end in ay plus s.'),
              ('pas_a_pas', 'Ask where the sound is. At the end of the word, it is ay. Then '
                            'add the s after it, never inside it.')],
             [('qcm', 1, {'question': 'Which one is correct?',
                          'options': ['plays', 'plaies', 'playes']},
               {'index': 0}, 'Plays.'),
              ('vrai_faux', 1, {'statement': 'Plaies is a correct English word.'},
               {'value': False}, 'No. The word is plays.'),
              ('qcm', 2, {'question': 'He … for the school team.',
                          'options': ['plays', 'plaies', 'plais']},
               {'index': 0}, 'He plays.'),
              ('texte_a_trous', 3, {'text': 'My father {{1}} the school fees.', 'blanks': 1},
               {'values': ['pays']}, 'Pays, with ay.'),
              ('vrai_faux', 4, {'statement': 'At the end of a word the long a sound is '
                                             'written ay.'},
               {'value': True}, 'Yes: plays, pays, days.')]),
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
                    # La bonne réponse ne doit pas se reconnaître à sa longueur.
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
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        assert ' ' not in v, 'réponse en plusieurs mots : ' + v
                        assert v.isalpha(), 'réponse non tapable au clavier : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie'
                                   else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'chronologie':
                        # Deux jetons identiques sont indiscernables à l-écran :
                        # l-enfant ne peut pas savoir lequel il a déjà posé.
                        assert len(set(payload['tokens'])) == longueur, \
                            'jeton en double : ' + str(payload['tokens'])
                    else:
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    # La faute du cahier doit être corrigée DANS la leçon, pas seulement
    # dans le commentaire en tête de fichier.
    tout = json.dumps(LECONS, ensure_ascii=False, default=str)
    assert 'chiefs' in tout, 'la correction de chieves a disparu'
    assert 'chieves' in tout, 'le piège doit être montré pour être écarté'
    assert 'plays' in tout and 'plaies' in tout, \
        'les deux mots ratés de la dictée doivent être travaillés'

    # Les clés d-images doivent être EXACTEMENT celles que le module de
    # dessin produit. Une clé mal tapée ne casse rien ici : elle casse
    # plus tard, dans l-application, par une image absente.
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-klein-anglais-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    manquantes = cles - dessinees
    inutiles = dessinees - cles
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(
        sorted(manquantes))
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
    chemin = os.path.join(racine, 'app', 'public', 'seed-klein-anglais-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-40s %-20s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
