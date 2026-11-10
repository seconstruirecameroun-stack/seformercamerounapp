# -*- coding: utf-8 -*-
"""
Les figures des cinq leçons d-ICT de KLEIN (CE1) — son cahier d-anglais
informatique, cinq pages du 8 septembre au 20 octobre 2026.

POURQUOI UN FICHIER DE PLUS, APRÈS CELUI DE SA TIC FRANÇAISE. Son école
enseigne la même matière dans les deux langues, et les deux cahiers
existent. Les figures de la TIC française ne peuvent pas servir ici : leur
script est contrôlé par ses leçons à lui, qui refuse toute figure dessinée
et jamais utilisée. Les instruments, eux, sont importés - on ne redessine
pas une radio deux fois.

DEUX OBJETS DE PLUS, parce que ce cahier-ci les demande et que les autres
ne les avaient pas : la CLOCHE et le SIFFLET. Ce sont les deux outils
locaux dont la leçon du 22 septembre donne l-usage, et un enfant de CE1
doit pouvoir les reconnaître sans lire.

Usage :  python work/figures-klein-ict-oct.py
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
fr = _charger('figures_revision', 'figures-brayne-revision-nov.py')
fk = _charger('figures_tic_klein', 'figures-klein-tic-oct.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

fiche, paire, _legende, _mesure = fr.fiche, fr.paire, fr._legende, fr._mesure
BOIS = (168, 122, 86)
LAITON = (206, 166, 86)


# --------------------------------------------------------------------------
# Les deux objets que ce cahier-ci demande

def _cloche(t, cx, cy):
    """Une cloche : la robe, le battant, l-anse."""
    t.poly([(cx - 40, cy + 30), (cx - 30, cy - 16), (cx - 14, cy - 34),
            (cx + 14, cy - 34), (cx + 30, cy - 16), (cx + 40, cy + 30)],
           fill=LAITON, bord=INK, trait=2.6)
    t.rrect(cx - 44, cy + 28, cx + 44, cy + 40, 5, fill=LAITON, bord=INK, trait=2.4)
    t.disque((cx, cy + 50), 8, fill=LAITON, bord=INK, trait=2.4)
    t.d.arc([(cx - 12) * S, (cy - 50) * S, (cx + 12) * S, (cy - 26) * S], 180, 360,
            fill=INK, width=int(2.6 * S))


def _sifflet(t, cx, cy):
    """Un sifflet d-arbitre : l-embouchure, la chambre ronde, le trou, l-anneau.

    Le premier jet était un simple cylindre : il ne se reconnaissait pas.
    Un sifflet se reconnaît à trois choses - le bec plat qu-on met en
    bouche, la chambre ronde qui résonne, et l-anneau du cordon.
    """
    # L-embouchure, plate et large.
    t.rrect(cx - 58, cy - 11, cx - 6, cy + 11, 5, fill=GRIS_CLAIR, bord=INK, trait=2.4)
    # La chambre ronde.
    t.disque((cx + 6, cy), 26, fill=GRIS_CLAIR, bord=INK, trait=2.6)
    # Le trou d-air, sur le dessus, juste après le bec.
    t.poly([(cx - 36, cy - 11), (cx - 22, cy - 11), (cx - 29, cy - 23)],
           fill=INK, bord=INK, trait=1.6)
    # L-anneau du cordon.
    t.d.ellipse([(cx + 28) * S, (cy - 12) * S, (cx + 48) * S, (cy + 8) * S],
                outline=INK, width=int(2.6 * S))


GRIS_CLAIR = (214, 216, 214)

OBJETS = dict(fk.OBJETS)
OBJETS.update({'cloche': _cloche, 'sifflet': _sifflet})
DECALAGE = dict(fk.DECALAGE)
DECALAGE.update({'cloche': -6, 'sifflet': 0})


def appareils(t, noms, titre=None, legende=None):
    """Un ou deux objets, dessinés au trait, avec leur nom dessous."""
    if titre:
        _legende(t, 58, titre, 17, INK)
    places = [(160, 152)] if len(noms) == 1 else [(90, 152), (230, 152)]
    for (cx, cy), (cle, etiquette) in zip(places, noms):
        OBJETS[cle](t, cx, cy + DECALAGE.get(cle, 0))
        _legende(t, 244, etiquette, 15, INK, large=132, cx=cx)
    if legende:
        _legende(t, 274, legende, 15)


# --------------------------------------------------------------------------
# Les couvertures

def _bandeau(t, titre):
    taille = 26
    while _mesure(t, titre, taille) > 700 and taille > 15:
        taille -= 1
    w = _mesure(t, titre, taille) + 56
    t.rrect(480 - w / 2, 192, 480 + w / 2, 232, 20, fill=GOLD, bord=INK, trait=2)
    t.texte((480, 212), titre, taille, INK)


def _couv_mots(t, titre, mots):
    _bandeau(t, titre)
    larg = min(220, 840 / max(1, len(mots)))
    depart = 480 - larg * len(mots) / 2
    for i, m in enumerate(mots):
        x = depart + larg * i
        t.rrect(x + 6, 262, x + larg - 6, 326, 10, fill=WHITE_WARM, bord=INK, trait=2)
        taille = 19
        while _mesure(t, m, taille) > larg - 24 and taille > 11:
            taille -= 1
        t.texte((x + larg / 2, 294), m, taille, INK)


def _couv_objets(t, titre, noms):
    _bandeau(t, titre)
    larg = 800 / len(noms)
    for i, cle in enumerate(noms):
        OBJETS[cle](t, 480 - larg * (len(noms) - 1) / 2 + larg * i,
                    296 + DECALAGE.get(cle, 0))


FIGURES = [
    # ------------------------------------------- 1. ICT equipment
    ('ki-eq-couv', 960, 540,
     lambda t: _couv_objets(t, 'ICT equipment', ['tambour', 'radio', 'ecran'])),
    ('ki-eq-ict', 320, 320,
     lambda t: fiche(t, 'I.C.T means', ['Information and', 'Communication', 'Technology'],
                     vif=(0, 1, 2))),
    ('ki-eq-deux', 320, 320,
     lambda t: paire(t, [('local tools', 'the old ones'), ('modern tools', 'the new ones')],
                     'Two types of equipment')),
    ('ki-eq-locaux', 320, 320,
     lambda t: fiche(t, 'Local tools', ['the gong, the flute', 'the whistle, the trumpet',
                                        'the xylophone, the mvet'])),
    ('ki-eq-modernes', 320, 320,
     lambda t: appareils(t, [('radio', 'the radio'), ('ecran', 'the computer')],
                         'Modern tools', 'The television, the camera, the phone too.')),

    # ------------------------------------------- 2. Uses of local ICT tools
    ('ki-us-couv', 960, 540,
     lambda t: _couv_objets(t, 'Uses of local ICT tools', ['cloche', 'sifflet', 'tambour'])),
    ('ki-us-cloche', 320, 320,
     lambda t: appareils(t, [('cloche', 'the bell')], 'The bell tells the time',
                         'It rings, and the lesson begins.')),
    ('ki-us-sifflet', 320, 320,
     lambda t: appareils(t, [('sifflet', 'the whistle')], 'The whistle',
                         'For sports and games, and to control traffic.')),
    ('ki-us-tambour', 320, 320,
     lambda t: appareils(t, [('tambour', 'the talking drum')], 'The drum and the gong',
                         'They make an announcement.')),

    # ------------------------------------------- 3. Local and modern
    ('ki-di-couv', 960, 540,
     lambda t: _couv_mots(t, 'Local and modern tools', ['distance', 'place', 'electricity'])),
    ('ki-di-distance', 320, 320,
     lambda t: paire(t, [('local', 'short distances'), ('modern', 'long distances')],
                     'How far the message goes')),
    ('ki-di-lieu', 320, 320,
     lambda t: paire(t, [('local', 'in villages'), ('modern', 'in towns')],
                     'Where they are used')),
    ('ki-di-electronique', 320, 320,
     lambda t: paire(t, [('the xylophone', 'non-electronic'), ('the radio', 'electronic')],
                     'With or without electricity')),

    # ------------------------------------------- 4. The telephone
    ('ki-te-couv', 960, 540,
     lambda t: _couv_objets(t, 'The telephone', ['telephone'])),
    ('ki-te-def', 320, 320,
     lambda t: appareils(t, [('telephone', 'the telephone')], 'Two types',
                         'The fixed one, and the mobile one.')),
    ('ki-te-appels', 320, 320,
     lambda t: fiche(t, 'It is used for', ['making calls', 'sending messages',
                                           'receiving messages'])),
    ('ki-te-musique', 320, 320,
     lambda t: fiche(t, 'And also for', ['calculating', 'playing music',
                                         'listening to music'])),
    ('ki-te-photos', 320, 320,
     lambda t: fiche(t, 'And for', ['research', 'watching movies',
                                    'snapping pictures', 'playing games'])),

    # ------------------------------------------- 5. The computer
    ('ki-co-couv', 960, 540,
     lambda t: _couv_objets(t, 'The computer and its uses', ['ecran', 'unite'])),
    ('ki-co-def', 320, 320,
     lambda t: fiche(t, 'An electronic device', ['it processes information',
                                                 'it stores information',
                                                 'it sends information'])),
    ('ki-co-ecole', 320, 320,
     lambda t: fiche(t, 'In school, it is used to', ['register pupils', 'process exams',
                                                     'do research', 'help pupils to learn'])),
    ('ki-co-aide', 320, 320,
     lambda t: paire(t, [('to entertain', 'watching movies'),
                         ('in business', 'to calculate salaries')], 'It also helps')),
    ('ki-co-hopital', 320, 320,
     lambda t: fiche(t, 'In hospitals', ['to store patients records',
                                         'to schedule doctors', 'and nurses'])),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

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
        t.fini().save(chemin, 'WEBP', quality=74, method=6)
        total += os.path.getsize(chemin)
    print('%d figures - %.1f Ko - 0 credit' % (len(FIGURES), total / 1024))
