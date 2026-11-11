# -*- coding: utf-8 -*-
# Grammaire — cinq leçons. Chargé par lecons-brayne-francais-oct.py.
#
# Les exemples sont ceux du cahier, et ceux du contrôle du 16 octobre quand la
# maîtresse les a corrigés : « N-aimes-tu pas aller au champ ? », « Le chef de
# mon village est un adolescent ».

FR = 'Français'
GRAM = 'Grammaire'

LECONS = [
    # ------------------------------------------------------------ 12 octobre
    L(FR, 'Les formes de phrases', GRAM, '2026-10-12',
      'Les formes de phrases indiquent les modifications de la structure d’une phrase pour '
      'exprimer un point de vue particulier sans changer son type de base. Il y a la forme '
      'affirmative, la forme négative et la forme interro-négative.',
      'bf-fp-couv', ['affirmative', 'négative', 'interro-négative'],

      N('definition',
        'Les formes de phrases indiquent les modifications de la structure d’une phrase pour '
        'exprimer un point de vue particulier sans changer son type de base.',
        'bf-fp-def', F('Les formes de phrases', 'la forme affirmative', 'la forme négative',
                       'la forme interro-négative'),
        ('simple', 'La même phrase peut dire oui, dire non, ou demander en disant non.'),
        ('visuel', 'Il vient. Il ne vient pas. Ne vient-il pas ? Trois formes, un seul sujet.'),
        Q('Combien de formes de phrases le cahier donne-t-il ?', 'Trois', 'Deux', 'Cinq'),
        V('La forme négative est une forme de phrase.', True),
        T('Les trois formes sont : affirmative, négative et interro-{{1}}.', 'négative'),
        Q('Laquelle est une forme de phrase ?', 'La forme affirmative', 'Le passé simple',
          'Le groupe nominal', n=3),
        V('Changer la forme d’une phrase change son type de base.', False, n=4,
          e='Non. Le type de base reste le même.')),

      N('definition',
        'La forme affirmative affirme ou assure l’information qu’elle apporte. Exemple : '
        'Yaoundé est la capitale politique du Cameroun.',
        'bf-fp-affirmative', F('La forme affirmative', 'elle affirme', 'elle assure',
                               'Yaoundé est la capitale'),
        ('simple', 'Une phrase affirmative dit que quelque chose est vrai.'),
        ('visuel', 'Mon village est situé dans la région du Centre : pas de « ne », pas de '
                   '« pas ».'),
        Q('« Mon village est situé dans la région du Centre. » Quelle forme ?', 'Affirmative',
          'Négative', 'Interro-négative'),
        V('« Yaoundé est la capitale politique du Cameroun » est à la forme affirmative.', True),
        T('La forme {{1}} affirme ou assure l’information qu’elle apporte.', 'affirmative'),
        Q('Laquelle de ces phrases est à la forme affirmative ?',
          'Le chef de mon village est un adolescent.',
          'Le chef de mon village n’est pas un adolescent.',
          'Le chef n’est-il pas un adolescent ?', n=3),
        V('« Mon oncle n’a pas regagné son poste » est à la forme affirmative.', False, n=4,
          e='Non. Il y a ne… pas : c’est la forme négative.')),

      N('definition',
        'Grâce à l’emploi de la négation ne… pas, ne… plus, ne… jamais, une phrase affirmative '
        'peut devenir négative. Exemple : Mon village n’est pas loin de Yaoundé.',
        'bf-fp-negative', F('La forme négative', 'ne… pas', 'ne… plus', 'ne… jamais',
                            'n’est pas loin de Yaoundé'),
        ('simple', 'La négation a deux morceaux, et le verbe se place entre les deux.'),
        ('pas_a_pas', 'Le chef est un adolescent. Mets ne avant est et pas après : le chef '
                      'n’est pas un adolescent.'),
        Q('« Mon oncle n’a pas regagné son poste de travail. » Quelle forme ?', 'Négative',
          'Affirmative', 'Interro-négative'),
        V('« Mon village n’est pas loin de Yaoundé » est à la forme négative.', True),
        T('Forme négative : le chef de mon village n’est {{1}} un adolescent.', 'pas'),
        Q('Laquelle est une négation ?', 'ne… jamais', 'est-ce que', 'parce que', n=3),
        V('La négation s’écrit avec un seul mot.', False, n=4,
          e='Non. Elle en a deux : ne et pas, ne et plus, ne et jamais.')),

      N('definition',
        'La forme interro-négative est une phrase qui combine à la fois une question et une '
        'négation. Exemple : Yaoundé n’est-elle pas la capitale politique du Cameroun ?',
        'bf-fp-interroneg', F('La forme interro-négative', 'une question', '+ une négation',
                              'N’aimes-tu pas aller au champ ?'),
        ('simple', 'On pose une question, et dans la question il y a ne… pas.'),
        ('visuel', 'Regarde la fin : un point d’interrogation. Regarde le milieu : n’… pas.'),
        Q('« N’aimes-tu pas aller au champ ? » Quelle forme ?', 'Interro-négative', 'Négative',
          'Affirmative'),
        V('Une phrase interro-négative se termine par un point d’interrogation.', True),
        T('La forme interro-négative combine une question et une {{1}}.', 'négation'),
        A('Relie chaque phrase à sa forme.', ('Il vient.', 'affirmative'),
          ('Il ne vient pas.', 'négative'), ('Ne vient-il pas ?', 'interro-négative')),
        Q('Laquelle de ces phrases est à la forme interro-négative ?',
          'Le chef n’est-il pas un adolescent ?', 'Le chef n’est pas un adolescent.',
          'Le chef est-il un adolescent ?', n=4),
        V('« Le chef est-il un adolescent ? » est à la forme interro-négative.', False, n=4,
          e='Non. C’est une question, mais sans négation.')),
      ),

    # ------------------------------------------------------------ 13 octobre
    L(FR, 'La phrase simple et la phrase complexe', GRAM, '2026-10-13',
      'La phrase simple contient un seul verbe conjugué : elle correspond à une seule '
      'proposition. La phrase complexe contient plusieurs verbes conjugués et se découpe en '
      'plusieurs propositions.',
      'bf-ps-couv', ['un verbe', 'plusieurs verbes'],

      N('definition',
        'La phrase simple contient un seul verbe conjugué. Elle correspond à une seule '
        'proposition. Exemple : La ville est très bruyante.',
        'bf-ps-simple', F('La phrase simple', 'un seul verbe conjugué', 'une seule proposition',
                          'La ville est très bruyante.', vif=(2,)),
        ('simple', 'Compte les verbes conjugués. Un seul : la phrase est simple.'),
        ('visuel', 'La ville est très bruyante : un seul verbe, est.'),
        Q('Combien de verbes conjugués contient une phrase simple ?', 'Un seul', 'Deux',
          'Aucun'),
        V('« La ville est très bruyante » est une phrase simple.', True),
        T('La phrase simple correspond à une seule {{1}}.', 'proposition'),
        Q('Laquelle de ces phrases est une phrase simple ?', 'Le village est calme.',
          'La ville est bruyante pourtant le village est calme.',
          'Il mange et il boit pendant que nous jouons.', n=3),
        V('Une phrase simple peut contenir trois verbes conjugués.', False, n=4,
          e='Non. Un seul verbe conjugué.')),

      N('definition',
        'La phrase complexe contient plusieurs verbes conjugués et se découpe en plusieurs '
        'propositions. Exemple : La ville est bruyante pourtant le village est calme.',
        'bf-ps-complexe', F('La phrase complexe', 'plusieurs verbes conjugués',
                            'plusieurs propositions', 'La ville est bruyante',
                            'pourtant le village est calme.', vif=(3, 4)),
        ('simple', 'Deux verbes conjugués ou plus : la phrase est complexe.'),
        ('pas_a_pas', 'Souligne les verbes : est, puis est. Deux verbes, donc deux '
                      'propositions.'),
        Q('« La ville est bruyante pourtant le village est calme. » Cette phrase est…',
          'complexe', 'simple', 'négative'),
        V('Une phrase complexe se découpe en plusieurs propositions.', True),
        T('La phrase complexe contient {{1}} verbes conjugués.', 'plusieurs'),
        A('Relie chaque phrase à son nom.', ('La ville est bruyante.', 'phrase simple'),
          ('Il rit et il chante.', 'phrase complexe')),
        Q('Combien de propositions dans « La ville est bruyante pourtant le village est '
          'calme » ?', 'Deux', 'Une seule', 'Quatre', n=4),
        V('« Il rit et il chante » est une phrase simple.', False, n=4,
          e='Non. Deux verbes conjugués, rit et chante : phrase complexe.')),
      ),

    # ------------------------------------------------------------ 19 octobre
    L(FR, 'Les noms propres et les noms communs', GRAM, '2026-10-19',
      'Un nom propre désigne un être, un animal familier ou un lieu de façon unique. Il '
      'commence par une majuscule. Un nom commun désigne un être, une chose ou un lieu de '
      'façon générale. Il s’écrit en minuscule et il est presque toujours précédé d’un '
      'déterminant.',
      'bf-np-couv', ['le Cameroun', 'la Sanaga', 'un village'],

      N('definition',
        'Un nom propre désigne un être, un animal familier ou un lieu de façon unique et '
        'particulière. Exemples : Sylviane, Nadège, Stéphane.',
        'bf-np-propre', F('Le nom propre', 'un être', 'un animal familier', 'un lieu',
                          'de façon unique'),
        ('simple', 'Il n’y a qu’un seul Cameroun, qu’une seule Sanaga : ce sont des noms '
                   'propres.'),
        ('visuel', 'Stéphane est le nom d’un garçon précis. Garçon est le nom de tous les '
                   'garçons.'),
        Q('Lequel est un nom propre ?', 'Nadège', 'maîtresse', 'village'),
        V('Un nom propre désigne un être ou un lieu de façon unique.', True),
        T('Un nom {{1}} désigne un être ou un lieu de façon unique et particulière.', 'propre'),
        Q('Lequel est un nom propre ?', 'la Sanaga', 'la rivière', 'le fleuve', n=3),
        V('« Village » est un nom propre.', False, n=4, e='Non. C’est un nom commun.')),

      N('relation',
        'Le nom propre commence par une majuscule et ne prend pas en général de déterminant, '
        'sauf pour les noms des pays, fleuves, montagnes : le Cameroun, la Sanaga, le Mont '
        'Cameroun.',
        'bf-np-majuscule', F('Majuscule et déterminant', 'Sylviane : pas de déterminant',
                             'le Cameroun : un pays', 'la Sanaga : un fleuve',
                             'le Mont Cameroun : une montagne'),
        ('simple', 'On dit Stéphane, pas le Stéphane. Mais on dit le Cameroun.'),
        ('visuel', 'La première lettre est toujours une grande lettre : S, N, C.'),
        Q('Par quoi commence toujours un nom propre ?', 'Une majuscule', 'Un déterminant',
          'Une minuscule'),
        V('On écrit « le Cameroun » avec un déterminant.', True),
        T('Le nom propre commence par une {{1}}.', 'majuscule'),
        Q('Quels noms propres prennent un déterminant ?', 'Les pays, les fleuves, les montagnes',
          'Les prénoms des enfants', 'Les noms des maîtresses', n=3),
        V('On écrit « la Sylviane » avec un déterminant.', False, n=4,
          e='Non. Un prénom ne prend pas de déterminant.')),

      N('definition',
        'Un nom commun désigne un être, une chose ou un lieu de façon générale. Il s’écrit en '
        'minuscule et est presque toujours précédé d’un déterminant : la maîtresse, un chien.',
        'bf-np-commun', F('Le nom commun', 'de façon générale', 'en minuscule',
                          'avec un déterminant', 'la maîtresse, un chien'),
        ('simple', 'Un chien, c’est n’importe quel chien. C’est un nom commun.'),
        ('visuel', 'Devant lui il y a presque toujours un petit mot : la, un, le.'),
        Q('Lequel est un nom commun ?', 'chien', 'Stéphane', 'Yaoundé'),
        V('Un nom commun est presque toujours précédé d’un déterminant.', True),
        T('Un nom commun s’écrit en {{1}}.', 'minuscule'),
        A('Range chaque nom dans sa famille.', ('Nadège', 'nom propre'),
          ('la maîtresse', 'nom commun'), ('la Sanaga', 'nom propre aussi'),
          ('le village', 'nom commun aussi')),
        V('« La maîtresse » est un nom propre.', False, n=4, e='Non. C’est un nom commun.'),
        Q('Dans « un chien », quel mot est le déterminant ?', 'un', 'chien', 'aucun des deux',
          n=4)),
      ),

    # ------------------------------------------------------------ 20 octobre
    L(FR, 'Les pronoms indéfinis', GRAM, '2026-10-20',
      'Les pronoms indéfinis remplacent un nom sans apporter de précision sur lui. Ils sont '
      'nombreux et variés : personne, rien, tout le monde, certains, plusieurs, chacun, l’un, '
      'l’autre, d’autres.',
      'bf-pi-couv', ['quelqu’un', 'personne', 'chacun'],

      N('definition',
        'Les pronoms indéfinis remplacent un nom sans apporter de précision sur lui. Exemple : '
        'Quelqu’un a apporté quelque chose venant du village.',
        'bf-pi-def', F('Le pronom indéfini', 'il remplace un nom', 'sans donner de précision',
                       'Quelqu’un a apporté', 'quelque chose'),
        ('simple', 'Quelqu’un : on sait qu’il y a une personne, on ne sait pas laquelle.'),
        ('visuel', 'Papa a apporté des ignames. Quelqu’un a apporté quelque chose : on ne sait '
                   'plus qui, ni quoi.'),
        Q('Que fait un pronom indéfini ?', 'Il remplace un nom sans le préciser',
          'Il indique le temps du verbe', 'Il relie deux phrases simples'),
        V('« Quelqu’un » est un pronom indéfini.', True),
        T('Les pronoms {{1}} remplacent un nom sans apporter de précision sur lui.', 'indéfinis'),
        Q('Dans « Quelqu’un a apporté quelque chose », combien de pronoms indéfinis ?', 'Deux',
          'Un seul', 'Aucun', n=3),
        V('Un pronom indéfini dit exactement de qui on parle.', False, n=4,
          e='Non. Il ne donne aucune précision.')),

      N('liste',
        'Ils sont nombreux et variés : personne, rien, tout le monde, certains, plusieurs, '
        'chacun, l’un, l’autre, d’autres.',
        'bf-pi-liste', F('Nombreux et variés', 'personne, rien', 'tout le monde',
                         'certains, plusieurs', 'chacun, l’un, l’autre'),
        ('simple', 'Personne et rien disent zéro. Tout le monde et chacun disent tous.'),
        ('visuel', 'Plusieurs sont venus, d’autres sont restés : on ne compte pas, on ne nomme '
                   'pas.'),
        Q('Lequel est un pronom indéfini ?', 'chacun', 'village', 'chanter'),
        V('« Plusieurs » est un pronom indéfini.', True),
        T('{{1}} n’est venu : la cour est vide.', 'personne',
          e='Personne n’est venu : la cour est vide.'),
        Q('Lequel n’est pas un pronom indéfini ?', 'Yaoundé', 'rien', 'certains', n=3),
        V('« Tout le monde » est un pronom indéfini.', True, n=4),
        Q('Lequel est un pronom indéfini ?', 'd’autres', 'pourtant', 'bruyante', n=4)),
      ),

    # ------------------------------------------------------------ 26 octobre
    L(FR, 'Le groupe nominal et le groupe verbal', GRAM, '2026-10-26',
      'Le groupe nominal est constitué d’un nom précédé d’un déterminant : un village. On peut '
      'y ajouter un adjectif qualificatif ou un autre groupe nominal. Le groupe verbal peut '
      'être constitué d’un seul verbe, ou d’un verbe accompagné d’un groupe nominal.',
      'bf-gn-couv', ['un doux village', 'conduit une voiture'],

      N('definition',
        'Le groupe nominal est constitué d’un nom précédé d’un déterminant. Exemple : un '
        'village. Le nom est le mot principal du groupe nominal.',
        'bf-gn-def', P('Le groupe nominal', ('un', 'déterminant'), ('village', 'nom')),
        ('simple', 'Un petit mot, puis un nom : c’est un groupe nominal.'),
        ('visuel', 'Dans « un village », le mot qui compte le plus est village : c’est le nom.'),
        Q('De quoi est constitué le groupe nominal ?', 'D’un nom précédé d’un déterminant',
          'D’un verbe conjugué tout seul', 'De deux verbes à l’infinitif'),
        V('« Un village » est un groupe nominal.', True),
        T('Le {{1}} est le mot principal du groupe nominal.', 'nom'),
        Q('Dans « un village », quel est le mot principal ?', 'village', 'un',
          'aucun des deux', n=3),
        V('Le déterminant est le mot principal du groupe nominal.', False, n=4,
          e='Non. C’est le nom.')),

      N('liste',
        'On peut ajouter d’autres éléments au groupe nominal : l’adjectif qualificatif, comme '
        'dans un doux village, ou un autre groupe nominal, comme dans le doux village de mes '
        'rêves.',
        'bf-gn-ajouts', F('On peut ajouter', 'un adjectif qualificatif', 'un doux village',
                          'un autre groupe nominal', 'le doux village de mes rêves',
                          vif=(1, 3)),
        ('simple', 'Le groupe nominal peut grandir : on lui ajoute des mots qui en disent '
                   'plus.'),
        ('pas_a_pas', 'Un village. Un doux village. Le doux village de mes rêves. Le nom reste '
                      'village.'),
        Q('Dans « un doux village », quel mot est l’adjectif qualificatif ?', 'doux', 'un',
          'village'),
        V('On peut ajouter un adjectif qualificatif au groupe nominal.', True),
        T('Dans « un doux village », doux est un {{1}} qualificatif.', 'adjectif'),
        Q('Dans « le doux village de mes rêves », quel groupe a été ajouté ?', 'de mes rêves',
          'le doux', 'village', n=3),
        V('Dans « un doux village », le mot principal est doux.', False, n=4,
          e='Non. Le mot principal reste le nom : village.')),

      N('relation',
        'Un groupe nominal peut aussi être constitué d’un seul nom. Exemple : Brice est '
        'inquiet.',
        'bf-gn-seul', F('Un seul nom', 'Brice est inquiet.', 'Brice : groupe nominal',
                        'un nom, tout seul'),
        ('simple', 'Un prénom n’a pas besoin de déterminant : il fait un groupe nominal à lui '
                   'seul.'),
        ('visuel', 'Brice est inquiet. Qui est inquiet ? Brice. Un mot, un groupe nominal.'),
        Q('Dans « Brice est inquiet », quel est le groupe nominal ?', 'Brice', 'est',
          'inquiet'),
        V('Un groupe nominal peut être constitué d’un seul nom.', True),
        T('Un groupe nominal peut aussi être constitué d’un seul {{1}}.', 'nom'),
        Q('Combien de mots compte le groupe nominal dans « Brice est inquiet » ?', 'Un seul',
          'Deux', 'Trois', n=3),
        V('Un groupe nominal a toujours au moins deux mots.', False, n=4,
          e='Non. Brice, tout seul, est un groupe nominal.')),

      N('relation',
        'Le groupe verbal peut être constitué d’un seul verbe : Marie conduit. Il peut être '
        'accompagné d’un groupe nominal : Marie, ma grande sœur, conduit une voiture.',
        'bf-gn-verbal', P('Le groupe verbal', ('Marie', 'conduit'),
                          ('ma grande sœur', 'conduit une voiture')),
        ('simple', 'Le groupe verbal dit ce que fait le sujet. Son mot principal est le '
                   'verbe.'),
        ('visuel', 'Marie conduit. Marie conduit une voiture. Le groupe verbal a grandi.'),
        Q('Dans « Marie conduit », quel est le groupe verbal ?', 'conduit', 'Marie',
          'Marie conduit'),
        V('Le groupe verbal peut être constitué d’un seul verbe.', True),
        T('Dans « Marie conduit une voiture », le groupe {{1}} est « conduit une voiture ».',
          'verbal'),
        A('Relie chaque groupe à son nom.', ('Marie, ma grande sœur', 'groupe nominal'),
          ('conduit une voiture', 'groupe verbal')),
        Q('Dans « Marie, ma grande sœur, conduit une voiture », quel est le groupe verbal ?',
          'conduit une voiture', 'ma grande sœur', 'Marie', n=4),
        V('Dans « Marie conduit une voiture », « une voiture » est un groupe nominal.', True,
          n=4)),
      ),
]
