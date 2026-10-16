# -*- coding: utf-8 -*-
"""
Les deux leçons du cahier de BRAYNE (CM1), des 15 et 16 octobre 2026.

  Géographie physique — Les bassins hydrographiques du Cameroun
  Géographie          — Les activités de l'homme au village et en ville

Transcrites depuis quatre photos. Les noms de fleuves et de villes sont ceux
du cahier, pas ceux d'un atlas : si l'enfant a écrit « Berbérati », c'est
« Berbérati » qu'il doit retrouver dans ses révisions.

Trois endroits restent douteux sur les photos — l'encre rouge passe sur le
bleu — et ils sont écartés plutôt que devinés :
  le troisième affluent de la Bénoué (après le Faro et le Mayo Kébi) ;
  le troisième affluent de la Sanaga (après le Wouri et le Mbam) ;
  le nom de la ville arrosée par la Sangha, lu « Berbérati » sans certitude.

Les deux leçons rejoignent la matière « Histoire-Géographie » du CM1, celle
de l'emploi du temps. Le chapitre garde l'intitulé du cahier.

Usage :  python work/lecons-brayne.py
"""

import io
import json
import os

STYLE = (
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac '
    'palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, '
    'no numbers, no watermark, no real person, no brand, no map, no country outline. '
)

BH = 'Les bassins hydrographiques du Cameroun'
AV = 'Les activités de l’homme au village et en ville'

LECONS = [
    {
        'titre': BH,
        'matiere': 'Histoire-Géographie',
        'chapitre': 'Géographie physique',
        'date': '2026-10-16',
        'resume': 'L’hydrographie est l’ensemble des cours d’eau d’une région. Un bassin '
                  'hydrographique est une région arrosée par un fleuve principal et ses affluents. '
                  'Le Cameroun compte quatre bassins : le Tchad, le Niger, l’Atlantique et le Congo.',
        'illustration': 'bh-bassins',
        'prompt': 'A wide calm river seen from above, winding through green hills, with three '
                  'smaller streams joining it, soft morning light.',
        'notions': [
            {
                'kind': 'definition',
                'phrase': 'L’hydrographie est l’ensemble des cours d’eau d’une région.',
                'image': 'bh-hydrographie',
                'prompt': 'Several small blue streams running across a green plain, seen from above.',
                'expl': [('simple', 'L’hydrographie, c’est tous les cours d’eau d’une région réunis.')],
            },
            {
                'kind': 'definition',
                'phrase': 'Un bassin hydrographique est une région arrosée par un fleuve principal et ses affluents.',
                'image': 'bh-bassin',
                'prompt': 'A green valley with one big river in the middle and small rivers joining it from the hills.',
                'expl': [('simple', 'Un bassin, c’est toute la région qu’un fleuve et ses affluents arrosent.'),
                         ('analogie', 'C’est comme un arbre couché : le tronc est le fleuve, les branches sont les affluents.')],
            },
            {
                'kind': 'definition',
                'phrase': 'Un affluent est un fleuve qui se jette dans un fleuve plus grand que lui pour le grossir.',
                'image': 'bh-affluent',
                'prompt': 'A narrow river flowing into a much wider river, the two waters meeting.',
                'expl': [('simple', 'L’affluent rejoint un plus grand fleuve et lui apporte son eau.')],
            },
            {
                'kind': 'liste',
                'phrase': 'Le Cameroun compte quatre bassins hydrographiques : le Tchad, le Niger, l’Atlantique et le Congo.',
                'image': 'bh-quatre',
                'prompt': 'Four separate blue ribbons of water flowing in four different directions on a soft background.',
                'expl': [('simple', 'Quatre bassins : Tchad, Niger, Atlantique, Congo.')],
            },
            {
                'kind': 'relation',
                'phrase': 'Le bassin du Tchad a pour fleuve principal le Logone, qui arrose la ville de Maroua.',
                'image': 'bh-tchad',
                'prompt': 'A river arriving into a wide shallow lake in a dry savannah, acacia trees on the banks.',
                'expl': [('simple', 'Le Logone arrose Maroua. Ses affluents : le Chari, la Vina, le Mbéré.')],
            },
            {
                'kind': 'relation',
                'phrase': 'Le bassin du Niger a pour fleuve principal la Bénoué, qui arrose la ville de Garoua.',
                'image': 'bh-niger',
                'prompt': 'A broad river passing beside a small savannah town with low houses and boats on the bank.',
                'expl': [('simple', 'La Bénoué arrose Garoua. Ses affluents : le Faro et le Mayo Kébi.')],
            },
            {
                'kind': 'relation',
                'phrase': 'Le bassin de l’Atlantique a pour fleuve principal la Sanaga, qui traverse trois régions et arrose la ville d’Édéa.',
                'image': 'bh-atlantique',
                'prompt': 'A large river widening towards the ocean, palm trees and a waterfall on the way.',
                'expl': [('simple', 'La Sanaga traverse trois régions et arrose Édéa. Ses affluents : le Wouri, le Mbam.')],
            },
            {
                'kind': 'relation',
                'phrase': 'Le bassin du Congo a pour fleuve principal la Sangha, qui arrose la ville de Berbérati.',
                'image': 'bh-congo',
                'prompt': 'A dark calm river flowing through a dense green rainforest, tall trees on both banks.',
                'expl': [('simple', 'La Sangha arrose Berbérati. Ses affluents : la Kadeï, le Dja, la Boumba et le Ngoko.')],
            },
        ],
    },
    {
        'titre': AV,
        'matiere': 'Histoire-Géographie',
        'chapitre': 'Géographie',
        'date': '2026-10-15',
        'resume': 'Au village, les activités de l’homme sont nombreuses et variées : l’artisanat, la '
                  'pêche, l’élevage, l’agriculture, les danses traditionnelles et la cuisine. En ville, '
                  'on travaille dans l’administration, le transport, l’industrie, l’éducation, le '
                  'commerce et la santé, ainsi que dans les petits métiers.',
        'illustration': 'av-village-ville',
        'prompt': 'On the left a small village with fields and a fisherman, on the right a town with '
                  'low buildings and a bus, a road joining the two.',
        'notions': [
            {
                'kind': 'liste',
                'phrase': 'Au village, les activités de l’homme sont l’artisanat, la pêche, l’élevage, l’agriculture, les danses traditionnelles et la cuisine.',
                'image': 'av-village',
                'prompt': 'A village scene with a potter at work, a fisherman with a net, goats, and a field being hoed.',
                'expl': [('simple', 'Au village : artisanat, pêche, élevage, agriculture, danses, cuisine.')],
            },
            {
                'kind': 'liste',
                'phrase': 'En ville, l’homme travaille dans l’administration, le transport, l’industrie, l’éducation, le commerce et la santé.',
                'image': 'av-ville',
                'prompt': 'A town street with an office building, a bus, a school, a shop and a small clinic side by side.',
                'expl': [('simple', 'En ville : bureaux, transport, usines, écoles, boutiques, hôpitaux.')],
            },
            {
                'kind': 'liste',
                'phrase': 'En ville, on trouve aussi les petits métiers : le call box, les vendeurs ambulants, les gardiens et les ménagères.',
                'image': 'av-petits-metiers',
                'prompt': 'A street corner with a small phone booth stand with a parasol, a vendor carrying goods on his head, and a guard at a gate.',
                'expl': [('simple', 'Les petits métiers : call box, vendeurs ambulants, gardiens, ménagères.'),
                         ('analogie', 'Ce sont les métiers du trottoir : on les croise tous les jours en allant à l’école.')],
            },
        ],
    },
]

# ───────────────────────────── questions ─────────────────────────────
# (titre, rang de la notion, kind, niveau, payload, answer, explain)
Q = []


def q(lecon, rang, kind, niveau, payload, answer, explain):
    Q.append({'lecon': lecon, 'rang': rang, 'kind': kind, 'level': niveau,
              'payload': payload, 'answer': answer, 'explain': explain})


def qcm(l, r, n, question, options, bonne, e):
    q(l, r, 'qcm', n, {'question': question, 'options': options}, {'index': bonne}, e)


def images(l, r, n, question, cles, bonne, e):
    q(l, r, 'qcm', n, {'question': question, 'images': cles}, {'index': bonne}, e)


def vf(l, r, n, phrase, valeur, e):
    q(l, r, 'vrai_faux', n, {'statement': phrase}, {'value': valeur}, e)


def relier(l, r, n, question, gauche, droite, e):
    q(l, r, 'association', n, {'question': question, 'gauche': gauche, 'droite': droite},
      {'order': list(range(len(gauche)))}, e)


def trous(l, r, n, texte, valeurs, e):
    q(l, r, 'texte_a_trous', n, {'text': texte, 'blanks': len(valeurs)}, {'values': valeurs}, e)


def dictee(l, r, n, phrase, e):
    q(l, r, 'dictee', n, {'phrase': phrase, 'langue': 'fr'}, {'phrase': phrase}, e)


def mots(l, r, n, jetons, e):
    q(l, r, 'chronologie', n, {'question': 'Remets la phrase dans le bon ordre.', 'tokens': jetons,
                               'consigne': 'Touche les mots dans l’ordre de la phrase.'},
      {'order': list(range(len(jetons)))}, e)


def ordre(l, r, n, question, jetons, e):
    q(l, r, 'chronologie', n, {'question': question, 'tokens': jetons}, {'order': list(range(len(jetons)))}, e)


# ═══════════════ Les bassins hydrographiques (8 notions) ═══════════════

# 1 — l'hydrographie
qcm(BH, 1, 1, 'L’hydrographie, c’est l’ensemble des…', ['cours d’eau', 'montagnes', 'routes'], 0,
    'Tous les cours d’eau d’une région.')
qcm(BH, 1, 1, 'L’hydrographie concerne…', ['une région', 'une maison', 'une école'], 0, 'Une région entière.')
qcm(BH, 1, 2, 'Que regroupe l’hydrographie d’une région ?',
    ['Tous ses cours d’eau', 'Tous ses villages', 'Toutes ses routes', 'Tous ses arbres'], 0,
    'L’ensemble des cours d’eau.')
dictee(BH, 1, 3, 'L’hydrographie est l’ensemble des cours d’eau.', 'La phrase du cahier.')
trous(BH, 1, 3, 'L’{{1}} est l’ensemble des cours d’{{2}} d’une région.', ['hydrographie', 'eau'],
      'Hydrographie, eau.')
vf(BH, 1, 4, 'L’hydrographie étudie les montagnes.', False, 'Non : les cours d’eau.')

# 2 — le bassin hydrographique
qcm(BH, 2, 1, 'Un bassin hydrographique est une région…', ['arrosée par un fleuve', 'couverte de sable', 'sans eau'], 0,
    'Arrosée par un fleuve et ses affluents.')
images(BH, 2, 1, 'Clique sur un bassin : un fleuve et ses affluents.',
       ['bh-bassin', 'bh-quatre', 'bh-hydrographie'], 0, 'Le fleuve et tout ce qu’il arrose.')
qcm(BH, 2, 2, 'Qu’est-ce qui arrose un bassin hydrographique ?',
    ['Un fleuve principal et ses affluents', 'La pluie seulement', 'Un lac sans rivière', 'La mer'], 0,
    'Le fleuve principal et ses affluents.')
mots(BH, 2, 3, ['Un bassin', 'est arrosé', 'par un fleuve', 'et ses affluents'], 'La définition du cahier.')
vf(BH, 2, 4, 'Un bassin hydrographique peut n’avoir aucun cours d’eau.', False, 'Il est arrosé par un fleuve.')

# 3 — l'affluent
qcm(BH, 3, 1, 'Un affluent se jette dans…', ['un fleuve plus grand', 'la forêt', 'un puits'], 0,
    'Dans un fleuve plus grand que lui.')
qcm(BH, 3, 1, 'À quoi sert un affluent ?', ['À grossir un fleuve', 'À vider un fleuve', 'À arrêter un fleuve'], 0,
    'Il apporte son eau.')
qcm(BH, 3, 2, 'Lequel est vrai pour un affluent ?',
    ['Il rejoint un fleuve plus grand', 'Il rejoint la mer directement', 'Il reste tout seul', 'Il coule à l’envers'], 0,
    'Il rejoint un plus grand que lui.')
images(BH, 3, 2, 'Clique sur l’affluent qui rejoint un grand fleuve.',
       ['bh-affluent', 'bh-tchad', 'bh-congo'], 0, 'La petite rivière rejoint la grande.')
dictee(BH, 3, 3, 'Un affluent se jette dans un fleuve plus grand.', 'La phrase du cahier.')
trous(BH, 3, 3, 'Un {{1}} se jette dans un fleuve plus {{2}} que lui.', ['affluent', 'grand'],
      'Affluent, grand.')
qcm(BH, 3, 4, 'Le Faro rejoint la Bénoué. Le Faro est donc…', ['un affluent', 'un fleuve principal', 'un lac'], 0,
    'Il se jette dans plus grand que lui.')

# 4 — les quatre bassins
qcm(BH, 4, 1, 'Combien de bassins hydrographiques au Cameroun ?', ['Quatre', 'Deux', 'Dix'], 0, 'Quatre.')
qcm(BH, 4, 2, 'Quels sont les quatre bassins du Cameroun ?',
    ['Tchad, Niger, Atlantique, Congo', 'Tchad, Niger, Nil, Congo', 'Niger, Congo, Nil, Zambèze',
     'Tchad, Atlantique, Sahara, Congo'], 0, 'Tchad, Niger, Atlantique, Congo.')
ordre(BH, 4, 3, 'Remets les quatre bassins dans l’ordre du cahier.',
      ['Le Tchad', 'Le Niger', 'L’Atlantique', 'Le Congo'], 'L’ordre de la leçon.')
vf(BH, 4, 4, 'Le Cameroun compte quatre bassins hydrographiques.', True, 'Oui : Tchad, Niger, Atlantique, Congo.')

# 5 — le bassin du Tchad
qcm(BH, 5, 1, 'Quel est le fleuve principal du bassin du Tchad ?', ['Le Logone', 'La Sanaga', 'La Sangha'], 0,
    'Le Logone.')
qcm(BH, 5, 2, 'Quelle ville le Logone arrose-t-il ?', ['Maroua', 'Garoua', 'Édéa', 'Douala'], 0, 'Maroua.')
relier(BH, 5, 2, 'Relie le bassin du Tchad à ce qui lui appartient.',
       ['Son fleuve principal', 'Sa ville', 'Un de ses affluents'],
       ['Le Logone', 'Maroua', 'Le Chari'], 'Logone, Maroua, Chari.')
trous(BH, 5, 3, 'Le bassin du Tchad a pour fleuve principal le {{1}}, qui arrose {{2}}.', ['Logone', 'Maroua'],
      'Logone, Maroua.')
qcm(BH, 5, 4, 'Tu es à Maroua, au bord du fleuve. Quel bassin ?', ['Le Tchad', 'Le Congo', 'L’Atlantique'], 0,
    'Maroua est arrosée par le Logone.')

# 6 — le bassin du Niger
qcm(BH, 6, 1, 'Quel est le fleuve principal du bassin du Niger ?', ['La Bénoué', 'Le Logone', 'La Sangha'], 0,
    'La Bénoué.')
qcm(BH, 6, 2, 'Quelle ville la Bénoué arrose-t-elle ?', ['Garoua', 'Maroua', 'Édéa', 'Yaoundé'], 0, 'Garoua.')
relier(BH, 6, 2, 'Relie le bassin du Niger à ce qui lui appartient.',
       ['Son fleuve principal', 'Sa ville', 'Un de ses affluents'],
       ['La Bénoué', 'Garoua', 'Le Faro'], 'Bénoué, Garoua, Faro.')
dictee(BH, 6, 3, 'La Bénoué arrose la ville de Garoua.', 'La phrase du cahier.')
qcm(BH, 6, 4, 'Un bateau descend la Bénoué depuis Garoua. Quel bassin ?', ['Le Niger', 'Le Tchad', 'Le Congo'], 0,
    'La Bénoué appartient au bassin du Niger.')

# 7 — le bassin de l'Atlantique
qcm(BH, 7, 1, 'Quel est le fleuve principal du bassin de l’Atlantique ?', ['La Sanaga', 'Le Logone', 'La Bénoué'], 0,
    'La Sanaga.')
qcm(BH, 7, 2, 'Combien de régions la Sanaga traverse-t-elle ?', ['Trois', 'Une', 'Dix', 'Deux'], 0, 'Trois régions.')
qcm(BH, 7, 2, 'Quelle ville la Sanaga arrose-t-elle ?', ['Édéa', 'Garoua', 'Maroua', 'Bertoua'], 0, 'Édéa.')
trous(BH, 7, 3, 'La {{1}} traverse trois régions et arrose la ville d’{{2}}.', ['Sanaga', 'Édéa'],
      'Sanaga, Édéa.')
qcm(BH, 7, 4, 'Un fleuve finit dans l’océan près d’Édéa. Lequel ?', ['La Sanaga', 'Le Logone', 'La Sangha'], 0,
    'La Sanaga, bassin de l’Atlantique.')

# 8 — le bassin du Congo
qcm(BH, 8, 1, 'Quel est le fleuve principal du bassin du Congo ?', ['La Sangha', 'La Sanaga', 'La Bénoué'], 0,
    'La Sangha.')
qcm(BH, 8, 2, 'Lequel est un affluent de la Sangha ?', ['Le Dja', 'Le Chari', 'Le Faro', 'Le Mbam'], 0,
    'Le Dja, avec la Kadeï, la Boumba et le Ngoko.')
relier(BH, 8, 2, 'Relie chaque bassin à son fleuve principal.',
       ['Le Tchad', 'Le Niger', 'L’Atlantique', 'Le Congo'],
       ['Le Logone', 'La Bénoué', 'La Sanaga', 'La Sangha'], 'Les quatre fleuves principaux.')
mots(BH, 8, 3, ['La Sangha', 'est le fleuve', 'du bassin', 'du Congo'], 'La Sangha, bassin du Congo.')
qcm(BH, 8, 4, 'Attention : Sanaga ou Sangha ? Laquelle est dans le bassin du Congo ?',
    ['La Sangha', 'La Sanaga'], 0, 'La Sangha, au Congo. La Sanaga va à l’Atlantique.')

# ═══════════ Les activités de l'homme au village et en ville (3) ═══════════

qcm(AV, 1, 1, 'Au village, on pratique…', ['la pêche', 'l’industrie', 'l’administration'], 0,
    'Pêche, artisanat, élevage, agriculture.')
qcm(AV, 1, 1, 'Fabriquer un panier à la main, c’est…', ['l’artisanat', 'le commerce', 'le transport'], 0,
    'C’est l’artisanat.')
qcm(AV, 1, 2, 'Laquelle n’est PAS une activité du village ?',
    ['L’industrie', 'La pêche', 'L’élevage', 'L’agriculture'], 0, 'L’industrie est en ville.')
relier(AV, 1, 2, 'Relie chaque activité du village à son geste.',
       ['L’agriculture', 'L’élevage', 'La pêche'],
       ['Cultiver un champ', 'Garder des animaux', 'Prendre du poisson'], 'Trois activités du village.')
dictee(AV, 1, 3, 'Au village, les activités sont nombreuses et variées.', 'La phrase du cahier.')
mots(AV, 1, 3, ['Au village', 'on pratique', 'l’artisanat', 'et la pêche'], 'Des activités du village.')
qcm(AV, 1, 4, 'Ton oncle garde des chèvres au village. Quelle activité ?',
    ['L’élevage', 'La pêche', 'L’artisanat'], 0, 'Garder des animaux, c’est l’élevage.')

qcm(AV, 2, 1, 'En ville, on travaille dans…', ['l’administration', 'la cueillette', 'la chasse'], 0,
    'Administration, transport, industrie, éducation, commerce, santé.')
qcm(AV, 2, 2, 'Quel secteur soigne les malades ?', ['La santé', 'Le commerce', 'Le transport', 'L’industrie'], 0,
    'Le secteur de la santé.')
relier(AV, 2, 2, 'Relie chaque secteur de la ville à son lieu.',
       ['L’éducation', 'La santé', 'Le commerce'],
       ['L’école', 'L’hôpital', 'Le marché'], 'Trois secteurs de la ville.')
trous(AV, 2, 3, 'En ville, on travaille dans l’{{1}}, le transport et l’{{2}}.', ['administration', 'industrie'],
      'Administration, industrie.')
qcm(AV, 2, 4, 'Un chauffeur de bus travaille dans quel secteur ?',
    ['Le transport', 'La santé', 'L’éducation'], 0, 'Le transport.')

qcm(AV, 3, 1, 'Le call box est…', ['un petit métier', 'une usine', 'une école'], 0, 'Un petit métier de la ville.')
images(AV, 3, 2, 'Clique sur les petits métiers de la ville.',
       ['av-petits-metiers', 'av-village', 'av-ville'], 0, 'Call box, vendeurs ambulants, gardiens.')
qcm(AV, 3, 2, 'Lequel est un petit métier ?',
    ['Le vendeur ambulant', 'Le médecin', 'L’ingénieur', 'Le professeur'], 0, 'Le vendeur ambulant.')
dictee(AV, 3, 3, 'Le call box est un petit métier de la ville.', 'La phrase du cahier.')
vf(AV, 3, 4, 'Le gardien fait partie des petits métiers.', True, 'Oui, comme le call box.')


# ─────────────────────────── vérifications ───────────────────────────

def verifier():
    titres = {l['titre']: len(l['notions']) for l in LECONS}
    cles = set()
    for l in LECONS:
        assert len(l['resume']) <= 400, l['titre']
        assert l['illustration'] not in cles
        cles.add(l['illustration'])
        for n in l['notions']:
            assert n['kind'] in ('definition', 'date', 'liste', 'relation'), n
            assert len(n['phrase']) <= 160, n['phrase']
            assert n['image'] not in cles, n['image']
            cles.add(n['image'])

    for r in Q:
        textes = json.dumps([r['payload'], r['answer'], r['explain']], ensure_ascii=False)
        assert "'" not in textes, 'apostrophe droite : ' + textes
        assert 1 <= r['rang'] <= titres[r['lecon']], r
        k, p, a = r['kind'], r['payload'], r['answer']
        if k == 'qcm' and 'images' in p:
            assert 2 <= len(p['images']) <= 4 and all(i in cles for i in p['images']), p
            assert 0 <= a['index'] < len(p['images'])
        elif k == 'qcm':
            assert 2 <= len(p['options']) <= 4 and len(set(p['options'])) == len(p['options']), p
            assert 0 <= a['index'] < len(p['options'])
            assert len(p['question']) <= 80, p['question']
        elif k == 'vrai_faux':
            assert isinstance(a['value'], bool) and len(p['statement']) <= 90, p
        elif k == 'association':
            assert len(p['gauche']) == len(p['droite']) == len(a['order'])
            assert 2 <= len(p['gauche']) <= 4
        elif k == 'texte_a_trous':
            assert p['text'].count('{{') == len(a['values']) == p['blanks'], p
        elif k == 'dictee':
            assert p['phrase'] == a['phrase'] and len(p['phrase'].split()) <= 10, p
        elif k == 'chronologie':
            assert sorted(a['order']) == list(range(len(p['tokens'])))
        else:
            raise AssertionError(k)
        if r['level'] == 4:
            assert k in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + k

    # Chaque notion doit pouvoir franchir les quatre étapes.
    for titre, total in titres.items():
        for rang in range(1, total + 1):
            niveaux = {r['level'] for r in Q if r['lecon'] == titre and r['rang'] == rang}
            assert niveaux >= {1, 2, 3, 4}, 'notion %s #%d : manque %s' % (titre, rang, {1, 2, 3, 4} - niveaux)
    return len(cles)


if __name__ == '__main__':
    images_a_produire = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sortie = {
        'lecons': [
            {**{k: v for k, v in l.items() if k != 'notions'},
             'prompt': STYLE + l['prompt'],
             'notions': [{'kind': n['kind'], 'statement': n['phrase'], 'illustration': n['image'],
                          'illustration_prompt': STYLE + n['prompt'],
                          'explications': [{'register': r, 'body': b} for r, b in n['expl']]}
                         for n in l['notions']]}
            for l in LECONS
        ],
        'questions': Q,
    }
    io.open(os.path.join(racine, 'work', 'lecons-brayne.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(sortie, ensure_ascii=False, indent=1))

    par_type = {}
    for r in Q:
        c = 'image' if (r['kind'] == 'qcm' and 'images' in r['payload']) else r['kind']
        par_type[c] = par_type.get(c, 0) + 1
    print('%d leçons · %d notions · %d questions · %d images'
          % (len(LECONS), sum(len(l['notions']) for l in LECONS), len(Q), images_a_produire))
    print('  ' + ', '.join('%s %d' % kv for kv in sorted(par_type.items())))
