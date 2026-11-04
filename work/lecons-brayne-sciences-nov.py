# -*- coding: utf-8 -*-
"""
Quatre leçons de sciences et de technologie pour BRAYNE (CM1) — cahier du
27 octobre au 2 novembre 2026.

Les roches, la gestion de l-eau, le mode de locomotion des animaux et le
fonctionnement des lampes. Tout vient du cahier, et rien n-y est ajouté.

TROIS RÉSERVES, dites ici et non cachées.

1. LA COULEUR DES ROCHES MAGMATIQUES. Le cahier les donne « de couleur
   noire » et cite le granite en exemple. C-est vrai du basalte ; le
   granite, lui, est souvent clair. La notion ne porte donc PAS sur la
   couleur, aucune question ne l-interroge, et une explication signale
   l-écart au lecteur. À vérifier avec la maîtresse.

2. LA LOCOMOTION S-ARRÊTE À LA TERRE FERME. Le cahier traite les animaux
   qui marchent, sautent et rampent, puis s-interrompt. Ni l-eau ni l-air.
   La leçon n-enseigne donc que la terre ferme et le dit dans son résumé :
   inventer la nage et le vol reviendrait à faire réviser un cours que la
   maîtresse n-a pas donné.

3. L-EAU DE JAVEL. Le cahier dit « quelques gouttes » sans quantité. La
   leçon le répète tel quel, et ajoute, dans une explication et sur la
   figure, qu-un enfant ne manipule jamais ce produit seul. Ce n-est pas
   du savoir ajouté, c-est une précaution sur un produit dangereux nommé
   dans une leçon destinée à un enfant de neuf ans.

Usage :  python work/lecons-brayne-sciences-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-brayne-sciences-nov.py. '

CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'fr'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü’0123456789-,.')
TAPABLE |= {c.upper() for c in TAPABLE}

# La matière est portée par la leçon : trois sont des sciences, la dernière
# est de la technologie.
LECONS = [
    # ----------------------------------------------------------------- 32
    (
        'Les roches', 'Sciences de la Terre', 'Sciences', '2026-10-27', 32,
        'Une roche est un bloc de minéraux d’origine naturelle, relativement dur. Il existe '
        'trois types de roches : les magmatiques, qui viennent de la lave ; les sédimentaires, '
        'qui se forment au fond de la mer ; et les métamorphiques, qui sont des roches '
        'transformées.',
        'bs-ro-couv',
        'Trois roches côte à côte : une sombre et grenue, une en couches, une veinée.',
        [
            ('definition', 'Une roche est un bloc de minéraux d’origine naturelle, relativement dur.',
             'bs-ro-def', 'Un bloc de pierre irrégulier, grenu, posé seul.',
             [('simple', 'Naturelle veut dire que personne ne l’a fabriquée : elle était déjà là.'),
              ('analogie', 'Une brique n’est pas une roche : on l’a faite. Un caillou du champ, si.')],
             [('qcm', 1, {'question': 'Qu’est-ce qu’une roche ?',
                          'options': ['un bloc de minéraux naturel et dur',
                                      'un morceau de bois séché', 'un objet fabriqué par l’homme']},
               {'index': 0}, 'Un bloc de minéraux d’origine naturelle.'),
              ('vrai_faux', 1, {'statement': 'Une roche est relativement dure.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Que veut dire « d’origine naturelle » ?',
                          'options': ['que personne ne l’a fabriquée', 'qu’elle vient de loin',
                                      'qu’elle est très ancienne']},
               {'index': 0}, 'Personne ne l’a fabriquée.'),
              ('texte_a_trous', 3, {'text': 'Une roche est un bloc de {{1}} d’origine naturelle.',
                                    'blanks': 1},
               {'values': ['minéraux']}, 'De minéraux.'),
              ('vrai_faux', 4, {'statement': 'Une brique cuite au four est une roche.'},
               {'value': False}, 'Non : elle a été fabriquée, elle n’est pas d’origine naturelle.')]),

            ('liste', 'Il existe trois types de roches : les magmatiques, les sédimentaires et les métamorphiques.',
             'bs-ro-trois', 'Les trois roches alignées, chacune avec son aspect propre.',
             [('simple', 'Trois types, et c’est leur façon de se former qui les sépare.'),
              ('visuel', 'Sur la figure, les trois n’ont pas le même aspect : grenue, en couches, veinée.')],
             [('qcm', 1, {'question': 'Combien de types de roches existe-t-il ?',
                          'options': ['trois', 'deux', 'cinq']},
               {'index': 0}, 'Trois.'),
              ('vrai_faux', 1, {'statement': 'Les roches sédimentaires sont un des trois types.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Lequel de ces mots n’est pas un type de roche ?',
                          'options': ['volcanique', 'magmatique', 'métamorphique']},
               {'index': 0}, 'Volcanique dit où la roche magmatique s’est formée, pas son type.'),
              ('texte_a_trous', 3, {'text': 'Les trois types sont magmatiques, {{1}} et métamorphiques.',
                                    'blanks': 1},
               {'values': ['sédimentaires']}, 'Sédimentaires.'),
              ('qcm', 4, {'question': 'Qu’est-ce qui sépare les trois types de roches ?',
                          'options': ['leur formation', 'leur poids', 'leur taille']},
               {'index': 0}, 'C’est leur formation qui les range.')]),

            ('relation',
             'Les roches magmatiques se forment à l’extérieur de la Terre — elles sont volcaniques — ou à l’intérieur — elles sont plutoniques.',
             'bs-ro-magma', 'Le basalte sombre et grenu, et le granite clair et moucheté.',
             [('pas_a_pas', 'La lave sort : la roche est volcanique. La lave reste dedans : elle est plutonique.'),
              ('simple', 'Exemples du cahier : le basalte et le granite.'),
              ('visuel', 'Le cahier les dit « de couleur noire ». C’est vrai du basalte ; le granite, lui, est souvent clair. À vérifier avec la maîtresse.')],
             [('qcm', 1, {'question': 'D’où viennent les roches magmatiques ?',
                          'options': ['de la lave', 'du fond de la mer', 'des montagnes']},
               {'index': 0}, 'De la lave.'),
              ('vrai_faux', 1, {'statement': 'Le basalte et le granite sont des roches magmatiques.'},
               {'value': True}, 'Oui, ce sont les deux exemples du cahier.'),
              ('association', 2, {'question': 'Relie chaque mot à l’endroit où la roche s’est formée.',
                                  'gauche': ['volcanique', 'plutonique'],
                                  'droite': ['à l’extérieur de la Terre', 'à l’intérieur de la Terre']},
               {'order': [0, 1]}, 'Volcanique dehors, plutonique dedans.'),
              ('texte_a_trous', 3,
               {'text': 'Une roche magmatique formée à l’intérieur de la Terre est dite {{1}}.',
                'blanks': 1},
               {'values': ['plutonique']}, 'Plutonique.'),
              ('qcm', 4, {'question': 'Une lave qui refroidit sans jamais sortir donne une roche…',
                          'options': ['plutonique', 'volcanique', 'sédimentaire']},
               {'index': 0}, 'Elle est restée à l’intérieur, donc plutonique.')]),

            ('relation',
             'Les roches sédimentaires se forment au fond de la mer, par sédimentation des débris d’autres roches.',
             'bs-ro-sedi', 'Une roche en couches superposées, couleur de sable.',
             [('pas_a_pas', 'Des roches se cassent. Les débris descendent. Ils se déposent au fond et se collent.'),
              ('simple', 'Exemples du cahier : l’argile et le calcaire.'),
              ('visuel', 'Sur la figure, les couches se voient : chacune est un dépôt.')],
             [('qcm', 1, {'question': 'Où se forment les roches sédimentaires ?',
                          'options': ['au fond de la mer', 'dans un volcan', 'dans les nuages']},
               {'index': 0}, 'Au fond de la mer.'),
              ('vrai_faux', 1, {'statement': 'L’argile et le calcaire sont des roches sédimentaires.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'De quoi les roches sédimentaires sont-elles faites ?',
                          'options': ['de débris d’autres roches', 'de lave refroidie',
                                      'de minéraux fondus']},
               {'index': 0}, 'De débris d’autres roches.'),
              ('texte_a_trous', 3, {'text': 'Les roches sédimentaires se forment au fond de la {{1}}.',
                                    'blanks': 1},
               {'values': ['mer']}, 'De la mer.'),
              ('qcm', 4, {'question': 'Un fleuve dépose du sable au fond de la mer pendant des siècles. On obtient…',
                          'options': ['une roche sédimentaire', 'une roche magmatique',
                                      'une roche métamorphique']},
               {'index': 0}, 'Des débris déposés et tassés : c’est une sédimentaire.')]),

            ('relation',
             'Les roches métamorphiques sont des roches transformées, qu’on trouve sur les chaînes montagneuses.',
             'bs-ro-meta', 'Une roche claire parcourue de veines.',
             [('simple', 'Transformées veut dire qu’elles étaient autre chose avant.'),
              ('pas_a_pas', 'Une roche est écrasée et chauffée longtemps : elle change et devient métamorphique.'),
              ('visuel', 'Exemples du cahier : le gneiss, le marbre et l’ardoise.')],
             [('qcm', 1, {'question': 'Que sont les roches métamorphiques ?',
                          'options': ['des roches transformées', 'des roches toutes neuves',
                                      'des roches fabriquées']},
               {'index': 0}, 'Des roches transformées.'),
              ('vrai_faux', 1, {'statement': 'Le marbre est une roche métamorphique.'},
               {'value': True}, 'Oui, avec le gneiss et l’ardoise.'),
              ('qcm', 2, {'question': 'Où trouve-t-on surtout les roches métamorphiques ?',
                          'options': ['sur les chaînes montagneuses', 'au fond des lacs',
                                      'dans le sable du désert']},
               {'index': 0}, 'Sur les chaînes montagneuses.'),
              ('texte_a_trous', 3, {'text': 'Le gneiss, le marbre et l’{{1}} sont métamorphiques.',
                                    'blanks': 1},
               {'values': ['ardoise']}, 'L’ardoise.'),
              ('qcm', 4, {'question': 'Une roche sédimentaire écrasée et chauffée très longtemps devient…',
                          'options': ['métamorphique', 'magmatique', 'sédimentaire encore']},
               {'index': 0}, 'Elle est transformée, donc métamorphique.')]),
        ],
    ),

    # ----------------------------------------------------------------- 33
    (
        'La gestion de l’eau', 'Développement durable', 'Sciences', '2026-10-28', 33,
        'Chaque village ou quartier doit avoir des points d’eau — puits, forage, source, '
        'robinet — pour permettre aux populations de s’approvisionner. Pour bien les gérer, on '
        'nettoie les alentours, on protège les sources et les puits, on prévoit des heures de '
        'ravitaillement, on désinfecte et on multiplie les points d’eau.',
        'bs-eau-couv',
        'Un puits et un robinet, les deux points d’eau les plus courants.',
        [
            ('definition',
             'Chaque village ou quartier doit avoir des points d’eau pour permettre aux populations de s’approvisionner.',
             'bs-eau-points', 'Un puits de quartier, avec sa margelle et son seau.',
             [('simple', 'S’approvisionner, c’est aller chercher l’eau dont on a besoin.'),
              ('analogie', 'Sans point d’eau proche, il faut marcher des kilomètres pour un seau.')],
             [('qcm', 1, {'question': 'À quoi sert un point d’eau dans un quartier ?',
                          'options': ['à permettre aux gens de s’approvisionner',
                                      'à décorer la place', 'à arroser les routes']},
               {'index': 0}, 'À permettre aux populations de s’approvisionner.'),
              ('vrai_faux', 1, {'statement': 'Chaque village doit avoir des points d’eau.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Que veut dire « s’approvisionner en eau » ?',
                          'options': ['aller chercher l’eau dont on a besoin',
                                      'faire bouillir l’eau', 'creuser un trou']},
               {'index': 0}, 'Aller chercher l’eau dont on a besoin.'),
              ('texte_a_trous', 3, {'text': 'Chaque quartier doit avoir des points d’{{1}}.',
                                    'blanks': 1},
               {'values': ['eau']}, 'D’eau.'),
              ('vrai_faux', 4, {'statement': 'Un seul point d’eau suffit toujours pour tout un village.'},
               {'value': False}, 'Non : le cahier demande justement de les multiplier.')]),

            ('liste', 'Les points d’eau sont le puits, le forage, la source et le robinet.',
             'bs-eau-sortes', 'Les quatre sortes de points d’eau, numérotées.',
             [('simple', 'Quatre sortes, et toutes donnent de l’eau au quartier.'),
              ('pas_a_pas', 'Le puits et le forage descendent chercher l’eau ; la source sort seule ; le robinet l’amène.')],
             [('qcm', 1, {'question': 'Lequel de ces mots est un point d’eau ?',
                          'options': ['le forage', 'le grenier', 'le marché']},
               {'index': 0}, 'Le forage.'),
              ('vrai_faux', 1, {'statement': 'Le robinet est un point d’eau.'},
               {'value': True}, 'Oui, avec le puits, le forage et la source.'),
              ('chronologie', 2, {'question': 'Range ces points d’eau comme le cahier les cite.',
                                  'tokens': ['le puits', 'le forage', 'la source', 'le robinet']},
               {'order': [0, 1, 2, 3]}, 'Puits, forage, source, robinet.'),
              ('texte_a_trous', 3, {'text': 'Le puits, le forage, la {{1}} et le robinet.', 'blanks': 1},
               {'values': ['source']}, 'La source.'),
              ('qcm', 4, {'question': 'Quel point d’eau donne de l’eau sans qu’on ait à creuser ?',
                          'options': ['la source', 'le puits', 'le forage']},
               {'index': 0}, 'La source sort seule du sol.')]),

            ('liste',
             'Pour bien gérer un point d’eau, on nettoie les alentours et on protège les sources et les puits pour éviter que la saleté y tombe.',
             'bs-eau-proteger', 'Les gestes de protection d’un point d’eau, numérotés.',
             [('simple', 'Une eau propre au fond ne sert à rien si la saleté tombe dedans.'),
              ('pas_a_pas', 'On nettoie autour, puis on couvre et on protège l’ouverture.')],
             [('qcm', 1, {'question': 'Que fait-on autour d’un point d’eau ?',
                          'options': ['on nettoie les alentours', 'on plante des arbres',
                                      'on construit un mur']},
               {'index': 0}, 'On nettoie les alentours.'),
              ('vrai_faux', 1, {'statement': 'Il faut protéger les sources et les puits.'},
               {'value': True}, 'Oui, pour éviter que la saleté y tombe.'),
              ('qcm', 2, {'question': 'Pourquoi protège-t-on l’ouverture d’un puits ?',
                          'options': ['pour éviter que la saleté y tombe',
                                      'pour que l’eau reste fraîche', 'pour cacher le puits']},
               {'index': 0}, 'Pour éviter que la saleté y tombe.'),
              ('texte_a_trous', 3, {'text': 'On protège les puits pour éviter que la {{1}} y tombe.',
                                    'blanks': 1},
               {'values': ['saleté']}, 'La saleté.'),
              ('vrai_faux', 4, {'statement': 'Nettoyer autour du puits suffit : l’ouverture peut rester libre.'},
               {'value': False}, 'Non. Le cahier demande les deux : nettoyer ET protéger.')]),

            ('liste',
             'Il faut aussi prévoir des heures de ravitaillement pour éviter le gaspillage, et multiplier les points d’eau.',
             'bs-eau-heures', 'Les deux dernières règles de gestion, numérotées.',
             [('simple', 'Des heures fixées, c’est moins de monde à la fois et moins d’eau perdue.'),
              ('analogie', 'Comme les heures de classe : chacun sait quand venir.')],
             [('qcm', 1, {'question': 'Pourquoi prévoit-on des heures de ravitaillement ?',
                          'options': ['pour éviter le gaspillage', 'pour fermer le puits la nuit',
                                      'pour faire payer l’eau']},
               {'index': 0}, 'Pour éviter le gaspillage.'),
              ('vrai_faux', 1, {'statement': 'Il faut multiplier les points de ravitaillement.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Que veut dire « gaspiller l’eau » ?',
                          'options': ['en perdre sans la utiliser', 'la faire bouillir',
                                      'la partager entre tous']},
               {'index': 0}, 'En perdre pour rien.'),
              ('texte_a_trous', 3, {'text': 'Des heures de ravitaillement évitent le {{1}}.',
                                    'blanks': 1},
               {'values': ['gaspillage']}, 'Le gaspillage.'),
              ('qcm', 4, {'question': 'Un quartier a un seul puits pour mille habitants. Que conseille le cahier ?',
                          'options': ['multiplier les points d’eau', 'creuser plus profond',
                                      'fermer le puits à midi']},
               {'index': 0}, 'Multiplier les points de ravitaillement.')]),

            ('relation', 'On désinfecte l’eau en y mettant quelques gouttes d’eau de javel.',
             'bs-eau-javel', 'Des gouttes qui tombent dans une eau claire, avec un avertissement.',
             [('simple', 'Désinfecter, c’est tuer les microbes qui rendent malade.'),
              ('pas_a_pas', 'Quelques gouttes suffisent. Le cahier ne donne pas d’autre quantité.'),
              ('visuel', 'L’eau de javel est un produit dangereux : un enfant ne la manipule jamais seul.')],
             [('qcm', 1, {'question': 'Avec quoi désinfecte-t-on l’eau d’un point d’eau ?',
                          'options': ['quelques gouttes d’eau de javel', 'du sable fin',
                                      'du jus de citron']},
               {'index': 0}, 'Quelques gouttes d’eau de javel.'),
              ('vrai_faux', 1, {'statement': 'Désinfecter l’eau sert à tuer les microbes.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Combien d’eau de javel le cahier demande-t-il ?',
                          'options': ['quelques gouttes', 'un litre', 'une bouteille entière']},
               {'index': 0}, 'Quelques gouttes seulement.'),
              ('texte_a_trous', 3, {'text': 'On désinfecte en y mettant quelques {{1}} d’eau de javel.',
                                    'blanks': 1},
               {'values': ['gouttes']}, 'Quelques gouttes.'),
              ('vrai_faux', 4, {'statement': 'Un enfant peut verser lui-même l’eau de javel dans le puits.'},
               {'value': False}, 'Non. C’est un produit dangereux : toujours avec un adulte.')]),
        ],
    ),

    # ----------------------------------------------------------------- 34
    (
        'Le mode de locomotion des animaux', 'Sciences de la Vie', 'Sciences', '2026-10-29', 34,
        'Les animaux vertébrés ont des modes de déplacement adaptés à leur milieu de vie et à '
        'leurs organes locomoteurs. Sur terre, ceux qui ont des pattes marchent, comme le chien '
        'et le lion, ou sautent, comme le lapin et le kangourou ; le serpent, lui, rampe sur '
        'son ventre. Le cahier s’arrête à la terre ferme.',
        'bs-loco-couv',
        'Trois animaux : l’un sur ses pattes, l’un en train de sauter, un serpent au sol.',
        [
            ('relation',
             'Les animaux vertébrés ont des modes de déplacement adaptés à leur milieu de vie et à leurs organes locomoteurs.',
             'bs-loco-milieu', 'Un animal à pattes et un serpent, côte à côte.',
             [('simple', 'Les organes locomoteurs, ce sont les parties du corps qui servent à avancer.'),
              ('pas_a_pas', 'Regarde d’abord où vit l’animal, puis avec quoi il avance.'),
              ('analogie', 'Le serpent n’a pas de pattes : son corps entier lui sert à avancer.')],
             [('qcm', 1, {'question': 'À quoi le mode de déplacement est-il adapté ?',
                          'options': ['au milieu de vie et aux organes', 'à la taille de l’animal',
                                      'à la couleur de son poil']},
               {'index': 0}, 'Au milieu de vie et aux organes locomoteurs.'),
              ('vrai_faux', 1, {'statement': 'Les organes locomoteurs servent à se déplacer.'},
               {'value': True}, 'Oui, c’est ce que veut dire le mot.'),
              ('qcm', 2, {'question': 'Qu’est-ce qu’un organe locomoteur ?',
                          'options': ['une partie du corps qui sert à avancer',
                                      'un organe qui sert à manger', 'un os du crâne']},
               {'index': 0}, 'Une partie du corps qui sert à se déplacer.'),
              ('texte_a_trous', 3,
               {'text': 'Le déplacement est adapté au {{1}} de vie de l’animal.', 'blanks': 1},
               {'values': ['milieu']}, 'Au milieu de vie.'),
              ('qcm', 4, {'question': 'Pourquoi le serpent ne marche-t-il pas ?',
                          'options': ['il n’a pas de pattes', 'il est trop lourd',
                                      'il vit dans l’eau']},
               {'index': 0}, 'Ses organes ne le permettent pas : il n’a pas de pattes.')]),

            ('relation', 'Sur terre, les animaux qui ont des pattes marchent : le chien, le lion.',
             'bs-loco-marche', 'Un animal à quatre pattes posé au sol.',
             [('simple', 'Les pattes touchent le sol l’une après l’autre : c’est marcher.'),
              ('visuel', 'Sur la figure, les pattes sont toutes posées au sol.')],
             [('qcm', 1, {'question': 'Comment se déplacent le chien et le lion ?',
                          'options': ['ils marchent', 'ils sautent', 'ils rampent']},
               {'index': 0}, 'Ils marchent sur leurs pattes.'),
              ('vrai_faux', 1, {'statement': 'Le lion marche sur ses pattes.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Avec quoi le chien se déplace-t-il ?',
                          'options': ['avec ses pattes', 'avec son ventre', 'avec sa queue']},
               {'index': 0}, 'Avec ses pattes.'),
              ('texte_a_trous', 3, {'text': 'Le chien et le lion {{1}} sur leurs pattes.', 'blanks': 1},
               {'values': ['marchent']}, 'Ils marchent.'),
              ('qcm', 4, {'question': 'Un animal à pattes qui ne saute pas et ne rampe pas…',
                          'options': ['marche', 'nage', 'vole']},
               {'index': 0}, 'Sur terre ferme, il marche.')]),

            ('relation', 'D’autres animaux à pattes sautent : le lapin, le kangourou.',
             'bs-loco-saute', 'Un animal aux pattes repliées, décollant du sol.',
             [('simple', 'Sauter, c’est quitter le sol d’un coup, avec les pattes de derrière.'),
              ('pas_a_pas', 'Les pattes se replient, poussent fort, et l’animal décolle.'),
              ('visuel', 'Sur la figure, les pattes sont repliées et l’animal n’est plus au sol.')],
             [('qcm', 1, {'question': 'Comment se déplacent le lapin et le kangourou ?',
                          'options': ['ils sautent', 'ils marchent', 'ils rampent']},
               {'index': 0}, 'Ils sautent.'),
              ('vrai_faux', 1, {'statement': 'Le kangourou saute.'},
               {'value': True}, 'Oui.'),
              ('association', 2, {'question': 'Relie chaque animal à son déplacement.',
                                  'gauche': ['le chien', 'le lapin', 'le serpent'],
                                  'droite': ['il marche', 'il saute', 'il rampe']},
               {'order': [0, 1, 2]}, 'Marcher, sauter, ramper.'),
              ('texte_a_trous', 3, {'text': 'Le lapin et le kangourou {{1}}.', 'blanks': 1},
               {'values': ['sautent']}, 'Ils sautent.'),
              ('qcm', 4, {'question': 'Qu’est-ce qui distingue le saut de la marche ?',
                          'options': ['l’animal quitte le sol', 'l’animal va moins vite',
                                      'l’animal n’a pas de pattes']},
               {'index': 0}, 'En sautant, il quitte le sol.')]),

            ('relation', 'Le serpent, lui, rampe sur son ventre, car il n’a pas de pattes.',
             'bs-loco-rampe', 'Un serpent ondulant posé au sol.',
             [('simple', 'Ramper, c’est avancer en se traînant sur le ventre.'),
              ('pas_a_pas', 'Le corps ondule, pousse contre le sol, et le serpent avance.'),
              ('visuel', 'Sur la figure, il n’y a aucune patte : c’est tout l’argument.')],
             [('qcm', 1, {'question': 'Comment le serpent se déplace-t-il ?',
                          'options': ['il rampe sur son ventre', 'il saute sur ses pattes',
                                      'il marche sur ses pattes']},
               {'index': 0}, 'Il rampe sur son ventre.'),
              ('vrai_faux', 1, {'statement': 'Le serpent n’a pas de pattes.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Avec quelle partie du corps le serpent avance-t-il ?',
                          'options': ['son ventre', 'ses pattes', 'ses ailes']},
               {'index': 0}, 'Son ventre.'),
              ('texte_a_trous', 3, {'text': 'Le serpent rampe sur son {{1}}.', 'blanks': 1},
               {'values': ['ventre']}, 'Sur son ventre.'),
              ('vrai_faux', 4, {'statement': 'Le serpent rampe parce qu’il est trop lourd pour marcher.'},
               {'value': False}, 'Non : il rampe parce qu’il n’a pas de pattes.')]),
        ],
    ),

    # ----------------------------------------------------------------- 35
    (
        'Les lampes électriques et solaires', 'Technologie', 'Technologie', '2026-11-02', 35,
        'La lampe électrique, ou ampoule, est un appareil d’éclairage qui fonctionne grâce au '
        'courant électrique : montée sur une douille reliée à un interrupteur, elle s’allume '
        'quand le courant passe par son filament. La lampe solaire, elle, est composée d’un '
        'panneau, d’un accumulateur, de fil conducteur, d’une ampoule et d’un interrupteur.',
        'bs-la-couv',
        'Une ampoule allumée, un panneau solaire et le soleil.',
        [
            ('definition',
             'La lampe électrique, ou ampoule, est un appareil d’éclairage qui fonctionne grâce au courant électrique.',
             'bs-la-ampoule', 'Une ampoule allumée, son filament visible.',
             [('simple', 'Un appareil d’éclairage est un objet qui sert à faire de la lumière.'),
              ('analogie', 'La lampe à pétrole éclaire avec une flamme ; l’ampoule, avec du courant.')],
             [('qcm', 1, {'question': 'Grâce à quoi la lampe électrique fonctionne-t-elle ?',
                          'options': ['au courant électrique', 'au pétrole de sa lampe',
                                      'au vent qui la traverse']},
               {'index': 0}, 'Au courant électrique.'),
              ('vrai_faux', 1, {'statement': 'Une ampoule est un appareil d’éclairage.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Qu’est-ce qu’un appareil d’éclairage ?',
                          'options': ['un objet qui sert à faire de la lumière',
                                      'un objet qui chauffe la pièce', 'un objet qui fait du bruit']},
               {'index': 0}, 'Un objet qui sert à faire de la lumière.'),
              ('texte_a_trous', 3,
               {'text': 'La lampe électrique fonctionne grâce au {{1}} électrique.', 'blanks': 1},
               {'values': ['courant']}, 'Au courant électrique.'),
              ('vrai_faux', 4, {'statement': 'Une ampoule éclaire même sans courant électrique.'},
               {'value': False}, 'Non : c’est le courant qui la fait fonctionner.')]),

            ('relation',
             'Pour fonctionner, la lampe doit être montée sur une douille connectée à un interrupteur.',
             'bs-la-douille', 'Une ampoule éteinte dans sa douille, reliée à un interrupteur.',
             [('simple', 'La douille tient l’ampoule et lui amène le courant.'),
              ('pas_a_pas', 'Ampoule, douille, fil, interrupteur : il manque une pièce et rien ne s’allume.')],
             [('qcm', 1, {'question': 'Sur quoi la lampe doit-elle être montée ?',
                          'options': ['une douille', 'une table', 'un panneau']},
               {'index': 0}, 'Sur une douille.'),
              ('vrai_faux', 1, {'statement': 'La douille doit être connectée à un interrupteur.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'À quoi sert la douille ?',
                          'options': ['à tenir l’ampoule et lui amener le courant',
                                      'à éteindre la lumière', 'à stocker le courant']},
               {'index': 0}, 'Elle tient l’ampoule et lui amène le courant.'),
              ('texte_a_trous', 3, {'text': 'La lampe est montée sur une {{1}}.', 'blanks': 1},
               {'values': ['douille']}, 'Une douille.'),
              ('qcm', 4, {'question': 'L’ampoule est bonne mais rien ne s’allume. Que vérifier d’abord ?',
                          'options': ['la douille et l’interrupteur', 'la couleur du verre',
                                      'la taille de l’ampoule']},
               {'index': 0}, 'Le courant passe par la douille et l’interrupteur.')]),

            ('relation',
             'Dès qu’on allume l’interrupteur, le courant passe par le filament et le verre propage la lumière.',
             'bs-la-filament', 'L’ampoule allumée, son filament parcouru par le courant.',
             [('simple', 'Le filament est le petit fil au milieu de l’ampoule.'),
              ('pas_a_pas', 'On appuie, le courant passe, le filament chauffe, le verre laisse sortir la lumière.'),
              ('visuel', 'Sur la figure, le filament est dessiné au milieu du verre.')],
             [('qcm', 1, {'question': 'Par quoi le courant passe-t-il dans l’ampoule ?',
                          'options': ['par le filament', 'par la douille seule',
                                      'par le panneau']},
               {'index': 0}, 'Par le filament.'),
              ('vrai_faux', 1, {'statement': 'C’est le verre qui propage la lumière.'},
               {'value': True}, 'Oui, le cahier le dit.'),
              ('chronologie', 2, {'question': 'Range ce qui se passe quand on allume.',
                                  'tokens': ['on allume l’interrupteur', 'le courant passe',
                                             'le filament s’éclaire', 'le verre propage la lumière']},
               {'order': [0, 1, 2, 3]}, 'Interrupteur, courant, filament, lumière.'),
              ('texte_a_trous', 3, {'text': 'Le courant passe par le {{1}} de l’ampoule.', 'blanks': 1},
               {'values': ['filament']}, 'Le filament.'),
              ('qcm', 4, {'question': 'Le filament d’une ampoule est cassé. Que se passe-t-il ?',
                          'options': ['elle ne s’allume plus', 'elle éclaire moins fort',
                                      'elle chauffe davantage']},
               {'index': 0}, 'Le courant ne peut plus passer : elle ne s’allume plus.')]),

            ('liste',
             'La lampe solaire est composée d’un panneau solaire, d’un accumulateur, de fil conducteur, d’une ampoule et d’un interrupteur.',
             'bs-la-solaire', 'Le panneau, l’accumulateur et l’ampoule, reliés.',
             [('simple', 'Cinq pièces, et chacune a son rôle.'),
              ('pas_a_pas', 'Le panneau prend le soleil, l’accumulateur garde, le fil conduit, l’ampoule éclaire.')],
             [('qcm', 1, {'question': 'Que trouve-t-on dans une lampe solaire ?',
                          'options': ['un panneau solaire', 'une mèche', 'du pétrole']},
               {'index': 0}, 'Un panneau solaire.'),
              ('vrai_faux', 1, {'statement': 'La lampe solaire comprend un accumulateur.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Quelle pièce garde l’énergie pour la nuit ?',
                          'options': ['l’accumulateur', 'le fil conducteur', 'l’interrupteur']},
               {'index': 0}, 'L’accumulateur.'),
              ('texte_a_trous', 3, {'text': 'La lampe solaire a un panneau et un {{1}}.', 'blanks': 1},
               {'values': ['accumulateur']}, 'Un accumulateur.'),
              ('qcm', 4, {'question': 'Quelle pièce manque si le courant ne va pas du panneau à l’ampoule ?',
                          'options': ['le fil conducteur', 'le panneau', 'le verre']},
               {'index': 0}, 'C’est le fil conducteur qui porte le courant.')]),

            ('relation',
             'Pour son bon fonctionnement, le panneau solaire doit être exposé au soleil pendant la journée afin de charger l’accumulateur.',
             'bs-la-soleil', 'Le panneau tourné vers le soleil, un rayon le frappant.',
             [('simple', 'Le panneau travaille le jour pour que la lampe éclaire le soir.'),
              ('pas_a_pas', 'Soleil sur le panneau, panneau qui charge l’accumulateur, accumulateur qui allume la lampe.'),
              ('analogie', 'Comme on remplit un seau le jour pour s’en servir la nuit.')],
             [('qcm', 1, {'question': 'Où doit être exposé le panneau solaire ?',
                          'options': ['au soleil', 'à l’ombre', 'sous la pluie']},
               {'index': 0}, 'Au soleil.'),
              ('vrai_faux', 1, {'statement': 'Le panneau doit être exposé pendant la journée.'},
               {'value': True}, 'Oui.'),
              ('qcm', 2, {'question': 'Pourquoi expose-t-on le panneau au soleil ?',
                          'options': ['pour charger l’accumulateur', 'pour le nettoyer',
                                      'pour le réchauffer']},
               {'index': 0}, 'Pour charger l’accumulateur.'),
              ('texte_a_trous', 3,
               {'text': 'Le panneau est exposé au soleil pour charger l’{{1}}.', 'blanks': 1},
               {'values': ['accumulateur']}, 'L’accumulateur.'),
              ('qcm', 4, {'question': 'Un panneau resté à l’ombre toute la journée. Le soir, la lampe…',
                          'options': ['ne s’allume pas', 'éclaire plus fort', 'chauffe']},
               {'index': 0}, 'L’accumulateur n’a pas été chargé.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues = set(), 0, 0
    for titre, chapitre, matiere, date, ordre, resume, img, prompt, notions in LECONS:
        assert matiere in ('Sciences', 'Technologie'), matiere
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
                    bonne = len(options[answer['index']])
                    autres = [len(o) for i, o in enumerate(options) if i != answer['index']]
                    assert bonne <= max(autres) * 2, 'bonne réponse bien plus longue : ' + str(payload)
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']), payload['statement'])
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    for v in answer['values']:
                        for c in v:
                            assert c in TAPABLE, 'caractère absent du clavier : « %s » dans %s' % (c, v)
                        assert len(v) <= 16, 'réponse trop longue : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    # LA COULEUR DES ROCHES MAGMATIQUES N-EST PAS INTERROGÉE. Le cahier les
    # dit noires et cite le granite, qui est clair. On enseigne l-écart dans
    # une explication, jamais dans une question — sinon on fait réviser une
    # faute, ou on contredit la maîtresse au moment de la note.
    tout = json.dumps([[n[5] for n in L[8]] for L in LECONS], ensure_ascii=False)
    for mot in ('couleur noire', 'de couleur'):
        assert mot not in tout, 'une question porte sur la couleur des roches : ' + mot

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-brayne-sciences-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    assert not (cles - dessinees), 'images jamais dessinées : ' + ', '.join(sorted(cles - dessinees))
    assert not (dessinees - cles), 'images jamais utilisées : ' + ', '.join(sorted(dessinees - cles))
    return len(cles), total, notions_vues


def paquet():
    return {
        'classe': CLASSE, 'enfant': ENFANT, 'lang': LANGUE,
        'lecons': [
            {
                'title': titre, 'chapter': chapitre, 'matiere': matiere,
                'taught_on': date, 'sort_order': ordre,
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
            for titre, chapitre, matiere, date, ordre, resume, img, prompt, notions in LECONS
        ],
    }


if __name__ == '__main__':
    images, items, notions = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-sciences-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, matiere, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-38s %-22s %-12s %d notions' % (ordre, titre, chapitre, matiere, len(ns)))
    print(chemin)
