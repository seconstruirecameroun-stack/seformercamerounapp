# -*- coding: utf-8 -*-
# Sciences — quatre leçons. Chargé par lecons-brayne-cahier-nov12.py.
#
# La germination ne porte pas de date : elle ouvre le cahier, avant le
# 12 octobre. Le paquet la range au 9 octobre pour l-ordre, et le fichier
# principal efface cette date avant d-écrire : l-app ne doit pas afficher un
# jour que le cahier ne donne pas.
#
# « La reproduction des animaux vertébrés » n-est pas un doublon de « La
# nutrition et la reproduction des animaux », déjà en base : elle apporte
# l-accouplement, l-ovule et les spermatozoïdes, et les ovovivipares.

SC = 'Sciences'
VIE = 'Science de la Vie'
AGRI = 'Sciences Agricoles'

LECONS = [
    # ------------------------------------------------------------ sans date
    L(SC, 'La germination', AGRI, '2026-10-09',
      'La germination est le passage de l’état de la graine à celui de la plante. Pour germer, '
      'une graine doit être libre et en bon état, être peu enterrée, et avoir de l’eau, de la '
      'chaleur, de la lumière et de l’air.',
      'bn-germ-couv', ['la graine', 'l’eau', 'la plantule'],

      N('definition',
        'La germination est le passage de l’état de la graine à celui de la plante.',
        'bn-germ-def', F('La germination', 'la graine', 'devient', 'une petite plante'),
        ('simple', 'La graine se réveille : une petite racine sort, puis une petite tige. '
                   'C’est la germination.'),
        ('visuel', 'Au début, une graine dure. Quelques jours plus tard, une petite plante '
                   'verte sort de la terre.'),
        Q('Qu’est-ce que la germination ?', 'Le passage de la graine à la plante',
          'La chute des feuilles de l’arbre', 'La récolte des fruits mûrs'),
        V('La germination est le passage de la graine à la plante.', True),
        T('La germination est le passage de l’état de la {{1}} à celui de la plante.', 'graine'),
        Q('Au début de la germination, on a…', 'une graine', 'une fleur', 'un fruit', n=3),
        V('La germination transforme une plante en graine.', False, n=4,
          e='Non. C’est l’inverse : la graine devient une plante.')),

      N('liste',
        'Pour germer, une graine doit être libre et en bon état, et être peu enterrée dans la '
        'terre.',
        'bn-germ-graine', F('La bonne graine', 'libre', 'en bon état', 'peu enterrée'),
        ('simple', 'Une graine cassée ou pourrie ne pousse pas. Trop profond, la petite tige '
                   'n’arrive pas jusqu’en haut.'),
        ('analogie', 'Enterrer une graine trop profond, c’est comme demander à un bébé de '
                     'sortir d’un trou très creux.'),
        Q('Une graine qui germe doit être…', 'en bon état', 'abîmée', 'cuite'),
        V('Une graine doit être peu enterrée pour germer.', True),
        T('Pour germer, la graine doit être peu {{1}} dans la terre.', 'enterrée'),
        Q('Quelle graine a le moins de chances de germer ?', 'Une graine enterrée très profond',
          'Une graine peu enterrée', 'Une graine libre et en bon état', n=3,
          e='La graine doit être peu enterrée.'),
        V('Une graine abîmée germe aussi bien qu’une graine en bon état.', False, n=4,
          e='Non. Pour germer, elle doit être en bon état.')),

      N('liste',
        'Pour germer, une graine doit avoir de l’eau, de la chaleur, de la lumière et de l’air, '
        'c’est-à-dire de l’oxygène.',
        'bn-germ-besoins', F('Ce qu’il lui faut', 'de l’eau', 'de la chaleur', 'de la lumière',
                             'de l’air (l’oxygène)'),
        ('simple', 'Quatre choses : l’eau, la chaleur, la lumière et l’air. S’il en manque une, '
                   'la graine reste endormie.'),
        ('visuel', 'Le soleil donne la chaleur et la lumière, l’arrosoir donne l’eau, et l’air '
                   'est partout autour.'),
        Q('Laquelle de ces choses aide la graine à germer ?', 'l’eau', 'le sel', 'le pétrole'),
        V('Une graine a besoin d’air pour germer.', True),
        T('Pour germer, la graine a besoin d’eau, de chaleur, de lumière et d’{{1}}.', 'air'),
        Q('Dans l’air, ce dont la graine a besoin, c’est…', 'l’oxygène', 'le sable',
          'la fumée', n=3),
        A('Relie chaque besoin à ce qui l’apporte.', ('l’eau', 'l’arrosoir'),
          ('la chaleur', 'le soleil'), n=3),
        V('Une graine a seulement besoin d’eau pour germer.', False, n=4,
          e='Non. Il lui faut aussi la chaleur, la lumière et l’air.')),

      N('relation',
        'Dans l’expérience du cahier, les graines arrosées et peu enterrées donnent des '
        'plantules huit jours après. Sans eau, ou trop enterrées, elles ne donnent rien.',
        'bn-germ-experience', F('8 jours après', 'arrosées : des plantules', 'sans eau : rien',
                                'trop enterrées : rien'),
        ('pas_a_pas', 'On sème dans trois bacs. On arrose le premier, pas le deuxième, et on '
                      'enterre profond dans le troisième. On attend huit jours.'),
        ('simple', 'Seul le bac où la graine a tout ce qu’il lui faut donne de petites plantes.'),
        Q('Huit jours après, que donnent les graines arrosées ?', 'Des plantules',
          'Rien du tout', 'Des fruits'),
        V('Dans le bac sans eau, rien ne pousse.', True),
        T('Les graines arrosées donnent des {{1}} huit jours après.', 'plantules'),
        Q('Pourquoi les graines trop enterrées ne poussent-elles pas ?',
          'Elles doivent être peu enterrées', 'Elles ont trop de lumière',
          'Elles ont trop de chaleur', n=3),
        V('Le bac sans eau donne des plantules au bout de huit jours.', False, n=4,
          e='Non. Sans eau, la graine ne germe pas.'))),

    # -------------------------------------------------------------- 19 octobre
    L(SC, 'Les critères de classification des animaux vertébrés', VIE, '2026-10-19',
      'Il existe deux grandes classes d’animaux : les vertébrés et les invertébrés. On peut '
      'aussi classer les animaux selon le revêtement de la peau, et selon leur mode de '
      'locomotion, de reproduction, de nutrition et de respiration.',
      'bn-crit-couv', ['vertébrés', 'invertébrés', 'critères'],

      N('definition',
        'Il existe deux grandes classes d’animaux : les vertébrés et les invertébrés.',
        'bn-crit-classes', F('Deux grandes classes', 'les vertébrés', 'les invertébrés'),
        ('simple', 'Un vertébré a des os dans le dos, une colonne vertébrale. Un invertébré '
                   'n’en a pas.'),
        ('visuel', 'Le chien et le poisson ont une colonne vertébrale. Le ver de terre n’en a '
                   'pas.'),
        Q('Combien de grandes classes d’animaux le cahier donne-t-il ?', 'Deux', 'Trois',
          'Cinq'),
        V('Les vertébrés et les invertébrés sont les deux grandes classes d’animaux.', True),
        T('Les deux grandes classes d’animaux sont les vertébrés et les {{1}}.', 'invertébrés'),
        Q('Quelles sont les deux grandes classes d’animaux ?',
          'Les vertébrés et les invertébrés', 'Les ovipares et les vivipares',
          'Les herbivores et les carnivores', n=3),
        V('Les mammifères et les oiseaux sont les deux grandes classes d’animaux.', False, n=4,
          e='Non. Les deux grandes classes sont les vertébrés et les invertébrés.')),

      N('liste',
        'On peut aussi classer les animaux selon le revêtement de la peau, et selon leur mode '
        'de locomotion, de reproduction, de nutrition et de respiration.',
        'bn-crit-autres', F('Les autres critères', 'le revêtement de la peau', 'la locomotion',
                            'la reproduction', 'la nutrition', 'la respiration'),
        ('simple', 'Un critère, c’est une question qu’on pose pour ranger les animaux : '
                   'comment se déplace-t-il ? que mange-t-il ?'),
        ('analogie', 'On range les élèves par taille ou par âge ; on range les animaux par '
                     'peau, par nourriture ou par déplacement.'),
        Q('Lequel est un critère pour classer les animaux ?', 'le revêtement de la peau',
          'le prix de l’animal', 'la longueur de son nom'),
        V('Le mode de respiration est un critère de classement des animaux.', True),
        T('Classer les animaux selon leur façon de se déplacer, c’est le mode de {{1}}.',
          'locomotion'),
        A('Relie chaque critère à sa question.', ('la locomotion', 'Comment se déplace-t-il ?'),
          ('la nutrition', 'Que mange-t-il ?'),
          ('la reproduction', 'Comment naissent ses petits ?'), n=3),
        Q('Classer les animaux selon ce qu’ils mangent, c’est le critère…', 'de la nutrition',
          'de la respiration', 'de la locomotion', n=4),
        V('Le revêtement de la peau dit comment l’animal se déplace.', False, n=4,
          e='Non. Le revêtement, c’est ce qui couvre la peau : poils, plumes ou écailles.'))),

    # -------------------------------------------------------------- 20 octobre
    L(SC, 'La classification des animaux : le revêtement de la peau', VIE, '2026-10-20',
      'Selon le revêtement de la peau, on classe les vertébrés en cinq groupes : les mammifères '
      '(poils), les oiseaux (plumes), les poissons (écailles non soudées), les reptiles '
      '(écailles soudées) et les amphibiens ou batraciens (corps nu).',
      'bn-peau-couv', ['poils', 'plumes', 'écailles'],

      N('liste',
        'Selon le revêtement de la peau, on peut classer les animaux vertébrés en cinq groupes : '
        'mammifères, oiseaux, poissons, reptiles et amphibiens.',
        'bn-peau-groupes', F('Cinq groupes', 'les mammifères', 'les oiseaux', 'les poissons',
                             'les reptiles', 'les amphibiens'),
        ('simple', 'On regarde ce qui couvre le corps de l’animal, et on le range dans l’un des '
                   'cinq groupes.'),
        ('visuel', 'Poils, plumes, écailles libres, écailles collées, peau nue : cinq habits, '
                   'cinq groupes.'),
        Q('En combien de groupes classe-t-on les vertébrés selon la peau ?', 'cinq', 'trois',
          'deux'),
        V('Les reptiles sont un des cinq groupes de vertébrés.', True),
        T('Selon le revêtement de la peau, on classe les vertébrés en {{1}} groupes.', '5'),
        Q('Lequel n’est pas un des cinq groupes du cahier ?', 'les insectes', 'les reptiles',
          'les amphibiens', n=3,
          e='Les cinq groupes sont : mammifères, oiseaux, poissons, reptiles, amphibiens.'),
        V('Les oiseaux et les poissons sont dans le même groupe.', False, n=4,
          e='Non. Les oiseaux ont des plumes, les poissons des écailles.')),

      N('relation',
        'Les mammifères ont le corps recouvert de poils : le chien, le chat. Les oiseaux ont le '
        'corps recouvert de plumes : le canard, la perdrix.',
        'bn-peau-poils', P('Poils et plumes', ('les mammifères', 'des poils'),
                           ('le chat', 'des poils'), ('les oiseaux', 'des plumes'),
                           ('la perdrix', 'des plumes')),
        ('simple', 'Si tu caresses des poils, c’est un mammifère. Si tu vois des plumes, c’est '
                   'un oiseau.'),
        ('visuel', 'Le chien a un pelage de poils ; le canard est couvert de plumes.'),
        Q('Le corps des mammifères est recouvert…', 'de poils', 'de plumes', 'd’écailles'),
        V('Le canard a le corps recouvert de plumes.', True),
        T('Les oiseaux ont le corps recouvert de {{1}}.', 'plumes'),
        Q('Lequel est un mammifère ?', 'le chien', 'la perdrix', 'le canard', n=3),
        V('Le chat est un oiseau.', False, n=4, e='Non. Il a des poils : c’est un mammifère.')),

      N('relation',
        'Les poissons ont le corps recouvert d’écailles non soudées : le tilapia, la carpe. Les '
        'reptiles ont des écailles soudées : la tortue, le crocodile, le lézard.',
        'bn-peau-ecailles', P('Deux sortes d’écailles', ('les poissons', 'non soudées'),
                              ('les reptiles', 'soudées'), ('le tilapia', 'un poisson'),
                              ('le crocodile', 'un reptile')),
        ('simple', 'Les écailles du poisson se détachent une à une. Celles du reptile sont '
                   'collées ensemble.'),
        ('visuel', 'La carapace de la tortue est d’un seul bloc ; le tilapia a de petites '
                   'écailles séparées.'),
        Q('Comment sont les écailles des poissons ?', 'non soudées', 'soudées', 'absentes'),
        V('Le crocodile a des écailles soudées.', True),
        T('Les reptiles ont le corps recouvert d’écailles {{1}}.', 'soudées'),
        A('Relie chaque animal à son groupe.', ('le tilapia', 'poisson'),
          ('la tortue', 'reptile'), ('le canard', 'oiseau'), n=3),
        V('La tortue a des écailles non soudées, comme le poisson.', False, n=4,
          e='Non. La tortue est un reptile : ses écailles sont soudées.'),
        Q('La carpe est…', 'un poisson', 'un reptile', 'un amphibien', n=4)),

      N('definition',
        'Les amphibiens, ou batraciens, ont le corps nu : la grenouille, le crapaud.',
        'bn-peau-nu', F('Les amphibiens', 'ou batraciens', 'le corps nu', 'la grenouille',
                        'le crapaud'),
        ('simple', 'La grenouille n’a ni poils, ni plumes, ni écailles : sa peau est nue.'),
        ('visuel', 'Touche une grenouille : sa peau est lisse et mouillée, rien ne la couvre.'),
        Q('Le corps des amphibiens est…', 'nu', 'couvert de poils', 'couvert de plumes'),
        V('La grenouille est un amphibien.', True),
        T('Les amphibiens s’appellent aussi les {{1}}.', 'batraciens'),
        Q('Lequel a le corps nu ?', 'le crapaud', 'le lézard', 'le chat', n=3),
        V('Le crapaud est un reptile.', False, n=4,
          e='Non. Il a le corps nu : c’est un amphibien, ou batracien.'))),

    # -------------------------------------------------------------- 26 octobre
    L(SC, 'La reproduction des animaux vertébrés', VIE, '2026-10-26',
      'La reproduction est la multiplication d’une espèce. Le mâle apporte les spermatozoïdes, '
      'la femelle l’ovule ; leur union donne un œuf. Il y a les vivipares, les ovipares et les '
      'ovovivipares.',
      'bn-repro-couv', ['vivipares', 'ovipares', 'ovovivipares'],

      N('definition',
        'La reproduction est la multiplication d’une espèce. Elle commence par l’accouplement '
        'd’un mâle avec une femelle.',
        'bn-repro-def', F('La reproduction', 'multiplier l’espèce', 'un mâle et une femelle',
                          'l’accouplement'),
        ('simple', 'Se reproduire, c’est avoir des petits : ainsi l’espèce ne disparaît pas.'),
        ('analogie', 'Une poule a des poussins, qui deviendront des poules : la famille des '
                     'poules continue.'),
        Q('Qu’est-ce que la reproduction ?', 'La multiplication d’une espèce',
          'La façon de se déplacer', 'La façon de se nourrir'),
        V('La reproduction commence par l’accouplement d’un mâle avec une femelle.', True),
        T('La reproduction est la {{1}} d’une espèce.', 'multiplication'),
        Q('Par quoi commence la reproduction ?', 'l’accouplement', 'la ponte', 'la naissance',
          n=3),
        V('La reproduction, c’est la façon dont un animal se nourrit.', False, n=4,
          e='Non. Ça, c’est la nutrition. La reproduction multiplie l’espèce.')),

      N('relation',
        'Le mâle apporte les spermatozoïdes et la femelle l’ovule ; l’union entre les deux donne '
        'un œuf.',
        'bn-repro-oeuf', P('Qui apporte quoi', ('le mâle', 'spermatozoïdes'),
                           ('la femelle', 'l’ovule'), ('les deux unis', 'un œuf')),
        ('pas_a_pas', 'Le spermatozoïde du mâle rencontre l’ovule de la femelle. Ensemble, ils '
                      'forment un œuf.'),
        ('simple', 'Il faut les deux, le mâle et la femelle, pour faire un œuf.'),
        Q('Qu’apporte la femelle ?', 'l’ovule', 'les spermatozoïdes', 'le lait'),
        V('Le mâle apporte les spermatozoïdes.', True),
        T('L’union du spermatozoïde et de l’{{1}} donne un œuf.', 'ovule'),
        Q('Que donne l’union du spermatozoïde et de l’ovule ?', 'un œuf', 'une graine',
          'une plume', n=3),
        V('La femelle apporte les spermatozoïdes.', False, n=4,
          e='Non. Elle apporte l’ovule ; le mâle apporte les spermatozoïdes.')),

      N('definition',
        'Les vivipares gardent l’œuf dans leur ventre et donnent plus tard naissance à des '
        'petits qui leur ressemblent : la chatte, la chienne, la chèvre, la lapine.',
        'bn-repro-vivi', F('Les vivipares', 'l’œuf reste dans le ventre', 'les petits naissent',
                           'la chatte, la chienne', 'la chèvre, la lapine'),
        ('simple', 'Chez les vivipares, le petit grandit dans le ventre de sa mère, puis il '
                   'naît.'),
        ('visuel', 'La chèvre met bas un petit chevreau qui lui ressemble déjà.'),
        Q('Comment appelle-t-on les animaux qui donnent naissance à leurs petits ?',
          'les vivipares', 'les ovipares', 'les ovovivipares'),
        V('La chèvre est vivipare.', True),
        T('La chatte et la lapine sont des {{1}}.', 'vivipares'),
        Q('Lequel est vivipare ?', 'la chienne', 'la poule', 'le pigeon', n=3),
        V('Les vivipares pondent leurs œufs dans la nature.', False, n=4,
          e='Non. Ce sont les ovipares. Les vivipares gardent l’œuf dans leur ventre.')),

      N('definition',
        'Les ovipares pondent leurs œufs dans la nature, ou les couvent pour les faire éclore '
        'plus tard : la poule, le pigeon, la tortue.',
        'bn-repro-ovi', F('Les ovipares', 'ils pondent des œufs', 'ils les couvent',
                          'la poule, le pigeon', 'la tortue'),
        ('simple', 'Ovipare : le petit grandit dans un œuf pondu dehors, puis il casse la '
                   'coquille.'),
        ('visuel', 'La poule couve ses œufs ; un jour, les poussins sortent.'),
        Q('La poule pond et couve ses œufs : elle est…', 'ovipare', 'vivipare', 'ovovivipare'),
        V('La tortue est ovipare.', True),
        T('Les animaux qui pondent des œufs sont {{1}}.', 'ovipares'),
        Q('Lequel est ovipare ?', 'le pigeon', 'la chèvre', 'la lapine', n=3),
        V('La chienne est ovipare.', False, n=4,
          e='Non. Elle donne naissance à ses petits : elle est vivipare.')),

      N('definition',
        'Les ovovivipares donnent naissance à des petits vivants, à partir d’œufs qui se sont '
        'développés dans le corps de la femelle : la vipère, le boa, l’hippocampe.',
        'bn-repro-ovovi', F('Les ovovivipares', 'l’œuf reste dans le corps',
                            'le petit naît vivant', 'la vipère, le boa', 'l’hippocampe'),
        ('simple', 'Il y a bien un œuf, mais il reste dans le corps. Le petit sort vivant.'),
        ('analogie', 'Ovo comme œuf, vivipare comme naître vivant : les deux à la fois.'),
        Q('La vipère, le boa et l’hippocampe sont…', 'ovovivipares', 'ovipares', 'vivipares'),
        V('Chez les ovovivipares, les petits naissent vivants à partir d’œufs.', True),
        T('La vipère et le boa sont {{1}}.', 'ovovivipares'),
        A('Relie chaque animal à son mode de reproduction.', ('la lapine', 'vivipare'),
          ('la poule', 'ovipare'), ('le boa', 'ovovivipare'), n=3),
        V('L’hippocampe est ovipare.', False, n=4,
          e='Non. D’après le cahier, l’hippocampe est ovovivipare.'),
        Q('Lequel est ovovivipare ?', 'le boa', 'la poule', 'la chatte', n=4))),
]
