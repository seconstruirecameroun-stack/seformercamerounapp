# -*- coding: utf-8 -*-
"""
Quatre leçons d-alimentation et de maison pour KLEIN (CE1) — pages
démêlées du lot du 5 novembre 2026 (cahier du 15 septembre au 20
octobre).

DEUX PAGES FONDUES EN UNE. Les ustensiles de cuisine (15 septembre) et
les meubles de la maison (22 septembre) sont deux pages du cahier qui
posent la même question : comment s-appellent les choses de la maison,
et à quoi servent-elles. Mises ensemble, elles permettent la seule
question qui compte vraiment — savoir distinguer les deux.

LA PAGE DES SIX CLASSES D-ALIMENTS a été recopiée à la hâte : le cahier
porte « vitamings », « fuits », « disease » écrit « diseasse », et la
ligne des sels minéraux mélange sel, eau, lait. Le contenu, lui, est
juste : six classes, leur source, leur rôle. Les leçons reprennent le
contenu et l-orthographe correcte, sans le signaler à l-enfant comme
une faute — ce sont des fautes de copie, pas de compréhension.

L-EAU APPARAÎT DEUX FOIS, et c-est exact : elle est une classe
d-aliment à elle seule (elle aide la digestion) et elle est aussi la
source des sels minéraux. Le cahier le dit, et c-est vrai.

Usage :  python work/lecons-klein-maison-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-klein-maison-nov.py. ')

# Economie familiale : nourriture, cuisine, conservation, maison. La
# matiere « Metiers » de la classe de KLEIN porte exactement cet alias.
MATIERE = 'Métiers'
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

NOURRITURE = 'Food'
MAISON = 'The home'

LECONS = [
    # ------------------------------------------------------------------ 37
    (
        'Food and its six classes', NOURRITURE, '2026-09-29', 37,
        'Food is any substance that living things eat or drink, or that plants absorb, to '
        'maintain life and growth. There are six classes: carbohydrates, proteins, vitamins, '
        'fats and oils, mineral salts and water. Each class has its own sources and its own '
        'work in the body.',
        'kn-fo-couv',
        'Quatre sources d-aliments alignées : grains, poisson, fruit, huile.',
        [
            ('definition',
             'Food is any substance that living things eat or drink, or that plants absorb, to '
             'maintain life and growth.',
             'kn-fo-def',
             'Quatre aliments : un tas de grains, un poisson, un fruit, un verre d-eau.',
             [('simple', 'Food is not only what you chew. Water is food, and what a plant '
                         'takes from the soil is food too.'),
              ('analogie', 'Food is to the body what fuel is to a lorry: without it, nothing '
                           'moves and nothing is repaired.')],
             [('qcm', 1, {'question': 'What is food for?',
                          'options': ['to maintain life and growth', 'to make the house clean',
                                      'to light the room']},
               {'index': 0}, 'To maintain life and growth.'),
              ('vrai_faux', 1, {'statement': 'Water is a food.'},
               {'value': True}, 'Yes, it is one of the six classes.'),
              ('qcm', 2, {'question': 'How do plants take their food?',
                          'options': ['they absorb it', 'they chew it', 'they buy it']},
               {'index': 0}, 'They absorb it.'),
              ('texte_a_trous', 3,
               {'text': 'Food keeps living things alive and helps them to {{1}}.', 'blanks': 1},
               {'values': ['grow']}, 'To grow.'),
              ('vrai_faux', 4, {'statement': 'Only animals need food, plants do not.'},
               {'value': False}, 'No. Plants absorb their food from the soil.')]),

            ('liste',
             'The six classes are carbohydrates, proteins, vitamins, fats and oils, mineral '
             'salts and water.',
             'kn-fo-six',
             'Une liste numérotée des six classes d-aliments et de leur rôle.',
             [('simple', 'Six classes, and each one does something the others cannot do.'),
              ('pas_a_pas', 'Look at your plate. Name what is on it. Then ask, for each thing, '
                            'which of the six classes it belongs to.')],
             [('qcm', 1, {'question': 'How many classes of food are there?',
                          'options': ['six', 'three', 'ten']},
               {'index': 0}, 'Six.'),
              ('qcm', 1, {'question': 'Which one is NOT a class of food?',
                          'options': ['plastics', 'proteins', 'vitamins']},
               {'index': 0}, 'Plastics. It is not a food at all.'),
              ('association', 2, {'question': 'Match each class with its work.',
                                  'gauche': ['carbohydrates', 'proteins', 'vitamins'],
                                  'droite': ['give energy', 'build the body',
                                             'prevent diseases']},
               {'order': [0, 1, 2]}, 'Energy, building, protection.'),
              ('texte_a_trous', 3, {'text': 'There are {{1}} classes of food.', 'blanks': 1},
               {'values': ['six']}, 'Six classes.'),
              ('vrai_faux', 4, {'statement': 'Water is counted as one of the classes of food.'},
               {'value': True}, 'Yes, the sixth one.')]),

            ('relation',
             'Carbohydrates give energy. Their sources are rice, cassava, yams, bread and '
             'other starchy foods.',
             'kn-fo-carb',
             'Un tas de grains, le mot carbohydrates, et son rôle écrit dessous.',
             [('simple', 'These are the foods that fill you and make you able to run and work.'),
              ('histoire', 'The farmer eats fufu in the morning. By noon he has dug half the '
                           'field. That is where the energy came from.')],
             [('qcm', 1, {'question': 'What do carbohydrates give?',
                          'options': ['energy', 'bones', 'water']},
               {'index': 0}, 'Energy.'),
              ('qcm', 1, {'question': 'Which one is a carbohydrate?',
                          'options': ['rice', 'fish', 'oil']},
               {'index': 0}, 'Rice.'),
              ('qcm', 2, {'question': 'Which of these is NOT a carbohydrate?',
                          'options': ['meat', 'cassava', 'yams']},
               {'index': 0}, 'Meat. It is a protein.'),
              ('texte_a_trous', 3, {'text': 'Rice and cassava give us {{1}}.', 'blanks': 1},
               {'values': ['energy']}, 'Energy.'),
              ('vrai_faux', 4, {'statement': 'A child who eats no carbohydrate will still have '
                                             'plenty of energy.'},
               {'value': False}, 'No. Carbohydrates are what give energy.')]),

            ('relation',
             'Proteins repair and build the body. Their sources are beans, meat, fish, eggs '
             'and milk.',
             'kn-fo-prot',
             'Un poisson, le mot proteins, et son rôle écrit dessous.',
             [('simple', 'When you grow taller, or when a wound closes, it is protein doing '
                         'the work.'),
              ('analogie', 'Carbohydrate is the fuel of the lorry. Protein is the metal the '
                           'lorry is built from.')],
             [('qcm', 1, {'question': 'What do proteins do?',
                          'options': ['they build the body', 'they give light',
                                      'they cool the body']},
               {'index': 0}, 'They repair and build the body.'),
              ('qcm', 1, {'question': 'Which one is a protein?',
                          'options': ['beans', 'rice', 'salt']},
               {'index': 0}, 'Beans.'),
              ('association', 2, {'question': 'Match each food with its class.',
                                  'gauche': ['fish', 'cassava', 'orange'],
                                  'droite': ['protein', 'carbohydrate', 'vitamin']},
               {'order': [0, 1, 2]}, 'Build, energy, protect.'),
              ('texte_a_trous', 3, {'text': 'Proteins repair and {{1}} the body.',
                                    'blanks': 1},
               {'values': ['build']}, 'They build the body.'),
              ('vrai_faux', 4, {'statement': 'Meat and fish belong to the same class of food.'},
               {'value': True}, 'Yes, both are proteins.')]),

            ('relation',
             'Vitamins prevent diseases. Their sources are fruits and vegetables.',
             'kn-fo-vit',
             'Un fruit, le mot vitamins, et son rôle écrit dessous.',
             [('simple', 'Vitamins do not make you strong or fat. They keep you from falling '
                         'ill.'),
              ('visuel', 'They come from what is coloured on the plate: the green, the red, '
                         'the orange.')],
             [('qcm', 1, {'question': 'What do vitamins do?',
                          'options': ['they prevent diseases', 'they give energy',
                                      'they make bones']},
               {'index': 0}, 'They prevent diseases.'),
              ('qcm', 1, {'question': 'Where do vitamins come from?',
                          'options': ['fruits and vegetables', 'oil and butter',
                                      'salt and water']},
               {'index': 0}, 'Fruits and vegetables.'),
              ('qcm', 2, {'question': 'A child who eats no fruit may easily…',
                          'options': ['fall ill', 'grow taller', 'run faster']},
               {'index': 0}, 'Fall ill, because vitamins protect.'),
              ('texte_a_trous', 3, {'text': 'Fruits and vegetables give us {{1}}.',
                                    'blanks': 1},
               {'values': ['vitamins']}, 'Vitamins.'),
              ('vrai_faux', 4, {'statement': 'Vitamins protect the body against diseases.'},
               {'value': True}, 'Yes, that is their work.')]),

            ('relation',
             'Fats and oils keep the body warm. Their sources are oil, butter, groundnuts and '
             'palm nuts.',
             'kn-fo-fat',
             'Une bouteille d-huile, le mot fats and oils, et son rôle écrit dessous.',
             [('simple', 'They also store energy for later, when there is nothing to eat.'),
              ('analogie', 'Like a blanket folded inside the body: it is there before you need '
                           'it.')],
             [('qcm', 1, {'question': 'What do fats and oils do?',
                          'options': ['they keep the body warm', 'they prevent diseases',
                                      'they help digestion']},
               {'index': 0}, 'They keep the body warm.'),
              ('qcm', 1, {'question': 'Which one is a fat or an oil?',
                          'options': ['butter', 'rice', 'orange']},
               {'index': 0}, 'Butter.'),
              ('qcm', 2, {'question': 'Which of these is NOT a fat or an oil?',
                          'options': ['cassava', 'groundnut oil', 'palm oil']},
               {'index': 0}, 'Cassava. It is a carbohydrate.'),
              ('texte_a_trous', 3, {'text': 'Oil and butter keep the body {{1}}.', 'blanks': 1},
               {'values': ['warm']}, 'Warm.'),
              ('vrai_faux', 4, {'statement': 'Oil belongs to the same class as butter.'},
               {'value': True}, 'Yes, both are fats and oils.')]),

            ('relation',
             'Mineral salts make bones. Their sources are salt, milk and water.',
             'kn-fo-min',
             'Une salière, le mot mineral salts, et son rôle écrit dessous.',
             [('simple', 'Bones and teeth are built from minerals. Without them they stay '
                         'soft.'),
              ('pas_a_pas', 'Milk in the morning, a little salt in the food, water all day. '
                            'That is enough for the bones of a child.')],
             [('qcm', 1, {'question': 'What do mineral salts make?',
                          'options': ['bones', 'energy', 'heat']},
               {'index': 0}, 'Bones.'),
              ('qcm', 1, {'question': 'Which one gives mineral salts?',
                          'options': ['milk', 'bread', 'palm oil']},
               {'index': 0}, 'Milk.'),
              ('qcm', 2, {'question': 'Which part of the body needs minerals most?',
                          'options': ['the bones', 'the hair', 'the ears']},
               {'index': 0}, 'The bones, and the teeth with them.'),
              ('texte_a_trous', 3, {'text': 'Mineral salts help to make strong {{1}}.',
                                    'blanks': 1},
               {'values': ['bones']}, 'Strong bones.'),
              ('vrai_faux', 4, {'statement': 'Mineral salts are only found in salt.'},
               {'value': False}, 'No. Milk and water give them too.')]),

            ('relation',
             'Water helps in digestion. It is a class of food on its own, and it is also where '
             'mineral salts are found.',
             'kn-fo-eau',
             'Un verre d-eau, le mot water, et son rôle écrit dessous.',
             [('simple', 'Food cannot move or be broken down in the body without water.'),
              ('histoire', 'You can live many days without eating. Without drinking, only a '
                           'few. That is how important this class is.')],
             [('qcm', 1, {'question': 'What does water help with?',
                          'options': ['digestion', 'making bones only', 'keeping warm']},
               {'index': 0}, 'Digestion.'),
              ('vrai_faux', 1, {'statement': 'Water is one of the six classes of food.'},
               {'value': True}, 'Yes, the sixth.'),
              ('qcm', 2, {'question': 'Why does water appear twice in the lesson?',
                          'options': ['it is a class and a source', 'it was written twice',
                                      'it is not a food']},
               {'index': 0}, 'It is a class, and also a source of mineral salts.'),
              ('texte_a_trous', 3, {'text': 'Water helps in {{1}}.', 'blanks': 1},
               {'values': ['digestion']}, 'In digestion.'),
              ('vrai_faux', 4, {'statement': 'A person can live many weeks with no water at '
                                             'all.'},
               {'value': False}, 'No. Water is needed every day.')]),
        ],
    ),

    # ------------------------------------------------------------------ 38
    (
        'Cooking methods', NOURRITURE, '2026-10-20', 38,
        'Food is cooked in different ways, and each way suits certain foods. You stew and boil '
        'in water, you fry in oil, you roast and grill on fire with neither water nor oil, and '
        'you toast and bake in an oven. The method chosen changes the taste and the texture.',
        'kn-cu-couv',
        'Une marmite sur le feu, une poêle et un four alignés.',
        [
            ('liste',
             'The methods are stewing, boiling, frying, roasting, grilling, toasting and '
             'baking.',
             'kn-cu-liste',
             'Une liste numérotée des façons de cuire les aliments.',
             [('simple', 'Three questions tell them apart: is there water, is there oil, is '
                         'there an oven?'),
              ('pas_a_pas', 'Water in the pot, it is boiling. Oil in the pan, it is frying. '
                            'Fire and nothing else, it is roasting.')],
             [('qcm', 1, {'question': 'Which one is a cooking method?',
                          'options': ['frying', 'sweeping', 'reading']},
               {'index': 0}, 'Frying.'),
              ('qcm', 1, {'question': 'Which method uses an oven?',
                          'options': ['baking', 'boiling', 'grilling']},
               {'index': 0}, 'Baking.'),
              ('association', 2, {'question': 'Match each method with what it uses.',
                                  'gauche': ['boiling', 'frying', 'baking'],
                                  'droite': ['water', 'oil', 'an oven']},
               {'order': [0, 1, 2]}, 'Water, oil, oven.'),
              ('texte_a_trous', 3, {'text': 'Cooking in hot oil is called {{1}}.', 'blanks': 1},
               {'values': ['frying']}, 'Frying.'),
              ('vrai_faux', 4, {'statement': 'Every food is cooked in the same way.'},
               {'value': False}, 'No. Each method suits certain foods.')]),

            ('relation',
             'Boiling cooks food in water. Yams, rice, cassava and potatoes are boiled.',
             'kn-cu-bouillir',
             'Une marmite posée sur le feu, le mot boiling, et ses exemples.',
             [('simple', 'The water must be hot and must cover the food.'),
              ('visuel', 'The pot sits on the fire, and the food is inside the water, not on '
                         'the metal.')],
             [('qcm', 1, {'question': 'What is used for boiling?',
                          'options': ['water', 'oil', 'nothing']},
               {'index': 0}, 'Water.'),
              ('qcm', 1, {'question': 'Which food is boiled?',
                          'options': ['rice', 'bread', 'biscuits']},
               {'index': 0}, 'Rice.'),
              ('qcm', 2, {'question': 'Which one is NOT usually boiled?',
                          'options': ['a cake', 'a yam', 'cassava']},
               {'index': 0}, 'A cake. It is baked.'),
              ('texte_a_trous', 3, {'text': 'Yams and cassava are cooked in {{1}}.',
                                    'blanks': 1},
               {'values': ['water']}, 'In water.'),
              ('vrai_faux', 4, {'statement': 'Boiling needs oil in the pot.'},
               {'value': False}, 'No, it needs water.')]),

            ('relation',
             'Frying cooks food in hot oil. Fish, meat, chicken and plantain are fried.',
             'kn-cu-frire',
             'Une poêle, le mot frying, et ses exemples.',
             [('simple', 'The oil must be hot before the food goes in, or the food drinks it.'),
              ('analogie', 'Boiling is a bath of water. Frying is a bath of oil.')],
             [('qcm', 1, {'question': 'What is used for frying?',
                          'options': ['hot oil', 'cold water', 'sand']},
               {'index': 0}, 'Hot oil.'),
              ('qcm', 1, {'question': 'Which food is fried?',
                          'options': ['plantain', 'bread', 'cake']},
               {'index': 0}, 'Plantain.'),
              ('vrai_faux', 2, {'statement': 'Fish can be fried.'},
               {'value': True}, 'Yes, fish, meat and chicken are fried.'),
              ('texte_a_trous', 3, {'text': 'To fry a plantain you need hot {{1}}.',
                                    'blanks': 1},
               {'values': ['oil']}, 'Hot oil.'),
              ('vrai_faux', 4, {'statement': 'Frying and boiling use the same liquid.'},
               {'value': False}, 'No. One uses oil, the other water.')]),

            ('relation',
             'Roasting and grilling cook food on the fire, with neither water nor oil. Plums, '
             'plantain, fish, yams and groundnuts are roasted.',
             'kn-cu-rotir',
             'Un gril posé au-dessus du feu, le mot roasting, et ses exemples.',
             [('simple', 'The food touches the heat itself. Nothing stands between the two.'),
              ('histoire', 'The roasted plantain sold at the roadside has no oil and no water '
                           'in it. Only fire and time.')],
             [('qcm', 1, {'question': 'What does roasting use?',
                          'options': ['fire only', 'oil only', 'water only']},
               {'index': 0}, 'Fire only.'),
              ('qcm', 1, {'question': 'Which food is grilled?',
                          'options': ['groundnuts', 'a plate of rice', 'a bowl of soup']},
               {'index': 0}, 'Groundnuts.'),
              ('qcm', 2, {'question': 'What is between the food and the fire when roasting?',
                          'options': ['nothing at all', 'a pot of water', 'a pan of oil']},
               {'index': 0}, 'Nothing at all.'),
              ('texte_a_trous', 3, {'text': 'Roasting uses neither oil nor {{1}}.',
                                    'blanks': 1},
               {'values': ['water']}, 'Neither oil nor water.'),
              ('vrai_faux', 4, {'statement': 'Roasting needs a pot.'},
               {'value': False}, 'No. The food is put on the fire itself.')]),

            ('relation',
             'Baking and toasting cook food in an oven. Biscuits, bread and cake are baked.',
             'kn-cu-four',
             'Un four fermé, le mot baking, et ses exemples.',
             [('simple', 'In an oven the heat comes from all sides at once, not from below '
                         'only.'),
              ('visuel', 'The oven is closed. That is what makes it an oven and not a fire.')],
             [('qcm', 1, {'question': 'Where is bread baked?',
                          'options': ['in an oven', 'in a pot of water', 'on a cutlass']},
               {'index': 0}, 'In an oven.'),
              ('qcm', 1, {'question': 'Which one is baked?',
                          'options': ['cake', 'rice', 'soup']},
               {'index': 0}, 'Cake.'),
              ('association', 2, {'question': 'Match each food with its method.',
                                  'gauche': ['bread', 'rice', 'plantain'],
                                  'droite': ['baking', 'boiling', 'frying']},
               {'order': [0, 1, 2]}, 'Oven, water, oil.'),
              ('texte_a_trous', 3, {'text': 'Biscuits, bread and cake are {{1}}.', 'blanks': 1},
               {'values': ['baked']}, 'They are baked.'),
              ('vrai_faux', 4, {'statement': 'An oven is closed while the food cooks.'},
               {'value': True}, 'Yes, that is what makes it an oven.')]),
        ],
    ),

    # ------------------------------------------------------------------ 39
    (
        'Food conservation', NOURRITURE, None, 39,
        'Food conservation is the process of keeping food to prevent it from getting bad. Food '
        'can be dried in the sun, frozen in the cold, canned in tins, salted, or smoked over a '
        'fire. Each method stops what makes food spoil: water, warmth, or air.',
        'kn-co-couv',
        'Le soleil, un réfrigérateur et une boîte de conserve alignés.',
        [
            ('definition',
             'Food conservation is the process of keeping food to prevent it from getting bad.',
             'kn-co-liste',
             'Une liste numérotée des cinq façons de conserver un aliment.',
             [('simple', 'Food goes bad because it is wet and warm. Every method takes away '
                         'one of the two.'),
              ('analogie', 'Conserving food is winning time: what would be lost tomorrow is '
                           'still good next month.')],
             [('qcm', 1, {'question': 'What does food conservation do?',
                          'options': ['it keeps food from spoiling', 'it cooks the food',
                                      'it makes the food sweet']},
               {'index': 0}, 'It keeps food from getting bad.'),
              ('qcm', 1, {'question': 'Which one is a way of conserving food?',
                          'options': ['drying', 'eating', 'buying']},
               {'index': 0}, 'Drying.'),
              ('association', 2, {'question': 'Match each method with what it uses.',
                                  'gauche': ['drying', 'freezing', 'smoking'],
                                  'droite': ['the sun', 'the cold', 'the fire']},
               {'order': [0, 1, 2]}, 'Sun, cold, fire.'),
              ('texte_a_trous', 3,
               {'text': 'Conservation keeps food from getting {{1}}.', 'blanks': 1},
               {'values': ['bad']}, 'From getting bad.'),
              ('vrai_faux', 4, {'statement': 'Conserved food can be kept much longer than '
                                             'fresh food.'},
               {'value': True}, 'Yes, that is the whole purpose.')]),

            ('relation',
             'Drying takes the water out of food, in the sun. Vegetables, maize and beans are '
             'dried.',
             'kn-co-secher',
             'Le soleil, le mot drying, et ses exemples.',
             [('simple', 'What has no water in it cannot rot.'),
              ('visuel', 'Maize spread on a mat in the yard is being conserved, not just left '
                         'out.')],
             [('qcm', 1, {'question': 'What does drying remove from food?',
                          'options': ['the water', 'the salt', 'the colour']},
               {'index': 0}, 'The water.'),
              ('qcm', 1, {'question': 'Which food is dried?',
                          'options': ['maize', 'milk', 'juice']},
               {'index': 0}, 'Maize.'),
              ('qcm', 2, {'question': 'Why does dry food keep longer?',
                          'options': ['it cannot rot without water', 'it is lighter to carry',
                                      'it is sweeter to the tongue']},
               {'index': 0}, 'Without water it cannot rot.'),
              ('texte_a_trous', 3, {'text': 'Drying takes the {{1}} out of the food.',
                                    'blanks': 1},
               {'values': ['water']}, 'The water.'),
              ('vrai_faux', 4, {'statement': 'Wet food keeps longer than dry food.'},
               {'value': False}, 'No. It is the dry food that keeps.')]),

            ('relation',
             'Freezing keeps food in the cold. Meat, fish and tomatoes are frozen.',
             'kn-co-geler',
             'Un réfrigérateur, le mot freezing, et ses exemples.',
             [('simple', 'Cold does not kill what spoils food, it only stops it from working.'),
              ('pas_a_pas', 'Put the meat in the freezer. Leave it there. Take it out only '
                            'when you will cook it.')],
             [('qcm', 1, {'question': 'What does freezing use?',
                          'options': ['the cold', 'the fire', 'the sun']},
               {'index': 0}, 'The cold.'),
              ('qcm', 1, {'question': 'Which food is frozen?',
                          'options': ['meat', 'maize', 'beans']},
               {'index': 0}, 'Meat.'),
              ('vrai_faux', 2, {'statement': 'Food taken out of the freezer keeps for ever.'},
               {'value': False}, 'No. Once it is warm again, it begins to spoil.'),
              ('texte_a_trous', 3, {'text': 'Meat and fish are kept in the {{1}}.',
                                    'blanks': 1},
               {'values': ['cold']}, 'In the cold.'),
              ('vrai_faux', 4, {'statement': 'Cold slows down what makes food spoil.'},
               {'value': True}, 'Yes, it stops it from working.')]),

            ('relation',
             'Canning keeps food closed inside a tin, away from the air. Fish, tomatoes, juice '
             'and milk are canned.',
             'kn-co-boite',
             'Une boîte de conserve, le mot canning, et ses exemples.',
             [('simple', 'The tin is sealed, so no air and nothing living can get in.'),
              ('analogie', 'Like a letter in a closed envelope: as long as it is shut, nothing '
                           'reaches what is inside.')],
             [('qcm', 1, {'question': 'What is food put into when it is canned?',
                          'options': ['a tin', 'a basket', 'a cloth']},
               {'index': 0}, 'A tin.'),
              ('qcm', 1, {'question': 'Which food is canned?',
                          'options': ['milk', 'yam', 'cassava']},
               {'index': 0}, 'Milk.'),
              ('qcm', 2, {'question': 'What is kept away from the food in a tin?',
                          'options': ['the air', 'the label', 'the metal']},
               {'index': 0}, 'The air.'),
              ('texte_a_trous', 3, {'text': 'Canned food is kept inside a sealed {{1}}.',
                                    'blanks': 1},
               {'values': ['tin']}, 'A sealed tin.'),
              ('vrai_faux', 4, {'statement': 'An open tin keeps food as well as a closed one.'},
               {'value': False}, 'No. Once it is open the air comes in.')]),

            ('relation',
             'Salting draws the water out of meat and fish and keeps them from spoiling.',
             'kn-co-saler',
             'Une salière, le mot salting, et ses exemples.',
             [('simple', 'Salt pulls the water out of the food, and what is dry does not rot.'),
              ('visuel', 'Salted fish is stiff and dry to the touch. That is the salt having '
                         'done its work.')],
             [('qcm', 1, {'question': 'What does salt do to meat?',
                          'options': ['it draws the water out', 'it adds water to it',
                                      'it cooks it']},
               {'index': 0}, 'It draws the water out.'),
              ('qcm', 1, {'question': 'Which food is salted?',
                          'options': ['fish', 'cake', 'juice']},
               {'index': 0}, 'Fish.'),
              ('qcm', 2, {'question': 'Salting works for the same reason as…',
                          'options': ['drying', 'freezing', 'canning']},
               {'index': 0}, 'Drying. Both take the water away.'),
              ('texte_a_trous', 3, {'text': 'Meat and fish can be kept with {{1}}.',
                                    'blanks': 1},
               {'values': ['salt']}, 'With salt.'),
              ('vrai_faux', 4, {'statement': 'Salting and drying both work by removing water.'},
               {'value': True}, 'Yes, in two different ways.')]),

            ('relation',
             'Smoking keeps fish and meat by hanging them over a fire, in the smoke.',
             'kn-co-fumer',
             'Du poisson sur une claie au-dessus du feu, avec la fumée qui monte.',
             [('simple', 'The smoke dries the food and covers it at the same time.'),
              ('histoire', 'The fish smoked at the lake travels for days to the market and '
                           'arrives still good.')],
             [('qcm', 1, {'question': 'What is used for smoking food?',
                          'options': ['smoke from a fire', 'cold water', 'the freezer']},
               {'index': 0}, 'Smoke from a fire.'),
              ('qcm', 1, {'question': 'Which food is smoked?',
                          'options': ['fish', 'cake', 'rice']},
               {'index': 0}, 'Fish.'),
              ('qcm', 2, {'question': 'Smoking is different from roasting because…',
                          'options': ['it is to keep, not to eat now', 'it uses no fire',
                                      'it uses a lot of oil']},
               {'index': 0}, 'Roasting cooks for now; smoking keeps for later.'),
              ('texte_a_trous', 3, {'text': 'Fish and meat can be kept by {{1}} them.',
                                    'blanks': 1},
               {'values': ['smoking']}, 'By smoking them.'),
              ('vrai_faux', 4, {'statement': 'Smoking is a way of conserving food.'},
               {'value': True}, 'Yes, one of the five.')]),
        ],
    ),

    # ------------------------------------------------------------------ 40
    (
        'Kitchen utensils and household furniture', MAISON, '2026-09-15', 40,
        'Kitchen utensils are hand held tools used in the kitchen for preparing food: the '
        'mortar and pestle, the pot, the knife, the spoon. Household furniture are the things '
        'of the home you can move and arrange to make the home more comfortable: chairs, '
        'tables, beds, cupboards. One prepares, the other makes the home easy to live in.',
        'kn-uf-couv',
        'Un mortier, une marmite, une chaise et un lit alignés.',
        [
            ('definition',
             'Kitchen utensils are hand held tools used in the kitchen for preparing food.',
             'kn-uf-ustensiles',
             'Quatre vignettes nommées : mortar and pestle, pot, knife, spoon.',
             [('simple', 'Hand held means you hold it. A kitchen is full of them.'),
              ('analogie', 'What the cutlass is to the farm, the knife is to the kitchen.')],
             [('qcm', 1, {'question': 'What are kitchen utensils used for?',
                          'options': ['preparing food', 'sleeping at night',
                                      'working in the farm']},
               {'index': 0}, 'For preparing food.'),
              ('qcm', 2, {'question': 'Which one is the mortar and pestle?',
                          'images': ['kn-u1-mortier', 'kn-u1-marmite', 'kn-u1-rape']},
               {'index': 0}, 'The mortar is the bowl, the pestle is the stick inside it.'),
              ('qcm', 2, {'question': 'Which one is the pot?',
                          'images': ['kn-u1-marmite', 'kn-u1-planche', 'kn-u1-couteau']},
               {'index': 0}, 'The pot has two handles and a wide mouth.'),
              ('texte_a_trous', 3,
               {'text': 'Kitchen utensils are used for preparing {{1}}.', 'blanks': 1},
               {'values': ['food']}, 'Preparing food.'),
              ('vrai_faux', 4, {'statement': 'A spoon is a kitchen utensil.'},
               {'value': True}, 'Yes, it is held in the hand and used for food.')]),

            ('liste',
             'Other utensils are the grater, the chopping board, the spatula, the fork and the '
             'grinding stone.',
             'kn-uf-autres',
             'Quatre vignettes nommées : grater, chopping board, spatula, fork.',
             [('simple', 'Each one does one job: grating, cutting on, turning, picking up.'),
              ('pas_a_pas', 'Look at the tool and ask what part of it touches the food. That '
                            'part tells you what it does.')],
             [('qcm', 1, {'question': 'What is a grater used for?',
                          'options': ['to grate food into small bits', 'to sleep on',
                                      'to dig the soil']},
               {'index': 0}, 'To grate food into small bits.'),
              ('qcm', 2, {'question': 'Which one is the grater?',
                          'images': ['kn-u1-rape', 'kn-u1-planche', 'kn-u1-marmite']},
               {'index': 0}, 'The grater is the one full of small holes.'),
              ('association', 2, {'question': 'Match each utensil with its job.',
                                  'gauche': ['knife', 'chopping board', 'spoon'],
                                  'droite': ['it cuts', 'you cut on it', 'it picks up']},
               {'order': [0, 1, 2]}, 'Cut, cut on, pick up.'),
              ('texte_a_trous', 3, {'text': 'You cut food on a chopping {{1}}.', 'blanks': 1},
               {'values': ['board']}, 'A chopping board.'),
              ('vrai_faux', 4, {'statement': 'The chopping board does the cutting by itself.'},
               {'value': False}, 'No. The knife cuts, the board is what you cut on.')]),

            ('relation',
             'The mortar and pestle, the grinding stone and the grater all make food smaller, '
             'each in its own way.',
             'kn-uf-moudre',
             'Quatre vignettes, le mortier et son pilon mis en avant.',
             [('simple', 'The mortar pounds, the stone crushes, the grater shreds.'),
              ('visuel', 'Look at how each one moves: up and down, back and forth, or along '
                         'the holes.')],
             [('qcm', 1, {'question': 'What do you do with a mortar and pestle?',
                          'options': ['you pound food in it', 'you sleep in it',
                                      'you sit on it']},
               {'index': 0}, 'You pound food in it.'),
              ('qcm', 2, {'question': 'Which one is NOT used to make food smaller?',
                          'options': ['the pot', 'the grater', 'the grinding stone']},
               {'index': 0}, 'The pot. It is used to cook.'),
              ('association', 2, {'question': 'Match each one with how it works.',
                                  'gauche': ['mortar and pestle', 'grinding stone', 'grater'],
                                  'droite': ['it pounds', 'it crushes', 'it shreds']},
               {'order': [0, 1, 2]}, 'Pound, crush, shred.'),
              ('texte_a_trous', 3, {'text': 'The stick you pound with is called the {{1}}.',
                                    'blanks': 1},
               {'values': ['pestle']}, 'The pestle.'),
              ('vrai_faux', 4, {'statement': 'The mortar is the bowl and the pestle is the '
                                             'stick.'},
               {'value': True}, 'Yes, the two together make one tool.')]),

            ('definition',
             'Household furniture are things of the home that you can move and arrange to make '
             'the home more comfortable.',
             'kn-uf-meubles',
             'Quatre vignettes nommées : chair, table, bed, cupboard.',
             [('simple', 'If it can be moved and arranged, it is furniture. A wall cannot be '
                         'moved, so a wall is not furniture.'),
              ('analogie', 'The house is the box. The furniture is what you put inside it to '
                           'be able to live there.')],
             [('qcm', 1, {'question': 'What is household furniture for?',
                          'options': ['to make the home comfortable', 'to cook the food',
                                      'to dig the garden']},
               {'index': 0}, 'To make the home more comfortable.'),
              ('qcm', 2, {'question': 'Which one is the cupboard?',
                          'images': ['kn-m1-armoire', 'kn-m1-table', 'kn-m1-chaise']},
               {'index': 0}, 'The cupboard is tall and has two doors.'),
              ('qcm', 2, {'question': 'Which one is the bed?',
                          'images': ['kn-m1-lit', 'kn-m1-table', 'kn-m1-armoire']},
               {'index': 0}, 'The bed is low and long, with a pillow.'),
              ('texte_a_trous', 3,
               {'text': 'Furniture can be moved and arranged in the {{1}}.', 'blanks': 1},
               {'values': ['home']}, 'In the home.'),
              ('vrai_faux', 4, {'statement': 'A wall of the house is a piece of furniture.'},
               {'value': False}, 'No. Furniture is what can be moved.')]),

            ('liste',
             'Other pieces of furniture are the sofa, the desk, the wardrobe and the shelf.',
             'kn-uf-autres-m',
             'Quatre vignettes nommées : sofa, desk, cupboard, chair.',
             [('simple', 'A sofa is a long soft seat. A desk is a table you write on.'),
              ('visuel', 'A wardrobe and a cupboard look alike: the wardrobe is the one for '
                         'clothes.')],
             [('qcm', 1, {'question': 'What is a sofa?',
                          'options': ['a long soft seat', 'a cooking pot', 'a farming tool']},
               {'index': 0}, 'A long soft seat.'),
              ('qcm', 1, {'question': 'What do you do at a desk?',
                          'options': ['you write', 'you cook', 'you dig']},
               {'index': 0}, 'You write.'),
              ('qcm', 2, {'question': 'Which one is the table?',
                          'images': ['kn-m1-table', 'kn-m1-lit', 'kn-m1-chaise']},
               {'index': 0}, 'The table is a flat top on four legs, with no back.'),
              ('texte_a_trous', 3, {'text': 'A wardrobe is a cupboard for your {{1}}.',
                                    'blanks': 1},
               {'values': ['clothes']}, 'For your clothes.'),
              ('vrai_faux', 4, {'statement': 'A desk and a table are both furniture.'},
               {'value': True}, 'Yes, both can be moved and arranged.')]),

            ('relation',
             'A utensil prepares food in the kitchen. A piece of furniture makes the home easy '
             'to live in. That is what tells them apart.',
             'kn-uf-difference',
             'Une marmite et une chaise côte à côte, avec ce qui les distingue écrit dessous.',
             [('simple', 'Ask what it is for. Food, it is a utensil. Living in the house, it '
                         'is furniture.'),
              ('pas_a_pas', 'A pot: does it prepare food? Yes. Utensil. A chair: does it '
                            'prepare food? No, you sit on it. Furniture.')],
             [('qcm', 1, {'question': 'A pot is…',
                          'options': ['a kitchen utensil', 'a piece of furniture',
                                      'a farming tool']},
               {'index': 0}, 'A kitchen utensil.'),
              ('qcm', 1, {'question': 'A bed is…',
                          'options': ['a piece of furniture', 'a kitchen utensil',
                                      'a cooking method']},
               {'index': 0}, 'A piece of furniture.'),
              ('association', 2, {'question': 'Match each thing with what it is.',
                                  'gauche': ['knife', 'cupboard', 'grater'],
                                  'droite': ['utensil', 'furniture', 'utensil also']},
               {'order': [0, 1, 2]}, 'Two utensils and one piece of furniture.'),
              ('texte_a_trous', 3,
               {'text': 'A thing used to prepare food is a kitchen {{1}}.', 'blanks': 1},
               {'values': ['utensil']}, 'A kitchen utensil.'),
              ('vrai_faux', 4, {'statement': 'A chair is a kitchen utensil because it is in '
                                             'the house.'},
               {'value': False}, 'No. It does not prepare food, so it is furniture.')]),
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
                    assert ('options' in payload) != ('images' in payload), \
                        'un QCM a des options ou des images, pas les deux : ' + str(payload)
                    choix = payload.get('options') or payload['images']
                    assert 2 <= len(choix) <= 4, payload
                    assert len(set(choix)) == len(choix), 'choix en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(choix), payload
                    if 'images' in payload:
                        cles_items.update(choix)
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
                        assert len(set(payload['droite'])) == len(payload['droite']), \
                            'deux étiquettes identiques à droite : ' + str(payload['droite'])
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    # Les six classes d-aliments doivent y être toutes les six.
    tout = json.dumps(LECONS, ensure_ascii=False, default=str)
    for classe in ('carbohydrate', 'protein', 'vitamin', 'fats and oils',
                   'mineral salts', 'water'):
        assert classe in tout, 'classe d-aliment absente : ' + classe

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-klein-maison-nov.py'))
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
    chemin = os.path.join(racine, 'app', 'public', 'seed-klein-maison-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions - %d images dont %d en reponse'
          % (len(LECONS), notions, items, images, en_question))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-44s %-12s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
