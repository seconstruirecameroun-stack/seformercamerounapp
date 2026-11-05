# -*- coding: utf-8 -*-
"""
Les figures des cinq leçons d-agriculture et de nature de KLEIN (CE1) —
cahier du 11 septembre au 27 octobre 2026.

Ici, contrairement aux leçons de grammaire, un tableau ne suffit pas.
« Spade » n-est pas une règle, c-est un objet : un enfant qui lit le mot
sans voir la bêche n-apprend qu-un son. Le module est donc d-abord une
boîte de PICTOGRAMMES, et les figures sont des compositions de ces
pictogrammes.

Chaque outil est dessiné à partir des deux mêmes morceaux :

  _manche   le bois, toujours de la même couleur et de la même épaisseur
  _fer      la partie métallique, toujours grise et cernée

Un outil se distingue donc d-un autre par sa FORME seule, jamais par sa
couleur — c-est ce qui permet de les mettre côte à côte dans une
question à images sans que la réponse se devine à la teinte.

  _vignette      un pictogramme dans une carte, son nom dessous
  _grille        quatre vignettes, deux par deux

Usage :  python work/figures-klein-agri-nov.py
"""

import importlib.util
import os

_ICI = os.path.dirname(os.path.abspath(__file__))


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fm = _charger('figures_maths', 'figures-maths.py')
fv = _charger('figures_venn', 'figures-venn.py')
fa = _charger('figures_anglais_oct', 'figures-anglais-oct.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

VERT, VERT_PALE, TERRE, ROUGE = fa.VERT, fa.VERT_PALE, fa.TERRE, fa.ROUGE
FER = (168, 176, 182)
BOIS = (176, 128, 80)

_mesure = fa._mesure
_pastille = fa._pastille
_taille_tenant = fa._taille_tenant
_liste = fa._liste
_bandeau_couv = fa._bandeau_couv
BANDEAU = fa.BANDEAU


# --------------------------------------------------------------------------
# Les deux morceaux dont tout outil est fait

def _manche(t, a, b, epaisseur=7):
    """Le bois. Un rectangle orienté, pour qu-un manche penché reste droit."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    longueur = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    nx, ny = -dy / longueur * epaisseur / 2, dx / longueur * epaisseur / 2
    t.poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)],
           fill=BOIS, bord=INK, trait=1.8)


def _fer(t, points):
    """La partie métallique. Toujours la même teinte, pour tous les outils."""
    t.poly(points, fill=FER, bord=INK, trait=1.8)


# --------------------------------------------------------------------------
# Les outils. Chacun tient dans un carré de 100 centré sur (cx, cy).

def houe(t, cx, cy):
    _manche(t, (cx + 26, cy - 40), (cx - 14, cy + 22))
    _fer(t, [(cx - 20, cy + 14), (cx + 2, cy + 28), (cx - 10, cy + 44), (cx - 34, cy + 30)])


def machette(t, cx, cy):
    _manche(t, (cx - 26, cy + 36), (cx - 12, cy + 10), 9)
    _fer(t, [(cx - 16, cy + 14), (cx - 4, cy + 4), (cx + 30, cy - 40),
             (cx + 18, cy - 44), (cx - 24, cy + 6)])


def beche(t, cx, cy):
    _manche(t, (cx, cy - 44), (cx, cy + 6))
    t.rrect(cx - 14, cy - 50, cx + 14, cy - 40, 4, fill=BOIS, bord=INK, trait=1.8)
    _fer(t, [(cx - 17, cy + 2), (cx + 17, cy + 2), (cx + 13, cy + 40), (cx - 13, cy + 40)])


def rateau(t, cx, cy):
    _manche(t, (cx + 18, cy - 44), (cx - 8, cy + 16))
    _fer(t, [(cx - 32, cy + 16), (cx + 14, cy + 16), (cx + 14, cy + 24), (cx - 32, cy + 24)])
    for k in range(5):
        x = cx - 28 + k * 10
        _fer(t, [(x - 2, cy + 24), (x + 2, cy + 24), (x + 2, cy + 40), (x - 2, cy + 40)])


def pioche(t, cx, cy):
    _manche(t, (cx, cy - 36), (cx, cy + 44))
    _fer(t, [(cx - 44, cy - 20), (cx - 8, cy - 34), (cx + 8, cy - 34), (cx + 44, cy - 20),
             (cx + 40, cy - 12), (cx + 6, cy - 24), (cx - 6, cy - 24), (cx - 40, cy - 12)])


def fourche(t, cx, cy):
    _manche(t, (cx, cy - 46), (cx, cy + 4))
    t.rrect(cx - 13, cy - 52, cx + 13, cy - 42, 4, fill=BOIS, bord=INK, trait=1.8)
    _fer(t, [(cx - 18, cy + 2), (cx + 18, cy + 2), (cx + 18, cy + 10), (cx - 18, cy + 10)])
    for k in range(4):
        x = cx - 14 + k * 9.5
        _fer(t, [(x - 2.5, cy + 10), (x + 2.5, cy + 10), (x + 2.5, cy + 42), (x, cy + 48),
                 (x - 2.5, cy + 42)])


def barre_a_mine(t, cx, cy):
    """Le crow bar : une barre droite, un bout aplati et recourbé."""
    _fer(t, [(cx - 5, cy - 44), (cx + 5, cy - 44), (cx + 5, cy + 30), (cx - 5, cy + 30)])
    _fer(t, [(cx - 5, cy + 26), (cx + 5, cy + 26), (cx + 22, cy + 42), (cx + 16, cy + 48)])


OUTILS = {'hoe': houe, 'cutlass': machette, 'spade': beche, 'rake': rateau,
          'pick axe': pioche, 'digging fork': fourche, 'crow bar': barre_a_mine}


# --------------------------------------------------------------------------
# Le reste du décor

def champ(t, cx, cy, w=120, h=46, sillons=True):
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 6,
            fill=TERRE, bord=INK, trait=2)
    if sillons:
        for k in range(3):
            y = cy - h / 2 + h * (k + 1) / 4
            t.ligne([(cx - w / 2 + 8, y), (cx + w / 2 - 8, y)], (138, 98, 68), 2.4)


def graine(t, cx, cy, l=26):
    t.d.ellipse([int((cx - l * 0.4) * S), int((cy - l * 0.6) * S),
                 int((cx + l * 0.4) * S), int((cy + l * 0.6) * S)],
                fill=TERRE, outline=INK, width=int(1.8 * S))


def pousse(t, cx, cy):
    t.ligne([(cx, cy + 22), (cx, cy - 10)], VERT, 3)
    for cote in (-1, 1):
        t.poly([(cx, cy - 2), (cx + cote * 20, cy - 16), (cx + cote * 4, cy - 20)],
               fill=VERT, bord=INK, trait=1.6)
    t.rrect(cx - 16, cy + 20, cx + 16, cy + 30, 4, fill=TERRE, bord=INK, trait=1.6)


def arrosoir(t, cx, cy):
    t.rrect(cx - 24, cy - 10, cx + 14, cy + 26, 6, fill=SKY, bord=INK, trait=2)
    t.poly([(cx + 14, cy - 2), (cx + 38, cy - 22), (cx + 44, cy - 16), (cx + 14, cy + 8)],
           fill=SKY, bord=INK, trait=2)
    t.d.arc([int((cx - 20) * S), int((cy - 30) * S), int((cx + 6) * S), int((cy - 2) * S)],
            190, 350, fill=INK, width=int(2.4 * S))
    for k in range(3):
        t.ligne([(cx + 40 + k * 4, cy - 10), (cx + 36 + k * 4, cy + 2)], BLEU, 2)


def tas(t, cx, cy, couleur=TERRE):
    """Un tas : fumier, compost, paillis. La forme dit le tas, pas la matière."""
    t.poly([(cx - 36, cy + 22), (cx - 14, cy - 18), (cx + 10, cy - 10),
            (cx + 34, cy + 22)], fill=couleur, bord=INK, trait=2)
    for dx in (-18, 0, 16):
        t.ligne([(cx + dx, cy + 14), (cx + dx + 6, cy + 4)], INK_2, 1.6)


def herbe(t, cx, cy, n=5, couleur=VERT):
    for k in range(n):
        x = cx - (n - 1) * 7 + k * 14
        t.ligne([(x, cy + 16), (x + (3 if k % 2 else -3), cy - 14)], couleur, 2.6)


def fleur(t, cx, cy):
    t.ligne([(cx, cy + 26), (cx, cy - 6)], VERT, 3)
    for k in range(6):
        import math
        a = math.pi * 2 * k / 6
        t.disque((cx + math.cos(a) * 13, cy - 6 + math.sin(a) * 13), 8,
                 fill=GOLD, bord=INK, trait=1.6)
    t.disque((cx, cy - 6), 7, fill=CLAY, bord=INK, trait=1.6)
    for cote in (-1, 1):
        t.poly([(cx, cy + 12), (cx + cote * 16, cy + 4), (cx + cote * 4, cy + 18)],
               fill=VERT, bord=INK, trait=1.5)


def cage(t, cx, cy, w=120, h=96):
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, 8,
            fill=WHITE_WARM, bord=INK, trait=2.4)
    for k in range(1, 7):
        x = cx - w / 2 + w * k / 7
        t.ligne([(x, cy - h / 2 + 4), (x, cy + h / 2 - 4)], INK_2, 2)


def bete(t, cx, cy, l=56):
    fa._bete(t, cx, cy, l)


def personne(t, cx, cy):
    t.disque((cx, cy - 26), 11, fill=SAND, bord=INK, trait=2)
    t.poly([(cx - 13, cy + 16), (cx - 9, cy - 12), (cx + 9, cy - 12), (cx + 13, cy + 16)],
           fill=BLEU, bord=INK, trait=2)
    for dx in (-6, 6):
        t.ligne([(cx + dx, cy + 16), (cx + dx, cy + 36)], INK, 2.4)


# --------------------------------------------------------------------------
# Les instruments de composition

def _vignette(t, cx, cy, dessin, nom, cote=130, fond=WHITE_WARM, vif=False):
    """Un pictogramme dans sa carte, son nom dessous. Jamais l-un sans l-autre."""
    t.rrect(cx - cote / 2, cy - cote / 2, cx + cote / 2, cy + cote / 2, 12,
            fill=(GOLD if vif else fond), bord=INK, trait=2)
    dessin(t, cx, cy - 10)
    taille = _taille_tenant(t, [nom], cote - 10, 14)
    t.texte((cx, cy + cote / 2 - 15), nom, taille, INK)


def _grille(t, items, cote=130, haut=92, gauche=86, pas=146, vif=None):
    """Deux colonnes, autant de lignes qu-il faut. Items : (dessin, nom)."""
    for i, (dessin, nom) in enumerate(items):
        _vignette(t, gauche + pas * (i % 2), haut + pas * (i // 2), dessin, nom,
                  cote, vif=(nom == vif))


def _fab_grille(noms, vif=None):
    def f(t):
        _grille(t, [(OUTILS[n], n) for n in noms], vif=vif)
    return f


def _fab_liste(items, titre):
    def f(t):
        _liste(t, items, titre)
    return f


def _fab_duo(gauche, droite, note=None):
    """Deux vignettes côte à côte : ce qui se fait / ce qui ne se fait pas."""
    def f(t):
        _vignette(t, 88, 140, gauche[0], gauche[1], 126)
        _vignette(t, 232, 140, droite[0], droite[1], 126)
        if note:
            t.texte((160, 248), note, 14, INK_2)
    return f


def _fab_scene(dessin, note=None):
    def f(t):
        dessin(t)
        if note:
            t.texte((160, 268), note, 14, INK_2)
    return f


# --------------------------------------------------------------------------
# Les scènes

def _sc_outil_sale(t):
    houe(t, 160, 130)
    for dx, dy in ((-40, 160), (-16, 172), (12, 164), (36, 174)):
        t.disque((160 + dx, dy), 7, fill=TERRE, bord=INK, trait=1.5)
    t.texte((160, 206), 'earth left on the blade', 13, INK_2)


def _sc_outil_propre(t):
    houe(t, 160, 130)
    for dx, dy in ((-44, 96), (44, 104), (-38, 170), (42, 168)):
        t.ligne([(160 + dx, dy), (160 + dx + 10, dy - 10)], GOLD, 2.6)
    t.texte((160, 206), 'washed and dried', 13, INK_2)


def _sc_ranger(t):
    t.ligne([(34, 88), (286, 88)], BOIS, 7)
    for cx, outil in ((88, houe), (160, machette), (232, beche)):
        t.ligne([(cx, 92), (cx, 134)], INK_2, 2)
        outil(t, cx, 176)
    t.texte((160, 250), 'hung up, in the right place', 14, INK_2)


def _sc_nettoyer(t):
    champ(t, 160, 150, 184, 62)
    herbe(t, 108, 128, 4, (150, 160, 120))
    herbe(t, 212, 128, 4, (150, 160, 120))
    machette(t, 160, 128)


def _sc_labour(t):
    champ(t, 160, 158, 184, 66)
    houe(t, 160, 120)


def _sc_fumier(t):
    champ(t, 160, 176, 184, 54)
    tas(t, 160, 127, (120, 96, 72))


def _sc_arroser(t):
    arrosoir(t, 96, 112)
    pousse(t, 206, 178)
    for k in range(5):
        x = 146 + k * 13
        t.ligne([(x, 108 + k * 11), (x - 5, 124 + k * 11)], BLEU, 2.2)


def _sc_sarcler(t):
    pousse(t, 160, 160)
    for cx in (92, 228):
        herbe(t, cx, 160, 5, (132, 150, 92))
        t.ligne([(cx - 26, 134), (cx + 26, 180)], ROUGE, 3.2)
        t.ligne([(cx + 26, 134), (cx - 26, 180)], ROUGE, 3.2)
    t.texte((160, 220), 'the grasses go, the plant stays', 13, INK_2)


def _sc_tailler(t):
    t.ligne([(160, 200), (160, 120)], VERT, 4)
    for cote, y in ((-1, 136), (1, 150), (-1, 164)):
        t.poly([(160, y), (160 + cote * 44, y - 18), (160 + cote * 12, y + 10)],
               fill=VERT, bord=INK, trait=1.8)
    t.poly([(96, 118), (142, 128), (142, 136), (94, 126)], fill=FER, bord=INK, trait=1.8)
    t.poly([(96, 150), (142, 134), (142, 142), (94, 158)], fill=FER, bord=INK, trait=1.8)
    t.disque((128, 132), 5, fill=INK_2, bord=INK, trait=1.4)
    for dy in (-1, 1):
        t.d.arc([int(66 * S), int((124 + dy * 18 - 11) * S), int(100 * S),
                 int((124 + dy * 18 + 11) * S)], 0, 360, fill=INK, width=int(2.4 * S))
    t.rrect(160 - 16, 196, 160 + 16, 208, 4, fill=TERRE, bord=INK, trait=1.6)
    t.texte((160, 242), 'cut the leaves that grew too long', 13, INK_2)


def _sc_paillage(t):
    champ(t, 160, 180, 184, 48)
    for k in range(7):
        x = 78 + k * 28
        t.ligne([(x, 152), (x + 18, 146)], GOLD, 3)
        t.ligne([(x + 4, 160), (x + 22, 155)], GOLD, 3)
    t.texte((160, 232), 'the soil is covered', 13, INK_2)


def _sc_compost(t):
    tas(t, 160, 152, (126, 108, 78))
    for dx, dy, cote in ((-26, 150, -1), (-4, 134, 1), (20, 146, -1)):
        t.poly([(160 + dx, dy), (160 + dx + cote * 26, dy - 16),
                (160 + dx + cote * 8, dy + 8)], fill=VERT, bord=INK, trait=1.8)
    t.texte((160, 212), 'peels and leaves, left to rot', 13, INK_2)


def _sc_zoo(t):
    cage(t, 116, 140, 132, 102)
    bete(t, 116, 144, 56)
    personne(t, 246, 170)


def _sc_regarder(t):
    cage(t, 108, 136, 86, 96)
    bete(t, 108, 142, 44)
    personne(t, 228, 150)
    t.pointille((196, 140), (146, 136), INK_2, 2.4)


def _sc_graine_pousse(t):
    _vignette(t, 88, 140, lambda tt, x, y: graine(tt, x, y + 6, 34), 'seed', 126)
    _vignette(t, 232, 140, lambda tt, x, y: pousse(tt, x, y), 'seedling', 126)
    t.texte((160, 248), 'you may plant one or the other', 14, INK_2)


# --- Couvertures ----------------------------------------------------------

def couv_outils(t):
    _bandeau_couv(t, 'Agricultural tools')
    for i, outil in enumerate((machette, houe, beche, rateau)):
        outil(t, 330 + i * 100, 300)


def couv_preparer(t):
    _bandeau_couv(t, 'Preparing the farm')
    champ(t, 480, 312, 240, 56)
    houe(t, 370, 272)
    pousse(t, 590, 282)


def couv_plantes(t):
    _bandeau_couv(t, 'Caring for plants')
    fleur(t, 392, 290)
    pousse(t, 480, 292)
    arrosoir(t, 572, 282)


def couv_sol(t):
    _bandeau_couv(t, 'Soil enrichment')
    champ(t, 480, 318, 240, 50)
    tas(t, 400, 272)
    tas(t, 560, 272, (126, 108, 78))


def couv_zoo(t):
    _bandeau_couv(t, 'The zoo')
    cage(t, 440, 292, 150, 100)
    bete(t, 440, 296, 62)
    personne(t, 578, 300)


def _fab_seul(nom):
    """L-outil seul, sans son nom : c-est l-image qui est la reponse.

    Une question a images ne peut pas porter l-etiquette de l-objet,
    sinon elle se repond en lisant. Ces sept figures sont donc les
    memes dessins que dans les grilles, mais nus.
    """
    def f(t):
        OUTILS[nom](t, 120, 84)
    return f


FIGURES = [
    # ---- Les outils seuls, pour les questions a images -------------------
    ('kn-ag-1-hoe', 240, 170, _fab_seul('hoe')),
    ('kn-ag-1-cutlass', 240, 170, _fab_seul('cutlass')),
    ('kn-ag-1-spade', 240, 170, _fab_seul('spade')),
    ('kn-ag-1-rake', 240, 170, _fab_seul('rake')),
    ('kn-ag-1-fork', 240, 170, _fab_seul('digging fork')),
    ('kn-ag-1-pick', 240, 170, _fab_seul('pick axe')),
    ('kn-ag-1-bar', 240, 170, _fab_seul('crow bar')),

    # ---- 33. Agricultural tools and their care --------------------------
    ('kn-ag-couv', 960, 540, couv_outils),
    ('kn-ag-def', 320, 320, _fab_grille(['cutlass', 'hoe', 'spade', 'rake'])),
    ('kn-ag-houe', 320, 320, _fab_grille(['hoe', 'cutlass', 'spade', 'rake'], vif='hoe')),
    ('kn-ag-creuser', 320, 320,
     _fab_grille(['digging fork', 'pick axe', 'crow bar', 'spade'])),
    ('kn-ag-soin', 320, 320, _fab_liste(
        ['Clean tools after use', 'Sharpen tools always', 'Oil the metal parts',
         'Dry tools after use'], 'Caring for tools')),
    ('kn-ag-propre', 320, 320, _fab_scene(_sc_outil_propre)),
    ('kn-ag-sale', 320, 320, _fab_scene(_sc_outil_sale)),
    ('kn-ag-ranger', 320, 320, _fab_scene(_sc_ranger)),

    # ---- 34. Preparing the farm for planting -----------------------------
    ('kn-pr-couv', 960, 540, couv_preparer),
    ('kn-pr-etapes', 320, 320, _fab_liste(
        ['Clear the farm', 'Dig or till the soil', 'Add manure', 'Water if there is no rain',
         'Plant the seed'], 'Five steps')),
    ('kn-pr-nettoyer', 320, 320, _fab_scene(_sc_nettoyer, 'the grasses are cut away')),
    ('kn-pr-labour', 320, 320, _fab_scene(_sc_labour, 'the soil is turned over')),
    ('kn-pr-fumier', 320, 320, _fab_scene(_sc_fumier, 'manure is spread on the soil')),
    ('kn-pr-graine', 320, 320, _fab_scene(_sc_graine_pousse)),

    # ---- 35. Caring for plants and flowers -------------------------------
    ('kn-pl-couv', 960, 540, couv_plantes),
    ('kn-pl-etapes', 320, 320, _fab_liste(
        ['Water them in the dry season', 'Weed the grasses around them',
         'Apply manure to feed them', 'Trim leaves when they overgrow'], 'Four ways')),
    ('kn-pl-arroser', 320, 320, _fab_scene(_sc_arroser, 'water, above all in the dry season')),
    ('kn-pl-sarcler', 320, 320, _fab_scene(_sc_sarcler)),
    ('kn-pl-tailler', 320, 320, _fab_scene(_sc_tailler)),

    # ---- 36. Soil enrichment ---------------------------------------------
    ('kn-so-couv', 960, 540, couv_sol),
    ('kn-so-moyens', 320, 320, _fab_liste(
        ['Apply manure', 'Add fertiliser', 'Mulch the soil', 'Add compost',
         'Conserve water'], 'Five ways')),
    ('kn-so-fumier', 320, 320, _fab_scene(_sc_fumier, 'animal dung spread on the soil')),
    ('kn-so-paillage', 320, 320, _fab_scene(_sc_paillage)),
    ('kn-so-compost', 320, 320, _fab_scene(_sc_compost)),

    # ---- 41. The zoo -------------------------------------------------------
    ('kn-zo-couv', 960, 540, couv_zoo),
    ('kn-zo-def', 320, 320, _fab_scene(_sc_zoo, 'wild animals kept for people to visit')),
    ('kn-zo-regarder', 320, 320, _fab_scene(_sc_regarder, 'you watch, you do not touch')),
    ('kn-zo-cage', 320, 320, _fab_scene(
        lambda t: (cage(t, 160, 150, 170, 120), bete(t, 160, 154, 68)),
        'the cage keeps the beast in')),
]


def controler():
    """Chaque figure est dessinée, mesurée, et refusée si elle déborde."""
    assert len({c for c, _w, _h, _f in FIGURES}) == len(FIGURES), 'deux figures ont la même clé'
    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        im = t.fini()
        fond = im.getpixel((1, 1))
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
            fautifs = fv._hors_bande(im)
            assert fautifs == 0, \
                'couverture %s : %d pixels hors de la fiche' % (cle, fautifs)
            dehors = 0
            for y in list(range(0, BANDEAU[0])) + list(range(BANDEAU[1], h)):
                f2 = im.getpixel((3, y))
                for x in range(0, w, 4):
                    if sum(abs(a - b) for a, b in zip(im.getpixel((x, y)), f2)) > 60:
                        dehors += 1
            assert dehors == 0, \
                'couverture %s : %d pixels hors du bandeau' % (cle, dehors)


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
