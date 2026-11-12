# -*- coding: utf-8 -*-
"""
Le cahier de sciences humaines de KLEIN (CE1, en français) et son cahier en
anglais (social studies, science, ICT), octobre 2026 — trente-huit pages
photographiées le 12 novembre.

LE PÈRE A DIT : FAIRE LE MÊME TRAVAIL QUE POUR BRAYNE — garder ce qui existe,
compléter avec ce qui manque. L-obéissance, le droit à l-identité,
l-intégration nationale, le filtrage de l-eau, la paix et le sol sont déjà en
base : ils ne sont ni réécrits ni doublés. La révision corrigée du
1er octobre n-est pas reprise.

DEUX LANGUES, DONC DEUX SORTES DE PAQUETS. Une même matière (l-histoire,
l-éducation civique, les sciences) reçoit ici des leçons en français et des
leçons en anglais ; chaque paquet porte une seule langue, et le script
d-insertion les écrit l-un après l-autre.

RIEN N-EST AJOUTÉ AU CAHIER. Ce qui ne se lit pas sûrement n-est pas posé ;
chaque partie dit quoi en tête. Les notes de lecture restent hors du dépôt.

Usage :  python work/lecons-klein-cahier-nov12.py
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
          'work/figures-klein-cahier-nov12.py. ')
CLASSE = 'CE1'
ENFANT = 'KLEIN'

# (partie, langue)
PARTIES = [
    ('klein-nov12-1-francais.py', 'fr'),
    ('klein-nov12-2-social.py', 'en'),
    ('klein-nov12-3-science.py', 'en'),
]

# Le cahier ne date pas ces leçons : la date ne sert qu-à l-ordre.
SANS_DATE = {'Les saisons et les végétaux'}

PAR_LANGUE = {}
for _partie, _langue in PARTIES:
    PAR_LANGUE.setdefault(_langue, []).extend(outils.charger(_ICI, [_partie]))
LECONS = [l for ls in PAR_LANGUE.values() for l in ls]

MATIERES = sorted({l[0] for l in LECONS})


def _fichier(matiere, langue):
    nom = (matiere.lower().replace('é', 'e').replace('è', 'e').replace(' ', '-'))
    return 'seed-klein-%s-%s-nov12.json' % (nom, langue)


def paquets():
    """La liste (matière, fichier, paquet), une par matière et par langue."""
    sortie = []
    for langue, lecons in sorted(PAR_LANGUE.items()):
        for matiere in sorted({l[0] for l in lecons}):
            p = outils.paquet(lecons, matiere, CLASSE, ENFANT, FIGURE, langue)
            for lecon in p['lecons']:
                if lecon['title'] in SANS_DATE:
                    lecon['taught_on'] = None
            sortie.append((matiere, _fichier(matiere, langue), p))
    return sortie


def verifier():
    return outils.verifier(LECONS, MATIERES, '2026-10-')


if __name__ == '__main__':
    images, items, notions, trous = verifier()
    racine = os.path.dirname(_ICI)
    for matiere, fichier, p in paquets():
        chemin = os.path.join(racine, 'app', 'public', fichier)
        io.open(chemin, 'w', encoding='utf-8', newline=chr(10)).write(
            json.dumps(p, ensure_ascii=False))
        print("  ['%s', '/%s']," % (matiere, fichier))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for m, titre, chapitre, date, _r, _i, _mots, ns in sorted(LECONS, key=lambda l: (l[0], l[3])):
        print('  %-24s %s  %-52s %d notions  %2d questions'
              % (m, date, titre, len(ns), sum(len(n[5]) for n in ns)))
