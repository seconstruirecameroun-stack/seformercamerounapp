# -*- coding: utf-8 -*-
"""
Les scripts des deux films des leçons de BRAYNE (CM1).

Même chaîne que les six films de KLEIN, mais calibrée pour un CM1 : les
phrases peuvent porter deux informations au lieu d'une, et les mots affichés
peuvent être des noms propres — à dix ans on lit « BÉNOUÉ » sans buter.

Règle tenue : ce qui est dit est montré. Quand la voix nomme la Sanaga, le
fleuve qui s'élargit vers l'océan est à l'image au moment où le mot tombe.

Usage :  python work/films-brayne.py
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, cinematic wide shot, '
    'no text, no letters, no numbers, no watermark, no real person, no brand, no map. '
)

FILMS = [
    (
        'bassins', 'Les bassins hydrographiques du Cameroun',
        'On remonte un fleuve : d’abord l’eau, puis les régions qu’elle traverse.',
        [
            ('L’hydrographie, c’est l’ensemble des cours d’eau d’une région.',
             'Many small blue streams running across a wide green plain, seen from high above, morning light.',
             ['HYDROGRAPHIE']),
            ('Un bassin est la région arrosée par un fleuve et ses affluents.',
             'A green valley with one wide river in the middle and several small rivers joining it from the hills.',
             ['UN BASSIN']),
            ('Un affluent se jette dans un fleuve plus grand pour le grossir.',
             'A narrow river flowing into a much wider river, the two waters meeting and swirling together.',
             ['UN AFFLUENT']),
            ('Le Cameroun compte quatre bassins : le Tchad, le Niger, l’Atlantique et le Congo.',
             'Four separate blue ribbons of water flowing away in four different directions over soft green land.',
             ['QUATRE BASSINS']),
            ('Le Logone arrose Maroua, et la Bénoué arrose Garoua.',
             'A broad river in a dry savannah passing beside a small town with low houses, acacia trees and boats.',
             ['LOGONE', 'BÉNOUÉ']),
            ('La Sanaga rejoint l’océan, et la Sangha coule dans la forêt.',
             'A large river widening towards the ocean on the left, and a dark calm river under tall rainforest trees on the right.',
             ['SANAGA', 'SANGHA']),
        ],
    ),
    (
        'activites', 'Les activités de l’homme au village et en ville',
        'Une journée qui commence au village et finit en ville.',
        [
            ('Au village, on pêche, on élève des animaux et on cultive la terre.',
             'A village by a river with a fisherman casting a net, goats grazing and a man hoeing a field.',
             ['AU VILLAGE']),
            ('On y fait aussi l’artisanat, les danses traditionnelles et la cuisine.',
             'A village square with a potter shaping a jar, dancers in traditional clothes and a woman cooking on a fire.',
             ['ARTISANAT']),
            ('En ville, on travaille dans les bureaux, les écoles et les hôpitaux.',
             'A calm town street with plain buildings without any sign, a bus, and people walking to work.',
             ['EN VILLE']),
            ('Il y a aussi les petits métiers : le call box et les vendeurs ambulants.',
             'A street corner with a small phone booth stand under a parasol and a vendor carrying goods on his head.',
             ['PETITS MÉTIERS']),
        ],
    ),
]


def verifier():
    plans = 0
    for cle, titre, fil, blocs in FILMS:
        for voix, image, mots in blocs:
            plans += 1
            assert "'" not in voix, voix
            assert len(voix.split()) <= 18, 'phrase trop longue : ' + voix
            assert len(mots) <= 2, mots
            for m in mots:
                assert len(m) <= 15, m
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-' + cle)
        os.makedirs(dossier, exist_ok=True)
        manifeste = {
            'title': titre, 'channel_type': 'Kids', 'style': 'Pastel Flat 2D',
            'aspect_ratio': '16:9', 'language': 'fr', 'talking_characters': False,
            'through_line': fil,
            'blocks': [{'n': i + 1, 'block_kind': 'narration', 'vo_line': v, 'shot': s, 'keywords': k}
                       for i, (v, s, k) in enumerate(blocs)],
        }
        io.open(os.path.join(dossier, 'script_manifest.json'), 'w', encoding='utf-8', newline='\n').write(
            json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n')

        md = ['# %s — script verrouillé' % titre, '',
              'Format : CM1, 16:9, %d plans.' % len(blocs),
              'Voix : Céline, articulation claire, débit posé.', '',
              'Fil conducteur : %s' % fil, '', '## Narration', '']
        md += ['%d. %s' % (i + 1, v) for i, (v, _, _) in enumerate(blocs)]
        md += ['', '## Ce qui est à l’image', '']
        md += ['%d. %s' % (i + 1, s) for i, (_, s, _) in enumerate(blocs)]
        md += ['', '## Mots affichés', '']
        md += ['%d. %s' % (i + 1, ' · '.join(k)) for i, (_, _, k) in enumerate(blocs)]
        io.open(os.path.join(dossier, 'script.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')

        io.open(os.path.join(dossier, 'prompts.txt'), 'w', encoding='utf-8', newline='\n').write(
            '\n'.join(STYLE + s for _, s, _ in blocs) + '\n')


if __name__ == '__main__':
    plans = verifier()
    ecrire()
    print('%d films · %d plans' % (len(FILMS), plans))
    for cle, titre, _, blocs in FILMS:
        print('  video-%-10s %d plans  %s' % (cle, len(blocs), titre))
