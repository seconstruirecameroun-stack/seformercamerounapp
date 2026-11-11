# -*- coding: utf-8 -*-
# Géographie et langue et culture nationale — deux leçons.
# Chargé par lecons-klein-cahier-oct.py.
#
# Le cahier écrit « Langues nationales » ; la matière s-appelle « Langue et
# culture nationale » dans sa classe, et elle était vide.

GEOG = 'Géographie'
LANGUE = 'Langue et culture nationale'

LECONS = [
    # ------------------------------------------------------------ 22 octobre
    L(GEOG, 'La végétation', 'Géographie physique', '2026-10-22',
      'La végétation est l’ensemble d’herbes et d’arbres qui poussent dans une région. Au '
      'Cameroun on distingue : la forêt dense, la savane et la steppe.',
      'kcg-ve-couv', ['la forêt dense', 'la savane', 'la steppe'],

      N('definition',
        'La végétation est l’ensemble d’herbes et d’arbres qui poussent dans une région.',
        'kcg-ve-def', F('La végétation', 'les herbes', 'les arbres',
                        'qui poussent dans une région'),
        ('simple', 'Tout ce qui pousse quelque part, c’est la végétation de cet endroit.'),
        ('visuel', 'Regarde autour du village : l’herbe, les arbres, c’est la végétation.'),
        Q('Qu’est-ce que la végétation ?', 'Les herbes et les arbres d’une région',
          'Les animaux d’une région', 'Les maisons d’une région'),
        V('La végétation est faite d’herbes et d’arbres.', True),
        T('La {{1}} est l’ensemble d’herbes et d’arbres qui poussent dans une région.',
          'végétation'),
        Q('Lequel fait partie de la végétation ?', 'un arbre', 'une chèvre', 'une case', n=3),
        V('La végétation, ce sont les animaux d’une région.', False, n=4,
          e='Non. Ce sont les herbes et les arbres.')),

      N('liste',
        'Au Cameroun on distingue : la forêt dense, la savane et la steppe.',
        'kcg-ve-types', F('Au Cameroun', 'la forêt dense', 'la savane', 'la steppe'),
        ('simple', 'Trois végétations différentes dans le même pays.'),
        ('visuel', 'Dans la forêt dense, les arbres sont serrés les uns contre les autres.'),
        Q('Combien de végétations distingue-t-on au Cameroun ?', 'Trois', 'Une seule', 'Dix'),
        V('La savane est une végétation du Cameroun.', True),
        T('Au Cameroun on distingue la forêt dense, la savane et la {{1}}.', 'steppe'),
        Q('Laquelle est une végétation du Cameroun ?', 'la forêt dense', 'la banquise',
          'le désert de glace', n=3),
        V('La steppe est une végétation du Cameroun.', True, n=4),
        Q('Laquelle n’est pas citée pour le Cameroun ?', 'la banquise', 'la savane',
          'la steppe', n=4)),
      ),

    # ------------------------------------------------------------ 23 octobre
    L(LANGUE, 'Le village et ses traditions', 'Les rites traditionnels', '2026-10-23',
      'Un rite traditionnel est une cérémonie organisée au village autour d’un évènement. '
      'Nous avons : les rites de naissance, d’intronisation, de veuvage, de mariage et de '
      'protection.',
      'kcl-ri-couv', ['naissance', 'mariage', 'protection'],

      N('definition',
        'Un rite traditionnel est une cérémonie organisée au village autour d’un évènement.',
        'kcl-ri-def', F('Un rite traditionnel', 'une cérémonie', 'organisée au village',
                        'autour d’un évènement'),
        ('simple', 'Quand quelque chose d’important arrive, le village se réunit pour une '
                   'cérémonie.'),
        ('visuel', 'Un bébé vient de naître : le village fait une cérémonie. C’est un rite.'),
        Q('Qu’est-ce qu’un rite traditionnel ?', 'Une cérémonie organisée au village',
          'Un jeu de ballon à l’école', 'Un marché de la ville'),
        V('Un rite traditionnel est organisé autour d’un évènement.', True),
        T('Un rite traditionnel est une {{1}} organisée au village.', 'cérémonie'),
        Q('Où organise-t-on un rite traditionnel ?', 'Au village', 'Au supermarché',
          'Au stade', n=3),
        V('Un rite traditionnel est un jeu.', False, n=4, e='Non. C’est une cérémonie.')),

      N('liste',
        'Nous avons : les rites de naissance, les rites d’intronisation, les rites de veuvage, '
        'les rites de mariage, les rites de protection.',
        'kcl-ri-liste', F('Cinq rites', 'la naissance', 'l’intronisation', 'le veuvage',
                          'le mariage, la protection'),
        ('simple', 'Un rite pour chaque grand moment de la vie du village.'),
        ('visuel', 'L’intronisation, c’est quand un nouveau chef prend sa place.'),
        Q('Lequel est un rite traditionnel ?', 'le rite de mariage', 'le rite du calcul',
          'le rite du football'),
        V('Il y a des rites de naissance.', True),
        T('Quand un bébé vient au monde, on fait un rite de {{1}}.', 'naissance'),
        Q('Combien de rites le cahier donne-t-il ?', 'Cinq', 'Deux', 'Dix', n=3),
        V('Le rite de protection est un rite traditionnel.', True, n=4),
        Q('Quel rite fait-on quand deux personnes se marient ?', 'Le rite de mariage',
          'Le rite de veuvage', 'Le rite de naissance', n=4)),
      ),
]
