# -*- coding: utf-8 -*-
"""
Les trois films des leçons de français de KLEIN (CE1).

Premiers films du registre typographique, décrit dans docs/charte-films.md :
quand la matière est la langue, il n'y a rien à photographier, et c'est la
langue elle-même qu'on met en mouvement. « Maman » se soulève, « Elle » prend
sa place ; un « s » glisse à la fin du mot, un « x » le remplace quand la
règle l'exige.

Aucune image n'est générée. Tout est composé par work/motion-texte.py, en
Fredoka, la police de l'application. Le film ne coûte donc que sa voix, se
corrige au mot près, et ne peut pas se tromper d'orthographe — ce qui serait
le comble pour une leçon de français.

Chaque plan déclare une scène typographique et ses paramètres. Le moteur de
rendu ne connaît que ces quelques verbes :

  phrase      les mots d'une phrase entrent un par un
  remplace    un mot se soulève, un autre prend sa place
  rangement   des mots en désordre se rangent en ligne
  bornes      la première lettre grandit, un point tombe à la fin
  blocs       la phrase se sépare en deux groupes de couleurs
  liste       des mots apparaissent l'un après l'autre, en grille
  suffixe     un mot au singulier, puis sa lettre de pluriel qui arrive

Usage :  python work/films-klein-francais.py
"""

import io
import json
import os

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')
SCENES = ('phrase', 'remplace', 'rangement', 'bornes', 'blocs', 'liste', 'suffixe')

# (clé, titre, leçon, fil conducteur, [(voix, scène, mots affichés, humeur)])
FILMS = [
    (
        'pronoms', 'Les pronoms personnels', 'Les pronoms personnels',
        'Un nom s’en va, un petit mot prend sa place.',
        [
            ('Le pronom est un mot qui remplace le nom.',
             {'scene': 'remplace', 'mots': ['Maman', 'va', 'au', 'champ'],
              'remplacer': 0, 'par': 'Elle'},
             ['LE PRONOM'], 'content'),
            ('Maman va au champ devient elle va au champ.',
             {'scene': 'phrase', 'mots': ['Elle', 'va', 'au', 'champ'], 'accent': 0},
             ['ELLE'], 'content'),
            ('Les pronoms personnels sont je, tu, il, elle, nous, vous, ils, elles.',
             {'scene': 'liste', 'mots': ['je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles'],
              'colonnes': 4},
             ['HUIT PRONOMS'], 'fete'),
        ],
    ),
    (
        'phrase', 'La phrase et ses constituants', 'La phrase et ses constituants',
        'Des mots en tas deviennent une phrase, puis se laissent couper en deux.',
        [
            ('La phrase est un ensemble de mots qui a un sens.',
             {'scene': 'rangement', 'mots': ['Les', 'femmes', 'travaillent', 'la', 'terre']},
             ['UN SENS'], 'content'),
            ('La phrase commence par une lettre majuscule et se termine par un point.',
             {'scene': 'bornes', 'mots': ['Les', 'femmes', 'travaillent', 'la', 'terre']},
             ['MAJUSCULE', 'POINT'], 'encourage'),
            ('La phrase a deux constituants : le groupe nominal et le groupe verbal.',
             {'scene': 'blocs', 'mots': ['Les', 'femmes', 'travaillent', 'la', 'terre'],
              'coupure': 2},
             ['GN', 'GV'], 'content'),
            ('Dans cette phrase, le groupe nominal est les femmes.',
             {'scene': 'blocs', 'mots': ['Les', 'femmes', 'travaillent', 'la', 'terre'],
              'coupure': 2, 'souligner': 0},
             ['LE GN'], 'fete'),
        ],
    ),
    (
        'pluriel', 'Le pluriel des noms en ou et en eu', 'Le pluriel des noms en ou et en eu',
        'Une lettre arrive à la fin du mot. Reste à savoir laquelle.',
        [
            ('Les noms terminés par ou prennent un s au pluriel.',
             {'scene': 'suffixe', 'singulier': 'un trou', 'pluriel': 'des trou',
              'lettre': 's'},
             ['OU PREND S'], 'content'),
            ('Six noms en ou prennent un x : bijou, caillou, chou, joujou, genou, pou.',
             {'scene': 'liste', 'mots': ['bijoux', 'cailloux', 'choux', 'joujoux', 'genoux', 'poux'],
              'colonnes': 3, 'accent_final': True},
             ['SIX EXCEPTIONS'], 'encourage'),
            ('Les noms terminés par eu prennent un x au pluriel.',
             {'scene': 'suffixe', 'singulier': 'un feu', 'pluriel': 'des feu',
              'lettre': 'x'},
             ['EU PREND X'], 'content'),
            ('Trois noms en eu prennent un s : pneu, bleu, émeu.',
             {'scene': 'liste', 'mots': ['pneus', 'bleus', 'émeus'], 'colonnes': 3,
              'accent_final': True},
             ['TROIS EXCEPTIONS'], 'fete'),
        ],
    ),
]


def verifier():
    plans = 0
    for cle, titre, lecon, fil, blocs in FILMS:
        for voix, scene, mots, humeur in blocs:
            plans += 1
            assert "'" not in voix, 'apostrophe droite : ' + voix
            assert len(voix.split()) <= 14, 'phrase trop longue pour un CE1 : ' + voix
            assert scene['scene'] in SCENES, scene['scene']
            assert humeur in HUMEURS, humeur
            assert len(mots) <= 2, mots
            for m in mots:
                assert len(m) <= 18 and m == m.upper(), m
            if scene['scene'] == 'remplace':
                assert 0 <= scene['remplacer'] < len(scene['mots'])
            if scene['scene'] == 'blocs':
                assert 0 < scene['coupure'] < len(scene['mots'])
            if scene['scene'] == 'suffixe':
                assert scene['lettre'] in ('s', 'x')
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, lecon, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-' + cle)
        os.makedirs(dossier, exist_ok=True)

        manifeste = {
            'title': titre, 'lesson': lecon, 'registre': 'typographique',
            'style': 'Fredoka sur fond pastel, composé', 'aspect_ratio': '16:9',
            'language': 'fr', 'narrator': 'Céline', 'mascotte': 'Niba',
            'through_line': fil,
            'blocks': [
                {'n': i + 1, 'vo_line': v, 'scene': s, 'keywords': k, 'niba': h}
                for i, (v, s, k, h) in enumerate(blocs)
            ],
        }
        io.open(os.path.join(dossier, 'script_manifest.json'), 'w',
                encoding='utf-8', newline='\n').write(
            json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n')

        md = ['# %s — script verrouillé' % titre, '',
              'Leçon : %s (CE1)' % lecon,
              'Registre : typographique. Rien n’est généré, tout est composé.',
              'Voix : Céline, articulation claire, débit posé.', '',
              'Fil conducteur : %s' % fil, '', '## Narration', '']
        md += ['%d. %s' % (i + 1, v) for i, (v, _, _, _) in enumerate(blocs)]
        md += ['', '## Ce qui bouge à l’écran', '']
        md += ['%d. %s — %s' % (i + 1, s['scene'],
                                json.dumps({k: v for k, v in s.items() if k != 'scene'},
                                           ensure_ascii=False))
               for i, (_, s, _, _) in enumerate(blocs)]
        md += ['', '## Mots affichés', '']
        md += ['%d. %s' % (i + 1, ' · '.join(k)) for i, (_, _, k, _) in enumerate(blocs)]
        md += ['', '## Humeur de Niba', '']
        md += ['%d. %s' % (i + 1, h) for i, (_, _, _, h) in enumerate(blocs)]
        io.open(os.path.join(dossier, 'script.md'), 'w',
                encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')


if __name__ == '__main__':
    plans = verifier()
    ecrire()
    print('%d films - %d plans - 0 image generee' % (len(FILMS), plans))
    for cle, titre, _l, _f, blocs in FILMS:
        print('  video-%-10s %d plans  %s' % (cle, len(blocs), titre))
