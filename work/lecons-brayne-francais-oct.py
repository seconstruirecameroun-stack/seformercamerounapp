# -*- coding: utf-8 -*-
"""
Le cahier du jour de BRAYNE (CM1), du 2 au 29 octobre 2026 — soixante-dix-sept
pages photographiées le 11 novembre : vingt-cinq leçons de français et cinq de
TIC.

RIEN N-EST AJOUTÉ AU CAHIER : chaque notion reprend une phrase qu-il a copiée,
avec ses exemples.

DEUX LEÇONS SONT ÉCRITES DEPUIS DES DEVOIRS CORRIGÉS, et pas depuis une page
de cours : l-infinitif et les groupes de verbes, puis en TIC les
périphériques, la saisie kilométrique et l-ENIAC. Ces cours datent de
septembre et n-ont pas été photographiés ; les corrections de la maîtresse
donnent les réponses. Ces deux leçons ne disent rien que la copie corrigée ne
dise.

LES QUESTIONS PÈSENT SUR LES CONFUSIONS QUE LES EXERCICES TRAVAILLENT : le
passé simple contre le passé composé, « on n- » devant « rien », les
homonymes, les périphériques de stockage contre ceux d-entrée.

LES NOTES DE LECTURE DU CAHIER NE SONT PAS DANS LE DÉPÔT. Elles contiennent
les copies de l-enfant et restent sur la machine du parent.

UNE SEULE SOURCE POUR LES QUESTIONS ET POUR LES IMAGES. Chaque notion porte
ici la description de sa fiche ; work/figures-brayne-francais-oct.py la
dessine depuis ce même fichier. Une image ne peut donc pas dire autre chose
que la leçon.

Le rang écrit dans le paquet n-est qu-un ordre : le script d-insertion le
recale après le dernier rang de la classe, qu-il lit en base.

Usage :  python work/lecons-brayne-francais-oct.py
"""

import importlib.util
import io
import json
import os

_ICI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('cahier_outils', os.path.join(_ICI, 'cahier-outils.py'))
outils = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(outils)

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-francais-oct.py. ')
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
MATIERES = (('Français', 'seed-brayne-francais-oct.json'), ('TIC', 'seed-brayne-tic-oct.json'))
PARTIES = [
    'brayne-fr-oct-1-conjugaison.py',
    'brayne-fr-oct-2-grammaire.py',
    'brayne-fr-oct-3-orthographe.py',
    'brayne-fr-oct-4-vocabulaire-ecrits.py',
    'brayne-fr-oct-5-tic.py',
]

LECONS = outils.charger(_ICI, PARTIES)


def verifier():
    return outils.verifier(LECONS, [m for m, _f in MATIERES], '2026-10-')


if __name__ == '__main__':
    images, items, notions, trous = verifier()
    racine = os.path.dirname(_ICI)
    for matiere, fichier in MATIERES:
        chemin = os.path.join(racine, 'app', 'public', fichier)
        io.open(chemin, 'w', encoding='utf-8', newline=chr(10)).write(
            json.dumps(outils.paquet(LECONS, matiere, CLASSE, ENFANT, FIGURE), ensure_ascii=False))
        print(chemin)

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for m, titre, chapitre, date, _r, _i, _mots, ns in sorted(LECONS, key=lambda l: (l[0], l[3])):
        print('  %-9s %s  %-52s %d notions  %2d questions'
              % (m, date, titre, len(ns), sum(len(n[5]) for n in ns)))
