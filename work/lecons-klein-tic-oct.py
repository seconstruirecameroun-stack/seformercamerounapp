# -*- coding: utf-8 -*-
"""
Sept leçons de TIC pour KLEIN (CE1) — son cahier d-informatique de
septembre à novembre 2026, quinze pages photographiées le 10 novembre.

LA MATIÈRE ÉTAIT VIDE, comme celle de BRAYNE la veille. « TIC » existe
dans sa classe, et pas une leçon n-y était rangée.

CE QUE PORTENT LES QUINZE PAGES. Treize sont de TIC : six séances de cours
et deux devoirs corrigés, du 11 septembre au 6 novembre. Les deux autres
ne le sont pas et ne sont pas reprises ici — une page de musique sur la
portée, et une page de langue maternelle sur les rites traditionnels. Si
le père les veut, elles feront leur propre lot.

TOUT EST EN FRANÇAIS, comme son cahier. Son frère a le même programme en
anglais ; KLEIN l-a en français, avec les mots qu-on lui demandera :
matériel, logiciel, pavé alphanumérique, source crédible.

LES DEUX DEVOIRS CORRIGÉS SERVENT DE SOURCE, et pas seulement de
contrôle. Le devoir du 6 novembre teste la SOURIS - ses parties, ses
fonctions - alors qu-aucune page de cours sur la souris n-a été
photographiée. La leçon de la souris est donc écrite depuis le devoir
lui-même, qui donne les cinq parties et les deux fonctions.

DEUX SCHÉMAS À ANNOTER, parce que son cahier les demande deux fois :
« Voici un téléphone portable, annote-le » et le dessin de la souris. Le
type de question existe depuis hier, et les noms des repères sont vérifiés
contre le script de figures, mot pour mot.

UNE RÉSERVE À PORTER AU PÈRE. Le devoir du 2 octobre fait corriger
« Il existe 3 types d-ordinateur » par FAUX. Aucune page photographiée ne
dit combien il y en a. Je n-invente pas un nombre : aucune question de ce
lot ne porte là-dessus, et c-est écrit dans work/brayne-revision-notes.md.

Usage :  python work/lecons-klein-tic-oct.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-klein-tic-oct.py. ')

MATIERE = 'TIC'
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'fr'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

SYSTEME = 'Le système informatique'
PRUDENCE = 'Les précautions'
OUTILS = 'Les outils TIC'
ORDINATEUR = 'L’ordinateur'
SOURCES = 'L’information'

# Les noms des repères, DANS L-ORDRE DES NUMÉROS DU DESSIN. Le contrôle les
# compare aux listes du script de figures : un numéro qui désignerait autre
# chose dans l-image que dans la question ferait rater une question sue.
PHONE = ('le haut-parleur', 'l’écran', 'le clavier', 'le microphone')
SOURIS = ('le clic gauche', 'le clic droit', 'la molette', 'le boîtier', 'le câble')


def annotation(figure, question, noms, niveau=3):
    """La question d-annotation : les noms sont donnés dans l-ordre du dessin.

    `ordre` est l-identité, et c-est voulu : l-application mélange les
    étiquettes avant de les montrer. Les écrire déjà mêlées ici rendrait la
    relecture impossible.
    """
    return ('annotation', niveau,
            {'question': question, 'figure': figure, 'etiquettes': list(noms)},
            {'ordre': list(range(len(noms)))},
            'Les numéros vont du haut vers le bas du dessin.')


LECONS = [
    # ------------------------------------------------------------------ 47
    (
        'Le système informatique', SYSTEME, '2026-09-11', 47,
        'Le système informatique, c’est tout le matériel informatique qui sert à traiter les '
        'informations. Il est composé de deux parties : la partie matérielle, qu’on appelle '
        'hardware, et la partie logicielle, qu’on appelle software.',
        'kt-sy-couv',
        'Deux cartes alignées : matériel, logiciel.',
        [
            ('definition',
             'Le système informatique, c’est tout le matériel informatique qui sert à traiter '
             'les informations.',
             'kt-sy-def',
             'Trois lignes : tout le matériel informatique, qui sert à traiter, les informations.',
             [('simple', 'Traiter une information, c’est la recevoir, la ranger, et la '
                         'ressortir.'),
              ('visuel', 'Un ordinateur tout seul ne fait rien : il lui faut aussi des '
                         'logiciels.')],
             [('qcm', 1, {'question': 'À quoi sert le système informatique ?',
                          'options': ['À traiter les informations', 'À faire la cuisine',
                                      'À transporter les élèves']},
               {'index': 0}, 'À traiter les informations.'),
              ('vrai_faux', 1,
               {'statement': 'Le système informatique sert à traiter les informations.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Le système informatique sert à {{1}} les informations.', 'blanks': 1},
               {'values': ['traiter']}, 'À traiter les informations.'),
              ('qcm', 3, {'question': 'Le système informatique, c’est…',
                          'options': ['tout le matériel informatique', 'une seule machine',
                                      'un cahier de classe']},
               {'index': 0}, 'Tout le matériel informatique.'),
              ('vrai_faux', 4,
               {'statement': 'Le système informatique sert à transporter les gens.'},
               {'value': False}, 'Non. Il traite les informations.')]),

            ('relation',
             'Il est composé de deux parties : le matériel, qu’on appelle hardware, et le '
             'logiciel, qu’on appelle software.',
             'kt-sy-deux',
             'Deux paires reliées : le matériel et hardware, le logiciel et software.',
             [('simple', 'Deux parties, deux mots anglais à retenir.'),
              ('visuel', 'Hard veut dire dur : c’est ce qu’on touche. Soft veut dire doux.')],
             [('qcm', 1, {'question': 'Combien de parties a le système informatique ?',
                          'options': ['Deux', 'Trois', 'Une seule']},
               {'index': 0}, 'Deux : le matériel et le logiciel.'),
              ('vrai_faux', 1, {'statement': 'Le matériel s’appelle aussi hardware.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Le logiciel s’appelle aussi {{1}}.', 'blanks': 1},
               {'values': ['software']}, 'Software.'),
              ('association', 3, {'question': 'Relie chaque partie à son nom anglais.',
                                  'gauche': ['le matériel', 'le logiciel'],
                                  'droite': ['hardware', 'software']},
               {'order': [0, 1]}, 'Hardware et software.'),
              ('vrai_faux', 4, {'statement': 'Le matériel s’appelle software.'},
               {'value': False}, 'Non : hardware.')]),

            ('liste',
             'La partie matérielle, c’est ce qu’on touche : le clavier, l’écran, la souris, le '
             'câble et l’unité centrale.',
             'kt-sy-materiel',
             'Un clavier et une unité centrale dessinés, nommés chacun.',
             [('simple', 'Si tu peux le prendre dans la main, c’est du matériel.'),
              ('visuel', 'Le câble aussi est du matériel : on le touche.')],
             [('qcm', 1, {'question': 'Lequel fait partie du matériel ?',
                          'options': ['Le clavier', 'L’antivirus', 'Internet']},
               {'index': 0}, 'Le clavier : on le touche.'),
              ('vrai_faux', 1, {'statement': 'L’écran fait partie de la partie matérielle.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'La partie matérielle, c’est ce qu’on {{1}}.', 'blanks': 1},
               {'values': ['touche']}, 'Ce qu’on touche.'),
              ('qcm', 3, {'question': 'Lequel n’est pas du matériel ?',
                          'options': ['Le fichier', 'La souris', 'L’unité centrale']},
               {'index': 0}, 'Le fichier est un logiciel : on ne le touche pas.'),
              ('vrai_faux', 4, {'statement': 'Le câble fait partie du logiciel.'},
               {'value': False}, 'Non, c’est du matériel.')]),

            ('liste',
             'La partie logicielle, c’est ce qu’on ne touche pas : le logiciel application, '
             'l’antivirus, internet et le fichier.',
             'kt-sy-logiciel',
             'Quatre lignes : le logiciel application, l’antivirus, internet, le fichier.',
             [('simple', 'Si tu ne peux pas le prendre dans la main, c’est du logiciel.'),
              ('analogie', 'Le matériel est le corps ; le logiciel est ce qui le fait '
                           'travailler.')],
             [('qcm', 1, {'question': 'Lequel fait partie du logiciel ?',
                          'options': ['L’antivirus', 'Le clavier', 'Le câble']},
               {'index': 0}, 'L’antivirus : on ne le touche pas.'),
              ('vrai_faux', 1, {'statement': 'Internet fait partie de la partie logicielle.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'La partie logicielle, c’est ce qu’on ne touche {{1}}.', 'blanks': 1},
               {'values': ['pas']}, 'Ce qu’on ne touche pas.'),
              ('association', 3, {'question': 'Range chaque élément dans sa partie.',
                                  'gauche': ['le clavier', 'l’antivirus', 'l’écran'],
                                  'droite': ['matériel', 'logiciel', 'matériel aussi']},
               {'order': [0, 1, 2]}, 'Deux matériels, un logiciel.'),
              ('vrai_faux', 4, {'statement': 'Le fichier fait partie du matériel.'},
               {'value': False}, 'Non, c’est du logiciel.')]),

            ('relation',
             'Un ordinateur est toujours constitué d’une partie matérielle et d’une partie '
             'logicielle. Il lui faut les deux.',
             'kt-sy-classer',
             'Trois paires reliées : la souris et matériel, l’antivirus et logiciel.',
             [('simple', 'Sans logiciel, l’ordinateur ne sait rien faire. Sans matériel, il '
                         'n’existe pas.'),
              ('pas_a_pas', 'Pour ranger un élément, demande-toi : est-ce que je peux le '
                            'toucher ?')],
             [('qcm', 1, {'question': 'De quoi est constitué un ordinateur ?',
                          'options': ['D’une partie matérielle et d’une partie logicielle',
                                      'D’une seule partie, la partie matérielle',
                                      'De trois parties différentes']},
               {'index': 0}, 'Des deux parties.'),
              ('vrai_faux', 1,
               {'statement': 'Un ordinateur a une partie matérielle et une partie logicielle.'},
               {'value': True}, 'Oui, les deux.'),
              ('texte_a_trous', 2,
               {'text': 'Pour ranger un élément, je me demande si je peux le {{1}}.',
                'blanks': 1},
               {'values': ['toucher']}, 'Si je peux le toucher.'),
              ('qcm', 3, {'question': 'Un ordinateur sans logiciel, que fait-il ?',
                          'options': ['Rien du tout', 'Tout, comme avant',
                                      'Il devient une radio']},
               {'index': 0}, 'Rien : il lui faut les deux parties.'),
              ('vrai_faux', 4,
               {'statement': 'Un ordinateur peut n’avoir qu’une partie matérielle.'},
               {'value': False}, 'Non. Il lui faut aussi le logiciel.')]),
        ],
    ),

    # ------------------------------------------------------------------ 48
    (
        'Les précautions avec le téléphone et l’ordinateur', PRUDENCE, '2026-09-18', 48,
        'Je ne dois pas utiliser le téléphone lorsqu’il est branché, ni au volant, ni dans une '
        'station-service. Je ne dois pas toucher ces appareils avec les mains mouillées. Et '
        'j’évite les écrans trop lumineux.',
        'kt-pr-couv',
        'Trois cartes : pas au volant, mains sèches, écran doux.',
        [
            ('relation',
             'Je ne dois pas utiliser le téléphone lorsqu’il est branché.',
             'kt-pr-branche',
             'Trois lignes : le téléphone se charge, on ne s’en sert pas, on attend.',
             [('simple', 'Quand il se charge, on le laisse tranquille.'),
              ('visuel', 'Le courant passe dans le fil : c’est le moment de ne pas y toucher.')],
             [('qcm', 1, {'question': 'Quand ne faut-il pas utiliser le téléphone ?',
                          'options': ['Quand il est branché', 'Quand il est éteint',
                                      'Quand il est dans le sac']},
               {'index': 0}, 'Quand il est branché.'),
              ('vrai_faux', 1,
               {'statement': 'On peut téléphoner pendant que le téléphone se charge.'},
               {'value': False}, 'Non. On attend qu’il soit débranché.'),
              ('texte_a_trous', 2,
               {'text': 'Je ne dois pas utiliser le téléphone lorsqu’il est {{1}}.',
                'blanks': 1},
               {'values': ['branché']}, 'Lorsqu’il est branché.'),
              ('qcm', 3, {'question': 'Que fait-on quand le téléphone se charge ?',
                          'options': ['On attend', 'On l’utilise quand même',
                                      'On le met dans l’eau']},
               {'index': 0}, 'On attend.'),
              ('vrai_faux', 4,
               {'statement': 'Un téléphone branché est un téléphone qu’on peut utiliser.'},
               {'value': False}, 'Non, justement pas.')]),

            ('liste',
             'Je ne dois pas utiliser le téléphone au volant, ni dans une station-service.',
             'kt-pr-volant',
             'Deux lignes : au volant en conduisant, dans une station-service.',
             [('simple', 'Au volant, on regarde la route. À la station, il y a de l’essence.'),
              ('visuel', 'L’essence prend feu très vite : un téléphone peut l’allumer.')],
             [('qcm', 1, {'question': 'Où ne faut-il pas utiliser le téléphone ?',
                          'options': ['Au volant', 'À la maison', 'Dans la cour']},
               {'index': 0}, 'Au volant, en conduisant.'),
              ('vrai_faux', 1,
               {'statement': 'On ne téléphone pas dans une station-service.'},
               {'value': True}, 'Oui, c’est dangereux.'),
              ('texte_a_trous', 2,
               {'text': 'Je ne dois pas téléphoner au {{1}}.', 'blanks': 1},
               {'values': ['volant']}, 'Au volant.'),
              ('qcm', 3, {'question': 'Pourquoi pas dans une station-service ?',
                          'options': ['L’essence peut prendre feu', 'Il n’y a pas de réseau',
                                      'C’est trop bruyant']},
               {'index': 0}, 'L’essence prend feu très vite.'),
              ('vrai_faux', 4, {'statement': 'On peut téléphoner en conduisant.'},
               {'value': False}, 'Non. On regarde la route.')]),

            ('relation',
             'Je ne dois pas toucher le téléphone ni l’ordinateur avec les mains mouillées.',
             'kt-pr-mains',
             'Trois lignes : l’eau et l’électricité, ne vont pas ensemble, on s’essuie d’abord.',
             [('simple', 'On s’essuie les mains avant de toucher un appareil.'),
              ('visuel', 'L’eau et l’électricité ne vont jamais ensemble.')],
             [('qcm', 1, {'question': 'Avec quelles mains touche-t-on un appareil ?',
                          'options': ['Des mains sèches', 'Des mains mouillées',
                                      'Des mains sales']},
               {'index': 0}, 'Des mains sèches.'),
              ('vrai_faux', 1,
               {'statement': 'On peut toucher un ordinateur avec les mains mouillées.'},
               {'value': False}, 'Non. On s’essuie d’abord.'),
              ('texte_a_trous', 2,
               {'text': 'Je ne touche pas les appareils avec les mains {{1}}.', 'blanks': 1},
               {'values': ['mouillées']}, 'Les mains mouillées.'),
              ('qcm', 3, {'question': 'Que fait-on avant de toucher un appareil ?',
                          'options': ['On s’essuie les mains', 'On se lave les pieds',
                                      'On ferme les yeux']},
               {'index': 0}, 'On s’essuie les mains.'),
              ('vrai_faux', 4, {'statement': 'L’eau et l’électricité vont bien ensemble.'},
               {'value': False}, 'Non, jamais.')]),

            ('relation',
             'J’évite les écrans trop lumineux : ils font mal aux yeux.',
             'kt-pr-ecrans',
             'Deux lignes : j’évite les écrans, trop lumineux.',
             [('simple', 'Un écran trop clair fatigue les yeux.'),
              ('pas_a_pas', 'Si l’écran pique les yeux, on baisse la lumière.')],
             [('qcm', 1, {'question': 'Quels écrans faut-il éviter ?',
                          'options': ['Les écrans trop lumineux', 'Les écrans trop petits',
                                      'Les écrans trop vieux']},
               {'index': 0}, 'Les écrans trop lumineux.'),
              ('vrai_faux', 1, {'statement': 'Un écran trop lumineux fatigue les yeux.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'J’évite les écrans trop {{1}}.', 'blanks': 1},
               {'values': ['lumineux']}, 'Trop lumineux.'),
              ('qcm', 3, {'question': 'Que fait-on si l’écran pique les yeux ?',
                          'options': ['On baisse la lumière', 'On se rapproche',
                                      'On éteint la pièce']},
               {'index': 0}, 'On baisse la lumière de l’écran.'),
              ('vrai_faux', 4, {'statement': 'Plus l’écran est lumineux, mieux c’est.'},
               {'value': False}, 'Non, cela fait mal aux yeux.')]),
        ],
    ),

    # ------------------------------------------------------------------ 49
    (
        'Les outils TIC et leurs fonctions', OUTILS, '2026-09-25', 49,
        'L’ordinateur traite automatiquement les informations. L’appareil photo capture les '
        'images et la caméra fait des vidéos. Le téléviseur informe en images, la radio en audio, '
        'et le téléphone sert à appeler.',
        'kt-ou-couv',
        'Quatre objets alignés : un écran, un appareil photo, une radio, un téléphone.',
        [
            ('relation',
             'L’ordinateur sert à traiter automatiquement les informations.',
             'kt-ou-ordinateur',
             'Un écran d’ordinateur dessiné, nommé.',
             [('simple', 'Automatiquement veut dire : tout seul, sans qu’on l’aide.'),
              ('visuel', 'Tu demandes, il cherche, il répond.')],
             [('qcm', 1, {'question': 'À quoi sert l’ordinateur ?',
                          'options': ['À traiter les informations', 'À capturer les images',
                                      'À faire des vidéos']},
               {'index': 0}, 'À traiter les informations.'),
              ('vrai_faux', 1,
               {'statement': 'L’ordinateur traite les informations automatiquement.'},
               {'value': True}, 'Oui, tout seul.'),
              ('texte_a_trous', 2,
               {'text': 'L’ordinateur traite {{1}} les informations.', 'blanks': 1},
               {'values': ['automatiquement']}, 'Automatiquement.'),
              ('qcm', 3, {'question': 'Que veut dire automatiquement ?',
                          'options': ['Tout seul', 'Très lentement', 'Avec beaucoup de gens']},
               {'index': 0}, 'Tout seul, sans qu’on l’aide.'),
              ('vrai_faux', 4, {'statement': 'L’ordinateur sert surtout à faire des vidéos.'},
               {'value': False}, 'Non, c’est la caméra.')]),

            ('relation',
             'L’appareil photo capture les images, et la caméra fait des vidéos.',
             'kt-ou-photo',
             'Un appareil photo dessiné, nommé.',
             [('simple', 'La photo ne bouge pas. La vidéo bouge.'),
              ('visuel', 'Un appareil photo prend un instant ; une caméra en prend beaucoup à '
                         'la suite.')],
             [('qcm', 1, {'question': 'Que fait l’appareil photo ?',
                          'options': ['Il capture les images', 'Il fait des vidéos',
                                      'Il donne le son']},
               {'index': 0}, 'Il capture les images.'),
              ('vrai_faux', 1, {'statement': 'La caméra fait des vidéos.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'L’appareil photo {{1}} les images.', 'blanks': 1},
               {'values': ['capture']}, 'Il capture les images.'),
              ('association', 3, {'question': 'Relie chaque outil à ce qu’il fait.',
                                  'gauche': ['l’appareil photo', 'la caméra'],
                                  'droite': ['des images', 'des vidéos']},
               {'order': [0, 1]}, 'Des images, des vidéos.'),
              ('vrai_faux', 4, {'statement': 'L’appareil photo fait des vidéos.'},
               {'value': False}, 'Non, c’est la caméra.')]),

            ('relation',
             'Le téléviseur donne des informations en images, et la radio en donne en audio.',
             'kt-ou-tele',
             'Deux paires reliées : le téléviseur en images, la radio en audio.',
             [('simple', 'La télévision se regarde ; la radio s’écoute.'),
              ('visuel', 'Audio veut dire : qu’on entend.')],
             [('qcm', 1, {'question': 'Comment la radio donne-t-elle les informations ?',
                          'options': ['En audio', 'En images', 'Sur du papier']},
               {'index': 0}, 'En audio : on l’écoute.'),
              ('vrai_faux', 1,
               {'statement': 'Le téléviseur donne des informations en images.'},
               {'value': True}, 'Oui, on les regarde.'),
              ('texte_a_trous', 2,
               {'text': 'La radio donne des informations en {{1}}.', 'blanks': 1},
               {'values': ['audio']}, 'En audio.'),
              ('association', 3, {'question': 'Relie chaque outil à sa façon d’informer.',
                                  'gauche': ['le téléviseur', 'la radio'],
                                  'droite': ['en images', 'en audio']},
               {'order': [0, 1]}, 'En images, en audio.'),
              ('vrai_faux', 4, {'statement': 'La radio donne des informations en images.'},
               {'value': False}, 'Non, en audio.')]),

            ('relation',
             'Le téléphone sert à appeler. Il a un haut-parleur, un écran, un clavier et un '
             'microphone.',
             'kt-ou-telephone',
             'Le schéma d’un téléphone portable, avec ses quatre repères numérotés.',
             [('simple', 'Le microphone prend ta voix ; le haut-parleur te fait entendre '
                         'l’autre.'),
              ('visuel', 'De haut en bas : le haut-parleur, l’écran, le clavier, le '
                         'microphone.')],
             [('qcm', 1, {'question': 'À quoi sert le téléphone ?',
                          'options': ['À appeler', 'À faire des calculs',
                                      'À capturer les images']},
               {'index': 0}, 'À appeler.'),
              ('vrai_faux', 1, {'statement': 'Le microphone du téléphone prend ta voix.'},
               {'value': True}, 'Oui, et le haut-parleur fait entendre l’autre.'),
              ('texte_a_trous', 2,
               {'text': 'Le téléphone sert à {{1}}.', 'blanks': 1},
               {'values': ['appeler']}, 'À appeler.'),
              annotation('kt-ou-telephone', 'Annote le téléphone portable.', PHONE),
              ('vrai_faux', 4, {'statement': 'Le haut-parleur du téléphone est tout en bas.'},
               {'value': False}, 'Non, il est tout en haut. Le microphone est en bas.')]),

            ('relation',
             'Le gong et le tambour sont des outils traditionnels de communication. Le téléphone '
             'et l’ordinateur sont des outils modernes.',
             'kt-ou-traditionnels',
             'Trois paires reliées : le gong et traditionnel, le téléphone et moderne.',
             [('simple', 'Les traditionnels ne marchent pas à l’électricité.'),
              ('analogie', 'Au village, le gong appelle la réunion comme le téléphone appelle '
                           'un ami.')],
             [('qcm', 1, {'question': 'Lequel est un outil traditionnel ?',
                          'options': ['Le tambour', 'Le téléphone', 'L’ordinateur']},
               {'index': 0}, 'Le tambour.'),
              ('vrai_faux', 1, {'statement': 'Le gong est un outil moderne de communication.'},
               {'value': False}, 'Non. Le gong est un outil traditionnel.'),
              ('texte_a_trous', 2,
               {'text': 'Le gong et le tambour sont des outils {{1}}.', 'blanks': 1},
               {'values': ['traditionnels']}, 'Traditionnels.'),
              ('association', 3, {'question': 'Relie chaque outil à sa sorte.',
                                  'gauche': ['le gong', 'l’ordinateur', 'le tambour'],
                                  'droite': ['traditionnel', 'moderne', 'traditionnel aussi']},
               {'order': [0, 1, 2]}, 'Deux traditionnels, un moderne.'),
              ('vrai_faux', 4, {'statement': 'Le téléphone est un outil moderne.'},
               {'value': True}, 'Oui.')]),
        ],
    ),

    # ------------------------------------------------------------------ 50
    (
        'Les fonctions de l’ordinateur', ORDINATEUR, '2026-10-16', 50,
        'L’ordinateur a quatre fonctions principales : saisir l’information avec le clavier, la '
        'traiter avec l’unité centrale, la stocker dans la mémoire, et afficher les résultats sur '
        'l’écran. Il sert aussi à calculer, chercher et communiquer.',
        'kt-fo-couv',
        'Quatre cartes alignées : saisir, traiter, stocker, afficher.',
        [
            ('relation',
             'La première fonction de l’ordinateur est de saisir l’information. C’est le clavier '
             'qui le fait.',
             'kt-fo-saisir',
             'Un clavier dessiné, nommé.',
             [('simple', 'Saisir, c’est faire entrer. On tape, et le texte entre.'),
              ('visuel', 'Le clavier est la porte d’entrée des mots.')],
             [('qcm', 1, {'question': 'Qui sert à saisir l’information ?',
                          'options': ['Le clavier', 'L’écran', 'La mémoire']},
               {'index': 0}, 'Le clavier.'),
              ('vrai_faux', 1, {'statement': 'Saisir l’information, c’est la faire entrer.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'C’est le {{1}} qui sert à saisir l’information.', 'blanks': 1},
               {'values': ['clavier']}, 'Le clavier.'),
              ('qcm', 3, {'question': 'Combien de fonctions principales a l’ordinateur ?',
                          'options': ['Quatre', 'Deux', 'Six']},
               {'index': 0}, 'Quatre.'),
              ('vrai_faux', 4, {'statement': 'C’est l’écran qui saisit l’information.'},
               {'value': False}, 'Non, c’est le clavier.')]),

            ('relation',
             'La deuxième fonction est de traiter l’information. C’est l’unité centrale qui le '
             'fait.',
             'kt-fo-traiter',
             'Une unité centrale dessinée, nommée.',
             [('simple', 'L’unité centrale est la tête de l’ordinateur : c’est elle qui '
                         'travaille.'),
              ('visuel', 'C’est la grande boîte, à côté de l’écran.')],
             [('qcm', 1, {'question': 'Qui traite l’information ?',
                          'options': ['L’unité centrale', 'Le clavier', 'L’écran']},
               {'index': 0}, 'L’unité centrale.'),
              ('vrai_faux', 1, {'statement': 'L’unité centrale traite l’information.'},
               {'value': True}, 'Oui, c’est elle qui travaille.'),
              ('texte_a_trous', 2,
               {'text': 'C’est l’{{1}} centrale qui traite l’information.', 'blanks': 1},
               {'values': ['unité']}, 'L’unité centrale.'),
              ('association', 3, {'question': 'Relie chaque fonction à son élément.',
                                  'gauche': ['saisir', 'traiter'],
                                  'droite': ['le clavier', 'l’unité centrale']},
               {'order': [0, 1]}, 'Le clavier, puis l’unité centrale.'),
              ('vrai_faux', 4, {'statement': 'C’est le clavier qui traite l’information.'},
               {'value': False}, 'Non, c’est l’unité centrale.')]),

            ('relation',
             'La troisième fonction est de stocker l’information. C’est la mémoire qui le fait.',
             'kt-fo-stocker',
             'Une clé de mémoire dessinée, nommée.',
             [('simple', 'Stocker, c’est garder. La mémoire garde ce qu’on lui donne.'),
              ('analogie', 'La mémoire est l’armoire de l’ordinateur.')],
             [('qcm', 1, {'question': 'Qui stocke l’information ?',
                          'options': ['La mémoire', 'L’écran', 'Le clavier']},
               {'index': 0}, 'La mémoire.'),
              ('vrai_faux', 1, {'statement': 'Stocker une information, c’est la garder.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'C’est la {{1}} qui stocke l’information.', 'blanks': 1},
               {'values': ['mémoire']}, 'La mémoire.'),
              ('qcm', 3, {'question': 'Que veut dire stocker ?',
                          'options': ['Garder', 'Effacer', 'Imprimer']},
               {'index': 0}, 'Garder.'),
              ('vrai_faux', 4, {'statement': 'La mémoire efface les informations.'},
               {'value': False}, 'Non, elle les garde.')]),

            ('relation',
             'La quatrième fonction est d’afficher les résultats. C’est l’écran qui le fait.',
             'kt-fo-afficher',
             'Un écran dessiné, nommé.',
             [('simple', 'Afficher, c’est montrer. On voit la réponse sur l’écran.'),
              ('visuel', 'Saisir, traiter, stocker, afficher : quatre fonctions, dans cet '
                         'ordre.')],
             [('qcm', 1, {'question': 'Qui affiche les résultats ?',
                          'options': ['L’écran', 'La mémoire', 'Le clavier']},
               {'index': 0}, 'L’écran.'),
              ('vrai_faux', 1, {'statement': 'C’est l’écran qui affiche les résultats.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'C’est l’{{1}} qui affiche les résultats.', 'blanks': 1},
               {'values': ['écran']}, 'L’écran.'),
              ('chronologie', 3, {'question': 'Remets les quatre fonctions dans l’ordre.',
                                  'tokens': ['saisir', 'traiter', 'stocker', 'afficher']},
               {'order': [0, 1, 2, 3]}, 'Saisir, traiter, stocker, afficher.'),
              ('vrai_faux', 4, {'statement': 'Afficher, c’est cacher la réponse.'},
               {'value': False}, 'Non, c’est la montrer.')]),

            ('liste',
             'L’ordinateur sert aussi à calculer, à faire des recherches et à communiquer.',
             'kt-fo-autres',
             'Trois lignes : calculer, faire des recherches, communiquer.',
             [('simple', 'Trois choses de plus, en plus de ses quatre fonctions.'),
              ('visuel', 'Communiquer, c’est écrire à quelqu’un qui est loin.')],
             [('qcm', 1, {'question': 'À quoi sert encore l’ordinateur ?',
                          'options': ['À calculer', 'À faire la lessive', 'À cuire le riz']},
               {'index': 0}, 'À calculer.'),
              ('vrai_faux', 1, {'statement': 'L’ordinateur sert aussi à communiquer.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'L’ordinateur sert aussi à faire des {{1}}.', 'blanks': 1},
               {'values': ['recherches']}, 'Des recherches.'),
              ('qcm', 3, {'question': 'Lequel ne fait pas partie de la liste ?',
                          'options': ['Déménager', 'Calculer', 'Communiquer']},
               {'index': 0}, 'Déménager : un ordinateur ne porte rien.'),
              ('vrai_faux', 4, {'statement': 'L’ordinateur sert à prendre la température.'},
               {'value': False}, 'Non, ce n’est pas sa fonction.')]),
        ],
    ),

    # ------------------------------------------------------------------ 51
    (
        'Le clavier de l’ordinateur', ORDINATEUR, '2026-10-30', 51,
        'Le clavier est un périphérique d’entrée de l’ordinateur. Il y a deux types de clavier : '
        'AZERTY pour le français et QWERTY pour l’anglais. Il a un pavé numérique, un pavé '
        'alphanumérique, des touches de fonctions et une barre d’espacement.',
        'kt-cl-couv',
        'Deux cartes alignées : AZERTY, QWERTY.',
        [
            ('definition',
             'Le clavier est un périphérique d’entrée de l’ordinateur : l’information entre par '
             'lui.',
             'kt-cl-entree',
             'Un clavier dessiné, nommé.',
             [('simple', 'Entrée veut dire que l’information va VERS l’ordinateur.'),
              ('visuel', 'L’écran, lui, est un périphérique de sortie.')],
             [('qcm', 1, {'question': 'Le clavier est un périphérique de quoi ?',
                          'options': ['D’entrée', 'De sortie', 'De mémoire']},
               {'index': 0}, 'D’entrée : l’information entre par lui.'),
              ('vrai_faux', 1, {'statement': 'Le clavier est un périphérique d’entrée.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Le clavier est un périphérique d’{{1}}.', 'blanks': 1},
               {'values': ['entrée']}, 'D’entrée.'),
              ('qcm', 3, {'question': 'Que veut dire périphérique d’entrée ?',
                          'options': ['L’information va vers l’ordinateur',
                                      'L’information sort de l’ordinateur',
                                      'L’information est effacée']},
               {'index': 0}, 'Elle va vers l’ordinateur.'),
              ('vrai_faux', 4, {'statement': 'Le clavier est un périphérique de sortie.'},
               {'value': False}, 'Non, d’entrée.')]),

            ('relation',
             'Il y a deux types de clavier : le clavier AZERTY pour le français, et le clavier '
             'QWERTY pour l’anglais.',
             'kt-cl-azerty',
             'Deux paires reliées : AZERTY et le français, QWERTY et l’anglais.',
             [('simple', 'Le nom vient des six premières lettres, en haut à gauche.'),
              ('visuel', 'Regarde un clavier : tu y liras A Z E R T Y, ou Q W E R T Y.')],
             [('qcm', 1, {'question': 'Quel clavier est fait pour le français ?',
                          'options': ['AZERTY', 'QWERTY', 'ABCDEF']},
               {'index': 0}, 'AZERTY.'),
              ('vrai_faux', 1, {'statement': 'Le clavier QWERTY est le clavier anglais.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Le clavier français s’appelle le clavier {{1}}.', 'blanks': 1},
               {'values': ['azerty']}, 'AZERTY.'),
              ('association', 3, {'question': 'Relie chaque clavier à sa langue.',
                                  'gauche': ['AZERTY', 'QWERTY'],
                                  'droite': ['le français', 'l’anglais']},
               {'order': [0, 1]}, 'Le français, l’anglais.'),
              ('vrai_faux', 4, {'statement': 'Il existe quatre types de clavier.'},
               {'value': False}, 'Non, le cahier en donne deux.')]),

            ('relation',
             'Le clavier a un pavé numérique, pour les chiffres, et un pavé alphanumérique, pour '
             'les lettres.',
             'kt-cl-paves',
             'Deux paires reliées : le pavé numérique et les chiffres, l’alphanumérique et les '
             'lettres.',
             [('simple', 'Numérique vient de nombre. Alphanumérique, c’est les lettres ET les '
                         'chiffres.'),
              ('visuel', 'Le pavé numérique est à droite du clavier, tout seul.')],
             [('qcm', 1, {'question': 'À quoi sert le pavé numérique ?',
                          'options': ['Aux chiffres', 'Aux lettres', 'Aux dessins']},
               {'index': 0}, 'Aux chiffres.'),
              ('vrai_faux', 1, {'statement': 'Le pavé alphanumérique porte les lettres.'},
               {'value': True}, 'Oui, les lettres et les chiffres.'),
              ('texte_a_trous', 2,
               {'text': 'Le pavé {{1}} sert aux chiffres.', 'blanks': 1},
               {'values': ['numérique']}, 'Le pavé numérique.'),
              ('association', 3, {'question': 'Relie chaque pavé à ce qu’il porte.',
                                  'gauche': ['le pavé numérique', 'le pavé alphanumérique'],
                                  'droite': ['les chiffres', 'les lettres']},
               {'order': [0, 1]}, 'Les chiffres, les lettres.'),
              ('vrai_faux', 4, {'statement': 'Le pavé numérique sert à écrire les lettres.'},
               {'value': False}, 'Non, les chiffres.')]),

            ('liste',
             'Le clavier a aussi les touches de fonctions, la barre d’espacement et les touches '
             'de direction.',
             'kt-cl-touches',
             'Deux lignes : les touches de fonctions, la barre d’espacement.',
             [('simple', 'La barre d’espacement est la longue touche du bas : elle sépare les '
                         'mots.'),
              ('visuel', 'Les touches de direction sont les quatre flèches.')],
             [('qcm', 1, {'question': 'À quoi sert la barre d’espacement ?',
                          'options': ['À séparer les mots', 'À effacer un mot',
                                      'À écrire en majuscules']},
               {'index': 0}, 'À séparer les mots.'),
              ('vrai_faux', 1,
               {'statement': 'Les touches de direction sont les quatre flèches.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'La barre d’espacement sert à {{1}} les mots.', 'blanks': 1},
               {'values': ['séparer']}, 'À séparer les mots.'),
              ('qcm', 3, {'question': 'Lequel n’est pas une partie du clavier ?',
                          'options': ['Le hardware', 'Le pavé numérique',
                                      'La barre d’espacement']},
               {'index': 0}, 'Le hardware est le nom de tout le matériel.'),
              ('vrai_faux', 4,
               {'statement': 'La barre d’espacement est la plus longue touche du clavier.'},
               {'value': True}, 'Oui, tout en bas.')]),
        ],
    ),

    # ------------------------------------------------------------------ 52
    (
        'La souris de l’ordinateur', ORDINATEUR, '2026-11-06', 52,
        'La souris a un boîtier, un clic gauche, un clic droit, une molette et un câble. Cliquer, '
        'c’est appuyer une fois sur le clic gauche. Double-cliquer, c’est appuyer deux fois très '
        'vite, et c’est ce qui ouvre.',
        'kt-so-couv',
        'Une souris dessinée, en grand.',
        [
            ('liste',
             'La souris a un boîtier, un clic gauche, un clic droit, une molette et un câble.',
             'kt-so-schema',
             'Le schéma d’une souris, avec ses cinq repères numérotés.',
             [('simple', 'Cinq parties : deux boutons, une molette, le corps et le fil.'),
              ('visuel', 'La molette est la petite roue entre les deux boutons.')],
             [('qcm', 1, {'question': 'Comment s’appelle la petite roue de la souris ?',
                          'options': ['La molette', 'Le boîtier', 'Le câble']},
               {'index': 0}, 'La molette.'),
              ('vrai_faux', 1, {'statement': 'La souris a un clic gauche et un clic droit.'},
               {'value': True}, 'Oui, deux boutons.'),
              ('texte_a_trous', 2,
               {'text': 'Le corps de la souris s’appelle le {{1}}.', 'blanks': 1},
               {'values': ['boîtier']}, 'Le boîtier.'),
              annotation('kt-so-schema', 'Annote le schéma de la souris.', SOURIS),
              ('vrai_faux', 4, {'statement': 'La souris a trois boutons pour cliquer.'},
               {'value': False}, 'Non, deux : le clic gauche et le clic droit.')]),

            ('relation',
             'Cliquer, c’est appuyer une fois sur le clic gauche.',
             'kt-so-cliquer',
             'Deux lignes : on appuie une fois, sur le clic gauche.',
             [('simple', 'Une seule pression, et on relâche.'),
              ('visuel', 'Cliquer sert à choisir ce qu’on montre.')],
             [('qcm', 1, {'question': 'Cliquer, c’est appuyer combien de fois ?',
                          'options': ['Une fois', 'Deux fois', 'Trois fois']},
               {'index': 0}, 'Une fois.'),
              ('vrai_faux', 1, {'statement': 'Cliquer est une fonction de la souris.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Cliquer, c’est appuyer une fois sur le clic {{1}}.', 'blanks': 1},
               {'values': ['gauche']}, 'Le clic gauche.'),
              ('qcm', 3, {'question': 'Sur quel bouton clique-t-on d’habitude ?',
                          'options': ['Le clic gauche', 'Le clic droit', 'La molette']},
               {'index': 0}, 'Le clic gauche.'),
              ('vrai_faux', 4, {'statement': 'Cliquer, c’est appuyer deux fois très vite.'},
               {'value': False}, 'Non, cela c’est double-cliquer.')]),

            ('relation',
             'Double-cliquer, c’est appuyer deux fois très vite sur le clic gauche. C’est ce qui '
             'ouvre.',
             'kt-so-double',
             'Trois lignes : on appuie deux fois, très vite, pour ouvrir.',
             [('simple', 'Deux pressions presque collées : clic-clic.'),
              ('pas_a_pas', 'Si le dossier ne s’ouvre pas, c’est qu’on a été trop lent.')],
             [('qcm', 1, {'question': 'Double-cliquer, c’est appuyer combien de fois ?',
                          'options': ['Deux fois', 'Une fois', 'Quatre fois']},
               {'index': 0}, 'Deux fois, très vite.'),
              ('vrai_faux', 1, {'statement': 'Le double-clic sert à ouvrir.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Double-cliquer, c’est appuyer {{1}} fois très vite.', 'blanks': 1},
               {'values': ['deux']}, 'Deux fois.'),
              ('qcm', 3, {'question': 'Que fait le double-clic ?',
                          'options': ['Il ouvre', 'Il efface', 'Il imprime']},
               {'index': 0}, 'Il ouvre.'),
              ('vrai_faux', 4, {'statement': 'On double-clique lentement.'},
               {'value': False}, 'Non, très vite.')]),

            ('relation',
             'La souris ne tourne pas et ne souligne pas : ce ne sont pas ses fonctions.',
             'kt-so-molette',
             'Deux lignes : elle ne tourne pas, elle ne souligne pas.',
             [('simple', 'Ses fonctions sont de cliquer et de double-cliquer.'),
              ('visuel', 'Souligner se fait avec le logiciel, pas avec la souris elle-même.')],
             [('qcm', 1, {'question': 'Laquelle n’est pas une fonction de la souris ?',
                          'options': ['Tourner', 'Cliquer', 'Double-cliquer']},
               {'index': 0}, 'Tourner.'),
              ('vrai_faux', 1, {'statement': 'Souligner est une fonction de la souris.'},
               {'value': False}, 'Non. Elle clique et double-clique.'),
              ('texte_a_trous', 2,
               {'text': 'Les deux fonctions de la souris sont cliquer et {{1}}.', 'blanks': 1},
               {'values': ['double-cliquer']}, 'Double-cliquer.'),
              ('qcm', 3, {'question': 'Laquelle est une fonction de la souris ?',
                          'options': ['Double-cliquer', 'Tourner', 'Souligner']},
               {'index': 0}, 'Double-cliquer.'),
              ('vrai_faux', 4, {'statement': 'La souris sert à tourner la page.'},
               {'value': False}, 'Non, ce n’est pas sa fonction.')]),
        ],
    ),

    # ------------------------------------------------------------------ 53
    (
        'Les sources crédibles de l’information', SOURCES, '2026-11-05', 53,
        'Une source crédible d’information est une source fiable, à laquelle on peut faire '
        'confiance, parce qu’elle donne des informations exactes, vérifiées et étayées. Les '
        'médias officiels, les sites du gouvernement et les sites éducatifs en sont.',
        'kt-sc-couv',
        'Trois cartes alignées : exactes, vérifiées, étayées.',
        [
            ('definition',
             'Une source crédible d’information est une source fiable, à laquelle on peut faire '
             'confiance.',
             'kt-sc-def',
             'Trois lignes : on peut lui faire confiance, ses informations sont exactes, '
             'vérifiées et étayées.',
             [('simple', 'Crédible veut dire : qu’on peut croire.'),
              ('pas_a_pas', 'Avant de croire une information, demande-toi d’où elle vient.')],
             [('qcm', 1, {'question': 'Que veut dire crédible ?',
                          'options': ['Qu’on peut croire', 'Qu’on doit payer',
                                      'Qui vient de loin']},
               {'index': 0}, 'Qu’on peut croire.'),
              ('vrai_faux', 1, {'statement': 'Une source crédible est une source fiable.'},
               {'value': True}, 'Oui, on peut lui faire confiance.'),
              ('texte_a_trous', 2,
               {'text': 'Une source crédible est une source {{1}}.', 'blanks': 1},
               {'values': ['fiable']}, 'Une source fiable.'),
              ('qcm', 3, {'question': 'Que faut-il se demander avant de croire une nouvelle ?',
                          'options': ['D’où elle vient', 'Si elle est amusante',
                                      'Qui la raconte le plus fort']},
               {'index': 0}, 'D’où elle vient.'),
              ('vrai_faux', 4, {'statement': 'Toutes les informations sont crédibles.'},
               {'value': False}, 'Non, il faut regarder leur source.')]),

            ('relation',
             'Une source crédible donne des informations exactes, vérifiées et étayées.',
             'kt-sc-medias',
             'Une radio et une télévision dessinées, nommées chacune.',
             [('simple', 'Exacte veut dire juste. Vérifiée veut dire qu’on a regardé deux fois.'),
              ('visuel', 'Étayée veut dire qu’on donne des preuves.')],
             [('qcm', 1, {'question': 'Comment sont les informations d’une source crédible ?',
                          'options': ['Exactes et vérifiées', 'Amusantes et courtes',
                                      'Longues et rares']},
               {'index': 0}, 'Exactes, vérifiées et étayées.'),
              ('vrai_faux', 1, {'statement': 'Une information vérifiée a été regardée deux fois.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Une source crédible donne des informations {{1}}.', 'blanks': 1},
               {'values': ['exactes']}, 'Exactes, vérifiées et étayées.'),
              ('qcm', 3, {'question': 'Que veut dire étayée ?',
                          'options': ['Qu’on donne des preuves', 'Qu’elle est très longue',
                                      'Qu’elle est en couleur']},
               {'index': 0}, 'Qu’on donne des preuves.'),
              ('vrai_faux', 4,
               {'statement': 'Une information crédible peut être fausse.'},
               {'value': False}, 'Non, elle est exacte et vérifiée.')]),

            ('liste',
             'Les médias officiels sont des sources crédibles : la radio, la télévision et la '
             'presse écrite.',
             'kt-sc-gouvernement',
             'Deux lignes : ils disent ce que fait l’État, et ils le vérifient.',
             [('simple', 'Officiel veut dire reconnu, qui a le droit d’informer.'),
              ('visuel', 'Le journal télévisé est un média officiel.')],
             [('qcm', 1, {'question': 'Lequel est un média officiel ?',
                          'options': ['Le journal télévisé', 'Le débat de la rue',
                                      'La boutique du quartier']},
               {'index': 0}, 'Le journal télévisé.'),
              ('vrai_faux', 1, {'statement': 'La presse écrite est un média officiel.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'La radio, la télévision et la presse écrite sont des {{1}} officiels.',
                'blanks': 1},
               {'values': ['médias']}, 'Des médias officiels.'),
              ('qcm', 3, {'question': 'Que veut dire officiel ?',
                          'options': ['Reconnu, qui a le droit d’informer',
                                      'Très ancien, de l’année passée',
                                      'Qui coûte beaucoup d’argent']},
               {'index': 0}, 'Reconnu.'),
              ('vrai_faux', 4, {'statement': 'La radio est un média officiel.'},
               {'value': True}, 'Oui, quand c’est une vraie station.')]),

            ('liste',
             'Les sites du gouvernement, les encyclopédies et les sites web éducatifs sont aussi '
             'des sources crédibles.',
             'kt-sc-enligne',
             'Deux lignes : les encyclopédies, les sites web éducatifs.',
             [('simple', 'Une encyclopédie est un grand livre qui explique tout, vérifié.'),
              ('visuel', 'Un site éducatif est fait pour apprendre, pas pour amuser.')],
             [('qcm', 1, {'question': 'Lequel est une source crédible ?',
                          'options': ['Une encyclopédie', 'Un débat de la rue',
                                      'Une boutique du quartier']},
               {'index': 0}, 'Une encyclopédie.'),
              ('vrai_faux', 1, {'statement': 'Les sites web éducatifs sont des sources crédibles.'},
               {'value': True}, 'Oui.'),
              ('texte_a_trous', 2,
               {'text': 'Les sites du {{1}} sont des sources crédibles.', 'blanks': 1},
               {'values': ['gouvernement']}, 'Les sites du gouvernement.'),
              ('qcm', 3, {'question': 'À quoi sert une encyclopédie ?',
                          'options': ['À expliquer, avec des faits vérifiés',
                                      'À raconter des histoires drôles',
                                      'À vendre des objets']},
               {'index': 0}, 'À expliquer, avec des faits vérifiés.'),
              ('vrai_faux', 4,
               {'statement': 'Un site éducatif est fait pour apprendre.'},
               {'value': True}, 'Oui.')]),

            ('liste',
             'Les débats de la rue, la boutique du quartier et les réseaux sociaux ne sont pas '
             'des sources crédibles.',
             'kt-sc-pasfiable',
             'Trois lignes : les débats de la rue, la boutique du quartier, les réseaux sociaux.',
             [('simple', 'Personne n’y vérifie ce qui est dit.'),
              ('pas_a_pas', 'Avant de répéter une nouvelle, demande-toi qui l’a vérifiée.')],
             [('qcm', 1, {'question': 'Lequel n’est pas une source crédible ?',
                          'options': ['Le débat de la rue', 'Le journal télévisé',
                                      'L’encyclopédie']},
               {'index': 0}, 'Le débat de la rue : personne ne vérifie.'),
              ('vrai_faux', 1,
               {'statement': 'La boutique du quartier est une source crédible.'},
               {'value': False}, 'Non. On y parle sans vérifier.'),
              ('texte_a_trous', 2,
               {'text': 'Dans la rue, personne ne {{1}} ce qui est dit.', 'blanks': 1},
               {'values': ['vérifie']}, 'Personne ne vérifie.'),
              ('qcm', 3, {'question': 'Lequel n’est pas une source crédible ?',
                          'options': ['Les réseaux sociaux', 'Les sites éducatifs',
                                      'La presse écrite']},
               {'index': 0}, 'Les réseaux sociaux : n’importe qui y écrit.'),
              ('vrai_faux', 4,
               {'statement': 'Tout ce qu’on lit sur les réseaux sociaux est vrai.'},
               {'value': False}, 'Non. N’importe qui peut y écrire n’importe quoi.')]),
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
                if ikind == 'annotation':
                    assert isinstance(payload['question'], str) and payload['question'].strip()
                    fig = payload['figure']
                    assert all(c.islower() or c.isdigit() or c == '-' for c in fig), fig
                    etiquettes = payload['etiquettes']
                    assert 2 <= len(etiquettes) <= 8, payload
                    assert len(set(etiquettes)) == len(etiquettes), payload
                    assert all(e.strip() for e in etiquettes), payload
                    assert sorted(answer['ordre']) == list(range(len(etiquettes))), answer
                elif ikind == 'qcm':
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
        'fig', os.path.join(ici, 'figures-klein-tic-oct.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)

    # Le dessin fait foi : les noms des repères doivent être EXACTEMENT ceux
    # que le script de figures numérote, dans le même ordre.
    assert tuple(PHONE) == tuple(fig.PHONE), 'les repères du téléphone ne coïncident pas'
    assert tuple(SOURIS) == tuple(fig.SOURIS), 'les repères de la souris ne coïncident pas'

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
    chemin = os.path.join(racine, 'app', 'public', 'seed-klein-tic-oct.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-46s %s  %d notions  %d questions'
              % (ordre, titre, date, len(ns), sum(len(n[5]) for n in ns)))
    print(chemin)
