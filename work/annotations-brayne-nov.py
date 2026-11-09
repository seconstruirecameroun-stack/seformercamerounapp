# -*- coding: utf-8 -*-
"""
Les trois schémas à annoter de la révision du 9 novembre 2026 — BRAYNE, CM1.

CE QUE CE FICHIER AJOUTE. Le tableau demande deux fois « annote le schéma
ci-dessous », et une troisième fois « complète le schéma » pour le cycle de
l-eau. Aucun type de question ne savait poser ce geste ; il existe
désormais - voir la migration 20261109180000_type_annotation.sql et
app/src/lib/annotation.ts - et ce fichier pose les trois questions.

Elles ne font pas de leçon neuve : elles s-accrochent aux notions qui
portent déjà la matière.

  la lampe à pétrole      sur la notion des cinq parties essentielles. Les
                          cinq noms du schéma sont EXACTEMENT les cinq de
                          la notion, ni un de plus ni un de moins
  le cycle de l-eau       sur la notion du cycle. Les quatre mots du schéma
                          sont ceux que le tableau donne à placer
  l-appareil de la femme  sur une notion NEUVE, parce que le schéma montre
                          deux parties que sa leçon ne nommait pas : la
                          trompe et le col. Poser une question sur un mot
                          qu-aucune notion n-enseigne, ce serait demander
                          ce qu-on n-a pas dit

L-ORDRE DES NUMÉROS VIENT DU DESSIN, et de nulle part ailleurs. Il est
recopié ici depuis figures-brayne-schemas-nov.py, et le contrôle du bas
vérifie que les deux listes sont identiques, mot pour mot : un numéro qui
désignerait autre chose dans l-image que dans la question ferait rater une
question sue.

Usage :  python work/annotations-brayne-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Schéma composé, non généré, dessiné par '
          'work/figures-brayne-schemas-nov.py. ')

CLASSE = 'CM1'
ENFANT = 'BRAYNE'
TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

LAM = 'La lampe à pétrole'
CYC = 'Le cycle de l’eau dans la nature'
ORG = 'Les organes reproducteurs'

# Les notions visées, relevées en base le 9 novembre 2026.
EN_BASE = {
    LAM: 'Elle a cinq parties essentielles : le réservoir, la molette, la mèche, le verre et la '
         'grille d’aération.',
    CYC: 'Le cycle de l’eau est le trajet que parcourt l’eau pour revenir à son point de départ.',
}

# Les noms, DANS L-ORDRE DES NUMÉROS DU DESSIN. Le contrôle les compare aux
# listes du script de figures.
NOMS = {
    'br-la-schema': ('la grille d’aération', 'le verre', 'la mèche', 'la molette',
                     'le réservoir'),
    'br-or-schema': ('la trompe', 'l’ovaire', 'l’utérus', 'le col de l’utérus', 'le vagin'),
    'br-cy-schema': ('l’évaporation', 'la condensation', 'le ruissellement', 'l’infiltration'),
}


def annotation(figure, question, niveau=3):
    """La question d-annotation : les noms sont donnés dans l-ordre du dessin.

    `ordre` est l-identité, et c-est voulu : les étiquettes SONT rangées
    dans l-ordre des numéros, et c-est l-application qui les mélange avant
    de les montrer. Les écrire déjà mêlées ici rendrait le fichier
    illisible et la relecture impossible.
    """
    noms = list(NOMS[figure])
    return ('annotation', niveau,
            {'question': question, 'figure': figure, 'etiquettes': noms},
            {'ordre': list(range(len(noms)))},
            'Les numéros vont du haut vers le bas du dessin.')


AJOUTS = [
    (LAM, EN_BASE[LAM], [
        annotation('br-la-schema', 'Annote le schéma de la lampe à pétrole.'),
    ]),
    (CYC, EN_BASE[CYC], [
        annotation('br-cy-schema', 'Complète le schéma du cycle de l’eau.'),
    ]),
]

NOTIONS_NEUVES = [
    (ORG, 5, 'relation',
     'Les deux trompes conduisent l’ovule de l’ovaire jusqu’à l’utérus, et le col est l’entrée '
     'de l’utérus, juste au-dessus du vagin.',
     'br-or-schema',
     'Le schéma de l’appareil de la femme, avec ses cinq repères numérotés.',
     [('simple', 'De haut en bas : l’ovaire, la trompe, l’utérus, le col, le vagin.'),
      ('pas_a_pas', 'L’ovule part de l’ovaire, passe par la trompe, et arrive dans l’utérus.')],
     [('qcm', 1, {'question': 'Qu’est-ce qui conduit l’ovule jusqu’à l’utérus ?',
                  'options': ['La trompe', 'Le col', 'Le vagin']},
       {'index': 0}, 'La trompe.'),
      ('vrai_faux', 1, {'statement': 'Le col est l’entrée de l’utérus.'},
       {'value': True}, 'Oui, juste au-dessus du vagin.'),
      ('texte_a_trous', 2,
       {'text': 'L’ovule part de l’ovaire et passe par la {{1}}.', 'blanks': 1},
       {'values': ['trompe']}, 'Par la trompe.'),
      annotation('br-or-schema', 'Annote l’appareil reproducteur de la femme.'),
      ('vrai_faux', 4, {'statement': 'L’ovule passe d’abord par le vagin avant l’utérus.'},
       {'value': False}, 'Non. Il vient de l’ovaire, par la trompe.')]),
]


def verifier_items(items, exiger_quatre_etapes):
    niveaux = set()
    for ikind, niveau, payload, answer, explain in items:
        niveaux.add(niveau)
        textes = json.dumps([payload, answer, explain], ensure_ascii=False)
        assert "'" not in textes, 'apostrophe droite interdite : ' + textes
        if niveau == 4:
            assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
        if ikind == 'annotation':
            # Les mêmes règles que le garde du composant, écrites ici pour
            # qu-une question fautive ne parte jamais en base.
            assert isinstance(payload['question'], str) and payload['question'].strip()
            fig = payload['figure']
            assert all(c.islower() or c.isdigit() or c == '-' for c in fig), fig
            etiquettes = payload['etiquettes']
            assert 2 <= len(etiquettes) <= 8, payload
            assert len(set(etiquettes)) == len(etiquettes), payload
            assert all(e.strip() for e in etiquettes), payload
            assert sorted(answer['ordre']) == list(range(len(etiquettes))), answer
        elif ikind == 'qcm':
            assert len(payload['question']) <= 90, payload
            options = payload['options']
            assert 2 <= len(options) <= 4 and len(set(options)) == len(options), payload
            assert 0 <= answer['index'] < len(options), payload
            for o in options:
                assert len(o) <= 70, o
            bonne = len(options[answer['index']])
            autres = [len(o) for k, o in enumerate(options) if k != answer['index']]
            assert bonne <= max(autres) * 2, payload['question']
        elif ikind == 'vrai_faux':
            assert isinstance(answer['value'], bool), payload
            assert len(payload['statement']) <= 110, payload
        elif ikind == 'texte_a_trous':
            n = payload['text'].count('{{')
            assert n == len(answer['values']) == payload['blanks'], payload
            for v in answer['values']:
                assert set(v) <= TAPABLE, 'réponse non tapable au clavier : ' + v
        else:
            raise AssertionError('type non jouable ici : ' + ikind)
    if exiger_quatre_etapes:
        assert niveaux == {1, 2, 3, 4}, 'étapes manquantes : %s' % sorted(niveaux)
    return len(items)


def verifier():
    # Le dessin fait foi : les noms de ce fichier doivent être EXACTEMENT
    # ceux que le script de figures numérote, dans le même ordre.
    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-brayne-schemas-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessines = {cle: noms for cle, _w, _h, _f, noms in fig.FIGURES}
    assert set(dessines) == set(NOMS), 'les schémas dessinés et ceux posés ne coïncident pas'
    for cle, noms in NOMS.items():
        assert tuple(noms) == tuple(dessines[cle]), \
            'les numéros de %s ne désignent pas la même chose dans le dessin et dans la question' \
            % cle

    total = 0
    for lecon, notion, items in AJOUTS:
        assert lecon in EN_BASE and EN_BASE[lecon] == notion, 'notion mal recopiée : ' + notion
        total += verifier_items(items, False)
    images = set()
    for lecon, rang, kind, phrase, img, prompt, expl, items in NOTIONS_NEUVES:
        assert kind in ('definition', 'date', 'liste', 'relation'), kind
        assert len(phrase) <= 180, 'notion trop longue (%d)' % len(phrase)
        assert img in NOMS, 'le schéma de la notion neuve n’est pas un schéma numéroté : ' + img
        images.add(img)
        for registre, corps in expl:
            assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), registre
            assert len(corps) <= 200, corps
        total += verifier_items(items, True)
    return total, len(images)


def paquet():
    return {
        'classe': CLASSE, 'enfant': ENFANT,
        'ajouts': [
            {'lecon': lecon, 'notion': notion,
             'items': [{'kind': ik, 'level': lv, 'payload': pl, 'answer': an, 'explain': ex}
                       for ik, lv, pl, an, ex in items]}
            for lecon, notion, items in AJOUTS
        ],
        'notions_neuves': [
            {'lecon': lecon, 'sort_order': rang, 'kind': kind, 'statement': phrase,
             'illustration': img, 'illustration_prompt': FIGURE + prompt,
             'explanations': [{'register': r, 'body': b} for r, b in expl],
             'items': [{'kind': ik, 'level': lv, 'payload': pl, 'answer': an, 'explain': ex}
                       for ik, lv, pl, an, ex in items]}
            for lecon, rang, kind, phrase, img, prompt, expl, items in NOTIONS_NEUVES
        ],
    }


if __name__ == '__main__':
    total, images = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-annotations-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d questions dont 3 annotations - %d notion neuve - %d schémas'
          % (total, len(NOTIONS_NEUVES), len(NOMS)))
    for cle, noms in NOMS.items():
        print('  %-14s %s' % (cle, ' / '.join('%d %s' % (i + 1, n) for i, n in enumerate(noms))))
    print(chemin)
