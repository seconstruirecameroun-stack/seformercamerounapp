# -*- coding: utf-8 -*-
"""
Le mouvement des figures de sciences, pour les films de BRAYNE (CM1).

Troisième greffe sur work/motion-texte.py, après le français et les
mathématiques : le fond, Niba, la bande de phrase, les pastilles du cahier et
la boucle de rendu sont les mêmes partout. Seules les scènes changent.

Ce module ne redessine rien. Les figures des leçons existent déjà dans
work/figures-sciences.py — la lampe et ses cinq parties, les verres, les
ondes de la voix, les cellules — et elles sont ici mises en mouvement telles
quelles, à travers une surface qui leur donne une opacité et un décalage.
Deux dessins de la même lampe finiraient par diverger, et le numéro 3
cesserait un jour de montrer la mèche.

Douze scènes couvrent les six films :

  fleche      une carte se change en une autre
  barres      deux intervalles d age qui se remplissent
  etiquettes  les mots d une liste qui arrivent un par un
  cellules    l ovule et le spermatozoïde, et sa queue qui bat
  ensemble    des organes épars que le cadre rassemble
  paires      un élément à gauche, un trait, son rôle à droite
  boucle      un trajet qui revient à son point de départ
  cycle       le paysage, et ses quatre étapes qui s allument
  verres      l eau claire et l eau trouble, la coche et la croix
  origines    le végétal et l animal qui deviennent du compost
  sols        un sol pauvre que le compost enrichit
  lampe       la lampe qui s allume, puis ses parties numérotées

Le film du cycle de l eau est bâti sur une seule scène jouée quatre fois,
chaque plan allumant une étape de plus. L enfant voit donc le paysage se
compléter sous ses yeux au lieu de changer d image à chaque phrase.

Usage comme bibliothèque :  from motion_sciences import rendre_plan
"""

import importlib.util
import math
import os
import sys

_ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ICI)


def _charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(_ICI, fichier))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mm = _charger('motion_maths', 'motion-maths.py')
fs = _charger('figures_sciences', 'figures-sciences.py')

motion = mm.motion
Plan = mm.Plan
_doux = mm._doux
BANDE_HAUT, BANDE_BAS = mm.BANDE_HAUT, mm.BANDE_BAS
HAUT_BANDE = BANDE_BAS - BANDE_HAUT

INK, INK_2 = mm.INK, mm.INK_2
WHITE_WARM, SAND, CLAY = mm.WHITE_WARM, motion.SAND, mm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = mm.GOLD, mm.MINT, mm.LILAC, mm.SKY, mm.BLEU
TONS = fs.TONS

# Les scripts nomment les couleurs plutôt que de les coder : un manifeste se
# relit, et « SKY » y dit quelque chose là où « [185, 212, 238] » ne dit rien.
COULEURS = {'SKY': SKY, 'LILAC': LILAC, 'MINT': MINT, 'SAND': SAND,
            'GOLD': GOLD, 'CLAY': CLAY, 'BLEU': BLEU, 'INK': INK}


def _ton(nom, defaut=SKY):
    if isinstance(nom, (list, tuple)):
        return tuple(nom)
    return COULEURS.get(nom, defaut)


class Surface:
    """Les figures de work/figures-sciences.py, posées sur un plan animé.

    Elles sont écrites pour une toile fixe : coordonnées en haut à gauche,
    pas d opacité. Cette surface leur donne les deux — un décalage, une
    échelle, et une opacité courante — sans qu une seule ligne de dessin soit
    recopiée ici.
    """

    def __init__(self, plan, ox=0.0, oy=0.0, echelle=1.0):
        self.p = plan
        self.ox, self.oy, self.e = ox, oy, echelle
        self.a = 255

    def _x(self, x):
        return self.ox + x * self.e

    def _y(self, y):
        return BANDE_HAUT + self.oy + y * self.e

    def _pts(self, pts):
        return [(self._x(x), self._y(y)) for x, y in pts]

    def opacite(self, v):
        self.a = max(0, min(255, int(255 * v)))
        return self.a > 0

    def pol(self, taille):
        return self.p.pol(taille * self.e)

    def rrect(self, x0, y0, x1, y1, r, fill=None, bord=None, trait=0):
        self.p.rrect(self._x(x0), self._y(y0), self._x(x1), self._y(y1), r * self.e,
                     fill=fill, bord=bord, trait=trait * self.e, alpha=self.a)

    def poly(self, pts, fill=None, bord=None, trait=0):
        self.p.poly(self._pts(pts), fill=fill, alpha=self.a)

    def ligne(self, pts, couleur, trait):
        self.p.ligne(self._pts(pts), couleur, trait * self.e, alpha=self.a)

    def disque(self, c, r, fill=None, bord=None, trait=0):
        self.p.disque((self._x(c[0]), self._y(c[1])), r * self.e,
                      fill=fill, bord=bord, trait=trait * self.e, alpha=self.a)

    def texte(self, xy, s, taille, couleur=INK, ancre='mm'):
        self.p.texte((self._x(xy[0]), self._y(xy[1])), s, taille * self.e,
                     couleur, self.a, ancre)


def _surface(p, largeur, hauteur):
    """Une surface qui centre une figure de `largeur` x `hauteur` dans la bande."""
    e = min(1280.0 / largeur, HAUT_BANDE / hauteur)
    return Surface(p, ox=(1280 - largeur * e) / 2, oy=(HAUT_BANDE - hauteur * e) / 2,
                   echelle=e)


def _compteur(p, n, couleur):
    mm._compteur(p, n, couleur)


# ───────────────────────────── les douze scènes ───────────────────────────

def _scene_fleche(p, par, t):
    s = _surface(p, 560, 400)
    a1 = _doux(t / 0.5)
    if s.opacite(a1):
        s.rrect(130, 40 + (1 - a1) * 30, 430, 110 + (1 - a1) * 30, 24, fill=MINT,
                bord=(255, 255, 255), trait=3)
        s.texte((280, 75 + (1 - a1) * 30), par['avant'], 46, INK)
    v = _doux((t - 1.0) / 0.55)
    if v > 0 and s.opacite(v):
        fs._fleche(s, (280, 130), (280, 130 + 110 * v), CLAY, 6, 18)
    a2 = _doux((t - 1.8) / 0.55)
    if a2 > 0 and s.opacite(a2):
        s.rrect(130, 280 + (1 - a2) * 26, 430, 350 + (1 - a2) * 26, 24, fill=LILAC,
                bord=(255, 255, 255), trait=3)
        s.texte((280, 315 + (1 - a2) * 26), par['apres'], 46, INK)


def _scene_barres(p, par, t):
    s = _surface(p, 720, 360)
    bas, haut = par.get('min', 10), par.get('max', 16)
    for i, (nom, a, b, couleur) in enumerate(par['lignes']):
        ton = _ton(couleur)
        v = _doux((t - (0.3 + i * 1.0)) / 0.8)
        if not s.opacite(min(1.0, 0.25 + v * 4)):
            continue
        y = 80 + i * 130
        s.texte((60, y - 48), nom, 34, INK_2, 'lm')
        s.rrect(56, y - 26, 664, y + 26, 26, fill=WHITE_WARM, bord=(255, 255, 255), trait=3)
        if v <= 0:
            continue
        s.opacite(1.0)
        x0 = 56 + (a - bas) / (haut - bas) * 608
        x1 = 56 + (b - bas) / (haut - bas) * 608
        s.rrect(x0, y - 26, x0 + (x1 - x0) * v, y + 26, 26, fill=ton)
        if v > 0.85:
            s.texte(((x0 + x1) / 2, y), '%d – %d' % (a, b), 32, INK)
    s.opacite(_doux((t - 2.4) / 0.5))
    s.texte((360, 330), '%d ans  ·  %d ans' % (bas, haut), 26, INK_2)


def _scene_etiquettes(p, par, t):
    mots = par['mots']
    s = _surface(p, 720, 400)
    hauteur = min(62, 340 / max(1, len(mots)) - 10)
    pas = hauteur + 14
    y0 = 200 - (len(mots) * pas) / 2 + pas / 2
    if par.get('onde'):
        y0 -= 34
    for i, mot in enumerate(mots):
        v = _doux((t - (0.25 + i * 0.42)) / 0.42)
        if not s.opacite(v):
            continue
        y = y0 + i * pas + (1 - v) * 22
        s.rrect(80, y - hauteur / 2, 640, y + hauteur / 2, hauteur * 0.34,
                fill=TONS[i % len(TONS)], bord=(255, 255, 255), trait=3)
        if par.get('numerote'):
            s.disque((124, y), hauteur * 0.32, fill=WHITE_WARM)
            s.texte((124, y), str(i + 1), hauteur * 0.38, INK_2)
            s.texte((164, y), mot, hauteur * 0.44, INK, 'lm')
        else:
            s.texte((360, y), mot, hauteur * 0.44, INK)
    if par.get('onde'):
        v = _doux((t - (0.25 + len(mots) * 0.42 + 0.3)) / 0.6)
        if s.opacite(v):
            grave = par['onde'] == 'grave'
            fs._onde(s, 360, 356, 460 * v, 2.0 if grave else 5.0,
                     34 if grave else 24, BLEU if grave else CLAY)


def _scene_cellules(p, par, t):
    s = _surface(p, 720, 360)
    a1 = _doux(t / 0.5)
    if s.opacite(a1):
        s.disque((190, 150), 76, fill=LILAC, bord=WHITE_WARM, trait=4)
        s.disque((190, 150), 28, fill=INK_2)
        s.texte((190, 268), 'ovule', 34, INK_2)
    a2 = _doux((t - 1.1) / 0.5)
    if a2 > 0 and s.opacite(a2):
        s.disque((470, 140), 34, fill=SKY, bord=WHITE_WARM, trait=4)
        # La queue bat : une sinusoïde dont la phase suit le temps.
        queue = [(470 + 30 + i * 6.6, 140 + math.sin(i / 3.0 + t * 5.0) * 20)
                 for i in range(20)]
        s.ligne(queue, SKY, 5)
        s.texte((520, 268), 'spermatozoïde', 30, INK_2)
    if s.opacite(_doux((t - 2.2) / 0.5)):
        s.texte((360, 330), 'cellules reproductrices', 32, CLAY)


def _scene_ensemble(p, par, t):
    s = _surface(p, 640, 360)
    # Les organes arrivent dispersés, puis le cadre les rassemble.
    v = _doux((t - 0.9) / 1.0)
    places = ((-150, -80), (0, -110), (150, -70), (-110, 60), (120, 70))
    for i, (dx, dy) in enumerate(places):
        a = _doux((t - (0.15 + i * 0.16)) / 0.35)
        if not s.opacite(a):
            continue
        s.disque((320 + dx * (1 - v * 0.55), 165 + dy * (1 - v * 0.55)), 36,
                 fill=TONS[i % len(TONS)], bord=WHITE_WARM, trait=4)
    if s.opacite(v):
        s.rrect(150, 60, 490, 272, 28, fill=None, bord=CLAY, trait=5)
    if s.opacite(_doux((t - 2.2) / 0.5)):
        s.texte((320, 326), 'un ensemble d’organes', 32, CLAY)


def _scene_paires(p, par, t):
    gauche, droite = par['gauche'], par['droite']
    s = _surface(p, 760, 400)
    hauteur = min(58, 360 / max(1, len(gauche)) - 8)
    pas = hauteur + 12
    y0 = 200 - (len(gauche) * pas) / 2 + pas / 2
    for i, (g, d) in enumerate(zip(gauche, droite)):
        y = y0 + i * pas
        a = _doux((t - (0.2 + i * 0.5)) / 0.4)
        if s.opacite(a):
            s.rrect(20, y - hauteur / 2, 330, y + hauteur / 2, hauteur * 0.34,
                    fill=TONS[i % len(TONS)], bord=(255, 255, 255), trait=3)
            s.texte((175, y), g, hauteur * 0.40, INK)
        v = _doux((t - (0.45 + i * 0.5)) / 0.35)
        if v > 0 and s.opacite(1.0):
            s.ligne([(336, y), (336 + 58 * v, y)], INK_2, 4)
        a2 = _doux((t - (0.65 + i * 0.5)) / 0.4)
        if a2 > 0 and s.opacite(a2):
            s.rrect(400, y - hauteur / 2, 740, y + hauteur / 2, hauteur * 0.34,
                    fill=WHITE_WARM, bord=(255, 255, 255), trait=3)
            s.texte((570, y), d, hauteur * 0.40, INK_2)


def _scene_boucle(p, par, t):
    s = _surface(p, 520, 380)
    v = _doux((t - 0.3) / 1.8)
    if v > 0 and s.opacite(1.0):
        n = max(2, int(120 * v))
        points = [(260 + math.cos(-math.pi / 2 + i / 120 * 2 * math.pi * 0.93) * 150,
                   190 + math.sin(-math.pi / 2 + i / 120 * 2 * math.pi * 0.93) * 125)
                  for i in range(n)]
        s.ligne(points, SKY, 10)
        if v > 0.92:
            fs._fleche(s, points[-8], points[-1], SKY, 10, 26)
    if s.opacite(_doux(t / 0.5)):
        fs._goutte(s, 260, 50, 28)
    if s.opacite(_doux((t - 2.4) / 0.5)):
        s.texte((260, 200), 'il revient', 36, CLAY)
        s.texte((260, 246), 'à son départ', 36, CLAY)


def _scene_cycle(p, par, t):
    """Le paysage, et les étapes allumées une à une jusqu'à `jusqua`."""
    jusqua = par.get('jusqua', 4)
    s = _surface(p, 960, 400)
    sol, mer = 312.0, 344.0

    s.opacite(1.0)
    s.rrect(0, mer, 960, 404, 0, fill=(150, 196, 226))
    s.poly([(0, sol), (326, sol - 26), (595, sol - 8), (960, sol - 34),
            (960, mer + 2), (0, mer + 2)], fill=(168, 196, 150))
    fs._soleil(s, 134, 80, 34)

    # Les étapes déjà acquises sont posées d'emblée ; seule la dernière du
    # plan s'allume sous les yeux de l'enfant.
    def part(k):
        if k < jusqua:
            return 1.0
        return _doux((t - 0.8) / 1.2) if k == jusqua else 0.0

    v = part(1)
    if v > 0 and s.opacite(v):
        for i in range(4):
            x = 211 + i * 43
            fs._fleche(s, (x, mer - 6), (x, mer - 6 - 160 * v), SKY, 4, 10)
    v = part(2)
    if v > 0 and s.opacite(v):
        fs._nuage(s, 538, 104, 62)
    v = part(3)
    if v > 0 and s.opacite(v):
        for i in range(7):
            x = 442 + i * 32
            s.ligne([(x, 144), (x - 6 - 60 * v, 144 + 90 * v)], SKY, 4)
    v = part(4)
    if v > 0 and s.opacite(v):
        for i in range(3):
            x = 672 + i * 86
            fs._fleche(s, (x, sol - 26 + i * 6), (x + 67, mer - 4), BLEU, 5, 12)

    nom = par.get('nom')
    if nom and s.opacite(_doux((t - 2.2) / 0.5)):
        # Le nom de l’étape se pose sur une pastille : écrit à même le vert
        # du sol, il devenait illisible à la taille d’un téléphone.
        demi = s.p.large(nom, 36 * s.e) / 2 / s.e + 34
        s.rrect(480 - demi, 356, 480 + demi, 400, 22, fill=WHITE_WARM)
        s.texte((480, 378), nom, 36, CLAY)


def _scene_verres(p, par, t):
    s = _surface(p, 640, 380)
    for i, claire in enumerate((True, False)):
        a = _doux((t - (0.25 + i * 0.7)) / 0.5)
        if not s.opacite(a):
            continue
        fs._verre(s, 200 + i * 240, 150, 220, claire=claire)
    for i, bonne in enumerate((True, False)):
        v = _doux((t - (1.7 + i * 0.6)) / 0.45)
        if not s.opacite(v):
            continue
        fs._coche(s, 200 + i * 240, 292, 34, bonne)
    if s.opacite(_doux((t - 3.0) / 0.5)):
        s.texte((320, 360), 'sans danger pour la santé', 30, CLAY)


def _scene_origines(p, par, t):
    s = _surface(p, 640, 380)
    for i, (mot, ton) in enumerate((('végétal', MINT), ('animal', SAND))):
        a = _doux((t - (0.2 + i * 0.45)) / 0.45)
        if not s.opacite(a):
            continue
        s.disque((200 + i * 240, 90), 62, fill=ton, bord=WHITE_WARM, trait=4)
        s.texte((200 + i * 240, 90), mot, 26, INK)
    v = _doux((t - 1.5) / 0.6)
    if v > 0 and s.opacite(v):
        fs._fleche(s, (200, 160), (280, 216), INK_2, 4, 11)
        fs._fleche(s, (440, 160), (360, 216), INK_2, 4, 11)
    a = _doux((t - 2.2) / 0.5)
    if a > 0 and s.opacite(a):
        s.rrect(190, 236, 450, 310, 24, fill=(132, 110, 78), bord=(255, 255, 255), trait=3)
        s.texte((320, 273), 'compost', 38, WHITE_WARM)
    if s.opacite(_doux((t - 2.9) / 0.5)):
        s.texte((320, 358), 'un engrais naturel', 30, CLAY)


def _scene_sols(p, par, t):
    s = _surface(p, 640, 360)
    for i, (ton, mot) in enumerate((((214, 198, 162), 'sol pauvre'),
                                    ((104, 84, 60), 'sol enrichi'))):
        a = _doux((t - (0.2 + i * 1.4)) / 0.5)
        if not s.opacite(a):
            continue
        cx = 170 + i * 300
        s.rrect(cx - 110, 170, cx + 110, 280, 16, fill=ton)
        s.texte((cx, 318), mot, 30, INK_2)
    v = _doux((t - 1.0) / 0.6)
    if v > 0 and s.opacite(v):
        fs._fleche(s, (292, 222), (292 + 86 * v, 222), CLAY, 6, 16)
    pousse = _doux((t - 2.1) / 0.7)
    if pousse > 0 and s.opacite(1.0):
        s.ligne([(470, 170), (470, 170 - 86 * pousse)], (120, 160, 96), 6)
        if pousse > 0.6:
            s.disque((446, 110), 24, fill=MINT)
            s.disque((494, 96), 24, fill=MINT)


def _scene_lampe(p, par, t):
    s = _surface(p, 640, 440)
    monte = _doux(t / 0.6)
    if not s.opacite(monte):
        return
    # La projection de la lampe est plus haute que son échelle : à 330 elle
    # débordait du cadre, et la grille comme le réservoir étaient rognés.
    cote, cy = 250.0, 190.0 + (1 - monte) * 22
    allumee = _doux((t - 1.0) / 0.6) > 0.5 if par.get('allumage') else True
    fs._lampe(s, 320, cy, cote, numeros=False, allumee=allumee)

    if par.get('numeros'):
        # Les repères se calculent depuis la même échelle que la lampe : une
        # liste écrite à la main se décalerait au premier changement de taille,
        # et le numéro 3 cesserait de montrer la mèche.
        places = ((320, cy + cote * 0.50), (320 + cote * 0.44, cy + cote * 0.38),
                  (320, cy + cote * 0.17), (320 - cote * 0.33, cy - cote * 0.18),
                  (320, cy - cote * 0.58))
        vus = 0
        for n, (x, y) in enumerate(places, start=1):
            v = _doux((t - (0.9 + (n - 1) * 0.45)) / 0.35)
            if v <= 0:
                continue
            vus = n
            s.opacite(v)
            s.disque((x, y), 26 * (1 + 0.5 * (1 - v)), fill=WHITE_WARM, bord=CLAY, trait=4)
            s.texte((x, y), str(n), 28, CLAY)
        _compteur(p, vus, GOLD)
    elif par.get('allumage') and s.opacite(_doux((t - 2.0) / 0.5)):
        s.texte((320, 412), 'lampe tempête', 34, CLAY)


SCENES = {
    'fleche': _scene_fleche, 'barres': _scene_barres, 'etiquettes': _scene_etiquettes,
    'cellules': _scene_cellules, 'ensemble': _scene_ensemble, 'paires': _scene_paires,
    'boucle': _scene_boucle, 'cycle': _scene_cycle, 'verres': _scene_verres,
    'origines': _scene_origines, 'sols': _scene_sols, 'lampe': _scene_lampe,
}


def _adapter(fn):
    def dessin(d, par, t):
        plan = Plan()
        fn(plan, par, t)
        plan.poser(d)
    return dessin


motion.SCENES.update({nom: _adapter(fn) for nom, fn in SCENES.items()})

rendre_plan = motion.rendre_plan
