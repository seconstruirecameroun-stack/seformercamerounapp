# -*- coding: utf-8 -*-
"""
Neuf leçons d-informatique pour BRAYNE (CM1) — son cahier de TIC d-octobre
2026, treize pages photographiées le 9 novembre au soir.

LA MATIÈRE ÉTAIT VIDE. « TIC » existe dans sa classe depuis le début, avec
sa couleur, et pas une seule leçon n-y était rangée. Les quatre séances du
cahier - le 6, le 16, le 23 et le 30 octobre - sont donc reprises en
entier, et c-est la première fois qu-il aura de l-informatique à réviser.

L-ANGLAIS EST CELUI DU CAHIER. Tout y est écrit en anglais, jusqu-aux mots
qu-on lui demandera de restituer : input, output, storage, extension,
Caps Lock. Traduire lui ferait réviser un vocabulaire qu-on ne lui
demandera pas.

UNE FAUTE DU CAHIER, ÉCARTÉE, et c-est la seule.

Page de la frappe, point 3 : « The Space bar. It is used to separate
words. It is also called the Shift key. » Les deux phrases ne vont pas
ensemble : la barre d-espace et la touche Shift sont DEUX touches
différentes, qu-il a sous les doigts et peut voir à vingt centimètres de
lui. La barre d-espace sépare les mots ; la touche Shift sert aux
majuscules. La leçon enseigne cela, et une notion entière porte la
différence - c-est le seul endroit où elle contredit le cahier, et le père
en est averti dans work/brayne-revision-notes.md.

CE QUI EST GARDÉ TEL QUEL, même si cela se discute :

  « les premiers ordinateurs étaient l-abaque et la Pascaline » - ce sont
  des machines à calculer plus que des ordinateurs, mais c-est le cadrage
  de l-école et c-est ce qu-on lui demandera

  « une extension de trois lettres » - vrai des six extensions du cahier
  (doc, jpg, mp3, mp4, xls, mdb), moins vrai aujourd-hui où docx en a
  quatre. La leçon dit trois, comme le cahier, et l-explication dit qu-il
  en existe de quatre

La Pascaline de 1642, elle, est juste : Blaise Pascal, dix-neuf ans.

Usage :  python work/lecons-brayne-tic-oct.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-tic-oct.py. ')

MATIERE = 'TIC'
CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'en'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

PERIPH = 'Computer peripherals'
OUTILS = 'ICT tools'
SECU = 'Security'
FICHIERS = 'Files'
FRAPPE = 'Typing'
EDITION = 'Editing'

LECONS = [
    # ------------------------------------------------------------------ 79
    (
        'Computer peripherals', PERIPH, '2026-10-06', 79,
        'Computer peripherals are of three types. Input peripherals send data into the computer, '
        'like the keyboard and the mouse. Output peripherals send information out of it, like the '
        'monitor and the printer. Storage peripherals keep the information, like the USB key.',
        'bt-pe-couv',
        'Quatre objets alignés : un clavier, un écran, une imprimante, une clé USB.',
        [
            ('definition',
             'Computer peripherals are of three types: input peripherals, output peripherals and '
             'storage peripherals.',
             'bt-pe-trois',
             'Trois lignes : data goes in, information goes out, it is kept.',
             [('simple', 'In, out, and kept. Three directions, three types.'),
              ('pas_a_pas', 'Ask yourself where the data goes: into the computer, out of it, or '
                            'nowhere because it stays.')],
             [('qcm', 1, {'question': 'How many types of computer peripherals are there?',
                          'options': ['Three', 'Two', 'Five']},
               {'index': 0}, 'Three: input, output and storage.'),
              ('vrai_faux', 1,
               {'statement': 'Input, output and storage are the three types of peripherals.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Computer peripherals are of {{1}} types.', 'blanks': 1},
               {'values': ['three']}, 'Three types.'),
              ('qcm', 3, {'question': 'Which one is not a type of peripheral?',
                          'options': ['Reading peripherals', 'Input peripherals',
                                      'Storage peripherals']},
               {'index': 0}, 'There is no reading peripheral.'),
              ('vrai_faux', 4, {'statement': 'A peripheral is a part of the human body.'},
               {'value': False}, 'No. It is a device used with a computer.')]),

            ('definition',
             'Input peripherals are devices used to send data or instructions into a computer: '
             'the keyboard, the mouse, the scanner, the microphone.',
             'bt-pe-entree',
             'Un clavier et une souris dessinés, nommés chacun.',
             [('simple', 'They carry what YOU say to the computer.'),
              ('visuel', 'You press, you click, you speak: it goes in.')],
             [('qcm', 1, {'question': 'What does an input peripheral do?',
                          'options': ['It sends data into the computer',
                                      'It sends information out', 'It keeps the information']},
               {'index': 0}, 'It sends data in.'),
              ('vrai_faux', 1, {'statement': 'The keyboard is an input peripheral.'},
               {'value': True}, 'Yes: it sends what you type into the computer.'),
              ('texte_a_trous', 2,
               {'text': 'A device that sends data into a computer is an {{1}} peripheral.',
                'blanks': 1},
               {'values': ['input']}, 'An input peripheral.'),
              ('qcm', 3, {'question': 'Which one is an input peripheral?',
                          'options': ['The microphone', 'The printer', 'The monitor']},
               {'index': 0}, 'The microphone sends your voice in.'),
              ('vrai_faux', 4, {'statement': 'The mouse is an output peripheral.'},
               {'value': False}, 'No, it is an input peripheral.')]),

            ('definition',
             'Output peripherals are devices that send information out of a computer: the '
             'monitor, the printer, the projector, the speaker.',
             'bt-pe-sortie',
             'Un écran et une imprimante dessinés, nommés chacun.',
             [('simple', 'They carry what the COMPUTER says to you.'),
              ('visuel', 'You read it, you hear it, you hold it on paper: it came out.')],
             [('qcm', 1, {'question': 'What does an output peripheral do?',
                          'options': ['It sends information out of the computer',
                                      'It sends data into the computer',
                                      'It keeps the information']},
               {'index': 0}, 'It sends information out.'),
              ('vrai_faux', 1, {'statement': 'The printer is an output peripheral.'},
               {'value': True}, 'Yes: the page comes out of the computer.'),
              ('texte_a_trous', 2,
               {'text': 'A device that sends information out is an {{1}} peripheral.',
                'blanks': 1},
               {'values': ['output']}, 'An output peripheral.'),
              ('qcm', 3, {'question': 'Which one is an output peripheral?',
                          'options': ['The speaker', 'The scanner', 'The keyboard']},
               {'index': 0}, 'The speaker: the sound comes out.'),
              ('vrai_faux', 4, {'statement': 'The projector sends data into the computer.'},
               {'value': False}, 'No, it sends the picture out.')]),

            ('definition',
             'Storage peripherals are devices that store or keep information: the memory card, '
             'the USB key, the flash drive, the compact disk.',
             'bt-pe-stockage',
             'Une clé USB dessinée, nommée.',
             [('simple', 'They hold the information when the computer is off.'),
              ('analogie', 'A storage peripheral is a bag: it carries what you wrote from one '
                           'computer to another.')],
             [('qcm', 1, {'question': 'What does a storage peripheral do?',
                          'options': ['It keeps the information',
                                      'It sends data into the computer',
                                      'It prints the information']},
               {'index': 0}, 'It stores or keeps it.'),
              ('vrai_faux', 1, {'statement': 'The USB key is a storage peripheral.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'A device that keeps information is a {{1}} peripheral.', 'blanks': 1},
               {'values': ['storage']}, 'A storage peripheral.'),
              ('association', 3, {'question': 'Match each device with its type.',
                                  'gauche': ['the mouse', 'the monitor', 'the memory card'],
                                  'droite': ['input', 'output', 'storage']},
               {'order': [0, 1, 2]}, 'In, out, kept.'),
              ('vrai_faux', 4, {'statement': 'The compact disk is a storage peripheral.'},
               {'value': True}, 'Yes, it keeps what is written on it.')]),
        ],
    ),

    # ------------------------------------------------------------------ 80
    (
        'RAM, ROM, USB and ICT', PERIPH, '2026-10-06', 80,
        'Four short words come back in every lesson. RAM means Random Access Memory. ROM means '
        'Read Only Memory. USB means Universal Serial Bus. And ICT means Information and '
        'Communication Technology.',
        'bt-ab-couv',
        'Quatre cartes alignées : RAM, ROM, USB, ICT.',
        [
            ('definition',
             'RAM means Random Access Memory. It is the memory the computer works in while it is '
             'switched on.',
             'bt-ab-ram',
             'Les trois mots de RAM, posés ligne à ligne : Random, Access, Memory.',
             [('simple', 'Three words, three letters: Random, Access, Memory.'),
              ('visuel', 'Read the first letter of each word, and you have RAM.')],
             [('qcm', 1, {'question': 'What does RAM mean?',
                          'options': ['Random Access Memory', 'Read Access Memory',
                                      'Rapid Access Machine']},
               {'index': 0}, 'Random Access Memory.'),
              ('vrai_faux', 1, {'statement': 'The R of RAM stands for Random.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'RAM means {{1}} Access Memory.', 'blanks': 1},
               {'values': ['random']}, 'Random Access Memory.'),
              ('qcm', 3, {'question': 'Which word is the M of RAM?',
                          'options': ['Memory', 'Machine', 'Mouse']},
               {'index': 0}, 'Memory.'),
              ('vrai_faux', 4, {'statement': 'RAM means Read Access Memory.'},
               {'value': False}, 'No: Random. Read is the R of ROM.')]),

            ('definition',
             'ROM means Read Only Memory. What is written in it can be read, but not changed.',
             'bt-ab-rom',
             'Les trois mots de ROM, posés ligne à ligne : Read, Only, Memory.',
             [('simple', 'Read only: you may look, you may not write.'),
              ('visuel', 'ROM and RAM differ by one letter, and by one idea: read, or random.')],
             [('qcm', 1, {'question': 'What does ROM mean?',
                          'options': ['Read Only Memory', 'Random Only Memory',
                                      'Read Open Machine']},
               {'index': 0}, 'Read Only Memory.'),
              ('vrai_faux', 1, {'statement': 'The O of ROM stands for Only.'},
               {'value': True}, 'Yes: Read Only Memory.'),
              ('texte_a_trous', 2,
               {'text': 'ROM means Read {{1}} Memory.', 'blanks': 1},
               {'values': ['only']}, 'Read Only Memory.'),
              ('qcm', 3, {'question': 'In ROM, what can you not do?',
                          'options': ['Change what is written', 'Read what is written',
                                      'Switch the computer on']},
               {'index': 0}, 'You cannot change it: it is read only.'),
              ('vrai_faux', 4, {'statement': 'ROM and RAM mean the same thing.'},
               {'value': False}, 'No. One is read only, the other is random access.')]),

            ('definition',
             'USB means Universal Serial Bus. It is the name of the plug that joins a device to '
             'the computer.',
             'bt-ab-usb',
             'Les trois mots de USB, posés ligne à ligne : Universal, Serial, Bus.',
             [('simple', 'Universal: the same plug fits a key, a mouse, a printer.'),
              ('visuel', 'The USB key is called so because of its plug.')],
             [('qcm', 1, {'question': 'What does USB mean?',
                          'options': ['Universal Serial Bus', 'United Serial Bus',
                                      'Universal Simple Box']},
               {'index': 0}, 'Universal Serial Bus.'),
              ('vrai_faux', 1, {'statement': 'The U of USB stands for Universal.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'USB means Universal {{1}} Bus.', 'blanks': 1},
               {'values': ['serial']}, 'Universal Serial Bus.'),
              ('qcm', 3, {'question': 'Which word is the B of USB?',
                          'options': ['Bus', 'Box', 'Button']},
               {'index': 0}, 'Bus.'),
              ('vrai_faux', 4, {'statement': 'USB means Universal Simple Box.'},
               {'value': False}, 'No: Universal Serial Bus.')]),

            ('definition',
             'ICT means Information and Communication Technology. It is the name of the subject '
             'itself.',
             'bt-ab-ict',
             'Les trois morceaux de ICT : Information and, Communication, Technology.',
             [('simple', 'Information, Communication, Technology: the three words of the '
                         'subject.'),
              ('visuel', 'The small word « and » does not take a letter in the abbreviation.')],
             [('qcm', 1, {'question': 'What does ICT mean?',
                          'options': ['Information and Communication Technology',
                                      'Internet and Computer Technology',
                                      'Information and Computer Tools']},
               {'index': 0}, 'Information and Communication Technology.'),
              ('vrai_faux', 1, {'statement': 'The T of ICT stands for Technology.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'ICT means Information and {{1}} Technology.', 'blanks': 1},
               {'values': ['communication']}, 'Communication.'),
              ('association', 3, {'question': 'Match each abbreviation with its first word.',
                                  'gauche': ['RAM', 'ROM', 'USB'],
                                  'droite': ['Random', 'Read', 'Universal']},
               {'order': [0, 1, 2]}, 'The first letter gives the first word.'),
              ('vrai_faux', 4, {'statement': 'The C of ICT stands for Computer.'},
               {'value': False}, 'No: Communication.')]),
        ],
    ),

    # ------------------------------------------------------------------ 81
    (
        'Local and modern ICT tools', OUTILS, '2026-10-06', 81,
        'ICT tools are of two kinds. The local ones are the flute, the drum, the bell, the '
        'xylophone and the gong. The modern ones are the computer, the radio, the phone, the '
        'camera and the television. Each one has its own use.',
        'bt-lo-couv',
        'Un tambour, une radio et un écran alignés.',
        [
            ('liste',
             'The local ICT tools are the flute, the drum, the bell, the xylophone and the gong.',
             'bt-lo-locaux',
             'Un tambour dessiné, nommé.',
             [('simple', 'They carry a message without electricity: you hear them far away.'),
              ('analogie', 'In the village, the gong calls the meeting the way a phone calls a '
                           'friend.')],
             [('qcm', 1, {'question': 'Which one is a local ICT tool?',
                          'options': ['The drum', 'The camera', 'The computer']},
               {'index': 0}, 'The drum.'),
              ('vrai_faux', 1, {'statement': 'The gong is a local ICT tool.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The flute, the drum and the gong are {{1}} tools.', 'blanks': 1},
               {'values': ['local']}, 'Local tools.'),
              ('qcm', 3, {'question': 'Which one is not a local ICT tool?',
                          'options': ['The television', 'The bell', 'The xylophone']},
               {'index': 0}, 'The television is a modern tool.'),
              ('vrai_faux', 4, {'statement': 'A local tool needs electricity to work.'},
               {'value': False}, 'No. A drum needs only a hand.')]),

            ('liste',
             'The modern ICT tools are the computer, the radio, the phone, the camera and the '
             'television.',
             'bt-lo-modernes',
             'Une radio dessinée, nommée.',
             [('simple', 'They are made in a factory, and most of them need electricity.'),
              ('visuel', 'They carry a message much further than a drum.')],
             [('qcm', 1, {'question': 'Which one is a modern ICT tool?',
                          'options': ['The radio', 'The flute', 'The gong']},
               {'index': 0}, 'The radio.'),
              ('vrai_faux', 1, {'statement': 'The camera is a modern ICT tool.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The computer, the radio and the phone are {{1}} tools.', 'blanks': 1},
               {'values': ['modern']}, 'Modern tools.'),
              ('association', 3, {'question': 'Match each tool with its kind.',
                                  'gauche': ['the drum', 'the television', 'the bell'],
                                  'droite': ['local', 'modern', 'local too']},
               {'order': [0, 1, 2]}, 'Two local, one modern.'),
              ('vrai_faux', 4, {'statement': 'The xylophone is a modern ICT tool.'},
               {'value': False}, 'No, it is a local one.')]),

            ('relation',
             'Each ICT tool has its use: the radio to hear information, the television to see '
             'things, the whistle to begin the course.',
             'bt-lo-usages',
             'Trois paires reliées : la radio pour entendre, la télévision pour voir.',
             [('simple', 'Ask what it gives you: a sound, a picture, or a signal.'),
              ('pas_a_pas', 'Read the tool, then say what you do with it in one word.')],
             [('qcm', 1, {'question': 'What is the radio used for?',
                          'options': ['To hear information', 'To see pictures',
                                      'To print a page']},
               {'index': 0}, 'To hear information.'),
              ('vrai_faux', 1, {'statement': 'The television is used to see things.'},
               {'value': True}, 'Yes.'),
              ('association', 2, {'question': 'Match each tool with its use.',
                                  'gauche': ['the radio', 'the television', 'the whistle'],
                                  'droite': ['to hear information', 'to see things',
                                             'to begin the course']},
               {'order': [0, 1, 2]}, 'Hear, see, begin.'),
              ('texte_a_trous', 3,
               {'text': 'The whistle is used to {{1}} the course.', 'blanks': 1},
               {'values': ['begin']}, 'To begin the course.'),
              ('vrai_faux', 4, {'statement': 'The radio is used to see things.'},
               {'value': False}, 'No, to hear them.')]),
        ],
    ),

    # ------------------------------------------------------------------ 82
    (
        'The first computers', OUTILS, '2026-10-06', 82,
        'The earliest computers were the abacus and the Pascaline. The abacus counts with beads '
        'that slide on rods. The Pascaline adds with wheels, and it was invented by Pascal in the '
        'year 1642.',
        'bt-pr-couv',
        'Trois cartes : the abacus, the Pascaline, 1642.',
        [
            ('liste',
             'The earliest computers were the abacus and the Pascaline.',
             'bt-pr-anciens',
             'Deux lignes : the abacus, the Pascaline.',
             [('simple', 'Two machines, long before electricity.'),
              ('visuel', 'They did not show anything on a screen: there was none.')],
             [('qcm', 1, {'question': 'What were the earliest computers called?',
                          'options': ['The abacus and the Pascaline',
                                      'The radio and the television',
                                      'The keyboard and the mouse']},
               {'index': 0}, 'The abacus and the Pascaline.'),
              ('vrai_faux', 1, {'statement': 'The abacus is one of the earliest computers.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The earliest computers were the {{1}} and the Pascaline.', 'blanks': 1},
               {'values': ['abacus']}, 'The abacus.'),
              ('qcm', 3, {'question': 'Which one is not an early computer?',
                          'options': ['The printer', 'The abacus', 'The Pascaline']},
               {'index': 0}, 'The printer is a peripheral of today.'),
              ('vrai_faux', 4, {'statement': 'The earliest computers had a screen.'},
               {'value': False}, 'No. There were no screens then.')]),

            ('date',
             'The Pascaline was invented by Pascal in the year 1642.',
             'bt-pr-pascal',
             'Deux lignes : invented by Pascal, in the year 1642.',
             [('simple', 'One name, one year: Pascal, 1642.'),
              ('histoire', 'Blaise Pascal was nineteen years old. He built it to help his father, '
                           'who counted taxes all day long.')],
             [('qcm', 1, {'question': 'Who invented the Pascaline?',
                          'options': ['Pascal', 'Newton', 'Edison']},
               {'index': 0}, 'Pascal, and the machine took his name.'),
              ('vrai_faux', 1, {'statement': 'The Pascaline was invented in the year 1642.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The Pascaline was invented in the year {{1}}.', 'blanks': 1},
               {'values': ['1642']}, 'In 1642.'),
              ('qcm', 3, {'question': 'In which year was the Pascaline invented?',
                          'options': ['1642', '1942', '1462']},
               {'index': 0}, '1642.'),
              ('vrai_faux', 4, {'statement': 'The Pascaline was invented in 1942.'},
               {'value': False}, 'No: 1642, three hundred years earlier.')]),

            ('relation',
             'The abacus counts with beads that slide on rods. The Pascaline adds with wheels '
             'that turn.',
             'bt-pr-abaque',
             'Deux paires : l’abaque compte avec des boules, la Pascaline avec des roues.',
             [('simple', 'Beads for one, wheels for the other.'),
              ('visuel', 'Both are moved by hand: no electricity, no button.')],
             [('qcm', 1, {'question': 'What does the abacus count with?',
                          'options': ['Beads', 'Wheels', 'Lights']},
               {'index': 0}, 'Beads that slide on rods.'),
              ('vrai_faux', 1, {'statement': 'The Pascaline works with wheels.'},
               {'value': True}, 'Yes, wheels that turn.'),
              ('association', 2, {'question': 'Match each machine with what moves in it.',
                                  'gauche': ['the abacus', 'the Pascaline'],
                                  'droite': ['beads', 'wheels']},
               {'order': [0, 1]}, 'Beads, then wheels.'),
              ('texte_a_trous', 3,
               {'text': 'The abacus counts with {{1}} that slide on rods.', 'blanks': 1},
               {'values': ['beads']}, 'With beads.'),
              ('vrai_faux', 4, {'statement': 'The abacus needs electricity to work.'},
               {'value': False}, 'No. You move the beads with your hand.')]),
        ],
    ),

    # ------------------------------------------------------------------ 83
    (
        'Security measures when using ICT tools', SECU, '2026-10-16', 83,
        'These are the precautions we must consider when using ICT tools, so that they remain '
        'secured and last longer. Clean them with a dry cloth, never eat or drink on them, never '
        'touch them with wet hands, switch them off after use, and install an antivirus.',
        'bt-se-couv',
        'Quatre cartes : clean, dry hands, switch off, antivirus.',
        [
            ('definition',
             'Security measures are the precautions we must consider when using ICT tools, so '
             'that they remain secured and last longer.',
             'bt-se-def',
             'Trois lignes : well maintained, remain secured, last longer.',
             [('simple', 'A tool well taken care of works longer. That is the whole reason.'),
              ('pas_a_pas', 'Before touching a machine, ask: are my hands clean and dry?')],
             [('qcm', 1, {'question': 'Why do we take security measures?',
                          'options': ['So that the tools last longer',
                                      'So that they go faster', 'So that they cost less']},
               {'index': 0}, 'So that they remain secured and last longer.'),
              ('vrai_faux', 1,
               {'statement': 'Security measures are precautions taken when using ICT tools.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Well maintained, the tools last {{1}}.', 'blanks': 1},
               {'values': ['longer']}, 'They last longer.'),
              ('qcm', 3, {'question': 'What is a precaution?',
                          'options': ['Something you do to avoid harm',
                                      'Something you do to go faster',
                                      'A part of the computer']},
               {'index': 0}, 'Something done to avoid harm.'),
              ('vrai_faux', 4,
               {'statement': 'ICT tools need no care at all.'},
               {'value': False}, 'No. They must be well maintained.')]),

            ('relation',
             'Always use a dry and clean piece of cloth to clean an ICT tool.',
             'bt-se-chiffon',
             'Trois lignes : a dry piece of cloth, a clean one, never a wet rag.',
             [('simple', 'Dry AND clean: a wet cloth damages, a dirty one scratches.'),
              ('visuel', 'Water and electricity never go together.')],
             [('qcm', 1, {'question': 'What do you clean an ICT tool with?',
                          'options': ['A dry and clean cloth', 'A wet cloth', 'Soap and water']},
               {'index': 0}, 'A dry and clean piece of cloth.'),
              ('vrai_faux', 1, {'statement': 'A wet cloth is good for cleaning a computer.'},
               {'value': False}, 'No. It must be dry.'),
              ('texte_a_trous', 2,
               {'text': 'Always use a {{1}} and clean piece of cloth.', 'blanks': 1},
               {'values': ['dry']}, 'A dry cloth.'),
              ('qcm', 3, {'question': 'Why must the cloth be dry?',
                          'options': ['Water damages the machine',
                                      'Water makes it go slower', 'Water makes it heavy']},
               {'index': 0}, 'Water and electricity do not go together.'),
              ('vrai_faux', 4, {'statement': 'You may clean a computer with any rag.'},
               {'value': False}, 'No: dry and clean.')]),

            ('relation',
             'Do not eat or drink while working on an ICT tool, and avoid touching it with wet '
             'hands.',
             'bt-se-manger',
             'Trois lignes : do not eat on them, do not drink on them, no wet hands.',
             [('simple', 'Crumbs fall between the keys; a drink spilt kills the machine.'),
              ('visuel', 'Wet hands leave water on every key you press.')],
             [('qcm', 1, {'question': 'What must you not do while working on a computer?',
                          'options': ['Eat and drink', 'Sit down', 'Read the screen']},
               {'index': 0}, 'Eat and drink.'),
              ('vrai_faux', 1, {'statement': 'You may touch a computer with wet hands.'},
               {'value': False}, 'No. Dry your hands first.'),
              ('texte_a_trous', 2,
               {'text': 'Avoid touching ICT tools with {{1}} hands.', 'blanks': 1},
               {'values': ['wet']}, 'With wet hands.'),
              ('qcm', 3, {'question': 'Why is eating on a keyboard a bad idea?',
                          'options': ['Crumbs fall between the keys',
                                      'The keyboard gets hungry', 'It makes the screen dark']},
               {'index': 0}, 'Crumbs fall in and block the keys.'),
              ('vrai_faux', 4,
               {'statement': 'A drink spilt on a computer can destroy it.'},
               {'value': True}, 'Yes, and often for good.')]),

            ('relation',
             'Always switch ICT tools off after use.',
             'bt-se-eteindre',
             'Une ligne en doré : always switch them off.',
             [('simple', 'Off after use: it saves the machine and the current.'),
              ('pas_a_pas', 'Finish the work, save the file, then switch off.')],
             [('qcm', 1, {'question': 'What do you do with an ICT tool after use?',
                          'options': ['Switch it off', 'Leave it on', 'Unplug the screen only']},
               {'index': 0}, 'Switch it off.'),
              ('vrai_faux', 1, {'statement': 'ICT tools are switched off after use.'},
               {'value': True}, 'Yes, always.'),
              ('texte_a_trous', 2,
               {'text': 'Always switch them {{1}} after use.', 'blanks': 1},
               {'values': ['off']}, 'Switch them off.'),
              ('qcm', 3, {'question': 'What do you do just before switching off?',
                          'options': ['Save your file', 'Clean the screen', 'Call a friend']},
               {'index': 0}, 'Save your work first.'),
              ('vrai_faux', 4, {'statement': 'A computer may be left on for ever.'},
               {'value': False}, 'No. Switch it off after use.')]),

            ('relation',
             'Always install an antivirus in your computer to protect it from computer viruses.',
             'bt-se-antivirus',
             'Deux lignes : install an antivirus, it protects the computer.',
             [('simple', 'A computer virus spoils the files. The antivirus stops it.'),
              ('analogie', 'The antivirus is the vaccine of the computer.')],
             [('qcm', 1, {'question': 'What protects a computer from viruses?',
                          'options': ['An antivirus', 'A dry cloth', 'A USB key']},
               {'index': 0}, 'An antivirus.'),
              ('vrai_faux', 1, {'statement': 'An antivirus protects the computer.'},
               {'value': True}, 'Yes, from computer viruses.'),
              ('texte_a_trous', 2,
               {'text': 'Always install an {{1}} in your computer.', 'blanks': 1},
               {'values': ['antivirus']}, 'An antivirus.'),
              ('qcm', 3, {'question': 'What does a computer virus do?',
                          'options': ['It spoils the files', 'It cleans the screen',
                                      'It makes the computer faster']},
               {'index': 0}, 'It spoils what is in the computer.'),
              ('vrai_faux', 4, {'statement': 'A computer virus makes a person ill.'},
               {'value': False}, 'No. It attacks the machine, not the body.')]),

            ('liste',
             'Two more measures from the exercise: never pour water on ICT tools, and never use a '
             'phone in a petrol station.',
             'bt-se-station',
             'Deux lignes : no water on ICT tools, no phone in a petrol station.',
             [('simple', 'Water kills the machine; a phone in a petrol station can start a fire.'),
              ('visuel', 'These two were the answers of the exercise in the exercise book.')],
             [('qcm', 1, {'question': 'Where must you not use a phone?',
                          'options': ['In a petrol station', 'In the classroom',
                                      'In the market']},
               {'index': 0}, 'In a petrol station.'),
              ('vrai_faux', 1, {'statement': 'You must never pour water on ICT tools.'},
               {'value': True}, 'Yes, water destroys them.'),
              ('texte_a_trous', 2,
               {'text': 'Do not pour {{1}} on ICT tools.', 'blanks': 1},
               {'values': ['water']}, 'Do not pour water.'),
              ('qcm', 3, {'question': 'Why is a phone dangerous in a petrol station?',
                          'options': ['It can start a fire', 'It makes too much noise',
                                      'It stops working there']},
               {'index': 0}, 'Petrol catches fire very easily.'),
              ('vrai_faux', 4, {'statement': 'Pouring water on a computer cleans it well.'},
               {'value': False}, 'No. It destroys it.')]),
        ],
    ),

    # ------------------------------------------------------------------ 84
    (
        'Files and their extensions', FICHIERS, '2026-10-16', 84,
        'A file is a collection of related data or information. It is saved with a name which '
        'ends with a three-letter extension: Doc for a text, JPG for an image, MP3 for a sound, '
        'MP4 for a video.',
        'bt-fi-couv',
        'Quatre cartes : Doc, JPG, MP3, MP4.',
        [
            ('definition',
             'A file is a collection of related data or information. It is saved with a name '
             'which ends with a three-letter extension.',
             'bt-fi-def',
             'Trois lignes : a collection of related data, saved with a name, and an extension.',
             [('simple', 'The name says what it is; the extension says what kind it is.'),
              ('visuel', 'In « lesson.doc », lesson is the name and doc is the extension.')],
             [('qcm', 1, {'question': 'What is a file?',
                          'options': ['A collection of related data', 'A part of the keyboard',
                                      'A kind of printer']},
               {'index': 0}, 'A collection of related data or information.'),
              ('vrai_faux', 1, {'statement': 'A file is saved with a name.'},
               {'value': True}, 'Yes, and the name ends with an extension.'),
              ('texte_a_trous', 2,
               {'text': 'A file is a collection of related {{1}}.', 'blanks': 1},
               {'values': ['data']}, 'Related data or information.'),
              ('qcm', 3, {'question': 'How many letters has the extension of a file?',
                          'options': ['Three', 'Two', 'Six']},
               {'index': 0}, 'Three, in this lesson. Some newer ones have four, like docx.'),
              ('vrai_faux', 4, {'statement': 'The extension comes at the end of the name.'},
               {'value': True}, 'Yes, after the dot.')]),

            ('relation',
             'A textual file is a text that is typed and saved in the computer. Its extension is '
             'Doc.',
             'bt-fi-texte',
             'La fiche d’un fichier texte, extension Doc en gros.',
             [('simple', 'You typed it with the keyboard: it is a textual file.'),
              ('visuel', 'Doc, like document.')],
             [('qcm', 1, {'question': 'What is the extension of a textual file?',
                          'options': ['Doc', 'JPG', 'MP3']},
               {'index': 0}, 'Doc.'),
              ('vrai_faux', 1, {'statement': 'A textual file is a text typed and saved.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'A textual file has the extension {{1}}.', 'blanks': 1},
               {'values': ['doc']}, 'Doc.'),
              ('qcm', 3, {'question': 'You typed your lesson and saved it. What file is it?',
                          'options': ['A textual file', 'An image file', 'A video file']},
               {'index': 0}, 'A textual file.'),
              ('vrai_faux', 4, {'statement': 'A textual file has the extension JPG.'},
               {'value': False}, 'No: Doc. JPG is for images.')]),

            ('relation',
             'An image file is a drawing or a photograph saved in the computer. Its extension is '
             'JPG.',
             'bt-fi-image',
             'La fiche d’un fichier image, extension JPG en gros.',
             [('simple', 'Anything you look at and do not read: a drawing, a photograph.'),
              ('visuel', 'JPG is said « jay-peg ».')],
             [('qcm', 1, {'question': 'What is the extension of an image file?',
                          'options': ['JPG', 'Doc', 'MP4']},
               {'index': 0}, 'JPG.'),
              ('vrai_faux', 1, {'statement': 'A photograph saved in a computer is an image file.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'An image file has the extension {{1}}.', 'blanks': 1},
               {'values': ['jpg']}, 'JPG.'),
              ('qcm', 3, {'question': 'You took a photograph and saved it. What file is it?',
                          'options': ['An image file', 'A textual file', 'An audio file']},
               {'index': 0}, 'An image file.'),
              ('vrai_faux', 4, {'statement': 'A drawing saved in a computer has the extension '
                                             'MP3.'},
               {'value': False}, 'No: JPG. MP3 is for sounds.')]),

            ('relation',
             'An audio file is a sound or a voice that has been recorded and saved in a computer. '
             'Its extension is MP3.',
             'bt-fi-audio',
             'La fiche d’un fichier audio, extension MP3 en gros.',
             [('simple', 'Anything you hear and do not see: a song, a voice.'),
              ('visuel', 'MP3 for the ear, MP4 for the eye and the ear together.')],
             [('qcm', 1, {'question': 'What is the extension of an audio file?',
                          'options': ['MP3', 'MP4', 'JPG']},
               {'index': 0}, 'MP3.'),
              ('vrai_faux', 1, {'statement': 'A song saved in a computer is an audio file.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'An audio file has the extension {{1}}.', 'blanks': 1},
               {'values': ['mp3']}, 'MP3.'),
              ('qcm', 3, {'question': 'You recorded your voice and saved it. What file is it?',
                          'options': ['An audio file', 'An image file', 'A textual file']},
               {'index': 0}, 'An audio file.'),
              ('vrai_faux', 4, {'statement': 'An audio file has the extension MP4.'},
               {'value': False}, 'No: MP3. MP4 is for videos.')]),

            ('relation',
             'A video file is a video that has been saved into a computer. Its extension is MP4.',
             'bt-fi-video',
             'La fiche d’un fichier vidéo, extension MP4 en gros.',
             [('simple', 'A video moves and speaks: picture and sound together.'),
              ('visuel', 'One letter apart from MP3, and one sense more.')],
             [('qcm', 1, {'question': 'What is the extension of a video file?',
                          'options': ['MP4', 'MP3', 'Doc']},
               {'index': 0}, 'MP4.'),
              ('vrai_faux', 1, {'statement': 'A video saved in a computer is a video file.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'A video file has the extension {{1}}.', 'blanks': 1},
               {'values': ['mp4']}, 'MP4.'),
              ('association', 3, {'question': 'Match each file with its extension.',
                                  'gauche': ['a text', 'a photograph', 'a song'],
                                  'droite': ['Doc', 'JPG', 'MP3']},
               {'order': [0, 1, 2]}, 'Doc, JPG, MP3.'),
              ('vrai_faux', 4, {'statement': 'A video file has the extension JPG.'},
               {'value': False}, 'No: MP4.')]),

            ('relation',
             'A text typed in Microsoft Word is identified by Doc, in Microsoft Excel by XLS, and '
             'in Microsoft Access by MDB.',
             'bt-fi-logiciels',
             'Trois paires reliées : Word et Doc, Excel et XLS, Access et MDB.',
             [('simple', 'The programme you typed in decides the extension.'),
              ('visuel', 'Word writes, Excel counts, Access keeps lists.')],
             [('qcm', 1, {'question': 'What identifies a file typed in Microsoft Word?',
                          'options': ['Doc', 'XLS', 'MDB']},
               {'index': 0}, 'Doc.'),
              ('vrai_faux', 1, {'statement': 'A file from Microsoft Excel is identified by XLS.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'A file typed in Microsoft Excel is identified by {{1}}.', 'blanks': 1},
               {'values': ['xls']}, 'XLS.'),
              ('association', 3, {'question': 'Match each programme with its extension.',
                                  'gauche': ['Word', 'Excel', 'Access'],
                                  'droite': ['Doc', 'XLS', 'MDB']},
               {'order': [0, 1, 2]}, 'Doc, XLS, MDB.'),
              ('vrai_faux', 4, {'statement': 'A file from Microsoft Access is identified by Doc.'},
               {'value': False}, 'No: MDB.')]),
        ],
    ),

    # ------------------------------------------------------------------ 85
    (
        'Creating and saving a file', FICHIERS, '2026-10-23', 85,
        'To create a text file: the Start menu, all programmes, Microsoft Word, then type and '
        'save. For an image file, Microsoft PowerPoint instead. To save: File on the menu bar, '
        'Save as, type an appropriate name, and click Save.',
        'bt-cr-couv',
        'Trois cartes : Start menu, all programmes, Save as.',
        [
            ('relation',
             'To create a text file: click the Start menu, click all programmes, click Microsoft '
             'Word, then type a text and save it with a name.',
             'bt-cr-texte',
             'Les quatre temps, numérotés : Start menu, all programmes, Word, type and save.',
             [('simple', 'Four steps, always in this order.'),
              ('pas_a_pas', 'Start, programmes, Word, then type. Nothing is saved before the '
                            'last step.')],
             [('qcm', 1, {'question': 'What do you click first to create a text file?',
                          'options': ['The Start menu', 'Microsoft Word', 'Save as']},
               {'index': 0}, 'The Start menu.'),
              ('vrai_faux', 1,
               {'statement': 'Microsoft Word is used to create a text file.'},
               {'value': True}, 'Yes.'),
              ('chronologie', 2, {'question': 'Put the four steps in the right order.',
                                  'tokens': ['Click the Start menu', 'Click all programmes',
                                             'Click Microsoft Word', 'Type and save']},
               {'order': [0, 1, 2, 3]}, 'Start, programmes, Word, type.'),
              ('texte_a_trous', 3,
               {'text': 'To create a text file, you click Microsoft {{1}}.', 'blanks': 1},
               {'values': ['word']}, 'Microsoft Word.'),
              ('vrai_faux', 4, {'statement': 'You type the text before opening Microsoft Word.'},
               {'value': False}, 'No. You open it first.')]),

            ('relation',
             'To create an image file: click the Start menu, click all programmes, click '
             'Microsoft PowerPoint, then draw and save it with a name.',
             'bt-cr-image',
             'Les quatre temps, numérotés : Start menu, all programmes, PowerPoint, draw and save.',
             [('simple', 'The same three first steps; only the programme changes.'),
              ('visuel', 'Word for words, PowerPoint for drawings.')],
             [('qcm', 1, {'question': 'Which programme is used to create an image file?',
                          'options': ['Microsoft PowerPoint', 'Microsoft Word',
                                      'Microsoft Excel']},
               {'index': 0}, 'Microsoft PowerPoint.'),
              ('vrai_faux', 1,
               {'statement': 'The first step is the same for a text file and an image file.'},
               {'value': True}, 'Yes: the Start menu.'),
              ('texte_a_trous', 2,
               {'text': 'To create an image file, you click Microsoft {{1}} Point.', 'blanks': 1},
               {'values': ['power']}, 'Microsoft PowerPoint.'),
              ('qcm', 3, {'question': 'What is the last step for an image file?',
                          'options': ['Draw and save', 'Type and save', 'Print the drawing']},
               {'index': 0}, 'Draw, then save with a name.'),
              ('vrai_faux', 4,
               {'statement': 'Microsoft Word is used to create an image file.'},
               {'value': False}, 'No: PowerPoint.')]),

            ('relation',
             'To save a created file: click File on the menu bar, click Save as in the dialogue '
             'box, type an appropriate name, and click Save.',
             'bt-cr-enregistrer',
             'Les quatre temps, numérotés : File, Save as, type a name, Save.',
             [('simple', 'File, Save as, a name, Save. Four gestures.'),
              ('visuel', 'A dialogue box is the little window that opens and waits for you.')],
             [('qcm', 1, {'question': 'Where do you click first to save a file?',
                          'options': ['File, on the menu bar', 'The Start menu',
                                      'The keyboard']},
               {'index': 0}, 'File, on the menu bar.'),
              ('vrai_faux', 1, {'statement': 'A dialogue box opens when you save a file.'},
               {'value': True}, 'Yes, and you click Save as in it.'),
              ('chronologie', 2, {'question': 'Put the four steps in the right order.',
                                  'tokens': ['Click File on the menu bar', 'Click Save as',
                                             'Type an appropriate name', 'Click Save']},
               {'order': [0, 1, 2, 3]}, 'File, Save as, the name, Save.'),
              ('texte_a_trous', 3,
               {'text': 'In the dialogue box, you click {{1}} as.', 'blanks': 1},
               {'values': ['save']}, 'Save as.'),
              ('vrai_faux', 4, {'statement': 'A file can be saved without any name.'},
               {'value': False}, 'No. You must type a name.')]),

            ('relation',
             'The name given to a file must be appropriate: it says what is inside, so that the '
             'file can be found again.',
             'bt-cr-nom',
             'La fiche d’un fichier nommé « lesson 1 », extension Doc.',
             [('simple', 'A file called « aaa » is lost the day after.'),
              ('pas_a_pas', 'Say in two or three words what is inside, and write that.')],
             [('qcm', 1, {'question': 'What is an appropriate name for a file?',
                          'options': ['One that says what is inside',
                                      'The shortest one possible', 'Always the same one']},
               {'index': 0}, 'One that says what is inside.'),
              ('vrai_faux', 1, {'statement': 'A good file name helps you find the file again.'},
               {'value': True}, 'Yes, that is what it is for.'),
              ('texte_a_trous', 2,
               {'text': 'You type an {{1}} name for the file.', 'blanks': 1},
               {'values': ['appropriate']}, 'An appropriate name.'),
              ('qcm', 3, {'question': 'Which is the better name for your science lesson?',
                          'options': ['science lesson', 'my new file', 'aaa bbb']},
               {'index': 0}, 'It says what is inside.'),
              ('vrai_faux', 4, {'statement': 'The name of a file does not matter at all.'},
               {'value': False}, 'No. It is how you find it again.')]),
        ],
    ),

    # ------------------------------------------------------------------ 86
    (
        'Typing: the keys that matter', FRAPPE, '2026-10-23', 86,
        'Typing is the act of using the keyboard to enter data into a computer. Caps Lock makes '
        'capitals, Backspace erases, the space bar separates words, Enter moves to a new line, '
        'Ctrl gives shortcuts, and the direction keys move the cursor.',
        'bt-ty-couv',
        'Une touche Caps Lock dessinée en grand.',
        [
            ('definition',
             'Typing is the act of using the keyboard to enter data, that is a text, into a '
             'computer.',
             'bt-ty-def',
             'Un clavier dessiné, nommé.',
             [('simple', 'Typing is writing with the keys instead of a pen.'),
              ('visuel', 'The keyboard is an input peripheral: the text goes in.')],
             [('qcm', 1, {'question': 'What is typing?',
                          'options': ['Using the keyboard to enter data',
                                      'Printing a page on paper',
                                      'Saving a file with a name']},
               {'index': 0}, 'Using the keyboard to enter data into a computer.'),
              ('vrai_faux', 1, {'statement': 'You type with the keyboard.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Typing is using the {{1}} to enter data.', 'blanks': 1},
               {'values': ['keyboard']}, 'The keyboard.'),
              ('qcm', 3, {'question': 'What kind of peripheral is the keyboard?',
                          'options': ['An input peripheral', 'An output peripheral',
                                      'A storage peripheral']},
               {'index': 0}, 'Input: the text goes into the computer.'),
              ('vrai_faux', 4, {'statement': 'You type with the mouse.'},
               {'value': False}, 'No, with the keyboard.')]),

            ('relation',
             'The Caps Lock key changes small letters into capital letters.',
             'bt-ty-caps',
             'La touche Caps Lock dessinée, avec son relief.',
             [('simple', 'Press it once and every letter comes out big.'),
              ('visuel', 'Press it again and the letters are small once more.')],
             [('qcm', 1, {'question': 'What does the Caps Lock key do?',
                          'options': ['It makes capital letters', 'It erases a word',
                                      'It moves to a new line']},
               {'index': 0}, 'It changes small letters into capitals.'),
              ('vrai_faux', 1, {'statement': 'Caps Lock gives capital letters.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'To write in capital letters, press {{1}} Lock.', 'blanks': 1},
               {'values': ['caps']}, 'Caps Lock.'),
              ('qcm', 3, {'question': 'You want to write YAOUNDE in capitals. Which key?',
                          'options': ['Caps Lock', 'Backspace', 'Enter']},
               {'index': 0}, 'Caps Lock.'),
              ('vrai_faux', 4, {'statement': 'Caps Lock erases the last letter.'},
               {'value': False}, 'No, that is Backspace.')]),

            ('relation',
             'The Backspace and Delete keys are used to erase a word wrongly written.',
             'bt-ty-backspace',
             'La touche Backspace dessinée, avec son relief.',
             [('simple', 'A mistake is not crossed out on a computer: it is erased.'),
              ('visuel', 'Backspace eats the letter just before the cursor.')],
             [('qcm', 1, {'question': 'What does the Backspace key do?',
                          'options': ['It erases what is wrongly written',
                                      'It makes capital letters', 'It saves the file']},
               {'index': 0}, 'It erases.'),
              ('vrai_faux', 1, {'statement': 'The Delete key also erases.'},
               {'value': True}, 'Yes, like Backspace.'),
              ('texte_a_trous', 2,
               {'text': 'To erase a word wrongly written, press {{1}}.', 'blanks': 1},
               {'values': ['backspace']}, 'Backspace.'),
              ('qcm', 3, {'question': 'You typed « Yaonde » instead of « Yaounde ». Which key?',
                          'options': ['Backspace', 'Enter', 'Caps Lock']},
               {'index': 0}, 'Backspace, to erase and write again.'),
              ('vrai_faux', 4, {'statement': 'Backspace adds a letter.'},
               {'value': False}, 'No. It takes one away.')]),

            ('relation',
             'The space bar is used to separate words. It is NOT the Shift key: the Shift key is '
             'another key, used for capital letters.',
             'bt-ty-espace',
             'Deux touches côte à côte : Space bar et Shift, deux touches différentes.',
             [('simple', 'The space bar is the long key at the bottom. Shift is the one with an '
                         'arrow, on the side.'),
              ('visuel', 'Look at a real keyboard: they are two different keys, far apart.')],
             [('qcm', 1, {'question': 'What is the space bar used for?',
                          'options': ['To separate words', 'To make capital letters',
                                      'To save the file']},
               {'index': 0}, 'To separate words.'),
              ('vrai_faux', 1, {'statement': 'The space bar and the Shift key are the same key.'},
               {'value': False}, 'No. They are two different keys on the keyboard.'),
              ('texte_a_trous', 2,
               {'text': 'The space bar is used to {{1}} words.', 'blanks': 1},
               {'values': ['separate']}, 'To separate words.'),
              ('qcm', 3, {'question': 'Which key is used for capital letters?',
                          'options': ['The Shift key', 'The space bar', 'The Enter key']},
               {'index': 0}, 'Shift, or Caps Lock.'),
              ('vrai_faux', 4, {'statement': 'The space bar makes capital letters.'},
               {'value': False}, 'No. It makes the space between two words.')]),

            ('relation',
             'The Enter key is used to move to a new line or to a new paragraph.',
             'bt-ty-entree',
             'La touche Enter dessinée, avec son relief.',
             [('simple', 'Enter is the key that goes down a line.'),
              ('visuel', 'On paper you go to the line with your hand; here, with Enter.')],
             [('qcm', 1, {'question': 'What does the Enter key do?',
                          'options': ['It moves to a new line', 'It erases a letter',
                                      'It prints the page']},
               {'index': 0}, 'It moves to a new line or a new paragraph.'),
              ('vrai_faux', 1, {'statement': 'Enter starts a new paragraph.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The {{1}} key moves to a new line.', 'blanks': 1},
               {'values': ['enter']}, 'The Enter key.'),
              ('qcm', 3, {'question': 'You finished a paragraph. Which key comes next?',
                          'options': ['Enter', 'Caps Lock', 'Backspace']},
               {'index': 0}, 'Enter.'),
              ('vrai_faux', 4, {'statement': 'Enter separates two words.'},
               {'value': False}, 'No, that is the space bar.')]),

            ('relation',
             'The Control key, written Ctrl, gives a command as a shortcut: Ctrl and C to copy, '
             'Ctrl and V to paste, Ctrl and S to save, Ctrl and P to print.',
             'bt-ty-ctrl',
             'Quatre paires reliées : Ctrl et C pour copier, Ctrl et V pour coller.',
             [('simple', 'Hold Ctrl, press the letter, let go. That is a shortcut.'),
              ('visuel', 'C for copy, S for save, P for print: the letter says the word.')],
             [('qcm', 1, {'question': 'What is Ctrl and C used for?',
                          'options': ['To copy', 'To paste', 'To print']},
               {'index': 0}, 'To copy.'),
              ('vrai_faux', 1, {'statement': 'Ctrl and S is used to save.'},
               {'value': True}, 'Yes: S for save.'),
              ('association', 2, {'question': 'Match each shortcut with what it does.',
                                  'gauche': ['Ctrl and C', 'Ctrl and V', 'Ctrl and P'],
                                  'droite': ['to copy', 'to paste', 'to print']},
               {'order': [0, 1, 2]}, 'Copy, paste, print.'),
              ('texte_a_trous', 3,
               {'text': 'To cut, you press Ctrl and the letter {{1}}.', 'blanks': 1},
               {'values': ['x']}, 'Ctrl and X.'),
              ('vrai_faux', 4, {'statement': 'Ctrl and P is used to paste.'},
               {'value': False}, 'No: P is to print. V is to paste.')]),

            ('relation',
             'The direction keys are used to move in the text: to the left, to the right, upward '
             'or downward.',
             'bt-ty-fleches',
             'La touche Direction dessinée, avec son relief.',
             [('simple', 'Four arrows, four directions, and the text does not change.'),
              ('visuel', 'They move where you WRITE, not what is written.')],
             [('qcm', 1, {'question': 'What are the direction keys used for?',
                          'options': ['To move in the text', 'To erase a word',
                                      'To save the file']},
               {'index': 0}, 'To move left, right, upward or downward.'),
              ('vrai_faux', 1, {'statement': 'There are four direction keys.'},
               {'value': True}, 'Left, right, up and down.'),
              ('texte_a_trous', 2,
               {'text': 'The direction keys move to the left, to the right, upward or {{1}}.',
                'blanks': 1},
               {'values': ['downward']}, 'Downward.'),
              ('qcm', 3, {'question': 'Which key moves you back one line in the text?',
                          'options': ['The upward direction key', 'The Backspace key',
                                      'The Caps Lock key']},
               {'index': 0}, 'The upward arrow.'),
              ('vrai_faux', 4, {'statement': 'A direction key erases what it passes over.'},
               {'value': False}, 'No. It only moves.')]),
        ],
    ),

    # ------------------------------------------------------------------ 87
    (
        'Editing', EDITION, '2026-10-30', 87,
        'Editing is checking and correcting a written work or text to make it clean, correct and '
        'easy to understand. You can change the font size, the page setting, the borders, the '
        'background, the text alignment, the capitalisation and the calligraphy.',
        'bt-ed-couv',
        'Trois cartes : font size, borders, alignment.',
        [
            ('definition',
             'Editing is checking and correcting a written work or text, to make it clean, '
             'correct and easy to understand.',
             'bt-ed-def',
             'Trois lignes : checking, correcting, easy to understand.',
             [('simple', 'You wrote it; now you make it right and make it clear.'),
              ('pas_a_pas', 'Read it again, find what is wrong, correct it, then make it '
                            'pleasant to read.')],
             [('qcm', 1, {'question': 'What is editing?',
                          'options': ['Checking and correcting a written work',
                                      'Typing a brand new text',
                                      'Printing a page on paper']},
               {'index': 0}, 'Checking and correcting a written work.'),
              ('vrai_faux', 1, {'statement': 'Editing makes a text easier to understand.'},
               {'value': True}, 'Yes, that is its purpose.'),
              ('texte_a_trous', 2,
               {'text': 'Editing is checking and {{1}} a written work.', 'blanks': 1},
               {'values': ['correcting']}, 'Checking and correcting.'),
              ('qcm', 3, {'question': 'When do you edit a text?',
                          'options': ['After writing it', 'Before writing it',
                                      'Instead of writing it']},
               {'index': 0}, 'After writing it.'),
              ('vrai_faux', 4, {'statement': 'Editing means writing a text for the first time.'},
               {'value': False}, 'No. It means correcting one already written.')]),

            ('liste',
             'When editing, you can change the font size, the page setting, the borders and the '
             'background.',
             'bt-ed-liste1',
             'Quatre lignes : font size, page setting, borders, background.',
             [('simple', 'These four change how the page LOOKS, not what it says.'),
              ('visuel', 'The border is the line around the page; the background is behind the '
                         'words.')],
             [('qcm', 1, {'question': 'Which one can you change when editing?',
                          'options': ['The font size', 'The keyboard', 'The printer']},
               {'index': 0}, 'The font size.'),
              ('vrai_faux', 1, {'statement': 'The background can be changed when editing.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'The {{1}} is the line drawn around the page.', 'blanks': 1},
               {'values': ['border']}, 'The border.'),
              ('qcm', 3, {'question': 'Your text is too small to read. What do you change?',
                          'options': ['The font size', 'The background', 'The borders']},
               {'index': 0}, 'The font size.'),
              ('vrai_faux', 4,
               {'statement': 'Changing the font size changes the meaning of the text.'},
               {'value': False}, 'No. Only how it looks.')]),

            ('liste',
             'When editing, you can also change the text alignment, the capitalisation and the '
             'calligraphy, which is the type of writing.',
             'bt-ed-liste2',
             'Trois lignes : text alignment, capitalisation, calligraphy.',
             [('simple', 'Alignment is where the lines begin; calligraphy is the shape of the '
                         'letters.'),
              ('visuel', 'Capitalisation is choosing where the capital letters go.')],
             [('qcm', 1, {'question': 'What is calligraphy?',
                          'options': ['The type of writing', 'The size of the page',
                                      'The colour behind the words']},
               {'index': 0}, 'The type of writing.'),
              ('vrai_faux', 1, {'statement': 'Text alignment can be changed when editing.'},
               {'value': True}, 'Yes.'),
              ('texte_a_trous', 2,
               {'text': 'Calligraphy is the type of {{1}}.', 'blanks': 1},
               {'values': ['writing']}, 'The type of writing.'),
              ('association', 3, {'question': 'Match each word with what it changes.',
                                  'gauche': ['alignment', 'capitalisation', 'calligraphy'],
                                  'droite': ['where the lines begin', 'the capital letters',
                                             'the shape of the letters']},
               {'order': [0, 1, 2]}, 'Three ways of changing the look.'),
              ('vrai_faux', 4, {'statement': 'Calligraphy is the name of a printer.'},
               {'value': False}, 'No. It is the type of writing.')]),

            ('relation',
             'Before editing anything, the words must be highlighted. Otherwise nothing changes.',
             'bt-ed-surligner',
             'Deux lignes : the words must be highlighted, otherwise nothing changes.',
             [('simple', 'You first show the computer WHICH words you mean.'),
              ('pas_a_pas', 'Hold the mouse button, slide over the words, let go. They turn '
                            'blue: they are highlighted.')],
             [('qcm', 1, {'question': 'What must you do before editing a word?',
                          'options': ['Highlight it', 'Print it', 'Erase it']},
               {'index': 0}, 'Highlight it.'),
              ('vrai_faux', 1, {'statement': 'Words must be highlighted before they are edited.'},
               {'value': True}, 'Yes, otherwise nothing changes.'),
              ('texte_a_trous', 2,
               {'text': 'For us to edit, the words must be {{1}}.', 'blanks': 1},
               {'values': ['highlighted']}, 'Highlighted.'),
              ('qcm', 3, {'question': 'You changed the font size and nothing happened. Why?',
                          'options': ['The words were not highlighted',
                                      'The file was not saved', 'The printer was off']},
               {'index': 0}, 'Nothing was highlighted, so nothing changed.'),
              ('vrai_faux', 4, {'statement': 'A text can be edited without highlighting it.'},
               {'value': False}, 'No. The computer would not know which words you mean.')]),
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
        'fig', os.path.join(ici, 'figures-brayne-tic-oct.py'))
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
    chemin = os.path.join(racine, 'app', 'public', 'seed-brayne-tic-oct.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-40s %s  %d notions  %d questions'
              % (ordre, titre, date, len(ns), sum(len(n[5]) for n in ns)))
    print(chemin)
