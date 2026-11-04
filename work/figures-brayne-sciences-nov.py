# -*- coding: utf-8 -*-
"""
Les figures des quatre leçons de sciences et de technologie de BRAYNE (CM1)
— cahier du 27 octobre au 2 novembre 2026.

Contrairement aux mathématiques, ces leçons-là parlent de choses qu-on peut
montrer : une roche, un puits, un serpent, une ampoule. Les figures sont
donc des objets et non des tableaux — mais des objets **tenus par ce que
la leçon dit**.

Trois exemples de cette contrainte :

  les roches      le basalte est sombre et grenu, le granite moucheté clair,
                  l-argile en couches, le marbre veiné. Quatre roches qui se
                  ressembleraient ne vaudraient pas mieux que quatre mots
  la locomotion   le chien a ses quatre pattes au sol, le lapin les a
                  repliées en l-air, le serpent n-en a pas du tout. C-est
                  l-organe qui commande le déplacement, et c-est lui qu-on
                  voit
  les lampes      l-ampoule montre SON filament, parce que la leçon dit que
                  le courant y passe. Une ampoule dessinée pleine
                  n-illustrerait pas la phrase

Usage :  python work/figures-brayne-sciences-nov.py
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

VERT = (122, 164, 108)
VERT_PALE = (206, 221, 199)
TERRE = (168, 122, 86)
GRIS = (138, 143, 146)
GRIS_CLAIR = (196, 199, 200)
NOIR_DOUX = (74, 78, 82)
ROUGE = (183, 66, 52)

BANDEAU = (184, 356)


# --------------------------------------------------------------------------
# Les briques

def _mesure(t, s, taille):
    return t.d.textlength(s, font=t.pol(taille)) / S


def _pastille(t, cx, cy, mot, taille, fond=WHITE_WARM, couleur=INK, marge=12, h=None):
    w = _mesure(t, mot, taille) + marge * 2
    h = h if h else taille + 14
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill=fond, bord=INK, trait=1.8)
    t.texte((cx, cy), mot, taille, couleur)
    return w


def _liste(t, items, titre=None, haut=80, pas=46):
    if titre:
        t.texte((160, haut - 26), titre, 16, INK)
    for i, texte in enumerate(items):
        y = haut + pas * i
        t.rrect(22, y, 298, y + 36, 10, fill=WHITE_WARM, bord=INK, trait=1.8)
        t.disque((44, y + 18), 11, fill=GOLD, bord=INK, trait=1.5)
        t.texte((44, y + 18), str(i + 1), 13, INK)
        taille = 13
        while taille > 9 and _mesure(t, texte, taille) > 228:
            taille -= 1
        t.texte((62, y + 18), texte, taille, INK, ancre='lm')


def _legende(t, mot, y=282, taille=17):
    t.texte((160, y), mot, taille, INK)


# --- les roches ------------------------------------------------------------

def _caillou(t, cx, cy, r, fond, bord=INK, grain=None, veines=None, couches=None):
    """Un bloc irrégulier : une roche n-est pas un galet rond."""
    pts = []
    for i in range(9):
        a = 2 * math.pi * i / 9
        d = r * (0.82 + 0.22 * ((i * 7) % 5) / 5.0)
        pts.append((cx + d * math.cos(a), cy + d * math.sin(a) * 0.82))
    t.poly(pts, fill=fond, bord=bord, trait=2.4)
    if grain:
        for k in range(14):
            a = 2 * math.pi * ((k * 5) % 14) / 14
            d = r * 0.18 * (1 + (k % 4))
            t.disque((cx + d * math.cos(a) * 0.9, cy + d * math.sin(a) * 0.6),
                     r * 0.075, fill=grain)
    if couches:
        for k in range(-2, 3):
            y = cy + k * r * 0.26
            t.ligne([(cx - r * 0.72, y), (cx + r * 0.72, y)], couches, 2)
    if veines:
        for k in (-1, 1):
            t.ligne([(cx - r * 0.7, cy + k * r * 0.28),
                     (cx - r * 0.1, cy - k * r * 0.1),
                     (cx + r * 0.7, cy + k * r * 0.34)], veines, 2.2)


# --- l-eau -----------------------------------------------------------------

def _puits(t, cx, cy, l=96):
    t.rrect(cx - l / 2, cy - l * 0.12, cx + l / 2, cy + l * 0.46, 6, fill=GRIS_CLAIR, bord=INK, trait=2.2)
    for k in range(-1, 2):
        t.ligne([(cx + k * l * 0.2, cy - l * 0.12), (cx + k * l * 0.2, cy + l * 0.46)], GRIS, 1.6)
    t.d.ellipse([int((cx - l * 0.42) * S), int((cy - l * 0.2) * S),
                 int((cx + l * 0.42) * S), int((cy - l * 0.02) * S)],
                fill=SKY, outline=INK, width=int(2 * S))
    t.ligne([(cx - l * 0.4, cy - l * 0.3), (cx - l * 0.4, cy - l * 0.62)], INK, 2.4)
    t.ligne([(cx + l * 0.4, cy - l * 0.3), (cx + l * 0.4, cy - l * 0.62)], INK, 2.4)
    t.ligne([(cx - l * 0.44, cy - l * 0.62), (cx + l * 0.44, cy - l * 0.62)], INK, 2.4)
    t.ligne([(cx, cy - l * 0.62), (cx, cy - l * 0.3)], INK_2, 1.6)
    t.rrect(cx - l * 0.1, cy - l * 0.32, cx + l * 0.1, cy - l * 0.16, 3, fill=TERRE, bord=INK, trait=1.6)


def _robinet(t, cx, cy, l=80):
    t.rrect(cx - l * 0.08, cy - l * 0.5, cx + l * 0.08, cy + l * 0.2, 4, fill=GRIS, bord=INK, trait=2)
    t.rrect(cx - l * 0.08, cy - l * 0.5, cx + l * 0.42, cy - l * 0.34, 4, fill=GRIS, bord=INK, trait=2)
    t.rrect(cx + l * 0.3, cy - l * 0.34, cx + l * 0.42, cy - l * 0.16, 3, fill=GRIS, bord=INK, trait=2)
    t.disque((cx, cy - l * 0.58), l * 0.12, fill=CLAY, bord=INK, trait=2)
    for k in range(3):
        t.disque((cx + l * 0.36, cy - l * 0.02 + k * l * 0.12), l * 0.05, fill=SKY, bord=None)


def _goutte(t, cx, cy, r=14, fond=SKY):
    t.poly([(cx, cy - r * 1.5), (cx + r, cy + r * 0.3), (cx, cy + r), (cx - r, cy + r * 0.3)],
           fill=fond, bord=INK, trait=1.8)


# --- les animaux -----------------------------------------------------------

def _bete(t, cx, cy, l, pattes='au sol'):
    """Un animal, et c-est SA position de pattes qui dit son déplacement."""
    t.rrect(cx - l * 0.42, cy - l * 0.16, cx + l * 0.26, cy + l * 0.2, 11,
            fill=SAND, bord=INK, trait=2.2)
    t.disque((cx + l * 0.36, cy - l * 0.18), l * 0.17, fill=SAND, bord=INK, trait=2.2)
    t.disque((cx + l * 0.42, cy - l * 0.2), l * 0.03, fill=INK)
    if pattes == 'au sol':
        for dx in (-0.3, -0.06, 0.1):
            t.ligne([(cx + l * dx, cy + l * 0.2), (cx + l * dx, cy + l * 0.46)], INK, 2.6)
        t.ligne([(cx - l * 0.6, cy + l * 0.46), (cx + l * 0.5, cy + l * 0.46)], INK_2, 2)
    elif pattes == 'repliees':
        for dx in (-0.28, 0.08):
            t.ligne([(cx + l * dx, cy + l * 0.2), (cx + l * dx - l * 0.12, cy + l * 0.36),
                     (cx + l * dx + l * 0.04, cy + l * 0.42)], INK, 2.6)
        # Les oreilles, et le petit arc du saut : il quitte le sol.
        for dx in (0.3, 0.4):
            t.ligne([(cx + l * dx, cy - l * 0.32), (cx + l * dx + l * 0.03, cy - l * 0.6)], INK, 2.4)
        t.d.arc([int((cx - l * 0.7) * S), int((cy + l * 0.3) * S),
                 int((cx + l * 0.7) * S), int((cy + l * 0.95) * S)],
                200, 340, fill=CLAY, width=int(2.2 * S))
        t.ligne([(cx - l * 0.8, cy + l * 0.66), (cx + l * 0.8, cy + l * 0.66)], INK_2, 2)


def _serpent(t, cx, cy, l=120):
    """Pas une patte : c-est tout l-argument de la notion."""
    pts = []
    for i in range(41):
        x = cx - l + 2 * l * i / 40
        pts.append((x, cy + 16 * math.sin(i / 40 * 3 * math.pi)))
    t.ligne(pts, VERT, 9)
    t.ligne(pts, INK, 1.4)
    t.disque(pts[-1], 8, fill=VERT, bord=INK, trait=1.8)
    t.disque((pts[-1][0] + 3, pts[-1][1] - 2), 1.8, fill=INK)
    t.ligne([(cx - l, cy + 26), (cx + l, cy + 26)], INK_2, 2)


# --- les lampes ------------------------------------------------------------

def _ampoule(t, cx, cy, l=92, allumee=True):
    if allumee:
        for k in range(8):
            a = 2 * math.pi * k / 8
            t.ligne([(cx + l * 0.62 * math.cos(a), cy - l * 0.1 + l * 0.62 * math.sin(a)),
                     (cx + l * 0.82 * math.cos(a), cy - l * 0.1 + l * 0.82 * math.sin(a))],
                    GOLD, 2.6)
    t.disque((cx, cy - l * 0.1), l * 0.42, fill=(GOLD if allumee else WHITE_WARM), bord=INK, trait=2.4)
    # Le filament : la leçon dit que le courant y passe, donc on le voit.
    t.ligne([(cx - l * 0.14, cy + l * 0.12), (cx - l * 0.08, cy - l * 0.1),
             (cx, cy + l * 0.02), (cx + l * 0.08, cy - l * 0.1),
             (cx + l * 0.14, cy + l * 0.12)], CLAY, 2.4)
    t.rrect(cx - l * 0.16, cy + l * 0.26, cx + l * 0.16, cy + l * 0.48, 3,
            fill=GRIS, bord=INK, trait=2)
    for k in range(3):
        t.ligne([(cx - l * 0.16, cy + l * 0.3 + k * l * 0.06),
                 (cx + l * 0.16, cy + l * 0.3 + k * l * 0.06)], INK_2, 1.4)


def _interrupteur(t, cx, cy, l=56, allume=True):
    t.rrect(cx - l / 2, cy - l * 0.36, cx + l / 2, cy + l * 0.36, 7, fill=WHITE_WARM, bord=INK, trait=2)
    t.rrect(cx - l * 0.3, cy - (l * 0.24 if allume else -l * 0.02),
            cx + l * 0.3, cy + (l * 0.02 if allume else l * 0.24), 4,
            fill=(CLAY if allume else GRIS_CLAIR), bord=INK, trait=1.6)


def _panneau(t, cx, cy, l=104):
    t.poly([(cx - l * 0.5, cy - l * 0.3), (cx + l * 0.5, cy - l * 0.3),
            (cx + l * 0.38, cy + l * 0.26), (cx - l * 0.62, cy + l * 0.26)],
           fill=BLEU, bord=INK, trait=2.2)
    for k in range(1, 3):
        t.ligne([(cx - l * 0.5 + l * k / 3, cy - l * 0.3),
                 (cx - l * 0.62 + l * k / 3, cy + l * 0.26)], (255, 255, 255, 120), 1.8)
    t.ligne([(cx - l * 0.56, cy - l * 0.02), (cx + l * 0.44, cy - l * 0.02)], (255, 255, 255, 120), 1.8)
    t.ligne([(cx - l * 0.1, cy + l * 0.26), (cx - l * 0.1, cy + l * 0.52)], INK, 2.4)
    t.ligne([(cx - l * 0.34, cy + l * 0.52), (cx + l * 0.14, cy + l * 0.52)], INK, 2.4)


def _soleil(t, cx, cy, r=24):
    t.disque((cx, cy), r, fill=GOLD, bord=INK, trait=2)
    for k in range(8):
        a = 2 * math.pi * k / 8
        t.ligne([(cx + r * 1.3 * math.cos(a), cy + r * 1.3 * math.sin(a)),
                 (cx + r * 1.7 * math.cos(a), cy + r * 1.7 * math.sin(a))], GOLD, 2.4)


def _accumulateur(t, cx, cy, l=56):
    t.rrect(cx - l / 2, cy - l * 0.34, cx + l / 2, cy + l * 0.34, 5, fill=MINT, bord=INK, trait=2)
    t.rrect(cx + l / 2, cy - l * 0.1, cx + l * 0.58, cy + l * 0.1, 2, fill=INK)
    t.texte((cx, cy), '+ −', 15, INK)


def _bandeau_couv(t, titre, sous=None):
    w = _mesure(t, titre, 26) + 56
    t.rrect(480 - w / 2, 192, 480 + w / 2, 232, 20, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 212), titre, 26, INK)
    if sous:
        t.texte((480, 344), sous, 17, INK)


# --------------------------------------------------------------------------
# Les figures

def couv_roches(t):
    _bandeau_couv(t, 'Les roches')
    _caillou(t, 300, 298, 46, NOIR_DOUX, grain=GRIS)
    _caillou(t, 480, 298, 46, SAND, couches=TERRE)
    _caillou(t, 660, 298, 46, GRIS_CLAIR, veines=GRIS)


def couv_eau(t):
    _bandeau_couv(t, 'La gestion de l’eau')
    _puits(t, 380, 292, 104)
    _robinet(t, 580, 300, 92)


def couv_locomotion(t):
    _bandeau_couv(t, 'Le mode de locomotion')
    _bete(t, 300, 290, 70, 'au sol')
    _bete(t, 480, 290, 70, 'repliees')
    _serpent(t, 680, 300, 70)


def couv_lampes(t):
    _bandeau_couv(t, 'Les lampes')
    _ampoule(t, 360, 284, 92, True)
    _panneau(t, 580, 292, 104)
    _soleil(t, 700, 250, 20)


FIGURES = [
    # Les roches
    ('bs-ro-couv', 960, 540, couv_roches),
    ('bs-ro-def', 320, 320,
     lambda t: (_caillou(t, 160, 158, 74, GRIS_CLAIR, grain=GRIS),
                _legende(t, 'un bloc de minéraux, dur'))),
    ('bs-ro-trois', 320, 320,
     lambda t: (_caillou(t, 80, 150, 44, NOIR_DOUX, grain=GRIS),
                _caillou(t, 160, 150, 44, SAND, couches=TERRE),
                _caillou(t, 240, 150, 44, GRIS_CLAIR, veines=GRIS),
                _legende(t, 'trois types de roches', 236),
                t.texte((160, 266), 'magmatique · sédimentaire · métamorphique', 11, INK_2))),
    ('bs-ro-magma', 320, 320,
     lambda t: (_caillou(t, 108, 150, 50, NOIR_DOUX, grain=GRIS),
                _caillou(t, 218, 150, 44, SAND, grain=CLAY),
                t.texte((108, 212), 'basalte', 14, INK),
                t.texte((218, 212), 'granite', 14, INK),
                _legende(t, 'les roches magmatiques', 258))),
    ('bs-ro-sedi', 320, 320,
     lambda t: (_caillou(t, 160, 150, 72, SAND, couches=TERRE),
                _legende(t, 'des débris déposés en couches', 240),
                t.texte((160, 270), 'argile · calcaire', 15, INK_2))),
    ('bs-ro-meta', 320, 320,
     lambda t: (_caillou(t, 160, 150, 72, GRIS_CLAIR, veines=GRIS),
                _legende(t, 'des roches transformées', 240),
                t.texte((160, 270), 'gneiss · marbre · ardoise', 15, INK_2))),
    # La gestion de l-eau
    ('bs-eau-couv', 960, 540, couv_eau),
    ('bs-eau-points', 320, 320,
     lambda t: (_puits(t, 160, 140, 110), _legende(t, 'un point d’eau du quartier', 244))),
    ('bs-eau-sortes', 320, 320,
     lambda t: _liste(t, ['le puits', 'le forage', 'la source', 'le robinet'],
                      'Les points d’eau')),
    ('bs-eau-proteger', 320, 320,
     lambda t: _liste(t, ['nettoyer les alentours', 'protéger les sources',
                          'protéger les puits', 'éviter que la saleté y tombe'],
                      'Pour bien les gérer')),
    ('bs-eau-heures', 320, 320,
     lambda t: _liste(t, ['prévoir des heures de ravitaillement',
                          'éviter le gaspillage',
                          'multiplier les points d’eau'], 'Et aussi')),
    ('bs-eau-javel', 320, 320,
     lambda t: (_goutte(t, 136, 140, 16), _goutte(t, 168, 128, 13), _goutte(t, 196, 146, 11),
                t.d.ellipse([int(96 * S), int(174 * S), int(224 * S), int(214 * S)],
                            fill=SKY, outline=INK, width=int(2 * S)),
                _legende(t, 'quelques gouttes d’eau de javel', 250),
                t.texte((160, 278), 'jamais seul : c’est un produit dangereux', 12, ROUGE))),
    # Le mode de locomotion
    ('bs-loco-couv', 960, 540, couv_locomotion),
    ('bs-loco-milieu', 320, 320,
     lambda t: (_bete(t, 110, 140, 74, 'au sol'), _serpent(t, 230, 150, 54),
                _legende(t, 'le milieu et les organes', 234),
                t.texte((160, 262), 'commandent le déplacement', 15, INK))),
    ('bs-loco-marche', 320, 320,
     lambda t: (_bete(t, 160, 148, 100, 'au sol'),
                _legende(t, 'marcher sur ses pattes', 250),
                t.texte((160, 278), 'le chien · le lion', 15, INK_2))),
    ('bs-loco-saute', 320, 320,
     lambda t: (_bete(t, 160, 140, 100, 'repliees'),
                _legende(t, 'sauter', 254),
                t.texte((160, 282), 'le lapin · le kangourou', 15, INK_2))),
    ('bs-loco-rampe', 320, 320,
     lambda t: (_serpent(t, 160, 150, 110),
                _legende(t, 'ramper sur son ventre', 244),
                t.texte((160, 272), 'le serpent, qui n’a pas de pattes', 14, INK_2))),
    # Les lampes
    ('bs-la-couv', 960, 540, couv_lampes),
    ('bs-la-ampoule', 320, 320,
     lambda t: (_ampoule(t, 160, 146, 112, True), _legende(t, 'la lampe électrique', 250))),
    ('bs-la-douille', 320, 320,
     lambda t: (_ampoule(t, 112, 140, 84, False), _interrupteur(t, 232, 150, 60, False),
                t.ligne([(112, 192), (112, 220), (232, 220), (232, 174)], INK, 2.4),
                _legende(t, 'la douille et l’interrupteur', 258))),
    ('bs-la-filament', 320, 320,
     lambda t: (_ampoule(t, 160, 140, 112, True), _interrupteur(t, 262, 226, 46, True),
                t.ligne([(160, 196), (160, 226), (238, 226)], CLAY, 2.6),
                _legende(t, 'le courant passe par le filament', 282, 15))),
    ('bs-la-solaire', 320, 320,
     lambda t: (_panneau(t, 150, 128, 116), _accumulateur(t, 160, 218, 62),
                _ampoule(t, 258, 216, 54, False),
                t.ligne([(160, 190), (160, 200)], INK, 2.2),
                _legende(t, 'panneau, accumulateur, ampoule', 272, 14))),
    ('bs-la-soleil', 320, 320,
     lambda t: (_soleil(t, 234, 86, 24), _panneau(t, 150, 160, 124),
                t.ligne([(216, 110), (178, 140)], GOLD, 2.6),
                _legende(t, 'exposé au soleil toute la journée', 248, 15),
                t.texte((160, 276), 'pour charger l’accumulateur', 14, INK_2))),
]


def controler():
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        im = t.fini().convert('RGB')
        fond = im.getpixel((2, 2))
        for x in range(0, w, 3):
            for y in (1, h - 2):
                assert sum(abs(a - b) for a, b in zip(im.getpixel((x, y)), fond)) < 90, \
                    '%s : le dessin touche le bord en (%d, %d)' % (cle, x, y)
        for y in range(0, h, 3):
            for x in (1, w - 2):
                assert sum(abs(a - b) for a, b in zip(im.getpixel((x, y)), fond)) < 90, \
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
