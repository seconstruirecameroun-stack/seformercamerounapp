# -*- coding: utf-8 -*-
"""
Les figures des quatre leçons d-anglais de KLEIN (CE1) — cahier du
19 septembre au 22 octobre 2026, lot démêlé le 5 novembre.

Ces leçons-là sont des leçons de FORME des mots : on part d-un mot, on
le change, on obtient un autre mot. « knife » devient « knives »,
« cap » devient « cape ». Montrer ça demande toujours la même image :
deux colonnes, et ce qui change mis en couleur.

D-où l-instrument principal du module :

  _table2    singulier à gauche, pluriel à droite, et la partie qui
             change teintée dans les deux. L-enfant ne lit pas deux
             mots : il lit un mot et sa transformation

  _fleche    un mot, une flèche, l-autre mot. Pour les cas isolés où
             un tableau serait une grosse machine pour trois mots

  _faux_vrai le piège barré au-dessus de la forme juste en dessous.
             Sert une seule fois, pour « chieves », qui est écrit dans
             le cahier et qui est faux

Le reste des instruments vient de figures-anglais-oct.py : on ne
redessine pas une pastille qui existe déjà.

Usage :  python work/figures-klein-anglais-nov.py
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
fa = _charger('figures_anglais_oct', 'figures-anglais-oct.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

ROUGE = fa.ROUGE
VERT = fa.VERT

_mesure = fa._mesure
_pastille = fa._pastille
_taille_tenant = fa._taille_tenant
_liste = fa._liste
_tuiles = fa._tuiles
_bandeau_couv = fa._bandeau_couv

BANDEAU = fa.BANDEAU


# --------------------------------------------------------------------------
# Les instruments

def _mot_colore(t, cx, cy, base, finale, taille, fond, teinte_finale):
    """Un mot dans une pastille, sa terminaison d-une autre couleur.

    Le mot est posé d-un bloc pour que l-espacement soit celui de la
    police, puis la terminaison est réécrite par-dessus en couleur :
    c-est la seule façon d-avoir « kni » et « ves » parfaitement
    accolés sans calculer le crénage à la main.
    """
    entier = base + finale
    w = _mesure(t, entier, taille) + 22
    h = taille + 16
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill=fond, bord=INK, trait=1.8)
    gauche = cx - _mesure(t, entier, taille) / 2
    t.texte((gauche, cy), base, taille, INK, ancre='lm')
    t.texte((gauche + _mesure(t, base, taille), cy), finale, taille, teinte_finale, ancre='lm')
    return w


def _table2(t, lignes, titre=None, haut=76, bas=288, gauche=16, droite=304):
    """Deux colonnes. Chaque ligne : (base_g, finale_g, base_d, finale_d).

    La terminaison qui change est teintée des deux côtés — en argile à
    gauche (ce qu-on enlève), en vert à droite (ce qu-on met). Un enfant
    qui regarde la colonne de droite voit la règle sans la lire.
    """
    if titre:
        t.texte(((gauche + droite) / 2, haut - 22), titre, 15, INK_2)
    larg = (droite - gauche) / 2
    entiers = [bg + fg for bg, fg, _bd, _fd in lignes] + [bd + fd for _bg, _fg, bd, fd in lignes]
    taille = _taille_tenant(t, entiers, larg, 17)
    pas = (bas - haut) / max(1, len(lignes))
    t.ligne([((gauche + droite) / 2, haut - 6), ((gauche + droite) / 2, bas)], INK_2, 1.6)
    for i, (bg, fg, bd, fd) in enumerate(lignes):
        y = haut + pas * (i + 0.5)
        _mot_colore(t, gauche + larg * 0.5, y, bg, fg, taille, WHITE_WARM, CLAY)
        _mot_colore(t, gauche + larg * 1.5, y, bd, fd, taille, MINT, VERT)


def _fleche(t, gauche, droite, cy=170, note=None, teinte=MINT):
    """Un mot, une flèche, l-autre mot. Pour les cas isolés."""
    _pastille(t, 160, cy - 46, gauche, 22, fond=WHITE_WARM, marge=16)
    t.ligne([(160, cy - 24), (160, cy + 22)], CLAY, 2.6)
    for d in (-7, 7):
        t.ligne([(160, cy + 22), (160 + d, cy + 12)], CLAY, 2.6)
    _pastille(t, 160, cy + 46, droite, 22, fond=teinte, marge=16)
    if note:
        t.texte((160, cy + 96), note, 14, INK_2)


def _faux_vrai(t, faux, vrai, note=None):
    """Le piège barré, la forme juste en dessous. Une seule fois ici."""
    w = _pastille(t, 160, 116, faux, 22, fond=(246, 222, 218), couleur=INK_2, marge=18)
    t.ligne([(160 - w / 2 + 6, 116), (160 + w / 2 - 6, 116)], ROUGE, 3)
    t.texte((160, 158), 'no', 15, ROUGE)
    _pastille(t, 160, 206, vrai, 24, fond=MINT, marge=18)
    t.texte((160, 246), 'yes', 15, VERT)
    if note:
        t.texte((160, 282), note, 13, INK_2)


def _paires(t, paires, titre=None, haut=80, bas=286):
    """Court / long : cap → cape, sur une ligne par paire.

    Le « e » ajouté est en or, parce que c-est lui le magicien. Le
    reste du mot ne change pas : il ne doit pas changer de couleur non
    plus, sinon on ne voit plus ce qui compte.
    """
    if titre:
        t.texte((160, haut - 22), titre, 15, INK_2)
    pas = (bas - haut) / max(1, len(paires))
    for i, (court, long_) in enumerate(paires):
        y = haut + pas * (i + 0.5)
        _pastille(t, 86, y, court, 19, fond=WHITE_WARM, marge=12)
        t.ligne([(130, y), (176, y)], CLAY, 2.4)
        for d in (-6, 6):
            t.ligne([(176, y), (168, y + d)], CLAY, 2.4)
        _mot_colore(t, 238, y, long_[:-1], long_[-1], 19, GOLD, ROUGE)


def _mot_marque(t, cx, cy, mot, indices, taille, fond, teinte):
    """Un mot dont SEULES les lettres citées sont teintées.

    _mot_colore teint tout ce qui suit la coupure : il va bien pour une
    terminaison, et il ment dès que la lettre qui compte est au milieu
    du mot. Ici on découpe en trois morceaux et on n-en teint qu-un.
    """
    w = _mesure(t, mot, taille) + 22
    h = taille + 16
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill=fond, bord=INK, trait=1.8)
    x = cx - _mesure(t, mot, taille) / 2
    for i, lettre in enumerate(mot):
        t.texte((x, cy), lettre, taille, teinte if i in indices else INK, ancre='lm')
        x += _mesure(t, mot[:i + 1], taille) - _mesure(t, mot[:i], taille)


def _trois_graphies(t, mots, son, note=None):
    """Le même son, trois façons de l-écrire. C-est là qu-il se trompe."""
    t.texte((160, 72), son, 26, INK)
    t.texte((160, 102), 'one sound', 14, INK_2)
    pas = 58
    for i, (mot, indices) in enumerate(mots):
        _mot_marque(t, 160, 150 + pas * i, mot, indices, 21, WHITE_WARM, ROUGE)
    if note:
        t.texte((160, 150 + pas * len(mots) + 10), note, 13, INK_2)


def _muet(t, mot, note):
    """La lettre qu-on écrit et qu-on ne dit pas, en gris et barrée."""
    _mot_marque(t, 160, 132, mot, {len(mot) - 1}, 34, GOLD, (150, 150, 150))
    largeur = _mesure(t, mot, 34)
    xe = 160 + largeur / 2 - _mesure(t, mot[-1], 34) / 2
    t.texte((xe, 180), 'silent', 14, INK_2)
    t.ligne([(xe, 164), (xe, 152)], INK_2, 1.8)
    t.texte((160, 232), note, 15, INK)


# --------------------------------------------------------------------------
# Les figures, leçon par leçon

def _fab_table2(lignes, titre=None):
    def f(t):
        _table2(t, lignes, titre)
    return f


def _fab_fleche(g, d, note=None, teinte=MINT):
    def f(t):
        _fleche(t, g, d, note=note, teinte=teinte)
    return f


def _fab_liste(items, titre):
    def f(t):
        _liste(t, items, titre)
    return f


def _fab_tuiles(melange, ordre, note=None):
    def f(t):
        _tuiles(t, melange, ordre)
        if note:
            t.texte((160, 282), note, 15, INK)
    return f


def _fab_paires(paires, titre=None):
    def f(t):
        _paires(t, paires, titre)
    return f


# --- Couvertures (tout tient dans la bande 184-356) -----------------------

def couv_f_ves(t):
    _bandeau_couv(t, 'f and fe become ves')
    for i, (base, fin, fond, teinte) in enumerate(
            (('kni', 'fe', WHITE_WARM, CLAY), ('kni', 'ves', MINT, VERT))):
        _mot_colore(t, 330 + i * 300, 300, base, fin, 30, fond, teinte)
    t.ligne([(430, 300), (530, 300)], CLAY, 3)
    for d in (-9, 9):
        t.ligne([(530, 300), (518, 300 + d)], CLAY, 3)


def couv_special(t):
    _bandeau_couv(t, 'Special plurals')
    for i, (base, fin, fond, teinte) in enumerate(
            (('f', 'oot', WHITE_WARM, CLAY), ('f', 'eet', MINT, VERT))):
        _mot_colore(t, 330 + i * 300, 300, base, fin, 30, fond, teinte)
    t.ligne([(430, 300), (530, 300)], CLAY, 3)
    for d in (-9, 9):
        t.ligne([(530, 300), (518, 300 + d)], CLAY, 3)


def couv_jumbled_letters(t):
    _bandeau_couv(t, 'Jumbled letters')
    for y, lettres, fond in ((268, ['s', 'c', 'o', 'o', 'h', 'l'], LILAC),
                             (330, ['s', 'c', 'h', 'o', 'o', 'l'], MINT)):
        x = 480 - (len(lettres) * 44) / 2
        for lettre in lettres:
            t.rrect(x, y - 19, x + 38, y + 19, 7, fill=fond, bord=INK, trait=2)
            t.texte((x + 19, y), lettre, 22, INK)
            x += 44


def couv_magic_e(t):
    _bandeau_couv(t, 'The magic e')
    _mot_colore(t, 380, 300, 'cap', '', 32, WHITE_WARM, INK)
    t.ligne([(450, 300), (530, 300)], CLAY, 3)
    for d in (-9, 9):
        t.ligne([(530, 300), (518, 300 + d)], CLAY, 3)
    _mot_colore(t, 610, 300, 'cap', 'e', 32, GOLD, ROUGE)


FIGURES = [
    # ---- 29. Plurals of nouns ending in f or fe -------------------------
    ('kn-pf-couv', 960, 540, couv_f_ves),
    ('kn-pf-regle', 320, 320, _fab_table2(
        [('thie', 'f', 'thie', 'ves'), ('lea', 'f', 'lea', 'ves'),
         ('kni', 'fe', 'kni', 'ves'), ('wi', 'fe', 'wi', 'ves')],
        'singular              plural')),
    ('kn-pf-plus', 320, 320, _fab_table2(
        [('li', 'fe', 'li', 'ves'), ('hal', 'f', 'hal', 'ves'),
         ('loa', 'f', 'loa', 'ves'), ('shel', 'f', 'shel', 'ves')],
        'four more')),
    ('kn-pf-wolf', 320, 320, _fab_fleche('wolf', 'wolves', 'f goes away, ves comes')),
    ('kn-pf-exception', 320, 320, _fab_table2(
        [('chief', '', 'chief', 's'), ('roof', '', 'roof', 's'),
         ('belief', '', 'belief', 's'), ('chef', '', 'chef', 's')],
        'these only add s')),
    ('kn-pf-piege', 320, 320, lambda t: _faux_vrai(
        t, 'chieves', 'chiefs', 'chief keeps its f and takes s')),
    ('kn-pf-phrase', 320, 320, _fab_tuiles(
        ['The tree', 'has', 'green', 'leaf'],
        ['The tree', 'has', 'green', 'leaves'], 'more than one leaf')),

    # ---- 30. Nouns with a special plural --------------------------------
    ('kn-sp-couv', 960, 540, couv_special),
    ('kn-sp-oo', 320, 320, _fab_table2(
        [('f', 'oot', 'f', 'eet'), ('t', 'ooth', 't', 'eeth'),
         ('g', 'oose', 'g', 'eese')],
        'oo becomes ee')),
    ('kn-sp-ouse', 320, 320, _fab_table2(
        [('m', 'ouse', 'm', 'ice'), ('l', 'ouse', 'l', 'ice')],
        'ouse becomes ice')),
    ('kn-sp-change', 320, 320, _fab_table2(
        [('child', '', 'child', 'ren'), ('m', 'an', 'm', 'en'),
         ('wom', 'an', 'wom', 'en'), ('ox', '', 'ox', 'en')],
        'the whole word changes')),
    ('kn-sp-person', 320, 320, _fab_fleche('person', 'people', 'a word of its own')),
    ('kn-sp-meme', 320, 320, _fab_table2(
        [('sheep', '', 'sheep', ''), ('deer', '', 'deer', ''),
         ('fish', '', 'fish', '')],
        'these do not change')),
    ('kn-sp-phrase', 320, 320, _fab_tuiles(
        ['There are', 'many', 'mouse', 'here'],
        ['There are', 'many', 'mice', 'here'], 'more than one mouse')),

    # ---- 31. Jumbled letters --------------------------------------------
    ('kn-jl-couv', 960, 540, couv_jumbled_letters),
    ('kn-jl-def', 320, 320, _fab_tuiles(
        ['n', 'g', 'i', 's'], ['s', 'i', 'n', 'g'], 'the letters put in order')),
    ('kn-jl-school', 320, 320, _fab_tuiles(
        ['s', 'c', 'o', 'o', 'h', 'l'], ['s', 'c', 'h', 'o', 'o', 'l'])),
    ('kn-jl-steps', 320, 320, _fab_liste(
        ['Read all the letters', 'Find the vowels', 'Try a beginning',
         'Read it to check'], 'Four steps')),
    ('kn-jl-book', 320, 320, _fab_tuiles(['o', 'b', 'k', 'o'], ['b', 'o', 'o', 'k'])),
    ('kn-jl-farm', 320, 320, _fab_tuiles(['r', 'a', 'm', 'f'], ['f', 'a', 'r', 'm'])),

    # ---- 32. The magic e -------------------------------------------------
    ('kn-me-couv', 960, 540, couv_magic_e),
    ('kn-me-regle', 320, 320, _fab_paires(
        [('cap', 'cape'), ('hat', 'hate'), ('kit', 'kite')],
        'the e wakes the vowel')),
    ('kn-me-plus', 320, 320, _fab_paires(
        [('not', 'note'), ('cub', 'cube'), ('rid', 'ride')])),
    ('kn-me-silence', 320, 320, lambda t: _muet(
        t, 'cube', 'you never say the last e')),
    ('kn-me-familles', 320, 320, _fab_table2(
        [('a', '_e', 'gr', 'ade'), ('e', '_e', 'sc', 'ene'),
         ('i', '_e', 'sh', 'ine'), ('o', '_e', 'v', 'ote'),
         ('u', '_e', 'c', 'ute')],
        'five families, one example each')),
    ('kn-me-ai-ay', 320, 320, lambda t: _trois_graphies(
        t, [('made', {1, 3}), ('maid', {1, 2}), ('may', {1, 2})], 'the long a',
        'three spellings, one sound')),
    ('kn-me-plays', 320, 320, lambda t: _faux_vrai(
        t, 'plaies', 'plays', 'at the end of a word, write ay')),
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
