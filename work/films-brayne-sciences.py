# -*- coding: utf-8 -*-
"""
Les six films des leçons de sciences et de technologie de BRAYNE (CM1).

Même registre que les mathématiques — la figure est dessinée, jamais générée
— appliqué cette fois à des objets du monde : un cycle, une lampe, des
cellules. La règle de la charte tient pour les mêmes raisons : une leçon qui
annonce cinq parties doit être illustrée par une lampe où l'enfant qui compte
trouve cinq.

Deux choix tiennent tout le reste.

Le film du cycle de l'eau est bâti sur UNE scène jouée quatre fois, chaque
plan allumant une étape de plus. Le paysage se complète sous les yeux de
l'enfant au lieu de changer à chaque phrase : c'est le cycle lui-même qui est
le fil conducteur, et non quatre images qui se succèdent.

Les deux leçons sur le corps n'ont aucune image de corps. Ni silhouette, ni
schéma anatomique. Ce qui bouge à l'écran, ce sont les mots de la leçon sur
des étiquettes, deux intervalles d'âge qui se remplissent, deux ondes pour la
voix — large chez le garçon, serrée chez la fille — et les deux cellules
reproductrices, dont la queue du spermatozoïde bat. L'enfant révise ce que la
maîtresse a écrit, sans qu'une image s'en mêle.

BRAYNE est en CM1 : ses phrases peuvent être plus longues que celles de
KLEIN. La limite passe de quatorze à dix-huit mots, pas davantage — au-delà,
une phrase cesse de tenir dans un plan de six secondes.

Usage :  python work/films-brayne-sciences.py
"""

import io
import json
import os

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')
SCENES = ('fleche', 'barres', 'etiquettes', 'cellules', 'ensemble', 'paires',
          'boucle', 'cycle', 'verres', 'origines', 'sols', 'lampe')
MOTS_MAX = 18

SKY = 'SKY'
LILAC = 'LILAC'

FILMS = [
    (
        'puberte', 'Les changements liés à la puberté', 'Les changements liés à la puberté',
        'Un enfant devient adulte, et le cahier dit exactement comment.',
        [
            ('La puberté est le passage de l’enfant à l’état adulte.',
             {'scene': 'fleche', 'avant': 'enfant', 'apres': 'adulte'},
             ['LA PUBERTÉ'], 'content'),
            ('Cela commence entre douze et quinze ans chez les garçons, onze et quatorze chez les filles.',
             {'scene': 'barres', 'min': 10, 'max': 16,
              'lignes': [['garçons', 12, 15, SKY], ['filles', 11, 14, LILAC]]},
             ['LES ÂGES'], 'content'),
            ('Chez le garçon, les épaules s’élargissent et la voix devient grave.',
             {'scene': 'etiquettes', 'onde': 'grave',
              'mots': ['les épaules s’élargissent', 'les muscles se développent',
                       'la voix devient grave']},
             ['LE GARÇON'], 'encourage'),
            ('Chez la fille, le bassin s’élargit et la voix devient fine.',
             {'scene': 'etiquettes', 'onde': 'fine',
              'mots': ['les seins se développent', 'le bassin s’élargit',
                       'la voix devient fine']},
             ['LA FILLE'], 'encourage'),
            ('Les testicules produisent les spermatozoïdes, les ovaires produisent les ovules.',
             {'scene': 'cellules'},
             ['LES CELLULES'], 'fete'),
        ],
    ),
    (
        'organes', 'Les organes reproducteurs', 'Les organes reproducteurs',
        'Des organes épars, un cadre qui les rassemble, puis le rôle de chacun.',
        [
            ('L’appareil reproducteur est l’ensemble des organes qui permettent de se reproduire.',
             {'scene': 'ensemble'},
             ['UN ENSEMBLE'], 'content'),
            ('Chez l’homme : le pénis, les deux testicules, les canaux et la prostate.',
             {'scene': 'etiquettes',
              'mots': ['le pénis', 'les deux testicules', 'les canaux', 'la prostate']},
             ['CHEZ L’HOMME'], 'content'),
            ('Chez la femme : la vulve, l’utérus, le vagin et les deux ovaires.',
             {'scene': 'etiquettes',
              'mots': ['la vulve', 'l’utérus', 'le vagin', 'les deux ovaires']},
             ['CHEZ LA FEMME'], 'content'),
            ('Les ovaires produisent les ovules, et l’utérus accueille la gestation.',
             {'scene': 'paires',
              'gauche': ['les testicules', 'les ovaires', 'l’utérus'],
              'droite': ['les spermatozoïdes', 'les ovules', 'la gestation']},
             ['CHACUN SON RÔLE'], 'fete'),
        ],
    ),
    (
        'cycle', 'Le cycle de l’eau dans la nature', 'Le cycle de l’eau dans la nature',
        'Un paysage qui se complète étape par étape, jusqu’à refermer la boucle.',
        [
            ('Le cycle de l’eau est le trajet que parcourt l’eau pour revenir à son point de départ.',
             {'scene': 'boucle'},
             ['UN TRAJET'], 'content'),
            ('Sous l’effet de la chaleur, l’eau se transforme en vapeur : c’est l’évaporation.',
             {'scene': 'cycle', 'jusqua': 1, 'nom': 'évaporation'},
             ['ÉVAPORATION'], 'content'),
            ('Au contact des zones froides, la vapeur devient un nuage : c’est la condensation.',
             {'scene': 'cycle', 'jusqua': 2, 'nom': 'condensation'},
             ['CONDENSATION'], 'content'),
            ('L’eau tombe sous forme de pluie : c’est la précipitation.',
             {'scene': 'cycle', 'jusqua': 3, 'nom': 'précipitation'},
             ['PRÉCIPITATION'], 'encourage'),
            ('Elle ruisselle jusqu’aux mers et aux fleuves, et le cycle recommence.',
             {'scene': 'cycle', 'jusqua': 4, 'nom': 'ruissellement'},
             ['RUISSELLEMENT'], 'fete'),
        ],
    ),
    (
        'eau-potable', 'L’eau potable', 'L’eau potable',
        'Deux verres, et tout ce qu’il faut faire pour passer de l’un à l’autre.',
        [
            ('Une eau potable est celle qu’on peut boire sans danger pour notre santé.',
             {'scene': 'verres'},
             ['POTABLE'], 'content'),
            ('On peut la javelliser et la filtrer, la bouillir et la filtrer, ou la décanter.',
             {'scene': 'paires',
              'gauche': ['javelliser', 'bouillir', 'javelliser'],
              'droite': ['et filtrer', 'et filtrer', 'et décanter']},
             ['TROIS FAÇONS'], 'encourage'),
            ('L’eau maintient la température, transporte les nutriments et évacue les déchets.',
             {'scene': 'etiquettes', 'numerote': True,
              'mots': ['la température', 'le transport des nutriments',
                       'l’évacuation des déchets']},
             ['TROIS RÔLES'], 'fete'),
        ],
    ),
    (
        'compost', 'L’amélioration des sols : le compost', 'L’amélioration des sols : le compost',
        'Ce qui vient des plantes et des bêtes revient nourrir la terre.',
        [
            ('Le compost est un engrais naturel fait de matières animales et végétales.',
             {'scene': 'origines'},
             ['LE COMPOST'], 'content'),
            ('On enrichit un sol pauvre en utilisant le compost.',
             {'scene': 'sols'},
             ['UN SOL RICHE'], 'encourage'),
            ('Feuilles mortes, cendre de bois, restes de repas, épluchures : tout est biodégradable.',
             {'scene': 'etiquettes',
              'mots': ['les feuilles mortes', 'la cendre de bois', 'les restes de repas',
                       'les épluchures', 'la litière d’animaux']},
             ['BIODÉGRADABLE'], 'fete'),
        ],
    ),
    (
        'lampe', 'La lampe à pétrole', 'La lampe à pétrole',
        'Une flamme qui s’allume, cinq parties qui se nomment, et le rôle de chacune.',
        [
            ('La lampe à pétrole, appelée aussi lampe tempête, est un appareil d’éclairage.',
             {'scene': 'lampe', 'allumage': True},
             ['LAMPE TEMPÊTE'], 'content'),
            ('Elle a cinq parties : le réservoir, la molette, la mèche, le verre et la grille.',
             {'scene': 'lampe', 'numeros': True},
             ['CINQ PARTIES'], 'encourage'),
            ('Le réservoir contient le pétrole, la mèche porte la flamme, le verre la protège.',
             {'scene': 'paires',
              'gauche': ['le réservoir', 'la mèche', 'le verre', 'la grille'],
              'droite': ['le pétrole', 'la flamme', 'le vent', 'l’air']},
             ['CHACUNE SON RÔLE'], 'fete'),
        ],
    ),
]


def verifier():
    plans = 0
    for cle, titre, lecon, fil, blocs in FILMS:
        for voix, scene, mots, humeur in blocs:
            plans += 1
            assert "'" not in voix, 'apostrophe droite : ' + voix
            assert len(voix.split()) <= MOTS_MAX, 'phrase trop longue : ' + voix
            assert scene['scene'] in SCENES, scene['scene']
            assert humeur in HUMEURS, humeur
            assert len(mots) <= 2, mots
            for m in mots:
                assert len(m) <= 18 and m == m.upper(), m
            if scene['scene'] == 'etiquettes':
                assert 1 <= len(scene['mots']) <= 5, scene
                assert scene.get('onde') in (None, 'grave', 'fine'), scene
            if scene['scene'] == 'paires':
                assert len(scene['gauche']) == len(scene['droite']), scene
                assert 1 <= len(scene['gauche']) <= 5, scene
            if scene['scene'] == 'cycle':
                assert 1 <= scene['jusqua'] <= 4, scene
            if scene['scene'] == 'barres':
                for nom, a, b, _ton in scene['lignes']:
                    # Une borne inversée dessinerait une barre de longueur
                    # négative, et l’intervalle du cahier serait faux.
                    assert scene['min'] <= a < b <= scene['max'], scene
    # Le film du cycle allume une étape de plus à chaque plan, dans l’ordre.
    cycle = [b[1] for b in dict((f[0], f[4]) for f in FILMS)['cycle']
             if b[1]['scene'] == 'cycle']
    assert [s['jusqua'] for s in cycle] == [1, 2, 3, 4], cycle
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, lecon, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-' + cle)
        os.makedirs(dossier, exist_ok=True)

        manifeste = {
            'title': titre, 'lesson': lecon, 'registre': 'figures de sciences',
            'style': 'Figures dessinées et Fredoka sur fond pastel, composé',
            'aspect_ratio': '16:9', 'language': 'fr', 'narrator': 'Céline',
            'mascotte': 'Niba', 'through_line': fil,
            'blocks': [
                {'n': i + 1, 'vo_line': v, 'scene': s, 'keywords': k, 'niba': h}
                for i, (v, s, k, h) in enumerate(blocs)
            ],
        }
        io.open(os.path.join(dossier, 'script_manifest.json'), 'w',
                encoding='utf-8', newline='\n').write(
            json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n')

        md = ['# %s — script verrouillé' % titre, '',
              'Leçon : %s (CM1)' % lecon,
              'Registre : figures de sciences. Rien n’est généré, tout est dessiné.',
              'Voix : Céline, articulation claire, débit posé.', '',
              'Fil conducteur : %s' % fil, '', '## Narration', '']
        md += ['%d. %s' % (i + 1, v) for i, (v, _, _, _) in enumerate(blocs)]
        md += ['', '## Ce qui bouge à l’écran', '']
        md += ['%d. %s — %s' % (i + 1, s['scene'],
                                json.dumps({k: v for k, v in s.items() if k != 'scene'},
                                           ensure_ascii=False))
               for i, (_, s, _, _) in enumerate(blocs)]
        md += ['', '## Mots affichés', '']
        md += ['%d. %s' % (i + 1, ' · '.join(k)) for i, (_, _, k, _) in enumerate(blocs)]
        md += ['', '## Humeur de Niba', '']
        md += ['%d. %s' % (i + 1, h) for i, (_, _, _, h) in enumerate(blocs)]
        io.open(os.path.join(dossier, 'script.md'), 'w',
                encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')


if __name__ == '__main__':
    plans = verifier()
    ecrire()
    print('%d films - %d plans - 0 image generee' % (len(FILMS), plans))
    for cle, titre, _l, _f, blocs in FILMS:
        print('  video-%-12s %d plans  %s' % (cle, len(blocs), titre))
