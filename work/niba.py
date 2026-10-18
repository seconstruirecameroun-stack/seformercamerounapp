# -*- coding: utf-8 -*-
"""
Niba dessiné hors du navigateur, pour être posé sur les films.

L'application dessine Niba en SVG. Un film est un fichier vidéo : il n'y a
pas de SVG à l'intérieur, et le lecteur ne sait pas superposer un composant
React sur une image qui bouge. Il faut donc le même lionceau, en pixels.

La seule façon honnête de le faire est de reprendre le tracé, pas de le
redessiner à l'œil : chaque cercle, chaque arc et chaque moustache vient de
app/src/components/jeu/Mascotte.tsx, aux mêmes coordonnées, dans le même
repère de 120 sur 120. Un Niba approximatif sur les films et un Niba exact
dans l'app donneraient deux personnages à l'enfant.

Les courbes du SVG sont des béziers quadratiques. Elles sont échantillonnées
ici plutôt qu'approchées par des arcs de cercle, pour que la bouche garde sa
forme exacte.

Usage comme bibliothèque :  from niba import dessiner ; dessiner('content', 220)
Usage direct (planche de contrôle) :  python work/niba.py
"""

import math
from PIL import Image, ImageDraw

# Les jetons de couleur de app/src/index.css, convertis une fois.
INK = (43, 64, 71, 255)
INK_2 = (90, 112, 118, 255)
WHITE_WARM = (255, 251, 244, 255)
SAND = (246, 230, 201, 255)
CLAY = (201, 112, 63, 255)
CLAY_DARK = (162, 81, 42, 255)
GOLD = (231, 174, 74, 255)

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')

# On dessine en suréchantillonnant : Pillow ne lisse pas les bords, et un
# lionceau crénelé sur un plan pastel se verrait immédiatement.
ECHELLE = 4


def _bezier(p0, p1, p2, n=48):
    """Une bézier quadratique, échantillonnée. Les 'q' du SVG passent ici."""
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((
            u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1],
        ))
    return pts


def dessiner(humeur='content', taille=240):
    """Niba en RGBA, fond transparent, dans un carré de `taille` pixels."""
    assert humeur in HUMEURS, humeur
    e = ECHELLE
    img = Image.new('RGBA', (120 * e, 120 * e), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def cercle(cx, cy, r, couleur):
        d.ellipse([(cx - r) * e, (cy - r) * e, (cx + r) * e, (cy + r) * e], fill=couleur)

    def ellipse(cx, cy, rx, ry, couleur):
        d.ellipse([(cx - rx) * e, (cy - ry) * e, (cx + rx) * e, (cy + ry) * e], fill=couleur)

    def trait(points, couleur, epaisseur):
        d.line([(x * e, y * e) for x, y in points], fill=couleur,
               width=int(epaisseur * e), joint='curve')
        # Pillow ne met pas de bout rond : on le pose à la main, sinon les
        # moustaches et la bouche finissent carrées.
        r = epaisseur * e / 2
        for x, y in (points[0], points[-1]):
            d.ellipse([x * e - r, y * e - r, x * e + r, y * e + r], fill=couleur)

    # La crinière : neuf pétales arrondis, décalés pour ne pas faire roue.
    for i in range(9):
        a = (i / 9) * 2 * math.pi - math.pi / 2
        cercle(60 + math.cos(a) * 36, 62 + math.sin(a) * 36, 16,
               CLAY if i % 2 == 0 else GOLD)

    # Les oreilles, posées assez loin du centre pour dépasser de la face.
    for x in (28, 92):
        cercle(x, 33, 12, CLAY_DARK)
        cercle(x, 33, 6, SAND)

    cercle(60, 62, 34, SAND)

    yeux_fermes = humeur in ('dort', 'fete')
    if yeux_fermes:
        for x in (40, 66):
            if humeur == 'dort':
                courbe = _bezier((x, 58), (x + 7, 63), (x + 14, 58))
            else:
                courbe = _bezier((x, 60), (x + 7, 52), (x + 14, 60))
            trait(courbe, INK, 3.5)
    else:
        for x in (47, 73):
            cercle(x, 58, 5, INK)
            cercle(x + 1.8, 56.2, 1.8, WHITE_WARM)

    # Les sourcils ne servent qu'à l'inquiétude : ailleurs, ils durcissent le
    # visage sans rien ajouter.
    if humeur == 'manque':
        trait(_bezier((40, 47), (47, 43), (53, 46)), INK_2, 3)
        trait(_bezier((67, 46), (73, 43), (80, 47)), INK_2, 3)

    ellipse(60, 72, 13, 9, WHITE_WARM)

    # La truffe : deux béziers qui se referment, remplies.
    truffe = _bezier((55, 69), (60, 65), (65, 69)) + _bezier((65, 69), (60, 74), (55, 69))
    d.polygon([(x * e, y * e) for x, y in truffe], fill=CLAY_DARK)

    # La bouche porte l'humeur à elle seule.
    if humeur == 'manque':
        trait(_bezier((52, 83), (60, 78), (68, 83)), INK, 3)
    elif humeur == 'fete':
        ouverte = _bezier((50, 78), (60, 90), (70, 78)) + _bezier((70, 78), (60, 83), (50, 78))
        d.polygon([(x * e, y * e) for x, y in ouverte], fill=CLAY_DARK)
        trait(_bezier((50, 78), (60, 90), (70, 78)), INK, 3)
    elif humeur == 'dort':
        trait(_bezier((55, 80), (60, 83), (65, 80)), INK, 3)
    else:
        trait(_bezier((52, 78), (60, 85), (68, 78)), INK, 3)

    # Les moustaches : trois traits qui suffisent à dire « félin ».
    moustache = (*INK_2[:3], 140)  # opacité 0,55
    for depart, fin in (((34, 68), (44, 68)), ((34, 75), (44, 75)),
                        ((86, 68), (76, 68)), ((86, 75), (76, 75))):
        trait([depart, fin], moustache, 2)

    return img.resize((taille, taille), Image.LANCZOS)


if __name__ == '__main__':
    import os
    planche = Image.new('RGBA', (5 * 240, 240), (250, 246, 238, 255))
    for i, h in enumerate(HUMEURS):
        planche.alpha_composite(dessiner(h, 240), (i * 240, 0))
    chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'niba-humeurs.png')
    planche.convert('RGB').save(chemin)
    print(chemin)
