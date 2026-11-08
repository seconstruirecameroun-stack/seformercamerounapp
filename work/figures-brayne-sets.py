# -*- coding: utf-8 -*-
"""
Les figures des cinq leçons sur les ensembles — fiche de révision CM1
« Sets and Venn diagrams », BRAYNE, novembre 2026.

UNE CONTRAINTE COMMANDE TOUT CE FICHIER : Fredoka n-a aucun des signes
d-ensembles. Vérifié dans la table de caractères de la police — ni le signe
d-appartenance, ni celui d-inclusion, ni l-intersection, ni l-union, ni
l-ensemble vide n-y sont. Écrits comme du texte, ils sortiraient en carrés
vides sur chaque image. Ils sont donc DESSINÉS : un arc, deux jambes, une
barre oblique. Le dessin a un second mérite sur le texte — l-enfant voit le
geste de la main qui trace le signe, qui est précisément ce qu-on lui
demande de reproduire au cahier.

(Dans l-application, le même signe écrit dans une question s-affiche
normalement : le navigateur va chercher la lettre manquante dans la police
du système. Le défaut ne concerne que les images, dessinées par PIL, qui
n-a pas ce secours.)

Quatre instruments, et les vingt-sept figures en sortent :

  accolades    « A = { 2, 4, 6, 8 } » dans son cadre. C-est l-écriture
               exacte du cahier, accolades et virgules comprises : un
               ensemble qu-on montre sans ses accolades n-apprend pas à
               les écrire
  signe        le signe tracé, en grand, avec son nom dessous en toutes
               lettres. Un signe sans son nom ne se lit pas à voix haute,
               et c-est à voix haute qu-on le retient
  venn         le rectangle, les ovales, la région teintée — repris des
               figures de l-unité 3, pour que ce soit le MÊME dessin que
               celui de ses quatre leçons de diagrammes
  fiche        une liste posée ligne à ligne, pour les suites de nombres
               et pour les étapes

Usage :  python work/figures-brayne-sets.py
"""

import importlib.util
import math
import os

_ICI = os.path.dirname(os.path.abspath(__file__))


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fm = _charger('figures_maths', 'figures-maths.py')
fv = _charger('figures_venn', 'figures-venn.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

ROUGE = (183, 66, 52)

# La bande qu-un bandeau de leçon montre réellement d-une couverture.
BANDEAU = (184, 356)


def _mesure(t, s, taille):
    return t.d.textlength(s, font=t.pol(taille)) / S


def _arc(t, boite, debut, fin, couleur=INK, trait=7):
    x0, y0, x1, y1 = boite
    t.d.arc([x0 * S, y0 * S, x1 * S, y1 * S], debut, fin,
            fill=couleur, width=max(1, int(trait * S)))


# --------------------------------------------------------------------------
# Les signes, tracés et non écrits

def _barre(t, cx, cy, r, couleur=ROUGE, trait=7):
    """La barre oblique qui NIE un signe. Toujours du même sens."""
    t.ligne([(cx - r * 0.85, cy + r * 0.95), (cx + r * 0.85, cy - r * 0.95)], couleur, trait)


def _appartient(t, cx, cy, r, trait=7):
    """Le signe d-appartenance : un arc ouvert à droite, barré au milieu."""
    _arc(t, (cx - r, cy - r, cx + r, cy + r), 35, 325, trait=trait)
    t.ligne([(cx - r * 0.62, cy), (cx + r * 0.72, cy)], INK, trait)


def _inclus(t, cx, cy, r, trait=7):
    """Le signe d-inclusion : le même arc, sans la barre du milieu."""
    _arc(t, (cx - r, cy - r, cx + r, cy + r), 35, 325, trait=trait)


def _intersection(t, cx, cy, r, trait=7):
    """L-intersection : une arche, et ses deux jambes qui descendent."""
    _arc(t, (cx - r, cy - r, cx + r, cy + r), 180, 360, trait=trait)
    t.ligne([(cx - r, cy), (cx - r, cy + r * 0.95)], INK, trait)
    t.ligne([(cx + r, cy), (cx + r, cy + r * 0.95)], INK, trait)


def _union(t, cx, cy, r, trait=7):
    """L-union : la même arche retournée, un récipient qui contient tout."""
    _arc(t, (cx - r, cy - r, cx + r, cy + r), 0, 180, trait=trait)
    t.ligne([(cx - r, cy - r * 0.95), (cx - r, cy)], INK, trait)
    t.ligne([(cx + r, cy - r * 0.95), (cx + r, cy)], INK, trait)


def _vide(t, cx, cy, r, trait=7):
    """L-ensemble vide : un rond barré, et rien dedans."""
    t.disque((cx, cy), r, fill=WHITE_WARM, bord=INK, trait=trait)
    _barre(t, cx, cy, r * 1.05, INK, trait)


def signe(t, quoi, nom, lecture=None, cx=160, cy=140, r=44):
    """Un signe en grand, son nom dessous, et ce qu-on dit en le lisant."""
    t.rrect(26, 32, 294, 212, 16, fill=WHITE_WARM, bord=INK, trait=2.4)
    if quoi == 'appartient':
        _appartient(t, cx, cy, r)
    elif quoi == 'nappartient':
        _appartient(t, cx, cy, r)
        _barre(t, cx, cy, r * 1.15)
    elif quoi == 'inclus':
        _inclus(t, cx, cy, r)
    elif quoi == 'pasinclus':
        _inclus(t, cx, cy, r)
        _barre(t, cx, cy, r * 1.15)
    elif quoi == 'inter':
        _intersection(t, cx, cy, r)
    elif quoi == 'union':
        _union(t, cx, cy, r)
    elif quoi == 'vide':
        _vide(t, cx, cy, r)
    elif quoi == 'complement':
        t.texte((cx, cy), 'A’', 72, INK)
    elif quoi == 'nombre':
        t.texte((cx, cy), 'n(A)', 46, INK)
    else:
        raise AssertionError('signe inconnu : ' + quoi)
    t.texte((160, 240), nom, 19, INK)
    if lecture:
        t.texte((160, 272), lecture, 15, INK_2)


def deux_signes(t, a, b, nom_a, nom_b, titre=None):
    """Deux signes qui vont par paire : le signe et son contraire."""
    t.rrect(20, 44, 300, 206, 16, fill=WHITE_WARM, bord=INK, trait=2.4)
    for cx, quoi in ((90, a), (230, b)):
        if quoi == 'appartient':
            _appartient(t, cx, 112, 34, 6)
        elif quoi == 'nappartient':
            _appartient(t, cx, 112, 34, 6)
            _barre(t, cx, 112, 40)
        elif quoi == 'inclus':
            _inclus(t, cx, 112, 34, 6)
        elif quoi == 'pasinclus':
            _inclus(t, cx, 112, 34, 6)
            _barre(t, cx, 112, 40)
        elif quoi == 'inter':
            _intersection(t, cx, 112, 34, 6)
        elif quoi == 'union':
            _union(t, cx, 112, 34, 6)
        else:
            raise AssertionError('signe inconnu : ' + quoi)
    for cx, mot in ((90, nom_a), (230, nom_b)):
        # Le nom doit tenir dans sa moitié de carte : « is not an element
        # of » débordait du cadre blanc à la taille commune.
        taille = 15
        while _mesure(t, mot, taille) > 132 and taille > 9:
            taille -= 1
        t.texte((cx, 180), mot, taille, INK)
    if titre:
        t.texte((160, 248), titre, 17, INK)


# --------------------------------------------------------------------------
# Les accolades : l-ensemble écrit comme au cahier

def accolades(t, nom, elements, legende=None, haut=104, taille=26):
    """« A = { 2, 4, 6, 8 } », accolades et virgules comprises."""
    texte = '%s = { %s }' % (nom, ', '.join(elements))
    while _mesure(t, texte, taille) > 250 and taille > 13:
        taille -= 1
    t.rrect(18, haut - 36, 302, haut + 36, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.texte((160, haut), texte, taille, INK)
    if legende:
        t.texte((160, haut + 76), legende, 16, INK_2)


def fiche(t, titre, lignes, haut=92, vif=()):
    """Une liste posée ligne à ligne, comme au cahier."""
    t.texte((160, haut - 28), titre, 17, INK)
    for i, ligne in enumerate(lignes):
        y = haut + i * 44
        chaud = i in vif
        t.rrect(22, y, 298, y + 36, 9,
                fill=(GOLD if chaud else WHITE_WARM), bord=INK, trait=1.8)
        taille = 15
        while _mesure(t, ligne, taille) > 252 and taille > 10:
            taille -= 1
        t.texte((160, y + 18), ligne, taille, INK)


# --------------------------------------------------------------------------
# Le Venn, repris des figures de l-unité 3

def venn(t, teintes, legende=None, lettres=True):
    """Deux ovales dans le rectangle, la région demandée teintée."""
    fv._cadre(t, 18, 48, 302, 208, taille=18)
    a, b = fv._deux(160, 128, 46, 76, 54)
    noms = [((114, 72), 'A'), ((206, 72), 'B')] if lettres else []
    fv._poser(t, (a, b), teintes, noms, trait=2.6, taille=17)
    if legende:
        t.texte((160, 248), legende, 16, INK)


def complement(t):
    """Le complement : tout U sauf les ovales.

    La teinte est posée SOUS le trait du rectangle, pas dessus : peinte
    jusqu-au bord du cadre, elle recouvrait le trait et le U du coin, et la
    figure ne montrait plus l-ensemble universel dont elle parle.
    """
    venn(t, [(lambda ms: fv._sauf(fv._rect_masque(t, 21, 51, 299, 205, 8),
                                  fv._ou(ms[0], ms[1])), SKY)],
         'Hors des ovales, mais dans U.')
    t.rrect(18, 48, 302, 208, 10, bord=INK, trait=3)
    t.texte((36, 64), 'U', 18, INK_2)


def _inter(ms):
    return fv._et(ms[0], ms[1])


def _union_m(ms):
    return fv._ou(ms[0], ms[1])


def _a_seul(ms):
    return fv._sauf(ms[0], ms[1])


# --------------------------------------------------------------------------
# Les couvertures

def _bandeau(t, titre, sous=None):
    w = _mesure(t, titre, 26) + 56
    t.rrect(480 - w / 2, 192, 480 + w / 2, 232, 20, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 212), titre, 26, INK)
    if sous:
        t.texte((480, 338), sous, 17, INK)


def couv_ensemble(t):
    _bandeau(t, 'What a set is')
    t.rrect(300, 258, 660, 326, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.texte((480, 292), 'A = { 2, 4, 6, 8 }', 28, INK)


def couv_types(t):
    _bandeau(t, 'The types of sets')
    mots = ('unit', 'finite', 'infinite', 'empty', 'universal')
    larg = 160
    for i, m in enumerate(mots):
        x = 480 - larg * 2.5 + larg * i
        t.rrect(x + 6, 262, x + larg - 6, 326, 10, fill=WHITE_WARM, bord=INK, trait=2)
        t.texte((x + larg / 2, 294), m, 19, INK)


def couv_signes(t):
    _bandeau(t, 'The signs of sets')
    for i, quoi in enumerate(('appartient', 'inclus', 'inter', 'union')):
        cx = 330 + i * 100
        if quoi == 'appartient':
            _appartient(t, cx, 294, 28, 6)
        elif quoi == 'inclus':
            _inclus(t, cx, 294, 28, 6)
        elif quoi == 'inter':
            _intersection(t, cx, 294, 28, 6)
        else:
            _union(t, cx, 294, 28, 6)


def couv_lister(t):
    _bandeau(t, 'Listing the elements')
    t.rrect(230, 258, 730, 326, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.texte((480, 292), '{ 2, 3, 5, 7, 11, 13, 17, 19 }', 26, INK)


def couv_compter(t):
    _bandeau(t, 'Counting with sets')
    t.rrect(250, 256, 710, 328, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.texte((292, 292), 'n(A', 26, INK, ancre='lm')
    _union(t, 360, 290, 15, 5)
    t.texte((392, 292), 'B) = n(A) + n(B) – n(A', 26, INK, ancre='lm')
    _intersection(t, 638, 290, 15, 5)
    t.texte((668, 292), 'B)', 26, INK, ancre='lm')


# --------------------------------------------------------------------------
# Les vingt-sept figures

FIGURES = [
    # Leçon 1 — ce qu-est un ensemble
    ('bs-se-couv', 960, 540, couv_ensemble),
    ('bs-se-def', 320, 320,
     lambda t: accolades(t, 'A', ['2', '4', '6', '8'],
                         'Des choses qui se ressemblent, réunies.')),
    ('bs-se-elements', 320, 320,
     lambda t: fiche(t, 'Les éléments de A = { 2, 4, 6, 8 }',
                     ['2 est un élément de A', '4 est un élément de A',
                      '6 est un élément de A', '8 est un élément de A'])),
    ('bs-se-accolades', 320, 320,
     lambda t: accolades(t, 'B', ['Monday', 'Tuesday', 'Sunday'],
                         'Les accolades ouvrent et ferment l’ensemble.')),
    ('bs-se-nombre', 320, 320, lambda t: signe(t, 'nombre', 'n(A) = 4',
                                               'le nombre d’éléments de A')),

    # Leçon 2 — les types d-ensembles
    ('bs-ty-couv', 960, 540, couv_types),
    ('bs-ty-unite', 320, 320,
     lambda t: accolades(t, 'A', ['7'], 'Un seul élément : un singleton.')),
    ('bs-ty-fini', 320, 320,
     lambda t: accolades(t, 'B', ['1', '2', '3', '4'],
                         'On peut les compter : quatre. C’est fini.')),
    ('bs-ty-infini', 320, 320,
     lambda t: accolades(t, 'C', ['1', '2', '3', '…'],
                         'Les points disent que cela ne s’arrête pas.')),
    ('bs-ty-vide', 320, 320, lambda t: signe(t, 'vide', 'the empty set',
                                             'aucun élément, et { } s’écrit aussi')),
    ('bs-ty-universel', 320, 320,
     lambda t: venn(t, [], 'U, le rectangle, contient tout le reste.')),

    # Leçon 3 — les signes
    ('bs-si-couv', 960, 540, couv_signes),
    ('bs-si-appartient', 320, 320,
     lambda t: deux_signes(t, 'appartient', 'nappartient',
                           'is an element of', 'is not an element of',
                           'Le signe barré dit toujours « non ».')),
    ('bs-si-inclus', 320, 320,
     lambda t: deux_signes(t, 'inclus', 'pasinclus',
                           'is a subset of', 'is not a subset of',
                           'L’arc s’ouvre vers le grand ensemble.')),
    ('bs-si-inter', 320, 320,
     lambda t: deux_signes(t, 'inter', 'union',
                           'intersection', 'union',
                           'L’arche garde ; le récipient rassemble.')),
    ('bs-si-complement', 320, 320,
     lambda t: signe(t, 'complement', 'the complement of A',
                     'tout ce qui, dans U, n’est pas dans A')),

    # Leçon 4 — lister les éléments
    ('bs-li-couv', 960, 540, couv_lister),
    ('bs-li-pairs', 320, 320,
     lambda t: accolades(t, 'E', ['2', '4', '6', '8', '10'],
                         'Even numbers less than 12.')),
    ('bs-li-premiers', 320, 320,
     lambda t: accolades(t, 'P', ['2', '3', '5', '7', '11', '13', '17', '19'],
                         'Prime numbers less than 20.')),
    ('bs-li-facteurs', 320, 320,
     lambda t: fiche(t, 'Factors of 18', ['1 × 18 = 18', '2 × 9 = 18', '3 × 6 = 18',
                                          '{ 1, 2, 3, 6, 9, 18 }'], vif=(3,))),
    ('bs-li-multiples', 320, 320,
     lambda t: fiche(t, 'Multiples of 5 up to 30', ['5 × 1 = 5      5 × 2 = 10',
                                                    '5 × 3 = 15    5 × 4 = 20',
                                                    '5 × 5 = 25    5 × 6 = 30',
                                                    '{ 5, 10, 15, 20, 25, 30 }'], vif=(3,))),

    # Leçon 5 — compter avec les ensembles
    ('bs-co-couv', 960, 540, couv_compter),
    ('bs-co-union', 320, 320,
     lambda t: venn(t, [(_union_m, SKY), (_inter, GOLD)],
                    'Le milieu doré serait compté deux fois.')),
    ('bs-co-complement', 320, 320, lambda t: complement(t)),
    ('bs-co-aumoins', 320, 320,
     lambda t: venn(t, [(_union_m, MINT)],
                    'At least one : tout l’intérieur des ovales.')),
    ('bs-co-aucun', 320, 320,
     lambda t: fiche(t, 'None', ['n(U) = 30', 'dans les ovales : 22',
                                 '30 – 22 = 8', '8 ne sont dans aucun'], vif=(3,))),
    ('bs-co-etapes', 320, 320,
     lambda t: fiche(t, 'Remplir un diagramme', ['1. le milieu d’abord',
                                                 '2. les parts à deux',
                                                 '3. les parts toutes seules',
                                                 '4. vérifier le total'])),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # Aucun signe d-ensemble écrit comme du texte : la police ne les a pas,
    # et ils sortiraient en carrés vides. C-est le défaut que ce fichier
    # existe pour éviter, donc il se vérifie et ne se surveille pas.
    source = io_lire(__file__)
    for interdit in [chr(c) for c in (0x2208, 0x2209, 0x2229, 0x222a,
                                       0x2282, 0x2284, 0x2205)]:
        assert interdit not in source, 'signe non dessinable écrit en toutes lettres'

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
            assert fv._hors_bande(t.fini()) == 0, 'couverture %s : dessin hors de la fiche' % cle
            dehors = 0
            for y in list(range(0, BANDEAU[0])) + list(range(BANDEAU[1], h)):
                f2 = im.getpixel((3, y))
                for x in range(0, w, 4):
                    if sum(abs(a - b) for a, b in zip(im.getpixel((x, y)), f2)) > 60:
                        dehors += 1
            assert dehors == 0, 'couverture %s : %d pixels hors du bandeau' % (cle, dehors)


def io_lire(chemin):
    import io
    return io.open(chemin, encoding='utf-8').read()


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
