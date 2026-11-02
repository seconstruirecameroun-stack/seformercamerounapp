# -*- coding: utf-8 -*-
"""
Les 17 figures d-Unit 3 — Venn diagram, pour BRAYNE (CM1).

Rien n-est généré : tout est tracé, à la même enseigne que les figures de
maths, de sciences et d-anglais. La classe Toile vient de figures-maths.py
et n-est pas recopiée.

Une leçon sur les diagrammes de Venn se joue entièrement à l-image. Dire
« l-intersection est la partie commune » n-apprend rien ; montrer la zone
commune teintée et le reste pâle apprend tout. Chaque figure ne teinte
donc **qu-une seule région**, celle dont la notion parle, et laisse les
autres en retrait. C-est le contraire d-un schéma complet : on ne montre
pas le diagramme, on montre la région.

Pillow ne sait pas intersecter deux formes. On passe donc par des masques
en niveaux de gris, qu-on croise ou qu-on réunit, et on reverse la couleur
à travers. Les contours sont retracés après les teintes, pour qu-aucun
aplat ne vienne manger un trait.

Usage :  python work/figures-venn.py
"""

import importlib.util
import math
import os

from PIL import Image, ImageChops, ImageDraw

_ICI = os.path.dirname(os.path.abspath(__file__))


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Le fond, la palette, le lissage et la police viennent des figures de maths :
# deux moteurs de dessin donneraient deux styles dans la même application.
fm = _charger('figures_maths', 'figures-maths.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

# Le rose pâle des régions en retrait : présentes, mais qui ne tirent pas
# l-œil. La région dont parle la notion est en CLAY, et elle seule.
RETRAIT = (236, 226, 212)


def _masque(t):
    return Image.new('L', t.im.size, 0)


def _ovale_masque(t, cx, cy, rx, ry):
    m = _masque(t)
    ImageDraw.Draw(m).ellipse(
        [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=255)
    return m


def _rect_masque(t, x0, y0, x1, y1, r):
    m = _masque(t)
    ImageDraw.Draw(m).rounded_rectangle(
        [x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=255)
    return m


def _et(a, b):
    return ImageChops.darker(a, b)


def _ou(a, b):
    return ImageChops.lighter(a, b)


def _sauf(a, b):
    return ImageChops.subtract(a, b)


def _teinter(t, masque, couleur):
    t.im.paste(Image.new('RGB', t.im.size, couleur), (0, 0), masque)


def _contour(t, cx, cy, rx, ry, trait=3, couleur=INK):
    t.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                outline=couleur, width=max(1, int(trait * S)))


def _cadre(t, x0, y0, x1, y1, signe=True, trait=3, taille=22):
    """Le rectangle du set universel, avec son signe dans le coin.

    Le signe est **U** et non l’epsilon du manuel : Fredoka n’a pas la lettre
    grecque, et elle sortait en carré vide sur chaque figure. Son cahier
    d’exercices écrit « U » lui aussi — autant garder celui qu’il voit.
    """
    t.rrect(x0, y0, x1, y1, 10, fill=WHITE_WARM, bord=INK, trait=trait)
    if signe:
        t.texte((x0 + 18, y0 + 16), 'U', taille, INK_2)


def _pastille(t, xy, lettre, rayon=17, taille=22):
    """La lettre d’un set, lisible quelle que soit la teinte dessous.

    Posée à même le dessin, elle disparaissait : sur un aplat sombre, sur un
    contour, et au centre des trois ovales les lettres B et C se recouvraient
    l’une l’autre. Un disque clair derrière règle les trois cas d’un coup.
    """
    t.disque(xy, rayon, fill=WHITE_WARM, bord=INK, trait=2)
    t.texte(xy, lettre, taille, INK)


def _deux(cx, cy, ecart, rx, ry):
    """Les centres de deux ovales qui se chevauchent."""
    return (cx - ecart, cy, rx, ry), (cx + ecart, cy, rx, ry)


def _trois(cx, cy, ecart, r):
    """Les trois centres d-un Venn à trois ovales : un en haut, deux en bas."""
    return [(cx + ecart * math.cos(math.radians(a)),
             cy + ecart * math.sin(math.radians(a)), r, r)
            for a in (-90, 30, 150)]


def _poser(t, ovales, teintes, etiquettes=None, trait=3, taille=20):
    """Teinte les régions demandées, puis retrace tous les contours dessus."""
    masques = [_ovale_masque(t, *o) for o in ovales]
    for region, couleur in teintes:
        _teinter(t, region(masques), couleur)
    for o in ovales:
        _contour(t, *o, trait=trait)
    for xy, s in (etiquettes or []):
        _pastille(t, xy, s, rayon=taille * 0.78, taille=taille)
    return masques


# --------------------------------------------------------------------------
# Leçon 1 — ce que montre un diagramme de Venn

def ve_diagramme(t):  # couverture 960x540
    _cadre(t, 70, 70, 890, 470, taille=40)
    a, b = _deux(480, 268, 128, 232, 150)
    _poser(t, [a, b],
           [(lambda m: _sauf(m[0], m[1]), SKY),
            (lambda m: _sauf(m[1], m[0]), GOLD),
            (lambda m: _et(m[0], m[1]), CLAY)],
           [((262, 120), 'A'), ((700, 120), 'B')], trait=5, taille=46)


def ve_relation(t):
    _cadre(t, 18, 54, 302, 268)
    a, b = _deux(160, 161, 46, 86, 64)
    _poser(t, [a, b],
           [(lambda m: _sauf(m[0], m[1]), RETRAIT),
            (lambda m: _sauf(m[1], m[0]), RETRAIT),
            (lambda m: _et(m[0], m[1]), CLAY)])
    t.texte((160, 292), 'ce qu’elles partagent', 18, INK_2)


def ve_rectangle(t):
    _cadre(t, 40, 76, 280, 244, taille=30)
    t.texte((160, 160), 'le set', 24, INK_2)
    t.texte((160, 192), 'universel', 24, INK_2)
    t.texte((160, 286), 'un rectangle', 20, INK)


def ve_ovale(t):
    _cadre(t, 16, 56, 304, 266)
    for (cx, lettre) in ((76, 'A'), (160, 'B'), (244, 'C')):
        _contour(t, cx, 168, 38, 62)
        t.texte((cx, 168), lettre, 26, INK)
    t.texte((160, 292), 'les sets de travail', 18, INK_2)


def ve_commencer(t):
    _cadre(t, 18, 48, 302, 262)
    a, b = _deux(160, 155, 46, 86, 64)
    m = _poser(t, [a, b],
               [(lambda q: _sauf(q[0], q[1]), RETRAIT),
                (lambda q: _sauf(q[1], q[0]), RETRAIT),
                (lambda q: _et(q[0], q[1]), CLAY)])
    del m
    for (cx, n, couleur) in ((82, '2', INK_2), (160, '1', WHITE_WARM), (238, '3', INK_2)):
        t.texte((cx, 155), n, 30, couleur)
    t.texte((160, 288), 'le milieu en premier', 18, INK_2)


# --------------------------------------------------------------------------
# Leçon 2 — les quatre relations

def _vignette(t, x0, y0, largeur, hauteur, dessin, legende):
    _cadre(t, x0, y0, x0 + largeur, y0 + hauteur, signe=False, trait=4)
    dessin(x0 + largeur / 2, y0 + hauteur / 2)
    t.texte((x0 + largeur / 2, y0 + hauteur + 34), legende, 26, INK)


def ve_quatre(t):  # couverture 960x540
    l, h = 196, 196
    y = 128

    def croisees(teinte):
        def dessin(cx, cy):
            a, b = _deux(cx, cy, 34, 62, 56)
            _poser(t, [a, b], teinte(a, b), trait=4)
        return dessin

    _vignette(t, 54, y, l, h, croisees(lambda a, b: [
        (lambda m: _sauf(m[0], m[1]), RETRAIT),
        (lambda m: _sauf(m[1], m[0]), RETRAIT),
        (lambda m: _et(m[0], m[1]), CLAY)]), 'intersection')

    _vignette(t, 286, y, l, h, croisees(lambda a, b: [
        (lambda m: _ou(m[0], m[1]), CLAY)]), 'union')

    def emboites(cx, cy):
        _teinter(t, _ovale_masque(t, cx, cy, 74, 60), RETRAIT)
        _teinter(t, _ovale_masque(t, cx, cy + 8, 40, 32), CLAY)
        _contour(t, cx, cy, 74, 60, trait=4)
        _contour(t, cx, cy + 8, 40, 32, trait=4)
    _vignette(t, 518, y, l, h, emboites, 'subset')

    def separes(cx, cy):
        for dx, couleur in ((-40, CLAY), (40, RETRAIT)):
            _teinter(t, _ovale_masque(t, cx + dx, cy, 36, 58), couleur)
            _contour(t, cx + dx, cy, 36, 58, trait=4)
    _vignette(t, 750, y, l, h, separes, 'disjoint')


def ve_intersection(t):
    _cadre(t, 18, 54, 302, 268)
    a, b = _deux(160, 161, 46, 86, 64)
    _poser(t, [a, b],
           [(lambda m: _sauf(m[0], m[1]), RETRAIT),
            (lambda m: _sauf(m[1], m[0]), RETRAIT),
            (lambda m: _et(m[0], m[1]), CLAY)],
           [((82, 105), 'P'), ((238, 105), 'K')], taille=24)
    t.texte((160, 292), 'dans les deux', 20, INK)


def ve_union(t):
    _cadre(t, 18, 54, 302, 268)
    a, b = _deux(160, 161, 46, 86, 64)
    _poser(t, [a, b], [(lambda m: _ou(m[0], m[1]), CLAY)],
           [((82, 105), 'C'), ((238, 105), 'D')], taille=24)
    t.texte((160, 292), 'tout, des deux côtés', 18, INK)


def ve_sous_ensemble(t):
    _cadre(t, 18, 54, 302, 268)
    _teinter(t, _ovale_masque(t, 160, 158, 104, 76), RETRAIT)
    _teinter(t, _ovale_masque(t, 160, 170, 56, 44), CLAY)
    _contour(t, 160, 158, 104, 76)
    _contour(t, 160, 170, 56, 44)
    t.texte((160, 100), 'A', 24, INK)
    t.texte((160, 170), 'B', 24, WHITE_WARM)
    t.texte((160, 292), 'B est dans A', 20, INK)


def ve_disjoints(t):
    _cadre(t, 18, 54, 302, 268)
    for cx, lettre, couleur in ((88, 'T', CLAY), (232, 'C', RETRAIT)):
        _teinter(t, _ovale_masque(t, cx, 161, 52, 74), couleur)
        _contour(t, cx, 161, 52, 74)
        t.texte((cx, 161), lettre, 26, WHITE_WARM if couleur == CLAY else INK)
    t.texte((160, 292), 'rien en commun', 20, INK)


def ve_reconnaitre(t):
    hauteur = 64
    for i, (legende, dessin) in enumerate((
        ('intersection', 'croisees'), ('subset', 'emboites'), ('disjoint', 'separes'),
    )):
        cy = 52 + i * (hauteur + 20)
        if dessin == 'croisees':
            a, b = _deux(84, cy, 24, 40, 30)
            _poser(t, [a, b],
                   [(lambda m: _sauf(m[0], m[1]), RETRAIT),
                    (lambda m: _sauf(m[1], m[0]), RETRAIT),
                    (lambda m: _et(m[0], m[1]), CLAY)], trait=2)
        elif dessin == 'emboites':
            _teinter(t, _ovale_masque(t, 84, cy, 54, 30), RETRAIT)
            _teinter(t, _ovale_masque(t, 84, cy, 26, 18), CLAY)
            _contour(t, 84, cy, 54, 30, trait=2)
            _contour(t, 84, cy, 26, 18, trait=2)
        else:
            for dx, couleur in ((-28, CLAY), (28, RETRAIT)):
                _teinter(t, _ovale_masque(t, 84 + dx, cy, 24, 30), couleur)
                _contour(t, 84 + dx, cy, 24, 30, trait=2)
        t.texte((168, cy), legende, 20, INK, ancre='lm')


# --------------------------------------------------------------------------
# Leçon 3 — lire chaque région

def _lettres(t, ovales, centre, part, taille):
    """Chaque lettre dans le lobe que son ovale ne partage avec personne."""
    for (x, y, rx, _ry), lettre in zip(ovales, 'ABC'):
        dx, dy = x - centre[0], y - centre[1]
        n = math.hypot(dx, dy) or 1.0
        _pastille(t, (x + dx / n * rx * part, y + dy / n * rx * part),
                  lettre, rayon=taille * 0.82, taille=taille)


def _trois_ovales(t, cx=160, cy=168, ecart=36, r=72):
    return _trois(cx, cy, ecart, r)


def ve_lire(t):  # couverture 960x540
    _cadre(t, 150, 50, 810, 500, taille=36)
    o = _trois(480, 268, 68, 142)
    m = [_ovale_masque(t, *x) for x in o]
    seul = [_sauf(_sauf(m[i], m[(i + 1) % 3]), m[(i + 2) % 3]) for i in range(3)]
    paire = [_sauf(_et(m[i], m[(i + 1) % 3]), m[(i + 2) % 3]) for i in range(3)]
    centre = _et(_et(m[0], m[1]), m[2])
    for masque, couleur in zip(seul, (SKY, GOLD, MINT)):
        _teinter(t, masque, couleur)
    for masque in paire:
        _teinter(t, masque, LILAC)
    _teinter(t, centre, CLAY)
    for x in o:
        _contour(t, *x, trait=5)
    _lettres(t, o, (480, 268), 0.74, 34)


def _trois_poser(t, teintes):
    """Trois ovales, et seules les régions nommées prennent la couleur."""
    o = _trois_ovales(t)
    m = [_ovale_masque(t, *x) for x in o]
    for region, couleur in teintes:
        _teinter(t, region(m), couleur)
    for x in o:
        _contour(t, *x)
    _lettres(t, o, (160, 168), 0.72, 19)
    return m


def ve_lister(t):
    _cadre(t, 10, 58, 310, 282)
    _trois_poser(t, [
        (lambda m: _ou(m[1], m[2]), RETRAIT),
        (lambda m: m[0], CLAY),
    ])
    t.texte((160, 302), 'tout l’ovale de A', 18, INK)


def ve_seulement(t):
    _cadre(t, 10, 58, 310, 282)
    _trois_poser(t, [
        (lambda m: _ou(_ou(m[0], m[1]), m[2]), RETRAIT),
        (lambda m: _sauf(_sauf(m[0], m[1]), m[2]), CLAY),
    ])
    t.texte((160, 302), 'A only', 20, INK)


def ve_centre(t):
    _cadre(t, 10, 58, 310, 282)
    _trois_poser(t, [
        (lambda m: _ou(_ou(m[0], m[1]), m[2]), RETRAIT),
        (lambda m: _et(_et(m[0], m[1]), m[2]), CLAY),
    ])
    t.texte((160, 302), 'dans les trois', 18, INK)


def ve_dehors(t):
    _cadre(t, 14, 48, 306, 264)
    a, b = _deux(160, 150, 42, 74, 56)
    _poser(t, [a, b],
           [(lambda m: _ou(m[0], m[1]), RETRAIT)])
    # Rentrés dans le cadre : posés aux coins, ils chevauchaient le trait du
    # rectangle, et un élément à cheval sur la bordure ne dit plus de quel
    # côté il est — c’est précisément ce que la figure doit montrer.
    for cx, cy in ((52, 84), (268, 84), (52, 228), (268, 228)):
        t.disque((cx, cy), 11, fill=CLAY)
    t.texte((160, 290), 'dehors, mais dans le rectangle', 16, INK)


def ve_nombre(t):
    _cadre(t, 18, 42, 302, 222)
    a, b = _deux(160, 128, 40, 70, 52)
    _poser(t, [a, b], [(lambda m: _ou(m[0], m[1]), RETRAIT)])
    points = [(104, 108), (128, 148), (196, 108), (216, 150), (160, 128),
              (54, 76), (266, 76), (54, 188), (266, 188)]
    for cx, cy in points:
        t.disque((cx, cy), 9, fill=CLAY)
    t.rrect(96, 248, 224, 300, 14, fill=SAND, bord=INK, trait=3)
    t.texte((160, 274), 'n = %d' % len(points), 26, INK)


FIGURES = [
    ('ve-diagramme', 960, 540, ve_diagramme),
    ('ve-relation', 320, 320, ve_relation),
    ('ve-rectangle', 320, 320, ve_rectangle),
    ('ve-ovale', 320, 320, ve_ovale),
    ('ve-commencer', 320, 320, ve_commencer),
    ('ve-quatre', 960, 540, ve_quatre),
    ('ve-intersection', 320, 320, ve_intersection),
    ('ve-union', 320, 320, ve_union),
    ('ve-sous-ensemble', 320, 320, ve_sous_ensemble),
    ('ve-disjoints', 320, 320, ve_disjoints),
    ('ve-reconnaitre', 320, 320, ve_reconnaitre),
    ('ve-lire', 960, 540, ve_lire),
    ('ve-lister', 320, 320, ve_lister),
    ('ve-seulement', 320, 320, ve_seulement),
    ('ve-centre', 320, 320, ve_centre),
    ('ve-dehors', 320, 320, ve_dehors),
    ('ve-nombre', 320, 320, ve_nombre),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # Les trois ovales doivent vraiment se croiser trois par trois, sinon la
    # région centrale dont parle la leçon n-existe pas sur le dessin.
    t = Toile(320, 320)
    o = _trois_ovales(t)
    m = [_ovale_masque(t, *x) for x in o]
    centre = _et(_et(m[0], m[1]), m[2])
    assert centre.getbbox() is not None, 'les trois ovales ne se croisent pas'
    for i in range(3):
        seul = _sauf(_sauf(m[i], m[(i + 1) % 3]), m[(i + 2) % 3])
        assert seul.getbbox() is not None, 'le set %d na pas de région propre' % i
        paire = _sauf(_et(m[i], m[(i + 1) % 3]), m[(i + 2) % 3])
        assert paire.getbbox() is not None, 'deux ovales se croisent sans région propre'

    # Deux ovales disjoints ne doivent partager aucun pixel : la figure
    # enseignerait le contraire de son nom.
    g = _ovale_masque(t, 88, 161, 52, 74)
    d = _ovale_masque(t, 232, 161, 52, 74)
    assert _et(g, d).getbbox() is None, 'les ovales disjoints se touchent'

    # Et deux ovales qui se chevauchent doivent, eux, partager quelque chose.
    a, b = _deux(160, 161, 46, 86, 64)
    assert _et(_ovale_masque(t, *a), _ovale_masque(t, *b)).getbbox() is not None, \
        'les ovales censés se croiser ne se croisent pas'


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
