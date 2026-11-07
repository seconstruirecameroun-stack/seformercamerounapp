# -*- coding: utf-8 -*-
"""
Cinq leçons de sciences en français pour KLEIN (CE1) — pages du cahier
d-octobre 2026, lot du 7 novembre.

D-OÙ VIENT CE CAHIER. L-étiquette de la page 12 porte « GUETSA / BRA… » :
le cahier photographié est celui de BRAYNE. Le père a demandé que ces
leçons aillent à KLEIN, et c-est cohérent — les leçons 4, 7, 8 et 9 de
KLEIN viennent déjà de ce même cahier, aux mêmes dates au jour près.
C-est écrit ici pour que personne n-ait à le redécouvrir dans six mois.

QUATRE PAGES ÉTAIENT DÉJÀ FAITES et ne sont pas refaites : la
reproduction des animaux (leçon 7), les soins aux animaux domestiques
(8), les milieux de vie des végétaux (9) et le filtre à eau (4).

LA FORME DES QUESTIONS VIENT DE LA RÉVISION DU 10 NOVEMBRE, qui est
dans le lot, corrigée. Elle est plus variée que l-épreuve anglaise de
BRAYNE, et chaque forme est reprise :

  « Coche la bonne réponse »            → vrai ou faux
  « Encadre les … dans la liste »       → choix multiple
  « Complète le tableau »               → association
  « Donne deux autres techniques »      → association et choix
  « Quel est le milieu de vie de … ? »  → question directe
  la phrase à compléter                 → texte à trous

UN MOT SUR LE NIVEAU. Ces pages sont d-un cahier de CM. Les leçons les
reprennent telles quelles mais les questions sont écrites pour un CE1 :
phrases courtes, un seul fait par question, et les mots difficiles
toujours posés avec leur exemple.

Usage :  python work/lecons-klein-sciences-nov.py
"""

import importlib.util
import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-klein-sciences-nov.py. ')

MATIERE = 'Sciences et technologies'
CLASSE = 'CE1'
ENFANT = 'KLEIN'
LANGUE = 'fr'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

PHYSIQUE = 'Sciences physiques'
AGRO = 'Sciences agropastorales'
VIE = 'Sciences de la vie'
CHIMIE = 'Sciences chimiques'

LECONS = [
    # ------------------------------------------------------------------ 42
    (
        'Le vent', PHYSIQUE, '2026-10-26', 42,
        'Le vent, c’est l’air en mouvement. On ne le voit pas : on voit ce qu’il fait bouger. '
        'Certains objets fonctionnent grâce à lui — le moulin à vent, la montgolfière, le '
        'cerf-volant, le bateau à voile, le parachute. La girouette montre d’où il vient, et '
        'l’anémomètre mesure sa vitesse.',
        'kv-ve-couv',
        'Des traits de vent, un moulin et un bateau à voile.',
        [
            ('definition',
             'Le vent, c’est l’air en mouvement.',
             'kv-ve-def',
             'Des traits de vent qui poussent un arbre.',
             [('simple', 'L’air est partout, même quand il ne bouge pas. Quand il bouge, on '
                         'l’appelle le vent.'),
              ('visuel', 'On ne dessine jamais le vent lui-même : on dessine ce qu’il '
                         'déplace.')],
             [('texte_a_trous', 1,
               {'text': 'Le vent, c’est l’air en {{1}}.', 'blanks': 1},
               {'values': ['mouvement']}, 'En mouvement.'),
              ('qcm', 1, {'question': 'Peut-on voir le vent ?',
                          'options': ['non, on voit ce qu’il bouge', 'oui, il est tout bleu',
                                      'oui, quand il fait chaud']},
               {'index': 0}, 'Non. On voit les feuilles bouger, pas le vent.'),
              ('qcm', 2, {'question': 'Le vent est fait de quoi ?',
                          'options': ['d’air', 'd’eau', 'de terre']},
               {'index': 0}, 'D’air.'),
              ('texte_a_trous', 3, {'text': 'Quand l’air ne bouge pas, il n’y a pas de {{1}}.',
                                    'blanks': 1},
               {'values': ['vent']}, 'Pas de vent.'),
              ('vrai_faux', 4, {'statement': 'Le vent est de l’air qui se déplace.'},
               {'value': True}, 'Oui, c’est exactement la définition.')]),

            ('liste',
             'Le moulin à vent, la montgolfière, le cerf-volant et le bateau à voile '
             'fonctionnent grâce au vent.',
             'kv-ve-objets',
             'Quatre vignettes nommées : le moulin, la montgolfière, le cerf-volant, le bateau '
             'à voile.',
             [('simple', 'Tous ces objets ont besoin du vent pour marcher. Sans vent, ils '
                         'restent immobiles.'),
              ('pas_a_pas', 'Regarde chaque objet et cherche la partie que le vent pousse : '
                            'une aile, une voile, une toile.')],
             [('qcm', 1, {'question': 'Lequel fonctionne grâce au vent ?',
                          'options': ['le bateau à voile', 'la lampe de poche',
                                      'la marmite']},
               {'index': 0}, 'Le bateau à voile.'),
              ('qcm', 1, {'question': 'Lequel n’a pas besoin du vent ?',
                          'options': ['la lampe à pétrole', 'le cerf-volant', 'le moulin']},
               {'index': 0}, 'La lampe à pétrole.'),
              ('association', 2, {'question': 'Relie chaque objet à ce que le vent pousse.',
                                  'gauche': ['le moulin', 'le bateau', 'le cerf-volant'],
                                  'droite': ['ses ailes', 'sa voile', 'sa toile']},
               {'order': [0, 1, 2]}, 'Des ailes, une voile, une toile.'),
              ('texte_a_trous', 3,
               {'text': 'Le cerf-volant monte dans le ciel grâce au {{1}}.', 'blanks': 1},
               {'values': ['vent']}, 'Grâce au vent.'),
              ('vrai_faux', 4, {'statement': 'Un bateau à voile avance même quand il n’y a pas '
                                             'du tout de vent.'},
               {'value': False}, 'Non. Sans vent, la voile ne pousse rien.')]),

            ('relation',
             'Le vent fait tourner les ailes du moulin, et le moulin écrase le grain.',
             'kv-ve-moulin',
             'Un moulin à vent poussé par des traits de vent.',
             [('simple', 'Les ailes tournent, et elles font tourner la meule à l’intérieur.'),
              ('histoire', 'Avant l’électricité, c’est le vent qui faisait la farine. Les '
                           'jours sans vent, le meunier attendait.')],
             [('qcm', 1, {'question': 'Qu’est-ce que le vent fait tourner sur le moulin ?',
                          'options': ['ses ailes', 'sa porte', 'son toit']},
               {'index': 0}, 'Ses ailes.'),
              ('texte_a_trous', 1, {'text': 'Le vent fait tourner les {{1}} du moulin.',
                                    'blanks': 1},
               {'values': ['ailes']}, 'Les ailes.'),
              ('qcm', 2, {'question': 'Que se passe-t-il quand il n’y a pas de vent ?',
                          'options': ['le moulin ne tourne pas', 'le moulin tourne plus vite',
                                      'le moulin se casse']},
               {'index': 0}, 'Il ne tourne pas.'),
              ('texte_a_trous', 3, {'text': 'Un moulin a besoin du vent pour {{1}}.',
                                    'blanks': 1},
               {'values': ['tourner']}, 'Pour tourner.'),
              ('vrai_faux', 4, {'statement': 'Le moulin à vent marche sans électricité.'},
               {'value': True}, 'Oui, c’est le vent qui le fait marcher.')]),

            ('relation',
             'Le vent pousse la voile du bateau, et le bateau avance sur l’eau.',
             'kv-ve-voile',
             'Un bateau à voile poussé par des traits de vent.',
             [('simple', 'La voile est un grand drap. Le vent appuie dessus et pousse le '
                         'bateau.'),
              ('visuel', 'Regarde la voile sur l’image : elle est gonflée du côté d’où vient '
                         'le vent.')],
             [('qcm', 1, {'question': 'Sur quoi le vent appuie-t-il ?',
                          'options': ['sur la voile', 'sur le fond du bateau',
                                      'sur les poissons']},
               {'index': 0}, 'Sur la voile.'),
              ('texte_a_trous', 1, {'text': 'Le vent pousse la {{1}} du bateau.', 'blanks': 1},
               {'values': ['voile']}, 'La voile.'),
              ('qcm', 2, {'question': 'Le bateau à voile avance sur quoi ?',
                          'options': ['sur l’eau', 'sur la route', 'dans le ciel']},
               {'index': 0}, 'Sur l’eau.'),
              ('texte_a_trous', 3, {'text': 'Poussé par le vent, le bateau {{1}}.',
                                    'blanks': 1},
               {'values': ['avance']}, 'Il avance.'),
              ('vrai_faux', 4, {'statement': 'La voile sert à pousser le bateau grâce au '
                                             'vent.'},
               {'value': True}, 'Oui, c’est à cela qu’elle sert.')]),

            ('relation',
             'La girouette montre d’où vient le vent. L’anémomètre mesure sa vitesse.',
             'kv-ve-mesure',
             'Une girouette et un anémomètre, nommés.',
             [('simple', 'Deux instruments, deux questions : d’où vient le vent, et à quelle '
                         'vitesse il souffle.'),
              ('pas_a_pas', 'La girouette pivote et pointe. L’anémomètre tourne, et plus il '
                            'tourne vite, plus le vent est fort.')],
             [('qcm', 1, {'question': 'Que montre la girouette ?',
                          'options': ['d’où vient le vent', 'l’heure qu’il est',
                                      'le poids du vent']},
               {'index': 0}, 'D’où vient le vent.'),
              ('texte_a_trous', 1, {'text': 'L’instrument qui mesure la vitesse du vent est '
                                            'l’{{1}}.', 'blanks': 1},
               {'values': ['anémomètre']}, 'L’anémomètre.'),
              ('association', 2, {'question': 'Relie chaque instrument à ce qu’il dit.',
                                  'gauche': ['la girouette', 'l’anémomètre'],
                                  'droite': ['la direction du vent', 'la vitesse du vent']},
               {'order': [0, 1]}, 'La direction, puis la vitesse.'),
              ('texte_a_trous', 3,
               {'text': 'Plus l’anémomètre tourne vite, plus le vent est {{1}}.', 'blanks': 1},
               {'values': ['fort']}, 'Plus il est fort.'),
              ('vrai_faux', 4, {'statement': 'La girouette et l’anémomètre disent la même '
                                             'chose.'},
               {'value': False}, 'Non. L’une dit d’où, l’autre dit à quelle vitesse.')]),

            ('relation',
             'Le parachute et la montgolfière sont portés par l’air. Le parachute ralentit la '
             'chute, la montgolfière monte.',
             'kv-ve-parachute',
             'Un parachute et une montgolfière, nommés.',
             [('simple', 'L’air retient le parachute et l’empêche de tomber vite.'),
              ('analogie', 'Ouvre une main à plat dans le vent, puis de côté : tu sens l’air '
                           'pousser dans le premier cas seulement.')],
             [('qcm', 1, {'question': 'À quoi sert le parachute ?',
                          'options': ['à ralentir la chute', 'à aller plus vite',
                                      'à faire du bruit']},
               {'index': 0}, 'À ralentir la chute.'),
              ('texte_a_trous', 1, {'text': 'Le parachute est porté par l’{{1}}.', 'blanks': 1},
               {'values': ['air']}, 'Par l’air.'),
              ('qcm', 2, {'question': 'La montgolfière, elle, fait quoi ?',
                          'options': ['elle monte dans le ciel', 'elle roule par terre',
                                      'elle nage dans l’eau']},
               {'index': 0}, 'Elle monte dans le ciel.'),
              ('texte_a_trous', 3,
               {'text': 'Le parachute {{1}} la chute de celui qui saute.', 'blanks': 1},
               {'values': ['ralentit']}, 'Il la ralentit.'),
              ('vrai_faux', 4, {'statement': 'Sans air, un parachute servirait à quelque '
                                             'chose.'},
               {'value': False}, 'Non. C’est l’air qui le retient.')]),
        ],
    ),

    # ------------------------------------------------------------------ 43
    (
        'La conservation des produits agricoles', AGRO, '2026-10-21', 43,
        'Pour conserver nos produits agricoles, on procède par la congélation, le séchage et le '
        'fumage, l’embouteillage et le salage, la fermentation, et en enfouissant dans la '
        'terre. Chaque procédé empêche la récolte de pourrir, soit en enlevant l’eau, soit en '
        'la mettant au froid ou à l’abri de l’air.',
        'kv-cp-couv',
        'Le soleil, un réfrigérateur, une jarre et un trou dans la terre.',
        [
            ('liste',
             'On conserve les produits agricoles par la congélation, le séchage, le fumage, '
             'l’embouteillage, le salage, la fermentation, ou en les enfouissant dans la terre.',
             'kv-cp-liste',
             'La liste numérotée des cinq procédés de conservation.',
             [('simple', 'Une récolte pourrit parce qu’elle est mouillée et au chaud. Chaque '
                         'procédé enlève l’un des deux.'),
              ('histoire', 'La grand-mère n’a pas de réfrigérateur. Elle enfouit ses tubercules '
                           'dans la terre, et ils tiennent jusqu’à la saison suivante.')],
             [('qcm', 1, {'question': 'Pourquoi conserve-t-on les récoltes ?',
                          'options': ['pour qu’elles ne pourrissent pas',
                                      'pour qu’elles pèsent plus', 'pour les rendre plus '
                                      'jolies']},
               {'index': 0}, 'Pour qu’elles ne pourrissent pas.'),
              ('qcm', 1, {'question': 'Lequel est un procédé de conservation ?',
                          'options': ['le séchage', 'le labour', 'le semis']},
               {'index': 0}, 'Le séchage.'),
              ('association', 2, {'question': 'Relie chaque procédé à ce qu’il utilise.',
                                  'gauche': ['la congélation', 'le séchage', 'le fumage'],
                                  'droite': ['le froid', 'le soleil', 'la fumée']},
               {'order': [0, 1, 2]}, 'Le froid, le soleil, la fumée.'),
              ('texte_a_trous', 3,
               {'text': 'Mettre la récolte dans un trou creusé, c’est l’{{1}} dans la terre.',
                'blanks': 1},
               {'values': ['enfouir']}, 'L’enfouir dans la terre.'),
              ('vrai_faux', 4, {'statement': 'Une récolte bien conservée se garde plus '
                                             'longtemps.'},
               {'value': True}, 'Oui, c’est tout le but.')]),

            ('relation',
             'La congélation garde les produits au froid. Le froid empêche ce qui fait pourrir '
             'de travailler.',
             'kv-cp-froid',
             'Un réfrigérateur.',
             [('simple', 'Le froid ne tue pas ce qui gâte les aliments : il l’arrête.'),
              ('pas_a_pas', 'On met au congélateur, on laisse, et on ne sort qu’au moment de '
                            'cuisiner.')],
             [('qcm', 1, {'question': 'Que fait la congélation ?',
                          'options': ['elle garde au froid', 'elle garde au chaud',
                                      'elle garde au soleil']},
               {'index': 0}, 'Elle garde au froid.'),
              ('texte_a_trous', 1, {'text': 'La congélation garde les aliments au {{1}}.',
                                    'blanks': 1},
               {'values': ['froid']}, 'Au froid.'),
              ('qcm', 2, {'question': 'Que se passe-t-il quand l’aliment se réchauffe ?',
                          'options': ['il recommence à pourrir', 'il reste bon pour toujours',
                                      'il devient plus dur']},
               {'index': 0}, 'Il recommence à pourrir.'),
              ('texte_a_trous', 3,
               {'text': 'On range la viande et le poisson dans le {{1}}.', 'blanks': 1},
               {'values': ['congélateur']}, 'Le congélateur.'),
              ('vrai_faux', 4, {'statement': 'Un aliment sorti du congélateur se garde pour '
                                             'toujours.'},
               {'value': False}, 'Non. Une fois réchauffé, il s’abîme.')]),

            ('relation',
             'Le séchage et le fumage enlèvent l’eau du produit. Ce qui est sec ne pourrit pas.',
             'kv-cp-sechage',
             'Le soleil pour le séchage, le feu et la fumée pour le fumage.',
             [('simple', 'Sans eau, rien ne peut pourrir à l’intérieur.'),
              ('visuel', 'Le maïs étalé sur une natte dans la cour est en train d’être '
                         'conservé, pas seulement posé là.')],
             [('texte_a_trous', 1,
               {'text': 'Le séchage enlève l’{{1}} du produit.', 'blanks': 1},
               {'values': ['eau']}, 'L’eau.'),
              ('qcm', 1, {'question': 'Qu’est-ce qui sèche le maïs dans la cour ?',
                          'options': ['le soleil', 'la pluie', 'la nuit']},
               {'index': 0}, 'Le soleil.'),
              ('qcm', 2, {'question': 'Le fumage utilise quoi ?',
                          'options': ['la fumée du feu', 'l’eau de la rivière',
                                      'le sable chaud']},
               {'index': 0}, 'La fumée du feu.'),
              ('texte_a_trous', 3,
               {'text': 'Un produit {{1}} ne pourrit pas.', 'blanks': 1},
               {'values': ['sec']}, 'Un produit sec.'),
              ('vrai_faux', 4, {'statement': 'Le séchage et le fumage enlèvent tous les deux '
                                             'l’eau.'},
               {'value': True}, 'Oui, de deux façons différentes.')]),

            ('relation',
             'L’embouteillage et le salage mettent le produit à l’abri. La bouteille ferme, et '
             'le sel tire l’eau.',
             'kv-cp-salage',
             'Une bouteille et une salière, nommées.',
             [('simple', 'La bouteille empêche l’air d’entrer. Le sel, lui, fait sortir l’eau.'),
              ('analogie', 'Une bouteille fermée, c’est une lettre dans une enveloppe collée : '
                           'rien n’atteint ce qu’il y a dedans.')],
             [('qcm', 1, {'question': 'Que fait le sel sur la viande ?',
                          'options': ['il en fait sortir l’eau', 'il y ajoute de l’eau',
                                      'il la fait cuire']},
               {'index': 0}, 'Il en fait sortir l’eau.'),
              ('texte_a_trous', 1,
               {'text': 'On conserve l’eau et le jus par l’{{1}}.', 'blanks': 1},
               {'values': ['embouteillage']}, 'L’embouteillage.'),
              ('qcm', 2, {'question': 'Qu’est-ce que la bouteille empêche d’entrer ?',
                          'options': ['l’air', 'le verre', 'le bouchon']},
               {'index': 0}, 'L’air.'),
              ('texte_a_trous', 3,
               {'text': 'Conserver la viande avec du sel, c’est le {{1}}.', 'blanks': 1},
               {'values': ['salage']}, 'Le salage.'),
              ('vrai_faux', 4, {'statement': 'Une bouteille ouverte conserve aussi bien qu’une '
                                             'bouteille fermée.'},
               {'value': False}, 'Non. Une fois ouverte, l’air entre.')]),

            ('relation',
             'La fermentation et l’enfouissement dans la terre sont deux procédés anciens, et '
             'ils marchent sans aucune machine.',
             'kv-cp-terre',
             'Une jarre pour la fermentation, et un trou dans la terre.',
             [('simple', 'On n’a besoin ni d’électricité ni d’argent : une jarre, ou un trou.'),
              ('histoire', 'C’est le procédé de la grand-mère quand il n’y a pas de courant au '
                           'village, et il tient toute la saison sèche.')],
             [('qcm', 1, {'question': 'Où enfouit-on les produits à conserver ?',
                          'options': ['dans la terre', 'sur le toit', 'dans la rivière']},
               {'index': 0}, 'Dans la terre.'),
              ('texte_a_trous', 1,
               {'text': 'On peut conserver un produit en l’enfouissant dans la {{1}}.',
                'blanks': 1},
               {'values': ['terre']}, 'Dans la terre.'),
              ('qcm', 2, {'question': 'Ces deux procédés ont besoin de quoi ?',
                          'options': ['de rien de particulier', 'd’électricité',
                                      'd’un grand four']},
               {'index': 0}, 'De rien de particulier.'),
              ('texte_a_trous', 3,
               {'text': 'Laisser un produit changer tout seul dans une jarre, c’est la {{1}}.',
                'blanks': 1},
               {'values': ['fermentation']}, 'La fermentation.'),
              ('vrai_faux', 4, {'statement': 'On peut conserver une récolte sans électricité.'},
               {'value': True}, 'Oui : séchage, salage, enfouissement, fermentation.')]),
        ],
    ),

    # ------------------------------------------------------------------ 44
    (
        'Les modes de locomotion des animaux', VIE, '2026-10-26', 44,
        'Les animaux ont divers modes de locomotion : la marche, comme le chien et le chat ; le '
        'saut, comme le lapin et la grenouille ; le vol, comme les oiseaux et les insectes ; la '
        'nage, comme les poissons et l’étoile de mer ; et le rampement, comme le serpent, le '
        'ver de terre et l’escargot.',
        'kv-lo-couv',
        'Quatre animaux qui se déplacent chacun à sa façon.',
        [
            ('liste',
             'Les animaux ont divers modes de locomotion : la marche, le saut, le vol, la nage '
             'et le rampement.',
             'kv-lo-def',
             'Quatre vignettes nommées : la marche, le saut, le vol, la nage.',
             [('simple', 'Cinq façons de se déplacer. Un animal en a presque toujours une '
                         'seule.'),
              ('pas_a_pas', 'Regarde ce qui touche le sol : des pattes, des ailes, une '
                            'nageoire, ou le corps entier.')],
             [('qcm', 1, {'question': 'Combien de modes de locomotion la leçon donne-t-elle ?',
                          'options': ['cinq', 'deux', 'dix']},
               {'index': 0}, 'Cinq.'),
              ('texte_a_trous', 1,
               {'text': 'La façon dont un animal se déplace est son mode de {{1}}.',
                'blanks': 1},
               {'values': ['locomotion']}, 'De locomotion.'),
              ('association', 2, {'question': 'Relie chaque animal à sa façon de se déplacer.',
                                  'gauche': ['le chien', 'l’oiseau', 'le poisson'],
                                  'droite': ['il marche', 'il vole', 'il nage']},
               {'order': [0, 1, 2]}, 'Marcher, voler, nager.'),
              ('texte_a_trous', 3,
               {'text': 'Les animaux ont divers modes de {{1}}.', 'blanks': 1},
               {'values': ['locomotion']}, 'De locomotion.'),
              ('vrai_faux', 4, {'statement': 'Tous les animaux se déplacent de la même façon.'},
               {'value': False}, 'Non, il y a cinq modes différents.')]),

            ('relation',
             'La marche est le mode de locomotion du chien et du chat. Ils avancent sur leurs '
             'pattes.',
             'kv-lo-marche',
             'Un animal à quatre pattes.',
             [('simple', 'Les pattes se posent l’une après l’autre sur le sol.'),
              ('visuel', 'Compte les pattes sur l’image : quatre, posées par terre.')],
             [('qcm', 1, {'question': 'Quel animal marche ?',
                          'options': ['le chien', 'le poisson', 'l’aigle']},
               {'index': 0}, 'Le chien.'),
              ('texte_a_trous', 1, {'text': 'Le chien et le chat avancent sur leurs {{1}}.',
                                    'blanks': 1},
               {'values': ['pattes']}, 'Sur leurs pattes.'),
              ('qcm', 2, {'question': 'Le mode de locomotion du chat est…',
                          'options': ['la marche', 'la nage', 'le vol']},
               {'index': 0}, 'La marche.'),
              ('texte_a_trous', 3, {'text': 'Se déplacer en posant ses pattes, c’est la {{1}}.',
                                    'blanks': 1},
               {'values': ['marche']}, 'La marche.'),
              ('vrai_faux', 4, {'statement': 'Le chat se déplace par la marche.'},
               {'value': True}, 'Oui, comme le chien.')]),

            ('relation',
             'Le saut est le mode de locomotion du lapin et de la grenouille. Ils poussent fort '
             'sur leurs pattes arrière.',
             'kv-lo-saut',
             'Un lapin.',
             [('simple', 'Leurs pattes de derrière sont longues et fortes : c’est elles qui '
                         'lancent.'),
              ('analogie', 'Comme un ressort qu’on appuie puis qu’on lâche.')],
             [('qcm', 1, {'question': 'Quel animal saute ?',
                          'options': ['la grenouille', 'le poisson', 'le serpent']},
               {'index': 0}, 'La grenouille.'),
              ('texte_a_trous', 1, {'text': 'Le lapin se déplace par le {{1}}.', 'blanks': 1},
               {'values': ['saut']}, 'Par le saut.'),
              ('qcm', 2, {'question': 'Quelles pattes servent à sauter ?',
                          'options': ['celles de derrière', 'celles de devant',
                                      'aucune des deux']},
               {'index': 0}, 'Celles de derrière.'),
              ('association', 3, {'question': 'Relie chaque animal à son mode.',
                                  'gauche': ['le lapin', 'le chat'],
                                  'droite': ['le saut', 'la marche']},
               {'order': [0, 1]}, 'Sauter, ou marcher.'),
              ('vrai_faux', 4, {'statement': 'La grenouille et le lapin se déplacent tous les '
                                             'deux par le saut.'},
               {'value': True}, 'Oui, tous les deux.')]),

            ('relation',
             'Le vol est le mode de locomotion des oiseaux et des insectes. Ils se déplacent '
             'dans l’air avec leurs ailes.',
             'kv-lo-vol',
             'Un oiseau en vol.',
             [('simple', 'Les ailes poussent sur l’air, comme la rame pousse sur l’eau.'),
              ('visuel', 'Un animal qui vole a toujours des ailes, grandes ou petites.')],
             [('texte_a_trous', 1, {'text': 'Les oiseaux se déplacent grâce à leurs {{1}}.',
                                    'blanks': 1},
               {'values': ['ailes']}, 'Leurs ailes.'),
              ('qcm', 1, {'question': 'Quel animal vole ?',
                          'options': ['l’oiseau', 'l’escargot', 'la vache']},
               {'index': 0}, 'L’oiseau.'),
              ('qcm', 2, {'question': 'Qui vole aussi, à part les oiseaux ?',
                          'options': ['les insectes', 'les poissons', 'les serpents']},
               {'index': 0}, 'Les insectes.'),
              ('texte_a_trous', 3,
               {'text': 'Se déplacer dans l’air, c’est le {{1}}.', 'blanks': 1},
               {'values': ['vol']}, 'Le vol.'),
              ('vrai_faux', 4, {'statement': 'Un animal qui vole a besoin d’ailes.'},
               {'value': True}, 'Oui, ce sont elles qui le portent.')]),

            ('relation',
             'La nage est le mode de locomotion des poissons et de l’étoile de mer. Ils se '
             'déplacent dans l’eau.',
             'kv-lo-nage',
             'Un poisson.',
             [('simple', 'Le poisson pousse l’eau avec sa queue et ses nageoires.'),
              ('pas_a_pas', 'Regarde où vit l’animal : s’il vit dans l’eau, il nage presque '
                            'toujours.')],
             [('qcm', 1, {'question': 'Où se déplace un animal qui nage ?',
                          'options': ['dans l’eau', 'dans l’air', 'sous la terre']},
               {'index': 0}, 'Dans l’eau.'),
              ('texte_a_trous', 1, {'text': 'Le poisson se déplace par la {{1}}.', 'blanks': 1},
               {'values': ['nage']}, 'Par la nage.'),
              ('qcm', 2, {'question': 'Avec quoi le poisson pousse-t-il l’eau ?',
                          'options': ['sa queue et ses nageoires', 'ses quatre pattes',
                                      'ses deux grandes ailes']},
               {'index': 0}, 'Sa queue et ses nageoires.'),
              ('texte_a_trous', 3,
               {'text': 'L’étoile de mer vit dans l’{{1}}.', 'blanks': 1},
               {'values': ['eau']}, 'Dans l’eau.'),
              ('vrai_faux', 4, {'statement': 'Un poisson sorti de l’eau peut encore nager.'},
               {'value': False}, 'Non. Il lui faut l’eau pour se déplacer.')]),

            ('relation',
             'Le rampement est le mode de locomotion du serpent, du ver de terre et de '
             'l’escargot. Ils se déplacent le corps contre le sol.',
             'kv-lo-rampement',
             'Un serpent qui ondule.',
             [('simple', 'Ils n’ont pas de pattes : c’est tout le corps qui avance.'),
              ('visuel', 'Sur l’image, le corps du serpent fait des vagues. C’est ce mouvement '
                         'qui le fait avancer.')],
             [('texte_a_trous', 1,
               {'text': 'Le serpent se déplace par le {{1}}.', 'blanks': 1},
               {'values': ['rampement']}, 'Par le rampement.'),
              ('qcm', 1, {'question': 'Quel animal rampe ?',
                          'options': ['l’escargot', 'le lapin', 'l’aigle']},
               {'index': 0}, 'L’escargot.'),
              ('qcm', 2, {'question': 'Qu’est-ce que les animaux qui rampent n’ont pas ?',
                          'options': ['de pattes', 'de tête', 'de bouche']},
               {'index': 0}, 'De pattes.'),
              ('association', 3, {'question': 'Relie chaque animal à son mode de locomotion.',
                                  'gauche': ['le ver de terre', 'le poisson', 'l’oiseau'],
                                  'droite': ['le rampement', 'la nage', 'le vol']},
               {'order': [0, 1, 2]}, 'Ramper, nager, voler.'),
              ('vrai_faux', 4, {'statement': 'Le ver de terre se déplace grâce à ses pattes.'},
               {'value': False}, 'Non. Il n’a pas de pattes, il rampe.')]),
        ],
    ),

    # ------------------------------------------------------------------ 45
    (
        'La nutrition chez les animaux', VIE, '2026-10-19', 45,
        'La ration alimentaire des animaux est variée. Les herbivores se nourrissent de '
        'végétaux, comme la chèvre, le mouton et la vache. Les carnivores se nourrissent de '
        'viande, comme le chien, le chat et le lion. Les omnivores mangent de tout, comme le '
        'porc, le canard et l’ours.',
        'kv-nu-couv',
        'Une chèvre et de l’herbe, puis de la viande et un serpent.',
        [
            ('definition',
             'La ration alimentaire des animaux est variée : certains mangent des végétaux, '
             'd’autres de la viande, et d’autres les deux.',
             'kv-nu-def',
             'Trois vignettes : de l’herbe, de la viande, et les deux ensemble.',
             [('simple', 'On classe un animal non pas sur sa taille, mais sur ce qu’il met dans '
                         'sa bouche.'),
              ('pas_a_pas', 'Pose une seule question : que mange-t-il ? Des plantes, de la '
                            'viande, ou les deux ?')],
             [('qcm', 1, {'question': 'Sur quoi classe-t-on les animaux dans cette leçon ?',
                          'options': ['sur ce qu’ils mangent', 'sur leur couleur',
                                      'sur leur taille']},
               {'index': 0}, 'Sur ce qu’ils mangent.'),
              ('texte_a_trous', 1,
               {'text': 'La ration alimentaire des animaux est {{1}}.', 'blanks': 1},
               {'values': ['variée']}, 'Elle est variée.'),
              ('association', 2, {'question': 'Relie chaque régime à ce qu’il mange.',
                                  'gauche': ['herbivore', 'carnivore', 'omnivore'],
                                  'droite': ['des végétaux', 'de la viande', 'de tout']},
               {'order': [0, 1, 2]}, 'Des végétaux, de la viande, de tout.'),
              ('qcm', 3, {'question': 'Combien de régimes la leçon donne-t-elle ?',
                          'options': ['trois', 'deux', 'six']},
               {'index': 0}, 'Trois.'),
              ('vrai_faux', 4, {'statement': 'Tous les animaux mangent la même chose.'},
               {'value': False}, 'Non, leur ration est variée.')]),

            ('relation',
             'Les herbivores se nourrissent de végétaux. La chèvre, le mouton et la vache sont '
             'des herbivores.',
             'kv-nu-herbivore',
             'Une chèvre, une flèche, et de l’herbe.',
             [('simple', 'Végétal veut dire plante : l’herbe, les feuilles, les tiges.'),
              ('visuel', 'Sur l’image, l’animal est tourné vers l’herbe, et rien d’autre.')],
             [('texte_a_trous', 1,
               {'text': 'Les animaux qui mangent des végétaux sont des {{1}}.', 'blanks': 1},
               {'values': ['herbivores']}, 'Des herbivores.'),
              ('qcm', 1, {'question': 'Lequel est un herbivore ?',
                          'options': ['la vache', 'le lion', 'le chat']},
               {'index': 0}, 'La vache.'),
              ('qcm', 2, {'question': 'Que mange un herbivore ?',
                          'options': ['des végétaux', 'de la viande', 'des pierres']},
               {'index': 0}, 'Des végétaux.'),
              ('texte_a_trous', 3,
               {'text': 'La chèvre, le mouton et la {{1}} sont des herbivores.', 'blanks': 1},
               {'values': ['vache']}, 'Et la vache.'),
              ('vrai_faux', 4, {'statement': 'Un herbivore mange de la viande de temps en '
                                             'temps.'},
               {'value': False}, 'Non. Il se nourrit de végétaux.')]),

            ('relation',
             'Les carnivores se nourrissent de viande. Le chien, le chat et le lion sont des '
             'carnivores.',
             'kv-nu-carnivore',
             'Un animal, une flèche, et un morceau de viande.',
             [('simple', 'Carnivore vient d’un mot qui veut dire chair.'),
              ('visuel', 'Sur l’image, c’est la viande qui est au bout de la flèche.')],
             [('texte_a_trous', 1,
               {'text': 'Les animaux qui mangent de la viande sont des {{1}}.', 'blanks': 1},
               {'values': ['carnivores']}, 'Des carnivores.'),
              ('qcm', 1, {'question': 'Lequel est un carnivore ?',
                          'options': ['le lion', 'la chèvre', 'le mouton']},
               {'index': 0}, 'Le lion.'),
              ('qcm', 2, {'question': 'Le chat est un…',
                          'options': ['carnivore', 'herbivore', 'végétal']},
               {'index': 0}, 'Un carnivore.'),
              ('texte_a_trous', 3,
               {'text': 'Le chien, le chat et le {{1}} sont des carnivores.', 'blanks': 1},
               {'values': ['lion']}, 'Et le lion.'),
              ('vrai_faux', 4, {'statement': 'Le lion et la vache ont le même régime.'},
               {'value': False}, 'Non. L’un est carnivore, l’autre herbivore.')]),

            ('relation',
             'Les omnivores mangent de tout, des végétaux comme de la viande. Le porc, le canard '
             'et l’ours sont des omnivores.',
             'kv-nu-omnivore',
             'Un animal entre de l’herbe et de la viande, avec le mot omnivore.',
             [('simple', 'Omni veut dire tout. Un omnivore ne refuse ni l’herbe ni la viande.'),
              ('histoire', 'Le porc du village mange les épluchures de la cuisine et les restes '
                           'de viande. Rien ne se perd, et c’est pour cela qu’on l’élève.')],
             [('texte_a_trous', 1,
               {'text': 'Les animaux qui mangent de tout sont des {{1}}.', 'blanks': 1},
               {'values': ['omnivores']}, 'Des omnivores.'),
              ('qcm', 1, {'question': 'Lequel est un omnivore ?',
                          'options': ['le porc', 'la vache', 'le lion']},
               {'index': 0}, 'Le porc.'),
              ('association', 2, {'question': 'Relie chaque animal à son régime.',
                                  'gauche': ['la chèvre', 'le lion', 'le canard'],
                                  'droite': ['herbivore', 'carnivore', 'omnivore']},
               {'order': [0, 1, 2]}, 'Végétaux, viande, les deux.'),
              ('texte_a_trous', 3,
               {'text': 'Le porc, le canard et l’{{1}} sont des omnivores.', 'blanks': 1},
               {'values': ['ours']}, 'Et l’ours.'),
              ('vrai_faux', 4, {'statement': 'Un omnivore mange des végétaux et de la viande.'},
               {'value': True}, 'Oui, les deux.')]),
        ],
    ),

    # ------------------------------------------------------------------ 46
    (
        'La combustion', CHIMIE, '2026-10-27', 46,
        'La combustion est la décomposition d’un corps par l’action du feu ou de l’air. Les '
        'corps combustibles sont ceux qui peuvent brûler : le papier, le coton, le bois, le '
        'plastique, le gaz, l’essence, le pétrole, la cire et le cuir. D’autres corps, comme '
        'l’eau et le fer, ne brûlent pas.',
        'kv-co-couv',
        'Une flamme.',
        [
            ('definition',
             'La combustion est la décomposition d’un corps par l’action du feu ou de l’air.',
             'kv-co-def',
             'Une flamme seule.',
             [('simple', 'Décomposer veut dire défaire. Le feu défait ce qu’il brûle.'),
              ('visuel', 'Après la combustion il reste de la cendre : ce n’est plus le même '
                         'corps.')],
             [('texte_a_trous', 1,
               {'text': 'La décomposition d’un corps par l’action du feu est la {{1}}.',
                'blanks': 1},
               {'values': ['combustion']}, 'La combustion.'),
              ('qcm', 1, {'question': 'Qu’est-ce qui provoque la combustion ?',
                          'options': ['le feu ou l’air', 'le froid', 'la pluie']},
               {'index': 0}, 'Le feu ou l’air.'),
              ('qcm', 2, {'question': 'Que reste-t-il après la combustion du bois ?',
                          'options': ['de la cendre', 'du bois neuf', 'de l’eau']},
               {'index': 0}, 'De la cendre.'),
              ('texte_a_trous', 3,
               {'text': 'La combustion est une {{1}} du corps qui brûle.', 'blanks': 1},
               {'values': ['décomposition']}, 'Une décomposition.'),
              ('vrai_faux', 4, {'statement': 'Après avoir brûlé, un corps est resté exactement '
                                             'le même.'},
               {'value': False}, 'Non. Il a été décomposé.')]),

            ('liste',
             'Les corps combustibles sont ceux qui peuvent brûler : le papier, le coton, le '
             'bois, le plastique, le gaz, l’essence, le pétrole, la cire et le cuir.',
             'kv-co-combustibles',
             'Quatre vignettes nommées : le papier, le bois, l’essence, le pétrole.',
             [('simple', 'Combustible veut dire : qui peut brûler.'),
              ('pas_a_pas', 'Beaucoup viennent d’une plante ou du pétrole. C’est un bon indice '
                            'quand on hésite.')],
             [('texte_a_trous', 1,
               {'text': 'Un corps qui peut brûler est un corps {{1}}.', 'blanks': 1},
               {'values': ['combustible']}, 'Un corps combustible.'),
              ('qcm', 1, {'question': 'Lequel est combustible ?',
                          'options': ['le bois', 'l’eau', 'le fer']},
               {'index': 0}, 'Le bois.'),
              ('qcm', 2, {'question': 'Parmi ces corps, lequel brûle ?',
                          'options': ['l’essence', 'le sable', 'la pierre']},
               {'index': 0}, 'L’essence.'),
              ('texte_a_trous', 3,
               {'text': 'Le papier, le coton et le {{1}} sont combustibles.', 'blanks': 1},
               {'values': ['bois']}, 'Et le bois.'),
              ('vrai_faux', 4, {'statement': 'Le carton est un corps combustible.'},
               {'value': True}, 'Oui, comme le papier dont il est fait.')]),

            ('relation',
             'Certains corps ne brûlent pas : l’eau, le fer, la pierre et le sable. On les dit '
             'incombustibles.',
             'kv-co-incombustibles',
             'Un verre d’eau et une bêche en fer, nommés.',
             [('simple', 'In veut dire non. Incombustible : qui ne brûle pas.'),
              ('analogie', 'C’est pour cela qu’on fait cuire dans une marmite en fer et pas '
                           'dans un carton.')],
             [('texte_a_trous', 1,
               {'text': 'Un corps qui ne brûle pas est {{1}}.', 'blanks': 1},
               {'values': ['incombustible']}, 'Incombustible.'),
              ('qcm', 1, {'question': 'Lequel ne brûle pas ?',
                          'options': ['le fer', 'le coton', 'la cire']},
               {'index': 0}, 'Le fer.'),
              ('qcm', 2, {'question': 'Pourquoi la marmite est-elle en fer ?',
                          'options': ['parce que le fer ne brûle pas',
                                      'parce que le fer est léger',
                                      'parce que le fer est joli']},
               {'index': 0}, 'Parce que le fer ne brûle pas.'),
              ('association', 3, {'question': 'Range chaque corps.',
                                  'gauche': ['le bois', 'l’eau', 'le papier'],
                                  'droite': ['il brûle', 'il ne brûle pas',
                                             'il brûle aussi']},
               {'order': [0, 1, 2]}, 'Deux brûlent, un ne brûle pas.'),
              ('vrai_faux', 4, {'statement': 'L’eau est un corps combustible.'},
               {'value': False}, 'Non. L’eau éteint le feu, elle ne brûle pas.')]),

            ('relation',
             'Le feu est dangereux. On ne joue jamais avec, et on appelle toujours un adulte.',
             'kv-co-prudence',
             'Une flamme barrée, avec le signe de l’interdit.',
             [('simple', 'Ce qui brûle le bois brûle aussi la peau.'),
              ('pas_a_pas', 'Si tu vois un feu qui n’est pas surveillé, tu ne t’approches pas '
                            'et tu appelles un grand.')],
             [('qcm', 1, {'question': 'Que fait-on quand on voit un feu non surveillé ?',
                          'options': ['on appelle un adulte', 'on souffle dessus',
                                      'on y met du papier']},
               {'index': 0}, 'On appelle un adulte.'),
              ('vrai_faux', 1, {'statement': 'On peut jouer avec le feu si on fait attention.'},
               {'value': False}, 'Non, jamais.'),
              ('qcm', 2, {'question': 'Qu’est-ce qui éteint le feu ?',
                          'options': ['l’eau', 'l’essence', 'le papier']},
               {'index': 0}, 'L’eau.'),
              ('texte_a_trous', 3,
               {'text': 'Le feu est {{1}} : on ne joue jamais avec.', 'blanks': 1},
               {'values': ['dangereux']}, 'Il est dangereux.'),
              ('vrai_faux', 4, {'statement': 'Verser de l’essence sur un feu est une bonne idée '
                                             'pour l’éteindre.'},
               {'value': False}, 'Non. L’essence brûle : le feu grandirait.')]),
        ],
    ),
]


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, cles_items, total, notions_vues, trous = set(), set(), 0, 0, 0
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
                if ikind == 'texte_a_trous':
                    trous += 1
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, \
                        'question trop longue (%d) : %s' % (len(payload['question']),
                                                            payload['question'])
                    assert ('options' in payload) != ('images' in payload), payload
                    choix = payload.get('options') or payload['images']
                    assert 2 <= len(choix) <= 4, payload
                    assert len(set(choix)) == len(choix), 'choix en double : ' + str(payload)
                    assert 0 <= answer['index'] < len(choix), payload
                    if 'images' in payload:
                        cles_items.update(choix)
                    else:
                        for o in choix:
                            assert len(o) <= 70, 'option trop longue : ' + o
                        bonne = len(choix[answer['index']])
                        autres = [len(o) for k, o in enumerate(choix) if k != answer['index']]
                        assert bonne <= max(autres) * 2, \
                            'bonne réponse bien plus longue que les autres : ' \
                            + payload['question']
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']),
                                                               payload['statement'])
                elif ikind == 'texte_a_trous':
                    n = payload['text'].count('{{')
                    assert n == len(answer['values']) == payload['blanks'], payload
                    assert n <= 2, 'plus de deux trous : ' + payload['text']
                    for v in answer['values']:
                        assert ' ' not in v, 'réponse en plusieurs mots : ' + v
                        assert v.isalpha(), 'réponse non tapable au clavier : ' + v
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

    # Les quatre leçons déjà faites ne doivent pas être refaites.
    tout = json.dumps([l[0] for l in LECONS], ensure_ascii=False)
    for deja in ('reproduction', 'soins aux animaux', 'milieux de vie', 'filtre'):
        assert deja not in tout.lower(), 'cette leçon existe déjà chez KLEIN : ' + deja

    ici = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location(
        'fig', os.path.join(ici, 'figures-klein-sciences-nov.py'))
    fig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fig)
    dessinees = {c for c, _w, _h, _f in fig.FIGURES}
    utilisees = cles | cles_items
    manquantes = utilisees - dessinees
    inutiles = dessinees - utilisees
    assert not manquantes, 'images demandées mais jamais dessinées : ' + ', '.join(
        sorted(manquantes))
    assert not inutiles, 'images dessinées mais jamais utilisées : ' + ', '.join(sorted(inutiles))
    return len(utilisees), total, notions_vues, trous


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
    chemin = os.path.join(racine, 'app', 'public', 'seed-klein-sciences-nov.json')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(paquet(), ensure_ascii=False))

    print('%d lecons - %d notions - %d questions dont %d a trous (%.0f%%) - %d images'
          % (len(LECONS), notions, items, trous, 100.0 * trous / items, images))
    for titre, chapitre, date, ordre, _r, _i, _p, ns in LECONS:
        print('  %2d  %-42s %-26s %d notions' % (ordre, titre, chapitre, len(ns)))
    print(chemin)
