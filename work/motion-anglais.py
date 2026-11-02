# -*- coding: utf-8 -*-
"""
Le mouvement des films d'anglais : Unit 13, Wood work and building.

Quatrième greffe sur work/motion-texte.py, après le français, les
mathématiques et les sciences. Le fond, Niba, la bande de phrase, les
pastilles et la boucle de rendu ne bougent pas ; seules les scènes changent.

Comme pour les sciences, rien n'est redessiné : les outils, le mur, la table
et le mortier viennent de work/figures-anglais.py et sont mis en mouvement
tels quels à travers la surface de work/motion-sciences.py.

Ce que ces films doivent faire, et qui commande tout le reste : KLEIN a
échangé builder et carpenter dans son cahier. Le film ne récite donc pas les
définitions l'une après l'autre — il les **oppose**. La scène `tri` pose un
énoncé de l'exercice et allume le bon métier parmi les trois, et c'est elle
qui porte le film.

  metier     l’objet du métier se construit, puis son nom arrive
  tri        un énoncé, trois métiers, et celui qui s-allume
  outils     les trois outils, chacun avec son étiquette
  chisel     deux ciseaux côte à côte, et ce qui les distingue
  adjectif   une phrase, et l-adjectif qui s-y détache
  sansphrase « heavier » barré, puis la vraie phrase qui se construit
  capitale   common sans majuscule, proper avec la sienne en or
  nombre     les tuiles 2 5 1, puis les mots qui arrivent
  trait      le trait d’union qui vient souder les deux mots
  suite      298, 299, puis 300 qui se détache

Usage comme bibliothèque :  from motion_anglais import rendre_plan
"""

import importlib.util
import os
import sys

_ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ICI)


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ms = _charger('motion_sciences', 'motion-sciences.py')
fa = _charger('figures_anglais', 'figures-anglais.py')

motion = ms.motion
Plan = ms.Plan
Surface = ms.Surface
_surface = ms._surface
_doux = ms._doux
HAUT_BANDE = ms.HAUT_BANDE

INK, INK_2 = ms.INK, ms.INK_2
WHITE_WARM, SAND, CLAY = ms.WHITE_WARM, ms.SAND, ms.CLAY
GOLD, MINT, LILAC, SKY, BLEU = ms.GOLD, ms.MINT, ms.LILAC, ms.SKY, ms.BLEU
fs = ms.fs

METIERS = ('builder', 'carpenter', 'carver')
TONS_METIER = {'builder': SKY, 'carpenter': MINT, 'carver': SAND}


def _carte(s, cx, cy, large, haut, ton, alpha=255):
    s.opacite(alpha / 255)
    s.rrect(cx - large / 2, cy - haut / 2, cx + large / 2, cy + haut / 2, 24,
            fill=ton, bord=(255, 255, 255), trait=4)


def _objet_du_metier(s, metier, cx, cy, part):
    """Ce que produit le métier, construit en proportion de `part`."""
    if metier == 'builder':
        # Le mur monte rang par rang : on voit le builder bâtir.
        rangs = max(1, int(round(part * 5)))
        fa._mur(s, cx - 105, cy - 40, 210, 22 * rangs, rangs=rangs)
    elif metier == 'carpenter':
        fa._table(s, cx, cy - 10, 250 * part)
    else:
        fa._mortier(s, cx, cy - 16, 190 * part)


def _scene_metier(p, par, t):
    metier = par['metier']
    s = _surface(p, 760, 420)
    part = _doux((t - 0.3) / 1.4)
    if part > 0:
        s.opacite(1.0)
        _objet_du_metier(s, metier, 360, 170, part)
    a = _doux((t - 1.9) / 0.5)
    if a > 0:
        # La carte se pose SOUS l’objet, assez bas pour ne pas l’entamer :
        # un nom qui chevauche la chose qu’il nomme brouille les deux.
        _carte(s, 360, 358, 420, 76, TONS_METIER[metier], 255 * a)
        s.opacite(a)
        s.texte((360, 358), metier, 46, INK)
    o = _doux((t - 2.6) / 0.5)
    if o > 0 and par.get('outil'):
        s.opacite(o)
        if par['outil'] == 'trowel':
            fa._truelle(s, 648, 150, 120, angle=-0.38)
        elif par['outil'] == 'saw':
            fa._scie(s, 634, 140, 180)
        else:
            fa._ciseau(s, 648, 130, 150, arrondi=True)


def _scene_tri(p, par, t):
    """Un énoncé de l'exercice, et le bon métier qui s'allume.

    C'est la scène du film : elle rejoue exactement la question où KLEIN a
    répondu de travers, et la réponse se montre au lieu de se dire.
    """
    s = _surface(p, 860, 400)
    a = _doux(t / 0.5)
    if a > 0:
        s.opacite(a)
        s.rrect(40, 30, 820, 120, 24, fill=WHITE_WARM, bord=(255, 255, 255), trait=4)
        s.texte((430, 75), par['enonce'], 36, INK)

    bon = par['metier']
    revele = _doux((t - 1.6) / 0.7)
    for i, m in enumerate(METIERS):
        v = _doux((t - (0.8 + i * 0.22)) / 0.4)
        if v <= 0:
            continue
        cx = 160 + i * 270
        gagnant = m == bon
        # Avant la révélation, les trois sont pareils : l'enfant choisit.
        ton = TONS_METIER[m] if (gagnant and revele > 0.5) else WHITE_WARM
        _carte(s, cx, 250, 240, 96, ton, 255 * v)
        s.opacite(v)
        s.texte((cx, 250), m, 34, INK if (gagnant and revele > 0.5) else INK_2)
        if gagnant and revele > 0.5:
            s.opacite(revele)
            fs._coche(s, cx + 100, 206, 22, True)
    if revele > 0.8:
        s.opacite(_doux((t - 2.5) / 0.5))
        s.texte((430, 358), par.get('note', ''), 30, CLAY)


def _scene_outils(p, par, t):
    s = _surface(p, 820, 400)
    for i, (nom, metier) in enumerate((('trowel', 'builder'), ('saw', 'carpenter'),
                                       ('gouge', 'carver'))):
        v = _doux((t - (0.3 + i * 0.7)) / 0.5)
        if v <= 0:
            continue
        y = 90 + i * 110
        s.opacite(v)
        s.rrect(40, y - 44, 300, y + 44, 22, fill=TONS_METIER[metier],
                bord=(255, 255, 255), trait=3)
        s.texte((170, y), nom, 36, INK)
        if i == 0:
            fa._truelle(s, 520, y, 120, angle=-0.38)
        elif i == 1:
            fa._scie(s, 500, y, 180)
        else:
            fa._ciseau(s, 520, y - 8, 140, arrondi=True)
        s.opacite(v)
        s.texte((720, y), metier, 28, INK_2)


def _scene_chisel(p, par, t):
    s = _surface(p, 700, 400)
    for i, (arrondi, mot) in enumerate(((False, 'carpenter'), (True, 'carver'))):
        v = _doux((t - (0.3 + i * 0.8)) / 0.5)
        if v <= 0:
            continue
        cx = 220 + i * 270
        s.opacite(v)
        fa._ciseau(s, cx, 170, 220, arrondi=arrondi)
        s.texte((cx, 310), mot, 32, INK_2)
    v = _doux((t - 2.2) / 0.6)
    if v > 0:
        s.opacite(v)
        s.texte((350, 372), 'same name, two tools', 32, CLAY)


def _scene_adjectif(p, par, t):
    """Une phrase, et l'adjectif qui s'y détache."""
    s = _surface(p, 900, 320)
    mots = par['mots']
    vise = par['adjectif']
    pol = 54
    larges = [s.p.large(m + ' ', pol * s.e) / s.e for m in mots]
    total = sum(larges)
    x = 450 - total / 2
    for i, m in enumerate(mots):
        a = _doux((t - (0.2 + i * 0.3)) / 0.35)
        if a <= 0:
            continue
        s.opacite(a)
        if i == vise:
            v = _doux((t - (0.2 + len(mots) * 0.3 + 0.4)) / 0.5)
            if v > 0:
                s.opacite(v)
                s.rrect(x - 8, 150 - pol * 0.68, x + larges[i] - 6, 150 + pol * 0.52,
                        14, fill=MINT)
            s.opacite(a)
        s.texte((x, 150), m, pol, INK, 'lm')
        x += larges[i]
    v = _doux((t - (0.2 + len(mots) * 0.3 + 0.9)) / 0.5)
    if v > 0:
        s.opacite(v)
        s.texte((450, 262), par.get('note', 'adjective'), 34, CLAY)


def _scene_sansphrase(p, par, t):
    """« heavier » barré, puis la vraie phrase qui se construit."""
    s = _surface(p, 760, 380)
    a = _doux(t / 0.5)
    if a > 0:
        s.opacite(a)
        s.rrect(220, 30, 540, 116, 22, fill=(226, 196, 190), bord=(255, 255, 255), trait=3)
        s.texte((380, 73), par['faux'], 44, INK_2)
    barre = _doux((t - 1.1) / 0.5)
    if barre > 0:
        s.opacite(1.0)
        s.ligne([(236, 73), (236 + 288 * barre, 73)], CLAY, 7)
    mots = par['vrais']
    pol = 44
    larges = [s.p.large(m + ' ', pol * s.e) / s.e for m in mots]
    x = 380 - sum(larges) / 2
    for i, m in enumerate(mots):
        v = _doux((t - (1.9 + i * 0.32)) / 0.36)
        if v <= 0:
            continue
        s.opacite(v)
        s.texte((x, 230 + (1 - v) * 22), m, pol, INK, 'lm')
        x += larges[i]
    f = _doux((t - (1.9 + len(mots) * 0.32 + 0.3)) / 0.4)
    if f > 0:
        s.opacite(f)
        s.texte((380, 330), 'that is a sentence', 32, CLAY)


def _scene_capitale(p, par, t):
    """Common sans majuscule, proper avec la sienne, qui passe à l'or."""
    s = _surface(p, 820, 360)
    mot, nom = par['mot'], par['nom']
    propre = par.get('propre', False)
    a = _doux(t / 0.5)
    if a <= 0:
        return
    pol = 54
    tete, reste = mot[0], mot[1:]
    lt = s.p.large(tete, pol * s.e) / s.e
    lr = s.p.large(reste + ' ' + nom, pol * s.e) / s.e
    x = 410 - (lt + lr) / 2
    s.opacite(a)
    v = _doux((t - 1.4) / 0.6) if propre else 0.0
    if v > 0:
        s.opacite(v)
        s.rrect(x - 10, 150 - pol * 0.68, x + lt + 8, 150 + pol * 0.52, 12, fill=GOLD)
    s.opacite(a)
    # Le décalage de huit pixels n’existe que pour dégager la pastille dorée.
    # Appliqué sans elle, il ouvrait un blanc au milieu du mot : « o ld ».
    ecart = 8 if propre else 0
    s.texte((x + lt / 2 - 1, 150), tete.upper() if propre else tete, pol,
            WHITE_WARM if v > 0.5 else INK)
    s.texte((x + lt + ecart, 150), reste + ' ' + nom, pol, INK, 'lm')
    n = _doux((t - 2.2) / 0.5)
    if n > 0:
        s.opacite(n)
        s.texte((410, 268), par['note'], 34, CLAY)


def _scene_nombre(p, par, t):
    s = _surface(p, 900, 380)
    chiffres = par['chiffres']
    for i, c in enumerate(chiffres):
        v = _doux((t - (0.25 + i * 0.3)) / 0.35)
        if v <= 0:
            continue
        s.opacite(v)
        cx = 450 - (len(chiffres) - 1) * 90 + i * 180
        s.rrect(cx - 72, 40, cx + 72, 196, 24, fill=(WHITE_WARM, SAND, MINT)[i % 3],
                bord=(255, 255, 255), trait=4)
        s.texte((cx, 118), c, 100, INK)
    mots = par['mots']
    pol = 42
    larges = [s.p.large(m + ' ', pol * s.e) / s.e for m in mots]
    x = 450 - sum(larges) / 2
    for i, m in enumerate(mots):
        v = _doux((t - (1.5 + i * 0.4)) / 0.4)
        if v <= 0:
            continue
        s.opacite(v)
        s.texte((x, 280), m, pol, INK, 'lm')
        x += larges[i]


def _scene_trait(p, par, t):
    """Le trait d'union qui vient souder les deux morceaux."""
    s = _surface(p, 760, 320)
    a, b = par['gauche'], par['droite']
    pol = 54
    la = s.p.large(a, pol * s.e) / s.e
    lb = s.p.large(b, pol * s.e) / s.e
    v = _doux((t - 1.0) / 0.8)
    # L’écart final reste assez large pour qu’un TRAIT s’y voie : refermé à
    # vingt-six pixels, le trait d’union se lisait comme un point.
    ecart = 70 * (1 - v) + 44
    x = 380 - (la + lb + ecart) / 2
    ap = _doux(t / 0.5)
    if ap <= 0:
        return
    s.opacite(ap)
    s.texte((x, 150), a, pol, INK, 'lm')
    s.texte((x + la + ecart, 150), b, pol, INK, 'lm')
    if v > 0.25:
        s.opacite(1.0)
        s.rrect(x + la + 8, 146, x + la + ecart - 8, 155, 5, fill=CLAY)
    n = _doux((t - 2.2) / 0.5)
    if n > 0:
        s.opacite(n)
        s.texte((380, 250), par['note'], 32, CLAY)


def _scene_suite(p, par, t):
    s = _surface(p, 560, 400)
    for i, n in enumerate(par['nombres']):
        v = _doux((t - (0.3 + i * 0.7)) / 0.45)
        if v <= 0:
            continue
        dernier = i == len(par['nombres']) - 1
        s.opacite(v)
        s.rrect(140, 30 + i * 118, 420, 130 + i * 118, 22,
                fill=GOLD if dernier else WHITE_WARM, bord=(255, 255, 255), trait=4)
        s.texte((280, 80 + i * 118), n, 58, WHITE_WARM if dernier else INK)
    f = _doux((t - 2.6) / 0.5)
    if f > 0:
        s.opacite(f)
        s.texte((280, 384), par['note'], 30, CLAY)


SCENES = {
    'metier': _scene_metier, 'tri': _scene_tri, 'outils': _scene_outils,
    'chisel': _scene_chisel, 'adjectif': _scene_adjectif,
    'sansphrase': _scene_sansphrase, 'capitale': _scene_capitale,
    'nombre': _scene_nombre, 'trait': _scene_trait, 'suite': _scene_suite,
}


def _adapter(fn):
    def dessin(d, par, t):
        plan = Plan()
        fn(plan, par, t)
        plan.poser(d)
    return dessin


motion.SCENES.update({nom: _adapter(fn) for nom, fn in SCENES.items()})

rendre_plan = motion.rendre_plan
