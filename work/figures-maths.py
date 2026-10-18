# -*- coding: utf-8 -*-
"""
Les figures des leçons de mathématiques de KLEIN (CE1).

Dix-sept images dessinées, aucune générée. La raison est dans
docs/charte-films.md : une leçon qui dit six faces, huit sommets et douze
arêtes doit être illustrée par un cube où l'enfant qui compte trouve six,
huit et douze. Un générateur ne garantit pas ce compte ; un dessin calculé,
oui. Et comme rien n'est généré, corriger une figure ne coûte rien.

Trois choix viennent de la direction donnée pour les mathématiques :

  les figures      le cube est une vraie projection, ses arêtes cachées sont
                   en pointillé, ses douze arêtes se comptent par groupes de
                   quatre — celles du haut, celles du bas, celles qui montent
  les objets       une centaine est un disque qu'on peut compter, pas un
                   chiffre abstrait ; deux cents, ce sont deux disques
  la police        Fredoka partout, la police de l'application, ronde et
                   large. Un chiffre a le même visage amical qu'un mot : à
                   sept ans, une typographie de manuel technique ajoute une
                   difficulté qui n'est pas celle qu'on enseigne

Usage :  python work/figures-maths.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fredoka.ttf')
SORTIE = os.path.join(RACINE, 'app', 'public', 'illustrations')

# Quatre fois la taille finale, puis réduction : les obliques du cube et les
# courbes des chiffres sortent lisses sans aucun lissage à la main.
S = 4

INK = (43, 64, 71)
INK_2 = (90, 112, 118)
WHITE_WARM = (255, 251, 244)
SAND = (246, 230, 201)
CLAY = (201, 112, 63)
GOLD = (231, 174, 74)
MINT = (189, 232, 214)
LILAC = (217, 206, 235)
SKY = (185, 212, 238)
BLEU = (109, 158, 203)


def _degrade(w, h):
    petit = Image.new('RGB', (2, h))
    d = ImageDraw.Draw(petit)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (1, y)], fill=(
            int(MINT[0] + (SAND[0] - MINT[0]) * t),
            int(MINT[1] + (SAND[1] - MINT[1]) * t),
            int(MINT[2] + (SAND[2] - MINT[2]) * t),
        ))
    return petit.resize((w, h), Image.BILINEAR)


class Toile:
    """Un dessin en coordonnées finales : la mise à l'échelle est interne."""

    def __init__(self, largeur, hauteur):
        self.w, self.h = largeur, hauteur
        self.im = _degrade(largeur * S, hauteur * S)
        self.d = ImageDraw.Draw(self.im, 'RGBA')

    def _p(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def pol(self, taille):
        return ImageFont.truetype(POLICE, int(taille * S))

    def rrect(self, x0, y0, x1, y1, r, fill=None, bord=None, trait=0):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S,
                                 fill=fill, outline=bord, width=max(1, int(trait * S)))

    def poly(self, pts, fill=None, bord=None, trait=0):
        self.d.polygon(self._p(pts), fill=fill, outline=bord,
                       width=max(1, int(trait * S)))

    def ligne(self, pts, couleur, trait):
        self.d.line(self._p(pts), fill=couleur, width=max(1, int(trait * S)),
                    joint='curve')

    def pointille(self, a, b, couleur, trait, pas=9):
        longueur = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(2, int(longueur / pas))
        for i in range(0, n, 2):
            t0, t1 = i / n, min(1.0, (i + 1) / n)
            self.ligne([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0),
                        (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                       couleur, trait)

    def disque(self, c, r, fill=None, bord=None, trait=0):
        self.d.ellipse([(c[0] - r) * S, (c[1] - r) * S, (c[0] + r) * S, (c[1] + r) * S],
                       fill=fill, outline=bord, width=max(1, int(trait * S)))

    def texte(self, xy, s, taille, couleur=INK, ancre='mm'):
        self.d.text((xy[0] * S, xy[1] * S), s, font=self.pol(taille),
                    fill=couleur, anchor=ancre)

    def ombre(self, cx, cy, rx, ry):
        self.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                       fill=(43, 64, 71, 28))

    def fini(self):
        return self.im.resize((self.w, self.h), Image.LANCZOS)


# --------------------------------------------------------------------------
# Le cube : une projection, pas un dessin d'intention

def _cube(cote, dx=None, dy=None):
    """Les huit sommets, puis les faces et les douze arêtes qui s'en déduisent.

    Rien n'est placé à la main : les comptes de la leçon sont des longueurs de
    listes, et une figure ne peut donc pas contredire sa propre notion.
    """
    dx = cote * 0.42 if dx is None else dx
    dy = cote * 0.42 if dy is None else dy
    f = {'ag': (0, 0), 'ad': (cote, 0), 'bd': (cote, cote), 'bg': (0, cote)}
    s = dict(f)
    s.update({'Ag': (dx, -dy), 'Ad': (cote + dx, -dy),
              'Bd': (cote + dx, cote - dy), 'Bg': (dx, cote - dy)})

    faces_vues = {
        'devant': ['ag', 'ad', 'bd', 'bg'],
        'dessus': ['ag', 'ad', 'Ad', 'Ag'],
        'droite': ['ad', 'bd', 'Bd', 'Ad'],
    }
    # Trois arêtes se cachent, et toutes les trois touchent le seul sommet
    # invisible : Bg, le coin arrière du bas à gauche.
    aretes = {
        'haut': [('ag', 'ad'), ('ad', 'Ad'), ('Ad', 'Ag'), ('Ag', 'ag')],
        'bas': [('bg', 'bd'), ('bd', 'Bd'), ('Bd', 'Bg'), ('Bg', 'bg')],
        'debout': [('ag', 'bg'), ('ad', 'bd'), ('Ad', 'Bd'), ('Ag', 'Bg')],
    }
    cachees = {('Bd', 'Bg'), ('Bg', 'bg'), ('Ag', 'Bg')}
    return s, faces_vues, aretes, cachees


def _poser_cube(t, cx, cy, cote, teintes=None, sommets=False,
                aretes_par_groupe=False, etiquettes=False):
    s, faces, aretes, cachees = _cube(cote)
    xs = [p[0] for p in s.values()]
    ys = [p[1] for p in s.values()]
    ox = cx - (min(xs) + max(xs)) / 2
    oy = cy - (min(ys) + max(ys)) / 2
    s = {k: (x + ox, y + oy) for k, (x, y) in s.items()}

    t.ombre(cx, oy + cote + cote * 0.10, cote * 0.52, cote * 0.09)

    tons = teintes or {'devant': WHITE_WARM, 'dessus': WHITE_WARM, 'droite': WHITE_WARM}
    for nom in ('dessus', 'droite', 'devant'):
        t.poly([s[k] for k in faces[nom]], fill=tons.get(nom, WHITE_WARM))

    groupes = {'haut': GOLD, 'bas': CLAY, 'debout': BLEU}
    for nom, paires in aretes.items():
        couleur = groupes[nom] if aretes_par_groupe else INK
        epais = 5 if aretes_par_groupe else 3
        for a, b in paires:
            if (a, b) in cachees or (b, a) in cachees:
                t.pointille(s[a], s[b], couleur if aretes_par_groupe else INK_2,
                            epais if aretes_par_groupe else 2)
            else:
                t.ligne([s[a], s[b]], couleur, epais)

    if sommets:
        r = max(5, cote * 0.055)
        for cle, p in s.items():
            vu = cle != 'Bg'
            t.disque(p, r, fill=CLAY if vu else None,
                     bord=WHITE_WARM if vu else CLAY, trait=2)

    if etiquettes:
        pol = cote * 0.11
        face = [s[k] for k in faces['devant']]
        mx = sum(p[0] for p in face) / 4
        my = sum(p[1] for p in face) / 4
        t.texte((mx - cote * 0.26, my - cote * 0.20), 'face', pol, INK_2)

        t.disque(s['ad'], max(5, cote * 0.05), fill=CLAY)
        t.ligne([s['ad'], (s['Ad'][0] + cote * 0.30, s['Ad'][1] - cote * 0.22)], INK_2, 2)
        t.texte((s['Ad'][0] + cote * 0.33, s['Ad'][1] - cote * 0.26), 'sommet', pol, INK_2, 'lm')

        mi = ((s['bg'][0] + s['bd'][0]) / 2, (s['bg'][1] + s['bd'][1]) / 2)
        t.ligne([mi, (mi[0] - cote * 0.34, mi[1] + cote * 0.28)], INK_2, 2)
        t.texte((mi[0] - cote * 0.36, mi[1] + cote * 0.31), 'arête', pol, INK_2, 'rm')
    return s


# --------------------------------------------------------------------------
# Les objets qu'on compte, et les tuiles de chiffres

def _tuile(t, cx, cy, w, h, texte, taille, fond=WHITE_WARM, encre=INK, barree=False):
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, min(w, h) * 0.22,
            fill=fond, bord=(255, 255, 255, 170), trait=2)
    t.texte((cx, cy), texte, taille, encre)
    if barree:
        t.ligne([(cx - w * 0.44, cy + h * 0.40), (cx + w * 0.44, cy - h * 0.40)], CLAY, 4)


def _centaine(t, cx, cy, cote):
    """Une centaine qui se compte vraiment : dix rangées de dix points.

    La première version portait dix points autour d’un disque marqué 100.
    L’enfant qui comptait trouvait dix, et l’image démentait son étiquette.
    Ici le compte est le bon : cent points, et le mot sous le paquet.
    """
    t.rrect(cx - cote / 2, cy - cote / 2, cx + cote / 2, cy + cote / 2,
            cote * 0.16, fill=MINT, bord=WHITE_WARM, trait=3)
    pas = cote * 0.082
    debut = cx - pas * 4.5
    haut = cy - pas * 4.5
    for i in range(10):
        for j in range(10):
            t.disque((debut + j * pas, haut + i * pas), cote * 0.019, fill=INK_2)
    t.texte((cx, cy + cote * 0.70), '100', cote * 0.26, INK)


def _tableau(t, cx, cy, largeur, colonnes, valeurs, legende=None, surligne=None):
    """Le tableau des sous-multiples : une colonne, un chiffre."""
    n = len(colonnes)
    cw = largeur / n
    hauteur_tete = cw * 0.52
    hauteur_case = cw * 0.80
    x0 = cx - largeur / 2
    y0 = cy - (hauteur_tete + hauteur_case) / 2

    for i, nom in enumerate(colonnes):
        chaud = surligne is not None and i in surligne
        t.rrect(x0 + i * cw + 2, y0, x0 + (i + 1) * cw - 2, y0 + hauteur_tete,
                cw * 0.14, fill=GOLD if chaud else LILAC)
        t.texte((x0 + i * cw + cw / 2, y0 + hauteur_tete / 2), nom,
                cw * 0.30, INK)

        t.rrect(x0 + i * cw + 2, y0 + hauteur_tete + 3,
                x0 + (i + 1) * cw - 2, y0 + hauteur_tete + hauteur_case,
                cw * 0.14, fill=WHITE_WARM, bord=(255, 255, 255, 170), trait=2)
        if i < len(valeurs) and valeurs[i] is not None:
            t.texte((x0 + i * cw + cw / 2,
                     y0 + hauteur_tete + 3 + hauteur_case / 2), str(valeurs[i]),
                    cw * 0.46, INK)

    if legende:
        t.texte((cx, y0 + hauteur_tete + hauteur_case + cw * 0.34), legende,
                cw * 0.30, CLAY)


# --------------------------------------------------------------------------
# Les dix-sept figures

def nb_nombres(t):  # couverture 960x540
    t.texte((480, 92), 'les nombres de 101 à 999', 44, INK_2)
    noms = ('centaines', 'dizaines', 'unités')
    for i, nom in enumerate(noms):
        cx = 300 + i * 180
        t.texte((cx, 196), nom, 28, INK_2)
        _tuile(t, cx, 310, 148, 160, '9', 110, (WHITE_WARM, SAND, MINT)[i])
    _tuile(t, 790, 310, 112, 160, '?', 88, LILAC, INK_2, barree=True)
    t.texte((480, 446), 'le plus grand nombre à trois chiffres', 30, CLAY)


def _mot_finale(t, cx, y, base, finale, taille):
    """Le mot entier, puis sa dernière lettre mise en valeur à sa suite.

    Jamais par-dessus : une pastille posée sur le mot cachait le t de cent,
    et la vignette apprenait « deux cens » à qui ne lisait que l’image.
    """
    pol = t.pol(taille)
    large_base = t.d.textlength(base, font=pol) / S
    large_fin = t.d.textlength(finale, font=pol) / S
    pastille = large_fin + taille * 0.46
    x0 = cx - (large_base + pastille) / 2
    t.texte((x0, y), base, taille, INK, 'lm')
    cxp = x0 + large_base + pastille / 2
    t.rrect(cxp - pastille / 2, y - taille * 0.62, cxp + pastille / 2, y + taille * 0.62,
            taille * 0.26, fill=GOLD)
    t.texte((cxp, y), finale, taille, WHITE_WARM)


def nb_regle(t):
    _mot_finale(t, 160, 106, 'cent', 's', 64)
    t.texte((160, 196), 'multiplié', 30, INK_2)
    t.rrect(74, 228, 246, 286, 18, fill=WHITE_WARM, bord=CLAY, trait=3)
    t.texte((160, 257), 'rien après', 28, CLAY)


def nb_cent(t):
    _centaine(t, 160, 110, 132)
    t.texte((160, 248), 'cent', 54, INK)
    t.rrect(70, 280, 250, 310, 14, fill=WHITE_WARM, bord=INK_2, trait=2)
    t.texte((160, 295), 'une seule', 22, INK_2)


def nb_deux_cents(t):
    _centaine(t, 92, 92, 104)
    _centaine(t, 228, 92, 104)
    _mot_finale(t, 160, 226, 'deux cent', 's', 40)
    t.texte((160, 292), '200', 42, CLAY)


def nb_340(t):
    _tuile(t, 160, 78, 180, 86, '340', 62, WHITE_WARM)
    t.texte((160, 170), 'trois cent', 40, INK)
    t.texte((160, 222), 'quarante', 40, CLAY)
    t.ligne([(228, 190), (228, 206)], CLAY, 4)
    t.ligne([(222, 200), (228, 208), (234, 200)], CLAY, 4)
    t.rrect(76, 262, 244, 298, 14, fill=WHITE_WARM, bord=CLAY, trait=2)
    t.texte((160, 280), 'pas de s', 26, CLAY)


def nb_999(t):
    for i in range(3):
        _tuile(t, 78 + i * 62, 128, 54, 84, '9', 50, (WHITE_WARM, SAND, MINT)[i])
    _tuile(t, 262, 128, 44, 84, '?', 40, LILAC, INK_2, barree=True)
    t.texte((160, 232), '999', 56, INK)
    t.texte((160, 288), 'le plus grand', 26, CLAY)


def cu_cube(t):  # couverture 960x540
    t.texte((480, 78), 'le cube', 48, INK_2)
    _poser_cube(t, 470, 290, 230, teintes={'dessus': MINT, 'droite': SKY,
                                           'devant': WHITE_WARM}, etiquettes=True)
    for i, (n, mot, couleur) in enumerate((('6', 'faces', GOLD), ('8', 'sommets', CLAY),
                                           ('12', 'arêtes', BLEU))):
        y = 170 + i * 92
        t.disque((836, y), 30, fill=couleur)
        t.texte((836, y), n, 30, WHITE_WARM)
        t.texte((836, y + 50), mot, 24, INK_2)


def cu_solide(t):
    _poser_cube(t, 160, 150, 150, teintes={'dessus': MINT, 'droite': SKY,
                                           'devant': WHITE_WARM})
    t.texte((160, 278), 'un solide', 34, CLAY)


def cu_faces(t):
    _poser_cube(t, 150, 148, 148, teintes={'dessus': MINT, 'droite': SKY,
                                           'devant': LILAC})
    t.disque((266, 62), 30, fill=GOLD)
    t.texte((266, 62), '6', 34, WHITE_WARM)
    t.texte((160, 282), 'faces carrées', 30, INK_2)


def cu_sommets(t):
    _poser_cube(t, 152, 146, 142, sommets=True)
    t.disque((266, 62), 30, fill=CLAY)
    t.texte((266, 62), '8', 34, WHITE_WARM)
    t.texte((160, 282), 'sommets', 30, INK_2)


def cu_aretes(t):
    _poser_cube(t, 150, 124, 130, aretes_par_groupe=True)
    for i, (couleur, mot) in enumerate(((GOLD, '4 en haut'), (CLAY, '4 en bas'),
                                        (BLEU, '4 debout'))):
        y = 244 + i * 28
        t.disque((60, y), 9, fill=couleur)
        t.texte((78, y), mot, 21, INK_2, 'lm')
    t.disque((268, 56), 30, fill=BLEU)
    t.texte((268, 56), '12', 28, WHITE_WARM)


def me_mesures(t):  # couverture 960x540
    t.texte((480, 86), 'les sous-multiples du mètre', 42, INK_2)
    _tableau(t, 480, 250, 520, ('m', 'dm', 'cm', 'mm'), [2, 0, 0, None],
             legende='2 m = 200 cm', surligne={2})
    # La règle descend sous la légende du tableau : à 392 elle lui passait au
    # travers, et « 2 m = 200 cm » devenait illisible.
    t.rrect(240, 420, 720, 462, 14, fill=WHITE_WARM, bord=(255, 255, 255, 170), trait=2)
    for i in range(25):
        x = 252 + i * 19
        haut = 432 if i % 5 else 424
        t.ligne([(x, haut), (x, 456)], INK_2 if i % 5 else CLAY, 2)
    t.texte((480, 500), 'une colonne, un chiffre', 28, INK_2)


def me_tableau(t):
    _tableau(t, 160, 150, 280, ('m', 'dm', 'cm', 'mm'), [None, None, None, None])
    t.texte((160, 262), 'je convertis', 30, CLAY)


def me_sous_multiples(t):
    for i, (nom, part) in enumerate((('m', 1.0), ('dm', 0.62), ('cm', 0.38), ('mm', 0.20))):
        y = 92 + i * 56
        largeur = 190 * part
        t.rrect(70, y - 16, 70 + largeur, y + 16, 12,
                fill=(MINT, SKY, LILAC, SAND)[i], bord=(255, 255, 255, 170), trait=2)
        t.texte((276, y), nom, 28, INK_2, 'rm')
    t.texte((160, 292), 'du plus grand au plus petit', 20, CLAY)


def me_2m(t):
    _tableau(t, 160, 140, 280, ('m', 'dm', 'cm', 'mm'), [2, 0, 0, None],
             legende='2 m = 200 cm', surligne={2})


def me_120(t):
    _tableau(t, 160, 140, 280, ('m', 'dm', 'cm', 'mm'), [1, 2, 0, None],
             legende='120 cm = 1 m 2 dm', surligne={2})


def me_304(t):
    _tableau(t, 160, 140, 280, ('m', 'dm', 'cm', 'mm'), [None, 3, 0, 4],
             legende='3 dm 4 mm = 304 mm', surligne={3})


FIGURES = [
    ('nb-nombres', 960, 540, nb_nombres),
    ('nb-regle', 320, 320, nb_regle),
    ('nb-cent', 320, 320, nb_cent),
    ('nb-deux-cents', 320, 320, nb_deux_cents),
    ('nb-340', 320, 320, nb_340),
    ('nb-999', 320, 320, nb_999),
    ('cu-cube', 960, 540, cu_cube),
    ('cu-solide', 320, 320, cu_solide),
    ('cu-faces', 320, 320, cu_faces),
    ('cu-sommets', 320, 320, cu_sommets),
    ('cu-aretes', 320, 320, cu_aretes),
    ('me-mesures', 960, 540, me_mesures),
    ('me-tableau', 320, 320, me_tableau),
    ('me-sous-multiples', 320, 320, me_sous_multiples),
    ('me-2m', 320, 320, me_2m),
    ('me-120', 320, 320, me_120),
    ('me-304', 320, 320, me_304),
]


def controler():
    """Le compte de la leçon est le compte de la figure, ou rien n'est dessiné."""
    s, faces, aretes, cachees = _cube(100)
    assert len(s) == 8, 'le cube doit avoir huit sommets : %d' % len(s)
    toutes = [p for groupe in aretes.values() for p in groupe]
    assert len(toutes) == 12, 'le cube doit avoir douze arêtes : %d' % len(toutes)
    assert len({frozenset(p) for p in toutes}) == 12, 'une arête est dessinée deux fois'
    assert len(cachees) == 3, 'trois arêtes seulement sont cachées'
    assert all(len(f) == 4 for f in faces.values()), 'une face du cube a quatre côtés'
    assert len(faces) == 3, 'trois faces sont visibles, les trois autres sont derrière'
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'


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
