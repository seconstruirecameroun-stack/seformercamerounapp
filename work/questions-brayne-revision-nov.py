# -*- coding: utf-8 -*-
"""
La relecture des sept leçons déjà en base, dans la forme de la révision du
9 novembre 2026 — BRAYNE, CM1.

CE QUE FAIT CE FICHIER, et en quoi il diffère des autres. Il ne crée pas
de leçons : il AJOUTE des questions à des notions qui existent, et deux
notions à une leçon qui existe. Le contenu de ces sept leçons était juste ;
c-est la FORME des questions qui ne couvrait pas l-épreuve annoncée.

LE RELEVÉ, FORME PAR FORME. Les formes du tableau sont : le tableau à
compléter en deux colonnes, le schéma à annoter par numéros, la liste à
entourer avec ses intrus, le texte à trous avec ses mots donnés, et la
question directe. Voici ce qui manquait :

  leçon 9   puberté        le TABLEAU fille / garçon n-était nulle part.
                           Les six changements du tableau - voix grave,
                           première éjaculation, voix aiguë, seins, barbe,
                           premières règles - ne se triaient jamais
  leçon 10  organes        aucune question dans la forme « le numéro 3
                           désigne… » : rien ne faisait nommer un organe
                           par son rôle ou sa place
  leçon 11  cycle de l-eau les QUATRE MOTS du schéma - infiltration,
                           évaporation, ruissellement, condensation - ne
                           se posaient jamais sur une étape
  leçon 12  eau potable    les quatre INTRUS de la liste à cocher -
                           tamiser, blanchir, tiédir, colorer - n-étaient
                           proposés nulle part
  leçon 13  compost        même défaut : les intrus de la liste à entourer
                           - piles, plastiques, tessons, clous - manquaient
  leçon 14  lampe          DEUX PARTIES MANQUAIENT : le bec et la poignée
                           de transport, que le texte à trous du tableau
                           demande. Et les précautions d-usage, demandées
                           à la question 3, n-étaient nulle part
  leçon 33  points d-eau   « cite 3 actions » n-avait pas sa question

Les leçons 32 (les roches) et 34 (le déplacement des animaux) couvrent
déjà leur partie du tableau, et ne reçoivent rien.

UN TROU QUE JE NE COMBLE PAS, ET C-EST VOULU. La question 1b demande
« quand DÉBUTE ET S-ACHÈVE la puberté ». Sa leçon donne le début - 12 à
15 ans chez le garçon, 11 à 14 ans chez la fille - et ne dit rien de la
fin. Je n-invente pas un âge : il n-est ni dans son cahier, ni dans les
photos. C-est au père de le demander à la maîtresse, et c-est écrit dans
work/brayne-revision-notes.md.

Usage :  python work/questions-brayne-revision-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-questions-nov.py. ')

CLASSE = 'CM1'
ENFANT = 'BRAYNE'
TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

# Les notions visées, relevées en base le 9 novembre 2026. Le script refuse
# de viser une notion qui ne figure pas ici, et l-insertion refuse d-en
# viser une qui ne figure pas en base : une faute de recopie ne peut donc
# pas accrocher des questions à la mauvaise notion, ni à aucune.
EN_BASE = {
    'Les changements liés à la puberté': [
        'La puberté est le passage de l’enfant à l’état adulte.',
        'Les changements commencent entre 12 et 15 ans chez les garçons, entre 11 et 14 ans '
        'chez les filles.',
        'Chez le garçon : les épaules s’élargissent, les muscles se développent, la voix devient '
        'grave, des poils apparaissent.',
        'Chez la fille : les seins se développent, le bassin s’élargit, la voix devient fine, '
        'des poils apparaissent.',
        'Les testicules commencent à produire les spermatozoïdes ; la jeune fille libère des '
        'ovules et ses premières règles apparaissent.',
    ],
    'Les organes reproducteurs': [
        'L’appareil reproducteur est l’ensemble des organes qui permettent de se reproduire.',
        'Chez l’homme : le pénis, les deux testicules, les canaux et la prostate.',
        'Chez la femme : la vulve, l’utérus, le vagin et les deux ovaires.',
        'Chaque organe a son rôle : les testicules produisent les spermatozoïdes, les ovaires '
        'les ovules, l’utérus accueille la gestation.',
    ],
    'Le cycle de l’eau dans la nature': [
        'Le cycle de l’eau est le trajet que parcourt l’eau pour revenir à son point de départ.',
        'Sous l’effet de la chaleur, l’eau des lacs et des fleuves se transforme en vapeur : '
        'c’est l’évaporation.',
        'Au contact des zones froides, la vapeur se transforme en nuage : c’est la condensation.',
        'L’eau tombe sous forme de pluie : c’est la précipitation. La pluie s’infiltre ensuite '
        'dans le sol.',
        'L’eau ruisselle et se retrouve dans les mers, les lacs et les fleuves, et le cycle '
        'recommence.',
    ],
    'L’eau potable': [
        'Une eau potable est celle qu’on peut boire sans danger pour notre santé.',
        'Pour rendre une eau potable, on peut la javelliser et la filtrer, la bouillir et la '
        'filtrer, ou la javelliser et la décanter.',
        'L’eau maintient la température du corps, facilite le transport des nutriments et '
        'l’évacuation des déchets.',
    ],
    'L’amélioration des sols : le compost': [
        'Le compost est un engrais naturel fabriqué à partir de matières provenant des animaux '
        'et des végétaux.',
        'On peut enrichir un sol pauvre en utilisant le compost.',
        'Les éléments du compost sont biodégradables : feuilles mortes, cendre de bois, restes '
        'de repas, épluchures de tubercules, litière d’animaux.',
    ],
    'La lampe à pétrole': [
        'La lampe à pétrole, encore appelée lampe tempête, est un appareil d’éclairage dont la '
        'source d’énergie est le pétrole.',
        'Elle a cinq parties essentielles : le réservoir, la molette, la mèche, le verre et la '
        'grille d’aération.',
        'Chaque partie a son rôle : le réservoir contient le pétrole, la molette règle la '
        'flamme, la mèche la porte, le verre la protège et la grille laisse circuler l’air.',
    ],
    'La gestion de l’eau': [
        'Chaque village ou quartier doit avoir des points d’eau pour permettre aux populations '
        'de s’approvisionner.',
        'Les points d’eau sont le puits, le forage, la source et le robinet.',
        'Pour bien gérer un point d’eau, on nettoie les alentours et on protège les sources et '
        'les puits pour éviter que la saleté y tombe.',
        'Il faut aussi prévoir des heures de ravitaillement pour éviter le gaspillage, et '
        'multiplier les points d’eau.',
        'On désinfecte l’eau en y mettant quelques gouttes d’eau de javel.',
    ],
}

PUB = 'Les changements liés à la puberté'
ORG = 'Les organes reproducteurs'
CYC = 'Le cycle de l’eau dans la nature'
POT = 'L’eau potable'
COM = 'L’amélioration des sols : le compost'
LAM = 'La lampe à pétrole'
GES = 'La gestion de l’eau'

# (leçon, notion visée, questions à ajouter)
AJOUTS = [
    # ---- leçon 9 : le tableau fille / garçon ------------------------------
    (PUB, EN_BASE[PUB][2], [
        ('qcm', 2, {'question': 'La voix devient grave. Chez qui ?',
                    'options': ['Chez le jeune garçon', 'Chez la jeune fille',
                                'Chez les deux']},
         {'index': 0}, 'Chez le garçon. Chez la fille, elle devient aiguë.'),
        ('qcm', 3, {'question': 'La barbe apparaît. Chez qui ?',
                    'options': ['Chez le jeune garçon', 'Chez la jeune fille',
                                'Chez les deux']},
         {'index': 0}, 'Chez le jeune garçon.'),
        ('vrai_faux', 4, {'statement': 'Chez le jeune garçon, la voix devient aiguë.'},
         {'value': False}, 'Non, elle devient grave.'),
    ]),
    (PUB, EN_BASE[PUB][3], [
        ('qcm', 2, {'question': 'Les seins se développent. Chez qui ?',
                    'options': ['Chez la jeune fille', 'Chez le jeune garçon',
                                'Chez les deux']},
         {'index': 0}, 'Chez la jeune fille.'),
        ('qcm', 3, {'question': 'La voix devient aiguë. Chez qui ?',
                    'options': ['Chez la jeune fille', 'Chez le jeune garçon',
                                'Chez les deux']},
         {'index': 0}, 'Chez la jeune fille. Chez le garçon, elle devient grave.'),
        ('vrai_faux', 4,
         {'statement': 'Les épaules qui s’élargissent sont un changement de la jeune fille.'},
         {'value': False}, 'Non, c’est un changement du jeune garçon.'),
    ]),
    (PUB, EN_BASE[PUB][4], [
        ('qcm', 2, {'question': 'La première éjaculation. Chez qui ?',
                    'options': ['Chez le jeune garçon', 'Chez la jeune fille',
                                'Chez les deux']},
         {'index': 0}, 'Chez le jeune garçon.'),
        ('qcm', 2, {'question': 'Les premières règles. Chez qui ?',
                    'options': ['Chez la jeune fille', 'Chez le jeune garçon',
                                'Chez les deux']},
         {'index': 0}, 'Chez la jeune fille.'),
        ('association', 3, {'question': 'Relie chaque changement à qui il concerne.',
                            'gauche': ['la première éjaculation', 'les premières règles',
                                       'des poils apparaissent'],
                            'droite': ['le jeune garçon', 'la jeune fille', 'les deux']},
         {'order': [0, 1, 2]}, 'Les poils, eux, viennent chez les deux.'),
        ('vrai_faux', 4,
         {'statement': 'Les premières règles annoncent que la jeune fille peut avoir un enfant.'},
         {'value': True}, 'Oui, ses ovaires libèrent des ovules.'),
    ]),

    # ---- leçon 10 : nommer un organe par sa place et son rôle -------------
    (ORG, EN_BASE[ORG][1], [
        ('qcm', 2, {'question': 'Sur le schéma, quel organe produit les spermatozoïdes ?',
                    'options': ['Les testicules', 'La prostate', 'Le pénis']},
         {'index': 0}, 'Les deux testicules.'),
        ('association', 3, {'question': 'Relie chaque organe de l’homme à son rôle.',
                            'gauche': ['les testicules', 'les canaux', 'la prostate'],
                            'droite': ['produisent les spermatozoïdes', 'les conduisent',
                                       'fabrique un liquide']},
         {'order': [0, 1, 2]}, 'Chacun a son rôle dans l’appareil.'),
    ]),
    (ORG, EN_BASE[ORG][2], [
        ('qcm', 2, {'question': 'Sur le schéma, quel organe accueille le bébé ?',
                    'options': ['L’utérus', 'Le vagin', 'La vulve']},
         {'index': 0}, 'L’utérus.'),
        ('qcm', 3, {'question': 'Sur le schéma, quel organe produit les ovules ?',
                    'options': ['Les ovaires', 'L’utérus', 'La vulve']},
         {'index': 0}, 'Les deux ovaires.'),
        ('vrai_faux', 4,
         {'statement': 'Les deux ovaires sont placés de chaque côté de l’utérus.'},
         {'value': True}, 'Oui, un de chaque côté.'),
    ]),
    (ORG, EN_BASE[ORG][3], [
        ('association', 2, {'question': 'Relie chaque organe à ce qu’il produit ou accueille.',
                            'gauche': ['les ovaires', 'l’utérus', 'les testicules'],
                            'droite': ['les ovules', 'la gestation', 'les spermatozoïdes']},
         {'order': [0, 1, 2]}, 'C’est la question du tableau à compléter.'),
    ]),

    # ---- leçon 11 : les quatre mots du schéma -----------------------------
    (CYC, EN_BASE[CYC][0], [
        ('association', 3, {'question': 'Relie chaque étape au mot du schéma.',
                            'gauche': ['l’eau chauffe et monte', 'la vapeur devient nuage',
                                       'l’eau entre dans le sol', 'l’eau coule sur le sol'],
                            'droite': ['évaporation', 'condensation', 'infiltration',
                                       'ruissellement']},
         {'order': [0, 1, 2, 3]}, 'Ce sont les quatre mots à poser sur le dessin.'),
        ('qcm', 2, {'question': 'Quel est le titre du schéma ?',
                    'options': ['Le cycle de l’eau', 'La pluie du matin', 'Les nuages du ciel']},
         {'index': 0}, 'Le cycle de l’eau.'),
    ]),
    (CYC, EN_BASE[CYC][1], [
        ('texte_a_trous', 2,
         {'text': 'Sous l’effet de la {{1}}, l’eau des fleuves se transforme en vapeur.',
          'blanks': 1},
         {'values': ['chaleur']}, 'Sous l’effet de la chaleur.'),
    ]),
    (CYC, EN_BASE[CYC][2], [
        ('texte_a_trous', 2,
         {'text': 'Dans l’atmosphère, la vapeur se refroidit et se transforme en {{1}}.',
          'blanks': 1},
         {'values': ['nuage']}, 'En nuage : c’est la condensation.'),
    ]),
    (CYC, EN_BASE[CYC][3], [
        ('texte_a_trous', 2, {'text': 'Le nuage grossit, se condense, et retombe sous forme '
                                      'de {{1}}.', 'blanks': 1},
         {'values': ['pluie']}, 'Sous forme de pluie.'),
    ]),
    (CYC, EN_BASE[CYC][4], [
        ('texte_a_trous', 2,
         {'text': 'L’eau s’infiltre, ruisselle et retombe dans le fleuve : c’est le {{1}} de '
                  'l’eau.', 'blanks': 1},
         {'values': ['cycle']}, 'C’est le cycle de l’eau.'),
        ('qcm', 3, {'question': 'Comment s’appelle l’eau qui coule sur le sol sans y entrer ?',
                    'options': ['Le ruissellement', 'L’infiltration', 'L’évaporation']},
         {'index': 0}, 'Le ruissellement.'),
    ]),

    # ---- leçon 12 : les intrus de la liste à cocher -----------------------
    (POT, EN_BASE[POT][1], [
        ('qcm', 2, {'question': 'Lequel ne rend pas une eau potable ?',
                    'options': ['La tiédir', 'La bouillir', 'La filtrer']},
         {'index': 0}, 'La tiédir ne tue pas les microbes. Il faut la bouillir.'),
        ('qcm', 3, {'question': 'Lequel ne rend pas une eau potable ?',
                    'options': ['La colorer', 'La javelliser', 'La décanter']},
         {'index': 0}, 'La colorer ne la nettoie pas du tout.'),
        ('association', 3, {'question': 'Relie chaque mot à ce qu’on fait vraiment.',
                            'gauche': ['javelliser', 'filtrer', 'bouillir'],
                            'droite': ['y mettre de l’eau de javel', 'la passer dans un filtre',
                                       'la faire chauffer très fort']},
         {'order': [0, 1, 2]}, 'Trois façons de rendre une eau potable.'),
        ('vrai_faux', 4, {'statement': 'Blanchir une eau suffit à la rendre potable.'},
         {'value': False}, 'Non. Blanchir et tamiser ne rendent pas une eau potable.'),
    ]),

    # ---- leçon 13 : les intrus de la liste à entourer ---------------------
    (COM, EN_BASE[COM][2], [
        ('qcm', 2, {'question': 'Lequel entre dans le compost ?',
                    'options': ['Les épluchures de manioc', 'Les vieilles piles',
                                'Les tessons de bouteille']},
         {'index': 0}, 'Les épluchures pourrissent : elles sont biodégradables.'),
        ('qcm', 2, {'question': 'Lequel n’entre pas dans le compost ?',
                    'options': ['Les vieux clous', 'Les feuilles de bananier',
                                'La fiente des animaux']},
         {'index': 0}, 'Les vieux clous ne pourrissent pas.'),
        ('qcm', 3, {'question': 'Lequel n’entre pas dans le compost ?',
                    'options': ['Les vieux plastiques', 'Les épluchures',
                                'Les feuilles mortes']},
         {'index': 0}, 'Le plastique ne pourrit pas : il pollue le sol.'),
        ('association', 3, {'question': 'Relie chaque élément à ce qu’il devient.',
                            'gauche': ['les épluchures de manioc', 'les vieilles piles',
                                       'les tessons de bouteille'],
                            'droite': ['vont au compost', 'polluent le sol', 'coupent les pieds']},
         {'order': [0, 1, 2]}, 'Un seul des trois est biodégradable.'),
        ('vrai_faux', 4, {'statement': 'Les vieilles piles peuvent aller dans le compost.'},
         {'value': False}, 'Non. Elles polluent la terre et l’eau.'),
    ]),

    # ---- leçon 14 : nommer les parties sur le schéma ----------------------
    (LAM, EN_BASE[LAM][1], [
        ('qcm', 2, {'question': 'Sur le schéma, quelle partie contient le pétrole ?',
                    'options': ['Le réservoir', 'Le verre', 'La grille d’aération']},
         {'index': 0}, 'Le réservoir.'),
        ('texte_a_trous', 2,
         {'text': 'Lorsqu’on verse le pétrole dans le {{1}}, la mèche l’absorbe.', 'blanks': 1},
         {'values': ['réservoir']}, 'Dans le réservoir.'),
        ('texte_a_trous', 3, {'text': 'La {{1}} permet de monter et de descendre la mèche.',
                              'blanks': 1},
         {'values': ['molette']}, 'La molette.'),
        ('qcm', 3, {'question': 'Quelle partie diffuse la lumière ?',
                    'options': ['Le verre', 'La molette', 'Le réservoir']},
         {'index': 0}, 'Le verre : il protège la flamme et diffuse la lumière.'),
        ('vrai_faux', 4, {'statement': 'La grille d’aération sert à diffuser la lumière.'},
         {'value': False}, 'Non, elle laisse circuler l’air. C’est le verre qui diffuse.'),
    ]),

    # ---- leçon 33 : citer des points d-eau et des actions -----------------
    (GES, EN_BASE[GES][1], [
        ('qcm', 2, {'question': 'Cite deux points d’eau.',
                    'options': ['Le puits et le forage', 'La route et le marché',
                                'La case et le champ']},
         {'index': 0}, 'Le puits, le forage, la source et le robinet.'),
    ]),
    (GES, EN_BASE[GES][2], [
        ('qcm', 2, {'question': 'Quelle action garde un point d’eau propre ?',
                    'options': ['Nettoyer ses alentours', 'Y jeter les ordures',
                                'Y laver le linge']},
         {'index': 0}, 'On nettoie les alentours.'),
        ('qcm', 3, {'question': 'Comment protège-t-on un puits ?',
                    'options': ['En le couvrant', 'En le laissant ouvert',
                                'En y jetant du sable']},
         {'index': 0}, 'On le couvre, pour que la saleté n’y tombe pas.'),
        ('vrai_faux', 4,
         {'statement': 'On peut laver son linge dans un point d’eau de boisson.'},
         {'value': False}, 'Non, cela salit l’eau que tout le monde boit.'),
    ]),
]

# (leçon, rang de la notion, kind, phrase, image, prompt, explications, questions)
#
# Les rangs valent 4 et 5, et non 3 et 4 : les notions de cette leçon-là
# sont numérotées à partir de UN, et non de zéro comme celles des lots
# récents. L-insertion a refusé le premier essai pour cette raison, avant
# d-avoir rien écrit.
NOTIONS_NEUVES = [
    (LAM, 4, 'liste',
     'La lampe a aussi un bec, qui tient la mèche, et une poignée de transport, qui permet de la '
     'porter sans se brûler.',
     'br-la-bec',
     'Deux paires reliées : le bec tient la mèche, la poignée sert à la porter.',
     [('simple', 'Avec le bec et la poignée, la lampe compte sept parties nommées, et non cinq.'),
      ('visuel', 'Le bec est juste au-dessus du réservoir ; la poignée est l’anse du dessus.')],
     [('qcm', 1, {'question': 'Quelle partie tient la mèche ?',
                  'options': ['Le bec', 'La poignée', 'Le verre']},
       {'index': 0}, 'Le bec.'),
      ('vrai_faux', 1, {'statement': 'La poignée de transport sert à porter la lampe.'},
       {'value': True}, 'Oui, sans se brûler les doigts.'),
      ('texte_a_trous', 2, {'text': 'Le {{1}} tient la mèche de la lampe.', 'blanks': 1},
       {'values': ['bec']}, 'Le bec.'),
      ('qcm', 3, {'question': 'À quoi sert la poignée de transport ?',
                  'options': ['À porter la lampe', 'À régler la flamme',
                              'À contenir le pétrole']},
       {'index': 0}, 'À la porter.'),
      ('vrai_faux', 4, {'statement': 'Le bec sert à porter la lampe.'},
       {'value': False}, 'Non, c’est la poignée de transport.')]),

    (LAM, 5, 'liste',
     'Avec une lampe à pétrole, on ne verse jamais le pétrole près de la flamme, on la tient loin '
     'des enfants et des rideaux, et on l’éteint avant de dormir.',
     'br-la-precautions',
     'Trois lignes : ne pas verser près de la flamme, la tenir loin des enfants, l’éteindre.',
     [('simple', 'Le pétrole brûle. Tout le danger vient de là.'),
      ('pas_a_pas', 'On éteint, on laisse refroidir, et seulement ensuite on remplit le '
                    'réservoir.')],
     [('qcm', 1, {'question': 'Quand remplit-on le réservoir ?',
                  'options': ['Lampe éteinte', 'Lampe allumée', 'Pendant qu’on dort']},
       {'index': 0}, 'Lampe éteinte, et refroidie.'),
      ('vrai_faux', 1, {'statement': 'On éteint la lampe à pétrole avant de dormir.'},
       {'value': True}, 'Oui, toujours.'),
      ('texte_a_trous', 2, {'text': 'On ne verse jamais le pétrole près de la {{1}}.',
                            'blanks': 1},
       {'values': ['flamme']}, 'Près de la flamme.'),
      ('qcm', 3, {'question': 'Où ne faut-il pas poser une lampe à pétrole allumée ?',
                  'options': ['Près d’un rideau', 'Sur une table', 'Au milieu de la pièce']},
       {'index': 0}, 'Près d’un rideau : le feu prendrait.'),
      ('vrai_faux', 4,
       {'statement': 'On peut laisser une lampe allumée à portée d’un petit enfant.'},
       {'value': False}, 'Non. Elle brûle, et elle se renverse.')]),
]


def verifier_items(items, exiger_quatre_etapes):
    """Les mêmes règles que partout : une faute ici devient une faute posée."""
    niveaux = set()
    trous = 0
    for ikind, niveau, payload, answer, explain in items:
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
            longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
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
    if exiger_quatre_etapes:
        assert niveaux == {1, 2, 3, 4}, 'étapes manquantes : %s' % sorted(niveaux)
    return len(items), trous


def verifier():
    total, trous = 0, 0
    for lecon, notion, items in AJOUTS:
        assert lecon in EN_BASE, 'leçon inconnue : ' + lecon
        assert notion in EN_BASE[lecon], \
            'notion non relevée en base, donc probablement mal recopiée : ' + notion
        # Une notion qui reçoit des questions en a déjà des quatre étapes :
        # les ajouts n-ont donc pas à les couvrir toutes.
        n, tr = verifier_items(items, False)
        total += n
        trous += tr

    images = set()
    for lecon, rang, kind, phrase, img, prompt, expl, items in NOTIONS_NEUVES:
        assert lecon in EN_BASE, 'leçon inconnue : ' + lecon
        assert phrase not in EN_BASE[lecon], 'cette notion existe déjà : ' + phrase
        assert kind in ('definition', 'date', 'liste', 'relation'), kind
        assert len(phrase) <= 180, 'notion trop longue (%d) : %s' % (len(phrase), phrase)
        assert img not in images, 'image en double : ' + img
        images.add(img)
        for registre, corps in expl:
            assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), registre
            assert len(corps) <= 200, 'explication trop longue : ' + corps
        n, tr = verifier_items(items, True)
        total += n
        trous += tr

    rangs = [(l, r) for l, r, *_ in NOTIONS_NEUVES]
    assert len(set(rangs)) == len(rangs), 'deux notions neuves au même rang'

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-brayne-questions-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    assert not images - dessinees, 'images jamais dessinées : ' + ', '.join(images - dessinees)
    assert not dessinees - images, 'images jamais utilisées : ' + ', '.join(dessinees - images)
    return total, trous, len(images)


def paquet():
    return {
        'classe': CLASSE, 'enfant': ENFANT,
        'ajouts': [
            {
                'lecon': lecon, 'notion': notion,
                'items': [{'kind': ik, 'level': lv, 'payload': pl, 'answer': an, 'explain': ex}
                          for ik, lv, pl, an, ex in items],
            }
            for lecon, notion, items in AJOUTS
        ],
        'notions_neuves': [
            {
                'lecon': lecon, 'sort_order': rang, 'kind': kind, 'statement': phrase,
                'illustration': img, 'illustration_prompt': FIGURE + prompt,
                'explanations': [{'register': r, 'body': b} for r, b in expl],
                'items': [{'kind': ik, 'level': lv, 'payload': pl, 'answer': an, 'explain': ex}
                          for ik, lv, pl, an, ex in items],
            }
            for lecon, rang, kind, phrase, img, prompt, expl, items in NOTIONS_NEUVES
        ],
    }


if __name__ == '__main__':
    total, trous, images = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-questions-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    par_lecon = {}
    for lecon, _n, items in AJOUTS:
        par_lecon[lecon] = par_lecon.get(lecon, 0) + len(items)
    for lecon, _r, _k, _p, _i, _pr, _e, items in NOTIONS_NEUVES:
        par_lecon[lecon] = par_lecon.get(lecon, 0) + len(items)

    print('%d questions ajoutées dont %d a trous - %d notions neuves - %d images'
          % (total, trous, len(NOTIONS_NEUVES), images))
    for lecon in sorted(par_lecon):
        print('  %-40s +%d questions' % (lecon, par_lecon[lecon]))
    print(chemin)
