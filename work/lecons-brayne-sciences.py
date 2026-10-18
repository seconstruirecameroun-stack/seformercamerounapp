# -*- coding: utf-8 -*-
"""
Les six leçons de sciences et de technologie du cahier de BRAYNE (CM1),
octobre 2026.

La puberté (lundi 12), les organes reproducteurs (mardi 13), le cycle de
l'eau (mercredi 14), l'eau potable (jeudi 15), le compost (vendredi 16) et la
lampe à pétrole (sans date, à la suite du vendredi).

Deux matières, pas une. Le référentiel de l'école donne au CM1 « Sciences »
et « Technologie » séparément, et la page de la lampe porte l'en-tête
Technologie quand les cinq autres portent Science de la Vie, Sciences
Physiques et Chimiques ou Sciences Agricoles. L'en-tête du cahier devient le
chapitre, et la matière suit le référentiel.

Deux leçons parlent du corps et de la reproduction. Elles sont transcrites
comme le cahier les donne, avec les mots exacts que la maîtresse a écrits au
tableau — pénis, testicules, vulve, utérus, ovaires. Un enfant de CM1
interrogé à l'école sur ces mots-là doit les avoir révisés sous ces mots-là.
Les questions restent factuelles : ce qui produit quoi, ce qui sert à quoi.

Rien n'est ajouté au cahier. La page de la lampe ne porte pas de date : elle
n'en reçoit pas.

Usage :  python work/lecons-brayne-sciences.py
"""

import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-sciences.py. '

CLASSE = 'CM1'
ENFANT = 'BRAYNE'

LECONS = [
    (
        'Les changements liés à la puberté', 'Sciences', 'Science de la Vie',
        '2026-10-12', 9,
        'La puberté est le passage de l’enfant à l’état adulte. Les changements, appelés caractères '
        'sexuels secondaires, commencent entre 12 et 15 ans chez les garçons et entre 11 et 14 ans '
        'chez les filles. Ils sont morphologiques et physiologiques.',
        'pu-puberte',
        'Une toise murale graduée de 10 à 16 ans, deux repères marqués sur la hauteur.',
        [
            (
                'definition',
                'La puberté est le passage de l’enfant à l’état adulte.',
                'pu-passage',
                'Deux cartes pastel reliées par une flèche : enfant à gauche, adulte à droite.',
                [
                    ('simple', 'C’est le moment où le corps d’un enfant devient peu à peu celui d’un adulte.'),
                    ('visuel', 'Un passage, donc quelque chose qui dure : cela ne se fait pas en un jour.'),
                ],
                [
                    ('qcm', 1, {'question': 'La puberté est le passage…',
                                'options': ['de l’enfant à l’état adulte', 'de l’adulte à l’enfant',
                                            'de l’école à la maison']},
                     {'index': 0}, 'De l’enfant à l’état adulte.'),
                    ('qcm', 1, {'question': 'La puberté concerne…',
                                'options': ['les garçons et les filles', 'les garçons seulement',
                                            'les filles seulement']},
                     {'index': 0}, 'Les deux, à des âges un peu différents.'),
                    ('qcm', 2, {'question': 'Qu’est-ce qui change à la puberté ?',
                                'options': ['Le corps et son fonctionnement', 'La taille seulement',
                                            'La voix seulement', 'Rien du tout']},
                     {'index': 0}, 'Des changements morphologiques et physiologiques.'),
                    ('texte_a_trous', 3,
                     {'text': 'La puberté est le {{1}} de l’enfant à l’état {{2}}.', 'blanks': 2},
                     {'values': ['passage', 'adulte']}, 'Le passage à l’état adulte.'),
                    ('vrai_faux', 4, {'statement': 'La puberté est le passage de l’enfant à l’état adulte.'},
                     {'value': True}, 'C’est la définition du cahier.'),
                ],
            ),
            (
                'date',
                'Les changements commencent entre 12 et 15 ans chez les garçons, entre 11 et 14 ans chez les filles.',
                'pu-ages',
                'Deux règles graduées côte à côte, l’une marquée 12 à 15, l’autre 11 à 14.',
                [
                    ('simple', 'Les filles commencent en général un peu plus tôt que les garçons.'),
                    ('pas_a_pas', 'Garçons : de 12 à 15 ans. Filles : de 11 à 14 ans. Un an d’écart au début comme à la fin.'),
                ],
                [
                    ('qcm', 1, {'question': 'Chez les garçons, les changements commencent entre…',
                                'options': ['12 et 15 ans', '5 et 8 ans', '20 et 25 ans']},
                     {'index': 0}, 'Entre 12 et 15 ans.'),
                    ('qcm', 1, {'question': 'Chez les filles, ils commencent entre…',
                                'options': ['11 et 14 ans', '3 et 6 ans', '18 et 21 ans']},
                     {'index': 0}, 'Entre 11 et 14 ans.'),
                    ('qcm', 2, {'question': 'Qui commence en général le plus tôt ?',
                                'options': ['Les filles', 'Les garçons', 'Personne',
                                            'Les deux au même âge']},
                     {'index': 0}, '11 ans, c’est avant 12 ans.'),
                    ('texte_a_trous', 3,
                     {'text': 'Chez les garçons, entre {{1}} et {{2}} ans.', 'blanks': 2},
                     {'values': ['12', '15']}, 'De 12 à 15 ans.'),
                    ('vrai_faux', 4, {'statement': 'Chez les filles, cela commence entre 11 et 14 ans.'},
                     {'value': True}, 'C’est ce que dit le cahier.'),
                ],
            ),
            (
                'liste',
                'Chez le garçon : les épaules s’élargissent, les muscles se développent, la voix devient grave, des poils apparaissent.',
                'pu-garcon',
                'Quatre pastilles alignées : une barre qui s’élargit, une courbe qui monte, une onde grave, trois traits.',
                [
                    ('simple', 'Quatre changements qu’on voit ou qu’on entend : les épaules, les muscles, la voix, les poils.'),
                    ('visuel', 'La voix devient grave, c’est-à-dire plus basse qu’avant.'),
                ],
                [
                    ('qcm', 1, {'question': 'Chez le garçon, la voix devient…',
                                'options': ['grave', 'fine', 'muette']},
                     {'index': 0}, 'Elle devient grave.'),
                    ('qcm', 1, {'question': 'Chez le garçon, les épaules…',
                                'options': ['s’élargissent', 'rétrécissent', 'disparaissent']},
                     {'index': 0}, 'Elles s’élargissent.'),
                    ('qcm', 2, {'question': 'Lequel est un changement du garçon ?',
                                'options': ['Le développement des muscles', 'Le développement des seins',
                                            'L’élargissement du bassin', 'La voix qui devient fine']},
                     {'index': 0}, 'Les trois autres sont chez la fille.'),
                    ('association', 3, {'question': 'Relie chaque partie à son changement.',
                                        'gauche': ['les épaules', 'la voix', 'les muscles'],
                                        'droite': ['Elles s’élargissent', 'Elle devient grave',
                                                   'Ils se développent']},
                     {'order': [0, 1, 2]}, 'Trois des quatre changements du garçon.'),
                    ('vrai_faux', 4, {'statement': 'Chez le garçon, la voix devient fine.'},
                     {'value': False}, 'Elle devient grave.'),
                ],
            ),
            (
                'liste',
                'Chez la fille : les seins se développent, le bassin s’élargit, la voix devient fine, des poils apparaissent.',
                'pu-fille',
                'Quatre pastilles alignées : une courbe, une barre qui s’élargit, une onde aiguë, trois traits.',
                [
                    ('simple', 'Quatre changements aussi, mais deux diffèrent de ceux du garçon : le bassin et la voix.'),
                    ('analogie', 'La voix devient fine chez la fille, grave chez le garçon : c’est le changement le plus facile à repérer.'),
                ],
                [
                    ('qcm', 1, {'question': 'Chez la fille, la voix devient…',
                                'options': ['fine', 'grave', 'muette']},
                     {'index': 0}, 'Elle devient fine.'),
                    ('qcm', 1, {'question': 'Chez la fille, le bassin…',
                                'options': ['s’élargit', 'rétrécit', 'disparaît']},
                     {'index': 0}, 'Il s’élargit.'),
                    ('qcm', 2, {'question': 'Lequel est un changement de la fille ?',
                                'options': ['L’élargissement du bassin', 'L’élargissement des épaules',
                                            'Le développement des muscles', 'La voix qui devient grave']},
                     {'index': 0}, 'Les trois autres sont chez le garçon.'),
                    ('texte_a_trous', 3,
                     {'text': 'Chez la fille, la voix devient {{1}} et le bassin {{2}}.', 'blanks': 2},
                     {'values': ['fine', 's’élargit']}, 'Fine, et le bassin s’élargit.'),
                    ('vrai_faux', 4,
                     {'statement': 'Les poils apparaissent chez le garçon comme chez la fille.'},
                     {'value': True}, 'C’est le seul changement commun aux deux listes.'),
                ],
            ),
            (
                'relation',
                'Les testicules commencent à produire les spermatozoïdes ; la jeune fille libère des ovules et ses premières règles apparaissent.',
                'pu-cellules',
                'Deux cellules dessinées côte à côte : un disque, et une cellule à longue queue.',
                [
                    ('simple', 'Ce sont les changements physiologiques : on ne les voit pas, ils se passent à l’intérieur.'),
                    ('pas_a_pas', 'Les testicules produisent les spermatozoïdes. Les ovaires libèrent les ovules. Les deux sont des cellules reproductrices.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les testicules produisent…',
                                'options': ['les spermatozoïdes', 'les ovules', 'le sang']},
                     {'index': 0}, 'Les spermatozoïdes.'),
                    ('qcm', 1, {'question': 'La jeune fille libère…',
                                'options': ['les ovules', 'les spermatozoïdes', 'la salive']},
                     {'index': 0}, 'Les ovules.'),
                    ('qcm', 2, {'question': 'Qu’apparaît-il chez la jeune fille ?',
                                'options': ['Les premières règles', 'La barbe', 'Les muscles',
                                            'Rien de nouveau']},
                     {'index': 0}, 'Les premières règles.'),
                    ('association', 3, {'question': 'Relie chaque organe à sa cellule.',
                                        'gauche': ['les testicules', 'les ovaires'],
                                        'droite': ['Les spermatozoïdes', 'Les ovules']},
                     {'order': [0, 1]}, 'Chacun produit sa cellule reproductrice.'),
                    ('vrai_faux', 4,
                     {'statement': 'Les spermatozoïdes et les ovules sont des cellules reproductrices.'},
                     {'value': True}, 'C’est le nom que leur donne le cahier.'),
                ],
            ),
        ],
    ),
    (
        'Les organes reproducteurs', 'Sciences', 'Science de la Vie',
        '2026-10-13', 10,
        'L’appareil reproducteur est l’ensemble des organes qui permettent de se reproduire ; on les '
        'appelle encore organes génitaux. Chez l’homme : le pénis, les deux testicules, les canaux et '
        'la prostate. Chez la femme : la vulve, l’utérus, le vagin et les deux ovaires.',
        'or-organes',
        'Deux cartouches pastel côte à côte, l’un titré « chez l’homme », l’autre « chez la femme ».',
        [
            (
                'definition',
                'L’appareil reproducteur est l’ensemble des organes qui permettent de se reproduire.',
                'or-appareil',
                'Plusieurs petites formes réunies dans un même cadre, pour dire l’ensemble.',
                [
                    ('simple', 'Un appareil, c’est un ensemble d’organes qui travaillent au même but.'),
                    ('visuel', 'On les appelle encore organes génitaux : les deux mots disent la même chose.'),
                ],
                [
                    ('qcm', 1, {'question': 'L’appareil reproducteur permet de…',
                                'options': ['se reproduire', 'respirer', 'marcher']},
                     {'index': 0}, 'De se reproduire.'),
                    ('qcm', 1, {'question': 'On appelle encore ces organes…',
                                'options': ['les organes génitaux', 'les organes des sens', 'les muscles']},
                     {'index': 0}, 'Les organes génitaux.'),
                    ('qcm', 2, {'question': 'Un appareil est…',
                                'options': ['un ensemble d’organes', 'un seul organe', 'un outil', 'un os']},
                     {'index': 0}, 'Un ensemble, pas un seul.'),
                    ('texte_a_trous', 3,
                     {'text': 'L’appareil {{1}} permet de se {{2}}.', 'blanks': 2},
                     {'values': ['reproducteur', 'reproduire']}, 'Reproducteur, pour se reproduire.'),
                    ('vrai_faux', 4,
                     {'statement': 'Organes génitaux et organes reproducteurs désignent la même chose.'},
                     {'value': True}, 'Le cahier donne les deux noms.'),
                ],
            ),
            (
                'liste',
                'Chez l’homme : le pénis, les deux testicules, les canaux et la prostate.',
                'or-homme',
                'Quatre étiquettes empilées portant les quatre noms, sur fond pastel.',
                [
                    ('simple', 'Quatre organes à retenir, chacun avec son rôle.'),
                    ('pas_a_pas', 'Le pénis sert à l’accouplement et à uriner. Les testicules produisent. Les canaux conduisent. La prostate fabrique un liquide.'),
                ],
                [
                    ('qcm', 1, {'question': 'Combien l’homme a-t-il de testicules ?',
                                'options': ['Deux', 'Un', 'Quatre']},
                     {'index': 0}, 'Deux.'),
                    ('qcm', 1, {'question': 'Que produisent les testicules ?',
                                'options': ['Les spermatozoïdes', 'Les ovules', 'Le sang']},
                     {'index': 0}, 'Les spermatozoïdes.'),
                    ('qcm', 2, {'question': 'Que fabrique la prostate ?',
                                'options': ['Un liquide', 'Des os', 'Des ovules', 'De l’air']},
                     {'index': 0}, 'Le liquide qui conduit les spermatozoïdes.'),
                    ('texte_a_trous', 3,
                     {'text': 'Les deux {{1}} produisent les {{2}}.', 'blanks': 2},
                     {'values': ['testicules', 'spermatozoïdes']}, 'Les testicules, les spermatozoïdes.'),
                    ('vrai_faux', 4, {'statement': 'La prostate produit les ovules.'},
                     {'value': False}, 'Elle fabrique un liquide ; les ovules viennent des ovaires.'),
                ],
            ),
            (
                'liste',
                'Chez la femme : la vulve, l’utérus, le vagin et les deux ovaires.',
                'or-femme',
                'Quatre étiquettes empilées portant les quatre noms, sur fond pastel.',
                [
                    ('simple', 'Quatre organes aussi, chacun avec son rôle précis.'),
                    ('pas_a_pas', 'La vulve est l’orifice externe. Le vagin est l’organe d’accouplement. L’utérus accueille la gestation. Les ovaires produisent les ovules.'),
                ],
                [
                    ('qcm', 1, {'question': 'Quel organe produit les ovules ?',
                                'options': ['Les ovaires', 'Les testicules', 'La prostate']},
                     {'index': 0}, 'Les ovaires.'),
                    ('qcm', 1, {'question': 'L’utérus est l’organe de…',
                                'options': ['la gestation', 'la vue', 'la marche']},
                     {'index': 0}, 'La gestation.'),
                    ('qcm', 2, {'question': 'La vulve est…',
                                'options': ['l’orifice externe', 'un os', 'une cellule', 'un muscle du bras']},
                     {'index': 0}, 'L’orifice externe des organes.'),
                    ('association', 3, {'question': 'Relie chaque organe à son rôle.',
                                        'gauche': ['l’utérus', 'les ovaires', 'le vagin'],
                                        'droite': ['La gestation', 'Les ovules', 'L’accouplement']},
                     {'order': [0, 1, 2]}, 'Chacun son rôle.'),
                    ('vrai_faux', 4, {'statement': 'La femme a deux ovaires.'},
                     {'value': True}, 'Deux, comme l’homme a deux testicules.'),
                ],
            ),
            (
                'relation',
                'Chaque organe a son rôle : les testicules produisent les spermatozoïdes, les ovaires les ovules, l’utérus accueille la gestation.',
                'or-roles',
                'Trois paires reliées par des traits : organe à gauche, rôle à droite.',
                [
                    ('simple', 'Retenir le nom ne suffit pas : c’est le rôle qu’on demande en classe.'),
                    ('visuel', 'Produire une cellule, conduire un liquide, accueillir : trois rôles différents.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où se passe la gestation ?',
                                'options': ['Dans l’utérus', 'Dans les ovaires', 'Dans la prostate']},
                     {'index': 0}, 'Dans l’utérus.'),
                    ('qcm', 1, {'question': 'Les canaux servent à…',
                                'options': ['conduire les liquides', 'produire les ovules', 'fabriquer les os']},
                     {'index': 0}, 'À conduire les liquides.'),
                    ('qcm', 2, {'question': 'Quel organe produit une cellule reproductrice ?',
                                'options': ['Les ovaires', 'L’utérus', 'La vulve', 'Les canaux']},
                     {'index': 0}, 'Les ovaires produisent les ovules.'),
                    ('texte_a_trous', 3,
                     {'text': 'Les ovaires produisent les {{1}} et les testicules les {{2}}.', 'blanks': 2},
                     {'values': ['ovules', 'spermatozoïdes']}, 'Ovules et spermatozoïdes.'),
                    ('vrai_faux', 4, {'statement': 'L’utérus produit les spermatozoïdes.'},
                     {'value': False}, 'Il accueille la gestation ; ce sont les testicules qui produisent.'),
                ],
            ),
        ],
    ),
    (
        'Le cycle de l’eau dans la nature', 'Sciences', 'Sciences Physiques et Chimiques',
        '2026-10-14', 11,
        'Le cycle de l’eau est le trajet que parcourt l’eau pour revenir à son point de départ : '
        'l’évaporation sous l’effet de la chaleur, la condensation en nuages au contact du froid, '
        'la précipitation sous forme de pluie, puis l’infiltration et le ruissellement.',
        'ce-cycle',
        'Le cycle complet en une image : soleil, mer, flèche montante, nuage, pluie, ruisseau.',
        [
            (
                'definition',
                'Le cycle de l’eau est le trajet que parcourt l’eau pour revenir à son point de départ.',
                'ce-trajet',
                'Une boucle fermée tracée par une flèche, qui revient à son origine.',
                [
                    ('simple', 'Un cycle, c’est un trajet qui revient là où il a commencé, et qui recommence.'),
                    ('analogie', 'Comme un tour de piste : on repasse toujours par le même point de départ.'),
                ],
                [
                    ('qcm', 1, {'question': 'Un cycle est un trajet qui…',
                                'options': ['revient à son point de départ', 'ne finit jamais',
                                            'va tout droit']},
                     {'index': 0}, 'Il revient à son point de départ.'),
                    ('qcm', 1, {'question': 'Le cycle de l’eau concerne…',
                                'options': ['l’eau', 'l’air seulement', 'les pierres']},
                     {'index': 0}, 'Le trajet de l’eau.'),
                    ('qcm', 2, {'question': 'Combien d’étapes le cahier donne-t-il ?',
                                'options': ['Quatre', 'Deux', 'Six', 'Dix']},
                     {'index': 0}, 'Évaporation, condensation, précipitation, ruissellement.'),
                    ('texte_a_trous', 3,
                     {'text': 'Le cycle de l’eau est le {{1}} que parcourt l’eau pour revenir à son point de {{2}}.',
                      'blanks': 2},
                     {'values': ['trajet', 'départ']}, 'Le trajet, et le point de départ.'),
                    ('vrai_faux', 4, {'statement': 'Le cycle de l’eau recommence sans arrêt.'},
                     {'value': True}, 'C’est ce que veut dire un cycle.'),
                ],
            ),
            (
                'relation',
                'Sous l’effet de la chaleur, l’eau des lacs et des fleuves se transforme en vapeur : c’est l’évaporation.',
                'ce-evaporation',
                'Un soleil, une étendue d’eau, et de fines flèches qui montent.',
                [
                    ('simple', 'La chaleur du soleil fait monter l’eau dans l’air, sous forme de vapeur.'),
                    ('visuel', 'La vapeur ne se voit pas : c’est de l’eau devenue gaz.'),
                ],
                [
                    ('qcm', 1, {'question': 'Qu’est-ce qui fait s’évaporer l’eau ?',
                                'options': ['La chaleur', 'Le froid', 'Le vent seulement']},
                     {'index': 0}, 'La chaleur.'),
                    ('qcm', 1, {'question': 'En s’évaporant, l’eau devient…',
                                'options': ['de la vapeur', 'de la glace', 'du sable']},
                     {'index': 0}, 'De la vapeur.'),
                    ('qcm', 2, {'question': 'Quelle est la première étape du cycle ?',
                                'options': ['L’évaporation', 'La condensation', 'La précipitation',
                                            'Le ruissellement']},
                     {'index': 0}, 'C’est par là que le cahier commence.'),
                    ('texte_a_trous', 3,
                     {'text': 'Sous l’effet de la {{1}}, l’eau se transforme en {{2}}.', 'blanks': 2},
                     {'values': ['chaleur', 'vapeur']}, 'La chaleur, la vapeur.'),
                    ('vrai_faux', 4, {'statement': 'C’est le froid qui fait s’évaporer l’eau.'},
                     {'value': False}, 'C’est la chaleur.'),
                ],
            ),
            (
                'relation',
                'Au contact des zones froides, la vapeur se transforme en nuage : c’est la condensation.',
                'ce-condensation',
                'De la vapeur qui monte et rencontre une bande froide, puis devient un nuage.',
                [
                    ('simple', 'En haut il fait froid : la vapeur redevient de minuscules gouttes, et cela fait un nuage.'),
                    ('analogie', 'Comme la buée sur une vitre froide : la vapeur redevient de l’eau.'),
                ],
                [
                    ('qcm', 1, {'question': 'La condensation transforme la vapeur en…',
                                'options': ['nuage', 'pierre', 'vent']},
                     {'index': 0}, 'En nuage.'),
                    ('qcm', 1, {'question': 'La condensation se produit au contact…',
                                'options': ['des zones froides', 'du sol chaud', 'du sable']},
                     {'index': 0}, 'Des zones froides.'),
                    ('qcm', 2, {'question': 'Où se répand la vapeur avant de se condenser ?',
                                'options': ['Dans l’atmosphère', 'Dans le sol', 'Dans les racines',
                                            'Dans les pierres']},
                     {'index': 0}, 'Dans l’atmosphère.'),
                    ('texte_a_trous', 3,
                     {'text': 'Au contact des zones {{1}}, la vapeur devient un {{2}}.', 'blanks': 2},
                     {'values': ['froides', 'nuage']}, 'Froides, et un nuage.'),
                    ('vrai_faux', 4, {'statement': 'La condensation vient après l’évaporation.'},
                     {'value': True}, 'C’est la deuxième étape.'),
                ],
            ),
            (
                'relation',
                'L’eau tombe sous forme de pluie : c’est la précipitation. La pluie s’infiltre ensuite dans le sol.',
                'ce-precipitation',
                'Un nuage, des traits de pluie, et des flèches qui entrent dans le sol.',
                [
                    ('simple', 'Le nuage devient trop lourd : l’eau retombe en pluie, puis entre dans la terre.'),
                    ('pas_a_pas', 'D’abord elle tombe, c’est la précipitation. Ensuite elle entre dans le sol, c’est l’infiltration.'),
                ],
                [
                    ('qcm', 1, {'question': 'La précipitation, c’est l’eau qui…',
                                'options': ['tombe en pluie', 'monte en vapeur', 'reste dans le nuage']},
                     {'index': 0}, 'Elle tombe en pluie.'),
                    ('qcm', 1, {'question': 'Après être tombée, la pluie…',
                                'options': ['s’infiltre dans le sol', 'remonte au nuage', 'disparaît']},
                     {'index': 0}, 'Elle s’infiltre dans le sol.'),
                    ('qcm', 2, {'question': 'Quelle étape vient juste avant la précipitation ?',
                                'options': ['La condensation', 'L’évaporation', 'Le ruissellement',
                                            'L’infiltration']},
                     {'index': 0}, 'Le nuage se forme d’abord.'),
                    ('texte_a_trous', 3,
                     {'text': 'L’eau tombe sous forme de {{1}}, puis elle s’{{2}} dans le sol.', 'blanks': 2},
                     {'values': ['pluie', 'infiltre']}, 'La pluie, puis l’infiltration.'),
                    ('vrai_faux', 4, {'statement': 'La pluie reste toujours à la surface du sol.'},
                     {'value': False}, 'Une partie s’infiltre.'),
                ],
            ),
            (
                'relation',
                'L’eau ruisselle et se retrouve dans les mers, les lacs et les fleuves, et le cycle recommence.',
                'ce-ruissellement',
                'Des filets d’eau qui descendent une pente jusqu’à une étendue, et une flèche de retour.',
                [
                    ('simple', 'Ruisseler, c’est couler à la surface. L’eau rejoint les mers, et tout repart.'),
                    ('visuel', 'C’est la dernière étape, et c’est elle qui referme la boucle.'),
                ],
                [
                    ('qcm', 1, {'question': 'Ruisseler, c’est…',
                                'options': ['couler à la surface', 'monter dans l’air', 'geler']},
                     {'index': 0}, 'Couler à la surface.'),
                    ('qcm', 1, {'question': 'Où l’eau se retrouve-t-elle à la fin ?',
                                'options': ['Dans les mers et les fleuves', 'Dans les nuages',
                                            'Dans le feu']},
                     {'index': 0}, 'Dans les mers, les lacs et les fleuves.'),
                    ('qcm', 2, {'question': 'Que se passe-t-il une fois l’eau revenue ?',
                                'options': ['Le cycle recommence', 'Le cycle s’arrête',
                                            'L’eau disparaît', 'Elle gèle pour toujours']},
                     {'index': 0}, 'Le cycle recommence.'),
                    ('chronologie', 3, {'question': 'Remets les quatre étapes dans l’ordre.',
                                        'tokens': ['évaporation', 'condensation', 'précipitation',
                                                   'ruissellement'],
                                        'consigne': 'Touche-les dans l’ordre du cahier.'},
                     {'order': [0, 1, 2, 3]}, 'C’est l’ordre des quatre étapes.'),
                    ('vrai_faux', 4, {'statement': 'Le ruissellement ramène l’eau vers les mers.'},
                     {'value': True}, 'Et le cycle repart de là.'),
                ],
            ),
        ],
    ),
    (
        'L’eau potable', 'Sciences', 'Science de la Vie', '2026-10-15', 12,
        'Une eau potable est celle qu’on peut boire sans danger pour notre santé. Pour rendre une eau '
        'potable, on peut la javelliser et la filtrer, la bouillir et la filtrer, ou la javelliser et '
        'la décanter. L’eau maintient la température du corps, transporte les nutriments et évacue '
        'les déchets.',
        'ep-potable',
        'Un verre d’eau claire posé près d’un verre d’eau trouble barré.',
        [
            (
                'definition',
                'Une eau potable est celle qu’on peut boire sans danger pour notre santé.',
                'ep-definition',
                'Un verre d’eau claire avec une coche, et un verre trouble avec une croix.',
                [
                    ('simple', 'Potable veut dire qu’on peut la boire sans tomber malade.'),
                    ('visuel', 'Une eau claire n’est pas forcément potable : on ne voit pas les microbes.'),
                ],
                [
                    ('qcm', 1, {'question': 'Une eau potable est une eau…',
                                'options': ['qu’on peut boire sans danger', 'qui sert à laver',
                                            'qu’on ne touche pas']},
                     {'index': 0}, 'Qu’on peut boire sans danger.'),
                    ('qcm', 1, {'question': 'Potable veut dire…',
                                'options': ['bonne à boire', 'bonne à jeter', 'bonne à chauffer']},
                     {'index': 0}, 'Bonne à boire.'),
                    ('qcm', 2, {'question': 'Une eau claire est-elle toujours potable ?',
                                'options': ['Non', 'Oui', 'Seulement en ville', 'Seulement au village']},
                     {'index': 0}, 'On ne voit pas les microbes.'),
                    ('texte_a_trous', 3,
                     {'text': 'Une eau {{1}} est celle qu’on peut {{2}} sans danger.', 'blanks': 2},
                     {'values': ['potable', 'boire']}, 'Potable, et boire.'),
                    ('vrai_faux', 4, {'statement': 'Une eau potable peut être bue sans danger.'},
                     {'value': True}, 'C’est la définition.'),
                ],
            ),
            (
                'liste',
                'Pour rendre une eau potable, on peut la javelliser et la filtrer, la bouillir et la filtrer, ou la javelliser et la décanter.',
                'ep-traiter',
                'Trois paires de pictogrammes : goutte et entonnoir, flamme et entonnoir, goutte et bocal au repos.',
                [
                    ('simple', 'Trois manières, et chacune combine deux gestes.'),
                    ('pas_a_pas', 'Javelliser tue les microbes, bouillir aussi. Filtrer retient les saletés, décanter les laisse tomber au fond.'),
                ],
                [
                    ('qcm', 1, {'question': 'Que peut-on faire pour rendre une eau potable ?',
                                'options': ['La bouillir et la filtrer', 'La saler', 'La secouer']},
                     {'index': 0}, 'Bouillir et filtrer.'),
                    ('qcm', 1, {'question': 'Javelliser sert à…',
                                'options': ['tuer les microbes', 'ajouter du goût', 'refroidir l’eau']},
                     {'index': 0}, 'À tuer les microbes.'),
                    ('qcm', 2, {'question': 'Décanter, c’est…',
                                'options': ['laisser les saletés tomber au fond', 'faire bouillir',
                                            'ajouter du sucre', 'verser dans un verre']},
                     {'index': 0}, 'Les laisser se déposer au fond.'),
                    ('texte_a_trous', 3,
                     {'text': 'On peut {{1}} l’eau et la {{2}} pour la rendre potable.', 'blanks': 2},
                     {'values': ['bouillir', 'filtrer']}, 'Bouillir et filtrer.'),
                    ('vrai_faux', 4, {'statement': 'Filtrer une eau suffit toujours à la rendre potable.'},
                     {'value': False}, 'Le cahier associe toujours deux gestes.'),
                ],
            ),
            (
                'liste',
                'L’eau maintient la température du corps, facilite le transport des nutriments et l’évacuation des déchets.',
                'ep-roles',
                'Trois pastilles : un thermomètre, une flèche de transport, une flèche de sortie.',
                [
                    ('simple', 'Trois rôles dans le corps : la température, le transport, l’évacuation.'),
                    ('visuel', 'C’est pour cela qu’on doit boire tous les jours, même sans avoir soif.'),
                ],
                [
                    ('qcm', 1, {'question': 'L’eau maintient dans le corps…',
                                'options': ['la température', 'la couleur', 'le bruit']},
                     {'index': 0}, 'La température ambiante.'),
                    ('qcm', 1, {'question': 'L’eau facilite le transport…',
                                'options': ['des nutriments', 'des os', 'des cheveux']},
                     {'index': 0}, 'Des nutriments.'),
                    ('qcm', 2, {'question': 'Quel est le troisième rôle de l’eau ?',
                                'options': ['Évacuer les déchets', 'Faire grandir les ongles',
                                            'Donner la voix', 'Colorer la peau']},
                     {'index': 0}, 'L’évacuation des déchets.'),
                    ('texte_a_trous', 3,
                     {'text': 'L’eau transporte les {{1}} et évacue les {{2}}.', 'blanks': 2},
                     {'values': ['nutriments', 'déchets']}, 'Nutriments et déchets.'),
                    ('vrai_faux', 4, {'statement': 'L’eau sert seulement à étancher la soif.'},
                     {'value': False}, 'Elle a trois rôles dans l’organisme.'),
                ],
            ),
        ],
    ),
    (
        'L’amélioration des sols : le compost', 'Sciences', 'Sciences Agricoles',
        '2026-10-16', 13,
        'On peut enrichir un sol pauvre en utilisant le compost, un engrais naturel fabriqué à partir '
        'de matières provenant des animaux et des végétaux. Les éléments qui entrent dans sa '
        'composition sont biodégradables : feuilles mortes, cendre de bois, restes de repas, '
        'épluchures de tubercules, litière d’animaux.',
        'co-compost',
        'Un tas de compost en coupe, avec des couches de matières différentes.',
        [
            (
                'definition',
                'Le compost est un engrais naturel fabriqué à partir de matières provenant des animaux et des végétaux.',
                'co-definition',
                'Un cadre portant deux origines : une silhouette de feuille et une silhouette d’animal.',
                [
                    ('simple', 'Naturel, parce qu’il est fait de ce qui vient des plantes et des bêtes, pas d’une usine.'),
                    ('visuel', 'Un engrais nourrit la terre, comme un repas nourrit un enfant.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le compost est un engrais…',
                                'options': ['naturel', 'chimique', 'minéral']},
                     {'index': 0}, 'Naturel.'),
                    ('qcm', 1, {'question': 'Le compost vient de matières…',
                                'options': ['animales et végétales', 'de plastique', 'de métal']},
                     {'index': 0}, 'Des animaux et des végétaux.'),
                    ('qcm', 2, {'question': 'À quoi sert un engrais ?',
                                'options': ['À nourrir le sol', 'À arroser', 'À couper l’herbe',
                                            'À chasser les oiseaux']},
                     {'index': 0}, 'À nourrir le sol.'),
                    ('texte_a_trous', 3,
                     {'text': 'Le compost est un engrais {{1}} fait de matières animales et {{2}}.',
                      'blanks': 2},
                     {'values': ['naturel', 'végétales']}, 'Naturel, animales et végétales.'),
                    ('vrai_faux', 4, {'statement': 'Le compost est fabriqué dans une usine.'},
                     {'value': False}, 'C’est un engrais naturel.'),
                ],
            ),
            (
                'relation',
                'On peut enrichir un sol pauvre en utilisant le compost.',
                'co-enrichir',
                'Deux carrés de terre côte à côte : l’un clair et nu, l’autre sombre avec une pousse.',
                [
                    ('simple', 'Un sol pauvre ne nourrit plus les plantes. Le compost lui rend ce qui lui manque.'),
                    ('analogie', 'C’est le repas du sol : sans lui, la plante pousse mal.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le compost sert à…',
                                'options': ['enrichir un sol pauvre', 'assécher un sol', 'durcir un sol']},
                     {'index': 0}, 'À l’enrichir.'),
                    ('qcm', 1, {'question': 'Un sol pauvre est un sol…',
                                'options': ['qui manque d’éléments nourriciers', 'trop mouillé',
                                            'trop grand']},
                     {'index': 0}, 'Il lui manque de quoi nourrir les plantes.'),
                    ('qcm', 2, {'question': 'Que devient un sol pauvre avec du compost ?',
                                'options': ['Il s’enrichit', 'Il s’appauvrit', 'Il disparaît',
                                            'Il ne change pas']},
                     {'index': 0}, 'Il s’enrichit.'),
                    ('texte_a_trous', 3,
                     {'text': 'On peut {{1}} un sol pauvre en utilisant le {{2}}.', 'blanks': 2},
                     {'values': ['enrichir', 'compost']}, 'Enrichir, avec le compost.'),
                    ('vrai_faux', 4, {'statement': 'Le compost appauvrit le sol.'},
                     {'value': False}, 'Il l’enrichit.'),
                ],
            ),
            (
                'liste',
                'Les éléments du compost sont biodégradables : feuilles mortes, cendre de bois, restes de repas, épluchures de tubercules, litière d’animaux.',
                'co-elements',
                'Cinq pastilles en ligne : feuille, cendre, assiette, épluchure, paille.',
                [
                    ('simple', 'Cinq éléments, et tous se décomposent dans la terre.'),
                    ('visuel', 'Biodégradable veut dire que la nature peut le défaire toute seule.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les éléments du compost sont…',
                                'options': ['biodégradables', 'en plastique', 'en verre']},
                     {'index': 0}, 'Biodégradables.'),
                    ('qcm', 1, {'question': 'Lequel entre dans le compost ?',
                                'options': ['Les feuilles mortes', 'Les sachets plastiques',
                                            'Les boîtes de conserve']},
                     {'index': 0}, 'Les feuilles mortes.'),
                    ('qcm', 2, {'question': 'Lequel n’est pas dans la liste du cahier ?',
                                'options': ['Le sable', 'La cendre de bois', 'Les restes de repas',
                                            'La litière d’animaux']},
                     {'index': 0}, 'Le sable ne se décompose pas.'),
                    ('texte_a_trous', 3,
                     {'text': 'On peut citer les feuilles {{1}} et la {{2}} de bois.', 'blanks': 2},
                     {'values': ['mortes', 'cendre']}, 'Feuilles mortes, cendre de bois.'),
                    ('vrai_faux', 4, {'statement': 'Les épluchures de tubercules entrent dans le compost.'},
                     {'value': True}, 'Elles sont dans la liste.'),
                ],
            ),
        ],
    ),
    (
        'La lampe à pétrole', 'Technologie', 'Technologie', None, 14,
        'La lampe à pétrole, encore appelée lampe tempête, est un appareil d’éclairage qui a pour '
        'source d’énergie le pétrole. Elle a cinq parties essentielles : le réservoir, la molette, '
        'la mèche, le verre et la grille d’aération.',
        'la-lampe',
        'Une lampe tempête dessinée de face, ses cinq parties repérées par des traits.',
        [
            (
                'definition',
                'La lampe à pétrole, encore appelée lampe tempête, est un appareil d’éclairage dont la source d’énergie est le pétrole.',
                'la-definition',
                'La lampe entière, posée, avec sa flamme allumée.',
                [
                    ('simple', 'Un appareil d’éclairage : il sert à faire de la lumière.'),
                    ('histoire', 'On l’appelle lampe tempête parce que son verre protège la flamme du vent.'),
                ],
                [
                    ('qcm', 1, {'question': 'La lampe à pétrole est un appareil…',
                                'options': ['d’éclairage', 'de cuisson', 'de mesure']},
                     {'index': 0}, 'D’éclairage.'),
                    ('qcm', 1, {'question': 'Sa source d’énergie est…',
                                'options': ['le pétrole', 'l’électricité', 'le vent']},
                     {'index': 0}, 'Le pétrole.'),
                    ('qcm', 2, {'question': 'On l’appelle aussi…',
                                'options': ['lampe tempête', 'lampe de poche', 'lampe solaire',
                                            'lampe de table']},
                     {'index': 0}, 'Lampe tempête.'),
                    ('texte_a_trous', 3,
                     {'text': 'La lampe à pétrole est un appareil d’{{1}} dont la source d’énergie est le {{2}}.',
                      'blanks': 2},
                     {'values': ['éclairage', 'pétrole']}, 'Éclairage, et pétrole.'),
                    ('vrai_faux', 4, {'statement': 'La lampe tempête marche à l’électricité.'},
                     {'value': False}, 'Elle marche au pétrole.'),
                ],
            ),
            (
                'liste',
                'Elle a cinq parties essentielles : le réservoir, la molette, la mèche, le verre et la grille d’aération.',
                'la-parties',
                'La lampe avec ses cinq parties numérotées de 1 à 5.',
                [
                    ('simple', 'Cinq parties, à savoir nommer dans l’ordre.'),
                    ('pas_a_pas', 'En partant du bas : le réservoir, la molette, la mèche, le verre, puis la grille au-dessus.'),
                ],
                [
                    ('qcm', 1, {'question': 'Combien la lampe a-t-elle de parties essentielles ?',
                                'options': ['Cinq', 'Trois', 'Huit']},
                     {'index': 0}, 'Cinq.'),
                    ('qcm', 1, {'question': 'Laquelle est une partie de la lampe ?',
                                'options': ['La mèche', 'La roue', 'Le manche']},
                     {'index': 0}, 'La mèche.'),
                    ('qcm', 2, {'question': 'Laquelle ne fait pas partie de la lampe ?',
                                'options': ['L’interrupteur', 'Le réservoir', 'La molette',
                                            'La grille d’aération']},
                     {'index': 0}, 'Une lampe à pétrole n’a pas d’interrupteur.'),
                    ('chronologie', 3, {'question': 'Range les parties du bas vers le haut.',
                                        'tokens': ['le réservoir', 'la molette', 'la mèche',
                                                   'le verre', 'la grille'],
                                        'consigne': 'Touche-les dans l’ordre.'},
                     {'order': [0, 1, 2, 3, 4]}, 'Du réservoir à la grille.'),
                    ('vrai_faux', 4, {'statement': 'Le verre est une des cinq parties.'},
                     {'value': True}, 'Il protège la flamme.'),
                ],
            ),
            (
                'relation',
                'Chaque partie a son rôle : le réservoir contient le pétrole, la molette règle la flamme, la mèche la porte, le verre la protège et la grille laisse circuler l’air.',
                'la-roles',
                'Cinq paires reliées : la partie à gauche, son rôle à droite.',
                [
                    ('simple', 'Savoir nommer ne suffit pas : c’est le rôle de chaque partie qu’on demande.'),
                    ('pas_a_pas', 'Le pétrole est stocké, monte par la mèche, brûle en flamme, la flamme est protégée, et l’air entre par la grille.'),
                ],
                [
                    ('qcm', 1, {'question': 'Que contient le réservoir ?',
                                'options': ['Le pétrole', 'L’eau', 'L’air']},
                     {'index': 0}, 'Le pétrole.'),
                    ('qcm', 1, {'question': 'À quoi sert la molette ?',
                                'options': ['À régler la flamme', 'À porter la lampe',
                                            'À casser le verre']},
                     {'index': 0}, 'À régler la flamme.'),
                    ('qcm', 2, {'question': 'À quoi sert la grille d’aération ?',
                                'options': ['À laisser circuler l’air', 'À éteindre la flamme',
                                            'À garder le pétrole', 'À décorer']},
                     {'index': 0}, 'L’air circule et la flamme reste allumée.'),
                    ('association', 3, {'question': 'Relie chaque partie à son rôle.',
                                        'gauche': ['le réservoir', 'la mèche', 'le verre'],
                                        'droite': ['Il contient le pétrole', 'Elle porte la flamme',
                                                   'Il protège du vent']},
                     {'order': [0, 1, 2]}, 'Trois des cinq rôles.'),
                    ('vrai_faux', 4, {'statement': 'La mèche fait monter le pétrole.'},
                     {'value': True}, 'Elle le fait monter et porte la flamme.'),
                ],
            ),
        ],
    ),
]

NIVEAUX_ATTENDUS = {1, 2, 3, 4}


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total = set(), 0
    for titre, matiere, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
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
                    assert len(payload['statement']) <= 100, payload
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                elif ikind == 'dictee':
                    assert payload['phrase'] == answer['phrase'], payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))
    return len(cles), total


def paquet():
    return {
        'classe': CLASSE, 'enfant': ENFANT,
        'lecons': [
            {
                'title': titre, 'matiere': matiere, 'chapter': chapitre,
                'taught_on': date, 'sort_order': ordre, 'summary': resume,
                'illustration': img, 'illustration_prompt': FIGURE + prompt,
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
            for titre, matiere, chapitre, date, ordre, resume, img, prompt, notions in LECONS
        ],
    }


if __name__ == '__main__':
    images, items = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-sciences.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    notions = sum(len(l[8]) for l in LECONS)
    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, matiere, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-42s %-12s %-28s %-10s %d notions'
              % (titre, matiere, chapitre, date or 'sans date', len(ns)))
    print(chemin)
