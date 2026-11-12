# -*- coding: utf-8 -*-
# Les leçons en français du cahier de sciences humaines de KLEIN — sept.
# Chargé par lecons-klein-cahier-nov12.py.
#
# CE QUI N-EST PAS POSÉ, FAUTE DE SE LIRE SUR LA PHOTO :
#   - l-histoire de Yaoundé : le tout premier nom de la ville et ce qu-il
#     signifie ;
#   - l-hydrographie : la longueur de la Sanaga.
#
# « Les saisons et les végétaux » ne porte pas de date : elle suit le
# 28 octobre. Le paquet la range au 29 pour l-ordre ; la date n-est pas
# écrite en base.

HIST = 'Histoire'
CIV = 'Éducation civique'
GEO = 'Géographie'
SC = 'Sciences et technologies'

LECONS = [
    # -------------------------------------------------------------- 12 octobre
    L(HIST, 'L’histoire de Yaoundé', 'Histoire', '2026-10-12',
      'Les premiers habitants de Yaoundé sont les Ewondo. Ils ont donné à la ville un nom qui '
      'veut dire « arachides ». Les Allemands ont changé ce nom, qui est devenu plus tard '
      'Yaoundé.',
      'kz-yde-couv', ['Ewondo', 'arachides', 'Yaoundé'],

      N('definition',
        'Les premiers habitants de la ville de Yaoundé sont les Ewondo. Ils lui ont donné un nom '
        'qui veut dire « arachides ».',
        'kz-yde-ewondo', F('Yaoundé', 'premiers habitants :', 'les Ewondo',
                           'un nom qui veut dire', '« arachides »'),
        ('simple', 'Avant la grande ville, il y avait les Ewondo. Ce sont eux qui ont nommé '
                   'l’endroit.'),
        ('visuel', 'Des champs d’arachides sur les collines : c’est le nom que les Ewondo ont '
                   'donné.'),
        Q('Qui sont les premiers habitants de Yaoundé ?', 'les Ewondo', 'les Allemands',
          'les Portugais'),
        V('Le nom donné par les Ewondo veut dire « arachides ».', True),
        T('Le nom donné par les Ewondo veut dire « {{1}} ».', 'arachides'),
        Q('Que veut dire le nom donné par les Ewondo ?', 'arachides', 'montagne', 'rivière', n=3),
        V('Les premiers habitants de Yaoundé sont les Allemands.', False, n=4,
          e='Non. Ce sont les Ewondo.')),

      N('relation',
        'Ce nom a été changé par les Allemands. Il est devenu plus tard Yaoundé.',
        'kz-yde-allemands', F('Le nom change', 'le nom des Ewondo', 'changé par les Allemands',
                              'devient Yaoundé'),
        ('pas_a_pas', 'D’abord le nom des Ewondo. Puis les Allemands le changent. À la fin, '
                      'on dit Yaoundé.'),
        ('simple', 'Le nom a voyagé : des Ewondo aux Allemands, puis jusqu’à nous.'),
        Q('Qui a changé le nom donné par les Ewondo ?', 'les Allemands', 'les Pygmées',
          'les Anglais'),
        V('Le nom de la ville est devenu Yaoundé.', True),
        T('Le nom a été {{1}} par les Allemands.', 'changé'),
        C('Remets dans l’ordre.', 'les Ewondo donnent un nom', 'les Allemands le changent',
          'il devient Yaoundé', n=3),
        V('Les Ewondo ont changé le nom donné par les Allemands.', False, n=4,
          e='Non. C’est l’inverse : les Allemands ont changé le nom des Ewondo.'))),

    # -------------------------------------------------------------- 19 octobre
    L(HIST, 'Les grandes figures historiques du Cameroun', 'Histoire', '2026-10-19',
      'Une grande figure historique est une personne qui a marqué l’histoire de sa localité. '
      'Au Cameroun : Douala Manga Bell, Martin Paul Samba, Ernest Ouandié, Ruben Um Nyobè, '
      'André Marie Mbida, Ahmadou Ahidjo, Charles Atangana, Ibrahim Njoya.',
      'kz-fig-couv', ['Manga Bell', 'Um Nyobè', 'Njoya'],

      N('definition',
        'Une grande figure historique est une personne qui a marqué l’histoire de sa localité.',
        'kz-fig-def', F('Une grande figure', 'une personne', 'qui a marqué l’histoire'),
        ('simple', 'C’est quelqu’un dont on se souvient longtemps, parce qu’il a fait de grandes '
                   'choses.'),
        ('visuel', 'Une statue, une rue, une école portent son nom.'),
        Q('Qu’est-ce qu’une grande figure historique ?',
          'Une personne qui a marqué l’histoire', 'Un grand dessin', 'Un très grand arbre'),
        V('Une grande figure historique a marqué l’histoire de sa localité.', True),
        T('Une grande figure historique est une {{1}} qui a marqué l’histoire.', 'personne'),
        Q('Une grande figure historique a marqué…', 'l’histoire', 'le tableau', 'le cahier',
          n=3),
        V('Une grande figure historique est un monument en pierre.', False, n=4,
          e='Non. C’est une personne.')),

      N('liste',
        'Au Cameroun, on peut citer Douala Manga Bell, Martin Paul Samba, Ernest Ouandié et '
        'Ruben Um Nyobè.',
        'kz-fig-1', F('Au Cameroun (1)', 'Douala Manga Bell', 'Martin Paul Samba',
                      'Ernest Ouandié', 'Ruben Um Nyobè'),
        ('simple', 'Quatre noms à retenir : Manga Bell, Samba, Ouandié, Um Nyobè.'),
        ('visuel', 'À Douala, une grande place porte le nom de Manga Bell.'),
        Q('Lequel est une grande figure historique du Cameroun ?', 'Ruben Um Nyobè',
          'Fernando Poo', 'Christophe Colomb'),
        V('Martin Paul Samba est une grande figure historique du Cameroun.', True),
        Q('Quel prénom va avec Ouandié ?', 'Ernest', 'Ruben', 'Charles', n=2),
        Q('Quel nom va avec Douala Manga… ?', 'Bell', 'Samba', 'Njoya', n=3),
        V('Ernest Ouandié est une grande figure historique du Cameroun.', True, n=4)),

      N('liste',
        'On peut aussi citer André Marie Mbida, Ahmadou Ahidjo, Charles Atangana et Ibrahim '
        'Njoya.',
        'kz-fig-2', F('Au Cameroun (2)', 'André Marie Mbida', 'Ahmadou Ahidjo',
                      'Charles Atangana', 'Ibrahim Njoya'),
        ('simple', 'Quatre autres noms : Mbida, Ahidjo, Atangana, Njoya.'),
        ('visuel', 'Le sultan Njoya, à Foumban, est connu de tous les écoliers.'),
        Q('Lequel est une grande figure historique du Cameroun ?', 'Charles Atangana',
          'Vasco de Gama', 'Lord Mansfield'),
        V('Ibrahim Njoya est une grande figure historique du Cameroun.', True),
        Q('Quel prénom va avec Ahidjo ?', 'Ahmadou', 'André', 'Ibrahim', n=2),
        A('Relie le prénom au nom.', ('Charles', 'Atangana'), ('Ibrahim', 'Njoya'),
          ('Ahmadou', 'Ahidjo'), n=3),
        V('André Marie Mbida est une grande figure historique du Cameroun.', True, n=4))),

    # -------------------------------------------------------------- 20 octobre
    L(CIV, 'Les communes et les chefferies', 'Les divisions administratives', '2026-10-20',
      'Au Cameroun, on a les communes urbaines, les communes rurales, les chefferies '
      'traditionnelles, les lamidats et le sultanat.',
      'kz-com-couv', ['communes', 'chefferies', 'lamidats'],

      N('liste',
        'Au Cameroun, on a les communes urbaines et les communes rurales.',
        'kz-com-communes', F('Les communes', 'les communes urbaines', 'les communes rurales'),
        ('simple', 'Urbaine, c’est en ville. Rurale, c’est à la campagne.'),
        ('visuel', 'La mairie de la ville, la mairie du village : deux communes.'),
        Q('Quelles communes a-t-on au Cameroun ?', 'urbaines et rurales',
          'chaudes et froides', 'grandes et petites'),
        V('Au Cameroun, il y a des communes rurales.', True),
        T('Au Cameroun, on a les communes urbaines et les communes {{1}}.', 'rurales'),
        Q('Une commune de ville est une commune…', 'urbaine', 'rurale', 'traditionnelle', n=3),
        V('Une commune rurale se trouve en pleine ville.', False, n=4,
          e='Non. Rurale veut dire à la campagne.')),

      N('liste',
        'On a aussi les chefferies traditionnelles, les lamidats et le sultanat.',
        'kz-com-chefferies', F('Aussi', 'les chefferies traditionnelles', 'les lamidats',
                               'le sultanat'),
        ('simple', 'Le chef, le lamido et le sultan dirigent selon la tradition.'),
        ('visuel', 'La chefferie au village, le lamidat au Nord, le sultanat à Foumban.'),
        Q('Lequel fait partie de la liste du cahier ?', 'les lamidats', 'les océans',
          'les forêts'),
        V('Le sultanat fait partie de la liste du cahier.', True),
        T('Au Cameroun, on a les chefferies {{1}}.', 'traditionnelles'),
        Q('Combien de choses le cahier cite-t-il en tout ?', 'cinq', 'deux', 'dix', n=3),
        V('Les lamidats sont des communes urbaines.', False, n=4,
          e='Non. Les lamidats sont cités à part, avec les chefferies et le sultanat.'))),

    # -------------------------------------------------------------- 21 octobre
    L(CIV, 'Les régions, les départements et les arrondissements',
      'Les divisions administratives', '2026-10-21',
      'Au Cameroun, nous avons 10 régions dirigées par les gouverneurs, 58 départements '
      'dirigés par les préfets et 360 arrondissements dirigés par les sous-préfets.',
      'kz-reg-couv', ['10 régions', '58 départements', '360'],

      N('relation',
        'Le Cameroun a 10 régions. Elles sont dirigées par les gouverneurs.',
        'kz-reg-regions', F('Les régions', '10 régions', 'dirigées par', 'les gouverneurs'),
        ('simple', 'Le pays est coupé en dix grands morceaux : les régions.'),
        ('visuel', 'Sur la carte du Cameroun, dix couleurs : dix régions.'),
        Q('Combien de régions le Cameroun a-t-il ?', '10', '58', '360'),
        V('Les régions sont dirigées par les gouverneurs.', True),
        T('Le Cameroun a {{1}} régions.', '10'),
        Q('Qui dirige une région ?', 'le gouverneur', 'le préfet', 'le sous-préfet', n=3),
        V('Les régions sont dirigées par les préfets.', False, n=4,
          e='Non. Les régions sont dirigées par les gouverneurs.')),

      N('relation',
        'Le Cameroun a 58 départements, dirigés par les préfets, et 360 arrondissements, '
        'dirigés par les sous-préfets.',
        'kz-reg-dep', P('Départements et arrond.', ('58 départements', 'les préfets'),
                        ('360 arrondissements', 'les sous-préfets')),
        ('pas_a_pas', 'Une région se coupe en départements, et un département en '
                      'arrondissements.'),
        ('simple', 'Plus le morceau est petit, plus il y en a : 10, puis 58, puis 360.'),
        Q('Qui dirige un département ?', 'le préfet', 'le gouverneur', 'le sous-préfet'),
        V('Les arrondissements sont dirigés par les sous-préfets.', True),
        T('Le Cameroun a {{1}} départements.', '58'),
        A('Relie chaque division à son chef.', ('la région', 'le gouverneur'),
          ('le département', 'le préfet'), ('l’arrondissement', 'le sous-préfet'), n=3),
        Q('Combien d’arrondissements le Cameroun a-t-il ?', '360', '58', '10', n=4),
        V('Il y a plus de régions que de départements.', False, n=4,
          e='Non. 10 régions, 58 départements.'))),

    # -------------------------------------------------------------- 26 octobre
    L(GEO, 'L’hydrographie', 'Géographie', '2026-10-26',
      'L’hydrographie est l’ensemble des cours d’eau d’un pays. Celle du Cameroun est composée '
      'de fleuves (la Sanaga, le plus long, le Wouri, le Nyong, le Mbam), de rivières, de lacs, '
      'de ruisseaux, de marigots et de la mer.',
      'kz-hydro-couv', ['fleuves', 'lacs', 'la mer'],

      N('definition',
        'L’hydrographie est l’ensemble des cours d’eau d’un pays.',
        'kz-hydro-def', F('L’hydrographie', 'tous les cours d’eau', 'd’un pays'),
        ('simple', 'Toute l’eau qui coule ou qui dort dans un pays, c’est son hydrographie.'),
        ('visuel', 'Sur la carte, tous les traits bleus : c’est l’hydrographie.'),
        Q('Qu’est-ce que l’hydrographie ?', 'L’ensemble des cours d’eau d’un pays',
          'L’ensemble des montagnes', 'L’ensemble des villes'),
        V('L’hydrographie est l’ensemble des cours d’eau d’un pays.', True),
        T('L’hydrographie est l’ensemble des cours d’{{1}} d’un pays.', 'eau'),
        Q('Sur une carte, l’hydrographie se dessine en…', 'bleu', 'marron', 'noir', n=3),
        V('L’hydrographie, ce sont les routes d’un pays.', False, n=4,
          e='Non. Ce sont ses cours d’eau.')),

      N('liste',
        'Les fleuves du Cameroun : le plus long est la Sanaga ; il y a aussi le Wouri, le Nyong '
        'et le Mbam.',
        'kz-hydro-fleuves', F('Les fleuves', 'la Sanaga, le plus long', 'le Wouri', 'le Nyong',
                              'le Mbam'),
        ('simple', 'La Sanaga est le plus long fleuve du Cameroun.'),
        ('visuel', 'À Douala, on traverse le pont sur le Wouri.'),
        Q('Quel est le plus long fleuve du Cameroun ?', 'la Sanaga', 'le Wouri', 'le Mbam'),
        V('Le Nyong est un fleuve du Cameroun.', True),
        Q('Lequel est un fleuve du Cameroun ?', 'le Wouri', 'le Nil', 'le Congo', n=2),
        Q('Le Wouri, le Nyong et le Mbam sont des…', 'fleuves', 'montagnes', 'villes', n=3),
        V('Le Wouri est le plus long fleuve du Cameroun.', False, n=4,
          e='Non. Le plus long est la Sanaga.')),

      N('liste',
        'L’hydrographie du Cameroun est aussi composée de rivières, de lacs, de ruisseaux, de '
        'marigots et de la mer.',
        'kz-hydro-autres', F('Et aussi', 'les rivières', 'les lacs', 'les ruisseaux',
                             'les marigots, la mer'),
        ('simple', 'Il n’y a pas que les fleuves : petits et grands, tous les cours d’eau '
                   'comptent.'),
        ('analogie', 'Le ruisseau est le petit frère de la rivière, et la rivière celle du '
                     'fleuve.'),
        Q('Lequel fait partie de l’hydrographie ?', 'le marigot', 'la colline', 'le plateau'),
        V('Les lacs font partie de l’hydrographie du Cameroun.', True),
        T('Un petit cours d’eau s’appelle un {{1}}.', 'ruisseau'),
        Q('Lequel ne fait pas partie de l’hydrographie ?', 'la forêt', 'la mer', 'la rivière',
          n=3),
        V('La mer ne fait pas partie de l’hydrographie du Cameroun.', False, n=4,
          e='Non. Le cahier cite aussi la mer.'))),

    # -------------------------------------------------------------- 28 octobre
    L(CIV, 'La sécurité au champ', 'Éducation à la sécurité', '2026-10-28',
      'Pour ma sécurité au champ, je dois porter des vêtements qui couvrent tout le corps, '
      'porter des chaussures fermées et solides comme des bottes, et ne pas jouer avec les '
      'objets tranchants ou pointus comme la machette ou le râteau.',
      'kz-champ-couv', ['vêtements', 'bottes', 'machette'],

      N('liste',
        'Pour ma sécurité au champ, je dois porter des vêtements qui couvrent tout le corps et '
        'des chaussures fermées et solides, comme des bottes.',
        'kz-champ-habits', F('Au champ, je porte', 'des vêtements couvrants',
                             'des chaussures fermées', 'des bottes'),
        ('simple', 'Les herbes coupent, les épines piquent : je couvre mon corps et mes pieds.'),
        ('visuel', 'Un enfant au champ en bottes, pantalon long et manches longues.'),
        Q('Que dois-je porter aux pieds au champ ?', 'des chaussures fermées et solides',
          'des sandales ouvertes', 'rien du tout'),
        V('Au champ, je porte des vêtements qui couvrent tout le corps.', True),
        T('Au champ, je porte des {{1}}.', 'bottes'),
        Q('Quels vêtements porter au champ ?', 'des vêtements qui couvrent tout le corps',
          'un petit maillot de bain léger', 'des habits de fête brillants', n=3),
        V('Au champ, il vaut mieux marcher pieds nus.', False, n=4,
          e='Non. Il faut des chaussures fermées et solides.')),

      N('definition',
        'Au champ, je ne dois pas jouer avec les objets tranchants, comme la machette, ou '
        'pointus, comme le râteau.',
        'kz-champ-outils', P('Je ne joue pas avec', ('tranchant', 'la machette'),
                             ('pointu', 'le râteau')),
        ('simple', 'Une machette coupe, un râteau pique : ce ne sont pas des jouets.'),
        ('histoire', 'Paul a voulu jouer avec la machette de son père. Il s’est coupé la main.'),
        Q('Avec quoi ne dois-je pas jouer au champ ?', 'la machette', 'mon ballon',
          'mon chapeau'),
        V('Le râteau est un objet pointu.', True),
        T('La machette est un objet {{1}}.', 'tranchant'),
        A('Relie chaque outil à son danger.', ('la machette', 'tranchant'),
          ('le râteau', 'pointu'), n=3),
        V('Je peux jouer avec la machette si je fais attention.', False, n=4,
          e='Non. On ne joue jamais avec les objets tranchants.'))),

    # -------------------------------------------------------------- sans date
    L(SC, 'Les saisons et les végétaux', 'Éducation à l’environnement', '2026-10-29',
      'Une saison est une période distincte de l’année. En saison sèche, les arbres perdent '
      'leurs feuilles et leurs écorces craquellent à cause de la chaleur. En saison des pluies, '
      'il pleut beaucoup et les végétaux retrouvent leur verdure.',
      'kz-sais-couv', ['saison sèche', 'saison des pluies'],

      N('definition',
        'Une saison est une période distincte de l’année. En fonction du climat, on a la saison '
        'sèche et la saison des pluies.',
        'kz-sais-def', F('Les saisons', 'la saison sèche', 'la saison des pluies'),
        ('simple', 'L’année est faite de périodes différentes : il fait sec, puis il pleut.'),
        ('visuel', 'Un calendrier avec un soleil sur certains mois, des nuages sur d’autres.'),
        Q('Qu’est-ce qu’une saison ?', 'Une période distincte de l’année', 'Un seul jour',
          'Une sorte d’arbre'),
        V('On a la saison sèche et la saison des pluies.', True),
        T('Une saison est une {{1}} distincte de l’année.', 'période'),
        Q('Combien de saisons le cahier donne-t-il ?', 'deux', 'quatre', 'une', n=3),
        V('Une saison dure une seule journée.', False, n=4,
          e='Non. C’est une période de l’année.')),

      N('relation',
        'En saison sèche, les arbres perdent leurs feuilles et ont des écorces craquelées, à '
        'cause de trop de chaleur.',
        'kz-sais-seche', F('La saison sèche', 'trop de chaleur', 'les feuilles tombent',
                           'l’écorce craquelle'),
        ('simple', 'Il fait si chaud que l’arbre lâche ses feuilles.'),
        ('visuel', 'Un arbre presque nu, son écorce fendue, sous un grand soleil.'),
        Q('Que font les arbres en saison sèche ?', 'Ils perdent leurs feuilles',
          'Ils font des fleurs partout', 'Ils grandissent très vite'),
        V('En saison sèche, l’écorce des arbres craquelle.', True),
        T('En saison sèche, les arbres perdent leurs {{1}}.', 'feuilles'),
        Q('Pourquoi l’écorce craquelle-t-elle en saison sèche ?', 'À cause de trop de chaleur',
          'À cause de la pluie', 'À cause du froid', n=3),
        V('En saison sèche, le feuillage est abondant.', False, n=4,
          e='Non. C’est en saison des pluies.')),

      N('relation',
        'En saison des pluies, il pleut abondamment : les végétaux retrouvent leur verdure et le '
        'feuillage est abondant.',
        'kz-sais-pluies', F('La saison des pluies', 'il pleut beaucoup', 'tout redevient vert',
                            'beaucoup de feuilles'),
        ('simple', 'La pluie revient, et les plantes redeviennent vertes.'),
        ('visuel', 'Le même arbre, couvert de feuilles vertes, sous la pluie.'),
        Q('Que se passe-t-il en saison des pluies ?', 'Les végétaux redeviennent verts',
          'Les arbres perdent leurs feuilles', 'Les écorces craquellent'),
        V('En saison des pluies, le feuillage est abondant.', True),
        T('En saison des pluies, les végétaux retrouvent leur {{1}}.', 'verdure'),
        A('Relie chaque saison à ce qu’on voit.', ('la saison sèche', 'les feuilles tombent'),
          ('la saison des pluies', 'tout redevient vert'), n=3),
        V('En saison des pluies, il ne pleut presque pas.', False, n=4,
          e='Non. Il pleut abondamment.'))),
]
