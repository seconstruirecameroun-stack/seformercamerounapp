# -*- coding: utf-8 -*-
"""
Le contour du Cameroun, en coordonnées géographiques.

Il vit dans son propre fichier parce qu-il ne sert pas qu-une fois : la
leçon des zones agricoles en a besoin, celle des bassins l-aurait voulu, et
toutes celles qui suivront aussi. Une carte redessinée à chaque leçon
finirait par ne plus avoir la même forme d-une leçon à l-autre.

Les sommets sont des longitudes et des latitudes, pas des pixels. La
projection se fait au moment de dessiner, ce qui permet de poser une ville
ou une région par ses vraies coordonnées sans retoucher le tracé.

Le découpage en zones ne prétend pas suivre les limites administratives :
ce sont les grandes aires dont parle la leçon — le Nord, l-Ouest, le
Centre, le Sud, l-Est, le Littoral. Elles servent à montrer OÙ pousse quoi,
pas à apprendre les frontières des dix régions.
"""

# Longitudes et latitudes, dans le sens des aiguilles depuis la pointe nord.
CONTOUR = [
    (14.60, 13.08),   # la pointe du lac Tchad
    (14.90, 12.70),
    (15.03, 11.95),
    (15.30, 11.05),
    (15.55, 10.15),
    (15.10, 9.35),
    (15.25, 8.55),
    (15.55, 7.80),
    (15.00, 7.45),
    (14.55, 6.35),
    (15.00, 5.90),
    (15.55, 5.35),
    (16.19, 5.10),
    (16.05, 4.20),
    (15.40, 3.40),
    (16.10, 2.90),
    (16.00, 2.20),
    (14.50, 2.15),
    (13.30, 2.16),
    (13.25, 1.65),   # la pointe sud, vers Campo
    (11.35, 2.17),
    (9.90, 2.17),
    (9.82, 2.35),
    (9.92, 3.00),
    (9.65, 3.55),
    (9.45, 3.95),
    (9.70, 4.05),
    (8.95, 4.55),
    (8.50, 4.55),
    (8.85, 5.50),
    (9.00, 6.00),
    (9.80, 6.80),
    (10.60, 6.90),
    (11.10, 6.65),
    (11.55, 7.00),
    (12.05, 8.05),
    (12.80, 8.95),
    (13.20, 9.95),
    (13.95, 11.05),
    (14.25, 11.65),
    (14.00, 12.35),
    (14.60, 13.08),
]

# Les aires dont parle la leçon, par un point et un rayon approximatifs.
ZONES = {
    'nord': (14.3, 10.6),
    'ouest': (10.3, 5.6),
    'centre': (12.2, 4.6),
    'sud': (12.0, 2.8),
    'est': (14.5, 4.6),
    'littoral': (9.9, 4.1),
}

# Les villes que le cahier cite.
VILLES = {
    'Maroua': (14.32, 10.59),
    'Garoua': (13.40, 9.30),
    'Ngaoundéré': (13.58, 7.33),
    'Yaoundé': (11.52, 3.87),
    'Douala': (9.71, 4.05),
    'Bamenda': (10.15, 5.96),
    'Bertoua': (13.68, 4.58),
    'Ebolowa': (11.15, 2.92),
}

LON = (min(p[0] for p in CONTOUR), max(p[0] for p in CONTOUR))
LAT = (min(p[1] for p in CONTOUR), max(p[1] for p in CONTOUR))


def projeter(boite, marge=10):
    """Rend une fonction (lon, lat) → (x, y) qui remplit la boîte donnée.

    L-échelle est la MÊME en x et en y : à ces latitudes un degré de
    longitude et un degré de latitude font presque la même distance, et
    étirer l-un des deux déformerait le pays au point de le rendre
    méconnaissable.
    """
    x0, y0, x1, y1 = boite
    larg = (x1 - x0) - 2 * marge
    haut = (y1 - y0) - 2 * marge
    echelle = min(larg / (LON[1] - LON[0]), haut / (LAT[1] - LAT[0]))
    dx = x0 + marge + (larg - echelle * (LON[1] - LON[0])) / 2
    dy = y0 + marge + (haut - echelle * (LAT[1] - LAT[0])) / 2

    def f(lon, lat):
        return (dx + (lon - LON[0]) * echelle,
                dy + (LAT[1] - lat) * echelle)

    return f


def contour(boite, marge=10):
    f = projeter(boite, marge)
    return [f(lon, lat) for lon, lat in CONTOUR]
