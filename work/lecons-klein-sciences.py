# -*- coding: utf-8 -*-
"""
Les trois leçons de sciences du cahier de KLEIN (CE1), octobre 2026.

Transcrites depuis trois photos : la reproduction des animaux (lundi
12 octobre), les soins aux animaux domestiques (vendredi 16 octobre), et les
milieux de vie des végétaux (page sans date).

Rien n'est ajouté au cahier. Les mots, les listes et les exemples sont ceux
des pages. Les corrections sont orthographiques et grammaticales : les
accents manquants sont remis, « ovovivipares qui idorent leurs œufs » est lu
« qui incubent leurs œufs », et les listes à l'orthographe hésitante
(« gresson », « hibzous ») sont rétablies en cresson et hibiscus.

Les trois pages portent des en-têtes différents — Sciences de la vie,
Activités agro-pastorales, Éducation à l'environnement — mais relèvent toutes
de la même matière au programme de CE1 : Sciences et technologies. L'en-tête
du cahier devient le chapitre, ce qui garde la nuance sans éparpiller les
leçons dans trois dossiers d'une seule leçon chacun.

KLEIN est en CE1 : questions courtes, mots simples, jamais plus de deux mots
à écrire. Chaque notion a ses quatre étapes — Découverte, Entraînement,
Maîtrise, Défi — sans quoi l'étape manquante serait infranchissable.

Usage :  python work/lecons-klein-sciences.py
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, '
    'no numbers, no watermark, no real person, no brand. '
)

MATIERE = 'Sciences et technologies'
COULEUR = '#d08a3c'

# Une leçon : (titre, chapitre, date, ordre, résumé, image, consigne, notions)
# Une notion : (kind, phrase, image, consigne, [explications], [questions])
# Une question : (kind, niveau, payload, answer, explain)

LECONS = [
    (
        'La reproduction des animaux', 'Sciences de la vie', '2026-10-12', 7,
        'Il y a trois modes de reproduction chez les animaux. Les ovipares pondent des œufs. '
        'Les vivipares donnent directement naissance aux petits. Les ovovivipares gardent leurs '
        'œufs dans le ventre avant de donner naissance.',
        'rp-reproduction',
        'A hen beside her eggs on the left, a goat with her kid in the middle, and a coiled snake on the right, '
        'on a soft plain background, calm and friendly.',
        [
            (
                'liste',
                'Il y a trois modes de reproduction chez les animaux : ovipare, vivipare et ovovivipare.',
                'rp-trois',
                'Three simple rounded panels side by side on a plain background: a clutch of eggs, a mother animal with her baby, '
                'and a snake with a soft glow at its belly.',
                [
                    ('simple', 'Les animaux ne font pas tous leurs petits de la même façon. Il y a trois façons.'),
                    ('analogie', 'C’est comme aller à l’école : à pied, en voiture ou à moto. Trois chemins, une seule arrivée.'),
                ],
                [
                    ('qcm', 1, {'question': 'Combien y a-t-il de modes de reproduction ?',
                                'options': ['Trois', 'Deux', 'Cinq']},
                     {'index': 0}, 'Le cahier en compte trois.'),
                    ('qcm', 1, {'question': 'Un mode de reproduction cité est…',
                                'options': ['ovipare', 'carnivore', 'herbivore']},
                     {'index': 0}, 'Ovipare, vivipare, ovovivipare.'),
                    ('qcm', 2, {'question': 'Lequel n’est pas un mode de reproduction ?',
                                'options': ['Le mode herbivore', 'Le mode ovipare', 'Le mode vivipare', 'Le mode ovovivipare']},
                     {'index': 0}, 'Herbivore dit ce que l’animal mange, pas comment il fait ses petits.'),
                    ('chronologie', 3, {'question': 'Remets les trois modes dans l’ordre du cahier.',
                                        'tokens': ['ovipare', 'vivipare', 'ovovivipare'],
                                        'consigne': 'Touche les mots dans l’ordre.'},
                     {'order': [0, 1, 2]}, 'Ovipare, vivipare, puis ovovivipare.'),
                    ('texte_a_trous', 3, {'text': 'Il y a {{1}} modes de reproduction chez les {{2}}.', 'blanks': 2},
                     {'values': ['trois', 'animaux']}, 'Trois modes, chez les animaux.'),
                    ('vrai_faux', 4, {'statement': 'Tous les animaux se reproduisent de la même façon.'},
                     {'value': False}, 'Non : il y a trois modes.'),
                ],
            ),
            (
                'definition',
                'Les ovipares se reproduisent en pondant des œufs : la poule, les poissons, l’escargot.',
                'rp-ovipare',
                'A hen sitting beside a small nest of eggs, with a fish and a snail nearby, plain soft background.',
                [
                    ('simple', 'Un ovipare pond des œufs. Le petit grandit dans l’œuf, puis il sort.'),
                    ('visuel', 'Pense à la poule du quartier : elle pond, elle couve, et les poussins sortent.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les ovipares se reproduisent en…',
                                'options': ['pondant des œufs', 'donnant naissance', 'changeant de peau']},
                     {'index': 0}, 'Ovipare veut dire qui pond des œufs.'),
                    ('qcm', 1, {'question': 'La poule est un animal…',
                                'options': ['ovipare', 'vivipare', 'ovovivipare']},
                     {'index': 0}, 'La poule pond des œufs.'),
                    ('qcm', 2, {'question': 'Lequel de ces animaux est ovipare ?',
                                'options': ['Le poisson', 'La vache', 'La chèvre', 'La chatte']},
                     {'index': 0}, 'Le poisson pond des œufs.'),
                    ('dictee', 3, {'phrase': 'Les ovipares pondent des œufs.', 'langue': 'fr'},
                     {'phrase': 'Les ovipares pondent des œufs.'}, 'Ovipare : qui pond des œufs.'),
                    ('qcm', 4, {'question': 'Un canard pond des œufs. Il est donc…',
                                'options': ['ovipare', 'vivipare', 'ovovivipare']},
                     {'index': 0}, 'Il pond : il est ovipare.'),
                ],
            ),
            (
                'definition',
                'Les vivipares donnent directement naissance aux petits : la chèvre, la vache, la chatte.',
                'rp-vivipare',
                'A goat standing beside her kid, a cow with her calf behind, soft plain background, gentle warm light.',
                [
                    ('simple', 'Un vivipare met son petit au monde tout formé. Il n’y a pas d’œuf à casser.'),
                    ('analogie', 'C’est comme la chatte de la maison : ses chatons naissent déjà vivants.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les vivipares donnent…',
                                'options': ['directement naissance aux petits', 'des œufs', 'seulement du lait']},
                     {'index': 0}, 'Le petit naît déjà formé.'),
                    ('qcm', 1, {'question': 'La vache est un animal…',
                                'options': ['vivipare', 'ovipare', 'ovovivipare']},
                     {'index': 0}, 'La vache met bas un veau.'),
                    ('qcm', 2, {'question': 'Clique sur un animal vivipare.',
                                'images': ['rp-vivipare', 'rp-ovipare', 'rp-ovovivipare', 'rp-trois']},
                     {'index': 0}, 'La chèvre et son petit.'),
                    ('texte_a_trous', 3, {'text': 'Les {{1}} donnent directement naissance aux {{2}}.', 'blanks': 2},
                     {'values': ['vivipares', 'petits']}, 'Vivipares : naissance directe.'),
                    ('vrai_faux', 4, {'statement': 'La chatte pond des œufs.'},
                     {'value': False}, 'Non : elle est vivipare.'),
                ],
            ),
            (
                'definition',
                'Les ovovivipares gardent leurs œufs dans le ventre avant de donner naissance : la vipère.',
                'rp-ovovivipare',
                'A coiled snake on warm sand with a soft glow showing small eggs inside her body, plain background.',
                [
                    ('simple', 'L’œuf reste dans le ventre de la mère. Le petit en sort déjà vivant.'),
                    ('pas_a_pas', 'La mère fabrique un œuf, elle le garde en elle, l’œuf s’ouvre dedans, le petit naît.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où l’ovovivipare garde-t-il ses œufs ?',
                                'options': ['Dans son ventre', 'Dans un nid', 'Dans l’eau']},
                     {'index': 0}, 'Les œufs restent dans le ventre.'),
                    ('qcm', 1, {'question': 'La vipère est un animal…',
                                'options': ['ovovivipare', 'ovipare', 'vivipare']},
                     {'index': 0}, 'C’est l’exemple du cahier.'),
                    ('association', 2, {'question': 'Relie chaque animal à son mode.',
                                        'gauche': ['La poule', 'La vache', 'La vipère'],
                                        'droite': ['Ovipare', 'Vivipare', 'Ovovivipare']},
                     {'order': [0, 1, 2]}, 'Pond, met bas, garde ses œufs en elle.'),
                    ('dictee', 3, {'phrase': 'La vipère est ovovivipare.', 'langue': 'fr'},
                     {'phrase': 'La vipère est ovovivipare.'}, 'Un seul mot à bien écrire.'),
                    ('qcm', 4, {'question': 'Il garde ses œufs dans le ventre puis met bas. Il est…',
                                'options': ['ovovivipare', 'ovipare', 'vivipare']},
                     {'index': 0}, 'Les deux à la fois : œuf dedans, petit vivant.'),
                ],
            ),
        ],
    ),
    (
        'Les soins aux animaux domestiques', 'Activités agro-pastorales', '2026-10-16', 8,
        'Les animaux peuvent être atteints de maladies : les maladies de la peau, la grippe, la rage, '
        'les infections pulmonaires, l’insuffisance rénale, la peste, les vers et la newcastle. Pour les '
        'éviter, il faut les vacciner, nettoyer leur habitat et les conduire chez un vétérinaire.',
        'sa-soins',
        'A calm farmyard with a goat, a hen and a dog, a clean water trough and a swept shelter, warm morning light.',
        [
            (
                'liste',
                'Les maladies de la peau de l’animal sont la gale et la teigne.',
                'sa-gale',
                'A close friendly view of a goat with a few dull patches on its coat, a soft brush and a bowl of clean water beside it.',
                [
                    ('simple', 'La gale et la teigne abîment la peau et le poil de l’animal.'),
                    ('visuel', 'On les voit : le poil tombe par plaques et la peau devient rugueuse.'),
                ],
                [
                    ('qcm', 1, {'question': 'La gale est une maladie…',
                                'options': ['de la peau', 'des poumons', 'des yeux']},
                     {'index': 0}, 'La gale touche la peau.'),
                    ('qcm', 1, {'question': 'Quelle maladie touche la peau ?',
                                'options': ['La teigne', 'La grippe', 'La peste']},
                     {'index': 0}, 'La teigne est une maladie de la peau.'),
                    ('qcm', 2, {'question': 'Quelles sont les deux maladies de la peau ?',
                                'options': ['La gale et la teigne', 'La toux et la bave',
                                            'La peste et les vers', 'La rage et la grippe']},
                     {'index': 0}, 'Le cahier en cite deux.'),
                    ('texte_a_trous', 3, {'text': 'Les maladies de la peau sont la {{1}} et la {{2}}.', 'blanks': 2},
                     {'values': ['gale', 'teigne']}, 'Gale et teigne.'),
                    ('vrai_faux', 4, {'statement': 'La gale se voit sur la peau de l’animal.'},
                     {'value': True}, 'Oui : c’est une maladie de la peau.'),
                ],
            ),
            (
                'liste',
                'La grippe de l’animal se reconnaît à la toux, à la bave et à la fatigue.',
                'sa-grippe',
                'A hen resting with drooping wings beside a bowl of water, a soft blanket of warm light, plain background.',
                [
                    ('simple', 'Un animal grippé tousse, bave et n’a plus de force.'),
                    ('analogie', 'C’est comme toi quand tu es grippé : tu tousses et tu es fatigué.'),
                ],
                [
                    ('qcm', 1, {'question': 'Quel signe montre la grippe ?',
                                'options': ['La toux', 'La peau rouge', 'Les cornes']},
                     {'index': 0}, 'La toux est un signe de la grippe.'),
                    ('qcm', 1, {'question': 'La grippe donne à l’animal…',
                                'options': ['de la fatigue', 'de la force', 'de la joie']},
                     {'index': 0}, 'Elle fatigue l’animal.'),
                    ('qcm', 2, {'question': 'Quels sont les trois signes de la grippe ?',
                                'options': ['Toux, bave, fatigue', 'Toux, cornes, poils',
                                            'Bave, dents, queue', 'Fatigue, plumes, lait']},
                     {'index': 0}, 'Toux, bave et fatigue.'),
                    ('chronologie', 3, {'question': 'Remets la phrase dans le bon ordre.',
                                        'tokens': ['La grippe', 'se reconnaît', 'à la toux', 'et à la bave'],
                                        'consigne': 'Touche les mots dans l’ordre de la phrase.'},
                     {'order': [0, 1, 2, 3]}, 'La grippe se reconnaît à la toux et à la bave.'),
                    ('vrai_faux', 4, {'statement': 'Un animal qui tousse et qui bave peut avoir la grippe.'},
                     {'value': True}, 'Ce sont deux des trois signes.'),
                ],
            ),
            (
                'definition',
                'La rage se reconnaît à une sécrétion excessive de salive et à l’agressivité.',
                'sa-rage',
                'A dog standing alone behind a low fence, mouth wet, a small warning distance kept by a calm empty foreground.',
                [
                    ('simple', 'Un animal enragé bave beaucoup et devient méchant. On ne s’en approche pas.'),
                    ('histoire', 'Quand un chien du quartier bave et grogne sans raison, on prévient un adulte.'),
                ],
                [
                    ('qcm', 1, {'question': 'La rage rend l’animal…',
                                'options': ['agressif', 'calme', 'joyeux']},
                     {'index': 0}, 'L’agressivité est un signe de la rage.'),
                    ('qcm', 1, {'question': 'Quel liquide coule beaucoup avec la rage ?',
                                'options': ['La salive', 'Le lait', 'L’eau']},
                     {'index': 0}, 'Une sécrétion excessive de salive.'),
                    ('qcm', 2, {'question': 'Quels sont les deux signes de la rage ?',
                                'options': ['Beaucoup de salive et l’agressivité', 'La toux et la bave',
                                            'La gale et la teigne', 'Les vers et la peste']},
                     {'index': 0}, 'Salive et agressivité.'),
                    ('dictee', 3, {'phrase': 'La rage rend l’animal agressif.', 'langue': 'fr'},
                     {'phrase': 'La rage rend l’animal agressif.'}, 'Agressif prend deux s.'),
                    ('vrai_faux', 4, {'statement': 'Un chien qui bave beaucoup et grogne peut avoir la rage.'},
                     {'value': True}, 'Ce sont les deux signes du cahier.'),
                ],
            ),
            (
                'liste',
                'L’animal peut aussi avoir une infection pulmonaire, une insuffisance rénale, la peste, les vers ou la newcastle.',
                'sa-autres',
                'Four small rounded cards on a plain background: a pair of lungs, a kidney, a lying hen, and a small worm shape, all soft and friendly.',
                [
                    ('simple', 'D’autres maladies touchent les poumons, les reins, ou viennent des vers.'),
                    ('visuel', 'L’insuffisance rénale fatigue l’animal et lui donne la diarrhée.'),
                ],
                [
                    ('qcm', 1, {'question': 'L’infection pulmonaire touche…',
                                'options': ['les poumons', 'la peau', 'les dents']},
                     {'index': 0}, 'Pulmonaire vient de poumon.'),
                    ('qcm', 1, {'question': 'Laquelle est une maladie de l’animal ?',
                                'options': ['La newcastle', 'La propreté', 'La gentillesse']},
                     {'index': 0}, 'La newcastle est dans la liste du cahier.'),
                    ('qcm', 2, {'question': 'L’insuffisance rénale donne…',
                                'options': ['de la fatigue et la diarrhée', 'de la toux',
                                            'des taches sur la peau', 'beaucoup de salive']},
                     {'index': 0}, 'Fatigue et diarrhée.'),
                    ('texte_a_trous', 3, {'text': 'L’animal peut avoir la {{1}}, les vers ou la {{2}}.', 'blanks': 2},
                     {'values': ['peste', 'newcastle']}, 'La peste et la newcastle.'),
                    ('vrai_faux', 4, {'statement': 'La newcastle est une maladie des animaux.'},
                     {'value': True}, 'Elle est citée dans le cahier.'),
                ],
            ),
            (
                'relation',
                'Pour éviter ces maladies, il faut vacciner les animaux, nettoyer leur habitat et les conduire chez un vétérinaire.',
                'sa-prevention',
                'A clean swept animal shelter with fresh straw, a bucket of clean water, and a small medical bag resting on a stool.',
                [
                    ('simple', 'On vaccine, on nettoie, et on va voir le vétérinaire. Trois gestes.'),
                    ('pas_a_pas', 'D’abord vacciner, ensuite nettoyer l’habitat, et si l’animal est malade, le vétérinaire.'),
                ],
                [
                    ('qcm', 1, {'question': 'Que faut-il faire pour éviter les maladies ?',
                                'options': ['Vacciner les animaux', 'Les laisser seuls', 'Les faire courir']},
                     {'index': 0}, 'Le vaccin protège.'),
                    ('qcm', 1, {'question': 'Chez qui conduit-on un animal malade ?',
                                'options': ['Chez un vétérinaire', 'Chez le boulanger', 'Chez le tailleur']},
                     {'index': 0}, 'Le vétérinaire soigne les animaux.'),
                    ('association', 2, {'question': 'Relie chaque geste à ce qui va avec.',
                                        'gauche': ['Vacciner', 'Nettoyer', 'Conduire'],
                                        'droite': ['Le vaccin', 'L’habitat', 'Le vétérinaire']},
                     {'order': [0, 1, 2]}, 'Trois gestes, trois mots.'),
                    ('texte_a_trous', 3, {'text': 'Il faut {{1}} les animaux et nettoyer leur {{2}}.', 'blanks': 2},
                     {'values': ['vacciner', 'habitat']}, 'Vacciner et nettoyer.'),
                    ('vrai_faux', 4, {'statement': 'Un habitat sale protège les animaux des maladies.'},
                     {'value': False}, 'Au contraire : il faut le nettoyer.'),
                ],
            ),
        ],
    ),
    (
        'Les milieux de vie des végétaux', 'Éducation à l’environnement', None, 9,
        'Les végétaux sont des êtres vivants qui ont des racines. Certains poussent sur la terre, '
        'd’autres poussent dans l’eau, et d’autres encore poussent dans la boue.',
        'mv-milieux',
        'One wide calm scene: a mango tree on dry red earth on the left, water lilies on a pond in the middle, '
        'and mangrove roots in dark mud on the right.',
        [
            (
                'definition',
                'Les végétaux sont des êtres vivants qui ont des racines.',
                'mv-vegetaux',
                'A small plant shown whole on a plain background, with its roots visible below the soil line, soft and clear.',
                [
                    ('simple', 'Un végétal est vivant : il grandit, il boit, il a des racines.'),
                    ('visuel', 'Les racines sont la partie cachée, sous la terre ou sous l’eau.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les végétaux sont des êtres…',
                                'options': ['vivants', 'morts', 'en pierre']},
                     {'index': 0}, 'Ils sont vivants.'),
                    ('qcm', 1, {'question': 'Qu’ont tous les végétaux ?',
                                'options': ['Des racines', 'Des ailes', 'Des dents']},
                     {'index': 0}, 'Tous ont des racines.'),
                    ('qcm', 2, {'question': 'Les végétaux ont tous…',
                                'options': ['des racines', 'des plumes', 'des pattes', 'des écailles']},
                     {'index': 0}, 'C’est ce qui les définit dans le cahier.'),
                    ('dictee', 3, {'phrase': 'Les végétaux sont des êtres vivants.', 'langue': 'fr'},
                     {'phrase': 'Les végétaux sont des êtres vivants.'}, 'Végétaux prend un accent.'),
                    ('vrai_faux', 4, {'statement': 'Une pierre est un végétal.'},
                     {'value': False}, 'Une pierre n’est pas vivante.'),
                ],
            ),
            (
                'liste',
                'Certains végétaux poussent sur la terre : le manguier, le palmier, l’hibiscus.',
                'mv-terrestre',
                'A mango tree and an oil palm growing on red laterite earth, a hibiscus flower in front, dry warm light.',
                [
                    ('simple', 'Ceux-là poussent sur la terre ferme. On dit qu’ils sont terrestres.'),
                    ('visuel', 'Le manguier de la cour est un végétal terrestre.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le manguier pousse…',
                                'options': ['sur la terre', 'dans l’eau', 'dans la boue']},
                     {'index': 0}, 'Le manguier est terrestre.'),
                    ('qcm', 1, {'question': 'Un végétal terrestre est…',
                                'options': ['le palmier', 'le nénuphar', 'le palétuvier']},
                     {'index': 0}, 'Le palmier pousse sur la terre.'),
                    ('qcm', 2, {'question': 'Clique sur un végétal qui pousse sur la terre.',
                                'images': ['mv-terrestre', 'mv-aquatique', 'mv-marecage', 'mv-vegetaux']},
                     {'index': 0}, 'Le manguier et le palmier.'),
                    ('texte_a_trous', 3, {'text': 'Le {{1}} et le palmier poussent sur la {{2}}.', 'blanks': 2},
                     {'values': ['manguier', 'terre']}, 'Manguier, palmier : la terre.'),
                    ('vrai_faux', 4, {'statement': 'Un arbre planté dans la cour est un végétal terrestre.'},
                     {'value': True}, 'Il pousse sur la terre.'),
                ],
            ),
            (
                'liste',
                'D’autres poussent dans l’eau : le roseau, le nénuphar, l’algue, le cresson.',
                'mv-aquatique',
                'A calm pond with water lilies floating, tall reeds at the edge and green algae under the clear water.',
                [
                    ('simple', 'Ceux-là poussent dans l’eau. On dit qu’ils sont aquatiques.'),
                    ('analogie', 'Le nénuphar est posé sur l’eau comme une assiette verte.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le nénuphar pousse…',
                                'options': ['dans l’eau', 'sur la terre', 'dans la boue']},
                     {'index': 0}, 'Le nénuphar est aquatique.'),
                    ('qcm', 1, {'question': 'Un végétal aquatique est…',
                                'options': ['l’algue', 'le manguier', 'le raphia']},
                     {'index': 0}, 'L’algue pousse dans l’eau.'),
                    ('association', 2, {'question': 'Relie chaque végétal à son milieu.',
                                        'gauche': ['Le manguier', 'Le nénuphar', 'Le palétuvier'],
                                        'droite': ['La terre', 'L’eau', 'La boue']},
                     {'order': [0, 1, 2]}, 'Terre, eau, boue.'),
                    ('dictee', 3, {'phrase': 'Le nénuphar pousse dans l’eau.', 'langue': 'fr'},
                     {'phrase': 'Le nénuphar pousse dans l’eau.'}, 'Nénuphar prend deux accents.'),
                    ('vrai_faux', 4, {'statement': 'Le roseau est un végétal aquatique.'},
                     {'value': True}, 'Il pousse dans l’eau.'),
                ],
            ),
            (
                'liste',
                'D’autres poussent dans la boue : le papyrus, le raphia, le palétuvier.',
                'mv-marecage',
                'Mangrove trees with arching stilt roots in dark shining mud, tall papyrus stems behind, soft humid light.',
                [
                    ('simple', 'Ceux-là poussent dans la boue d’un marécage.'),
                    ('visuel', 'Le palétuvier tient debout sur des racines en arceaux, les pieds dans la boue.'),
                ],
                [
                    ('qcm', 1, {'question': 'Le palétuvier pousse…',
                                'options': ['dans la boue', 'sur un rocher', 'dans le sable sec']},
                     {'index': 0}, 'Le palétuvier pousse dans la boue.'),
                    ('qcm', 1, {'question': 'Quel végétal pousse dans la boue ?',
                                'options': ['Le raphia', 'Le manguier', 'L’algue']},
                     {'index': 0}, 'Le raphia pousse dans la boue.'),
                    ('qcm', 2, {'question': 'Les végétaux de la boue poussent dans…',
                                'options': ['un marécage', 'un désert', 'une maison', 'une rivière rapide']},
                     {'index': 0}, 'La boue, c’est le marécage.'),
                    ('texte_a_trous', 3, {'text': 'Le {{1}} et le raphia poussent dans la {{2}}.', 'blanks': 2},
                     {'values': ['papyrus', 'boue']}, 'Papyrus, raphia, palétuvier.'),
                    ('vrai_faux', 4, {'statement': 'Le palétuvier pousse dans un marécage.'},
                     {'value': True}, 'Le marécage, c’est la boue.'),
                ],
            ),
        ],
    ),
]

NIVEAUX_ATTENDUS = {1, 2, 3, 4}


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total = set(), 0
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
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
                total += 1
                niveaux.add(niveau)
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                if ikind == 'qcm':
                    assert len(payload['question']) <= 80, 'question trop longue : ' + payload['question']
                    if 'images' in payload:
                        assert len(payload['images']) == 4, payload
                        assert 0 <= answer['index'] < 4, payload
                    else:
                        options = payload['options']
                        assert 2 <= len(options) <= 4, payload
                        assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                        assert 0 <= answer['index'] < len(options), payload
                        for o in options:
                            assert len(o) <= 60, 'option trop longue pour un CE1 : ' + o
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 90, payload
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous pour un CE1 : ' + payload['text']
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


def litteral(valeur):
    """Un littéral JSON prêt pour SQL : les apostrophes typographiques passent."""
    return "'" + json.dumps(valeur, ensure_ascii=False) + "'"


ENTETE = """-- Se Former Cameroun — les trois leçons de sciences du cahier de KLEIN (CE1)
--
-- Transcrites depuis trois photos : la reproduction des animaux (lundi
-- 12 octobre 2026), les soins aux animaux domestiques (vendredi 16 octobre
-- 2026), et les milieux de vie des végétaux (page sans date).
--
-- Rien n'est ajouté au cahier. Les mots, les listes et les exemples sont ceux
-- des pages. Les corrections sont orthographiques : accents rétablis,
-- « gresson » lu cresson, « hibzous » lu hibiscus, et « qui idorent leurs
-- œufs » lu « qui incubent leurs œufs ».
--
-- Les trois pages portent des en-têtes différents — Sciences de la vie,
-- Activités agro-pastorales, Éducation à l'environnement — mais relèvent de
-- la même matière au programme de CE1 : Sciences et technologies. L'en-tête
-- du cahier devient le chapitre.
--
-- Chaque notion a ses quatre étapes : Découverte, Entraînement, Maîtrise et
-- Défi. Une étape sans question serait infranchissable, et la leçon
-- resterait bloquée pour toujours.
--
-- Les leçons naissent en 'approved' : elles ont été relues par le parent qui
-- les a photographiées, au moment de les fournir.
--
-- Réexécutable : la fonction ne s'applique qu'une fois.

create or replace function public.seed_sciences_klein(p_parent uuid)
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

  -- La matière existe déjà : le référentiel de l'école la crée pour le CE1.
  -- On la retrouve par son libellé et sa classe plutôt que de la recréer, pour
  -- ne pas éparpiller les leçons dans deux dossiers du même nom.
  select id into v_subject from subjects
   where parent_id = p_parent and label = '%s'
     and (class_id = v_class or class_id is null)
   order by class_id nulls last
   limit 1;
  if v_subject is null then
    insert into subjects (parent_id, class_id, label, color)
    values (p_parent, v_class, '%s', '%s')
    returning id into v_subject;
  end if;
""" % (MATIERE, MATIERE, COULEUR)

PIED = """  return 1;
end;
$$;

select public.seed_sciences_klein(parent_id)
  from children
 where first_name = 'KLEIN'
   and not exists (select 1 from lessons where title = 'La reproduction des animaux')
 limit 1;
"""


def sql():
    out = [ENTETE]
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        out.append("  -- %s (%s)" % (titre, chapitre))
        out.append("  insert into lessons")
        out.append("    (parent_id, subject_id, class_id, title, summary, lang, chapter, taught_on,")
        out.append("     sort_order, status, illustration, illustration_prompt)")
        out.append("  values (p_parent, v_subject, v_class, %s," % litteral(titre))
        out.append("    %s," % litteral(resume))
        out.append("    'fr', %s, %s, %d, 'approved', %s,"
                   % (litteral(chapitre), ("date '%s'" % date) if date else 'null', ordre, litteral(img)))
        out.append("    %s)" % litteral(STYLE + prompt))
        out.append("  returning id into v_lesson;\n")

        for ni, (kind, phrase, nimg, nprompt, expl, items) in enumerate(notions, start=1):
            out.append("  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,")
            out.append("     illustration, illustration_prompt)")
            out.append("  values (p_parent, v_lesson, '%s', %s, %d, 'approved', %s,"
                       % (kind, litteral(phrase), ni, litteral(nimg)))
            out.append("    %s)" % litteral(STYLE + nprompt))
            out.append("  returning id into v_notion;\n")

            out.append("  insert into explanations (parent_id, notion_id, register, body, status) values")
            out.append(',\n'.join("    (p_parent, v_notion, '%s', %s, 'approved')" % (r, litteral(b))
                                  for r, b in expl) + ';\n')

            out.append("  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values")
            lignes = []
            for ikind, niveau, payload, answer, explain in items:
                lignes.append(
                    "    (p_parent, v_notion, '%s', %d,\n     %s::jsonb,\n     %s::jsonb, %s, 'approved')"
                    % (ikind, niveau, litteral(payload), litteral(answer), litteral(explain))
                )
            out.append(',\n'.join(lignes) + ';\n')

    out.append(PIED)
    return '\n'.join(out)


if __name__ == '__main__':
    images, items = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'supabase', 'migrations', '20261017030000_lecons_klein_sciences.sql')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(sql())

    notions = sum(len(l[7]) for l in LECONS)
    print('%d lecons - %d notions - %d questions - %d images a produire'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-36s %-28s %s  %d notions' % (titre, chapitre, date or 'sans date', len(ns)))
    print(chemin)
