# -*- coding: utf-8 -*-
"""
Les figures des dix leçons d-anglais de KLEIN (CE1) — cahier du 26 octobre
au 2 novembre 2026.

Cinquante-cinq images, aucune générée, et presque aucune dessinée à la
main : ces leçons-là sont des **tableaux**. « small, smaller, smallest »
ne s-illustre pas par une scène, il s-illustre par ses trois colonnes —
celles que la maîtresse a tracées au tableau et que KLEIN a recopiées.
Une image qui montre autre chose que ce tableau lui apprendrait autre
chose que ce qu-on lui demandera.

Le module est donc fait d-instruments et non de dessins :

  _table3      trois colonnes, une ligne par mot. Sert aux trois leçons de
               comparaison, avec des mots différents à chaque fois
  _grille2x2   près / loin croisé avec singulier / pluriel. C-est la forme
               même de la leçon sur les démonstratifs : quatre mots, deux
               questions à se poser
  _calendrier  les douze mois, ceux dont on parle allumés. Un mois allumé
               au milieu des onze autres se retient mieux qu-un mois seul
  _tuiles      les mots en désordre en haut, la phrase remise en bas. Le
               désordre doit être VISIBLE, sinon la leçon n-a pas d-objet

Un instrument se corrige une fois pour les cinquante-cinq figures.

Usage :  python work/figures-anglais-oct.py
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

VERT = (122, 164, 108)
VERT_PALE = (206, 221, 199)
TERRE = (168, 122, 86)
ROUGE = (183, 66, 52)

# La bande qu-un bandeau de leçon montre réellement d-une couverture
# 960x540, mesurée dans l-application. Plus étroite que celle de la fiche.
BANDEAU = (184, 356)


# --------------------------------------------------------------------------
# Les instruments

def _mesure(t, s, taille):
    return t.d.textlength(s, font=t.pol(taille)) / S


def _pastille(t, cx, cy, mot, taille, fond=WHITE_WARM, couleur=INK, marge=10, h=None):
    """Un mot dans une pastille, large juste ce qu-il faut."""
    w = _mesure(t, mot, taille) + marge * 2
    h = h if h else taille + 14
    t.rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, h / 2, fill=fond, bord=INK, trait=1.8)
    t.texte((cx, cy), mot, taille, couleur)
    return w


def _taille_tenant(t, mots, largeur, taille_max, mini=8):
    """La plus grande taille où le plus long des mots tient encore."""
    taille = taille_max
    while taille > mini and max(_mesure(t, m, taille) for m in mots) + 18 > largeur:
        taille -= 1
    return taille


def _table3(t, lignes, haut=70, bas=290, gauche=14, droite=306, titre=None, surligne=None):
    """Trois colonnes : le mot, son comparatif, son superlatif.

    C-est la forme du cahier. Les colonnes ont la même largeur et la
    taille du texte descend jusqu-à ce que le plus long mot tienne : un
    mot coupé vaudrait mieux ne pas être écrit.
    """
    if titre:
        t.texte(((gauche + droite) / 2, haut - 18), titre, 15, INK_2)
    cols = 3
    larg = (droite - gauche) / cols
    mots = [m for ligne in lignes for m in ligne]
    taille = _taille_tenant(t, mots, larg, 13)
    pas = (bas - haut) / max(1, len(lignes))
    for i, ligne in enumerate(lignes):
        y = haut + pas * (i + 0.5)
        for j, mot in enumerate(ligne):
            cx = gauche + larg * (j + 0.5)
            vif = surligne is not None and (i, j) in surligne
            _pastille(t, cx, y, mot, taille,
                      fond=(GOLD if vif else (SAND if j == 0 else WHITE_WARM)),
                      marge=6, h=min(pas * 0.74, 42))


def _grille2x2(t, cases, surligne=None, haut=86, bas=268, gauche=56, droite=302):
    """près / loin croisé avec un / plusieurs. Quatre mots, deux questions."""
    lx = (gauche + droite) / 2
    ly = (haut + bas) / 2
    t.texte(((gauche + lx) / 2, haut - 20), 'one', 14, INK_2)
    t.texte(((lx + droite) / 2, haut - 20), 'many', 14, INK_2)
    # Collées au bord, ces deux étiquettes étaient rognées. Elles ont
    # maintenant leur colonne, et la grille a reculé d-autant.
    t.texte((gauche - 30, (haut + ly) / 2), 'near', 13, INK_2)
    t.texte((gauche - 30, (ly + bas) / 2), 'far', 13, INK_2)
    for i in range(2):
        for j in range(2):
            x0 = gauche + (droite - gauche) / 2 * j
            y0 = haut + (bas - haut) / 2 * i
            mot = cases[i][j]
            vif = surligne == mot
            t.rrect(x0 + 5, y0 + 5, x0 + (droite - gauche) / 2 - 5, y0 + (bas - haut) / 2 - 5,
                    12, fill=(GOLD if vif else WHITE_WARM), bord=INK, trait=2)
            t.texte((x0 + (droite - gauche) / 4, y0 + (bas - haut) / 4), mot, 22, INK)


MOIS = ('January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December')


def _calendrier(t, surlignes=(), note=None, haut=58, bas=272, gauche=16, droite=304):
    """Les douze mois, ceux dont on parle allumés."""
    larg = (droite - gauche) / 3
    pas = (bas - haut) / 4
    taille = _taille_tenant(t, MOIS, larg, 12)
    for k, mois in enumerate(MOIS):
        cx = gauche + larg * (k % 3 + 0.5)
        cy = haut + pas * (k // 3 + 0.5)
        vif = mois in surlignes
        _pastille(t, cx, cy, mois, taille,
                  fond=(GOLD if vif else WHITE_WARM),
                  couleur=INK, marge=5, h=pas * 0.72)
    if note:
        t.texte(((gauche + droite) / 2, bas + 26), note, 15, INK)


def _tuiles(t, melange, ordre, haut=74, bas=236):
    """Le désordre en haut, la phrase remise en bas. La flèche fait le lien."""
    for y, mots, fond in ((haut, melange, LILAC), (bas, ordre, MINT)):
        taille = _taille_tenant(t, mots, 300 / max(1, len(mots)), 14)
        larges = [_mesure(t, m, taille) + 12 for m in mots]
        total = sum(larges) + 6 * (len(mots) - 1)
        x = 160 - total / 2
        for mot, w in zip(mots, larges):
            t.rrect(x, y - 15, x + w, y + 15, 7, fill=fond, bord=INK, trait=1.8)
            t.texte((x + w / 2, y), mot, taille, INK)
            x += w + 6
    t.ligne([(160, haut + 26), (160, bas - 26)], CLAY, 2.6)
    for d in (-7, 7):
        t.ligne([(160, bas - 26), (160 + d, bas - 36)], CLAY, 2.6)


def _liste(t, items, titre=None, haut=76, taille=13):
    """Une liste numérotée, comme celle que le cahier met après « leads to »."""
    if titre:
        t.texte((160, haut - 24), titre, 16, INK)
    pas = 46
    for i, texte in enumerate(items):
        y = haut + pas * i
        t.rrect(24, y, 296, y + 36, 10, fill=WHITE_WARM, bord=INK, trait=1.8)
        t.disque((44, y + 18), 11, fill=GOLD, bord=INK, trait=1.5)
        t.texte((44, y + 18), str(i + 1), 13, INK)
        taille_ligne = _taille_tenant(t, [texte], 226, taille)
        t.texte((62, y + 18), texte, taille_ligne, INK, ancre='lm')


def _bandeau_couv(t, titre, sous_titre=None):
    """Le haut d-une couverture : tout doit tenir dans la bande du bandeau."""
    w = _mesure(t, titre, 26) + 56
    t.rrect(480 - w / 2, 192, 480 + w / 2, 232, 20, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 212), titre, 26, INK)
    if sous_titre:
        t.texte((480, 338), sous_titre, 17, INK)


# --------------------------------------------------------------------------
# Les pictogrammes

def _maison(t, cx, cy, l=70):
    h = l * 0.78
    t.rrect(cx - l / 2, cy - h / 2, cx + l / 2, cy + h / 2, 3, fill=SAND, bord=INK, trait=2)
    t.poly([(cx - l * 0.62, cy - h / 2), (cx, cy - h * 1.05), (cx + l * 0.62, cy - h / 2)],
           fill=CLAY, bord=INK, trait=2)
    t.rrect(cx - l * 0.13, cy + h / 2 - l * 0.34, cx + l * 0.13, cy + h / 2, 2,
            fill=TERRE, bord=INK, trait=1.5)


def _pot(t, cx, cy, l=56):
    t.poly([(cx - l * 0.34, cy - l * 0.36), (cx + l * 0.34, cy - l * 0.36),
            (cx + l * 0.46, cy + l * 0.1), (cx + l * 0.3, cy + l * 0.42),
            (cx - l * 0.3, cy + l * 0.42), (cx - l * 0.46, cy + l * 0.1)],
           fill=TERRE, bord=INK, trait=2)
    t.rrect(cx - l * 0.42, cy - l * 0.46, cx + l * 0.42, cy - l * 0.3, 4,
            fill=CLAY, bord=INK, trait=1.8)


def _plante(t, cx, cy, l=60):
    t.ligne([(cx, cy + l * 0.45), (cx, cy - l * 0.3)], VERT, 3)
    for cote in (-1, 1):
        t.d.pieslice([int((cx - l * 0.4 if cote < 0 else cx) * S), int((cy - l * 0.3) * S),
                      int((cx if cote < 0 else cx + l * 0.4) * S), int((cy + l * 0.1) * S)],
                     0 if cote < 0 else 180, 180 if cote < 0 else 360,
                     fill=VERT, outline=INK, width=int(1.6 * S))
    t.rrect(cx - l * 0.36, cy + l * 0.4, cx + l * 0.36, cy + l * 0.56, 4,
            fill=TERRE, bord=INK, trait=1.6)


def _bete(t, cx, cy, l=62):
    """Un animal très simple : un corps, une tête, quatre pattes."""
    t.rrect(cx - l * 0.42, cy - l * 0.16, cx + l * 0.26, cy + l * 0.2, 10,
            fill=SAND, bord=INK, trait=2)
    t.disque((cx + l * 0.34, cy - l * 0.16), l * 0.17, fill=SAND, bord=INK, trait=2)
    for dx in (-0.3, -0.06, 0.1):
        t.ligne([(cx + l * dx, cy + l * 0.2), (cx + l * dx, cy + l * 0.42)], INK, 2.4)


def _copie(t, cx, cy):
    """Tricher : un regard qui passe d-une feuille à l-autre."""
    for dx, fond in ((-34, WHITE_WARM), (34, WHITE_WARM)):
        t.rrect(cx + dx - 26, cy - 34, cx + dx + 26, cy + 34, 5, fill=fond, bord=INK, trait=2)
        for i in range(4):
            t.ligne([(cx + dx - 17, cy - 20 + i * 14), (cx + dx + 17, cy - 20 + i * 14)], INK_2, 1.6)
    t.d.arc([int((cx - 22) * S), int((cy - 56) * S), int((cx + 22) * S), int((cy - 20) * S)],
            200, 340, fill=ROUGE, width=int(2.6 * S))
    t.ligne([(cx + 20, cy - 44), (cx + 26, cy - 52)], ROUGE, 2.6)
    t.ligne([(cx + 20, cy - 44), (cx + 28, cy - 42)], ROUGE, 2.6)


def _pupitre_vide(t, cx, cy):
    """L-école buissonnière : la table est là, la chaise est vide."""
    t.rrect(cx - 44, cy - 10, cx + 44, cy + 2, 3, fill=SAND, bord=INK, trait=2)
    for dx in (-36, 36):
        t.ligne([(cx + dx, cy + 2), (cx + dx, cy + 40)], INK, 2.4)
    t.rrect(cx - 16, cy + 14, cx + 16, cy + 22, 3, fill=CLAY, bord=INK, trait=1.8)
    t.ligne([(cx + 16, cy + 22), (cx + 16, cy - 16)], INK, 2.2)
    t.texte((cx, cy - 36), '?', 30, ROUGE)


# --------------------------------------------------------------------------
# Les figures, leçon par leçon

def _fab_couv(titre, sous):
    def f(t):
        _bandeau_couv(t, titre, sous)
    return f


def _fab_table(lignes, titre=None, surligne=None):
    def f(t):
        _table3(t, lignes, titre=titre, surligne=surligne)
    return f


def _fab_calendrier(surlignes, note):
    def f(t):
        _calendrier(t, surlignes, note)
    return f


def _fab_tuiles(melange, ordre, note=None):
    def f(t):
        _tuiles(t, melange, ordre)
        if note:
            t.texte((160, 282), note, 15, INK)
    return f


def _fab_liste(items, titre):
    def f(t):
        _liste(t, items, titre)
    return f


def _fab_demo(surligne, exemple):
    def f(t):
        _grille2x2(t, (('this', 'these'), ('that', 'those')), surligne)
        t.texte((160, 294), exemple, 13, INK)
    return f


# --- Couvertures (tout tient dans la bande 184-356) -----------------------

def couv_jumbled(t):
    _bandeau_couv(t, 'Jumbled words')
    _tuiles_couv(t, ['class', 'am', 'in', 'I'], ['I', 'am', 'in', 'class'])


def couv_sentences(t):
    _bandeau_couv(t, 'Jumbled sentences')
    _tuiles_couv(t, ['breakfast', 'bed', 'wake up'], ['wake up', 'bed', 'breakfast'])


def _tuiles_couv(t, melange, ordre):
    """La même idée que _tuiles, mais couchée pour tenir dans le bandeau."""
    for y, mots, fond in ((268, melange, LILAC), (322, ordre, MINT)):
        larges = [_mesure(t, m, 17) + 20 for m in mots]
        total = sum(larges) + 10 * (len(mots) - 1)
        x = 480 - total / 2
        for mot, w in zip(mots, larges):
            t.rrect(x, y - 17, x + w, y + 17, 8, fill=fond, bord=INK, trait=2)
            t.texte((x + w / 2, y), mot, 17, INK)
            x += w + 10


def couv_demo(t):
    _bandeau_couv(t, 'Demonstrative adjectives')
    for i, mot in enumerate(('this', 'these', 'that', 'those')):
        _pastille(t, 222 + i * 172, 300, mot, 24, fond=(SKY, MINT, SAND, LILAC)[i], marge=20)


def couv_comparatif(t):
    _bandeau_couv(t, 'Comparing adjectives')
    for i, mot in enumerate(('small', 'smaller', 'smallest')):
        _pastille(t, 250 + i * 230, 300, mot, 24, fond=(WHITE_WARM, SAND, GOLD)[i], marge=22)


def couv_plus(t):
    _bandeau_couv(t, 'More and most')
    for i, mot in enumerate(('beautiful', 'more beautiful', 'most beautiful')):
        _pastille(t, 236 + i * 244, 300, mot, 20, fond=(WHITE_WARM, SAND, GOLD)[i], marge=16)


def couv_irregulier(t):
    _bandeau_couv(t, 'Irregular adjectives')
    for i, mot in enumerate(('good', 'better', 'best')):
        _pastille(t, 268 + i * 212, 300, mot, 24, fond=(WHITE_WARM, SAND, GOLD)[i], marge=24)


def couv_mois(t):
    _bandeau_couv(t, 'The months of the year')
    larg = 148
    for k in range(12):
        cx = 110 + larg * (k % 6) + (0 if k < 6 else 0)
        cy = 276 if k < 6 else 322
        _pastille(t, cx, cy, MOIS[k][:3], 16, fond=(GOLD if k in (0, 11) else WHITE_WARM), marge=14)


def couv_jours(t):
    _bandeau_couv(t, 'Days in each month')
    for i, (n, mots) in enumerate((('31', '7 months'), ('30', '4 months'), ('28 or 29', 'February'))):
        cx = 232 + i * 248
        t.rrect(cx - 96, 258, cx + 96, 344, 14, fill=WHITE_WARM, bord=INK, trait=2.2)
        t.texte((cx, 288), n, 28, CLAY)
        t.texte((cx, 324), mots, 16, INK)


def couv_cheating(t):
    _bandeau_couv(t, 'Cheating and truancy')
    _copie(t, 370, 300)
    _pupitre_vide(t, 600, 292)


def couv_sol(t):
    _bandeau_couv(t, 'Uses of the soil')
    _plante(t, 300, 300, 70)
    _maison(t, 420, 300, 74)
    _pot(t, 540, 300, 64)
    _bete(t, 660, 300, 70)


# --------------------------------------------------------------------------

COMPARE_COURT = [('small', 'smaller', 'smallest'), ('old', 'older', 'oldest'),
                 ('young', 'younger', 'youngest'), ('long', 'longer', 'longest'),
                 ('short', 'shorter', 'shortest')]
COMPARE_DOUBLE = [('fat', 'fatter', 'fattest'), ('big', 'bigger', 'biggest')]
COMPARE_YI = [('happy', 'happier', 'happiest'), ('lazy', 'lazier', 'laziest')]
COMPARE_PLUS = [('beautiful', 'more beautiful', 'most beautiful'),
                ('handsome', 'more handsome', 'most handsome'),
                ('careful', 'more careful', 'most careful')]
COMPARE_PLUS_2 = [('wonderful', 'more wonderful', 'most wonderful'),
                  ('gracious', 'more gracious', 'most gracious')]
COMPARE_PLUS_3 = [('intelligent', 'more intelligent', 'most intelligent'),
                  ('expensive', 'more expensive', 'most expensive')]
IRREG_1 = [('good', 'better', 'best'), ('bad', 'worse', 'worst')]
IRREG_2 = [('little', 'less', 'least'), ('many, much', 'more', 'most')]
IRREG_3 = [('far', 'farther', 'farthest'), ('far', 'further', 'furthest')]
IRREG_4 = [('old', 'older', 'oldest'), ('old', 'elder', 'eldest')]

MOIS_30 = ('April', 'June', 'September', 'November')
MOIS_31 = ('January', 'March', 'May', 'July', 'August', 'October', 'December')

FIGURES = [
    # Jumbled words
    ('an-jw-couv', 960, 540, couv_jumbled),
    ('an-jw-def', 320, 320, _fab_tuiles(['are', 'words', 'jumbled'], ['jumbled', 'words', 'are'],
                                        'words put back in order')),
    ('an-jw-class', 320, 320, _fab_tuiles(['class', 'am', 'in', 'I'], ['I', 'am', 'in', 'class'])),
    ('an-jw-clean', 320, 320, _fab_tuiles(['clean', 'is', 'classroom', 'my'],
                                          ['my', 'classroom', 'is', 'clean'])),
    ('an-jw-monday', 320, 320, _fab_tuiles(['Is', 'today', 'Monday'], ['Monday', 'is', 'today'])),
    # Jumbled sentences
    ('an-js-couv', 960, 540, couv_sentences),
    ('an-js-def', 320, 320, _fab_tuiles(['bed', 'wake up', 'breakfast'],
                                        ['wake up', 'bed', 'breakfast'],
                                        'sentences put in order')),
    ('an-js-steps', 320, 320, _fab_liste(['Read slowly', 'Put numbers', 'Read to check',
                                          'Copy in order'], 'Four steps')),
    ('an-js-morning', 320, 320, _fab_liste(['I wake up at 6 am', 'I make my bed',
                                            'I greet my parents', 'I take my breakfast'],
                                           'My morning')),
    ('an-js-last', 320, 320, _fab_liste(['I take my breakfast',
                                         'I say goodbye and go to school'], 'The end')),
    # Demonstrative adjectives
    ('an-dm-couv', 960, 540, couv_demo),
    ('an-dm-def', 320, 320, _fab_demo(None, 'they show where a noun is')),
    ('an-dm-this', 320, 320, _fab_demo('this', 'This is a cap on my head.')),
    ('an-dm-these', 320, 320, _fab_demo('these', 'These are cups on the table.')),
    ('an-dm-that', 320, 320, _fab_demo('that', 'That is a house over there.')),
    ('an-dm-those', 320, 320, _fab_demo('those', 'Those are caps over there.')),
    ('an-dm-grid', 320, 320, _fab_demo(None, 'near or far, one or many')),
    # Comparing with -er and -est
    ('an-cr-couv', 960, 540, couv_comparatif),
    ('an-cr-rule', 320, 320, _fab_table([('small', 'smaller', 'smallest')],
                                        'add -er and -est', {(0, 1), (0, 2)})),
    ('an-cr-table', 320, 320, _fab_table(COMPARE_COURT, 'the regular way')),
    ('an-cr-double', 320, 320, _fab_table(COMPARE_DOUBLE, 'the last letter doubles',
                                          {(0, 1), (0, 2), (1, 1), (1, 2)})),
    ('an-cr-yi', 320, 320, _fab_table(COMPARE_YI, 'y becomes i',
                                      {(0, 1), (0, 2), (1, 1), (1, 2)})),
    ('an-cr-three', 320, 320, _fab_table([('positive', 'comparative', 'superlative')],
                                         'three forms')),
    # More and most
    ('an-cm-couv', 960, 540, couv_plus),
    ('an-cm-rule', 320, 320, _fab_table([('beautiful', 'more beautiful', 'most beautiful')],
                                        'long words take more and most', {(0, 1), (0, 2)})),
    ('an-cm-list', 320, 320, _fab_table(COMPARE_PLUS, 'three long adjectives')),
    ('an-cm-list2', 320, 320, _fab_table(COMPARE_PLUS_2, 'two more')),
    ('an-cm-list3', 320, 320, _fab_table(COMPARE_PLUS_3, 'and two more')),
    ('an-cm-great', 320, 320, _fab_table([('great', 'greater', 'greatest')],
                                         'great is short: no more, no most', {(0, 1), (0, 2)})),
    # Irregular adjectives
    ('an-ci-couv', 960, 540, couv_irregulier),
    ('an-ci-rule', 320, 320, _fab_table([('good', 'better', 'best')],
                                        'no rule: learn them', {(0, 1), (0, 2)})),
    ('an-ci-good', 320, 320, _fab_table(IRREG_1, 'good and bad')),
    ('an-ci-little', 320, 320, _fab_table(IRREG_2, 'little, many and much')),
    ('an-ci-far', 320, 320, _fab_table(IRREG_3, 'far has two ways')),
    ('an-ci-old', 320, 320, _fab_table(IRREG_4, 'old has two ways')),
    # The months of the year
    ('an-mo-couv', 960, 540, couv_mois),
    ('an-mo-twelve', 320, 320, _fab_calendrier((), 'twelve months in a year')),
    ('an-mo-first', 320, 320, _fab_calendrier(('January',), 'the first month')),
    ('an-mo-last', 320, 320, _fab_calendrier(('December',), 'the last month')),
    ('an-mo-six', 320, 320, _fab_calendrier(MOIS[:6], 'January to June')),
    ('an-mo-rest', 320, 320, _fab_calendrier(MOIS[6:], 'July to December')),
    # Days in each month
    ('an-jo-couv', 960, 540, couv_jours),
    ('an-jo-30', 320, 320, _fab_calendrier(MOIS_30, 'these four have 30 days')),
    ('an-jo-31', 320, 320, _fab_calendrier(MOIS_31, 'these seven have 31 days')),
    ('an-jo-feb', 320, 320, _fab_calendrier(('February',), '28 days, 29 in a leap year')),
    ('an-jo-count', 320, 320, _fab_liste(['7 months have 31 days', '4 months have 30 days',
                                          'February has 28 or 29'], 'Twelve months')),
    # Cheating and truancy
    ('an-ch-couv', 960, 540, couv_cheating),
    ('an-ch-def', 320, 320, lambda t: (_copie(t, 160, 150),
                                       t.texte((160, 240), 'acting dishonestly', 17, INK),
                                       t.texte((160, 268), 'to gain something', 17, INK))),
    ('an-ch-leads', 320, 320, _fab_liste(['Failure in exams', 'Lack of trust and respect',
                                          'Hatred and stress'], 'Cheating leads to')),
    ('an-ch-truancy', 320, 320, lambda t: (_pupitre_vide(t, 160, 146),
                                           t.texte((160, 238), 'staying away from school', 15, INK),
                                           t.texte((160, 266), 'without permission', 15, INK))),
    ('an-ch-truant', 320, 320, lambda t: (_pupitre_vide(t, 160, 140),
                                          _pastille(t, 160, 244, 'a truant', 22, fond=GOLD, marge=22),
                                          t.texte((160, 288), 'that is his name', 14, INK_2))),
    # Uses of the soil
    ('an-so-couv', 960, 540, couv_sol),
    ('an-so-uses', 320, 320, _fab_liste(['Plant crops and flowers', 'Build houses',
                                         'Make pots and statues', 'A home for animals'],
                                        'Soil is used to')),
    ('an-so-plant', 320, 320, lambda t: (_plante(t, 160, 150, 92),
                                         t.texte((160, 248), 'crops and flowers', 17, INK))),
    ('an-so-house', 320, 320, lambda t: (_maison(t, 160, 150, 108),
                                         t.texte((160, 248), 'houses', 17, INK))),
    ('an-so-pot', 320, 320, lambda t: (_pot(t, 160, 150, 92),
                                       t.texte((160, 248), 'pots and statues', 17, INK))),
    ('an-so-home', 320, 320, lambda t: (_bete(t, 160, 150, 96),
                                        t.texte((160, 248), 'a home for animals', 17, INK))),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double : ' + str(
        [c for c in cles if cles.count(c) > 1])

    # Les douze mois sont douze, et les trois groupes de jours les
    # couvrent tous exactement une fois. Le cahier, lui, oubliait July
    # dans la liste des mois de 31 jours : une figure qui recopierait
    # l-oubli enseignerait que July n-a pas 31 jours.
    assert len(MOIS) == 12, MOIS
    groupes = list(MOIS_30) + list(MOIS_31) + ['February']
    assert sorted(groupes) == sorted(MOIS), 'les groupes de jours ne couvrent pas les douze mois'
    assert 'July' in MOIS_31, 'July a 31 jours'
    assert len(MOIS_31) == 7 and len(MOIS_30) == 4, (len(MOIS_31), len(MOIS_30))

    # Rien ne doit toucher le bord du cadre, et une couverture ne doit rien
    # mettre hors de la bande que le bandeau montre.
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
            fautifs = fv._hors_bande(t.fini())
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
