# -*- coding: utf-8 -*-
"""
Les trois films d'Unit 13 — Wood work and building, pour KLEIN (CE1).

Premiers films d'anglais, et premiers films qui ne sont pas dits par Céline.
La règle est écrite dans docs/charte-films.md : **la voix suit la langue de
la leçon**. L'objectif affiché de l'unité est « spell and pronounce words
dealing with wood work and building » — un enfant qui entend trowel, chisel
et two hundred and fifty-one prononcés avec un accent français apprend une
prononciation fausse dans le film même qui prétend la lui enseigner.

La direction de narration, elle, ne bouge pas : narrateur éducatif, diction
nette, débit posé, parole immédiate. C'est le ton qui fait la collection, pas
le timbre.

Le film des métiers est bâti autour de la faute. KLEIN a échangé builder et
carpenter dans son cahier d'exercices ; le film ne récite donc pas les trois
définitions à la file, il les **oppose**. Trois plans posent chacun un énoncé
exact de l'Exercise 13 E et allument le bon métier parmi les trois. La
réponse se montre au lieu de se dire.

Usage :  python work/films-klein-anglais.py
"""

import io
import json
import os

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')
SCENES = ('metier', 'tri', 'outils', 'chisel', 'adjectif', 'sansphrase',
          'capitale', 'nombre', 'trait', 'suite')
MOTS_MAX = 16

FILMS = [
    (
        'metiers', 'Builder, carpenter and carver', 'Builder, carpenter and carver',
        'Three men work with their hands, and each one has his own tool.',
        [
            ('A builder builds houses with bricks and cement.',
             {'scene': 'metier', 'metier': 'builder', 'outil': 'trowel'},
             ['BUILDER'], 'content'),
            ('A carpenter makes tables, chairs and doors out of wood.',
             {'scene': 'metier', 'metier': 'carpenter', 'outil': 'saw'},
             ['CARPENTER'], 'content'),
            ('A wood carver carves wood to make a mortar.',
             {'scene': 'metier', 'metier': 'carver', 'outil': 'gouge'},
             ['CARVER'], 'content'),
            ('He arranges blocks to make a wall. He is a builder.',
             {'scene': 'tri', 'enonce': 'He arranges blocks to make a wall.',
              'metier': 'builder', 'note': 'blocks and walls'},
             ['WHO IS HE?'], 'encourage'),
            ('He makes tables out of wood. He is a carpenter.',
             {'scene': 'tri', 'enonce': 'He makes tables out of wood.',
              'metier': 'carpenter', 'note': 'wood and furniture'},
             ['WHO IS HE?'], 'encourage'),
            ('He uses a trowel. He is a builder.',
             {'scene': 'tri', 'enonce': 'He uses a trowel.',
              'metier': 'builder', 'note': 'the trowel spreads cement'},
             ['WHO IS HE?'], 'encourage'),
            ('Both the carpenter and the carver use a chisel.',
             {'scene': 'chisel'},
             ['THE CHISEL'], 'fete'),
        ],
    ),
    (
        'adjectifs', 'Kinds of adjectives', 'Kinds of adjectives',
        'One word describes another, and sometimes it keeps a capital letter.',
        [
            ('An adjective is a word that describes a noun.',
             {'scene': 'adjectif', 'mots': ['a', 'sharp', 'trowel'], 'adjectif': 1,
              'note': 'sharp describes the trowel'},
             ['ADJECTIVE'], 'content'),
            ('Heavier is not a sentence. The hammer is heavy — that is a sentence.',
             {'scene': 'sansphrase', 'faux': 'heavier',
              'vrais': ['The', 'hammer', 'is', 'heavy.']},
             ['A SENTENCE'], 'encourage'),
            ('Common adjectives take no capital letter.',
             {'scene': 'capitale', 'mot': 'old', 'nom': 'carpenter', 'propre': False,
              'note': 'common — no capital'},
             ['COMMON'], 'content'),
            ('Proper adjectives come from places, and they keep their capital letter.',
             {'scene': 'capitale', 'mot': 'cameroonian', 'nom': 'carpenter',
              'propre': True, 'note': 'proper — from Cameroon'},
             ['PROPER'], 'fete'),
        ],
    ),
    (
        'nombres', 'Numbers 251 to 300', 'Numbers 251 to 300',
        'Three figures, a few words, and one small line that joins them.',
        [
            ('We read two hundred and fifty-one.',
             {'scene': 'nombre', 'chiffres': ['2', '5', '1'],
              'mots': ['two', 'hundred', 'and', 'fifty-one']},
             ['251'], 'content'),
            ('A hyphen joins the tens and the units.',
             {'scene': 'trait', 'gauche': 'fifty', 'droite': 'one',
              'note': 'never “fifty one”'},
             ['THE HYPHEN'], 'encourage'),
            ('After two hundred and ninety-nine comes three hundred.',
             {'scene': 'suite', 'nombres': ['298', '299', '300'],
              'note': 'three hundred, with no “and”'},
             ['UP TO 300'], 'fete'),
        ],
    ),
]


def verifier():
    plans = 0
    for cle, titre, lecon, fil, blocs in FILMS:
        for voix, scene, mots, humeur in blocs:
            plans += 1
            assert "'" not in voix, 'apostrophe droite : ' + voix
            assert len(voix.split()) <= MOTS_MAX, 'phrase trop longue : ' + voix
            assert scene['scene'] in SCENES, scene['scene']
            assert humeur in HUMEURS, humeur
            assert len(mots) <= 2, mots
            for m in mots:
                assert len(m) <= 18 and m == m.upper(), m
            if scene['scene'] in ('metier', 'tri'):
                assert scene['metier'] in ('builder', 'carpenter', 'carver'), scene
            if scene['scene'] == 'adjectif':
                assert 0 <= scene['adjectif'] < len(scene['mots']), scene
            if scene['scene'] == 'capitale':
                # Un adjectif propre sans majuscule à montrer n’aurait rien à
                # enseigner : la scène met en valeur la PREMIÈRE lettre.
                assert scene['mot'] and scene['mot'][0].isalpha(), scene
            if scene['scene'] == 'nombre':
                assert len(scene['chiffres']) == 3, scene
    # Le film des métiers doit rejouer les énoncés exacts de l’exercice raté,
    # sinon il ne sert pas à ce pour quoi il est fait.
    tris = [b[1] for b in dict((f[0], f[4]) for f in FILMS)['metiers']
            if b[1]['scene'] == 'tri']
    assert len(tris) == 3, tris
    assert [s['metier'] for s in tris] == ['builder', 'carpenter', 'builder'], tris
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, lecon, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-en-' + cle)
        os.makedirs(dossier, exist_ok=True)

        manifeste = {
            'title': titre, 'lesson': lecon, 'registre': 'anglais',
            'style': 'Figures dessinées et Fredoka sur fond pastel, composé',
            'aspect_ratio': '16:9', 'language': 'en',
            'narrator': 'voix anglaise — la voix suit la langue de la leçon',
            'mascotte': 'Niba', 'through_line': fil,
            'blocks': [
                {'n': i + 1, 'vo_line': v, 'scene': s, 'keywords': k, 'niba': h}
                for i, (v, s, k, h) in enumerate(blocs)
            ],
        }
        io.open(os.path.join(dossier, 'script_manifest.json'), 'w',
                encoding='utf-8', newline='\n').write(
            json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n')

        md = ['# %s — script verrouillé' % titre, '',
              'Leçon : %s (CE1, anglais)' % lecon,
              'Registre : anglais. Rien n’est généré, tout est dessiné.',
              'Voix : anglaise. La voix suit la langue de la leçon — voir la charte.', '',
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
        print('  video-en-%-10s %d plans  %s' % (cle, len(blocs), titre))
