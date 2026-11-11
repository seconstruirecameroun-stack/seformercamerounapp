# -*- coding: utf-8 -*-
# Vocabulaire, lecture, production d-écrits — sept leçons.
# Chargé par lecons-klein-cahier-oct.py.
#
# Le cri des animaux domestiques : le cahier en donne huit. Le nom du cri de
# la poule n-est pas lisible avec certitude sur la photo ; il n-est pas repris,
# et la leçon en porte sept.
#
# La page de lecture du 12 octobre porte un titre dont un mot manque sur la
# photo (« La savonnerie … grand-mère », page 20). La leçon s-appelle donc par
# sa page.
#
# Dans le champ lexical de la ville, le cahier range le stade, le supermarché
# et l-école sous le mot « nature ». La leçon dit « les lieux », qui est ce que
# la maîtresse a demandé à l-exercice du 10 novembre (« lieu : stade »).

FR = 'Français'
VOC = 'Vocabulaire'
LECT = 'Lecture'
PROD = 'Production d’écrits'

LECONS = [
    # ------------------------------------------------------------ 12 octobre
    L(FR, 'Le champ lexical du village', VOC, '2026-10-12',
      'Les mots et expressions qui se rapportent au village sont : les personnes, comme '
      'villageois, paysan, agriculteur ; les habitats, comme case, hutte, cabane ; la nature, '
      'comme forêt, campagne, champ ; les activités, comme agriculture, élevage, pêche.',
      'kcf-vi-couv', ['villageois', 'hutte', 'forêt', 'pêche'],

      N('liste',
        'Au village, les personnes sont : villageois, paysan, agriculteur. Les habitats sont : '
        'case, hutte, cabane.',
        'kcf-vi-personnes', P('Le village', ('les personnes', 'villageois'),
                              ('les personnes', 'paysan'), ('les habitats', 'case, hutte'),
                              ('les habitats', 'cabane')),
        ('simple', 'Un habitat, c’est l’endroit où l’on habite.'),
        ('visuel', 'Le villageois habite le village. Il dort dans une case ou une hutte.'),
        Q('Qui habite au village ?', 'Le villageois', 'Le citadin', 'Le fonctionnaire'),
        V('La hutte est un habitat du village.', True),
        T('Celui qui habite le village s’appelle le {{1}}.', 'villageois'),
        Q('Lequel est un habitat du village ?', 'la case', 'l’immeuble', 'le duplex', n=3),
        V('L’immeuble est un habitat du village.', False, n=4,
          e='Non. L’immeuble est en ville. Au village : case, hutte, cabane.')),

      N('liste',
        'Au village, la nature c’est : forêt, campagne, champ. Les activités sont : '
        'agriculture, élevage, pêche.',
        'kcf-vi-nature', P('Le village', ('la nature', 'forêt, champ'),
                           ('la nature', 'campagne'), ('les activités', 'agriculture'),
                           ('les activités', 'élevage, pêche')),
        ('simple', 'Une activité, c’est un travail qu’on fait.'),
        ('visuel', 'L’agriculteur cultive le champ. Le pêcheur va à la pêche.'),
        Q('Lequel est une activité du village ?', 'l’élevage', 'le stade', 'la banque'),
        V('La forêt appartient au champ lexical du village.', True),
        T('Cultiver la terre, c’est l’{{1}}.', 'agriculture'),
        A('Range chaque mot du village.', ('paysan', 'une personne'), ('cabane', 'un habitat'),
          ('forêt', 'la nature'), ('pêche', 'une activité')),
        Q('Lequel appartient au champ lexical du village ?', 'la chasse', 'le supermarché',
          'l’avenue', n=4),
        V('Le taxi-brousse appartient au champ lexical du village.', True, n=4)),
      ),

    # ------------------------------------------------------------ 19 octobre
    L(FR, 'Le champ lexical de la ville', VOC, '2026-10-19',
      'Les mots et expressions qui tournent autour de la ville sont : les personnes, les '
      'citadins ; les habitats, comme villas, duplex, appartements, immeubles, hôtels ; les '
      'lieux, comme stade, supermarché, boulangeries, pharmacies, hôpitaux, écoles ; les '
      'activités, comme commerçants, fonctionnaires, travailleurs.',
      'kcf-vl-couv', ['citadins', 'immeubles', 'stade'],

      N('liste',
        'En ville, les personnes sont les citadins. Les habitats sont : villas, duplex, '
        'appartements, immeubles, hôtels.',
        'kcf-vl-habitats', F('La ville', 'les personnes : citadins', 'villas, duplex',
                             'appartements', 'immeubles, hôtels'),
        ('simple', 'Le citadin habite la ville, comme le villageois habite le village.'),
        ('visuel', 'Un immeuble a plusieurs étages. Un duplex a deux niveaux.'),
        Q('Qui habite en ville ?', 'Le citadin', 'Le villageois', 'Le paysan'),
        V('L’immeuble est un habitat de la ville.', True),
        T('Ceux qui habitent la ville s’appellent les {{1}}.', 'citadins'),
        Q('Lequel est un habitat de la ville ?', 'la villa', 'la hutte', 'la case', n=3),
        V('Les citadins habitent au village.', False, n=4,
          e='Non. Les citadins habitent la ville.')),

      N('liste',
        'En ville, les lieux sont : stade, supermarché, boulangeries, pharmacies, hôpitaux, '
        'écoles.',
        'kcf-vl-lieux', F('Les lieux de la ville', 'stade, supermarché', 'boulangeries',
                          'pharmacies, hôpitaux', 'écoles'),
        ('simple', 'Ce sont les endroits où l’on va en ville.'),
        ('visuel', 'À la boulangerie on achète le pain. À la pharmacie, les médicaments.'),
        Q('Lequel est un lieu de la ville ?', 'le stade', 'la forêt', 'le champ'),
        V('Le supermarché appartient au champ lexical de la ville.', True),
        T('On achète le pain à la {{1}}.', 'boulangerie'),
        Q('Lequel appartient au champ lexical de la ville ?', 'la banque', 'la hutte',
          'la chasse', n=3),
        V('La pharmacie est un lieu de la ville.', True, n=4)),

      N('liste',
        'En ville, les activités sont : commerçants, fonctionnaires, travailleurs.',
        'kcf-vl-activites', F('Les activités de la ville', 'commerçants', 'fonctionnaires',
                              'travailleurs'),
        ('simple', 'Le commerçant vend. Le fonctionnaire travaille pour l’État.'),
        ('visuel', 'Au marché, le commerçant est derrière son étal.'),
        Q('Lequel est une activité de la ville ?', 'commerçant', 'pêche', 'élevage'),
        V('Les fonctionnaires travaillent en ville.', True),
        T('Celui qui vend dans une boutique est un {{1}}.', 'commerçant'),
        A('Range chaque mot dans son champ lexical.', ('immeuble', 'la ville'),
          ('hutte', 'le village'), ('avenue', 'la ville aussi'),
          ('villageois', 'le village aussi')),
        Q('Lequel appartient au champ lexical de la ville ?', 'l’avenue', 'la cabane',
          'le paysan', n=4),
        V('La villa appartient au champ lexical du village.', False, n=4,
          e='Non. La villa est un habitat de la ville.')),
      ),

    # ------------------------------------------------------------ 26 octobre
    L(FR, 'Le cri des animaux domestiques', VOC, '2026-10-26',
      'Les animaux s’expriment par des cris différents : l’aboiement du chien, le miaulement '
      'du chat, le hennissement du cheval, le grognement du porc, le bêlement de la chèvre, le '
      'meuglement du bœuf, le nasillement du canard.',
      'kcf-cr-couv', ['l’aboiement', 'le miaulement', 'le bêlement'],

      N('liste',
        'L’aboiement, c’est le chien. Le miaulement, c’est le chat. Le hennissement, c’est le '
        'cheval. Le grognement, c’est le porc.',
        'kcf-cr-quatre', P('Quatre cris', ('le chien', 'l’aboiement'),
                           ('le chat', 'le miaulement'), ('le cheval', 'le hennissement'),
                           ('le porc', 'le grognement')),
        ('simple', 'Chaque animal a son cri, et chaque cri a son nom.'),
        ('visuel', 'Le chien aboie : son cri est l’aboiement. Le chat miaule : le '
                   'miaulement.'),
        Q('Comment s’appelle le cri du chien ?', 'L’aboiement', 'Le miaulement',
          'Le bêlement'),
        V('Le miaulement est le cri du chat.', True),
        T('Le cri du cheval s’appelle le {{1}}.', 'hennissement'),
        A('Relie chaque animal à son cri.', ('le chien', 'l’aboiement'),
          ('le chat', 'le miaulement'), ('le cheval', 'le hennissement'),
          ('le porc', 'le grognement')),
        Q('Quel animal pousse un grognement ?', 'Le porc', 'Le cheval', 'Le chat', n=4)),

      N('liste',
        'Le bêlement, c’est la chèvre. Le meuglement, c’est le bœuf. Le nasillement, c’est le '
        'canard.',
        'kcf-cr-trois', P('Trois cris', ('la chèvre', 'le bêlement'),
                          ('le bœuf', 'le meuglement'), ('le canard', 'le nasillement')),
        ('simple', 'La chèvre bêle, le bœuf meugle, le canard nasille.'),
        ('visuel', 'Bê… fait la chèvre : c’est le bêlement.'),
        Q('Comment s’appelle le cri de la chèvre ?', 'Le bêlement', 'Le meuglement',
          'L’aboiement'),
        V('Le meuglement est le cri du bœuf.', True),
        T('Le cri du canard s’appelle le {{1}}.', 'nasillement'),
        A('Relie chaque animal à son cri.', ('la chèvre', 'le bêlement'),
          ('le bœuf', 'le meuglement'), ('le canard', 'le nasillement')),
        Q('Quel animal pousse un meuglement ?', 'Le bœuf', 'Le canard', 'La chèvre', n=4),
        V('Le bêlement est le cri du chien.', False, n=4,
          e='Non. Le bêlement est le cri de la chèvre.')),
      ),

    # ------------------------------------------------------------ 12 octobre
    L(FR, 'Lecture, page 20 : les mots difficiles', LECT, '2026-10-12',
      'Les mots difficiles du texte de la page 20 : une coopérative, un ensemble de personnes '
      'qui travaillent en groupe ; les plaisanteries, les choses amusantes ; la modestie, '
      'simple, humble.',
      'kcf-l1-couv', ['coopérative', 'plaisanteries', 'modestie'],

      N('definition',
        'Une coopérative : un ensemble de personnes qui travaillent en groupe, une petite '
        'entreprise.',
        'kcf-l1-cooperative', F('Une coopérative', 'des personnes', 'qui travaillent en groupe',
                                'une petite entreprise'),
        ('simple', 'Dans une coopérative, on travaille ensemble.'),
        ('visuel', 'Des femmes qui fabriquent du savon ensemble forment une coopérative.'),
        Q('Qu’est-ce qu’une coopérative ?', 'Des personnes qui travaillent en groupe',
          'Une personne qui travaille seule', 'Un grand champ de maïs'),
        T('Dans une coopérative, les personnes travaillent en {{1}}.', 'groupe'),
        V('Une coopérative est une petite entreprise.', True, n=3),
        V('Dans une coopérative, on travaille tout seul.', False, n=4,
          e='Non. On travaille en groupe.')),

      N('definition',
        'Les plaisanteries : les choses amusantes.',
        'kcf-l1-plaisanteries', F('Les plaisanteries', 'les choses amusantes'),
        ('simple', 'Une plaisanterie fait rire.'),
        ('visuel', 'Quand ton ami dit une chose drôle, c’est une plaisanterie.'),
        Q('Que sont les plaisanteries ?', 'Les choses amusantes', 'Les choses tristes',
          'Les choses lourdes'),
        T('Les plaisanteries sont des choses {{1}}.', 'amusantes'),
        V('Une plaisanterie fait rire.', True, n=3),
        V('Les plaisanteries sont des choses tristes.', False, n=4,
          e='Non. Ce sont des choses amusantes.')),

      N('definition',
        'La modestie : simple, humble.',
        'kcf-l1-modestie', F('La modestie', 'simple', 'humble'),
        ('simple', 'Quelqu’un de modeste ne se vante pas.'),
        ('visuel', 'Il a gagné, et il ne le crie pas partout : il est modeste.'),
        Q('Quel mot va avec la modestie ?', 'humble', 'bruyant', 'rapide'),
        T('La modestie : simple, {{1}}.', 'humble'),
        V('Quelqu’un de modeste est simple.', True, n=3),
        V('Quelqu’un de modeste se vante beaucoup.', False, n=4,
          e='Non. Il est simple et humble.')),
      ),

    # ------------------------------------------------------------ 19 octobre
    L(FR, 'Le temps des semis : les mots difficiles', LECT, '2026-10-19',
      'Les mots difficiles du texte « Le temps des semis » : les sillons, petites tranchées '
      'creusées dans la terre ; une averse, la pluie ; répétitif, quelque chose qui revient à '
      'plusieurs reprises.',
      'kcf-l2-couv', ['sillons', 'averse', 'répétitif'],

      N('definition',
        'Les sillons : petites tranchées creusées dans la terre.',
        'kcf-l2-sillons', F('Les sillons', 'de petites tranchées', 'creusées dans la terre'),
        ('simple', 'Ce sont les lignes creuses où l’on met les graines.'),
        ('visuel', 'Dans un champ labouré, les sillons font des rayures.'),
        Q('Que sont les sillons ?', 'De petites tranchées dans la terre',
          'De gros nuages de pluie', 'Des outils pour semer'),
        T('Les sillons sont creusés dans la {{1}}.', 'terre'),
        V('Les sillons sont de petites tranchées.', True, n=3),
        V('Les sillons sont dans le ciel.', False, n=4, e='Non. Ils sont dans la terre.')),

      N('definition',
        'Une averse : la pluie.',
        'kcf-l2-averse', F('Une averse', 'la pluie'),
        ('simple', 'Une averse, c’est de la pluie qui tombe d’un coup.'),
        ('visuel', 'Le ciel devient noir, et l’averse arrive.'),
        Q('Qu’est-ce qu’une averse ?', 'La pluie', 'Le vent', 'Le soleil'),
        T('Une averse, c’est la {{1}}.', 'pluie'),
        V('Quand il y a une averse, il pleut.', True, n=3),
        V('Une averse, c’est un grand soleil.', False, n=4, e='Non. C’est la pluie.')),

      N('definition',
        'Répétitif : quelque chose qui revient à plusieurs reprises.',
        'kcf-l2-repetitif', F('Répétitif', 'qui revient', 'à plusieurs reprises'),
        ('simple', 'Ce qui est répétitif recommence encore et encore.'),
        ('visuel', 'Semer, graine après graine, est un geste répétitif.'),
        Q('Que veut dire « répétitif » ?', 'Qui revient plusieurs fois',
          'Qui n’arrive qu’une fois', 'Qui va très vite'),
        T('Répétitif : quelque chose qui revient à {{1}} reprises.', 'plusieurs'),
        V('Un geste répétitif se fait plusieurs fois.', True, n=3),
        V('Répétitif veut dire qui n’arrive qu’une seule fois.', False, n=4,
          e='Non. Qui revient à plusieurs reprises.')),
      ),

    # ------------------------------------------------------------ 26 octobre
    L(FR, 'Au marché : les mots difficiles', LECT, '2026-10-26',
      'Les mots difficiles du texte « Au marché », page 27 : odorantes, ce qui a une odeur ; '
      'animés, qui a beaucoup de bruits ; un motif, une décoration sur le tissu.',
      'kcf-l3-couv', ['odorantes', 'animés', 'motif'],

      N('definition',
        'Odorantes : ce qui a une odeur.',
        'kcf-l3-odorantes', F('Odorantes', 'ce qui a une odeur'),
        ('simple', 'Ce qui est odorant se sent avec le nez.'),
        ('visuel', 'Au marché, les épices sont odorantes.'),
        Q('Que veut dire « odorantes » ?', 'Qui ont une odeur', 'Qui font du bruit',
          'Qui ont des couleurs'),
        T('Odorantes : ce qui a une {{1}}.', 'odeur'),
        V('Des épices odorantes ont une odeur.', True, n=3),
        V('Odorantes veut dire qui font du bruit.', False, n=4,
          e='Non. Qui ont une odeur.')),

      N('definition',
        'Animés : qui a beaucoup de bruits.',
        'kcf-l3-animes', F('Animés', 'qui a beaucoup de bruits'),
        ('simple', 'Un lieu animé est plein de monde et de bruit.'),
        ('visuel', 'Le marché, le samedi, est très animé.'),
        Q('Que veut dire « animés » ?', 'Qui ont beaucoup de bruits', 'Qui sont très calmes',
          'Qui sont fermés'),
        T('Animés : qui a beaucoup de {{1}}.', 'bruits'),
        V('Un marché animé fait beaucoup de bruit.', True, n=3),
        V('Un lieu animé est silencieux.', False, n=4, e='Non. Il a beaucoup de bruits.')),

      N('definition',
        'Un motif : une décoration sur le tissu.',
        'kcf-l3-motif', F('Un motif', 'une décoration', 'sur le tissu'),
        ('simple', 'C’est le dessin qu’on voit sur un pagne.'),
        ('visuel', 'Des fleurs, des ronds, des oiseaux sur un tissu : ce sont des motifs.'),
        Q('Qu’est-ce qu’un motif ?', 'Une décoration sur le tissu', 'Un bruit du marché',
          'Une odeur de cuisine'),
        T('Un motif est une décoration sur le {{1}}.', 'tissu'),
        V('Un motif se trouve sur un tissu.', True, n=3),
        V('Un motif est une odeur.', False, n=4, e='Non. C’est une décoration.')),
      ),

    # ------------------------------------------------- 20 et 27 octobre
    L(FR, 'Le conte', PROD, '2026-10-20',
      'Un conte est un texte narratif qui raconte une histoire imaginaire au passé lointain, '
      'en trois parties : l’introduction, le développement et la conclusion. Le texte support '
      'est « Le lièvre et la tortue ».',
      'kcf-co-couv', ['introduction', 'développement', 'conclusion'],

      N('definition',
        'Un conte est un texte narratif qui raconte une histoire imaginaire au passé lointain, '
        'en trois parties.',
        'kcf-co-def', F('Le conte', 'une histoire imaginaire', 'au passé lointain',
                        'en trois parties'),
        ('simple', 'Un conte est une histoire inventée, qui se passe il y a très longtemps.'),
        ('visuel', 'Un lièvre qui parle à une tortue : c’est imaginaire, c’est un conte.'),
        Q('Le conte raconte une histoire…', 'imaginaire', 'vraie', 'd’aujourd’hui'),
        V('Un conte a trois parties.', True),
        T('Un conte raconte une histoire {{1}}.', 'imaginaire'),
        C('Range les trois parties du conte dans l’ordre.', 'l’introduction',
          'le développement', 'la conclusion'),
        V('Un conte raconte ce qui s’est passé hier à l’école.', False, n=4,
          e='Non. Une histoire imaginaire, au passé lointain.')),

      N('liste',
        'L’introduction commence par « il était une fois », « il y a très longtemps », '
        '« jadis ». Elle donne le lieu, comme village, forêt, château, et les personnages.',
        'kcf-co-intro', F('L’introduction', 'il était une fois', 'il y a très longtemps, jadis',
                          'le lieu', 'les personnages'),
        ('simple', 'Au début, on dit quand, où et avec qui.'),
        ('visuel', 'Il était une fois, dans le village de Bilon, un lièvre très rapide.'),
        Q('Par quels mots commence souvent un conte ?', 'Il était une fois',
          'Demain matin', 'Cher ami'),
        V('L’introduction donne le lieu et les personnages.', True),
        T('Un conte commence souvent par : il était une {{1}}.', 'fois'),
        Q('Dans « Le lièvre et la tortue », où se passe l’histoire ?',
          'Dans le village de Bilon', 'Dans une grande ville', 'Dans un château', n=3),
        V('« Jadis » peut commencer un conte.', True, n=4)),

      N('definition',
        'Le développement : ici on raconte les faits dans un ordre chronologique.',
        'kcf-co-developpement', F('Le développement', 'on raconte les faits',
                                  'dans l’ordre', 'le lièvre s’endort',
                                  'la tortue avance pas à pas', vif=(3, 4)),
        ('simple', 'On raconte ce qui se passe, une chose après l’autre.'),
        ('visuel', 'La course commence, le lièvre s’endort sous un arbre, la tortue avance, le '
                   'lièvre se réveille trop tard.'),
        Q('Dans le développement, on raconte les faits…', 'dans l’ordre',
          'en commençant par la fin', 'sans aucun ordre'),
        V('Dans le conte, la tortue avance pas à pas sans jamais s’arrêter.', True),
        T('Le lièvre s’allonge sous un arbre et s’{{1}}.', 'endort',
          e='Il s’endort, et la tortue le dépasse.'),
        C('Range les faits du conte dans l’ordre.', 'le lièvre propose une course',
          'le lièvre s’endort sous un arbre', 'le lièvre se réveille',
          'les animaux applaudissent la tortue'),
        Q('Jusqu’où le lièvre et la tortue font-ils la course ?', 'Jusqu’au manguier',
          'Jusqu’à la rivière', 'Jusqu’au marché', n=4)),

      N('definition',
        'La conclusion : on fait ressortir la leçon de morale. Le lièvre s’excusa, tout '
        'honteux. Depuis ce jour il ne se moque plus de personne.',
        'kcf-co-conclusion', F('La conclusion', 'la leçon de morale', 'le lièvre s’excuse',
                               'il ne se moque plus', 'de personne', vif=(0,)),
        ('simple', 'À la fin, le conte nous apprend quelque chose.'),
        ('visuel', 'Tous les animaux applaudissent la tortue : celle qui allait lentement a '
                   'gagné.'),
        Q('Que fait-on ressortir dans la conclusion ?', 'La leçon de morale',
          'Le nom du village', 'Le début de la course'),
        V('À la fin du conte, le lièvre s’excuse.', True),
        T('Dans la conclusion, on fait ressortir la leçon de {{1}}.', 'morale'),
        Q('Qui les animaux applaudissent-ils à la fin ?', 'La tortue', 'Le lièvre',
          'Le manguier', n=3),
        V('À la fin du conte, le lièvre continue de se moquer de tout le monde.', False, n=4,
          e='Non. Depuis ce jour il ne se moque plus de personne.'),
        Q('Qui gagne la course ?', 'La tortue', 'Le lièvre', 'Personne', n=4)),
      ),
]
