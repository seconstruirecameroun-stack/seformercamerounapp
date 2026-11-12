# -*- coding: utf-8 -*-
"""
Les images des cahiers de sciences, d-ECM et d-histoire-géographie de BRAYNE
(octobre 2026, photographiés le 12 novembre) : une couverture par leçon et une
fiche par notion.

RIEN N-EST DÉCRIT ICI. Chaque figure est lue dans les leçons elles-mêmes
(work/lecons-brayne-cahier-nov12.py et ses trois parties) : la fiche d-une
notion porte les mots de la notion, la couverture porte les mots que la leçon
annonce. Une image ne peut donc pas dire autre chose que la leçon.

Les fiches sont faites de texte, composé avec la police de l-app, et jamais
générées : zéro crédit.

Usage :  python work/figures-brayne-cahier-nov12.py
"""

import importlib.util
import os

_ICI = os.path.dirname(os.path.abspath(__file__))


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == '__main__':
    _charger('cahier_figures', 'cahier-figures.py').dessiner(
        _charger('lecons', 'lecons-brayne-cahier-nov12.py').LECONS)
