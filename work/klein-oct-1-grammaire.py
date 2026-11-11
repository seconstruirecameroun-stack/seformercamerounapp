# -*- coding: utf-8 -*-
# Grammaire — six leçons. Chargé par lecons-klein-cahier-oct.py.
#
# Deux confusions reviennent dans les exercices corrigés du cahier, et les
# questions y reviennent aussi : le TYPE d-une phrase (déclarative,
# interrogative, exclamative, impérative) n-est pas sa FORME (affirmative,
# négative) ; et mettre une phrase à la forme négative ne se fait pas toujours
# avec « pas » — toujours devient ne… jamais, encore devient ne… plus.

FR = 'Français'
GRAM = 'Grammaire'

LECONS = [
    # ------------------------------------------------------------ 12 octobre
    L(FR, 'Le verbe', GRAM, '2026-10-12',
      'Le verbe est un mot qui exprime l’action menée, ou l’état d’une personne, d’un animal '
      'ou d’une chose. Pour l’identifier dans une phrase, je pose la question « Que fait ? » '
      'ou « Que font ? ».',
      'kcf-ve-couv', ['l’action', 'l’état', 'que fait ?'],

      N('definition',
        'Le verbe est un mot qui exprime l’action menée, ou l’état d’une personne, d’un animal '
        'ou d’une chose.',
        'kcf-ve-def', F('Le verbe', 'il dit l’action', 'ou il dit l’état', 'd’une personne',
                        'd’un animal, d’une chose'),
        ('simple', 'Le verbe dit ce qu’on fait : courir, manger, aller.'),
        ('visuel', 'Les villageois vont au champ : le mot qui dit ce qu’ils font, c’est vont.'),
        Q('Que dit le verbe ?', 'L’action ou l’état', 'Le nom d’une ville',
          'La couleur d’un objet'),
        V('Le verbe est un mot qui exprime l’action.', True),
        T('Le {{1}} est un mot qui exprime l’action ou l’état.', 'verbe'),
        Q('Lequel de ces mots est un verbe ?', 'manger', 'village', 'petit', n=3),
        V('« Village » est un verbe.', False, n=4, e='Non. C’est un nom.')),

      N('definition',
        'Pour identifier le verbe dans une phrase, je pose la question « Que fait ? » ou « Que '
        'font ? ». Les villageois vont au champ. Que font les villageois ? Ils vont.',
        'kcf-ve-question', F('Je pose la question', 'Que fait ?', 'Que font ?',
                             'Les villageois vont au champ.', 'Ils vont : le verbe',
                             vif=(4,)),
        ('simple', 'La réponse à « Que font-ils ? » te donne le verbe.'),
        ('pas_a_pas', 'Papa conduit sa voiture. Que fait papa ? Il conduit. Le verbe est '
                      'conduit.'),
        Q('Quelle question pose-t-on pour trouver le verbe ?', 'Que fait ?', 'Où est-ce ?',
          'Combien ?'),
        V('Dans « Les villageois vont au champ », le verbe est « vont ».', True),
        T('Les villageois vont au champ. Le verbe est {{1}}.', 'vont'),
        Q('Dans « Papa conduit sa voiture », quel est le verbe ?', 'conduit', 'papa',
          'voiture', n=3),
        Q('Dans « Les femmes récoltent les ignames », quel est le verbe ?', 'récoltent',
          'femmes', 'ignames', n=4)),
      ),

    # ------------------------------------------------------------ 19 octobre
    L(FR, 'Les signes de ponctuation', GRAM, '2026-10-19',
      'Les signes de ponctuation sont : le point, le point-virgule, la virgule, les deux '
      'points, les points de suspension, le point d’interrogation, le point d’exclamation, le '
      'tiret, les guillemets et les parenthèses.',
      'kcf-po-couv', ['le point', 'la virgule', 'le tiret'],

      N('liste',
        'Le point ( . ), la virgule ( , ), le point-virgule ( ; ) et les deux points ( : ) sont '
        'des signes de ponctuation.',
        'kcf-po-points', S('Quatre signes', ('.', 'le point'), (',', 'la virgule'),
                           (';', 'le point-virgule'), (':', 'les deux points')),
        ('simple', 'Le point finit la phrase. La virgule fait une petite pause.'),
        ('visuel', 'Le point-virgule, c’est un point posé sur une virgule.'),
        Q('Comment s’appelle ce signe : « , » ?', 'La virgule', 'Le point', 'Le tiret'),
        V('Ce signe « . » s’appelle le point.', True),
        T('Ce signe « ; » s’appelle le point-{{1}}.', 'virgule'),
        A('Relie chaque signe à son nom.', ('.', 'le point'), (',', 'la virgule'),
          (':', 'les deux points')),
        V('Ce signe « : » s’appelle la virgule.', False, n=4,
          e='Non. Ce sont les deux points.')),

      N('liste',
        'Les points de suspension ( … ), le point d’interrogation ( ? ) et le point '
        'd’exclamation ( ! ) sont des signes de ponctuation.',
        'kcf-po-question', S('Trois signes', ('…', 'suspension'), ('?', 'interrogation'),
                             ('!', 'exclamation')),
        ('simple', 'Le « ? » finit une question. Le « ! » finit une phrase qui s’exclame.'),
        ('visuel', 'Que fait papa ? Quelle jolie robe !'),
        Q('Comment s’appelle ce signe : « ? » ?', 'Le point d’interrogation',
          'Le point d’exclamation', 'Les points de suspension'),
        V('Ce signe « ! » s’appelle le point d’exclamation.', True),
        T('Ce signe « ? » s’appelle le point d’{{1}}.', 'interrogation'),
        A('Relie chaque signe à son nom.', ('?', 'le point d’interrogation'),
          ('!', 'le point d’exclamation'), ('…', 'les points de suspension')),
        Q('Quel signe termine la phrase « Que fait papa » ?', 'Le point d’interrogation',
          'Le point d’exclamation', 'La virgule', n=4)),

      N('liste',
        'Le tiret ( – ), les guillemets ( « » ) et les parenthèses ( ) sont des signes de '
        'ponctuation.',
        'kcf-po-tiret', F('Trois signes encore', 'le tiret', 'les guillemets',
                          'les parenthèses'),
        ('simple', 'Les guillemets et les parenthèses vont toujours par deux : on ouvre, puis '
                   'on ferme.'),
        ('visuel', 'Le lièvre cria : « Tortue, tu es trop lente ! » Les guillemets entourent ce '
                   'qu’il dit.'),
        Q('Quels signes entourent les paroles d’un personnage ?', 'Les guillemets',
          'Les virgules', 'Les points'),
        V('Le tiret est un signe de ponctuation.', True),
        T('Ces signes « ( ) » s’appellent les {{1}}.', 'parenthèses'),
        Q('Lequel n’est pas un signe de ponctuation ?', 'la lettre a', 'le tiret',
          'les guillemets', n=3),
        V('Les guillemets vont par deux.', True, n=4)),
      ),

    # ------------------------------------------------------------ 22 octobre
    L(FR, 'Les types de phrases : déclarative et interrogative', GRAM, '2026-10-22',
      'La phrase déclarative sert à donner une information et se termine par un point. La '
      'phrase interrogative sert à poser une question et se termine par un point '
      'd’interrogation.',
      'kcf-t1-couv', ['déclarative', 'interrogative'],

      N('definition',
        'La phrase déclarative sert à donner une information et se termine par un point. '
        'Exemple : Papa conduit sa voiture.',
        'kcf-t1-declarative', F('La phrase déclarative', 'elle donne une information',
                                'elle finit par un point', 'Papa conduit sa voiture.',
                                vif=(2,)),
        ('simple', 'Elle raconte, elle dit quelque chose. À la fin : un point.'),
        ('visuel', 'Les femmes récoltent les ignames. On apprend quelque chose : c’est une '
                   'phrase déclarative.'),
        Q('À quoi sert la phrase déclarative ?', 'À donner une information',
          'À poser une question', 'À donner un ordre'),
        V('La phrase déclarative se termine par un point.', True),
        T('La phrase {{1}} sert à donner une information.', 'déclarative'),
        Q('« Les femmes récoltent les ignames. » Quel est le type de cette phrase ?',
          'Déclarative', 'Impérative', 'Interrogative', n=3),
        Q('« Albert et Ali sont au manège. » Quel est le type de cette phrase ?',
          'Déclarative', 'Exclamative', 'Interrogative', n=4),
        V('« Les femmes récoltent les ignames. » est une phrase impérative.', False, n=4,
          e='Non. Elle donne une information : elle est déclarative.')),

      N('definition',
        'La phrase interrogative sert à poser une question et se termine par un point '
        'd’interrogation. Exemple : Que fait papa ?',
        'kcf-t1-interrogative', F('La phrase interrogative', 'elle pose une question',
                                  'elle finit par ?', 'Que fait papa ?', vif=(2,)),
        ('simple', 'Elle demande. À la fin : un point d’interrogation.'),
        ('visuel', 'Est-ce que tu as soif ? Regarde la fin de la phrase.'),
        Q('À quoi sert la phrase interrogative ?', 'À poser une question',
          'À donner une information', 'À dire sa joie'),
        V('La phrase interrogative se termine par un point d’interrogation.', True),
        T('La phrase {{1}} sert à poser une question.', 'interrogative'),
        Q('« Est-ce que tu as soif ? » Quel est le type de cette phrase ?', 'Interrogative',
          'Déclarative', 'Impérative', n=3),
        V('« Que fait papa ? » est une phrase déclarative.', False, n=4,
          e='Non. Elle pose une question : elle est interrogative.')),
      ),

    # ------------------------------------------------------------ 26 octobre
    L(FR, 'Les types de phrases : exclamative et impérative', GRAM, '2026-10-26',
      'La phrase exclamative sert à exprimer des sentiments et se termine par un point '
      'd’exclamation. La phrase impérative ou injonctive sert à donner un conseil ou un '
      'ordre.',
      'kcf-t2-couv', ['exclamative', 'impérative'],

      N('definition',
        'La phrase exclamative sert à exprimer des sentiments : joie, tristesse, peur, '
        'surprise. Elle se termine par un point d’exclamation. Exemple : Quelle jolie robe !',
        'kcf-t2-exclamative', F('La phrase exclamative', 'joie, tristesse', 'peur, surprise',
                                'elle finit par !', 'Quelle jolie robe !', vif=(3,)),
        ('simple', 'Elle dit ce qu’on ressent. À la fin : un point d’exclamation.'),
        ('visuel', 'Que c’est beau ! On entend la joie.'),
        Q('À quoi sert la phrase exclamative ?', 'À exprimer des sentiments',
          'À poser une question', 'À donner un ordre'),
        V('La phrase exclamative se termine par un point d’exclamation.', True),
        T('La phrase {{1}} sert à exprimer des sentiments.', 'exclamative'),
        Q('« Que c’est beau ! » Quel est le type de cette phrase ?', 'Exclamative',
          'Déclarative', 'Interrogative', n=3),
        Q('« Quelle belle école ! » Quel est le type de cette phrase ?', 'Exclamative',
          'Impérative', 'Interrogative', n=4)),

      N('definition',
        'La phrase impérative ou injonctive sert à donner un conseil, comme « Lave les mains '
        'avant le repas. », ou un ordre, comme « Sors ! ».',
        'kcf-t2-imperative', P('La phrase impérative', ('un conseil', 'Lave les mains.'),
                               ('un ordre', 'Sors !')),
        ('simple', 'Elle dit à quelqu’un de faire quelque chose.'),
        ('visuel', 'Mets-toi au travail. Fais bien les devoirs. Ce sont des phrases '
                   'impératives.'),
        Q('À quoi sert la phrase impérative ?', 'À donner un conseil ou un ordre',
          'À poser une question', 'À raconter une histoire'),
        V('« Sors ! » est une phrase impérative.', True),
        T('La phrase impérative s’appelle aussi la phrase {{1}}.', 'injonctive'),
        A('Relie chaque phrase à son type.', ('Papa conduit sa voiture.', 'déclarative'),
          ('Que fait papa ?', 'interrogative'), ('Quelle jolie robe !', 'exclamative'),
          ('Mets-toi au travail.', 'impérative')),
        Q('« Fais bien les devoirs. » Quel est le type de cette phrase ?', 'Impérative',
          'Déclarative', 'Exclamative', n=4),
        V('« Lave les mains avant le repas. » est une phrase interrogative.', False, n=4,
          e='Non. Elle donne un conseil : elle est impérative.')),
      ),

    # ------------------------------------------------------------ 26 octobre
    L(FR, 'Les formes de phrases', GRAM, '2026-10-26',
      'La phrase peut être à la forme affirmative, comme « Cette ville est belle. », ou à la '
      'forme négative, comme « Cette ville n’est pas belle. ». Les expressions de la négation '
      'sont : ne… jamais, ne… plus, ne… point, ne… guère.',
      'kcf-fo-couv', ['affirmative', 'négative'],

      N('relation',
        'La phrase peut être à la forme affirmative. Exemple : Cette ville est belle. Elle '
        'peut être à la forme négative. Exemple : Cette ville n’est pas belle.',
        'kcf-fo-deux', P('Deux formes', ('affirmative', 'est belle'),
                         ('négative', 'n’est pas belle')),
        ('simple', 'La forme affirmative dit oui. La forme négative dit non.'),
        ('pas_a_pas', 'Anita aime la lecture. Mets n’ avant aime et pas après : Anita n’aime '
                      'pas la lecture.'),
        Q('« Cette ville n’est pas belle. » Quelle est la forme de cette phrase ?', 'Négative',
          'Affirmative', 'Interrogative'),
        V('« Cette ville est belle. » est à la forme affirmative.', True),
        T('Forme négative : Anita n’aime {{1}} la lecture.', 'pas'),
        Q('« Les femmes récoltent les ignames. » Quelle est la forme de cette phrase ?',
          'Affirmative', 'Négative', 'Déclarative', n=3),
        Q('Mets à la forme négative : « Les femmes récoltent les ignames. »',
          'Les femmes ne récoltent pas les ignames.', 'Les femmes récoltent-elles les ignames ?',
          'Les femmes récoltent beaucoup d’ignames.', n=4),
        V('« Affirmative » est un type de phrase.', False, n=4,
          e='Non. Affirmative et négative sont des formes. Déclarative est un type.')),

      N('liste',
        'Les expressions de la négation sont : ne… jamais, ne… plus, ne… point, ne… guère.',
        'kcf-fo-negation', F('La négation', 'ne… jamais', 'ne… plus', 'ne… point',
                             'ne… guère'),
        ('simple', 'La négation a toujours deux morceaux : ne, et un autre mot.'),
        ('visuel', 'Toujours devient ne… jamais. Encore devient ne… plus.'),
        Q('Laquelle est une expression de la négation ?', 'ne… jamais', 'est-ce que',
          'il était une fois'),
        V('« ne… plus » est une expression de la négation.', True),
        T('Rémi va toujours au village. Forme négative : Rémi ne va {{1}} au village.',
          'jamais', e='Toujours devient ne… jamais : Rémi ne va jamais au village.'),
        T('Je suis encore venu. Forme négative : je ne suis {{1}} venu.', 'plus', n=3,
          e='Encore devient ne… plus : je ne suis plus venu.'),
        Q('Mets à la forme négative : « As-tu mangé ? »', 'N’as-tu pas mangé ?',
          'As-tu pas mangé ?', 'Tu as mangé ?', n=4),
        Q('Mets à la forme négative : « Rémi va toujours au village. »',
          'Rémi ne va jamais au village.', 'Rémi va au village.', 'Rémi va souvent au village.',
          n=4)),
      ),

    # ------------------------------------------------------------ 29 octobre
    L(FR, 'Le groupe nominal sujet', GRAM, '2026-10-29',
      'Le groupe nominal sujet, ou G.N.S, c’est le groupe de mots autour du nom qui fait '
      'l’action du verbe. Il est constitué d’un déterminant, d’un adjectif qualificatif et '
      'd’un nom. Pour le trouver, on pose la question « Qui est-ce qui ? » avant le verbe.',
      'kcf-gs-couv', ['déterminant', 'adjectif', 'nom'],

      N('definition',
        'Le G.N.S, c’est l’ensemble ou groupe de mots autour du nom qui fait l’action du '
        'verbe.',
        'kcf-gs-def', F('Le G.N.S', 'groupe nominal sujet', 'les mots autour du nom',
                        'qui fait l’action du verbe'),
        ('simple', 'C’est le groupe de mots qui dit qui fait l’action.'),
        ('visuel', 'Ce petit garçon est malade. Le G.N.S est « ce petit garçon ».'),
        Q('Que veut dire G.N.S ?', 'Groupe nominal sujet', 'Grand nom simple',
          'Groupe du nom sans verbe'),
        V('Le G.N.S est le groupe de mots autour du nom qui fait l’action.', True),
        T('G.N.S veut dire groupe nominal {{1}}.', 'sujet'),
        Q('Dans « Ce petit garçon est malade », quel est le G.N.S ?', 'Ce petit garçon',
          'est malade', 'malade', n=3),
        V('Dans « Ce petit garçon est malade », le G.N.S est « est malade ».', False, n=4,
          e='Non. Le G.N.S est « ce petit garçon ».')),

      N('liste',
        'Le G.N.S est constitué d’un déterminant, comme le, la, un, une, ce, mon, son ; d’un '
        'adjectif qualificatif, comme petit, grand, vieux ; et d’un nom.',
        'kcf-gs-constituants', P('Notre jolie école', ('notre', 'déterminant'),
                                 ('jolie', 'adjectif'), ('école', 'nom')),
        ('simple', 'Trois sortes de mots : le petit mot du début, le mot qui décrit, et le '
                   'nom.'),
        ('visuel', 'Notre jolie école est grande : notre, jolie, école.'),
        Q('Dans « Notre jolie école », quel mot est le déterminant ?', 'notre', 'jolie',
          'école'),
        V('« Petit » est un adjectif qualificatif.', True),
        T('Dans « Notre jolie école », le nom est {{1}}.', 'école'),
        A('Relie chaque mot à ce qu’il est.', ('notre', 'déterminant'),
          ('jolie', 'adjectif qualificatif'), ('école', 'nom')),
        Q('Dans « Ce petit garçon », quel mot est l’adjectif qualificatif ?', 'petit', 'ce',
          'garçon', n=4),
        V('« Mon » est un déterminant.', True, n=4)),

      N('definition',
        'Pour trouver le G.N.S, on pose la question « Qui est-ce qui ? » avant le verbe. Ce '
        'petit garçon est malade. Qui est-ce qui est malade ? Ce petit garçon.',
        'kcf-gs-question', F('Je pose la question', 'Qui est-ce qui ?',
                             'Qui est-ce qui est malade ?', 'Ce petit garçon', vif=(2,)),
        ('simple', 'La réponse à « Qui est-ce qui ? » est le G.N.S.'),
        ('pas_a_pas', 'Notre jolie école est grande. Qui est-ce qui est grande ? Notre jolie '
                      'école.'),
        Q('Quelle question pose-t-on pour trouver le G.N.S ?', 'Qui est-ce qui ?', 'Que fait ?',
          'Combien ?'),
        V('On pose la question « Qui est-ce qui ? » avant le verbe.', True),
        T('Pour trouver le G.N.S, on demande : {{1}} est-ce qui ?', 'qui'),
        Q('« Notre jolie école est grande. » Qui est-ce qui est grande ?', 'Notre jolie école',
          'est grande', 'grande', n=3),
        V('Pour trouver le G.N.S, on pose la question « Que fait ? ».', False, n=4,
          e='Non. « Que fait ? » trouve le verbe. « Qui est-ce qui ? » trouve le G.N.S.')),
      ),
]
