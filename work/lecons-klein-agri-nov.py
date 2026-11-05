# -*- coding: utf-8 -*-
"""
Cinq leçons d-agriculture et de nature pour KLEIN (CE1) — pages démêlées
du lot du 5 novembre 2026 (cahier du 11 septembre au 27 octobre).

Rangées sous Sciences et technologies, et posées EN ANGLAIS, parce que
c-est la langue du cahier et donc celle dans laquelle la maîtresse
interrogera. Le libellé de la matière reste en français dans
l-application : c-est l-étagère qui est française, pas le contenu.

TROIS PAGES FONDUES EN UNE. Les outils agricoles (11 septembre), les
outils pour creuser (25 septembre) et l-entretien des outils (18
septembre) sont trois leçons du cahier sur le même objet. Pour un
enfant de CE1 elles n-en font qu-une : voici les outils, voici ceux qui
creusent, voici comment on en prend soin. Les séparer aurait donné
trois leçons de quatre questions au lieu d-une leçon complète.

LES QUESTIONS À IMAGES. Nommer une bêche est un savoir visuel. Sept
outils sont donc dessinés une seconde fois, seuls et sans étiquette,
pour que la question « which one is the spade » se joue sur des images
et non sur des mots. Une question à images ne porte jamais le nom de
l-objet, sinon elle se répond en lisant.

Usage :  python work/lecons-klein-agri-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-klein-agri-nov.py. ')

# La classe de KLEIN porte deja une matiere « Metiers », dont les alias
# sont Economie familiale, Agropastoral, Travaux manuels. C-est l-etagere
# de ces pages : le cahier fait de l-agropastoral, pas des sciences.
# Le zoo, lui, parle du vivant et reste en Sciences et technologies.
MATIERE = 'Métiers'
MATIERE_PAR_ORDRE = {41: 'Sciences et technologies'}
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

OUTILS = 'Farming tools'
TERRE = 'Working the soil'
VIVANT = 'Living things'

LECONS = [
    # ------------------------------------------------------------------ 33
    (
        'Agricultural tools and their care', OUTILS, '2026-09-11', 33,
        'Agricultural tools are the tools used to work in the farm: the cutlass, the hoe, the '
        'spade, the rake. Some of them are made to dig. A tool that is cleaned, dried, oiled '
        'and hung in its place lasts for years. A tool left dirty in the grass is lost.',
        'kn-ag-couv',
        'Quatre outils alignés : machette, houe, bêche, râteau.',
        [
            ('definition',
             'Agricultural tools are tools used to work in the farm.',
             'kn-ag-def',
             'Quatre vignettes nommées : cutlass, hoe, spade, rake.',
             [('simple', 'They are held in the hand, and they are used outside, on the soil.'),
              ('analogie', 'A farmer without tools is like a pupil without a pen: the work is '
                           'there, but nothing can be done.')],
             [('qcm', 1, {'question': 'What are agricultural tools used for?',
                          'options': ['to work in the farm', 'to cook in the kitchen',
                                      'to write in a book']},
               {'index': 0}, 'To work in the farm.'),
              ('qcm', 1, {'question': 'Which one is an agricultural tool?',
                          'options': ['a hoe', 'a spoon', 'a chair']},
               {'index': 0}, 'A hoe.'),
              ('qcm', 2, {'question': 'Which one is the rake?',
                          'images': ['kn-ag-1-rake', 'kn-ag-1-spade', 'kn-ag-1-cutlass']},
               {'index': 0}, 'The rake has many teeth in a row.'),
              ('texte_a_trous', 3,
               {'text': 'Agricultural tools are used to work in the {{1}}.', 'blanks': 1},
               {'values': ['farm']}, 'In the farm.'),
              ('vrai_faux', 4, {'statement': 'A cutlass is an agricultural tool.'},
               {'value': True}, 'Yes, it is used in the farm.')]),

            ('liste',
             'The cutlass cuts, the hoe breaks the soil, the spade lifts it and the rake '
             'gathers what is loose.',
             'kn-ag-houe',
             'Les mêmes quatre vignettes, la houe mise en avant.',
             [('simple', 'Each tool does one thing. That is why a farmer carries more than '
                         'one.'),
              ('pas_a_pas', 'Look at the end of the tool. A flat edge cuts. A wide blade '
                            'lifts. Many teeth gather.')],
             [('qcm', 1, {'question': 'Which tool is used to cut grasses?',
                          'options': ['the cutlass', 'the rake', 'the spade']},
               {'index': 0}, 'The cutlass.'),
              ('qcm', 2, {'question': 'Which one is the hoe?',
                          'images': ['kn-ag-1-hoe', 'kn-ag-1-rake', 'kn-ag-1-bar']},
               {'index': 0}, 'The hoe has a blade set across its handle.'),
              ('association', 2, {'question': 'Match each tool with its work.',
                                  'gauche': ['cutlass', 'rake', 'spade'],
                                  'droite': ['it cuts', 'it gathers', 'it lifts soil']},
               {'order': [0, 1, 2]}, 'Each tool has its own work.'),
              ('texte_a_trous', 3, {'text': 'The tool with many teeth is the {{1}}.',
                                    'blanks': 1},
               {'values': ['rake']}, 'The rake.'),
              ('vrai_faux', 4, {'statement': 'One tool can do every work in the farm.'},
               {'value': False}, 'No. Each tool does its own work.')]),

            ('liste',
             'The digging tools are the digging fork, the pick axe, the crow bar, the spade, '
             'the hoe and the cutlass.',
             'kn-ag-creuser',
             'Quatre vignettes nommées : digging fork, pick axe, crow bar, spade.',
             [('simple', 'These are the tools that go INTO the soil, not along it.'),
              ('visuel', 'Look at their ends: they are pointed or narrow, so that they can '
                         'enter the ground.')],
             [('qcm', 1, {'question': 'Which one is a digging tool?',
                          'options': ['the pick axe', 'the rake', 'the basket']},
               {'index': 0}, 'The pick axe.'),
              ('qcm', 2, {'question': 'Which one is the digging fork?',
                          'images': ['kn-ag-1-fork', 'kn-ag-1-rake', 'kn-ag-1-spade']},
               {'index': 0}, 'The digging fork has thick tines that go into the soil.'),
              ('qcm', 2, {'question': 'Which one is the crow bar?',
                          'images': ['kn-ag-1-bar', 'kn-ag-1-pick', 'kn-ag-1-hoe']},
               {'index': 0}, 'The crow bar is one straight bar with a bent end.'),
              ('texte_a_trous', 3, {'text': 'A tool that goes into the soil is a {{1}} tool.',
                                    'blanks': 1},
               {'values': ['digging']}, 'A digging tool.'),
              ('vrai_faux', 4, {'statement': 'The spade can be used for digging.'},
               {'value': True}, 'Yes, it is a digging tool.')]),

            ('liste',
             'Care for tools: clean them after use, sharpen them, oil the metal parts, dry '
             'them, hang them and keep them in the right place.',
             'kn-ag-soin',
             'Une liste numérotée des gestes qui gardent un outil en état.',
             [('simple', 'Six habits, and all six take less than five minutes after the work.'),
              ('histoire', 'The farmer who washes his cutlass every evening still has it in '
                           'ten years. His neighbour buys one every season.')],
             [('qcm', 1, {'question': 'When should a tool be cleaned?',
                          'options': ['after use', 'once a year', 'never']},
               {'index': 0}, 'After every use.'),
              ('qcm', 1, {'question': 'Why do you oil the metal parts?',
                          'options': ['to stop rust', 'to make them heavy',
                                      'to change their colour']},
               {'index': 0}, 'To stop them from rusting.'),
              ('chronologie', 2, {'question': 'Put these three in order after the work.',
                                  'tokens': ['Clean the tool', 'Dry the tool',
                                             'Hang it in its place']},
               {'order': [0, 1, 2]}, 'Clean, dry, then hang it up.'),
              ('texte_a_trous', 3, {'text': 'Oil the metal parts so that they do not {{1}}.',
                                    'blanks': 1},
               {'values': ['rust']}, 'So that they do not rust.'),
              ('vrai_faux', 4, {'statement': 'A sharp tool works better than a blunt one.'},
               {'value': True}, 'Yes, that is why you sharpen it.')]),

            ('relation',
             'A washed and dried tool keeps its metal bright and does not rust.',
             'kn-ag-propre',
             'Une houe propre, avec des éclats qui marquent le métal net.',
             [('simple', 'Water is what makes metal rust, so the tool must be dried, not only '
                         'washed.'),
              ('pas_a_pas', 'Wash the earth off. Wipe the blade with a cloth. Then put a '
                            'little oil on the metal.')],
             [('qcm', 1, {'question': 'After washing a tool, what must you do?',
                          'options': ['dry it', 'leave it wet', 'bury it']},
               {'index': 0}, 'Dry it.'),
              ('vrai_faux', 1, {'statement': 'Washing is enough, drying is not needed.'},
               {'value': False}, 'No. Water left on metal makes it rust.'),
              ('qcm', 2, {'question': 'What makes a metal tool rust?',
                          'options': ['water left on it', 'sunlight', 'its handle']},
               {'index': 0}, 'Water left on the metal.'),
              ('texte_a_trous', 3, {'text': 'Wash the tool, then {{1}} it with a cloth.',
                                    'blanks': 1},
               {'values': ['dry']}, 'Dry it.'),
              ('vrai_faux', 4, {'statement': 'A dry tool rusts faster than a wet one.'},
               {'value': False}, 'No. It is the wet one that rusts.')]),

            ('relation',
             'A tool left dirty keeps earth on its blade. The earth holds water, and the water '
             'eats the metal.',
             'kn-ag-sale',
             'Une houe avec de la terre restée collée sur le fer.',
             [('simple', 'The earth on the blade is not only dirt: it stays wet for days.'),
              ('analogie', 'Like a wet cloth folded in a bag: it is the staying wet that '
                           'spoils it, not the water itself.')],
             [('qcm', 1, {'question': 'What is wrong with the tool in the picture?',
                          'options': ['earth is left on it', 'it is too new',
                                      'it has no handle']},
               {'index': 0}, 'Earth is left on the blade.'),
              ('qcm', 2, {'question': 'Why is earth on a blade bad?',
                          'options': ['it holds water', 'it is heavy', 'it smells']},
               {'index': 0}, 'It holds water against the metal.'),
              ('vrai_faux', 2, {'statement': 'Earth left on a blade helps the tool.'},
               {'value': False}, 'No, it makes it rust.'),
              ('texte_a_trous', 3, {'text': 'Earth left on a blade holds {{1}}.', 'blanks': 1},
               {'values': ['water']}, 'It holds water.'),
              ('vrai_faux', 4, {'statement': 'A dirty tool lasts as long as a clean one.'},
               {'value': False}, 'No. It rusts and is lost sooner.')]),

            ('relation',
             'Tools are hung up and kept in the right place, so that they are found, and so '
             'that nobody is hurt by them.',
             'kn-ag-ranger',
             'Trois outils suspendus à une barre, chacun à son crochet.',
             [('simple', 'A tool on the ground is a tool somebody will step on.'),
              ('pas_a_pas', 'After drying, hang the tool on its hook. Tomorrow you will know '
                            'where it is without looking.')],
             [('qcm', 1, {'question': 'Where should tools be kept?',
                          'options': ['in the right place', 'on the ground',
                                      'in the cooking pot']},
               {'index': 0}, 'In the right place.'),
              ('qcm', 1, {'question': 'Why are garden tools hung up?',
                          'options': ['so nobody steps on them', 'so they look nice',
                                      'so they grow']},
               {'index': 0}, 'So that nobody steps on them.'),
              ('qcm', 2, {'question': 'A tool left on the ground is…',
                          'options': ['dangerous', 'safer', 'cleaner']},
               {'index': 0}, 'Dangerous.'),
              ('texte_a_trous', 3, {'text': 'Keep your tools in the right {{1}}.', 'blanks': 1},
               {'values': ['place']}, 'In the right place.'),
              ('vrai_faux', 4, {'statement': 'Hanging tools up keeps them safe and easy to '
                                             'find.'},
               {'value': True}, 'Yes, both at once.')]),
        ],
    ),

    # ------------------------------------------------------------------ 34
    (
        'Preparing the farm for planting', TERRE, '2026-10-16', 34,
        'Before anything grows, the farm is made ready. You clear it, you dig or till the '
        'soil, you add manure, you water it if there is no rain, and only then do you plant '
        'the seed or the seedling. The order matters: each step prepares the next one.',
        'kn-pr-couv',
        'Un champ labouré, une houe à gauche, une jeune pousse à droite.',
        [
            ('liste',
             'Five steps: clear the farm, dig or till the soil, add manure, water if there is '
             'no rain, then plant the seed.',
             'kn-pr-etapes',
             'Une liste numérotée des cinq étapes de préparation du champ.',
             [('simple', 'Five steps, always in this order, from the empty ground to the seed '
                         'in the soil.'),
              ('pas_a_pas', 'Nothing is planted first. The seed goes in last, when the soil is '
                            'clean, open, fed and wet.')],
             [('qcm', 1, {'question': 'What is the first step?',
                          'options': ['clear the farm', 'plant the seed', 'add manure']},
               {'index': 0}, 'Clear the farm first.'),
              ('qcm', 1, {'question': 'What is the last step?',
                          'options': ['plant the seed', 'clear the farm', 'dig the soil']},
               {'index': 0}, 'Plant the seed, last of all.'),
              ('chronologie', 2, {'question': 'Put the steps in order.',
                                  'tokens': ['Clear the farm', 'Dig the soil', 'Add manure',
                                             'Plant the seed']},
               {'order': [0, 1, 2, 3]}, 'Clear, dig, feed, plant.'),
              ('texte_a_trous', 3, {'text': 'You water the soil if there is no {{1}}.',
                                    'blanks': 1},
               {'values': ['rain']}, 'If there is no rain.'),
              ('vrai_faux', 4, {'statement': 'You plant the seed before you clear the farm.'},
               {'value': False}, 'No. Clearing comes first, planting last.')]),

            ('relation',
             'Clearing the farm means cutting away the grasses and bushes, so that the crop '
             'does not have to fight them.',
             'kn-pr-nettoyer',
             'Un champ dont les herbes sont coupées à la machette.',
             [('simple', 'Grasses drink the same water and eat the same food as your crop.'),
              ('analogie', 'Like sweeping a room before you lay the mat: you do not lay it on '
                           'top of the dirt.')],
             [('qcm', 1, {'question': 'What do you remove when you clear the farm?',
                          'options': ['grasses and bushes', 'the soil', 'the manure']},
               {'index': 0}, 'Grasses and bushes.'),
              ('qcm', 2, {'question': 'Which tool clears a farm?',
                          'images': ['kn-ag-1-cutlass', 'kn-ag-1-bar', 'kn-ag-1-fork']},
               {'index': 0}, 'The cutlass cuts the grasses.'),
              ('qcm', 2, {'question': 'Why are grasses removed?',
                          'options': ['they take the water', 'they are pretty',
                                      'they are heavy']},
               {'index': 0}, 'They take the water and the food from your crop.'),
              ('texte_a_trous', 3, {'text': 'To clear the farm you cut away the {{1}}.',
                                    'blanks': 1},
               {'values': ['grasses']}, 'The grasses.'),
              ('vrai_faux', 4, {'statement': 'Grasses left in the farm help the crop grow.'},
               {'value': False}, 'No. They take its water and its food.')]),

            ('relation',
             'Digging or tilling turns the soil over, so that it becomes soft and air can '
             'enter it.',
             'kn-pr-labour',
             'Un champ retourné, avec une houe au-dessus.',
             [('simple', 'Hard soil stops a root. Soft soil lets it go down.'),
              ('visuel', 'The lines across the field are the furrows: the soil has been turned '
                         'over, not only scratched.')],
             [('qcm', 1, {'question': 'What does digging do to the soil?',
                          'options': ['it makes it soft', 'it makes it hard',
                                      'it makes it wet']},
               {'index': 0}, 'It makes it soft.'),
              ('qcm', 2, {'question': 'Which tool is used to till the soil?',
                          'images': ['kn-ag-1-hoe', 'kn-ag-1-rake', 'kn-ag-1-bar']},
               {'index': 0}, 'The hoe breaks and turns the soil.'),
              ('qcm', 2, {'question': 'Why must soil be soft for a plant?',
                          'options': ['so the roots can go down', 'so it looks better',
                                      'so it is lighter to carry']},
               {'index': 0}, 'So that the roots can go down into it.'),
              ('texte_a_trous', 3, {'text': 'Digging makes the soil {{1}}.', 'blanks': 1},
               {'values': ['soft']}, 'Soft.'),
              ('vrai_faux', 4, {'statement': 'Roots grow more easily in hard soil.'},
               {'value': False}, 'No. They grow more easily in soft soil.')]),

            ('relation',
             'Manure is spread on the soil to feed it before anything is planted.',
             'kn-pr-fumier',
             'Un tas de fumier posé sur un champ labouré.',
             [('simple', 'The soil gives food to the plant. Manure gives food to the soil.'),
              ('histoire', 'Where the goats slept all season, the maize is always taller. The '
                           'farmer noticed, and now he carries the dung himself.')],
             [('qcm', 1, {'question': 'Why is manure added to the soil?',
                          'options': ['to feed the soil', 'to dry the soil',
                                      'to cut the grasses']},
               {'index': 0}, 'To feed the soil.'),
              ('qcm', 2, {'question': 'When is manure added?',
                          'options': ['before planting', 'after harvest', 'never']},
               {'index': 0}, 'Before planting, at step three.'),
              ('vrai_faux', 2, {'statement': 'Manure makes the soil richer.'},
               {'value': True}, 'Yes, that is why it is spread.'),
              ('texte_a_trous', 3, {'text': 'Manure is added to feed the {{1}}.', 'blanks': 1},
               {'values': ['soil']}, 'The soil.'),
              ('vrai_faux', 4, {'statement': 'A soil that is never fed stays rich for ever.'},
               {'value': False}, 'No. It becomes poor and the crops grow small.')]),

            ('definition',
             'You may plant a seed, which has not yet grown, or a seedling, which is a young '
             'plant already started.',
             'kn-pr-graine',
             'Deux vignettes : une graine, et une jeune pousse nommée seedling.',
             [('simple', 'A seed is closed and dry. A seedling already has a stem and leaves.'),
              ('visuel', 'In the picture, the one on the left has no leaf at all. The one on '
                         'the right already has two.')],
             [('qcm', 1, {'question': 'What is a seedling?',
                          'options': ['a young plant', 'a dry seed', 'a kind of soil']},
               {'index': 0}, 'A young plant.'),
              ('qcm', 1, {'question': 'Which one has no leaves yet?',
                          'options': ['the seed', 'the seedling', 'both of them']},
               {'index': 0}, 'The seed.'),
              ('association', 2, {'question': 'Match each one with what it is.',
                                  'gauche': ['seed', 'seedling'],
                                  'droite': ['closed and dry', 'already has leaves']},
               {'order': [0, 1]}, 'The seed is dry, the seedling is growing.'),
              ('texte_a_trous', 3, {'text': 'A young plant already started is a {{1}}.',
                                    'blanks': 1},
               {'values': ['seedling']}, 'A seedling.'),
              ('vrai_faux', 4, {'statement': 'A seed and a seedling are the same thing.'},
               {'value': False}, 'No. One is dry and closed, the other is already growing.')]),
        ],
    ),

    # ------------------------------------------------------------------ 35
    (
        'Caring for plants and flowers', TERRE, '2026-10-23', 35,
        'A plant that is put in the ground is not finished with you. Water it, above all in '
        'the dry season. Weed the grasses around it. Feed it with manure. Trim its leaves when '
        'they grow too long. Four habits, and the plant does the rest by itself.',
        'kn-pl-couv',
        'Une fleur, une jeune pousse et un arrosoir alignés.',
        [
            ('liste',
             'Four ways: water them in the dry season, weed around them, apply manure, and '
             'trim their leaves when they overgrow.',
             'kn-pl-etapes',
             'Une liste numérotée des quatre façons de soigner une plante.',
             [('simple', 'Water, weed, feed, trim. Four words to remember the whole lesson.'),
              ('pas_a_pas', 'Go round the plant. Is the soil dry? Water. Are there grasses? '
                            'Weed. Is it pale? Feed. Are the leaves too long? Trim.')],
             [('qcm', 1, {'question': 'How many ways of caring are in this lesson?',
                          'options': ['four', 'two', 'seven']},
               {'index': 0}, 'Four.'),
              ('qcm', 1, {'question': 'Which one is a way of caring for a plant?',
                          'options': ['weeding around it', 'stepping on it',
                                      'cutting its root']},
               {'index': 0}, 'Weeding around it.'),
              ('chronologie', 2, {'question': 'Put the four habits in the order of the lesson.',
                                  'tokens': ['Water them', 'Weed around them', 'Apply manure',
                                             'Trim the leaves']},
               {'order': [0, 1, 2, 3]}, 'Water, weed, feed, trim.'),
              ('texte_a_trous', 3, {'text': 'Apply manure to make the plants {{1}} well.',
                                    'blanks': 1},
               {'values': ['grow']}, 'To make them grow well.'),
              ('vrai_faux', 4, {'statement': 'Once a plant is in the ground it needs nothing '
                                             'more.'},
               {'value': False}, 'No. It needs water, weeding, food and trimming.')]),

            ('relation',
             'Plants are watered above all during the dry season, when no rain comes to do it '
             'for you.',
             'kn-pl-arroser',
             'Un arrosoir qui verse sur une jeune pousse.',
             [('simple', 'In the rainy season the sky waters the plants. In the dry season you '
                         'are the sky.'),
              ('analogie', 'A plant drinks every day, like you. It just cannot go to the tap.')],
             [('qcm', 1, {'question': 'When must you water plants most?',
                          'options': ['in the dry season', 'in the rainy season',
                                      'only at night']},
               {'index': 0}, 'In the dry season.'),
              ('vrai_faux', 1, {'statement': 'Plants need water to live.'},
               {'value': True}, 'Yes, every one of them.'),
              ('qcm', 2, {'question': 'Why is watering less needed in the rainy season?',
                          'options': ['the rain does it', 'plants sleep then',
                                      'the soil is hard']},
               {'index': 0}, 'The rain waters them.'),
              ('texte_a_trous', 3, {'text': 'Water the plants during the {{1}} season.',
                                    'blanks': 1},
               {'values': ['dry']}, 'The dry season.'),
              ('vrai_faux', 4, {'statement': 'A plant can live a long time with no water at '
                                             'all.'},
               {'value': False}, 'No. Without water it dries up and dies.')]),

            ('relation',
             'Weeding means removing the grasses that grow around the plant, so that it keeps '
             'the water and the food for itself.',
             'kn-pl-sarcler',
             'Une jeune pousse entre deux touffes d-herbe barrées de rouge.',
             [('simple', 'The grasses are not wicked. They are simply drinking first.'),
              ('visuel', 'In the picture the crossed tufts go, and the plant in the middle '
                         'stays.')],
             [('qcm', 1, {'question': 'What do you remove when you weed?',
                          'options': ['the grasses', 'the plant', 'the soil']},
               {'index': 0}, 'The grasses around the plant.'),
              ('qcm', 2, {'question': 'Why do grasses hurt a young plant?',
                          'options': ['they drink its water', 'they are too green',
                                      'they are too short']},
               {'index': 0}, 'They drink its water and take its food.'),
              ('vrai_faux', 2, {'statement': 'When you weed, you pull out the plant too.'},
               {'value': False}, 'No. The plant stays, only the grasses go.'),
              ('texte_a_trous', 3, {'text': 'Always {{1}} and remove the grasses around them.',
                                    'blanks': 1},
               {'values': ['weed']}, 'Weed around them.'),
              ('vrai_faux', 4, {'statement': 'Weeding leaves more water for the plant.'},
               {'value': True}, 'Yes, it no longer shares it.')]),

            ('relation',
             'Leaves that have grown too long are trimmed, so that light and air reach the '
             'whole plant.',
             'kn-pl-tailler',
             'Une plante dont une feuille trop longue est coupée à la cisaille.',
             [('simple', 'You cut the leaves, never the stem and never the root.'),
              ('pas_a_pas', 'Find the leaf that hides the others. Cut it where it joins the '
                            'stem. Leave the rest alone.')],
             [('qcm', 1, {'question': 'What do you trim on a plant?',
                          'options': ['its leaves', 'its roots', 'its stem']},
               {'index': 0}, 'Its leaves.'),
              ('qcm', 1, {'question': 'When do you trim the leaves?',
                          'options': ['when they overgrow', 'every morning',
                                      'when the plant is new']},
               {'index': 0}, 'When they have grown too long.'),
              ('qcm', 2, {'question': 'Why are long leaves trimmed?',
                          'options': ['to let light reach the plant', 'to make the plant small',
                                      'to kill the plant']},
               {'index': 0}, 'To let light and air reach the whole plant.'),
              ('texte_a_trous', 3, {'text': 'Trim their {{1}} when they overgrow.',
                                    'blanks': 1},
               {'values': ['leaves']}, 'Their leaves.'),
              ('vrai_faux', 4, {'statement': 'Trimming means cutting the root of the plant.'},
               {'value': False}, 'No. You cut only the leaves.')]),
        ],
    ),

    # ------------------------------------------------------------------ 36
    (
        'Soil enrichment', TERRE, '2026-10-27', 36,
        'Soil enrichment is the work of making the soil more fertile. You can apply manure or '
        'animal dung, add fertiliser, mulch the soil, add compost, and conserve its water. A '
        'rich soil grows a tall crop; a tired soil grows a small one.',
        'kn-so-couv',
        'Un champ avec un tas de fumier et un tas de compost.',
        [
            ('definition',
             'Soil enrichment is the process of making the soil more fertile.',
             'kn-so-moyens',
             'Une liste numérotée des cinq façons d-enrichir un sol.',
             [('simple', 'Fertile means able to feed a plant. Enrichment is giving back what '
                         'the crops took.'),
              ('analogie', 'A soil is like a purse: if you only take out and never put in, one '
                           'day there is nothing left.')],
             [('qcm', 1, {'question': 'What does soil enrichment do?',
                          'options': ['it makes the soil fertile', 'it makes the soil dry',
                                      'it removes the soil']},
               {'index': 0}, 'It makes the soil more fertile.'),
              ('qcm', 1, {'question': 'What does fertile mean?',
                          'options': ['able to feed plants', 'hard and full of stones',
                                      'always wet and cold']},
               {'index': 0}, 'Able to feed plants.'),
              ('qcm', 2, {'question': 'Which one does NOT enrich the soil?',
                          'options': ['burning all the grasses', 'adding compost',
                                      'applying manure']},
               {'index': 0}, 'Burning everything leaves nothing to feed the soil.'),
              ('texte_a_trous', 3, {'text': 'Soil enrichment makes the soil more {{1}}.',
                                    'blanks': 1},
               {'values': ['fertile']}, 'More fertile.'),
              ('vrai_faux', 4, {'statement': 'A soil stays fertile however much you harvest '
                                             'from it.'},
               {'value': False}, 'No. What is taken out must be put back.')]),

            ('relation',
             'Manure and animal dung are spread on the soil. They rot, and what they leave '
             'behind feeds the plants.',
             'kn-so-fumier',
             'Un tas de fumier posé sur un champ.',
             [('simple', 'It comes from animals, it costs nothing, and it is the oldest way of '
                         'all.'),
              ('pas_a_pas', 'Gather the dung. Spread it over the soil. Dig it in. Wait, and '
                            'then plant.')],
             [('qcm', 1, {'question': 'Where does animal dung come from?',
                          'options': ['from animals', 'from the shop', 'from the river']},
               {'index': 0}, 'From animals.'),
              ('qcm', 2, {'question': 'What does manure do in the soil?',
                          'options': ['it rots and feeds it', 'it dries it', 'it hardens it']},
               {'index': 0}, 'It rots and feeds the soil.'),
              ('association', 2, {'question': 'Match each one with where it comes from.',
                                  'gauche': ['manure', 'fertiliser'],
                                  'droite': ['from animals', 'from a factory']},
               {'order': [0, 1]}, 'One is natural, the other is bought.'),
              ('texte_a_trous', 3, {'text': 'Applying animal {{1}} enriches the soil.',
                                    'blanks': 1},
               {'values': ['dung']}, 'Animal dung.'),
              ('vrai_faux', 4, {'statement': 'Manure and fertiliser do the same work in the '
                                             'soil.'},
               {'value': True}, 'Yes, both feed it, but they do not come from the same place.')]),

            ('relation',
             'Mulching means covering the soil with dry grass or straw, so that the water stays '
             'in it instead of drying away.',
             'kn-so-paillage',
             'Un champ couvert de paille.',
             [('simple', 'The cover is a roof for the soil. Under it, the ground stays wet much '
                         'longer.'),
              ('analogie', 'Like a lid on a pot: the water does not leave, so you need to add '
                           'less.')],
             [('qcm', 1, {'question': 'What is the soil covered with when you mulch?',
                          'options': ['dry grass or straw', 'stones from the river',
                                      'water from the tap']},
               {'index': 0}, 'Dry grass or straw.'),
              ('qcm', 1, {'question': 'What does mulching keep in the soil?',
                          'options': ['the water', 'the stones', 'the air']},
               {'index': 0}, 'The water.'),
              ('qcm', 2, {'question': 'Mulching is most useful in which season?',
                          'options': ['the dry season', 'the rainy season', 'no season']},
               {'index': 0}, 'The dry season, when water is short.'),
              ('texte_a_trous', 3, {'text': 'Mulching keeps the {{1}} in the soil.',
                                    'blanks': 1},
               {'values': ['water']}, 'The water.'),
              ('vrai_faux', 4, {'statement': 'Mulching helps to conserve water.'},
               {'value': True}, 'Yes, that is exactly its work.')]),

            ('relation',
             'Compost is made from peels and leaves left to rot. When it is ready it is added '
             'to the soil.',
             'kn-so-compost',
             'Un tas de compost avec des épluchures et des feuilles dessus.',
             [('simple', 'What the kitchen throws away becomes what the farm eats.'),
              ('histoire', 'The peels of the plantains you ate last month are in the soil that '
                           'grows the plantains you will eat next year.')],
             [('qcm', 1, {'question': 'What is compost made from?',
                          'options': ['peels and leaves', 'stones and sand',
                                      'water and salt']},
               {'index': 0}, 'Peels and leaves left to rot.'),
              ('qcm', 2, {'question': 'What must happen to the peels first?',
                          'options': ['they must rot', 'they must dry in the sun',
                                      'they must be burnt']},
               {'index': 0}, 'They must rot.'),
              ('vrai_faux', 2, {'statement': 'Compost is thrown away, not used.'},
               {'value': False}, 'No. It is added to the soil.'),
              ('texte_a_trous', 3, {'text': 'Peels and leaves left to rot become {{1}}.',
                                    'blanks': 1},
               {'values': ['compost']}, 'Compost.'),
              ('vrai_faux', 4, {'statement': 'Kitchen waste can be turned into food for the '
                                             'soil.'},
               {'value': True}, 'Yes, that is what compost is.')]),
        ],
    ),

    # ------------------------------------------------------------------ 41
    (
        'The zoo', VIVANT, '2026-10-19', 41,
        'A zoo is a place where wild animals are kept for people to visit, for leisure or to '
        'study them. The words that go with it are wild life, beast, cage, park, leisure and '
        'research. In a zoo you watch the animals; you do not touch them.',
        'kn-zo-couv',
        'Une cage avec un animal, et un visiteur à côté qui la regarde.',
        [
            ('definition',
             'A zoo is a place where wild animals are kept for people to visit, for leisure or '
             'to study them.',
             'kn-zo-def',
             'Un animal dans une cage, un visiteur à côté.',
             [('simple', 'Wild animals are animals that do not live with people. In a zoo you '
                         'can see them without going to the forest.'),
              ('analogie', 'A zoo is a library of animals: you come, you look, you learn, and '
                           'you leave them where they are.')],
             [('qcm', 1, {'question': 'What is a zoo?',
                          'options': ['a place with wild animals', 'a place to buy food',
                                      'a place to sleep']},
               {'index': 0}, 'A place where wild animals are kept.'),
              ('qcm', 1, {'question': 'Which animals are kept in a zoo?',
                          'options': ['wild animals', 'only goats', 'only fish']},
               {'index': 0}, 'Wild animals.'),
              ('qcm', 2, {'question': 'Why do people go to a zoo?',
                          'options': ['for leisure or study', 'to farm the land',
                                      'to sleep for the night']},
               {'index': 0}, 'For leisure, or to study the animals.'),
              ('texte_a_trous', 3, {'text': 'A place where wild animals are kept is a {{1}}.',
                                    'blanks': 1},
               {'values': ['zoo']}, 'A zoo.'),
              ('vrai_faux', 4, {'statement': 'A zoo keeps wild animals, not farm animals.'},
               {'value': True}, 'Yes, that is what makes it a zoo.')]),

            ('liste',
             'The words of the zoo are wild life, beast, cage, park, leisure and research.',
             'kn-zo-regarder',
             'Un visiteur qui regarde un animal en cage, le regard figuré par un pointillé.',
             [('simple', 'A beast is a wild animal. Leisure is the free time you come with. '
                         'Research is the study somebody does there.'),
              ('visuel', 'The dotted line in the picture is the look: it goes from the person '
                         'to the animal, and nothing else crosses.')],
             [('qcm', 1, {'question': 'What is a beast?',
                          'options': ['a wild animal', 'a cage', 'a visitor']},
               {'index': 0}, 'A wild animal.'),
              ('qcm', 1, {'question': 'What does leisure mean?',
                          'options': ['free time', 'hard work', 'a kind of animal']},
               {'index': 0}, 'Free time.'),
              ('association', 2, {'question': 'Match each word with its meaning.',
                                  'gauche': ['beast', 'leisure', 'research'],
                                  'droite': ['a wild animal', 'free time', 'careful study']},
               {'order': [0, 1, 2]}, 'Three words of the zoo.'),
              ('texte_a_trous', 3, {'text': 'People who study the animals are doing {{1}}.',
                                    'blanks': 1},
               {'values': ['research']}, 'Research.'),
              ('vrai_faux', 4, {'statement': 'In a zoo you may touch the wild animals.'},
               {'value': False}, 'No. You watch them, you do not touch them.')]),

            ('relation',
             'The cage keeps the beast inside. It protects the visitors, and it keeps the '
             'animal from running away.',
             'kn-zo-cage',
             'Un animal derrière les barreaux d-une cage.',
             [('simple', 'The bars work in both directions: the animal stays in, the people '
                         'stay out.'),
              ('pas_a_pas', 'Stand behind the line. Look through the bars. Do not put your hand '
                            'through them.')],
             [('qcm', 1, {'question': 'What does a cage do?',
                          'options': ['it keeps the animal in', 'it feeds the animal',
                                      'it washes the animal']},
               {'index': 0}, 'It keeps the animal inside.'),
              ('qcm', 1, {'question': 'Who else does a cage protect?',
                          'options': ['the visitors', 'nobody', 'the trees']},
               {'index': 0}, 'The visitors.'),
              ('qcm', 2, {'question': 'Where is a cage usually found?',
                          'options': ['in a zoo', 'in a kitchen', 'in a farm']},
               {'index': 0}, 'In a zoo.'),
              ('texte_a_trous', 3, {'text': 'The bars of the {{1}} keep the beast inside.',
                                    'blanks': 1},
               {'values': ['cage']}, 'The cage.'),
              ('vrai_faux', 4, {'statement': 'A cage protects the people as well as holding '
                                             'the animal.'},
               {'value': True}, 'Yes, it works both ways.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, cles_items, total, notions_vues = set(), set(), 0, 0
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
                    # Les réponses sont des textes OU des images, jamais les deux.
                    assert ('options' in payload) != ('images' in payload), \
                        'un QCM a des options ou des images, pas les deux : ' + str(payload)
                    choix = payload.get('options') or payload['images']
                    assert 2 <= len(choix) <= 4, payload
                    assert len(set(choix)) == len(choix), 'choix en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(choix), payload
                    if 'images' in payload:
                        cles_items.update(choix)
                        # Une question à images ne doit pas nommer l-objet
                        # cherché dans ses propres clés : la réponse se
                        # lirait dans le nom du fichier si elle était
                        # visible, et surtout l-énoncé doit se suffire.
                        assert len(choix) >= 3, 'trop peu de choix en images : ' + str(payload)
                    else:
                        for o in choix:
                            assert len(o) <= 70, 'option trop longue : ' + o
                        bonne = len(choix[answer['index']])
                        autres = [len(o) for k, o in enumerate(choix) if k != answer['index']]
                        assert bonne <= max(autres) * 2, \
                            'bonne réponse bien plus longue que les autres : ' \
                            + payload['question']
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
                        assert len(set(payload['tokens'])) == longueur, \
                            'jeton en double : ' + str(payload['tokens'])
                    else:
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    # Les clés d-images doivent être EXACTEMENT celles que le module de
    # dessin produit — celles des leçons ET celles des questions.
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-klein-agri-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    utilisees = cles | cles_items
    manquantes = utilisees - dessinees
    inutiles = dessinees - utilisees
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(
        sorted(manquantes))
    assert not inutiles, 'images dessinées mais jamais utilisées : ' + ', '.join(sorted(inutiles))
    return len(utilisees), total, notions_vues, len(cles_items)


def paquet():
    return {
        'matiere': MATIERE, 'classe': CLASSE, 'enfant': ENFANT, 'lang': LANGUE,
        'lecons': [
            {
                'matiere': MATIERE_PAR_ORDRE.get(ordre, MATIERE),
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
    images, items, notions, en_question = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-klein-agri-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions - %d images dont %d en reponse'
          % (len(LECONS), notions, items, images, en_question))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-38s %-18s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
