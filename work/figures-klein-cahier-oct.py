# -*- coding: utf-8 -*-
"""
Les images du cahier du jour de KLEIN (octobre 2026) : une couverture par
leçon, une fiche par notion, lues dans les leçons elles-mêmes
(work/lecons-klein-cahier-oct.py). Le dessin est fait par
work/cahier-figures.py, commun aux deux cahiers.

Usage :  python work/figures-klein-cahier-oct.py
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
        _charger('lecons', 'lecons-klein-cahier-oct.py').LECONS)
