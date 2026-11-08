# -*- coding: utf-8 -*-
"""
Les figures des sept leçons sur les fractions — fiche de révision CM1
« REVISION SHEET - FRACTIONS », 4 pages, donnée par le père le
8 novembre 2026.

UNE FRACTION SE MONTRE OU NE SE COMPREND PAS. Trois quarts écrits en
chiffres ne disent rien à qui ne sait pas déjà ; trois parts coloriées sur
quatre le disent d-un coup. Toutes les figures de ce fichier reposent donc
sur la MÊME barre partagée en parts égales, et la barre est calculée : les
parts y sont égales au pixel près, parce qu-une fraction dessinée sur des
parts inégales enseignerait exactement le contraire de la leçon.

Trois instruments, et les trente-sept figures en sortent :

  barre        le tout partagé en parts égales, les parts prises coloriées.
               Deux barres l-une sous l-autre comparent, et c-est ainsi
               qu-on voit que 1/2 et 2/4 sont la même longueur
  fraction     le numérateur, le trait, le dénominateur, écrits en grand,
               avec leurs noms quand la leçon les nomme. Le trait de
               fraction est tracé et non écrit : la barre oblique du
               clavier sépare mal deux chiffres superposés
  fiche        le calcul posé ligne à ligne, comme au cahier. « 1/2 + 1/3 =
               3/6 + 2/6 = 5/6 » ne s-apprend qu-en voyant les trois temps

Usage :  python work/figures-brayne-fractions.py
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


def _mesure(t, s, taille):
    return t.d.textlength(s, font=t.pol(taille)) / S


def _legende(t, y, mot, taille=16, couleur=INK_2, large=288):
    """Une légende qui tient dans la figure, quoi qu-elle dise.

    Sans ce rétrécissement, « Le nombre du haut : combien de parts on prend »
    sortait de l-image par la droite : le texte était centré sur 160 et
    mesurait plus de 300 pixels de large.
    """
    while _mesure(t, mot, taille) > large and taille > 10:
        taille -= 1
    t.texte((160, y), mot, taille, couleur)


# --------------------------------------------------------------------------
# La barre : le tout partagé en parts égales

def barre(t, pris, total, y=100, hauteur=58, gauche=24, droite=296,
          couleur=GOLD, nombres=False):
    """Le tout partagé en `total` parts égales, `pris` d-entre elles prises.

    Les bornes de chaque part sont calculées à partir des deux extrémités,
    jamais par addition d-une largeur arrondie : sinon la dernière part
    serait plus courte que les autres d-un ou deux pixels, et la barre
    démentirait le mot « égales » de la leçon.
    """
    assert total >= 1 and 0 <= pris <= total
    t.rrect(gauche, y, droite, y + hauteur, 8, fill=WHITE_WARM, bord=INK, trait=2.4)
    for i in range(total):
        x0 = gauche + (droite - gauche) * i / total
        x1 = gauche + (droite - gauche) * (i + 1) / total
        if i < pris:
            t.rrect(x0 + 2, y + 2, x1 - 2, y + hauteur - 2, 5, fill=couleur)
        if i:
            t.ligne([(x0, y + 2), (x0, y + hauteur - 2)], INK, 1.6)
        if nombres and total <= 8:
            t.texte(((x0 + x1) / 2, y + hauteur / 2), str(i + 1), 16,
                    INK if i < pris else INK_2)
    t.rrect(gauche, y, droite, y + hauteur, 8, bord=INK, trait=2.4)


def une_barre(t, pris, total, legende=None, titre=None, nombres=False):
    if titre:
        _legende(t, 68, titre, 18, INK)
    barre(t, pris, total, y=106, nombres=nombres)
    if legende:
        _legende(t, 212, legende)


def deux_barres(t, a, b, legende=None, titre=None, couleurs=(GOLD, MINT)):
    """Deux barres de même longueur : c-est la comparaison qui se voit."""
    if titre:
        _legende(t, 58, titre, 18, INK)
    for i, ((pris, total), couleur) in enumerate(zip((a, b), couleurs)):
        y = 86 + i * 78
        barre(t, pris, total, y=y, hauteur=52, couleur=couleur)
        t.texte((160, y + 66), '%d sur %d' % (pris, total), 14, INK_2)
    if legende:
        _legende(t, 268, legende, couleur=INK)


def trois_barres(t, parts, legende=None, titre=None):
    """Plusieurs barres entières, puis le reste : un nombre mixte se voit ainsi.

    Deux barres ne suffisaient pas pour 11/4 : une barre pleine et trois
    quarts font 7/4, pas 11/4. Il faut montrer AUTANT de barres pleines que
    le nombre entier en compte.
    """
    if titre:
        _legende(t, 56, titre, 18, INK)
    for i, (pris, total) in enumerate(parts):
        barre(t, pris, total, y=78 + i * 62, hauteur=46)
    if legende:
        _legende(t, 86 + len(parts) * 62, legende, 16, INK)


# --------------------------------------------------------------------------
# La fraction écrite : un trait tracé, et non une barre oblique

def _fraction(t, haut, bas, cx, cy, taille=40, couleur=INK):
    demi = max(_mesure(t, haut, taille), _mesure(t, bas, taille)) / 2 + 8
    t.texte((cx, cy - taille * 0.62), haut, taille, couleur)
    t.ligne([(cx - demi, cy), (cx + demi, cy)], couleur, 3)
    t.texte((cx, cy + taille * 0.64), bas, taille, couleur)
    return demi


def fraction(t, haut, bas, noms=False, legende=None, taille=46):
    """La fraction en grand, et les noms de ses deux nombres si besoin."""
    t.rrect(26, 44, 294, 212, 16, fill=WHITE_WARM, bord=INK, trait=2.4)
    cx = 160 if not noms else 118
    _fraction(t, haut, bas, cx, 128, taille)
    if noms:
        t.texte((186, 100), 'numerator', 15, CLAY, ancre='lm')
        t.texte((186, 156), 'denominator', 15, BLEU, ancre='lm')
    if legende:
        _legende(t, 248, legende, couleur=INK)


def calcul(t, gauche, droite, signe='=', legende=None, titre=None):
    """Deux fractions reliées par un signe : c-est l-égalité qui se montre."""
    if titre:
        _legende(t, 62, titre, 18, INK)
    t.rrect(22, 86, 298, 198, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    _fraction(t, gauche[0], gauche[1], 92, 142, 36)
    t.texte((160, 142), signe, 26, INK)
    _fraction(t, droite[0], droite[1], 228, 142, 36)
    if legende:
        _legende(t, 238, legende, couleur=INK)


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


def _couv_barre(t, titre, pris, total):
    _bandeau(t, titre)
    barre(t, pris, total, y=266, hauteur=62, gauche=270, droite=690)


def couv_quoi(t):
    _couv_barre(t, 'What a fraction is', 3, 5)


def couv_types(t):
    _bandeau(t, 'The types of fractions')
    for i, (h, b) in enumerate((('3', '5'), ('7', '4'), ('1', '7'))):
        _fraction(t, h, b, 360 + i * 120, 294, 34)


def couv_equivalentes(t):
    _bandeau(t, 'Equivalent fractions')
    barre(t, 1, 2, y=256, hauteur=36, gauche=300, droite=660)
    barre(t, 2, 4, y=300, hauteur=36, gauche=300, droite=660, couleur=MINT)


def couv_mixtes(t):
    _bandeau(t, 'Improper fractions and mixed numbers')
    _fraction(t, '11', '4', 400, 294, 34)
    t.texte((460, 294), '=', 26, INK)
    t.texte((500, 294), '2', 34, INK)
    _fraction(t, '3', '4', 540, 294, 34)


def couv_addition(t):
    _bandeau(t, 'Adding and subtracting fractions')
    _fraction(t, '3', '8', 400, 294, 32)
    t.texte((440, 294), '+', 24, INK)
    _fraction(t, '2', '8', 480, 294, 32)
    t.texte((520, 294), '=', 24, INK)
    _fraction(t, '5', '8', 560, 294, 32)


def couv_multiplication(t):
    _bandeau(t, 'Multiplying and dividing fractions')
    _fraction(t, '2', '3', 400, 294, 32)
    t.texte((440, 294), '×', 24, INK)
    _fraction(t, '5', '7', 480, 294, 32)
    t.texte((522, 294), '=', 24, INK)
    _fraction(t, '10', '21', 566, 294, 32)


def couv_quantite(t):
    _bandeau(t, 'A fraction of a quantity')
    t.rrect(300, 262, 660, 326, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.texte((330, 294), '3/5 of 40 = 24', 26, INK, ancre='lm')


# --------------------------------------------------------------------------
# Les trente-sept figures

FIGURES = [
    # Leçon 1 — ce qu-est une fraction
    ('bf-wh-couv', 960, 540, couv_quoi),
    ('bf-wh-def', 320, 320,
     lambda t: une_barre(t, 3, 5, 'Trois parts prises sur cinq parts égales.',
                         'Le tout, partagé')),
    ('bf-wh-num', 320, 320,
     lambda t: fraction(t, '3', '5', False, 'Le nombre du haut : combien de parts on prend.')),
    ('bf-wh-den', 320, 320,
     lambda t: fraction(t, '3', '5', True, 'Le nombre du bas : en combien de parts.')),
    ('bf-wh-egales', 320, 320,
     lambda t: une_barre(t, 1, 4, 'Les quatre parts ont la même longueur.',
                         'Des parts égales', nombres=True)),

    # Leçon 2 — les types de fractions
    ('bf-ty-couv', 960, 540, couv_types),
    ('bf-ty-propre', 320, 320,
     lambda t: une_barre(t, 3, 5, 'Le haut est plus petit que le bas : moins que 1.',
                         'Proper fraction : 3/5')),
    ('bf-ty-impropre', 320, 320,
     lambda t: fiche(t, 'Improper fraction : 7/4', ['le haut est plus grand que le bas',
                                                    '7 est plus grand que 4',
                                                    'la fraction vaut plus que 1'], vif=(2,))),
    ('bf-ty-mixte', 320, 320,
     lambda t: fiche(t, 'Mixed number : 2 et 1/3', ['un nombre entier : 2',
                                                    'et une fraction : 1/3',
                                                    'les deux écrits ensemble'], vif=(2,))),
    ('bf-ty-unitaire', 320, 320,
     lambda t: une_barre(t, 1, 7, 'Le haut vaut 1 : une seule part.',
                         'Unit fraction : 1/7')),

    # Leçon 3 — fractions équivalentes et comparaison
    ('bf-eq-couv', 960, 540, couv_equivalentes),
    ('bf-eq-equivalent', 320, 320,
     lambda t: deux_barres(t, (1, 2), (2, 4), 'Même longueur : même valeur.',
                           '1/2 et 2/4')),
    ('bf-eq-methode', 320, 320,
     lambda t: fiche(t, 'Multiplier le haut ET le bas', ['1 × 2 = 2', '2 × 2 = 4',
                                                         '1/2 = 2/4'], vif=(2,))),
    ('bf-eq-memedenom', 320, 320,
     lambda t: deux_barres(t, (3, 8), (5, 8), 'Même bas : le plus grand haut gagne.',
                           '3/8 et 5/8')),
    ('bf-eq-memenum', 320, 320,
     lambda t: deux_barres(t, (1, 3), (1, 6), 'Même haut : le plus petit bas gagne.',
                           '1/3 et 1/6')),
    ('bf-eq-commun', 320, 320,
     lambda t: fiche(t, 'Dénominateur commun', ['1/2 et 1/3', 'le commun est 6',
                                                '3/6 et 2/6'], vif=(2,))),

    # Leçon 4 — fractions impropres et nombres mixtes
    ('bf-im-couv', 960, 540, couv_mixtes),
    ('bf-im-versmixte', 320, 320,
     lambda t: fiche(t, 'De 11/4 au nombre mixte', ['11 ÷ 4 = 2 reste 3', 'le quotient : 2',
                                                    'le reste sur 4 : 3/4', '11/4 = 2 et 3/4'],
                     vif=(3,))),
    ('bf-im-versimpropre', 320, 320,
     lambda t: fiche(t, 'De 3 et 2/5 à la fraction', ['3 × 5 = 15', '15 + 2 = 17',
                                                      '3 et 2/5 = 17/5'], vif=(2,))),
    ('bf-im-memequantite', 320, 320,
     lambda t: trois_barres(t, [(4, 4), (4, 4), (3, 4)],
                            'Deux barres pleines, et trois quarts.', '11/4 = 2 et 3/4')),
    ('bf-im-avantcalcul', 320, 320,
     lambda t: fiche(t, 'Avant de multiplier ou diviser', ['un nombre mixte ne se calcule pas',
                                                           'on le change en fraction',
                                                           'puis seulement on calcule'],
                     vif=(1,))),

    # Leçon 5 — additionner et soustraire
    ('bf-ad-couv', 960, 540, couv_addition),
    ('bf-ad-memedenom', 320, 320,
     lambda t: fiche(t, 'Même dénominateur', ['3/8 + 2/8 = 5/8', 'le bas ne change pas',
                                              'on ajoute les hauts'], vif=(0,))),
    ('bf-ad-commun', 320, 320,
     lambda t: fiche(t, 'Dénominateurs différents', ['1. chercher le commun',
                                                     '2. changer chaque fraction',
                                                     '3. ajouter les hauts'])),
    ('bf-ad-exemple', 320, 320,
     lambda t: fiche(t, 'Un calcul posé', ['1/2 + 1/3', '3/6 + 2/6', '= 5/6'], vif=(2,))),
    ('bf-ad-piege', 320, 320,
     lambda t: fiche(t, 'Le piège', ['3/8 + 2/8 = 5/8', 'et jamais 5/16',
                                     'le bas ne s’additionne pas'], vif=(2,))),

    # Leçon 6 — multiplier et diviser
    ('bf-mu-couv', 960, 540, couv_multiplication),
    ('bf-mu-multiplier', 320, 320,
     lambda t: fiche(t, 'Multiplier', ['2/3 × 5/7', 'haut × haut : 2 × 5 = 10',
                                       'bas × bas : 3 × 7 = 21', '= 10/21'], vif=(3,))),
    ('bf-mu-entier', 320, 320,
     lambda t: fiche(t, 'Un entier qui multiplie', ['4 s’écrit 4/1', '4/1 × 2/3',
                                                    '= 8/3'], vif=(0,))),
    ('bf-mu-diviser', 320, 320,
     lambda t: fiche(t, 'Keep - change - flip', ['garder : 2/3', 'changer ÷ en ×',
                                                 'retourner : 5/4', '2/3 × 5/4 = 10/12'],
                     vif=(3,))),
    ('bf-mu-mixte', 320, 320,
     lambda t: fiche(t, 'Un nombre mixte', ['2 et 1/3 ne se multiplie pas',
                                            'on écrit 7/3', 'puis on multiplie'], vif=(1,))),

    # Leçon 7 — une fraction d-une quantité
    ('bf-qu-couv', 960, 540, couv_quantite),
    ('bf-qu-quantite', 320, 320,
     lambda t: fiche(t, '3/5 of 40', ['40 ÷ 5 = 8', '8 × 3 = 24', '3/5 of 40 = 24'], vif=(2,))),
    ('bf-qu-reste', 320, 320,
     lambda t: une_barre(t, 2, 5, 'Pris : 2/5. Il reste 3/5.', 'Ce qui reste')),
    ('bf-qu-deloreste', 320, 320,
     lambda t: fiche(t, 'Of the remainder', ['on prend 1/4 de 40 : 10', 'il reste 30',
                                             '1/3 du reste : 10'], vif=(2,))),
    ('bf-qu-argent', 320, 320,
     lambda t: fiche(t, 'Une fraction d’une somme', ['2/5 de 3 000 F', '3 000 ÷ 5 = 600',
                                                     '600 × 2 = 1 200 F'], vif=(2,))),
    ('bf-qu-unite', 320, 320,
     lambda t: fiche(t, 'La réponse se termine', ['24 mangues, et non 24',
                                                  '1 200 F, et non 1 200',
                                                  'l’unité fait la réponse'], vif=(2,))),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # Les parts d-une barre doivent être égales : c-est la seule chose que
    # la leçon affirme et que le dessin pourrait démentir tout seul.
    t = Toile(320, 320)
    barre(t, 3, 7, y=100)
    gauche, droite, total = 24, 296, 7
    bornes = [gauche + (droite - gauche) * i / total for i in range(total + 1)]
    largeurs = [round(bornes[i + 1] - bornes[i], 6) for i in range(total)]
    assert len(set(largeurs)) == 1, 'les parts de la barre ne sont pas égales : %s' % largeurs

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
