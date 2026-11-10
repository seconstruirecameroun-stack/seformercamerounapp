# -*- coding: utf-8 -*-
"""
Les figures des sept leçons de TIC de KLEIN (CE1) — son cahier
d-informatique de septembre à novembre 2026, photographié le 10 novembre.

CE QUI CHANGE PAR RAPPORT AU LOT DE BRAYNE. Les instruments sont les
mêmes — on ne redessine pas un clavier deux fois — mais KLEIN est en CE1 :
les légendes sont plus courtes, et les objets qu-il doit reconnaître sont
ceux de son cahier à lui, en français. Deux objets de plus sont dessinés
ici, parce que son cahier les demande et que celui de BRAYNE ne les avait
pas : le téléphone portable et l-appareil photo.

DEUX SCHÉMAS À ANNOTER. Son cahier pose deux fois le geste : « Voici un
téléphone portable, annote-le » et « On te donne le dessin ci-dessous »
pour la souris. Le type de question existe depuis hier, et les deux
schémas sont dessinés ici avec leurs numéros, comme ceux de BRAYNE : les
repères sont posés À CÔTÉ de la pièce, reliés par un trait, jamais dessus.

Usage :  python work/figures-klein-tic-oct.py
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
fs = _charger('figures_schemas', 'figures-brayne-schemas-nov.py')
fb = _charger('figures_tic_brayne', 'figures-brayne-tic-oct.py')

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

fiche, paire, _legende, _mesure = fr.fiche, fr.paire, fr._legende, fr._mesure
repere = fs.repere
touche, fichier = fb.touche, fb.fichier
GRIS, GRIS_SOMBRE, ECRAN = fb.GRIS, fb.GRIS_SOMBRE, fb.ECRAN


# --------------------------------------------------------------------------
# Les deux objets que le cahier de KLEIN demande en plus

def _telephone(t, cx, cy, l=92, h=156):
    """Un téléphone portable : haut-parleur, écran, clavier, microphone."""
    t.rrect(cx - l / 2, cy - h / 2, cx + l / 2, cy + h / 2, 14,
            fill=INK, bord=INK, trait=2.4)
    # le haut-parleur, une fente en haut
    t.rrect(cx - 15, cy - h / 2 + 10, cx + 15, cy - h / 2 + 16, 3, fill=GRIS)
    # l-écran
    t.rrect(cx - l / 2 + 9, cy - h / 2 + 24, cx + l / 2 - 9, cy + 6, 4, fill=ECRAN)
    # le clavier, trois rangées de trois touches
    for rang in range(3):
        for col in range(3):
            x = cx - 30 + col * 21
            y = cy + 16 + rang * 17
            t.rrect(x, y, x + 15, y + 12, 2.5, fill=WHITE_WARM, bord=GRIS, trait=1)
    # le microphone, un petit rond en bas
    t.disque((cx, cy + h / 2 - 11), 4.5, fill=GRIS)


def _photo(t, cx, cy):
    """Un appareil photo : un boîtier, un objectif, un déclencheur."""
    t.rrect(cx - 52, cy - 26, cx + 52, cy + 32, 9, fill=GRIS, bord=INK, trait=2.4)
    t.rrect(cx - 24, cy - 38, cx + 6, cy - 26, 4, fill=GRIS, bord=INK, trait=2.2)
    t.disque((cx - 4, cy + 4), 22, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.disque((cx - 4, cy + 4), 12, fill=ECRAN, bord=INK, trait=1.8)
    t.disque((cx + 32, cy - 10), 6, fill=CLAY, bord=INK, trait=1.8)


def _unite(t, cx, cy):
    """L-unité centrale : la tour, avec son bouton et ses fentes."""
    t.rrect(cx - 30, cy - 52, cx + 30, cy + 52, 7, fill=GRIS, bord=INK, trait=2.4)
    t.disque((cx, cy - 36), 6, fill=MINT, bord=INK, trait=1.8)
    for i in range(3):
        t.rrect(cx - 20, cy - 14 + i * 16, cx + 20, cy - 8 + i * 16, 2,
                fill=WHITE_WARM, bord=INK_2, trait=1.2)


OBJETS = dict(fb.OBJETS)
OBJETS.update({'telephone': _telephone, 'photo': _photo, 'unite': _unite})
DECALAGE = dict(fb.DECALAGE)
DECALAGE.update({'telephone': 6, 'photo': 2, 'unite': 0})


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
# Les deux schémas à annoter

PHONE = ('le haut-parleur', 'l’écran', 'le clavier', 'le microphone')


def phone_schema(t):
    cx, cy = 128, 160
    _telephone(t, cx, cy, 96, 180)
    repere(t, 1, (250, 86), (cx + 44, 86))
    repere(t, 2, (252, 132), (cx + 46, 132))
    repere(t, 3, (250, 196), (cx + 46, 196))
    repere(t, 4, (246, 244), (cx + 6, 242))


SOURIS = ('le clic gauche', 'le clic droit', 'la molette', 'le boîtier', 'le câble')


def souris_schema(t):
    cx, cy = 148, 172
    # Le câble, qui sort par le haut.
    t.ligne([(cx, cy - 56), (cx, cy - 86), (cx + 34, cy - 104)], INK, 3)
    # Le boîtier.
    t.rrect(cx - 40, cy - 56, cx + 40, cy + 58, 38, fill=WHITE_WARM, bord=INK, trait=2.6)
    # Les deux boutons et la molette.
    t.ligne([(cx, cy - 56), (cx, cy - 10)], INK, 2.2)
    t.ligne([(cx - 40, cy - 10), (cx + 40, cy - 10)], INK, 2.2)
    t.rrect(cx - 5, cy - 46, cx + 5, cy - 24, 5, fill=GRIS, bord=INK, trait=1.8)

    # Le repère du câble vise le CÂBLE, et non le haut du boîtier : au
    # premier jet son point tombait à côté de la molette, et le numéro 5
    # désignait donc la même chose que le numéro 3.
    repere(t, 1, (46, 150), (cx - 22, cy - 40))
    repere(t, 2, (254, 150), (cx + 22, cy - 40))
    repere(t, 3, (250, 92), (cx + 5, cy - 35))
    repere(t, 4, (254, 228), (cx + 36, cy + 26))
    repere(t, 5, (56, 62), (cx + 10, cy - 94))


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
    larg = min(210, 840 / max(1, len(mots)))
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
    # ------------------------------------------- 1. Le système informatique
    ('kt-sy-couv', 960, 540,
     lambda t: _couv_mots(t, 'Le système informatique', ['matériel', 'logiciel'])),
    ('kt-sy-def', 320, 320,
     lambda t: fiche(t, 'Le système informatique', ['tout le matériel informatique',
                                                    'qui sert à traiter',
                                                    'les informations'])),
    ('kt-sy-deux', 320, 320,
     lambda t: paire(t, [('le matériel', 'hardware'), ('le logiciel', 'software')],
                     'Deux parties, deux noms')),
    ('kt-sy-materiel', 320, 320,
     lambda t: appareils(t, [('clavier', 'le clavier'), ('unite', 'l’unité centrale')],
                         'La partie matérielle', 'Ce qu’on touche.')),
    ('kt-sy-logiciel', 320, 320,
     lambda t: fiche(t, 'La partie logicielle', ['le logiciel application', 'l’antivirus',
                                                 'internet', 'le fichier'])),
    ('kt-sy-classer', 320, 320,
     lambda t: paire(t, [('la souris', 'matériel'), ('l’antivirus', 'logiciel'),
                         ('l’écran', 'matériel aussi')], 'Ranger dans la bonne case')),

    # ------------------------------------------- 2. Les précautions
    ('kt-pr-couv', 960, 540,
     lambda t: _couv_mots(t, 'Les précautions', ['pas au volant', 'mains sèches',
                                                 'écran doux'])),
    ('kt-pr-branche', 320, 320,
     lambda t: fiche(t, 'Pas quand il est branché', ['le téléphone se charge',
                                                     'on ne s’en sert pas',
                                                     'on attend'], vif=(1,))),
    ('kt-pr-volant', 320, 320,
     lambda t: fiche(t, 'Deux endroits interdits', ['au volant, en conduisant',
                                                    'dans une station-service'])),
    ('kt-pr-mains', 320, 320,
     lambda t: fiche(t, 'Jamais les mains mouillées', ['l’eau et l’électricité',
                                                       'ne vont pas ensemble',
                                                       'on s’essuie d’abord'], vif=(2,))),
    ('kt-pr-ecrans', 320, 320,
     lambda t: fiche(t, 'Les yeux aussi', ['j’évite les écrans', 'trop lumineux'])),

    # ------------------------------------------- 3. Les outils TIC
    ('kt-ou-couv', 960, 540,
     lambda t: _couv_objets(t, 'Les fonctions des outils TIC',
                            ['ecran', 'photo', 'radio', 'telephone'])),
    ('kt-ou-ordinateur', 320, 320,
     lambda t: appareils(t, [('ecran', 'l’ordinateur')], 'Il traite les informations',
                         'Et il le fait tout seul.')),
    ('kt-ou-photo', 320, 320,
     lambda t: appareils(t, [('photo', 'l’appareil photo')], 'Il capture les images',
                         'La caméra, elle, fait des vidéos.')),
    ('kt-ou-tele', 320, 320,
     lambda t: paire(t, [('le téléviseur', 'en images'), ('la radio', 'en audio')],
                     'Deux façons d’informer')),
    ('kt-ou-telephone', 320, 320, lambda t: phone_schema(t)),
    ('kt-ou-traditionnels', 320, 320,
     lambda t: paire(t, [('le gong', 'traditionnel'), ('le tambour', 'traditionnel aussi'),
                         ('le téléphone', 'moderne')], 'Anciens et modernes')),

    # ------------------------------------------- 4. Les fonctions de l-ordinateur
    ('kt-fo-couv', 960, 540,
     lambda t: _couv_mots(t, 'Les fonctions de l’ordinateur',
                          ['saisir', 'traiter', 'stocker', 'afficher'])),
    ('kt-fo-saisir', 320, 320,
     lambda t: appareils(t, [('clavier', 'le clavier')], '1. Saisir l’information',
                         'On entre le texte.')),
    ('kt-fo-traiter', 320, 320,
     lambda t: appareils(t, [('unite', 'l’unité centrale')], '2. Traiter l’information',
                         'Elle fait le travail.')),
    ('kt-fo-stocker', 320, 320,
     lambda t: appareils(t, [('cle', 'la mémoire')], '3. Stocker l’information',
                         'Elle la garde.')),
    ('kt-fo-afficher', 320, 320,
     lambda t: appareils(t, [('ecran', 'l’écran')], '4. Afficher les résultats',
                         'On voit la réponse.')),
    ('kt-fo-autres', 320, 320,
     lambda t: fiche(t, 'Il sert aussi à', ['calculer', 'faire des recherches',
                                            'communiquer'])),

    # ------------------------------------------- 5. Le clavier
    ('kt-cl-couv', 960, 540,
     lambda t: _couv_mots(t, 'Le clavier de l’ordinateur', ['AZERTY', 'QWERTY'])),
    ('kt-cl-entree', 320, 320,
     lambda t: appareils(t, [('clavier', 'le clavier')], 'Un périphérique d’entrée',
                         'Le texte entre par lui.')),
    ('kt-cl-azerty', 320, 320,
     lambda t: paire(t, [('AZERTY', 'le français'), ('QWERTY', 'l’anglais')],
                     'Deux types de clavier')),
    ('kt-cl-paves', 320, 320,
     lambda t: paire(t, [('le pavé numérique', 'les chiffres'),
                         ('le pavé alphanumérique', 'les lettres')],
                     'Deux pavés')),
    ('kt-cl-touches', 320, 320,
     lambda t: fiche(t, 'Et aussi', ['les touches de fonctions',
                                     'la barre d’espacement'])),

    # ------------------------------------------- 6. La souris
    ('kt-so-couv', 960, 540,
     lambda t: _couv_objets(t, 'La souris de l’ordinateur', ['souris'])),
    ('kt-so-schema', 320, 320, lambda t: souris_schema(t)),
    ('kt-so-cliquer', 320, 320,
     lambda t: fiche(t, 'Cliquer', ['on appuie une fois', 'sur le clic gauche'], vif=(1,))),
    ('kt-so-double', 320, 320,
     lambda t: fiche(t, 'Double-cliquer', ['on appuie deux fois', 'très vite',
                                           'pour ouvrir'], vif=(2,))),
    ('kt-so-molette', 320, 320,
     lambda t: fiche(t, 'Ce qu’elle ne fait pas', ['elle ne tourne pas',
                                                   'elle ne souligne pas'])),

    # ------------------------------------------- 7. Les sources crédibles
    ('kt-sc-couv', 960, 540,
     lambda t: _couv_mots(t, 'Les sources crédibles', ['exactes', 'vérifiées', 'étayées'])),
    ('kt-sc-def', 320, 320,
     lambda t: fiche(t, 'Une source crédible', ['on peut lui faire confiance',
                                                'ses informations sont exactes',
                                                'vérifiées et étayées'])),
    ('kt-sc-medias', 320, 320,
     lambda t: appareils(t, [('radio', 'la radio'), ('ecran', 'la télévision')],
                         'Les médias officiels', 'Et la presse écrite.')),
    ('kt-sc-gouvernement', 320, 320,
     lambda t: fiche(t, 'Les sites du gouvernement', ['ils disent ce que fait l’État',
                                                      'et ils le vérifient'])),
    ('kt-sc-enligne', 320, 320,
     lambda t: fiche(t, 'En ligne aussi', ['les encyclopédies', 'les sites web éducatifs'])),
    ('kt-sc-pasfiable', 320, 320,
     lambda t: fiche(t, 'Ce qui n’est pas crédible', ['les débats de la rue',
                                                      'la boutique du quartier',
                                                      'les réseaux sociaux'])),
]


def controler():
    """Ce que la figure montre doit être ce que la leçon dit."""
    cles = [c for c, _w, _h, _f in FIGURES]
    assert len(set(cles)) == len(cles), 'clé en double'

    # Les deux schémas numérotés : autant de repères que de noms.
    assert len(PHONE) == 4 and len(set(PHONE)) == 4, PHONE
    assert len(SOURIS) == 5 and len(set(SOURIS)) == 5, SOURIS

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
    print('  kt-ou-telephone  ' + ' / '.join('%d %s' % (i + 1, n) for i, n in enumerate(PHONE)))
    print('  kt-so-schema     ' + ' / '.join('%d %s' % (i + 1, n) for i, n in enumerate(SOURIS)))
