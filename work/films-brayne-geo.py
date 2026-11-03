# -*- coding: utf-8 -*-
"""
Les deux films des zones agricoles du Cameroun, pour BRAYNE (CM1).

La voix est française : la leçon l-est, et la charte dit que la voix suit
la langue de la leçon. C-est donc Céline, comme pour toutes les leçons
françaises de l-application.

Le fil des deux films est le même geste : **la carte s-allume**. Un film de
géographie qui réciterait « le coton au Nord, la canne au Centre » ne vaut
pas mieux que la liste du cahier. Ici la phrase est dite pendant que la
région s-éclaire sur la silhouette du pays, toujours la même silhouette —
c-est le seul moyen pour qu-à la fin il voie le Cameroun quand on lui dit
« à l-Est ».

Le premier film reste ici : ce qui pousse et se mange au pays. Le second
part : ce qui est transformé ou vendu à l-étranger. Le dernier plan de
chacun rappelle cette différence, parce que c-est elle qu-on lui demandera.

Usage :  python work/films-brayne-geo.py
"""

import io
import json
import os

HUMEURS = ('content', 'fete', 'encourage', 'manque', 'dort')
SCENES = ('champ', 'deux', 'assiette', 'zone', 'villes', 'ville', 'usine',
          'noms', 'chemins')
MOTS_MAX = 18
ZONES = ('nord', 'ouest', 'centre', 'sud', 'littoral', 'est')

FILMS = [
    (
        'vivrieres', 'Les cultures vivrières', 'L’agriculture et les cultures vivrières',
        'Ce qui pousse ici, et qui se mange ici.',
        [
            ('L’agriculture est une activité qui consiste à cultiver la terre.',
             {'scene': 'champ'},
             ['CULTIVER LA TERRE'], 'content'),
            ('Au Cameroun, on distingue deux grandes sortes de cultures.',
             {'scene': 'deux', 'gauche': 'vivrières', 'droite': 'de rente'},
             ['DEUX SORTES'], 'content'),
            ('Les cultures vivrières nourrissent les populations locales.',
             {'scene': 'assiette', 'note': 'elles restent ici'},
             ['VIVRIÈRES'], 'content'),
            ('Le mil, le maïs, le sorgho et les arachides poussent dans le Nord.',
             {'scene': 'zone', 'zones': ['nord'],
              'cultures': ['mil', 'maïs', 'sorgho', 'arachides']},
             ['LE NORD'], 'content'),
            ('On les cultive principalement à Maroua, à Garoua et à Ngaoundéré.',
             {'scene': 'villes', 'zones': ['nord'],
              'villes': ['Maroua', 'Garoua', 'Ngaoundéré']},
             ['TROIS VILLES'], 'encourage'),
            ('Les pommes de terre et les ignames sont cultivés à l’Ouest.',
             {'scene': 'zone', 'zones': ['ouest'],
              'cultures': ['pommes de terre', 'ignames']},
             ['L’OUEST'], 'content'),
            ('Le manioc, le macabo et la patate, dans le Centre, le Sud et le Littoral.',
             {'scene': 'zone', 'zones': ['centre', 'sud', 'littoral'],
              'cultures': ['manioc', 'macabo', 'patate']},
             ['LE CENTRE'], 'content'),
            ('Les légumes frais, eux, sont cultivés dans les villes.',
             {'scene': 'ville', 'note': 'près de ceux qui les mangent'},
             ['LES VILLES'], 'encourage'),
            ('Tout cela reste au pays, et finit dans nos assiettes.',
             {'scene': 'assiette', 'note': 'destinées aux populations locales'},
             ['ICI'], 'fete'),
        ],
    ),
    (
        'rente', 'Les cultures de rente', 'Les cultures de rente',
        'Ce qui part : l’usine, le bateau, et cinq régions.',
        [
            ('Les cultures de rente sont transformées dans les industries.',
             {'scene': 'usine'},
             ['L’USINE'], 'content'),
            ('Ou bien elles sont vendues à l’étranger.',
             {'scene': 'chemins', 'note': 'vers ailleurs'},
             ['L’ÉTRANGER'], 'content'),
            ('On les appelle aussi cultures industrielles, ou cultures d’exportation.',
             {'scene': 'noms',
              'noms': ['de rente', 'industrielles', 'd’exportation']},
             ['TROIS NOMS'], 'encourage'),
            ('Le cacao, le café et le thé sont cultivés à l’Ouest.',
             {'scene': 'zone', 'zones': ['ouest'], 'cultures': ['cacao', 'café', 'thé']},
             ['L’OUEST'], 'content'),
            ('Le coton, au Nord du Cameroun.',
             {'scene': 'zone', 'zones': ['nord'], 'cultures': ['coton']},
             ['LE NORD'], 'content'),
            ('La canne à sucre, au Centre.',
             {'scene': 'zone', 'zones': ['centre'], 'cultures': ['canne à sucre']},
             ['LE CENTRE'], 'content'),
            ('Le palmier à huile, dans le Sud.',
             {'scene': 'zone', 'zones': ['sud'], 'cultures': ['palmier à huile']},
             ['LE SUD'], 'content'),
            ('Et le tabac, à l’Est du pays.',
             {'scene': 'zone', 'zones': ['est'], 'cultures': ['tabac']},
             ['L’EST'], 'encourage'),
            ('La même terre, deux chemins : l’un reste ici, l’autre prend le bateau.',
             {'scene': 'chemins', 'note': 'vivrière ou de rente'},
             ['DEUX CHEMINS'], 'fete'),
        ],
    ),
]


def verifier():
    plans = 0
    vues = set()
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
            for z in scene.get('zones', []):
                assert z in ZONES, z
                vues.add(z)
            if scene['scene'] == 'zone':
                assert scene.get('cultures'), scene
                assert scene.get('zones'), scene
            if scene['scene'] == 'villes':
                assert len(scene['villes']) == 3, scene

    # Les six zones de la leçon doivent toutes s-allumer au moins une fois
    # dans les films : une région dont on parle sans jamais la montrer est
    # une région qu-il ne saura pas placer.
    manquantes = set(ZONES) - vues
    assert not manquantes, 'zones jamais montrées : ' + ', '.join(sorted(manquantes))

    # Et chaque culture de rente du cahier doit avoir son plan.
    rente = [b[1] for b in dict((f[0], f[4]) for f in FILMS)['rente'] if b[1]['scene'] == 'zone']
    attendues = {'cacao', 'coton', 'canne à sucre', 'palmier à huile', 'tabac'}
    citees = {c for s in rente for c in s['cultures']}
    assert attendues <= citees, 'culture de rente oubliée : ' + str(attendues - citees)
    return plans


def ecrire():
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle, titre, lecon, fil, blocs in FILMS:
        dossier = os.path.join(racine, 'video-' + cle)
        os.makedirs(dossier, exist_ok=True)

        manifeste = {
            'title': titre, 'lesson': lecon, 'registre': 'geographie',
            'style': 'Carte du Cameroun dessinée et Fredoka sur fond pastel, composé',
            'aspect_ratio': '16:9', 'language': 'fr',
            'narrator': 'voix française — la voix suit la langue de la leçon',
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
              'Leçon : %s (CM1, géographie)' % lecon,
              'Registre : géographie. Rien n’est généré, tout est dessiné.',
              'Voix : française — Céline, comme toutes les leçons françaises.', '',
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
        print('  video-%-12s %d plans  %s' % (cle, len(blocs), titre))
