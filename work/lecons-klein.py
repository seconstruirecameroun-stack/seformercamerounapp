# -*- coding: utf-8 -*-
"""
Les six leçons du cahier de KLEIN (CE1), du 13 au 15 octobre 2026.

Transcrites depuis six photos. La fonction d'extraction n'étant toujours pas
déployée, la transcription et la structuration sont faites à la main — mais
dans le format exact qu'elle produira : un résumé court, des notions typées
d'une phrase, des explications, des questions par niveau, et une consigne
d'image par notion.

Rien n'est ajouté au cahier. Les mots, les listes et les chiffres sont ceux
des pages. Les seules corrections sont orthographiques et grammaticales :
« Une enfant obéissant » devient « Un enfant obéissant », les accents
manquants sont remis, et la dernière phrase de l'obéissance, laissée en
suspens dans le cahier (« Si nous voulons réussir dans la vie [...]
obéissance »), est rétablie au plus près de ce qui est écrit.

KLEIN est en CE1, pas en CM1 : les questions sont plus courtes, les mots plus
simples, et les textes à trous ne demandent jamais plus de deux mots.

Usage :  python work/lecons-klein.py
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, '
    'no numbers, no watermark, no real person, no brand. '
)

# Une leçon : (matière, couleur, titre, résumé, image, consigne d'image, notions)
# Une notion : (kind, phrase, image, consigne, [explications], [questions])
# Une explication : (registre, texte)
# Une question : (kind, niveau, payload, answer, explain)

LECONS = [
    (
        'Éducation morale', '#c2708f',
        'L’obéissance',
        'L’obéissance, c’est exécuter les ordres et les consignes d’un aîné sans discuter. '
        'Un enfant obéissant est aimé de tout le monde. Si nous voulons réussir dans la vie, obéissons.',
        'ob-ecoute',
        'A child listening attentively to a kind adult who is pointing at a tidy room, both smiling, warm morning light.',
        [
            (
                'definition',
                'L’obéissance est le fait d’exécuter les ordres et les consignes d’un aîné sans discuter.',
                'ob-consigne',
                'A grown-up hand gently pointing the way and a small child nodding, simple scene, plain soft background.',
                [
                    ('simple', 'Obéir, c’est faire ce qu’un aîné demande, tout de suite et sans discuter.'),
                    ('analogie', 'C’est comme au football : quand l’arbitre siffle, on s’arrête sans discuter.'),
                ],
                [
                    ('qcm', 1, {'question': 'Obéir, c’est…', 'options': ['faire ce qu’un aîné demande', 'discuter longtemps', 'partir en courant']},
                     {'index': 0}, 'Obéir, c’est faire ce qu’on demande.'),
                    ('qcm', 1, {'question': 'Quand un aîné donne une consigne, j’obéis…', 'options': ['sans discuter', 'en discutant', 'demain']},
                     {'index': 0}, 'Sans discuter.'),
                    ('qcm', 2, {'question': 'Qui donne les consignes que l’on doit suivre ?', 'options': ['Un aîné', 'Un bébé', 'Un chat', 'Personne']},
                     {'index': 0}, 'Un aîné : un plus grand que nous.'),
                    ('qcm', 2, {'question': 'Que fait un enfant obéissant ?', 'options': ['Il exécute les ordres sans discuter', 'Il refuse les ordres', 'Il discute chaque consigne', 'Il fait semblant d’écouter']},
                     {'index': 0}, 'Il exécute sans discuter.'),
                    ('texte_a_trous', 3, {'text': 'L’obéissance, c’est exécuter les ordres d’un {{1}} sans {{2}}.', 'blanks': 2},
                     {'values': ['aîné', 'discuter']}, 'D’un aîné, sans discuter.'),
                    ('qcm', 3, {'question': 'Ton grand frère te demande de ranger. Que fais-tu ?', 'options': ['Je range tout de suite', 'Je discute longtemps', 'Je fais autre chose', 'Je me cache']},
                     {'index': 0}, 'On exécute la consigne d’un aîné.'),
                ],
            ),
            (
                'relation',
                'Un enfant obéissant est aimé de tout le monde.',
                'ob-aime',
                'A smiling child surrounded by three happy family members, soft hearts floating, plain soft background.',
                [
                    ('simple', 'Quand tu obéis, les autres sont contents de toi et t’aiment.'),
                ],
                [
                    ('qcm', 1, {'question': 'Un enfant obéissant est…', 'options': ['aimé de tout le monde', 'grondé tous les jours', 'oublié']},
                     {'index': 0}, 'Il est aimé de tout le monde.'),
                    ('qcm', 1, {'question': 'Qui aime un enfant obéissant ?', 'options': ['Tout le monde', 'Personne', 'Les animaux seulement']},
                     {'index': 0}, 'Tout le monde.'),
                    ('qcm', 2, {'question': 'Pourquoi aime-t-on un enfant obéissant ?', 'options': ['Il fait ce qu’on lui demande', 'Il crie très fort', 'Il court très vite', 'Il mange beaucoup']},
                     {'index': 0}, 'Parce qu’il fait ce qu’on lui demande.'),
                    ('texte_a_trous', 3, {'text': 'Un enfant obéissant est {{1}} de tout le monde.', 'blanks': 1},
                     {'values': ['aimé']}, 'Aimé de tout le monde.'),
                ],
            ),
            (
                'relation',
                'Si nous voulons réussir dans la vie, obéissons.',
                'ob-reussir',
                'A child climbing three soft steps towards a glowing star, simple and encouraging, plain soft background.',
                [
                    ('simple', 'Obéir aujourd’hui aide à réussir plus tard.'),
                ],
                [
                    ('qcm', 1, {'question': 'Pour réussir dans la vie, il faut…', 'options': ['obéir', 'désobéir', 'dormir toute la journée']},
                     {'index': 0}, 'Il faut obéir.'),
                    ('qcm', 2, {'question': 'Que nous apporte l’obéissance ?', 'options': ['Elle nous aide à réussir dans la vie', 'Elle fait perdre du temps', 'Elle fâche les aînés', 'Elle rend triste']},
                     {'index': 0}, 'Elle aide à réussir.'),
                    ('texte_a_trous', 3, {'text': 'Si nous voulons {{1}} dans la vie, obéissons.', 'blanks': 1},
                     {'values': ['réussir']}, 'Réussir.'),
                ],
            ),
        ],
    ),
    (
        'Droits et devoirs', '#5b8ac2',
        'Le droit à l’identité',
        'Chaque enfant a droit à une identité. L’identité lui confère un nom et une nationalité.',
        'id-identite',
        'A friendly open booklet with a child portrait drawn on it and a small flag beside, plain soft background.',
        [
            (
                'definition',
                'Chaque enfant a droit à une identité.',
                'id-enfant',
                'Three children of different looks standing side by side, each with a soft glowing badge on the chest, plain background.',
                [
                    ('simple', 'Tous les enfants, sans exception, ont droit à une identité.'),
                    ('analogie', 'C’est comme une étiquette sur ton cartable : elle dit que ce cartable est à toi.'),
                ],
                [
                    ('qcm', 1, {'question': 'Qui a droit à une identité ?', 'options': ['Chaque enfant', 'Seulement les grands', 'Personne']},
                     {'index': 0}, 'Chaque enfant.'),
                    ('qcm', 1, {'question': 'Avoir une identité, c’est un…', 'options': ['droit', 'jeu', 'cadeau de fête']},
                     {'index': 0}, 'C’est un droit.'),
                    ('qcm', 2, {'question': 'L’identité est…', 'options': ['un droit de chaque enfant', 'un cadeau d’anniversaire', 'une punition', 'un jouet']},
                     {'index': 0}, 'Un droit, pour chaque enfant.'),
                    ('texte_a_trous', 3, {'text': 'Chaque enfant a droit à une {{1}}.', 'blanks': 1},
                     {'values': ['identité']}, 'Une identité.'),
                ],
            ),
            (
                'liste',
                'L’identité confère un nom et une nationalité.',
                'id-nom-nation',
                'A name card next to a small waving flag, joined by a soft ribbon, plain soft background.',
                [
                    ('simple', 'Ton identité te donne deux choses : un nom et une nationalité.'),
                ],
                [
                    ('qcm', 1, {'question': 'L’identité donne un nom et une…', 'options': ['nationalité', 'voiture', 'maison']},
                     {'index': 0}, 'Un nom et une nationalité.'),
                    ('qcm', 1, {'question': 'Mon nom fait partie de…', 'options': ['mon identité', 'mon école', 'mon jeu']},
                     {'index': 0}, 'Le nom fait partie de l’identité.'),
                    ('qcm', 2, {'question': 'Que confère l’identité ?', 'options': ['Un nom et une nationalité', 'Un nom et une maison', 'Une nationalité et un vélo', 'Un âge et une taille']},
                     {'index': 0}, 'Un nom et une nationalité.'),
                    ('qcm', 2, {'question': 'Être camerounais, c’est quelle partie de l’identité ?', 'options': ['La nationalité', 'Le nom', 'L’âge', 'La taille']},
                     {'index': 0}, 'C’est la nationalité.'),
                    ('texte_a_trous', 3, {'text': 'L’identité confère un {{1}} et une {{2}}.', 'blanks': 2},
                     {'values': ['nom', 'nationalité']}, 'Un nom et une nationalité.'),
                ],
            ),
        ],
    ),
    (
        'Éducation civique', '#3f9d8f',
        'L’intégration nationale',
        'L’intégration nationale est un mélange des cultures et des traditions au sein d’une population. '
        'Au Cameroun, plus de 250 ethnies vivent dans la paix et l’harmonie, à travers les mariages '
        'interethniques, la cohabitation des peuples et les affectations des travailleurs.',
        'in-cameroun',
        'A joyful crowd of children in varied traditional clothes holding hands in a wide circle, plain soft background.',
        [
            (
                'definition',
                'L’intégration nationale est un mélange des cultures et des traditions au sein d’une population.',
                'in-melange',
                'Several coloured ribbons braiding together into one wide ribbon, plain soft background.',
                [
                    ('simple', 'C’est quand des cultures et des traditions différentes se mélangent dans un même pays.'),
                    ('analogie', 'C’est comme un plat de famille : chacun apporte un ingrédient, et on mange ensemble.'),
                ],
                [
                    ('qcm', 1, {'question': 'L’intégration nationale, c’est un mélange de…', 'options': ['cultures et de traditions', 'voitures', 'animaux']},
                     {'index': 0}, 'Des cultures et des traditions.'),
                    ('qcm', 1, {'question': 'L’intégration nationale concerne…', 'options': ['une population', 'une seule famille', 'un seul enfant']},
                     {'index': 0}, 'Toute une population.'),
                    ('qcm', 2, {'question': 'Qu’est-ce que l’intégration nationale ?', 'options': ['Le mélange des cultures et des traditions d’une population', 'Un jeu d’équipe', 'Un voyage à l’étranger', 'Une fête d’école']},
                     {'index': 0}, 'Un mélange des cultures et des traditions.'),
                    ('texte_a_trous', 3, {'text': 'L’intégration nationale est un mélange des {{1}} et des {{2}}.', 'blanks': 2},
                     {'values': ['cultures', 'traditions']}, 'Des cultures et des traditions.'),
                ],
            ),
            (
                'relation',
                'Au Cameroun, plus de 250 ethnies vivent dans la paix et l’harmonie.',
                'in-ethnies',
                'A soft map shape of a country filled with many small coloured houses living side by side, plain background.',
                [
                    ('simple', 'Le Cameroun compte plus de 250 ethnies, et elles vivent en paix.'),
                ],
                [
                    ('qcm', 1, {'question': 'Au Cameroun, il y a plus de…', 'options': ['250 ethnies', '2 ethnies', '10 ethnies']},
                     {'index': 0}, 'Plus de 250 ethnies.'),
                    ('qcm', 1, {'question': 'Au Cameroun, les ethnies vivent dans…', 'options': ['la paix', 'la dispute', 'la peur']},
                     {'index': 0}, 'Dans la paix et l’harmonie.'),
                    ('qcm', 2, {'question': 'Combien d’ethnies compte le Cameroun ?', 'options': ['Plus de 250', 'Moins de 10', 'Exactement 50', 'Une seule']},
                     {'index': 0}, 'Plus de 250.'),
                    ('texte_a_trous', 3, {'text': 'Au Cameroun, plus de {{1}} ethnies vivent dans la paix.', 'blanks': 1},
                     {'values': ['250']}, 'Plus de 250.'),
                ],
            ),
            (
                'liste',
                'L’intégration nationale se fait à travers les mariages interethniques, la cohabitation des peuples et les affectations des travailleurs.',
                'in-moyens',
                'Three simple pictures side by side: two hands with wedding rings, two neighbouring houses, and a travelling bag with a bus, plain background.',
                [
                    ('simple', 'Trois choses rapprochent les peuples : les mariages entre ethnies, le fait de vivre côte à côte, et les travailleurs envoyés dans d’autres régions.'),
                ],
                [
                    ('qcm', 1, {'question': 'Quand deux personnes de deux ethnies se marient, cela aide…', 'options': ['l’intégration nationale', 'la dispute', 'personne']},
                     {'index': 0}, 'C’est un mariage interethnique.'),
                    ('qcm', 1, {'question': 'Vivre côte à côte avec d’autres peuples, c’est la…', 'options': ['cohabitation', 'séparation', 'dispute']},
                     {'index': 0}, 'C’est la cohabitation.'),
                    ('qcm', 2, {'question': 'Lequel n’aide PAS l’intégration nationale ?', 'options': ['Refuser les autres ethnies', 'Les mariages interethniques', 'La cohabitation des peuples', 'Les affectations des travailleurs']},
                     {'index': 0}, 'Refuser les autres sépare au lieu de rassembler.'),
                    ('chronologie', 3, {'question': 'Remets les trois moyens dans l’ordre du cahier.',
                                        'tokens': ['Les mariages interethniques', 'La cohabitation des peuples', 'Les affectations des travailleurs']},
                     {'order': [0, 1, 2]}, 'Mariages, cohabitation, affectations.'),
                    ('texte_a_trous', 3, {'text': 'La {{1}} des peuples aide l’intégration nationale.', 'blanks': 1},
                     {'values': ['cohabitation']}, 'La cohabitation.'),
                ],
            ),
        ],
    ),
    (
        'Technologies', '#d08a3c',
        'Les techniques de filtrage de l’eau',
        'On peut réaliser un filtre à eau avec une demi-bouteille, du sable, du coton, du charbon et du '
        'gravier. L’eau non potable entre par le haut, traverse le gravier, le charbon, le sable puis le '
        'coton, et l’eau potable sort en bas.',
        'fi-filtre',
        'A half plastic bottle turned upside down as a water filter, layers of gravel, charcoal, sand and cotton, a clean drop falling into a glass below, plain background.',
        [
            (
                'liste',
                'On peut réaliser un filtre à eau avec une demi-bouteille, du sable, du coton, du charbon et du gravier.',
                'fi-materiel',
                'Five small piles side by side: a half bottle, sand, cotton, charcoal and gravel, neatly arranged, plain background.',
                [
                    ('simple', 'Le matériel : une demi-bouteille, du sable, du coton, du charbon et du gravier.'),
                    ('pas_a_pas', 'On coupe la bouteille, on la retourne, puis on met le coton, le sable, le charbon et le gravier.'),
                ],
                [
                    ('qcm', 1, {'question': 'Pour faire un filtre, on utilise une…', 'options': ['demi-bouteille', 'assiette', 'cuillère']},
                     {'index': 0}, 'Une demi-bouteille.'),
                    ('qcm', 1, {'question': 'Lequel sert à filtrer l’eau ?', 'options': ['Le sable', 'Le sucre', 'Le savon']},
                     {'index': 0}, 'Le sable fait partie du filtre.'),
                    ('qcm', 2, {'question': 'Quels matériaux met-on dans le filtre ?', 'options': ['Du gravier, du charbon, du sable et du coton', 'Du sucre, du sel et de l’huile', 'Du papier et de la colle', 'Des feuilles et des cailloux peints']},
                     {'index': 0}, 'Gravier, charbon, sable et coton.'),
                    ('texte_a_trous', 3, {'text': 'On fabrique le filtre avec une demi-{{1}}, du sable, du coton, du charbon et du {{2}}.', 'blanks': 2},
                     {'values': ['bouteille', 'gravier']}, 'Une demi-bouteille et du gravier.'),
                ],
            ),
            (
                'liste',
                'Dans le filtre, l’eau traverse le gravier, le charbon, le sable puis le coton.',
                'fi-couches',
                'A cut-away view of four stacked layers in a bottle, from top to bottom gravel, charcoal, sand, cotton, with a blue arrow going down, plain background.',
                [
                    ('simple', 'De haut en bas : gravier, charbon, sable, coton.'),
                    ('visuel', 'Le gravier arrête les gros morceaux, le coton retient les plus petites saletés.'),
                ],
                [
                    ('qcm', 1, {'question': 'Dans le filtre, l’eau passe d’abord par…', 'options': ['le gravier', 'le coton', 'la bouteille vide']},
                     {'index': 0}, 'Le gravier est en haut.'),
                    ('qcm', 1, {'question': 'Que traverse l’eau en dernier ?', 'options': ['Le coton', 'Le gravier', 'Le charbon']},
                     {'index': 0}, 'Le coton est tout en bas.'),
                    ('qcm', 2, {'question': 'Dans quel ordre l’eau traverse-t-elle le filtre ?', 'options': ['Gravier, charbon, sable, coton', 'Coton, sable, charbon, gravier', 'Sable, gravier, coton, charbon', 'Charbon, coton, gravier, sable']},
                     {'index': 0}, 'Gravier, charbon, sable, coton.'),
                    ('chronologie', 3, {'question': 'Remets les couches du filtre, du haut vers le bas.',
                                        'tokens': ['Gravier', 'Charbon', 'Sable', 'Coton']},
                     {'order': [0, 1, 2, 3]}, 'Gravier, charbon, sable, coton.'),
                ],
            ),
            (
                'relation',
                'L’eau non potable entre dans le filtre et l’eau potable en sort.',
                'fi-eau-potable',
                'On the left a glass of cloudy water, on the right a glass of clear water, an arrow between them, plain background.',
                [
                    ('simple', 'L’eau sale entre en haut, l’eau propre sort en bas.'),
                ],
                [
                    ('qcm', 1, {'question': 'L’eau qui entre dans le filtre est…', 'options': ['non potable', 'potable', 'sucrée']},
                     {'index': 0}, 'Elle est non potable : on ne peut pas la boire.'),
                    ('qcm', 1, {'question': 'L’eau qui sort du filtre est…', 'options': ['potable', 'plus sale', 'brûlante']},
                     {'index': 0}, 'Elle est potable.'),
                    ('qcm', 2, {'question': 'À quoi sert un filtre à eau ?', 'options': ['À rendre l’eau potable', 'À chauffer l’eau', 'À colorer l’eau', 'À geler l’eau']},
                     {'index': 0}, 'À rendre l’eau potable.'),
                    ('texte_a_trous', 3, {'text': 'L’eau non potable entre dans le filtre et l’eau {{1}} en sort.', 'blanks': 1},
                     {'values': ['potable']}, 'L’eau potable.'),
                ],
            ),
        ],
    ),
    (
        'Éducation à la paix', '#7a76c4',
        'La paix',
        'Pour maintenir la paix, je pratique le vivre-ensemble au village ou en ville, en acceptant les '
        'autres, en étant tolérant, en les assistant et en collaborant avec eux.',
        'pa-village',
        'Neighbours of a small village helping each other carry baskets under a calm sky, dove flying above, plain background.',
        [
            (
                'relation',
                'Pour maintenir la paix, je pratique le vivre-ensemble au village ou en ville.',
                'pa-ensemble',
                'Two small houses, one rural and one in town, joined by a path with children walking together, plain background.',
                [
                    ('simple', 'La paix se construit là où l’on vit : au village comme en ville.'),
                ],
                [
                    ('qcm', 1, {'question': 'Pour maintenir la paix, je pratique le…', 'options': ['vivre-ensemble', 'chacun pour soi', 'silence toute la journée']},
                     {'index': 0}, 'Le vivre-ensemble.'),
                    ('qcm', 1, {'question': 'Où pratique-t-on le vivre-ensemble ?', 'options': ['Au village ou en ville', 'Seulement à l’école', 'Nulle part']},
                     {'index': 0}, 'Au village ou en ville.'),
                    ('qcm', 2, {'question': 'Que faut-il faire pour maintenir la paix ?', 'options': ['Pratiquer le vivre-ensemble', 'Se disputer', 'Rester tout seul', 'Crier plus fort']},
                     {'index': 0}, 'Pratiquer le vivre-ensemble.'),
                    ('texte_a_trous', 3, {'text': 'Pour maintenir la {{1}}, je pratique le vivre-{{2}}.', 'blanks': 2},
                     {'values': ['paix', 'ensemble']}, 'La paix, le vivre-ensemble.'),
                ],
            ),
            (
                'liste',
                'Le vivre-ensemble, c’est accepter les autres, être tolérant, les assister et collaborer avec eux.',
                'pa-mains',
                'Four hands of different skin tones joining together over a soft circle, plain background.',
                [
                    ('simple', 'Quatre gestes : accepter, tolérer, assister, collaborer.'),
                    ('analogie', 'C’est comme porter une table à plusieurs : si un seul lâche, tout tombe.'),
                ],
                [
                    ('qcm', 1, {'question': 'Vivre ensemble, c’est d’abord…', 'options': ['accepter les autres', 'refuser les autres', 'ignorer les autres']},
                     {'index': 0}, 'Accepter les autres.'),
                    ('qcm', 1, {'question': 'Aider quelqu’un, c’est l’…', 'options': ['assister', 'oublier', 'éviter']},
                     {'index': 0}, 'C’est l’assister.'),
                    ('qcm', 2, {'question': 'Lequel ne fait PAS partie du vivre-ensemble ?', 'options': ['Refuser les autres', 'Être tolérant', 'Assister les autres', 'Collaborer avec eux']},
                     {'index': 0}, 'Refuser les autres éloigne de la paix.'),
                    ('chronologie', 3, {'question': 'Remets les trois façons de vivre ensemble, dans l’ordre du cahier.',
                                        'tokens': ['Être tolérant', 'Assister les autres', 'Collaborer avec eux']},
                     {'order': [0, 1, 2]}, 'Tolérer, assister, collaborer.'),
                    ('texte_a_trous', 3, {'text': 'Je vis en paix en étant {{1}} avec les autres.', 'blanks': 1},
                     {'values': ['tolérant']}, 'En étant tolérant.'),
                ],
            ),
        ],
    ),
    (
        'Géographie', '#6f9a3f',
        'Le sol',
        'Le sol est la partie superficielle de la terre. Il diffère en fonction de sa structure : '
        'sablonneux, ferralitique, basaltique ou argileux.',
        'so-terre',
        'A gentle cut-away of the ground showing a thin top layer with grass and a small plant, plain soft background.',
        [
            (
                'definition',
                'Le sol est la partie superficielle de la terre.',
                'so-coupe',
                'A simple slice of ground with the very top layer highlighted in a warm colour, plain background.',
                [
                    ('simple', 'Le sol, c’est la couche du dessus, celle sur laquelle on marche.'),
                    ('analogie', 'C’est comme la peau de la terre : fine, mais c’est là que tout pousse.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où se trouve le sol ?', 'options': ['À la surface de la terre', 'Au centre de la Terre', 'Dans le ciel']},
                     {'index': 0}, 'À la surface : c’est la partie superficielle.'),
                    ('qcm', 1, {'question': 'Le sol est la partie… de la terre', 'options': ['superficielle', 'profonde', 'invisible']},
                     {'index': 0}, 'Superficielle veut dire « du dessus ».'),
                    ('qcm', 2, {'question': 'Qu’est-ce que le sol ?', 'options': ['La partie superficielle de la terre', 'Le ciel au-dessus de nous', 'L’eau de la rivière', 'Le centre de la Terre']},
                     {'index': 0}, 'La partie superficielle de la terre.'),
                    ('texte_a_trous', 3, {'text': 'Le sol est la partie {{1}} de la terre.', 'blanks': 1},
                     {'values': ['superficielle']}, 'Superficielle.'),
                ],
            ),
            (
                'relation',
                'Le sol diffère en fonction de sa structure.',
                'so-structures',
                'Four small jars of earth of different colours and grain sizes lined up, plain background.',
                [
                    ('simple', 'Tous les sols ne se ressemblent pas : cela dépend de leur structure.'),
                ],
                [
                    ('qcm', 1, {'question': 'Tous les sols sont-ils pareils ?', 'options': ['Non, ils sont différents', 'Oui, tous pareils']},
                     {'index': 0}, 'Ils diffèrent selon leur structure.'),
                    ('qcm', 2, {'question': 'Qu’est-ce qui fait la différence entre les sols ?', 'options': ['Leur structure', 'Leur prix', 'Leur nom', 'Leur âge']},
                     {'index': 0}, 'Leur structure.'),
                    ('texte_a_trous', 3, {'text': 'Le sol diffère en fonction de sa {{1}}.', 'blanks': 1},
                     {'values': ['structure']}, 'Sa structure.'),
                ],
            ),
            (
                'definition',
                'Le sol sablonneux est fait de grains de roche.',
                'so-sablonneux',
                'A close view of pale sandy soil with visible grains, a small shell shape, plain background.',
                [('simple', 'Sablonneux : il est fait de grains de roche, comme du sable.')],
                [
                    ('qcm', 1, {'question': 'Le sol sablonneux est fait de…', 'options': ['grains de roche', 'eau', 'fer']},
                     {'index': 0}, 'De grains de roche.'),
                    ('qcm', 2, {'question': 'Quel sol est fait de grains de roche ?', 'options': ['Le sol sablonneux', 'Le sol argileux', 'Le sol basaltique', 'Le sol ferralitique']},
                     {'index': 0}, 'Le sol sablonneux.'),
                    ('texte_a_trous', 3, {'text': 'Le sol {{1}} est fait de grains de roche.', 'blanks': 1},
                     {'values': ['sablonneux']}, 'Sablonneux.'),
                ],
            ),
            (
                'definition',
                'Le sol ferralitique est rouge et riche en fer.',
                'so-ferralitique',
                'A close view of deep red earth with a small iron-coloured pebble, plain background.',
                [('simple', 'Ferralitique : il est rouge parce qu’il contient beaucoup de fer.')],
                [
                    ('qcm', 1, {'question': 'Le sol ferralitique est de quelle couleur ?', 'options': ['Rouge', 'Noir', 'Blanc']},
                     {'index': 0}, 'Il est rouge.'),
                    ('qcm', 2, {'question': 'Pourquoi le sol ferralitique est-il rouge ?', 'options': ['Il est riche en fer', 'Il est riche en eau', 'Il a été brûlé', 'Il a été peint']},
                     {'index': 0}, 'Parce qu’il est riche en fer.'),
                    ('texte_a_trous', 3, {'text': 'Le sol ferralitique est rouge et riche en {{1}}.', 'blanks': 1},
                     {'values': ['fer']}, 'En fer.'),
                ],
            ),
            (
                'definition',
                'Le sol basaltique est noir et fertile.',
                'so-basaltique',
                'A close view of dark black earth with a healthy green sprout growing, plain background.',
                [('simple', 'Basaltique : il est noir, et les plantes y poussent bien.')],
                [
                    ('qcm', 1, {'question': 'Le sol basaltique est…', 'options': ['noir', 'rouge', 'jaune']},
                     {'index': 0}, 'Il est noir.'),
                    ('qcm', 2, {'question': 'Quel sol est noir et fertile ?', 'options': ['Le basaltique', 'L’argileux', 'Le sablonneux', 'Le ferralitique']},
                     {'index': 0}, 'Le basaltique.'),
                    ('texte_a_trous', 3, {'text': 'Le sol basaltique est {{1}} et fertile.', 'blanks': 1},
                     {'values': ['noir']}, 'Noir.'),
                ],
            ),
            (
                'definition',
                'Le sol argileux est mou et pas fertile.',
                'so-argileux',
                'A close view of soft grey clay earth, a finger print pressed into it, no plant, plain background.',
                [('simple', 'Argileux : il est mou, et les plantes y poussent mal.')],
                [
                    ('qcm', 1, {'question': 'Le sol argileux est…', 'options': ['mou', 'dur comme la pierre', 'brûlant']},
                     {'index': 0}, 'Il est mou.'),
                    ('qcm', 2, {'question': 'Quel sol n’est pas fertile ?', 'options': ['L’argileux', 'Le basaltique', 'Le ferralitique', 'Aucun']},
                     {'index': 0}, 'L’argileux n’est pas fertile.'),
                    ('texte_a_trous', 3, {'text': 'Le sol argileux est mou et pas {{1}}.', 'blanks': 1},
                     {'values': ['fertile']}, 'Pas fertile.'),
                ],
            ),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles = set()
    total_items = 0
    for matiere, couleur, titre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 320, 'résumé trop long : ' + titre
        assert img not in cles, 'image en double : ' + img
        cles.add(img)
        for kind, phrase, nimg, nprompt, expl, items in notions:
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 150, 'notion trop longue : ' + phrase
            assert nimg not in cles, 'image en double : ' + nimg
            cles.add(nimg)
            for registre, corps in expl:
                assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), registre
                assert len(corps) <= 200, 'explication trop longue : ' + corps
            niveaux = set()
            for ikind, niveau, payload, answer, explain in items:
                total_items += 1
                niveaux.add(niveau)
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                if ikind == 'qcm':
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 60, 'option trop longue pour un CE1 : ' + o
                    assert len(payload['question']) <= 80, 'question trop longue : ' + payload['question']
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous pour un CE1 : ' + payload['text']
                elif ikind == 'chronologie':
                    assert sorted(answer['order']) == list(range(len(payload['tokens']))), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == {1, 2, 3}, 'niveaux manquants sur « %s » : %s' % (phrase, sorted(niveaux))
    return len(cles), total_items


def litteral(valeur):
    return "'" + json.dumps(valeur, ensure_ascii=False) + "'"


def sql():
    out = [ENTETE]
    for li, (matiere, couleur, titre, resume, img, prompt, notions) in enumerate(LECONS, start=1):
        out.append("  -- ─────────────────────────────────────────────────────────────")
        out.append("  -- %s — %s" % (matiere, titre))
        out.append("  -- ─────────────────────────────────────────────────────────────")
        out.append("  insert into subjects (parent_id, label, color) values (p_parent, '%s', '%s')" % (matiere, couleur))
        out.append("  on conflict (parent_id, label) do update set color = excluded.color")
        out.append("  returning id into v_subject;\n")
        out.append("  insert into lessons")
        out.append("    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,")
        out.append("     illustration, illustration_prompt)")
        out.append("  values (p_parent, v_subject, v_class, '%s'," % titre)
        out.append("    '%s'," % resume)
        out.append("    'fr', '%s', %d, 'approved', '%s'," % (matiere, li, img))
        out.append("    '%s')" % (STYLE + prompt))
        out.append("  returning id into v_lesson;\n")

        for ni, (kind, phrase, nimg, nprompt, expl, items) in enumerate(notions, start=1):
            out.append("  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)")
            out.append("  values (p_parent, v_lesson, '%s', '%s', %d, 'approved', '%s'," % (kind, phrase, ni, nimg))
            out.append("    '%s')" % (STYLE + nprompt))
            out.append("  returning id into v_notion;\n")

            if expl:
                out.append("  insert into explanations (parent_id, notion_id, register, body, status) values")
                out.append(',\n'.join("    (p_parent, v_notion, '%s', '%s', 'approved')" % (r, b) for r, b in expl) + ';\n')

            out.append("  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values")
            lignes = []
            for ikind, niveau, payload, answer, explain in items:
                lignes.append(
                    "    (p_parent, v_notion, '%s', %d,\n     %s::jsonb,\n     %s::jsonb, '%s', 'approved')"
                    % (ikind, niveau, litteral(payload), litteral(answer), explain)
                )
            out.append(',\n'.join(lignes) + ';\n')

    out.append(PIED)
    return '\n'.join(out)


ENTETE = """-- Se Former Cameroun — les six leçons du cahier de KLEIN (CE1)
--
-- Transcrites depuis six photos du cahier, du mardi 13 au jeudi 15 octobre
-- 2026. La fonction d'extraction n'étant pas encore déployée, la
-- transcription et la structuration sont faites à la main, dans le format
-- exact qu'elle produira.
--
-- Rien n'est ajouté au cahier : les mots, les listes et les chiffres sont
-- ceux des pages. Les corrections sont orthographiques et grammaticales
-- (« Une enfant obéissant » → « Un enfant obéissant », accents rétablis), et
-- la dernière phrase de l'obéissance, laissée en suspens, est rétablie au
-- plus près de ce qui est écrit.
--
-- KLEIN est en CE1, pas en CM1 : questions plus courtes, mots plus simples,
-- jamais plus de deux mots à écrire. Chaque notion a ses trois étapes.
--
-- Six matières nouvelles naissent ici, nommées comme le cahier les nomme :
-- Éducation morale, Droits et devoirs, Éducation civique, Technologies,
-- Éducation à la paix, Géographie.
--
-- Les leçons naissent en 'approved' : elles ont été relues par le parent qui
-- les a photographiées, au moment de les fournir.

create or replace function public.seed_lecons_klein(p_parent uuid)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  v_class   uuid;
  v_subject uuid;
  v_lesson  uuid;
  v_notion  uuid;
begin
  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';
"""

PIED = """  return 1;
end;
$$;

-- Rattache les leçons à la famille déjà présente, une seule fois.
select public.seed_lecons_klein(parent_id)
  from children
 where first_name = 'KLEIN'
   and not exists (select 1 from lessons where title = 'Le sol')
 limit 1;
"""

if __name__ == '__main__':
    images, items = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'supabase', 'migrations', '20261016120000_lecons_klein.sql')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(sql())

    notions = sum(len(l[6]) for l in LECONS)
    print('%d leçons · %d notions · %d questions · %d images à produire'
          % (len(LECONS), notions, items, images))
    print(chemin)
