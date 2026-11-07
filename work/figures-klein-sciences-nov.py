# -*- coding: utf-8 -*-
"""
Les figures des cinq leçons de sciences en français de KLEIN (CE1) —
pages du cahier d-octobre, lot du 7 novembre 2026.

UNE PRÉCAUTION SUR CE LOT. L-étiquette de la page 12 porte « GUETSA /
BRA… » : le cahier photographié est physiquement celui de BRAYNE. Le
père a demandé que ces leçons aillent à KLEIN, ce qui est cohérent —
les leçons 4, 7, 8 et 9 de KLEIN viennent déjà de ce même cahier, aux
mêmes dates. C-est noté ici pour que personne n-ait à le redécouvrir.

CE QUE CES LEÇONS DEMANDENT D-UNE IMAGE

Quatre d-entre elles sont des leçons de CLASSEMENT : on range des
objets selon ce qui les fait marcher, des animaux selon leur façon de
se déplacer ou ce qu-ils mangent, des corps selon qu-ils brûlent ou
non. L-image utile est donc la grille nommée, déjà écrite pour les
outils de KLEIN, et le module s-en sert sans la redessiner.

Ce qu-il faut ajouter, ce sont les objets du vent — un moulin, une
voile, une girouette ne ressemblent à rien d-existant ici — et une
petite ménagerie : un quadrupède, un oiseau, un serpent, une
grenouille, un escargot. Ils sont bâtis sur la même convention que les
outils : la FORME distingue, jamais la couleur, pour qu-on puisse en
aligner quatre sans que la réponse se devine à la teinte.

Usage :  python work/figures-klein-sciences-nov.py
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
fk = _charger('figures_klein_maison', 'figures-klein-maison-nov.py')
fb = _charger('figures_brayne_env', 'figures-brayne-env-nov.py')
fs = _charger('figures_brayne_sante', 'figures-brayne-sante-nov.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

VERT, TERRE, ROUGE = fa.VERT, fa.TERRE, fa.ROUGE
FER, BOIS = fg.FER, fg.BOIS
GRIS = fb.GRIS

champ, tas, herbe, pousse = fg.champ, fg.tas, fg.herbe, fg.pousse
poisson, sel = fk.poisson, fk.sel
# La bouteille et la cuve ont ete dessinees pour les lecons de sante de
# BRAYNE : elles servent ici telles quelles.
bouteille = fs.bouteille
soleil, frigo, fumee, feu, boite = fk.soleil, fk.frigo, fk.fumee, fk.feu, fk.boite
feuille, arbre, _note = fb.feuille, fb.arbre, fb._note

_mesure = fa._mesure
_pastille = fa._pastille
_taille_tenant = fa._taille_tenant
_liste = fa._liste
_bandeau_couv = fa._bandeau_couv
_vignette = fg._vignette
_grille = fg._grille
BANDEAU = fa.BANDEAU


# --------------------------------------------------------------------------
# Les objets que le vent fait marcher

def moulin(t, cx, cy, l=1.0):
    t.poly([(cx - 16 * l, cy + 36 * l), (cx - 9 * l, cy - 10 * l),
            (cx + 9 * l, cy - 10 * l), (cx + 16 * l, cy + 36 * l)],
           fill=SAND, bord=INK, trait=2)
    for k in range(4):
        a = math.pi / 2 * k + 0.4
        t.poly([(cx, cy - 16 * l),
                (cx + math.cos(a) * 34 * l, cy - 16 * l + math.sin(a) * 34 * l),
                (cx + math.cos(a + 0.5) * 26 * l, cy - 16 * l + math.sin(a + 0.5) * 26 * l)],
               fill=WHITE_WARM, bord=INK, trait=1.8)
    t.disque((cx, cy - 16 * l), 5 * l, fill=CLAY, bord=INK, trait=1.6)


def montgolfiere(t, cx, cy, l=1.0):
    t.d.ellipse([int((cx - 26 * l) * S), int((cy - 42 * l) * S),
                 int((cx + 26 * l) * S), int((cy + 8 * l) * S)],
                fill=CLAY, outline=INK, width=int(2 * S))
    t.ligne([(cx - 13 * l, cy + 4 * l), (cx - 9 * l, cy + 24 * l)], INK, 1.8)
    t.ligne([(cx + 13 * l, cy + 4 * l), (cx + 9 * l, cy + 24 * l)], INK, 1.8)
    t.rrect(cx - 10 * l, cy + 24 * l, cx + 10 * l, cy + 40 * l, 3,
            fill=BOIS, bord=INK, trait=2)


def cerf_volant(t, cx, cy, l=1.0):
    t.poly([(cx, cy - 34 * l), (cx + 22 * l, cy - 6 * l), (cx, cy + 22 * l),
            (cx - 22 * l, cy - 6 * l)], fill=MINT, bord=INK, trait=2)
    t.ligne([(cx, cy - 34 * l), (cx, cy + 22 * l)], INK_2, 1.4)
    t.ligne([(cx - 22 * l, cy - 6 * l), (cx + 22 * l, cy - 6 * l)], INK_2, 1.4)
    for k in range(3):
        t.d.arc([int((cx - 8 * l) * S), int((cy + 22 * l + k * 12 * l) * S),
                 int((cx + 8 * l) * S), int((cy + 34 * l + k * 12 * l) * S)],
                180, 360 if k % 2 else 0, fill=CLAY, width=int(2 * S))


def voilier(t, cx, cy, l=1.0):
    t.poly([(cx - 34 * l, cy + 18 * l), (cx + 34 * l, cy + 18 * l),
            (cx + 24 * l, cy + 34 * l), (cx - 24 * l, cy + 34 * l)],
           fill=BOIS, bord=INK, trait=2)
    t.ligne([(cx, cy + 16 * l), (cx, cy - 36 * l)], INK, 2.4)
    t.poly([(cx + 2 * l, cy - 34 * l), (cx + 28 * l, cy + 12 * l), (cx + 2 * l, cy + 12 * l)],
           fill=WHITE_WARM, bord=INK, trait=2)
    t.poly([(cx - 2 * l, cy - 26 * l), (cx - 22 * l, cy + 12 * l), (cx - 2 * l, cy + 12 * l)],
           fill=SKY, bord=INK, trait=2)


def parachute(t, cx, cy, l=1.0):
    t.d.pieslice([int((cx - 32 * l) * S), int((cy - 34 * l) * S),
                  int((cx + 32 * l) * S), int((cy + 14 * l) * S)], 180, 360,
                 fill=GOLD, outline=INK, width=int(2 * S))
    for dx in (-26, -9, 9, 26):
        t.ligne([(cx + dx * l, cy - 7 * l), (cx, cy + 24 * l)], INK_2, 1.5)
    t.disque((cx, cy + 30 * l), 8 * l, fill=SAND, bord=INK, trait=1.8)


def girouette(t, cx, cy, l=1.0):
    t.ligne([(cx, cy + 38 * l), (cx, cy - 30 * l)], INK, 2.6)
    t.poly([(cx + 4 * l, cy - 34 * l), (cx + 34 * l, cy - 22 * l), (cx + 4 * l, cy - 10 * l)],
           fill=CLAY, bord=INK, trait=2)
    t.poly([(cx - 4 * l, cy - 32 * l), (cx - 22 * l, cy - 22 * l), (cx - 4 * l, cy - 12 * l)],
           fill=CLAY, bord=INK, trait=2)
    t.ligne([(cx - 20 * l, cy - 2 * l), (cx + 20 * l, cy - 2 * l)], INK_2, 2)
    t.ligne([(cx, cy - 18 * l), (cx, cy + 14 * l)], INK_2, 2)


def anemometre(t, cx, cy, l=1.0):
    t.ligne([(cx, cy + 38 * l), (cx, cy - 6 * l)], INK, 2.6)
    for k in range(3):
        a = math.pi * 2 * k / 3 - math.pi / 2
        bx, by = cx + math.cos(a) * 26 * l, cy - 6 * l + math.sin(a) * 26 * l
        t.ligne([(cx, cy - 6 * l), (bx, by)], INK_2, 2)
        t.d.pieslice([int((bx - 10 * l) * S), int((by - 10 * l) * S),
                      int((bx + 10 * l) * S), int((by + 10 * l) * S)], 0, 360,
                     fill=SKY, outline=INK, width=int(1.8 * S))
    t.disque((cx, cy - 6 * l), 4 * l, fill=CLAY, bord=INK, trait=1.5)


def souffle(t, cx, cy, n=3, l=1.0):
    """Le vent lui-même : des traits courbes, puisqu-on ne le voit pas."""
    for k in range(n):
        y = cy + (k - (n - 1) / 2) * 15 * l
        t.d.arc([int((cx - 34 * l) * S), int((y - 12 * l) * S),
                 int((cx + 22 * l) * S), int((y + 12 * l) * S)],
                200, 340, fill=SKY, width=int(3 * l * S))
        t.ligne([(cx + 20 * l, y - 8 * l), (cx + 30 * l, y - 2 * l)], SKY, 3 * l)


# --------------------------------------------------------------------------
# La petite ménagerie

def quadrupede(t, cx, cy, l=1.0, couleur=SAND, cornes=False, queue=True):
    t.rrect(cx - 28 * l, cy - 10 * l, cx + 18 * l, cy + 14 * l, 10 * l,
            fill=couleur, bord=INK, trait=2)
    t.disque((cx + 26 * l, cy - 14 * l), 11 * l, fill=couleur, bord=INK, trait=2)
    t.poly([(cx + 20 * l, cy - 22 * l), (cx + 26 * l, cy - 32 * l),
            (cx + 30 * l, cy - 20 * l)], fill=couleur, bord=INK, trait=1.6)
    for dx in (-22, -8, 6, 14):
        t.ligne([(cx + dx * l, cy + 12 * l), (cx + dx * l, cy + 32 * l)], INK, 2.4 * l)
    if queue:
        t.ligne([(cx - 28 * l, cy - 6 * l), (cx - 40 * l, cy - 20 * l)], INK, 2.2 * l)
    if cornes:
        for d in (-1, 1):
            t.ligne([(cx + 24 * l, cy - 22 * l), (cx + (24 + d * 9) * l, cy - 34 * l)],
                    INK, 2.4 * l)


def oiseau(t, cx, cy, l=1.0):
    t.d.ellipse([int((cx - 22 * l) * S), int((cy - 10 * l) * S),
                 int((cx + 16 * l) * S), int((cy + 12 * l) * S)],
                fill=SKY, outline=INK, width=int(2 * S))
    t.disque((cx + 20 * l, cy - 12 * l), 9 * l, fill=SKY, bord=INK, trait=2)
    t.poly([(cx + 28 * l, cy - 12 * l), (cx + 40 * l, cy - 8 * l),
            (cx + 28 * l, cy - 5 * l)], fill=GOLD, bord=INK, trait=1.5)
    t.poly([(cx - 10 * l, cy - 6 * l), (cx - 2 * l, cy - 30 * l),
            (cx + 12 * l, cy - 4 * l)], fill=(150, 186, 216), bord=INK, trait=1.8)
    t.poly([(cx - 22 * l, cy + 2 * l), (cx - 40 * l, cy - 6 * l),
            (cx - 38 * l, cy + 12 * l)], fill=SKY, bord=INK, trait=1.8)


def lapin(t, cx, cy, l=1.0):
    t.d.ellipse([int((cx - 24 * l) * S), int((cy - 8 * l) * S),
                 int((cx + 12 * l) * S), int((cy + 16 * l) * S)],
                fill=SAND, outline=INK, width=int(2 * S))
    t.disque((cx + 18 * l, cy - 10 * l), 11 * l, fill=SAND, bord=INK, trait=2)
    for d in (-1, 1):
        t.d.ellipse([int((cx + (14 + d * 7) * l) * S), int((cy - 38 * l) * S),
                     int((cx + (20 + d * 7) * l) * S), int((cy - 16 * l) * S)],
                    fill=SAND, outline=INK, width=int(1.8 * S))
    t.ligne([(cx - 10 * l, cy + 14 * l), (cx - 2 * l, cy + 28 * l)], INK, 2.4 * l)
    t.ligne([(cx + 6 * l, cy + 14 * l), (cx + 12 * l, cy + 28 * l)], INK, 2.4 * l)
    t.disque((cx - 26 * l, cy + 2 * l), 6 * l, fill=WHITE_WARM, bord=INK, trait=1.6)


def serpent(t, cx, cy, l=1.0):
    pts = []
    for k in range(25):
        u = k / 24
        pts.append((cx - 40 * l + 80 * l * u, cy + math.sin(u * math.pi * 2.2) * 16 * l))
    t.ligne(pts, VERT, 7 * l)
    t.disque(pts[-1], 7 * l, fill=VERT, bord=INK, trait=1.6)
    t.ligne([pts[-1], (pts[-1][0] + 12 * l, pts[-1][1])], ROUGE, 2)


def escargot(t, cx, cy, l=1.0):
    t.poly([(cx - 30 * l, cy + 14 * l), (cx + 24 * l, cy + 14 * l),
            (cx + 20 * l, cy + 22 * l), (cx - 30 * l, cy + 22 * l)],
           fill=SAND, bord=INK, trait=2)
    pts = []
    for k in range(34):
        a = k / 33 * math.pi * 3.4
        r = (4 + k * 0.62) * l
        pts.append((cx + math.cos(a) * r, cy + 2 * l + math.sin(a) * r))
    t.ligne(pts, CLAY, 4.4 * l)
    for d in (0, 7):
        t.ligne([(cx - 28 * l, cy + 12 * l), (cx - (34 + d) * l, cy - 2 * l)], INK, 1.8)


def grenouille(t, cx, cy, l=1.0):
    t.d.ellipse([int((cx - 22 * l) * S), int((cy - 10 * l) * S),
                 int((cx + 22 * l) * S), int((cy + 18 * l) * S)],
                fill=VERT, outline=INK, width=int(2 * S))
    for d in (-1, 1):
        t.disque((cx + d * 11 * l, cy - 14 * l), 8 * l, fill=VERT, bord=INK, trait=1.8)
        t.disque((cx + d * 11 * l, cy - 15 * l), 3 * l, fill=INK)
        t.poly([(cx + d * 20 * l, cy + 8 * l), (cx + d * 34 * l, cy + 2 * l),
                (cx + d * 30 * l, cy + 20 * l)], fill=VERT, bord=INK, trait=1.8)


def viande(t, cx, cy, l=1.0):
    t.d.ellipse([int((cx - 24 * l) * S), int((cy - 16 * l) * S),
                 int((cx + 16 * l) * S), int((cy + 16 * l) * S)],
                fill=(198, 110, 98), outline=INK, width=int(2 * S))
    t.rrect(cx + 10 * l, cy - 6 * l, cx + 34 * l, cy + 4 * l, 4 * l,
            fill=WHITE_WARM, bord=INK, trait=1.8)


def jarre(t, cx, cy, l=1.0):
    t.poly([(cx - 20 * l, cy - 18 * l), (cx + 20 * l, cy - 18 * l),
            (cx + 26 * l, cy + 10 * l), (cx + 16 * l, cy + 32 * l),
            (cx - 16 * l, cy + 32 * l), (cx - 26 * l, cy + 10 * l)],
           fill=CLAY, bord=INK, trait=2)
    t.rrect(cx - 24 * l, cy - 26 * l, cx + 24 * l, cy - 16 * l, 4 * l,
            fill=TERRE, bord=INK, trait=2)
    for dx in (-10, 2, 12):
        t.d.arc([int((cx + dx * l - 5 * l) * S), int((cy - 44 * l) * S),
                 int((cx + dx * l + 5 * l) * S), int((cy - 30 * l) * S)],
                160, 380, fill=INK_2, width=int(1.8 * S))


def enfoui(t, cx, cy, l=1.0):
    """Enfouir dans la terre : la coupe du sol et ce qu-on y a mis."""
    t.rrect(cx - 68 * l, cy - 6 * l, cx + 68 * l, cy + 40 * l, 5,
            fill=TERRE, bord=INK, trait=2)
    t.d.ellipse([int((cx - 30 * l) * S), int((cy + 2 * l) * S),
                 int((cx + 30 * l) * S), int((cy + 34 * l) * S)],
                fill=(104, 84, 64), outline=INK, width=int(2 * S))
    for dx, dy in ((-12, 14), (6, 12), (-2, 24)):
        t.d.ellipse([int((cx + dx * l - 7 * l) * S), int((cy + dy * l - 5 * l) * S),
                     int((cx + dx * l + 7 * l) * S), int((cy + dy * l + 5 * l) * S)],
                    fill=SAND, outline=INK, width=int(1.5 * S))


# --------------------------------------------------------------------------
# Les fabriques

def _fab_liste(items, titre):
    def f(t):
        _liste(t, items, titre)
    return f


def _fab_scene(dessin, note=None, y=268):
    def f(t):
        dessin(t)
        if note:
            _note(t, note, y)
    return f


def _fab_grille(items, vif=None):
    def f(t):
        _grille(t, items, vif=vif)
    return f


def _fab_duo(g, d, note=None):
    def f(t):
        _vignette(t, 86, 132, g[0], g[1], 122)
        _vignette(t, 234, 132, d[0], d[1], 122)
        if note:
            _note(t, note, 240)
    return f


def _fab_regime(animal, aliment, nom, phrase):
    """Un animal, ce qu-il mange, et le nom de son régime."""
    def f(t):
        animal(t, 100, 112)
        fb._fleche(t, (156, 118), (196, 118), CLAY, 2.6)
        aliment(t, 244, 112)
        _pastille(t, 160, 190, nom, 20, fond=GOLD, marge=18)
        _note(t, phrase, 240, 15, INK)
    return f


def _fab_mode(animal, nom, exemples):
    def f(t):
        animal(t, 160, 116)
        _pastille(t, 160, 190, nom, 20, fond=MINT, marge=18)
        _note(t, exemples, 240, 15)
    return f


# --------------------------------------------------------------------------
# Les scènes

def _sc_vent_def(t):
    souffle(t, 108, 140, 3, 1.3)
    arbre(t, 236, 130, 1.0)
    _note(t, 'le vent, c-est l-air en mouvement', 232, 15, INK)
    _note(t, 'on ne le voit pas, on voit ce qu-il bouge', 262, 13)


def _sc_combustion(t):
    feu(t, 160, 150, 1.4)
    _note(t, 'un corps se decompose par l-action du feu', 236, 14, INK)


def _sc_prudence(t):
    feu(t, 160, 146, 1.1)
    for d in (-1, 1):
        t.ligne([(160 + d * 64, 108), (160 + d * 92, 92)], ROUGE, 3)
    t.disque((160, 212), 17, fill=ROUGE, bord=INK, trait=2)
    t.ligne([(150, 212), (170, 212)], WHITE_WARM, 4)
    _note(t, 'on ne joue jamais avec le feu', 254, 15, INK)


# --- Couvertures ----------------------------------------------------------

def couv_vent(t):
    _bandeau_couv(t, 'Le vent')
    souffle(t, 356, 300, 3, 1.1)
    moulin(t, 470, 290, 1.0)
    voilier(t, 578, 294, 1.0)


def couv_conservation(t):
    _bandeau_couv(t, 'Conserver les récoltes')
    soleil(t, 374, 288)
    frigo(t, 452, 296)
    jarre(t, 528, 292)
    enfoui(t, 614, 288)


def couv_locomotion(t):
    _bandeau_couv(t, 'Se déplacer')
    quadrupede(t, 368, 300, 0.95)
    lapin(t, 460, 296, 0.95)
    oiseau(t, 548, 292, 0.95)
    serpent(t, 630, 300, 0.85)


def couv_nutrition(t):
    _bandeau_couv(t, 'Ce que mangent les animaux')
    quadrupede(t, 380, 300, 0.95, cornes=True)
    herbe(t, 458, 290, 5)
    viande(t, 544, 292)
    serpent(t, 628, 296, 0.8)


def couv_combustion(t):
    _bandeau_couv(t, 'La combustion')
    feu(t, 480, 300, 1.3)


FIGURES = [
    # ---- 42. Le vent --------------------------------------------------------
    ('kv-ve-couv', 960, 540, couv_vent),
    ('kv-ve-def', 320, 320, _fab_scene(_sc_vent_def)),
    ('kv-ve-objets', 320, 320, _fab_grille([
        (lambda t, x, y: moulin(t, x, y, 0.82), 'le moulin'),
        (lambda t, x, y: montgolfiere(t, x, y, 0.82), 'la montgolfière'),
        (lambda t, x, y: cerf_volant(t, x, y, 0.82), 'le cerf-volant'),
        (lambda t, x, y: voilier(t, x, y, 0.82), 'le bateau à voile')])),
    ('kv-ve-moulin', 320, 320, _fab_scene(
        lambda t: (moulin(t, 196, 140, 1.5), souffle(t, 74, 130, 3, 1.1)),
        'le vent fait tourner les ailes du moulin', 254)),
    ('kv-ve-voile', 320, 320, _fab_scene(
        lambda t: (voilier(t, 190, 140, 1.5), souffle(t, 72, 124, 3, 1.0)),
        'le vent pousse la voile, et le bateau avance', 254)),
    ('kv-ve-mesure', 320, 320, _fab_duo(
        (lambda t, x, y: girouette(t, x, y, 0.82), 'la girouette'),
        (lambda t, x, y: anemometre(t, x, y, 0.82), 'l-anémomètre'),
        'la direction, puis la vitesse du vent')),
    ('kv-ve-parachute', 320, 320, _fab_duo(
        (lambda t, x, y: parachute(t, x, y, 0.82), 'le parachute'),
        (lambda t, x, y: montgolfiere(t, x, y, 0.82), 'la montgolfière'),
        'tous deux portés par l-air')),

    # ---- 43. La conservation des produits agricoles -------------------------
    ('kv-cp-couv', 960, 540, couv_conservation),
    ('kv-cp-liste', 320, 380, _fab_liste(
        ['La congélation', 'Le séchage et le fumage', 'L-embouteillage et le salage',
         'La fermentation', 'Enfouir dans la terre'], 'Conserver les récoltes')),
    ('kv-cp-froid', 320, 320, _fab_scene(
        lambda t: frigo(t, 160, 140), 'la congélation garde au froid', 236)),
    ('kv-cp-sechage', 320, 320, _fab_duo(
        (lambda t, x, y: soleil(t, x, y), 'le séchage'),
        (lambda t, x, y: fumee(t, x, y - 6), 'le fumage'),
        'tous deux enlèvent l-eau')),
    ('kv-cp-salage', 320, 320, _fab_duo(
        (lambda t, x, y: bouteille(t, x, y), 'l-embouteillage'),
        (lambda t, x, y: sel(t, x, y), 'le salage'),
        'on met à l-abri de l-air')),
    ('kv-cp-terre', 320, 320, _fab_duo(
        (lambda t, x, y: jarre(t, x, y, 0.9), 'la fermentation'),
        (lambda t, x, y: enfoui(t, x, y, 0.62), 'enfouir dans la terre'),
        'deux façons anciennes, et qui marchent')),

    # ---- 44. Les modes de locomotion ----------------------------------------
    ('kv-lo-couv', 960, 540, couv_locomotion),
    ('kv-lo-def', 320, 320, _fab_grille([
        (lambda t, x, y: quadrupede(t, x, y, 0.82), 'la marche'),
        (lambda t, x, y: lapin(t, x, y, 0.82), 'le saut'),
        (lambda t, x, y: oiseau(t, x, y, 0.82), 'le vol'),
        (lambda t, x, y: poisson(t, x, y), 'la nage')])),
    ('kv-lo-marche', 320, 320, _fab_mode(
        lambda t, x, y: quadrupede(t, x, y, 1.3), 'la marche', 'le chien, le chat')),
    ('kv-lo-saut', 320, 320, _fab_mode(
        lambda t, x, y: lapin(t, x, y, 1.3), 'le saut', 'le lapin, la grenouille')),
    ('kv-lo-vol', 320, 320, _fab_mode(
        lambda t, x, y: oiseau(t, x, y, 1.3), 'le vol', 'les oiseaux, les insectes')),
    ('kv-lo-nage', 320, 320, _fab_mode(
        lambda t, x, y: poisson(t, x, y), 'la nage', 'les poissons, l-étoile de mer')),
    ('kv-lo-rampement', 320, 320, _fab_mode(
        lambda t, x, y: serpent(t, x, y, 1.1), 'le rampement',
        'le serpent, le ver de terre, l-escargot')),

    # ---- 45. La nutrition chez les animaux ----------------------------------
    ('kv-nu-couv', 960, 540, couv_nutrition),
    # Trois regimes montres par ce qu-ils MANGENT, pas par la couleur de
    # l-animal. La premiere version alignait le meme quadrupede en trois
    # teintes : trois cases identiques, qui n-apprenaient rien et qui
    # contredisaient la regle posee en tete de ce fichier.
    ('kv-nu-def', 320, 320, _fab_grille([
        (lambda t, x, y: herbe(t, x, y, 5), 'herbivore'),
        (lambda t, x, y: viande(t, x, y), 'carnivore'),
        (lambda t, x, y: (herbe(t, x - 24, y, 3), viande(t, x + 26, y, 0.8)), 'omnivore')])),
    ('kv-nu-herbivore', 320, 320, _fab_regime(
        lambda t, x, y: quadrupede(t, x, y, 0.95, cornes=True),
        lambda t, x, y: herbe(t, x, y, 5), 'herbivore',
        'la chèvre, le mouton, la vache')),
    ('kv-nu-carnivore', 320, 320, _fab_regime(
        lambda t, x, y: quadrupede(t, x, y, 0.95, couleur=(214, 176, 132)),
        lambda t, x, y: viande(t, x, y), 'carnivore',
        'le chien, le chat, le lion')),
    ('kv-nu-omnivore', 320, 320, _fab_scene(
        lambda t: (quadrupede(t, 160, 104, 0.95, couleur=(206, 186, 196)),
                   herbe(t, 104, 176, 4), viande(t, 214, 172),
                   _pastille(t, 160, 230, 'omnivore', 20, fond=GOLD, marge=18)),
        'le porc, le canard, l-ours : ils mangent tout', 274)),

    # ---- 46. La combustion ---------------------------------------------------
    ('kv-co-couv', 960, 540, couv_combustion),
    ('kv-co-def', 320, 320, _fab_scene(_sc_combustion)),
    ('kv-co-combustibles', 320, 320, _fab_grille([
        (lambda t, x, y: feuille(t, x, y, 0.8, SAND), 'le papier'),
        (lambda t, x, y: arbre(t, x, y - 8, 0.82), 'le bois'),
        (lambda t, x, y: bouteille(t, x, y, GOLD), 'l-essence'),
        (lambda t, x, y: boite(t, x, y), 'le pétrole')])),
    ('kv-co-incombustibles', 320, 320, _fab_duo(
        (lambda t, x, y: fk.verre_eau(t, x, y), 'l-eau'),
        (lambda t, x, y: fg.beche(t, x, y), 'le fer'),
        'ceux-là ne brûlent pas')),
    ('kv-co-prudence', 320, 320, _fab_scene(_sc_prudence, None)),
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
