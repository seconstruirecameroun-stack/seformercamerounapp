# -*- coding: utf-8 -*-
"""
Le mouvement des mots, pour les films de français.

Rien n'est généré ici : chaque image est composée, en Fredoka, la police de
l'application. C'est ce qui permet d'écrire « cailloux » sans craindre qu'un
générateur en fasse « caillouxs », et de corriger un mot sans repayer une
image.

Sept scènes suffisent aux trois films, et chacune est le geste de sa règle :

  phrase      les mots entrent un par un, de gauche à droite
  remplace    un mot se soulève et s'efface, un autre descend à sa place
  rangement   les mots arrivent en désordre, puis glissent jusqu'à leur rang
  bornes      la première lettre grandit, un point tombe à la fin
  blocs       la phrase se sépare en deux rectangles de couleurs
  liste       les mots apparaissent l'un après l'autre, en grille
  suffixe     un mot au singulier, puis sa lettre de pluriel qui arrive

Le cadre est partagé : la typographie occupe les deux tiers hauts, Niba et la
bande de phrase gardent le bas, les mots du cahier le coin haut droit.

Usage comme bibliothèque :  from motion_texte import rendre_plan
"""

import math
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from niba import dessiner  # noqa: E402

import imageio_ffmpeg  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
LARGEUR, HAUTEUR = 1280, 720
IPS = 24
MARGE = 36
POLICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fredoka.ttf')

INK = (43, 64, 71)
INK_2 = (90, 112, 118)
WHITE_WARM = (255, 251, 244)
SAND = (246, 230, 201)
CLAY = (201, 112, 63)
GOLD = (231, 174, 74)
MINT = (189, 232, 214)
LILAC = (217, 206, 235)
SKY = (185, 212, 238)

# La zone de jeu typographique : au-dessus de Niba et de la bande de phrase.
SCENE_HAUT, SCENE_BAS = 130, 470
SCENE_MILIEU = (SCENE_HAUT + SCENE_BAS) // 2


def _fond():
    """Un dégradé pastel calme, calculé une fois et réutilisé."""
    petit = Image.new('RGB', (2, HAUTEUR))
    d = ImageDraw.Draw(petit)
    for y in range(HAUTEUR):
        t = y / (HAUTEUR - 1)
        d.line([(0, y), (1, y)], fill=(
            int(MINT[0] + (SAND[0] - MINT[0]) * t),
            int(MINT[1] + (SAND[1] - MINT[1]) * t),
            int(MINT[2] + (SAND[2] - MINT[2]) * t),
        ))
    return petit.resize((LARGEUR, HAUTEUR), Image.BILINEAR)


FOND = _fond()


def _doux(t):
    """Une accélération puis un freinage : rien ne démarre ni ne s'arrête net."""
    t = max(0.0, min(1.0, t))
    return 0.5 - 0.5 * math.cos(math.pi * t)


def _police(taille):
    return ImageFont.truetype(POLICE, taille)


def _largeur(d, texte, pol):
    return d.textlength(texte, font=pol)


def _mot(d, texte, x, y, pol, couleur=INK, alpha=255):
    """Un mot posé par son coin haut gauche, avec une opacité."""
    if alpha >= 250:
        d.text((x, y), texte, font=pol, fill=couleur)
        return
    calque = Image.new('RGBA', (LARGEUR, HAUTEUR), (0, 0, 0, 0))
    ImageDraw.Draw(calque).text((x, y), texte, font=pol, fill=(*couleur, alpha))
    d._image.alpha_composite(calque)


def _taille_qui_tient(mots, espace, taille_max=86, taille_min=44):
    """La plus grande taille où la phrase tient dans la largeur utile."""
    img = Image.new('RGB', (10, 10))
    d = ImageDraw.Draw(img)
    for taille in range(taille_max, taille_min - 1, -2):
        pol = _police(taille)
        total = sum(_largeur(d, m, pol) for m in mots) + espace * (len(mots) - 1)
        if total <= LARGEUR - 2 * (MARGE + 40):
            return taille
    return taille_min


# ───────────────────────────── les sept scènes ─────────────────────────────

def _positions(d, mots, pol, espace):
    total = sum(_largeur(d, m, pol) for m in mots) + espace * (len(mots) - 1)
    x = (LARGEUR - total) / 2
    pos = []
    for m in mots:
        pos.append(x)
        x += _largeur(d, m, pol) + espace
    return pos


def _scene_phrase(d, p, t):
    mots, pol, espace = p['mots'], p['_pol'], p['_espace']
    pos = _positions(d, mots, pol, espace)
    y = SCENE_MILIEU - pol.size // 2
    for i, m in enumerate(mots):
        debut = 0.08 + i * 0.13
        a = _doux((t - debut) / 0.3)
        if a <= 0:
            continue
        couleur = CLAY if p.get('accent') == i else INK
        _mot(d, m, pos[i], y + (1 - a) * 26, pol, couleur, int(255 * a))


def _scene_remplace(d, p, t):
    mots, pol, espace = p['mots'], p['_pol'], p['_espace']
    i = p['remplacer']
    nouveau = p['par']
    # La phrase se pose, puis le mot visé s'en va et l'autre descend.
    pos = _positions(d, mots, pol, espace)
    y = SCENE_MILIEU - pol.size // 2
    for j, m in enumerate(mots):
        a = _doux((t - (0.08 + j * 0.12)) / 0.3)
        if a <= 0:
            continue
        if j == i:
            depart = _doux((t - 0.95) / 0.45)   # il se soulève et s'efface
            if depart > 0:
                _mot(d, m, pos[j], y - depart * 70, pol, CLAY,
                     int(255 * a * (1 - depart)))
            else:
                _mot(d, m, pos[j], y, pol, CLAY, int(255 * a))
        else:
            _mot(d, m, pos[j], y, pol, INK, int(255 * a))
    arrivee = _doux((t - 1.25) / 0.5)
    if arrivee > 0:
        _mot(d, nouveau, pos[i], y - (1 - arrivee) * 70, pol, CLAY,
             int(255 * arrivee))


def _scene_rangement(d, p, t):
    mots, pol, espace = p['mots'], p['_pol'], p['_espace']
    pos = _positions(d, mots, pol, espace)
    y = SCENE_MILIEU - pol.size // 2
    # Un désordre stable : même graine pour tous les plans.
    desordre = [(-180, -70), (150, 60), (-90, 80), (190, -60), (40, 95)]
    a = _doux((t - 0.5) / 1.5)
    for j, m in enumerate(mots):
        dx, dy = desordre[j % len(desordre)]
        _mot(d, m, pos[j] + dx * (1 - a), y + dy * (1 - a), pol, INK,
             int(255 * min(1.0, 0.35 + t)))


def _scene_bornes(d, p, t):
    mots, pol, espace = p['mots'], p['_pol'], p['_espace']
    pos = _positions(d, mots, pol, espace)
    y = SCENE_MILIEU - pol.size // 2
    # La première lettre grandit, donc le premier mot s'élargit : tout ce qui
    # suit doit reculer d'autant, sinon « Les femmes » devient « Lesfemmes ».
    g = _doux((t - 0.7) / 0.6)
    grande = _police(int(pol.size * (1 + 0.45 * g)))
    pousse = _largeur(d, mots[0][0], grande) - _largeur(d, mots[0][0], pol)
    for j, m in enumerate(mots):
        if j == 0:
            _mot(d, m[0], pos[j], y - (grande.size - pol.size) * 0.78, grande,
                 CLAY if g > 0.1 else INK)
            _mot(d, m[1:], pos[j] + _largeur(d, m[0], grande), y, pol, INK)
        else:
            _mot(d, m, pos[j] + pousse, y, pol, INK)
    # Le point tombe à la fin.
    chute = _doux((t - 1.6) / 0.5)
    if chute > 0:
        fin = pos[-1] + pousse + _largeur(d, mots[-1], pol)
        r = pol.size * 0.11
        cy = y + pol.size * 0.82 - (1 - chute) * 130
        d.ellipse([fin + 6, cy - r, fin + 6 + 2 * r, cy + r], fill=CLAY)


def _scene_blocs(d, p, t):
    mots, pol, espace = p['mots'], p['_pol'], p['_espace']
    coupure = p['coupure']
    pos = _positions(d, mots, pol, espace)
    y = SCENE_MILIEU - pol.size // 2
    ecart = _doux((t - 0.8) / 0.8) * 34
    gauche = [x - ecart for x in pos[:coupure]]
    droite = [x + ecart for x in pos[coupure:]]
    cadre = _doux((t - 1.3) / 0.6)
    if cadre > 0:
        for groupe, mts, couleur in ((gauche, mots[:coupure], SKY),
                                     (droite, mots[coupure:], LILAC)):
            x0 = groupe[0] - 18
            x1 = groupe[-1] + _largeur(d, mts[-1], pol) + 18
            d.rounded_rectangle([x0, y - 16, x1, y + pol.size + 16], radius=20,
                                fill=couleur)
    for x, m in zip(gauche, mots[:coupure]):
        _mot(d, m, x, y, pol, INK)
    for x, m in zip(droite, mots[coupure:]):
        _mot(d, m, x, y, pol, INK)
    if p.get('souligner') is not None:
        s = _doux((t - 2.0) / 0.6)
        if s > 0:
            # On souligne le groupe entier : « les femmes », pas « les ». Un
            # trait sous le seul article apprendrait le contraire de la règle.
            groupe = gauche if p['souligner'] == 0 else droite
            mts = mots[:coupure] if p['souligner'] == 0 else mots[coupure:]
            base = groupe[0]
            large = groupe[-1] + _largeur(d, mts[-1], pol) - base
            d.rounded_rectangle([base, y + pol.size + 6, base + large * s,
                                 y + pol.size + 13], radius=4, fill=CLAY)


def _scene_liste(d, p, t):
    mots = p['mots']
    colonnes = p.get('colonnes', 4)
    lignes = (len(mots) + colonnes - 1) // colonnes
    pol = _police(66 if len(mots) <= 6 else 58)
    hauteur_ligne = pol.size + 34
    y0 = SCENE_MILIEU - (lignes * hauteur_ligne) // 2
    for i, m in enumerate(mots):
        a = _doux((t - (0.25 + i * 0.22)) / 0.35)
        if a <= 0:
            continue
        col, lig = i % colonnes, i // colonnes
        dans_ligne = mots[lig * colonnes:(lig + 1) * colonnes]
        largeurs = [_largeur(d, x, pol) for x in dans_ligne]
        total = sum(largeurs) + 56 * (len(dans_ligne) - 1)
        x = (LARGEUR - total) / 2 + sum(largeurs[:col]) + 56 * col
        y = y0 + lig * hauteur_ligne
        if p.get('accent_final'):
            tete, queue = m[:-1], m[-1]
            _mot(d, tete, x, y, pol, INK, int(255 * a))
            _mot(d, queue, x + _largeur(d, tete, pol), y, pol, CLAY, int(255 * a))
        else:
            _mot(d, m, x, y, pol, INK, int(255 * a))


def _scene_suffixe(d, p, t):
    pol = _police(78)
    y = SCENE_MILIEU - pol.size // 2
    # D'abord le singulier, seul et centré.
    sing = p['singulier']
    a1 = _doux((t - 0.15) / 0.4)
    sortie = _doux((t - 1.2) / 0.4)
    if a1 > 0 and sortie < 1:
        x = (LARGEUR - _largeur(d, sing, pol)) / 2
        _mot(d, sing, x, y - sortie * 60, pol, INK, int(255 * a1 * (1 - sortie)))
    # Puis le pluriel, auquel la lettre vient s'ajouter.
    a2 = _doux((t - 1.5) / 0.4)
    if a2 > 0:
        plur, lettre = p['pluriel'], p['lettre']
        l_plur = _largeur(d, plur, pol)
        l_lettre = _largeur(d, lettre, pol)
        x = (LARGEUR - (l_plur + l_lettre)) / 2
        _mot(d, plur, x, y, pol, INK, int(255 * a2))
        venue = _doux((t - 2.1) / 0.55)
        if venue > 0:
            _mot(d, lettre, x + l_plur + (1 - venue) * 150, y, pol, CLAY,
                 int(255 * venue))


SCENES = {
    'phrase': _scene_phrase, 'remplace': _scene_remplace,
    'rangement': _scene_rangement, 'bornes': _scene_bornes,
    'blocs': _scene_blocs, 'liste': _scene_liste, 'suffixe': _scene_suffixe,
}


# ──────────────────────────── le cadre complet ────────────────────────────

def _coupe(texte, pol, largeur_max, d):
    lignes, courante = [], ''
    for mot in texte.split():
        essai = (courante + ' ' + mot).strip()
        if d.textlength(essai, font=pol) <= largeur_max:
            courante = essai
        else:
            if courante:
                lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def _habillage(phrase, mots, humeur):
    """Niba, sa phrase et les mots du cahier : identiques aux films de science."""
    img = Image.new('RGBA', (LARGEUR, HAUTEUR), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pm = _police(34)
    x = LARGEUR - MARGE
    for mot in reversed(mots):
        l = d.textlength(mot, font=pm)
        d.rounded_rectangle([x - l - 34, MARGE, x, MARGE + 54], radius=27,
                            fill=(*WHITE_WARM, 240))
        d.text((x - l - 17, MARGE + 10), mot, font=pm, fill=(*INK, 255))
        x -= l + 34 + 10
    taille = 132
    img.alpha_composite(dessiner(humeur, taille), (MARGE, HAUTEUR - MARGE - taille))
    pp = _police(33)
    gauche = MARGE + taille + 16
    lignes = _coupe(phrase, pp, LARGEUR - MARGE - gauche - 48, d)
    h = 26 + 42 * len(lignes)
    haut = HAUTEUR - MARGE - h
    d.rounded_rectangle([gauche, haut, LARGEUR - MARGE, haut + h], radius=24,
                        fill=(*WHITE_WARM, 240))
    for i, ligne in enumerate(lignes):
        d.text((gauche + 24, haut + 13 + i * 42), ligne, font=pp, fill=(*INK, 255))
    return img


def rendre_plan(bloc, duree, sortie):
    """Un plan complet, du premier au dernier vingt-quatrième de seconde."""
    p = dict(bloc['scene'])
    if 'mots' in p and p['scene'] in ('phrase', 'remplace', 'rangement', 'bornes', 'blocs'):
        p['_espace'] = 26
        p['_pol'] = _police(_taille_qui_tient(p['mots'], p['_espace']))
    habillage = _habillage(bloc['vo_line'], bloc['keywords'], bloc['niba'])
    dessin = SCENES[p['scene']]

    images = int(round(duree * IPS))
    proc = subprocess.Popen(
        [FFMPEG, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
         '-s', '%dx%d' % (LARGEUR, HAUTEUR), '-r', str(IPS), '-i', '-',
         '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
         '-pix_fmt', 'yuv420p', sortie],
        stdin=subprocess.PIPE)
    for n in range(images):
        cadre = FOND.copy().convert('RGBA')
        d = ImageDraw.Draw(cadre)
        d._image = cadre
        dessin(d, p, n / IPS)
        cadre.alpha_composite(habillage)
        proc.stdin.write(cadre.convert('RGB').tobytes())
    proc.stdin.close()
    proc.wait()
    return sortie
