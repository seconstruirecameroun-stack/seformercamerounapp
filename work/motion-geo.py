# -*- coding: utf-8 -*-
"""
Le mouvement des figures de géographie, pour les films de BRAYNE (CM1).

Quatrième greffe sur work/motion-texte.py, après le français, les
mathématiques et les sciences : le fond, Niba, la bande de phrase et la
boucle de rendu sont les mêmes partout. Seules les scènes changent.

Le geste du film tient en une image : **la carte s-allume**. Un film de
géographie qui réciterait « le coton au Nord, la canne au Centre » ne
vaudrait pas mieux que la liste du cahier. Ici la phrase est dite pendant
que la région s-éclaire sur la silhouette du pays — toujours la même
silhouette, d-un plan à l-autre et d-un film à l-autre.

La carte n-est pas redessinée pour le mouvement. Le contour vient de
work/carte-cameroun.py, les zones sont calculées comme dans
work/figures-geo.py — même ellipse, même rognage au contour. Deux dessins
du même pays finiraient par diverger, et un jour le Nord de la vidéo ne
serait plus le Nord de la leçon.

Elles sont composées une fois en tuiles RGBA, puis posées sur le calque
avec une opacité qui monte. Une zone qui apparaît en fondu se comprend
mieux qu-une zone déjà là : l-œil voit QUE quelque chose s-allume, et où.

Neuf scènes couvrent les deux films :

  champ     la terre retournée, et la houe qui arrive
  deux      le pays, et les deux sortes de cultures de part et d autre
  assiette  le plat de famille qui se remplit
  zone      le pays, une région qui s allume, les cultures qui se posent
  villes    la même carte, et trois villes qui s allument l une après l autre
  ville     les immeubles, et les planches de légumes devant
  usine     l usine, sa fumée, et ce qui en sort
  noms      les trois noms de la même chose, l un sous l autre
  chemins   le champ, et deux chemins : la case et le bateau

Usage comme bibliothèque :  from motion_geo import rendre_plan
"""

import importlib.util
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw

_ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ICI)


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mm = _charger('motion_maths', 'motion-maths.py')
ms = _charger('motion_sciences', 'motion-sciences.py')
fg = _charger('figures_geo', 'figures-geo.py')
cc = _charger('carte_cameroun', 'carte-cameroun.py')

motion = mm.motion
Plan = mm.Plan
_doux = mm._doux
Surface = ms.Surface
BANDE_HAUT, BANDE_BAS, K = mm.BANDE_HAUT, mm.BANDE_BAS, mm.K
LARGEUR = motion.LARGEUR
HAUT_BANDE = BANDE_BAS - BANDE_HAUT

INK, INK_2 = mm.INK, mm.INK_2
WHITE_WARM, SAND, CLAY = mm.WHITE_WARM, motion.SAND, mm.CLAY
GOLD, MINT, LILAC, SKY = mm.GOLD, mm.MINT, mm.LILAC, mm.SKY
VERT, VERT_PALE, TERRE, ROUGE = fg.VERT, fg.VERT_PALE, fg.TERRE, fg.ROUGE

# La carte vit à gauche de la bande, les mots à droite : on lit de gauche à
# droite, et la région doit être vue avant d-être nommée.
CARTE = (96, BANDE_HAUT + 14, 440, BANDE_BAS - 16)
MOTS_X = 820


def _fondu(t, debut, duree=0.4):
    """De 0 à 1 entre `debut` et `debut + duree`, adouci.

    `t` est en SECONDES depuis le début du plan, comme partout dans
    motion-texte.py — et non une fraction de sa durée. Écrit en fractions,
    tout le mouvement se jouait dans le premier dixième de seconde et le
    reste du plan tenait une image fixe.
    """
    return _doux(max(0.0, min(1.0, (t - debut) / duree)))


# ─────────────────────────── la carte, en tuiles ──────────────────────────

_TUILES = {}


def _pts_calque(pts):
    return [(x * K, (y - BANDE_HAUT) * K) for x, y in pts]


def _taille():
    return (LARGEUR * K, HAUT_BANDE * K)


def _masque_pays(boite):
    m = Image.new('L', _taille(), 0)
    ImageDraw.Draw(m).polygon(_pts_calque(cc.contour(boite)), fill=255)
    return m


def _masque_zone(boite, zone):
    lon, lat, rlon, rlat = fg.ZONES[zone]
    f = cc.projeter(boite)
    x0, y0 = f(lon - rlon, lat + rlat)
    x1, y1 = f(lon + rlon, lat - rlat)
    m = Image.new('L', _taille(), 0)
    ImageDraw.Draw(m).ellipse(
        [x0 * K, (y0 - BANDE_HAUT) * K, x1 * K, (y1 - BANDE_HAUT) * K], fill=255)
    return ImageChops.darker(m, _masque_pays(boite))


def _tuile(cle, fabrique):
    if cle not in _TUILES:
        _TUILES[cle] = fabrique()
    return _TUILES[cle]


def _tuile_pays(boite):
    def faire():
        im = Image.new('RGBA', _taille(), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        pts = _pts_calque(cc.contour(boite))
        d.polygon(pts, fill=(*VERT_PALE, 255))
        d.line(pts + [pts[0]], fill=(*INK, 255), width=3 * K, joint='curve')
        return im
    return _tuile(('pays', boite), faire)


def _tuile_zones(boite, zones):
    def faire():
        im = Image.new('RGBA', _taille(), (*VERT, 255))
        masque = Image.new('L', _taille(), 0)
        for z in zones:
            masque = ImageChops.lighter(masque, _masque_zone(boite, z))
        im.putalpha(masque)
        return im
    return _tuile(('zones', boite, tuple(sorted(zones))), faire)


def _poser(plan, tuile, opacite):
    if opacite <= 0.01:
        return
    if opacite >= 0.99:
        plan.im.alpha_composite(tuile)
        return
    copie = tuile.copy()
    copie.putalpha(copie.getchannel('A').point(lambda v: int(v * opacite)))
    plan.im.alpha_composite(copie)


def _carte(plan, t, zones=(), apparition=0.0, allumage=0.28):
    """Le pays, puis les zones qui s-allument. Rend la projection."""
    _poser(plan, _tuile_pays(CARTE), _fondu(t, apparition, 0.25))
    if zones:
        _poser(plan, _tuile_zones(CARTE, zones), _fondu(t, allumage, 0.35))
    return cc.projeter(CARTE)


# ───────────────────────────── les petits objets ──────────────────────────

def _pastille(plan, x, y, texte, taille=36, fond=WHITE_WARM, encre=INK, alpha=255):
    demi = plan.large(texte, taille) / 2 + 26
    plan.rrect(x - demi, y - taille * 0.78, x + demi, y + taille * 0.78,
               taille * 0.62, fill=fond, bord=INK, trait=3, alpha=alpha)
    plan.texte((x, y), texte, taille, encre, alpha)


def _surface(plan, echelle):
    """Une surface pour dessiner les figures de figures-geo à l-échelle.

    Attention au repère : un point (x, y) de la figure atterrit dans le
    cadre en (x × échelle, BANDE_HAUT + y × échelle). Posé à y = 250 avec
    une échelle de 1,7, un objet tombe à 521 — sous la bande, qui s-arrête à
    512. On n-en voyait plus que le toit. `_placer` évite d-avoir à y penser.
    """
    return Surface(plan, ox=0, oy=0, echelle=echelle)


def _placer(plan, echelle, cx, cy, dessin, opacite=1.0):
    """Dessine à (cx, cy) EN COORDONNÉES DU CADRE, quelle que soit l-échelle."""
    s = _surface(plan, echelle)
    if not s.opacite(opacite):
        return
    dessin(s, cx / echelle, (cy - BANDE_HAUT) / echelle)


# Une culture, un dessin. La table est explicite : un film qui montrerait
# une cabosse en disant « le coton » enseignerait le contraire de la leçon.
CULTURES = {
    'mil': lambda s, x, y: fg._epi(s, x, y, 120),
    'maïs': lambda s, x, y: fg._epi(s, x, y, 120, GOLD),
    'sorgho': lambda s, x, y: fg._epi(s, x, y, 120, CLAY),
    'arachides': lambda s, x, y: fg._arachide(s, x, y, 100),
    'pommes de terre': lambda s, x, y: fg._tubercule(s, x, y, 120, 58),
    'ignames': lambda s, x, y: fg._igname(s, x, y, 140),
    'manioc': lambda s, x, y: fg._tubercule(s, x, y, 140, 48),
    'macabo': lambda s, x, y: fg._tubercule(s, x, y, 110, 60, (178, 140, 96)),
    'patate': lambda s, x, y: fg._tubercule(s, x, y, 120, 54, (196, 136, 96)),
    'cacao': lambda s, x, y: fg._cabosse(s, x, y, 120),
    'café': lambda s, x, y: fg._grain_cafe(s, x, y, 26),
    'thé': lambda s, x, y: fg._feuille(s, x, y, 110, 64),
    'coton': lambda s, x, y: fg._coton(s, x, y, 46),
    'canne à sucre': lambda s, x, y: fg._canne(s, x, y, 150),
    'palmier à huile': lambda s, x, y: fg._palmier(s, x, y, 170),
    'tabac': lambda s, x, y: fg._feuille(s, x, y, 140, 86, (150, 176, 100)),
}


def _dessiner_culture(plan, nom, x, y, alpha):
    fait = CULTURES.get(nom)
    if not fait:
        return
    _placer(plan, 1.0, x, y, lambda s, cx, cy: fait(s, cx, cy), alpha / 255.0)


# ─────────────────────────────── les scènes ───────────────────────────────

def _scene_champ(p, par, t):
    del par
    a = _fondu(t, 0.10, 0.45)
    p.rrect(300, 300, 980, 450, 18, fill=TERRE, alpha=255 * a)
    for i in range(5):
        v = _fondu(t, 0.55 + i * 0.18, 0.35)
        p.ligne([(330, 330 + i * 26), (330 + 620 * v, 330 + i * 26)], (138, 96, 66), 6)
    av = _fondu(t, 1.70, 0.55)
    _placer(p, 2.0, 430 - 90 * (1 - av), 236, lambda s, x, y: fg._houe(s, x, y, 110), av)


def _scene_deux(p, par, t):
    _carte(p, t, (), apparition=0.10)
    for i, (cle, defaut, couleur) in enumerate(
            (('gauche', 'vivrières', VERT), ('droite', 'de rente', CLAY))):
        a = _fondu(t, 1.20 + i * 0.85, 0.45)
        if a > 0.01:
            _pastille(p, 900, 220 + i * 130, par.get(cle, defaut), 42,
                      fond=couleur, encre=WHITE_WARM, alpha=255 * a)


def _scene_assiette(p, par, t):
    a = _fondu(t, 0.10, 0.45)
    p.disque((640, 340), 148, fill=WHITE_WARM, bord=INK, trait=5, alpha=255 * a)
    p.disque((640, 340), 114, fill=SAND, bord=INK_2, trait=3, alpha=255 * a)
    for i, nom in enumerate(('manioc', 'mil', 'arachides')):
        v = _fondu(t, 1.00 + i * 0.55, 0.40)
        _dessiner_culture(p, nom, 558 + i * 84, 340 + (24 if i == 1 else -14), 255 * v)
    note = par.get('note')
    if note:
        n = _fondu(t, 2.70, 0.45)
        if n > 0.01:
            _pastille(p, 640, 160, note, 32, alpha=255 * n)


def _scene_zone(p, par, t):
    f = _carte(p, t, par.get('zones', ()), apparition=0.08, allumage=0.95)
    del f
    cultures = par.get('cultures', [])
    for i, nom in enumerate(cultures):
        a = _fondu(t, 1.55 + i * 0.38, 0.38)
        if a <= 0.01:
            continue
        y = 200 + i * 86 - (len(cultures) - 1) * 43 + 110
        _pastille(p, MOTS_X + 120, y, nom, 38, alpha=255 * a)
    if cultures:
        _dessiner_culture(p, cultures[0], 600, 300, 255 * _fondu(t, 1.50, 0.45))


def _scene_villes(p, par, t):
    f = _carte(p, t, par.get('zones', ('nord',)), apparition=0.08, allumage=0.60)
    for i, nom in enumerate(par.get('villes', [])):
        a = _fondu(t, 1.40 + i * 0.62, 0.38)
        if a <= 0.01:
            continue
        x, y = f(*cc.VILLES[nom])
        p.disque((x, y), 11 + 5 * (1 - a), fill=CLAY, bord=WHITE_WARM, trait=3,
                 alpha=255 * a)
        _pastille(p, MOTS_X, 190 + i * 110, nom, 40, alpha=255 * a)


def _scene_ville(p, par, t):
    for i, h in enumerate((120, 180, 150, 200, 130)):
        a = _fondu(t, 0.10 + i * 0.20, 0.35)
        x = 420 + i * 110
        p.rrect(x - 44, 330 - h, x + 44, 330, 8, fill=SAND, bord=INK, trait=3,
                alpha=255 * a)
        for k in range(h // 60):
            p.rrect(x - 24, 330 - h + 26 + k * 52, x + 24, 330 - h + 56 + k * 52, 4,
                    fill=WHITE_WARM, bord=INK_2, trait=2, alpha=255 * a)
    j = _fondu(t, 1.55, 0.45)
    p.rrect(360, 346, 980, 486, 16, fill=(150, 178, 126), bord=INK, trait=3,
            alpha=255 * j)
    for i in range(3):
        v = _fondu(t, 1.95 + i * 0.32, 0.40)
        for k in range(7):
            _placer(p, 1.0, 400 + k * 90, 384 + i * 44, 
                    lambda s, x, y: fg._feuille(s, x, y, 56, 30, (176, 206, 150), False), v)
    note = par.get('note')
    if note:
        n = _fondu(t, 2.90, 0.40)
        if n > 0.01:
            _pastille(p, 670, 134, note, 30, alpha=255 * n)


def _scene_usine(p, par, t):
    del par
    a = _fondu(t, 0.10, 0.45)
    _placer(p, 2.2, 506, 338, lambda s, x, y: fg._usine(s, x, y, 92), a)
    for i in range(3):
        v = _fondu(t, 1.20 + i * 0.42, 0.55)
        if v <= 0.01:
            continue
        p.disque((690 - i * 10, 306 - i * 54 - 24 * v), 24 + i * 7,
                 fill=(226, 224, 220), alpha=255 * v * (1 - 0.3 * i))
    b = _fondu(t, 2.10, 0.50)
    _placer(p, 1.8, 920 + 60 * b, 420, lambda s, x, y: fg._navire(s, x, y), b)


def _scene_noms(p, par, t):
    noms = par.get('noms', [])
    for i, nom in enumerate(noms):
        a = _fondu(t, 0.45 + i * 0.85, 0.42)
        if a <= 0.01:
            continue
        _pastille(p, 640, 190 + i * 110, nom, 44,
                  fond=(CLAY if i == len(noms) - 1 else WHITE_WARM),
                  encre=(WHITE_WARM if i == len(noms) - 1 else INK), alpha=255 * a)


def _scene_chemins(p, par, t):
    a = _fondu(t, 0.10, 0.45)
    p.rrect(500, 172, 790, 278, 14, fill=TERRE, bord=INK, trait=3, alpha=255 * a)
    for i in range(2):
        p.ligne([(520, 206 + i * 36), (770, 206 + i * 36)], (138, 96, 66), 5,
                alpha=255 * a)
    p.texte((645, 142), 'le champ', 32, INK, 255 * a)

    g = _fondu(t, 1.25, 0.45)
    d = _fondu(t, 1.95, 0.45)
    if g > 0.01:
        p.ligne([(500, 252), (500 - 150 * g, 252 + 110 * g)], VERT, 7, alpha=255 * g)
    if d > 0.01:
        p.ligne([(790, 252), (790 + 150 * d, 252 + 110 * d)], CLAY, 7, alpha=255 * d)
    _placer(p, 1.7, 330, 398, lambda s, x, y: fg._case(s, x, y, 70),
            _fondu(t, 1.80, 0.45))
    _placer(p, 1.5, 980, 404, lambda s, x, y: fg._navire(s, x, y),
            _fondu(t, 2.45, 0.45))
    note = par.get('note')
    if note:
        # La note se pose SOUS la scène. Posée en haut, elle recouvrait
        # l-étiquette du champ et on lisait « vers ailleurs » à sa place.
        n = _fondu(t, 3.10, 0.40)
        if n > 0.01:
            _pastille(p, 640, 478, note, 30, alpha=255 * n)


SCENES = {
    'champ': _scene_champ, 'deux': _scene_deux, 'assiette': _scene_assiette,
    'zone': _scene_zone, 'villes': _scene_villes, 'ville': _scene_ville,
    'usine': _scene_usine, 'noms': _scene_noms, 'chemins': _scene_chemins,
}


def _adapter(fn):
    def dessin(d, par, t):
        plan = Plan()
        fn(plan, par, t)
        plan.poser(d)
    return dessin


motion.SCENES.update({nom: _adapter(fn) for nom, fn in SCENES.items()})

rendre_plan = motion.rendre_plan


def controler():
    """Ce que le film montre doit être ce que la leçon dit."""
    import json

    # Toutes les scènes des scripts doivent exister ici, et toutes les
    # cultures citées doivent avoir un dessin : un plan qui ne dessinerait
    # rien pendant que la voix nomme une culture serait un plan vide.
    manquantes, sans_dessin = set(), set()
    for cle in ('vivrieres', 'rente'):
        chemin = os.path.join(_ICI, 'video-' + cle, 'script_manifest.json')
        manifeste = json.load(open(chemin, encoding='utf-8'))
        for bloc in manifeste['blocks']:
            s = bloc['scene']
            if s['scene'] not in SCENES:
                manquantes.add(s['scene'])
            for nom in s.get('cultures', []):
                if nom not in CULTURES:
                    sans_dessin.add(nom)
    assert not manquantes, 'scène sans mouvement : ' + ', '.join(sorted(manquantes))
    assert not sans_dessin, 'culture sans dessin : ' + ', '.join(sorted(sans_dessin))

    # La carte doit tenir dans la bande, sinon le haut du pays passe derrière
    # la phrase et la pointe du lac Tchad disparaît.
    for x, y in cc.contour(CARTE):
        assert BANDE_HAUT <= y <= BANDE_BAS, 'la carte sort de la bande : %.0f' % y
        assert 0 <= x <= LARGEUR, 'la carte sort du cadre : %.0f' % x

    # Et chaque zone doit exister à cette échelle-là aussi.
    for zone in fg.ZONES:
        assert _masque_zone(CARTE, zone).getbbox() is not None, 'zone vide : ' + zone

    # Rien ne doit toucher le bord de la bande. Un dessin posé trop bas y est
    # COUPÉ, sans que rien ne le signale : la case du plan « deux chemins »
    # tombait à 521 pour une bande qui s-arrête à 512, et il n-en restait que
    # le toit. Un objet qui mord le bord est un objet tronqué.
    coupes = []
    for cle in ('vivrieres', 'rente'):
        chemin = os.path.join(_ICI, 'video-' + cle, 'script_manifest.json')
        for bloc in json.load(open(chemin, encoding='utf-8'))['blocks']:
            par = dict(bloc['scene'])
            for seconde in (0.4, 1.2, 2.0, 2.8, 3.6, 4.4):
                plan = Plan()
                SCENES[par['scene']](plan, par, seconde)
                a = plan.im.getchannel('A')
                haut = a.crop((0, 0, a.width, 2)).getbbox()
                bas = a.crop((0, a.height - 2, a.width, a.height)).getbbox()
                if haut or bas:
                    coupes.append('%s à %.1f s (%s)'
                                  % (par['scene'], seconde, 'haut' if haut else 'bas'))
    assert not coupes, 'dessin coupé par le bord de la bande : ' + ' · '.join(sorted(set(coupes)))


if __name__ == '__main__':
    controler()
    print('%d scenes - %d cultures dessinees - controle ok'
          % (len(SCENES), len(CULTURES)))
