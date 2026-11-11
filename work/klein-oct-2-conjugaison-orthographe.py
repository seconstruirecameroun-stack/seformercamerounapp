# -*- coding: utf-8 -*-
# Conjugaison, orthographe, syllabaire — cinq leçons.
# Chargé par lecons-klein-cahier-oct.py.
#
# Le pluriel des noms en au : le cahier donne trois exceptions qui prennent un
# s, et la photo ne permet d-en lire que deux — landau et sarrau, confirmées
# par l-exercice du 10 novembre. Aucune question ne porte sur la troisième.

FR = 'Français'
CONJ = 'Conjugaison'
ORTHO = 'Orthographe'
SYLL = 'Syllabaire'

LECONS = [
    # ------------------------------------------------------------ 21 octobre
    L(FR, 'Les temps simples du mode indicatif', CONJ, '2026-10-21',
      'Le mode indicatif a quatre temps simples : le présent, le futur simple, l’imparfait et '
      'le passé simple. Actuellement nous sommes en classe. Mes parents iront en ville demain. '
      'Hier, je faisais mes devoirs. Jadis David fut un grand roi.',
      'kcf-ts-couv', ['présent', 'futur', 'imparfait', 'passé simple'],

      N('liste',
        'Le mode indicatif a quatre temps simples : le présent, le futur simple, l’imparfait et '
        'le passé simple.',
        'kcf-ts-quatre', F('Quatre temps simples', 'le présent', 'le futur simple',
                           'l’imparfait', 'le passé simple'),
        ('simple', 'Quatre temps pour dire maintenant, demain, hier et il y a très longtemps.'),
        ('visuel', 'Compte-les sur tes doigts : présent, futur simple, imparfait, passé '
                   'simple.'),
        Q('Combien de temps simples a le mode indicatif ?', 'Quatre', 'Deux', 'Six'),
        V('L’imparfait est un temps simple de l’indicatif.', True),
        T('Les temps simples : le présent, le futur simple, l’imparfait et le passé {{1}}.',
          'simple'),
        Q('Lequel est un temps simple de l’indicatif ?', 'le futur simple', 'le village',
          'le pronom', n=3),
        V('Le mode indicatif a dix temps simples.', False, n=4, e='Non. Il en a quatre.')),

      N('relation',
        'Le présent : Actuellement nous sommes en classe. Le futur simple : Mes parents iront '
        'en ville demain.',
        'kcf-ts-present', P('Maintenant et demain', ('actuellement', 'le présent'),
                            ('demain', 'le futur simple')),
        ('simple', 'Le présent, c’est maintenant. Le futur, c’est ce qui n’est pas encore '
                   'arrivé.'),
        ('visuel', 'Cherche le petit mot : actuellement veut dire maintenant, demain annonce '
                   'le futur.'),
        Q('« Actuellement nous sommes en classe. » À quel temps est le verbe ?', 'Au présent',
          'Au futur simple', 'À l’imparfait'),
        V('« Mes parents iront en ville demain. » est au futur simple.', True),
        T('Mes parents iront en ville {{1}}.', 'demain'),
        Q('« Mes parents iront en ville demain. » À quel temps est le verbe ?',
          'Au futur simple', 'Au présent', 'Au passé simple', n=3),
        V('« Actuellement nous sommes en classe. » est au futur simple.', False, n=4,
          e='Non. Actuellement veut dire maintenant : c’est le présent.')),

      N('relation',
        'L’imparfait : Hier, je faisais mes devoirs. Le passé simple : Jadis David fut un grand '
        'roi.',
        'kcf-ts-passe', P('Hier et jadis', ('hier', 'l’imparfait'),
                          ('jadis', 'le passé simple')),
        ('simple', 'Les deux parlent du passé. Jadis veut dire il y a très longtemps.'),
        ('visuel', 'Hier, je faisais. Jadis, David fut.'),
        Q('« Hier, je faisais mes devoirs. » À quel temps est le verbe ?', 'À l’imparfait',
          'Au présent', 'Au futur simple'),
        V('« Jadis David fut un grand roi. » est au passé simple.', True),
        T('Hier, je {{1}} mes devoirs.', 'faisais'),
        A('Relie chaque phrase à son temps.', ('Nous sommes en classe.', 'présent'),
          ('Mes parents iront en ville.', 'futur simple'),
          ('Je faisais mes devoirs.', 'imparfait'), ('David fut un grand roi.', 'passé simple')),
        Q('« Jadis David fut un grand roi. » À quel temps est le verbe ?', 'Au passé simple',
          'Au futur simple', 'Au présent', n=4)),
      ),

    # ------------------------------------------------------------ 28 octobre
    L(FR, 'Être et avoir au présent de l’indicatif', CONJ, '2026-10-28',
      'Avoir au présent : j’ai, tu as, il ou elle a, nous avons, vous avez, ils ou elles ont. '
      'Être au présent : je suis, tu es, il ou elle est, nous sommes, vous êtes, ils ou elles '
      'sont.',
      'kcf-ea-couv', ['j’ai', 'je suis', 'ils ont', 'ils sont'],

      N('liste',
        'Avoir au présent : j’ai, tu as, il ou elle a, nous avons, vous avez, ils ou elles ont.',
        'kcf-ea-avoir', F('Avoir', 'j’ai, tu as', 'il a, elle a', 'nous avons, vous avez',
                          'ils ont, elles ont'),
        ('simple', 'Avoir, c’est posséder : elle a une belle robe.'),
        ('visuel', 'Les élèves ont des livres : ont, avec un o.'),
        Q('Complète avec avoir : « Elle … une belle robe. »', 'a', 'est', 'ont'),
        V('Avec nous, on dit « nous avons ».', True),
        T('Les élèves {{1}} des livres. (avoir)', 'ont'),
        T('Edouard et toi {{1}} les mêmes parents. (avoir)', 'avez', n=3,
          e='Edouard et toi, c’est vous : vous avez.'),
        Q('Complète avec avoir : « Tu … mal à la tête. »', 'as', 'a', 'es', n=4)),

      N('liste',
        'Être au présent : je suis, tu es, il ou elle est, nous sommes, vous êtes, ils ou elles '
        'sont.',
        'kcf-ea-etre', F('Être', 'je suis, tu es', 'il est, elle est',
                         'nous sommes, vous êtes', 'ils sont, elles sont'),
        ('simple', 'Être dit comment on est ou où on est : nous sommes en classe.'),
        ('visuel', 'Mes parents sont en ville : sont, avec un s.'),
        Q('Complète avec être : « Nous … en classe. »', 'sommes', 'avons', 'sont'),
        V('Avec vous, on dit « vous êtes ».', True),
        T('Mes parents {{1}} en ville. (être)', 'sont'),
        T('Mes frères et moi {{1}} au village. (être)', 'sommes', n=3,
          e='Mes frères et moi, c’est nous : nous sommes.'),
        A('Relie chaque forme à son verbe.', ('ils ont', 'avoir'), ('ils sont', 'être'),
          ('tu as', 'avoir aussi'), ('tu es', 'être aussi')),
        Q('Complète avec être : « Vous … contents. »', 'êtes', 'avez', 'sont', n=4),
        V('« Ils ont » est le verbe être.', False, n=4,
          e='Non. Ils ont, c’est avoir. Être : ils sont.')),
      ),

    # ------------------------------------------------------------ 22 octobre
    L(FR, 'Le pluriel des noms en au et en eau', ORTHO, '2026-10-22',
      'Les noms en au et en eau forment leur pluriel avec un x à la fin : un fléau, des '
      'fléaux ; un cadeau, des cadeaux ; le tuyau, les tuyaux. Sauf landau et sarrau, qui '
      'prennent un s au pluriel.',
      'kcf-au-couv', ['des cadeaux', 'des tuyaux', 'des landaus'],

      N('relation',
        'Les noms en au et en eau forment leur pluriel avec un x à la fin. Un fléau, des '
        'fléaux. Un cadeau, des cadeaux. Le tuyau, les tuyaux.',
        'kcf-au-regle', P('Un x à la fin', ('un fléau', 'des fléaux'),
                          ('un cadeau', 'des cadeaux'), ('le tuyau', 'les tuyaux')),
        ('simple', 'Au pluriel, pas de s : un x.'),
        ('visuel', 'Un cadeau, deux cadeaux. Regarde la dernière lettre.'),
        Q('Quel est le pluriel de « un cadeau » ?', 'des cadeaux', 'des cadeaus', 'des cadeau'),
        V('Au pluriel, « tuyau » s’écrit « tuyaux ».', True),
        T('Un fléau, des {{1}}.', 'fléaux'),
        T('Le noyau, les {{1}}.', 'noyaux', n=3),
        Q('Quelle lettre ajoute-t-on au pluriel des noms en au et en eau ?', 'x', 's', 'z',
          n=4)),

      N('relation',
        'Sauf landau et sarrau, qui prennent un s au pluriel : un landau, des landaus ; un '
        'sarrau, des sarraus.',
        'kcf-au-sauf', P('Sauf ces deux-là', ('un landau', 'des landaus'),
                         ('un sarrau', 'des sarraus')),
        ('simple', 'Deux noms ne suivent pas la règle : ils prennent un s.'),
        ('visuel', 'Un landau est une voiture de bébé. Un sarrau est une blouse de travail.'),
        Q('Quel est le pluriel de « un landau » ?', 'des landaus', 'des landaux', 'des landau'),
        V('Au pluriel, « sarrau » prend un s.', True),
        T('Un landau, des {{1}}.', 'landaus'),
        A('Relie chaque nom à son pluriel.', ('un cadeau', 'des cadeaux'),
          ('un landau', 'des landaus'), ('un tuyau', 'des tuyaux'),
          ('un sarrau', 'des sarraus')),
        V('Le pluriel de « landau » est « landaux ».', False, n=4,
          e='Non. Landau prend un s : des landaus.'),
        Q('Quel est le pluriel de « un sarrau » ?', 'des sarraus', 'des sarraux', 'des sarrau',
          n=4)),
      ),

    # ------------------------------------------------------------ 27 octobre
    L(FR, 'Le pluriel des noms en al et en ail', ORTHO, '2026-10-27',
      'Les noms en al forment leur pluriel en aux : un cheval, des chevaux. Sauf bal, '
      'carnaval, chacal, festival, régal, récital. Les noms en ail forment leur pluriel avec '
      's : un détail, des détails. Sauf bail, corail, vitrail, travail.',
      'kcf-al-couv', ['des chevaux', 'des bals', 'des détails'],

      N('relation',
        'Les noms en al forment leur pluriel en aux. Exemple : un cheval, des chevaux.',
        'kcf-al-aux', P('al devient aux', ('un cheval', 'des chevaux'),
                        ('un journal', 'des journaux')),
        ('simple', 'On enlève al et on met aux.'),
        ('visuel', 'Chev-al, chev-aux. Journ-al, journ-aux.'),
        Q('Quel est le pluriel de « un cheval » ?', 'des chevaux', 'des chevals', 'des cheval'),
        V('Le pluriel de « un journal » est « des journaux ».', True),
        T('Un cheval, des {{1}}.', 'chevaux'),
        T('Un journal, des {{1}}.', 'journaux', n=3),
        V('Le pluriel de « un cheval » est « des chevals ».', False, n=4,
          e='Non : des chevaux.')),

      N('liste',
        'Sauf bal, carnaval, chacal, festival, régal, récital, qui prennent un s. Exemple : un '
        'bal, des bals.',
        'kcf-al-sauf', F('Sauf ces six-là', 'bal, carnaval', 'chacal, festival',
                         'régal, récital', 'un bal, des bals', vif=(3,)),
        ('simple', 'Six noms en al gardent leur al et prennent seulement un s.'),
        ('visuel', 'Un festival, des festivals : rien ne change, sauf le s.'),
        Q('Quel est le pluriel de « un bal » ?', 'des bals', 'des baux', 'des bal'),
        V('Le pluriel de « un festival » est « des festivals ».', True),
        T('Un bal, des {{1}}.', 'bals'),
        Q('Lequel de ces noms prend un s au pluriel ?', 'carnaval', 'cheval', 'journal', n=3),
        V('Le pluriel de « un bal » est « des baux ».', False, n=4, e='Non : des bals.'),
        Q('Quel est le pluriel de « un festival » ?', 'des festivals', 'des festivaux',
          'des festival', n=4)),

      N('relation',
        'Les noms en ail forment leur pluriel avec s. Exemple : un détail, des détails.',
        'kcf-al-ail', F('ail prend un s', 'un détail', 'des détails', vif=(1,)),
        ('simple', 'Pour les noms en ail, on ajoute simplement un s.'),
        ('visuel', 'Détail, détails : une seule lettre en plus.'),
        Q('Quel est le pluriel de « un détail » ?', 'des détails', 'des détaux', 'des détail'),
        V('Les noms en ail forment leur pluriel avec s.', True),
        T('Un détail, des {{1}}.', 'détails'),
        Q('Quelle lettre ajoute-t-on au pluriel des noms en ail ?', 's', 'x', 'z', n=3),
        V('Le pluriel de « un détail » est « des détaux ».', False, n=4,
          e='Non : des détails.')),

      N('liste',
        'Sauf bail, corail, vitrail, travail, qui forment leur pluriel en aux. Exemple : un '
        'corail, des coraux.',
        'kcf-al-ailsauf', P('Sauf ces quatre-là', ('un corail', 'des coraux'),
                            ('un travail', 'des travaux'), ('un vitrail', 'des vitraux')),
        ('simple', 'Quatre noms en ail font comme les noms en al : ils prennent aux.'),
        ('visuel', 'Trav-ail, trav-aux. Vitr-ail, vitr-aux.'),
        Q('Quel est le pluriel de « un corail » ?', 'des coraux', 'des corails', 'des corail'),
        V('Le pluriel de « un travail » est « des travaux ».', True),
        T('Un vitrail, des {{1}}.', 'vitraux'),
        A('Relie chaque nom à son pluriel.', ('un cheval', 'des chevaux'),
          ('un bal', 'des bals'), ('un détail', 'des détails'), ('un travail', 'des travaux')),
        V('Le pluriel de « un travail » est « des travails ».', False, n=4,
          e='Non : des travaux.'),
        Q('Quel est le pluriel de « un vitrail » ?', 'des vitraux', 'des vitrails',
          'des vitrail', n=4)),
      ),

    # ------------------------------------------------------------ 14 octobre
    L(FR, 'Les syllabes ga, go, gi, gu', SYLL, '2026-10-14',
      'On classe les mots selon leur syllabe. Avec ga : garnir, galop, gazon, gamin. Avec go : '
      'gorgée, gomme. Avec gi : girafon, girouette, gîte, ogive. Avec gu : figure, légume, '
      'lagune.',
      'kcf-sy-couv', ['ga', 'go', 'gi', 'gu'],

      N('liste',
        'Avec la syllabe ga : garnir, galop, gazon, gamin. Avec la syllabe go : gorgée, gomme.',
        'kcf-sy-gago', P('ga et go', ('ga', 'galop, gazon'), ('ga', 'garnir, gamin'),
                         ('go', 'gorgée, gomme')),
        ('simple', 'Cherche la syllabe dans le mot : ga-lop, go-mme.'),
        ('visuel', 'Dans cigale aussi il y a ga : ci-ga-le.'),
        Q('Quel mot contient la syllabe ga ?', 'gazon', 'gomme', 'légume'),
        V('Le mot « gomme » contient la syllabe go.', True),
        T('Le mot « galop » commence par la syllabe {{1}}.', 'ga'),
        Q('Quel mot contient la syllabe go ?', 'gorgée', 'gamin', 'girafon', n=3),
        V('Le mot « gamin » contient la syllabe go.', False, n=4, e='Non : ga-min.')),

      N('liste',
        'Avec la syllabe gi : girafon, girouette, gîte, ogive. Avec la syllabe gu : figure, '
        'légume, lagune.',
        'kcf-sy-gigu', P('gi et gu', ('gi', 'girafon, gîte'), ('gi', 'girouette, ogive'),
                         ('gu', 'figure, légume')),
        ('simple', 'Cherche la syllabe dans le mot : gi-rafon, lé-gu-me.'),
        ('visuel', 'La syllabe n’est pas toujours au début : fi-gu-re, o-gi-ve.'),
        Q('Quel mot contient la syllabe gu ?', 'légume', 'gazon', 'girafon'),
        V('Le mot « girouette » contient la syllabe gi.', True),
        T('Le mot « figure » contient la syllabe {{1}}.', 'gu'),
        A('Range chaque mot avec sa syllabe.', ('galop', 'ga'), ('gomme', 'go'),
          ('girafon', 'gi'), ('lagune', 'gu')),
        Q('Quel mot contient la syllabe gi ?', 'ogive', 'lagune', 'gorgée', n=4),
        V('Le mot « lagune » contient la syllabe gi.', False, n=4, e='Non : la-gu-ne.')),
      ),
]
