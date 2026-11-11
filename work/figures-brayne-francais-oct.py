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


fk = _charger('figures_klein_tic', 'figures-klein-tic-oct.py')
lecons = _charger('lecons_brayne_francais', 'lecons-brayne-francais-oct.py')

Toile, SORTIE = fk.Toile, fk.SORTIE


def _notion(figure):
    if figure[0] == 'fiche':
        _genre, titre, lignes, vif = figure
        # Une fiche courte se pose plus bas : trois lignes collées en haut
        # d-un carré laissaient la moitié de l-image vide.
        haut = 92 + max(0, 4 - len(lignes)) * 20
        return lambda t: fk.fiche(t, titre, lignes, haut=haut, vif=vif)
    _genre, titre, couples = figure
    return lambda t: fk.paire(t, couples, titre)


def _figures():
    sortie = []
    for _m, titre, _chap, _date, _resume, img, mots, notions in lecons.LECONS:
        sortie.append((img, 960, 540,
                       (lambda ti, mo: lambda t: fk._couv_mots(t, ti, mo))(titre, mots)))
        for _kind, _phrase, nimg, figure, _expl, _items in notions:
            sortie.append((nimg, 320, 320, _notion(figure)))
    return sortie


FIGURES = _figures()


def controler():
    """Aucun dessin ne touche le bord, aucune couverture ne sort de sa fiche."""
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
        if (w, h) == (960, 540):
            assert fk.fv._hors_bande(t.fini()) == 0, \
                'couverture %s : dessin hors de la fiche' % cle


if __name__ == '__main__':
    controler()
    os.makedirs(SORTIE, exist_ok=True)
    total = 0
    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        chemin = os.path.join(SORTIE, cle + '.webp')
        t.fini().save(chemin, 'WEBP', quality=74, method=6)
        total += os.path.getsize(chemin)
    print('%d figures - %.1f Ko - 0 credit' % (len(FIGURES), total / 1024))
