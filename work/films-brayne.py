# -*- coding: utf-8 -*-
"""
Les scripts des deux films des leçons de BRAYNE (CM1).

Même chaîne que les six films de KLEIN, mais calibrée pour un CM1 : les
phrases peuvent porter deux informations au lieu d'une, et les mots affichés
peuvent être des noms propres — à dix ans on lit « BÉNOUÉ » sans buter.

Règle tenue : ce qui est dit est montré. Quand la voix nomme la Sanaga, le
fleuve qui s'élargit vers l'océan est à l'image au moment où le mot tombe.

Deux règles ajoutées le 16 octobre 2026, détaillées dans docs/charte-films.md :

  · Niba explique. Chaque plan porte une humeur du lionceau, et c'est lui qui
    dit la phrase. L'enfant n'écoute plus un inconnu : il écoute celui qui le
    félicite depuis des semaines.

  · Un lieu nommé est le vrai lieu. « Le Logone arrose Maroua » montrait
    jusqu'ici une savane quelconque — ni Maroua, ni l'Extrême-Nord, nulle
    part. Les plans portent maintenant le paysage réel : sahel ocre et monts
    Mandara au nord, hautes herbes et bancs de sable sur la Bénoué, forêt et
    mangrove sur la Sanaga, forêt sombre et eau lente sur la Sangha.

Usage :  python work/films-brayne.py
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, cinematic wide shot, '
    'no text, no letters, no numbers, no watermark, no real person, no brand. '
)

# Les paysages du Cameroun, repris tels quels dans les plans. Un enfant d'ici
# les distingue du premier coup d'œil ; un décor interchangeable ne lui
# apprend rien et, pire, ne lui ressemble pas.
SAHEL = (
    'the real Sahel of the Far North of Cameroon: flat pale ochre plain, dusty pale sky, '
    'sparse flat-topped thorny acacias, rounded granite domes of the Mandara hills, '
    'conical earth houses with pointed thatch caps, millet granaries, a humped zebu'
)
SOUDAN = (
    'the real Sudanian savannah of the North of Cameroon: tall golden grass, broad scattered '
    'trees, a wide river showing pale sandbanks, wooden pirogues at a river landing'
)
FORET = (
    'the real forest of southern Cameroon: dense green rainforest, oil palms, red laterite '
    'earth, a wide brown river'
)
EQUATEUR = (
    'the real equatorial forest of eastern Cameroon: very dense dark forest, very tall '
    'emergent trees, slow still black water under deep shade'
)

FILMS = [
    (
        'bassins', 'Les bassins hydrographiques du Cameroun',
        'On remonte un fleuve : d’abord l’eau, puis les régions qu’elle traverse.',
        [
            ('L’hydrographie, c’est l’ensemble des cours d’eau d’une région.',
             'The outline of Cameroon seen from high above, narrow and pointed at the north, '
             'wide in the south; many small blue streams drawing themselves across it, morning light.',
             ['HYDROGRAPHIE'], 'content'),
            ('Un bassin est la région arrosée par un fleuve et ses affluents.',
             'One wide river in a valley with several smaller rivers joining it from the hills, '
             'and a soft tinted area spreading outward to show the land this river waters.',
             ['UN BASSIN'], 'content'),
            ('Un affluent se jette dans un fleuve plus grand pour le grossir.',
             'A narrow river flowing into a much wider river, the two waters meeting, '
             'the wide river visibly swelling and continuing thicker than before.',
             ['UN AFFLUENT'], 'encourage'),
            ('Le Cameroun compte quatre bassins : le Tchad, le Niger, l’Atlantique et le Congo.',
             'The map of Cameroon with four basins tinted in their real places — Chad at the '
             'northern tip, Niger around Garoua, Atlantic across the centre and south, Congo in '
             'the far south-east corner — and four arrows showing where the water finally goes.',
             ['QUATRE BASSINS'], 'content'),
            ('Le Logone arrose Maroua, et la Bénoué arrose Garoua.',
             'Split view, both in the real north. Left: ' + SAHEL + ', with the Logone running '
             'north past Maroua. Right: ' + SOUDAN + ', with the Bénoué turning west at Garoua.',
             ['LOGONE', 'BÉNOUÉ'], 'content'),
            ('La Sanaga rejoint l’océan, et la Sangha coule dans la forêt.',
             'Split view. Left: ' + FORET + ', the Sanaga widening towards the Atlantic with '
             'mangroves and the dark cone of Mount Cameroon on the horizon. Right: ' + EQUATEUR +
             ', the Sangha flowing slowly under the trees.',
             ['SANAGA', 'SANGHA'], 'fete'),
        ],
    ),
    (
        'activites', 'Les activités de l’homme au village et en ville',
        'Une journée qui commence au village et finit en ville.',
        [
            ('Au village, on pêche, on élève des animaux et on cultive la terre.',
             'A Cameroonian village on a river bank with red laterite earth and oil palms, '
             'a fisherman casting a net from a wooden pirogue, goats grazing, a man hoeing a field.',
             ['AU VILLAGE'], 'content'),
            ('On y fait aussi l’artisanat, les danses traditionnelles et la cuisine.',
             'A Cameroonian village square under a mango tree: a potter shaping a clay jar, '
             'dancers in traditional cloth, a woman cooking over a wood fire with a large pot.',
             ['ARTISANAT'], 'content'),
            ('En ville, on travaille dans les bureaux, les écoles et les hôpitaux.',
             'A calm Cameroonian town street with low concrete buildings without any sign, '
             'red earth at the roadside, a yellow shared taxi, people walking to work.',
             ['EN VILLE'], 'content'),
            ('Il y a aussi les petits métiers : le call box et les vendeurs ambulants.',
             'A Cameroonian street corner with a small call box stand under a parasol and a '
             'street vendor carrying goods on his head.',
             ['PETITS MÉTIERS'], 'fete'),
        ],
    ),
]

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')


def verifier():
    plans = 0
    for cle, titre, fil, blocs in FILMS:
        for voix, image, mots, humeur in blocs:
            plans += 1
            assert "'" not in voix, voix
            assert len(voix.split()) <= 18, 'phrase trop longue : ' + voix
            assert len(mots) <= 2, mots
            assert humeur in HUMEURS, humeur
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
            'aspect_ratio': '16:9', 'language': 'fr', 'talking_characters': True,
            'narrator': 'Niba',
            'through_line': fil,
            'blocks': [{'n': i + 1, 'block_kind': 'narration', 'vo_line': v, 'shot': s,
                        'keywords': k, 'niba': h}
                       for i, (v, s, k, h) in enumerate(blocs)],
        }
        io.open(os.path.join(dossier, 'script_manifest.json'), 'w', encoding='utf-8', newline='\n').write(
            json.dumps(manifeste, ensure_ascii=False, indent=2) + '\n')

        md = ['# %s — script verrouillé' % titre, '',
              'Format : CM1, 16:9, %d plans.' % len(blocs),
              'Voix : Céline, articulation claire, débit posé. Niba explique à l’écran.', '',
              'Fil conducteur : %s' % fil, '', '## Narration', '']
        md += ['%d. %s' % (i + 1, v) for i, (v, _, _, _) in enumerate(blocs)]
        md += ['', '## Ce qui est à l’image', '']
        md += ['%d. %s' % (i + 1, s) for i, (_, s, _, _) in enumerate(blocs)]
        md += ['', '## Mots affichés', '']
        md += ['%d. %s' % (i + 1, ' · '.join(k)) for i, (_, _, k, _) in enumerate(blocs)]
        md += ['', '## Humeur de Niba', '']
        md += ['%d. %s' % (i + 1, h) for i, (_, _, _, h) in enumerate(blocs)]
        io.open(os.path.join(dossier, 'script.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')

        io.open(os.path.join(dossier, 'prompts.txt'), 'w', encoding='utf-8', newline='\n').write(
            '\n'.join(STYLE + s for _, s, _, _ in blocs) + '\n')


if __name__ == '__main__':
    plans = verifier()
    ecrire()
    print('%d films · %d plans' % (len(FILMS), plans))
    for cle, titre, _, blocs in FILMS:
        print('  video-%-10s %d plans  %s' % (cle, len(blocs), titre))
