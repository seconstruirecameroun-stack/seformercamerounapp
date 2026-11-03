# -*- coding: utf-8 -*-
"""
Les droits de l-enfant — ECM, BRAYNE (CM1), mardi 3 novembre 2026.

Une seule leçon : le cahier n-en pose qu-une, d-un seul jour, sous un seul
titre. La découper en deux ferait deux leçons de trois notions dont aucune
ne tiendrait debout toute seule.

La difficulté de cette leçon n-est pas de retenir trois droits, c-est de ne
pas les confondre. « Le nom », « la nationalité », « l-identité » se
ressemblent par les mots, et un enfant qui les récite dans l-ordre peut
être incapable de dire lequel relie à une famille. Les questions sont donc
construites pour **séparer**, pas pour réciter : à chaque fois qu-un droit
est demandé, les deux autres sont dans les mauvaises réponses.

Une remarque d-honnêteté sur le contenu. Le cahier range les trois droits
sous l-article 7 de la C.D.E. Dans le texte de la Convention, l-article 7
porte le nom et la nationalité, et l-identité relève de l-article 8. La
leçon suit le cahier, parce que c-est le cahier qui sera interrogé — mais
aucune question ne porte sur le numéro d-article attaché à l-identité en
particulier. Là où la classe et le texte divergent, on n-interroge pas.

Usage :  python work/lecons-brayne-ecm.py
"""

import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-ecm.py. '

MATIERE = 'ECM'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'fr'
CHAPITRE = 'Droits et devoirs'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

LECONS = [
    (
        'Les droits de l’enfant', CHAPITRE, '2026-11-03', 26,
        'Les droits de l’enfant sont protégés par l’article 7 de la C.D.E, la Convention '
        'Internationale des Droits de l’Enfant. Parmi eux : le droit au nom, qui relie l’enfant '
        'à une famille de sang ou adoptive ; le droit à la nationalité, qui le rattache à un '
        'pays ; et le droit à l’identité, qui renseigne sur le nom, la nationalité, la date et '
        'le lieu de naissance, le sexe et les parents.',
        'dr-droits-couv',
        'Trois cartes sous un même bandeau d’article : une étiquette, la carte du Cameroun, un acte de naissance.',
        [
            (
                'definition',
                'Les droits de l’enfant sont protégés par l’article 7 de la C.D.E.',
                'dr-article7',
                'Un livre ouvert, le mot ARTICLE et un grand 7 sur la page de droite, un signet rouge.',
                [
                    ('simple', 'Un article, c’est un paragraphe numéroté dans un texte de loi. Celui-ci porte le numéro 7.'),
                    ('analogie', 'Comme un article du règlement de l’école, mais signé par des pays entiers.'),
                ],
                [
                    ('qcm', 1, {'question': 'Quel article protège les droits de l’enfant ?',
                                'options': ['L’article 7', 'L’article 3', 'L’article 12']},
                     {'index': 0}, 'L’article 7, comme le dit le cahier.'),
                    ('vrai_faux', 1, {'statement': 'Les droits de l’enfant sont protégés par l’article 7.'},
                     {'value': True}, 'Oui.'),
                    ('qcm', 2, {'question': 'Les droits de l’enfant sont protégés par…',
                                'options': ['l’article 7 de la C.D.E', 'une décision du maire',
                                            'le règlement de l’école']},
                     {'index': 0}, 'Par l’article 7 de la C.D.E.'),
                    ('texte_a_trous', 3,
                     {'text': 'Les droits de l’enfant sont protégés par l’{{1}} 7 de la C.D.E.', 'blanks': 1},
                     {'values': ['article']}, 'L’article 7.'),
                    ('vrai_faux', 4,
                     {'statement': 'Les droits de l’enfant sont protégés par l’article 7 du règlement de l’école.'},
                     {'value': False}, 'Non : l’article 7 de la C.D.E, pas celui d’un règlement d’école.'),
                ],
            ),
            (
                'definition',
                'C.D.E veut dire Convention Internationale des Droits de l’Enfant.',
                'dr-cide',
                'Un livret bleu portant C.D.E sur une bande blanche, avec un sceau doré.',
                [
                    ('simple', 'Une convention, c’est un accord que des pays signent ensemble et s’engagent à respecter.'),
                    ('visuel', 'Sur la figure, le sceau doré en bas : c’est lui qui fait qu’un papier protège.'),
                ],
                [
                    ('qcm', 1, {'question': 'Que veut dire C.D.E ?',
                                'options': ['Convention Internationale des Droits de l’Enfant',
                                            'Code des Droits de l’École',
                                            'Conseil des Directeurs et des Élèves']},
                     {'index': 0}, 'Convention Internationale des Droits de l’Enfant.'),
                    ('vrai_faux', 1,
                     {'statement': 'La C.D.E est la Convention Internationale des Droits de l’Enfant.'},
                     {'value': True}, 'Oui.'),
                    ('association', 2, {'question': 'Relie chaque lettre au mot qu’elle remplace.',
                                        'gauche': ['C', 'D', 'E'],
                                        'droite': ['Convention', 'Droits', 'Enfant']},
                     {'order': [0, 1, 2]}, 'C comme Convention, D comme Droits, E comme Enfant.'),
                    ('texte_a_trous', 3,
                     {'text': 'La C.D.E est la {{1}} Internationale des Droits de l’Enfant.', 'blanks': 1},
                     {'values': ['Convention']}, 'Convention.'),
                    ('qcm', 4, {'question': 'Dans C.D.E, que désigne la lettre E ?',
                                'options': ['L’Enfant', 'L’École', 'L’État']},
                     {'index': 0}, 'E comme Enfant.'),
                ],
            ),
            (
                'definition',
                'Le nom relie l’enfant à une famille, qu’elle soit de sang ou adoptive.',
                'dr-nom',
                'Une étiquette portant NOM, une flèche, et une maison : le nom relie à une famille.',
                [
                    ('simple', 'Ton nom dit de quelle famille tu es. C’est ce qu’il sert d’abord à faire.'),
                    ('visuel', 'Sur la figure, la flèche va de l’étiquette à la maison : du nom vers la famille.'),
                    ('pas_a_pas', 'Un enfant naît. On lui donne un nom. Ce nom le rattache à sa famille, de sang ou adoptive.'),
                ],
                [
                    ('qcm', 1, {'question': 'À quoi le nom relie-t-il l’enfant ?',
                                'options': ['À une famille', 'À un pays', 'À une école']},
                     {'index': 0}, 'À une famille.'),
                    ('vrai_faux', 1, {'statement': 'Le nom relie l’enfant à une famille.'},
                     {'value': True}, 'Oui.'),
                    ('qcm', 2, {'question': 'La famille à laquelle le nom relie peut être…',
                                'options': ['de sang ou adoptive', 'seulement de sang',
                                            'seulement adoptive']},
                     {'index': 0}, 'Le cahier dit bien : de sang ou adoptive.'),
                    ('texte_a_trous', 3, {'text': 'Le nom relie l’enfant à une {{1}}.', 'blanks': 1},
                     {'values': ['famille']}, 'Une famille.'),
                    ('vrai_faux', 4,
                     {'statement': 'Un enfant adopté n’est relié à aucune famille par son nom.'},
                     {'value': False}, 'Non. Une famille adoptive est une famille, le cahier le précise.'),
                ],
            ),
            (
                'definition',
                'La nationalité rattache l’enfant au pays de ses parents ou à celui dans lequel il est né.',
                'dr-nationalite',
                'Un enfant, une flèche, et la carte du Cameroun : la nationalité rattache à un pays.',
                [
                    ('simple', 'La nationalité dit de quel pays tu es. Le nom dit la famille, la nationalité dit le pays.'),
                    ('visuel', 'Même image que pour le nom, mais la flèche ne va pas au même endroit : elle va au pays.'),
                    ('analogie', 'Deux enfants d’une même classe peuvent avoir le même pays et des familles différentes.'),
                ],
                [
                    ('qcm', 1, {'question': 'À quoi la nationalité rattache-t-elle l’enfant ?',
                                'options': ['À un pays', 'À une famille', 'À une école']},
                     {'index': 0}, 'À un pays. C’est le nom qui relie à la famille.'),
                    ('vrai_faux', 1, {'statement': 'La nationalité rattache l’enfant à un pays.'},
                     {'value': True}, 'Oui.'),
                    ('qcm', 2, {'question': 'La nationalité rattache l’enfant au pays…',
                                'options': ['de ses parents, ou celui où il est né',
                                            'de son école', 'de ses voisins']},
                     {'index': 0}, 'Celui de ses parents, ou celui dans lequel il est né.'),
                    ('texte_a_trous', 3, {'text': 'La nationalité rattache l’enfant à un {{1}}.', 'blanks': 1},
                     {'values': ['pays']}, 'Un pays.'),
                    ('vrai_faux', 4,
                     {'statement': 'La nationalité peut venir du pays des parents ou du pays de naissance.'},
                     {'value': True}, 'Oui, le cahier donne les deux cas.'),
                ],
            ),
            (
                'liste',
                'L’identité renseigne sur le nom, la nationalité, la date et le lieu de naissance, le sexe de l’enfant et ses parents.',
                'dr-identite',
                'Un acte de naissance avec une photo et ses cinq lignes : nom, nationalité, date et lieu, sexe, parents.',
                [
                    ('simple', 'L’identité rassemble tout ce qui dit qui tu es. Le nom et la nationalité en font partie.'),
                    ('visuel', 'Sur la figure, les lignes de l’acte de naissance se comptent : il y en a cinq.'),
                    ('analogie', 'C’est ce qu’on recopie sur un acte de naissance quand on t’inscrit à l’école.'),
                ],
                [
                    ('qcm', 1, {'question': 'Sur quoi l’identité renseigne-t-elle ?',
                                'options': ['Le nom, la nationalité, la naissance, le sexe, les parents',
                                            'La taille et le poids de l’enfant',
                                            'Les notes obtenues à l’école']},
                     {'index': 0}, 'Les cinq mentions du cahier.'),
                    ('vrai_faux', 1,
                     {'statement': 'L’identité renseigne sur le nom et la nationalité de l’enfant.'},
                     {'value': True}, 'Oui, parmi les cinq mentions.'),
                    ('qcm', 2, {'question': 'Combien de mentions le cahier donne-t-il pour l’identité ?',
                                'options': ['Cinq', 'Trois', 'Huit']},
                     {'index': 0}, 'Cinq : nom, nationalité, date et lieu, sexe, parents.'),
                    ('texte_a_trous', 3,
                     {'text': 'L’identité renseigne aussi sur le {{1}} de l’enfant.', 'blanks': 1},
                     {'values': ['sexe']}, 'Le sexe.'),
                    ('vrai_faux', 4, {'statement': 'L’identité d’un enfant ne dit rien de ses parents.'},
                     {'value': False}, 'Si : les parents font partie des cinq mentions.'),
                ],
            ),
            (
                'relation',
                'Parmi les droits de l’enfant figurent le droit au nom, le droit à la nationalité et le droit à l’identité.',
                'dr-trois',
                'Les trois droits en trois bandes numérotées : une famille, un pays, cinq mentions.',
                [
                    ('simple', 'Trois droits, trois destinations : le nom va à la famille, la nationalité au pays, l’identité à tout le reste.'),
                    ('pas_a_pas', 'Demande-toi : « cela relie à qui ? » Famille, c’est le nom. Pays, c’est la nationalité.'),
                    ('visuel', 'Sur la figure, les trois bandes sont numérotées 1, 2, 3 sous un même article.'),
                ],
                [
                    ('qcm', 1, {'question': 'Lequel de ces trois est un droit de l’enfant ?',
                                'options': ['Le droit au nom', 'Le droit de conduire',
                                            'Le droit de voter']},
                     {'index': 0}, 'Le droit au nom, cité par le cahier.'),
                    ('association', 2, {'question': 'Relie chaque droit à ce qu’il fait.',
                                        'gauche': ['Le nom', 'La nationalité', 'L’identité'],
                                        'droite': ['Relie à une famille', 'Rattache à un pays',
                                                   'Donne cinq mentions']},
                     {'order': [0, 1, 2]}, 'Famille, pays, cinq mentions : c’est ce qui les sépare.'),
                    ('qcm', 2, {'question': 'Quel droit rattache l’enfant à un pays ?',
                                'options': ['Le droit à la nationalité', 'Le droit au nom',
                                            'Le droit à l’identité']},
                     {'index': 0}, 'La nationalité.'),
                    ('texte_a_trous', 3, {'text': 'Le droit au {{1}} relie l’enfant à une famille.', 'blanks': 1},
                     {'values': ['nom']}, 'Le nom.'),
                    ('qcm', 4, {'question': 'Quel droit relie l’enfant à une famille ?',
                                'options': ['Le droit au nom', 'Le droit à la nationalité',
                                            'Le droit à l’identité']},
                     {'index': 0}, 'Le nom. La nationalité, elle, rattache à un pays.'),
                ],
            ),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total = set(), 0
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 400, 'résumé trop long (%d) : %s' % (len(resume), titre)
        assert img not in cles, 'image en double : ' + img
        cles.add(img)
        for kind, phrase, nimg, nprompt, expl, items in notions:
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 180, 'notion trop longue : ' + phrase
            assert nimg not in cles, 'image en double : ' + nimg
            cles.add(nimg)
            for registre, corps in expl:
                assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), registre
                assert len(corps) <= 200, 'explication trop longue : ' + corps
            niveaux = set()
            for ikind, niveau, payload, answer, explain in items:
                total += 1
                niveaux.add(niveau)
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, 'question trop longue : ' + payload['question']
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 70, 'option trop longue : ' + o
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']), payload['statement'])
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        # Le clavier n-a pas de touche espace dans un texte à
                        # trous, ni de chiffres : une réponse en deux mots ou
                        # un numéro serait impossible à taper.
                        assert ' ' not in v, 'réponse en plusieurs mots : ' + v
                        assert v.replace('’', '').isalpha(), 'réponse non tapable : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    # Les trois droits se ressemblent par les mots : c-est leur confusion
    # qu-on révise. Chaque fois qu-on demande l-un d-eux, les deux autres
    # doivent être proposés — sinon la bonne réponse se devine sans savoir.
    # Un droit se reconnaît soit à son nom, soit à sa destination : « le
    # nom » et « une famille » désignent la même chose pour l-enfant.
    CONCEPTS = {
        'nom': ('nom', 'famille'),
        'nationalite': ('nationalité', 'pays'),
        'identite': ('identité', 'mentions'),
    }
    separateurs = 0
    for _t, _c, _d, _o, _r, _i, _p, notions in LECONS:
        for _k, _ph, _ni, _np, _ex, items in notions:
            for ikind, _lv, payload, _an, _exp in items:
                if ikind != 'qcm':
                    continue
                # Une option qui cite DEUX droits à la fois ne sépare rien :
                # elle les range ensemble. Seules comptent les options qui
                # désignent un seul des trois, et il en faut deux.
                vus = set()
                for o in payload['options']:
                    bas = o.lower()
                    touche = {c for c, ms in CONCEPTS.items() if any(m in bas for m in ms)}
                    if len(touche) == 1:
                        vus |= touche
                if len(vus) >= 2:
                    separateurs += 1
    assert separateurs >= 4, 'trop peu de questions qui séparent les trois droits : %d' % separateurs
    return len(cles), total, separateurs


def paquet():
    return {
        'matiere': MATIERE, 'classe': CLASSE, 'enfant': ENFANT, 'lang': LANGUE,
        'lecons': [
            {
                'title': titre, 'chapter': chapitre, 'taught_on': date, 'sort_order': ordre,
                'summary': resume, 'illustration': img, 'illustration_prompt': FIGURE + prompt,
                'notions': [
                    {
                        'kind': k, 'statement': p, 'illustration': ni,
                        'illustration_prompt': FIGURE + npr,
                        'explanations': [{'register': r, 'body': b} for r, b in ex],
                        'items': [{'kind': ik, 'level': lv, 'payload': pl,
                                   'answer': an, 'explain': exp}
                                  for ik, lv, pl, an, exp in it],
                    }
                    for k, p, ni, npr, ex, it in notions
                ],
            }
            for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS
        ],
    }


if __name__ == '__main__':
    images, items, separateurs = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-ecm.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    notions = sum(len(l[7]) for l in LECONS)
    print('%d lecon - %d notions - %d questions - %d images - %d questions qui separent'
          % (len(LECONS), notions, items, images, separateurs))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-30s %s  %d notions' % (titre, date, len(ns)))
    print(chemin)
