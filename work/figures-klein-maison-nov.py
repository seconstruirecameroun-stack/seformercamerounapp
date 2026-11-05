# -*- coding: utf-8 -*-
"""
Les figures des quatre leçons d-alimentation et de maison de KLEIN (CE1)
— cahier du 15 septembre au 20 octobre 2026.

Même parti pris que pour les outils : un ustensile est un OBJET, pas une
règle. On ne retient pas « mortar and pestle » en lisant les mots, on le
retient en voyant le mortier. Le module est donc une seconde boîte de
pictogrammes, bâtie sur les mêmes conventions que figures-klein-agri :

  - le bois est toujours BOIS, le métal toujours FER, la terre cuite
    toujours TERRE. Un objet se reconnaît à sa FORME, jamais à sa
    couleur, pour qu-on puisse en aligner quatre dans une question à
    images sans que la bonne réponse saute aux yeux
  - chaque pictogramme tient dans un carré de 100 centré sur (cx, cy)

Les six classes d-aliments posent un cas à part : « protein » n-est pas
un objet, c-est une catégorie. Elles sont donc montrées par leur
SOURCE — ce que la maîtresse a écrit dans la colonne du milieu — et le
nom de la classe reste écrit.

Usage :  python work/figures-klein-maison-nov.py
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
fa = _charger('figures_anglais_oct', 'figures-anglais-oct.py')
fg = _charger('figures_klein_agri', 'figures-klein-agri-nov.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

VERT, VERT_PALE, TERRE, ROUGE = fa.VERT, fa.VERT_PALE, fa.TERRE, fa.ROUGE
FER, BOIS = fg.FER, fg.BOIS
FEU = (226, 136, 58)
FROID = (176, 212, 232)

_mesure = fa._mesure
_pastille = fa._pastille
_taille_tenant = fa._taille_tenant
_liste = fa._liste
_bandeau_couv = fa._bandeau_couv
_vignette = fg._vignette
_grille = fg._grille
BANDEAU = fa.BANDEAU


# --------------------------------------------------------------------------
# Les ustensiles de cuisine

def mortier(t, cx, cy):
    """Le mortier et son pilon. Le pilon penche, sinon on lit un verre."""
    t.poly([(cx - 30, cy + 2), (cx + 30, cy + 2), (cx + 20, cy + 40), (cx - 20, cy + 40)],
           fill=TERRE, bord=INK, trait=2)
    t.rrect(cx - 34, cy - 6, cx + 34, cy + 6, 5, fill=CLAY, bord=INK, trait=2)
    fg._manche(t, (cx + 22, cy - 46), (cx + 4, cy - 4), 9)
    t.disque((cx + 24, cy - 46), 8, fill=BOIS, bord=INK, trait=1.8)


def marmite(t, cx, cy):
    t.poly([(cx - 28, cy - 12), (cx + 28, cy - 12), (cx + 22, cy + 32), (cx - 22, cy + 32)],
           fill=FER, bord=INK, trait=2)
    t.rrect(cx - 34, cy - 20, cx + 34, cy - 10, 4, fill=FER, bord=INK, trait=2)
    for cote in (-1, 1):
        t.d.arc([int((cx + cote * 30 - 9) * S), int((cy - 14) * S),
                 int((cx + cote * 30 + 9) * S), int((cy + 6) * S)],
                0, 360, fill=INK, width=int(2.2 * S))


def couteau(t, cx, cy):
    fg._manche(t, (cx - 30, cy + 34), (cx - 12, cy + 8), 9)
    fg._fer(t, [(cx - 16, cy + 12), (cx - 6, cy + 2), (cx + 30, cy - 36),
                (cx + 34, cy - 28), (cx - 10, cy + 18)])


def cuillere(t, cx, cy):
    fg._manche(t, (cx + 10, cy + 40), (cx - 2, cy - 8), 7)
    t.d.ellipse([int((cx - 18) * S), int((cy - 40) * S), int((cx + 14) * S), int((cy - 4) * S)],
                fill=FER, outline=INK, width=int(2 * S))


def fourchette(t, cx, cy):
    fg._manche(t, (cx, cy + 40), (cx, cy - 6), 7)
    fg._fer(t, [(cx - 14, cy - 10), (cx + 14, cy - 10), (cx + 14, cy - 2), (cx - 14, cy - 2)])
    for k in range(4):
        x = cx - 11 + k * 7.3
        fg._fer(t, [(x - 2, cy - 38), (x + 2, cy - 38), (x + 2, cy - 10), (x - 2, cy - 10)])


def rape(t, cx, cy):
    """La râpe : une tôle percée, et c-est le percement qui la nomme."""
    fg._fer(t, [(cx - 18, cy - 34), (cx + 18, cy - 34), (cx + 24, cy + 32),
                (cx - 24, cy + 32)])
    for i in range(5):
        for j in range(3):
            x = cx - 12 + j * 12 + (6 if i % 2 else 0)
            y = cy - 24 + i * 13
            t.poly([(x - 4, y + 3), (x + 4, y + 3), (x, y - 4)], fill=WHITE_WARM,
                   bord=INK_2, trait=1.2)


def planche(t, cx, cy):
    t.rrect(cx - 30, cy - 28, cx + 30, cy + 30, 6, fill=BOIS, bord=INK, trait=2)
    t.disque((cx + 20, cy - 18), 5, fill=WHITE_WARM, bord=INK, trait=1.6)
    for k in range(3):
        t.ligne([(cx - 20, cy - 6 + k * 13), (cx + 20, cy - 6 + k * 13)], (150, 108, 68), 2)


def spatule(t, cx, cy):
    fg._manche(t, (cx, cy + 42), (cx, cy - 6), 7)
    fg._fer(t, [(cx - 16, cy - 8), (cx + 16, cy - 8), (cx + 13, cy - 38), (cx - 13, cy - 38)])


def pierre(t, cx, cy):
    """La pierre à écraser : une dalle et sa molette."""
    t.poly([(cx - 36, cy + 10), (cx + 36, cy + 10), (cx + 30, cy + 34), (cx - 30, cy + 34)],
           fill=(150, 150, 150), bord=INK, trait=2)
    t.d.ellipse([int((cx - 20) * S), int((cy - 16) * S), int((cx + 20) * S), int((cy + 12) * S)],
                fill=(176, 176, 176), outline=INK, width=int(2 * S))


USTENSILES = {'mortar and pestle': mortier, 'pot': marmite, 'knife': couteau,
              'spoon': cuillere, 'fork': fourchette, 'grater': rape,
              'chopping board': planche, 'spatula': spatule,
              'grinding stone': pierre}


# --------------------------------------------------------------------------
# Les meubles

def chaise(t, cx, cy):
    t.rrect(cx - 22, cy - 40, cx - 12, cy + 34, 3, fill=BOIS, bord=INK, trait=2)
    t.rrect(cx - 22, cy - 2, cx + 26, cy + 8, 3, fill=BOIS, bord=INK, trait=2)
    t.rrect(cx - 18, cy - 36, cx - 14, cy - 4, 2, fill=(150, 108, 68), bord=INK, trait=1.4)
    for x in (cx - 20, cx + 20):
        t.rrect(x - 4, cy + 8, x + 4, cy + 36, 2, fill=BOIS, bord=INK, trait=1.8)


def table(t, cx, cy):
    t.rrect(cx - 38, cy - 14, cx + 38, cy - 2, 4, fill=BOIS, bord=INK, trait=2)
    for x in (cx - 30, cx + 30):
        t.rrect(x - 4, cy - 2, x + 4, cy + 34, 2, fill=BOIS, bord=INK, trait=1.8)


def lit(t, cx, cy):
    t.rrect(cx - 40, cy - 30, cx - 30, cy + 20, 3, fill=BOIS, bord=INK, trait=2)
    t.rrect(cx + 30, cy - 10, cx + 40, cy + 20, 3, fill=BOIS, bord=INK, trait=2)
    t.rrect(cx - 36, cy - 6, cx + 36, cy + 14, 4, fill=WHITE_WARM, bord=INK, trait=2)
    t.rrect(cx - 30, cy - 16, cx - 8, cy - 4, 4, fill=SKY, bord=INK, trait=1.8)
    for x in (cx - 34, cx + 34):
        t.rrect(x - 3, cy + 14, x + 3, cy + 32, 2, fill=BOIS, bord=INK, trait=1.6)


def armoire(t, cx, cy):
    t.rrect(cx - 28, cy - 38, cx + 28, cy + 34, 5, fill=BOIS, bord=INK, trait=2)
    t.ligne([(cx, cy - 34), (cx, cy + 30)], INK, 2)
    for dx in (-7, 7):
        t.disque((cx + dx, cy - 2), 3.5, fill=FER, bord=INK, trait=1.4)
    for x in (cx - 22, cx + 22):
        t.rrect(x - 3, cy + 34, x + 3, cy + 42, 2, fill=BOIS, bord=INK, trait=1.6)


def canape(t, cx, cy):
    t.rrect(cx - 40, cy - 22, cx + 40, cy + 6, 8, fill=CLAY, bord=INK, trait=2)
    t.rrect(cx - 40, cy + 2, cx + 40, cy + 22, 7, fill=(216, 132, 84), bord=INK, trait=2)
    for x in (cx - 36, cx + 36):
        t.rrect(x - 7, cy - 8, x + 7, cy + 20, 6, fill=CLAY, bord=INK, trait=2)
    for x in (cx - 30, cx + 30):
        t.rrect(x - 3, cy + 22, x + 3, cy + 34, 2, fill=BOIS, bord=INK, trait=1.6)


def pupitre(t, cx, cy):
    t.poly([(cx - 36, cy - 14), (cx + 36, cy - 22), (cx + 36, cy - 10), (cx - 36, cy - 2)],
           fill=BOIS, bord=INK, trait=2)
    t.rrect(cx - 36, cy - 2, cx + 36, cy + 6, 3, fill=(150, 108, 68), bord=INK, trait=1.8)
    for x in (cx - 30, cx + 30):
        t.rrect(x - 4, cy + 6, x + 4, cy + 36, 2, fill=BOIS, bord=INK, trait=1.8)


MEUBLES = {'chair': chaise, 'table': table, 'bed': lit, 'cupboard': armoire,
           'sofa': canape, 'desk': pupitre}


# --------------------------------------------------------------------------
# Les aliments, montrés par leur source

def grain(t, cx, cy):
    """Un tas de grains : riz, maïs, manioc. La classe des glucides."""
    t.poly([(cx - 34, cy + 24), (cx, cy - 18), (cx + 34, cy + 24)],
           fill=SAND, bord=INK, trait=2)
    for dx, dy in ((-16, 12), (0, 2), (14, 12), (-6, 18), (8, 18)):
        t.d.ellipse([int((cx + dx - 5) * S), int((cy + dy - 3) * S),
                     int((cx + dx + 5) * S), int((cy + dy + 3) * S)],
                    fill=GOLD, outline=INK, width=int(1.2 * S))


def poisson(t, cx, cy):
    """Un poisson : viande, haricot, poisson. La classe des protides."""
    t.poly([(cx - 34, cy), (cx - 12, cy - 20), (cx + 18, cy - 16), (cx + 30, cy),
            (cx + 18, cy + 16), (cx - 12, cy + 20)], fill=SKY, bord=INK, trait=2)
    t.poly([(cx + 28, cy), (cx + 44, cy - 16), (cx + 44, cy + 16)],
           fill=SKY, bord=INK, trait=2)
    t.disque((cx - 18, cy - 4), 4, fill=INK)


def fruit(t, cx, cy):
    """Un fruit et sa feuille : fruits et légumes, la classe des vitamines."""
    t.disque((cx, cy + 4), 26, fill=ROUGE, bord=INK, trait=2)
    t.ligne([(cx, cy - 22), (cx + 2, cy - 36)], (110, 86, 60), 3)
    t.poly([(cx + 2, cy - 32), (cx + 28, cy - 40), (cx + 14, cy - 22)],
           fill=VERT, bord=INK, trait=1.8)


def huile(t, cx, cy):
    """Une bouteille d-huile : la classe des lipides."""
    t.rrect(cx - 6, cy - 40, cx + 6, cy - 26, 2, fill=GOLD, bord=INK, trait=1.8)
    t.poly([(cx - 6, cy - 26), (cx + 6, cy - 26), (cx + 18, cy - 8), (cx + 18, cy + 34),
            (cx - 18, cy + 34), (cx - 18, cy - 8)], fill=GOLD, bord=INK, trait=2)
    t.rrect(cx - 13, cy + 2, cx + 13, cy + 20, 3, fill=WHITE_WARM, bord=INK, trait=1.6)


def sel(t, cx, cy):
    """Une salière : sels minéraux."""
    t.poly([(cx - 16, cy - 18), (cx + 16, cy - 18), (cx + 20, cy + 32), (cx - 20, cy + 32)],
           fill=WHITE_WARM, bord=INK, trait=2)
    t.rrect(cx - 14, cy - 28, cx + 14, cy - 16, 4, fill=FER, bord=INK, trait=2)
    for dx in (-5, 0, 5):
        t.disque((cx + dx, cy - 22), 1.8, fill=INK)


def verre_eau(t, cx, cy):
    t.poly([(cx - 18, cy - 30), (cx + 18, cy - 30), (cx + 13, cy + 32), (cx - 13, cy + 32)],
           fill=WHITE_WARM, bord=INK, trait=2)
    t.poly([(cx - 15, cy - 8), (cx + 15, cy - 8), (cx + 13, cy + 30), (cx - 13, cy + 30)],
           fill=SKY, bord=INK, trait=1.6)


ALIMENTS = {'rice and cassava': grain, 'meat and fish': poisson,
            'fruits and vegetables': fruit, 'oil and butter': huile,
            'mineral salts': sel, 'water': verre_eau}


# --------------------------------------------------------------------------
# La cuisson et la conservation

def feu(t, cx, cy, l=1.0):
    for d, couleur in ((0, FEU), (7, GOLD)):
        t.poly([(cx - (22 - d) * l, cy + 26), (cx - (10 - d * 0.5) * l, cy - (10 - d) * l),
                (cx, cy + (2 + d) * l), (cx + (10 - d * 0.5) * l, cy - (22 - d) * l),
                (cx + (22 - d) * l, cy + 26)], fill=couleur, bord=INK, trait=1.8)


def poele(t, cx, cy):
    t.d.ellipse([int((cx - 30) * S), int((cy - 14) * S), int((cx + 20) * S),
                 int((cy + 18) * S)], fill=FER, outline=INK, width=int(2 * S))
    fg._manche(t, (cx + 18, cy - 2), (cx + 46, cy - 14), 7)


def four(t, cx, cy):
    t.rrect(cx - 34, cy - 30, cx + 34, cy + 34, 6, fill=FER, bord=INK, trait=2)
    t.rrect(cx - 26, cy - 10, cx + 26, cy + 26, 4, fill=(86, 72, 66), bord=INK, trait=2)
    t.rrect(cx - 20, cy - 24, cx + 20, cy - 18, 3, fill=WHITE_WARM, bord=INK, trait=1.4)
    for k in range(3):
        t.ligne([(cx - 18, cy + k * 11), (cx + 18, cy + k * 11)], (150, 136, 128), 2)


def grille_feu(t, cx, cy):
    """Le gril : une claie posee sur ses pieds, et le feu dessous."""
    feu(t, cx, cy + 24, 0.58)
    for y in (cy - 20, cy - 10):
        t.ligne([(cx - 38, y), (cx + 38, y)], FER, 3.2)
    for k in range(9):
        x = cx - 36 + k * 9
        t.ligne([(x, cy - 20), (x, cy - 10)], FER, 2.2)
    for x in (cx - 34, cx + 34):
        t.ligne([(x, cy - 10), (x, cy + 26)], FER, 2.6)


def soleil(t, cx, cy):
    t.disque((cx, cy), 20, fill=GOLD, bord=INK, trait=2)
    for k in range(8):
        a = math.pi * 2 * k / 8
        t.ligne([(cx + math.cos(a) * 26, cy + math.sin(a) * 26),
                 (cx + math.cos(a) * 38, cy + math.sin(a) * 38)], GOLD, 3)


def frigo(t, cx, cy):
    t.rrect(cx - 26, cy - 38, cx + 26, cy + 38, 6, fill=FROID, bord=INK, trait=2)
    t.ligne([(cx - 26, cy - 8), (cx + 26, cy - 8)], INK, 2)
    for dy in (-24, 10):
        t.rrect(cx + 14, cy + dy, cx + 19, cy + dy + 16, 2, fill=FER, bord=INK, trait=1.4)
    for k in range(3):
        t.ligne([(cx - 16 + k * 7, cy + 12), (cx - 20 + k * 7, cy + 26)], BLEU, 2)


def boite(t, cx, cy):
    t.rrect(cx - 22, cy - 26, cx + 22, cy + 30, 4, fill=FER, bord=INK, trait=2)
    t.d.ellipse([int((cx - 22) * S), int((cy - 34) * S), int((cx + 22) * S),
                 int((cy - 18) * S)], fill=(196, 202, 206), outline=INK, width=int(2 * S))
    t.rrect(cx - 16, cy - 12, cx + 16, cy + 14, 3, fill=WHITE_WARM, bord=INK, trait=1.6)


def fumee(t, cx, cy):
    feu(t, cx, cy + 30, 0.6)
    for k, dx in enumerate((-14, 0, 14)):
        t.d.arc([int((cx + dx - 11) * S), int((cy - 34 + k * 6) * S),
                 int((cx + dx + 11) * S), int((cy - 14 + k * 6) * S)],
                160, 380, fill=INK_2, width=int(2.4 * S))
    t.poly([(cx - 24, cy - 2), (cx + 24, cy - 2), (cx + 18, cy + 8), (cx - 18, cy + 8)],
           fill=SKY, bord=INK, trait=1.8)


# --------------------------------------------------------------------------
# Les instruments de composition

def _fab_grille_u(noms, vif=None):
    def f(t):
        _grille(t, [(USTENSILES[n], n) for n in noms], vif=vif)
    return f


def _fab_grille_m(noms, vif=None):
    def f(t):
        _grille(t, [(MEUBLES[n], n) for n in noms], vif=vif)
    return f


def _fab_seul(table_, nom):
    """L-objet seul, sans son nom, sur une toile juste a sa taille.

    En 320x320 l-objet occupait un quart du cadre : pose a cote de
    trois autres dans une question a images, il devenait illisible.
    La toile fait donc 170, l-objet en remplit les deux tiers.
    """
    def f(t):
        table_[nom](t, 120, 84)
    return f


def _fab_liste(items, titre):
    def f(t):
        _liste(t, items, titre)
    return f


def _classe(t, dessin, classe, role):
    """Une classe d-aliment : sa source dessinée, son nom, son rôle."""
    dessin(t, 160, 116)
    _pastille(t, 160, 192, classe, 20, fond=GOLD, marge=18)
    taille = _taille_tenant(t, [role], 290, 15)
    t.texte((160, 240), role, taille, INK)


def _fab_classe(dessin, classe, role):
    def f(t):
        _classe(t, dessin, classe, role)
    return f


def _methode(t, dessin, nom, exemples):
    dessin(t, 160, 120)
    _pastille(t, 160, 192, nom, 20, fond=MINT, marge=18)
    taille = _taille_tenant(t, [exemples], 290, 15)
    t.texte((160, 240), exemples, taille, INK_2)


def _fab_methode(dessin, nom, exemples):
    def f(t):
        _methode(t, dessin, nom, exemples)
    return f


def _fab_duo(g, d, note):
    def f(t):
        _vignette(t, 88, 136, g[0], g[1], 124)
        _vignette(t, 232, 136, d[0], d[1], 124)
        t.texte((160, 240), note, 14, INK_2)
    return f


# --- Couvertures ----------------------------------------------------------

def couv_aliments(t):
    _bandeau_couv(t, 'Food and its classes')
    for i, dessin in enumerate((grain, poisson, fruit, huile)):
        dessin(t, 348 + i * 88, 300)


def couv_cuisson(t):
    _bandeau_couv(t, 'Cooking methods')
    marmite(t, 384, 296)
    feu(t, 384, 322, 0.6)
    poele(t, 486, 300)
    four(t, 592, 296)


def couv_conservation(t):
    _bandeau_couv(t, 'Food conservation')
    soleil(t, 382, 290)
    frigo(t, 480, 296)
    boite(t, 578, 296)


def couv_maison(t):
    _bandeau_couv(t, 'Utensils and furniture')
    mortier(t, 376, 292)
    marmite(t, 460, 296)
    chaise(t, 540, 296)
    lit(t, 620, 300)


FIGURES = [
    # ---- Les objets seuls, pour les questions a images -------------------
    ('kn-u1-mortier', 240, 170, _fab_seul(USTENSILES, 'mortar and pestle')),
    ('kn-u1-marmite', 240, 170, _fab_seul(USTENSILES, 'pot')),
    ('kn-u1-couteau', 240, 170, _fab_seul(USTENSILES, 'knife')),
    ('kn-u1-rape', 240, 170, _fab_seul(USTENSILES, 'grater')),
    ('kn-u1-planche', 240, 170, _fab_seul(USTENSILES, 'chopping board')),
    ('kn-m1-chaise', 240, 170, _fab_seul(MEUBLES, 'chair')),
    ('kn-m1-table', 240, 170, _fab_seul(MEUBLES, 'table')),
    ('kn-m1-lit', 240, 170, _fab_seul(MEUBLES, 'bed')),
    ('kn-m1-armoire', 240, 170, _fab_seul(MEUBLES, 'cupboard')),

    # ---- 37. Food and its six classes ------------------------------------
    ('kn-fo-couv', 960, 540, couv_aliments),
    ('kn-fo-def', 320, 320, lambda t: (
        grain(t, 102, 130), poisson(t, 214, 126), fruit(t, 102, 216), verre_eau(t, 214, 212),
        t.texte((160, 276), 'what living things eat or drink', 14, INK_2))),
    # Six classes ne tiennent pas dans un carre de 320 : la toile
    # s-allonge plutot que de serrer les lignes jusqu-a l-illisible.
    ('kn-fo-six', 320, 380, _fab_liste(
        ['Carbohydrates give energy', 'Proteins build the body',
         'Vitamins prevent diseases', 'Fats keep the body warm',
         'Minerals make bones', 'Water helps digestion'], 'Six classes of food')),
    ('kn-fo-carb', 320, 320, _fab_classe(grain, 'carbohydrates', 'rice and cassava, for energy')),
    ('kn-fo-prot', 320, 320, _fab_classe(poisson, 'proteins', 'beans, meat and fish, to build')),
    ('kn-fo-vit', 320, 320, _fab_classe(fruit, 'vitamins', 'fruits and vegetables, to protect')),
    ('kn-fo-fat', 320, 320, _fab_classe(huile, 'fats and oils', 'oil and butter, to keep warm')),
    ('kn-fo-min', 320, 320, _fab_classe(sel, 'mineral salts', 'salt and milk, to make bones')),
    ('kn-fo-eau', 320, 320, _fab_classe(verre_eau, 'water', 'water, to help digestion')),

    # ---- 38. Cooking methods ----------------------------------------------
    ('kn-cu-couv', 960, 540, couv_cuisson),
    ('kn-cu-liste', 320, 320, _fab_liste(
        ['Stewing and boiling', 'Frying in oil', 'Roasting on fire', 'Grilling over fire',
         'Toasting and baking'], 'Ways of cooking')),
    ('kn-cu-bouillir', 320, 320, _fab_methode(
        lambda t, cx, cy: (marmite(t, cx, cy - 22), feu(t, cx, cy + 26, 0.6)),
        'boiling', 'yams, rice, cassava, potato')),
    ('kn-cu-frire', 320, 320, _fab_methode(poele, 'frying', 'fish, meat, chicken, plantain')),
    ('kn-cu-rotir', 320, 320, _fab_methode(grille_feu, 'roasting', 'plum, plantain, fish, yam')),
    ('kn-cu-four', 320, 320, _fab_methode(four, 'baking', 'biscuits, bread, cake')),

    # ---- 39. Food conservation --------------------------------------------
    ('kn-co-couv', 960, 540, couv_conservation),
    ('kn-co-liste', 320, 320, _fab_liste(
        ['Drying in the sun', 'Freezing in the cold', 'Canning in tins', 'Salting with salt',
         'Smoking over fire'], 'Five ways to keep food')),
    ('kn-co-secher', 320, 320, _fab_methode(soleil, 'drying', 'vegetables, maize, beans')),
    ('kn-co-geler', 320, 320, _fab_methode(frigo, 'freezing', 'meat, fish, tomato')),
    ('kn-co-boite', 320, 320, _fab_methode(boite, 'canning', 'fish, tomato, juice, milk')),
    ('kn-co-fumer', 320, 320, _fab_methode(fumee, 'smoking', 'fish and meat, over the fire')),
    ('kn-co-saler', 320, 320, _fab_methode(sel, 'salting', 'meat and fish, kept with salt')),

    # ---- 40. Kitchen utensils and household furniture ---------------------
    ('kn-uf-couv', 960, 540, couv_maison),
    ('kn-uf-ustensiles', 320, 320, _fab_grille_u(
        ['mortar and pestle', 'pot', 'knife', 'spoon'])),
    ('kn-uf-autres', 320, 320, _fab_grille_u(
        ['grater', 'chopping board', 'spatula', 'fork'])),
    ('kn-uf-moudre', 320, 320, _fab_grille_u(
        ['mortar and pestle', 'grinding stone', 'grater', 'knife'],
        vif='mortar and pestle')),
    ('kn-uf-meubles', 320, 320, _fab_grille_m(['chair', 'table', 'bed', 'cupboard'])),
    ('kn-uf-autres-m', 320, 320, _fab_grille_m(['sofa', 'desk', 'cupboard', 'chair'])),
    ('kn-uf-difference', 320, 320, _fab_duo(
        (marmite, 'a pot'), (chaise, 'a chair'),
        'one prepares food, one makes the home easy')),
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
