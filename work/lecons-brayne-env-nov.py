# -*- coding: utf-8 -*-
"""
Sept leçons d-éducation à l-environnement pour BRAYNE (CM1) — cahier
« Sciences / Health / En. Educ », du 15 octobre au 5 novembre 2026.

EN ANGLAIS, parce que c-est la langue du cahier et donc celle de
l-examen. Le libellé de la matière reste français dans l-application :
c-est l-étagère qui est française, pas le contenu.

LA FORME DES QUESTIONS VIENT DE SON ÉPREUVE, PAS DE MOI.

Les pages 26 à 32 du lot ne sont pas un cours : c-est la révision du
5 novembre, corrigée de la main de la maîtresse. Le style y est
massivement la PHRASE À COMPLÉTER — « Living things that grow from the
soil are called ______ » — et non le choix multiple. Les leçons suivent
cette forme : le texte à trous domine, l-association sert aux tableaux
cause/effet, et le QCM ne vient que là où le cahier pose lui-même un
choix. Un enfant qui révise doit s-entraîner dans la forme où il sera
interrogé, pas dans une autre.

LE DÉFI VISE SES NEUF FAUTES, RELEVÉES SUR SA COPIE.

chlorophyll pris pour « leaves », incinerator pour « pit »,
photosynthesis pour « water cycle », preservation pour « conservation »,
drying pour « frying », carbon dioxide pour « odour », et trois séries
d-exemples fausses. Sept de ces neuf fautes sont des confusions de mot
PROCHE : il sait de quoi on parle et prend le mot d-à côté. Les
questions de palier 4 opposent donc le mot juste à celui qu-il a écrit,
jamais à un mot sans rapport — sinon elles ne l-entraînent à rien.

DEUX RÉSERVES SUR LE CAHIER, portées au père dans
work/brayne-revision-notes.md :

1. La page sur le sol prescrit de brûler les plastiques ; celle sur
   l-air demande de ne pas les brûler. Les deux se contredisent, et
   c-est la seconde qui a raison. Les leçons enseignent ce que le cahier
   dit, parce que c-est ce qui sera demandé, et la contradiction est
   signalée au père plutôt qu-à l-enfant.
2. Le cahier écrit que la plante absorbe l-eau « par les racines et les
   tiges ». L-absorption se fait par les racines. La leçon dit racines,
   qui est d-ailleurs la réponse attendue partout ailleurs.

Usage :  python work/lecons-brayne-env-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-env-nov.py. ')

MATIERE = 'Sciences'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

POLLUTION = 'Pollution'
DECHETS = 'Waste'
ENSEMBLE = 'Living together'
PLANTES = 'Plants'

LECONS = [
    # ------------------------------------------------------------------ 36
    (
        'Air pollution', POLLUTION, '2026-10-15', 36,
        'Air pollution is the release of poisonous or dangerous substances into the '
        'atmosphere. It comes from car exhausts, industries, burning waste and poor '
        'sanitation. It irritates the eyes, brings air borne diseases, makes acid rain fall on '
        'the crops, and destroys the ozone layer, which leads to global warming.',
        'br-ap-couv',
        'Une usine et une voiture, chacune avec sa fumée.',
        [
            ('definition',
             'Air pollution is the release of poisonous or dangerous substances into the '
             'atmosphere.',
             'br-ap-def',
             'Une usine qui fume et une voiture qui fume.',
             [('simple', 'The air itself does not change place. What changes is what we put '
                         'into it.'),
              ('analogie', 'Like pouring dirty water into a clean tank: the tank is still '
                           'there, but nobody wants to drink from it.')],
             [('texte_a_trous', 1,
               {'text': 'The release of poisonous substances into the atmosphere is called '
                        'air {{1}}.', 'blanks': 1},
               {'values': ['pollution']}, 'Air pollution.'),
              ('qcm', 1, {'question': 'Where do the poisonous substances go?',
                          'options': ['into the atmosphere', 'into the river',
                                      'into the ground']},
               {'index': 0}, 'Into the atmosphere, which is the air around us.'),
              ('texte_a_trous', 2,
               {'text': 'Air pollution puts {{1}} substances into the air we breathe.',
                'blanks': 1},
               {'values': ['poisonous']}, 'Poisonous substances.'),
              ('vrai_faux', 3, {'statement': 'Air pollution can be seen in the smoke of a '
                                             'factory.'},
               {'value': True}, 'Yes, smoke is one of the things released.'),
              ('vrai_faux', 4, {'statement': 'Air that looks clean is always free of '
                                             'pollution.'},
               {'value': False}, 'No. Many polluting gases cannot be seen at all.')]),

            ('liste',
             'Air is polluted by carbon dioxide from car exhausts and industries, by solid and '
             'liquid waste, by sulphur and nitrogen dioxide, and by poor sanitation.',
             'br-ap-causes',
             'La liste numérotée des cinq causes de la pollution de l-air.',
             [('simple', 'Four of the five causes come from something that burns or that '
                         'rots.'),
              ('pas_a_pas', 'Ask where the gas comes from: an engine, a factory, a volcano, or '
                            'a gutter. Those are the four doors.')],
             [('texte_a_trous', 1,
               {'text': 'Carbon {{1}} from car exhausts pollutes the air.', 'blanks': 1},
               {'values': ['dioxide']}, 'Carbon dioxide.'),
              ('qcm', 1, {'question': 'Which gas comes out of a car exhaust pipe?',
                          'options': ['carbon dioxide', 'oxygen', 'water vapour only']},
               {'index': 0}, 'Carbon dioxide.'),
              ('qcm', 2, {'question': 'Sulphur dioxide is produced during…',
                          'options': ['a volcanic eruption', 'a rain fall', 'a harvest']},
               {'index': 0}, 'A volcanic eruption.'),
              ('texte_a_trous', 3,
               {'text': 'Poor {{1}} in the gutters pollutes the air with bad odour.',
                'blanks': 1},
               {'values': ['sanitation']}, 'Poor sanitation.'),
              # Son epreuve : il a repondu « odour » a la question sur le gaz.
              ('qcm', 4, {'question': 'Air pollution is caused by poisonous gases such as…',
                          'options': ['carbon dioxide', 'odour', 'water vapour']},
               {'index': 0}, 'Carbon dioxide. Odour is a smell, not a gas that pollutes.')]),

            ('liste',
             'Air pollution causes eye irritation, brings air borne diseases like cough, makes '
             'acid rain that destroys crops, and destroys the ozone layer.',
             'br-ap-effets',
             'La liste numérotée des quatre effets de la pollution de l-air.',
             [('simple', 'Two effects touch the body, two touch the world around it.'),
              ('visuel', 'Eyes and chest first, then the crops, then the sky itself.')],
             [('texte_a_trous', 1,
               {'text': 'Air pollution causes eye {{1}}.', 'blanks': 1},
               {'values': ['irritation']}, 'Eye irritation.'),
              ('qcm', 1, {'question': 'Which disease is carried by polluted air?',
                          'options': ['cough', 'malaria', 'a broken leg']},
               {'index': 0}, 'Cough, which is an air borne disease.'),
              ('association', 2, {'question': 'Match each effect with what it harms.',
                                  'gauche': ['eye irritation', 'acid rain',
                                             'destroyed ozone layer'],
                                  'droite': ['the eyes', 'the crops', 'the whole earth']},
               {'order': [0, 1, 2]}, 'The body, the farm, the planet.'),
              ('texte_a_trous', 3,
               {'text': 'Diseases carried by dirty air are called air {{1}} diseases.',
                'blanks': 1},
               {'values': ['borne']}, 'Air borne diseases.'),
              ('vrai_faux', 4, {'statement': 'Acid rain destroys crops and animals.'},
               {'value': True}, 'Yes, that is one of the four effects.')]),

            ('relation',
             'Dirty air irritates the eyes: it makes them red, watery and painful.',
             'br-ap-oeil',
             'Un oeil irrité, et un nuage de fumée.',
             [('simple', 'The eye is wet and open all day. Whatever floats in the air lands on '
                         'it.'),
              ('pas_a_pas', 'If your eyes burn near a fire of tyres, move away. That burning IS '
                            'the pollution.')],
             [('qcm', 1, {'question': 'What does polluted air do to the eyes?',
                          'options': ['it irritates them', 'it makes them stronger',
                                      'it does nothing at all']},
               {'index': 0}, 'It irritates them.'),
              ('texte_a_trous', 2, {'text': 'Polluted air makes the eyes red and {{1}}.',
                                    'blanks': 1},
               {'values': ['watery']}, 'Red and watery.'),
              ('qcm', 2, {'question': 'Why is the eye easily reached by dirty air?',
                          'options': ['it is open and wet', 'it is very strong',
                                      'it is far from the nose']},
               {'index': 0}, 'It is open and wet all day.'),
              ('texte_a_trous', 3, {'text': 'Burning tyres make the eyes {{1}}.', 'blanks': 1},
               {'values': ['burn']}, 'They burn.'),
              ('vrai_faux', 4, {'statement': 'Eye irritation is one of the effects of air '
                                             'pollution.'},
               {'value': True}, 'Yes, the first one the lesson gives.')]),

            ('relation',
             'Polluted air makes acid rain. The rain falls on the farms and destroys crops and '
             'animals.',
             'br-ap-pluie',
             'Un nuage gris qui pleut sur un champ aux herbes abîmées.',
             [('simple', 'The gases rise, the rain brings them back down, and they come down '
                         'sour.'),
              ('histoire', 'The rain that should have watered the maize burns its leaves '
                           'instead. The farmer did nothing wrong; the town upwind did.')],
             [('texte_a_trous', 1, {'text': 'Polluted air produces {{1}} rain.', 'blanks': 1},
               {'values': ['acid']}, 'Acid rain.'),
              ('qcm', 1, {'question': 'What does acid rain destroy?',
                          'options': ['crops and animals', 'only stones', 'only the air']},
               {'index': 0}, 'Crops and animals.'),
              ('qcm', 2, {'question': 'Where does the acid in the rain come from?',
                          'options': ['from the polluted air', 'from the soil',
                                      'from the roots']},
               {'index': 0}, 'From the gases in the polluted air.'),
              ('texte_a_trous', 3,
               {'text': 'Acid rain destroys the {{1}} that the farmer planted.', 'blanks': 1},
               {'values': ['crops']}, 'The crops.'),
              ('vrai_faux', 4, {'statement': 'Acid rain is good for the farm because it is '
                                             'water.'},
               {'value': False}, 'No. It destroys crops and animals.')]),

            ('relation',
             'Air pollution destroys the ozone layer. The hole lets the sun through and leads '
             'to global warming.',
             'br-ap-ozone',
             'La couche d-ozone en arc, le trou, et le soleil qui passe au travers.',
             [('simple', 'The ozone layer is a roof. A roof with a hole stops protecting the '
                         'house.'),
              ('analogie', 'Global warming is the whole world keeping a blanket it cannot take '
                           'off.')],
             [('texte_a_trous', 1,
               {'text': 'Air pollution destroys the {{1}} layer.', 'blanks': 1},
               {'values': ['ozone']}, 'The ozone layer.'),
              ('qcm', 1, {'question': 'What does the destroyed ozone layer lead to?',
                          'options': ['global warming', 'more rain', 'colder weather']},
               {'index': 0}, 'Global warming.'),
              ('texte_a_trous', 2,
               {'text': 'Global warming is the increase in world {{1}}.', 'blanks': 1},
               {'values': ['temperature']}, 'In world temperature.'),
              ('qcm', 3, {'question': 'What passes through the hole in the ozone layer?',
                          'options': ['the rays of the sun', 'the rain', 'the wind only']},
               {'index': 0}, 'The rays of the sun.'),
              ('vrai_faux', 4, {'statement': 'The ozone layer protects the earth from the sun.'},
               {'value': True}, 'Yes, and that is why a hole in it is dangerous.')]),

            ('liste',
             'Air pollution is prevented by limiting the burning of bushes and tyres, disposing '
             'waste properly, servicing car engines, and using incinerators.',
             'br-ap-prevention',
             'La liste numérotée des quatre moyens de prévention.',
             [('simple', 'Three of the four are about not burning things in the open.'),
              ('pas_a_pas', 'Before you light a fire outside, ask what it will send into the '
                            'air, and whether somebody must breathe it.')],
             [('texte_a_trous', 1,
               {'text': 'We must limit the {{1}} of bushes and tyres in public places.',
                'blanks': 1},
               {'values': ['burning']}, 'The burning.'),
              ('qcm', 1, {'question': 'Why should a car engine be serviced regularly?',
                          'options': ['to release less carbon dioxide', 'to make it louder',
                                      'to make it heavier']},
               {'index': 0}, 'So that it releases less carbon dioxide.'),
              ('qcm', 2, {'question': 'Where should waste be burnt?',
                          'options': ['in an incinerator', 'in the street', 'in the gutter']},
               {'index': 0}, 'In an incinerator.'),
              ('texte_a_trous', 3,
               {'text': 'Solid and liquid wastes must be disposed of {{1}}.', 'blanks': 1},
               {'values': ['properly']}, 'Properly.'),
              ('vrai_faux', 4, {'statement': 'Burning tyres in the street helps to keep the '
                                             'air clean.'},
               {'value': False}, 'No. It is one of the things we must limit.')]),
        ],
    ),

    # ------------------------------------------------------------------ 37
    (
        'Soil pollution', POLLUTION, '2026-10-20', 37,
        'Soil pollution is the contamination of the soil with poisonous substances that are '
        'harmful to humans and to other living organisms in the soil. It comes from plastics, '
        'chemical fertilisers, engine oil and bush fire. Heaps of waste breed rats, snakes and '
        'mosquitoes, and spilt chemicals kill the organisms that live in the soil.',
        'br-sp-couv',
        'Un champ avec des déchets de plusieurs sortes posés dessus.',
        [
            ('definition',
             'Soil pollution is the contamination of the soil with poisonous substances harmful '
             'to humans and to other living organisms in the soil.',
             'br-sp-def',
             'Un champ sur lequel traînent plusieurs déchets.',
             [('simple', 'The soil is alive. Worms, roots and tiny organisms live in it, and '
                         'poison reaches them first.'),
              ('analogie', 'Polluting the soil is poisoning the plate before the food is even '
                           'served.')],
             [('texte_a_trous', 1,
               {'text': 'The contamination of the soil with poisonous substances is called '
                        'soil {{1}}.', 'blanks': 1},
               {'values': ['pollution']}, 'Soil pollution.'),
              ('qcm', 1, {'question': 'Who is harmed by soil pollution?',
                          'options': ['humans and living organisms',
                                      'only the stones in the ground',
                                      'only the rain that falls']},
               {'index': 0}, 'Humans and the living organisms in the soil.'),
              ('texte_a_trous', 2,
               {'text': 'Soil pollution harms the living {{1}} that live in the soil.',
                'blanks': 1},
               {'values': ['organisms']}, 'The living organisms.'),
              ('qcm', 3, {'question': 'Soil pollution is a kind of…',
                          'options': ['contamination', 'harvest', 'irrigation']},
               {'index': 0}, 'Contamination.'),
              ('vrai_faux', 4, {'statement': 'Nothing is alive in the soil, so pollution does '
                                             'not harm it.'},
               {'value': False}, 'No. Many organisms live in the soil.')]),

            ('liste',
             'The soil is polluted by non biodegradable household waste such as plastics, by '
             'chemical fertilisers, by engine oil from vehicles, and by bush fire.',
             'br-sp-causes',
             'La liste numérotée des quatre causes de la pollution du sol.',
             [('simple', 'Non biodegradable means it will not rot away, however long you wait.'),
              ('pas_a_pas', 'Ask of each waste: will the soil be able to eat it? If not, it '
                            'stays, and it pollutes.')],
             [('texte_a_trous', 1,
               {'text': 'Waste that cannot rot away is called non {{1}}.', 'blanks': 1},
               {'values': ['biodegradable']}, 'Non biodegradable.'),
              ('qcm', 1, {'question': 'Which household waste pollutes the soil most?',
                          'options': ['plastics', 'banana peels', 'dry leaves']},
               {'index': 0}, 'Plastics, because they do not rot.'),
              ('qcm', 2, {'question': 'Which industrial waste is named in the lesson?',
                          'options': ['chemical fertilisers', 'wooden boxes', 'paper sheets']},
               {'index': 0}, 'Chemical fertilisers.'),
              ('texte_a_trous', 3,
               {'text': 'Engine {{1}} thrown from vehicles pollutes the soil.', 'blanks': 1},
               {'values': ['oil']}, 'Engine oil.'),
              ('vrai_faux', 4, {'statement': 'Bush fire is one of the causes of soil '
                                             'pollution.'},
               {'value': True}, 'Yes, the fourth one in the lesson.')]),

            ('relation',
             'Bush fire burns the plants and the organisms that live in the top soil, and it '
             'leaves the ground bare.',
             'br-sp-feu',
             'Un champ en feu sur trois foyers, avec la fumée qui monte.',
             [('simple', 'Burning a field is quick, and it costs the soil its life.'),
              ('histoire', 'The farmer burns to clear in one day what the hoe would take a '
                           'week to do. The soil pays the difference for years.')],
             [('qcm', 1, {'question': 'What does bush fire do to the soil?',
                          'options': ['it kills what lives in it', 'it waters it',
                                      'it makes it richer']},
               {'index': 0}, 'It kills the organisms living in it.'),
              ('texte_a_trous', 2, {'text': 'We must avoid burning the {{1}} for farming.',
                                    'blanks': 1},
               {'values': ['bush']}, 'The bush.'),
              ('qcm', 2, {'question': 'Bush fire also pollutes which other thing?',
                          'options': ['the air', 'the rocks', 'the metal']},
               {'index': 0}, 'The air, with its smoke.'),
              ('texte_a_trous', 3,
               {'text': 'After a bush fire the ground is left {{1}}.', 'blanks': 1},
               {'values': ['bare']}, 'Bare.'),
              ('vrai_faux', 4, {'statement': 'Bush fire pollutes the soil and the air at the '
                                             'same time.'},
               {'value': True}, 'Yes, both at once.')]),

            ('liste',
             'Heaps of waste breed rats, snakes and mosquitoes. Spilt chemicals kill soil '
             'organisms, urine destroys the soil, and bad odour causes diseases.',
             'br-sp-dangers',
             'La liste numérotée des cinq dangers de la pollution du sol.',
             [('simple', 'A heap of rubbish is a house. Something always moves in.'),
              ('visuel', 'Rats and snakes come for the shelter; mosquitoes come for the water '
                         'trapped underneath.')],
             [('qcm', 1, {'question': 'What breeds in heaps of waste?',
                          'options': ['rats, snakes and mosquitoes', 'fish and crabs',
                                      'goats and sheep']},
               {'index': 0}, 'Rats, snakes and mosquitoes.'),
              ('texte_a_trous', 1,
               {'text': 'Heaps of waste are a breeding place for dangerous {{1}}.',
                'blanks': 1},
               {'values': ['animals']}, 'Dangerous animals and insects.'),
              ('qcm', 2, {'question': 'What do spilt chemicals kill?',
                          'options': ['the soil organisms', 'the clouds', 'the stones']},
               {'index': 0}, 'The organisms living in the soil.'),
              ('texte_a_trous', 3,
               {'text': 'Bad {{1}} from waste carelessly dumped causes diseases.',
                'blanks': 1},
               {'values': ['odour']}, 'Bad odour.'),
              ('vrai_faux', 4, {'statement': 'Urine carelessly thrown pollutes the soil and '
                                             'the air.'},
               {'value': True}, 'Yes, the lesson says it does both.')]),

            ('liste',
             'Soil pollution is prevented by not burning the bush, collecting plastic waste, '
             'avoiding chemical fertilisers, and not throwing engine oil about.',
             'br-sp-prevention',
             'La liste numérotée des quatre moyens de prévention.',
             [('simple', 'Three of the four are simply: pick it up instead of leaving it.'),
              ('pas_a_pas', 'Collect, then dispose. The waste that is gathered stops being a '
                            'danger the moment it is gathered.')],
             [('texte_a_trous', 1,
               {'text': 'Plastic wastes should be well {{1}}.', 'blanks': 1},
               {'values': ['collected']}, 'Well collected.'),
              ('qcm', 1, {'question': 'What should be avoided when farming?',
                          'options': ['burning the bush', 'using a hoe', 'planting seeds']},
               {'index': 0}, 'Burning the bush.'),
              ('qcm', 2, {'question': 'Which fertiliser should be avoided?',
                          'options': ['chemical fertiliser', 'animal manure', 'compost']},
               {'index': 0}, 'Chemical fertiliser.'),
              ('texte_a_trous', 3,
               {'text': 'We must avoid throwing engine oil {{1}}.', 'blanks': 1},
               {'values': ['carelessly']}, 'Carelessly.'),
              ('vrai_faux', 4, {'statement': 'Chemical fertiliser is the safest way to feed '
                                             'the soil.'},
               {'value': False}, 'No. The lesson says to avoid it.')]),
        ],
    ),

    # ------------------------------------------------------------------ 38
    (
        'Waste and its disposal', DECHETS, '2026-10-22', 38,
        'Waste is anything that is not useful and needs to be thrown away. Waste disposal is '
        'the way by which we throw our waste to keep the environment clean. There are two main '
        'types: organic waste, which decomposes naturally, and inorganic waste, which does '
        'not. Waste is disposed of in dust bins, refuse pits, incinerators, refuse bags and '
        'latrines.',
        'br-dc-couv',
        'Deux poubelles de couleurs différentes et une fosse à ordures.',
        [
            ('definition',
             'Waste is anything that is not useful and needs to be thrown away. Waste disposal '
             'is the way by which we throw it to keep the environment clean.',
             'br-dc-def',
             'Une grande poubelle.',
             [('simple', 'Two words, two ideas: what we throw, and how we throw it.'),
              ('pas_a_pas', 'First ask: is it still useful? If no, it is waste. Then ask: '
                            'where does it go? That is disposal.')],
             [('texte_a_trous', 1,
               {'text': '{{1}} is anything that is not useful and needs to be thrown away.',
                'blanks': 1},
               {'values': ['Waste']}, 'Waste.'),
              ('texte_a_trous', 1,
               {'text': 'The way by which we throw our waste is called waste {{1}}.',
                'blanks': 1},
               {'values': ['disposal']}, 'Waste disposal.'),
              ('qcm', 2, {'question': 'Why do we dispose of waste properly?',
                          'options': ['to keep the environment clean', 'to make it heavier',
                                      'to sell it at the market']},
               {'index': 0}, 'To keep the environment clean.'),
              ('qcm', 3, {'question': 'An old shoe nobody can wear is…',
                          'options': ['waste', 'a resource', 'a fertiliser']},
               {'index': 0}, 'Waste, because it is no longer useful.'),
              ('vrai_faux', 4, {'statement': 'Waste and waste disposal mean the same thing.'},
               {'value': False}, 'No. One is the thing, the other is how we throw it.')]),

            ('liste',
             'There are two main types of waste: organic waste, which decomposes naturally, and '
             'inorganic waste, which cannot decompose naturally.',
             'br-dc-types',
             'Deux poubelles, l-une pour ce qui se décompose, l-autre pour ce qui ne se '
             'décompose pas.',
             [('simple', 'Organic comes from what was alive. Inorganic comes from what was '
                         'made.'),
              ('visuel', 'The green bin takes what the soil can eat. The grey bin takes what it '
                         'cannot.')],
             [('texte_a_trous', 1,
               {'text': 'Waste that decomposes naturally is called {{1}} waste.', 'blanks': 1},
               {'values': ['organic']}, 'Organic waste.'),
              # Son epreuve : « Plastic, shoes and bags are examples of ___ waste »
              ('texte_a_trous', 1,
               {'text': 'Plastics, shoes and bags are examples of {{1}} waste.', 'blanks': 1},
               {'values': ['inorganic']}, 'Inorganic waste.'),
              ('association', 2, {'question': 'Match each waste with its type.',
                                  'gauche': ['faeces', 'a plastic bottle', 'dry leaves'],
                                  'droite': ['organic', 'inorganic', 'organic too']},
               {'order': [0, 1, 2]}, 'What was alive rots; what was made does not.'),
              ('qcm', 3, {'question': 'How many main types of waste are there?',
                          'options': ['two', 'four', 'seven']},
               {'index': 0}, 'Two: organic and inorganic.'),
              # Son epreuve : il avait repondu « organic manure » aux exemples.
              ('qcm', 4, {'question': 'Two examples of organic waste are…',
                          'options': ['plants and faeces', 'plastics and bottles',
                                      'metals and glass']},
               {'index': 0}, 'Plants and faeces. Both were once alive, so both rot.')]),

            ('liste',
             'Waste is disposed of in dust bins, refuse pits, incinerators, refuse bags, and '
             'pit or water closet latrines.',
             'br-dc-methodes',
             'La liste numérotée des cinq méthodes d-évacuation des déchets.',
             [('simple', 'Each method suits a place: the house, the yard, the town, the road, '
                         'the toilet.'),
              ('pas_a_pas', 'Collect in a bin, carry to a pit or a bag, and burn only what must '
                            'be burnt, in an incinerator.')],
             [('qcm', 1, {'question': 'What is used to collect waste in schools and homes?',
                          'options': ['a dust bin', 'a cooking pot', 'a school bag']},
               {'index': 0}, 'A dust bin or trash can.'),
              ('texte_a_trous', 1,
               {'text': 'Refuse {{1}} are left along the road side to be collected.',
                'blanks': 1},
               {'values': ['bags']}, 'Refuse bags.'),
              ('chronologie', 2, {'question': 'Put the three steps in order.',
                                  'tokens': ['Collect in a dust bin', 'Carry it outside',
                                             'The company takes it away']},
               {'order': [0, 1, 2]}, 'Collect, carry, then it is taken away.'),
              ('texte_a_trous', 3,
               {'text': 'Faeces and urine are disposed of in a {{1}}.', 'blanks': 1},
               {'values': ['latrine']}, 'A latrine.'),
              ('vrai_faux', 4, {'statement': 'A dust bin and a refuse pit do the same work.'},
               {'value': False}, 'No. The bin collects inside; the pit holds it outside.')]),

            ('relation',
             'A refuse pit is a hole dug a distance away from the house, where garbage is '
             'thrown.',
             'br-dc-fosse',
             'Une fosse creusée dans le sol, avec des déchets dedans.',
             [('simple', 'Away from the house, because of the smell and the animals it draws.'),
              ('visuel', 'The hole is deep so that the waste stays below the level of the '
                         'ground.')],
             [('texte_a_trous', 1,
               {'text': 'A hole dug away from the house for garbage is a refuse {{1}}.',
                'blanks': 1},
               {'values': ['pit']}, 'A refuse pit.'),
              ('qcm', 1, {'question': 'Where is a refuse pit dug?',
                          'options': ['away from the house', 'inside the kitchen',
                                      'under the bed']},
               {'index': 0}, 'A distance away from the house.'),
              ('qcm', 2, {'question': 'Why is the pit dug far from the house?',
                          'options': ['because of smell and animals', 'because it is deeper',
                                      'because the soil is softer']},
               {'index': 0}, 'Because of the smell and the animals it attracts.'),
              ('texte_a_trous', 3,
               {'text': 'Garbage thrown into a pit stays below the level of the {{1}}.',
                'blanks': 1},
               {'values': ['ground']}, 'The ground.'),
              ('vrai_faux', 4, {'statement': 'A refuse pit should be dug beside the kitchen '
                                             'door.'},
               {'value': False}, 'No, it is dug a distance away.')]),

            ('relation',
             'An incinerator is a concrete structure where garbage or refuse is burnt in towns.',
             'br-dc-incinerateur',
             'Un incinérateur en béton avec sa cheminée et son feu.',
             [('simple', 'It is built to burn, so the fire stays inside and does not spread.'),
              ('analogie', 'A fire in the street goes everywhere. The same fire in an '
                           'incinerator stays where it was put.')],
             # Son epreuve : il a repondu « pit » a cette question exacte.
             [('texte_a_trous', 1,
               {'text': 'A structure built away from the town for burning waste is an {{1}}.',
                'blanks': 1},
               {'values': ['incinerator']}, 'An incinerator.'),
              ('qcm', 1, {'question': 'What is an incinerator made of?',
                          'options': ['concrete', 'paper', 'cloth']},
               {'index': 0}, 'Concrete.'),
              ('qcm', 2, {'question': 'What happens to the refuse in an incinerator?',
                          'options': ['it is burnt', 'it is buried', 'it is washed']},
               {'index': 0}, 'It is burnt.'),
              ('texte_a_trous', 3,
               {'text': 'Incinerators are found mostly in {{1}}.', 'blanks': 1},
               {'values': ['towns']}, 'In towns.'),
              ('qcm', 4, {'question': 'A pit built for burning waste is called…',
                          'options': ['an incinerator', 'a pit', 'a refuse bag']},
               {'index': 0}, 'An incinerator. A pit only holds the waste; it does not burn it.')]),

            ('relation',
             'Refuse bags are bags in which waste is collected and kept along the road side for '
             'the hygiene and sanitation company to collect.',
             'br-dc-sac',
             'Un sac à ordures fermé.',
             [('simple', 'The bag is not where the waste ends. It is how it travels.'),
              ('pas_a_pas', 'Fill the bag, close it, put it at the road side on the right day, '
                            'and the company takes it.')],
             [('texte_a_trous', 1,
               {'text': 'Waste is kept in bags along the road {{1}}.', 'blanks': 1},
               {'values': ['side']}, 'The road side.'),
              ('qcm', 1, {'question': 'Who collects the refuse bags?',
                          'options': ['the sanitation company', 'the school teacher',
                                      'the farmer next door']},
               {'index': 0}, 'The hygiene and sanitation company.'),
              ('qcm', 2, {'question': 'Why are the bags closed?',
                          'options': ['so the waste does not spill', 'so they look nice',
                                      'so they weigh more']},
               {'index': 0}, 'So that the waste does not spill out.'),
              ('texte_a_trous', 3,
               {'text': 'The company that collects the bags works for hygiene and {{1}}.',
                'blanks': 1},
               {'values': ['sanitation']}, 'Hygiene and sanitation.'),
              ('vrai_faux', 4, {'statement': 'A refuse bag is a place where waste stays for '
                                             'ever.'},
               {'value': False}, 'No, it is only how the waste travels to its place.')]),
        ],
    ),

    # ------------------------------------------------------------------ 39
    (
        'Waste transformation', DECHETS, '2026-10-22', 39,
        'Waste transformation, or recycling, is the transformation of waste into useful '
        'materials. It reduces environmental pollution and saves our money and our resources. '
        'Waste paper becomes new paper and bags, animal dung becomes organic manure, and human '
        'faeces collected in an enclosed pit become biogas, which is used as fuel.',
        'br-rc-couv',
        'Une poubelle, une flèche, et un tas de matière utile.',
        [
            ('definition',
             'Waste transformation is the transformation of waste into useful materials. It is '
             'also called recycling.',
             'br-rc-def',
             'Une chaîne : le déchet à gauche, la matière utile à droite.',
             [('simple', 'Nothing is added. The same matter is simply put to a new use.'),
              ('analogie', 'Like turning an old shirt into a cleaning cloth: it was finished as '
                           'a shirt, it is not finished as matter.')],
             # Son epreuve : la question exacte etait posee le 5 novembre.
             [('texte_a_trous', 1,
               {'text': 'The transformation of waste into other useful materials is called '
                        '{{1}}.', 'blanks': 1},
               {'values': ['recycling']}, 'Recycling, or waste transformation.'),
              ('qcm', 1, {'question': 'What does waste become after transformation?',
                          'options': ['a useful material', 'more waste', 'nothing at all']},
               {'index': 0}, 'A useful material.'),
              ('qcm', 2, {'question': 'Another name for waste transformation is…',
                          'options': ['recycling', 'disposal', 'pollution']},
               {'index': 0}, 'Recycling.'),
              ('texte_a_trous', 3,
               {'text': 'Recycling turns waste into {{1}} materials.', 'blanks': 1},
               {'values': ['useful']}, 'Useful materials.'),
              ('vrai_faux', 4, {'statement': 'Recycling and throwing away are two names for '
                                             'the same act.'},
               {'value': False}, 'No. One makes the waste useful again, the other does not.')]),

            ('liste',
             'Waste transformation reduces environmental pollution and helps to economise our '
             'money and our resources.',
             'br-rc-importance',
             'La liste des raisons pour lesquelles on recycle.',
             [('simple', 'What is recycled is not thrown, so it does not pollute, and it does '
                         'not have to be bought again.'),
              ('pas_a_pas', 'Count twice: once what you do not throw, once what you do not '
                            'buy.')],
             [('texte_a_trous', 1,
               {'text': 'Recycling reduces environmental {{1}}.', 'blanks': 1},
               {'values': ['pollution']}, 'Environmental pollution.'),
              ('qcm', 1, {'question': 'What else does recycling save?',
                          'options': ['money and resources', 'a little time',
                                      'nothing at all']},
               {'index': 0}, 'Money and resources.'),
              ('qcm', 2, {'question': 'Why does recycling reduce pollution?',
                          'options': ['the waste is not thrown away', 'it makes more waste',
                                      'it burns the waste']},
               {'index': 0}, 'Because the waste is used instead of being thrown.'),
              ('texte_a_trous', 3,
               {'text': 'Recycling helps us to {{1}} our money.', 'blanks': 1},
               {'values': ['economise']}, 'To economise our money.'),
              ('vrai_faux', 4, {'statement': 'Recycling is useful for the environment and for '
                                             'the pocket.'},
               {'value': True}, 'Yes, for both at once.')]),

            ('relation',
             'Waste papers can be used to produce more papers, bags, or things for decoration.',
             'br-rc-papier',
             'Une chaîne : le papier usagé devient papier et sacs neufs.',
             [('simple', 'Paper is made of fibres, and the fibres can be used again.'),
              ('visuel', 'The same sheet becomes another sheet, or a bag, or a decoration.')],
             [('texte_a_trous', 1,
               {'text': 'Waste papers can be used to produce more {{1}}.', 'blanks': 1},
               {'values': ['papers']}, 'More papers.'),
              ('qcm', 1, {'question': 'What else can waste paper become?',
                          'options': ['bags', 'metal', 'water']},
               {'index': 0}, 'Bags, or things for decoration.'),
              ('qcm', 2, {'question': 'Paper can be recycled because it is made of…',
                          'options': ['fibres', 'stone', 'glass']},
               {'index': 0}, 'Fibres, which can be used again.'),
              ('texte_a_trous', 3,
               {'text': 'Old paper can be turned into bags or used for {{1}}.', 'blanks': 1},
               {'values': ['decoration']}, 'For decoration.'),
              ('vrai_faux', 4, {'statement': 'Once paper has been written on it can never be '
                                             'used again.'},
               {'value': False}, 'No. It can be recycled into new paper.')]),

            ('relation',
             'The faeces of goats, pigs and cows are used as organic manure. Fowl droppings, '
             'dried and ground, make the best organic manure.',
             'br-rc-fumier',
             'Une chaîne : le fumier devient engrais organique pour la plante.',
             [('simple', 'What the animal cannot use, the plant can.'),
              ('histoire', 'The droppings swept out of the fowl house in the morning feed the '
                           'maize in the afternoon.')],
             [('qcm', 1, {'question': 'Which droppings make the best organic manure?',
                          'options': ['fowl droppings', 'goat droppings', 'cow droppings']},
               {'index': 0}, 'Fowl droppings.'),
              ('texte_a_trous', 1,
               {'text': 'Animal faeces are used as organic {{1}}.', 'blanks': 1},
               {'values': ['manure']}, 'Organic manure.'),
              ('chronologie', 2, {'question': 'Put the three steps for fowl droppings in order.',
                                  'tokens': ['Dry them', 'Grind them', 'Use them as manure']},
               {'order': [0, 1, 2]}, 'Dried, ground, then used.'),
              ('texte_a_trous', 3,
               {'text': 'Fowl droppings are dried and {{1}} before use.', 'blanks': 1},
               {'values': ['ground']}, 'Dried and ground.'),
              ('vrai_faux', 4, {'statement': 'Animal dung is waste that can become a resource.'},
               {'value': True}, 'Yes, that is exactly what recycling means.')]),

            ('relation',
             'Human faeces and urine are collected in an underground chamber and transformed '
             'into biogas, which is used as a source of energy.',
             'br-rc-biogaz',
             'Une fosse fermée sous la terre, avec le gaz qui en sort par un tuyau.',
             [('simple', 'The chamber is closed. It is that closing which makes the gas.'),
              ('analogie', 'What would have been a danger in the open becomes a cooking fire '
                           'once it is enclosed.')],
             # Son epreuve : la question exacte etait posee le 5 novembre.
             [('texte_a_trous', 1,
               {'text': 'The gas that comes from an enclosed pit of faeces is called {{1}}.',
                'blanks': 1},
               {'values': ['biogas']}, 'Biogas.'),
              ('qcm', 1, {'question': 'What is biogas used for in our homes?',
                          'options': ['cooking', 'washing', 'painting']},
               {'index': 0}, 'For cooking. It is a source of energy.'),
              ('qcm', 2, {'question': 'Where is the chamber built?',
                          'options': ['under the ground', 'on the roof', 'in the river']},
               {'index': 0}, 'Under the ground.'),
              ('texte_a_trous', 3,
               {'text': 'Biogas is used as a source of {{1}}.', 'blanks': 1},
               {'values': ['energy']}, 'Of energy.'),
              ('vrai_faux', 4, {'statement': 'Biogas can be made in an open pit left uncovered.'},
               {'value': False}, 'No. The chamber must be enclosed.')]),
        ],
    ),

    # ------------------------------------------------------------------ 40
    (
        'Conflicts and their resolution', ENSEMBLE, '2026-10-22', 40,
        'A conflict is a disagreement between two or more people resulting in violence or war. '
        'Conflicts are seen at home, in school, in villages, in communities, in countries and '
        'in churches. They come from jealousy, family problems, wrong decisions by leaders, and '
        'stubbornness. Conflict resolution is the act of bringing a conflict to an end.',
        'br-cf-couv',
        'Deux personnes qui se disputent, une flèche, et les mêmes qui se serrent la main.',
        [
            ('definition',
             'A conflict is a disagreement between two or more people resulting in violence or '
             'war.',
             'br-cf-def',
             'Deux personnes face à face, et l-éclair du désaccord entre elles.',
             [('simple', 'Two people can disagree quietly. It becomes a conflict when the '
                         'disagreement turns to violence.'),
              ('pas_a_pas', 'Count the people: at least two. Find the disagreement. Then look '
                            'at what it has turned into.')],
             [('texte_a_trous', 1,
               {'text': 'A disagreement between two or more people is called a {{1}}.',
                'blanks': 1},
               {'values': ['conflict']}, 'A conflict.'),
              ('qcm', 1, {'question': 'How many people are needed for a conflict?',
                          'options': ['two or more', 'only one', 'at least ten']},
               {'index': 0}, 'Two or more.'),
              ('texte_a_trous', 2,
               {'text': 'A conflict can result in violence or {{1}}.', 'blanks': 1},
               {'values': ['war']}, 'Violence or war.'),
              ('qcm', 3, {'question': 'When does a disagreement become a conflict?',
                          'options': ['when it turns to violence', 'when it is written down',
                                      'when it is forgotten']},
               {'index': 0}, 'When it results in violence or war.'),
              ('vrai_faux', 4, {'statement': 'A person can be in conflict entirely alone.'},
               {'value': False}, 'No. A conflict needs two or more people.')]),

            ('liste',
             'Conflicts can be seen at home, in school, in villages, in communities, in '
             'countries and in churches.',
             'br-cf-lieux',
             'La liste numérotée des lieux où naissent les conflits.',
             [('simple', 'Wherever people live together, a conflict can start.'),
              ('visuel', 'The list goes from the smallest place to the largest: the house, then '
                         'the school, then the whole country.')],
             [('qcm', 1, {'question': 'Where can a conflict be seen?',
                          'options': ['at home and in school', 'only in countries',
                                      'only in churches']},
               {'index': 0}, 'In all of those places.'),
              ('texte_a_trous', 1,
               {'text': 'Conflicts can be seen at {{1}}, in school and in villages.',
                'blanks': 1},
               {'values': ['home']}, 'At home.'),
              ('chronologie', 2, {'question': 'Order these places from smallest to largest.',
                                  'tokens': ['home', 'school', 'village', 'country']},
               {'order': [0, 1, 2, 3]}, 'Home, school, village, country.'),
              ('texte_a_trous', 3,
               {'text': 'A conflict between two {{1}} can become a war.', 'blanks': 1},
               {'values': ['countries']}, 'Between two countries.'),
              ('vrai_faux', 4, {'statement': 'Conflicts happen only between countries.'},
               {'value': False}, 'No. They happen at home and in school too.')]),

            ('liste',
             'Conflicts are caused by jealousy, by family problems over property, by wrong '
             'decisions taken by political leaders, and by stubbornness and disrespect.',
             'br-cf-causes',
             'La liste numérotée des quatre causes de conflit.',
             [('simple', 'Three of the four causes are about what people feel; one is about '
                         'what leaders decide.'),
              ('histoire', 'Two brothers inherit one field. Neither will give way. The field '
                           'that fed them both now divides them.')],
             [('qcm', 1, {'question': 'Which feeling causes conflicts at home and at work?',
                          'options': ['jealousy', 'patience', 'kindness']},
               {'index': 0}, 'Jealousy.'),
              ('texte_a_trous', 1,
               {'text': 'Family problems over {{1}} cause conflicts.', 'blanks': 1},
               {'values': ['property']}, 'Over property, often inheritance.'),
              ('qcm', 2, {'question': 'Which cause comes from political leaders?',
                          'options': ['wrong decisions', 'laziness', 'jealousy']},
               {'index': 0}, 'Wrong decisions taken by political leaders.'),
              ('texte_a_trous', 3,
               {'text': 'Stubbornness, disrespect and {{1}} also cause conflicts.',
                'blanks': 1},
               {'values': ['laziness']}, 'And laziness.'),
              ('vrai_faux', 4, {'statement': 'Only leaders can cause a conflict.'},
               {'value': False}, 'No. Jealousy and stubbornness cause them too.')]),

            ('liste',
             'Conflicts lead to loss of lives and properties, bring enmity in the family and '
             'the community, and lead to violence and war.',
             'br-cf-effets',
             'La liste numérotée des trois effets des conflits.',
             [('simple', 'What is lost in a conflict is rarely given back when it ends.'),
              ('analogie', 'A broken pot can be mended, but it never again holds water the way '
                           'it did.')],
             [('qcm', 1, {'question': 'What can a conflict cause people to lose?',
                          'options': ['lives and properties', 'only time', 'only money']},
               {'index': 0}, 'Lives and properties.'),
              ('texte_a_trous', 1,
               {'text': 'Conflict brings {{1}} in the family and the community.', 'blanks': 1},
               {'values': ['enmity']}, 'Enmity, which means being enemies.'),
              ('association', 2, {'question': 'Match each effect with where it is felt.',
                                  'gauche': ['loss of lives', 'enmity', 'war'],
                                  'droite': ['in the family', 'in the community',
                                             'in the country']},
               {'order': [0, 1, 2]}, 'From the home outwards.'),
              ('texte_a_trous', 3,
               {'text': 'A conflict that grows between countries leads to {{1}}.',
                'blanks': 1},
               {'values': ['war']}, 'To war.'),
              ('vrai_faux', 4, {'statement': 'A conflict always ends without anybody losing '
                                             'anything.'},
               {'value': False}, 'No. Lives and properties are lost.')]),

            ('relation',
             'Conflict resolution is the act of bringing a conflict to an end: there shall be '
             'dialogue, we apologise when wrong, and we learn to forgive.',
             'br-cf-resolution',
             'Les deux mêmes personnes, cette fois se serrant la main.',
             [('simple', 'Three acts, in order: talk, say sorry, forgive.'),
              ('pas_a_pas', 'Sit down and speak. If you were wrong, say so. If the other was '
                            'wrong and has said so, forgive.')],
             [('texte_a_trous', 1,
               {'text': 'Bringing a conflict to an end is called conflict {{1}}.', 'blanks': 1},
               {'values': ['resolution']}, 'Conflict resolution.'),
              ('qcm', 1, {'question': 'What is the first way to resolve a conflict?',
                          'options': ['dialogue', 'fighting', 'running away']},
               {'index': 0}, 'Dialogue, which means talking together.'),
              ('chronologie', 2, {'question': 'Put the three acts in order.',
                                  'tokens': ['Have a dialogue', 'Apologise when wrong',
                                             'Forgive those who offend us']},
               {'order': [0, 1, 2]}, 'Talk, apologise, forgive.'),
              ('texte_a_trous', 3,
               {'text': 'We should always {{1}} when we are wrong.', 'blanks': 1},
               {'values': ['apologise']}, 'Apologise.'),
              ('vrai_faux', 4, {'statement': 'Dialogue is one of the ways a conflict is '
                                             'brought to an end.'},
               {'value': True}, 'Yes, the first one.')]),
        ],
    ),

    # ------------------------------------------------------------------ 41
    (
        'Plants and their kinds', PLANTES, '2026-10-27', 41,
        'A plant is a living thing that grows from the soil. It absorbs water through its roots '
        'and makes its own food in the leaves, using water, sunlight and carbon dioxide, in a '
        'process called photosynthesis. Plants are weeds, herbs, shrubs, trees or leguminous '
        'plants, and they live for one year, two years, or many years.',
        'br-pl-couv',
        'Une plante entière avec ses racines dans la terre.',
        [
            ('definition',
             'A plant is a living thing that grows from the soil. It absorbs water through its '
             'roots to prepare its food.',
             'br-pl-def',
             'Une plante entière, tige, feuilles, fleur, fruit et racines.',
             [('simple', 'A plant is alive: it grows, it feeds, it makes more of itself.'),
              ('visuel', 'Half of a plant is under the ground. That half is what holds it and '
                         'feeds it.')],
             # Son epreuve : la question exacte etait la premiere du 5 novembre.
             [('texte_a_trous', 1,
               {'text': 'Living things that grow from the soil are called {{1}}.', 'blanks': 1},
               {'values': ['plants']}, 'Plants.'),
              ('qcm', 1, {'question': 'Through which part does a plant absorb water?',
                          'options': ['its roots', 'its flowers', 'its fruits']},
               {'index': 0}, 'Through its roots.'),
              ('texte_a_trous', 2,
               {'text': 'A plant grows from the {{1}}.', 'blanks': 1},
               {'values': ['soil']}, 'From the soil.'),
              ('qcm', 3, {'question': 'A plant is…',
                          'options': ['a living thing', 'a kind of stone', 'a kind of water']},
               {'index': 0}, 'A living thing.'),
              ('vrai_faux', 4, {'statement': 'A plant takes in its water through the flowers.'},
               {'value': False}, 'No. It takes it in through the roots.')]),

            ('relation',
             'A plant makes its own food in a process called photosynthesis, using water, '
             'sunlight and carbon dioxide.',
             'br-pl-photo',
             'Le soleil, le gaz carbonique et l-eau qui convergent vers une feuille.',
             [('simple', 'Three things go in: water, sunlight, carbon dioxide. Food comes out.'),
              ('analogie', 'The leaf is a kitchen, and the sun is the fire that cooks in it.')],
             # Son epreuve : il avait repondu « water cycle ».
             [('texte_a_trous', 1,
               {'text': 'Plants make their food in a process called {{1}}.', 'blanks': 1},
               {'values': ['photosynthesis']}, 'Photosynthesis.'),
              ('qcm', 1, {'question': 'Which three things does photosynthesis need?',
                          'options': ['water, sunlight, carbon dioxide', 'soil, wind, stone',
                                      'oil, salt, water']},
               {'index': 0}, 'Water, sunlight and carbon dioxide.'),
              ('qcm', 2, {'question': 'In which part of the plant is the food made?',
                          'options': ['the leaves', 'the roots', 'the fruits']},
               {'index': 0}, 'In the leaves.'),
              ('texte_a_trous', 3,
               {'text': 'Plants need {{1}} from the sun to make their food.', 'blanks': 1},
               {'values': ['sunlight']}, 'Sunlight.'),
              ('qcm', 4, {'question': 'Plants manufacture their food in a process called…',
                          'options': ['photosynthesis', 'the water cycle', 'transpiration']},
               {'index': 0}, 'Photosynthesis. The water cycle is about rain, not about food.')]),

            ('liste',
             'Weeds are unwanted plants that grow everywhere, herbs have soft stems, shrubs have '
             'woody stems, and trees are large tall plants with woody stems.',
             'br-pl-types',
             'Quatre vignettes nommées : weeds, herbs, shrubs, trees.',
             [('simple', 'The stem tells you which is which: soft for a herb, woody for a shrub '
                         'or a tree.'),
              ('pas_a_pas', 'Touch the stem. Soft, it is a herb. Hard and short, a shrub. Hard '
                            'and tall, a tree.')],
             [('texte_a_trous', 1,
               {'text': 'Unwanted plants that grow everywhere are called {{1}}.', 'blanks': 1},
               {'values': ['weeds']}, 'Weeds.'),
              ('qcm', 1, {'question': 'Plants with soft stems are called…',
                          'options': ['herbs', 'trees', 'shrubs']},
               {'index': 0}, 'Herbs.'),
              ('association', 2, {'question': 'Match each plant with its stem.',
                                  'gauche': ['herb', 'shrub', 'tree'],
                                  'droite': ['a soft stem', 'a woody stem',
                                             'a woody stem and tall']},
               {'order': [0, 1, 2]}, 'Soft, woody, woody and tall.'),
              ('texte_a_trous', 3,
               {'text': 'Shrubs are plants with {{1}} stems.', 'blanks': 1},
               {'values': ['woody']}, 'Woody stems.'),
              ('vrai_faux', 4, {'statement': 'A shrub has a soft stem like a herb.'},
               {'value': False}, 'No. A shrub has a woody stem.')]),

            ('relation',
             'Leguminous plants have root nodules. They are important because they add nitrogen '
             'into the soil, and the nitrogen improves soil fertility.',
             'br-pl-legum',
             'Une racine portant ses nodosités.',
             [('simple', 'They feed the soil instead of only taking from it.'),
              ('histoire', 'The farmer who plants beans one season finds the maize taller the '
                           'next. The beans left the nitrogen behind.')],
             # Son epreuve : il avait repondu « tomato ».
             [('texte_a_trous', 1,
               {'text': 'Leguminous plants have root {{1}}.', 'blanks': 1},
               {'values': ['nodules']}, 'Root nodules.'),
              ('qcm', 1, {'question': 'What do leguminous plants add into the soil?',
                          'options': ['nitrogen', 'plastic', 'salt']},
               {'index': 0}, 'Nitrogen.'),
              ('texte_a_trous', 2,
               {'text': 'The nitrogen they add improves soil {{1}}.', 'blanks': 1},
               {'values': ['fertility']}, 'Soil fertility.'),
              ('qcm', 3, {'question': 'Why are leguminous plants important?',
                          'options': ['they make the soil richer', 'they grow very fast',
                                      'they need no water']},
               {'index': 0}, 'They make the soil richer by adding nitrogen.'),
              ('qcm', 4, {'question': 'Two examples of leguminous plants are…',
                          'options': ['beans and groundnut', 'tomato and pepper',
                                      'orange and apple']},
               {'index': 0}, 'Beans and groundnut. Tomato has no root nodules.')]),

            ('liste',
             'Annual plants grow for only one year and die, biennial plants grow for two years, '
             'and perennial plants grow for many years.',
             'br-pl-kinds',
             'La liste des trois sortes de plantes selon leur durée de vie.',
             [('simple', 'One year, two years, many years. The name says the number.'),
              ('visuel', 'Annual comes from année, biennial has bi for two, perennial means '
                         'through the years.')],
             # Son epreuve : il avait repondu « apple and orange ».
             [('texte_a_trous', 1,
               {'text': 'Plants that grow for only one year are called {{1}} plants.',
                'blanks': 1},
               {'values': ['annual']}, 'Annual plants.'),
              ('qcm', 1, {'question': 'How long does a biennial plant grow?',
                          'options': ['two years', 'one year', 'many years']},
               {'index': 0}, 'Two years.'),
              ('association', 2, {'question': 'Match each kind with its length of life.',
                                  'gauche': ['annual', 'biennial', 'perennial'],
                                  'droite': ['one year', 'two years', 'many years']},
               {'order': [0, 1, 2]}, 'One, two, many.'),
              ('texte_a_trous', 3,
               {'text': 'Plants that grow for many years are called {{1}} plants.',
                'blanks': 1},
               {'values': ['perennial']}, 'Perennial plants.'),
              ('qcm', 4, {'question': 'Two examples of annual plants are…',
                          'options': ['beans and maize', 'apple and orange',
                                      'mango and avocado']},
               {'index': 0}, 'Beans and maize. Apple and orange trees live many years.')]),
        ],
    ),

    # ------------------------------------------------------------------ 42
    (
        'The parts of a plant and their functions', PLANTES, '2026-10-27', 42,
        'A plant has a terminal bud, leaves, flowers, fruits, branches, a stem and roots. The '
        'bud makes young leaves and branches, the leaves make the food and send out excess '
        'water, the flower becomes the fruit, the branches carry and transport, the stem holds '
        'the branches, and the roots hold the plant and absorb water and minerals.',
        'br-pt-couv',
        'Le schéma de la plante, et la liste de ses parties.',
        [
            ('liste',
             'The parts of a plant are the terminal bud, the leaves, the flowers, the fruits, '
             'the branches, the stem and the roots.',
             'br-pt-schema',
             'Le schéma complet de la plante, chaque partie étiquetée.',
             [('simple', 'Seven parts. Three are above the soil and easy to see, one is below '
                         'and does half the work.'),
              ('visuel', 'Read the diagram from the top down: bud, leaf, flower, fruit, branch, '
                         'stem, root.')],
             [('qcm', 1, {'question': 'Which part of a plant is under the soil?',
                          'options': ['the roots', 'the leaves', 'the flowers']},
               {'index': 0}, 'The roots.'),
              ('texte_a_trous', 1,
               {'text': 'The part at the very top of the plant is the terminal {{1}}.',
                'blanks': 1},
               {'values': ['bud']}, 'The terminal bud.'),
              ('association', 2, {'question': 'Match each part with where it is found.',
                                  'gauche': ['terminal bud', 'flower', 'roots'],
                                  'droite': ['at the top', 'on a branch', 'under the soil']},
               {'order': [0, 1, 2]}, 'Top, branch, soil.'),
              ('texte_a_trous', 3,
               {'text': 'The {{1}} holds the branches of the plant.', 'blanks': 1},
               {'values': ['stem']}, 'The stem.'),
              ('vrai_faux', 4, {'statement': 'Every part of a plant is above the soil.'},
               {'value': False}, 'No. The roots are under it.')]),

            ('relation',
             'The terminal or apical bud grows to produce young leaves and branches.',
             'br-pt-bourgeon',
             'Le schéma, le bourgeon terminal mis en avant.',
             [('simple', 'It is the growing point. Everything new on the plant starts there.'),
              ('analogie', 'The bud is the tip of a pencil that keeps drawing the plant '
                           'longer.')],
             [('texte_a_trous', 1,
               {'text': 'The terminal bud produces young leaves and {{1}}.', 'blanks': 1},
               {'values': ['branches']}, 'Young leaves and branches.'),
              ('qcm', 1, {'question': 'Another name for the terminal bud is the…',
                          'options': ['apical bud', 'root cap', 'leaf blade']},
               {'index': 0}, 'The apical bud.'),
              ('qcm', 2, {'question': 'Where is the terminal bud found?',
                          'options': ['at the tip of the stem', 'under the soil',
                                      'inside the fruit']},
               {'index': 0}, 'At the tip of the stem.'),
              ('texte_a_trous', 3,
               {'text': 'The bud at the tip of the plant is also called the {{1}} bud.',
                'blanks': 1},
               {'values': ['apical']}, 'The apical bud.'),
              ('vrai_faux', 4, {'statement': 'The terminal bud is where the plant grows '
                                             'longer.'},
               {'value': True}, 'Yes, it makes the new leaves and branches.')]),

            ('relation',
             'Green leaves contain a pigment called chlorophyll which traps sunlight. The food '
             'is prepared in the leaves, and excess water leaves through the stomata.',
             'br-pt-feuille',
             'Le schéma, la feuille mise en avant.',
             [('simple', 'The leaf does two things: it makes the food, and it lets out the '
                         'water the plant does not need.'),
              ('pas_a_pas', 'Chlorophyll catches the light, the leaf makes the food, and the '
                            'stomata let the extra water out.')],
             # Son epreuve : il avait repondu « leaves » a la question du pigment.
             [('texte_a_trous', 1,
               {'text': 'The green pigment that traps sunlight is called {{1}}.', 'blanks': 1},
               {'values': ['chlorophyll']}, 'Chlorophyll.'),
              ('texte_a_trous', 1,
               {'text': 'Plants send out excess water in a process called {{1}}.',
                'blanks': 1},
               {'values': ['transpiration']}, 'Transpiration.'),
              ('qcm', 2, {'question': 'Tiny holes on the surface of a leaf are called…',
                          'options': ['stomata', 'nodules', 'buds']},
               {'index': 0}, 'Stomata.'),
              ('texte_a_trous', 3,
               {'text': 'The food of the whole plant is prepared in the {{1}}.', 'blanks': 1},
               {'values': ['leaves']}, 'In the leaves.'),
              ('qcm', 4, {'question': 'The green pigment in green leaves is called…',
                          'options': ['chlorophyll', 'leaves', 'stomata']},
               {'index': 0}, 'Chlorophyll. The leaf is the part; chlorophyll is what is in it.')]),

            ('relation',
             'Flowers grow to produce the fruits. Fruits grow to produce seeds and serve as '
             'food.',
             'br-pt-fleur',
             'Le schéma, la fleur mise en avant.',
             [('simple', 'The flower comes first, the fruit comes from it, and the seed is '
                         'inside the fruit.'),
              ('visuel', 'On the diagram the flower and the fruit sit on the same branch, one '
                         'on each side.')],
             [('texte_a_trous', 1,
               {'text': 'Flowers grow to produce the {{1}}.', 'blanks': 1},
               {'values': ['fruits']}, 'The fruits.'),
              ('qcm', 1, {'question': 'What do fruits produce?',
                          'options': ['seeds', 'roots', 'branches']},
               {'index': 0}, 'Seeds.'),
              ('chronologie', 2, {'question': 'Put the three stages in order.',
                                  'tokens': ['flower', 'fruit', 'seed']},
               {'order': [0, 1, 2]}, 'Flower, then fruit, then seed.'),
              ('texte_a_trous', 3,
               {'text': 'Fruits produce seeds and also serve as {{1}}.', 'blanks': 1},
               {'values': ['food']}, 'As food.'),
              ('vrai_faux', 4, {'statement': 'The fruit comes before the flower.'},
               {'value': False}, 'No. The flower comes first and becomes the fruit.')]),

            ('relation',
             'Branches hold the fruits, flowers and leaves into the air, and transport food '
             'from the leaves to the other parts. The stem holds the branches.',
             'br-pt-tige',
             'Le schéma, la tige mise en avant.',
             [('simple', 'The branch carries and transports. The stem only holds.'),
              ('analogie', 'The stem is the trunk of the house; the branches are the shelves '
                           'fixed to it.')],
             [('texte_a_trous', 1,
               {'text': 'The {{1}} holds the branches of the plant.', 'blanks': 1},
               {'values': ['stem']}, 'The stem.'),
              ('qcm', 1, {'question': 'What do branches hold into the air?',
                          'options': ['fruits, flowers and leaves', 'the roots only',
                                      'the soil']},
               {'index': 0}, 'The fruits, flowers and leaves.'),
              ('qcm', 2, {'question': 'What do branches transport?',
                          'options': ['food from the leaves', 'water from the clouds',
                                      'soil from the ground']},
               {'index': 0}, 'Food, from the leaves to the other parts.'),
              ('texte_a_trous', 3,
               {'text': 'Branches transport food from the {{1}} to the other parts.',
                'blanks': 1},
               {'values': ['leaves']}, 'From the leaves.'),
              ('vrai_faux', 4, {'statement': 'The stem and the branches do exactly the same '
                                             'work.'},
               {'value': False}, 'No. The branches also transport the food.')]),

            ('relation',
             'Roots act as the legs of the plant. They hold it firm to the soil and absorb '
             'water and minerals through a process called osmosis.',
             'br-pt-racine',
             'Les racines dans la terre, avec les flèches de l-eau qui monte.',
             [('simple', 'Roots do three things: they hold, they absorb, and some of them '
                         'store food.'),
              ('pas_a_pas', 'Pull a weed and you feel the holding. Water a dry plant and you '
                            'see the absorbing.')],
             [('texte_a_trous', 1,
               {'text': 'Water and minerals enter the plant through a process called {{1}}.',
                'blanks': 1},
               {'values': ['osmosis']}, 'Osmosis.'),
              ('qcm', 1, {'question': 'What do the roots absorb from the soil?',
                          'options': ['water and minerals', 'sunlight', 'carbon dioxide']},
               {'index': 0}, 'Water and minerals.'),
              ('qcm', 2, {'question': 'Roots are compared to which part of a body?',
                          'options': ['the legs', 'the eyes', 'the hands']},
               {'index': 0}, 'The legs, because they hold the plant up.'),
              ('texte_a_trous', 3,
               {'text': 'Some roots also help to {{1}} excess food for the plant.',
                'blanks': 1},
               {'values': ['store']}, 'To store it.'),
              ('vrai_faux', 4, {'statement': 'The roots only hold the plant, they absorb '
                                             'nothing.'},
               {'value': False}, 'No. They absorb water and minerals too.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, cles_items, total, notions_vues = set(), set(), 0, 0
    trous = 0
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

    # La forme de l-épreuve doit se retrouver dans les leçons : si le texte
    # à trous cessait de dominer, on entraînerait BRAYNE à autre chose que
    # ce qu-on lui demandera.
    assert trous >= total * 0.35, \
        'le texte à trous ne domine plus : %d sur %d questions' % (trous, total)

    # Et les neuf fautes relevées sur sa copie doivent être travaillées.
    tout = json.dumps(LECONS, ensure_ascii=False, default=str)
    for mot in ('chlorophyll', 'incinerator', 'photosynthesis', 'recycling', 'biogas',
                'nodules', 'annual', 'inorganic', 'carbon dioxide'):
        assert mot in tout, 'la faute sur « %s » nest pas travaillée' % mot

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-brayne-env-nov.py'))
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
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-env-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous (%.0f%%) - %d images'
          % (len(LECONS), notions, items, trous, 100.0 * trous / items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-42s %-16s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
