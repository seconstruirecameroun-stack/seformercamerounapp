# -*- coding: utf-8 -*-
"""
Les figures des cinq leçons de mathématiques de BRAYNE (CM1) —
contrôle du 30 octobre et remédiation du 4 novembre 2026.

Ces leçons-là ne s-illustrent pas par des scènes : ce sont des **outils**.
Une conversion de capacité se comprend sur l-échelle des unités, une
moyenne sur le tableau de notes, un pourcentage sur une barre partagée en
cent. Dessiner autre chose apprendrait autre chose que ce qu-on demandera.

Quatre instruments, et les figures en sortent :

  echelle      kl hl dal l dl cl ml, avec les cases qu-on remplit de zéros.
               C-est l-outil que la maîtresse fait tracer, et la faute de
               BRAYNE (2 hl 5 l écrit 250 dl au lieu de 2050) se voit
               dessus : il a oublié une case
  notes        le tableau de notes, la somme et la division. La moyenne est
               une opération, pas une idée
  barre        cent carrés, la part colorée. 240 sur 300 ne se sent pas,
               mais 80 carrés sur 100 se voient
  triangle     les droites remarquables, chacune avec ce qui la définit :
               la médiane va au MILIEU du côté, la hauteur tombe à angle
               DROIT. C-est cette différence que l-exercice demande

Usage :  python work/figures-brayne-maths-nov.py
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
ROUGE = (183, 66, 52)
TERRE = (168, 122, 86)

# La bande qu-un bandeau de leçon montre réellement d-une couverture.
BANDEAU = (184, 356)

UNITES = ('kl', 'hl', 'dal', 'l', 'dl', 'cl', 'ml')


# --------------------------------------------------------------------------
# Les instruments

def _mesure(t, s, taille):
    return t.d.textlength(s, font=t.pol(taille)) / S


def _pastille(t, cx, cy, mot, taille, fond=WHITE_WARM, couleur=INK, marge=10, h=None):
    w = _mesure(t, mot, taille) + marge * 2
    h = h if h else taille + 14
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill=fond, bord=INK, trait=1.8)
    t.texte((cx, cy), mot, taille, couleur)
    return w


def echelle(t, chiffres=None, surligne=(), haut=96, bas=168, gauche=14, droite=306, note=None):
    """L-échelle des capacités, et ce qu-on écrit dans les cases.

    `chiffres` donne une case par unité : un chiffre, un point pour la
    virgule, ou None pour laisser vide. C-est là que se voit la faute de
    recopie : une case oubliée décale tout le nombre.
    """
    larg = (droite - gauche) / len(UNITES)
    for i, u in enumerate(UNITES):
        x = gauche + larg * i
        vif = u in surligne
        t.rrect(x + 1, haut, x + larg - 1, bas, 6,
                fill=(GOLD if vif else WHITE_WARM), bord=INK, trait=1.8)
        t.texte((x + larg / 2, haut + 15), u, 13, INK_2)
        if chiffres and i < len(chiffres) and chiffres[i] is not None:
            t.texte((x + larg / 2, bas - 20), str(chiffres[i]), 20, INK)
    # Le litre est l-unité de référence : on l-ancre.
    xl = gauche + larg * (UNITES.index('l') + 0.5)
    t.ligne([(xl, bas + 4), (xl, bas + 14)], CLAY, 2.2)
    t.texte((xl, bas + 26), 'unité', 12, CLAY)
    if note:
        t.texte(((gauche + droite) / 2, bas + 56), note, 15, INK)


def notes(t, valeurs, somme=None, moyenne=None, haut=80, gauche=24, droite=296):
    """Le tableau de notes, la somme, puis la division."""
    larg = (droite - gauche) / len(valeurs)
    for i, v in enumerate(valeurs):
        x = gauche + larg * i
        t.rrect(x + 2, haut, x + larg - 2, haut + 46, 6, fill=WHITE_WARM, bord=INK, trait=1.8)
        t.texte((x + larg / 2, haut + 23), str(v), 18, INK)
    if somme is not None:
        t.texte((160, haut + 86), 'somme : %d' % somme, 18, INK)
    if moyenne is not None:
        t.texte((160, haut + 124), '%d ÷ %d' % (somme, len(valeurs)), 16, INK_2)
        _pastille(t, 160, haut + 164, 'moyenne : %d' % moyenne, 18, fond=GOLD, marge=16)


def barre(t, part, total, note=None):
    """Cent carrés, la part colorée. Un pourcentage se compte, il ne se sent pas.

    Le carré fait 15 px : dix rangées tiennent alors dans 150 px, et il
    reste la place d-écrire dessous. La première version calculait sa
    taille sur la largeur disponible et débordait du cadre par le bas.
    """
    pc = round(100 * part / total)
    cote, haut, gauche = 15, 62, 85
    for k in range(100):
        x = gauche + cote * (k % 10)
        y = haut + cote * (k // 10)
        t.rrect(x + 1, y + 1, x + cote - 1, y + cote - 1, 2,
                fill=(CLAY if k < pc else WHITE_WARM), bord=INK_2, trait=1)
    bas = haut + cote * 10
    t.texte((160, bas + 22), '%d sur %d' % (part, total), 15, INK_2)
    _pastille(t, 160, bas + 56, '%d %%' % pc, 22, fond=GOLD, marge=18)
    if note:
        t.texte((160, bas + 88), note, 14, INK)


def _sommets():
    # Volontairement QUELCONQUE, et non isocèle. Sur un triangle presque
    # isocèle, la médiane et la hauteur issues du même sommet se
    # superposent à l-œil — la figure enseignerait alors qu-elles sont la
    # même droite, ce que l-exercice demande justement de distinguer.
    return [(60, 234), (262, 234), (104, 92)]


def triangle(t, quoi=None, titre=None):
    """Le triangle et SA droite remarquable, celle qui le définit."""
    A, B, C = _sommets()
    t.poly([A, B, C], fill=MINT, bord=INK, trait=2.4)
    for p, nom in ((A, 'A'), (B, 'B'), (C, 'C')):
        t.texte((p[0] + (-14 if p is A else 14 if p is B else 0), p[1] + (12 if p is not C else -16)),
                nom, 15, INK_2)

    if quoi == 'mediane':
        M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
        t.ligne([C, M], CLAY, 2.6)
        t.disque(M, 4, fill=CLAY)
        t.texte((M[0], M[1] + 20), 'milieu', 13, CLAY)
    elif quoi == 'hauteur':
        H = (C[0], B[1])
        t.ligne([C, H], CLAY, 2.6)
        t.rrect(H[0] - 10, H[1] - 10, H[0], H[1], 0, fill=None, bord=CLAY, trait=1.8)
        t.texte((H[0] + 72, H[1] - 14), 'angle droit', 13, CLAY)
    elif quoi == 'bissectrice':
        t.ligne([C, ((A[0] + B[0]) / 2 + 20, 230)], CLAY, 2.6)
        t.texte((160, 258), 'coupe l’angle en deux', 13, CLAY)

    if titre:
        t.texte((160, 288), titre, 17, INK)


def angle(t, degres, nom, cx=160, cy=170, r=78):
    """Un angle, dessiné à sa vraie mesure. Un angle droit faux n-enseigne rien."""
    a = math.radians(degres)
    p1 = (cx + r, cy)
    p2 = (cx + r * math.cos(a), cy - r * math.sin(a))
    t.ligne([p1, (cx, cy)], INK, 3)
    t.ligne([(cx, cy), p2], INK, 3)
    if abs(degres - 90) < 0.5:
        t.rrect(cx, cy - 16, cx + 16, cy, 0, fill=None, bord=CLAY, trait=2)
    else:
        t.d.arc([int((cx - 30) * S), int((cy - 30) * S), int((cx + 30) * S), int((cy + 30) * S)],
                -int(degres), 0, fill=CLAY, width=int(2.4 * S))
    t.disque((cx, cy), 4, fill=INK)
    _pastille(t, cx, cy + 56, '%s · %d°' % (nom, degres), 17, fond=GOLD, marge=16)


def pile(t, etiquettes, titre=None, haut=84):
    """Une opération posée, ligne à ligne, comme au cahier."""
    if titre:
        t.texte((160, haut - 24), titre, 16, INK)
    for i, (gauche_, droite_) in enumerate(etiquettes):
        y = haut + i * 44
        t.rrect(24, y, 296, y + 36, 9, fill=WHITE_WARM, bord=INK, trait=1.8)
        t.texte((40, y + 18), gauche_, 14, INK, ancre='lm')
        t.texte((280, y + 18), droite_, 15, CLAY, ancre='rm')


def _bandeau_couv(t, titre, sous=None):
    w = _mesure(t, titre, 26) + 56
    t.rrect(480 - w / 2, 192, 480 + w / 2, 232, 20, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 212), titre, 26, INK)
    if sous:
        t.texte((480, 340), sous, 17, INK)


# --------------------------------------------------------------------------
# Les figures

def couv_capacite(t):
    _bandeau_couv(t, 'Les mesures de capacité')
    larg = 96
    for i, u in enumerate(UNITES):
        x = 480 - larg * 3.5 + larg * i
        vif = u == 'l'
        t.rrect(x + 3, 262, x + larg - 3, 330, 8, fill=(GOLD if vif else WHITE_WARM), bord=INK, trait=2)
        t.texte((x + larg / 2, 296), u, 22, INK)


def couv_moyenne(t):
    _bandeau_couv(t, 'La moyenne')
    for i, v in enumerate((15, 18, 10, 12, 10)):
        _pastille(t, 268 + i * 106, 282, str(v), 22, marge=18)
    _pastille(t, 480, 334, 'moyenne : 13', 20, fond=GOLD, marge=18)


def couv_pourcentage(t):
    _bandeau_couv(t, 'Le pourcentage')
    larg = 26
    for k in range(20):
        x = 480 - larg * 10 + larg * k
        t.rrect(x + 2, 266, x + larg - 2, 266 + larg - 4, 3,
                fill=(CLAY if k < 16 else WHITE_WARM), bord=INK_2, trait=1.2)
    _pastille(t, 480, 328, '80 % de réussite', 20, fond=GOLD, marge=18)


def couv_problemes(t):
    _bandeau_couv(t, 'Les problèmes')
    for i, (haut_, bas_) in enumerate((('7 500 F', 'arachides'), ('6 000 F', 'maïs'),
                                       ('21 000 F', 'pistaches'))):
        cx = 260 + i * 220
        t.rrect(cx - 92, 258, cx + 92, 332, 12, fill=WHITE_WARM, bord=INK, trait=2)
        t.texte((cx, 284), haut_, 22, INK)
        t.texte((cx, 314), bas_, 15, INK_2)


def couv_geometrie(t):
    _bandeau_couv(t, 'Angles et triangles')
    for i, (deg, nom) in enumerate(((45, 'aigu'), (90, 'droit'), (130, 'obtus'), (180, 'plat'))):
        cx = 216 + i * 176
        a = math.radians(deg)
        r = 52
        t.ligne([(cx + r, 318), (cx, 318)], INK, 2.6)
        t.ligne([(cx, 318), (cx + r * math.cos(a), 318 - r * math.sin(a))], INK, 2.6)
        t.disque((cx, 318), 3.5, fill=INK)
        t.texte((cx, 340), nom, 15, INK)


FIGURES = [
    # Les mesures de capacité
    ('bm-cap-couv', 960, 540, couv_capacite),
    ('bm-cap-echelle', 320, 320,
     lambda t: echelle(t, surligne=('l',), note='du plus grand au plus petit')),
    ('bm-cap-litre', 320, 320,
     lambda t: echelle(t, chiffres=[None, '2', '0', '5', '0', None, None], surligne=('hl', 'dl'),
                       note='2 hl 5 l = 2 050 dl')),
    ('bm-cap-petites', 320, 320,
     lambda t: echelle(t, chiffres=[None, None, None, None, '1', '2', '0'], surligne=('cl', 'ml'),
                       note='120 ml = 12 cl')),
    ('bm-cap-somme', 320, 320,
     lambda t: pile(t, [('560 l', '560'), ('+ 440 l', '440'), ('= 1 000 l', '1 000 l'),
                        ('soit', '100 dal')], 'Un fût de 560 l')),
    ('bm-cap-zero', 320, 320,
     lambda t: echelle(t, chiffres=[None, '5', '2', '8', '0', '0', '0'], surligne=('hl', 'ml'),
                       note='5 hl 28 l = 528 000 ml')),
    # La moyenne
    ('bm-moy-couv', 960, 540, couv_moyenne),
    ('bm-moy-table', 320, 320, lambda t: notes(t, (15, 18, 10, 12, 10), 65, 13)),
    ('bm-moy-somme', 320, 320,
     lambda t: pile(t, [('on additionne tout', '65'), ('on compte les notes', '5'),
                        ('on divise', '65 ÷ 5'), ('la moyenne', '13')], 'En trois gestes')),
    ('bm-moy-manque', 320, 320,
     lambda t: pile(t, [('total des cinq notes', '70'), ('les quatre connues', '57'),
                        ('celle qui manque', '70 − 57'), ('la note de TIC', '13')],
                    'Trouver la note qui manque')),
    ('bm-moy-sens', 320, 320, lambda t: notes(t, (14, 12, 15, 13, 16), 70, 14)),
    # Le pourcentage
    ('bm-pc-couv', 960, 540, couv_pourcentage),
    ('bm-pc-barre', 320, 320, lambda t: barre(t, 240, 300, note='240 reçus sur 300')),
    ('bm-pc-formule', 320, 320,
     lambda t: pile(t, [('réussite', '240 × 100'), ('on divise par', '300'),
                        ('ce qui donne', '80 %')], 'La règle')),
    ('bm-pc-echec', 320, 320, lambda t: barre(t, 60, 300, note='60 recalés sur 300')),
    ('bm-pc-cent', 320, 320,
     lambda t: pile(t, [('réussite', '80 %'), ('échec', '20 %'), ('ensemble', '100 %')],
                    'Les deux font cent')),
    ('bm-pc-autre', 320, 320, lambda t: barre(t, 600, 800, note='600 reçus sur 800')),
    # Les problèmes
    ('bm-pb-couv', 960, 540, couv_problemes),
    ('bm-pb-partage', 320, 320,
     lambda t: pile(t, [('arachides', '7 500 F'), ('maïs', '6 000 F'), ('pistaches', '21 000 F'),
                        ('ensemble', '34 500 F')], 'Les gains du champ')),
    ('bm-pb-division', 320, 320,
     lambda t: pile(t, [('à partager', '34 500 F'), ('entre', '3 femmes'),
                        ('chacune reçoit', '11 500 F')], 'Partager équitablement')),
    ('bm-pb-achat', 320, 320,
     lambda t: pile(t, [('28 barres à 400 F', '11 200 F'), ('15 kg de riz à 200 F', '3 000 F'),
                        ('somme reçue', '14 200 F')], 'Chez l’épicier')),
    ('bm-pb-masse', 320, 320,
     lambda t: pile(t, [('70 moutons', '70'), ('chacun pèse', '75 kg'),
                        ('masse totale', '5 250 kg')], 'La camionnette')),
    ('bm-pb-etapes', 320, 320,
     lambda t: pile(t, [('1. lire ce qu’on cherche', ''), ('2. poser l’opération', ''),
                        ('3. calculer', ''), ('4. écrire la phrase-réponse', '')],
                    'Un problème se fait en quatre temps')),
    # Angles et triangles
    ('bm-geo-couv', 960, 540, couv_geometrie),
    ('bm-geo-aigu', 320, 320, lambda t: angle(t, 45, 'aigu')),
    ('bm-geo-droit', 320, 320, lambda t: angle(t, 90, 'droit')),
    ('bm-geo-obtus', 320, 320, lambda t: angle(t, 130, 'obtus')),
    ('bm-geo-plat', 320, 320, lambda t: angle(t, 180, 'plat')),
    ('bm-geo-mediane', 320, 320, lambda t: triangle(t, 'mediane', 'la médiane va au milieu')),
    ('bm-geo-hauteur', 320, 320, lambda t: triangle(t, 'hauteur', 'la hauteur tombe à angle droit')),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # L-échelle des capacités doit être complète et dans l-ordre : c-est
    # elle qui fait la conversion, et une unité oubliée décale tout.
    assert UNITES == ('kl', 'hl', 'dal', 'l', 'dl', 'cl', 'ml'), UNITES

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
        for y in range(0, h, 3):
            for x in (1, w - 2):
                p = im.getpixel((x, y))
                assert sum(abs(a - b) for a, b in zip(p, fond)) < 90, \
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
