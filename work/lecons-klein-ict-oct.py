# -*- coding: utf-8 -*-
"""
Cinq leçons d-ICT pour KLEIN (CE1) — son cahier d-anglais informatique,
cinq pages du 8 septembre au 20 octobre 2026.

CE N-EST PAS UN DOUBLON DE SA TIC FRANÇAISE, et il faut le dire parce que
cela en a l-air. Son école enseigne la même matière dans LES DEUX LANGUES,
avec deux cahiers, deux maîtres et deux épreuves. Les sept leçons entrées
hier sont son cours français ; ces cinq-ci sont son cours anglais. Le
recouvrement est réel sur deux points - les outils locaux et modernes, et
le téléphone - mais ce qu-on lui demandera, ce sont les MOTS ANGLAIS :
equipment, transmit, distances, device, to register, to schedule.

Les lessons sont donc rangées dans la même matière TIC, avec des chapitres
en anglais : elles se retrouvent à côté des françaises, et la langue de
chaque leçon dit laquelle est laquelle.

CE QUE LE CAHIER ANGLAIS AJOUTE, et que le français n-avait pas :

  les trois DIFFÉRENCES entre outils locaux et modernes - la distance, le
  village ou la ville, l-électricité. Le cahier français les opposait sans
  jamais dire en quoi ils diffèrent

  les USAGES des outils locaux, un par un : la cloche donne l-heure, le
  sifflet sert aux sports et à régler la circulation, le tambour parleur
  et le gong font les annonces

  les six usages du TÉLÉPHONE et les trois familles d-usages de
  l-ORDINATEUR - l-école, le divertissement et le commerce, l-hôpital

LE MVET EST GARDÉ. Le cahier le range parmi les outils locaux, et c-est
juste : c-est une harpe-cithare traditionnelle du Cameroun. Un enfant de
Yaoundé doit le reconnaître dans une liste où figurent la flûte et le
xylophone.

Usage :  python work/lecons-klein-ict-oct.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-klein-ict-oct.py. ')

MATIERE = 'TIC'
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

EQUIPEMENT = 'ICT equipment'
LOCAUX = 'Local ICT tools'
MACHINES = 'The telephone and the computer'

LECONS = [
    # ------------------------------------------------------------------ 54
    (
        'ICT equipment', EQUIPEMENT, '2026-09-08', 54,
        'I.C.T means Information and Communication Technology. ICT equipments are the various '
        'tools used for communication, and there are two types: the local or traditional tools, '
        'and the modern tools.',
        'ki-eq-couv',
        'Un tambour, une radio et un écran alignés.',
        [
            ('definition',
             'I.C.T means Information and Communication Technology.',
             'ki-eq-ict',
             'Les trois morceaux de I.C.T : Information and, Communication, Technology.',
             [('simple', 'Three words, three letters. The small word « and » takes no letter.'),
              ('visuel', 'Read the first letter of each big word: I, C, T.')],
             [('qcm', 1, {'question': 'What does I.C.T mean?',
                          'options': ['Information and Communication Technology',
                                      'Information and Computer Tools',
                                      'Internet and Camera Technology']},
               {'index': 0}, 'Information and Communication Technology.'),
              ('vrai_faux', 1, {'statement': 'The T of I.C.T stands for Technology.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'I.C.T means Information and {{1}} Technology.', 'blanks': 1},
               {'values': ['communication']}, 'Communication.'),
              ('qcm', 3, {'question': 'Which word is the C of I.C.T?',
                          'options': ['Communication', 'Computer', 'Camera']},
               {'index': 0}, 'Communication.'),
              ('vrai_faux', 4, {'statement': 'The C of I.C.T stands for Computer.'},
               {'value': False}, 'No: Communication.')]),

            ('definition',
             'ICT equipments are the various tools used for communication. There are two types: '
             'the local tools and the modern tools.',
             'ki-eq-deux',
             'Deux paires reliées : local tools et the old ones, modern tools et the new ones.',
             [('simple', 'Equipment means the tools you use to do something.'),
              ('visuel', 'Two types: the old ones of the village, and the new ones.')],
             [('qcm', 1, {'question': 'What are ICT equipments used for?',
                          'options': ['For communication', 'For cooking', 'For farming']},
               {'index': 0}, 'For communication.'),
              ('vrai_faux', 1, {'statement': 'There are two types of ICT equipment.'},
               {'value': True}, 'Local tools and modern tools.'),
              ('texte_a_trous', 2,
               {'text': 'ICT equipments are tools used for {{1}}.', 'blanks': 1},
               {'values': ['communication']}, 'For communication.'),
              ('qcm', 3, {'question': 'How many types of ICT equipment are there?',
                          'options': ['Two', 'Three', 'Five']},
               {'index': 0}, 'Two: local and modern.'),
              ('vrai_faux', 4, {'statement': 'ICT equipments are used to carry water.'},
               {'value': False}, 'No. They are used for communication.')]),

            ('liste',
             'The local or traditional tools are the gong, the flute, the whistle, the trumpet, '
             'the xylophone and the mvet.',
             'ki-eq-locaux',
             'Trois lignes portant les six outils locaux du cahier.',
             [('simple', 'They are made by hand, and they need no electricity.'),
              ('histoire', 'The mvet is a traditional stringed instrument of Cameroon. It is '
                           'played at the village, and it tells long stories.')],
             [('qcm', 1, {'question': 'Which one is a local ICT tool?',
                          'options': ['The gong', 'The camera', 'The radio']},
               {'index': 0}, 'The gong.'),
              ('vrai_faux', 1, {'statement': 'The mvet is a local ICT tool.'},
               {'value': True}, 'Yes, it is a traditional instrument of Cameroon.'),
              ('texte_a_trous', 2,
               {'text': 'The gong, the flute and the mvet are {{1}} tools.', 'blanks': 1},
               {'values': ['local']}, 'Local tools.'),
              ('qcm', 3, {'question': 'Which one is not a local tool?',
                          'options': ['The television', 'The trumpet', 'The xylophone']},
               {'index': 0}, 'The television is a modern tool.'),
              ('vrai_faux', 4, {'statement': 'A local tool needs electricity.'},
               {'value': False}, 'No. It is played by hand or by mouth.')]),

            ('liste',
             'The modern tools are the computer, the television, the camera, the radio and the '
             'telephone.',
             'ki-eq-modernes',
             'Une radio et un ordinateur dessinés, nommés chacun.',
             [('simple', 'They are made in a factory, and most of them need electricity.'),
              ('visuel', 'They carry a message much further than a gong.')],
             [('qcm', 1, {'question': 'Which one is a modern ICT tool?',
                          'options': ['The camera', 'The flute', 'The gong']},
               {'index': 0}, 'The camera.'),
              ('vrai_faux', 1, {'statement': 'The telephone is a modern ICT tool.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The computer and the radio are {{1}} tools.', 'blanks': 1},
               {'values': ['modern']}, 'Modern tools.'),
              ('association', 3, {'question': 'Match each tool with its type.',
                                  'gauche': ['the gong', 'the television', 'the flute'],
                                  'droite': ['local', 'modern', 'local too']},
               {'order': [0, 1, 2]}, 'Two local, one modern.'),
              ('vrai_faux', 4, {'statement': 'The xylophone is a modern ICT tool.'},
               {'value': False}, 'No, it is a local one.')]),
        ],
    ),

    # ------------------------------------------------------------------ 55
    (
        'Uses of local ICT tools', LOCAUX, '2026-09-22', 55,
        'Each local ICT tool has its own use. The bell tells the time. The whistle is used for '
        'sports and games, and to control traffic. The talking drum and the gong are used to '
        'make an announcement.',
        'ki-us-couv',
        'Une cloche, un sifflet et un tambour alignés.',
        [
            ('relation',
             'The bell is used to tell the time.',
             'ki-us-cloche',
             'Une cloche dessinée, nommée.',
             [('simple', 'At school, the bell rings and the lesson begins.'),
              ('visuel', 'Everyone hears it at the same moment: that is why it tells the '
                         'time.')],
             [('qcm', 1, {'question': 'What is the bell used for?',
                          'options': ['To tell the time', 'To control traffic',
                                      'To make an announcement']},
               {'index': 0}, 'To tell the time.'),
              ('vrai_faux', 1, {'statement': 'The bell tells the time.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The bell is used to tell the {{1}}.', 'blanks': 1},
               {'values': ['time']}, 'The time.'),
              ('qcm', 3, {'question': 'At school, what does the bell say?',
                          'options': ['That the lesson begins', 'That it is raining',
                                      'That the food is ready']},
               {'index': 0}, 'That the lesson begins or ends.'),
              ('vrai_faux', 4, {'statement': 'The bell is used to control traffic.'},
               {'value': False}, 'No, that is the whistle.')]),

            ('relation',
             'The whistle is used for sports and games, and to control traffic.',
             'ki-us-sifflet',
             'Un sifflet dessiné, nommé.',
             [('simple', 'The referee blows it, and the game stops or starts.'),
              ('visuel', 'The policeman blows it too, and the cars stop.')],
             [('qcm', 1, {'question': 'What is the whistle used for?',
                          'options': ['For sports and games', 'To tell the time',
                                      'To send a letter']},
               {'index': 0}, 'For sports and games, and to control traffic.'),
              ('vrai_faux', 1, {'statement': 'The whistle is used to control traffic.'},
               {'value': True}, 'Yes, the policeman blows it.'),
              ('texte_a_trous', 2,
               {'text': 'The whistle is used for sports and {{1}}.', 'blanks': 1},
               {'values': ['games']}, 'Sports and games.'),
              ('qcm', 3, {'question': 'Who blows a whistle to stop the cars?',
                          'options': ['The policeman', 'The teacher', 'The farmer']},
               {'index': 0}, 'The policeman, to control traffic.'),
              ('vrai_faux', 4, {'statement': 'The whistle is used to make an announcement.'},
               {'value': False}, 'No, that is the drum and the gong.')]),

            ('relation',
             'The talking drum and the gong are used to make an announcement.',
             'ki-us-tambour',
             'Un tambour parleur dessiné, nommé.',
             [('simple', 'An announcement is a message said to everybody at once.'),
              ('histoire', 'In the village, the gong calls the meeting: everyone knows there is '
                           'news to hear.')],
             [('qcm', 1, {'question': 'What are the drum and the gong used for?',
                          'options': ['To make an announcement', 'To tell the time',
                                      'To control traffic']},
               {'index': 0}, 'To make an announcement.'),
              ('vrai_faux', 1, {'statement': 'The talking drum makes an announcement.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The drum and the gong make an {{1}}.', 'blanks': 1},
               {'values': ['announcement']}, 'An announcement.'),
              ('association', 3, {'question': 'Match each tool with its use.',
                                  'gauche': ['the bell', 'the whistle', 'the gong'],
                                  'droite': ['to tell the time', 'for sports',
                                             'to make an announcement']},
               {'order': [0, 1, 2]}, 'Time, sports, announcement.'),
              ('vrai_faux', 4, {'statement': 'An announcement is said to one person only.'},
               {'value': False}, 'No, to everybody at once.')]),
        ],
    ),

    # ------------------------------------------------------------------ 56
    (
        'Local and modern ICT tools: the differences', LOCAUX, '2026-09-29', 56,
        'Local tools transmit information over short distances, are mostly used in villages, and '
        'are non-electronic. Modern tools transmit information over long distances, are mostly '
        'used in towns, and are electronic devices.',
        'ki-di-couv',
        'Trois cartes alignées : distance, place, electricity.',
        [
            ('relation',
             'Local tools transmit information over short distances. Modern tools transmit it '
             'over long distances.',
             'ki-di-distance',
             'Deux paires reliées : local et short distances, modern et long distances.',
             [('simple', 'You hear a gong from the next field. A radio is heard from another '
                         'town.'),
              ('visuel', 'Transmit means: carry the message from here to there.')],
             [('qcm', 1, {'question': 'How far does a local tool carry the message?',
                          'options': ['Over short distances', 'Over long distances',
                                      'All over the world']},
               {'index': 0}, 'Over short distances.'),
              ('vrai_faux', 1,
               {'statement': 'Modern tools transmit information over long distances.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Local tools transmit information over {{1}} distances.', 'blanks': 1},
               {'values': ['short']}, 'Short distances.'),
              ('qcm', 3, {'question': 'What does transmit mean?',
                          'options': ['To carry the message', 'To write the message',
                                      'To hide the message']},
               {'index': 0}, 'To carry it from here to there.'),
              ('vrai_faux', 4,
               {'statement': 'A gong carries a message further than a radio.'},
               {'value': False}, 'No. The radio goes much further.')]),

            ('relation',
             'Local tools are mostly used in villages. Modern tools are mostly used in towns.',
             'ki-di-lieu',
             'Deux paires reliées : local et in villages, modern et in towns.',
             [('simple', 'Mostly means: most of the time, but not always.'),
              ('visuel', 'In the village, the gong. In the town, the telephone.')],
             [('qcm', 1, {'question': 'Where are local tools mostly used?',
                          'options': ['In villages', 'In towns', 'At the hospital']},
               {'index': 0}, 'In villages.'),
              ('vrai_faux', 1, {'statement': 'Modern tools are mostly used in towns.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Local tools are mostly used in {{1}}.', 'blanks': 1},
               {'values': ['villages']}, 'In villages.'),
              ('qcm', 3, {'question': 'What does mostly mean?',
                          'options': ['Most of the time', 'Never', 'Only once']},
               {'index': 0}, 'Most of the time, but not always.'),
              ('vrai_faux', 4, {'statement': 'A modern tool can never be used in a village.'},
               {'value': False}, 'It can. But most of the time it is used in towns.')]),

            ('relation',
             'Local tools are non-electronic, like the xylophone. Modern tools are electronic '
             'devices, like the telephone and the radio.',
             'ki-di-electronique',
             'Deux paires reliées : le xylophone non-electronic, la radio electronic.',
             [('simple', 'Non-electronic means: it works without electricity.'),
              ('visuel', 'A device is a machine made to do one thing.')],
             [('qcm', 1, {'question': 'What does non-electronic mean?',
                          'options': ['It works without electricity', 'It is very old',
                                      'It is very small']},
               {'index': 0}, 'It works without electricity.'),
              ('vrai_faux', 1, {'statement': 'The radio is an electronic device.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The xylophone is a {{1}} tool: it needs no electricity.', 'blanks': 1},
               {'values': ['local']}, 'A local tool.'),
              ('association', 3, {'question': 'Match each difference with the local tools.',
                                  'gauche': ['the distance', 'the place', 'the electricity'],
                                  'droite': ['short', 'villages', 'none']},
               {'order': [0, 1, 2]}, 'Short distances, villages, no electricity.'),
              ('vrai_faux', 4, {'statement': 'The telephone is non-electronic.'},
               {'value': False}, 'No, it is an electronic device.')]),
        ],
    ),

    # ------------------------------------------------------------------ 57
    (
        'The telephone', MACHINES, '2026-10-20', 57,
        'The telephone is a modern ICT tool used to communicate with people at a distance. There '
        'are two types: fixed telephones and mobile telephones. It is used for calls, messages, '
        'calculating, music, research, movies, pictures and games.',
        'ki-te-couv',
        'Un téléphone portable dessiné, en grand.',
        [
            ('definition',
             'The telephone is a modern ICT tool used to communicate with people at a distance. '
             'There are two types: fixed and mobile telephones.',
             'ki-te-def',
             'Un téléphone dessiné, nommé, avec ses deux types.',
             [('simple', 'A fixed telephone stays on the table. A mobile one goes in your '
                         'pocket.'),
              ('visuel', 'At a distance means: the other person is far away.')],
             [('qcm', 1, {'question': 'How many types of telephone are there?',
                          'options': ['Two', 'Three', 'One']},
               {'index': 0}, 'Two: fixed and mobile.'),
              ('vrai_faux', 1, {'statement': 'A mobile telephone can be carried about.'},
               {'value': True}, 'Yes, that is why it is called mobile.'),
              ('texte_a_trous', 2,
               {'text': 'There are two types of telephone: fixed and {{1}}.', 'blanks': 1},
               {'values': ['mobile']}, 'Mobile telephones.'),
              ('qcm', 3, {'question': 'What is the telephone used for?',
                          'options': ['To communicate at a distance', 'To cook the food',
                                      'To carry the water']},
               {'index': 0}, 'To communicate with people at a distance.'),
              ('vrai_faux', 4, {'statement': 'The telephone is a local ICT tool.'},
               {'value': False}, 'No, it is a modern one.')]),

            ('liste',
             'The telephone is used for making calls, and for sending and receiving messages.',
             'ki-te-appels',
             'Trois lignes : making calls, sending messages, receiving messages.',
             [('simple', 'You send a message; the other person receives it.'),
              ('visuel', 'A call is heard; a message is read.')],
             [('qcm', 1, {'question': 'What is the first use of a telephone?',
                          'options': ['Making calls', 'Watching movies',
                                      'Snapping pictures']},
               {'index': 0}, 'Making calls.'),
              ('vrai_faux', 1, {'statement': 'A telephone can send and receive messages.'},
               {'value': True}, 'Yes, both.'),
              ('texte_a_trous', 2,
               {'text': 'The telephone is used for making {{1}}.', 'blanks': 1},
               {'values': ['calls']}, 'Making calls.'),
              ('qcm', 3, {'question': 'You write to a friend on the phone. You are…',
                          'options': ['sending a message', 'making a call',
                                      'playing a game']},
               {'index': 0}, 'Sending a message.'),
              ('vrai_faux', 4, {'statement': 'A telephone can only make calls.'},
               {'value': False}, 'No, it does many other things.')]),

            ('liste',
             'The telephone is also used for calculating, and for playing and listening to music.',
             'ki-te-musique',
             'Trois lignes : calculating, playing music, listening to music.',
             [('simple', 'A telephone holds a calculator inside it.'),
              ('visuel', 'It plays the music, and you listen to it.')],
             [('qcm', 1, {'question': 'What else is a telephone used for?',
                          'options': ['Calculating', 'Cooking', 'Washing']},
               {'index': 0}, 'Calculating.'),
              ('vrai_faux', 1, {'statement': 'You can listen to music on a telephone.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The telephone is used for playing and listening to {{1}}.',
                'blanks': 1},
               {'values': ['music']}, 'Music.'),
              ('qcm', 3, {'question': 'You need to add two numbers. What can you use?',
                          'options': ['The telephone', 'The whistle', 'The gong']},
               {'index': 0}, 'The telephone: it can calculate.'),
              ('vrai_faux', 4, {'statement': 'A telephone cannot calculate.'},
               {'value': False}, 'It can: calculating is one of its uses.')]),

            ('liste',
             'The telephone is used for research, watching movies, snapping pictures and playing '
             'games.',
             'ki-te-photos',
             'Quatre lignes : research, watching movies, snapping pictures, playing games.',
             [('simple', 'To snap a picture is to take a photograph.'),
              ('visuel', 'Research means: looking for what you do not know yet.')],
             [('qcm', 1, {'question': 'What does to snap a picture mean?',
                          'options': ['To take a photograph', 'To break the phone',
                                      'To draw with a pen']},
               {'index': 0}, 'To take a photograph.'),
              ('vrai_faux', 1, {'statement': 'A telephone can be used for research.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The telephone is used for snapping {{1}}.', 'blanks': 1},
               {'values': ['pictures']}, 'Snapping pictures.'),
              ('qcm', 3, {'question': 'You look for an answer on the phone. You are doing…',
                          'options': ['research', 'a call', 'a game']},
               {'index': 0}, 'Research.'),
              ('vrai_faux', 4, {'statement': 'Watching movies is a use of the telephone.'},
               {'value': True}, 'Yes, the cahier lists it.')]),
        ],
    ),

    # ------------------------------------------------------------------ 58
    (
        'The computer and its uses', MACHINES, '2026-10-20', 58,
        'A computer is an electronic device used to process, store and send information. In '
        'school it registers pupils, processes exams and results, and helps pupils to learn. It '
        'also entertains, calculates salaries in business, and keeps patients records.',
        'ki-co-couv',
        'Un écran et une unité centrale alignés.',
        [
            ('definition',
             'A computer is an electronic device used to process, store and send information.',
             'ki-co-def',
             'Trois lignes : it processes, it stores, it sends information.',
             [('simple', 'Three verbs to remember: process, store, send.'),
              ('visuel', 'A device is a machine made to do a job.')],
             [('qcm', 1, {'question': 'What is a computer?',
                          'options': ['An electronic device', 'A local ICT tool',
                                      'A kind of drum']},
               {'index': 0}, 'An electronic device.'),
              ('vrai_faux', 1, {'statement': 'A computer stores information.'},
               {'value': True}, 'Yes, and it processes and sends it too.'),
              ('texte_a_trous', 2,
               {'text': 'A computer is used to process, {{1}} and send information.',
                'blanks': 1},
               {'values': ['store']}, 'To store information.'),
              ('qcm', 3, {'question': 'Which one is not what a computer does?',
                          'options': ['It cooks the food', 'It stores information',
                                      'It sends information']},
               {'index': 0}, 'A computer does not cook.'),
              ('vrai_faux', 4, {'statement': 'A computer is a non-electronic tool.'},
               {'value': False}, 'No, it is an electronic device.')]),

            ('liste',
             'In school, the computer is used to register pupils, to process exams and results, '
             'to do research, and to help teachers and pupils to learn.',
             'ki-co-ecole',
             'Quatre lignes : register pupils, process exams, do research, help pupils to learn.',
             [('simple', 'To register a pupil is to write his name on the school list.'),
              ('visuel', 'Your own results were processed by a computer.')],
             [('qcm', 1, {'question': 'What does the computer do in school?',
                          'options': ['It registers pupils', 'It rings the bell',
                                      'It sweeps the floor']},
               {'index': 0}, 'It registers pupils.'),
              ('vrai_faux', 1, {'statement': 'The computer processes exams and results.'},
               {'value': True}, 'Yes, in school.'),
              ('texte_a_trous', 2,
               {'text': 'In school, the computer is used to {{1}} pupils.', 'blanks': 1},
               {'values': ['register']}, 'To register pupils.'),
              ('qcm', 3, {'question': 'What does to register mean?',
                          'options': ['To write a name on a list', 'To ring a bell',
                                      'To clean a room']},
               {'index': 0}, 'To write a name on a list.'),
              ('vrai_faux', 4,
               {'statement': 'The computer helps teachers and pupils to learn.'},
               {'value': True}, 'Yes, that is one of its uses in school.')]),

            ('liste',
             'The computer also helps to entertain, for example by watching movies, and in '
             'business, to calculate salaries.',
             'ki-co-aide',
             'Deux paires reliées : to entertain et watching movies, in business et salaries.',
             [('simple', 'To entertain is to give pleasure: a film, a song, a game.'),
              ('visuel', 'A salary is the money paid for work.')],
             [('qcm', 1, {'question': 'What does to entertain mean?',
                          'options': ['To give pleasure', 'To count money', 'To write a list']},
               {'index': 0}, 'To give pleasure.'),
              ('vrai_faux', 1, {'statement': 'In business, the computer calculates salaries.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'In business, the computer calculates {{1}}.', 'blanks': 1},
               {'values': ['salaries']}, 'Salaries.'),
              ('qcm', 3, {'question': 'What is a salary?',
                          'options': ['The money paid for work', 'A kind of exam',
                                      'A sort of computer']},
               {'index': 0}, 'The money paid for work.'),
              ('vrai_faux', 4, {'statement': 'Watching a movie is a way of entertaining.'},
               {'value': True}, 'Yes.')]),

            ('liste',
             'In hospitals, the computer is used to store patients records and to schedule '
             'doctors and nurses.',
             'ki-co-hopital',
             'Trois lignes : store patients records, schedule doctors, and nurses.',
             [('simple', 'A record is everything written about one patient.'),
              ('visuel', 'To schedule is to say who works, and when.')],
             [('qcm', 1, {'question': 'What does the computer store in a hospital?',
                          'options': ['Patients records', 'The medicines', 'The beds']},
               {'index': 0}, 'Patients records.'),
              ('vrai_faux', 1,
               {'statement': 'In hospitals, the computer schedules doctors and nurses.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'In hospitals, the computer stores patients {{1}}.', 'blanks': 1},
               {'values': ['records']}, 'Patients records.'),
              ('qcm', 3, {'question': 'What does to schedule mean?',
                          'options': ['To say who works and when', 'To pay the salary',
                                      'To clean the room']},
               {'index': 0}, 'To say who works, and when.'),
              ('vrai_faux', 4, {'statement': 'A record is everything written about a patient.'},
               {'value': True}, 'Yes.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues, trous = set(), 0, 0, 0
    titres = [l[0] for l in LECONS]
    assert len(set(titres)) == len(titres), 'titre en double'
    rangs = [l[3] for l in LECONS]
    assert len(set(rangs)) == len(rangs), 'rang en double'

    for titre, chapitre, date, ordre, resume, img, prompt, notions in LECONS:
        assert len(resume) <= 400, 'résumé trop long (%d) : %s' % (len(resume), titre)
        assert date is None or len(date) == 10, date
        assert img not in cles, 'image en double : ' + img
        cles.add(img)
        for kind, phrase, nimg, nprompt, expl, items in notions:
            notions_vues += 1
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 180, 'notion trop longue (%d) : %s' % (len(phrase), phrase)
            assert nimg not in cles, 'image en double : ' + nimg
            cles.add(nimg)
            for registre, corps in expl:
                assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), \
                    registre
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
                    assert len(payload['question']) <= 90, \
                        'question trop longue (%d) : %s' % (len(payload['question']),
                                                            payload['question'])
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(options), payload
                    for o in options:
                        assert len(o) <= 70, 'option trop longue : ' + o
                    bonne = len(options[answer['index']])
                    autres = [len(o) for k, o in enumerate(options) if k != answer['index']]
                    assert bonne <= max(autres) * 2, \
                        'bonne réponse bien plus longue que les autres : ' + payload['question']
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']),
                                                               payload['statement'])
                elif ikind == 'texte_a_trous':
                    trous += 1
                    n = payload['text'].count('{{')
                    assert n == len(answer['values']) == payload['blanks'], payload
                    assert n <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        assert v == v.strip() != '', 'réponse mal cadrée : ' + repr(v)
                        assert set(v) <= TAPABLE, 'réponse non tapable au clavier : ' + v
                elif ikind in ('chronologie', 'association'):
                    longueur = len(payload['tokens'] if ikind == 'chronologie'
                                   else payload['gauche'])
                    assert sorted(answer['order']) == list(range(longueur)), payload
                    if ikind == 'chronologie':
                        assert len(set(payload['tokens'])) == longueur, \
                            'jeton en double : ' + str(payload['tokens'])
                    else:
                        assert len(payload['gauche']) == len(payload['droite']), payload
                        assert len(set(payload['droite'])) == len(payload['droite']), \
                            'deux étiquettes identiques à droite : ' + str(payload['droite'])
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-klein-ict-oct.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    manquantes = cles - dessinees
    inutiles = dessinees - cles
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(
        sorted(manquantes))
    assert not inutiles, 'images dessinées mais jamais utilisées : ' + ', '.join(sorted(inutiles))
    return len(cles), total, notions_vues, trous


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
    images, items, notions, trous = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin = os.path.join(racine, 'app', 'public', 'seed-klein-ict-oct.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-44s %s  %d notions  %d questions'
              % (ordre, titre, date, len(ns), sum(len(n[5]) for n in ns)))
    print(chemin)
