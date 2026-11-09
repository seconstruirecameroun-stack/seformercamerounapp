# -*- coding: utf-8 -*-
"""
Les figures de la révision du 9 novembre 2026 pour BRAYNE (CM1) — onze
leçons tirées des tableaux photographiés par le père : deux en sciences,
neuf en anglais.

CE QUE CES LEÇONS DEMANDENT DE MONTRER. Les deux leçons de sciences
portent sur des CHOSES — un sol, un animal — et se montrent par une
vignette de la chose avec ce qu-on en dit. Les neuf leçons d-anglais
portent sur des MOTS dans une phrase, et une phrase ne s-illustre pas par
un dessin : ce qu-il faut voir, c-est le mot à sa place dans la phrase,
mis en évidence. Dessiner un chien à côté de « the old woman » apprendrait
le chien et non l-adjectif.

Quatre instruments, et les cinquante-huit figures en sortent :

  phrase       la phrase écrite, coupée en lignes comme dans un livre, et
               le mot de la leçon en pastille dorée. C-est l-instrument de
               toutes les leçons d-anglais : l-enfant voit la place du mot
               avant d-en voir la règle
  paire        deux colonnes reliées : un mot et son contraire, un mot et
               son synonyme, un animal et son régime. Le trait entre les
               deux est tracé, parce que l-exercice du tableau demande
               précisément de relier
  sol          le profil d-un sol dans son pot, avec sa texture : des
               grains pour le sable, des mottes pour l-argile, des débris
               pour l-humus. Un sol se reconnaît à ce qu-on y voit
  fiche        la liste posée ligne à ligne, comme au cahier

Usage :  python work/figures-brayne-revision-nov.py
"""

import importlib.util
import os
import random

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
TERRE = (168, 122, 86)
GRIS = (176, 176, 170)
ROUGE = (183, 66, 52)
BANDEAU = (184, 356)


def _mesure(t, s, taille):
    return t.d.textlength(s, font=t.pol(taille)) / S


def _legende(t, y, mot, taille=16, couleur=INK_2, large=288, cx=160):
    while _mesure(t, mot, taille) > large and taille > 9:
        taille -= 1
    t.texte((cx, y), mot, taille, couleur)


# --------------------------------------------------------------------------
# La phrase, et le mot mis à sa place

# Ce qu-une pastille ajoute de chaque côté du mot qu-elle entoure.
MARGE_VIF = 6


def _largeur(t, mot, vif, taille):
    """La place que prend un mot, pastille comprise.

    La pastille est comptée ICI et nulle part ailleurs : comptée seulement au
    tracé, elle mordait sur le mot d-à côté — « this yellow bag » montrait
    une pastille posée sur le « s » de this et sur le « b » de bag.
    """
    return _mesure(t, mot, taille) + (MARGE_VIF * 2 if vif else 0)


def _couper(t, mots, taille, large):
    """Coupe une suite de mots en lignes qui tiennent dans la largeur."""
    espace = _mesure(t, ' ', taille)
    lignes, courante, prise = [], [], 0.0
    for mot, vif in mots:
        w = _largeur(t, mot, vif, taille)
        ajout = w + (espace if courante else 0)
        if courante and prise + ajout > large:
            lignes.append(courante)
            courante, prise = [(mot, vif)], w
        else:
            courante.append((mot, vif))
            prise += ajout
    if courante:
        lignes.append(courante)
    return lignes


def phrase(t, mots, legende=None, titre=None, taille=19, large=250, haut=None):
    """La phrase écrite, le ou les mots de la leçon en pastille dorée.

    `mots` est une suite de (mot, vif). La pastille est posée SOUS le mot et
    non autour : un fond doré derrière une lettre la rend moins lisible, et
    c-est la lettre qu-on lit.
    """
    while True:
        lignes = _couper(t, mots, taille, large)
        if len(lignes) <= 4 or taille <= 12:
            break
        taille -= 1
    if titre:
        _legende(t, 56, titre, 17, INK)
    h = len(lignes) * (taille + 16)
    y0 = haut if haut is not None else 160 - h / 2 + taille / 2
    t.rrect(20, y0 - taille - 14, 300, y0 + h - taille / 2 + 2, 14,
            fill=WHITE_WARM, bord=INK, trait=2.4)
    espace = _mesure(t, ' ', taille)
    for i, ligne in enumerate(lignes):
        largeurs = [_largeur(t, m, v, taille) for m, v in ligne]
        x = 160 - (sum(largeurs) + espace * (len(ligne) - 1)) / 2
        y = y0 + i * (taille + 16)
        for (mot, vif), w in zip(ligne, largeurs):
            if vif:
                t.rrect(x, y - taille * 0.74, x + w, y + taille * 0.72, 7,
                        fill=GOLD, bord=INK, trait=1.4)
            t.texte((x + w / 2, y), mot, taille, INK)
            x += w + espace
    if legende:
        _legende(t, y0 + h + 18, legende, 15)


def P(texte, vifs=()):
    """Découpe une phrase en mots, et marque ceux qui doivent ressortir."""
    mots = texte.split(' ')
    vifs = set(vifs)
    return [(m, i in vifs) for i, m in enumerate(mots)]


# --------------------------------------------------------------------------
# Les paires reliées

def paire(t, couples, titre=None, legende=None, couleur=GOLD):
    """Deux colonnes et le trait qui les relie, comme l-exercice du tableau."""
    if titre:
        _legende(t, 56, titre, 17, INK)
    # Les lignes se resserrent quand il y en a quatre : à l-écartement des
    # trois lignes, la légende tombait hors de l-image.
    pas = 46 if len(couples) > 3 else 52
    haut = (84 if titre else 66) + max(0, (3 - len(couples))) * 22
    for i, (g, d) in enumerate(couples):
        y = haut + i * pas
        for x0, x1, mot, fond in ((16, 148, g, WHITE_WARM), (172, 304, d, couleur)):
            t.rrect(x0, y, x1, y + 38, 9, fill=fond, bord=INK, trait=1.8)
            taille = 15
            while _mesure(t, mot, taille) > (x1 - x0) - 12 and taille > 9:
                taille -= 1
            t.texte(((x0 + x1) / 2, y + 19), mot, taille, INK)
        t.ligne([(148, y + 19), (172, y + 19)], INK, 1.8)
    if legende:
        _legende(t, haut + len(couples) * pas + 14, legende, 15)


def fiche(t, titre, lignes, haut=92, vif=()):
    """Une liste posée ligne à ligne, comme au cahier."""
    _legende(t, haut - 28, titre, 17, INK)
    for i, ligne in enumerate(lignes):
        y = haut + i * 44
        t.rrect(22, y, 298, y + 36, 9,
                fill=(GOLD if i in vif else WHITE_WARM), bord=INK, trait=1.8)
        taille = 16
        while _mesure(t, ligne, taille) > 252 and taille > 10:
            taille -= 1
        t.texte((160, y + 18), ligne, taille, INK)


# --------------------------------------------------------------------------
# Le sol dans son pot

def sol(t, nom, fond, texture, legende=None, cx=160, cy=150):
    """Un profil de sol, et la texture qui le fait reconnaître.

    Les grains sont tirés d-un hasard FIXÉ par le nom du sol : la figure est
    donc la même à chaque exécution, sans quoi deux lancements du script
    donneraient deux images différentes pour la même leçon.
    """
    x0, x1 = cx - 112, cx + 112
    y0, y1 = cy - 56, cy + 62
    t.rrect(x0, y0, x1, y1, 12, fill=fond, bord=INK, trait=2.4)
    alea = random.Random(nom)
    for _ in range(texture[0]):
        gx = alea.uniform(x0 + 12, x1 - 12)
        gy = alea.uniform(y0 + 12, y1 - 12)
        r = alea.uniform(*texture[1])
        t.disque((gx, gy), r, fill=texture[2], bord=INK, trait=1.1)
    t.rrect(x0, y0, x1, y1, 12, bord=INK, trait=2.4)
    _legende(t, y1 + 34, nom, 19, INK)
    if legende:
        _legende(t, y1 + 64, legende, 15)


# --------------------------------------------------------------------------
# Les couvertures

def _bandeau(t, titre):
    taille = 26
    while _mesure(t, titre, taille) > 700 and taille > 16:
        taille -= 1
    w = _mesure(t, titre, taille) + 56
    t.rrect(480 - w / 2, 192, 480 + w / 2, 232, 20, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 212), titre, taille, INK)


def _couv_mots(t, titre, mots, vif=()):
    _bandeau(t, titre)
    larg = min(190, 820 / max(1, len(mots)))
    depart = 480 - larg * len(mots) / 2
    for i, m in enumerate(mots):
        x = depart + larg * i
        t.rrect(x + 5, 262, x + larg - 5, 326, 10,
                fill=(GOLD if i in vif else WHITE_WARM), bord=INK, trait=2)
        taille = 20
        while _mesure(t, m, taille) > larg - 22 and taille > 11:
            taille -= 1
        t.texte((x + larg / 2, 294), m, taille, INK)


def _couv_phrase(t, titre, texte, taille=24):
    _bandeau(t, titre)
    while _mesure(t, texte, taille) > 760 and taille > 14:
        taille -= 1
    w = _mesure(t, texte, taille) + 64
    t.rrect(480 - w / 2, 260, 480 + w / 2, 328, 14, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.texte((480, 294), texte, taille, INK)


# --------------------------------------------------------------------------
# Les cinquante-huit figures

SOLS = {
    'argileux': ((196, 150, 120), (14, (9, 14), (168, 118, 92))),
    'sablonneux': ((236, 214, 170), (120, (2.2, 3.4), (206, 178, 126))),
    'humifere': ((96, 78, 62), (26, (4, 9), (62, 92, 58))),
    'calcaire': ((228, 226, 214), (16, (7, 12), (198, 198, 188))),
    'rocailleux': ((176, 172, 160), (13, (12, 19), (138, 136, 128))),
    'marecageux': ((120, 132, 118), (30, (5, 10), (108, 146, 158))),
}


def _sol(nom, etiquette, legende):
    fond, texture = SOLS[nom]
    return lambda t: sol(t, etiquette, fond, texture, legende)


FIGURES = [
    # ---------------------------------------------------------- Les sols
    ('br-so-couv', 960, 540,
     lambda t: _couv_mots(t, 'Les types de sols',
                          ['argileux', 'sablonneux', 'humifère', 'calcaire'])),
    ('br-so-def', 320, 320,
     lambda t: fiche(t, 'Le sol', ['la partie superficielle de la terre',
                                   'composée de roches de plusieurs sortes',
                                   'c’est là que poussent les plantes'])),
    ('br-so-argileux', 320, 320,
     _sol('argileux', 'Le sol argileux', 'Fait d’argile : il colle et retient l’eau.')),
    ('br-so-sablonneux', 320, 320,
     _sol('sablonneux', 'Le sol sablonneux', 'Fait de sable : l’eau le traverse vite.')),
    ('br-so-humifere', 320, 320,
     _sol('humifere', 'Le sol humifère', 'Riche en humus : c’est le plus fertile.')),
    ('br-so-calcaire', 320, 320,
     _sol('calcaire', 'Le sol calcaire', 'Fait de calcaire : clair et sec.')),
    ('br-so-autres', 320, 320,
     lambda t: paire(t, [('rocailleux', 'des cailloux'), ('marécageux', 'de l’eau'),
                         ('humifère', 'de l’humus')], 'Chaque sol, ce qui le remplit')),

    # ------------------------------------------------- Les animaux
    ('br-an-couv', 960, 540,
     lambda t: _couv_mots(t, 'Nutrition et reproduction des animaux',
                          ['herbivore', 'carnivore', 'omnivore', 'granivore'])),
    ('br-an-nutrition', 320, 320,
     lambda t: paire(t, [('herbivore', 'des plantes'), ('carnivore', 'de la viande'),
                         ('omnivore', 'de tout'), ('granivore', 'des graines')],
                     'Le mode de nutrition', 'Ce que l’animal mange.')),
    ('br-an-reproduction', 320, 320,
     lambda t: paire(t, [('ovipare', 'pond des œufs'),
                         ('vivipare', 'des petits vivants')],
                     'Le mode de reproduction', 'Comment naissent ses petits.')),
    ('br-an-pigeon', 320, 320,
     lambda t: fiche(t, 'Le pigeon', ['il vole', 'il est granivore', 'il est ovipare'])),
    ('br-an-vache', 320, 320,
     lambda t: paire(t, [('la vache', 'herbivore'), ('le porc', 'omnivore'),
                         ('tous les deux', 'vivipares')],
                     'Deux animaux qui marchent')),
    ('br-an-maquereau', 320, 320,
     lambda t: paire(t, [('le maquereau', 'nage, ovipare'),
                         ('la vipère', 'rampe, vivipare')],
                     'Deux carnivores', 'La vipère ne pond pas d’œufs.')),

    # ------------------------------------------------- 1. Les adjectifs
    ('be-ad-couv', 960, 540,
     lambda t: _couv_phrase(t, 'Adjectives', 'that old woman')),
    ('be-ad-def', 320, 320,
     lambda t: phrase(t, P('That fat man is living in a white house.', (1, 7)),
                      'Un adjectif dit comment est le nom.')),
    ('be-ad-place', 320, 320,
     lambda t: phrase(t, P('Please give this yellow bag to that old woman.', (3, 7)),
                      'Il se place avant le nom.')),
    ('be-ad-trouver', 320, 320,
     lambda t: phrase(t, P('Many people say that slow water runs deep.', (0, 4)),
                      'Cherche le mot qui décrit le nom.')),
    ('be-ad-plusieurs', 320, 320,
     lambda t: fiche(t, 'Des adjectifs à reconnaître', ['fat, white, yellow, old',
                                                        'slow, many, beautiful',
                                                        'ils décrivent un nom'])),

    # ------------------------------------------------- 2. Comparer
    ('be-cm-couv', 960, 540,
     lambda t: _couv_phrase(t, 'Comparing with adjectives', 'better than French')),
    ('be-cm-er', 320, 320,
     lambda t: fiche(t, 'Les mots courts prennent -er', ['tall devient taller',
                                                         'old devient older',
                                                         'fast devient faster'])),
    ('be-cm-more', 320, 320,
     lambda t: phrase(t, P('Nigeria is the most populated country in Africa.', (3,)),
                      'Les mots longs prennent more ou most.')),
    ('be-cm-good', 320, 320,
     lambda t: fiche(t, 'Trois mots irréguliers', ['good devient better, best',
                                                   'bad devient worse, worst',
                                                   'ils ne prennent pas -er'], vif=(0,))),
    ('be-cm-than', 320, 320,
     lambda t: phrase(t, P('Our teacher speaks English better than French.', (4, 5)),
                      'On compare deux choses avec than.')),

    # ------------------------------------------------- 3. Les relatifs
    ('be-re-couv', 960, 540,
     lambda t: _couv_mots(t, 'Relative pronouns', ['who', 'whom', 'whose', 'which'])),
    ('be-re-who', 320, 320,
     lambda t: phrase(t, P('This is the girl who came here.', (4,)),
                      'who remplace une personne qui fait.')),
    ('be-re-whom', 320, 320,
     lambda t: phrase(t, P('The man with whom I travelled is a soldier.', (3,)),
                      'whom vient après une préposition.')),
    ('be-re-whose', 320, 320,
     lambda t: phrase(t, P('This is the girl whose father came here.', (4,)),
                      'whose dit à qui la chose appartient.')),
    ('be-re-which', 320, 320,
     lambda t: phrase(t, P('Which of the girls is more beautiful?', (0,)),
                      'which choisit dans un groupe connu.')),

    # ------------------------------------------------- 4. Les possessifs
    ('be-po-couv', 960, 540,
     lambda t: _couv_mots(t, 'Possessive pronouns', ['mine', 'yours', 'his', 'theirs'])),
    ('be-po-mine', 320, 320,
     lambda t: phrase(t, P('The books on the table are mine.', (6,)),
                      'mine remplace « my books ».')),
    ('be-po-yours', 320, 320,
     lambda t: phrase(t, P('His case is better than yours.', (5,)),
                      'yours remplace « your case ».')),
    ('be-po-theirs', 320, 320,
     lambda t: phrase(t, P('All class 5 pupils can do theirs.', (6,)),
                      'theirs remplace « their homework ».')),
    ('be-po-sans', 320, 320,
     lambda t: paire(t, [('my book', 'mine'), ('your case', 'yours'),
                         ('their work', 'theirs')],
                     'Le possessif remplace les deux mots')),

    # ------------------------------------- 5. Réfléchis et démonstratifs
    ('be-de-couv', 960, 540,
     lambda t: _couv_mots(t, 'Reflexive and demonstrative',
                          ['myself', 'themselves', 'this', 'those'])),
    ('be-de-reflexive', 320, 320,
     lambda t: phrase(t, P('Nana and Ohoa blamed themselves for the problems.', (4,)),
                      'themselves, et jamais themself.')),
    ('be-de-this', 320, 320,
     lambda t: phrase(t, P('This is my father house.', (0,)),
                      'this pour une seule chose, tout près.')),
    ('be-de-these', 320, 320,
     lambda t: paire(t, [('this', 'these'), ('that', 'those')],
                     'Un seul, et plusieurs', 'À droite, le pluriel.')),
    ('be-de-those', 320, 320,
     lambda t: phrase(t, P('Those boys are not your friends.', (0,)),
                      'those pour plusieurs, plus loin.')),

    # ------------------------------------------------- 6. Les articles
    ('be-ar-couv', 960, 540,
     lambda t: _couv_mots(t, 'A, an, the', ['a', 'an', 'the'])),
    ('be-ar-a', 320, 320,
     lambda t: phrase(t, P('We bought a one way ticket.', (2,)),
                      'a devant un son de consonne.')),
    ('be-ar-an', 320, 320,
     lambda t: phrase(t, P('An oasis is the most fertile place in the desert.', (0,)),
                      'an devant un son de voyelle.')),
    ('be-ar-the', 320, 320,
     lambda t: phrase(t, P('My mother left for the market an hour ago.', (5,)),
                      'the pour une chose déjà connue.')),
    ('be-ar-choisir', 320, 320,
     lambda t: fiche(t, 'On écoute, on ne regarde pas', ['an hour : le h ne se dit pas',
                                                         'a one way ticket : on dit « ouan »',
                                                         'c’est le SON qui décide'], vif=(2,))),

    # ------------------------------------------------- 7. Les contraires
    ('be-an-couv', 960, 540,
     lambda t: _couv_phrase(t, 'Antonyms', 'wet is the opposite of dry')),
    ('be-an-def', 320, 320,
     lambda t: fiche(t, 'Un antonyme', ['c’est le contraire d’un mot',
                                        'wet et dry', 'long et short'])),
    ('be-an-paires1', 320, 320,
     lambda t: paire(t, [('wet', 'dry'), ('light', 'heavy'), ('behind', 'in front of')],
                     'Un mot, son contraire')),
    ('be-an-paires2', 320, 320,
     lambda t: paire(t, [('short', 'long'), ('purchased', 'sold'), ('old', 'new')],
                     'Un mot, son contraire')),
    ('be-an-phrase', 320, 320,
     lambda t: phrase(t, P('A bag of cement is too heavy for me to carry.', (6,)),
                      'Le contraire de light, c’est heavy.')),

    # ------------------------------------------------- 8. Les synonymes
    ('be-sy-couv', 960, 540,
     lambda t: _couv_phrase(t, 'Synonyms', 'blank means empty')),
    ('be-sy-def', 320, 320,
     lambda t: fiche(t, 'Un synonyme', ['c’est un mot de même sens',
                                        'blank et empty', 'silly et foolish'])),
    ('be-sy-paires1', 320, 320,
     lambda t: paire(t, [('blank', 'empty'), ('left', 'abandoned'), ('rushed', 'hurried')],
                     'Un mot, son synonyme')),
    ('be-sy-paires2', 320, 320,
     lambda t: paire(t, [('silly', 'foolish'), ('unite', 'join'), ('wicked', 'cruel')],
                     'Un mot, son synonyme')),
    ('be-sy-phrase', 320, 320,
     lambda t: phrase(t, P('The examiner gave us a blank sheet of paper.', (5,)),
                      'blank veut dire empty.')),

    # ------------------------------------------------- 9. Le paludisme
    ('be-ma-couv', 960, 540,
     lambda t: _couv_phrase(t, 'Malaria', 'caused by a parasite')),
    ('be-ma-cause', 320, 320,
     lambda t: phrase(t, P('Malaria is caused by a parasite.', (2, 5)),
                      'caused by : causé par.')),
    ('be-ma-femelle', 320, 320,
     lambda t: phrase(t, P('Only the female mosquito carries the disease.', (2,)),
                      'Seule la femelle porte la maladie.')),
    ('be-ma-transmission', 320, 320,
     lambda t: fiche(t, 'Les trois gestes du moustique', ['it sucks the blood',
                                                          'it takes in the parasite',
                                                          'it transfers it to another'],
                     vif=(2,))),
    ('be-ma-symptomes', 320, 320,
     lambda t: phrase(t, P('Such a patient feels chilly, feverish and weak.', (3,)),
                      'feels : il se sent.')),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # Chaque sol a sa texture : deux sols dessinés pareil ne se
    # reconnaîtraient pas l-un de l-autre, et c-est tout l-exercice.
    fonds = [v[0] for v in SOLS.values()]
    assert len(set(fonds)) == len(fonds), 'deux sols de la même couleur'

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
            assert fv._hors_bande(t.fini()) == 0, 'couverture %s : dessin hors de la fiche' % cle


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
