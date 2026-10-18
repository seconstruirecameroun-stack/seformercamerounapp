# -*- coding: utf-8 -*-
"""
Le mouvement des nombres et des figures, pour les films de mathématiques.

Le registre est décrit dans docs/charte-films.md : les mathématiques ne sont
ni le monde ni la langue. Il y a quelque chose à montrer — une figure, une
quantité, une colonne — à condition de le dessiner juste.

Ce module se greffe sur work/motion-texte.py plutôt que de le recopier : le
fond, Niba, la bande de phrase, les pastilles du cahier et la boucle de rendu
sont les mêmes qu'en français. Seules les scènes changent.

  conditions  le mot cent, puis les deux conditions qui lui donnent son s
  cent        des paquets de cent qu’on compte, et le mot qui leur répond
  chiffres    des tuiles de chiffres, et celle qui ne peut pas exister
  cube        le solide, ses sommets qui s’allument, ses arêtes par groupes
  patron      le cube qui s’ouvre en six carrés
  tableau     les colonnes, les chiffres qui tombent, la lecture qui suit
  echelle     les quatre unités, de la plus grande à la plus petite

La figure est dessinée sur un calque deux fois trop grand, puis réduite : une
arête oblique tracée directement dans le cadre sortirait en escalier, et une
leçon de géométrie ne peut pas se permettre une figure crénelée.

Les comptes ne sont jamais écrits à la main. Les huit sommets et les douze
arêtes viennent de work/figures-maths.py, qui les déduit du cube lui-même et
refuse de dessiner si le compte n’est pas bon.

Usage comme bibliothèque :  from motion_maths import rendre_plan
"""

import importlib.util
import os
import sys

from PIL import Image, ImageDraw, ImageFont

_ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ICI)


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


motion = _charger('motion_texte', 'motion-texte.py')
figures = _charger('figures_maths', 'figures-maths.py')

LARGEUR, HAUTEUR = motion.LARGEUR, motion.HAUTEUR
POLICE = motion.POLICE
_doux = motion._doux

INK = motion.INK
INK_2 = motion.INK_2
WHITE_WARM = motion.WHITE_WARM
CLAY = motion.CLAY
GOLD = motion.GOLD
MINT = motion.MINT
LILAC = motion.LILAC
SKY = motion.SKY
BLEU = figures.BLEU

# La bande où vivent les figures : au-dessus de Niba et de sa phrase.
BANDE_HAUT, BANDE_BAS = 96, 512
K = 2  # le calque est deux fois trop grand, puis réduit


class Plan:
    """Un calque de figure, en coordonnées du cadre, rendu sans crénelage."""

    def __init__(self):
        self.h = BANDE_BAS - BANDE_HAUT
        self.im = Image.new('RGBA', (LARGEUR * K, self.h * K), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * K, (y - BANDE_HAUT) * K) for x, y in pts]

    def pol(self, taille):
        return ImageFont.truetype(POLICE, max(1, int(taille * K)))

    def large(self, texte, taille):
        return self.d.textlength(texte, font=self.pol(taille)) / K

    def texte(self, xy, s, taille, couleur=INK, alpha=255, ancre='mm'):
        self.d.text((xy[0] * K, (xy[1] - BANDE_HAUT) * K), s, font=self.pol(taille),
                    fill=(*couleur, int(alpha)), anchor=ancre)

    def rrect(self, x0, y0, x1, y1, r, fill=None, bord=None, trait=0, alpha=255):
        self.d.rounded_rectangle(
            [x0 * K, (y0 - BANDE_HAUT) * K, x1 * K, (y1 - BANDE_HAUT) * K],
            radius=r * K,
            fill=(*fill, int(alpha)) if fill else None,
            outline=(*bord, int(alpha)) if bord else None,
            width=max(1, int(trait * K)))

    def poly(self, pts, fill=None, alpha=255):
        self.d.polygon(self._p(pts), fill=(*fill, int(alpha)) if fill else None)

    def ligne(self, pts, couleur, trait, alpha=255):
        self.d.line(self._p(pts), fill=(*couleur, int(alpha)),
                    width=max(1, int(trait * K)), joint='curve')

    def pointille(self, a, b, couleur, trait, alpha=255, pas=11):
        n = max(2, int(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 / pas))
        for i in range(0, n, 2):
            t0, t1 = i / n, min(1.0, (i + 1) / n)
            self.ligne([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                        (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                       couleur, trait, alpha)

    def disque(self, c, r, fill=None, bord=None, trait=0, alpha=255):
        self.d.ellipse([(c[0] - r) * K, (c[1] - r - BANDE_HAUT) * K,
                        (c[0] + r) * K, (c[1] + r - BANDE_HAUT) * K],
                       fill=(*fill, int(alpha)) if fill else None,
                       outline=(*bord, int(alpha)) if bord else None,
                       width=max(1, int(trait * K)))

    def poser(self, d):
        d._image.alpha_composite(
            self.im.resize((LARGEUR, self.h), Image.LANCZOS), (0, BANDE_HAUT))


def _compteur(p, n, couleur, alpha=255):
    """Le compte en cours, en haut à droite de la figure."""
    if n <= 0:
        return
    p.disque((1148, 176), 44, fill=couleur, alpha=alpha)
    p.texte((1148, 176), str(n), 44, WHITE_WARM, alpha)


def _paquet_cent(p, cx, cy, cote, alpha=255):
    """Cent points en dix rangées : une centaine qui se compte vraiment."""
    p.rrect(cx - cote / 2, cy - cote / 2, cx + cote / 2, cy + cote / 2,
            cote * 0.16, fill=MINT, bord=WHITE_WARM, trait=3, alpha=alpha)
    pas = cote * 0.082
    for i in range(10):
        for j in range(10):
            p.disque((cx - pas * 4.5 + j * pas, cy - pas * 4.5 + i * pas),
                     cote * 0.019, fill=INK_2, alpha=alpha)


# ───────────────────────────── les sept scènes ─────────────────────────────

def _scene_conditions(p, par, t):
    """Le mot cent, puis les deux conditions, et le s seulement après."""
    base, taille = 'cent', 104
    a = _doux(t / 0.45)
    if a <= 0:
        return
    s_la = _doux((t - 2.4) / 0.5)
    lb = p.large(base, taille)
    ls = p.large('s', taille)
    pastille = (ls + taille * 0.5) * s_la
    x0 = 640 - (lb + pastille) / 2
    p.texte((x0, 230), base, taille, INK, 255 * a, 'lm')
    if s_la > 0:
        cx = x0 + lb + pastille / 2
        p.rrect(cx - pastille / 2, 230 - taille * 0.60, cx + pastille / 2,
                230 + taille * 0.60, taille * 0.26, fill=GOLD, alpha=255 * s_la)
        p.texte((cx, 230), 's', taille, WHITE_WARM, 255 * s_la)

    for i, (mot, couleur) in enumerate((('multiplié', SKY), ('rien après', LILAC))):
        v = _doux((t - (1.1 + i * 0.7)) / 0.5)
        if v <= 0:
            continue
        cx = 640 + (i * 2 - 1) * 190
        y = 400 + (1 - v) * 44
        demi = p.large(mot, 44) / 2 + 36
        p.rrect(cx - demi, y - 40, cx + demi, y + 40, 28, fill=couleur, alpha=255 * v)
        p.texte((cx, y), mot, 44, INK, 255 * v)


def _scene_cent(p, par, t):
    """Des paquets de cent, puis le mot qui leur correspond."""
    n = par['paquets']
    # Un paquet doit rester comptable : à cent cinquante pixels ses cent points
    # se referment en une trame grise, et le dessin redevient un symbole.
    cote = {1: 196, 2: 172, 3: 152}[n]
    ecart = cote + 30
    for i in range(n):
        a = _doux((t - (0.15 + i * 0.35)) / 0.4)
        if a <= 0:
            continue
        _paquet_cent(p, 640 + (i - (n - 1) / 2) * ecart, 232, cote, 255 * a)

    debut = 0.15 + n * 0.35 + 0.35
    a = _doux((t - debut) / 0.45)
    if a <= 0:
        return
    mot, taille = par['mot'], 82
    finale = par.get('finale')
    suivant = par.get('suivant')

    # Le s arrive après le mot ; si un nombre le suit, il repart. C’est la
    # règle entière en un seul geste, et dans le bon ordre.
    v_s = _doux((t - (debut + 0.9)) / 0.45) if finale else 0.0
    v_sv = _doux((t - (debut + 1.7)) / 0.5) if suivant else 0.0
    if suivant:
        v_s *= (1 - v_sv)

    lm = p.large(mot, taille)
    pastille = (p.large(finale, taille) + taille * 0.5) * v_s if finale else 0.0
    lsv = (p.large(' ' + suivant, taille)) * v_sv if suivant else 0.0
    x0 = 640 - (lm + pastille + lsv) / 2
    p.texte((x0, 420), mot, taille, INK, 255 * a, 'lm')
    if v_s > 0.01:
        cx = x0 + lm + pastille / 2
        p.rrect(cx - pastille / 2, 420 - taille * 0.60, cx + pastille / 2,
                420 + taille * 0.60, taille * 0.26, fill=GOLD, alpha=255 * v_s)
        p.texte((cx, 420 - (1 - v_s) * 60), finale, taille, WHITE_WARM, 255 * v_s)
    if v_sv > 0:
        p.texte((x0 + lm + pastille, 420), ' ' + suivant, taille, CLAY,
                255 * v_sv, 'lm')


def _scene_chiffres(p, par, t):
    """Des tuiles de chiffres, et celle qui ne peut pas exister."""
    tuiles = par['tuiles']
    larg, haut, ecart = 124, 176, 20
    total = len(tuiles) * larg + (len(tuiles) - 1) * ecart
    if par.get('barree'):
        total += larg * 0.86 + ecart + 24
    x = 640 - total / 2
    tons = (WHITE_WARM, motion.SAND, MINT)
    for i, ch in enumerate(tuiles):
        a = _doux((t - (0.2 + i * 0.34)) / 0.4)
        cx = x + larg / 2 + i * (larg + ecart)
        if a <= 0:
            continue
        p.rrect(cx - larg / 2, 232 - haut / 2, cx + larg / 2, 232 + haut / 2,
                larg * 0.22, fill=tons[i % 3], alpha=255 * a)
        p.texte((cx, 232), ch, 118, INK, 255 * a)
    if par.get('barree'):
        v = _doux((t - (0.2 + len(tuiles) * 0.34 + 0.5)) / 0.5)
        if v > 0:
            cx = x + len(tuiles) * (larg + ecart) + 24 + larg * 0.43
            p.rrect(cx - larg * 0.43, 232 - haut / 2, cx + larg * 0.43,
                    232 + haut / 2, larg * 0.22, fill=LILAC, alpha=255 * v)
            p.texte((cx, 232), '?', 98, INK_2, 255 * v)
            barre = _doux((t - (0.2 + len(tuiles) * 0.34 + 1.0)) / 0.4)
            if barre > 0:
                x0, y0 = cx - larg * 0.38, 232 + haut * 0.42
                x1, y1 = cx + larg * 0.38, 232 - haut * 0.42
                p.ligne([(x0, y0), (x0 + (x1 - x0) * barre, y0 + (y1 - y0) * barre)],
                        CLAY, 7)
    mot = par.get('mot')
    if mot:
        a = _doux((t - 1.9) / 0.5)
        if a > 0:
            p.texte((640, 416), mot, 60, CLAY, 255 * a)


def _geometrie_cube(cx, cy, cote):
    s, faces, aretes, cachees = figures._cube(cote)
    xs = [q[0] for q in s.values()]
    ys = [q[1] for q in s.values()]
    ox = cx - (min(xs) + max(xs)) / 2
    oy = cy - (min(ys) + max(ys)) / 2
    return ({k: (x + ox, y + oy) for k, (x, y) in s.items()},
            faces, aretes, cachees)


def _dessiner_cube(p, s, faces, aretes, cachees, alpha=255, teintes=True,
                   arretes_visibles=True):
    tons = ({'dessus': MINT, 'droite': SKY, 'devant': WHITE_WARM} if teintes
            else {'dessus': WHITE_WARM, 'droite': WHITE_WARM, 'devant': WHITE_WARM})
    for nom in ('dessus', 'droite', 'devant'):
        p.poly([s[k] for k in faces[nom]], fill=tons[nom], alpha=alpha)
    if not arretes_visibles:
        return
    for paires in aretes.values():
        for a, b in paires:
            if (a, b) in cachees or (b, a) in cachees:
                p.pointille(s[a], s[b], INK_2, 2, alpha)
            else:
                p.ligne([s[a], s[b]], INK, 3, alpha)


def _scene_cube(p, par, t):
    """Le solide, puis ce qu on y compte, un élément à la fois."""
    # La projection est plus haute que le côté : 246 débordait du haut de la
    # bande et rognait les arêtes du fond, celles-là mêmes qu’on fait compter.
    cote = 214
    monte = _doux(t / 0.6)
    if monte <= 0:
        return
    cy = 264 + (1 - monte) * 34
    s, faces, aretes, cachees = _geometrie_cube(620, cy, cote)
    compter = par.get('compter')

    # L’ombre ne sert qu’au plan du solide, où elle dit le volume. Sous un cube
    # dont on compte les sommets, elle n’est plus qu’une tache qui distrait.
    if compter is None:
        p.disque((620, cy + cote * 0.62), cote * 0.38, fill=(43, 64, 71),
                 alpha=16 * monte)
    _dessiner_cube(p, s, faces, aretes, cachees, 255 * monte,
                   teintes=(compter is None))

    if compter == 'sommets':
        ordre = ['ag', 'ad', 'Ad', 'Ag', 'bg', 'bd', 'Bd', 'Bg']
        vus = 0
        for i, cle in enumerate(ordre):
            v = _doux((t - (0.9 + i * 0.26)) / 0.3)
            if v <= 0:
                continue
            vus = i + 1
            r = cote * 0.055 * (1 + 0.6 * (1 - v))
            if cle == 'Bg':
                p.disque(s[cle], r, bord=CLAY, trait=3, alpha=255 * v)
            else:
                p.disque(s[cle], r, fill=CLAY, bord=WHITE_WARM, trait=2, alpha=255 * v)
        _compteur(p, vus, CLAY)

    elif compter == 'aretes':
        groupes = (('haut', GOLD), ('bas', CLAY), ('debout', BLEU))
        n, vues = 0, 0
        for nom, couleur in groupes:
            for a, b in aretes[nom]:
                v = _doux((t - (0.9 + n * 0.20)) / 0.26)
                n += 1
                if v <= 0:
                    continue
                vues = n
                pa, pb = s[a], s[b]
                pm = (pa[0] + (pb[0] - pa[0]) * v, pa[1] + (pb[1] - pa[1]) * v)
                if (a, b) in cachees or (b, a) in cachees:
                    p.pointille(pa, pm, couleur, 5)
                else:
                    p.ligne([pa, pm], couleur, 6)
        _compteur(p, vues, BLEU)
        for i, (couleur, mot) in enumerate(((GOLD, '4 en haut'), (CLAY, '4 en bas'),
                                            (BLEU, '4 debout'))):
            v = _doux((t - (1.5 + i * 0.85)) / 0.4)
            if v <= 0:
                continue
            y = 390 + i * 40
            p.disque((248, y), 12, fill=couleur, alpha=255 * v)
            p.texte((274, y), mot, 34, INK_2, 255 * v, 'lm')

    else:
        a = _doux((t - 1.6) / 0.5)
        if a > 0:
            # Sous l’ombre, jamais dessus : posé à 466 le mot tombait sur
            # l’arête du bas et se lisait au travers de la figure.
            p.texte((620, 492), 'un solide', 52, CLAY, 255 * a)


def _scene_patron(p, par, t):
    """Le cube qui s ouvre : six carrés, comptés un à un."""
    cote = 206
    ferme = 1 - _doux((t - 0.9) / 0.6)
    if ferme > 0.01:
        s, faces, aretes, cachees = _geometrie_cube(640, 268, cote * ferme)
        _dessiner_cube(p, s, faces, aretes, cachees, 255 * ferme)

    c = 118
    # Un patron en croix : la forme même que l’enfant découpe en classe.
    cases = [(0, -1), (-1, 0), (0, 0), (1, 0), (2, 0), (0, 1)]
    ox, oy = 640 - c * 0.5, 272
    vus = 0
    for i, (gx, gy) in enumerate(cases):
        v = _doux((t - (1.5 + i * 0.30)) / 0.34)
        if v <= 0:
            continue
        vus = i + 1
        x = ox + gx * c
        y = oy + gy * c
        p.rrect(x - c / 2 + 3, y - c / 2 + 3, x + c / 2 - 3, y + c / 2 - 3, 12,
                fill=(MINT, SKY, WHITE_WARM, LILAC, motion.SAND, MINT)[i],
                bord=WHITE_WARM, trait=3, alpha=255 * v)
        p.texte((x, y), str(i + 1), 48, INK_2, 200 * v)
    _compteur(p, vus, GOLD)
    a = _doux((t - 3.4) / 0.5)
    if a > 0:
        p.texte((640, 492), 'six carrés', 46, CLAY, 255 * a)


def _scene_tableau(p, par, t):
    """Les colonnes, puis les chiffres qui tombent dans la bonne case."""
    colonnes = ('m', 'dm', 'cm', 'mm')
    larg, cw = 620, 155
    x0 = 640 - larg / 2
    y_tete, h_tete = 196, 78
    y_case, h_case = 282, 116
    cible = par.get('cible')
    chiffres = par.get('chiffres') or [None] * 4

    for i, nom in enumerate(colonnes):
        v = _doux((t - (0.1 + i * 0.18)) / 0.35)
        if v <= 0:
            continue
        chaud = cible == i and _doux((t - 2.9) / 0.5) > 0.5
        p.rrect(x0 + i * cw + 4, y_tete - (1 - v) * 40, x0 + (i + 1) * cw - 4,
                y_tete + h_tete - (1 - v) * 40, 18,
                fill=GOLD if chaud else LILAC, alpha=255 * v)
        p.texte((x0 + i * cw + cw / 2, y_tete + h_tete / 2 - (1 - v) * 40), nom,
                44, INK, 255 * v)
        p.rrect(x0 + i * cw + 4, y_case, x0 + (i + 1) * cw - 4, y_case + h_case,
                18, fill=WHITE_WARM, bord=(255, 255, 255), trait=3, alpha=255 * v)

    poses = 0
    for i, ch in enumerate(chiffres):
        if ch is None:
            continue
        v = _doux((t - (1.2 + poses * 0.42)) / 0.4)
        poses += 1
        if v <= 0:
            continue
        cy = y_case + h_case / 2 - (1 - v) * 120
        p.texte((x0 + i * cw + cw / 2, cy), str(ch), 76, INK, 255 * v)

    legende = par.get('legende')
    if legende:
        a = _doux((t - 3.3) / 0.5)
        if a > 0:
            p.texte((640, 470), legende, 48, CLAY, 255 * a)


def _scene_echelle(p, par, t):
    """Les quatre unités, de la plus grande à la plus petite."""
    unites = (('m', 1.0, MINT), ('dm', 0.62, SKY), ('cm', 0.38, LILAC),
              ('mm', 0.20, motion.SAND))
    for i, (nom, part, couleur) in enumerate(unites):
        v = _doux((t - (0.25 + i * 0.5)) / 0.45)
        if v <= 0:
            continue
        y = 190 + i * 78
        large = 600 * part * v
        p.rrect(360, y - 26, 360 + large, y + 26, 20, fill=couleur,
                bord=(255, 255, 255), trait=3, alpha=255)
        p.texte((340, y), nom, 44, INK_2, 255 * v, 'rm')
    a = _doux((t - 2.8) / 0.5)
    if a > 0:
        p.texte((640, 490), 'dix fois plus petit à chaque colonne', 36, CLAY, 255 * a)


SCENES = {
    'conditions': _scene_conditions, 'cent': _scene_cent, 'chiffres': _scene_chiffres,
    'cube': _scene_cube, 'patron': _scene_patron, 'tableau': _scene_tableau,
    'echelle': _scene_echelle,
}


def _adapter(fn):
    """Chaque scène dessine sur son calque, qui est ensuite réduit et posé."""
    def dessin(d, par, t):
        p = Plan()
        fn(p, par, t)
        p.poser(d)
    return dessin


motion.SCENES.update({nom: _adapter(fn) for nom, fn in SCENES.items()})

rendre_plan = motion.rendre_plan
