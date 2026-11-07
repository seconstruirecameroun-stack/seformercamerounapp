# -*- coding: utf-8 -*-
"""
Les figures des cinq leçons d-éducation à la santé de BRAYNE (CM1) —
cahier « Sciences / Health / En. Educ », octobre et novembre 2026.

PRESQUE RIEN N-EST DESSINÉ ICI.

Les aliments, les modes de cuisson et les méthodes de conservation ont
déjà été dessinés pour KLEIN, dans figures-klein-maison-nov.py. Un
poisson est un poisson, qu-il serve à un CE1 ou à un CM1 : le
redessiner ne donnerait pas une meilleure image, seulement une seconde
à corriger le jour où la première est fausse.

Ce module n-ajoute donc que ce qui manque réellement :

  _tableau3   classe | source | fonction, les trois colonnes du cahier.
              C-est sous cette forme que la maîtresse a écrit les six
              classes d-aliments, et sous cette forme qu-elle interroge
  assiette    l-assiette équilibrée, partagée en parts. Elle n-existait
              pas : KLEIN n-a pas de leçon sur le régime
  bouteille   la conservation par embouteillage
  cuve        la cuisson à la vapeur, que la marmite seule ne dit pas

Et les quatre figures des toilettes, qui ne ressemblent à rien d-autre
dans le dépôt.

Usage :  python work/figures-brayne-sante-nov.py
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
fk = _charger('figures_klein_maison', 'figures-klein-maison-nov.py')
fb = _charger('figures_brayne_env', 'figures-brayne-env-nov.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

VERT, TERRE, ROUGE = fa.VERT, fa.TERRE, fa.ROUGE
FER, BOIS = fg.FER, fg.BOIS
FROID = fk.FROID

# Les pictogrammes empruntés, nommés ici pour qu-on voie d-où ils viennent.
grain, poisson, fruit = fk.grain, fk.poisson, fk.fruit
huile, sel, verre_eau = fk.huile, fk.sel, fk.verre_eau
marmite, poele, four, feu = fk.marmite, fk.poele, fk.four, fk.feu
grille_feu, soleil, frigo, boite, fumee = (fk.grille_feu, fk.soleil, fk.frigo,
                                           fk.boite, fk.fumee)
latrine = fb.latrine
_note = fb._note

_mesure = fa._mesure
_pastille = fa._pastille
_taille_tenant = fa._taille_tenant
_liste = fa._liste
_bandeau_couv = fa._bandeau_couv
_vignette = fg._vignette
_grille = fg._grille
BANDEAU = fa.BANDEAU


# --------------------------------------------------------------------------
# Ce qui manquait

def bouteille(t, cx, cy, couleur=SKY):
    t.rrect(cx - 5, cy - 42, cx + 5, cy - 28, 2, fill=couleur, bord=INK, trait=1.6)
    t.rrect(cx - 7, cy - 46, cx + 7, cy - 38, 2, fill=CLAY, bord=INK, trait=1.6)
    t.poly([(cx - 5, cy - 28), (cx + 5, cy - 28), (cx + 16, cy - 10), (cx + 16, cy + 34),
            (cx - 16, cy + 34), (cx - 16, cy - 10)], fill=couleur, bord=INK, trait=2)
    t.rrect(cx - 11, cy + 2, cx + 11, cy + 18, 3, fill=WHITE_WARM, bord=INK, trait=1.4)


def cuve(t, cx, cy):
    """La cuisson à la vapeur : la marmite, son couvercle, et la vapeur."""
    marmite(t, cx, cy + 8)
    t.d.ellipse([int((cx - 30) * S), int((cy - 20) * S), int((cx + 30) * S),
                 int((cy - 6) * S)], fill=FER, outline=INK, width=int(2 * S))
    t.disque((cx, cy - 18), 5, fill=CLAY, bord=INK, trait=1.5)
    for dx in (-16, 0, 16):
        t.d.arc([int((cx + dx - 8) * S), int((cy - 50) * S), int((cx + dx + 8) * S),
                 int((cy - 26) * S)], 160, 380, fill=INK_2, width=int(2.2 * S))


def assiette(t, cx, cy, parts, r=62):
    """L-assiette et ses parts.

    `parts` est une liste de (fraction, couleur). Le dessin dit d-un
    coup d-oeil si le repas est partagé entre plusieurs classes
    d-aliments ou pris par une seule.
    """
    t.disque((cx, cy), r + 8, fill=WHITE_WARM, bord=INK, trait=2.4)
    debut = -90.0
    for fraction, couleur in parts:
        fin = debut + 360.0 * fraction
        t.d.pieslice([int((cx - r) * S), int((cy - r) * S), int((cx + r) * S),
                      int((cy + r) * S)], debut, fin, fill=couleur,
                     outline=INK, width=int(2 * S))
        debut = fin


def _tableau3(t, lignes, titres=('class', 'source', 'function'),
              haut=64, bas=300, gauche=10, droite=310):
    """Trois colonnes : la classe, sa source, son rôle. La forme du cahier."""
    larges = (0.30, 0.34, 0.36)
    bords = [gauche]
    for f in larges:
        bords.append(bords[-1] + (droite - gauche) * f)
    for i, titre in enumerate(titres):
        t.texte(((bords[i] + bords[i + 1]) / 2, haut - 14), titre, 13, INK_2)
    pas = (bas - haut) / max(1, len(lignes))
    tous = [c for ligne in lignes for c in ligne]
    taille = _taille_tenant(t, tous, (droite - gauche) * min(larges), 12)
    for r, ligne in enumerate(lignes):
        y = haut + pas * (r + 0.5)
        for i, cellule in enumerate(ligne):
            cx = (bords[i] + bords[i + 1]) / 2
            fond = SAND if i == 0 else (MINT if i == 2 else WHITE_WARM)
            w = (bords[i + 1] - bords[i]) - 6
            h = min(pas * 0.8, 40)
            t.rrect(cx - w / 2, y - h / 2, cx + w / 2, y + h / 2, 7,
                    fill=fond, bord=INK, trait=1.5)
            t.texte((cx, y), cellule, taille, INK)


def _duo(t, gauche, droite, note=None):
    _vignette(t, 86, 132, gauche[0], gauche[1], 122)
    _vignette(t, 234, 132, droite[0], droite[1], 122)
    if note:
        _note(t, note, 240)


# --------------------------------------------------------------------------
# Les fabriques

def _fab_liste(items, titre):
    def f(t):
        _liste(t, items, titre)
    return f


def _fab_scene(dessin, note=None, y=268):
    def f(t):
        dessin(t)
        if note:
            _note(t, note, y)
    return f


def _fab_tableau(lignes, titres=('class', 'source', 'function')):
    def f(t):
        _tableau3(t, lignes, titres)
    return f


def _fab_classe(dessin, nom, role):
    """Une classe d-aliment : sa source, son nom, son rôle."""
    def f(t):
        dessin(t, 160, 116)
        _pastille(t, 160, 192, nom, 20, fond=GOLD, marge=18)
        _note(t, role, 240, 15, INK)
    return f


def _fab_methode(dessin, nom, exemples):
    def f(t):
        dessin(t, 160, 120)
        _pastille(t, 160, 192, nom, 20, fond=MINT, marge=18)
        _note(t, exemples, 240, 15)
    return f


def _fab_duo(g, d, note):
    def f(t):
        _duo(t, g, d, note)
    return f


def _fab_grille(items):
    def f(t):
        _grille(t, items)
    return f


# --------------------------------------------------------------------------
# Les scènes

def _sc_wc(t):
    latrine(t, 150, 140)
    for k in range(4):
        t.ligne([(196 + k * 7, 112 + k * 3), (192 + k * 7, 132 + k * 3)], BLEU, 2.4)
    _note(t, 'water is used to flush after using', 236, 14)


def _sc_wc_propre(t):
    latrine(t, 160, 124)
    t.rrect(44, 190, 276, 206, 4, fill=SKY, bord=INK, trait=2)
    for dx in (-70, -20, 36, 86):
        t.ligne([(160 + dx, 212), (160 + dx + 10, 226)], BLEU, 2.2)
    _note(t, 'the floor is mopped and kept dry', 254, 14)


def _sc_assiette_eq(t):
    assiette(t, 160, 136, [(0.34, SAND), (0.33, (214, 150, 132)), (0.33, MINT)])
    _note(t, 'a balanced diet: every class', 238, 14)
    _note(t, 'carbohydrate, protein, vitamin', 266, 13)


def _sc_assiette_des(t):
    assiette(t, 160, 136, [(1.0, SAND)])
    _note(t, 'an unbalanced diet: only one class', 238, 14)


def _sc_repas(t):
    for k, (nom, heure) in enumerate((('breakfast', 'morning'), ('lunch', 'midday'),
                                      ('supper', 'evening'))):
        cx = 66 + k * 94
        assiette(t, cx, 118, [(0.5, SAND), (0.5, MINT)], 30)
        t.texte((cx, 170), nom, 14, INK)
        t.texte((cx, 192), heure, 12, INK_2)
    _note(t, 'the meals of one day', 240, 14)


def _sc_sous(t):
    assiette(t, 160, 132, [(0.22, SAND), (0.78, WHITE_WARM)])
    _note(t, 'less food than the body requires', 236, 14)


def _sc_sur(t):
    assiette(t, 160, 132, [(1.0, SAND)], 72)
    _note(t, 'more food than the body requires', 240, 14)


# --- Couvertures ----------------------------------------------------------

def couv_wc(t):
    _bandeau_couv(t, 'The water closet')
    latrine(t, 470, 296)
    for k in range(4):
        t.ligne([(516 + k * 8, 268 + k * 3), (512 + k * 8, 288 + k * 3)], BLEU, 2.6)


def couv_food(t):
    _bandeau_couv(t, 'Food and its classes')
    for i, dessin in enumerate((poisson, grain, fruit, huile, verre_eau)):
        dessin(t, 336 + i * 72, 300)


def couv_cuisson(t):
    _bandeau_couv(t, 'Preparing food')
    marmite(t, 384, 288)
    feu(t, 384, 322, 0.5)
    cuve(t, 480, 296)
    four(t, 584, 294)


def couv_conserve(t):
    _bandeau_couv(t, 'Preserving food')
    soleil(t, 372, 290)
    frigo(t, 456, 296)
    boite(t, 534, 296)
    bouteille(t, 606, 296)


def couv_regime(t):
    _bandeau_couv(t, 'Diet and meals')
    assiette(t, 420, 290, [(0.34, SAND), (0.33, (214, 150, 132)), (0.33, MINT)], 46)
    assiette(t, 540, 290, [(1.0, SAND)], 46)


FIGURES = [
    # ---- 43. The water closet ---------------------------------------------
    ('bs-wc-couv', 960, 540, couv_wc),
    ('bs-wc-def', 320, 320, _fab_scene(_sc_wc)),
    ('bs-wc-soin', 320, 320, _fab_liste(
        ['Flush it immediately after use', 'Use good and soft toilet tissue',
         'Clean the bowl with disinfectant', 'Do not climb on the sitting pot'],
        'Care of the water closet')),
    ('bs-wc-sol', 320, 320, _fab_scene(_sc_wc_propre)),
    ('bs-wc-murs', 320, 320, _fab_liste(
        ['Mop the floor with disinfectant', 'Always keep the floor dry',
         'Scrub the walls with a brush', 'Remove cobwebs from the ceiling'],
        'Keeping the room clean')),

    # ---- 44. Food and its six classes --------------------------------------
    ('bs-fd-couv', 960, 540, couv_food),
    ('bs-fd-def', 320, 320, _fab_grille([
        (poisson, 'fish'), (grain, 'rice'), (fruit, 'fruit'), (verre_eau, 'water')])),
    ('bs-fd-table', 320, 380, _fab_tableau([
        ('protein', 'fish, eggs', 'builds'),
        ('carbohydrate', 'rice, corn', 'energy'),
        ('fats and oil', 'butter, oil', 'energy'),
        ('mineral salts', 'salt, milk', 'bones'),
        ('vitamins', 'fruits', 'protects'),
        ('water', 'water, juice', 'digestion')])),
    ('bs-fd-prot', 320, 320, _fab_classe(
        poisson, 'proteins', 'fish, meat, eggs, beans: they build and repair')),
    ('bs-fd-carb', 320, 320, _fab_classe(
        grain, 'carbohydrates', 'cassava, rice, corn, bread: they give energy')),
    ('bs-fd-fat', 320, 320, _fab_classe(
        huile, 'fats and oil', 'butter, oil, groundnut: they give energy')),
    ('bs-fd-min', 320, 320, _fab_classe(
        sel, 'mineral salts', 'cooking salt, milk: strong bones and teeth')),
    ('bs-fd-vit', 320, 320, _fab_classe(
        fruit, 'vitamins', 'fruits and vegetables: they prevent diseases')),
    ('bs-fd-eau', 320, 320, _fab_classe(
        verre_eau, 'water', 'water and juice: they ease digestion')),

    # ---- 45. Preparing food -------------------------------------------------
    ('bs-cp-couv', 960, 540, couv_cuisson),
    ('bs-cp-table', 320, 380, _fab_tableau([
        ('boiling', 'egg, rice, yam', 'in water'),
        ('baking', 'bread, cake', 'in an oven'),
        ('steaming', 'koki, egusi', 'in steam'),
        ('grilling', 'meat, fish', 'on fire'),
        ('roasting', 'chicken, fish', 'on fire'),
        ('stewing', 'tomato stew', 'slowly')],
        titres=('method', 'example', 'how'))),
    ('bs-cp-vapeur', 320, 320, _fab_methode(
        cuve, 'steaming', 'koki and egusi pudding')),
    ('bs-cp-four', 320, 320, _fab_methode(four, 'baking', 'bread and cake, in an oven')),
    ('bs-cp-grill', 320, 320, _fab_methode(
        grille_feu, 'grilling', 'meat, fish and chicken')),
    ('bs-cp-friture', 320, 320, _fab_duo(
        (lambda t, x, y: poele(t, x, y), 'shallow frying'),
        (lambda t, x, y: marmite(t, x, y - 4), 'deep frying'),
        'eggs and pancake, or fish and chicken')),
    ('bs-cp-pourquoi', 320, 320, _fab_liste(
        ['To kill germs', 'To make it look attractive', 'To make it taste better',
         'To make it last longer'], 'Why we cook food')),

    # ---- 46. Preserving food -------------------------------------------------
    ('bs-cv-couv', 960, 540, couv_conserve),
    ('bs-cv-table', 320, 380, _fab_tableau([
        ('salting', 'meat, fish', 'with salt'),
        ('drying', 'corn, beans', 'in the air'),
        ('canning', 'fish, grains', 'in a tin'),
        ('bottling', 'water, juice', 'in a bottle'),
        ('smoking', 'meat, fish', 'over fire'),
        ('freezing', 'meat, fish', 'in the cold')],
        titres=('method', 'example', 'how'))),
    ('bs-cv-sec', 320, 320, _fab_methode(
        soleil, 'drying', 'corn, groundnut and beans')),
    ('bs-cv-froid', 320, 320, _fab_methode(
        frigo, 'freezing', 'vegetable, meat and fish')),
    ('bs-cv-boite', 320, 320, _fab_duo(
        (lambda t, x, y: boite(t, x, y), 'canning'),
        (lambda t, x, y: bouteille(t, x, y), 'bottling'),
        'tins for grains, bottles for drinks')),
    ('bs-cv-fumee', 320, 320, _fab_duo(
        (lambda t, x, y: sel(t, x, y), 'salting'),
        (lambda t, x, y: fumee(t, x, y - 6), 'smoking'),
        'both keep meat and fish')),

    # ---- 47. Diet, meals and feeding -------------------------------------------
    ('bs-dt-couv', 960, 540, couv_regime),
    ('bs-dt-diet', 320, 320, _fab_scene(_sc_assiette_eq)),
    ('bs-dt-types', 320, 320, _fab_liste(
        ['Balanced diet: every class present', 'Mixed diet: several classes',
         'Unbalanced diet: one class only'], 'Three types of diet')),
    ('bs-dt-desequilibre', 320, 320, _fab_scene(_sc_assiette_des)),
    ('bs-dt-repas', 320, 320, _fab_scene(_sc_repas)),
    ('bs-dt-sous', 320, 320, _fab_scene(_sc_sous)),
    ('bs-dt-sur', 320, 320, _fab_scene(_sc_sur)),
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
