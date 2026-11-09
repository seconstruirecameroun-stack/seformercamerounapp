# -*- coding: utf-8 -*-
"""
Les deux figures des notions ajoutées à la leçon « La lampe à pétrole »
(BRAYNE, CM1) lors de la relecture de la révision du 9 novembre 2026.

POURQUOI DEUX FIGURES SEULEMENT. La relecture ajoute surtout des QUESTIONS
à des notions qui existent déjà, et une question n-a pas d-image. Seules
deux notions sont neuves — le bec et la poignée de transport, puis les
précautions d-usage — et une notion, elle, doit avoir la sienne.

POURQUOI UN FICHIER À PART. Les instruments viennent de
figures-brayne-revision-nov.py, mais les figures ne peuvent pas y vivre :
ce fichier-là est contrôlé par son script de leçons, qui refuse toute
figure dessinée et non utilisée. Deux figures utilisées ailleurs le
feraient échouer.

Usage :  python work/figures-brayne-questions-nov.py
"""

import importlib.util
import os

_ICI = os.path.dirname(os.path.abspath(__file__))


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fr = _charger('figures_revision', 'figures-brayne-revision-nov.py')
Toile, SORTIE = fr.Toile, fr.SORTIE
fiche, paire = fr.fiche, fr.paire


FIGURES = [
    ('br-la-bec', 320, 320,
     lambda t: paire(t, [('le bec', 'tient la mèche'),
                         ('la poignée', 'sert à la porter')],
                     'Deux parties de plus', 'On la porte sans se brûler.')),
    ('br-la-precautions', 320, 320,
     lambda t: fiche(t, 'Les précautions', ['ne jamais verser près de la flamme',
                                            'la tenir loin des enfants',
                                            'l’éteindre avant de dormir'])),
]


def controler():
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'
    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        im = t.fini().convert('RGB')
        fond = im.getpixel((2, 2))
        for x in range(0, w, 3):
            for y in (1, h - 2):
                p = im.getpixel((x, y))
                assert sum(abs(a - b) for a, b in zip(p, fond)) < 90, \
                    '%s : le dessin touche le bord en (%d, %d)' % (cle, x, y)
        for y in range(0, h, 3):
            for x in (1, w - 2):
                p = im.getpixel((x, y))
                assert sum(abs(a - b) for a, b in zip(p, fond)) < 90, \
                    '%s : le dessin touche le bord en (%d, %d)' % (cle, x, y)


if __name__ == '__main__':
    controler()
    os.makedirs(SORTIE, exist_ok=True)
    total = 0
    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        chemin = os.path.join(SORTIE, cle + '.webp')
        t.fini().save(chemin, 'WEBP', quality=72, method=6)
        total += os.path.getsize(chemin)
    print('%d figures - %.1f Ko - 0 credit' % (len(FIGURES), total / 1024))
