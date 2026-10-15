# -*- coding: utf-8 -*-
"""
Les scripts des six films des leçons de KLEIN (CE1).

Même chaîne que le film des grandes découvertes : une image par phrase, la
voix de Céline, et le montage en local. Ce qui change, c'est le calibrage.

KLEIN est en CE1. Un film de CM1 va trop vite pour lui : on raccourcit les
phrases (dix à quinze mots), on garde une seule idée par plan, et le mot
affiché tient en deux mots. Un film de leçon dure de trente à cinquante
secondes — au-delà, l'enfant décroche avant la fin.

Règle tenue : ce qui est dit est montré. Si la voix nomme le charbon, le
charbon est à l'image au moment où le mot tombe.

Usage :  python work/films-klein.py
         → écrit work/video-<cle>/script.md et script_manifest.json
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, cinematic wide shot, '
    'no text, no letters, no numbers, no watermark, no real person, no brand. '
)

# clé, titre de la leçon, fil conducteur, plans (voix, image, mots affichés)
FILMS = [
    (
        'obeissance', 'L’obéissance',
        'Une journée d’un enfant à la maison : on lui demande, il fait, on l’aime.',
        [
            ('Obéir, c’est faire ce qu’un aîné demande, sans discuter.',
             'A calm living room, a grandmother gently asking something of a small boy who listens carefully, warm morning light.',
             ['OBÉIR']),
            ('Quand maman appelle, je viens tout de suite.',
             'A mother standing at a doorway calling, a boy running towards her across a tidy courtyard, happy movement.',
             ['TOUT DE SUITE']),
            ('Un enfant obéissant est aimé de tout le monde.',
             'A family of four smiling around a small boy, soft hearts floating above them, warm colours.',
             ['AIMÉ DE TOUS']),
            ('Si nous voulons réussir dans la vie, obéissons.',
             'A boy climbing three soft wide steps towards a big glowing star in a gentle sky.',
             ['RÉUSSIR']),
        ],
    ),
    (
        'identite', 'Le droit à l’identité',
        'Un carnet d’identité qui s’ouvre et se remplit, page après page.',
        [
            ('Chaque enfant a droit à une identité.',
             'Three children of different looks standing together, each with a soft glowing badge on the chest, friendly scene.',
             ['CHAQUE ENFANT']),
            ('L’identité lui donne un nom.',
             'A large open booklet on a table with a child portrait drawn on the left page and an empty name line on the right.',
             ['UN NOM']),
            ('Elle lui donne aussi une nationalité.',
             'The same open booklet with a small waving flag planted beside it and a globe in the soft background.',
             ['UNE NATIONALITÉ']),
        ],
    ),
    (
        'integration', 'L’intégration nationale',
        'Un village qui grandit : d’abord quelques cases, puis tout un pays qui vit ensemble.',
        [
            ('L’intégration nationale, c’est le mélange des cultures et des traditions.',
             'Several coloured ribbons of different patterns braiding together into one wide ribbon above a crowd of small figures.',
             ['MÉLANGE']),
            ('Au Cameroun, plus de deux cent cinquante ethnies vivent dans la paix.',
             'Many small colourful African houses of different styles on gentle hills, tiny people walking between them, warm sun.',
             ['250 ETHNIES']),
            ('Les mariages entre ethnies rapprochent les familles.',
             'Two families in different traditional clothes joining hands around a happy couple, flowers in the air.',
             ['MARIAGES']),
            ('La cohabitation et les affectations des travailleurs les rapprochent encore.',
             'Neighbouring houses side by side and a small bus arriving with a worker carrying a bag, friendly village street.',
             ['COHABITATION']),
        ],
    ),
    (
        'filtrage', 'Les techniques de filtrage de l’eau',
        'Une expérience, du début à la fin : l’eau sale entre, l’eau propre sort.',
        [
            ('L’eau du puits n’est pas toujours potable.',
             'A child holding a glass of cloudy brown water next to a village well, worried friendly face.',
             ['EAU SALE']),
            ('Je coupe une bouteille en deux, et je la retourne.',
             'A clear plastic bottle cut in half and turned upside down, resting in the neck of a glass jar, clean simple scene.',
             ['LA BOUTEILLE']),
            ('Je mets le coton, puis le sable, puis le charbon, puis le gravier.',
             'A cut-away of the upside down bottle filling with four clean layers, white cotton at the bottom, then beige sand, then black charcoal, then grey gravel on top.',
             ['LES COUCHES']),
            ('Je verse l’eau sale tout en haut.',
             'A hand pouring cloudy water into the top of the layered bottle filter, droplets in the air.',
             ['JE VERSE']),
            ('En bas, l’eau qui sort est propre : elle est potable.',
             'A clear drop falling from the bottle neck into a glass of perfectly clear water below, bright and clean.',
             ['EAU POTABLE']),
        ],
    ),
    (
        'paix', 'La paix',
        'Un village où chacun fait un geste, et où la paix tient parce que tout le monde s’y met.',
        [
            ('Pour garder la paix, je vis bien avec les autres.',
             'A calm village square with children and adults greeting each other, a white dove flying above.',
             ['LA PAIX']),
            ('J’accepte les autres, même s’ils sont différents.',
             'Two children of different looks sharing one bench and one book, smiling at each other.',
             ['ACCEPTER']),
            ('Je les aide quand ils en ont besoin.',
             'A child helping another lift a heavy basket of fruit, both leaning in together.',
             ['AIDER']),
            ('Et je travaille avec eux : c’est le vivre-ensemble.',
             'Four children of different skin tones carrying one long plank together towards a half built hut, teamwork.',
             ['VIVRE ENSEMBLE']),
        ],
    ),
    (
        'sol', 'Le sol',
        'Une main qui gratte la terre, et quatre sols qui défilent sous nos yeux.',
        [
            ('Le sol est la partie du dessus de la terre.',
             'A gentle cut-away of the ground, the thin top layer highlighted, grass and a small plant growing on it.',
             ['LE DESSUS']),
            ('Tous les sols ne sont pas pareils.',
             'Four small open jars of earth of clearly different colours lined up on a wooden table.',
             ['PAS PAREILS']),
            ('Le sol sablonneux est fait de grains de roche.',
             'A close wide view of pale sandy soil with visible grains running through open fingers.',
             ['SABLONNEUX']),
            ('Le sol ferralitique est rouge : il est riche en fer.',
             'A close wide view of bright red laterite earth, clearly red and rust coloured, a dark iron pebble on it.',
             ['FERRALITIQUE']),
            ('Le sol basaltique est noir, et les plantes y poussent bien.',
             'A close wide view of dark black earth with several healthy green sprouts growing out of it.',
             ['BASALTIQUE']),
            ('Le sol argileux est mou, et il n’est pas fertile.',
             'A close wide view of soft grey clay earth, cracked and bare, a finger print pressed into it, no plant.',
             ['ARGILEUX']),
        ],
    ),
]


def verifier():
    plans = 0
    for cle, titre, fil, blocs in FILMS:
        assert 3 <= len(blocs) <= 6, cle
        for voix, image, mots in blocs:
            plans += 1
            assert "'" not in voix, 'apostrophe droite : ' + voix
            mots_voix = len(voix.split())
            assert mots_voix <= 16, 'phrase trop longue pour un CE1 (%d mots) : %s' % (mots_voix, voix)
            assert len(mots) <= 2, 'trop de mots affichés : ' + str(mots)
            for m in mots:
                assert len(m) <= 15, 'mot affiché trop long : ' + m
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-' + cle)
        os.makedirs(dossier, exist_ok=True)

        manifeste = {
            'title': titre,
            'channel_type': 'Kids',
            'style': 'Pastel Flat 2D',
            'aspect_ratio': '16:9',
            'language': 'fr',
            'talking_characters': False,
            'through_line': fil,
            'blocks': [
                {'n': i + 1, 'block_kind': 'narration', 'vo_line': v, 'shot': s, 'keywords': k}
                for i, (v, s, k) in enumerate(blocs)
            ],
        }
        io.open(os.path.join(dossier, 'script_manifest.json'), 'w', encoding='utf-8', newline='\n').write(
            json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n'
        )

        md = ['# %s — script verrouillé' % titre, '',
              'Format : CE1, 16:9, %d plans.' % len(blocs),
              'Style : Pastel Flat 2D, celui des illustrations de la leçon.',
              'Voix : Céline, articulation très claire, débit posé pour un CE1.', '',
              'Fil conducteur : %s' % fil, '',
              'Règle tenue : une seule idée par plan, et ce qui est dit est montré.', '',
              '## Narration', '']
        md += ['%d. %s' % (i + 1, v) for i, (v, _, _) in enumerate(blocs)]
        md += ['', '## Ce qui est à l’image', '']
        md += ['%d. %s' % (i + 1, s) for i, (_, s, _) in enumerate(blocs)]
        md += ['', '## Mots affichés', '']
        md += ['%d. %s' % (i + 1, ' · '.join(k)) for i, (_, _, k) in enumerate(blocs)]
        io.open(os.path.join(dossier, 'script.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')

        # Les consignes d'image, prêtes à être envoyées au générateur.
        io.open(os.path.join(dossier, 'prompts.txt'), 'w', encoding='utf-8', newline='\n').write(
            '\n'.join(STYLE + s for _, s, _ in blocs) + '\n'
        )


if __name__ == '__main__':
    plans = verifier()
    ecrire()
    print('%d films · %d plans' % (len(FILMS), plans))
    for cle, titre, _, blocs in FILMS:
        print('  video-%-12s %d plans  %s' % (cle, len(blocs), titre))
