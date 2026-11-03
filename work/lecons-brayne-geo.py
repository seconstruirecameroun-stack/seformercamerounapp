# -*- coding: utf-8 -*-
"""
Les grandes zones agricoles du Cameroun — géographie, BRAYNE (CM1),
lundi 2 novembre 2026.

Deux leçons, parce que le cahier lui-même pose deux étoiles : les cultures
vivrières d-un côté, les cultures de rente de l-autre. Les mélanger ferait
une leçon de treize notions où l-essentiel — ce qui distingue les deux — se
perdrait au milieu.

Tout vient du cahier, rien n-y est ajouté. Deux lignes étaient illisibles
sur la photo (le bord de page écrase un mot, et une ligne mêle le rouge et
le bleu) : elles ont été demandées au père plutôt que devinées. Ce sont
« les ignames cultivés à l-Ouest » et « le palmier à huile dans le Sud ».

La leçon est une leçon de carte : « quelle culture, quelle région » ne
s-apprend pas dans une liste, il s-apprend sur le pays. Chaque notion de
région porte donc la carte du Cameroun avec SA zone allumée et les autres
en retrait — la même carte à chaque fois, pour que l-enfant finisse par la
connaître.

Usage :  python work/lecons-brayne-geo.py
"""

import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-geo.py. '

MATIERE = 'Géographie'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'fr'
CHAPITRE = 'Les grandes zones agricoles du Cameroun'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

LECONS = [
    (
        'L’agriculture et les cultures vivrières', CHAPITRE, '2026-11-02', 24,
        'L’agriculture est une activité qui consiste à cultiver la terre. Au Cameroun on distingue '
        'deux grandes sortes de cultures. Les cultures vivrières sont destinées à la consommation '
        'des populations locales : on les mange sur place, dans le pays.',
        'ag-vivrieres-couv',
        'La carte du Cameroun, les zones vivrières allumées, un panier de récolte posé devant.',
        [
            (
                'definition',
                'L’agriculture est une activité qui consiste à cultiver la terre.',
                'ag-agriculture',
                'Une houe plantée dans des sillons de terre retournée, sous un soleil pastel.',
                [
                    ('simple', 'Cultiver la terre : la préparer, y semer, et récolter ce qui pousse.'),
                    ('analogie', 'Le champ derrière la maison, c’est déjà de l’agriculture — en plus petit.'),
                ],
                [
                    ('qcm', 1, {'question': 'L’agriculture consiste à…',
                                'options': ['cultiver la terre', 'construire des maisons',
                                            'élever des poissons']},
                     {'index': 0}, 'C’est l’activité qui consiste à cultiver la terre.'),
                    ('vrai_faux', 1, {'statement': 'L’agriculture est une activité qui consiste à cultiver la terre.'},
                     {'value': True}, 'Oui, c’est la définition du cahier.'),
                    ('qcm', 2, {'question': 'Laquelle de ces activités est de l’agriculture ?',
                                'options': ['Semer du maïs dans un champ', 'Vendre du poisson au marché',
                                            'Réparer une route']},
                     {'index': 0}, 'Semer et récolter, c’est cultiver la terre.'),
                    ('texte_a_trous', 3, {'text': 'L’agriculture consiste à cultiver la {{1}}.', 'blanks': 1},
                     {'values': ['terre']}, 'La terre.'),
                    ('qcm', 4, {'question': 'L’agriculture, c’est cultiver…',
                                'options': ['la terre', 'la mer', 'la ville']},
                     {'index': 0}, 'La terre.'),
                ],
            ),
            (
                'definition',
                'Les cultures vivrières sont destinées à la consommation des populations locales.',
                'ag-vivrieres',
                'Un plat de famille posé sur une natte, entouré de tubercules et d’épis.',
                [
                    ('simple', 'Vivrières vient de vivre : ce sont les cultures qui nourrissent les gens d’ici.'),
                    ('analogie', 'Ce que ta mère achète au marché pour le repas du soir vient d’une culture vivrière.'),
                    ('pas_a_pas', 'On sème. On récolte. On mange sur place. Rien ne part à l’étranger.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les cultures vivrières sont destinées à…',
                                'options': ['la consommation des populations locales',
                                            'la vente à l’étranger', 'la fabrication de tissus']},
                     {'index': 0}, 'Elles nourrissent les populations locales.'),
                    ('vrai_faux', 1, {'statement': 'Les cultures vivrières sont vendues à l’étranger.'},
                     {'value': False}, 'Non. Ce sont les cultures de rente qui partent à l’étranger.'),
                    ('association', 2, {'question': 'Relie chaque mot à ce qu’il veut dire.',
                                        'gauche': ['Culture vivrière', 'Population locale'],
                                        'droite': ['Elle nourrit les gens du pays',
                                                   'Les gens qui vivent ici']},
                     {'order': [0, 1]}, 'Vivrière : pour vivre, ici.'),
                    ('texte_a_trous', 3, {'text': 'Les cultures {{1}} nourrissent les populations locales.', 'blanks': 1},
                     {'values': ['vivrières']}, 'Vivrières.'),
                    ('vrai_faux', 4, {'statement': 'Une culture vivrière se mange dans le pays où elle pousse.'},
                     {'value': True}, 'Oui.'),
                ],
            ),
            (
                'liste',
                'Le mil, le maïs, le sorgho et les arachides sont cultivés principalement à Maroua, Garoua et Ngaoundéré.',
                'ag-nord',
                'La carte du Cameroun, la zone du Nord allumée, trois points pour Maroua, Garoua et Ngaoundéré.',
                [
                    ('simple', 'Quatre cultures, et toutes dans le Nord : le mil, le maïs, le sorgho, les arachides.'),
                    ('visuel', 'Sur la carte, ce sont les trois villes alignées du haut : Maroua, Garoua, Ngaoundéré.'),
                    ('pas_a_pas', 'Maroua tout en haut, Garoua au-dessous, Ngaoundéré plus bas encore. Les trois sont dans le Nord.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on principalement le mil et le sorgho ?',
                                'options': ['À Maroua, Garoua et Ngaoundéré', 'À Douala et Kribi',
                                            'À Bamenda et Dschang']},
                     {'index': 0}, 'Les trois villes du Nord citées par le cahier.'),
                    ('vrai_faux', 1, {'statement': 'Les arachides sont cultivées principalement dans le Nord.'},
                     {'value': True}, 'Oui, avec le mil, le maïs et le sorgho.'),
                    ('chronologie', 2, {'question': 'Range ces villes du Nord vers le Sud.',
                                        'tokens': ['Maroua', 'Garoua', 'Ngaoundéré'],
                                        'consigne': 'La plus au nord en premier.'},
                     {'order': [0, 1, 2]}, 'Maroua, puis Garoua, puis Ngaoundéré.'),
                    ('qcm', 2, {'question': 'Laquelle de ces cultures n’est pas dans la liste du Nord ?',
                                'options': ['Le cacao', 'Le mil', 'Le sorgho']},
                     {'index': 0}, 'Le cacao est une culture de rente, cultivée à l’Ouest.'),
                    ('texte_a_trous', 3, {'text': 'Le mil, le maïs, le sorgho et les arachides poussent dans le {{1}}.', 'blanks': 1},
                     {'values': ['Nord']}, 'Dans le Nord.'),
                    ('qcm', 4, {'question': 'Maroua, Garoua et Ngaoundéré se trouvent…',
                                'options': ['dans le Nord', 'sur la côte', 'à l’Est']},
                     {'index': 0}, 'Dans le Nord.'),
                ],
            ),
            (
                'liste',
                'Les pommes de terre et les ignames sont cultivés à l’Ouest.',
                'ag-ouest',
                'La carte du Cameroun, la zone de l’Ouest allumée, une pomme de terre et une igname posées dessus.',
                [
                    ('simple', 'Deux tubercules, une seule région : les pommes de terre et les ignames, à l’Ouest.'),
                    ('visuel', 'L’Ouest, c’est la partie en relief à gauche de la carte, vers Bamenda.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on les pommes de terre et les ignames ?',
                                'options': ['À l’Ouest', 'Dans le Nord', 'À l’Est']},
                     {'index': 0}, 'À l’Ouest.'),
                    ('vrai_faux', 1, {'statement': 'Les ignames sont cultivés à l’Ouest.'},
                     {'value': True}, 'Oui, avec les pommes de terre.'),
                    ('association', 2, {'question': 'Relie chaque culture à sa région.',
                                        'gauche': ['Les pommes de terre', 'Le mil'],
                                        'droite': ['L’Ouest', 'Le Nord']},
                     {'order': [0, 1]}, 'Les pommes de terre à l’Ouest, le mil dans le Nord.'),
                    ('texte_a_trous', 3, {'text': 'Les pommes de terre et les ignames sont cultivés à l’{{1}}.', 'blanks': 1},
                     {'values': ['Ouest']}, 'À l’Ouest.'),
                    ('qcm', 4, {'question': 'Les ignames poussent…',
                                'options': ['à l’Ouest', 'dans le Nord', 'dans le Littoral']},
                     {'index': 0}, 'À l’Ouest.'),
                ],
            ),
            (
                'liste',
                'Le manioc, le macabo et la patate sont cultivés dans le Centre, le Sud et le Littoral.',
                'ag-centre',
                'La carte du Cameroun, le Centre, le Sud et le Littoral allumés, du manioc et du macabo devant.',
                [
                    ('simple', 'Trois cultures, trois régions voisines : le Centre, le Sud et le Littoral.'),
                    ('visuel', 'Ce sont les régions du bas de la carte, de Yaoundé jusqu’à la mer.'),
                    ('analogie', 'Le bâton de manioc du marché vient de ces régions-là.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on le manioc, le macabo et la patate ?',
                                'options': ['Dans le Centre, le Sud et le Littoral', 'Dans le Nord seulement',
                                            'À l’Est seulement']},
                     {'index': 0}, 'Dans le Centre, le Sud et le Littoral.'),
                    ('vrai_faux', 1, {'statement': 'Le manioc est cultivé dans le Nord du Cameroun.'},
                     {'value': False}, 'Non : dans le Centre, le Sud et le Littoral.'),
                    ('association', 2, {'question': 'Relie chaque culture à sa région.',
                                        'gauche': ['Le manioc', 'Les ignames', 'Le sorgho'],
                                        'droite': ['Le Centre, le Sud et le Littoral', 'L’Ouest', 'Le Nord']},
                     {'order': [0, 1, 2]}, 'Chaque culture a sa zone.'),
                    ('texte_a_trous', 3, {'text': 'Le macabo et la patate poussent dans le Centre, le Sud et le {{1}}.', 'blanks': 1},
                     {'values': ['Littoral']}, 'Le Littoral.'),
                    ('qcm', 4, {'question': 'Le macabo pousse…',
                                'options': ['dans le Centre', 'dans le Nord', 'à l’Est']},
                     {'index': 0}, 'Dans le Centre, avec le Sud et le Littoral.'),
                ],
            ),
            (
                'relation',
                'Les légumes frais sont cultivés dans les villes.',
                'ag-legumes',
                'Des maisons de ville au fond, des planches de légumes verts cultivées devant.',
                [
                    ('simple', 'Les légumes frais se cultivent près de ceux qui les mangent : dans les villes.'),
                    ('pas_a_pas', 'Un légume frais se garde mal. Plus le champ est près de la ville, plus il arrive frais.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on les légumes frais ?',
                                'options': ['Dans les villes', 'Seulement dans le Nord',
                                            'Seulement à l’étranger']},
                     {'index': 0}, 'Dans les villes, d’après le cahier.'),
                    ('vrai_faux', 1, {'statement': 'Les légumes frais sont cultivés dans les villes.'},
                     {'value': True}, 'Oui.'),
                    ('qcm', 2, {'question': 'Pourquoi cultiver les légumes frais près des villes ?',
                                'options': ['Ils arrivent plus frais', 'Ils poussent plus gros',
                                            'Ils coûtent plus cher']},
                     {'index': 0}, 'Un légume frais se garde mal : plus le trajet est court, mieux c’est.'),
                    ('texte_a_trous', 3, {'text': 'Les légumes frais sont cultivés dans les {{1}}.', 'blanks': 1},
                     {'values': ['villes']}, 'Dans les villes.'),
                    ('vrai_faux', 4, {'statement': 'Les légumes frais sont une culture vivrière.'},
                     {'value': True}, 'Oui : ils nourrissent les populations locales.'),
                ],
            ),
        ],
    ),
    (
        'Les cultures de rente', CHAPITRE, '2026-11-02', 25,
        'Les cultures de rente, ou cultures industrielles, encore appelées cultures d’exportation, '
        'sont transformées dans les industries ou sont vendues à l’étranger. Chacune a sa région : '
        'le cacao, le café et le thé à l’Ouest, le coton au Nord, la canne à sucre au Centre, le '
        'palmier à huile dans le Sud et le tabac à l’Est.',
        'ag-rente-couv',
        'La carte du Cameroun avec les cinq zones de rente allumées, chacune marquée de sa culture.',
        [
            (
                'definition',
                'Les cultures de rente sont transformées dans les industries ou vendues à l’étranger. On les appelle aussi industrielles ou d’exportation.',
                'ag-rente',
                'Une usine et un navire : la récolte entre d’un côté, repart de l’autre.',
                [
                    ('simple', 'Elles ne sont pas faites pour être mangées ici : elles sont transformées ou vendues ailleurs.'),
                    ('analogie', 'Le cacao part, le chocolat revient. C’est cela, une culture d’exportation.'),
                    ('pas_a_pas', 'On récolte. L’usine transforme, ou le bateau emporte. L’argent revient au pays.'),
                ],
                [
                    ('qcm', 1, {'question': 'Les cultures de rente sont…',
                                'options': ['transformées ou vendues à l’étranger',
                                            'mangées par les populations locales',
                                            'cultivées dans les villes']},
                     {'index': 0}, 'Transformées dans les industries ou vendues à l’étranger.'),
                    ('qcm', 1, {'question': 'Quel autre nom donne-t-on aux cultures de rente ?',
                                'options': ['Cultures d’exportation', 'Cultures vivrières',
                                            'Cultures de saison']},
                     {'index': 0}, 'Cultures industrielles, ou cultures d’exportation.'),
                    ('association', 2, {'question': 'Relie chaque sorte de culture à sa destination.',
                                        'gauche': ['Culture vivrière', 'Culture de rente'],
                                        'droite': ['Les populations locales', 'L’industrie et l’étranger']},
                     {'order': [0, 1]}, 'Vivrière : ici. De rente : ailleurs.'),
                    ('texte_a_trous', 3, {'text': 'Les cultures de {{1}} sont vendues à l’étranger.', 'blanks': 1},
                     {'values': ['rente']}, 'De rente.'),
                    ('vrai_faux', 4, {'statement': 'Une culture de rente est aussi appelée culture d’exportation.'},
                     {'value': True}, 'Oui, ou culture industrielle.'),
                ],
            ),
            (
                'liste',
                'Le cacao, le café et le thé sont cultivés à l’Ouest.',
                'ag-cacao',
                'La carte du Cameroun, l’Ouest allumé, une cabosse de cacao, des grains de café et une feuille de thé.',
                [
                    ('simple', 'Trois cultures de rente dans la même région : cacao, café, thé, à l’Ouest.'),
                    ('visuel', 'Trois boissons et une pâte, toutes venues du même côté de la carte.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on le cacao, le café et le thé ?',
                                'options': ['À l’Ouest', 'Au Nord', 'À l’Est']},
                     {'index': 0}, 'À l’Ouest.'),
                    ('vrai_faux', 1, {'statement': 'Le café est une culture vivrière.'},
                     {'value': False}, 'Non : c’est une culture de rente.'),
                    ('association', 2, {'question': 'Relie chaque culture de rente à sa région.',
                                        'gauche': ['Le cacao', 'Le coton'],
                                        'droite': ['L’Ouest', 'Le Nord']},
                     {'order': [0, 1]}, 'Le cacao à l’Ouest, le coton au Nord.'),
                    ('texte_a_trous', 3, {'text': 'Le cacao, le café et le thé sont cultivés à l’{{1}}.', 'blanks': 1},
                     {'values': ['Ouest']}, 'À l’Ouest.'),
                    ('qcm', 4, {'question': 'Le thé est cultivé…',
                                'options': ['à l’Ouest', 'au Nord', 'dans le Sud']},
                     {'index': 0}, 'À l’Ouest.'),
                ],
            ),
            (
                'liste',
                'Le coton est cultivé au Nord du Cameroun.',
                'ag-coton',
                'La carte du Cameroun, le Nord allumé, une capsule de coton ouverte posée dessus.',
                [
                    ('simple', 'Le coton, c’est le Nord — la même région que le mil et le sorgho.'),
                    ('analogie', 'Le coton ne se mange pas : il devient du tissu. C’est pour cela qu’il est de rente.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on le coton ?',
                                'options': ['Au Nord du Cameroun', 'Dans le Sud', 'Dans le Littoral']},
                     {'index': 0}, 'Au Nord du Cameroun.'),
                    ('vrai_faux', 1, {'statement': 'Le coton est cultivé au Nord du Cameroun.'},
                     {'value': True}, 'Oui.'),
                    ('qcm', 2, {'question': 'Quelle culture partage la région du coton ?',
                                'options': ['Le sorgho', 'Le cacao', 'Le palmier à huile']},
                     {'index': 0}, 'Le sorgho est aussi cultivé dans le Nord.'),
                    ('texte_a_trous', 3, {'text': 'Le coton est cultivé au {{1}} du Cameroun.', 'blanks': 1},
                     {'values': ['Nord']}, 'Au Nord.'),
                    ('qcm', 4, {'question': 'Le coton sert surtout à…',
                                'options': ['faire du tissu', 'faire du pain', 'faire de l’huile']},
                     {'index': 0}, 'Il est transformé en tissu : c’est une culture de rente.'),
                ],
            ),
            (
                'liste',
                'La canne à sucre est cultivée au Centre.',
                'ag-canne',
                'La carte du Cameroun, le Centre allumé, trois tiges de canne à sucre liées devant.',
                [
                    ('simple', 'La canne à sucre pousse au Centre, autour de Yaoundé.'),
                    ('visuel', 'Sur la carte, le Centre est la région du milieu, là où se trouve la capitale.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on la canne à sucre ?',
                                'options': ['Au Centre', 'À l’Ouest', 'À l’Est']},
                     {'index': 0}, 'Au Centre.'),
                    ('vrai_faux', 1, {'statement': 'La canne à sucre est cultivée au Centre.'},
                     {'value': True}, 'Oui.'),
                    ('association', 2, {'question': 'Relie chaque culture de rente à sa région.',
                                        'gauche': ['La canne à sucre', 'Le cacao', 'Le coton'],
                                        'droite': ['Le Centre', 'L’Ouest', 'Le Nord']},
                     {'order': [0, 1, 2]}, 'Chacune a sa région.'),
                    ('texte_a_trous', 3, {'text': 'La canne à sucre est cultivée au {{1}}.', 'blanks': 1},
                     {'values': ['Centre']}, 'Au Centre.'),
                    ('qcm', 4, {'question': 'La canne à sucre est une culture…',
                                'options': ['de rente', 'vivrière', 'de ville']},
                     {'index': 0}, 'De rente : elle est transformée à l’usine.'),
                ],
            ),
            (
                'liste',
                'Le palmier à huile est cultivé dans le Sud.',
                'ag-palmier',
                'La carte du Cameroun, le Sud allumé, un palmier à huile et son régime de fruits.',
                [
                    ('simple', 'Le palmier à huile, c’est le Sud — la région la plus humide du pays.'),
                    ('analogie', 'L’huile rouge de la cuisine vient de ses régimes de fruits.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on le palmier à huile ?',
                                'options': ['Dans le Sud', 'Dans le Nord', 'À l’Est']},
                     {'index': 0}, 'Dans le Sud.'),
                    ('vrai_faux', 1, {'statement': 'Le palmier à huile est cultivé dans le Nord.'},
                     {'value': False}, 'Non : dans le Sud.'),
                    ('qcm', 2, {'question': 'Que donne le palmier à huile ?',
                                'options': ['De l’huile', 'Du sucre', 'Du tissu']},
                     {'index': 0}, 'De l’huile, d’où son nom.'),
                    ('texte_a_trous', 3, {'text': 'Le palmier à huile est cultivé dans le {{1}}.', 'blanks': 1},
                     {'values': ['Sud']}, 'Dans le Sud.'),
                    ('qcm', 4, {'question': 'Le palmier à huile pousse…',
                                'options': ['dans le Sud', 'au Nord', 'à l’Ouest']},
                     {'index': 0}, 'Dans le Sud.'),
                ],
            ),
            (
                'liste',
                'Le tabac est cultivé à l’Est du pays.',
                'ag-tabac',
                'La carte du Cameroun, l’Est allumé, deux larges feuilles de tabac posées dessus.',
                [
                    ('simple', 'Le tabac, c’est l’Est — la grande région forestière à droite de la carte.'),
                    ('visuel', 'Sur la carte, l’Est est le grand bloc de droite, le plus large du pays.'),
                ],
                [
                    ('qcm', 1, {'question': 'Où cultive-t-on le tabac ?',
                                'options': ['À l’Est du pays', 'Au Nord', 'Dans le Littoral']},
                     {'index': 0}, 'À l’Est du pays.'),
                    ('vrai_faux', 1, {'statement': 'Le tabac est cultivé à l’Est du pays.'},
                     {'value': True}, 'Oui.'),
                    ('association', 2, {'question': 'Relie chaque culture à sa région.',
                                        'gauche': ['Le tabac', 'Le palmier à huile', 'La canne à sucre'],
                                        'droite': ['L’Est', 'Le Sud', 'Le Centre']},
                     {'order': [0, 1, 2]}, 'Chacune à sa place sur la carte.'),
                    ('texte_a_trous', 3, {'text': 'Le tabac est cultivé à l’{{1}} du pays.', 'blanks': 1},
                     {'values': ['Est']}, 'À l’Est.'),
                    ('qcm', 4, {'question': 'Le tabac est une culture…',
                                'options': ['de rente', 'vivrière', 'de légume']},
                     {'index': 0}, 'De rente.'),
                ],
            ),
            (
                'relation',
                'Ce qui distingue les deux sortes de cultures, c’est à qui elles sont destinées : aux populations locales, ou à l’industrie et à l’étranger.',
                'ag-difference',
                'Deux flèches partant d’un même champ : l’une vers une case, l’autre vers un navire.',
                [
                    ('simple', 'La même terre, deux destinations. C’est la destination qui donne le nom.'),
                    ('pas_a_pas', 'Demande-toi où va la récolte. Si elle reste ici, elle est vivrière. Si elle part, elle est de rente.'),
                    ('analogie', 'Le maïs du repas reste à la maison ; le cacao prend le bateau.'),
                ],
                [
                    ('qcm', 1, {'question': 'Qu’est-ce qui distingue une culture vivrière d’une culture de rente ?',
                                'options': ['À qui elle est destinée', 'La couleur de la plante',
                                            'La saison des pluies']},
                     {'index': 0}, 'La destination : ici, ou à l’industrie et à l’étranger.'),
                    ('association', 2, {'question': 'Range chaque culture dans sa sorte.',
                                        'gauche': ['Le manioc', 'Le cacao', 'Le mil', 'Le coton'],
                                        'droite': ['Vivrière', 'De rente', 'Vivrière aussi', 'De rente aussi']},
                     {'order': [0, 1, 2, 3]}, 'Le manioc et le mil se mangent ici ; le cacao et le coton partent.'),
                    ('texte_a_trous', 3, {'text': 'Une culture qui part à l’étranger est une culture de {{1}}.', 'blanks': 1},
                     {'values': ['rente']}, 'De rente.'),
                    ('vrai_faux', 4, {'statement': 'Le maïs et le cacao sont tous les deux des cultures de rente.'},
                     {'value': False}, 'Non : le maïs est vivrier, le cacao est de rente.'),
                ],
            ),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total = set(), 0
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
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
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
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
                    assert len(payload['statement']) <= 110, payload
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        # Le clavier n-a pas de touche espace dans un texte à
                        # trous : une réponse en deux mots serait impossible.
                        assert ' ' not in v, 'réponse en plusieurs mots : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))
    return len(cles), total


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
    images, items = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-geo.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    notions = sum(len(l[7]) for l in LECONS)
    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-44s %s  %d notions' % (titre, date, len(ns)))
    print(chemin)
