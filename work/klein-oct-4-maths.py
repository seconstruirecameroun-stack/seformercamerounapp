# -*- coding: utf-8 -*-
# Mathématiques — neuf leçons. Chargé par lecons-klein-cahier-oct.py.
#
# Trois leçons du même cahier sont déjà dans l-app et ne sont pas refaites :
# les nombres de 101 à 999, le cube, les sous-multiples du mètre.
#
# Les symboles des ensembles s-écrivent dans les questions, où l-app les
# affiche. Les fiches, elles, ne portent que leurs noms : la police de l-app
# n-a pas ces cinq signes, et une image ne doit pas montrer un carré vide à la
# place d-un symbole.

MA = 'Mathématiques'
NOMBRES = 'Nombres et calculs'
GEO = 'Géométrie'
MESURES = 'Mesures et grandeurs'

LECONS = [
    # ------------------------------------------------------------ 12 octobre
    L(MA, 'La centaine', NOMBRES, '2026-10-12',
      'La centaine représente le nombre 100. C’est le premier nombre à 3 chiffres. La '
      'centaine est égale à 10 dizaines et 100 unités. 100 s’écrit cent, et il prend un s '
      'quand il est multiplié : 200 s’écrit deux cents.',
      'kcm-ce-couv', ['100', '10 dizaines', '100 unités'],

      N('definition',
        'La centaine représente le nombre 100. C’est le premier nombre à 3 chiffres.',
        'kcm-ce-def', F('La centaine', 'le nombre 100', 'le premier nombre', 'à 3 chiffres'),
        ('simple', 'Avant 100, les nombres ont un ou deux chiffres. 100 en a trois.'),
        ('visuel', '99 a deux chiffres. On ajoute 1 : 100, et il y a trois chiffres.'),
        Q('Quel nombre la centaine représente-t-elle ?', '100', '10', '1 000'),
        V('100 est le premier nombre à 3 chiffres.', True),
        T('La centaine représente le nombre {{1}}.', '100'),
        Q('Combien de chiffres a le nombre 100 ?', 'Trois', 'Deux', 'Quatre', n=3),
        V('99 est le premier nombre à 3 chiffres.', False, n=4,
          e='Non. 99 a deux chiffres. Le premier à trois chiffres est 100.')),

      N('relation',
        'La centaine est égale à 10 dizaines et à 100 unités. 1 c = 10 d. 1 c = 100 u.',
        'kcm-ce-egal', P('Une centaine', ('1 c', '10 d'), ('1 c', '100 u')),
        ('simple', 'Dix paquets de dix font cent.'),
        ('visuel', 'Dans le tableau c, d, u : 1 dans la colonne c, puis 0 et 0.'),
        Q('Une centaine est égale à combien de dizaines ?', '10', '100', '1'),
        V('Une centaine est égale à 100 unités.', True),
        T('1 centaine = {{1}} dizaines.', '10'),
        T('1 centaine = {{1}} unités.', '100', n=3),
        V('Une centaine est égale à 10 unités.', False, n=4,
          e='Non. 10 unités font une dizaine. Une centaine fait 100 unités.')),

      N('relation',
        '100 s’écrit cent. Il prend un s quand il est multiplié. Exemple : 200 s’écrit deux '
        'cents.',
        'kcm-ce-ecrire', P('En lettres', ('100', 'cent'), ('200', 'deux cents')),
        ('simple', 'Un seul cent : pas de s. Plusieurs cents : un s.'),
        ('visuel', 'Deux cents : il y en a deux, donc un s, comme deux chats.'),
        Q('Comment écrit-on 200 en lettres ?', 'deux cents', 'deux cent', 'deux-cens'),
        V('100 s’écrit « cent ».', True),
        T('200 s’écrit deux {{1}}.', 'cents'),
        Q('Quand « cent » prend-il un s ?', 'Quand il est multiplié', 'Quand il est seul',
          'Quand il vaut 100', n=3),
        V('100 s’écrit « cents », avec un s.', False, n=4,
          e='Non. Un seul cent : pas de s.')),
      ),

    # ------------------------------------------------------------ 19 octobre
    L(MA, 'Les symboles des ensembles', NOMBRES, '2026-10-19',
      'Cinq symboles : ∈ veut dire appartient ; ∉ veut dire n’appartient pas ; ∩ veut dire '
      'intersection ; ∪ veut dire union ; ∅ veut dire ensemble vide.',
      'kcm-sy-couv', ['appartient', 'intersection', 'union'],

      N('relation',
        'Le symbole ∈ veut dire appartient. Le symbole ∉ veut dire n’appartient pas.',
        'kcm-sy-appartient', F('Deux symboles', 'appartient', 'n’appartient pas',
                               'le second est barré'),
        ('simple', 'Appartenir à un ensemble, c’est être dedans.'),
        ('visuel', 'Le second symbole est le premier avec une barre dessus : la barre dit '
                   'non.'),
        Q('Que veut dire le symbole ∈ ?', 'appartient', 'n’appartient pas', 'union'),
        V('Le symbole ∉ veut dire « n’appartient pas ».', True),
        T('Le symbole ∈ veut dire {{1}}.', 'appartient'),
        Q('Que veut dire le symbole ∉ ?', 'n’appartient pas', 'appartient', 'ensemble vide',
          n=3),
        V('Le symbole ∈ veut dire « n’appartient pas ».', False, n=4,
          e='Non. Sans la barre, il veut dire appartient.')),

      N('relation',
        'Le symbole ∩ veut dire intersection. Le symbole ∪ veut dire union. Le symbole ∅ veut '
        'dire ensemble vide.',
        'kcm-sy-union', F('Trois symboles', 'intersection', 'union', 'ensemble vide'),
        ('simple', 'L’union met tout ensemble. L’intersection garde ce qui est en commun.'),
        ('visuel', 'Le symbole de l’union ressemble à la lettre U, comme Union.'),
        Q('Que veut dire le symbole ∪ ?', 'union', 'intersection', 'appartient'),
        V('Le symbole ∩ veut dire « intersection ».', True),
        T('Le symbole ∅ veut dire ensemble {{1}}.', 'vide'),
        A('Relie chaque symbole à son nom.', ('∈', 'appartient'), ('∩', 'intersection'),
          ('∪', 'union'), ('∅', 'ensemble vide')),
        Q('Que veut dire le symbole ∩ ?', 'intersection', 'union', 'ensemble vide', n=4),
        V('Le symbole ∅ veut dire « union ».', False, n=4, e='Non. Il veut dire ensemble vide.')),
      ),

    # ------------------------------------------------------------ 20 octobre
    L(MA, 'L’addition avec retenue', NOMBRES, '2026-10-20',
      'Pour effectuer une addition avec retenue, je commence par les unités en tenant compte '
      'de la retenue. Exemple : 372 + 29 = 401.',
      'kcm-ad-couv', ['les unités', 'la retenue', '372 + 29'],

      N('definition',
        'Pour effectuer une addition avec retenue, je commence par les unités en tenant '
        'compte de la retenue.',
        'kcm-ad-regle', F('L’addition avec retenue', 'je commence par les unités',
                          'je note la retenue', 'je l’ajoute à la colonne', 'suivante'),
        ('simple', 'Quand une colonne dépasse 9, on garde les unités et on reporte la dizaine.'),
        ('pas_a_pas', '2 + 9 = 11. J’écris 1 et je retiens 1. Je l’ajoute aux dizaines.'),
        Q('Par quelle colonne commence-t-on une addition ?', 'Les unités', 'Les centaines',
          'Les dizaines'),
        V('Dans une addition avec retenue, on tient compte de la retenue.', True),
        T('Pour effectuer une addition, je commence par les {{1}}.', 'unités'),
        Q('2 + 9 = 11. Qu’est-ce que j’écris, et qu’est-ce que je retiens ?',
          'J’écris 1, je retiens 1', 'J’écris 11, je ne retiens rien',
          'J’écris 9, je retiens 2', n=3),
        V('Dans une addition, on commence par les centaines.', False, n=4,
          e='Non. On commence par les unités.')),

      N('relation',
        'Exemple : 372 + 29 = 401.',
        'kcm-ad-exemple', F('Trois additions', '372 + 29 = 401', '587 + 45 = 632',
                            '456 + 274 = 730'),
        ('simple', 'On pose les nombres l’un sous l’autre, unités sous unités.'),
        ('pas_a_pas', '372 + 29 : 2 + 9 = 11, j’écris 1, retenue 1. 7 + 2 + 1 = 10, j’écris 0, '
                      'retenue 1. 3 + 1 = 4. Résultat : 401.'),
        Q('Combien font 372 + 29 ?', '401', '391', '3 101'),
        V('587 + 45 = 632.', True),
        T('372 + 29 = {{1}}.', '401'),
        T('456 + 274 = {{1}}.', '730', n=3),
        Q('Combien font 874 + 227 ?', '1 101', '1 091', '991', n=4),
        V('587 + 45 = 622.', False, n=4, e='Non. 587 + 45 = 632.')),
      ),

    # ------------------------------------------------------------ 21 octobre
    L(MA, 'Le pavé', GEO, '2026-10-21',
      'Le pavé est un solide géométrique qui a 6 faces rectangulaires, 8 sommets et 12 '
      'arêtes.',
      'kcm-pa-couv', ['6 faces', '8 sommets', '12 arêtes'],

      N('definition',
        'Le pavé est un solide géométrique qui a 6 faces rectangulaires.',
        'kcm-pa-faces', F('Le pavé', 'un solide géométrique', '6 faces',
                          'des faces rectangulaires', vif=(2,)),
        ('simple', 'Une boîte de sucre, une brique : ce sont des pavés.'),
        ('visuel', 'Le cube a des faces carrées. Le pavé a des faces rectangulaires.'),
        Q('Combien de faces a le pavé ?', '6', '4', '8'),
        V('Les faces du pavé sont rectangulaires.', True),
        T('Le pavé a {{1}} faces rectangulaires.', '6'),
        Q('Quelle forme ont les faces du pavé ?', 'Rectangulaire', 'Ronde', 'Triangulaire',
          n=3),
        V('Le pavé a 12 faces.', False, n=4, e='Non. Il a 6 faces.')),

      N('liste',
        'Le pavé a 8 sommets et 12 arêtes.',
        'kcm-pa-sommets', F('Le pavé', '8 sommets', '12 arêtes'),
        ('simple', 'Un sommet est un coin. Une arête est un bord entre deux faces.'),
        ('visuel', 'Pose ton doigt sur un coin de la boîte : c’est un sommet.'),
        Q('Combien de sommets a le pavé ?', '8', '6', '12'),
        V('Le pavé a 12 arêtes.', True),
        T('Le pavé a {{1}} arêtes.', '12'),
        A('Relie chaque partie du pavé à son nombre.', ('les faces', '6'), ('les sommets', '8'),
          ('les arêtes', '12')),
        Q('Combien d’arêtes a le pavé ?', '12', '8', '6', n=4),
        V('Le pavé a 6 sommets.', False, n=4, e='Non. Il a 8 sommets.')),
      ),

    # ------------------------------------------------------------ 22 octobre
    L(MA, 'Les mesures de masses', MESURES, '2026-10-22',
      'Le gramme, g, est l’unité principale de masse. Ses multiples sont kg, hg, dag. Ses '
      'sous-multiples sont dg, cg, mg. Pour les convertir, j’utilise le tableau de '
      'conversion.',
      'kcm-ma-couv', ['kg', 'g', 'mg'],

      N('definition',
        'Le gramme, g, est l’unité principale de masse.',
        'kcm-ma-gramme', F('Le gramme', 'il s’écrit g', 'l’unité principale', 'de masse'),
        ('simple', 'La masse dit si un objet est lourd ou léger.'),
        ('visuel', 'Sur un paquet de sucre, on lit des grammes ou des kilogrammes.'),
        Q('Quelle est l’unité principale de masse ?', 'Le gramme', 'Le mètre', 'Le litre'),
        V('Le gramme s’écrit g.', True),
        T('Le {{1}} est l’unité principale de masse.', 'gramme'),
        Q('Que mesure-t-on en grammes ?', 'La masse', 'La longueur', 'Le temps', n=3),
        V('Le mètre est l’unité principale de masse.', False, n=4,
          e='Non. C’est le gramme. Le mètre mesure la longueur.')),

      N('liste',
        'Les multiples du gramme sont : kg, hg, dag. Ses sous-multiples sont : dg, cg, mg.',
        'kcm-ma-multiples', P('Autour du gramme', ('multiples', 'kg, hg, dag'),
                              ('sous-multiples', 'dg, cg, mg')),
        ('simple', 'Les multiples sont plus grands que le gramme. Les sous-multiples sont plus '
                   'petits.'),
        ('visuel', 'kg veut dire kilogramme. mg veut dire milligramme.'),
        Q('Lequel est un multiple du gramme ?', 'kg', 'mg', 'cg'),
        V('Le mg est un sous-multiple du gramme.', True),
        T('Les multiples du gramme sont kg, hg et {{1}}.', 'dag'),
        Q('Lequel est un sous-multiple du gramme ?', 'dg', 'hg', 'kg', n=3),
        V('Le kg est un sous-multiple du gramme.', False, n=4,
          e='Non. Le kg est un multiple : il est plus grand que le gramme.')),

      N('liste',
        'Pour les convertir, j’utilise le tableau de conversion : kg, hg, dag, g, dg, cg, mg.',
        'kcm-ma-tableau', F('Le tableau de conversion', 'kg  hg  dag', 'g', 'dg  cg  mg',
                            vif=(1,)),
        ('simple', 'Le gramme est au milieu. À gauche les plus grands, à droite les plus '
                   'petits.'),
        ('visuel', 'On écrit un seul chiffre par colonne, comme pour les mètres.'),
        Q('Quelle unité est au milieu du tableau de conversion ?', 'g', 'kg', 'mg'),
        V('Dans le tableau, le kg est tout à gauche.', True),
        T('Pour convertir, j’utilise le tableau de {{1}}.', 'conversion'),
        C('Range les unités de la plus grande à la plus petite.', 'kg', 'hg', 'dag', 'g'),
        Q('Quelle unité est tout à droite du tableau de conversion ?', 'mg', 'g', 'kg', n=4)),
      ),

    # ------------------------------------------------------------ 26 octobre
    L(MA, 'Composer et décomposer les nombres à 3 chiffres', NOMBRES, '2026-10-26',
      'Pour décomposer un nombre à 3 chiffres, je le regroupe par centaines, dizaines et '
      'unités : 485 = 4 c 8 d 5 u = 400 + 80 + 5. Pour composer, je rassemble les centaines, '
      'les dizaines et les unités : 4 c 8 d 5 u = 485.',
      'kcm-dc-couv', ['485', '4 c 8 d 5 u', '400 + 80 + 5'],

      N('relation',
        'Pour décomposer un nombre à 3 chiffres, je le regroupe par centaines, dizaines et '
        'unités. Exemple : 485 = 4 c 8 d 5 u = 400 + 80 + 5.',
        'kcm-dc-decomposer', F('Décomposer 485', '4 centaines', '8 dizaines', '5 unités',
                               '400 + 80 + 5'),
        ('simple', 'Décomposer, c’est séparer le nombre en centaines, dizaines et unités.'),
        ('visuel', 'Dans 485 : le 4 vaut 400, le 8 vaut 80, le 5 vaut 5.'),
        Q('Dans 485, combien y a-t-il de centaines ?', '4', '8', '5'),
        V('485 = 400 + 80 + 5.', True),
        T('485 = 400 + {{1}} + 5.', '80'),
        Q('Dans 485, que vaut le chiffre 8 ?', '80', '8', '800', n=3),
        V('485 = 4 c 5 d 8 u.', False, n=4, e='Non. 485 = 4 c 8 d 5 u.')),

      N('relation',
        'Pour composer, je rassemble tous les chiffres : les centaines, les dizaines et les '
        'unités. Exemple : 4 c 8 d 5 u = 485.',
        'kcm-dc-composer', F('Composer', '4 c  8 d  5 u', 'je rassemble', '485', vif=(2,)),
        ('simple', 'Composer, c’est le chemin inverse : on remet les morceaux ensemble.'),
        ('visuel', 'Centaines d’abord, dizaines ensuite, unités à la fin.'),
        Q('Quel nombre est égal à 4 c 8 d 5 u ?', '485', '458', '584'),
        V('4 c 8 d 5 u = 485.', True),
        T('4 c 8 d 5 u = {{1}}.', '485'),
        T('400 + 80 + 5 = {{1}}.', '485', n=3),
        Q('Quel nombre est égal à 3 c 4 d 0 u ?', '340', '304', '34', n=4)),
      ),

    # ------------------------------------------------------------ 27 octobre
    L(MA, 'La soustraction sans emprunt', NOMBRES, '2026-10-27',
      'Pour trouver le reste ou la différence entre 2 nombres, j’effectue la soustraction. Son '
      'signe est −. Je place le plus grand nombre au-dessus et je commence par les unités. '
      'Exemple : 748 − 222 = 526.',
      'kcm-so-couv', ['le reste', 'la différence', '748 - 222'],

      N('definition',
        'Pour trouver le reste ou la différence entre 2 nombres, j’effectue la soustraction. '
        'Son signe est −.',
        'kcm-so-def', F('La soustraction', 'le reste', 'la différence', 'son signe : moins'),
        ('simple', 'Soustraire, c’est enlever.'),
        ('visuel', 'J’ai 7 mangues, j’en donne 2. Il m’en reste 5 : c’est une soustraction.'),
        Q('Quelle opération donne le reste ou la différence ?', 'La soustraction', 'L’addition',
          'La multiplication'),
        V('Le signe de la soustraction est −.', True),
        T('Pour trouver la différence entre 2 nombres, j’effectue la {{1}}.', 'soustraction'),
        Q('Quel est le signe de la soustraction ?', '−', '+', '=', n=3),
        V('Le signe de la soustraction est +.', False, n=4,
          e='Non. + est le signe de l’addition.')),

      N('definition',
        'Pour effectuer la soustraction, je place le plus grand nombre au-dessus et je '
        'commence par les unités. Exemple : 748 − 222 = 526.',
        'kcm-so-poser', F('Poser la soustraction', 'le plus grand au-dessus',
                          'je commence par les unités', '748 - 222 = 526', vif=(2,)),
        ('simple', 'Le grand nombre en haut, le petit en dessous, et on part de la droite.'),
        ('pas_a_pas', '748 − 222 : 8 − 2 = 6, puis 4 − 2 = 2, puis 7 − 2 = 5. Résultat : 526.'),
        Q('Quel nombre place-t-on au-dessus ?', 'Le plus grand', 'Le plus petit',
          'N’importe lequel'),
        V('Dans une soustraction, je commence par les unités.', True),
        T('748 − 222 = {{1}}.', '526'),
        Q('Combien font 748 − 222 ?', '526', '562', '970', n=3),
        V('Dans une soustraction, on place le plus petit nombre au-dessus.', False, n=4,
          e='Non. Le plus grand nombre au-dessus.')),
      ),

    # ------------------------------------------------------------ 28 octobre
    L(MA, 'Le problème', NOMBRES, '2026-10-28',
      'Le problème est un texte composé de 2 parties : l’énoncé, et la question ou la '
      'consigne, qui demande une solution pour le problème.',
      'kcm-pb-couv', ['l’énoncé', 'la question'],

      N('definition',
        'Le problème est un texte composé de 2 parties : l’énoncé, et la question ou la '
        'consigne, qui demande une solution pour le problème.',
        'kcm-pb-def', F('Le problème', '2 parties', 'l’énoncé', 'la question',
                        'ou la consigne'),
        ('simple', 'L’énoncé raconte. La question demande.'),
        ('visuel', 'La question se reconnaît à son point d’interrogation.'),
        Q('De combien de parties est composé un problème ?', '2', '3', '5'),
        V('L’énoncé est une partie du problème.', True),
        T('Un problème a deux parties : l’énoncé et la {{1}}.', 'question'),
        Q('Quelle partie demande une solution ?', 'La question', 'L’énoncé', 'Le titre', n=3),
        V('Un problème n’a qu’une seule partie.', False, n=4,
          e='Non. Il en a deux : l’énoncé et la question.')),

      N('relation',
        'Exemple. L’énoncé : La classe du CE1B compte 14 filles et 17 garçons. La question : '
        'Combien d’élèves compte cette classe ?',
        'kcm-pb-exemple', F('La classe du CE1B', '14 filles et 17 garçons', 'c’est l’énoncé',
                            'Combien d’élèves ?', 'c’est la question', vif=(1, 3)),
        ('simple', 'On lit l’énoncé pour savoir ce qu’on a. On lit la question pour savoir ce '
                   'qu’on cherche.'),
        ('pas_a_pas', 'On cherche le nombre d’élèves. Les filles et les garçons ensemble : 14 '
                      '+ 17 = 31.'),
        Q('« La classe du CE1B compte 14 filles et 17 garçons. » C’est…', 'l’énoncé',
          'la question', 'la solution'),
        V('« Combien d’élèves compte cette classe ? » est la question.', True),
        T('14 filles et 17 garçons : 14 + 17 = {{1}} élèves.', '31'),
        Q('Quelle opération faut-il pour trouver le nombre d’élèves ?', 'Une addition',
          'Une soustraction', 'Aucune', n=3),
        Q('Combien d’élèves compte la classe du CE1B ?', '31', '21', '3', n=4)),
      ),

    # ------------------------------------------------------------ 29 octobre
    L(MA, 'Le cylindre', GEO, '2026-10-29',
      'Le cylindre est un solide à 2 bases circulaires et parallèles, séparées d’une hauteur.',
      'kcm-cy-couv', ['2 bases', 'circulaires', 'une hauteur'],

      N('definition',
        'Le cylindre est un solide à 2 bases circulaires et parallèles.',
        'kcm-cy-bases', F('Le cylindre', 'un solide', '2 bases circulaires', 'et parallèles'),
        ('simple', 'Une boîte de lait, un tronc d’arbre coupé : ce sont des cylindres.'),
        ('visuel', 'Circulaire veut dire en forme de rond. Il y a un rond en haut et un rond '
                   'en bas.'),
        Q('Combien de bases a le cylindre ?', '2', '6', '1'),
        V('Les bases du cylindre sont circulaires.', True),
        T('Le cylindre est un solide à {{1}} bases circulaires.', '2'),
        Q('Quelle forme ont les bases du cylindre ?', 'Circulaire', 'Carrée',
          'Rectangulaire', n=3),
        V('Les bases du cylindre sont carrées.', False, n=4,
          e='Non. Elles sont circulaires, en forme de rond.')),

      N('definition',
        'Les 2 bases du cylindre sont séparées d’une hauteur.',
        'kcm-cy-hauteur', F('Le cylindre', 'une base en haut', 'la hauteur',
                            'une base en bas', vif=(1,)),
        ('simple', 'La hauteur est la distance entre la base du bas et la base du haut.'),
        ('visuel', 'Sur le dessin du cahier : base, hauteur, base.'),
        Q('Qu’est-ce qui sépare les 2 bases du cylindre ?', 'La hauteur', 'Une arête',
          'Un sommet'),
        V('Les 2 bases du cylindre sont séparées d’une hauteur.', True),
        T('Les 2 bases du cylindre sont séparées d’une {{1}}.', 'hauteur'),
        A('Relie chaque solide à ses faces ou à ses bases.', ('le cube', '6 faces carrées'),
          ('le pavé', '6 faces rectangulaires'), ('le cylindre', '2 bases circulaires')),
        Q('Quel solide a 2 bases circulaires ?', 'Le cylindre', 'Le cube', 'Le pavé', n=4)),
      ),
]
