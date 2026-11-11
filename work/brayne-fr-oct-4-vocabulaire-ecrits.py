# -*- coding: utf-8 -*-
# Vocabulaire, production d-écrits, lecture — sept leçons.
# Chargé par lecons-brayne-francais-oct.py.
#
# Les couples de mots sont ceux du cahier et de ses exercices corrigés :
# métropole et ville, campagnard et villageois, cœur et chœur, compte et
# conte.
#
# La page de lecture du 14 octobre porte un titre que la photo ne permet pas
# de lire en entier (« Une famille… », page 28 du manuel). La leçon s-appelle
# donc par sa page, et ne prétend pas connaître le titre du texte.

FR = 'Français'
VOC = 'Vocabulaire'
PROD = 'Production d’écrits'
LECT = 'Lecture'

LECONS = [
    # ------------------------------------------------------------ 13 octobre
    L(FR, 'Les synonymes, les antonymes, les homonymes', VOC, '2026-10-13',
      'Les synonymes sont des mots qui ont le même sens mais s’écrivent différemment. Les '
      'antonymes sont des mots de sens contraire ou opposé. Les homonymes sont des mots ayant '
      'la même prononciation mais de sens différent.',
      'bf-sy-couv', ['même sens', 'sens contraire', 'même son'],

      N('definition',
        'Les synonymes sont des mots qui ont le même sens mais s’écrivent différemment. '
        'Exemples : village, campagne ; balade, promenade.',
        'bf-sy-synonymes', P('Le même sens', ('village', 'campagne'), ('balade', 'promenade'),
                             ('métropole', 'ville'), ('véhicule', 'voiture')),
        ('simple', 'Deux mots différents pour dire la même chose.'),
        ('visuel', 'Une métropole, c’est une grande ville. Un campagnard, c’est un '
                   'villageois.'),
        Q('Quel est le synonyme de « métropole » ?', 'ville', 'train', 'village'),
        V('« Balade » et « promenade » sont des synonymes.', True),
        T('Un synonyme de véhicule : une {{1}}.', 'voiture'),
        A('Relie chaque mot à son synonyme.', ('métropole', 'ville'),
          ('conducteur', 'chauffeur'), ('véhicule', 'voiture'), ('campagnard', 'villageois')),
        Q('Quel est le synonyme de « campagnard » ?', 'villageois', 'citadin', 'voyageur', n=4),
        V('« Métropole » et « train » sont des synonymes.', False, n=4,
          e='Non. Une métropole est une grande ville.')),

      N('definition',
        'Les antonymes sont des mots de sens contraire ou opposé. Exemples : bruit et silence, '
        'prudent et imprudent.',
        'bf-sy-antonymes', P('Le sens contraire', ('bruit', 'silence'),
                             ('prudent', 'imprudent'), ('gentil', 'méchant'),
                             ('triste', 'heureux')),
        ('simple', 'Deux mots qui disent le contraire l’un de l’autre.'),
        ('visuel', 'Souvent on fabrique l’antonyme avec im : poli, impoli ; prudent, '
                   'imprudent.'),
        Q('Quel est l’antonyme de « gentil » ?', 'méchant', 'aimable', 'poli'),
        V('« Bruit » et « silence » sont des antonymes.', True),
        T('L’antonyme de poli : {{1}}.', 'impoli'),
        A('Relie chaque mot à son antonyme.', ('imprudent', 'prudent'), ('gentil', 'méchant'),
          ('triste', 'heureux'), ('poli', 'impoli')),
        Q('Quel est l’antonyme de « triste » ?', 'heureux', 'malheureux', 'fatigué', n=4)),

      N('definition',
        'Les homonymes sont des mots ayant la même prononciation mais de sens différent. '
        'Exemples : père, paire ; champ, chant.',
        'bf-sy-homonymes', P('Le même son', ('père', 'paire'), ('champ', 'chant'),
                             ('cœur', 'chœur'), ('compte', 'conte')),
        ('simple', 'On les entend pareil, mais ils ne veulent pas dire la même chose.'),
        ('visuel', 'Le cœur bat dans la poitrine. Le chœur, c’est un groupe qui chante.'),
        Q('Quel est l’homonyme de « cœur » ?', 'chœur', 'corps', 'cour'),
        Q('Quel est l’homonyme de « compte » ?', 'conte', 'compter', 'calcul'),
        V('« Champ » et « chant » sont des homonymes.', True),
        T('L’homonyme de vers, comme la couleur de l’herbe : {{1}}.', 'vert'),
        A('Relie chaque mot à son homonyme.', ('plaine', 'pleine'), ('cœur', 'chœur'),
          ('compte', 'conte'), ('vers', 'vert')),
        V('Deux homonymes ont le même sens.', False, n=4,
          e='Non. Ils ont le même son, mais un sens différent.'),
        Q('« Père » et « paire » sont des…', 'homonymes', 'synonymes', 'antonymes', n=4)),
      ),

    # ------------------------------------------------------------ 21 octobre
    L(FR, 'Le champ lexical de la ville et du village', VOC, '2026-10-21',
      'Les mots du champ lexical de la ville se répartissent en habitations, voies de '
      'circulation, transports et services. Ceux du village se répartissent en habitations, '
      'voies de circulation et activités.',
      'bf-cl-couv', ['immeuble', 'boulevard', 'hutte', 'sentier'],

      N('liste',
        'En ville, les habitations sont : immeuble, appartement, hôtel. Les voies de circulation '
        'sont : rue, avenue, boulevard, trottoir, tunnel, pont, carrefour.',
        'bf-cl-ville1', F('La ville', 'immeuble, appartement, hôtel', 'rue, avenue, boulevard',
                          'trottoir, tunnel', 'pont, carrefour'),
        ('simple', 'Une habitation, c’est là où on loge. Une voie, c’est par où on passe.'),
        ('visuel', 'Le boulevard est une très large rue. Le carrefour est l’endroit où les '
                   'rues se croisent.'),
        Q('Lequel est une habitation de la ville ?', 'immeuble', 'boulevard', 'taxi'),
        V('Le boulevard est une voie de circulation de la ville.', True),
        T('Les rues se croisent au {{1}}.', 'carrefour'),
        Q('Lequel est une voie de circulation de la ville ?', 'avenue', 'appartement',
          'hôpital', n=3),
        V('L’hôtel est une voie de circulation.', False, n=4, e='Non. C’est une habitation.')),

      N('liste',
        'En ville, les transports sont : moto, bus, taxi, train. Les services sont : hôpital, '
        'banque, supermarché, cinéma, théâtre, université, restaurant.',
        'bf-cl-ville2', F('La ville', 'moto, bus, taxi, train', 'hôpital, banque',
                          'supermarché, cinéma', 'théâtre, université'),
        ('simple', 'Un transport vous emmène. Un service vous soigne, vous vend, vous '
                   'instruit.'),
        ('visuel', 'À l’hôpital on soigne, à la banque on garde l’argent, à l’université on '
                   'étudie.'),
        Q('Lequel est un transport de la ville ?', 'taxi', 'banque', 'trottoir'),
        V('L’hôpital est un service de la ville.', True),
        T('On garde son argent à la {{1}}.', 'banque'),
        A('Range chaque mot de la ville.', ('immeuble', 'habitation'), ('avenue', 'voie'),
          ('bus', 'transport'), ('cinéma', 'service')),
        V('Le supermarché est un transport.', False, n=4, e='Non. C’est un service.')),

      N('liste',
        'Au village, les habitations sont : maison, ferme, hutte, case. Les voies de '
        'circulation sont : chemin, sentier, champs, piste, forêt, colline, rivière, verger.',
        'bf-cl-village1', F('Le village', 'maison, ferme, hutte, case', 'chemin, sentier, piste',
                            'champs, forêt, colline', 'rivière, verger'),
        ('simple', 'Au village on ne trouve pas d’immeuble : on trouve des cases et des '
                   'huttes.'),
        ('visuel', 'Le sentier est un petit chemin étroit. La piste est une route de terre.'),
        Q('Lequel est une habitation du village ?', 'hutte', 'immeuble', 'hôtel'),
        V('Le sentier appartient au champ lexical du village.', True),
        T('Un petit chemin étroit s’appelle un {{1}}.', 'sentier'),
        Q('Lequel appartient au champ lexical du village ?', 'case', 'boulevard', 'tunnel',
          n=3),
        V('L’immeuble appartient au champ lexical du village.', False, n=4,
          e='Non. C’est une habitation de la ville.')),

      N('liste',
        'Au village, les activités sont : agriculture, pêche, élevage, artisanat, cueillette, '
        'ramassage.',
        'bf-cl-village2', F('Les activités du village', 'agriculture, pêche', 'élevage',
                            'artisanat', 'cueillette, ramassage'),
        ('simple', 'Ce sont les travaux qui font vivre le village.'),
        ('visuel', 'L’élevage, c’est élever des bêtes. La cueillette, c’est cueillir les '
                   'fruits.'),
        Q('Lequel est une activité du village ?', 'élevage', 'cinéma', 'université'),
        V('La pêche est une activité du village.', True),
        T('Cultiver la terre, c’est l’{{1}}.', 'agriculture'),
        A('Range chaque mot dans son champ lexical.', ('boulevard', 'la ville'),
          ('sentier', 'le village'), ('supermarché', 'la ville aussi'),
          ('cueillette', 'le village aussi')),
        Q('Lequel n’est pas une activité du village ?', 'théâtre', 'artisanat', 'ramassage',
          n=4),
        V('L’artisanat est une activité du village.', True, n=4)),
      ),

    # ------------------------------------------------------------ 20 octobre
    L(FR, 'Le texte narratif', PROD, '2026-10-20',
      'Le texte narratif est un texte qui raconte une histoire réelle ou imaginaire en suivant '
      'une suite d’évènements. Il comporte trois parties essentielles : l’introduction, le '
      'développement et la conclusion. Ses types sont le récit, le conte, la fable, '
      'l’histoire et la légende.',
      'bf-tn-couv', ['introduction', 'développement', 'conclusion'],

      N('definition',
        'Le texte narratif est un texte qui raconte une histoire réelle ou imaginaire en '
        'suivant une suite d’évènements.',
        'bf-tn-def', F('Le texte narratif', 'il raconte une histoire', 'réelle ou imaginaire',
                       'une suite d’évènements'),
        ('simple', 'Narrer, c’est raconter. Un texte narratif raconte ce qui s’est passé.'),
        ('visuel', 'D’abord, ensuite, puis, enfin : les évènements se suivent.'),
        Q('Que fait un texte narratif ?', 'Il raconte une histoire', 'Il donne une recette',
          'Il décrit un objet'),
        V('Un texte narratif peut raconter une histoire imaginaire.', True),
        T('Le texte {{1}} raconte une histoire réelle ou imaginaire.', 'narratif'),
        Q('Dans un texte narratif, l’histoire suit…', 'une suite d’évènements',
          'l’ordre alphabétique', 'une liste de mots', n=3),
        V('Un texte narratif ne raconte que des histoires vraies.', False, n=4,
          e='Non. L’histoire peut être réelle ou imaginaire.')),

      N('liste',
        'Il comporte trois parties : l’introduction, avec le temps, le lieu et les '
        'personnages ; le développement, où on raconte l’histoire ; la conclusion, la fin de '
        'l’histoire.',
        'bf-tn-parties', P('Trois parties', ('l’introduction', 'temps, lieu'),
                           ('le développement', 'toute l’histoire'),
                           ('la conclusion', 'la fin, la chute')),
        ('simple', 'Un début qui présente, un milieu qui raconte, une fin qui termine.'),
        ('visuel', 'La conclusion peut être heureuse ou malheureuse.'),
        Q('Combien de parties essentielles comporte un texte narratif ?', 'Trois', 'Deux',
          'Cinq'),
        V('Dans l’introduction, on retrouve le temps, le lieu et les personnages.', True),
        T('Dans le {{1}}, on raconte intégralement l’histoire.', 'développement'),
        C('Range les trois parties du texte narratif dans l’ordre.', 'l’introduction',
          'le développement', 'la conclusion'),
        Q('Dans quelle partie exprime-t-on la fin ou la chute de l’histoire ?',
          'La conclusion', 'L’introduction', 'Le développement', n=4),
        V('La conclusion d’une histoire est toujours heureuse.', False, n=4,
          e='Non. Elle peut être heureuse ou malheureuse.')),

      N('liste',
        'Les types de texte narratif sont : le récit, le conte, la fable, l’histoire, la '
        'légende.',
        'bf-tn-types', F('Les types de texte narratif', 'le récit', 'le conte', 'la fable',
                         'l’histoire, la légende'),
        ('simple', 'Cinq façons de raconter.'),
        ('visuel', 'Le conte commence souvent par « il était une fois ».'),
        Q('Lequel est un type de texte narratif ?', 'le conte', 'la recette', 'la lettre'),
        V('La fable est un type de texte narratif.', True),
        T('Les types de texte narratif : le récit, le conte, la fable, l’histoire, la {{1}}.',
          'légende'),
        Q('Lequel n’est pas un type de texte narratif ?', 'le dictionnaire', 'la légende',
          'le récit', n=3),
        V('Le récit est un type de texte narratif.', True, n=4)),
      ),

    # ------------------------------------------------------------ 22 octobre
    L(FR, 'Le récit', PROD, '2026-10-22',
      'Le récit est un texte narratif qui consiste à narrer ou à raconter une suite '
      'd’évènements réels ou imaginaires. Il est divisé en trois parties : l’introduction ou '
      'situation initiale, le développement ou corps du devoir, la conclusion ou situation '
      'finale.',
      'bf-re-couv', ['situation initiale', 'péripéties', 'situation finale'],

      N('definition',
        'Le récit est un texte narratif qui consiste à narrer ou à raconter une suite '
        'd’évènements réels ou imaginaires.',
        'bf-re-def', F('Le récit', 'un texte narratif', 'il raconte', 'une suite d’évènements',
                       'réels ou imaginaires'),
        ('simple', 'Faire un récit, c’est raconter ce qui est arrivé, dans l’ordre.'),
        ('visuel', 'Une journée à Yaoundé : le bus, le centre-ville, le marché, le Mont Fébé.'),
        Q('Le récit est un texte…', 'narratif', 'publicitaire', 'scientifique'),
        V('Le récit raconte une suite d’évènements.', True),
        T('Le récit consiste à narrer ou à {{1}} une suite d’évènements.', 'raconter'),
        Q('Les évènements d’un récit peuvent être…', 'réels ou imaginaires',
          'seulement réels', 'seulement imaginaires', n=3),
        V('Le récit est divisé en trois parties.', True, n=4)),

      N('definition',
        'L’introduction ou situation initiale : ici on présente le cadre, le temps, le lieu et '
        'les personnages.',
        'bf-re-intro', F('La situation initiale', 'le cadre', 'le temps', 'le lieu',
                         'les personnages'),
        ('simple', 'Avant de raconter, on dit quand, où et avec qui.'),
        ('visuel', 'La semaine dernière, mon oncle m’a emmené visiter la ville de Yaoundé : le '
                   'temps, le personnage, le lieu.'),
        Q('Que présente-t-on dans la situation initiale ?', 'Le temps, le lieu, les personnages',
          'La fin de l’histoire', 'L’opinion de celui qui écrit'),
        V('L’introduction s’appelle aussi la situation initiale.', True),
        T('L’introduction s’appelle aussi la situation {{1}}.', 'initiale'),
        Q('Dans « La semaine dernière, mon oncle m’a emmené à Yaoundé », où est le lieu ?',
          'Yaoundé', 'la semaine dernière', 'mon oncle', n=3),
        V('Dans la situation initiale, on raconte la fin de l’histoire.', False, n=4,
          e='Non. On présente le cadre, le temps, le lieu et les personnages.')),

      N('liste',
        'Le développement : on raconte de manière chronologique, en commençant par l’élément '
        'déclencheur, ensuite les péripéties et enfin le dénouement. On utilise les temps du '
        'passé.',
        'bf-re-developpement', F('Le développement', 'l’élément déclencheur', 'les péripéties',
                                 'le dénouement', 'aux temps du passé', vif=(3,)),
        ('simple', 'Quelque chose arrive, des aventures suivent, puis tout se dénoue.'),
        ('visuel', 'D’abord, ensuite, puis, enfin : ces mots font avancer le récit dans '
                   'l’ordre.'),
        Q('Par quoi commence le développement ?', 'L’élément déclencheur', 'Le dénouement',
          'La conclusion'),
        V('Dans le développement, on raconte de manière chronologique.', True),
        T('Dans le développement, on utilise les temps du {{1}}.', 'passé'),
        C('Range les trois moments du développement dans l’ordre.', 'l’élément déclencheur',
          'les péripéties', 'le dénouement'),
        Q('Quels temps utilise-t-on dans le développement d’un récit ?', 'Les temps du passé',
          'Seulement le futur simple', 'Seulement l’infinitif', n=4),
        V('Le dénouement vient avant les péripéties.', False, n=4,
          e='Non. D’abord les péripéties, enfin le dénouement.')),

      N('definition',
        'La conclusion ou la situation finale : ici on donne son opinion, ses sentiments. Elle '
        'peut être heureuse ou malheureuse.',
        'bf-re-conclusion', F('La situation finale', 'on donne son opinion', 'ses sentiments',
                              'heureuse ou malheureuse'),
        ('simple', 'À la fin, on dit ce qu’on en a pensé et ce qu’on a ressenti.'),
        ('visuel', 'La ville est belle et animée, mais trop bruyante. Je préfère le calme de '
                   'mon village.'),
        Q('Que donne-t-on dans la conclusion d’un récit ?', 'Son opinion, ses sentiments',
          'Le lieu et les personnages', 'L’élément déclencheur'),
        V('La conclusion s’appelle aussi la situation finale.', True),
        T('La conclusion peut être heureuse ou {{1}}.', 'malheureuse'),
        A('Relie chaque partie du récit à ce qu’on y met.',
          ('la situation initiale', 'le temps, le lieu'),
          ('le développement', 'les péripéties'), ('la situation finale', 'son opinion')),
        Q('« Je préfère le calme de mon village » appartient à…', 'la conclusion',
          'l’introduction', 'l’élément déclencheur', n=4)),
      ),

    # ------------------------------------------------------------ 29 octobre
    L(FR, 'Le conte', PROD, '2026-10-29',
      'Le conte est un récit imaginaire dont les personnages peuvent être des humains, des '
      'objets ou des animaux. Il commence toujours par des indicateurs temporels comme il '
      'était une fois. Il a trois parties : la situation initiale, les péripéties et la '
      'situation finale.',
      'bf-co-couv', ['il était une fois', 'jadis', 'autrefois'],

      N('definition',
        'Le conte est un récit imaginaire dont les personnages peuvent être des humains, des '
        'objets ou des animaux.',
        'bf-co-def', F('Le conte', 'un récit imaginaire', 'des humains', 'des objets',
                       'des animaux'),
        ('simple', 'Dans un conte, tout est inventé : un animal ou un objet peut être un '
                   'personnage.'),
        ('visuel', 'Un homme et son chien dans un chalet, sur une montagne : deux personnages, '
                   'un humain et un animal.'),
        Q('Le conte est un récit…', 'imaginaire', 'réel', 'scientifique'),
        V('Dans un conte, les personnages peuvent être des animaux.', True),
        T('Le conte est un récit {{1}}.', 'imaginaire'),
        Q('Qui peut être un personnage de conte ?', 'Des humains, des objets, des animaux',
          'Seulement des humains', 'Seulement des animaux', n=3),
        V('Un conte raconte toujours une histoire vraie.', False, n=4,
          e='Non. Le conte est un récit imaginaire.')),

      N('liste',
        'Il commence toujours par des indicateurs temporels tels que : il était une fois, il y '
        'a longtemps, auparavant, autrefois, jadis.',
        'bf-co-indicateurs', F('Pour commencer un conte', 'il était une fois',
                               'il y a longtemps', 'auparavant, autrefois', 'jadis'),
        ('simple', 'Ces mots disent que l’histoire se passe dans un passé lointain.'),
        ('visuel', 'Il était une fois, sur une montagne, vivait un homme et son chien.'),
        Q('Par quoi commence toujours un conte ?', 'Un indicateur temporel', 'Une question',
          'Une conclusion'),
        V('« Il était une fois » est un indicateur temporel.', True),
        T('Un conte commence souvent par : il était une {{1}}.', 'fois'),
        Q('Lequel est un indicateur temporel de conte ?', 'jadis', 'pourtant', 'parce que',
          n=3),
        V('« Autrefois » peut commencer un conte.', True, n=4),
        Q('Lequel ne commence pas un conte ?', 'demain matin', 'il y a longtemps',
          'auparavant', n=4)),

      N('liste',
        'Le conte a trois parties : la situation initiale, où on retrouve le temps, le lieu et '
        'les personnages ; les péripéties ; la situation finale, qui est la fin du conte.',
        'bf-co-parties', P('Trois parties', ('situation initiale', 'temps, lieu'),
                           ('les péripéties', 'les actions'),
                           ('situation finale', 'la fin du conte')),
        ('simple', 'Un début, des aventures, une fin.'),
        ('visuel', 'La situation finale peut être heureuse ou malheureuse.'),
        Q('Combien de parties a le conte ?', 'Trois', 'Deux', 'Quatre'),
        V('La situation finale est la fin du conte.', True),
        T('La situation {{1}} est la fin du conte.', 'finale'),
        C('Range les trois parties du conte dans l’ordre.', 'la situation initiale',
          'les péripéties', 'la situation finale'),
        V('La situation finale d’un conte est toujours heureuse.', False, n=4,
          e='Non. Elle peut être heureuse ou malheureuse.')),

      N('definition',
        'Les péripéties sont le déroulement des actions. Les personnages rencontrent des '
        'difficultés. Le dénouement intervient à la fin des péripéties comme solution à la '
        'difficulté.',
        'bf-co-peripeties', F('Les péripéties', 'le déroulement des actions',
                              'des difficultés', 'd’autres personnages aident',
                              'le dénouement : la solution', vif=(3,)),
        ('simple', 'Un problème arrive, on lutte, et le dénouement apporte la solution.'),
        ('visuel', 'L’homme entend un bruit étrange, trouve son chien couché, regarde sa '
                   'patte : ce sont les péripéties.'),
        Q('Que rencontrent les personnages pendant les péripéties ?', 'Des difficultés',
          'Le titre du conte', 'L’auteur du conte'),
        V('Les personnages peuvent se faire aider par d’autres personnages.', True),
        T('Le {{1}} intervient à la fin des péripéties comme solution à la difficulté.',
          'dénouement'),
        Q('Qu’apporte le dénouement ?', 'La solution à la difficulté', 'Un nouveau problème',
          'Le lieu de l’histoire', n=3),
        V('Le dénouement intervient au début du conte.', False, n=4,
          e='Non. Il intervient à la fin des péripéties.')),
      ),

    # ------------------------------------------------------------ 14 octobre
    L(FR, 'Lecture, page 28 : les mots difficiles', LECT, '2026-10-14',
      'Les mots difficiles du texte de la page 28 : une poignée, le souper, un agouti, un '
      'canari, une concession. Le champ lexical du village : l’enclos, le bois sec, le '
      'chasseur, les ignames, le canari, la chèvre, les herbes sèches, le champ.',
      'bf-l1-couv', ['une poignée', 'un agouti', 'un canari'],

      N('liste',
        'Une poignée : ce qui peut tenir dans une seule main. Le souper : repas qu’on mange la '
        'nuit avant de dormir. Un agouti : petit animal de forêt semblable à un gros rat.',
        'bf-l1-mots1', P('Trois mots', ('une poignée', 'dans une main'),
                         ('le souper', 'le repas du soir'), ('un agouti', 'animal de forêt')),
        ('simple', 'Une poignée d’arachides, c’est ce que ta main peut prendre en une fois.'),
        ('visuel', 'L’agouti vit en forêt et ressemble à un gros rat.'),
        Q('Qu’est-ce qu’une poignée ?', 'Ce qui tient dans une seule main',
          'Un grand sac de riz', 'Un repas du matin'),
        V('Le souper est le repas qu’on mange la nuit avant de dormir.', True),
        T('Un {{1}} est un petit animal de forêt semblable à un gros rat.', 'agouti'),
        A('Relie chaque mot à ce qu’il veut dire.', ('une poignée', 'ce que tient une main'),
          ('le souper', 'le repas de la nuit'), ('un agouti', 'un animal de forêt')),
        V('Un agouti est un oiseau.', False, n=4,
          e='Non. C’est un petit animal de forêt semblable à un gros rat.')),

      N('liste',
        'Un canari : marmite traditionnelle faite en terre cuite. Une concession : grand '
        'terrain ayant plusieurs maisons où vit une famille.',
        'bf-l1-mots2', P('Deux mots', ('un canari', 'marmite en terre'),
                         ('une concession', 'terrain, maisons')),
        ('simple', 'Dans le texte, le canari n’est pas un oiseau : c’est une marmite.'),
        ('visuel', 'Dans une concession, plusieurs maisons de la même famille partagent la '
                   'même cour.'),
        Q('Dans ce texte, qu’est-ce qu’un canari ?', 'Une marmite en terre cuite',
          'Un petit oiseau jaune', 'Un panier de feuilles'),
        V('Une concession est un grand terrain ayant plusieurs maisons.', True),
        T('Le canari est une marmite traditionnelle faite en terre {{1}}.', 'cuite'),
        Q('Qui vit dans une concession ?', 'Une famille', 'Un troupeau', 'Une école', n=3),
        V('Le canari est fait en fer.', False, n=4, e='Non. Il est fait en terre cuite.')),

      N('liste',
        'Le champ lexical du village : l’enclos, le bois sec, le chasseur, les ignames, les '
        'feuilles, le canari, la chèvre, les herbes sèches, le champ.',
        'bf-l1-champ', F('Les mots du village', 'l’enclos, le bois sec', 'le chasseur',
                         'les ignames, les feuilles', 'la chèvre, le champ'),
        ('simple', 'Un champ lexical, ce sont tous les mots qui parlent du même sujet.'),
        ('visuel', 'L’enclos garde les chèvres, le canari cuit les ignames.'),
        Q('Lequel appartient au champ lexical du village ?', 'l’enclos', 'l’immeuble',
          'le tunnel'),
        V('« Le chasseur » appartient au champ lexical du village.', True),
        T('Tous les mots qui parlent du même sujet forment un champ {{1}}.', 'lexical'),
        Q('Lequel n’appartient pas au champ lexical du village ?', 'le boulevard',
          'la chèvre', 'les ignames', n=3),
        V('« Les herbes sèches » appartiennent au champ lexical du village.', True, n=4)),
      ),

    # ------------------------------------------------------------ 20 octobre
    L(FR, 'L’arrivée en ville : les mots difficiles', LECT, '2026-10-20',
      'Les mots difficiles du texte « L’arrivée en ville », page 33 : un flot, '
      's’agglutinaient, les artères, la cohue, étroites, sidéré, bigarré, détonnaient.',
      'bf-l2-couv', ['un flot', 'la cohue', 'sidéré'],

      N('liste',
        'Un flot : un grand nombre. S’agglutinaient : se serraient très fort les uns contre '
        'les autres. Les artères : les rues. La cohue : foule de personnes qui se bousculent.',
        'bf-l2-mots1', P('Quatre mots', ('un flot', 'un grand nombre'),
                         ('s’agglutinaient', 'se serraient'), ('les artères', 'les rues'),
                         ('la cohue', 'la foule')),
        ('simple', 'Ces quatre mots disent tous qu’il y a beaucoup de monde en ville.'),
        ('visuel', 'Dans la cohue, tout le monde passe en même temps et se bouscule.'),
        Q('Dans ce texte, que sont « les artères » ?', 'Les rues', 'Les arbres',
          'Les maisons'),
        V('Un flot, c’est un grand nombre.', True),
        T('La {{1}} est une foule de personnes qui se bousculent.', 'cohue'),
        A('Relie chaque mot à ce qu’il veut dire.', ('un flot', 'un grand nombre'),
          ('les artères', 'les rues'), ('la cohue', 'une foule qui bouscule'),
          ('s’agglutinaient', 'se serraient fort')),
        Q('« Les gens s’agglutinaient » veut dire qu’ils…', 'se serraient les uns contre les '
          'autres', 'couraient très vite', 'dormaient dans la rue', n=4)),

      N('liste',
        'Étroites : petites. Sidéré : très surpris, choqué. Bigarré : de toutes les couleurs. '
        'Détonnaient : se faisaient trop remarquer.',
        'bf-l2-mots2', P('Quatre mots', ('étroites', 'petites'), ('sidéré', 'très surpris'),
                         ('bigarré', 'de toutes couleurs'),
                         ('détonnaient', 'se remarquaient')),
        ('simple', 'Sidéré, c’est plus fort que surpris : on en reste sans voix.'),
        ('visuel', 'Un pagne bigarré a du rouge, du jaune, du vert, du bleu.'),
        Q('Que veut dire « sidéré » ?', 'Très surpris, choqué', 'Très fatigué', 'Très content'),
        V('« Bigarré » veut dire de toutes les couleurs.', True),
        T('Des rues {{1}} sont des rues petites.', 'étroites'),
        A('Relie chaque mot à ce qu’il veut dire.', ('étroites', 'petites'),
          ('sidéré', 'très surpris'), ('bigarré', 'de toutes les couleurs'),
          ('détonnaient', 'se faisaient remarquer')),
        V('« Sidéré » veut dire très fatigué.', False, n=4,
          e='Non. Très surpris, choqué.'),
        Q('Des habits qui « détonnaient » sont des habits qui…', 'se faisaient trop remarquer',
          'étaient très propres', 'coûtaient très cher', n=4)),
      ),
]
