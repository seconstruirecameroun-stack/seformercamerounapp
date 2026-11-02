# -*- coding: utf-8 -*-
"""
Les figures d'Unit 13 — Wood work and building, pour KLEIN (CE1).

Dix-sept images dessinées, aucune générée, et le même moteur que les maths
et les sciences : deux moteurs donneraient deux styles dans la même
application.

Ici le dessin fait plus que décorer. La faute de KLEIN est d'avoir échangé
builder et carpenter, et d'avoir mis « carver » partout ailleurs. Une
illustration qui montre un mur de briques à côté du mot builder, une table à
côté de carpenter et un mortier à côté de carver lui donne la prise que le
texte seul ne lui donnait pas — il reconnaît avant de nommer.

Les outils sont donc dessinés pour être reconnaissables, pas jolis : la
truelle est triangulaire, la scie a ses dents, la gouge a sa lame arrondie
qui la distingue du ciseau droit. C'est cette différence-là que l'exercice
lui demande, et c'est elle qu'on voit.

Usage :  python work/figures-anglais.py
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
fs = _charger('figures_sciences', 'figures-sciences.py')

Toile, SORTIE = fm.Toile, fm.SORTIE
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU
TONS = fs.TONS

BOIS = (176, 132, 86)
BOIS_SOMBRE = (132, 96, 58)
BRIQUE = (182, 94, 70)
MORTIER = (226, 218, 200)
ACIER = (196, 204, 212)
MANCHE = (150, 104, 62)


# ───────────────────────────── les objets du cours ────────────────────────

def _mur(t, x, y, large, haut, rangs=4):
    """Un mur de briques en appareil : les joints sont décalés d'un rang à l'autre."""
    h = haut / rangs
    for r in range(rangs):
        decale = (h * 1.1) if r % 2 else 0
        xx = x - decale
        while xx < x + large:
            debut = max(xx, x) + 2
            fin = min(xx + h * 2.2, x + large) - 2
            # Une brique coupée par le bord du mur peut devenir plus étroite
            # que ses marges : on la saute plutôt que de dessiner à l'envers.
            if fin > debut:
                t.rrect(debut, y + haut - (r + 1) * h + 2, fin,
                        y + haut - r * h - 2, h * 0.14, fill=BRIQUE)
            xx += h * 2.2 + 3
    t.rrect(x, y + haut, x + large, y + haut + haut * 0.10, 3, fill=MORTIER)


def _truelle(t, cx, cy, e, angle=-0.5):
    """La truelle : une lame triangulaire et un manche. L'outil du builder."""
    co, si = math.cos(angle), math.sin(angle)
    def p(dx, dy):
        return (cx + dx * co - dy * si, cy + dx * si + dy * co)
    t.poly([p(-e * 0.55, 0), p(e * 0.1, -e * 0.28), p(e * 0.52, 0), p(e * 0.1, e * 0.28)],
           fill=ACIER, bord=INK_2, trait=2)
    t.rrect(cx + 0, cy - e * 0.09, cx + e * 0.95, cy + e * 0.09, e * 0.09, fill=MANCHE)
    t.disque((cx + e * 0.95, cy), e * 0.12, fill=CLAY)


def _scie(t, cx, cy, e):
    """La scie : lame dentée et poignée. L'outil du carpenter."""
    t.poly([(cx - e * 0.55, cy - e * 0.12), (cx + e * 0.35, cy - e * 0.12),
            (cx + e * 0.35, cy + e * 0.06), (cx - e * 0.55, cy + e * 0.06)],
           fill=ACIER, bord=INK_2, trait=2)
    n = 11
    for i in range(n):
        x = cx - e * 0.54 + i * (e * 0.88 / n)
        t.poly([(x, cy + e * 0.06), (x + e * 0.045, cy + e * 0.06),
                (x + e * 0.022, cy + e * 0.16)], fill=INK_2)
    t.rrect(cx + e * 0.33, cy - e * 0.22, cx + e * 0.62, cy + e * 0.18, e * 0.08,
            fill=MANCHE, bord=INK_2, trait=2)


def _marteau(t, cx, cy, e):
    t.rrect(cx - e * 0.07, cy - e * 0.18, cx + e * 0.07, cy + e * 0.6, e * 0.06,
            fill=MANCHE)
    t.rrect(cx - e * 0.34, cy - e * 0.42, cx + e * 0.22, cy - e * 0.16, e * 0.07,
            fill=(86, 92, 98))
    t.poly([(cx + e * 0.22, cy - e * 0.42), (cx + e * 0.40, cy - e * 0.33),
            (cx + e * 0.40, cy - e * 0.25), (cx + e * 0.22, cy - e * 0.16)],
           fill=(86, 92, 98))


def _ciseau(t, cx, cy, e, arrondi=False):
    """Un ciseau. Lame droite pour le carpenter, arrondie pour le carver."""
    t.rrect(cx - e * 0.09, cy - e * 0.5, cx + e * 0.09, cy - e * 0.02, e * 0.08,
            fill=MANCHE, bord=INK_2, trait=2)
    t.rrect(cx - e * 0.06, cy - e * 0.04, cx + e * 0.06, cy + e * 0.34, e * 0.02,
            fill=ACIER, bord=INK_2, trait=2)
    if arrondi:
        t.disque((cx, cy + e * 0.36), e * 0.09, fill=ACIER, bord=INK_2, trait=2)
    else:
        t.poly([(cx - e * 0.06, cy + e * 0.34), (cx + e * 0.06, cy + e * 0.34),
                (cx, cy + e * 0.47)], fill=ACIER)


def _mortier(t, cx, cy, e):
    """Le mortier en bois : ce que produit le wood carver."""
    t.poly([(cx - e * 0.42, cy - e * 0.3), (cx + e * 0.42, cy - e * 0.3),
            (cx + e * 0.2, cy + e * 0.42), (cx - e * 0.2, cy + e * 0.42)],
           fill=BOIS, bord=BOIS_SOMBRE, trait=3)
    t.disque((cx, cy - e * 0.3), e * 0.42, fill=BOIS_SOMBRE)
    t.disque((cx, cy - e * 0.3), e * 0.3, fill=(96, 68, 40))
    t.rrect(cx - e * 0.26, cy + e * 0.42, cx + e * 0.26, cy + e * 0.5, e * 0.04,
            fill=BOIS_SOMBRE)


def _table(t, cx, cy, e):
    """Une table en bois : ce que produit le carpenter."""
    t.rrect(cx - e * 0.5, cy - e * 0.2, cx + e * 0.5, cy - e * 0.06, e * 0.04,
            fill=BOIS, bord=BOIS_SOMBRE, trait=3)
    for s in (-1, 1):
        # Les bornes sont ordonnées : à gauche, cx + s*0.46e est plus petit que
        # cx + s*0.40e, et Pillow refuse un rectangle tracé à l’envers.
        x0, x1 = sorted((cx + s * e * 0.40, cx + s * e * 0.46))
        t.rrect(x0, cy - e * 0.06, x1, cy + e * 0.42, e * 0.03, fill=BOIS_SOMBRE)


def _etagere(t, cx, cy, e):
    t.rrect(cx - e * 0.4, cy - e * 0.42, cx + e * 0.4, cy + e * 0.42, e * 0.05,
            fill=BOIS, bord=BOIS_SOMBRE, trait=3)
    for i in range(2):
        y = cy - e * 0.14 + i * e * 0.28
        t.ligne([(cx - e * 0.4, y), (cx + e * 0.4, y)], BOIS_SOMBRE, 4)


def _clous(t, cx, cy, e, n=4):
    for i in range(n):
        x = cx - e * 0.2 + i * e * 0.13
        t.rrect(x - e * 0.016, cy - e * 0.2, x + e * 0.016, cy + e * 0.22, e * 0.01,
                fill=ACIER)
        t.disque((x, cy - e * 0.22), e * 0.045, fill=(120, 128, 136))


def _cadre(t, cx, cy, large, haut):
    t.rrect(cx - large / 2, cy - haut / 2, cx + large / 2, cy + haut / 2, 22,
            fill=(255, 255, 255, 150), bord=(255, 255, 255), trait=3)


def _titre(t, cx, cy, large, haut, titre, ton):
    fs._etiquette(t, cx, cy - haut / 2 + 34, large - 36, 48, titre, 26, ton)


# ───────────────────────── leçon 1 : les trois métiers ────────────────────

def an_metiers(t):  # 960x540
    t.texte((480, 72), 'builder · carpenter · carver', 40, INK_2)
    metiers = (('builder', SKY), ('carpenter', MINT), ('carver', SAND))
    # Le titre se pose EN DERNIER : dessiné avant, le mortier du carver lui
    # passait par-dessus et la carte n’annonçait plus rien.
    for i, _m in enumerate(metiers):
        cx = 170 + i * 310
        _cadre(t, cx, 300, 280, 330)
        if i == 0:
            _mur(t, cx - 95, 250, 190, 94, rangs=4)
            _truelle(t, cx, 400, 110)
        elif i == 1:
            _table(t, cx, 290, 230)
            _scie(t, cx, 400, 200)
        else:
            _mortier(t, cx, 310, 176)
            _ciseau(t, cx + 104, 320, 120, arrondi=True)
    for i, (titre, ton) in enumerate(metiers):
        _titre(t, 170 + i * 310, 300, 280, 330, titre, ton)
    t.texte((480, 500), 'bricks · wood · wood', 26, CLAY)


def an_builder(t):
    _mur(t, 44, 108, 232, 118, rangs=5)
    _truelle(t, 196, 254, 120)
    t.texte((160, 64), 'builder', 38, INK)
    t.texte((160, 304), 'bricks and cement', 22, CLAY)


def an_carpenter(t):
    _table(t, 150, 140, 260)
    _scie(t, 164, 240, 200)
    t.texte((160, 62), 'carpenter', 34, INK)
    t.texte((160, 304), 'things out of wood', 22, CLAY)


def an_carver(t):
    # Le mortier est large du haut : à 210 il montait jusque sous le titre,
    # qui se lisait au travers du bois.
    t.texte((160, 58), 'carver', 38, INK)
    _mortier(t, 126, 192, 168)
    _ciseau(t, 254, 186, 132, arrondi=True)
    t.texte((160, 304), 'a mortar, out of wood', 21, CLAY)


def an_outils(t):
    for i, (nom, ton) in enumerate((('trowel', SKY), ('saw', MINT), ('gouge', SAND))):
        y = 76 + i * 86
        fs._etiquette(t, 76, y, 120, 46, nom, 22, ton)
        if i == 0:
            _truelle(t, 206, y, 96, angle=-0.38)
        elif i == 1:
            _scie(t, 212, y, 150)
        else:
            _ciseau(t, 212, y - 6, 110, arrondi=True)
    t.texte((160, 302), 'one tool, one trade', 21, CLAY)


def an_boite(t):
    t.rrect(40, 150, 280, 272, 18, fill=BOIS, bord=BOIS_SOMBRE, trait=3)
    t.rrect(40, 150, 280, 174, 10, fill=BOIS_SOMBRE)
    t.rrect(136, 128, 184, 152, 8, fill=BOIS_SOMBRE)
    _marteau(t, 86, 108, 100)
    _scie(t, 186, 96, 150)
    _ciseau(t, 248, 104, 96)
    _clous(t, 160, 220, 180, n=5)
    t.texte((160, 304), 'the carpenter’s box', 21, CLAY)


def an_chisel(t):
    _ciseau(t, 100, 140, 160, arrondi=False)
    _ciseau(t, 220, 140, 160, arrondi=True)
    t.texte((100, 248), 'straight', 22, INK_2)
    t.texte((220, 248), 'rounded', 22, CLAY)
    t.texte((160, 300), 'same name, two tools', 21, CLAY)


def an_syllabes(t):
    for i, (mot, parts) in enumerate((('ham|mer', 2), ('tro|wel', 2), ('saw', 1), ('sand', 1))):
        y = 72 + i * 62
        if parts == 2:
            a, b = mot.split('|')
            la = t.pol(28).getlength(a) / fm.S
            lb = t.pol(28).getlength(b) / fm.S
            total = la + lb + 22
            x = 160 - total / 2
            fs._etiquette(t, x + la / 2, y, la + 24, 44, a, 26, MINT)
            fs._etiquette(t, x + la + 22 + lb / 2, y, lb + 24, 44, b, 26, SKY)
            t.texte((288, y), '2', 26, CLAY)
        else:
            lw = t.pol(28).getlength(mot) / fm.S
            fs._etiquette(t, 160, y, lw + 26, 44, mot, 26, SAND)
            t.texte((288, y), '1', 26, CLAY)
    t.texte((160, 304), 'clap the syllables', 21, CLAY)


# ───────────────────────── leçon 2 : les adjectifs ────────────────────────

def an_adjectifs(t):  # 960x540
    # Deux blocs de couleur pleins, pas deux lignes de texte : à la taille
    # d’une vignette de carte, une phrase fine disparaît et l’enfant ne
    # reconnaît plus sa leçon.
    t.texte((480, 70), 'kinds of adjectives', 40, INK_2)
    for i, (mot, nom, ton, note) in enumerate((
        ('sharp', 'trowel', MINT, 'common'),
        ('Cameroonian', 'carpenter', LILAC, 'proper'),
    )):
        x0 = 60 + i * 450
        t.rrect(x0, 130, x0 + 390, 460, 28, fill=ton, bord=(255, 255, 255), trait=4)
        taille = 64 if len(mot) <= 7 else 44
        if i == 1:
            # La majuscule est tout le sujet : on la met en valeur À SA PLACE
            # dans le mot. Une pastille posée à côté recouvrait le C au lieu
            # de le montrer.
            tete, reste = mot[0], mot[1:]
            lt = t.pol(taille).getlength(tete) / fm.S
            lr = t.pol(taille).getlength(reste) / fm.S
            x = x0 + 195 - (lt + lr) / 2
            t.rrect(x - 8, 230 - taille * 0.62, x + lt + 6, 230 + taille * 0.52,
                    10, fill=GOLD)
            t.texte((x + lt / 2 - 1, 230), tete, taille, WHITE_WARM)
            t.texte((x + lt + 6, 230), reste, taille, INK, 'lm')
        else:
            t.texte((x0 + 195, 230), mot, taille, INK)
        t.texte((x0 + 195, 300), nom, 36, INK_2)
        fs._etiquette(t, x0 + 195, 390, 300, 56, note, 30, WHITE_WARM)


def an_adjectif(t):
    fs._etiquette(t, 160, 160, 150, 56, 'house', 32, WHITE_WARM)
    for i, (mot, ton, dx, dy) in enumerate((('big', MINT, -96, -80), ('old', SKY, 96, -80),
                                            ('nice', LILAC, 0, 86))):
        fs._etiquette(t, 160 + dx, 160 + dy, 104, 44, mot, 24, ton)
        fs._fleche(t, (160 + dx * 0.55, 160 + dy * 0.62), (160 + dx * 0.2, 160 + dy * 0.26),
                   INK_2, 3, 9)
    t.texte((160, 294), 'they describe the noun', 20, CLAY)


def an_phrase(t):
    t.rrect(30, 110, 290, 190, 18, fill=WHITE_WARM, bord=(255, 255, 255), trait=3)
    t.texte((160, 136), 'The hammer', 26, INK)
    t.texte((160, 168), 'is heavy.', 26, INK)
    t.ligne([(140, 184), (196, 184)], CLAY, 4)
    fs._etiquette(t, 160, 234, 220, 46, 'heavier', 24, (226, 196, 190))
    t.ligne([(66, 234), (254, 234)], CLAY, 4)
    t.texte((160, 282), 'one word is not', 20, CLAY)
    t.texte((160, 306), 'a sentence', 20, CLAY)


def an_communs(t):
    for i, mot in enumerate(('a big house', 'an old carpenter', 'a wet surface',
                             'a neat workshop')):
        fs._etiquette(t, 160, 86 + i * 58, 268, 48, mot, 22, TONS[i % len(TONS)])
    t.texte((160, 300), 'no capital letter', 22, CLAY)


def an_propres(t):
    for i, (mot, reste) in enumerate((('C', 'ameroonian'), ('N', 'igerian'), ('B', 'ritish'))):
        y = 96 + i * 72
        lm = t.pol(30).getlength(mot) / fm.S
        lr = t.pol(30).getlength(reste) / fm.S
        x = 160 - (lm + lr) / 2
        fs._etiquette(t, 160, y, lm + lr + 40, 52, '', 1, TONS[i % len(TONS)])
        t.rrect(x - 6, y - 22, x + lm + 4, y + 22, 8, fill=GOLD)
        t.texte((x + lm / 2 - 1, y), mot, 30, WHITE_WARM)
        t.texte((x + lm + 4, y), reste, 30, INK, 'lm')
    t.texte((160, 300), 'from a place, with a capital', 18, CLAY)


# ───────────────────────── leçon 3 : les nombres ──────────────────────────

def an_nombres(t):  # 960x540
    # Les tuiles portent la vignette à elles seules : trois gros chiffres se
    # lisent encore à cent pixels de large, une phrase non.
    t.texte((480, 66), 'numbers 251 to 300', 38, INK_2)
    for i, c in enumerate('251'):
        fm._tuile(t, 300 + i * 180, 270, 160, 220, c, 140, (WHITE_WARM, SAND, MINT)[i])
    fm._tuile(t, 790, 270, 120, 220, '…', 80, LILAC, INK_2)
    t.texte((480, 440), 'two hundred and fifty-one', 36, INK)
    t.texte((480, 492), 'up to three hundred', 26, CLAY)


def an_lire(t):
    fm._tuile(t, 160, 96, 180, 84, '251', 60, WHITE_WARM)
    fs._fleche(t, (160, 146), (160, 186), CLAY, 5, 13)
    t.texte((160, 216), 'two hundred', 26, INK)
    t.texte((160, 250), 'and fifty-one', 26, INK)
    t.texte((160, 300), 'hundreds, and, then the rest', 18, CLAY)


def an_trait(t):
    for i, (a, b) in enumerate((('fifty', 'one'), ('sixty', 'four'), ('ninety', 'nine'))):
        y = 92 + i * 72
        la = t.pol(26).getlength(a) / fm.S
        lb = t.pol(26).getlength(b) / fm.S
        total = la + lb + 30
        x = 160 - total / 2
        t.texte((x, y), a, 26, INK, 'lm')
        t.rrect(x + la + 4, y - 5, x + la + 26, y + 5, 5, fill=CLAY)
        t.texte((x + la + 30, y), b, 26, INK, 'lm')
    t.texte((160, 300), 'never “fifty one”', 22, CLAY)


def an_trois_cents(t):
    for i, n in enumerate(('298', '299', '300')):
        fm._tuile(t, 160, 92 + i * 80, 196, 66, n, 46,
                  GOLD if n == '300' else WHITE_WARM,
                  WHITE_WARM if n == '300' else INK)
    t.texte((160, 300), 'three hundred, with no “and”', 19, CLAY)


FIGURES = [
    ('an-metiers', 960, 540, an_metiers),
    ('an-builder', 320, 320, an_builder),
    ('an-carpenter', 320, 320, an_carpenter),
    ('an-carver', 320, 320, an_carver),
    ('an-outils', 320, 320, an_outils),
    ('an-boite', 320, 320, an_boite),
    ('an-chisel', 320, 320, an_chisel),
    ('an-syllabes', 320, 320, an_syllabes),
    ('an-adjectifs', 960, 540, an_adjectifs),
    ('an-adjectif', 320, 320, an_adjectif),
    ('an-phrase', 320, 320, an_phrase),
    ('an-communs', 320, 320, an_communs),
    ('an-propres', 320, 320, an_propres),
    ('an-nombres', 960, 540, an_nombres),
    ('an-lire', 320, 320, an_lire),
    ('an-trait', 320, 320, an_trait),
    ('an-trois-cents', 320, 320, an_trois_cents),
]


def controler():
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'
    assert len(FIGURES) == 17, 'dix-sept figures attendues : %d' % len(FIGURES)


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
        print('  %-18s %4dx%-4d %6.1f Ko' % (cle, w, h, poids / 1024))
    print('%d figures - %.1f Ko - 0 credit' % (len(FIGURES), total / 1024))
