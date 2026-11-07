# -*- coding: utf-8 -*-
"""
Les figures des sept leçons d-éducation à l-environnement de BRAYNE (CM1)
— cahier « Sciences / Health / En. Educ » du 15 octobre au 5 novembre 2026.

CE QUE CES LEÇONS DEMANDENT D-UNE IMAGE

Elles ne parlent pas d-objets qu-on nomme, comme les outils de KLEIN,
mais de CHAÎNES : une cause produit un effet, un déchet devient une
ressource, une dispute se dénoue. Une vignette isolée ne montre pas une
chaîne. Le module est donc bâti sur trois instruments de liaison :

  _chaine    deux ou trois cases reliées par des flèches. C-est la forme
             de « déchet → transformation → matière utile » et de
             « cause → pollution → effet »
  _deux_tas  ce qui se décompose à gauche, ce qui ne se décompose pas à
             droite. La leçon sur les déchets tient tout entière là
  _liste     la liste numérotée du cahier, reprise telle quelle : c-est
             sous cette forme que la maîtresse interroge

Et une exception, qui vaut qu-on la dessine pour elle-même : le SCHÉMA
DE LA PLANTE. Le cahier en porte un, annoté de sa main ; la question
d-examen est de replacer les étiquettes. Une image qui montrerait autre
chose que ce schéma-là entraînerait à autre chose que l-examen.

Les pictogrammes d-aliments, de cuisson et de conservation ne sont pas
redessinés : ils viennent de figures-klein-maison-nov.py. Un instrument
se corrige une fois.

Usage :  python work/figures-brayne-env-nov.py
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
FUMEE = (150, 150, 152)
GRIS = (176, 176, 178)

_mesure = fa._mesure
_pastille = fa._pastille
_taille_tenant = fa._taille_tenant
_liste = fa._liste
_bandeau_couv = fa._bandeau_couv
_vignette = fg._vignette
_grille = fg._grille
champ, tas, herbe, pousse, personne = fg.champ, fg.tas, fg.herbe, fg.pousse, fg.personne
BANDEAU = fa.BANDEAU


# --------------------------------------------------------------------------
# Les pictogrammes propres à ces leçons

def usine(t, cx, cy, l=1.0):
    t.rrect(cx - 40 * l, cy - 6 * l, cx + 40 * l, cy + 34 * l, 4, fill=GRIS, bord=INK, trait=2)
    t.rrect(cx + 12 * l, cy - 40 * l, cx + 28 * l, cy - 2 * l, 3, fill=GRIS, bord=INK, trait=2)
    for k in range(3):
        x = cx - 30 * l + k * 20 * l
        t.rrect(x - 6 * l, cy + 6 * l, x + 6 * l, cy + 18 * l, 2, fill=SKY, bord=INK, trait=1.4)


def voiture(t, cx, cy, l=1.0):
    t.rrect(cx - 34 * l, cy - 2 * l, cx + 34 * l, cy + 16 * l, 6, fill=CLAY, bord=INK, trait=2)
    t.poly([(cx - 20 * l, cy - 2 * l), (cx - 12 * l, cy - 20 * l), (cx + 14 * l, cy - 20 * l),
            (cx + 22 * l, cy - 2 * l)], fill=SKY, bord=INK, trait=2)
    for dx in (-20, 20):
        t.disque((cx + dx * l, cy + 18 * l), 8 * l, fill=INK_2, bord=INK, trait=1.6)


def bouffee(t, cx, cy, n=3, l=1.0, couleur=FUMEE):
    """La fumée qui sort : trois boules de plus en plus hautes et pâles."""
    for k in range(n):
        r = (9 + k * 4) * l
        t.disque((cx + k * 13 * l, cy - k * 15 * l), r, fill=couleur, bord=INK, trait=1.6)


def oeil(t, cx, cy):
    t.poly([(cx - 26, cy), (cx - 10, cy - 15), (cx + 10, cy - 15), (cx + 26, cy),
            (cx + 10, cy + 15), (cx - 10, cy + 15)], fill=WHITE_WARM, bord=INK, trait=2)
    t.disque((cx, cy), 9, fill=SKY, bord=INK, trait=1.8)
    t.disque((cx, cy), 4, fill=INK)
    for d in (-1, 1):
        t.ligne([(cx + d * 30, cy - 8), (cx + d * 40, cy - 14)], ROUGE, 2.4)


def nuage(t, cx, cy, l=1.0, couleur=GRIS, pluie=False):
    for dx, dy, r in ((-20, 2, 15), (0, -6, 19), (20, 2, 15)):
        t.disque((cx + dx * l, cy + dy * l), r * l, fill=couleur, bord=INK, trait=1.8)
    t.rrect(cx - 30 * l, cy - 2 * l, cx + 30 * l, cy + 14 * l, 8 * l,
            fill=couleur, bord=INK, trait=1.8)
    if pluie:
        for k in range(5):
            x = cx - 24 * l + k * 12 * l
            t.ligne([(x, cy + 22 * l), (x - 4 * l, cy + 40 * l)], BLEU, 2.4)


def ozone(t, cx, cy, trou=True):
    """La couche d-ozone, et le trou par lequel le soleil frappe."""
    t.d.arc([int((cx - 76) * S), int((cy - 30) * S), int((cx + 76) * S), int((cy + 46) * S)],
            200, 340, fill=SKY, width=int(9 * S))
    if trou:
        t.d.arc([int((cx - 76) * S), int((cy - 30) * S), int((cx + 76) * S), int((cy + 46) * S)],
                258, 282, fill=(246, 230, 201), width=int(11 * S))
        for k in range(3):
            t.ligne([(cx - 8 + k * 8, cy - 8), (cx - 14 + k * 8, cy + 34)], GOLD, 2.6)
    t.disque((cx, cy - 56), 17, fill=GOLD, bord=INK, trait=2)


def poubelle(t, cx, cy, couleur=VERT, l=1.0):
    t.poly([(cx - 22 * l, cy - 14 * l), (cx + 22 * l, cy - 14 * l), (cx + 17 * l, cy + 30 * l),
            (cx - 17 * l, cy + 30 * l)], fill=couleur, bord=INK, trait=2)
    t.rrect(cx - 27 * l, cy - 24 * l, cx + 27 * l, cy - 13 * l, 4, fill=couleur,
            bord=INK, trait=2)
    t.rrect(cx - 6 * l, cy - 31 * l, cx + 6 * l, cy - 24 * l, 3, fill=couleur, bord=INK, trait=1.6)


def fosse(t, cx, cy):
    """La fosse à ordures : un trou dans le sol, des déchets dedans."""
    t.rrect(cx - 72, cy, cx + 72, cy + 34, 4, fill=TERRE, bord=INK, trait=2)
    t.poly([(cx - 34, cy), (cx + 34, cy), (cx + 24, cy + 32), (cx - 24, cy + 32)],
           fill=(96, 78, 60), bord=INK, trait=2)
    for dx, dy, c in ((-14, 10, SKY), (6, 8, CLAY), (-2, 20, GOLD)):
        t.disque((cx + dx, cy + dy), 7, fill=c, bord=INK, trait=1.4)


def incinerateur(t, cx, cy):
    t.rrect(cx - 30, cy - 10, cx + 30, cy + 34, 5, fill=GRIS, bord=INK, trait=2)
    t.rrect(cx - 10, cy - 44, cx + 10, cy - 6, 3, fill=GRIS, bord=INK, trait=2)
    fg.__dict__  # noqa: B018  (garde le module chargé lisible dans la trace)
    t.poly([(cx - 14, cy + 30), (cx - 6, cy + 10), (cx, cy + 22), (cx + 6, cy + 6),
            (cx + 14, cy + 30)], fill=(226, 136, 58), bord=INK, trait=1.8)
    bouffee(t, cx + 2, cy - 54, 2, 0.6)


def sac(t, cx, cy, couleur=(96, 108, 118)):
    t.poly([(cx - 24, cy - 12), (cx + 24, cy - 12), (cx + 19, cy + 32), (cx - 19, cy + 32)],
           fill=couleur, bord=INK, trait=2)
    t.d.arc([int((cx - 20) * S), int((cy - 28) * S), int((cx + 20) * S), int((cy + 2) * S)],
            190, 350, fill=INK, width=int(2.4 * S))


def latrine(t, cx, cy):
    """La cuvette des toilettes à l-eau, de profil."""
    t.rrect(cx - 10, cy - 42, cx + 26, cy - 8, 5, fill=WHITE_WARM, bord=INK, trait=2)
    t.d.ellipse([int((cx - 30) * S), int((cy - 14) * S), int((cx + 22) * S), int((cy + 10) * S)],
                fill=WHITE_WARM, outline=INK, width=int(2 * S))
    t.d.ellipse([int((cx - 23) * S), int((cy - 8) * S), int((cx + 15) * S), int((cy + 4) * S)],
                fill=SKY, outline=INK, width=int(1.6 * S))
    t.poly([(cx - 20, cy + 8), (cx + 10, cy + 8), (cx + 6, cy + 34), (cx - 14, cy + 34)],
           fill=WHITE_WARM, bord=INK, trait=2)


def dispute(t, cx, cy):
    """Deux personnes face à face, et l-éclair du désaccord entre elles."""
    personne(t, cx - 46, cy)
    personne(t, cx + 46, cy)
    t.poly([(cx - 7, cy - 44), (cx + 7, cy - 44), (cx + 1, cy - 28), (cx + 11, cy - 28),
            (cx - 5, cy - 2), (cx, cy - 22), (cx - 9, cy - 22)],
           fill=ROUGE, bord=INK, trait=1.8)


def entente(t, cx, cy):
    """Les deux mêmes, et la poignée de main à la place de l-éclair."""
    personne(t, cx - 46, cy)
    personne(t, cx + 46, cy)
    t.rrect(cx - 22, cy - 6, cx + 22, cy + 6, 6, fill=SAND, bord=INK, trait=2)
    t.disque((cx, cy), 10, fill=SAND, bord=INK, trait=2)
    t.texte((cx, cy - 36), 'ok', 17, VERT)


def feuille(t, cx, cy, l=1.0, couleur=VERT, angle=0.0):
    """Une feuille : deux arcs qui se rejoignent en pointe aux deux bouts.

    Le losange de la premiere version se lisait comme un cerf-volant. La
    forme est donc construite point par point : la largeur suit un sinus
    le long de la nervure, ce qui donne le renflement du milieu et les
    deux pointes.
    """
    pts_h, pts_b = [], []
    for k in range(13):
        u = k / 12
        x = (-30 + 60 * u) * l
        e = math.sin(math.pi * u) * 15 * l
        pts_h.append((x, -e))
        pts_b.append((x, e))
    ca, sa = math.cos(angle), math.sin(angle)
    tourne = lambda q: [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in q]
    t.poly(tourne(pts_h + pts_b[::-1]), fill=couleur, bord=INK, trait=1.8)
    t.ligne(tourne([(-28 * l, 0), (28 * l, 0)]), (86, 122, 74), max(1.4, 1.8 * l))


def arbre(t, cx, cy, l=1.0):
    """Un arbre a la taille d-une vignette.

    Le schema complet de la plante fait 240 de large : il est fait pour
    etre lu, pas pour tenir dans une carte de 130. Un arbre dessine a sa
    taille dit « grande plante a tige ligneuse » aussi bien.
    """
    t.rrect(cx - 6 * l, cy - 4 * l, cx + 6 * l, cy + 38 * l, 3, fill=BOIS, bord=INK, trait=2)
    for cote in (-1, 1):
        t.ligne([(cx, cy + 12 * l), (cx + cote * 15 * l, cy - 2 * l)], BOIS, 2.6)
    for dx, dy, r in ((-18, -2, 17), (18, -2, 17), (0, -22, 21)):
        t.disque((cx + dx * l, cy + dy * l), r * l, fill=VERT, bord=INK, trait=2)


def arbuste(t, cx, cy, l=1.0):
    """Un arbuste : des tiges ligneuses courtes, et pas de tronc.

    La premiere version le montrait par une feuille — ce qui disait
    « plante », pas « arbuste ». Or la lecon les distingue justement par
    la tige : molle pour les herbes, ligneuse pour les arbustes. C-est
    donc la tige qu-il faut voir.
    """
    for cote in (-1, 0, 1):
        t.ligne([(cx, cy + 30 * l), (cx + cote * 16 * l, cy + 2 * l)], BOIS, 3.4 * l)
    for dx, dy, r in ((-17, 0, 14), (17, 0, 14), (0, -14, 16)):
        t.disque((cx + dx * l, cy + dy * l), r * l, fill=VERT, bord=INK, trait=2)
    t.rrect(cx - 20 * l, cy + 28 * l, cx + 20 * l, cy + 36 * l, 3, fill=TERRE,
            bord=INK, trait=1.6)


def nodosites(t, cx, cy):
    """Une racine et ses nodosités : c-est par là que l-azote entre."""
    t.ligne([(cx, cy - 32), (cx, cy + 10)], VERT, 3)
    for dx, dy in ((-26, 30), (0, 36), (26, 30)):
        t.ligne([(cx, cy + 8), (cx + dx, cy + dy)], (138, 102, 72), 2.6)
        t.disque((cx + dx * 0.78, cy + dy * 0.8), 6.5, fill=MINT, bord=INK, trait=1.5)
    t.disque((cx - 12, cy + 24), 5.5, fill=MINT, bord=INK, trait=1.5)
    t.disque((cx + 13, cy + 25), 5.5, fill=MINT, bord=INK, trait=1.5)


# --------------------------------------------------------------------------
# Le schéma de la plante, celui que le cahier porte annoté

def schema_plante(t, cx, cy, etiquettes=True, vise=None, echelle=1.0):
    """La plante entiere, annotee comme au tableau.

    Trois regles apprises en la ratant une premiere fois :

    - les etiquettes se posent EN DEHORS du dessin, reliees par une
      amorce. Posees dessus, « fruit » tombait sur une feuille et
      « roots » se perdait dans la couleur de la terre ;
    - la terre est une bande claire, pas un bloc brun : les racines
      doivent se voir dedans, c-est tout l-interet de la couper ;
    - l-ordre de trace va du fond vers l-avant, sinon la tige deborde
      sous la ligne de terre.
    """
    e = echelle
    sol = cy + 58 * e

    # la terre, claire, pour que les racines s-y lisent
    t.rrect(cx - 120 * e, sol, cx + 120 * e, sol + 46 * e, 5, fill=SAND, bord=INK, trait=2)
    for ecart, prof in ((-1, 1.0), (1, 1.0), (-1, 0.58), (1, 0.58)):
        t.ligne([(cx, sol + 2 * e), (cx + ecart * 46 * prof * e, sol + 38 * prof * e)],
                (138, 102, 72), 3 * e)
    t.ligne([(cx, sol + 2 * e), (cx, sol + 42 * e)], (138, 102, 72), 3.4 * e)

    # la tige, puis ce qui s-y accroche
    t.ligne([(cx, sol), (cx, cy - 52 * e)], VERT, 5.5 * e)
    for cote, y in ((-1, cy + 10 * e), (1, cy - 18 * e)):
        t.ligne([(cx, y), (cx + cote * 40 * e, y - 20 * e)], VERT, 3.4 * e)
        feuille(t, cx + cote * 66 * e, y - 28 * e, 0.6 * e, angle=-cote * 0.42)
    feuille(t, cx - 52 * e, cy + 44 * e, 0.52 * e, angle=0.5)

    t.disque((cx + 40 * e, cy - 40 * e), 11 * e, fill=ROUGE, bord=INK, trait=1.8)
    for k in range(6):
        a = math.pi * 2 * k / 6
        t.disque((cx - 40 * e + math.cos(a) * 11 * e, cy - 34 * e + math.sin(a) * 11 * e),
                 6.5 * e, fill=GOLD, bord=INK, trait=1.5)
    t.disque((cx - 40 * e, cy - 34 * e), 5.5 * e, fill=CLAY, bord=INK, trait=1.5)
    t.poly([(cx, cy - 52 * e), (cx - 9 * e, cy - 70 * e), (cx + 9 * e, cy - 70 * e)],
           fill=MINT, bord=INK, trait=1.8)

    if not etiquettes:
        return

    # (nom, point vise, cote) — le texte va au bord, l-amorce fait le lien
    pose = [
        ('terminal bud', (cx + 6 * e, cy - 66 * e), 'd'),
        ('fruit', (cx + 48 * e, cy - 40 * e), 'd'),
        ('leaf', (cx + 66 * e, cy - 46 * e), 'd'),
        ('flower', (cx - 48 * e, cy - 34 * e), 'g'),
        ('branch', (cx - 24 * e, cy + 2 * e), 'g'),
        ('stem', (cx - 4 * e, cy + 34 * e), 'g'),
        ('roots', (cx - 26 * e, sol + 26 * e), 'g'),
    ]
    rangs_d, rangs_g = [], []
    for nom, cible, cote in pose:
        (rangs_d if cote == 'd' else rangs_g).append((nom, cible))

    for cote, rangs in (('d', rangs_d), ('g', rangs_g)):
        bord = cx + 150 * e if cote == 'd' else cx - 150 * e
        hauts = [cy - 72 * e + i * 32 * e for i in range(len(rangs))]
        if cote == 'g':
            hauts = [cy - 40 * e + i * 36 * e for i in range(len(rangs))]
        for (nom, (bx, by)), y in zip(rangs, hauts):
            vif = nom == vise
            couleur = ROUGE if vif else INK_2
            t.ligne([(bx, by), (bord, y)], couleur, 1.6 * e)
            t.disque((bx, by), 2.6 * e, fill=couleur)
            t.texte((bord + (4 if cote == 'd' else -4) * e, y), nom, 13 * e, couleur,
                    'lm' if cote == 'd' else 'rm')


# --------------------------------------------------------------------------
# Les instruments de liaison

def _fleche(t, a, b, couleur=CLAY, trait=3):
    t.ligne([a, b], couleur, trait)
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = max(1e-6, (dx * dx + dy * dy) ** 0.5)
    ux, uy = dx / n, dy / n
    for s in (-1, 1):
        t.ligne([b, (b[0] - ux * 11 + s * uy * 7, b[1] - uy * 11 - s * ux * 7)], couleur, trait)


def _chaine(t, cases, haut=96, cote=86, note=None):
    """Deux ou trois cases reliées par des flèches : la chaîne de la leçon."""
    n = len(cases)
    largeur = 320 - 24
    pas = largeur / n
    for i, (dessin, nom) in enumerate(cases):
        cx = 12 + pas * (i + 0.5)
        t.rrect(cx - cote / 2, haut - cote / 2, cx + cote / 2, haut + cote / 2, 10,
                fill=WHITE_WARM, bord=INK, trait=2)
        dessin(t, cx, haut - 4)
        taille = _taille_tenant(t, [nom], cote + 10, 13)
        t.texte((cx, haut + cote / 2 + 15), nom, taille, INK)
        if i:
            _fleche(t, (cx - pas + cote / 2 + 5, haut), (cx - cote / 2 - 5, haut))
    if note:
        _note(t, note, haut + cote / 2 + 48)


def _deux_tas(t, gauche, droite, titres=('organic', 'inorganic'), note=None):
    """Ce qui se décompose / ce qui ne se décompose pas."""
    for i, (items, titre, couleur) in enumerate(
            ((gauche, titres[0], VERT), (droite, titres[1], (96, 108, 118)))):
        cx = 84 + i * 152
        t.texte((cx, 66), titre, 16, INK)
        poubelle(t, cx, 112, couleur, 1.05)
        for k, mot in enumerate(items):
            _pastille(t, cx, 176 + k * 30, mot, 13, fond=WHITE_WARM, marge=9)
    if note:
        _note(t, note, 290, 13)


def _fab_liste(items, titre):
    def f(t):
        _liste(t, items, titre)
    return f


def _fab_chaine(cases, note=None):
    def f(t):
        _chaine(t, cases, note=note)
    return f


def _note(t, texte, y=268, taille=14, couleur=None, largeur=292):
    """Une legende qui tient toujours dans le cadre.

    Ecrite a taille fixe, une phrase un peu longue sortait des deux
    cotes a la fois — et le controle de bord signalait « le dessin
    touche le bord » sans dire que c-etait le texte. La taille descend
    donc jusqu-a ce que la phrase tienne.
    """
    t.texte((160, y), texte, _taille_tenant(t, [texte], largeur, taille),
            couleur if couleur else INK_2)


def _fab_scene(dessin, note=None, y=268):
    def f(t):
        dessin(t)
        if note:
            _note(t, note, y)
    return f


def _fab_vise(partie, note):
    """Le meme schema, une partie mise en rouge, et ce qu-elle fait."""
    def f(t):
        schema_plante(t, 240, 126, vise=partie)
        t.texte((240, 300), note, _taille_tenant(t, [note], 440, 14), INK_2)
    return f


def _fab_grille(items, vif=None):
    def f(t):
        _grille(t, items, vif=vif)
    return f


# --------------------------------------------------------------------------
# Les scènes

def _sc_air_def(t):
    usine(t, 112, 170)
    bouffee(t, 138, 128, 3)
    voiture(t, 228, 196)
    bouffee(t, 256, 172, 2, 0.7)


def _sc_air_ozone(t):
    ozone(t, 160, 160)


def _sc_air_oeil(t):
    oeil(t, 160, 128)
    nuage(t, 160, 216, 0.9, GRIS)


def _sc_pluie(t):
    nuage(t, 160, 110, 1.0, GRIS, pluie=True)
    champ(t, 160, 220, 180, 42)
    herbe(t, 112, 194, 3, (150, 160, 120))
    herbe(t, 208, 194, 3, (150, 160, 120))


def _sc_sol_def(t):
    champ(t, 160, 190, 200, 58)
    for dx, dy, c in ((-56, 168, SKY), (-8, 176, GRIS), (44, 166, CLAY)):
        t.disque((160 + dx, dy), 11, fill=c, bord=INK, trait=1.6)
    _note(t, 'poisonous substances in the soil', 248, 13)


def _sc_sol_feu(t):
    champ(t, 160, 212, 190, 44)
    for dx in (-54, 0, 54):
        fg.__dict__  # noqa: B018
    from_feu = _charger('figures_klein_maison', 'figures-klein-maison-nov.py')
    for dx in (-54, 0, 54):
        from_feu.feu(t, 160 + dx, 164, 0.7)
    bouffee(t, 178, 126, 2, 0.7)


def _sc_dechets_def(t):
    poubelle(t, 160, 150, (96, 108, 118), 1.5)
    _note(t, 'anything that is not useful', 232, 14)


def _sc_biogaz(t):
    t.rrect(44, 190, 276, 250, 5, fill=TERRE, bord=INK, trait=2)
    t.d.ellipse([int(104 * S), int(196 * S), int(216 * S), int(244 * S)],
                fill=(96, 78, 60), outline=INK, width=int(2 * S))
    t.rrect(150, 150, 170, 196, 3, fill=FER, bord=INK, trait=2)
    bouffee(t, 162, 140, 3, 0.7, MINT)
    _note(t, 'an enclosed pit, and the gas that comes out', 276, 13)


def _sc_plante_def(t):
    schema_plante(t, 160, 140, etiquettes=False)


def _sc_photo(t):
    t.disque((62, 86), 18, fill=GOLD, bord=INK, trait=2)
    for k in range(6):
        a = math.pi * 2 * k / 6
        t.ligne([(62 + math.cos(a) * 24, 86 + math.sin(a) * 24),
                 (62 + math.cos(a) * 34, 86 + math.sin(a) * 34)], GOLD, 2.6)
    feuille(t, 178, 134, 1.5)
    _fleche(t, (96, 100), (140, 124), GOLD, 2.6)
    t.texte((248, 92), 'CO2', 16, INK_2)
    _fleche(t, (240, 106), (212, 124), INK_2, 2.4)
    t.texte((62, 196), 'water', 15, BLEU)
    _fleche(t, (84, 188), (142, 158), BLEU, 2.6)
    _note(t, 'sunlight, carbon dioxide and water', 248, 13)
    _note(t, 'make food in the leaf', 276, 14, INK)


def _sc_nodosites(t):
    nodosites(t, 160, 140)
    _note(t, 'root nodules', 226, 14, INK)
    _note(t, 'they add nitrogen to the soil', 256, 13)


def _sc_schema(t):
    schema_plante(t, 240, 132)


def _sc_racine(t):
    t.rrect(32, 128, 288, 164, 4, fill=TERRE, bord=INK, trait=2)
    t.ligne([(160, 70), (160, 140)], VERT, 5)
    for ecart, prof in ((-1, 1.0), (1, 1.0), (-1, 0.55), (1, 0.55)):
        t.ligne([(160, 138), (160 + ecart * 46 * prof, 138 + 56 * prof)], (138, 102, 72), 2.8)
    t.ligne([(160, 138), (160, 200)], (138, 102, 72), 3.2)
    for dx, dy in ((-30, 174), (28, 176), (0, 192)):
        _fleche(t, (160 + dx, dy), (160 + dx * 0.3, 150), BLEU, 2.2)
    _note(t, 'water and minerals go up', 232, 14, INK)
    _note(t, 'through a process called osmosis', 260, 13)


def _sc_dispute(t):
    dispute(t, 160, 150)


def _sc_entente(t):
    entente(t, 160, 150)


# --- Couvertures ----------------------------------------------------------

def couv_air(t):
    _bandeau_couv(t, 'Air pollution')
    usine(t, 392, 310, 1.1)
    bouffee(t, 420, 266, 3, 1.0)
    voiture(t, 560, 318, 1.1)
    bouffee(t, 592, 292, 2, 0.8)


def couv_sol(t):
    _bandeau_couv(t, 'Soil pollution')
    champ(t, 480, 318, 230, 50)
    for dx, c in ((-70, SKY), (-16, GRIS), (46, CLAY)):
        t.disque((480 + dx, 290), 13, fill=c, bord=INK, trait=1.8)


def couv_dechets(t):
    _bandeau_couv(t, 'Waste and its disposal')
    poubelle(t, 396, 300, VERT, 1.3)
    poubelle(t, 480, 300, (96, 108, 118), 1.3)
    fosse(t, 586, 276)


def couv_recyclage(t):
    _bandeau_couv(t, 'Waste transformation')
    poubelle(t, 388, 300, (96, 108, 118), 1.2)
    _fleche(t, (432, 300), (512, 300), CLAY, 3.4)
    tas(t, 572, 288)


def couv_conflits(t):
    _bandeau_couv(t, 'Conflicts')
    dispute(t, 404, 300)
    _fleche(t, (486, 300), (538, 300), CLAY, 3)
    entente(t, 614, 300)


def couv_plantes(t):
    _bandeau_couv(t, 'Plants')
    schema_plante(t, 480, 254, etiquettes=False, echelle=0.9)


def couv_parties(t):
    _bandeau_couv(t, 'Parts of a plant')
    schema_plante(t, 400, 254, etiquettes=False, echelle=0.9)
    for k, nom in enumerate(('bud', 'leaf', 'stem', 'root')):
        t.texte((612, 220 + k * 34), nom, 19, INK_2, 'lm')


FIGURES = [
    # ---- 36. Air pollution ------------------------------------------------
    ('br-ap-couv', 960, 540, couv_air),
    ('br-ap-def', 320, 320, _fab_scene(
        _sc_air_def, 'poisonous substances released into the atmosphere')),
    ('br-ap-causes', 320, 380, _fab_liste(
        ['Carbon dioxide from car exhausts', 'Carbon dioxide from industries',
         'Release of solid and liquid waste', 'Sulphur and nitrogen dioxide',
         'Poor sanitation in the gutters'], 'Causes of air pollution')),
    ('br-ap-effets', 320, 320, _fab_liste(
        ['It causes eye irritation', 'It brings air borne diseases',
         'Acid rain destroys crops', 'It destroys the ozone layer'],
        'Effects of air pollution')),
    ('br-ap-oeil', 320, 320, _fab_scene(_sc_air_oeil, 'dirty air irritates the eyes')),
    ('br-ap-pluie', 320, 320, _fab_scene(_sc_pluie, 'acid rain falls on the crops')),
    ('br-ap-ozone', 320, 320, _fab_scene(
        _sc_air_ozone, 'the ozone layer, and the hole in it', 262)),
    ('br-ap-prevention', 320, 320, _fab_liste(
        ['Limit the burning of bushes and tyres', 'Dispose of waste properly',
         'Service your car engine regularly', 'Use incinerators to burn waste'],
        'Prevention')),

    # ---- 37. Soil pollution -----------------------------------------------
    ('br-sp-couv', 960, 540, couv_sol),
    ('br-sp-def', 320, 320, _fab_scene(_sc_sol_def)),
    ('br-sp-causes', 320, 320, _fab_liste(
        ['Plastics and household waste', 'Chemical fertilisers',
         'Engine oil from vehicles', 'Bush fire'], 'Causes of soil pollution')),
    ('br-sp-feu', 320, 320, _fab_scene(_sc_sol_feu, 'bush fire spoils the soil', 262)),
    ('br-sp-dangers', 320, 380, _fab_liste(
        ['Heaps of waste breed rats and snakes', 'They breed mosquitoes',
         'Chemicals kill the soil organisms', 'Urine destroys the soil',
         'Bad odour causes diseases'], 'Dangers of soil pollution')),
    ('br-sp-prevention', 320, 320, _fab_liste(
        ['Avoid burning the bush for farming', 'Collect plastic wastes well',
         'Avoid using chemical fertilisers', 'Do not throw engine oil about'],
        'Prevention')),

    # ---- 38. Waste and its disposal ---------------------------------------
    ('br-dc-couv', 960, 540, couv_dechets),
    ('br-dc-def', 320, 320, _fab_scene(_sc_dechets_def)),
    ('br-dc-types', 320, 320, lambda t: _deux_tas(
        t, ['faeces', 'plants', 'food'], ['plastics', 'bottles', 'metals'],
        note='one decomposes, the other does not')),
    ('br-dc-methodes', 320, 380, _fab_liste(
        ['Dust bin or trash can', 'Refuse pit', 'Incinerator', 'Refuse bags',
         'Pit or water closet latrine'], 'Methods of waste disposal')),
    ('br-dc-fosse', 320, 320, _fab_scene(
        lambda t: fosse(t, 160, 140), 'a refuse pit, dug away from the house')),
    ('br-dc-incinerateur', 320, 320, _fab_scene(
        lambda t: incinerateur(t, 160, 150), 'an incinerator, where waste is burnt')),
    ('br-dc-sac', 320, 320, _fab_scene(
        lambda t: sac(t, 160, 140), 'refuse bags, left for the company to collect')),

    # ---- 39. Waste transformation ------------------------------------------
    ('br-rc-couv', 960, 540, couv_recyclage),
    ('br-rc-def', 320, 320, _fab_chaine(
        [(lambda t, x, y: poubelle(t, x, y, (96, 108, 118), 0.8), 'waste'),
         (lambda t, x, y: feuille(t, x, y, 0.8), 'useful material')],
        'waste becomes something useful again')),
    ('br-rc-importance', 320, 320, _fab_liste(
        ['It reduces environmental pollution', 'It saves our money',
         'It saves our resources'], 'Why we recycle')),
    ('br-rc-papier', 320, 320, _fab_chaine(
        [(lambda t, x, y: sac(t, x, y - 4), 'waste paper'),
         (lambda t, x, y: sac(t, x, y - 4, CLAY), 'new paper and bags')])),
    ('br-rc-fumier', 320, 320, _fab_chaine(
        [(lambda t, x, y: tas(t, x, y, (120, 96, 72)), 'animal dung'),
         (lambda t, x, y: pousse(t, x, y), 'organic manure')],
        'fowl droppings make the best manure')),
    ('br-rc-biogaz', 320, 320, _fab_scene(_sc_biogaz, None)),

    # ---- 40. Conflicts ------------------------------------------------------
    ('br-cf-couv', 960, 540, couv_conflits),
    ('br-cf-def', 320, 320, _fab_scene(
        _sc_dispute, 'a disagreement between two or more people')),
    ('br-cf-lieux', 320, 380, _fab_liste(
        ['At home', 'In school', 'In villages', 'In communities', 'In countries'],
        'Where conflicts are seen')),
    ('br-cf-causes', 320, 320, _fab_liste(
        ['Jealousy at home or at work', 'Family problems over property',
         'Wrong decisions by leaders', 'Stubbornness and disrespect'],
        'Causes of conflicts')),
    ('br-cf-effets', 320, 320, _fab_liste(
        ['Loss of lives and properties', 'Enmity in the family',
         'It leads to violence and war'], 'Effects of conflicts')),
    ('br-cf-resolution', 320, 320, _fab_scene(
        _sc_entente, 'dialogue, apologise, forgive')),

    # ---- 41. Plants ---------------------------------------------------------
    ('br-pl-couv', 960, 540, couv_plantes),
    ('br-pl-def', 320, 320, _fab_scene(
        _sc_plante_def, 'a living thing that grows from the soil', 276)),
    ('br-pl-photo', 320, 320, _fab_scene(_sc_photo, None)),
    ('br-pl-types', 320, 320, _fab_grille([
        (lambda t, x, y: herbe(t, x, y, 5, (150, 160, 120)), 'weeds'),
        (lambda t, x, y: pousse(t, x, y), 'herbs'),
        (lambda t, x, y: arbuste(t, x, y - 10, 0.92), 'shrubs'),
        (lambda t, x, y: arbre(t, x, y - 12), 'trees')])),
    ('br-pl-legum', 320, 320, _fab_scene(_sc_nodosites, None)),
    ('br-pl-kinds', 320, 320, _fab_liste(
        ['Annual: one year, then it dies', 'Biennial: two years',
         'Perennial: many years'], 'Kinds of plants')),

    # ---- 42. Parts of a plant ------------------------------------------------
    ('br-pt-couv', 960, 540, couv_parties),
    ('br-pt-schema', 480, 300, _fab_scene(_sc_schema, None)),
    ('br-pt-bourgeon', 480, 330, _fab_vise('terminal bud',
                                           'it makes young leaves and branches')),
    ('br-pt-feuille', 480, 330, _fab_vise('leaf', 'chlorophyll traps the sunlight')),
    ('br-pt-fleur', 480, 330, _fab_vise('flower', 'the flower becomes the fruit')),
    ('br-pt-tige', 480, 330, _fab_vise('stem', 'the stem holds the branches')),
    ('br-pt-racine', 320, 320, _fab_scene(_sc_racine, None)),
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
