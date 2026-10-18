# -*- coding: utf-8 -*-
"""
Les trois films des leçons de sciences de KLEIN (CE1).

La reproduction des animaux, les soins aux animaux domestiques, les milieux
de vie des végétaux. Treize plans en tout, un par notion du cahier, plus une
ouverture là où la leçon en a besoin.

Les règles tenues sont celles de docs/charte-films.md :

  · Niba explique à l'écran — il est posé par l'application, en SVG, avec une
    humeur par plan. Il ne prend pas la voix.
  · La narration reste Céline, direction de jeu inchangée.
  · Un lieu nommé est le vrai lieu. Ici la leçon ne nomme pas de ville, mais
    elle nomme des arbres : le manguier et le palmier à huile poussent sur de
    la latérite rouge, le palétuvier sur ses racines en arceaux dans la boue.
    Pas d'arbre générique.
  · Une seule idée par plan, et ce qui est dit est montré.
  · Le film se comprend sans le son : les mots sont posés par-dessus.

KLEIN est en CE1 : une information par phrase, quatorze mots au plus, et des
mots qu'un enfant de sept ans prononce sans buter.

Usage :  python work/films-klein-sciences.py
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, cinematic wide shot, '
    'no text, no letters, no numbers, no watermark, no real person, no brand. '
)

# Le coin bas-gauche reste libre dans chaque plan : c'est la place de Niba et
# de sa bulle, posés par l'application par-dessus la vidéo.
PLACE_NIBA = ' Keep the lower left corner calm and uncluttered.'

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')

# (clé, titre, leçon, fil conducteur, [(voix, plan, mots, humeur)])
FILMS = [
    (
        'reproduction', 'La reproduction des animaux', 'La reproduction des animaux',
        'On va voir naître trois petits, chacun à sa façon.',
        [
            ('Les animaux ne font pas tous leurs petits de la même façon.',
             'A calm farmyard in southern Cameroon with red laterite earth and an oil palm behind: '
             'a hen on the left, a goat in the middle, and a snake coiled on warm sand on the right, '
             'each one quietly in its own corner.',
             ['TROIS MODES'], 'content'),
            ('Les ovipares pondent des œufs : la poule, le poisson, l’escargot.',
             'A hen settling on a small nest of pale eggs, a fish in a shallow pool beside her and a '
             'snail on a leaf, warm morning light.',
             ['OVIPARE'], 'content'),
            ('Les vivipares donnent directement naissance aux petits : la chèvre, la vache.',
             'A goat standing beside her newborn kid on red earth, a cow with her calf a little '
             'further back, soft warm light.',
             ['VIVIPARE'], 'content'),
            ('Les ovovivipares gardent leurs œufs dans le ventre : la vipère.',
             'A snake coiled on warm sand, a soft glow inside her body showing small eggs, one tiny '
             'snake just emerging beside her.',
             ['OVOVIVIPARE'], 'fete'),
        ],
    ),
    (
        'soins', 'Les soins aux animaux domestiques', 'Les soins aux animaux domestiques',
        'Un animal tombe malade, on apprend à le voir et à le soigner.',
        [
            ('Les animaux de la maison peuvent tomber malades.',
             'A quiet Cameroonian courtyard with red earth, a goat lying down with its head low, '
             'a hen standing still nearby, soft overcast light.',
             ['LES MALADIES'], 'manque'),
            ('La gale et la teigne abîment la peau et le poil.',
             'A close calm view of an animal flank with a plain uniform coat, showing three clearly '
             'round bare patches where the hair has fallen out.',
             ['GALE', 'TEIGNE'], 'encourage'),
            ('La grippe donne la toux, la bave et la fatigue.',
             'A hen resting with drooping wings beside a bowl of water, head low, a soft blanket of '
             'warm light around her.',
             ['LA GRIPPE'], 'encourage'),
            ('La rage fait beaucoup baver et rend l’animal agressif.',
             'Seen from a safe distance: a lone dog far away beside a puddle, head low, while an '
             'adult gently leads a child away along a path, both seen from behind.',
             ['LA RAGE'], 'manque'),
            ('On vaccine, on nettoie l’habitat, on va chez le vétérinaire.',
             'A clean swept animal shelter with fresh straw and a bucket of clear water, a small '
             'medical bag on a stool, the goat standing again and alert.',
             ['LES TROIS GESTES'], 'fete'),
        ],
    ),
    (
        'milieux', 'Les milieux de vie des végétaux', 'Les milieux de vie des végétaux',
        'On remonte de la terre ferme jusqu’à la boue, en suivant l’eau.',
        [
            ('Les végétaux sont vivants : ils ont tous des racines.',
             'A single young plant shown whole on red laterite earth, its roots visible under a '
             'cut-away of the soil, soft clear light.',
             ['DES RACINES'], 'content'),
            ('Certains poussent sur la terre : le manguier, le palmier.',
             'A mango tree heavy with fruit and an oil palm growing on dry red laterite earth, a '
             'hibiscus flower in front, warm afternoon light.',
             ['SUR LA TERRE'], 'content'),
            ('D’autres poussent dans l’eau : le nénuphar, le roseau.',
             'A calm pond with water lilies floating flat on the surface, tall reeds at the edge and '
             'green algae visible under the clear water.',
             ['DANS L’EAU'], 'content'),
            ('D’autres poussent dans la boue : le palétuvier, le papyrus.',
             'Mangrove trees standing on arching stilt roots in dark shining mud, tall papyrus stems '
             'behind them, soft humid light.',
             ['DANS LA BOUE'], 'fete'),
        ],
    ),
]


def verifier():
    """Une phrase trop longue ou un mot trop grand se verrait à l'écran."""
    plans = 0
    for cle, titre, lecon, fil, blocs in FILMS:
        for voix, plan, mots, humeur in blocs:
            plans += 1
            assert "'" not in voix, 'apostrophe droite : ' + voix
            assert len(voix.split()) <= 14, 'phrase trop longue pour un CE1 : ' + voix
            assert len(mots) <= 2, mots
            assert humeur in HUMEURS, humeur
            for m in mots:
                assert len(m) <= 18, 'mot trop long pour la bande : ' + m
                assert m == m.upper(), m
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, lecon, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-' + cle)
        os.makedirs(dossier, exist_ok=True)

        manifeste = {
            'title': titre, 'lesson': lecon, 'channel_type': 'Kids',
            'style': 'Pastel Flat 2D', 'aspect_ratio': '16:9', 'language': 'fr',
            'narrator': 'Céline', 'talking_characters': False, 'mascotte': 'Niba',
            'through_line': fil,
            'blocks': [
                {'n': i + 1, 'block_kind': 'narration', 'vo_line': v,
                 'shot': s + PLACE_NIBA, 'keywords': k, 'niba': h}
                for i, (v, s, k, h) in enumerate(blocs)
            ],
        }
        io.open(os.path.join(dossier, 'script_manifest.json'), 'w',
                encoding='utf-8', newline='\n').write(
            json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n')

        md = ['# %s — script verrouillé' % titre, '',
              'Leçon : %s (CE1)' % lecon,
              'Format : 16:9, %d plans.' % len(blocs),
              'Voix : Céline, articulation claire, débit posé. Niba explique à l’écran.', '',
              'Fil conducteur : %s' % fil, '', '## Narration', '']
        md += ['%d. %s' % (i + 1, v) for i, (v, _, _, _) in enumerate(blocs)]
        md += ['', '## Ce qui est à l’image', '']
        md += ['%d. %s' % (i + 1, s) for i, (_, s, _, _) in enumerate(blocs)]
        md += ['', '## Mots affichés', '']
        md += ['%d. %s' % (i + 1, ' · '.join(k)) for i, (_, _, k, _) in enumerate(blocs)]
        md += ['', '## Humeur de Niba', '']
        md += ['%d. %s' % (i + 1, h) for i, (_, _, _, h) in enumerate(blocs)]
        io.open(os.path.join(dossier, 'script.md'), 'w',
                encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')

        io.open(os.path.join(dossier, 'prompts.txt'), 'w',
                encoding='utf-8', newline='\n').write(
            '\n'.join(STYLE + s + PLACE_NIBA for _, s, _, _ in blocs) + '\n')


if __name__ == '__main__':
    plans = verifier()
    ecrire()
    print('%d films - %d plans' % (len(FILMS), plans))
    for cle, titre, _l, _f, blocs in FILMS:
        print('  video-%-14s %d plans  %s' % (cle, len(blocs), titre))
