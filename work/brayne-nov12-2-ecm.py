# -*- coding: utf-8 -*-
# ECM — quatre leçons. Chargé par lecons-brayne-cahier-nov12.py.
#
# « La modestie » n-a pas d-en-tête de date : elle suit les Pygmées du
# 22 octobre sur la même page, et en prend la date.
#
# « La démocratie » vient de la révision corrigée d-ECM. La définition s-y lit
# en entier ; les principes, que la copie demande sans qu-on lise la réponse,
# sont ceux que la révision de KLEIN entoure et que tous les manuels donnent.
# Cette révision n-est pas datée : elle précède le 12 octobre, et l-app
# n-affiche pas de date.

ECM = 'ECM'
MORALE = 'Éducation morale'
CITOYEN = 'Éducation à la citoyenneté'

LECONS = [
    # ---------------------------------------------------------- sans date
    L(ECM, 'La démocratie', CITOYEN, '2026-10-01',
      'La démocratie est le gouvernement du peuple, par le peuple et pour le peuple. Ses '
      'principes : le vote, le multipartisme, l’alternance au pouvoir, la séparation des '
      'pouvoirs et la liberté d’expression. Le bon citoyen règle les conflits par la paix et '
      'respecte les droits de tous.',
      'bn-demo-couv', ['le peuple', 'le vote', 'la liberté'],

      N('definition',
        'La démocratie est le gouvernement du peuple, par le peuple et pour le peuple.',
        'bn-demo-def', F('La démocratie', 'le gouvernement', 'du peuple, par le peuple',
                         'et pour le peuple'),
        ('simple', 'En démocratie, c’est le peuple qui choisit ceux qui le dirigent.'),
        ('analogie', 'Comme l’élection du chef de classe : les élèves votent, et le chef '
                     'travaille pour eux.'),
        Q('Qu’est-ce que la démocratie ?', 'Le gouvernement du peuple, par le peuple, pour le peuple',
          'Le pouvoir d’un seul chef pour toujours', 'Le pouvoir des plus forts seulement'),
        V('En démocratie, le pouvoir vient du peuple.', True),
        T('La démocratie est le gouvernement du {{1}}, par le peuple et pour le peuple.',
          'peuple'),
        Q('En démocratie, qui choisit les dirigeants ?', 'le peuple', 'l’armée',
          'un seul homme', n=3),
        V('En démocratie, un seul homme décide de tout, sans élection.', False, n=4,
          e='Non. Ça, c’est la dictature. En démocratie, le peuple choisit.')),

      N('liste',
        'Les principes de la démocratie sont le vote, le multipartisme, l’alternance au pouvoir, '
        'la séparation des pouvoirs et la liberté d’expression.',
        'bn-demo-principes', F('Ses principes', 'le vote', 'le multipartisme',
                               'l’alternance au pouvoir', 'la liberté d’expression'),
        ('simple', 'On vote, plusieurs partis existent, les dirigeants changent, et chacun peut '
                   'dire ce qu’il pense.'),
        ('pas_a_pas', 'Multipartisme : plusieurs partis. Alternance : le pouvoir peut changer de '
                      'mains. Séparation des pouvoirs : celui qui fait la loi n’est pas celui '
                      'qui juge.'),
        Q('Lequel est un principe de la démocratie ?', 'le vote', 'la dictature',
          'le libertinage'),
        V('La liberté d’expression est un principe de la démocratie.', True),
        T('Le fait d’avoir plusieurs partis politiques s’appelle le {{1}}.', 'multipartisme'),
        Q('Lequel n’est PAS un principe de la démocratie ?', 'la dictature',
          'l’alternance au pouvoir', 'la séparation des pouvoirs', n=3),
        A('Relie chaque principe à ce qu’il veut dire.', ('le vote', 'choisir ses dirigeants'),
          ('le multipartisme', 'plusieurs partis'),
          ('l’alternance', 'le pouvoir change de mains'), n=3),
        V('Le libertinage est un principe de la démocratie.', False, n=4,
          e='Non. La liberté d’expression, oui ; le libertinage, c’est faire n’importe quoi.')),

      N('liste',
        'Le bon citoyen ne fait pas la guerre pour avoir la paix, obéit tout de suite, '
        'n’impose pas son avis par la force et respecte les droits des personnes handicapées.',
        'bn-demo-citoyen', F('Le bon citoyen', 'cherche la paix', 'obéit tout de suite',
                             'n’impose pas par la force', 'respecte les handicapés'),
        ('simple', 'Un citoyen règle les problèmes par la parole, jamais par la force.'),
        ('histoire', 'Deux camarades ne sont pas d’accord : ils discutent, et chacun écoute '
                     'l’autre.'),
        V('Pour avoir la paix, il faut faire la guerre.', False,
          e='Non. La paix se construit par le dialogue, pas par la guerre.'),
        V('Les personnes handicapées ont des droits, comme tout le monde.', True),
        T('Obéir lentement, ce n’est pas {{1}}.', 'obéir'),
        V('Je ne dois jamais ouvrir la porte à un inconnu.', True, n=3),
        V('Je peux imposer mon point de vue par la force.', False, n=4,
          e='Non. On donne son avis par la parole, et on écoute celui des autres.'),
        Q('Que fait un bon citoyen en cas de désaccord ?', 'Il discute dans le calme',
          'Il frappe l’autre', 'Il crie plus fort', n=4))),

    # -------------------------------------------------------------- 12 octobre
    L(ECM, 'La notion du bien et du mal', MORALE, '2026-10-12',
      'Le bien est tout ce qui est conforme, juste et agréable, honnête et louable : il apporte '
      'la joie, la paix, l’harmonie et la douceur. Le mal est tout ce qui est pénible et '
      'désagréable, le contraire du bien : il apporte la tristesse, les problèmes, les '
      'querelles et la douleur.',
      'bn-bien-couv', ['le bien', 'le mal'],

      N('definition',
        'Le bien est tout ce qui est conforme, juste et agréable. C’est tout ce qui est honnête '
        'et louable.',
        'bn-bien-def', F('Le bien', 'juste', 'agréable', 'honnête', 'louable'),
        ('simple', 'Faire le bien, c’est agir de façon juste et honnête, d’une façon dont on '
                   'peut être fier.'),
        ('histoire', 'Ama trouve un billet dans la cour et le porte à la maîtresse. Elle a fait '
                     'le bien.'),
        Q('Qu’est-ce que le bien ?', 'Tout ce qui est juste et agréable',
          'Tout ce qui est pénible', 'Tout ce qui fait peur'),
        V('Le bien est tout ce qui est honnête et louable.', True),
        T('Le bien est tout ce qui est conforme, {{1}} et agréable.', 'juste'),
        Q('Lequel de ces gestes fait le bien ?', 'Rendre l’argent trouvé à son propriétaire',
          'Garder l’argent trouvé pour soi', 'Se moquer d’un camarade', n=3),
        V('Mentir pour avoir une meilleure note, c’est faire le bien.', False, n=4,
          e='Non. Ce n’est ni juste ni honnête.')),

      N('liste',
        'Le bien apporte la joie, la paix, l’harmonie et la douceur.',
        'bn-bien-fruits', F('Le bien apporte', 'la joie', 'la paix', 'l’harmonie', 'la douceur'),
        ('simple', 'Là où on fait le bien, on vit content et sans dispute.'),
        ('visuel', 'Une classe où chacun aide l’autre : tout le monde sourit.'),
        Q('Qu’apporte le bien ?', 'la joie et la paix', 'les querelles', 'la douleur'),
        V('Le bien apporte l’harmonie.', True),
        T('Le bien apporte la joie, la {{1}} et la douceur.', 'paix'),
        Q('Lequel n’est pas apporté par le bien ?', 'la tristesse', 'la douceur',
          'l’harmonie', n=3),
        V('Le bien apporte les problèmes.', False, n=4,
          e='Non. Le bien apporte la joie, la paix, l’harmonie et la douceur.')),

      N('definition',
        'Le mal est tout ce qui est pénible et désagréable ; c’est le contraire du bien. Il '
        'apporte la tristesse, les problèmes, les querelles et la douleur.',
        'bn-bien-mal', F('Le mal', 'pénible, désagréable', 'le contraire du bien',
                         'la tristesse', 'les querelles, la douleur'),
        ('simple', 'Le mal fait souffrir les autres, ou soi-même. C’est l’inverse du bien.'),
        ('histoire', 'Un élève casse la règle d’un camarade et rit : la dispute commence. Il a '
                     'fait le mal.'),
        Q('Le mal est…', 'le contraire du bien', 'une sorte de bien', 'une sorte de joie'),
        V('Le mal apporte les querelles.', True),
        T('Le mal est tout ce qui est pénible et {{1}}.', 'désagréable'),
        A('Relie chacun à ce qu’il apporte.', ('le bien', 'la joie'),
          ('le mal', 'la tristesse'), n=3),
        V('Le mal apporte la paix et l’harmonie.', False, n=4,
          e='Non. Le mal apporte la tristesse, les problèmes, les querelles et la douleur.'))),

    # -------------------------------------------------------------- 19 octobre
    L(ECM, 'La notion de la loi', CITOYEN, '2026-10-19',
      'La loi est une règle de droit écrite qui s’impose à tous ; elle évite le désordre dans '
      'un pays. Elle est votée par le parlement, promulguée par le président de la République, '
      'puis publiée dans les journaux officiels. Ceux qui ne la respectent pas sont punis.',
      'bn-loi-couv', ['la loi', 'le parlement', 'le président'],

      N('definition',
        'La loi est une règle de droit écrite qui s’impose à tous ceux qui sont sous son '
        'autorité. Elle permet d’éviter le désordre dans un pays.',
        'bn-loi-def', F('La loi', 'une règle de droit écrite', 'elle s’impose à tous',
                        'elle évite le désordre'),
        ('simple', 'La loi dit ce qu’on a le droit de faire et ce qui est interdit, pour tout '
                   'le monde.'),
        ('analogie', 'Le règlement de l’école vaut pour tous les élèves ; la loi vaut pour '
                     'tout le pays.'),
        Q('Qu’est-ce que la loi ?', 'Une règle de droit écrite', 'Un conseil qu’on peut oublier',
          'Une chanson du pays'),
        V('La loi permet d’éviter le désordre dans un pays.', True),
        T('La loi est une règle de droit {{1}} qui s’impose à tous.', 'écrite'),
        Q('À qui s’impose la loi ?', 'À tous ceux qui sont sous son autorité',
          'Seulement aux enfants', 'Seulement aux commerçants', n=3),
        V('La loi ne s’impose qu’à ceux qui l’acceptent.', False, n=4,
          e='Non. Elle s’impose à tous ceux qui sont sous son autorité.')),

      N('relation',
        'La loi est proposée et votée par le parlement. Elle est promulguée par le président de '
        'la République, puis publiée dans les journaux officiels, pour que tout le monde la '
        'connaisse.',
        'bn-loi-chemin', F('Le chemin de la loi', '1. votée par le parlement',
                           '2. promulguée par le président', '3. publiée au journal officiel'),
        ('pas_a_pas', 'D’abord le parlement vote. Ensuite le président promulgue. Enfin on '
                      'publie la loi.'),
        ('simple', 'On publie la loi dans les journaux officiels pour que personne ne puisse '
                   'dire : je ne savais pas.'),
        Q('Qui vote la loi ?', 'le parlement', 'le président de la République', 'le maire'),
        V('La loi est promulguée par le président de la République.', True),
        T('La loi est proposée et votée par le {{1}}.', 'parlement'),
        C('Remets dans l’ordre le chemin de la loi.', 'votée par le parlement',
          'promulguée par le président', 'publiée au journal officiel', n=3),
        Q('Pourquoi publie-t-on la loi dans les journaux officiels ?',
          'Pour que tout le monde la connaisse', 'Pour la garder secrète',
          'Pour l’annuler', n=4),
        V('C’est le président de la République qui vote la loi.', False, n=4,
          e='Non. Le parlement la vote ; le président la promulgue.')),

      N('definition',
        'Ceux qui ne respectent pas la loi sont punis. Respectons la loi pour une vie en société '
        'organisée, disciplinée et paisible.',
        'bn-loi-respect', F('Respectons la loi', 'sinon, on est puni', 'une société organisée',
                            'disciplinée', 'et paisible'),
        ('simple', 'Quand chacun respecte la loi, tout le monde vit tranquille.'),
        ('visuel', 'Au feu rouge, toutes les voitures s’arrêtent : personne ne se cogne.'),
        Q('Que se passe-t-il pour ceux qui ne respectent pas la loi ?', 'Ils sont punis',
          'Ils sont récompensés', 'Rien du tout'),
        V('Respecter la loi rend la vie en société paisible.', True),
        T('Respectons la loi pour une vie en société organisée, disciplinée et {{1}}.',
          'paisible'),
        Q('Respecter la loi donne une société…', 'organisée', 'en désordre', 'bruyante', n=3),
        V('Celui qui ne respecte pas la loi n’est jamais puni.', False, n=4,
          e='Non. Ceux qui ne respectent pas la loi sont punis.'))),

    # -------------------------------------------------------------- 22 octobre
    L(ECM, 'La modestie', MORALE, '2026-10-22',
      'La modestie est le fait d’être humble envers les autres. Pour être modeste, il faut '
      'éviter de se croire supérieur aux autres et avoir de la considération pour ses '
      'semblables. Soyons modestes pour rendre la vie agréable.',
      'bn-modestie-couv', ['humble', 'les autres'],

      N('definition',
        'La modestie est le fait d’être humble envers les autres.',
        'bn-modestie-def', F('La modestie', 'être humble', 'envers les autres'),
        ('simple', 'Être modeste, c’est ne pas se vanter, même quand on réussit.'),
        ('histoire', 'Paul a eu la meilleure note. Il ne se moque pas des autres : il aide son '
                     'voisin. Paul est modeste.'),
        Q('Qu’est-ce que la modestie ?', 'Être humble envers les autres',
          'Se vanter devant les autres', 'Commander les autres'),
        V('Être modeste, c’est être humble envers les autres.', True),
        T('La modestie est le fait d’être {{1}} envers les autres.', 'humble'),
        Q('Lequel est un enfant modeste ?', 'Celui qui gagne sans se moquer des autres',
          'Celui qui dit qu’il est le meilleur', 'Celui qui rit des erreurs des autres', n=3),
        V('Un enfant modeste se vante de ses notes devant tout le monde.', False, n=4,
          e='Non. L’enfant modeste reste humble.')),

      N('liste',
        'Pour être modeste, nous devons éviter de nous croire supérieurs aux autres et avoir de '
        'la considération pour nos semblables. Soyons modestes pour rendre la vie agréable.',
        'bn-modestie-comment', F('Pour être modeste', 'ne pas se croire supérieur',
                                 'respecter ses semblables', 'la vie devient agréable'),
        ('simple', 'Personne n’est au-dessus des autres. On respecte chacun, et la vie est plus '
                   'douce.'),
        ('analogie', 'Dans une équipe, celui qui se croit le chef de tous finit seul.'),
        Q('Pour être modeste, il faut éviter…', 'de se croire supérieur aux autres',
          'd’aider les autres', 'de saluer les autres'),
        V('Être modeste, c’est avoir de la considération pour ses semblables.', True),
        T('Pour être modeste, j’ai de la {{1}} pour mes semblables.', 'considération'),
        Q('Pourquoi être modeste, d’après le cahier ?', 'Pour rendre la vie agréable',
          'Pour être le premier partout', 'Pour être plus fort que les autres', n=3),
        V('Se croire supérieur aux autres, c’est être modeste.', False, n=4,
          e='Non. Pour être modeste, il faut éviter de se croire supérieur.'))),

    # -------------------------------------------------------------- 26 octobre
    L(ECM, 'L’histoire de l’hymne national du Cameroun', CITOYEN, '2026-10-26',
      'L’hymne national est un chant de ralliement choisi par les dirigeants pour représenter '
      'un pays. « Ô Cameroun, berceau de nos ancêtres » a été composé en 1928 et adopté en 1957 '
      'par l’ALCAM. René Djam Afame a écrit les paroles, Samuel Minkio Bamba la musique.',
      'bn-hymne-couv', ['1928', '1957', 'Foulassi'],

      N('definition',
        'L’hymne national est un chant de ralliement choisi par les dirigeants pour représenter '
        'un pays.',
        'bn-hymne-def', F('L’hymne national', 'un chant de ralliement', 'il représente le pays'),
        ('simple', 'C’est le chant de tout le pays. On le chante debout, au lever du drapeau.'),
        ('visuel', 'Le matin, toute l’école chante devant le drapeau : c’est l’hymne national.'),
        Q('Qu’est-ce que l’hymne national ?', 'Un chant qui représente le pays',
          'Le drapeau du pays', 'La devise du pays'),
        V('L’hymne national est un chant de ralliement.', True),
        T('L’hymne national est un {{1}} de ralliement.', 'chant'),
        Q('Qui choisit l’hymne national ?', 'les dirigeants du pays', 'les élèves de la classe',
          'les commerçants', n=3),
        V('L’hymne national est le drapeau du pays.', False, n=4,
          e='Non. L’hymne est un chant.')),

      N('date',
        'Notre hymne, « Ô Cameroun, berceau de nos ancêtres », a été composé en 1928 et adopté '
        'en 1957 par l’ALCAM.',
        'bn-hymne-dates', F('Ô Cameroun', 'berceau de nos ancêtres', 'composé en 1928',
                            'adopté en 1957', 'par l’ALCAM'),
        ('pas_a_pas', 'D’abord écrit en 1928, l’hymne n’est devenu officiel qu’en 1957.'),
        ('simple', 'Composé en 1928, adopté en 1957 : vingt-neuf ans entre les deux.'),
        Q('Quel est le titre de notre hymne national ?', 'Ô Cameroun, berceau de nos ancêtres',
          'Paix, travail, patrie', 'Le chant de la forêt'),
        V('Notre hymne a été composé en 1928.', True),
        T('L’hymne a été adopté en {{1}} par l’ALCAM.', '1957'),
        Q('En quelle année l’hymne a-t-il été composé ?', '1928', '1957', '1960', n=3),
        V('L’hymne a été adopté en 1928.', False, n=4,
          e='Non. Composé en 1928, il a été adopté en 1957.')),

      N('relation',
        'Il a été composé par des élèves de la première promotion de l’école normale de '
        'Foulassi : René Djam Afame pour les paroles, Samuel Minkio Bamba pour la musique.',
        'bn-hymne-auteurs', P('Les auteurs', ('les paroles', 'René Djam Afame'),
                              ('la musique', 'Samuel Minkio Bamba')),
        ('simple', 'Deux élèves de l’école normale de Foulassi : l’un a écrit les mots, '
                   'l’autre la mélodie.'),
        ('analogie', 'Une chanson, ce sont des paroles et une musique : ici, deux auteurs.'),
        Q('Qui a écrit les paroles de l’hymne ?', 'René Djam Afame', 'Samuel Minkio Bamba',
          'Fernando Poo'),
        V('Samuel Minkio Bamba a composé la musique de l’hymne.', True),
        T('Les auteurs de l’hymne étaient élèves de l’école {{1}} de Foulassi.', 'normale'),
        A('Relie chaque auteur à sa part.', ('René Djam Afame', 'les paroles'),
          ('Samuel Minkio Bamba', 'la musique'), n=3),
        V('René Djam Afame a composé la musique de l’hymne.', False, n=4,
          e='Non. Il a écrit les paroles ; Samuel Minkio Bamba a fait la musique.'))),
]
