# -*- coding: utf-8 -*-
"""
Les 132 images du cahier du jour de BRAYNE (octobre 2026) : 30 couvertures et
102 fiches de notion.

RIEN N-EST DÉCRIT ICI. Chaque figure est lue dans les leçons elles-mêmes
(work/lecons-brayne-francais-oct.py et ses cinq parties) : la fiche d-une
notion porte les mots de la notion, la couverture porte les mots que la leçon
annonce. Une image ne peut donc pas dire autre chose que la leçon, et une
leçon corrigée redessine son image à la prochaine exécution.

Une leçon de langue n-a pas d-objet à montrer : ce qui s-y voit, ce sont les
mots — une terminaison, une paire de synonymes, les lignes d-une règle. Les
fiches sont donc faites de texte, composé avec la police de l-app, et jamais
générées : zéro crédit.

Usage :  python work/figures-brayne-francais-oct.py
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
        _charger('lecons', 'lecons-brayne-francais-oct.py').LECONS)
