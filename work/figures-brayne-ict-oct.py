# -*- coding: utf-8 -*-
"""
Les figures des neuf leçons d-informatique de BRAYNE (CM1) — son cahier de
TIC d-octobre 2026, treize pages photographiées le 9 novembre au soir.

CE QUE CES LEÇONS DEMANDENT DE MONTRER. Elles portent sur des OBJETS qu-il
a sous les yeux - un clavier, un écran, une clé USB - et sur des MOTS
écrits sur ces objets : Ctrl, Caps Lock, la barre d-espace. Les deux se
dessinent, et doivent se dessiner : un enfant qui a vu la touche Ctrl la
reconnaît sur le clavier de la salle, ce qu-une liste de mots ne donne
pas.

Quatre instruments, et les cinquante figures en sortent :

  touche       une touche de clavier, avec son nom gravé dessus et son
               relief. C-est l-instrument des six notions de frappe
  appareil     les objets du cahier, dessinés au trait : écran, clavier,
               souris, imprimante, clé USB, tambour, radio. Aucun n-est
               décoratif - chacun est la réponse d-une question
  fichier      la fiche d-un fichier avec son extension en gros, parce que
               c-est l-extension qu-on lui demandera, et non l-icône
  fiche/paire  repris de figures-brayne-revision-nov.py, pour les listes
               et les appariements

Usage :  python work/figures-brayne-ict-oct.py
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

Toile, SORTIE, S = fm.Toile, fm.SORTIE, fm.S
INK, INK_2 = fm.INK, fm.INK_2
WHITE_WARM, SAND, CLAY = fm.WHITE_WARM, fm.SAND, fm.CLAY
GOLD, MINT, LILAC, SKY, BLEU = fm.GOLD, fm.MINT, fm.LILAC, fm.SKY, fm.BLEU

fiche, paire, _legende, _mesure = fr.fiche, fr.paire, fr._legende, fr._mesure

GRIS = (198, 200, 198)
GRIS_SOMBRE = (142, 146, 146)
ECRAN = (96, 126, 142)
BOIS = (168, 122, 86)
BANDEAU = (184, 356)


# --------------------------------------------------------------------------
# La touche de clavier

def touche(t, nom, legende=None, titre=None, cx=160, cy=146, larg=150, haut=86, taille=26):
    """Une touche, avec le relief qui la fait reconnaître pour une touche."""
    if titre:
        _legende(t, 62, titre, 17, INK)
    t.rrect(cx - larg / 2, cy - haut / 2 + 7, cx + larg / 2, cy + haut / 2 + 7, 12,
            fill=GRIS_SOMBRE, bord=INK, trait=2.4)
    t.rrect(cx - larg / 2, cy - haut / 2, cx + larg / 2, cy + haut / 2, 12,
            fill=WHITE_WARM, bord=INK, trait=2.4)
    while _mesure(t, nom, taille) > larg - 22 and taille > 10:
        taille -= 1
    t.texte((cx, cy), nom, taille, INK)
    if legende:
        _legende(t, cy + haut / 2 + 46, legende, 16, INK)


def deux_touches(t, a, b, titre=None, legende=None):
    """Deux touches côte à côte : une touche et celle qu-on lui confond."""
    if titre:
        _legende(t, 56, titre, 17, INK)
    touche(t, a, None, None, cx=88, cy=136, larg=126, haut=72, taille=20)
    touche(t, b, None, None, cx=232, cy=136, larg=126, haut=72, taille=20)
    if legende:
        _legende(t, 232, legende, 16, INK)


# --------------------------------------------------------------------------
# Les objets du cahier

def _ecran(t, cx, cy, l=120, h=84):
    t.rrect(cx - l / 2, cy - h / 2, cx + l / 2, cy + h / 2, 8, fill=INK, bord=INK, trait=2.4)
    t.rrect(cx - l / 2 + 7, cy - h / 2 + 7, cx + l / 2 - 7, cy + h / 2 - 7, 4, fill=ECRAN)
    t.rrect(cx - 11, cy + h / 2, cx + 11, cy + h / 2 + 16, 3, fill=GRIS, bord=INK, trait=2)
    t.rrect(cx - 34, cy + h / 2 + 16, cx + 34, cy + h / 2 + 24, 4, fill=GRIS, bord=INK, trait=2)


def _clavier(t, cx, cy, l=150, h=52):
    t.rrect(cx - l / 2, cy - h / 2, cx + l / 2, cy + h / 2, 8, fill=GRIS, bord=INK, trait=2.4)
    for rang in range(3):
        for col in range(9):
            x = cx - l / 2 + 10 + col * (l - 20) / 9
            y = cy - h / 2 + 9 + rang * (h - 18) / 3
            t.rrect(x, y, x + (l - 20) / 9 - 3, y + (h - 18) / 3 - 3, 2,
                    fill=WHITE_WARM, bord=INK_2, trait=1)


def _souris(t, cx, cy):
    t.rrect(cx - 22, cy - 30, cx + 22, cy + 30, 21, fill=WHITE_WARM, bord=INK, trait=2.4)
    t.ligne([(cx, cy - 30), (cx, cy - 6)], INK, 2)
    t.ligne([(cx - 22, cy - 6), (cx + 22, cy - 6)], INK, 2)


def _imprimante(t, cx, cy):
    t.rrect(cx - 46, cy - 10, cx + 46, cy + 30, 8, fill=GRIS, bord=INK, trait=2.4)
    t.rrect(cx - 30, cy - 44, cx + 30, cy - 10, 4, fill=WHITE_WARM, bord=INK, trait=2.2)
    t.rrect(cx - 34, cy + 14, cx + 34, cy + 44, 4, fill=WHITE_WARM, bord=INK, trait=2.2)
    for i in range(3):
        t.ligne([(cx - 24, cy + 24 + i * 7), (cx + 24, cy + 24 + i * 7)], INK_2, 1.6)


def _cle_usb(t, cx, cy):
    t.rrect(cx - 54, cy - 18, cx + 26, cy + 18, 6, fill=LILAC, bord=INK, trait=2.4)
    t.rrect(cx + 26, cy - 11, cx + 56, cy + 11, 3, fill=GRIS, bord=INK, trait=2.2)
    t.rrect(cx + 32, cy - 6, cx + 44, cy + 6, 2, fill=WHITE_WARM, bord=INK_2, trait=1.4)
    t.disque((cx - 40, cy), 4.5, fill=WHITE_WARM, bord=INK, trait=1.6)


def _tambour(t, cx, cy):
    t.poly([(cx - 34, cy - 30), (cx + 34, cy - 30), (cx + 24, cy + 34), (cx - 24, cy + 34)],
           fill=BOIS, bord=INK, trait=2.4)
    t.d.ellipse([(cx - 34) * S, (cy - 42) * S, (cx + 34) * S, (cy - 18) * S],
                fill=SAND, outline=INK, width=int(2.4 * S))
    for i in range(-2, 3):
        t.ligne([(cx + i * 13, cy - 26), (cx + i * 10, cy + 30)], INK_2, 1.6)


def _radio(t, cx, cy):
    t.rrect(cx - 54, cy - 32, cx + 54, cy + 32, 8, fill=SAND, bord=INK, trait=2.4)
    t.disque((cx - 24, cy + 2), 20, fill=WHITE_WARM, bord=INK, trait=2.2)
    for r in (7, 13):
        t.disque((cx - 24, cy + 2), r, bord=INK_2, trait=1.4)
    for i in range(3):
        t.rrect(cx + 10, cy - 18 + i * 14, cx + 44, cy - 10 + i * 14, 3,
                fill=WHITE_WARM, bord=INK_2, trait=1.4)
    t.ligne([(cx + 36, cy - 32), (cx + 56, cy - 58)], INK, 2.4)
    t.disque((cx + 56, cy - 58), 3.5, fill=INK)


OBJETS = {
    'ecran': _ecran, 'clavier': lambda t, x, y: _clavier(t, x, y),
    'souris': _souris, 'imprimante': _imprimante, 'cle': _cle_usb,
    'tambour': _tambour, 'radio': _radio,
}


DECALAGE = {'ecran': -16, 'imprimante': -6, 'radio': -4}


def appareils(t, noms, titre=None, legende=None):
    """Un ou deux objets du cahier, dessinés au trait, avec leur nom."""
    if titre:
        _legende(t, 58, titre, 17, INK)
    places = [(160, 148)] if len(noms) == 1 else [(90, 148), (230, 148)]
    for (cx, cy), (cle, etiquette) in zip(places, noms):
        # L-écran descend plus bas que les autres objets : son pied et son
        # socle prennent 24 pixels de plus, et le nom « the monitor » tombait
        # dessus. Chaque objet porte donc son décalage propre.
        OBJETS[cle](t, cx, cy + DECALAGE.get(cle, 0))
        _legende(t, 212, etiquette, 15, INK, large=132, cx=cx)
    if legende:
        _legende(t, 250, legende, 16, INK)


# --------------------------------------------------------------------------
# La fiche d-un fichier

def fichier(t, nom, extension, legende=None, titre=None):
    """Un fichier et son extension, qui est ce qu-on lui demandera."""
    if titre:
        _legende(t, 58, titre, 17, INK)
    cx, cy = 160, 150
    corne = 26
    t.poly([(cx - 62, cy - 62), (cx + 62 - corne, cy - 62), (cx + 62, cy - 62 + corne),
            (cx + 62, cy + 62), (cx - 62, cy + 62)], fill=WHITE_WARM, bord=INK, trait=2.6)
    t.poly([(cx + 62 - corne, cy - 62), (cx + 62 - corne, cy - 62 + corne),
            (cx + 62, cy - 62 + corne)], fill=SAND, bord=INK, trait=2)
    _legende(t, cy - 16, nom, 15, INK_2, large=104)
    t.rrect(cx - 50, cy + 2, cx + 50, cy + 44, 8, fill=GOLD, bord=INK, trait=2.2)
    taille = 24
    while _mesure(t, extension, taille) > 88 and taille > 12:
        taille -= 1
    t.texte((cx, cy + 23), extension, taille, INK)
    if legende:
        _legende(t, 244, legende, 16, INK)


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
    larg = min(200, 840 / max(1, len(mots)))
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
    larg = 820 / len(noms)
    for i, cle in enumerate(noms):
        OBJETS[cle](t, 480 - larg * (len(noms) - 1) / 2 + larg * i,
                    292 + DECALAGE.get(cle, 0))


def _couv_touche(t, titre, nom):
    _bandeau(t, titre)
    t.rrect(380, 266, 580, 334, 12, fill=GRIS_SOMBRE, bord=INK, trait=2.4)
    t.rrect(380, 258, 580, 326, 12, fill=WHITE_WARM, bord=INK, trait=2.4)
    taille = 26
    while _mesure(t, nom, taille) > 170 and taille > 12:
        taille -= 1
    t.texte((480, 292), nom, taille, INK)


FIGURES = [
    # -------------------------------------------------- 1. Les périphériques
    ('bt-pe-couv', 960, 540, lambda t: _couv_objets(t, 'Computer peripherals',
                                                    ['clavier', 'ecran', 'imprimante', 'cle'])),
    ('bt-pe-trois', 320, 320,
     lambda t: fiche(t, 'Three types', ['input: data goes IN',
                                        'output: information goes OUT',
                                        'storage: it is kept'])),
    ('bt-pe-entree', 320, 320,
     lambda t: appareils(t, [('clavier', 'the keyboard'), ('souris', 'the mouse')],
                         'Input peripherals', 'They send data into the computer.')),
    ('bt-pe-sortie', 320, 320,
     lambda t: appareils(t, [('ecran', 'the monitor'), ('imprimante', 'the printer')],
                         'Output peripherals', 'They send information out.')),
    ('bt-pe-stockage', 320, 320,
     lambda t: appareils(t, [('cle', 'the USB key')], 'Storage peripherals',
                         'It keeps the information.')),

    # -------------------------------------------------- 2. Les abréviations
    ('bt-ab-couv', 960, 540, lambda t: _couv_mots(t, 'RAM, ROM, USB, ICT',
                                                  ['RAM', 'ROM', 'USB', 'ICT'])),
    ('bt-ab-ram', 320, 320,
     lambda t: fiche(t, 'RAM', ['Random', 'Access', 'Memory'], vif=(0, 1, 2))),
    ('bt-ab-rom', 320, 320,
     lambda t: fiche(t, 'ROM', ['Read', 'Only', 'Memory'], vif=(0, 1, 2))),
    ('bt-ab-usb', 320, 320,
     lambda t: fiche(t, 'USB', ['Universal', 'Serial', 'Bus'], vif=(0, 1, 2))),
    ('bt-ab-ict', 320, 320,
     lambda t: fiche(t, 'ICT', ['Information and', 'Communication', 'Technology'],
                     vif=(0, 1, 2))),

    # -------------------------------------------- 3. Outils locaux et modernes
    ('bt-lo-couv', 960, 540, lambda t: _couv_objets(t, 'Local and modern ICT tools',
                                                    ['tambour', 'radio', 'ecran'])),
    ('bt-lo-locaux', 320, 320,
     lambda t: appareils(t, [('tambour', 'the drum')], 'Local tools',
                         'The flute, the bell, the gong too.')),
    ('bt-lo-modernes', 320, 320,
     lambda t: appareils(t, [('radio', 'the radio')], 'Modern tools',
                         'The computer, the phone, the camera too.')),
    ('bt-lo-usages', 320, 320,
     lambda t: paire(t, [('the radio', 'to hear'), ('the television', 'to see'),
                         ('the whistle', 'to begin')], 'What each one is for')),

    # -------------------------------------------------- 4. Les premières machines
    ('bt-pr-couv', 960, 540, lambda t: _couv_mots(t, 'The first computers',
                                                  ['the abacus', 'the Pascaline', '1642'])),
    ('bt-pr-anciens', 320, 320,
     lambda t: fiche(t, 'The earliest computers', ['the abacus', 'the Pascaline'], vif=(0, 1))),
    ('bt-pr-pascal', 320, 320,
     lambda t: fiche(t, 'The Pascaline', ['invented by Pascal', 'in the year 1642'], vif=(1,))),
    ('bt-pr-abaque', 320, 320,
     lambda t: paire(t, [('the abacus', 'counts with beads'),
                         ('the Pascaline', 'adds with wheels')], 'Two machines, two gestures')),

    # -------------------------------------------------- 5. La sécurité
    ('bt-se-couv', 960, 540,
     lambda t: _couv_mots(t, 'Security measures', ['clean', 'dry hands', 'switch off',
                                                   'antivirus'])),
    ('bt-se-def', 320, 320,
     lambda t: fiche(t, 'Why these measures', ['the tools are well maintained',
                                               'they remain secured', 'they last longer'])),
    ('bt-se-chiffon', 320, 320,
     lambda t: fiche(t, 'To clean them', ['a dry piece of cloth', 'and a clean one',
                                          'never a wet rag'], vif=(2,))),
    ('bt-se-manger', 320, 320,
     lambda t: fiche(t, 'Never while working', ['do not eat on them', 'do not drink on them',
                                                'no wet hands'])),
    ('bt-se-eteindre', 320, 320,
     lambda t: fiche(t, 'After use', ['always switch them off'], vif=(0,))),
    ('bt-se-antivirus', 320, 320,
     lambda t: fiche(t, 'Against the virus', ['install an antivirus',
                                              'it protects the computer'], vif=(0,))),
    ('bt-se-station', 320, 320,
     lambda t: fiche(t, 'Two more from the exercise', ['no water on ICT tools',
                                                       'no phone in a petrol station'])),

    # -------------------------------------------------- 6. Les fichiers
    ('bt-fi-couv', 960, 540, lambda t: _couv_mots(t, 'Files and their extensions',
                                                  ['Doc', 'JPG', 'MP3', 'MP4'])),
    ('bt-fi-def', 320, 320,
     lambda t: fiche(t, 'What a file is', ['a collection of related data',
                                           'saved with a name',
                                           'and a three-letter extension'], vif=(2,))),
    ('bt-fi-texte', 320, 320,
     lambda t: fichier(t, 'my text', 'Doc', 'A text typed and saved.', 'Textual file')),
    ('bt-fi-image', 320, 320,
     lambda t: fichier(t, 'my photo', 'JPG', 'A drawing or a photograph.', 'Image file')),
    ('bt-fi-audio', 320, 320,
     lambda t: fichier(t, 'my song', 'MP3', 'A sound or a voice recorded.', 'Audio file')),
    ('bt-fi-video', 320, 320,
     lambda t: fichier(t, 'my film', 'MP4', 'A video saved in the computer.', 'Video file')),
    ('bt-fi-logiciels', 320, 320,
     lambda t: paire(t, [('Word', 'Doc'), ('Excel', 'XLS'), ('Access', 'MDB')],
                     'Each programme, its extension')),

    # -------------------------------------------------- 7. Créer et enregistrer
    ('bt-cr-couv', 960, 540, lambda t: _couv_mots(t, 'Creating and saving a file',
                                                  ['Start menu', 'all programmes', 'Save as'])),
    ('bt-cr-texte', 320, 320,
     lambda t: fiche(t, 'To create a text file', ['1. the Start menu', '2. all programmes',
                                                  '3. Microsoft Word', '4. type, then save'])),
    ('bt-cr-image', 320, 320,
     lambda t: fiche(t, 'To create an image file', ['1. the Start menu', '2. all programmes',
                                                    '3. Microsoft PowerPoint',
                                                    '4. draw, then save'])),
    ('bt-cr-enregistrer', 320, 320,
     lambda t: fiche(t, 'To save it', ['1. File, on the menu bar', '2. click Save as',
                                       '3. type a name', '4. click Save'])),
    ('bt-cr-nom', 320, 320,
     lambda t: fichier(t, 'lesson 1', 'Doc', 'An appropriate name, and its extension.',
                       'The name you give it')),

    # -------------------------------------------------- 8. La frappe
    ('bt-ty-couv', 960, 540, lambda t: _couv_touche(t, 'Typing: the keys', 'Caps Lock')),
    ('bt-ty-def', 320, 320,
     lambda t: appareils(t, [('clavier', 'the keyboard')], 'What typing is',
                         'Using the keyboard to enter data.')),
    ('bt-ty-caps', 320, 320,
     lambda t: touche(t, 'Caps Lock', 'It changes small letters into capitals.')),
    ('bt-ty-backspace', 320, 320,
     lambda t: touche(t, 'Backspace', 'It erases a word wrongly written.')),
    ('bt-ty-espace', 320, 320,
     lambda t: deux_touches(t, 'Space bar', 'Shift', 'Two different keys',
                            'The space bar separates words.')),
    ('bt-ty-entree', 320, 320,
     lambda t: touche(t, 'Enter', 'It moves to a new line.')),
    ('bt-ty-ctrl', 320, 320,
     lambda t: paire(t, [('Ctrl + C', 'to copy'), ('Ctrl + V', 'to paste'),
                         ('Ctrl + S', 'to save'), ('Ctrl + P', 'to print')],
                     'The control key')),
    ('bt-ty-fleches', 320, 320,
     lambda t: touche(t, 'Direction', 'Left, right, upward or downward.')),

    # -------------------------------------------------- 9. L-édition
    ('bt-ed-couv', 960, 540, lambda t: _couv_mots(t, 'Editing', ['font size', 'borders',
                                                                 'alignment'])),
    ('bt-ed-def', 320, 320,
     lambda t: fiche(t, 'What editing is', ['checking a written work', 'correcting it',
                                            'to make it easy to understand'])),
    ('bt-ed-liste1', 320, 320,
     lambda t: fiche(t, 'Things to do', ['the font size', 'the page setting', 'the borders',
                                         'the background'])),
    ('bt-ed-liste2', 320, 320,
     lambda t: fiche(t, 'And three more', ['the text alignment', 'the capitalisation',
                                           'the calligraphy'])),
    ('bt-ed-surligner', 320, 320,
     lambda t: fiche(t, 'Before anything else', ['the words must be highlighted',
                                                 'otherwise nothing changes'], vif=(0,))),
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
