# -*- coding: utf-8 -*-
"""
Les cahiers de sciences, d-histoire-géographie et d-ECM de BRAYNE (CM1),
octobre 2026 — soixante-neuf pages photographiées le 12 novembre.

LE PÈRE A DIT : GARDER CE QUI EXISTE, COMPLÉTER AVEC CE QUI MANQUE. Les
leçons déjà en base (puberté, organes reproducteurs, cycle de l-eau, eau
potable, compost, lampe à pétrole, types de sols, roches, gestion de l-eau,
locomotion, Préhistoire, grandes inventions, bassins hydrographiques,
activités au village et en ville) ne sont ni réécrites ni doublées. Restent
quatorze leçons : quatre de sciences, quatre d-ECM, six d-histoire-géographie.

RIEN N-EST AJOUTÉ AU CAHIER : chaque notion reprend une phrase qu-il a copiée.
Ce qui ne se lit pas sûrement sur la photo n-est pas posé ; chaque partie dit
quoi en tête.

LES NOTES DE LECTURE NE SONT PAS DANS LE DÉPÔT. Elles restent sur la machine
du parent.

Usage :  python work/lecons-brayne-cahier-nov12.py
"""

import importlib.util
import io
import json
import os

_ICI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('cahier_outils', os.path.join(_ICI, 'cahier-outils.py'))
outils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(outils)

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-cahier-nov12.py. ')
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
MATIERES = (
    ('Sciences', 'seed-brayne-sciences-nov12.json'),
    ('ECM', 'seed-brayne-ecm-nov12.json'),
    ('Histoire-Géographie', 'seed-brayne-histgeo-nov12.json'),
)
PARTIES = [
    'brayne-nov12-1-sciences.py',
    'brayne-nov12-2-ecm.py',
    'brayne-nov12-3-histoire-geo.py',
]

# Le cahier ne date pas ces leçons : la date du paquet ne sert qu-à l-ordre,
# et n-est pas écrite en base.
SANS_DATE = {'La germination'}

LECONS = outils.charger(_ICI, PARTIES)


def verifier():
    return outils.verifier(LECONS, [m for m, _f in MATIERES], '2026-10-')


if __name__ == '__main__':
    images, items, notions, trous = verifier()
    racine = os.path.dirname(_ICI)
    for matiere, fichier in MATIERES:
        paquet = outils.paquet(LECONS, matiere, CLASSE, ENFANT, FIGURE)
        for lecon in paquet['lecons']:
            if lecon['title'] in SANS_DATE:
                lecon['taught_on'] = None
        chemin = os.path.join(racine, 'app', 'public', fichier)
        io.open(chemin, 'w', encoding='utf-8', newline=chr(10)).write(
            json.dumps(paquet, ensure_ascii=False))
        print(chemin)

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for m, titre, chapitre, date, _r, _i, _mots, ns in sorted(LECONS, key=lambda l: (l[0], l[3])):
        print('  %-20s %s  %-56s %d notions  %2d questions'
              % (m, date, titre, len(ns), sum(len(n[5]) for n in ns)))
