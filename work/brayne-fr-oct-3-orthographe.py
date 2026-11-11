# -*- coding: utf-8 -*-
# Orthographe — six leçons. Chargé par lecons-brayne-francais-oct.py.
#
# La leçon « on et on n- » insiste sur les phrases où la négation ne se
# termine pas par « pas » — « on n-a rien compris » — parce que c-est là que
# le n- s-oublie.

FR = 'Français'
ORTHO = 'Orthographe'

LECONS = [
    # ------------------------------------------------------------ 14 octobre
    L(FR, 'On et on n’', ORTHO, '2026-10-14',
      '« On » est un pronom personnel ou un pronom indéfini. Il s’emploie dans la phrase à la '
      'forme affirmative : on a mangé une pomme au champ. « On n’ », suivi de pas, s’emploie '
      'dans les phrases à la forme négative : on n’a pas mangé la pomme au champ.',
      'bf-on-couv', ['on a mangé', 'on n’a pas mangé'],

      N('definition',
        '« On » est un pronom personnel ou un pronom indéfini. Il s’emploie dans la phrase à la '
        'forme affirmative. Exemple : On a mangé une pomme au champ.',
        'bf-on-affirmative', F('On : forme affirmative', 'On a mangé une pomme.',
                               'On est arrivé à l’heure.', 'Quand on veut, on peut !'),
        ('simple', 'Quand la phrase dit oui, on écrit « on » tout seul.'),
        ('pas_a_pas', 'Remplace on par il. Il a mangé : pas de négation, donc « on a mangé ».'),
        Q('Complète : « … est arrivé à l’heure au rendez-vous. »', 'On', 'On n’', 'Ont'),
        V('Dans « On a mangé une pomme au champ », la phrase est à la forme affirmative.', True),
        T('« On » est un {{1}} personnel ou indéfini.', 'pronom'),
        Q('Complète : « Quand … veut, … peut ! »', 'on, on', 'on n’, on n’', 'on, on n’', n=3),
        V('Dans une phrase affirmative, on écrit « on n’ ».', False, n=4,
          e='Non. « On » tout seul : on a mangé.')),

      N('definition',
        '« On » suivi de la négation « n’ » et de « pas » s’emploie dans les phrases à la forme '
        'négative. Exemple : On n’a pas mangé la pomme au champ.',
        'bf-on-negative', F('On n’ : forme négative', 'On n’a pas mangé.',
                            'On n’a rien compris.', 'On n’aime pas les légumes.', vif=(1,)),
        ('simple', 'Quand la phrase dit non, il faut le n’ : on n’a pas, on n’a rien, on n’a '
                   'jamais.'),
        ('pas_a_pas', 'Remplace on par il. Il n’a rien compris : tu entends le n’. Donc « on '
                      'n’a rien compris ».'),
        Q('Complète : « … a rien compris à cet exercice de français. »', 'On n’', 'On', 'Ont'),
        Q('Complète : « … aime pas manger les légumes trop cuits. »', 'On n’', 'On', 'Ont'),
        V('On écrit « On n’a pas mangé la pomme au champ ».', True),
        T('On n’a {{1}} compris à cet exercice.', 'rien'),
        Q('Quel mot montre que « On n’a rien compris » est une phrase négative ?', 'rien',
          'compris', 'on', n=3),
        V('On écrit « On a rien compris à cet exercice ».', False, n=4,
          e='Non. Rien est une négation : on n’a rien compris.'),
        Q('Laquelle de ces phrases est bien écrite ?', 'On n’a jamais vu ce film.',
          'On a jamais vu ce film.', 'Ont a jamais vu ce film.', n=4)),
      ),

    # ------------------------------------------------------------ 15 octobre
    L(FR, 'Les mots commençant par ef et of', ORTHO, '2026-10-15',
      'Les mots commençant par ef et of s’écrivent toujours avec deux f. Exemples : effacer, '
      'effrayant, effet, effort, offre, officiel, offenser, office.',
      'bf-ff-couv', ['effacer', 'effort', 'offre', 'officiel'],

      N('definition',
        'Les mots commençant par ef s’écrivent toujours avec deux f. Exemples : effacer, '
        'effrayant, effet, effort.',
        'bf-ff-ef', F('ef : deux f', 'effacer', 'effrayant', 'effet', 'effort'),
        ('simple', 'Si un mot commence par le son « èf », écris deux f.'),
        ('visuel', 'Ef-facer, ef-fort : le premier f finit la syllabe, le second commence la '
                   'suivante.'),
        Q('Laquelle de ces écritures est juste ?', 'effacer', 'efacer', 'éfacer'),
        V('« Effort » s’écrit avec deux f.', True),
        T('Avec la gomme, on peut {{1}} le tableau. (deux f)', 'effacer'),
        Q('Laquelle de ces écritures est juste ?', 'effrayant', 'efrayant', 'effraiyant', n=3),
        V('« Effet » s’écrit avec un seul f.', False, n=4, e='Non : effet, deux f.')),

      N('definition',
        'Les mots commençant par of s’écrivent toujours avec deux f. Exemples : offre, '
        'officiel, offenser, office.',
        'bf-ff-of', F('of : deux f', 'offre', 'officiel', 'offenser', 'office'),
        ('simple', 'Si un mot commence par le son « of », écris deux f.'),
        ('visuel', 'Of-fre, of-ficiel : deux f, comme dans les mots en ef.'),
        Q('Laquelle de ces écritures est juste ?', 'officiel', 'oficiel', 'ofissiel'),
        V('« Offre » s’écrit avec deux f.', True),
        T('Le marchand fait une {{1}} : deux mangues pour le prix d’une. (deux f)', 'offre'),
        Q('Laquelle de ces écritures est juste ?', 'offenser', 'ofenser', 'offancer', n=3),
        V('« Office » s’écrit avec un seul f.', False, n=4, e='Non : office, deux f.'),
        Q('Combien de f dans les mots qui commencent par ef et of ?', 'Deux', 'Un seul',
          'Trois', n=4)),
      ),

    # ------------------------------------------------------------ 21 octobre
    L(FR, 'À et a', ORTHO, '2026-10-21',
      '« a » sans accent, c’est le verbe avoir conjugué au présent de l’indicatif : il peut '
      'être remplacé par avait ou aura. « à » avec accent est une préposition, un mot '
      'invariable qui sert à introduire un lieu, un temps ou un objet.',
      'bf-aa-couv', ['il a', 'il avait', 'à l’école'],

      N('definition',
        '« a » sans accent, c’est le verbe avoir conjugué au présent de l’indicatif. Il peut '
        'être remplacé par avait ou aura. Exemple : Il a une belle montre.',
        'bf-aa-verbe', F('a : le verbe avoir', 'Il a une belle montre.',
                         'Il avait une belle montre.', 'Il aura une belle montre.'),
        ('simple', 'Si tu peux dire avait à la place, écris a sans accent.'),
        ('pas_a_pas', 'Il a une montre. Essaie : il avait une montre. Ça marche : pas '
                      'd’accent.'),
        Q('Complète : « Il … une belle montre. »', 'a', 'à', 'as'),
        V('« a » sans accent est le verbe avoir.', True),
        T('« a » sans accent peut être remplacé par {{1}} ou aura.', 'avait'),
        Q('Dans quelle phrase écrit-on « a » sans accent ?', 'Landry a un cahier neuf.',
          'Landry va à l’école.', 'Il arrive à midi.', n=3),
        V('Dans « Il a une belle montre », on peut dire « Il avait une belle montre ».', True,
          n=4)),

      N('definition',
        '« à » avec accent est une préposition. C’est un mot invariable qui sert à introduire '
        'un lieu, un temps ou un objet. Exemple : Landry va à l’école.',
        'bf-aa-preposition', F('à : la préposition', 'un mot invariable', 'un lieu : à l’école',
                               'un temps : à midi', 'Landry va à l’école.'),
        ('simple', 'Si tu ne peux pas dire avait à la place, écris à avec accent.'),
        ('pas_a_pas', 'Landry va à l’école. Essaie : Landry va avait l’école. Ça ne veut rien '
                      'dire : accent.'),
        Q('Complète : « Landry va … l’école. »', 'à', 'a', 'as'),
        V('« à » avec accent est une préposition.', True),
        T('« à » avec accent est un mot {{1}} : il ne change jamais.', 'invariable'),
        A('Relie chaque mot à ce qu’il est.', ('a', 'le verbe avoir'), ('à', 'une préposition')),
        V('Dans « Landry va à l’école », on peut remplacer à par avait.', False, n=4,
          e='Non. « Landry va avait l’école » ne veut rien dire : c’est la préposition à.'),
        Q('Complète : « Il … une montre et il va … l’école. »', 'a, à', 'à, a', 'a, a', n=4)),
      ),

    # ------------------------------------------------------------ 27 octobre
    L(FR, 'L’accord de l’adjectif avec le nom', ORTHO, '2026-10-27',
      'L’adjectif qualificatif s’accorde en genre, féminin ou masculin, et en nombre, '
      'singulier ou pluriel, avec le nom qu’il qualifie. Une ville bruyante, des villes '
      'bruyantes.',
      'bf-ad-couv', ['une ville bruyante', 'des villes bruyantes'],

      N('definition',
        'L’adjectif qualificatif s’accorde en genre, féminin ou masculin, et en nombre, '
        'singulier ou pluriel, avec le nom qu’il qualifie.',
        'bf-ad-regle', P('Genre et nombre', ('le genre', 'féminin, masculin'),
                         ('le nombre', 'singulier, pluriel')),
        ('simple', 'L’adjectif copie le nom : si le nom est féminin pluriel, l’adjectif aussi.'),
        ('visuel', 'Le genre, c’est féminin ou masculin. Le nombre, c’est un seul ou '
                   'plusieurs.'),
        Q('Avec quoi l’adjectif qualificatif s’accorde-t-il ?', 'Avec le nom qu’il qualifie',
          'Avec le verbe de la phrase', 'Avec le premier mot'),
        V('L’adjectif qualificatif s’accorde en genre et en nombre.', True),
        T('L’adjectif s’accorde en genre et en {{1}} avec le nom.', 'nombre'),
        A('Relie chaque mot à ce qu’il veut dire.', ('le genre', 'féminin ou masculin'),
          ('le nombre', 'singulier ou pluriel')),
        V('L’adjectif qualificatif ne change jamais.', False, n=4,
          e='Non. Il s’accorde avec le nom.')),

      N('relation',
        'Exemples : une ville bruyante, au féminin singulier ; des villes bruyantes, au féminin '
        'pluriel.',
        'bf-ad-exemple', P('Une ville, des villes', ('une ville bruyante', 'féminin singulier'),
                           ('des villes bruyantes', 'féminin pluriel')),
        ('simple', 'Ville est féminin : bruyant prend un e. Villes est pluriel : il prend '
                   'aussi un s.'),
        ('pas_a_pas', 'Bruyant. Féminin : bruyante. Féminin pluriel : bruyantes.'),
        Q('Complète : « une ville … ».', 'bruyante', 'bruyant', 'bruyants'),
        V('On écrit « des villes bruyantes » avec es à la fin de l’adjectif.', True),
        T('Des villes {{1}}. (bruyant)', 'bruyantes'),
        Q('« Des villes bruyantes » : l’adjectif est au…', 'féminin pluriel',
          'masculin singulier', 'féminin singulier', n=3),
        V('On écrit « une ville bruyant ».', False, n=4,
          e='Non. Ville est féminin : une ville bruyante.'),
        Q('Complète : « des villages … ».', 'bruyants', 'bruyantes', 'bruyante', n=4)),
      ),

    # ------------------------------------------------------------ 28 octobre
    L(FR, 'L’accord du verbe avec son sujet', ORTHO, '2026-10-28',
      'Le verbe s’accorde en personne avec son ou ses sujets. Si le sujet est au singulier, le '
      'verbe s’accorde au singulier. Si le sujet est au pluriel, le verbe s’accorde au '
      'pluriel. S’il y a plusieurs sujets, le verbe se met au pluriel.',
      'bf-vs-couv', ['l’enfant chante', 'les enfants chantent'],

      N('relation',
        'Si le sujet est au singulier, le verbe s’accorde au singulier. Exemple : L’enfant '
        'chante. Qui est-ce qui chante ? L’enfant.',
        'bf-vs-singulier', P('Sujet au singulier', ('l’enfant', 'chante'),
                             ('le sujet', 'le verbe')),
        ('simple', 'Un seul enfant : le verbe s’écrit chante.'),
        ('pas_a_pas', 'Pour trouver le sujet, demande : qui est-ce qui chante ? L’enfant.'),
        Q('Complète : « L’enfant … ».', 'chante', 'chantent', 'chantes'),
        V('Si le sujet est au singulier, le verbe s’accorde au singulier.', True),
        T('Pour trouver le sujet, on demande : {{1}} est-ce qui chante ?', 'qui'),
        Q('Dans « L’enfant chante », quel est le sujet ?', 'L’enfant', 'chante',
          'aucun des deux', n=3),
        V('On écrit « L’enfant chantent ».', False, n=4,
          e='Non. Un seul enfant : l’enfant chante.')),

      N('relation',
        'Si le sujet est au pluriel, le verbe s’accorde au pluriel. Exemple : Les enfants '
        'chantent.',
        'bf-vs-pluriel', P('Sujet au pluriel', ('les enfants', 'chantent'),
                           ('le sujet', 'le verbe')),
        ('simple', 'Plusieurs enfants : le verbe prend ent.'),
        ('visuel', 'Le ent de chantent ne s’entend pas, mais il s’écrit.'),
        Q('Complète : « Les enfants … ».', 'chantent', 'chante', 'chantes'),
        V('Dans « Les enfants chantent », le sujet est au pluriel.', True),
        T('Les enfants {{1}}. (chanter)', 'chantent'),
        Q('Dans « Les enfants chantent », quel est le sujet ?', 'Les enfants', 'chantent',
          'aucun des deux', n=3),
        V('On écrit « Les enfants chante ».', False, n=4,
          e='Non. Plusieurs enfants : les enfants chantent.')),

      N('relation',
        'S’il y a plusieurs sujets, le verbe se met au pluriel. Exemple : L’enfant et son ami '
        'chantent.',
        'bf-vs-plusieurs', F('Plusieurs sujets', 'l’enfant : sujet 1', 'son ami : sujet 2',
                             'chantent : le verbe', vif=(2,)),
        ('simple', 'Un sujet et encore un sujet, cela fait deux : le verbe se met au pluriel.'),
        ('visuel', 'L’enfant et son ami, c’est comme « ils » : ils chantent.'),
        Q('Complète : « L’enfant et son ami … ».', 'chantent', 'chante', 'chantes'),
        V('S’il y a plusieurs sujets, le verbe se met au pluriel.', True),
        T('L’enfant et son ami {{1}}. (chanter)', 'chantent'),
        Q('Combien de sujets dans « L’enfant et son ami chantent » ?', 'Deux', 'Un seul',
          'Trois', n=3),
        V('On écrit « L’enfant et son ami chante ».', False, n=4,
          e='Non. Deux sujets : le verbe est au pluriel, chantent.'),
        Q('Complète : « Le père et la mère … dans la forêt. »', 'partent', 'part', 'pars',
          n=4)),
      ),

    # ------------------------------------------------------------ 29 octobre
    L(FR, 'Le féminin des noms', ORTHO, '2026-10-29',
      'Un nom est au féminin lorsqu’on peut placer les déterminants une ou la devant. Le '
      'féminin se forme en ajoutant un e muet, en ajoutant euse ou trice, ou en doublant la '
      'consonne. Certains noms restent invariables, d’autres changent complètement de forme.',
      'bf-fe-couv', ['une amie', 'une chanteuse', 'une reine'],

      N('definition',
        'Un nom est au féminin lorsqu’on peut placer les déterminants « une » ou « la » devant.',
        'bf-fe-def', F('Le nom féminin', 'on peut dire une', 'on peut dire la',
                       'une amie, la reine'),
        ('simple', 'Essaie avec une : une maison, ça va. Une village, ça ne va pas.'),
        ('visuel', 'Une amie, la chanteuse, une jument : ce sont des noms féminins.'),
        Q('Lequel de ces noms est au féminin ?', 'amie', 'chanteur', 'cheval'),
        V('Devant un nom féminin, on peut placer « une » ou « la ».', True),
        T('Un nom est au féminin quand on peut placer une ou {{1}} devant.', 'la'),
        Q('Quel déterminant va devant un nom féminin ?', 'une', 'un', 'le', n=3),
        V('« Un roi » est un nom féminin.', False, n=4, e='Non. Le féminin est une reine.')),

      N('relation',
        'On forme le féminin en ajoutant « e » muet à la fin du nom masculin. Exemple : un ami, '
        'une amie.',
        'bf-fe-e', F('On ajoute un e muet', 'un ami', 'une amie', vif=(1,)),
        ('simple', 'Le e ne s’entend pas, mais il s’écrit : ami, amie.'),
        ('visuel', 'Muet veut dire silencieux : ami et amie se prononcent pareil.'),
        Q('Quel est le féminin de « un ami » ?', 'une amie', 'une ami', 'une amis'),
        V('Le « e » qu’on ajoute pour le féminin est muet.', True),
        T('Un ami, une {{1}}.', 'amie'),
        Q('Que veut dire « e muet » ?', 'Un e qui ne s’entend pas', 'Un e avec un accent',
          'Un e qu’on n’écrit pas', n=3),
        V('Le féminin de « un ami » s’écrit « une ami ».', False, n=4,
          e='Non : une amie, avec un e.')),

      N('relation',
        'On forme le féminin en ajoutant euse ou trice à la fin, selon le nom masculin. '
        'Exemples : un chanteur, une chanteuse ; un acteur, une actrice.',
        'bf-fe-euse', P('euse ou trice', ('un chanteur', 'une chanteuse'),
                        ('un acteur', 'une actrice')),
        ('simple', 'Eur devient euse, teur devient souvent trice.'),
        ('visuel', 'Chant-eur, chant-euse. Ac-teur, ac-trice.'),
        Q('Quel est le féminin de « un chanteur » ?', 'une chanteuse', 'une chanteure',
          'une chantrice'),
        V('Le féminin de « un acteur » est « une actrice ».', True),
        T('Un chanteur, une {{1}}.', 'chanteuse'),
        A('Relie chaque masculin à son féminin.', ('un chanteur', 'une chanteuse'),
          ('un acteur', 'une actrice'), ('un ami', 'une amie')),
        V('Le féminin de « un acteur » est « une acteuse ».', False, n=4,
          e='Non : une actrice.')),

      N('relation',
        'On forme le féminin en doublant la consonne pour les noms terminés par n, t, l. '
        'Exemples : un chat, une chatte ; un patron, une patronne ; un criminel, une '
        'criminelle.',
        'bf-fe-double', P('On double la consonne', ('un chat', 'une chatte'),
                          ('un patron', 'une patronne'), ('un criminel', 'une criminelle')),
        ('simple', 'La dernière lettre s’écrit deux fois, puis on ajoute e.'),
        ('visuel', 'Cha-t, cha-tte. Patro-n, patro-nne. Crimine-l, crimine-lle.'),
        Q('Quel est le féminin de « un patron » ?', 'une patronne', 'une patrone',
          'une patronesse'),
        V('Le féminin de « un chat » est « une chatte ».', True),
        T('Un criminel, une {{1}}.', 'criminelle'),
        Q('Pour quelles lettres finales double-t-on la consonne ?', 'n, t, l', 'a, e, i',
          'r, s, x', n=3),
        V('Le féminin de « un patron » s’écrit « une patrone ».', False, n=4,
          e='Non : une patronne, avec deux n.')),

      N('relation',
        'D’autres noms restent invariables. Exemples : un élève, une élève ; un artiste, une '
        'artiste.',
        'bf-fe-invariable', P('Ils ne changent pas', ('un élève', 'une élève'),
                              ('un artiste', 'une artiste')),
        ('simple', 'Invariable veut dire qui ne change pas : seul le déterminant change.'),
        ('visuel', 'Un élève, une élève : le même mot, lettre pour lettre.'),
        Q('Quel est le féminin de « un élève » ?', 'une élève', 'une élèvesse', 'une élèveuse'),
        V('« Artiste » s’écrit pareil au masculin et au féminin.', True),
        T('Un artiste, une {{1}}.', 'artiste'),
        Q('Que veut dire « invariable » ?', 'Qui ne change pas', 'Qui est au pluriel',
          'Qui finit par e', n=3),
        V('Le féminin de « un élève » est « une élèvesse ».', False, n=4,
          e='Non. Élève est invariable : une élève.')),

      N('relation',
        'D’autres noms changent complètement de forme. Exemples : un cheval, une jument ; un '
        'roi, une reine ; un frère, une sœur.',
        'bf-fe-forme', P('Un autre mot', ('un cheval', 'une jument'), ('un roi', 'une reine'),
                         ('un frère', 'une sœur')),
        ('simple', 'Ces féminins ne se fabriquent pas : il faut les connaître.'),
        ('visuel', 'Frère et sœur n’ont pas une seule lettre à la même place.'),
        Q('Quel est le féminin de « un cheval » ?', 'une jument', 'une chevale',
          'une chevalle'),
        V('Le féminin de « un roi » est « une reine ».', True),
        T('Un frère, une {{1}}.', 'sœur'),
        A('Relie chaque masculin à son féminin.', ('un cheval', 'une jument'),
          ('un roi', 'une reine'), ('un frère', 'une sœur')),
        V('Le féminin de « un cheval » est « une chevale ».', False, n=4,
          e='Non : une jument.'),
        Q('Quel est le féminin de « un roi » ?', 'une reine', 'une roie', 'une roine', n=4)),
      ),
]
