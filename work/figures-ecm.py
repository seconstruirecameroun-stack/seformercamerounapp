# -*- coding: utf-8 -*-
"""
Les figures de la leçon « Les droits de l-enfant » — ECM, BRAYNE (CM1).

Sept images dessinées, aucune générée. Le problème propre à cette leçon
est qu-elle ne parle d-aucun objet : un droit ne se photographie pas.
L-enfant doit pourtant distinguer trois droits qui se ressemblent par les
mots — le nom, la nationalité, l-identité — et que seules les questions
sépareront.

Le parti pris est donc de donner à chaque droit **le papier qui le prouve**,
parce que c-est ce qu-un enfant camerounais a déjà vu passer à la maison :

  le nom           une étiquette qui rattache l-enfant à une maison. Le
                   cahier dit « relie à une famille » : la figure relie,
                   avec un trait qu-on peut suivre du doigt
  la nationalité   le Cameroun, et c-est **la même silhouette** que dans la
                   leçon de géographie. Deux dessins du même pays finiraient
                   par diverger, et le pays de la nationalité ne serait plus
                   celui des zones agricoles
  l-identité       l-acte de naissance, avec ses cinq lignes exactement :
                   nom, nationalité, date et lieu, sexe, parents. Un enfant
                   qui compte les lignes de la figure retrouve les cinq
                   mentions du cahier

Usage :  python work/figures-ecm.py
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
cc = _charger('carte_cameroun', 'carte-cameroun.py')
fv = _charger('figures_venn', 'figures-venn.py')

Toile, SORTIE = fm.Toile, fm.SORTIE
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

VERT_PALE = (206, 221, 199)
TERRE = (168, 122, 86)

# Les cinq mentions de l-acte de naissance, dans l-ordre du cahier. La
# figure et la leçon lisent la même liste : si le cahier en ajoutait une,
# il n-y aurait qu-un endroit à corriger.
MENTIONS = ('le nom', 'la nationalité', 'la date et le lieu', 'le sexe', 'les parents')

# La bande d-une couverture 960x540 que le bandeau d-une leçon montre
# réellement, mesurée dans l-application : le reste est rogné.
BANDEAU = (184, 356)


# --------------------------------------------------------------------------
# Les briques communes

def _carte(t, boite, remplissage=VERT_PALE, trait=2.0):
    """Le Cameroun, repris tel quel de la leçon de géographie."""
    pts = cc.contour(boite)
    t.poly(pts, fill=remplissage)
    t.ligne(pts + [pts[0]], INK, trait)


def _maison(t, cx, cy, l=44):
    """Une maison : le mur, le toit, la porte. C-est la famille."""
    h = l * 0.78
    t.rrect(cx - l / 2, cy - h / 2, cx + l / 2, cy + h / 2, 3, fill=SAND, bord=INK, trait=2)
    t.poly([(cx - l * 0.62, cy - h / 2), (cx, cy - h * 1.05), (cx + l * 0.62, cy - h / 2)],
           fill=CLAY, bord=INK, trait=2)
    t.rrect(cx - l * 0.13, cy + h / 2 - l * 0.34, cx + l * 0.13, cy + h / 2, 2,
            fill=TERRE, bord=INK, trait=1.5)


def _etiquette(t, cx, cy, l=74, h=44, mot=None, taille=15):
    """Une étiquette percée, celle qu-on attache à quelque chose."""
    t.poly([(cx - l / 2, cy - h / 2), (cx + l / 2 - h * 0.42, cy - h / 2),
            (cx + l / 2, cy), (cx + l / 2 - h * 0.42, cy + h / 2),
            (cx - l / 2, cy + h / 2)],
           fill=WHITE_WARM, bord=INK, trait=2)
    # Un trou de la taille d-une lettre se lit comme une lettre : la
    # première version donnait « O NOM ». Il est plus petit et plus au bord.
    t.disque((cx - l / 2 + h * 0.19, cy), h * 0.075, fill=None, bord=INK_2, trait=1.3)
    if mot:
        t.texte((cx + l * 0.02, cy), mot, taille, INK)


def _carte_identite(t, x0, y0, x1, y1, titre='IDENTITÉ', mentions=MENTIONS, taille=12):
    """L-acte de naissance : une photo, un titre, et SES cinq lignes."""
    t.rrect(x0, y0, x1, y1, 7, fill=WHITE_WARM, bord=INK, trait=2.2)
    bande = y0 + (y1 - y0) * 0.19
    t.rrect(x0, y0, x1, bande, 7, fill=BLEU)
    t.rrect(x0, bande - 7, x1, bande, 0, fill=BLEU)
    t.texte(((x0 + x1) / 2, (y0 + bande) / 2), titre, taille + 2, WHITE_WARM)

    # La photo : un visage, parce qu-un acte de naissance est celui de
    # quelqu-un et pas d-un dossier.
    ph = (x1 - x0) * 0.26
    px0, py0 = x0 + (x1 - x0) * 0.07, bande + (y1 - bande) * 0.13
    t.rrect(px0, py0, px0 + ph, py0 + ph * 1.12, 4, fill=SKY, bord=INK, trait=1.6)
    t.disque((px0 + ph / 2, py0 + ph * 0.38), ph * 0.19, fill=SAND, bord=INK, trait=1.4)
    t.d.pieslice([int((px0 + ph * 0.18) * fm.S), int((py0 + ph * 0.56) * fm.S),
                  int((px0 + ph * 0.82) * fm.S), int((py0 + ph * 1.3) * fm.S)],
                 180, 360, fill=CLAY, outline=INK, width=int(1.4 * fm.S))

    lx = px0 + ph + (x1 - x0) * 0.08
    haut, bas = py0, y1 - (y1 - y0) * 0.09
    pas = (bas - haut) / len(mentions)
    for i, mot in enumerate(mentions):
        y = haut + pas * (i + 0.5)
        t.ligne([(lx, y + pas * 0.33), (x1 - (x1 - x0) * 0.07, y + pas * 0.33)], INK_2, 1.2)
        t.texte((lx, y), mot, taille, INK, ancre='lm')


def _fleche(t, a, b, couleur=CLAY, trait=2.6, tete=9):
    """Un trait qui relie, avec une pointe : on voit ce qui va vers quoi."""
    import math
    t.ligne([a, b], couleur, trait)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for d in (2.5, -2.5):
        t.ligne([b, (b[0] + tete * math.cos(ang + d), b[1] + tete * math.sin(ang + d))],
                couleur, trait)


# --------------------------------------------------------------------------
# Les figures

def fig_couverture(t):
    """Trois droits, trois papiers, sous un même article.

    Tout tient dans la bande 184-356. Ce n-est pas une marge de confort :
    le bandeau d-une leçon ne montre QUE cette bande, et la première
    version, dessinée large, s-y présentait avec ses trois cartes coupées
    en deux. Le titre n-est pas dessiné non plus — l-application écrit le
    sien par-dessus, et deux titres superposés ne se lisent ni l-un ni
    l-autre.
    """
    # Le bandeau de l-article : il tient les trois cartes ensemble, parce
    # que le cahier les donne comme TROIS droits du MÊME article.
    t.rrect(300, 190, 660, 224, 16, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 207), 'article 7 de la C.D.E', 17, INK)

    for cx, titre, dessin in (
        (232, 'le nom', 'nom'),
        (480, 'la nationalité', 'pays'),
        (728, 'l’identité', 'acte'),
    ):
        t.rrect(cx - 100, 238, cx + 100, 350, 14, fill=WHITE_WARM, bord=INK, trait=2.2)
        t.texte((cx, 334), titre, 16, INK)
        if dessin == 'nom':
            _etiquette(t, cx, 283, 104, 48, 'NOM', 16)
        elif dessin == 'pays':
            _carte(t, (cx - 34, 250, cx + 34, 316))
        else:
            _carte_identite(t, cx - 78, 250, cx + 78, 318, 'IDENTITÉ',
                            ('nom', 'nationalité'), 9)


def fig_article7(t):
    """Un livre ouvert, et le numéro que le cahier donne."""
    t.ombre(160, 268, 104, 14)
    t.rrect(42, 86, 278, 250, 8, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.ligne([(160, 86), (160, 250)], INK_2, 1.8)
    for y in (116, 136, 156, 176, 196):
        t.ligne([(58, y), (146, y)], INK_2, 1.4)
    t.texte((210, 130), 'ARTICLE', 13, INK_2)
    t.texte((210, 186), '7', 62, CLAY)
    # Le signet : on revient toujours à la même page. Il est à droite du mot
    # « ARTICLE », qu-il recouvrait dans la première version.
    t.poly([(250, 86), (268, 86), (268, 134), (259, 123), (250, 134)],
           fill=CLAY, bord=INK, trait=1.8)
    t.texte((160, 282), 'l’article 7', 19, INK)


def fig_cide(t):
    """La convention : un texte signé, pas une idée en l-air."""
    t.ombre(160, 272, 92, 13)
    t.rrect(56, 64, 264, 256, 9, fill=BLEU, bord=INK, trait=2.4)
    t.rrect(56, 112, 264, 160, 0, fill=WHITE_WARM)
    t.texte((160, 136), 'C.D.E', 38, INK)
    t.texte((160, 88), 'CONVENTION', 15, WHITE_WARM)
    for y in (186, 206):
        t.ligne([(84, y), (236, y)], (255, 251, 244, 150), 2)
    # Le sceau : c-est ce qui fait qu-un papier protège.
    t.disque((218, 228), 20, fill=GOLD, bord=INK, trait=2)
    t.disque((218, 228), 12, fill=None, bord=INK, trait=1.4)
    t.texte((160, 290), 'des Droits de l’Enfant', 17, INK)


def fig_nom(t):
    """L-étiquette et la maison, reliées. Le cahier dit « relie »."""
    _etiquette(t, 86, 150, 108, 56, 'NOM', 18)
    _maison(t, 242, 150, 76)
    _fleche(t, (146, 150), (196, 150))
    t.texte((160, 232), 'le nom relie l’enfant', 17, INK)
    t.texte((160, 262), 'à une famille', 17, INK)
    # De sang ou adoptive : le cahier le précise, la figure aussi.
    t.rrect(44, 284, 276, 312, 12, fill=MINT, bord=INK, trait=1.6)
    t.texte((160, 298), 'de sang ou adoptive', 14, INK)


def _enfant(t, cx, cy, r=20):
    """Un enfant : une tête et des épaules. C-est lui qu-on rattache."""
    t.disque((cx, cy), r, fill=SAND, bord=INK, trait=2)
    t.d.pieslice([int((cx - r * 1.5) * fm.S), int((cy + r * 0.55) * fm.S),
                  int((cx + r * 1.5) * fm.S), int((cy + r * 3.2) * fm.S)],
                 180, 360, fill=CLAY, outline=INK, width=int(2 * fm.S))


def fig_nationalite(t):
    """Même image que le nom, autre destination : c-est là qu-est la leçon."""
    _enfant(t, 84, 136, 24)
    _carte(t, (186, 64, 282, 206))
    _fleche(t, (130, 148), (174, 148))
    t.texte((160, 238), 'la nationalité rattache', 17, INK)
    t.texte((160, 268), 'l’enfant à un pays', 17, INK)
    t.rrect(36, 288, 284, 314, 12, fill=MINT, bord=INK, trait=1.6)
    t.texte((160, 301), 'celui des parents, ou de sa naissance', 12, INK)


def fig_identite(t):
    """Cinq mentions, cinq lignes. On peut les compter."""
    _carte_identite(t, 26, 52, 294, 258)
    t.texte((160, 288), 'cinq mentions', 18, INK)


def fig_trois(t):
    """Les trois droits côte à côte : c-est leur différence qu-on révise."""
    for i, (mot, detail) in enumerate((
        ('le nom', 'une famille'),
        ('la nationalité', 'un pays'),
        ('l’identité', 'cinq mentions'),
    )):
        y = 92 + i * 76
        t.rrect(30, y - 30, 290, y + 30, 14, fill=WHITE_WARM, bord=INK, trait=2)
        t.disque((64, y), 15, fill=(GOLD, SKY, MINT)[i], bord=INK, trait=1.8)
        t.texte((64, y), str(i + 1), 17, INK)
        t.texte((92, y - 10), mot, 17, INK, ancre='lm')
        t.texte((92, y + 12), detail, 13, INK_2, ancre='lm')
    t.texte((160, 290), 'article 7', 18, INK)


FIGURES = [
    ('dr-droits-couv', 960, 540, fig_couverture),
    ('dr-article7', 320, 320, fig_article7),
    ('dr-cide', 320, 320, fig_cide),
    ('dr-nom', 320, 320, fig_nom),
    ('dr-nationalite', 320, 320, fig_nationalite),
    ('dr-identite', 320, 320, fig_identite),
    ('dr-trois', 320, 320, fig_trois),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # Les cinq mentions du cahier doivent être cinq sur la figure. Une
    # figure qui en montrerait quatre enseignerait le contraire de la
    # question qui demande combien il y en a.
    assert len(MENTIONS) == 5, MENTIONS

    # Rien ne doit toucher le bord du cadre : un dessin coupé se lit mal et
    # donne l-impression d-une image ratée.
    for cle, w, h, fabrique in FIGURES:
        t = Toile(w, h)
        fabrique(t)
        im = t.fini().convert('RGB')
        fond = im.getpixel((2, 2))
        for x in range(0, w, 3):
            for y in (1, h - 2):
                p = im.getpixel((x, y))
                assert sum(abs(a - b) for a, b in zip(p, fond)) < 90, \
                    '%s : le dessin touche le bord en (%d, %d)' % (cle, x, y)

        # Sur une couverture, rien d-important ne doit sortir de la bande
        # que l-application montre réellement.
        if (w, h) == (960, 540):
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
