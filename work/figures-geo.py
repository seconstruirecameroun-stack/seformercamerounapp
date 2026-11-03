# -*- coding: utf-8 -*-
"""
Les 15 figures des zones agricoles du Cameroun, pour BRAYNE (CM1).

Rien n-est généré : tout est tracé. La Toile, la palette et la police
viennent de figures-maths.py ; le contour du pays vient de
carte-cameroun.py ; le contrôle de bande vient de figures-venn.py. Trois
emprunts, aucune copie.

Le parti pris de la leçon tient en une phrase : **la même carte, à chaque
notion**. « Quelle culture, quelle région » ne s-apprend pas dans une
liste, il s-apprend sur le pays. Huit des quinze figures sont donc la carte
du Cameroun avec UNE zone allumée et le reste en retrait, plus la culture
dont parle la notion posée à côté. À force de revoir la même silhouette,
l-enfant finit par la connaître — ce qu-une liste de noms de régions ne
donnera jamais.

Les zones ne sont pas les limites administratives, et ne prétendent pas
l-être : ce sont les grandes aires dont parle le cahier, découpées en
rectangles de longitude et de latitude puis rognées au contour du pays. On
montre où pousse quoi, on n-enseigne pas la frontière des dix régions.
"""

import importlib.util
import math
import os

from PIL import Image, ImageChops, ImageDraw

_ICI = os.path.dirname(os.path.abspath(__file__))


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fm = _charger('figures_maths', 'figures-maths.py')
cc = _charger('carte_cameroun', 'carte-cameroun.py')
fv = _charger('figures_venn', 'figures-venn.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

VERT = (122, 164, 108)
VERT_PALE = (206, 221, 199)
TERRE = (168, 122, 86)
ROUGE = (183, 66, 52)

# Les aires de la leçon : un centre et deux rayons, en degrés. Des ELLIPSES
# et non des rectangles — rognée au contour du pays, une ellipse donne une
# tache qui ressemble à une région, là où un rectangle laissait un carré
# posé au milieu de la carte, avec deux angles droits en plein territoire.
# Elles ne suivent pas les limites administratives et ne le prétendent pas.
ZONES = {
    'nord': (14.10, 9.90, 3.30, 3.70),
    'ouest': (9.95, 5.95, 1.50, 1.35),
    'centre': (12.25, 4.60, 1.25, 1.05),
    'sud': (11.70, 2.60, 2.45, 0.92),
    'littoral': (9.80, 3.95, 0.95, 0.80),
    'est': (15.00, 4.40, 1.55, 2.30),
}


def _masque(t):
    return Image.new('L', t.im.size, 0)


def _masque_pays(t, boite):
    m = _masque(t)
    ImageDraw.Draw(m).polygon(
        [(x * S, y * S) for x, y in cc.contour(boite)], fill=255)
    return m


def _masque_zone(t, boite, zone):
    lon, lat, rlon, rlat = ZONES[zone]
    f = cc.projeter(boite)
    x0, y0 = f(lon - rlon, lat + rlat)
    x1, y1 = f(lon + rlon, lat - rlat)
    m = _masque(t)
    ImageDraw.Draw(m).ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=255)
    return ImageChops.darker(m, _masque_pays(t, boite))


def _teinter(t, masque, couleur):
    t.im.paste(Image.new('RGB', t.im.size, couleur), (0, 0), masque)


def carte(t, boite, allumees=(), villes=(), trait=2.5, etiquette=None, taille=17,
          tout=False):
    """Le pays, une ou plusieurs zones allumées, le reste en retrait.

    `tout` allume le pays entier : sur une couverture, la réunion de cinq
    ellipses laissait entre elles des creux pâles qui se lisaient comme des
    trous dans le territoire. Une couverture annonce la leçon, elle ne
    désigne pas une région.
    """
    pays = _masque_pays(t, boite)
    _teinter(t, pays, VERT if tout else VERT_PALE)
    if not tout:
        for zone in allumees:
            _teinter(t, _masque_zone(t, boite, zone), VERT)
    t.ligne(cc.contour(boite) + [cc.contour(boite)[0]], INK, trait)
    f = cc.projeter(boite)
    milieu = (boite[0] + boite[2]) / 2
    for nom in villes:
        x, y = f(*cc.VILLES[nom])
        t.disque((x, y), 4.5, fill=CLAY, bord=WHITE_WARM, trait=1.4)
        # Le nom se pose du côté où il reste de la place. À droite du point
        # systématiquement, « Bertoua » sortait du cadre et « Maroua »
        # traversait la frontière.
        if x > milieu:
            t.texte((x - 8, y), nom, 13, INK, ancre='rm')
        else:
            t.texte((x + 8, y), nom, 13, INK, ancre='lm')
    if etiquette:
        t.texte(((boite[0] + boite[2]) / 2, boite[3] + 16), etiquette, taille, INK)
    return f


# ───────────────────────────── les cultures ──────────────────────────────

def _epi(t, cx, cy, h=56, couleur=GOLD):
    """Un épi : une tige, et des grains en quinconce de part et d-autre."""
    t.ligne([(cx, cy + h / 2), (cx, cy - h / 2)], VERT, 3)
    for i in range(6):
        y = cy - h / 2 + 6 + i * (h - 12) / 5
        for s in (-1, 1):
            t.disque((cx + s * 6, y), 5, fill=couleur, bord=INK, trait=1.2)


def _arachide(t, cx, cy, l=40):
    for s in (-1, 1):
        t.disque((cx + s * l * 0.22, cy), l * 0.26, fill=SAND, bord=TERRE, trait=2)
    t.rrect(cx - l * 0.18, cy - l * 0.14, cx + l * 0.18, cy + l * 0.14, l * 0.12,
            fill=SAND, bord=None)


def _tubercule(t, cx, cy, l=52, h=26, couleur=TERRE, taches=True):
    t.rrect(cx - l / 2, cy - h / 2, cx + l / 2, cy + h / 2, h / 2, fill=couleur, bord=INK, trait=2)
    if taches:
        for dx, dy in ((-l * 0.2, -3), (0, 4), (l * 0.2, -2)):
            t.disque((cx + dx, cy + dy), 2.6, fill=INK_2)


def _igname(t, cx, cy, l=64):
    t.rrect(cx - l / 2, cy - 11, cx + l / 2, cy + 11, 10, fill=TERRE, bord=INK, trait=2)
    t.poly([(cx + l / 2, cy - 8), (cx + l / 2 + 12, cy), (cx + l / 2, cy + 8)],
           fill=TERRE, bord=INK, trait=2)


def _cabosse(t, cx, cy, h=56):
    t.disque((cx, cy), h * 0.42, fill=(196, 118, 58), bord=INK, trait=2)
    t.rrect(cx - h * 0.30, cy - h * 0.46, cx + h * 0.30, cy + h * 0.46, h * 0.30,
            fill=(196, 118, 58), bord=INK, trait=2)
    for dx in (-h * 0.15, 0, h * 0.15):
        t.ligne([(cx + dx, cy - h * 0.36), (cx + dx, cy + h * 0.36)], (140, 78, 36), 2)


def _grain_cafe(t, cx, cy, r=11):
    t.disque((cx, cy), r, fill=(126, 78, 48), bord=INK, trait=1.6)
    t.ligne([(cx, cy - r * 0.7), (cx, cy + r * 0.7)], SAND, 2)


def _feuille(t, cx, cy, l=44, h=26, couleur=VERT, nervure=True):
    """Une feuille : deux arcs qui se rejoignent en pointe, pas un losange.

    Le losange servait au thé ET au tabac et ne ressemblait à aucun des
    deux. Une feuille se reconnaît à sa pointe et à son ventre rond ; c-est
    cela qu-il faut dessiner si l-enfant doit la reconnaître.
    """
    pts = []
    for s in (1, -1):
        for i in range(13):
            k = i / 12
            x = cx - l / 2 + l * k
            pts.append((x, cy - s * (h / 2) * math.sin(math.pi * k) ** 0.75))
    t.poly(pts, fill=couleur, bord=INK, trait=2)
    if nervure:
        t.ligne([(cx - l / 2, cy), (cx + l / 2, cy)], INK_2, 1.6)
        for i in range(1, 4):
            x = cx - l / 2 + l * i / 4
            d = (h / 2) * math.sin(math.pi * i / 4) ** 0.75 * 0.62
            t.ligne([(x, cy), (x + l * 0.10, cy - d)], INK_2, 1.1)
            t.ligne([(x, cy), (x + l * 0.10, cy + d)], INK_2, 1.1)


def _coton(t, cx, cy, r=13):
    for dx, dy in ((0, -r * 0.8), (-r * 0.85, r * 0.35), (r * 0.85, r * 0.35)):
        t.disque((cx + dx, cy + dy), r * 0.72, fill=WHITE_WARM, bord=INK, trait=1.8)
    t.disque((cx, cy), r * 0.5, fill=WHITE_WARM, bord=None)
    for a in (210, 270, 330, 30, 90, 150):
        x = cx + math.cos(math.radians(a)) * r * 1.35
        y = cy + math.sin(math.radians(a)) * r * 1.35
        t.poly([(cx, cy), (x, y), (cx + math.cos(math.radians(a + 26)) * r * 1.1,
                                   cy + math.sin(math.radians(a + 26)) * r * 1.1)],
               fill=(120, 96, 64), bord=None)


def _canne(t, cx, cy, h=66):
    for i, dx in enumerate((-13, 0, 13)):
        haut = h - abs(dx) * 0.5
        t.rrect(cx + dx - 5, cy - haut / 2, cx + dx + 5, cy + haut / 2, 4,
                fill=(150, 176, 104), bord=INK, trait=1.8)
        for k in range(1, 4):
            y = cy - haut / 2 + k * haut / 4
            t.ligne([(cx + dx - 5, y), (cx + dx + 5, y)], INK_2, 1.4)
        del i


def _palmier(t, cx, cy, h=74):
    """Tronc épais, palmes larges et retombantes, régime de fruits dessous.

    La première version n-avait que des traits fins en éventail : elle se
    lisait comme un balai. Une palme n-est pas un trait, c-est une feuille
    large qui retombe.
    """
    sommet = cy - h * 0.12
    t.rrect(cx - h * 0.075, sommet, cx + h * 0.075, cy + h * 0.52, h * 0.05,
            fill=TERRE, bord=INK, trait=2)
    for k in range(3):
        y = sommet + h * 0.18 + k * h * 0.14
        t.ligne([(cx - h * 0.075, y), (cx + h * 0.075, y)], (138, 96, 66), 1.8)
    for a in (196, 222, 248, 292, 318, 344):
        r = math.radians(a)
        bout = (cx + math.cos(r) * h * 0.50, sommet + math.sin(r) * h * 0.34)
        ecart = math.radians(a + (13 if math.cos(r) > 0 else -13))
        creux = (cx + math.cos(ecart) * h * 0.34, sommet + math.sin(ecart) * h * 0.20 + h * 0.10)
        t.poly([(cx, sommet), bout, creux], fill=VERT, bord=INK, trait=1.6)
    t.disque((cx, sommet + h * 0.13), h * 0.11, fill=ROUGE, bord=INK, trait=1.6)


def _houe(t, cx, cy, h=70):
    t.ligne([(cx - h * 0.26, cy - h * 0.42), (cx + h * 0.10, cy + h * 0.30)], TERRE, 6)
    t.poly([(cx + h * 0.02, cy + h * 0.22), (cx + h * 0.30, cy + h * 0.14),
            (cx + h * 0.26, cy + h * 0.46), (cx - h * 0.02, cy + h * 0.40)],
           fill=(150, 156, 160), bord=INK, trait=2)


def _usine(t, cx, cy, l=74):
    t.rrect(cx - l / 2, cy - 8, cx + l / 2, cy + 26, 5, fill=SAND, bord=INK, trait=2)
    for dx in (-l * 0.26, 0, l * 0.26):
        t.rrect(cx + dx - 7, cy - 1, cx + dx + 7, cy + 13, 2, fill=WHITE_WARM, bord=INK, trait=1.4)
    t.rrect(cx + l * 0.18, cy - 34, cx + l * 0.34, cy - 6, 3, fill=(160, 150, 146), bord=INK, trait=2)
    for i, (dx, r) in enumerate(((-2, 7), (8, 9), (19, 6))):
        t.disque((cx + l * 0.26 + dx, cy - 44 - i * 3), r, fill=(226, 224, 220))


def _navire(t, cx, cy, l=92):
    t.poly([(cx - l / 2, cy), (cx + l / 2, cy), (cx + l * 0.36, cy + 22), (cx - l * 0.36, cy + 22)],
           fill=(92, 112, 124), bord=INK, trait=2)
    for i, (dx, couleur) in enumerate(((-0.26, CLAY), (-0.05, GOLD), (0.16, SKY))):
        t.rrect(cx + l * dx - 11, cy - 20, cx + l * dx + 11, cy - 2, 2,
                fill=couleur, bord=INK, trait=1.6)
        del i
    t.ligne([(cx - l * 0.58, cy + 26), (cx + l * 0.58, cy + 26)], SKY, 3)


def _case(t, cx, cy, l=62):
    t.rrect(cx - l * 0.36, cy - 4, cx + l * 0.36, cy + 28, 4, fill=SAND, bord=INK, trait=2)
    t.poly([(cx - l * 0.46, cy - 2), (cx, cy - l * 0.42), (cx + l * 0.46, cy - 2)],
           fill=TERRE, bord=INK, trait=2)
    t.rrect(cx - 7, cy + 10, cx + 7, cy + 28, 2, fill=TERRE, bord=INK, trait=1.5)


def _fleche(t, a, b, couleur=INK, trait=4):
    t.ligne([a, b], couleur, trait)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (1, -1):
        t.ligne([b, (b[0] - math.cos(ang + s * 0.5) * 13,
                     b[1] - math.sin(ang + s * 0.5) * 13)], couleur, trait)


# ──────────────────────────────── les figures ─────────────────────────────

CARTE_OBJET = (6, 16, 196, 292)
ICONE_X = 256


def _carte_et_icone(t, zones, villes, dessin, legende):
    carte(t, CARTE_OBJET, zones, villes)
    dessin(t, ICONE_X, 150)
    t.texte((160, 308), legende, 17, INK)


def ag_vivrieres_couv(t):  # couverture 960x540
    carte(t, (70, 112, 330, 428), (),
          ('Maroua', 'Garoua', 'Ngaoundéré', 'Yaoundé'), trait=3.5, tout=True)
    _epi(t, 470, 200, 86)
    _arachide(t, 470, 300, 64)
    _igname(t, 600, 200, 86)
    _tubercule(t, 600, 300, 76, 36)
    t.texte((560, 390), 'cultures vivrières', 34, INK)


def ag_agriculture(t):
    t.rrect(28, 170, 292, 262, 12, fill=TERRE, bord=INK, trait=2)
    for i in range(4):
        y = 186 + i * 22
        t.ligne([(40, y), (280, y)], (138, 96, 66), 3)
    _houe(t, 160, 120, 96)
    t.texte((160, 296), 'cultiver la terre', 19, INK)


def ag_vivrieres(t):
    t.disque((160, 170), 76, fill=WHITE_WARM, bord=INK, trait=3)
    t.disque((160, 170), 58, fill=SAND, bord=INK_2, trait=1.6)
    _tubercule(t, 136, 156, 54, 26)
    _epi(t, 196, 168, 56)
    _arachide(t, 150, 200, 46)
    t.texte((160, 282), 'on les mange ici', 19, INK)


def ag_nord(t):
    carte(t, CARTE_OBJET, ('nord',), ('Maroua', 'Garoua', 'Ngaoundéré'))
    _epi(t, ICONE_X, 110, 58)
    _arachide(t, ICONE_X, 182, 50)
    t.texte((160, 308), 'mil · maïs · sorgho · arachides', 15, INK)


def ag_ouest(t):
    carte(t, CARTE_OBJET, ('ouest',), ('Bamenda',))
    _tubercule(t, ICONE_X, 120, 60, 30)
    _igname(t, ICONE_X, 186, 66)
    t.texte((160, 308), 'pommes de terre · ignames', 16, INK)


def ag_centre(t):
    # Douala et Yaoundé sont trop proches à cette échelle : leurs deux noms
    # se recouvraient. Yaoundé suffit à situer le Centre.
    carte(t, CARTE_OBJET, ('centre', 'sud', 'littoral'), ('Yaoundé',))
    _tubercule(t, ICONE_X, 116, 68, 24, TERRE)
    _tubercule(t, ICONE_X, 164, 52, 30, (178, 140, 96))
    _tubercule(t, ICONE_X, 212, 56, 26, (196, 136, 96))
    t.texte((160, 308), 'manioc · macabo · patate', 16, INK)


def ag_legumes(t):
    for x, h in ((56, 92), (108, 130), (160, 108), (212, 146), (264, 96)):
        t.rrect(x - 22, 160 - h, x + 22, 160, 4, fill=SAND, bord=INK, trait=2)
        for k in range(max(1, h // 34)):
            t.rrect(x - 12, 160 - h + 14 + k * 30, x + 12, 160 - h + 30 + k * 30, 2,
                    fill=WHITE_WARM, bord=INK_2, trait=1.2)
    t.rrect(16, 166, 304, 266, 10, fill=(150, 178, 126), bord=INK, trait=2)
    for i in range(3):
        y = 190 + i * 32
        t.ligne([(32, y), (288, y)], VERT, 4)
        for k in range(6):
            _feuille(t, 46 + k * 48, y, 30, 18, (176, 206, 150), False)
    t.texte((160, 294), 'les légumes frais, près des villes', 15, INK)


def ag_rente_couv(t):  # couverture 960x540
    carte(t, (60, 112, 320, 428), (), ('Bamenda', 'Bertoua', 'Ebolowa'), trait=3.5, tout=True)
    _cabosse(t, 450, 180, 76)
    _coton(t, 560, 180, 20)
    _canne(t, 670, 180, 80)
    _palmier(t, 470, 320, 90)
    _feuille(t, 600, 320, 72, 42, (142, 170, 92))
    t.texte((610, 400), 'cultures de rente', 32, INK)


def ag_rente(t):
    _usine(t, 108, 150, 88)
    _navire(t, 222, 206, 96)
    _fleche(t, (46, 96), (272, 96), CLAY, 4)
    t.texte((160, 72), 'vers l’étranger', 18, CLAY)
    t.texte((160, 290), 'transformées ou vendues', 17, INK)


def ag_cacao(t):
    carte(t, CARTE_OBJET, ('ouest',), ('Bamenda',))
    _cabosse(t, ICONE_X, 104, 54)
    _grain_cafe(t, ICONE_X - 14, 170, 11)
    _grain_cafe(t, ICONE_X + 12, 182, 11)
    _feuille(t, ICONE_X, 232, 48, 28)
    t.texte((160, 308), 'cacao · café · thé', 17, INK)


def ag_coton(t):
    carte(t, CARTE_OBJET, ('nord',), ('Maroua', 'Garoua'))
    _coton(t, ICONE_X, 150, 22)
    t.texte((160, 308), 'le coton, au Nord', 17, INK)


def ag_canne(t):
    carte(t, CARTE_OBJET, ('centre',), ('Yaoundé',))
    _canne(t, ICONE_X, 150, 92)
    t.texte((160, 308), 'la canne à sucre, au Centre', 16, INK)


def ag_palmier(t):
    carte(t, CARTE_OBJET, ('sud',), ('Ebolowa',))
    _palmier(t, ICONE_X, 140, 104)
    t.texte((160, 308), 'le palmier à huile, au Sud', 16, INK)


def ag_tabac(t):
    carte(t, CARTE_OBJET, ('est',), ('Bertoua',))
    _feuille(t, ICONE_X, 120, 60, 40, (150, 176, 100))
    _feuille(t, ICONE_X, 182, 54, 34, (166, 190, 118))
    t.texte((160, 308), 'le tabac, à l’Est', 17, INK)


def ag_difference(t):
    t.rrect(104, 132, 216, 196, 10, fill=TERRE, bord=INK, trait=2)
    for i in range(2):
        t.ligne([(116, 152 + i * 22), (204, 152 + i * 22)], (138, 96, 66), 3)
    t.texte((160, 118), 'le champ', 16, INK)
    _fleche(t, (104, 164), (58, 232), VERT, 4)
    _fleche(t, (216, 164), (262, 232), CLAY, 4)
    _case(t, 54, 250, 66)
    _navire(t, 258, 252, 76)
    t.texte((54, 300), 'ici', 17, VERT)
    t.texte((258, 300), 'ailleurs', 17, CLAY)


FIGURES = [
    ('ag-vivrieres-couv', 960, 540, ag_vivrieres_couv),
    ('ag-agriculture', 320, 320, ag_agriculture),
    ('ag-vivrieres', 320, 320, ag_vivrieres),
    ('ag-nord', 320, 320, ag_nord),
    ('ag-ouest', 320, 320, ag_ouest),
    ('ag-centre', 320, 320, ag_centre),
    ('ag-legumes', 320, 320, ag_legumes),
    ('ag-rente-couv', 960, 540, ag_rente_couv),
    ('ag-rente', 320, 320, ag_rente),
    ('ag-cacao', 320, 320, ag_cacao),
    ('ag-coton', 320, 320, ag_coton),
    ('ag-canne', 320, 320, ag_canne),
    ('ag-palmier', 320, 320, ag_palmier),
    ('ag-tabac', 320, 320, ag_tabac),
    ('ag-difference', 320, 320, ag_difference),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # Chaque zone doit exister sur la carte : une zone vide laisserait la
    # notion sans rien d-allumé, et l-enfant ne verrait aucune différence
    # entre « le coton au Nord » et « le coton à l-Est ».
    t = Toile(320, 320)
    for zone in ZONES:
        m = _masque_zone(t, CARTE_OBJET, zone)
        assert m.getbbox() is not None, 'zone vide sur la carte : ' + zone

    # Et deux zones voisines ne doivent pas se confondre : si elles se
    # recouvraient largement, « au Nord » et « à l-Est » allumeraient à peu
    # près la même chose et la carte n-enseignerait plus rien.
    for a in ZONES:
        for b in ZONES:
            if a >= b:
                continue
            ma = _masque_zone(t, CARTE_OBJET, a)
            mb = _masque_zone(t, CARTE_OBJET, b)
            commun = ImageChops.darker(ma, mb)
            aire_a = sum(ma.point(lambda v: 1 if v else 0).getdata())
            aire_commune = sum(commun.point(lambda v: 1 if v else 0).getdata())
            assert aire_commune <= aire_a * 0.12, \
                'les zones %s et %s se recouvrent trop (%.0f%%)' % (a, b, 100 * aire_commune / aire_a)

    # Sur une couverture, rien d-important ne doit sortir de la bande que
    # l-application montre réellement.
    for cle, w, h, fabrique in FIGURES:
        if (w, h) != (960, 540):
            continue
        t = Toile(w, h)
        fabrique(t)
        fautifs = fv._hors_bande(t.fini())
        assert fautifs == 0, \
            'couverture %s : %d pixels de dessin hors de la bande visible' % (cle, fautifs)


if __name__ == '__main__':
    controler()
    os.makedirs(SORTIE, exist_ok=True)
    total = 0
    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        chemin = os.path.join(SORTIE, cle + '.webp')
        t.fini().save(chemin, 'WEBP', quality=72, method=6)
        poids = os.path.getsize(chemin)
        total += poids
        print('  %-20s %4dx%-4d %6.1f Ko' % (cle, w, h, poids / 1024))
    print('%d figures - %.1f Ko - 0 credit' % (len(FIGURES), total / 1024))
