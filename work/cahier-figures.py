# -*- coding: utf-8 -*-
"""
Les images d-un cahier du jour, dessinées depuis ses leçons.

Une couverture par leçon, une fiche par notion, et rien qui soit décrit deux
fois : la figure est lue dans la leçon elle-même. Commun aux cahiers de
BRAYNE et de KLEIN, comme cahier-outils.py.

Une leçon de langue n-a pas d-objet à montrer : ce qui s-y voit, ce sont les
mots. Les fiches sont donc faites de texte, composé avec la police de l-app,
et jamais générées : zéro crédit.
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
Toile, SORTIE = fk.Toile, fk.SORTIE


def _signes(t, couples, titre):
    """Comme fk.paire, mais le signe de gauche est écrit en grand."""
    fk._legende(t, 56, titre, 17, fk.INK)
    pas = 46 if len(couples) > 3 else 52
    haut = 84 + max(0, (3 - len(couples))) * 22
    for i, (signe, nom) in enumerate(couples):
        y = haut + i * pas
        t.rrect(16, y, 148, y + 38, 9, fill=fk.WHITE_WARM, bord=fk.INK, trait=1.8)
        t.rrect(172, y, 304, y + 38, 9, fill=fk.GOLD, bord=fk.INK, trait=1.8)
        t.texte((82, y + 19), signe, 30, fk.INK)
        taille = 15
        while fk._mesure(t, nom, taille) > 120 and taille > 9:
            taille -= 1
        t.texte((238, y + 19), nom, taille, fk.INK)
        t.ligne([(148, y + 19), (172, y + 19)], fk.INK, 1.8)


def _notion(figure):
    if figure[0] == 'signes':
        _genre, titre, couples = figure
        return lambda t: _signes(t, couples, titre)
    if figure[0] == 'fiche':
        _genre, titre, lignes, vif = figure
        # Une fiche courte se pose plus bas : trois lignes collées en haut
        # d-un carré laissaient la moitié de l-image vide.
        haut = 92 + max(0, 4 - len(lignes)) * 20
        return lambda t: fk.fiche(t, titre, lignes, haut=haut, vif=vif)
    _genre, titre, couples = figure
    return lambda t: fk.paire(t, couples, titre)


def figures(LECONS):
    sortie = []
    for _m, titre, _chap, _date, _resume, img, mots, notions in LECONS:
        sortie.append((img, 960, 540,
                       (lambda ti, mo: lambda t: fk._couv_mots(t, ti, mo))(titre, mots)))
        for _kind, _phrase, nimg, figure, _expl, _items in notions:
            sortie.append((nimg, 320, 320, _notion(figure)))
    return sortie


def controler(FIGURES):
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
                assert sum(abs(a - b) for a, b in zip(p, fond)) < 90,                     '%s : le dessin touche le bord en (%d, %d)' % (cle, x, y)
        for y in range(0, h, 3):
            for x in (1, w - 2):
                p = im.getpixel((x, y))
                assert sum(abs(a - b) for a, b in zip(p, fond)) < 90,                     '%s : le dessin touche le bord en (%d, %d)' % (cle, x, y)
        if (w, h) == (960, 540):
            assert fk.fv._hors_bande(t.fini()) == 0,                 'couverture %s : dessin hors de la fiche' % cle


def dessiner(LECONS):
    FIGURES = figures(LECONS)
    controler(FIGURES)
    os.makedirs(SORTIE, exist_ok=True)
    total = 0
    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        chemin = os.path.join(SORTIE, cle + '.webp')
        t.fini().save(chemin, 'WEBP', quality=74, method=6)
        total += os.path.getsize(chemin)
    print('%d figures - %.1f Ko - 0 credit' % (len(FIGURES), total / 1024))
