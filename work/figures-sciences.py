# -*- coding: utf-8 -*-
"""
Les figures des six leçons de sciences et de technologie de BRAYNE (CM1).

Vingt-neuf images dessinées, aucune générée. Deux raisons, et la seconde
n'est pas technique.

La première est celle de la charte : une leçon qui annonce cinq parties à une
lampe, quatre étapes à un cycle de l'eau ou deux ovaires doit être illustrée
par une figure où l'enfant qui compte trouve cinq, quatre et deux. Un
générateur ne garantit aucun de ces comptes.

La seconde tient aux deux leçons sur la puberté et les organes reproducteurs.
Elles parlent du corps d'un enfant de onze ans. On n'en fait donc pas des
images de corps : ni silhouettes, ni schémas anatomiques, ni rien qui
représente un enfant. Ce qui est montré, ce sont les mots de la leçon posés
sur des étiquettes, des règles graduées pour les âges, des ondes pour la
voix, et les deux cellules reproductrices — un disque et une cellule à
longue queue, les icônes que tout manuel emploie. L'enfant révise ce que la
maîtresse a écrit au tableau, sans qu'une image s'en mêle.

Usage :  python work/figures-sciences.py
"""

import importlib.util
import math
import os

from PIL import Image

_ICI = os.path.dirname(os.path.abspath(__file__))


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Le fond, la palette, le lissage et la police viennent des figures de maths :
# deux moteurs de dessin donneraient deux styles dans la même application.
fm = _charger('figures_maths', 'figures-maths.py')

Toile = fm.Toile
SORTIE = fm.SORTIE
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

TONS = (MINT, SKY, LILAC, SAND, WHITE_WARM)


# ───────────────────────────── les outils communs ─────────────────────────

def _etiquette(t, cx, cy, largeur, hauteur, texte, taille, fond=WHITE_WARM, encre=INK):
    t.rrect(cx - largeur / 2, cy - hauteur / 2, cx + largeur / 2, cy + hauteur / 2,
            hauteur * 0.32, fill=fond, bord=(255, 255, 255), trait=2)
    t.texte((cx, cy), texte, taille, encre)


def _pile(t, cx, haut, largeur, mots, taille, hauteur=44, pas=56):
    """Une liste de mots, empilée. Les noms d'organes sont la leçon."""
    for i, mot in enumerate(mots):
        _etiquette(t, cx, haut + i * pas, largeur, hauteur, mot, taille, TONS[i % len(TONS)])


def _paires(t, gauche, droite, haut, taille=19, pas=56):
    """Deux colonnes reliées : l'élément à gauche, son rôle à droite."""
    for i, (g, d) in enumerate(zip(gauche, droite)):
        y = haut + i * pas
        _etiquette(t, 92, y, 148, 40, g, taille, TONS[i % len(TONS)])
        t.ligne([(168, y), (196, y)], INK_2, 3)
        _etiquette(t, 234, y, 148, 40, d, taille, WHITE_WARM, INK_2)


def _onde(t, cx, cy, largeur, periodes, amplitude, couleur):
    """Une onde : serrée pour une voix fine, large pour une voix grave."""
    points = []
    for i in range(121):
        x = cx - largeur / 2 + largeur * i / 120
        points.append((x, cy - math.sin(i / 120 * periodes * 2 * math.pi) * amplitude))
    t.ligne(points, couleur, 4)


def _fleche(t, a, b, couleur, trait=4, tete=11):
    t.ligne([a, b], couleur, trait)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for s in (2.5, -2.5):
        t.ligne([b, (b[0] + math.cos(ang + s) * tete, b[1] + math.sin(ang + s) * tete)],
                couleur, trait)


def _goutte(t, cx, cy, r, couleur=SKY):
    t.poly([(cx, cy - r * 1.7), (cx + r * 0.95, cy + r * 0.25), (cx, cy + r),
            (cx - r * 0.95, cy + r * 0.25)], fill=couleur)
    t.disque((cx, cy + r * 0.05), r * 0.95, fill=couleur)


def _nuage(t, cx, cy, e, couleur=WHITE_WARM):
    for dx, dy, r in ((-0.55, 0.12, 0.45), (0.0, -0.18, 0.58), (0.58, 0.14, 0.42),
                      (-0.2, 0.3, 0.42), (0.26, 0.32, 0.4)):
        t.disque((cx + dx * e, cy + dy * e), r * e, fill=couleur)


def _soleil(t, cx, cy, r):
    for i in range(8):
        a = i * math.pi / 4
        t.ligne([(cx + math.cos(a) * r * 1.3, cy + math.sin(a) * r * 1.3),
                 (cx + math.cos(a) * r * 1.75, cy + math.sin(a) * r * 1.75)], GOLD, 4)
    t.disque((cx, cy), r, fill=GOLD)


def _coche(t, cx, cy, r, bonne):
    """Un crochet ou une croix, tracés.

    Posés comme caractères, ils sortaient en carrés vides : Fredoka ne porte
    ni le signe de la coche ni celui de la croix, et une pastille muette ne
    dit pas si l’eau est bonne ou mauvaise.
    """
    t.disque((cx, cy), r, fill=MINT if bonne else CLAY)
    if bonne:
        t.ligne([(cx - r * 0.45, cy), (cx - r * 0.1, cy + r * 0.38),
                 (cx + r * 0.48, cy - r * 0.38)], INK, max(3, r * 0.16))
    else:
        for s in (1, -1):
            t.ligne([(cx - r * 0.4, cy - r * 0.4 * s), (cx + r * 0.4, cy + r * 0.4 * s)],
                    WHITE_WARM, max(3, r * 0.16))


def _verre(t, cx, cy, h, claire=True):
    larg = h * 0.62
    t.poly([(cx - larg / 2, cy - h / 2), (cx + larg / 2, cy - h / 2),
            (cx + larg * 0.38, cy + h / 2), (cx - larg * 0.38, cy + h / 2)],
           fill=WHITE_WARM)
    t.poly([(cx - larg * 0.44, cy - h * 0.18), (cx + larg * 0.44, cy - h * 0.18),
            (cx + larg * 0.38, cy + h / 2), (cx - larg * 0.38, cy + h / 2)],
           fill=SKY if claire else (166, 146, 112))


def _lampe(t, cx, cy, e, numeros=False, allumee=True):
    """La lampe tempête, et ses cinq parties, toujours les mêmes.

    Les positions sont calculées depuis e : une partie ne peut donc pas
    glisser d'une figure à l'autre, et le numéro 3 montre toujours la mèche.
    """
    # Le réservoir.
    t.rrect(cx - e * 0.42, cy + e * 0.28, cx + e * 0.42, cy + e * 0.72, e * 0.12,
            fill=SAND, bord=INK, trait=3)
    # La molette, sur le flanc du réservoir.
    t.disque((cx + e * 0.44, cy + e * 0.38), e * 0.10, fill=CLAY, bord=INK, trait=3)
    # Le verre, en tonneau.
    t.poly([(cx - e * 0.30, cy + e * 0.28), (cx - e * 0.40, cy - e * 0.12),
            (cx - e * 0.26, cy - e * 0.52), (cx + e * 0.26, cy - e * 0.52),
            (cx + e * 0.40, cy - e * 0.12), (cx + e * 0.30, cy + e * 0.28)],
           fill=(214, 236, 248))
    t.ligne([(cx - e * 0.30, cy + e * 0.28), (cx - e * 0.40, cy - e * 0.12),
             (cx - e * 0.26, cy - e * 0.52)], INK, 3)
    t.ligne([(cx + e * 0.30, cy + e * 0.28), (cx + e * 0.40, cy - e * 0.12),
             (cx + e * 0.26, cy - e * 0.52)], INK, 3)
    # La mèche et sa flamme.
    t.rrect(cx - e * 0.05, cy + e * 0.02, cx + e * 0.05, cy + e * 0.28, e * 0.02,
            fill=INK_2)
    if allumee:
        t.poly([(cx, cy - e * 0.22), (cx + e * 0.11, cy + e * 0.02),
                (cx, cy + e * 0.08), (cx - e * 0.11, cy + e * 0.02)], fill=GOLD)
    # La grille d'aération, au sommet.
    t.rrect(cx - e * 0.30, cy - e * 0.66, cx + e * 0.30, cy - e * 0.50, e * 0.06,
            fill=INK_2)
    for i in range(5):
        x = cx - e * 0.22 + i * e * 0.11
        t.ligne([(x, cy - e * 0.64), (x, cy - e * 0.52)], SAND, 2)

    if numeros:
        for n, (x, y) in enumerate((
            (cx, cy + e * 0.50),          # 1 réservoir
            (cx + e * 0.44, cy + e * 0.38),  # 2 molette
            (cx, cy + e * 0.17),          # 3 mèche
            (cx - e * 0.33, cy - e * 0.18),  # 4 verre
            (cx, cy - e * 0.58),          # 5 grille
        ), start=1):
            t.disque((x, y), e * 0.095, fill=WHITE_WARM, bord=CLAY, trait=3)
            t.texte((x, y), str(n), e * 0.11, CLAY)


# ───────────────────────── la puberté (sans aucun corps) ──────────────────

def pu_puberte(t):  # 960x540
    t.texte((480, 92), 'la puberté', 46, INK_2)
    t.rrect(300, 150, 360, 450, 18, fill=WHITE_WARM, bord=(255, 255, 255), trait=3)
    for i in range(7):
        y = 420 - i * 45
        t.ligne([(300, y), (338 if i % 2 else 352, y)], INK_2, 3)
        if i % 2 == 0:
            t.texte((288, y), str(10 + i), 24, INK_2, 'rm')
    t.texte((330, 125), 'ans', 22, INK_2)
    _etiquette(t, 560, 240, 300, 62, 'enfant', 34, MINT)
    _fleche(t, (560, 285), (560, 345), CLAY, 5, 14)
    _etiquette(t, 560, 390, 300, 62, 'adulte', 34, LILAC)
    t.texte((760, 315), 'un passage,', 26, INK_2)
    t.texte((760, 350), 'pas un saut', 26, INK_2)


def pu_passage(t):
    _etiquette(t, 160, 92, 230, 62, 'enfant', 34, MINT)
    _fleche(t, (160, 138), (160, 196), CLAY, 5, 14)
    _etiquette(t, 160, 240, 230, 62, 'adulte', 34, LILAC)
    t.texte((160, 296), 'le passage', 26, CLAY)


def pu_ages(t):
    for i, (nom, a, b, ton) in enumerate((('garçons', 12, 15, SKY), ('filles', 11, 14, LILAC))):
        y = 108 + i * 108
        t.texte((160, y - 44), nom, 26, INK_2)
        t.rrect(44, y - 16, 276, y + 16, 16, fill=WHITE_WARM, bord=(255, 255, 255), trait=2)
        # L'échelle va de 10 à 16 ans : la barre dit l'intervalle du cahier.
        x0 = 44 + (a - 10) / 6 * 232
        x1 = 44 + (b - 10) / 6 * 232
        t.rrect(x0, y - 16, x1, y + 16, 16, fill=ton)
        t.texte(((x0 + x1) / 2, y), '%d – %d' % (a, b), 24, INK)
    t.texte((160, 282), '10 ans ................ 16 ans', 20, INK_2)


def pu_garcon(t):
    _pile(t, 160, 70, 272, ['les épaules s’élargissent', 'les muscles se développent',
                            'la voix devient grave', 'des poils apparaissent'], 18)
    _onde(t, 160, 290, 230, 2.0, 22, BLEU)


def pu_fille(t):
    _pile(t, 160, 70, 272, ['les seins se développent', 'le bassin s’élargit',
                            'la voix devient fine', 'des poils apparaissent'], 18)
    _onde(t, 160, 290, 230, 5.0, 16, CLAY)


def pu_cellules(t):
    # L'ovule : un disque. Le spermatozoïde : une tête et une longue queue.
    t.disque((98, 128), 46, fill=LILAC, bord=WHITE_WARM, trait=3)
    t.disque((98, 128), 17, fill=INK_2)
    t.texte((98, 206), 'ovule', 24, INK_2)

    t.disque((196, 118), 20, fill=SKY, bord=WHITE_WARM, trait=3)
    queue = [(196 + 16 + i * 3.6, 118 + math.sin(i / 3.0) * 12) for i in range(18)]
    t.ligne(queue, SKY, 4)
    t.texte((218, 206), 'spermatozoïde', 17, INK_2)
    t.texte((160, 268), 'cellules', 26, CLAY)
    t.texte((160, 300), 'reproductrices', 26, CLAY)


# ───────────────────────── les organes reproducteurs ──────────────────────

def or_organes(t):  # 960x540
    t.texte((480, 86), 'les organes reproducteurs', 40, INK_2)
    for i, (titre, mots, ton) in enumerate((
        ('chez l’homme', ['le pénis', 'les deux testicules', 'les canaux', 'la prostate'], SKY),
        ('chez la femme', ['la vulve', 'l’utérus', 'le vagin', 'les deux ovaires'], LILAC),
    )):
        cx = 288 + i * 384
        t.rrect(cx - 170, 140, cx + 170, 470, 24, fill=(255, 255, 255, 120))
        _etiquette(t, cx, 176, 268, 52, titre, 26, ton)
        for j, mot in enumerate(mots):
            _etiquette(t, cx, 248 + j * 62, 268, 48, mot, 24, WHITE_WARM)


def or_appareil(t):
    t.rrect(40, 70, 280, 236, 24, fill=(255, 255, 255, 150), bord=CLAY, trait=3)
    for i, (dx, dy) in enumerate(((-62, -42), (0, -46), (62, -38), (-44, 24), (34, 30))):
        t.disque((160 + dx, 150 + dy), 24, fill=TONS[i % len(TONS)], bord=WHITE_WARM, trait=3)
    t.texte((160, 262), 'un ensemble', 26, CLAY)
    t.texte((160, 294), 'd’organes', 26, CLAY)


def or_homme(t):
    _pile(t, 160, 78, 268, ['le pénis', 'les deux testicules', 'les canaux', 'la prostate'], 23)
    t.texte((160, 300), 'chez l’homme', 24, CLAY)


def or_femme(t):
    _pile(t, 160, 78, 268, ['la vulve', 'l’utérus', 'le vagin', 'les deux ovaires'], 23)
    t.texte((160, 300), 'chez la femme', 24, CLAY)


def or_roles(t):
    _paires(t, ['les testicules', 'les ovaires', 'l’utérus'],
            ['spermatozoïdes', 'ovules', 'gestation'], 108, 18, 66)
    t.texte((160, 282), 'chacun son rôle', 24, CLAY)


# ───────────────────────────── le cycle de l'eau ──────────────────────────

def _scene_cycle(t, w, h, etapes=(1, 2, 3, 4), titres=False):
    """La scène complète, avec les étapes qu'on veut allumer."""
    ech = w / 960.0
    sol = h * 0.78
    mer = h * 0.86
    t.rrect(0, mer, w, h + 10, 0, fill=(150, 196, 226))
    t.poly([(0, sol), (w * 0.34, sol - 26 * ech), (w * 0.62, sol - 8 * ech), (w, sol - 34 * ech),
            (w, mer + 2), (0, mer + 2)], fill=(168, 196, 150))
    _soleil(t, w * 0.14, h * 0.20, 34 * ech)

    if 1 in etapes:
        for i in range(4):
            x = w * (0.22 + i * 0.045)
            _fleche(t, (x, mer - 6), (x, h * 0.38), SKY, 3, 8)
        if titres:
            t.texte((w * 0.28, h * 0.52), 'évaporation', 22 * ech * 1.6, SKY)
    if 2 in etapes:
        _nuage(t, w * 0.56, h * 0.26, 62 * ech)
        if titres:
            t.texte((w * 0.56, h * 0.42), 'condensation', 22 * ech * 1.6, INK_2)
    if 3 in etapes:
        for i in range(7):
            x = w * (0.46 + i * 0.033)
            t.ligne([(x, h * 0.36), (x - 6 * ech, h * 0.56)], SKY, 3)
        if titres:
            t.texte((w * 0.56, h * 0.64), 'précipitation', 22 * ech * 1.6, SKY)
    if 4 in etapes:
        # Trois filets qui descendent, pas une flèche isolée : une seule
        # pointe au coin de l’image ne se lisait pas comme un ruissellement.
        for i in range(3):
            x = w * (0.70 + i * 0.09)
            _fleche(t, (x, sol - (26 - i * 6) * ech), (x + w * 0.07, mer - 4), BLEU, 4, 10)
        if titres:
            t.texte((w * 0.82, h * 0.70), 'ruissellement', 20 * ech * 1.6, BLEU)


def ce_cycle(t):  # 960x540
    _scene_cycle(t, 960, 540, titres=True)
    t.texte((480, 70), 'le cycle de l’eau', 42, INK_2)


def ce_trajet(t):
    # Une boucle qui revient à son origine : la définition, sans décor.
    points = []
    for i in range(121):
        a = -math.pi / 2 + i / 120 * 2 * math.pi * 0.92
        points.append((160 + math.cos(a) * 92, 150 + math.sin(a) * 78))
    t.ligne(points, SKY, 7)
    _fleche(t, points[-6], points[-1], SKY, 7, 18)
    _goutte(t, 160, 72, 17)
    t.texte((160, 268), 'il revient', 26, CLAY)
    t.texte((160, 300), 'à son départ', 26, CLAY)


def ce_evaporation(t):
    _scene_cycle(t, 320, 320, etapes=(1,))
    t.texte((160, 300), 'évaporation', 26, CLAY)


def ce_condensation(t):
    _scene_cycle(t, 320, 320, etapes=(1, 2))
    t.texte((160, 300), 'condensation', 26, CLAY)


def ce_precipitation(t):
    _scene_cycle(t, 320, 320, etapes=(2, 3))
    t.texte((160, 300), 'précipitation', 26, CLAY)


def ce_ruissellement(t):
    _scene_cycle(t, 320, 320, etapes=(3, 4))
    t.texte((160, 300), 'ruissellement', 26, CLAY)


# ───────────────────────────── l'eau potable ──────────────────────────────

def ep_potable(t):  # 960x540
    t.texte((480, 92), 'l’eau potable', 44, INK_2)
    _verre(t, 370, 300, 200, claire=True)
    _coche(t, 370, 424, 30, True)
    _verre(t, 590, 300, 200, claire=False)
    _coche(t, 590, 424, 30, False)
    t.texte((480, 486), 'celle qu’on peut boire sans danger', 28, CLAY)


def ep_definition(t):
    _verre(t, 100, 140, 150, claire=True)
    _coche(t, 100, 238, 24, True)
    _verre(t, 220, 140, 150, claire=False)
    _coche(t, 220, 238, 24, False)
    t.texte((160, 296), 'sans danger', 26, CLAY)


def ep_traiter(t):
    for i, (a, b) in enumerate((('javelliser', 'filtrer'), ('bouillir', 'filtrer'),
                                ('javelliser', 'décanter'))):
        y = 92 + i * 72
        _etiquette(t, 96, y, 136, 46, a, 20, TONS[i % len(TONS)])
        t.texte((172, y), '+', 26, INK_2)
        _etiquette(t, 240, y, 118, 46, b, 20, WHITE_WARM)
    t.texte((160, 296), 'deux gestes à chaque fois', 20, CLAY)


def ep_roles(t):
    for i, (icone, mot, ton) in enumerate(((' ', 'la température', MINT),
                                           (' ', 'le transport', SKY),
                                           (' ', 'l’évacuation', LILAC))):
        y = 96 + i * 76
        t.disque((76, y), 26, fill=ton, bord=WHITE_WARM, trait=3)
        t.texte((76, y), str(i + 1), 26, INK)
        t.texte((112, y), mot, 23, INK_2, 'lm')
    t.texte((160, 296), 'les trois rôles de l’eau', 20, CLAY)


# ───────────────────────────── le compost ─────────────────────────────────

def co_compost(t):  # 960x540
    t.texte((480, 92), 'le compost', 44, INK_2)
    # Un tas en couches : c'est ainsi qu'il se monte, et qu'il se dessine.
    for i, (ton, part) in enumerate(((SAND, 1.0), ((176, 150, 110), 0.82),
                                     ((132, 110, 78), 0.62), ((96, 78, 56), 0.4))):
        demi = 230 * part
        y = 420 - i * 56
        t.poly([(480 - demi, y), (480 + demi, y), (480 + demi * 0.82, y - 56),
                (480 - demi * 0.82, y - 56)], fill=ton)
    t.disque((480, 190), 16, fill=MINT)
    t.ligne([(480, 206), (480, 236)], (120, 160, 96), 5)
    t.texte((480, 486), 'un engrais naturel', 28, CLAY)


def co_definition(t):
    t.rrect(40, 72, 280, 212, 22, fill=(255, 255, 255, 150), bord=CLAY, trait=3)
    t.disque((106, 128), 36, fill=MINT, bord=WHITE_WARM, trait=3)
    t.texte((106, 128), 'végétal', 15, INK)
    t.disque((214, 128), 36, fill=SAND, bord=WHITE_WARM, trait=3)
    t.texte((214, 128), 'animal', 16, INK)
    _fleche(t, (106, 170), (152, 194), INK_2, 3, 8)
    _fleche(t, (214, 170), (168, 194), INK_2, 3, 8)
    t.texte((160, 256), 'compost', 30, INK)
    t.texte((160, 294), 'engrais naturel', 22, CLAY)


def co_enrichir(t):
    for i, (ton, pousse, mot) in enumerate((((214, 198, 162), False, 'sol pauvre'),
                                            ((104, 84, 60), True, 'sol enrichi'))):
        cx = 92 + i * 136
        t.rrect(cx - 56, 140, cx + 56, 212, 12, fill=ton)
        if pousse:
            t.ligne([(cx, 140), (cx, 96)], (120, 160, 96), 5)
            t.disque((cx - 14, 104), 13, fill=MINT)
            t.disque((cx + 14, 96), 13, fill=MINT)
        t.texte((cx, 240), mot, 19, INK_2)
    _fleche(t, (152, 176), (196, 176), CLAY, 5, 12)
    t.texte((160, 294), 'le compost nourrit la terre', 18, CLAY)


def co_elements(t):
    mots = ['feuilles mortes', 'cendre de bois', 'restes de repas',
            'épluchures', 'litière d’animaux']
    for i, mot in enumerate(mots):
        y = 66 + i * 50
        t.disque((60, y), 15, fill=TONS[i % len(TONS)], bord=WHITE_WARM, trait=2)
        t.texte((84, y), mot, 21, INK_2, 'lm')
    t.texte((160, 300), 'tous biodégradables', 21, CLAY)


# ───────────────────────────── la lampe à pétrole ─────────────────────────

def la_lampe(t):  # 960x540
    t.texte((480, 80), 'la lampe à pétrole', 42, INK_2)
    _lampe(t, 420, 300, 300, numeros=True)
    noms = ['le réservoir', 'la molette', 'la mèche', 'le verre', 'la grille']
    for i, nom in enumerate(noms):
        y = 172 + i * 56
        t.disque((700, y), 20, fill=WHITE_WARM, bord=CLAY, trait=3)
        t.texte((700, y), str(i + 1), 22, CLAY)
        t.texte((728, y), nom, 25, INK_2, 'lm')
    t.texte((480, 500), 'cinq parties essentielles', 26, CLAY)


def la_definition(t):
    _lampe(t, 160, 136, 172)
    t.texte((160, 268), 'lampe tempête', 26, INK)
    t.texte((160, 300), 'elle marche au pétrole', 19, CLAY)


def la_parties(t):
    _lampe(t, 160, 140, 176, numeros=True)
    t.disque((268, 56), 28, fill=GOLD)
    t.texte((268, 56), '5', 30, WHITE_WARM)
    t.texte((160, 300), 'cinq parties', 24, CLAY)


def la_roles(t):
    _paires(t, ['le réservoir', 'la molette', 'la mèche', 'le verre', 'la grille'],
            ['le pétrole', 'la flamme', 'elle monte', 'le vent', 'l’air'], 76, 17, 50)
    t.texte((160, 304), 'chacune son rôle', 21, CLAY)


FIGURES = [
    ('pu-puberte', 960, 540, pu_puberte),
    ('pu-passage', 320, 320, pu_passage),
    ('pu-ages', 320, 320, pu_ages),
    ('pu-garcon', 320, 320, pu_garcon),
    ('pu-fille', 320, 320, pu_fille),
    ('pu-cellules', 320, 320, pu_cellules),
    ('or-organes', 960, 540, or_organes),
    ('or-appareil', 320, 320, or_appareil),
    ('or-homme', 320, 320, or_homme),
    ('or-femme', 320, 320, or_femme),
    ('or-roles', 320, 320, or_roles),
    ('ce-cycle', 960, 540, ce_cycle),
    ('ce-trajet', 320, 320, ce_trajet),
    ('ce-evaporation', 320, 320, ce_evaporation),
    ('ce-condensation', 320, 320, ce_condensation),
    ('ce-precipitation', 320, 320, ce_precipitation),
    ('ce-ruissellement', 320, 320, ce_ruissellement),
    ('ep-potable', 960, 540, ep_potable),
    ('ep-definition', 320, 320, ep_definition),
    ('ep-traiter', 320, 320, ep_traiter),
    ('ep-roles', 320, 320, ep_roles),
    ('co-compost', 960, 540, co_compost),
    ('co-definition', 320, 320, co_definition),
    ('co-enrichir', 320, 320, co_enrichir),
    ('co-elements', 320, 320, co_elements),
    ('la-lampe', 960, 540, la_lampe),
    ('la-definition', 320, 320, la_definition),
    ('la-parties', 320, 320, la_parties),
    ('la-roles', 320, 320, la_roles),
]


def controler():
    """Les comptes des leçons sont les comptes des figures, ou rien n'est dessiné."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'
    assert len(FIGURES) == 29, 'vingt-neuf figures attendues : %d' % len(FIGURES)


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
