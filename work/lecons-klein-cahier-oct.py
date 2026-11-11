# -*- coding: utf-8 -*-
"""
Le cahier du jour de KLEIN (CE1), du 12 au 29 octobre 2026 — cinquante et une
pages photographiées le 11 novembre : dix-huit leçons de français, neuf de
mathématiques, une de géographie, une de langue et culture nationale.

SIX LEÇONS DU CAHIER SONT DÉJÀ DANS L-APP et ne sont pas refaites : les
pronoms personnels, la phrase et ses constituants, le pluriel des noms en ou
et en eu, les nombres de 101 à 999, le cube, les sous-multiples du mètre.

RIEN N-EST AJOUTÉ AU CAHIER : chaque notion reprend une phrase qu-il a copiée,
avec ses exemples. Les pages qui ne portent qu-un renvoi au manuel —
réorganiser une histoire, comparer les nombres, les syllabes ja je ji — ne
font pas de leçon : il n-y a pas de cours à reprendre.

LES QUESTIONS PÈSENT SUR CE QUE LES EXERCICES CORRIGÉS TRAVAILLENT : la forme
négative avec jamais et plus, et la différence entre le TYPE d-une phrase et
sa FORME.

TROIS RÉSERVES, écrites aussi dans les notes de lecture, qui restent hors du
dépôt : une troisième exception au pluriel en au que la photo ne permet pas
de lire ; le nom du cri de la poule ; un mot de la dictée du 2 novembre.
Aucune question ne porte sur ces trois points.

L-outillage est celui du cahier de BRAYNE (work/cahier-outils.py) : même
vérificateur, même paquet.

Usage :  python work/lecons-klein-cahier-oct.py
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
          'work/figures-klein-cahier-oct.py. ')
CLASSE = 'CE1'
ENFANT = 'KLEIN'
MATIERES = (
    ('Français', 'seed-klein-francais-oct.json'),
    ('Mathématiques', 'seed-klein-maths-oct.json'),
    ('Géographie', 'seed-klein-geographie-oct.json'),
    ('Langue et culture nationale', 'seed-klein-langue-oct.json'),
)
PARTIES = [
    'klein-oct-1-grammaire.py',
    'klein-oct-2-conjugaison-orthographe.py',
    'klein-oct-3-vocabulaire-lecture.py',
    'klein-oct-4-maths.py',
    'klein-oct-5-autres.py',
]

LECONS = outils.charger(_ICI, PARTIES)


def verifier():
    return outils.verifier(LECONS, [m for m, _f in MATIERES], '2026-10-')


if __name__ == '__main__':
    images, items, notions, trous = verifier()
    racine = os.path.dirname(_ICI)
    if not os.environ.get('PARTIES_SEULES'):
        for matiere, fichier in MATIERES:
            chemin = os.path.join(racine, 'app', 'public', fichier)
            io.open(chemin, 'w', encoding='utf-8', newline=chr(10)).write(
                json.dumps(outils.paquet(LECONS, matiere, CLASSE, ENFANT, FIGURE), ensure_ascii=False))
            print(chemin)

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for m, titre, chapitre, date, _r, _i, _mots, ns in sorted(LECONS, key=lambda l: (l[0], l[3])):
        print('  %-13s %s  %-50s %d notions  %2d questions'
              % (m[:13], date, titre, len(ns), sum(len(n[5]) for n in ns)))
