# -*- coding: utf-8 -*-
"""
Les figures des huit leçons sur les nombres décimaux — fiche de révision
CM1 « REVISION SHEET - DECIMAL NUMBERS », 3 pages, donnée par le père le
8 novembre 2026.

UN NOMBRE DÉCIMAL EST UNE AFFAIRE DE COLONNES, et toutes les fautes de ce
chapitre sont des fautes de colonne : comparer 2.05 à 2.5 sans aligner,
poser une addition sans aligner les virgules, arrondir en regardant le
mauvais chiffre. Les figures montrent donc des COLONNES, toujours les
mêmes, dans le même ordre, avec la virgule au même endroit. Une leçon de
place value illustrée par autre chose que la place des chiffres
n-illustrerait rien.

Trois instruments, et les quarante et une figures en sortent :

  tableau      les colonnes nommées - tens, units, tenths, hundredths,
               thousandths - et le nombre posé dedans, un chiffre par
               case. La colonne qu-on examine s-allume
  colonne      l-opération posée, les virgules alignées à la verticale.
               Le trait vertical de la virgule est tracé : c-est lui que
               l-enfant doit voir avant de calculer
  fiche        le calcul en trois temps, ligne à ligne, comme au cahier

Usage :  python work/figures-brayne-decimaux.py
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

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

ROUGE = (183, 66, 52)
BANDEAU = (184, 356)

# Les colonnes, dans l-ordre, de la plus grande à la plus petite. Le point
# est une colonne à part : il n-est pas un chiffre, et une figure qui le
# rangerait parmi les chiffres enseignerait une faute.
COLONNES = ('tens', 'units', '.', 'tenths', 'hundredths', 'thousandths')


def _mesure(t, s, taille):
    return t.d.textlength(s, font=t.pol(taille)) / S


def _legende(t, y, mot, taille=16, couleur=INK_2, large=288, cx=160):
    while _mesure(t, mot, taille) > large and taille > 9:
        taille -= 1
    t.texte((cx, y), mot, taille, couleur)


# --------------------------------------------------------------------------
# Le tableau de position

def tableau(t, chiffres, surligne=(), haut=96, bas=176, gauche=14, droite=306,
            noms=True):
    """Les colonnes nommées, et le nombre posé dedans, un chiffre par case.

    `chiffres` donne une case par colonne de COLONNES, ou None pour la
    laisser vide. La colonne du point est étroite : elle ne porte pas un
    chiffre, et lui donner la même largeur qu-aux autres ferait croire le
    contraire.
    """
    assert len(chiffres) == len(COLONNES)
    poids = [1.0 if c != '.' else 0.42 for c in COLONNES]
    somme = sum(poids)
    x = gauche
    for i, (nom, p) in enumerate(zip(COLONNES, poids)):
        larg = (droite - gauche) * p / somme
        vif = nom in surligne
        t.rrect(x + 1, haut, x + larg - 1, bas, 6,
                fill=(GOLD if vif else WHITE_WARM), bord=INK, trait=1.8)
        if noms and nom != '.':
            court = {'hundredths': 'hund.', 'thousandths': 'thou.'}.get(nom, nom)
            taille = 11
            while _mesure(t, court, taille) > larg - 6 and taille > 7:
                taille -= 1
            t.texte((x + larg / 2, haut + 14), court, taille, INK_2)
        if chiffres[i] is not None:
            t.texte((x + larg / 2, bas - 22), str(chiffres[i]), 22, INK)
        x += larg


def nombre_pose(t, chiffres, surligne=(), titre=None, legende=None):
    if titre:
        _legende(t, 62, titre, 18, INK)
    tableau(t, chiffres, surligne)
    if legende:
        _legende(t, 220, legende, 16, INK)


# --------------------------------------------------------------------------
# L-opération posée, virgules alignées

def colonne(t, lignes, signe=None, trait_apres=None, haut=90, legende=None, titre=None):
    """Une opération posée, les virgules à la verticale les unes des autres.

    Les nombres sont alignés sur leur point, et non à droite : c-est la
    règle de la leçon, et une figure alignée à droite montrerait exactement
    la faute qu-on veut lui éviter.
    """
    gauche, point_x = 90, 196
    # Le repère vertical se trace AVANT les nombres : tracé après, il
    # passait exactement sur les virgules et les effaçait toutes.
    t.pointille((point_x, haut - 30), (point_x, haut + len(lignes) * 44 - 18),
                (214, 186, 160), 1.6, pas=7)
    for i, texte in enumerate(lignes):
        y = haut + i * 44
        avant, _, apres = texte.partition('.')
        t.texte((point_x - 4, y), avant, 24, INK, ancre='rm')
        if apres != '' or '.' in texte:
            t.texte((point_x, y), '.', 24, CLAY, ancre='mm')
            t.texte((point_x + 6, y), apres, 24, INK, ancre='lm')
        if signe and i == len(lignes) - 2 and trait_apres is None:
            t.texte((gauche - 40, y), signe, 24, INK)
        if trait_apres is not None and i == trait_apres:
            t.ligne([(44, y + 22), (276, y + 22)], INK, 2)
        if signe and trait_apres is not None and i == trait_apres:
            t.texte((56, y), signe, 24, INK)
    bas = haut + len(lignes) * 44
    if titre:
        _legende(t, haut - 46, titre, 18, INK)
    if legende:
        _legende(t, bas + 14, legende, 16, INK)


def fiche(t, titre, lignes, haut=92, vif=()):
    """Le calcul posé ligne à ligne, comme au cahier."""
    _legende(t, haut - 28, titre, 17, INK)
    for i, ligne in enumerate(lignes):
        y = haut + i * 44
        t.rrect(22, y, 298, y + 36, 9,
                fill=(GOLD if i in vif else WHITE_WARM), bord=INK, trait=1.8)
        taille = 16
        while _mesure(t, ligne, taille) > 252 and taille > 10:
            taille -= 1
        t.texte((160, y + 18), ligne, taille, INK)


# --------------------------------------------------------------------------
# Les couvertures

def _bandeau(t, titre):
    w = _mesure(t, titre, 26) + 56
    t.rrect(480 - w / 2, 192, 480 + w / 2, 232, 20, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 212), titre, 26, INK)


def _couv_cadre(t, titre, texte, taille=28):
    _bandeau(t, titre)
    w = _mesure(t, texte, taille) + 72
    t.rrect(480 - w / 2, 258, 480 + w / 2, 326, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.texte((480, 292), texte, taille, INK)


def couv_position(t):
    _bandeau(t, 'Decimal place value')
    tableau(t, ['3', '4', None, '7', '2', '8'], ('tenths',),
            haut=252, bas=332, gauche=280, droite=680)


def couv_comparer(t):
    _couv_cadre(t, 'Comparing and ordering decimals', '2.500 > 2.050')


def couv_arrondir(t):
    _couv_cadre(t, 'Rounding decimals', '3.276 = 3.28')


def couv_significatifs(t):
    _couv_cadre(t, 'Significant figures', '526.8 = 527')


def couv_fractions(t):
    _couv_cadre(t, 'Decimals and fractions', '0.75 = 75/100 = 3/4', 26)


def couv_addition(t):
    _couv_cadre(t, 'Adding and subtracting decimals', '4.006 + 2.940 = 6.946', 24)


def couv_multiplication(t):
    _couv_cadre(t, 'Multiplying and dividing decimals', '3.6 × 2.5 = 9.0', 26)


def couv_problemes(t):
    _couv_cadre(t, 'Decimal word problems', '48.5 kg - 20.2 kg = 28.3 kg', 24)


# --------------------------------------------------------------------------
# Les quarante et une figures

FIGURES = [
    # Leçon 1 — la place des chiffres
    ('bd-pv-couv', 960, 540, couv_position),
    ('bd-pv-point', 320, 320,
     lambda t: nombre_pose(t, ['3', '4', None, '7', '2', '8'], ('.',),
                           'Le point sépare', 'À gauche le tout, à droite les parts.')),
    ('bd-pv-dixiemes', 320, 320,
     lambda t: nombre_pose(t, ['3', '4', None, '7', '2', '8'], ('tenths',),
                           'Le premier après le point', 'Le 7 est le chiffre des dixièmes.')),
    ('bd-pv-centiemes', 320, 320,
     lambda t: nombre_pose(t, ['3', '4', None, '7', '2', '8'],
                           ('hundredths', 'thousandths'),
                           'Le deuxième et le troisième', 'Centièmes, puis millièmes.')),
    ('bd-pv-nombre', 320, 320,
     lambda t: nombre_pose(t, ['3', '4', None, '7', '2', '8'], (),
                           'Le nombre 34.728', 'Chaque chiffre a sa colonne.')),
    ('bd-pv-lecture', 320, 320,
     lambda t: fiche(t, 'On lit chiffre par chiffre', ['4.5 : four point five',
                                                       '0.07 : zero point zero seven',
                                                       '12.304 : twelve point three zero four'])),

    # Leçon 2 — comparer et ranger
    ('bd-cp-couv', 960, 540, couv_comparer),
    ('bd-cp-gauche', 320, 320,
     lambda t: fiche(t, 'De gauche à droite', ['on compare les unités',
                                               'puis les dixièmes',
                                               'puis les centièmes'])),
    ('bd-cp-zeros', 320, 320,
     lambda t: fiche(t, 'Ajouter des zéros', ['2.5 s’écrit aussi 2.500',
                                              'le nombre ne change pas',
                                              'les colonnes s’alignent'], vif=(2,))),
    ('bd-cp-exemple', 320, 320,
     lambda t: colonne(t, ['2.500', '2.050'], titre='Lequel est le plus grand ?',
                       legende='2.5 est plus grand que 2.05.')),
    ('bd-cp-ordre', 320, 320,
     lambda t: fiche(t, 'Ascending order', ['0.07', '0.077', '0.7', '0.707'])),

    # Leçon 3 — arrondir
    ('bd-ro-couv', 960, 540, couv_arrondir),
    ('bd-ro-regle', 320, 320,
     lambda t: fiche(t, 'La règle', ['on regarde le chiffre d’après',
                                     '5 ou plus : on ajoute 1',
                                     'moins de 5 : on garde'])),
    ('bd-ro-entier', 320, 320,
     lambda t: nombre_pose(t, ['3', '4', None, '7', '2', '8'], ('tenths',),
                           'Au nombre entier', 'On regarde les dixièmes : 7.')),
    ('bd-ro-dixieme', 320, 320,
     lambda t: nombre_pose(t, ['3', '4', None, '7', '2', '8'], ('hundredths',),
                           'Au dixième près', 'On regarde les centièmes : 2.')),
    ('bd-ro-centieme', 320, 320,
     lambda t: fiche(t, '3.276 au centième', ['on regarde le millième : 6',
                                              '6 est plus grand que 5',
                                              '3.276 devient 3.28'], vif=(2,))),

    # Leçon 4 — les chiffres significatifs
    ('bd-sf-couv', 960, 540, couv_significatifs),
    ('bd-sf-premier', 320, 320,
     lambda t: fiche(t, 'On compte à partir de…', ['du premier chiffre non nul',
                                                   'dans 0.004025',
                                                   'on commence au 4'], vif=(2,))),
    ('bd-sf-garder', 320, 320,
     lambda t: fiche(t, 'Garder le nombre demandé', ['3 chiffres significatifs',
                                                     'on en garde trois',
                                                     'les autres partent'])),
    ('bd-sf-arrondir', 320, 320,
     lambda t: fiche(t, 'Le chiffre suivant arrondit', ['526.8 à 3 chiffres',
                                                        'le suivant est 8',
                                                        '526.8 devient 527'], vif=(2,))),
    ('bd-sf-exemples', 320, 320,
     lambda t: fiche(t, 'Deux exemples', ['526.8 donne 527', '0.004025 donne 0.00403',
                                          'trois chiffres chaque fois'], vif=(2,))),

    # Leçon 5 — décimaux et fractions
    ('bd-fr-couv', 960, 540, couv_fractions),
    ('bd-fr-moitie', 320, 320,
     lambda t: fiche(t, 'La moitié', ['0.5 = 5/10', '5/10 = 1/2', '0.5 est une moitié'],
                     vif=(2,))),
    ('bd-fr-quarts', 320, 320,
     lambda t: fiche(t, 'Les quarts', ['0.25 = 25/100 = 1/4', '0.75 = 75/100 = 3/4'])),
    ('bd-fr-versdecimal', 320, 320,
     lambda t: fiche(t, 'De la fraction au décimal', ['3/10 : trois dixièmes',
                                                      'donc 0.3'], vif=(1,))),
    ('bd-fr-vingtieme', 320, 320,
     lambda t: fiche(t, 'Passer par les centièmes', ['7/20', '7 × 5 = 35 et 20 × 5 = 100',
                                                     '35/100 = 0.35'], vif=(2,))),

    # Leçon 6 — additionner et soustraire
    ('bd-as-couv', 960, 540, couv_addition),
    ('bd-as-aligner', 320, 320,
     lambda t: colonne(t, ['4.006', '2.940'], titre='Aligner les points',
                       legende='Les points l’un sous l’autre.')),
    ('bd-as-zeros', 320, 320,
     lambda t: fiche(t, 'Compléter par des zéros', ['64.8 s’écrit 64.80',
                                                    'les colonnes sont pleines',
                                                    'on peut soustraire'], vif=(2,))),
    ('bd-as-addition', 320, 320,
     lambda t: colonne(t, ['4.006', '2.940', '6.946'], signe='+', trait_apres=1,
                       titre='Une addition posée')),
    ('bd-as-soustraction', 320, 320,
     lambda t: colonne(t, ['64.80', '5.63', '59.17'], signe='–', trait_apres=1,
                       titre='Une soustraction posée')),

    # Leçon 7 — multiplier et diviser
    ('bd-md-couv', 960, 540, couv_multiplication),
    ('bd-md-multiplier', 320, 320,
     lambda t: fiche(t, 'Multiplier', ['on multiplie sans les points',
                                       'on compte les décimales',
                                       'on pose le point'])),
    ('bd-md-exemple', 320, 320,
     lambda t: fiche(t, '0.08 × 4.2', ['8 × 42 = 336', '2 + 1 = 3 décimales',
                                       '0.336'], vif=(2,))),
    ('bd-md-diviser', 320, 320,
     lambda t: fiche(t, 'Diviser', ['le diviseur doit être entier',
                                    'on multiplie les deux par 10',
                                    'ou par 100'])),
    ('bd-md-exemple2', 320, 320,
     lambda t: fiche(t, '2.4 ÷ 0.08', ['les deux × 100', '240 ÷ 8', '= 30'], vif=(2,))),

    # Leçon 8 — les problèmes
    ('bd-pb-couv', 960, 540, couv_problemes),
    ('bd-pb-motscles', 320, 320,
     lambda t: fiche(t, 'Les mots qui commandent', ['altogether : on ajoute',
                                                    'left : on soustrait'])),
    ('bd-pb-partage', 320, 320,
     lambda t: fiche(t, 'Les deux autres', ['each, share : on divise',
                                            'times : on multiplie'])),
    ('bd-pb-operation', 320, 320,
     lambda t: fiche(t, 'Écrire avant de calculer', ['1. lire ce qu’on cherche',
                                                     '2. écrire l’opération',
                                                     '3. calculer'])),
    ('bd-pb-unite', 320, 320,
     lambda t: colonne(t, ['48.5', '20.2', '28.3'], signe='–', trait_apres=1,
                       titre='48.5 kg – 20.2 kg', legende='La réponse : 28.3 kg.')),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # L-ordre des colonnes EST la leçon : une inversion enseignerait une
    # faute sur chacune des huit leçons à la fois.
    assert COLONNES == ('tens', 'units', '.', 'tenths', 'hundredths', 'thousandths'), COLONNES

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
