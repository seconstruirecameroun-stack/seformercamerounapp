# -*- coding: utf-8 -*-
"""
Cinq leçons d-éducation à la santé pour BRAYNE (CM1) — cahier
« Sciences / Health / En. Educ », octobre et novembre 2026.

UNE LEÇON SANS PAGE DE COURS, ET POURQUOI ELLE EXISTE QUAND MÊME.

Le régime, les repas, la sous-alimentation et la sur-alimentation sont
interrogés dans la révision du 5 novembre (questions 5, 6, 9, 10, 11 et
12 de la partie Health Education), mais la page de cours correspondante
n-est pas dans le lot : le cahier renvoie à « See note on Home
Economics ». Les définitions, elles, sont écrites noir sur blanc dans
les réponses corrigées. La leçon 47 est donc bâtie sur ces réponses-là,
et sur rien d-autre. C-est le seul cas du lot où je prends le corrigé
pour source, et c-est assumé : ce qui sera demandé à l-examen est
exactement ce que la maîtresse a fait écrire.

LA FORME SUIT SON ÉPREUVE. Comme pour les sept leçons d-environnement,
le texte à trous domine, parce que c-est sous cette forme que la
maîtresse interroge. Un contrôle refuse le fichier si sa part tombe
sous 35 %.

DEUX FAUTES DE SA COPIE SONT TRAVAILLÉES ICI :
  preservation, qu-il a écrit « conservation » ;
  drying pour le maïs, qu-il a écrit « frying ».

Usage :  python work/lecons-brayne-sante-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-sante-nov.py. ')

MATIERE = 'Sciences'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

HYGIENE = 'Hygiene'
ALIMENTS = 'Food'
SANTE = 'Food and health'

LECONS = [
    # ------------------------------------------------------------------ 43
    (
        'The water closet and its care', HYGIENE, '2026-10-29', 43,
        'The water closet is a type of latrine in which water is used to flush after using. It '
        'is cared for by flushing immediately, using good soft tissue, cleaning the bowl with '
        'disinfectant, and never climbing on the sitting pot. The room is kept clean by mopping '
        'the floor, keeping it dry, scrubbing the walls and removing cobwebs.',
        'bs-wc-couv',
        'Une cuvette de toilettes à l-eau avec sa chasse.',
        [
            ('definition',
             'The water closet is a type of latrine in which water is used to flush after '
             'using.',
             'bs-wc-def',
             'La cuvette, et l-eau de la chasse.',
             [('simple', 'What makes it a water closet is the water. Other latrines have none.'),
              ('pas_a_pas', 'Use it, then flush it. The flushing is not optional: it is what '
                            'the toilet is for.')],
             [('texte_a_trous', 1,
               {'text': 'A latrine in which water is used to flush is called a water {{1}}.',
                'blanks': 1},
               {'values': ['closet']}, 'A water closet.'),
              ('qcm', 1, {'question': 'What is used to flush a water closet?',
                          'options': ['water', 'sand', 'ash']},
               {'index': 0}, 'Water.'),
              ('texte_a_trous', 2,
               {'text': 'The water closet is a type of {{1}}.', 'blanks': 1},
               {'values': ['latrine']}, 'A latrine.'),
              ('qcm', 3, {'question': 'When is the water closet flushed?',
                          'options': ['immediately after use', 'once a week',
                                      'only when it smells']},
               {'index': 0}, 'Immediately after use.'),
              ('vrai_faux', 4, {'statement': 'Every latrine uses water to flush.'},
               {'value': False}, 'No. Only the water closet does.')]),

            ('liste',
             'Care of the water closet: flush immediately after use, use good and soft toilet '
             'tissue, clean the bowl regularly with disinfectant, and do not climb on the '
             'sitting pot.',
             'bs-wc-soin',
             'La liste numérotée des quatre gestes de soin du water closet.',
             [('simple', 'Three of the four protect the next person who comes in.'),
              ('pas_a_pas', 'Flush. Use soft tissue. Clean the bowl. Sit, never stand on it.')],
             [('texte_a_trous', 1,
               {'text': 'Always flush the water closet {{1}} after use.', 'blanks': 1},
               {'values': ['immediately']}, 'Immediately.'),
              ('qcm', 1, {'question': 'What kind of toilet tissue should be used?',
                          'options': ['good and soft tissue', 'old newspaper',
                                      'hard dry leaves']},
               {'index': 0}, 'Good and soft toilet tissue.'),
              ('qcm', 2, {'question': 'What is used to clean the bowl?',
                          'options': ['disinfectant', 'cooking oil', 'plain sand']},
               {'index': 0}, 'Disinfectant.'),
              ('texte_a_trous', 3,
               {'text': 'You must not climb or jump on the sitting {{1}}.', 'blanks': 1},
               {'values': ['pot']}, 'The sitting pot.'),
              ('vrai_faux', 4, {'statement': 'Standing on the sitting pot is a safe way to use '
                                             'it.'},
               {'value': False}, 'No. The lesson says never to climb on it.')]),

            ('relation',
             'The floor of the toilet is mopped regularly with disinfectant and always kept '
             'dry.',
             'bs-wc-sol',
             'La cuvette et le sol lavé, avec l-eau qu-on essuie.',
             [('simple', 'A wet floor is slippery, and it is where germs stay longest.'),
              ('analogie', 'A dry floor is a floor nothing grows on.')],
             [('texte_a_trous', 1,
               {'text': 'Mop the floor regularly with {{1}}.', 'blanks': 1},
               {'values': ['disinfectant']}, 'With disinfectant.'),
              ('qcm', 1, {'question': 'How should the toilet floor be kept?',
                          'options': ['dry', 'wet', 'covered with sand']},
               {'index': 0}, 'Dry.'),
              ('qcm', 2, {'question': 'Why is a wet floor dangerous?',
                          'options': ['it is slippery', 'it is cold', 'it is dark']},
               {'index': 0}, 'It is slippery, and germs stay on it.'),
              ('texte_a_trous', 3,
               {'text': 'Always keep the toilet floor {{1}}.', 'blanks': 1},
               {'values': ['dry']}, 'Dry.'),
              ('vrai_faux', 4, {'statement': 'Water left on the toilet floor helps to keep it '
                                             'clean.'},
               {'value': False}, 'No. The floor must be kept dry.')]),

            ('liste',
             'The walls are scrubbed with a brush and the cobwebs are removed from the ceiling '
             'and the walls regularly.',
             'bs-wc-murs',
             'La liste numérotée des gestes qui gardent la pièce propre.',
             [('simple', 'The bowl is not the whole toilet. The walls and the ceiling are part '
                         'of it.'),
              ('visuel', 'Look up before you leave: a cobweb on the ceiling says the room has '
                         'not been cleaned in a while.')],
             [('texte_a_trous', 1,
               {'text': 'Scrub the walls with a {{1}}.', 'blanks': 1},
               {'values': ['brush']}, 'With a brush.'),
              ('qcm', 1, {'question': 'What is removed from the ceiling?',
                          'options': ['cobwebs', 'the light', 'the paint']},
               {'index': 0}, 'Cobwebs.'),
              ('qcm', 2, {'question': 'How often are the walls cleaned?',
                          'options': ['regularly', 'once a year', 'never']},
               {'index': 0}, 'Regularly.'),
              ('texte_a_trous', 3,
               {'text': 'Remove {{1}} from the ceiling and the walls.', 'blanks': 1},
               {'values': ['cobwebs']}, 'Cobwebs.'),
              ('vrai_faux', 4, {'statement': 'Caring for a toilet means cleaning the bowl and '
                                             'nothing else.'},
               {'value': False}, 'No. The floor, the walls and the ceiling too.')]),
        ],
    ),

    # ------------------------------------------------------------------ 44
    (
        'Food and its six classes', ALIMENTS, '2026-10-29', 44,
        'Food is anything solid or liquid that we eat to sustain life and have energy. There '
        'are six classes: proteins build and repair worn out tissues, carbohydrates and fats '
        'give energy, mineral salts make strong bones and teeth, vitamins prevent diseases, and '
        'water eases digestion and regulates the body temperature.',
        'bs-fd-couv',
        'Cinq sources d-aliments alignées : poisson, grains, fruit, huile, eau.',
        [
            ('definition',
             'Food is anything solid or liquid that we eat to sustain life and have energy.',
             'bs-fd-def',
             'Quatre vignettes nommées : fish, rice, fruit, water.',
             [('simple', 'Solid or liquid: water counts, and so does juice.'),
              ('pas_a_pas', 'Ask two things of what is on the plate: does it keep me alive, '
                            'and does it give me energy?')],
             [('texte_a_trous', 1,
               {'text': 'Food is anything solid or {{1}} that we eat.', 'blanks': 1},
               {'values': ['liquid']}, 'Solid or liquid.'),
              ('qcm', 1, {'question': 'What do we eat food for?',
                          'options': ['to sustain life and have energy', 'to pass the time',
                                      'to make noise']},
               {'index': 0}, 'To sustain life and have energy.'),
              ('texte_a_trous', 2,
               {'text': 'We eat food to {{1}} life and have energy.', 'blanks': 1},
               {'values': ['sustain']}, 'To sustain life.'),
              ('qcm', 3, {'question': 'Is water a food?',
                          'options': ['yes, it is a liquid food', 'no, it is only a drink',
                                      'only when it is hot']},
               {'index': 0}, 'Yes. It is one of the six classes.'),
              ('vrai_faux', 4, {'statement': 'Only solid things can be called food.'},
               {'value': False}, 'No. Liquids are food too.')]),

            ('liste',
             'There are six classes of food: proteins, carbohydrates, fats and oil, mineral '
             'salts, vitamins and water.',
             'bs-fd-table',
             'Le tableau à trois colonnes : la classe, sa source, sa fonction.',
             [('simple', 'Six classes, and each one has a source and a job.'),
              ('visuel', 'Read the table across, never down: a class, where it comes from, '
                         'what it does.')],
             [('texte_a_trous', 1,
               {'text': 'There are {{1}} classes of food.', 'blanks': 1},
               {'values': ['six']}, 'Six.'),
              ('association', 1, {'question': 'Match each class with its function.',
                                  'gauche': ['proteins', 'carbohydrates', 'vitamins'],
                                  'droite': ['they build the body', 'they give energy',
                                             'they prevent diseases']},
               {'order': [0, 1, 2]}, 'Build, energy, protect.'),
              ('association', 2, {'question': 'Match each class with its source.',
                                  'gauche': ['proteins', 'carbohydrates', 'mineral salts'],
                                  'droite': ['fish and eggs', 'rice and corn', 'salt and milk']},
               {'order': [0, 1, 2]}, 'Each class has its own foods.'),
              ('texte_a_trous', 3,
               {'text': 'Fats and oil, like carbohydrates, give the body {{1}}.', 'blanks': 1},
               {'values': ['energy']}, 'Energy.'),
              ('vrai_faux', 4, {'statement': 'Two different classes of food can have the same '
                                             'function.'},
               {'value': True}, 'Yes: carbohydrates and fats both give energy.')]),

            ('relation',
             'Proteins build and repair worn out tissues. Their sources are milk, fish, meat, '
             'eggs and beans.',
             'bs-fd-prot',
             'Un poisson, le mot proteins, et son rôle.',
             [('simple', 'When you grow or when a wound closes, it is protein doing the work.'),
              ('analogie', 'Carbohydrate is the fuel; protein is the metal the lorry is built '
                           'from.')],
             [('texte_a_trous', 1,
               {'text': 'Proteins build and {{1}} worn out tissues.', 'blanks': 1},
               {'values': ['repair']}, 'Build and repair.'),
              ('qcm', 1, {'question': 'Which food gives protein?',
                          'options': ['beans', 'rice', 'palm oil']},
               {'index': 0}, 'Beans.'),
              ('qcm', 2, {'question': 'Which of these is NOT a source of protein?',
                          'options': ['cassava', 'eggs', 'fish']},
               {'index': 0}, 'Cassava. It is a carbohydrate.'),
              ('texte_a_trous', 3,
               {'text': 'Milk, fish, meat and eggs are sources of {{1}}.', 'blanks': 1},
               {'values': ['protein']}, 'Of protein.'),
              ('vrai_faux', 4, {'statement': 'Protein is what repairs the body after a wound.'},
               {'value': True}, 'Yes, it builds and repairs tissues.')]),

            ('relation',
             'Carbohydrates provide the body with energy. Their sources are cassava, rice, corn '
             'and bread.',
             'bs-fd-carb',
             'Un tas de grains, le mot carbohydrates, et son rôle.',
             [('simple', 'These are the foods that fill you and let you work all morning.'),
              ('histoire', 'The farmer eats fufu at dawn. By noon the field is half dug. That '
                           'is where the energy came from.')],
             [('texte_a_trous', 1,
               {'text': 'Carbohydrates provide the body with {{1}}.', 'blanks': 1},
               {'values': ['energy']}, 'With energy.'),
              ('qcm', 1, {'question': 'Which food is a carbohydrate?',
                          'options': ['cassava', 'fish', 'butter']},
               {'index': 0}, 'Cassava.'),
              ('qcm', 2, {'question': 'Which of these is NOT a carbohydrate?',
                          'options': ['eggs', 'rice', 'bread']},
               {'index': 0}, 'Eggs. They are a protein.'),
              ('texte_a_trous', 3,
               {'text': 'Cassava, rice, corn and {{1}} are carbohydrates.', 'blanks': 1},
               {'values': ['bread']}, 'And bread.'),
              ('vrai_faux', 4, {'statement': 'A child who eats no carbohydrate will still have '
                                             'plenty of energy.'},
               {'value': False}, 'No. Carbohydrates are what give energy.')]),

            ('relation',
             'Fats and oil provide the body with energy. Their sources are butter, cheese, oil, '
             'pork and groundnut.',
             'bs-fd-fat',
             'Une bouteille d-huile, le mot fats and oil, et son rôle.',
             [('simple', 'They give energy like carbohydrates, but they also store it for '
                         'later.'),
              ('visuel', 'They are the greasy foods: what leaves a mark on the paper.')],
             [('texte_a_trous', 1,
               {'text': 'Fats and oil provide the body with {{1}}.', 'blanks': 1},
               {'values': ['energy']}, 'With energy.'),
              ('qcm', 1, {'question': 'Which one belongs to fats and oil?',
                          'options': ['butter', 'rice', 'orange']},
               {'index': 0}, 'Butter.'),
              ('qcm', 2, {'question': 'Which class shares its function with fats and oil?',
                          'options': ['carbohydrates', 'vitamins', 'mineral salts']},
               {'index': 0}, 'Carbohydrates. Both give energy.'),
              ('texte_a_trous', 3,
               {'text': 'Butter, cheese, oil and {{1}} belong to fats and oil.', 'blanks': 1},
               {'values': ['groundnut']}, 'And groundnut.'),
              ('vrai_faux', 4, {'statement': 'Fats and oil give energy, just as carbohydrates '
                                             'do.'},
               {'value': True}, 'Yes, the same function.')]),

            ('relation',
             'Mineral salts provide us with strong bones and teeth. Their sources are cooking '
             'salt, milk and egg shell.',
             'bs-fd-min',
             'Une salière, le mot mineral salts, et son rôle.',
             [('simple', 'Bones and teeth are built from minerals. Without them they stay '
                         'soft.'),
              ('pas_a_pas', 'Milk in the morning, a little salt in the food. That is enough for '
                            'a child.')],
             [('texte_a_trous', 1,
               {'text': 'Mineral salts give us strong bones and {{1}}.', 'blanks': 1},
               {'values': ['teeth']}, 'Bones and teeth.'),
              ('qcm', 1, {'question': 'Which food gives mineral salts?',
                          'options': ['milk', 'bread', 'palm oil']},
               {'index': 0}, 'Milk.'),
              ('qcm', 2, {'question': 'Which part of the body needs minerals most?',
                          'options': ['the bones', 'the hair', 'the ears']},
               {'index': 0}, 'The bones, and the teeth with them.'),
              ('texte_a_trous', 3,
               {'text': 'Cooking {{1}} and milk are sources of mineral salts.', 'blanks': 1},
               {'values': ['salt']}, 'Cooking salt.'),
              ('vrai_faux', 4, {'statement': 'Mineral salts give energy to the body.'},
               {'value': False}, 'No. They make strong bones and teeth.')]),

            ('relation',
             'Vitamins prevent diseases. Their sources are fruits, vegetables and sunlight.',
             'bs-fd-vit',
             'Un fruit, le mot vitamins, et son rôle.',
             [('simple', 'Vitamins do not make you strong or fat. They keep you from falling '
                         'ill.'),
              ('visuel', 'They come from what is coloured on the plate: the green, the red, the '
                         'orange.')],
             [('texte_a_trous', 1,
               {'text': 'Vitamins {{1}} diseases.', 'blanks': 1},
               {'values': ['prevent']}, 'They prevent diseases.'),
              ('qcm', 1, {'question': 'Where do vitamins come from?',
                          'options': ['fruits and vegetables', 'butter and oil',
                                      'salt and water']},
               {'index': 0}, 'Fruits and vegetables.'),
              ('qcm', 2, {'question': 'Which one also gives vitamins?',
                          'options': ['sunlight', 'cold water', 'dry sand']},
               {'index': 0}, 'Sunlight, as the cahier notes.'),
              ('texte_a_trous', 3,
               {'text': 'A child who eats no fruit may easily fall {{1}}.', 'blanks': 1},
               {'values': ['ill']}, 'Fall ill.'),
              ('vrai_faux', 4, {'statement': 'Vitamins protect the body against diseases.'},
               {'value': True}, 'Yes, that is their function.')]),

            ('relation',
             'Water eases digestion and regulates the body temperature. Its sources are water '
             'and juice.',
             'bs-fd-eau',
             'Un verre d-eau, le mot water, et son rôle.',
             [('simple', 'Water does two jobs at once: it moves the food along and it cools the '
                         'body.'),
              ('histoire', 'You can live many days without eating. Without drinking, only a '
                           'few.')],
             [('texte_a_trous', 1,
               {'text': 'Water eases {{1}} in the body.', 'blanks': 1},
               {'values': ['digestion']}, 'It eases digestion.'),
              ('qcm', 1, {'question': 'What else does water regulate?',
                          'options': ['the body temperature', 'the colour of the skin',
                                      'the size of the bones']},
               {'index': 0}, 'The body temperature.'),
              ('qcm', 2, {'question': 'Which drink also belongs to this class?',
                          'options': ['juice', 'palm oil', 'melted butter']},
               {'index': 0}, 'Juice.'),
              ('texte_a_trous', 3,
               {'text': 'Water regulates the body {{1}}.', 'blanks': 1},
               {'values': ['temperature']}, 'The body temperature.'),
              ('vrai_faux', 4, {'statement': 'Water has two functions in the body, not one.'},
               {'value': True}, 'Yes: digestion and temperature.')]),
        ],
    ),

    # ------------------------------------------------------------------ 45
    (
        'Preparing food: the cooking methods', ALIMENTS, None, 45,
        'Food preparation is the various methods through which food can be cooked. Boiling uses '
        'water, baking uses an oven, steaming uses steam, grilling and roasting use fire, and '
        'stewing cooks slowly in sauce. Frying is cooking in hot oil, and it is either shallow '
        'or deep. We cook to kill germs, to make food attractive, tasty, and longer lasting.',
        'bs-cp-couv',
        'Une marmite sur le feu, une cuve à vapeur et un four.',
        [
            ('definition',
             'Food preparation is the various methods through which food can be cooked.',
             'bs-cp-table',
             'Le tableau des six méthodes de cuisson avec leurs exemples.',
             [('simple', 'Three questions tell the methods apart: water, oil, or an oven?'),
              ('visuel', 'Read the table across: the method, a food it suits, and how it '
                         'cooks.')],
             [('texte_a_trous', 1,
               {'text': 'The various methods through which food is cooked is called food '
                        '{{1}}.', 'blanks': 1},
               {'values': ['preparation']}, 'Food preparation.'),
              ('association', 1, {'question': 'Match each method with a food.',
                                  'gauche': ['boiling', 'baking', 'grilling'],
                                  'droite': ['rice and yam', 'bread and cake',
                                             'meat and fish']},
               {'order': [0, 1, 2]}, 'Water, oven, fire.'),
              ('qcm', 2, {'question': 'Which method cooks food in water?',
                          'options': ['boiling', 'baking', 'grilling']},
               {'index': 0}, 'Boiling.'),
              ('texte_a_trous', 3,
               {'text': 'Tomato stew and groundnut stew are cooked by {{1}}.', 'blanks': 1},
               {'values': ['stewing']}, 'By stewing.'),
              ('vrai_faux', 4, {'statement': 'Every food is cooked in the same way.'},
               {'value': False}, 'No. Each method suits certain foods.')]),

            ('relation',
             'Steaming cooks food in the steam of boiling water. Koki and egusi pudding are '
             'steamed.',
             'bs-cp-vapeur',
             'Une marmite couverte, avec la vapeur qui monte.',
             [('simple', 'The food never touches the water. Only the steam reaches it.'),
              ('analogie', 'Boiling is a bath. Steaming is standing in the bathroom with the '
                           'hot tap running.')],
             [('texte_a_trous', 1,
               {'text': 'Koki and egusi pudding are cooked by {{1}}.', 'blanks': 1},
               {'values': ['steaming']}, 'By steaming.'),
              ('qcm', 1, {'question': 'What cooks the food when you steam it?',
                          'options': ['the steam', 'hot oil', 'the open fire']},
               {'index': 0}, 'The steam.'),
              ('qcm', 2, {'question': 'In steaming, does the food touch the water?',
                          'options': ['no, only the steam', 'yes, it is covered',
                                      'yes, it floats in it']},
               {'index': 0}, 'No. Only the steam reaches it.'),
              ('texte_a_trous', 3,
               {'text': 'A pot used for steaming must have a {{1}}.', 'blanks': 1},
               {'values': ['cover']}, 'A cover, to keep the steam in.'),
              ('vrai_faux', 4, {'statement': 'Steaming and boiling are the same method.'},
               {'value': False}, 'No. In boiling the food is in the water.')]),

            ('relation',
             'Baking cooks food in an oven. Bread and cake are baked.',
             'bs-cp-four',
             'Un four fermé, le mot baking, et ses exemples.',
             [('simple', 'In an oven the heat comes from all sides at once.'),
              ('visuel', 'The oven is closed. That is what makes it an oven and not a fire.')],
             [('texte_a_trous', 1,
               {'text': 'Bread and cake are cooked by {{1}}.', 'blanks': 1},
               {'values': ['baking']}, 'By baking.'),
              ('qcm', 1, {'question': 'Where is bread baked?',
                          'options': ['in an oven', 'in a pot of water', 'on an open fire']},
               {'index': 0}, 'In an oven.'),
              ('qcm', 2, {'question': 'Why does an oven cook evenly?',
                          'options': ['the heat comes from all sides', 'it is very small',
                                      'it uses water']},
               {'index': 0}, 'The heat surrounds the food.'),
              ('texte_a_trous', 3,
               {'text': 'An oven must be {{1}} while the food cooks.', 'blanks': 1},
               {'values': ['closed']}, 'Closed.'),
              ('vrai_faux', 4, {'statement': 'Bread can be cooked by boiling it in water.'},
               {'value': False}, 'No. Bread is baked.')]),

            ('relation',
             'Grilling and roasting cook food directly on the fire. Meat, fish and chicken are '
             'grilled or roasted.',
             'bs-cp-grill',
             'Un gril posé au-dessus du feu.',
             [('simple', 'Nothing stands between the food and the heat: no water, no oil.'),
              ('histoire', 'The fish grilled at the roadside has no oil and no water in it. '
                           'Only fire and time.')],
             [('texte_a_trous', 1,
               {'text': 'Meat, fish and chicken can be cooked by {{1}}.', 'blanks': 1},
               {'values': ['grilling']}, 'By grilling.'),
              ('qcm', 1, {'question': 'What does grilling use?',
                          'options': ['fire only', 'oil only', 'water only']},
               {'index': 0}, 'Fire only.'),
              ('qcm', 2, {'question': 'What is between the food and the fire?',
                          'options': ['nothing at all', 'a pot of water', 'a pan of oil']},
               {'index': 0}, 'Nothing at all.'),
              ('texte_a_trous', 3,
               {'text': 'Chicken, meat and fish can also be cooked by {{1}}.', 'blanks': 1},
               {'values': ['roasting']}, 'By roasting.'),
              ('vrai_faux', 4, {'statement': 'Grilling needs a pot of water.'},
               {'value': False}, 'No. The food is put over the fire itself.')]),

            ('relation',
             'Frying is a method of cooking food in hot oil. There are two types: shallow '
             'frying, for eggs and pancake, and deep frying, for fish and chicken.',
             'bs-cp-friture',
             'Une poêle pour la friture à plat, une marmite pour la friture profonde.',
             [('simple', 'Shallow means a little oil. Deep means enough oil to cover the '
                         'food.'),
              ('pas_a_pas', 'Look at how much oil is in the pan. That alone tells you which of '
                            'the two it is.')],
             [('texte_a_trous', 1,
               {'text': 'Frying is a method of cooking food in hot {{1}}.', 'blanks': 1},
               {'values': ['oil']}, 'In hot oil.'),
              ('qcm', 1, {'question': 'How many types of frying are there?',
                          'options': ['two', 'four', 'seven']},
               {'index': 0}, 'Two: shallow and deep.'),
              ('association', 2, {'question': 'Match each type of frying with its example.',
                                  'gauche': ['shallow frying', 'deep frying'],
                                  'droite': ['eggs and pancake', 'fish and chicken']},
               {'order': [0, 1]}, 'A little oil, or enough to cover.'),
              ('texte_a_trous', 3,
               {'text': 'Frying fish in oil that covers it is called {{1}} frying.',
                'blanks': 1},
               {'values': ['deep']}, 'Deep frying.'),
              ('vrai_faux', 4, {'statement': 'Shallow frying and deep frying differ by how much '
                                             'oil is used.'},
               {'value': True}, 'Yes, that is exactly the difference.')]),

            ('liste',
             'We cook food to kill germs, to make it look attractive, to make it taste better, '
             'and to make it last longer.',
             'bs-cp-pourquoi',
             'La liste numérotée des quatre raisons pour lesquelles on cuit les aliments.',
             [('simple', 'One reason is about health, one about the eye, one about the tongue, '
                         'one about time.'),
              ('pas_a_pas', 'The first reason is the one that matters most: heat kills what '
                            'would have made you ill.')],
             [('texte_a_trous', 1,
               {'text': 'We cook food to kill {{1}}.', 'blanks': 1},
               {'values': ['germs']}, 'To kill germs.'),
              ('qcm', 1, {'question': 'Which reason for cooking is about health?',
                          'options': ['to kill germs', 'to make it attractive',
                                      'to make it tasty']},
               {'index': 0}, 'To kill germs.'),
              ('qcm', 2, {'question': 'How many reasons does the lesson give?',
                          'options': ['four', 'two', 'six']},
               {'index': 0}, 'Four.'),
              ('texte_a_trous', 3,
               {'text': 'Cooking also makes food {{1}} longer.', 'blanks': 1},
               {'values': ['last']}, 'Last longer.'),
              ('vrai_faux', 4, {'statement': 'Cooking food can make it safer to eat.'},
               {'value': True}, 'Yes, because the heat kills the germs.')]),
        ],
    ),

    # ------------------------------------------------------------------ 46
    (
        'Preserving food', ALIMENTS, None, 46,
        'Food preservation is the different ways in which food can be kept. Salting keeps meat '
        'and fish, drying keeps corn and beans, canning keeps fish and grains, bottling keeps '
        'water and juice, smoking keeps meat and fish, freezing keeps vegetables and meat, and '
        'sunning keeps fish, corn and groundnut.',
        'bs-cv-couv',
        'Le soleil, un réfrigérateur, une boîte de conserve et une bouteille.',
        [
            ('definition',
             'Food preservation is the different ways in which food can be kept, so that it '
             'lasts longer.',
             'bs-cv-table',
             'Le tableau des méthodes de conservation avec leurs exemples.',
             [('simple', 'Food spoils because it is wet and warm. Every method takes away one '
                         'of the two.'),
              ('analogie', 'Preserving food is winning time: what would be lost tomorrow is '
                           'still good next month.')],
             # Son epreuve : il avait ecrit « conservation ».
             [('texte_a_trous', 1,
               {'text': 'The method of keeping food for it to last longer is called {{1}}.',
                'blanks': 1},
               {'values': ['preservation']}, 'Preservation.'),
              ('association', 1, {'question': 'Match each method with what it uses.',
                                  'gauche': ['drying', 'freezing', 'smoking'],
                                  'droite': ['the air and sun', 'the cold', 'the fire']},
               {'order': [0, 1, 2]}, 'Sun, cold, fire.'),
              ('qcm', 2, {'question': 'Why does preserved food last longer?',
                          'options': ['what spoils it is stopped', 'it is cooked twice',
                                      'it is made heavier']},
               {'index': 0}, 'What makes food spoil is stopped.'),
              ('texte_a_trous', 3,
               {'text': 'Preservation is the different ways in which food can be {{1}}.',
                'blanks': 1},
               {'values': ['kept']}, 'Can be kept.'),
              ('qcm', 4, {'question': 'Keeping food so it lasts longer is called…',
                          'options': ['preservation', 'conservation', 'preparation']},
               {'index': 0},
               'Preservation. Conservation is about protecting nature, not food.')]),

            ('relation',
             'Drying and sunning take the water out of food. Corn, groundnut and beans are '
             'dried.',
             'bs-cv-sec',
             'Le soleil, le mot drying, et ses exemples.',
             [('simple', 'What has no water in it cannot rot.'),
              ('visuel', 'Maize spread on a mat in the yard is being preserved, not just left '
                         'out.')],
             # Son epreuve : il avait repondu « frying » pour le mais.
             [('texte_a_trous', 1,
               {'text': 'Corn, groundnut and beans are kept by {{1}}.', 'blanks': 1},
               {'values': ['drying']}, 'By drying.'),
              ('qcm', 1, {'question': 'What does drying take out of the food?',
                          'options': ['the water', 'the salt', 'the colour']},
               {'index': 0}, 'The water.'),
              ('qcm', 2, {'question': 'Drying food in the sun is also called…',
                          'options': ['sunning', 'bottling', 'stewing']},
               {'index': 0}, 'Sunning.'),
              ('texte_a_trous', 3,
               {'text': 'Food that has no {{1}} in it cannot rot.', 'blanks': 1},
               {'values': ['water']}, 'No water.'),
              ('qcm', 4, {'question': 'Which method can be used to conserve maize?',
                          'options': ['drying', 'frying', 'stewing']},
               {'index': 0}, 'Drying. Frying is a way of cooking, not of keeping.')]),

            ('relation',
             'Freezing keeps food in the cold. Vegetables, meat, fish and tomatoes are frozen.',
             'bs-cv-froid',
             'Un réfrigérateur, le mot freezing, et ses exemples.',
             [('simple', 'Cold does not kill what spoils food. It only stops it working.'),
              ('pas_a_pas', 'Put it in the freezer. Leave it there. Take it out only when you '
                            'will cook it.')],
             [('texte_a_trous', 1,
               {'text': 'Vegetables, meat and fish can be kept by {{1}}.', 'blanks': 1},
               {'values': ['freezing']}, 'By freezing.'),
              ('qcm', 1, {'question': 'What does freezing use?',
                          'options': ['the cold', 'the fire', 'the sun']},
               {'index': 0}, 'The cold.'),
              ('qcm', 2, {'question': 'What happens when frozen food becomes warm again?',
                          'options': ['it begins to spoil', 'it lasts even longer',
                                      'it becomes cooked']},
               {'index': 0}, 'It begins to spoil.'),
              ('texte_a_trous', 3,
               {'text': 'Cold stops what makes food {{1}}.', 'blanks': 1},
               {'values': ['spoil']}, 'Makes food spoil.'),
              ('vrai_faux', 4, {'statement': 'Food taken out of the freezer keeps for ever.'},
               {'value': False}, 'No. Once warm, it begins to spoil.')]),

            ('relation',
             'Canning keeps food in a sealed tin, and bottling keeps it in a bottle. Fish and '
             'grains are canned; water, beer and juice are bottled.',
             'bs-cv-boite',
             'Une boîte de conserve et une bouteille, nommées.',
             [('simple', 'Both close the food away from the air. One in metal, one in glass.'),
              ('analogie', 'Like a letter in a sealed envelope: as long as it is shut, nothing '
                           'reaches what is inside.')],
             [('texte_a_trous', 1,
               {'text': 'Water, beer and juice are kept by {{1}}.', 'blanks': 1},
               {'values': ['bottling']}, 'By bottling.'),
              ('qcm', 1, {'question': 'What is food put into when it is canned?',
                          'options': ['a tin', 'a basket', 'a cloth bag']},
               {'index': 0}, 'A tin.'),
              ('association', 2, {'question': 'Match each method with its container.',
                                  'gauche': ['canning', 'bottling'],
                                  'droite': ['a tin', 'a bottle']},
               {'order': [0, 1]}, 'Metal, or glass.'),
              ('texte_a_trous', 3,
               {'text': 'Both canning and bottling keep the {{1}} away from the food.',
                'blanks': 1},
               {'values': ['air']}, 'The air.'),
              ('vrai_faux', 4, {'statement': 'An open tin keeps food as well as a closed one.'},
               {'value': False}, 'No. Once open, the air comes in.')]),

            ('relation',
             'Salting draws the water out of meat and fish. Smoking dries them over a fire and '
             'covers them with smoke.',
             'bs-cv-fumee',
             'Une salière et du poisson fumé au-dessus du feu.',
             [('simple', 'Both methods end the same way: the food is dry, so it does not rot.'),
              ('histoire', 'The fish smoked at the lake travels for days to the market and '
                           'arrives still good.')],
             [('texte_a_trous', 1,
               {'text': 'Meat and fish can be kept with {{1}}.', 'blanks': 1},
               {'values': ['salt']}, 'With salt.'),
              ('qcm', 1, {'question': 'What does salt do to meat?',
                          'options': ['it draws the water out', 'it adds water to it',
                                      'it cooks it through']},
               {'index': 0}, 'It draws the water out.'),
              ('qcm', 2, {'question': 'Smoking keeps food by…',
                          'options': ['drying and covering it', 'freezing it',
                                      'bottling it tightly']},
               {'index': 0}, 'Drying it and covering it with smoke.'),
              ('texte_a_trous', 3,
               {'text': 'Meat and fish hung over a fire are kept by {{1}}.', 'blanks': 1},
               {'values': ['smoking']}, 'By smoking.'),
              ('vrai_faux', 4, {'statement': 'Salting and drying both work by removing water.'},
               {'value': True}, 'Yes, in two different ways.')]),
        ],
    ),

    # ------------------------------------------------------------------ 47
    (
        'Diet, meals and feeding', SANTE, None, 47,
        'A diet is the kind of food we eat and the different nutrients it contains. There are '
        'three types: balanced, mixed and unbalanced. Meals are the different types of food we '
        'eat at different periods of the day. Underfeeding is eating less food than the body '
        'requires; overfeeding is eating more than it requires.',
        'bs-dt-couv',
        'Deux assiettes : l-une partagée entre plusieurs classes, l-autre d-une seule.',
        [
            ('definition',
             'A diet is the kind of food we eat and the different nutrients that it contains.',
             'bs-dt-diet',
             'Une assiette partagée en trois parts de classes différentes.',
             [('simple', 'A diet is not one meal. It is what you eat, taken together.'),
              ('visuel', 'Look at the plate: how many colours are on it? That is the first '
                         'question to ask of a diet.')],
             [('texte_a_trous', 1,
               {'text': 'The kind of food we eat and the nutrients it contains is called a '
                        '{{1}}.', 'blanks': 1},
               {'values': ['diet']}, 'A diet.'),
              ('qcm', 1, {'question': 'What does a diet contain?',
                          'options': ['different nutrients', 'only water', 'only salt']},
               {'index': 0}, 'Different nutrients.'),
              ('qcm', 2, {'question': 'A diet describes…',
                          'options': ['what a person eats', 'how fast a person eats',
                                      'where a person eats']},
               {'index': 0}, 'What a person eats.'),
              ('texte_a_trous', 3,
               {'text': 'A diet is made of the different {{1}} in our food.', 'blanks': 1},
               {'values': ['nutrients']}, 'The nutrients.'),
              ('vrai_faux', 4, {'statement': 'A diet and a single meal mean the same thing.'},
               {'value': False}, 'No. A diet is what you eat taken as a whole.')]),

            ('liste',
             'There are three types of diet: a balanced diet, a mixed diet and an unbalanced '
             'diet.',
             'bs-dt-types',
             'La liste des trois sortes de régime.',
             [('simple', 'Balanced means every class is there. Unbalanced means one class is '
                         'missing or alone.'),
              ('pas_a_pas', 'Count the classes on the plate. Six present, it is balanced. One '
                            'alone, it is unbalanced.')],
             [('texte_a_trous', 1,
               {'text': 'A diet that contains every class of food is a {{1}} diet.',
                'blanks': 1},
               {'values': ['balanced']}, 'A balanced diet.'),
              ('qcm', 1, {'question': 'How many types of diet are there?',
                          'options': ['three', 'two', 'six']},
               {'index': 0}, 'Three.'),
              ('association', 2, {'question': 'Match each diet with what is on the plate.',
                                  'gauche': ['balanced', 'mixed', 'unbalanced'],
                                  'droite': ['every class', 'several classes',
                                             'one class only']},
               {'order': [0, 1, 2]}, 'Every, several, one.'),
              ('texte_a_trous', 3,
               {'text': 'A plate with only one class of food is an {{1}} diet.', 'blanks': 1},
               {'values': ['unbalanced']}, 'An unbalanced diet.'),
              ('vrai_faux', 4, {'statement': 'A balanced diet and a mixed diet are the same '
                                             'thing.'},
               {'value': False}, 'No. A mixed diet has several classes, not necessarily all.')]),

            ('relation',
             'An unbalanced diet contains only one class of food. It does not give the body '
             'everything it needs.',
             'bs-dt-desequilibre',
             'Une assiette remplie d-une seule classe d-aliment.',
             [('simple', 'You can eat a lot and still be badly fed, if you always eat the same '
                         'thing.'),
              ('histoire', 'A child who eats only fufu is never hungry and never well. The '
                           'energy is there; the protein and the vitamins are not.')],
             [('qcm', 1, {'question': 'What is wrong with an unbalanced diet?',
                          'options': ['it misses some classes', 'it has too much water',
                                      'it is always cold']},
               {'index': 0}, 'It misses some classes of food.'),
              ('texte_a_trous', 1,
               {'text': 'An unbalanced diet has only {{1}} class of food.', 'blanks': 1},
               {'values': ['one']}, 'Only one class.'),
              ('qcm', 2, {'question': 'Can a person eat a lot and still be badly fed?',
                          'options': ['yes, if the diet is unbalanced', 'no, never',
                                      'only when the food is cold']},
               {'index': 0}, 'Yes, if the diet is unbalanced.'),
              ('texte_a_trous', 3,
               {'text': 'A good diet must be {{1}}, with every class present.', 'blanks': 1},
               {'values': ['balanced']}, 'Balanced.'),
              ('vrai_faux', 4, {'statement': 'Eating a large quantity is enough to be well '
                                             'fed.'},
               {'value': False}, 'No. The classes must be there too.')]),

            ('definition',
             'Meals are the different types of food that we eat at different periods of the '
             'day.',
             'bs-dt-repas',
             'Trois assiettes : le petit déjeuner, le déjeuner et le dîner.',
             [('simple', 'Breakfast, lunch and supper are three meals, and together they make '
                         'the day.'),
              ('visuel', 'The same classes can come back at each meal, in different foods.')],
             [('texte_a_trous', 1,
               {'text': 'The food we eat at different periods of the day is called {{1}}.',
                'blanks': 1},
               {'values': ['meals']}, 'Meals.'),
              ('qcm', 1, {'question': 'Which one is the first meal of the day?',
                          'options': ['breakfast', 'lunch', 'supper']},
               {'index': 0}, 'Breakfast.'),
              ('chronologie', 2, {'question': 'Put the meals of the day in order.',
                                  'tokens': ['breakfast', 'lunch', 'supper']},
               {'order': [0, 1, 2]}, 'Breakfast, lunch, supper.'),
              ('texte_a_trous', 3,
               {'text': 'A meal eaten at midday is called {{1}}.', 'blanks': 1},
               {'values': ['lunch']}, 'Lunch.'),
              ('vrai_faux', 4, {'statement': 'A meal and a diet are two names for the same '
                                             'thing.'},
               {'value': False}, 'No. Meals are eaten at times; a diet is the whole of what you '
                                 'eat.')]),

            ('relation',
             'Underfeeding is when we eat less food than the body requires.',
             'bs-dt-sous',
             'Une assiette presque vide.',
             [('simple', 'The body asks for a certain amount. Giving it less is underfeeding.'),
              ('visuel', 'On the picture most of the plate is empty. That emptiness is the '
                         'whole idea.')],
             [('texte_a_trous', 1,
               {'text': 'Eating less food than the body requires is called {{1}}.',
                'blanks': 1},
               {'values': ['underfeeding']}, 'Underfeeding.'),
              ('qcm', 1, {'question': 'Underfeeding means eating…',
                          'options': ['less than the body requires', 'more than it requires',
                                      'exactly what it requires']},
               {'index': 0}, 'Less than the body requires.'),
              ('qcm', 2, {'question': 'What can underfeeding do to a child?',
                          'options': ['stop him growing well', 'make him grow faster',
                                      'make him taller']},
               {'index': 0}, 'It stops him growing well.'),
              ('texte_a_trous', 3,
               {'text': 'A child who is underfed does not {{1}} well.', 'blanks': 1},
               {'values': ['grow']}, 'Does not grow well.'),
              ('vrai_faux', 4, {'statement': 'Underfeeding is eating more than the body '
                                             'requires.'},
               {'value': False}, 'No, that is overfeeding.')]),

            ('relation',
             'Overfeeding is the act of taking more food than the body requires.',
             'bs-dt-sur',
             'Une assiette trop remplie.',
             [('simple', 'More than the body asks for is not better. What is not used is '
                         'stored.'),
              ('analogie', 'Pouring more water than the bucket holds does not fill it more. It '
                           'spills.')],
             [('texte_a_trous', 1,
               {'text': 'Taking more food than the body requires is called {{1}}.',
                'blanks': 1},
               {'values': ['overfeeding']}, 'Overfeeding.'),
              ('qcm', 1, {'question': 'Overfeeding means eating…',
                          'options': ['more than the body requires', 'less than it requires',
                                      'only at night']},
               {'index': 0}, 'More than the body requires.'),
              ('association', 2, {'question': 'Match each word with its meaning.',
                                  'gauche': ['underfeeding', 'overfeeding'],
                                  'droite': ['too little food', 'too much food']},
               {'order': [0, 1]}, 'Less, or more, than the body needs.'),
              ('texte_a_trous', 3,
               {'text': 'Both underfeeding and overfeeding are bad for the {{1}}.',
                'blanks': 1},
               {'values': ['body']}, 'For the body.'),
              ('vrai_faux', 4, {'statement': 'Eating much more than the body needs is good for '
                                             'health.'},
               {'value': False}, 'No. That is overfeeding.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, cles_items, total, notions_vues, trous = set(), set(), 0, 0, 0
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
                if ikind == 'texte_a_trous':
                    trous += 1
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, \
                        'question trop longue (%d) : %s' % (len(payload['question']),
                                                            payload['question'])
                    assert ('options' in payload) != ('images' in payload), payload
                    choix = payload.get('options') or payload['images']
                    assert 2 <= len(choix) <= 4, payload
                    assert len(set(choix)) == len(choix), 'choix en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(choix), payload
                    if 'images' in payload:
                        cles_items.update(choix)
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
                    n = payload['text'].count('{{')
                    assert n == len(answer['values']) == payload['blanks'], payload
                    assert n <= 2, 'plus de deux trous : ' + payload['text']
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

    assert trous >= total * 0.35, \
        'le texte à trous ne domine plus : %d sur %d questions' % (trous, total)

    # Les deux fautes de sa copie travaillées ici.
    tout = json.dumps(LECONS, ensure_ascii=False, default=str)
    assert 'preservation' in tout and 'conservation' in tout, \
        'la confusion preservation / conservation doit être posée'
    assert 'drying' in tout and 'frying' in tout, \
        'la confusion drying / frying doit être posée'

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-brayne-sante-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    utilisees = cles | cles_items
    manquantes = utilisees - dessinees
    inutiles = dessinees - utilisees
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(
        sorted(manquantes))
    assert not inutiles, 'images dessinées mais jamais utilisées : ' + ', '.join(sorted(inutiles))
    return len(utilisees), total, notions_vues, trous


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
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-sante-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous (%.0f%%) - %d images'
          % (len(LECONS), notions, items, trous, 100.0 * trous / items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-40s %-16s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
