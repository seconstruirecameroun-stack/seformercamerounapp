# -*- coding: utf-8 -*-
"""
Unit 13 — Wood work and building : le cours d'anglais de KLEIN (CE1),
lundi 2 novembre 2026, et les deux endroits où il a trébuché.

Le père a photographié le manuel ET le cahier d'exercices rempli. Les
leçons qui suivent ne sortent donc pas du programme : elles sortent de ses
fautes, relevées une à une.

  Exercise 13 E — 1 bonne réponse sur 5. Il a échangé builder et
  carpenter, et il a mis « carver » partout ailleurs :

      He arranges blocks to make a wall  → il a écrit Carpenter (builder)
      He makes tables out of wood        → il a écrit builder   (carpenter)
      He puts roofs on houses            → il a écrit builder   (carpenter)
      He uses a trowel                   → il a écrit Carver    (builder)

  Exercise 13 D — « Use the following adjectives to construct sentences ».
  Devant Heavy, Beautiful, Short et young, il a écrit « Heaves »,
  « mort Beautiful », « Shorter », « younger ». Il n'a pas construit de
  phrases : il a donné des comparatifs. Il a lu la consigne de travers.

Ces deux fautes commandent tout le reste. La première leçon oppose les
trois métiers phrase par phrase, avec les cinq énoncés exacts de
l'exercice. La deuxième distingue l'adjectif de son comparatif avant même
de parler de common et proper.

Tout est en anglais, y compris les explications : c'est dans cette langue
qu'il sera interrogé, et un enfant d'école bilingue n'a pas besoin qu'on
lui traduise « a sharp trowel ». La dictée parle anglais elle aussi —
langue 'en' dans le payload, sinon la voix du navigateur lirait les
phrases avec un accent français.

Une incohérence du cahier, signalée et non recopiée : le texte de
l'Exercise 13 A parle de « my sister Bih », et la question 2 demande
« What does Ngwa my brother do ? ». Le frère n'existe nulle part dans le
texte. Rien ici ne s'appuie sur ce prénom.

Usage :  python work/lecons-klein-anglais.py
"""

import io
import json
import os

FIGURE = 'Figure composée, non générée, dessinée par work/figures-anglais.py. '

MATIERE = 'Anglais'
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'en'

LECONS = [
    (
        'Builder, carpenter and carver', 'Unit 13 — Wood work and building',
        '2026-11-02', 16,
        'A builder builds houses with bricks, cement and sand. A carpenter makes things out of '
        'wood: chairs, doors, cupboards, tables and shelves, and he puts roofs on houses. A wood '
        'carver carves wood to make things like mortars. Each one has his own tools.',
        'an-metiers',
        'Trois cartouches côte à côte : builder, carpenter, carver, chacun avec son outil.',
        [
            (
                'definition',
                'A builder builds houses. He works with bricks, cement, sand and a trowel.',
                'an-builder',
                'Un mur de briques en cours de montage, avec une truelle posée dessus.',
                [
                    ('simple', 'The builder works with bricks and cement. He builds walls and houses.'),
                    ('visuel', 'Think of Mr. Tulsy in your book: he builds houses in the village.'),
                ],
                [
                    ('qcm', 1, {'question': 'What does a builder build?',
                                'options': ['Houses', 'Tables', 'Mortars']},
                     {'index': 0}, 'A builder builds houses.'),
                    ('qcm', 1, {'question': 'A builder works with…',
                                'options': ['bricks and cement', 'wood only', 'paper']},
                     {'index': 0}, 'Bricks, cement and sand.'),
                    ('qcm', 2, {'question': 'He arranges blocks to make a wall. Who is he?',
                                'options': ['A builder', 'A carpenter', 'A carver', 'A teacher']},
                     {'index': 0}, 'Blocks and walls are the builder.'),
                    ('texte_a_trous', 3, {'text': 'A {{1}} builds houses with {{2}}.', 'blanks': 2},
                     {'values': ['builder', 'bricks']}, 'A builder builds houses with bricks.'),
                    ('vrai_faux', 4, {'statement': 'A builder makes tables out of wood.'},
                     {'value': False}, 'That is the carpenter.'),
                ],
            ),
            (
                'definition',
                'A carpenter makes things out of wood: chairs, doors, cupboards, tables and shelves.',
                'an-carpenter',
                'Une table et une étagère en bois, avec une scie posée à côté.',
                [
                    ('simple', 'The carpenter works with wood. He makes furniture for the house.'),
                    ('pas_a_pas', 'He cuts the wood with a saw, joins it with nails and a hammer, then it becomes a table.'),
                ],
                [
                    ('qcm', 1, {'question': 'What does a carpenter work with?',
                                'options': ['Wood', 'Cement', 'Stones']},
                     {'index': 0}, 'A carpenter works with wood.'),
                    ('qcm', 1, {'question': 'He makes tables out of wood. Who is he?',
                                'options': ['A carpenter', 'A builder', 'A carver']},
                     {'index': 0}, 'Tables out of wood: the carpenter.'),
                    ('qcm', 2, {'question': 'He puts roofs on houses. Who is he?',
                                'options': ['A carpenter', 'A builder', 'A carver', 'A driver']},
                     {'index': 0}, 'Roofing is the carpenter in your book.'),
                    ('texte_a_trous', 3,
                     {'text': 'A {{1}} makes chairs, doors and {{2}} out of wood.', 'blanks': 2},
                     {'values': ['carpenter', 'tables']}, 'A carpenter makes tables.'),
                    ('vrai_faux', 4, {'statement': 'A carpenter can put a roof on a house.'},
                     {'value': True}, 'Yes, his services are needed for roofing.'),
                ],
            ),
            (
                'definition',
                'A wood carver carves wood to make things like mortars. He uses a flat chisel and gouges.',
                'an-carver',
                'Un mortier en bois et une gouge à lame arrondie.',
                [
                    ('simple', 'The carver also works with wood, but he carves it. He makes mortars.'),
                    ('visuel', 'His gouges have rounded blades. The carpenter has straight ones.'),
                ],
                [
                    ('qcm', 1, {'question': 'What does a wood carver make?',
                                'options': ['Mortars', 'Walls', 'Cement']},
                     {'index': 0}, 'A carver makes mortars.'),
                    ('qcm', 1, {'question': 'He produces a mortar. Who is he?',
                                'options': ['A carver', 'A builder', 'A carpenter']},
                     {'index': 0}, 'The wood carver.'),
                    ('qcm', 2, {'question': 'The blades of a carver’s gouges are…',
                                'options': ['rounded', 'straight', 'square', 'broken']},
                     {'index': 0}, 'Rounded blades.'),
                    ('texte_a_trous', 3, {'text': 'A wood {{1}} makes a {{2}} out of wood.', 'blanks': 2},
                     {'values': ['carver', 'mortar']}, 'A wood carver makes a mortar.'),
                    ('vrai_faux', 4, {'statement': 'A carver uses cement.'},
                     {'value': False}, 'He uses wood. Cement is for the builder.'),
                ],
            ),
            (
                'relation',
                'The builder uses a trowel; the carpenter uses a saw and a hammer; the carver uses a flat chisel.',
                'an-outils',
                'Trois outils alignés et étiquetés : trowel, saw, gouge.',
                [
                    ('simple', 'One tool, one trade. The trowel spreads cement, the saw cuts wood.'),
                    ('pas_a_pas', 'Ask yourself: is it for cement or for wood? Cement means builder. Wood means carpenter or carver.'),
                ],
                [
                    ('qcm', 1, {'question': 'He uses a trowel. Who is he?',
                                'options': ['A builder', 'A carpenter', 'A carver']},
                     {'index': 0}, 'The trowel spreads cement: the builder.'),
                    ('qcm', 1, {'question': 'What is a saw used for?',
                                'options': ['To cut wood', 'To spread cement', 'To carry sand']},
                     {'index': 0}, 'The carpenter cuts wood with a saw.'),
                    ('qcm', 2, {'question': 'What does the builder spread with a trowel?',
                                'options': ['Cement', 'Wood', 'Nails', 'Paint']},
                     {'index': 0}, 'He spreads cement.'),
                    ('association', 3, {'question': 'Match each worker to his tool.',
                                        'gauche': ['builder', 'carpenter', 'carver'],
                                        'droite': ['a trowel', 'a saw', 'a gouge']},
                     {'order': [0, 1, 2]}, 'Trowel, saw, gouge.'),
                    ('vrai_faux', 4, {'statement': 'A carpenter uses a trowel to cut wood.'},
                     {'value': False}, 'He uses a saw. The trowel is the builder’s.'),
                ],
            ),
            (
                'liste',
                'The carpenter’s tools: a saw, a hammer, a chisel, nails, tapes and a planing machine.',
                'an-boite',
                'Une boîte à outils ouverte avec marteau, scie, ciseau et clous.',
                [
                    ('simple', 'Six tools from the passage. All of them work on wood.'),
                    ('visuel', 'The hammer sends the nail into the wood; the chisel cuts.'),
                ],
                [
                    ('qcm', 1, {'question': 'What do you use to send a nail into wood?',
                                'options': ['A hammer', 'A saw', 'A trowel']},
                     {'index': 0}, 'The hammer.'),
                    ('qcm', 1, {'question': 'Which one is a carpenter’s tool?',
                                'options': ['A saw', 'A wheelbarrow', 'A spade']},
                     {'index': 0}, 'The saw. The other two are the builder’s.'),
                    ('qcm', 2, {'question': 'Which tool is NOT in the carpenter’s box?',
                                'options': ['A wheelbarrow', 'A hammer', 'Nails', 'A saw']},
                     {'index': 0}, 'The wheelbarrow carries sand: it is the builder’s.'),
                    ('texte_a_trous', 3,
                     {'text': 'I use the {{1}} to send the nail into the {{2}}.', 'blanks': 2},
                     {'values': ['hammer', 'wood']}, 'The hammer, into the wood.'),
                    ('vrai_faux', 4, {'statement': 'Nails are used by the carpenter.'},
                     {'value': True}, 'With a hammer.'),
                ],
            ),
            (
                'relation',
                'Both the carpenter and the carver use a chisel, but the carver’s chisel is flat and his gouges are rounded.',
                'an-chisel',
                'Deux ciseaux côte à côte : une lame droite, une lame arrondie.',
                [
                    ('simple', 'Same name, two tools. That is why the boy in the book takes the wrong one.'),
                    ('histoire', 'In Exercise 13 A, he is sent for his uncle’s chisel and brings his sister’s by mistake.'),
                ],
                [
                    ('qcm', 1, {'question': 'Who uses a chisel?',
                                'options': ['The carpenter and the carver', 'The builder only',
                                            'Nobody']},
                     {'index': 0}, 'Both of them.'),
                    ('qcm', 1, {'question': 'What do you use a chisel for?',
                                'options': ['To cut', 'To carry water', 'To measure']},
                     {'index': 0}, 'To cut wood or stone.'),
                    ('qcm', 2, {'question': 'How do you know the carver’s chisel?',
                                'options': ['It is flat', 'It is longer', 'It is red', 'It is heavy']},
                     {'index': 0}, 'Flat, with rounded gouges.'),
                    ('texte_a_trous', 3,
                     {'text': 'The carver uses a flat {{1}} and gouges with {{2}} blades.', 'blanks': 2},
                     {'values': ['chisel', 'rounded']}, 'A flat chisel, rounded blades.'),
                    ('vrai_faux', 4,
                     {'statement': 'The carpenter and the carver have exactly the same chisel.'},
                     {'value': False}, 'They look alike, but they are not the same.'),
                ],
            ),
            (
                'liste',
                'Saw and sand have one syllable. Ham-mer, chi-sel, tro-wel and tim-ber have two.',
                'an-syllabes',
                'Quatre mots coupés en deux morceaux, et deux mots entiers.',
                [
                    ('simple', 'Clap your hands once for saw, twice for ham-mer.'),
                    ('visuel', 'One clap is monosyllabic. Two claps is disyllabic.'),
                ],
                [
                    ('qcm', 1, {'question': 'How many syllables are there in “hammer”?',
                                'options': ['Two', 'One', 'Three']},
                     {'index': 0}, 'Ham-mer: two.'),
                    ('qcm', 1, {'question': 'How many syllables are there in “saw”?',
                                'options': ['One', 'Two', 'Four']},
                     {'index': 0}, 'Saw: one.'),
                    ('qcm', 2, {'question': 'Which word has only one syllable?',
                                'options': ['sand', 'timber', 'trowel', 'chisel']},
                     {'index': 0}, 'Sand. The others have two.'),
                    ('chronologie', 3, {'question': 'Put the two parts of the word in order.',
                                        'tokens': ['tro', 'wel'],
                                        'consigne': 'Touch the parts in the right order.'},
                     {'order': [0, 1]}, 'tro-wel.'),
                    ('vrai_faux', 4, {'statement': 'Timber is a disyllabic word.'},
                     {'value': True}, 'Tim-ber: two syllables.'),
                ],
            ),
        ],
    ),
    (
        'Kinds of adjectives', 'Unit 13 — Grammar', '2026-11-02', 17,
        'An adjective is a word that describes a noun or a pronoun. In a sentence it comes before '
        'the noun: a sharp trowel, a nice house. Common adjectives are not capitalized; proper '
        'adjectives come from the names of places and are capitalized: a Cameroonian carpenter.',
        'an-adjectifs',
        'Deux cartes : « a sharp trowel » et « a Cameroonian carpenter », le C en majuscule.',
        [
            (
                'definition',
                'An adjective is a word that describes a noun or a pronoun.',
                'an-adjectif',
                'Un nom au centre, et trois adjectifs qui pointent vers lui.',
                [
                    ('simple', 'An adjective tells you how the thing is: big, old, sharp, nice.'),
                    ('visuel', 'A house is a noun. A nice house: nice is the adjective.'),
                ],
                [
                    ('qcm', 1, {'question': 'An adjective describes…',
                                'options': ['a noun', 'a number', 'a day']},
                     {'index': 0}, 'A noun or a pronoun.'),
                    ('qcm', 1, {'question': 'In “a sharp trowel”, which word is the adjective?',
                                'options': ['sharp', 'trowel', 'a']},
                     {'index': 0}, 'Sharp describes the trowel.'),
                    ('qcm', 2, {'question': 'In “My grandmother is an old woman”, the adjective is…',
                                'options': ['old', 'grandmother', 'woman', 'is']},
                     {'index': 0}, 'Old describes the woman.'),
                    ('texte_a_trous', 3,
                     {'text': 'An {{1}} is a word that describes a {{2}}.', 'blanks': 2},
                     {'values': ['adjective', 'noun']}, 'An adjective describes a noun.'),
                    ('vrai_faux', 4, {'statement': 'In “a big hammer”, big is the adjective.'},
                     {'value': True}, 'It describes the hammer.'),
                ],
            ),
            (
                'relation',
                'To use an adjective, put it in a sentence before the noun: “He has a heavy hammer.”',
                'an-phrase',
                'Une phrase complète, l’adjectif souligné, avec un point à la fin.',
                [
                    ('simple', 'A sentence needs a subject, a verb and a full stop. “Heavier” is not a sentence.'),
                    ('pas_a_pas', 'Take the adjective heavy. Who? The hammer. Say it: “The hammer is heavy.” That is a sentence.'),
                ],
                [
                    ('qcm', 1, {'question': 'Which one is a sentence?',
                                'options': ['The hammer is heavy.', 'Heavier', 'Heavy']},
                     {'index': 0}, 'A sentence has a subject and a verb.'),
                    ('qcm', 1, {'question': 'Which one is a sentence with “short”?',
                                'options': ['The nail is short.', 'Shorter', 'Short nail']},
                     {'index': 0}, 'Subject, verb, full stop.'),
                    ('qcm', 2, {'question': 'Is “younger” a sentence?',
                                'options': ['No, it is only a word', 'Yes', 'Yes, with a capital',
                                            'Yes, if it is long']},
                     {'index': 0}, 'One word is never a sentence.'),
                    ('texte_a_trous', 3,
                     {'text': 'The builder has a {{1}} house. The saw is {{2}}.', 'blanks': 2},
                     {'values': ['beautiful', 'sharp']}, 'Beautiful, and sharp.'),
                    ('vrai_faux', 4,
                     {'statement': 'To construct a sentence with “beautiful”, you write “more beautiful”.'},
                     {'value': False}, 'That is not a sentence. Say: “The house is beautiful.”'),
                ],
            ),
            (
                'liste',
                'Common adjectives are not capitalized: a big house, an old carpenter, a wet surface, a neat workshop.',
                'an-communs',
                'Quatre étiquettes en minuscules, posées sur fond clair.',
                [
                    ('simple', 'They are everyday words. They never take a capital letter.'),
                    ('visuel', 'big, old, wet, neat, rough, fine, good, bad, famous, important.'),
                ],
                [
                    ('qcm', 1, {'question': 'Common adjectives take…',
                                'options': ['no capital letter', 'always a capital', 'a number']},
                     {'index': 0}, 'No capital letter.'),
                    ('qcm', 1, {'question': 'Which one is a common adjective?',
                                'options': ['old', 'Nigerian', 'British']},
                     {'index': 0}, 'Old is a common adjective.'),
                    ('qcm', 2, {'question': 'Which one is written correctly?',
                                'options': ['a rough floor', 'a Rough floor', 'A rough Floor',
                                            'a ROUGH floor']},
                     {'index': 0}, 'No capital on a common adjective.'),
                    ('texte_a_trous', 3,
                     {'text': 'The carpenter has a {{1}} saw and a {{2}} workshop.', 'blanks': 2},
                     {'values': ['sharp', 'neat']}, 'A sharp saw, a neat workshop.'),
                    ('vrai_faux', 4, {'statement': 'We write “an Old carpenter”.'},
                     {'value': False}, 'Old is common: no capital.'),
                ],
            ),
            (
                'liste',
                'Proper adjectives come from the names of places and are capitalized: a Cameroonian carpenter, a Nigerian builder, the British Consul.',
                'an-propres',
                'Trois étiquettes avec une majuscule nette en tête de mot.',
                [
                    ('simple', 'They come from a country or a place, so they keep the capital letter.'),
                    ('pas_a_pas', 'Cameroon gives Cameroonian. Nigeria gives Nigerian. Britain gives British.'),
                ],
                [
                    ('qcm', 1, {'question': 'Proper adjectives come from…',
                                'options': ['names of places', 'numbers', 'colours']},
                     {'index': 0}, 'From proper nouns, mostly places.'),
                    ('qcm', 1, {'question': 'Which one is a proper adjective?',
                                'options': ['Cameroonian', 'beautiful', 'heavy']},
                     {'index': 0}, 'Cameroonian comes from Cameroon.'),
                    ('qcm', 2, {'question': 'Which one is written correctly?',
                                'options': ['a Nigerian builder', 'a nigerian builder',
                                            'A nigerian Builder', 'a NIGERIAN builder']},
                     {'index': 0}, 'A proper adjective keeps its capital.'),
                    ('texte_a_trous', 3,
                     {'text': 'A {{1}} carpenter comes from Cameroon. A {{2}} builder comes from Nigeria.',
                      'blanks': 2},
                     {'values': ['Cameroonian', 'Nigerian']}, 'Cameroonian, Nigerian.'),
                    ('vrai_faux', 4, {'statement': 'We write “a cameroonian carpenter”.'},
                     {'value': False}, 'It needs a capital C.'),
                ],
            ),
        ],
    ),
    (
        'Numbers 251 to 300', 'Unit 13 — Numbers', '2026-11-02', 18,
        'Numbers from 251 to 300 are read “two hundred and fifty-one”, “two hundred and fifty-two”, '
        'and so on, up to “three hundred”. The tens and the units are joined by a hyphen: '
        'fifty-one, sixty-four, ninety-nine.',
        'an-nombres',
        'Trois tuiles 2 5 1 et le mot « two hundred and fifty-one » dessous.',
        [
            (
                'relation',
                'We read 251 as “two hundred and fifty-one”.',
                'an-lire',
                'Le nombre 251 et sa lecture en mots, reliés par une flèche.',
                [
                    ('simple', 'First the hundreds, then “and”, then the tens and the units.'),
                    ('pas_a_pas', '2 gives two hundred. Then and. Then 51 gives fifty-one.'),
                ],
                [
                    ('qcm', 1, {'question': 'How do you read 251?',
                                'options': ['Two hundred and fifty-one', 'Twenty-five one',
                                            'Two fifty one']},
                     {'index': 0}, 'Two hundred and fifty-one.'),
                    ('qcm', 1, {'question': 'Which word comes after “two hundred”?',
                                'options': ['and', 'the', 'of']},
                     {'index': 0}, 'Two hundred and…'),
                    ('qcm', 2, {'question': 'How do you read 274?',
                                'options': ['Two hundred and seventy-four', 'Two hundred seventy four',
                                            'Two seventy-four', 'Twenty-seven four']},
                     {'index': 0}, 'Two hundred and seventy-four.'),
                    ('dictee', 3, {'phrase': 'Two hundred and fifty-one.', 'langue': 'en'},
                     {'phrase': 'Two hundred and fifty-one.'}, 'Mind the hyphen in fifty-one.'),
                    ('vrai_faux', 4, {'statement': '300 is read “three hundred”.'},
                     {'value': True}, 'Three hundred, with no “and”.'),
                ],
            ),
            (
                'liste',
                'The tens and the units are joined by a hyphen: fifty-one, sixty-four, ninety-nine.',
                'an-trait',
                'Trois mots composés, le trait d’union mis en relief.',
                [
                    ('simple', 'Fifty and one become one word with a small line between them.'),
                    ('visuel', 'fifty-one, sixty-four, ninety-nine. Never fifty one.'),
                ],
                [
                    ('qcm', 1, {'question': 'Which one is written correctly?',
                                'options': ['fifty-one', 'fifty one', 'fiftyone']},
                     {'index': 0}, 'With a hyphen.'),
                    ('qcm', 1, {'question': 'What joins the tens and the units?',
                                'options': ['A hyphen', 'A comma', 'A full stop']},
                     {'index': 0}, 'A hyphen.'),
                    ('qcm', 2, {'question': 'How do you write 296 in words?',
                                'options': ['Two hundred and ninety-six', 'Two hundred and ninety six',
                                            'Two hundred ninety-six', 'Two ninety-six']},
                     {'index': 0}, 'And, plus a hyphen.'),
                    ('texte_a_trous', 3,
                     {'text': '259 is two hundred and {{1}}. 282 is two hundred and {{2}}.',
                      'blanks': 2},
                     {'values': ['fifty-nine', 'eighty-two']}, 'Fifty-nine, eighty-two.'),
                    ('vrai_faux', 4, {'statement': 'We write “two hundred and sixty four”.'},
                     {'value': False}, 'It needs a hyphen: sixty-four.'),
                ],
            ),
            (
                'relation',
                'After two hundred and ninety-nine comes three hundred.',
                'an-trois-cents',
                'La suite 298, 299, 300, la dernière tuile mise en avant.',
                [
                    ('simple', 'The numbers stop at three hundred in this lesson.'),
                    ('visuel', '299 then 300. Three hundred is written without “and”.'),
                ],
                [
                    ('qcm', 1, {'question': 'What comes after 299?',
                                'options': ['300', '298', '400']},
                     {'index': 0}, 'Three hundred.'),
                    ('qcm', 1, {'question': 'How do you read 300?',
                                'options': ['Three hundred', 'Three hundred and', 'Thirty hundred']},
                     {'index': 0}, 'Three hundred.'),
                    ('qcm', 2, {'question': 'What comes just before 300?',
                                'options': ['Two hundred and ninety-nine', 'Two hundred and ninety',
                                            'Three hundred and one', 'Two hundred']},
                     {'index': 0}, '299 comes just before.'),
                    ('chronologie', 3, {'question': 'Put these numbers in order.',
                                        'tokens': ['251', '274', '299', '300'],
                                        'consigne': 'Touch them from the smallest to the biggest.'},
                     {'order': [0, 1, 2, 3]}, 'From 251 to 300.'),
                    ('vrai_faux', 4, {'statement': 'We write “three hundred and”.'},
                     {'value': False}, 'Just three hundred.'),
                ],
            ),
        ],
    ),
]

NIVEAUX_ATTENDUS = {1, 2, 3, 4}


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total = set(), 0
    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 400, 'résumé trop long : ' + titre
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
                    assert len(payload['statement']) <= 110, payload
                elif ikind == 'texte_a_trous':
                    trous = payload['text'].count('{{')
                    assert trous == len(answer['values']) == payload['blanks'], payload
                    assert trous <= 2, 'plus de deux trous : ' + payload['text']
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie' else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'association':
                        assert len(payload['gauche']) == len(payload['droite']), payload
                elif ikind == 'dictee':
                    assert payload['phrase'] == answer['phrase'], payload
                    # Sans cela, la voix du navigateur lirait l-anglais avec
                    # un accent français, et la dictée serait inécoutable.
                    assert payload.get('langue') == LANGUE, 'dictée sans langue anglaise : ' + str(payload)
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))
    return len(cles), total


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
    images, items = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-anglais.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    notions = sum(len(l[7]) for l in LECONS)
    print('%d lecons - %d notions - %d questions - %d images'
          % (len(LECONS), notions, items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %-32s %-34s %s  %d notions' % (titre, chapitre, date, len(ns)))
    print(chemin)
