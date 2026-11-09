# -*- coding: utf-8 -*-
"""
Les trois schémas à annoter de la révision du 9 novembre 2026 — BRAYNE, CM1.

CE QUE CES FIGURES ONT DE PARTICULIER. Elles ne décorent pas une notion :
elles SONT la question. L-enfant lit le dessin, et c-est le dessin qui
porte les numéros. Trois conséquences tenues par le contrôle du bas :

  les numéros vont de 1 à n, sans trou ni doublon. Un numéro 4 qui
  manquerait laisserait une étiquette sans place

  chaque repère est posé SUR ce qu-il désigne, et jamais dans le vide.
  C-est la seule chose qu-un script ne peut pas vérifier tout seul : les
  positions sont donc calculées à partir des formes elles-mêmes - le
  repère du réservoir est au centre du réservoir, pas à des coordonnées
  recopiées à la main

  la pastille d-un numéro est claire et cerclée d-encre, pour rester
  lisible sur un aplat sombre comme sur un aplat clair

Les trois schémas sont ceux que le tableau demande d-annoter : la lampe à
pétrole, l-appareil reproducteur de la femme, et le cycle de l-eau.

Usage :  python work/figures-brayne-schemas-nov.py
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

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

VERT = (122, 164, 108)
TERRE = (168, 122, 86)
ROSE = (226, 176, 176)
GRIS = (196, 198, 196)
EAU = (126, 170, 206)


def _arc(t, boite, debut, fin, couleur=INK, trait=3):
    x0, y0, x1, y1 = boite
    t.d.arc([x0 * S, y0 * S, x1 * S, y1 * S], debut, fin,
            fill=couleur, width=max(1, int(trait * S)))


def repere(t, numero, xy, vers=None, rayon=13):
    """Le numéro, posé À CÔTÉ de ce qu-il désigne, avec son trait de rappel.

    Posé DESSUS, il cachait la chose même : le premier jet mettait le
    numéro de l-ovaire au centre de l-ovaire, qui disparaissait dessous, et
    les numéros de la lampe se recouvraient l-un l-autre. Le trait de rappel
    est tracé avant la pastille, pour qu-il passe sous elle et non dessus.
    """
    if vers is not None:
        t.ligne([xy, vers], INK_2, 1.8)
        t.disque(vers, 3.2, fill=INK_2)
    t.disque(xy, rayon, fill=WHITE_WARM, bord=INK, trait=2.2)
    t.texte(xy, str(numero), rayon + 4, INK)


def fleche(t, a, b, couleur=INK, trait=3, pointe=9):
    """Une flèche droite, sa pointe calculée depuis sa direction."""
    t.ligne([a, b], couleur, trait)
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    for cote in (-0.5, 0.5):
        t.ligne([b, (b[0] - pointe * math.cos(angle + cote),
                     b[1] - pointe * math.sin(angle + cote))], couleur, trait)


# --------------------------------------------------------------------------
# 1. La lampe à pétrole

LAMPE = ('la grille d’aération', 'le verre', 'la mèche', 'la molette', 'le réservoir')


def lampe(t):
    cx = 150
    # Le réservoir : un tronc de cône posé sur son pied.
    reservoir = [(cx - 46, 232), (cx + 46, 232), (cx + 38, 272), (cx - 38, 272)]
    t.poly(reservoir, fill=GOLD, bord=INK, trait=2.6)
    t.rrect(cx - 50, 272, cx + 50, 284, 5, fill=SAND, bord=INK, trait=2.4)

    # Le bec, qui tient la mèche, et la molette sur son flanc.
    t.rrect(cx - 22, 212, cx + 22, 234, 5, fill=SAND, bord=INK, trait=2.4)
    t.disque((cx + 34, 222), 11, fill=WHITE_WARM, bord=INK, trait=2.4)
    for a in range(0, 360, 45):
        t.ligne([(cx + 34 + 5 * math.cos(math.radians(a)),
                  222 + 5 * math.sin(math.radians(a))),
                 (cx + 34 + 10 * math.cos(math.radians(a)),
                  222 + 10 * math.sin(math.radians(a)))], INK, 1.4)

    # Le verre : la cheminée, renflée en bas et resserrée en haut.
    verre = [(cx - 20, 212), (cx - 34, 186), (cx - 30, 140), (cx - 20, 112),
             (cx + 20, 112), (cx + 30, 140), (cx + 34, 186), (cx + 20, 212)]
    t.poly(verre, fill=(214, 232, 240), bord=INK, trait=2.6)

    # La mèche et sa flamme, vues à travers le verre.
    t.rrect(cx - 5, 182, cx + 5, 214, 3, fill=(236, 226, 206), bord=INK, trait=1.8)
    t.poly([(cx, 150), (cx + 13, 184), (cx - 13, 184)], fill=GOLD, bord=CLAY, trait=2)

    # La grille d-aération, au sommet.
    t.rrect(cx - 30, 92, cx + 30, 112, 6, fill=GRIS, bord=INK, trait=2.4)
    for i in range(-2, 3):
        t.ligne([(cx + i * 11, 96), (cx + i * 11, 108)], INK, 1.6)

    # La poignée de transport, par-dessus.
    _arc(t, (cx - 44, 56, cx + 44, 120), 190, 350, INK, 3)

    repere(t, 1, (250, 92), (cx + 28, 100))
    repere(t, 2, (258, 152), (cx + 29, 152))
    repere(t, 3, (62, 196), (cx - 6, 198))
    repere(t, 4, (256, 222), (cx + 44, 222))
    repere(t, 5, (62, 254), (cx - 34, 252))


# --------------------------------------------------------------------------
# 2. L-appareil reproducteur de la femme

FEMME = ('la trompe', 'l’ovaire', 'l’utérus', 'le col de l’utérus', 'le vagin')


def appareil_femme(t):
    cx, haut = 160, 118
    # L-utérus : une poire, large en haut, qui se resserre vers le col.
    uterus = [(cx - 44, haut), (cx + 44, haut), (cx + 34, haut + 54),
              (cx + 13, haut + 84), (cx - 13, haut + 84), (cx - 34, haut + 54)]
    t.poly(uterus, fill=ROSE, bord=INK, trait=2.6)

    # Les deux trompes : un tube calculé point par point, qui part du coin
    # de l-utérus, bombe vers le haut, et finit sur l-ovaire. Les arcs de
    # cercle du premier jet ne touchaient ni l-un ni l-autre.
    for cote in (-1, 1):
        depart = (cx + cote * 42, haut + 2)
        arrivee = (cx + cote * 96, haut - 6)
        tube = []
        for k in range(25):
            u = k / 24
            tube.append((depart[0] + (arrivee[0] - depart[0]) * u,
                         depart[1] + (arrivee[1] - depart[1]) * u
                         - 30 * math.sin(math.pi * u)))
        t.ligne(tube, INK, 6)
        t.disque((cx + cote * 104, haut - 4), 14, fill=SAND, bord=INK, trait=2.4)

    # Le col, puis le vagin.
    t.rrect(cx - 13, haut + 82, cx + 13, haut + 104, 4, fill=(208, 156, 156),
            bord=INK, trait=2.4)
    t.poly([(cx - 17, haut + 104), (cx + 17, haut + 104), (cx + 21, haut + 150),
            (cx - 21, haut + 150)], fill=ROSE, bord=INK, trait=2.6)

    repere(t, 1, (cx + 70, haut - 58), (cx + 69, haut - 24))
    repere(t, 2, (cx - 104, haut - 44), (cx - 104, haut - 20))
    repere(t, 3, (cx + 92, haut + 34), (cx + 36, haut + 34))
    repere(t, 4, (cx - 76, haut + 92), (cx - 15, haut + 92))
    repere(t, 5, (cx + 88, haut + 128), (cx + 20, haut + 128))


# --------------------------------------------------------------------------
# 3. Le cycle de l-eau

CYCLE = ('l’évaporation', 'la condensation', 'le ruissellement', 'l’infiltration')


def cycle_eau(t):
    # Le sol, et la mer à gauche.
    t.poly([(14, 196), (120, 196), (190, 164), (306, 150), (306, 300), (14, 300)],
           fill=TERRE, bord=INK, trait=2.4)
    t.poly([(14, 196), (120, 196), (120, 250), (14, 250)], fill=EAU, bord=None)
    t.ligne([(14, 196), (120, 196)], INK, 2.4)
    t.ligne([(120, 196), (120, 250)], INK, 2)
    t.ligne([(14, 250), (120, 250)], INK, 2)

    # Le soleil, qui chauffe.
    t.disque((282, 60), 20, fill=GOLD, bord=INK, trait=2.4)
    for a in range(0, 360, 45):
        r = math.radians(a)
        t.ligne([(282 + 25 * math.cos(r), 60 + 25 * math.sin(r)),
                 (282 + 33 * math.cos(r), 60 + 33 * math.sin(r))], CLAY, 2.2)

    # Le nuage.
    for dx, dy, r in ((-26, 4, 20), (0, -8, 25), (26, 4, 20)):
        t.disque((112 + dx, 72 + dy), r, fill=WHITE_WARM, bord=None)
    t.rrect(82, 72, 142, 94, 11, fill=WHITE_WARM, bord=None)
    for dx, dy, r in ((-26, 4, 20), (0, -8, 25), (26, 4, 20)):
        t.d.arc([(112 + dx - r) * S, (72 + dy - r) * S,
                 (112 + dx + r) * S, (72 + dy + r) * S], 180, 360,
                fill=INK, width=int(2.4 * S))
    t.ligne([(86, 94), (138, 94)], INK, 2.4)

    # L-évaporation : l-eau qui monte.
    fleche(t, (54, 188), (54, 112), BLEU, 3)
    # La pluie.
    for x in (96, 112, 128):
        t.ligne([(x, 104), (x - 4, 126)], BLEU, 2.4)
    # Le ruissellement : l-eau qui descend la pente vers la mer.
    fleche(t, (212, 166), (134, 192), BLEU, 3)
    # L-infiltration : l-eau qui entre dans le sol.
    fleche(t, (238, 166), (238, 232), BLEU, 3)

    repere(t, 1, (28, 146), (52, 148))
    repere(t, 2, (56, 40), (92, 60))
    repere(t, 3, (186, 128), (174, 176))
    repere(t, 4, (288, 214), (242, 212))


FIGURES = [
    ('br-la-schema', 320, 320, lampe, LAMPE),
    ('br-or-schema', 320, 320, appareil_femme, FEMME),
    ('br-cy-schema', 320, 320, cycle_eau, CYCLE),
]


def controler():
    """Les numéros, les bords, et rien d-autre que le script puisse savoir."""
    cles = [c for c, _w, _h, _f, _n in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    for cle, w, h, fabrique, noms in FIGURES:
        # Les numéros vont de 1 à n : c-est le nombre d-étiquettes qui le dit,
        # et le dessin pose exactement ces numéros-là.
        assert len(noms) == len(set(noms)), 'deux étiquettes identiques : ' + cle
        assert 2 <= len(noms) <= 8, 'nombre de repères hors des bornes : ' + cle

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
    for cle, w, h, fabrique, _noms in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        chemin = os.path.join(SORTIE, cle + '.webp')
        t.fini().save(chemin, 'WEBP', quality=78, method=6)
        total += os.path.getsize(chemin)
    print('%d schémas - %.1f Ko - 0 credit' % (len(FIGURES), total / 1024))
    for cle, _w, _h, _f, noms in FIGURES:
        print('  %-14s %s' % (cle, ' / '.join('%d %s' % (i + 1, n) for i, n in enumerate(noms))))
