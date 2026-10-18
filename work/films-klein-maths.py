# -*- coding: utf-8 -*-
"""
Les trois films des leçons de mathématiques de KLEIN (CE1).

Premiers films du registre des nombres et des figures, décrit dans
docs/charte-films.md. Contrairement au français, il y a ici quelque chose à
montrer : un cube est une figure, une centaine est une quantité, une
conversion est un tableau. Mais la figure doit être exacte, donc elle est
dessinée, jamais générée.

Les scènes sont des gestes de la règle, comme en français :

  conditions  le mot cent, puis les deux conditions qui lui donnent son s
  cent        des paquets de cent qu’on compte, et le mot qui leur répond
  chiffres    des tuiles de chiffres, et celle qui ne peut pas exister
  cube        le solide, ses sommets qui s’allument, ses arêtes par groupes
  patron      le cube qui s’ouvre en six carrés
  tableau     les colonnes, les chiffres qui tombent, la lecture qui suit
  echelle     les quatre unités, de la plus grande à la plus petite

Trois plans portent tout le poids pédagogique du film des nombres : un
paquet, deux paquets, trois paquets. La même scène, trois fois, avec une
condition qui change — et le s qui arrive, puis qui repart quand « quarante »
se présente. La règle s’apprend par la variation, pas par la phrase.

Usage :  python work/films-klein-maths.py
"""

import io
import json
import os

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')
SCENES = ('conditions', 'cent', 'chiffres', 'cube', 'patron', 'tableau', 'echelle')

# (clé, titre, leçon, fil conducteur, [(voix, scène, mots affichés, humeur)])
FILMS = [
    (
        'nombres', 'Les nombres de 101 à 999', 'Les nombres de 101 à 999',
        'Un s arrive au bout de cent, puis repart dès qu’un nombre le suit.',
        [
            ('Cent prend un s quand il est multiplié et qu’aucun nombre ne le suit.',
             {'scene': 'conditions'},
             ['LA RÈGLE'], 'content'),
            ('Cent s’écrit sans s, car il n’est pas multiplié.',
             {'scene': 'cent', 'paquets': 1, 'mot': 'cent'},
             ['CENT'], 'content'),
            ('Deux cents prend un s : rien ne suit le mot cent.',
             {'scene': 'cent', 'paquets': 2, 'mot': 'deux cent', 'finale': 's'},
             ['DEUX CENTS'], 'encourage'),
            ('Trois cent quarante perd son s, car quarante suit cent.',
             {'scene': 'cent', 'paquets': 3, 'mot': 'trois cent', 'finale': 's',
              'suivant': 'quarante'},
             ['PAS DE S'], 'content'),
            ('Neuf cent quatre-vingt-dix-neuf est le plus grand nombre à trois chiffres.',
             {'scene': 'chiffres', 'tuiles': ['9', '9', '9'], 'barree': True,
              'mot': '999'},
             ['999'], 'fete'),
        ],
    ),
    (
        'cube', 'Le cube', 'Le cube',
        'Un solide qu’on ouvre, puis qu’on compte : six, huit, douze.',
        [
            ('Le cube est un solide.',
             {'scene': 'cube'},
             ['LE CUBE'], 'content'),
            ('Le cube a six faces carrées.',
             {'scene': 'patron'},
             ['SIX FACES'], 'content'),
            ('Le cube a huit sommets.',
             {'scene': 'cube', 'compter': 'sommets'},
             ['HUIT SOMMETS'], 'encourage'),
            ('Le cube a douze arêtes.',
             {'scene': 'cube', 'compter': 'aretes'},
             ['DOUZE ARÊTES'], 'fete'),
        ],
    ),
    (
        'mesures', 'Les mesures de grandeurs : les sous-multiples',
        'Les mesures de grandeurs : les sous-multiples',
        'Quatre colonnes, et un chiffre qui tombe dans la bonne.',
        [
            ('Pour convertir une mesure, j’utilise le tableau des sous-multiples.',
             {'scene': 'tableau'},
             ['LE TABLEAU'], 'content'),
            ('Les sous-multiples du mètre sont le décimètre, le centimètre et le millimètre.',
             {'scene': 'echelle'},
             ['M DM CM MM'], 'content'),
            ('Deux mètres font deux cents centimètres.',
             {'scene': 'tableau', 'chiffres': [2, 0, 0, None], 'cible': 2,
              'legende': '2 m = 200 cm'},
             ['2 M = 200 CM'], 'encourage'),
            ('Cent vingt centimètres font un mètre et deux décimètres.',
             {'scene': 'tableau', 'chiffres': [1, 2, 0, None], 'cible': 0,
              'legende': '120 cm = 1 m 2 dm'},
             ['120 CM'], 'content'),
            ('Trois décimètres et quatre millimètres font trois cent quatre millimètres.',
             {'scene': 'tableau', 'chiffres': [None, 3, 0, 4], 'cible': 3,
              'legende': '3 dm 4 mm = 304 mm'},
             ['304 MM'], 'fete'),
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
            if scene['scene'] == 'cent':
                assert 1 <= scene['paquets'] <= 3, scene
                # Le s ne peut pas repartir s’il n’est jamais arrivé.
                assert not scene.get('suivant') or scene.get('finale'), scene
            if scene['scene'] == 'cube':
                assert scene.get('compter') in (None, 'sommets', 'aretes'), scene
            if scene['scene'] == 'tableau':
                chiffres = scene.get('chiffres')
                if chiffres is not None:
                    assert len(chiffres) == 4, scene
                    assert scene.get('cible') is not None, scene
                    # La colonne qu’on surligne doit porter un chiffre, sinon la
                    # lecture annoncée ne se lit nulle part à l’écran.
                    assert chiffres[scene['cible']] is not None, scene
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, lecon, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-' + cle)
        os.makedirs(dossier, exist_ok=True)

        manifeste = {
            'title': titre, 'lesson': lecon, 'registre': 'nombres et figures',
            'style': 'Fredoka et figures dessinées sur fond pastel, composé',
            'aspect_ratio': '16:9', 'language': 'fr', 'narrator': 'Céline',
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
              'Leçon : %s (CE1)' % lecon,
              'Registre : nombres et figures. Rien n’est généré, tout est dessiné.',
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
