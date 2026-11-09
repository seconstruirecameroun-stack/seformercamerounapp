# -*- coding: utf-8 -*-
"""
Onze leçons pour la révision de BRAYNE (CM1) — onze photos de tableau
envoyées par le père le 9 novembre 2026, à 16 h 25.

CE QUE PORTENT LES TABLEAUX. Deux épreuves distinctes, photographiées dans
deux salles : une révision de SCIENCES ET TECHNOLOGIE en français, en cinq
parties, et un REVIEW EXERCISE d-anglais en six parties plus un texte
lacunaire sur le paludisme.

CE QUI ÉTAIT DÉJÀ EN BASE, et n-est donc pas refait. La révision de
sciences porte sur neuf points, et sept ont déjà leur leçon :

  la puberté, le tableau fille / garçon      leçon 9
  l-appareil reproducteur à annoter          leçon 10
  le cycle de l-eau et son texte à trous     leçon 11
  rendre une eau potable                     leçon 12
  le compost                                 leçon 13
  la lampe à pétrole, schéma et précautions  leçon 14
  les points d-eau et leur entretien         leçon 33
  les roches et leurs trois types            leçon 32
  le mode de déplacement des animaux         leçon 34

DEUX TROUS, et ce sont les deux leçons de sciences écrites ici :

  les TYPES DE SOLS (partie IV, questions c et d) : la leçon 32 porte les
  roches, pas les sols. Rien en base ne dit ce qu-est un sol argileux.

  les modes de NUTRITION et de REPRODUCTION des animaux (partie I,
  question 4) : la leçon 34 ne porte que le déplacement, et le tableau du
  tableau noir demande les trois colonnes.

L-ANGLAIS, LUI, N-EXISTAIT PAS DU TOUT. BRAYNE n-a aucune matière
« Anglais » : ses leçons en anglais sont des leçons de sciences. Les
trente numéros du Review exercise - adjectifs, comparatifs, relatifs,
possessifs, réfléchis, démonstratifs, articles, contraires, synonymes - et
le texte sur le paludisme n-avaient donc rien. Neuf leçons les portent.

DEUX RÉSERVES SUR LE TABLEAU, à dire au père plutôt qu-à recopier.

« sols visqueux » figure dans la liste à entourer de la partie IV. Ce
n-est pas un type de sol : c-est l-intrus de l-exercice. Il est gardé ici
comme intrus, jamais comme réponse.

La VIPÈRE est demandée dans la colonne « mode de reproduction ». Elle ne
pond pas d-œufs : ses petits naissent vivants, elle est ovovivipare. La
leçon le dit ainsi, et l-explication donne le mot exact. Si la maîtresse
attend « ovipare », c-est le tableau qui se trompe, et le père doit le
savoir avant l-épreuve.

Usage :  python work/lecons-brayne-revision-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-revision-nov.py. ')

CLASSE = 'CM1'
ENFANT = 'BRAYNE'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

SCIENCES = 'Sciences'
ANGLAIS = 'Anglais'
GRAMMAIRE = 'Grammar and vocabulary'

TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

# (titre, matière, chapitre, langue, rang, résumé, image, prompt, notions)
LECONS = [
    # ------------------------------------------------------------------ 68
    (
        'Les types de sols', SCIENCES, 'Sciences de la Terre', 'fr', 68,
        'Le sol est la partie superficielle de la terre, composée de roches de plusieurs sortes. '
        'Le sol argileux est fait d’argile, le sol sablonneux de sable, le sol humifère est riche '
        'en humus, le sol calcaire est fait de calcaire. Il y a aussi le sol rocailleux et le sol '
        'marécageux.',
        'br-so-couv',
        'Quatre cartes alignées : argileux, sablonneux, humifère, calcaire.',
        [
            ('definition',
             'Le sol est la partie superficielle de la terre. Il est composé de roches de '
             'plusieurs sortes, et c’est là que poussent les plantes.',
             'br-so-def',
             'Trois lignes : la partie superficielle, les roches, les plantes.',
             [('simple', 'C’est la couche du dessus, celle qu’on creuse et dans laquelle on '
                         'sème.'),
              ('visuel', 'Sous le sol, il y a encore de la roche, mais ce n’est plus du sol.')],
             [('qcm', 1, {'question': 'Qu’est-ce que le sol ?',
                          'options': ['La partie superficielle de la terre',
                                      'Le centre de la Terre', 'Une sorte de plante']},
               {'index': 0}, 'La couche du dessus, où poussent les plantes.'),
              ('vrai_faux', 1, {'statement': 'Le sol est composé de roches de plusieurs sortes.'},
               {'value': True}, 'Oui, et c’est ce qui fait les différents types de sols.'),
              ('texte_a_trous', 2,
               {'text': 'Le sol est la partie {{1}} de la terre.', 'blanks': 1},
               {'values': ['superficielle']}, 'La partie superficielle.'),
              ('qcm', 3, {'question': 'Pourquoi le sol est-il important ?',
                          'options': ['C’est là que poussent les plantes',
                                      'Il éclaire la nuit', 'Il fait tomber la pluie']},
               {'index': 0}, 'Les plantes y poussent.'),
              ('vrai_faux', 4, {'statement': 'Tous les sols sont faits de la même chose.'},
               {'value': False}, 'Non. Chaque type de sol a sa composition.')]),

            ('definition',
             'Le sol argileux est fait d’argile. Il colle entre les doigts et retient l’eau.',
             'br-so-argileux',
             'Un profil de sol brun-rouge, avec de grosses mottes d’argile.',
             [('simple', 'Mouillé, il devient pâteux ; sec, il durcit et se fendille.'),
              ('analogie', 'C’est la terre dont on fait les poteries et les briques.')],
             [('qcm', 1, {'question': 'De quoi est fait le sol argileux ?',
                          'options': ['D’argile', 'De sable', 'D’humus']},
               {'index': 0}, 'D’argile.'),
              ('vrai_faux', 1, {'statement': 'Le sol argileux retient l’eau.'},
               {'value': True}, 'Oui, l’eau ne le traverse pas.'),
              ('texte_a_trous', 2,
               {'text': 'Le sol argileux est fait d’{{1}}.', 'blanks': 1},
               {'values': ['argile']}, 'D’argile.'),
              ('qcm', 3, {'question': 'Avec quel sol fabrique-t-on les briques ?',
                          'options': ['Le sol argileux', 'Le sol sablonneux',
                                      'Le sol calcaire']},
               {'index': 0}, 'Le sol argileux : l’argile se façonne.'),
              ('vrai_faux', 4, {'statement': 'L’eau traverse très vite le sol argileux.'},
               {'value': False}, 'Non, il la retient. C’est le sol sablonneux qu’elle traverse.')]),

            ('definition',
             'Le sol sablonneux est fait de sable. L’eau le traverse vite, et il retient peu.',
             'br-so-sablonneux',
             'Un profil de sol clair, couvert de petits grains de sable.',
             [('simple', 'Il coule entre les doigts et ne colle pas.'),
              ('visuel', 'Verse de l’eau dessus : elle disparaît aussitôt.')],
             [('qcm', 1, {'question': 'De quoi est fait le sol sablonneux ?',
                          'options': ['De sable', 'D’argile', 'De calcaire']},
               {'index': 0}, 'De sable.'),
              ('vrai_faux', 1, {'statement': 'L’eau traverse vite le sol sablonneux.'},
               {'value': True}, 'Oui, il la retient très peu.'),
              ('texte_a_trous', 2,
               {'text': 'Le sol sablonneux est fait de {{1}}.', 'blanks': 1},
               {'values': ['sable']}, 'De sable.'),
              ('qcm', 3, {'question': 'Quel sol retient le moins l’eau ?',
                          'options': ['Le sol sablonneux', 'Le sol argileux',
                                      'Le sol marécageux']},
               {'index': 0}, 'Le sol sablonneux : l’eau le traverse.'),
              ('vrai_faux', 4, {'statement': 'Le sol sablonneux colle entre les doigts.'},
               {'value': False}, 'Non, il coule. C’est le sol argileux qui colle.')]),

            ('definition',
             'Le sol humifère est riche en humus, c’est-à-dire en débris de plantes et d’animaux '
             'décomposés. C’est le plus fertile.',
             'br-so-humifere',
             'Un profil de sol très sombre, avec des débris de feuilles.',
             [('simple', 'Il est noir et sent la forêt. C’est celui où les plantes poussent le '
                         'mieux.'),
              ('pas_a_pas', 'Les feuilles tombent, pourrissent, et deviennent de l’humus. C’est '
                            'ce que fait aussi le compost.')],
             [('qcm', 1, {'question': 'De quoi le sol humifère est-il riche ?',
                          'options': ['D’humus', 'De sable', 'De cailloux']},
               {'index': 0}, 'D’humus.'),
              ('vrai_faux', 1, {'statement': 'Le sol humifère est le plus fertile.'},
               {'value': True}, 'Oui, c’est là que les plantes poussent le mieux.'),
              ('texte_a_trous', 2,
               {'text': 'Le sol humifère est riche en {{1}}.', 'blanks': 1},
               {'values': ['humus']}, 'En humus.'),
              ('qcm', 3, {'question': 'Qu’est-ce que l’humus ?',
                          'options': ['Des débris de plantes décomposés',
                                      'Une sorte de caillou', 'De l’eau sale']},
               {'index': 0}, 'Des débris de plantes et d’animaux décomposés.'),
              ('vrai_faux', 4,
               {'statement': 'Le compost sert justement à fabriquer de l’humus.'},
               {'value': True}, 'Oui, c’est le même travail de décomposition.')]),

            ('definition',
             'Le sol calcaire est fait de calcaire. Il est clair, sec, et peu fertile.',
             'br-so-calcaire',
             'Un profil de sol très clair, avec des éclats de calcaire.',
             [('simple', 'Le calcaire est une roche blanche. Le sol qu’il forme est pâle.'),
              ('visuel', 'La craie du tableau est du calcaire.')],
             [('qcm', 1, {'question': 'De quoi est fait le sol calcaire ?',
                          'options': ['De calcaire', 'D’argile', 'D’humus']},
               {'index': 0}, 'De calcaire.'),
              ('vrai_faux', 1, {'statement': 'Le sol calcaire est clair et sec.'},
               {'value': True}, 'Oui, et peu fertile.'),
              ('texte_a_trous', 2,
               {'text': 'Le sol calcaire est fait de {{1}}.', 'blanks': 1},
               {'values': ['calcaire']}, 'De calcaire.'),
              ('qcm', 3, {'question': 'Quelle matière connue est du calcaire ?',
                          'options': ['La craie', 'Le fer', 'Le plastique']},
               {'index': 0}, 'La craie du tableau.'),
              ('vrai_faux', 4, {'statement': 'Le sol calcaire est le plus fertile de tous.'},
               {'value': False}, 'Non. Le plus fertile est le sol humifère.')]),

            ('liste',
             'Le sol rocailleux est plein de cailloux, et le sol marécageux est gorgé d’eau. En '
             'revanche, le sol visqueux n’existe pas.',
             'br-so-autres',
             'Trois paires reliées : rocailleux, marécageux, humifère et ce qui les remplit.',
             [('simple', 'Un sol rocailleux se laboure mal : la houe tape sur les pierres.'),
              ('visuel', 'Un sol marécageux garde l’eau à la surface : on y enfonce.')],
             [('qcm', 1, {'question': 'De quoi est plein le sol rocailleux ?',
                          'options': ['De cailloux', 'D’eau', 'De sable']},
               {'index': 0}, 'De cailloux.'),
              ('vrai_faux', 1, {'statement': 'Le sol marécageux est gorgé d’eau.'},
               {'value': True}, 'Oui, on y enfonce.'),
              ('texte_a_trous', 2,
               {'text': 'Le sol marécageux est gorgé d’{{1}}.', 'blanks': 1},
               {'values': ['eau']}, 'D’eau.'),
              ('qcm', 3, {'question': 'Lequel n’est pas un type de sol ?',
                          'options': ['Le sol visqueux', 'Le sol rocailleux',
                                      'Le sol marécageux']},
               {'index': 0}, 'Le sol visqueux n’existe pas : c’est l’intrus de la liste.'),
              ('vrai_faux', 4, {'statement': 'Le sol visqueux est un type de sol.'},
               {'value': False}, 'Non. Méfie-toi de celui-là dans la liste à entourer.')]),
        ],
    ),

    # ------------------------------------------------------------------ 69
    (
        'La nutrition et la reproduction des animaux', SCIENCES, 'Science de la Vie', 'fr', 69,
        'Le mode de nutrition dit ce que l’animal mange : herbivore, carnivore, omnivore ou '
        'granivore. Le mode de reproduction dit comment naissent ses petits : ovipare s’il pond '
        'des œufs, vivipare si les petits naissent vivants.',
        'br-an-couv',
        'Quatre cartes alignées : herbivore, carnivore, omnivore, granivore.',
        [
            ('definition',
             'Le mode de nutrition dit ce que l’animal mange : herbivore, carnivore, omnivore ou '
             'granivore.',
             'br-an-nutrition',
             'Quatre paires reliées : herbivore et des plantes, carnivore et de la viande.',
             [('simple', 'Herbivore : des plantes. Carnivore : de la viande. Omnivore : de tout. '
                         'Granivore : des graines.'),
              ('visuel', 'Le mot dit déjà ce qu’il mange : « herbi » pour l’herbe, « carni » '
                         'pour la chair, « grani » pour la graine.')],
             [('qcm', 1, {'question': 'Que mange un herbivore ?',
                          'options': ['Des plantes', 'De la viande', 'Des graines']},
               {'index': 0}, 'Des plantes.'),
              ('vrai_faux', 1, {'statement': 'Un omnivore mange de tout.'},
               {'value': True}, 'Oui, des plantes et de la viande.'),
              ('association', 2, {'question': 'Relie chaque mot à ce que l’animal mange.',
                                  'gauche': ['herbivore', 'carnivore', 'granivore'],
                                  'droite': ['des plantes', 'de la viande', 'des graines']},
               {'order': [0, 1, 2]}, 'Herbe, chair, graine : le mot le dit.'),
              ('texte_a_trous', 3,
               {'text': 'Un animal qui ne mange que des graines est {{1}}.', 'blanks': 1},
               {'values': ['granivore']}, 'Granivore.'),
              ('vrai_faux', 4, {'statement': 'Un carnivore mange surtout de l’herbe.'},
               {'value': False}, 'Non, il mange de la viande.')]),

            ('definition',
             'Le mode de reproduction dit comment naissent les petits : l’animal est ovipare s’il '
             'pond des œufs, et vivipare si ses petits naissent vivants.',
             'br-an-reproduction',
             'Deux paires reliées : ovipare et pond des œufs, vivipare et des petits vivants.',
             [('simple', 'La poule pond : elle est ovipare. La chèvre met bas : elle est '
                         'vivipare.'),
              ('visuel', '« Ovi » veut dire œuf, et « vivi » veut dire vivant.')],
             [('qcm', 1, {'question': 'Que fait un animal ovipare ?',
                          'options': ['Il pond des œufs', 'Il met au monde des petits vivants',
                                      'Il ne se reproduit pas']},
               {'index': 0}, 'Il pond des œufs.'),
              ('vrai_faux', 1, {'statement': 'Un animal vivipare met au monde des petits vivants.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Un animal qui pond des œufs est {{1}}.', 'blanks': 1},
               {'values': ['ovipare']}, 'Ovipare.'),
              ('qcm', 3, {'question': 'La vache met au monde un veau vivant. Elle est…',
                          'options': ['vivipare', 'ovipare', 'granivore']},
               {'index': 0}, 'Vivipare.'),
              ('vrai_faux', 4, {'statement': 'La poule est un animal vivipare.'},
               {'value': False}, 'Non, elle pond des œufs : elle est ovipare.')]),

            ('relation',
             'Le pigeon vole, il est granivore, et il est ovipare.',
             'br-an-pigeon',
             'Trois lignes : il vole, il est granivore, il est ovipare.',
             [('simple', 'Trois colonnes du tableau, trois réponses pour le pigeon.'),
              ('pas_a_pas', 'Demande-toi d’abord comment il se déplace, puis ce qu’il mange, '
                            'puis comment naissent ses petits.')],
             [('qcm', 1, {'question': 'Comment se déplace le pigeon ?',
                          'options': ['Il vole', 'Il rampe', 'Il nage']},
               {'index': 0}, 'Il vole.'),
              ('vrai_faux', 1, {'statement': 'Le pigeon est granivore.'},
               {'value': True}, 'Oui, il mange des graines.'),
              ('texte_a_trous', 2,
               {'text': 'Le pigeon pond des œufs : il est {{1}}.', 'blanks': 1},
               {'values': ['ovipare']}, 'Ovipare.'),
              ('qcm', 3, {'question': 'Que mange le pigeon ?',
                          'options': ['Des graines', 'De la viande', 'De l’herbe']},
               {'index': 0}, 'Des graines : il est granivore.'),
              ('vrai_faux', 4, {'statement': 'Le pigeon est vivipare.'},
               {'value': False}, 'Non, il pond des œufs.')]),

            ('relation',
             'La vache marche et broute : elle est herbivore. Le porc marche et mange de tout : '
             'il est omnivore. Tous les deux sont vivipares.',
             'br-an-vache',
             'Trois paires : la vache et herbivore, le porc et omnivore, tous deux vivipares.',
             [('simple', 'Deux animaux qui marchent, deux régimes différents, un même mode de '
                         'reproduction.'),
              ('visuel', 'Le veau et le porcelet naissent vivants : pas d’œuf chez eux.')],
             [('qcm', 1, {'question': 'Que mange la vache ?',
                          'options': ['De l’herbe', 'De la viande', 'Des graines seulement']},
               {'index': 0}, 'De l’herbe : elle est herbivore.'),
              ('vrai_faux', 1, {'statement': 'Le porc est omnivore.'},
               {'value': True}, 'Oui, il mange de tout.'),
              ('texte_a_trous', 2,
               {'text': 'La vache et le porc sont tous les deux {{1}}.', 'blanks': 1},
               {'values': ['vivipares']}, 'Vivipares.'),
              ('qcm', 3, {'question': 'Comment se déplacent la vache et le porc ?',
                          'options': ['Ils marchent', 'Ils volent', 'Ils rampent']},
               {'index': 0}, 'Ils marchent.'),
              ('vrai_faux', 4, {'statement': 'La vache pond des œufs.'},
               {'value': False}, 'Non, le veau naît vivant.')]),

            ('relation',
             'Le maquereau nage et la vipère rampe ; tous deux sont carnivores. Le maquereau pond '
             'des œufs, tandis que les petits de la vipère naissent vivants.',
             'br-an-maquereau',
             'Deux paires : le maquereau nage et pond, la vipère rampe et met bas.',
             [('simple', 'Le maquereau est un poisson : il pond des œufs dans l’eau.'),
              ('pas_a_pas', 'La vipère garde ses œufs dans son ventre, et ses petits en sortent '
                            'vivants. Le mot exact est ovovivipare. Beaucoup d’autres serpents, '
                            'eux, pondent bien des œufs.')],
             [('qcm', 1, {'question': 'Comment se déplace le maquereau ?',
                          'options': ['Il nage', 'Il vole', 'Il marche']},
               {'index': 0}, 'Il nage : c’est un poisson.'),
              ('vrai_faux', 1, {'statement': 'Le maquereau et la vipère sont carnivores.'},
               {'value': True}, 'Oui, tous les deux.'),
              ('texte_a_trous', 2,
               {'text': 'Le maquereau pond des œufs : il est {{1}}.', 'blanks': 1},
               {'values': ['ovipare']}, 'Ovipare.'),
              ('qcm', 3, {'question': 'Comment naissent les petits de la vipère ?',
                          'options': ['Ils naissent vivants', 'Ils sortent d’un œuf pondu',
                                      'Ils naissent dans l’eau']},
               {'index': 0}, 'Vivants : la vipère est ovovivipare.'),
              ('vrai_faux', 4, {'statement': 'La vipère se déplace en rampant.'},
               {'value': True}, 'Oui, elle n’a pas de pattes.')]),
        ],
    ),

    # ------------------------------------------------------------------ 70
    (
        'Adjectives', ANGLAIS, GRAMMAIRE, 'en', 70,
        'An adjective describes a noun: it says what the noun is like. It is usually written just '
        'before the noun. In that old woman, old is the adjective and woman is the noun.',
        'be-ad-couv',
        'Le groupe « that old woman » écrit en grand dans son cadre.',
        [
            ('definition',
             'An adjective describes a noun: it says what the noun is like.',
             'be-ad-def',
             'La phrase « That fat man is living in a white house », fat et white en doré.',
             [('simple', 'Ask yourself: what is the noun like? The answer is the adjective.'),
              ('visuel', 'In a white house, white tells you what the house is like.')],
             [('qcm', 1, {'question': 'What does an adjective do?',
                          'options': ['It describes a noun', 'It replaces a noun',
                                      'It counts the nouns']},
               {'index': 0}, 'It says what the noun is like.'),
              ('vrai_faux', 1, {'statement': 'In a white house, white is an adjective.'},
               {'value': True}, 'Yes: it describes the house.'),
              ('texte_a_trous', 2,
               {'text': 'An adjective describes a {{1}}.', 'blanks': 1},
               {'values': ['noun']}, 'A noun.'),
              ('qcm', 3, {'question': 'In That fat man, which word is the adjective?',
                          'options': ['fat', 'man', 'that']},
               {'index': 0}, 'fat describes the man.'),
              ('vrai_faux', 4, {'statement': 'An adjective describes a verb.'},
               {'value': False}, 'No. It describes a noun.')]),

            ('relation',
             'An adjective is usually written just before the noun it describes: this yellow bag, '
             'that old woman.',
             'be-ad-place',
             'La phrase « Please give this yellow bag to that old woman », yellow et old en doré.',
             [('simple', 'Look just in front of the noun: the adjective is nearly always there.'),
              ('pas_a_pas', 'Find the noun first. Then read the word before it.')],
             [('qcm', 1, {'question': 'Where is the adjective usually written?',
                          'options': ['Just before the noun', 'At the end of the sentence',
                                      'Before the verb']},
               {'index': 0}, 'Just before the noun.'),
              ('vrai_faux', 1, {'statement': 'In this yellow bag, yellow comes before bag.'},
               {'value': True}, 'Yes, and bag is the noun.'),
              ('texte_a_trous', 2,
               {'text': 'An adjective is usually written just {{1}} the noun.', 'blanks': 1},
               {'values': ['before']}, 'Before the noun.'),
              ('qcm', 3, {'question': 'In that old woman, which word is the noun?',
                          'options': ['woman', 'old', 'that']},
               {'index': 0}, 'woman, and old describes it.'),
              ('vrai_faux', 4,
               {'statement': 'In this yellow bag, the adjective comes after the noun.'},
               {'value': False}, 'No, it comes before it.')]),

            ('relation',
             'To find the adjective in a sentence, look for the word that tells you what a noun '
             'is like.',
             'be-ad-trouver',
             'La phrase « Many people say that slow water runs deep », many et slow en doré.',
             [('simple', 'Slow water: slow says what the water is like, so slow is the '
                         'adjective.'),
              ('pas_a_pas', 'Underline the nouns. Then look at the word in front of each one.')],
             [('qcm', 1, {'question': 'In slow water, which word is the adjective?',
                          'options': ['slow', 'water', 'runs']},
               {'index': 0}, 'slow tells you what the water is like.'),
              ('vrai_faux', 1, {'statement': 'In Many people, many is an adjective.'},
               {'value': True}, 'Yes: it tells you how many people.'),
              ('texte_a_trous', 2,
               {'text': 'The adjective tells you what the noun is {{1}}.', 'blanks': 1},
               {'values': ['like']}, 'What the noun is like.'),
              ('qcm', 3, {'question': 'In a big black dog, how many adjectives are there?',
                          'options': ['Two', 'One', 'Three']},
               {'index': 0}, 'big and black: two adjectives.'),
              ('vrai_faux', 4, {'statement': 'A noun can have two adjectives before it.'},
               {'value': True}, 'Yes: a big black dog.')]),

            ('liste',
             'fat, white, yellow, old, slow and many are adjectives: each one describes a noun.',
             'be-ad-plusieurs',
             'La liste des adjectifs du tableau, posée ligne à ligne.',
             [('simple', 'These are the very words of the exercise. Learn them as adjectives.'),
              ('visuel', 'Colours, sizes and ages are nearly always adjectives.')],
             [('qcm', 1, {'question': 'Which one of these words is an adjective?',
                          'options': ['yellow', 'woman', 'give']},
               {'index': 0}, 'yellow describes a noun.'),
              ('vrai_faux', 1, {'statement': 'The word old is an adjective.'},
               {'value': True}, 'Yes.'),
              ('qcm', 2, {'question': 'Which one is not an adjective?',
                          'options': ['house', 'white', 'slow']},
               {'index': 0}, 'house is a noun.'),
              ('texte_a_trous', 3,
               {'text': 'Colours such as white and yellow are {{1}}.', 'blanks': 1},
               {'values': ['adjectives']}, 'Adjectives.'),
              ('vrai_faux', 4, {'statement': 'The word many is an adjective here.'},
               {'value': True}, 'Yes: many people.')]),
        ],
    ),

    # ------------------------------------------------------------------ 71
    (
        'Comparing with adjectives', ANGLAIS, GRAMMAIRE, 'en', 71,
        'Short adjectives take -er to compare two things: tall becomes taller. Long adjectives '
        'take more or most: the most populated country. And three words are irregular: good '
        'becomes better and best, bad becomes worse and worst. When two things are compared, than '
        'follows.',
        'be-cm-couv',
        'Le groupe « better than French » écrit en grand dans son cadre.',
        [
            ('relation',
             'Short adjectives take -er to compare two things: tall becomes taller, old becomes '
             'older.',
             'be-cm-er',
             'Trois exemples : tall et taller, old et older, fast et faster.',
             [('simple', 'One short word, one ending: taller, older, faster.'),
              ('pas_a_pas', 'Count the syllables. One or two: add -er.')],
             [('qcm', 1, {'question': 'What does a short adjective take to compare?',
                          'options': ['The ending -er', 'The word more',
                                      'Nothing at all']},
               {'index': 0}, 'The ending -er.'),
              ('vrai_faux', 1, {'statement': 'The word tall becomes taller.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'A short adjective takes the ending {{1}} to compare.', 'blanks': 1},
               {'values': ['er']}, 'The ending -er.'),
              ('qcm', 3, {'question': 'What does fast become?',
                          'options': ['faster', 'more fast', 'fastly']},
               {'index': 0}, 'faster.'),
              ('vrai_faux', 4, {'statement': 'A short adjective takes more to compare.'},
               {'value': False}, 'No, it takes -er.')]),

            ('relation',
             'Long adjectives take more or most instead of an ending: the most populated country '
             'in Africa.',
             'be-cm-more',
             'La phrase « Nigeria is the most populated country in Africa », most en doré.',
             [('simple', 'Populated is long, so you say more populated, the most populated.'),
              ('visuel', 'You never say populateder. It would not even be sayable.')],
             [('qcm', 1, {'question': 'What do long adjectives take?',
                          'options': ['more or most', 'the ending -er',
                                      'the ending -est']},
               {'index': 0}, 'more or most.'),
              ('vrai_faux', 1,
               {'statement': 'You say the most populated country, not the populatedest.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Long adjectives take more or {{1}}.', 'blanks': 1},
               {'values': ['most']}, 'more or most.'),
              ('qcm', 3, {'question': 'How do you compare beautiful?',
                          'options': ['more beautiful', 'beautifuller', 'beautifulest']},
               {'index': 0}, 'more beautiful.'),
              ('vrai_faux', 4, {'statement': 'A long adjective takes the ending -er.'},
               {'value': False}, 'No, it takes more or most.')]),

            ('relation',
             'Three words are irregular: good becomes better and best, and bad becomes worse and '
             'worst. They never take -er.',
             'be-cm-good',
             'Trois lignes : good devient better et best, bad devient worse et worst.',
             [('simple', 'These ones are learnt by heart. There is no rule to apply.'),
              ('visuel', 'gooder does not exist, and neither does badder.')],
             [('qcm', 1, {'question': 'What does good become?',
                          'options': ['better', 'gooder', 'more good']},
               {'index': 0}, 'better.'),
              ('vrai_faux', 1, {'statement': 'The word bad becomes worse.'},
               {'value': True}, 'Yes, and then worst.'),
              ('texte_a_trous', 2,
               {'text': 'The word good becomes {{1}}.', 'blanks': 1},
               {'values': ['better']}, 'better.'),
              ('qcm', 3, {'question': 'Our teacher speaks English … than French.',
                          'options': ['better', 'gooder', 'more good']},
               {'index': 0}, 'better than French.'),
              ('vrai_faux', 4, {'statement': 'The word good becomes gooder.'},
               {'value': False}, 'No: better.')]),

            ('relation',
             'When two things are compared, the word than follows the adjective: better than '
             'French, taller than me.',
             'be-cm-than',
             'La phrase « Our teacher speaks English better than French », better than en doré.',
             [('simple', 'Two things compared, and than between them.'),
              ('pas_a_pas', 'Write the compared adjective, then than, then the second thing.')],
             [('qcm', 1, {'question': 'Which word follows a compared adjective?',
                          'options': ['than', 'that', 'then']},
               {'index': 0}, 'than.'),
              ('vrai_faux', 1, {'statement': 'You say better than French.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Two things compared are joined by the word {{1}}.', 'blanks': 1},
               {'values': ['than']}, 'than.'),
              ('qcm', 3, {'question': 'He scored … marks in English than in French.',
                          'options': ['better', 'best', 'good']},
               {'index': 0}, 'better … than.'),
              ('vrai_faux', 4, {'statement': 'You say better then French.'},
               {'value': False}, 'No: than, with an a.')]),
        ],
    ),

    # ------------------------------------------------------------------ 72
    (
        'Relative pronouns', ANGLAIS, GRAMMAIRE, 'en', 72,
        'who is for a person who does the action; whom comes after a preposition; whose says who '
        'owns something; and which chooses inside a group that is already known.',
        'be-re-couv',
        'Quatre cartes alignées : who, whom, whose, which.',
        [
            ('definition',
             'who stands for a person who does the action: this is the girl who came here.',
             'be-re-who',
             'La phrase « This is the girl who came here », who en doré.',
             [('simple', 'The girl came. She does the action, so who.'),
              ('pas_a_pas', 'Ask who does the verb. If it is the person, write who.')],
             [('qcm', 1, {'question': 'When do you use who?',
                          'options': ['For a person who does the action',
                                      'For a thing', 'After a preposition']},
               {'index': 0}, 'For a person who does the action.'),
              ('vrai_faux', 1, {'statement': 'You say the girl who came here.'},
               {'value': True}, 'Yes: she does the action.'),
              ('texte_a_trous', 2,
               {'text': 'This is the girl {{1}} came here.', 'blanks': 1},
               {'values': ['who']}, 'who.'),
              ('qcm', 3, {'question': 'This is the man … helped us.',
                          'options': ['who', 'whose', 'which']},
               {'index': 0}, 'who: he does the action.'),
              ('vrai_faux', 4, {'statement': 'who is used for things, not for people.'},
               {'value': False}, 'No, who is for people.')]),

            ('definition',
             'whom comes after a preposition: the man with whom I travelled.',
             'be-re-whom',
             'La phrase « The man with whom I travelled is a soldier », whom en doré.',
             [('simple', 'with whom, to whom, for whom. There is always a small word in front.'),
              ('visuel', 'If you can see with, to or for just before, write whom.')],
             [('qcm', 1, {'question': 'What comes just before whom?',
                          'options': ['A preposition', 'A noun of a person',
                                      'A verb of action']},
               {'index': 0}, 'A preposition: with, to, for.'),
              ('vrai_faux', 1, {'statement': 'You say the man with whom I travelled.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The man with {{1}} I travelled is a soldier.', 'blanks': 1},
               {'values': ['whom']}, 'whom.'),
              ('qcm', 3, {'question': 'The friend to … I wrote is ill.',
                          'options': ['whom', 'who', 'whose']},
               {'index': 0}, 'After to, you write whom.'),
              ('vrai_faux', 4, {'statement': 'You say the man with who I travelled.'},
               {'value': False}, 'No: with whom.')]),

            ('definition',
             'whose says who owns something: this is the girl whose father came here.',
             'be-re-whose',
             'La phrase « This is the girl whose father came here », whose en doré.',
             [('simple', 'The father belongs to the girl, so whose.'),
              ('pas_a_pas', 'If the next word is a thing or a person that BELONGS, write whose.')],
             [('qcm', 1, {'question': 'What does whose say?',
                          'options': ['Who owns something', 'Who does the action',
                                      'Which thing is chosen']},
               {'index': 0}, 'Who owns something.'),
              ('vrai_faux', 1, {'statement': 'You say the girl whose father came here.'},
               {'value': True}, 'Yes: the father belongs to the girl.'),
              ('texte_a_trous', 2,
               {'text': 'This is the girl {{1}} father came here.', 'blanks': 1},
               {'values': ['whose']}, 'whose.'),
              ('qcm', 3, {'question': 'The boy … bag was stolen is crying.',
                          'options': ['whose', 'who', 'whom']},
               {'index': 0}, 'The bag belongs to the boy.'),
              ('vrai_faux', 4, {'statement': 'whose is followed by the thing that is owned.'},
               {'value': True}, 'Yes: whose father, whose bag.')]),

            ('definition',
             'which chooses inside a group that is already known: which of the girls is more '
             'beautiful?',
             'be-re-which',
             'La phrase « Which of the girls is more beautiful? », which en doré.',
             [('simple', 'The girls are known. You are asked to choose among them.'),
              ('visuel', 'which of the … is the sign: there is a group, and a choice to make.')],
             [('qcm', 1, {'question': 'When do you use which?',
                          'options': ['To choose inside a known group',
                                      'To say who owns', 'After a preposition']},
               {'index': 0}, 'To choose inside a known group.'),
              ('vrai_faux', 1, {'statement': 'You say which of the girls is more beautiful.'},
               {'value': True}, 'Yes: you choose among them.'),
              ('texte_a_trous', 2,
               {'text': '{{1}} of the girls is more beautiful?', 'blanks': 1},
               {'values': ['which']}, 'which.'),
              ('qcm', 3, {'question': '… of these books is yours?',
                          'options': ['Which', 'Who', 'Whom']},
               {'index': 0}, 'A choice inside a known group.'),
              ('vrai_faux', 4, {'statement': 'which is used to say who owns something.'},
               {'value': False}, 'No, that is whose.')]),
        ],
    ),

    # ------------------------------------------------------------------ 73
    (
        'Possessive pronouns', ANGLAIS, GRAMMAIRE, 'en', 73,
        'A possessive pronoun replaces a possessive adjective and its noun at once: mine stands '
        'for my books, yours for your case, theirs for their homework. It is never followed by a '
        'noun.',
        'be-po-couv',
        'Quatre cartes alignées : mine, yours, his, theirs.',
        [
            ('definition',
             'mine replaces my and its noun: the books on the table are mine.',
             'be-po-mine',
             'La phrase « The books on the table are mine », mine en doré.',
             [('simple', 'Instead of saying my books again, you say mine.'),
              ('visuel', 'mine is never followed by a noun. You do not say mine books.')],
             [('qcm', 1, {'question': 'What does mine replace?',
                          'options': ['my and its noun', 'me alone', 'my alone']},
               {'index': 0}, 'The whole group: my books becomes mine.'),
              ('vrai_faux', 1, {'statement': 'You say the books are mine.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The books on the table are {{1}}.', 'blanks': 1},
               {'values': ['mine']}, 'mine.'),
              ('qcm', 3, {'question': 'The books on the table are … .',
                          'options': ['mine', 'me', 'my']},
               {'index': 0}, 'mine, which replaces my books.'),
              ('vrai_faux', 4, {'statement': 'You say these are mine books.'},
               {'value': False}, 'No. Either my books, or mine.')]),

            ('definition',
             'yours replaces your and its noun: his case is better than yours.',
             'be-po-yours',
             'La phrase « His case is better than yours », yours en doré.',
             [('simple', 'yours stands for your case: you do not say it twice.'),
              ('visuel', 'yours has no apostrophe. It is never written your-s with a mark.')],
             [('qcm', 1, {'question': 'What does yours replace?',
                          'options': ['your and its noun', 'you alone', 'yourself']},
               {'index': 0}, 'your case becomes yours.'),
              ('vrai_faux', 1, {'statement': 'You say his case is better than yours.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'His case is better than {{1}}.', 'blanks': 1},
               {'values': ['yours']}, 'yours.'),
              ('qcm', 3, {'question': 'His case is better than … .',
                          'options': ['yours', 'your', 'you']},
               {'index': 0}, 'yours replaces your case.'),
              ('vrai_faux', 4, {'statement': 'You say his case is better than your.'},
               {'value': False}, 'No: yours.')]),

            ('definition',
             'theirs replaces their and its noun: all class 5 pupils can do theirs.',
             'be-po-theirs',
             'La phrase « All class 5 pupils can do theirs », theirs en doré.',
             [('simple', 'theirs stands for their homework.'),
              ('visuel', 'Do not mix theirs with them: them is not a possessive.')],
             [('qcm', 1, {'question': 'What does theirs replace?',
                          'options': ['their and its noun', 'them alone',
                                      'themselves']},
               {'index': 0}, 'their homework becomes theirs.'),
              ('vrai_faux', 1, {'statement': 'You say the pupils can do theirs.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'All class 5 pupils can do {{1}}.', 'blanks': 1},
               {'values': ['theirs']}, 'theirs.'),
              ('qcm', 3, {'question': 'All class 5 pupils can do … homework.',
                          'options': ['their', 'theirs', 'them']},
               {'index': 0}, 'Before the noun homework, you write their.'),
              ('vrai_faux', 4, {'statement': 'You say the pupils can do them.'},
               {'value': False}, 'No: theirs.')]),

            ('relation',
             'A possessive pronoun is never followed by a noun. Before a noun you write my, your '
             'or their instead.',
             'be-po-sans',
             'Trois paires : my book et mine, your case et yours, their work et theirs.',
             [('simple', 'With a noun: my book. Without a noun: mine.'),
              ('pas_a_pas', 'Look at the next word. If a noun follows, use my, your, their.')],
             [('qcm', 1, {'question': 'What never follows a possessive pronoun?',
                          'options': ['A noun', 'A full stop', 'A verb']},
               {'index': 0}, 'A noun.'),
              ('vrai_faux', 1, {'statement': 'Before a noun, you write my and not mine.'},
               {'value': True}, 'Yes: my book.'),
              ('association', 2, {'question': 'Match each group with its pronoun.',
                                  'gauche': ['my book', 'your case', 'their work'],
                                  'droite': ['mine', 'yours', 'theirs']},
               {'order': [0, 1, 2]}, 'Each pair says the same thing in two ways.'),
              ('texte_a_trous', 3,
               {'text': 'Before a noun you write my; without a noun you write {{1}}.',
                'blanks': 1},
               {'values': ['mine']}, 'mine.'),
              ('vrai_faux', 4, {'statement': 'You can say yours case.'},
               {'value': False}, 'No: your case, or yours alone.')]),
        ],
    ),

    # ------------------------------------------------------------------ 74
    (
        'Reflexive and demonstrative pronouns', ANGLAIS, GRAMMAIRE, 'en', 74,
        'A reflexive pronoun points back at the subject: themselves for several people, never '
        'themself. A demonstrative points at something: this and that for one thing, these and '
        'those for several.',
        'be-de-couv',
        'Quatre cartes alignées : myself, themselves, this, those.',
        [
            ('relation',
             'When several people do something to themselves, you write themselves. The word '
             'themself does not exist.',
             'be-de-reflexive',
             'La phrase « Nana and Ohoa blamed themselves for the problems », themselves en doré.',
             [('simple', 'Nana and Ohoa are two, so the word takes -selves.'),
              ('visuel', 'One person: himself, herself, myself. Several: ourselves, yourselves, '
                         'themselves.')],
             [('qcm', 1, {'question': 'Nana and Ohoa blamed … for the problems.',
                          'options': ['themselves', 'themself', 'them']},
               {'index': 0}, 'Two people, so themselves.'),
              ('vrai_faux', 1, {'statement': 'The word themself does not exist.'},
               {'value': True}, 'Yes: it is always themselves.'),
              ('texte_a_trous', 2,
               {'text': 'Nana and Ohoa blamed {{1}} for the problems.', 'blanks': 1},
               {'values': ['themselves']}, 'themselves.'),
              ('qcm', 3, {'question': 'Which one is written for one single person?',
                          'options': ['himself', 'themselves', 'ourselves']},
               {'index': 0}, 'himself: one person.'),
              ('vrai_faux', 4, {'statement': 'Several people blamed themself.'},
               {'value': False}, 'No: themselves.')]),

            ('definition',
             'this points at one single thing that is near: this is my father house.',
             'be-de-this',
             'La phrase « This is my father house », This en doré.',
             [('simple', 'One thing, and it is close to you: this.'),
              ('visuel', 'that is also one thing, but further away.')],
             [('qcm', 1, {'question': 'How many things does this point at?',
                          'options': ['One', 'Two', 'Several']},
               {'index': 0}, 'One single thing.'),
              ('vrai_faux', 1, {'statement': 'this is used for something near.'},
               {'value': True}, 'Yes, and that for something further.'),
              ('texte_a_trous', 2,
               {'text': '{{1}} is my father house.', 'blanks': 1},
               {'values': ['this']}, 'this.'),
              ('qcm', 3, {'question': '… is my father house.',
                          'options': ['This', 'These', 'Those']},
               {'index': 0}, 'One house, and it is near: This.'),
              ('vrai_faux', 4, {'statement': 'this points at several things at once.'},
               {'value': False}, 'No, only one.')]),

            ('relation',
             'these is the plural of this, and those is the plural of that.',
             'be-de-these',
             'Deux paires : this et these, that et those.',
             [('simple', 'One becomes several: this becomes these, that becomes those.'),
              ('pas_a_pas', 'Count the things first. One: this or that. Several: these or '
                            'those.')],
             [('qcm', 1, {'question': 'What is the plural of this?',
                          'options': ['these', 'those', 'that']},
               {'index': 0}, 'these.'),
              ('vrai_faux', 1, {'statement': 'The plural of that is those.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each word with its plural.',
                                  'gauche': ['this', 'that'],
                                  'droite': ['these', 'those']},
               {'order': [0, 1]}, 'this becomes these, that becomes those.'),
              ('texte_a_trous', 3,
               {'text': 'The plural of this is {{1}}.', 'blanks': 1},
               {'values': ['these']}, 'these.'),
              ('vrai_faux', 4, {'statement': 'The plural of this is those.'},
               {'value': False}, 'No: these. those is the plural of that.')]),

            ('relation',
             'A demonstrative agrees with the noun that follows it: those boys, these books, this '
             'house.',
             'be-de-those',
             'La phrase « Those boys are not your friends », Those en doré.',
             [('simple', 'boys is plural, so the word before it must be plural too: those.'),
              ('visuel', 'that boys would be wrong, exactly as a French ce garçons would be.')],
             [('qcm', 1, {'question': '… boys are not your friends.',
                          'options': ['Those', 'That', 'This']},
               {'index': 0}, 'boys is plural, so Those.'),
              ('vrai_faux', 1, {'statement': 'You say those boys, and not that boys.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': '{{1}} boys are not your friends.', 'blanks': 1},
               {'values': ['those']}, 'those.'),
              ('qcm', 3, {'question': 'Which group is correct?',
                          'options': ['these books', 'this books', 'those book']},
               {'index': 0}, 'Plural with plural: these books.'),
              ('vrai_faux', 4, {'statement': 'You can write this books.'},
               {'value': False}, 'No: these books.')]),
        ],
    ),

    # ------------------------------------------------------------------ 75
    (
        'A, an and the', ANGLAIS, GRAMMAIRE, 'en', 75,
        'a comes before a consonant sound, an before a vowel sound, and the before something '
        'already known or unique. It is the sound that decides, not the letter: an hour, a one '
        'way ticket.',
        'be-ar-couv',
        'Trois cartes alignées : a, an, the.',
        [
            ('relation',
             'a comes before a word that begins with a consonant sound: a book, a one way ticket.',
             'be-ar-a',
             'La phrase « We bought a one way ticket », a en doré.',
             [('simple', 'one begins with the sound of w, which is a consonant sound, so a.'),
              ('visuel', 'Say the word aloud. If it starts like a consonant, write a.')],
             [('qcm', 1, {'question': 'When do you write a?',
                          'options': ['Before a consonant sound', 'Before a vowel sound',
                                      'Before a plural']},
               {'index': 0}, 'Before a consonant sound.'),
              ('vrai_faux', 1, {'statement': 'You say a one way ticket.'},
               {'value': True}, 'Yes: one is said like wan.'),
              ('texte_a_trous', 2,
               {'text': 'We bought {{1}} one way ticket.', 'blanks': 1},
               {'values': ['a']}, 'a.'),
              ('qcm', 3, {'question': 'We bought … one way ticket.',
                          'options': ['a', 'an', 'the']},
               {'index': 0}, 'a, because of the sound of one.'),
              ('vrai_faux', 4, {'statement': 'You say an one way ticket.'},
               {'value': False}, 'No: a one way ticket.')]),

            ('relation',
             'an comes before a word that begins with a vowel sound: an oasis, an hour.',
             'be-ar-an',
             'La phrase « An oasis is the most fertile place in the desert », An en doré.',
             [('simple', 'In hour, the h is silent, so the word begins with a vowel sound.'),
              ('visuel', 'an apple, an egg, an oasis, an hour.')],
             [('qcm', 1, {'question': 'When do you write an?',
                          'options': ['Before a vowel sound', 'Before a consonant sound',
                                      'Before a verb']},
               {'index': 0}, 'Before a vowel sound.'),
              ('vrai_faux', 1, {'statement': 'You say an hour.'},
               {'value': True}, 'Yes: the h is not said.'),
              ('texte_a_trous', 2,
               {'text': 'My mother left for the market {{1}} hour ago.', 'blanks': 1},
               {'values': ['an']}, 'an.'),
              ('qcm', 3, {'question': '… oasis is the most fertile place in the desert.',
                          'options': ['An', 'A', 'The']},
               {'index': 0}, 'oasis begins with a vowel sound.'),
              ('vrai_faux', 4, {'statement': 'You say a hour.'},
               {'value': False}, 'No: an hour.')]),

            ('relation',
             'the comes before something already known, or something there is only one of: the '
             'market, the desert.',
             'be-ar-the',
             'La phrase « My mother left for the market an hour ago », the en doré.',
             [('simple', 'Everybody knows which market: the one in the village.'),
              ('pas_a_pas', 'Ask yourself: do we both know which one? If yes, write the.')],
             [('qcm', 1, {'question': 'When do you write the?',
                          'options': ['For something already known', 'For any new thing',
                                      'Only before a plural']},
               {'index': 0}, 'For something already known or unique.'),
              ('vrai_faux', 1, {'statement': 'You say the market when everybody knows which one.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'My mother left for {{1}} market.', 'blanks': 1},
               {'values': ['the']}, 'the.'),
              ('qcm', 3, {'question': 'Our teacher bought … new bike.',
                          'options': ['a', 'an', 'the']},
               {'index': 0}, 'A bike we did not know about yet.'),
              ('vrai_faux', 4,
               {'statement': 'the is used for something nobody has heard of yet.'},
               {'value': False}, 'No, that is a or an.')]),

            ('relation',
             'It is the SOUND that decides between a and an, and not the letter written: an hour '
             'with a silent h, a one way ticket said like wan.',
             'be-ar-choisir',
             'Trois lignes : an hour, a one way ticket, c’est le son qui décide.',
             [('simple', 'Say the word aloud before choosing. Your ear is right more often than '
                         'your eye.'),
              ('visuel', 'hour begins with h but sounds like our. one begins with o but sounds '
                         'like wan.')],
             [('qcm', 1, {'question': 'What decides between a and an?',
                          'options': ['The sound of the next word',
                                      'The first letter written', 'The length of the word']},
               {'index': 0}, 'The sound.'),
              ('vrai_faux', 1, {'statement': 'In hour, the letter h is not said.'},
               {'value': True}, 'Yes, which is why you write an hour.'),
              ('texte_a_trous', 2,
               {'text': 'It is the {{1}} that decides between a and an.', 'blanks': 1},
               {'values': ['sound']}, 'The sound.'),
              ('qcm', 3, {'question': 'Which one is correct?',
                          'options': ['an hour', 'a hour', 'an one']},
               {'index': 0}, 'an hour, because of the silent h.'),
              ('vrai_faux', 4, {'statement': 'A word beginning with the letter o always takes an.'},
               {'value': False}, 'No: a one way ticket.')]),
        ],
    ),

    # ------------------------------------------------------------------ 76
    (
        'Antonyms', ANGLAIS, GRAMMAIRE, 'en', 76,
        'An antonym is a word of the opposite meaning: wet and dry, light and heavy, short and '
        'long, behind and in front of, purchased and sold.',
        'be-an-couv',
        'La phrase « wet is the opposite of dry » écrite dans son cadre.',
        [
            ('definition',
             'An antonym is a word that means the opposite of another word.',
             'be-an-def',
             'Trois lignes : le contraire d’un mot, wet et dry, long et short.',
             [('simple', 'Opposite, not merely different. Wet and dry; hot and cold.'),
              ('visuel', 'If one is true, the other cannot be true at the same time.')],
             [('qcm', 1, {'question': 'What is an antonym?',
                          'options': ['A word of the opposite meaning',
                                      'A word of the same meaning',
                                      'A word of the same sound']},
               {'index': 0}, 'The opposite meaning.'),
              ('vrai_faux', 1, {'statement': 'wet and dry are antonyms.'},
               {'value': True}, 'Yes, they are opposites.'),
              ('texte_a_trous', 2,
               {'text': 'An antonym is a word of the {{1}} meaning.', 'blanks': 1},
               {'values': ['opposite']}, 'The opposite meaning.'),
              ('qcm', 3, {'question': 'What is the antonym of long?',
                          'options': ['short', 'tall', 'wide']},
               {'index': 0}, 'short.'),
              ('vrai_faux', 4, {'statement': 'An antonym means the same thing.'},
               {'value': False}, 'No, that is a synonym.')]),

            ('liste',
             'wet and dry, light and heavy, behind and in front of: three pairs of antonyms.',
             'be-an-paires1',
             'Trois paires reliées : wet et dry, light et heavy, behind et in front of.',
             [('simple', 'My mother bought some dry firewood: dry is the opposite of wet.'),
              ('visuel', 'Wet firewood does not burn. That is why dry is the word wanted.')],
             [('qcm', 1, {'question': 'What is the antonym of wet?',
                          'options': ['dry', 'cold', 'clean']},
               {'index': 0}, 'dry.'),
              ('vrai_faux', 1, {'statement': 'The antonym of light is heavy.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each word with its opposite.',
                                  'gauche': ['wet', 'light', 'behind'],
                                  'droite': ['dry', 'heavy', 'in front of']},
               {'order': [0, 1, 2]}, 'Three pairs of opposites.'),
              ('texte_a_trous', 3,
               {'text': 'My mother bought some {{1}} firewood.', 'blanks': 1},
               {'values': ['dry']}, 'dry, the opposite of wet.'),
              ('vrai_faux', 4, {'statement': 'The antonym of behind is beside.'},
               {'value': False}, 'No: in front of.')]),

            ('liste',
             'short and long, purchased and sold, old and new: three more pairs of antonyms.',
             'be-an-paires2',
             'Trois paires reliées : short et long, purchased et sold, old et new.',
             [('simple', 'purchased means bought, so its opposite is sold.'),
              ('pas_a_pas', 'Read the sentence, find the word in brackets, and write its '
                            'opposite in the gap.')],
             [('qcm', 1, {'question': 'What is the antonym of short?',
                          'options': ['long', 'small', 'thin']},
               {'index': 0}, 'long.'),
              ('vrai_faux', 1, {'statement': 'The antonym of purchased is sold.'},
               {'value': True}, 'Yes: purchased means bought.'),
              ('texte_a_trous', 2,
               {'text': 'The rope is too {{1}} for the work.', 'blanks': 1},
               {'values': ['long']}, 'long, the opposite of short.'),
              ('qcm', 3, {'question': 'My father … his old car. The opposite of purchased is…',
                          'options': ['sold', 'kept', 'drove']},
               {'index': 0}, 'sold.'),
              ('vrai_faux', 4, {'statement': 'The antonym of old is ancient.'},
               {'value': False}, 'No: new.')]),

            ('relation',
             'In a sentence, the antonym must keep the meaning sensible: a bag of cement is too '
             'heavy for me to carry.',
             'be-an-phrase',
             'La phrase « A bag of cement is too heavy for me to carry », heavy en doré.',
             [('simple', 'A bag of cement is not light. The opposite of light is heavy.'),
              ('pas_a_pas', 'Put your word back into the sentence and read it again. It must '
                            'make sense.')],
             [('qcm', 1, {'question': 'A bag of cement is too … for me to carry.',
                          'options': ['heavy', 'light', 'dry']},
               {'index': 0}, 'heavy, the opposite of light.'),
              ('vrai_faux', 1, {'statement': 'A bag of cement is heavy.'},
               {'value': True}, 'Yes, which is why it is hard to carry.'),
              ('texte_a_trous', 2,
               {'text': 'A bag of cement is too {{1}} for me to carry.', 'blanks': 1},
               {'values': ['heavy']}, 'heavy.'),
              ('qcm', 3, {'question': 'Please stand … for the pupils to see your face.',
                          'options': ['in front of', 'behind', 'under']},
               {'index': 0}, 'The opposite of behind.'),
              ('vrai_faux', 4,
               {'statement': 'Any opposite fits, even if the sentence stops making sense.'},
               {'value': False}, 'No. Read the sentence again before you write.')]),
        ],
    ),

    # ------------------------------------------------------------------ 77
    (
        'Synonyms', ANGLAIS, GRAMMAIRE, 'en', 77,
        'A synonym is a word of the same meaning: blank and empty, left and abandoned, rushed and '
        'hurried, silly and foolish, unite and join, wicked and cruel.',
        'be-sy-couv',
        'La phrase « blank means empty » écrite dans son cadre.',
        [
            ('definition',
             'A synonym is a word that has the same meaning as another word.',
             'be-sy-def',
             'Trois lignes : un mot de même sens, blank et empty, silly et foolish.',
             [('simple', 'Two words, one meaning. You can put one in the place of the other.'),
              ('visuel', 'A synonym says the same thing; an antonym says the contrary.')],
             [('qcm', 1, {'question': 'What is a synonym?',
                          'options': ['A word of the same meaning',
                                      'A word of the opposite meaning',
                                      'A word with the same first letter']},
               {'index': 0}, 'The same meaning.'),
              ('vrai_faux', 1, {'statement': 'blank and empty are synonyms.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'A synonym is a word of the {{1}} meaning.', 'blanks': 1},
               {'values': ['same']}, 'The same meaning.'),
              ('qcm', 3, {'question': 'What is a synonym of silly?',
                          'options': ['foolish', 'clever', 'nice']},
               {'index': 0}, 'foolish.'),
              ('vrai_faux', 4, {'statement': 'A synonym means the contrary.'},
               {'value': False}, 'No, that is an antonym.')]),

            ('liste',
             'blank and empty, left and abandoned, rushed and hurried: three pairs of synonyms.',
             'be-sy-paires1',
             'Trois paires reliées : blank et empty, left et abandoned, rushed et hurried.',
             [('simple', 'A blank sheet is an empty sheet: nothing is written on it.'),
              ('visuel', 'They rushed down the road, they hurried down the road: the same '
                         'thing.')],
             [('qcm', 1, {'question': 'What is a synonym of blank?',
                          'options': ['empty', 'dirty', 'clean']},
               {'index': 0}, 'empty.'),
              ('vrai_faux', 1, {'statement': 'rushed and hurried mean the same thing.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each word with its synonym.',
                                  'gauche': ['blank', 'left', 'rushed'],
                                  'droite': ['empty', 'abandoned', 'hurried']},
               {'order': [0, 1, 2]}, 'Three pairs of the same meaning.'),
              ('texte_a_trous', 3,
               {'text': 'The examiner gave us a blank sheet, that is an {{1}} sheet.',
                'blanks': 1},
               {'values': ['empty']}, 'empty.'),
              ('vrai_faux', 4, {'statement': 'A synonym of rushed is walked.'},
               {'value': False}, 'No: hurried. Walking is not rushing.')]),

            ('liste',
             'silly and foolish, unite and join, wicked and cruel: three more pairs of synonyms.',
             'be-sy-paires2',
             'Trois paires reliées : silly et foolish, unite et join, wicked et cruel.',
             [('simple', 'To unite two ropes is to join them.'),
              ('pas_a_pas', 'Read the underlined word, then try each word of the bracket in its '
                            'place.')],
             [('qcm', 1, {'question': 'What is a synonym of unite?',
                          'options': ['join', 'break', 'cut']},
               {'index': 0}, 'join.'),
              ('vrai_faux', 1, {'statement': 'wicked and cruel are synonyms.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The silly goat is a {{1}} goat.', 'blanks': 1},
               {'values': ['foolish']}, 'foolish.'),
              ('qcm', 3, {'question': 'The bricklayer tried to unite the ropes. unite means…',
                          'options': ['join', 'cut', 'wrap']},
               {'index': 0}, 'join.'),
              ('vrai_faux', 4, {'statement': 'A synonym of silly is clever.'},
               {'value': False}, 'No, clever is its opposite.')]),

            ('relation',
             'Replacing a word by its synonym does not change what the sentence says: a blank '
             'sheet of paper is an empty sheet of paper.',
             'be-sy-phrase',
             'La phrase « The examiner gave us a blank sheet of paper », blank en doré.',
             [('simple', 'Put the synonym in the place of the word and read again: the meaning '
                         'must hold.'),
              ('visuel', 'If the sentence changes meaning, the word was not a synonym.')],
             [('qcm', 1, {'question': 'The examiner gave us a blank sheet. blank means…',
                          'options': ['empty', 'dirty', 'torn']},
               {'index': 0}, 'empty.'),
              ('vrai_faux', 1,
               {'statement': 'Replacing a word by its synonym keeps the meaning.'},
               {'value': True}, 'Yes, that is the test.'),
              ('texte_a_trous', 2,
               {'text': 'The wicked man {{1}} his wife at the hospital.', 'blanks': 1},
               {'values': ['abandoned']}, 'abandoned, a synonym of left.'),
              ('qcm', 3, {'question': 'They rushed down the road. rushed means…',
                          'options': ['hurried', 'danced', 'walked']},
               {'index': 0}, 'hurried.'),
              ('vrai_faux', 4,
               {'statement': 'A synonym may change what the sentence says.'},
               {'value': False}, 'No. If it changes it, it was not a synonym.')]),
        ],
    ),

    # ------------------------------------------------------------------ 78
    (
        'Malaria: a guided writing', ANGLAIS, 'Guided writing', 'en', 78,
        'Malaria is caused by a parasite which is carried by the anopheles mosquito from one '
        'person to another. Only the female mosquito, which is a blood-sucker, carries the '
        'disease. Such a patient feels chilly, feverish and weak, and may die if his temperature '
        'rises too high.',
        'be-ma-couv',
        'La phrase « caused by a parasite » écrite dans son cadre.',
        [
            ('definition',
             'Malaria is caused by a parasite. The parasite is carried by the anopheles mosquito.',
             'be-ma-cause',
             'La phrase « Malaria is caused by a parasite », caused et parasite en doré.',
             [('simple', 'The mosquito is not the illness. It carries the parasite that gives '
                         'it.'),
              ('visuel', 'caused by: the cause comes after the word by.')],
             [('qcm', 1, {'question': 'What is malaria caused by?',
                          'options': ['A parasite', 'A cold wind', 'Dirty clothes']},
               {'index': 0}, 'A parasite.'),
              ('vrai_faux', 1, {'statement': 'Malaria is caused by a parasite.'},
               {'value': True}, 'Yes, and the mosquito carries it.'),
              ('texte_a_trous', 2,
               {'text': 'Malaria is caused by a {{1}}.', 'blanks': 1},
               {'values': ['parasite']}, 'A parasite.'),
              ('qcm', 3, {'question': 'Which mosquito carries the parasite?',
                          'options': ['The anopheles', 'Every kind of fly', 'The housefly']},
               {'index': 0}, 'The anopheles mosquito.'),
              ('vrai_faux', 4, {'statement': 'The mosquito itself is the disease.'},
               {'value': False}, 'No, it carries the parasite that causes it.')]),

            ('relation',
             'Only the female anopheles mosquito carries the disease. She is a blood-sucker.',
             'be-ma-femelle',
             'La phrase « Only the female mosquito carries the disease », female en doré.',
             [('simple', 'The male does not bite. Only the female takes blood.'),
              ('visuel', 'A blood-sucker is an animal that sucks blood: the word says it.')],
             [('qcm', 1, {'question': 'Which mosquito carries the disease?',
                          'options': ['Only the female', 'Only the male', 'Both of them']},
               {'index': 0}, 'Only the female.'),
              ('vrai_faux', 1, {'statement': 'The female anopheles is a blood-sucker.'},
               {'value': True}, 'Yes: she sucks blood.'),
              ('texte_a_trous', 2,
               {'text': 'Only the {{1}} mosquito carries the disease.', 'blanks': 1},
               {'values': ['female']}, 'The female.'),
              ('qcm', 3, {'question': 'What does blood-sucker mean?',
                          'options': ['An animal that sucks blood', 'A kind of medicine',
                                      'A sort of net']},
               {'index': 0}, 'An animal that sucks blood.'),
              ('vrai_faux', 4, {'statement': 'The male mosquito carries the disease too.'},
               {'value': False}, 'No, only the female.')]),

            ('relation',
             'The mosquito sucks the blood of a sick person, takes in the parasite, and then '
             'transfers it into the blood of a healthy person.',
             'be-ma-transmission',
             'Trois lignes : it sucks the blood, it takes in the parasite, it transfers it.',
             [('simple', 'Three steps, always in this order: sucks, takes in, transfers.'),
              ('pas_a_pas', 'First a sick person, then the parasite inside the mosquito, then a '
                            'healthy person who catches it.')],
             [('qcm', 1, {'question': 'What does the mosquito do first?',
                          'options': ['It sucks blood', 'It transfers the parasite',
                                      'It dies']},
               {'index': 0}, 'It sucks the blood of a sick person.'),
              ('vrai_faux', 1,
               {'statement': 'The mosquito transfers the parasite into a healthy person.'},
               {'value': True}, 'Yes, when it bites again.'),
              ('chronologie', 2, {'question': 'Put the three steps in the right order.',
                                  'tokens': ['It sucks the blood of a sick person',
                                             'It takes in the parasite',
                                             'It transfers it to a healthy person']},
               {'order': [0, 1, 2]}, 'Sucks, takes in, transfers.'),
              ('texte_a_trous', 3,
               {'text': 'The mosquito {{1}} the parasite into his blood stream.', 'blanks': 1},
               {'values': ['transfers']}, 'transfers.'),
              ('vrai_faux', 4,
               {'statement': 'The mosquito transfers the parasite before it sucks any blood.'},
               {'value': False}, 'No, it must take it in first.')]),

            ('relation',
             'Such a patient feels chilly, feverish and weak, and he may die if his temperature '
             'rises too high.',
             'be-ma-symptomes',
             'La phrase « Such a patient feels chilly, feverish and weak », feels en doré.',
             [('simple', 'chilly: he is cold. feverish: he is hot. weak: he has no strength.'),
              ('visuel', 'feels is the word for what the body tells you.')],
             [('qcm', 1, {'question': 'How does such a patient feel?',
                          'options': ['Chilly, feverish and weak', 'Strong and happy',
                                      'Hungry only']},
               {'index': 0}, 'Chilly, feverish and weak.'),
              ('vrai_faux', 1, {'statement': 'A patient with malaria feels weak.'},
               {'value': True}, 'Yes, he has no strength.'),
              ('texte_a_trous', 2,
               {'text': 'Such a patient {{1}} chilly, feverish and weak.', 'blanks': 1},
               {'values': ['feels']}, 'feels.'),
              ('qcm', 3, {'question': 'What may happen if his temperature rises too high?',
                          'options': ['He may die', 'He gets stronger', 'He feels nothing']},
               {'index': 0}, 'He may die. Malaria is serious.'),
              ('vrai_faux', 4, {'statement': 'Malaria is never dangerous.'},
               {'value': False}, 'No. A patient may die of it.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues, trous = set(), 0, 0, 0
    titres = [l[0] for l in LECONS]
    assert len(set(titres)) == len(titres), 'titre en double'
    rangs = [l[4] for l in LECONS]
    assert len(set(rangs)) == len(rangs), 'rang en double'

    for titre, matiere, chapitre, langue, ordre, resume, img, prompt, notions in LECONS:
        assert matiere in (SCIENCES, ANGLAIS), matiere
        assert langue in ('fr', 'en'), langue
        assert len(resume) <= 400, 'résumé trop long (%d) : %s' % (len(resume), titre)
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
        'fig', os.path.join(ici, 'figures-brayne-revision-nov.py'))
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
        'classe': CLASSE, 'enfant': ENFANT,
        'lecons': [
            {
                'title': titre, 'matiere': matiere, 'chapter': chapitre, 'lang': langue,
                'taught_on': None, 'sort_order': ordre,
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
            for titre, matiere, chapitre, langue, ordre, resume, img, prompt, notions in LECONS
        ],
    }


if __name__ == '__main__':
    images, items, notions, trous = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-revision-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for titre, matiere, _c, langue, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-12s %-44s %d notions  %d questions'
              % (ordre, matiere, titre, len(ns), sum(len(n[5]) for n in ns)))
    print(chemin)
