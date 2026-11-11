# -*- coding: utf-8 -*-
# Conjugaison — sept leçons. Chargé par lecons-brayne-francais-oct.py.
#
# Chaque leçon de temps oppose le temps demandé à celui qu-on écrit le plus
# souvent à sa place : le passé simple au passé composé, le futur simple au
# futur antérieur. C-est ce que les exercices corrigés du cahier travaillent.

FR = 'Français'
CONJ = 'Conjugaison'

LECONS = [
    # ---------------------------------------------------------------- devoir
    L(FR, 'L’infinitif et les trois groupes de verbes', CONJ, '2026-10-02',
      'L’infinitif est le nom du verbe : pleut vient de pleuvoir. Les verbes se rangent en '
      'trois groupes. Jeter est du 1er groupe, vieillir du 2e groupe parce qu’on dit nous '
      'vieillissons, et mettre, aller, tenir, parcourir sont du 3e groupe.',
      'bf-gr-couv', ['1er groupe', '2e groupe', '3e groupe'],

      N('definition',
        'L’infinitif est le nom du verbe. Il pleut : c’est le verbe pleuvoir. Les crocodiles '
        'revivent : c’est le verbe revivre.',
        'bf-gr-infinitif', P('Trouver l’infinitif', ('il pleut', 'pleuvoir'),
                             ('ils revivent', 'revivre'), ('elle est', 'être'),
                             ('nous allons', 'aller')),
        ('simple', 'L’infinitif, c’est le verbe quand personne ne le conjugue : chanter, finir, '
                   'pleuvoir.'),
        ('pas_a_pas', 'Dis « il faut… » devant : il faut pleuvoir, il faut revivre. Le mot qui '
                      'vient est l’infinitif.'),
        Q('Quel est l’infinitif de « il pleut » ?', 'pleuvoir', 'pleuter', 'pleurer'),
        V('L’infinitif de « ils revivent » est revivre.', True),
        T('La forêt est verdoyante. L’infinitif du verbe est {{1}}.', 'être',
          e='Est, c’est le verbe être.'),
        A('Relie chaque verbe conjugué à son infinitif.', ('il pleut', 'pleuvoir'),
          ('ils revivent', 'revivre'), ('nous allons', 'aller'), ('ton père semble', 'sembler')),
        Q('Quel est l’infinitif de « les crocodiles revivent » ?', 'revivre', 'revenir',
          'revoir', n=4),
        V('L’infinitif de « il pleut » est pleurer.', False, n=4,
          e='Non. Il pleut, c’est pleuvoir. Pleurer, c’est verser des larmes.')),

      N('liste',
        'Jeter, grimper et pourchasser sont du 1er groupe : leur infinitif se termine par er.',
        'bf-gr-premier', F('Le 1er groupe', 'jeter', 'grimper', 'pourchasser',
                           'ils finissent par er'),
        ('simple', 'Presque tous les verbes en er sont du 1er groupe : chanter, manger, jeter.'),
        ('visuel', 'Regarde la fin du mot : jet-er, grimp-er, pourchass-er.'),
        Q('Lequel est un verbe du 1er groupe ?', 'grimper', 'grossir', 'mettre'),
        V('Jeter est un verbe du 1er groupe.', True),
        T('Les verbes du 1er groupe se terminent par {{1}}.', 'er'),
        Q('Lequel est un verbe du 1er groupe ?', 'pourchasser', 'franchir', 'tenir', n=3),
        V('Vieillir est un verbe du 1er groupe.', False, n=4, e='Non. Vieillir est du 2e groupe.')),

      N('liste',
        'Vieillir, franchir et grossir sont du 2e groupe : ils finissent par ir et font nous '
        'vieillissons, nous franchissons, nous grossissons.',
        'bf-gr-deuxieme', P('Le 2e groupe : issons', ('vieillir', 'vieillissons'),
                            ('franchir', 'franchissons'), ('grossir', 'grossissons')),
        ('simple', 'Un verbe en ir est du 2e groupe seulement s’il fait issons avec nous.'),
        ('pas_a_pas', 'Mets « nous » devant. Nous grossissons : 2e groupe. Nous tenons : pas '
                      'de issons, donc 3e groupe.'),
        Q('Lequel est un verbe du 2e groupe ?', 'franchir', 'parcourir', 'tenir'),
        V('Grossir est un verbe du 2e groupe.', True),
        T('Vieillir est du 2e groupe : nous {{1}}.', 'vieillissons'),
        A('Relie chaque verbe du 2e groupe à sa forme avec nous.', ('vieillir', 'vieillissons'),
          ('franchir', 'franchissons'), ('grossir', 'grossissons')),
        V('Tous les verbes qui finissent par ir sont du 2e groupe.', False, n=4,
          e='Non. Tenir et parcourir finissent par ir et sont du 3e groupe.'),
        Q('Comment reconnaît-on un verbe du 2e groupe ?', 'Il fait issons avec nous',
          'Il finit toujours par er', 'Il ne se conjugue pas', n=4)),

      N('liste',
        'Mettre, aller, tenir et parcourir sont du 3e groupe. Tenir et parcourir finissent par '
        'ir, mais on dit nous tenons, nous parcourons.',
        'bf-gr-troisieme', F('Le 3e groupe', 'mettre', 'aller', 'tenir : nous tenons',
                             'parcourir : nous parcourons'),
        ('simple', 'Le 3e groupe réunit tous les verbes qui ne sont ni du 1er ni du 2e.'),
        ('visuel', 'Aller finit par er, mais il est du 3e groupe : je vais, nous allons, ils '
                   'vont.'),
        Q('Dans quel groupe est le verbe tenir ?', 'Le 3e groupe', 'Le 2e groupe',
          'Le 1er groupe'),
        V('Mettre est un verbe du 3e groupe.', True),
        T('Parcourir est du 3e groupe : nous {{1}}.', 'parcourons'),
        A('Range chaque verbe dans son groupe.', ('jeter', '1er groupe'), ('grossir', '2e groupe'),
          ('tenir', '3e groupe')),
        V('Parcourir est un verbe du 2e groupe.', False, n=4,
          e='Non. On dit nous parcourons, pas nous parcourissons : 3e groupe.'),
        Q('Dans quel groupe est le verbe aller ?', 'Le 3e groupe', 'Le 1er groupe',
          'Le 2e groupe', n=4)),
      ),

    # ------------------------------------------------------------ 12 octobre
    L(FR, 'Les temps du mode indicatif', CONJ, '2026-10-12',
      'Le mode indicatif est celui qui parle de la certitude, des actions réelles. Il est '
      'divisé en deux : les temps simples et les temps composés. Il y a quatre temps simples '
      'et quatre temps composés.',
      'bf-in-couv', ['temps simples', 'temps composés'],

      N('definition',
        'Le mode indicatif est celui qui parle de la certitude, des actions réelles.',
        'bf-in-mode', F('Le mode indicatif', 'la certitude', 'les actions réelles'),
        ('simple', 'Avec l’indicatif on dit ce qui est, ce qui était ou ce qui sera.'),
        ('visuel', 'Il pleut, il pleuvait, il pleuvra : trois faits, trois temps de '
                   'l’indicatif.'),
        Q('De quoi parle le mode indicatif ?', 'De la certitude, des actions réelles',
          'Des ordres que l’on donne', 'Des souhaits et des rêves'),
        V('Le mode indicatif parle des actions réelles.', True),
        T('Le mode indicatif parle de la {{1}}.', 'certitude'),
        Q('Quel mode parle de la certitude ?', 'L’indicatif', 'L’impératif', 'L’infinitif', n=3),
        V('Le mode indicatif sert à parler de ce qui n’est pas sûr.', False, n=4,
          e='Non. Il parle de la certitude.')),

      N('relation',
        'Le mode indicatif est divisé en deux : les temps simples et les temps composés.',
        'bf-in-deux', P('Un mot ou deux mots', ('temps simple', 'je chante'),
                        ('temps composé', 'j’ai chanté')),
        ('simple', 'Un temps simple tient en un seul mot. Un temps composé en demande deux.'),
        ('visuel', 'Je chante : un mot. J’ai chanté : deux mots, ai et chanté.'),
        Q('En combien de parties le mode indicatif est-il divisé ?', 'Deux', 'Trois', 'Quatre'),
        V('L’indicatif a des temps simples et des temps composés.', True),
        T('L’indicatif est divisé en temps simples et en temps {{1}}.', 'composés'),
        Q('« J’ai chanté » est écrit à un temps…', 'composé', 'simple', 'infinitif', n=3),
        V('« Je chantais » est un temps composé.', False, n=4,
          e='Non. Un seul mot : c’est un temps simple.')),

      N('liste',
        'Les temps simples de l’indicatif sont : le présent, l’imparfait, le futur simple et le '
        'passé simple.',
        'bf-in-simples', F('Les quatre temps simples', 'le présent', 'l’imparfait',
                           'le futur simple', 'le passé simple'),
        ('simple', 'Quatre temps, et chacun s’écrit en un seul mot.'),
        ('visuel', 'Je chante, je chantais, je chanterai, je chantai.'),
        Q('Lequel est un temps simple de l’indicatif ?', 'Le passé simple', 'Le passé composé',
          'Le futur antérieur'),
        V('L’imparfait est un temps simple de l’indicatif.', True),
        T('Les temps simples sont le présent, l’imparfait, le futur simple et le passé {{1}}.',
          'simple'),
        Q('Combien y a-t-il de temps simples à l’indicatif ?', 'Quatre', 'Deux', 'Huit', n=3),
        V('Le passé composé est un temps simple.', False, n=4,
          e='Non. Son nom le dit : il est composé.')),

      N('liste',
        'Les temps composés de l’indicatif sont : le passé composé, le plus-que-parfait, le '
        'futur antérieur et le passé antérieur.',
        'bf-in-composes', F('Les quatre temps composés', 'le passé composé',
                            'le plus-que-parfait', 'le futur antérieur', 'le passé antérieur'),
        ('simple', 'Quatre temps, et chacun s’écrit en deux mots.'),
        ('visuel', 'J’ai chanté, j’avais chanté, j’aurai chanté, j’eus chanté.'),
        Q('Lequel est un temps composé de l’indicatif ?', 'Le plus-que-parfait', 'L’imparfait',
          'Le passé simple'),
        V('Le futur antérieur est un temps composé.', True),
        T('Les temps composés sont le passé composé, le plus-que-parfait, le futur antérieur et '
          'le passé {{1}}.', 'antérieur'),
        A('Range chaque temps dans sa famille.', ('le présent', 'temps simple'),
          ('le passé composé', 'temps composé')),
        V('Le passé simple est un temps composé.', False, n=4,
          e='Non. Le passé simple est un temps simple.'),
        Q('Lequel n’est pas un temps composé ?', 'Le futur simple', 'Le futur antérieur',
          'Le passé antérieur', n=4)),
      ),

    # ------------------------------------------------------------ 14 octobre
    L(FR, 'Le 1er groupe aux temps simples de l’indicatif', CONJ, '2026-10-14',
      'Les verbes du 1er groupe sont des verbes réguliers. Au présent : e, es, e, ons, ez, ent. '
      'Au futur simple on garde l’infinitif : ai, as, a, ons, ez, ont. À l’imparfait : ais, ais, '
      'ait, ions, iez, aient. Au passé simple : ai, as, a, âmes, âtes, èrent.',
      'bf-p1-couv', ['je chante', 'je chantais', 'je chanterai', 'je chantai'],

      N('liste',
        'Au présent de l’indicatif, on ajoute au radical les terminaisons e, es, e, ons, ez, '
        'ent. Je chante, tu chantes, il chante, nous chantons.',
        'bf-p1-present', F('Le présent', 'je chante, tu chantes', 'il chante',
                           'nous chantons, vous chantez', 'ils chantent'),
        ('simple', 'Le radical, c’est le verbe sans er : chant. On colle la terminaison '
                   'derrière.'),
        ('visuel', 'Avec tu il y a toujours un s : tu chantes, tu jettes, tu pollues.'),
        Q('Complète au présent : « tu … ».', 'chantes', 'chante', 'chantent'),
        V('Au présent, on écrit « ils chantent » avec ent.', True),
        T('Au présent : vous jetez vos déchets, vous {{1}} le climat. (polluer)', 'polluez'),
        Q('Quelle est la terminaison du présent avec nous ?', 'ons', 'ez', 'ent', n=3),
        V('Au présent, on écrit « tu chante » sans s.', False, n=4, e='Non : tu chantes.')),

      N('liste',
        'Au futur simple, on récrit le verbe à l’infinitif et on ajoute les terminaisons ai, as, '
        'a, ons, ez, ont. Nous chanterons, vous chanterez.',
        'bf-p1-futur', F('Le futur simple', 'je chanterai, tu chanteras', 'il chantera',
                         'nous chanterons', 'vous chanterez, ils chanteront'),
        ('simple', 'On garde tout l’infinitif : chanter + ai donne chanterai.'),
        ('pas_a_pas', 'Écris chanter. Ajoute ons. Tu as nous chanterons.'),
        Q('Complète au futur simple : « nous … ».', 'chanterons', 'chantons', 'chantions'),
        V('Au futur simple, on garde l’infinitif du verbe.', True),
        T('Au futur simple : demain, vous {{1}}. (chanter)', 'chanterez'),
        Q('Quelle est la terminaison du futur simple avec ils ?', 'ont', 'ent', 'aient', n=3),
        V('« Je chanterai » est au futur simple.', True, n=4)),

      N('liste',
        'À l’imparfait de l’indicatif, on ajoute au radical les terminaisons ais, ais, ait, '
        'ions, iez, aient. Je chantais, vous chantiez, ils chantaient.',
        'bf-p1-imparfait', F('L’imparfait', 'je chantais, tu chantais', 'il chantait',
                             'nous chantions, vous chantiez', 'ils chantaient'),
        ('simple', 'L’imparfait raconte ce qui durait dans le passé : autrefois, je chantais.'),
        ('visuel', 'Avec ils, la terminaison est longue : aient. Ses yeux lui mangeaient le '
                   'visage.'),
        Q('Complète à l’imparfait : « ils … ».', 'chantaient', 'chantent', 'chantèrent'),
        V('À l’imparfait, on écrit « vous chantiez ».', True),
        T('À l’imparfait : ses grands yeux noirs lui {{1}} le visage. (manger)', 'mangeaient',
          e='Mangeaient : on garde le e après le g pour que le son reste doux.'),
        Q('Quelle est la terminaison de l’imparfait avec nous ?', 'ions', 'ons', 'âmes', n=3),
        V('« Il chantait » est au passé simple.', False, n=4, e='Non. C’est l’imparfait.')),

      N('liste',
        'Au passé simple, on ajoute au radical les terminaisons ai, as, a, âmes, âtes, èrent. Je '
        'chantai, il chanta, nous chantâmes, ils chantèrent.',
        'bf-p1-passe', F('Le passé simple', 'je chantai, tu chantas', 'il chanta',
                         'nous chantâmes, vous chantâtes', 'ils chantèrent', vif=(1, 3)),
        ('simple', 'Le passé simple tient en UN mot : il voyagea. « Il a voyagé » a deux mots : '
                   'c’est le passé composé.'),
        ('pas_a_pas', 'Prends le radical : achet. Avec elles, ajoute èrent : elles achetèrent.'),
        Q('Mets au passé simple : « elles (acheter) un appartement ».', 'achetèrent',
          'ont acheté', 'achetaient'),
        Q('Mets au passé simple : « il (voyager) tôt le matin ».', 'voyagea', 'a voyagé',
          'voyageait'),
        V('« Il a voyagé » est au passé simple.', False,
          e='Non. Deux mots : c’est le passé composé. Au passé simple : il voyagea.'),
        T('Au passé simple : elles {{1}} un appartement. (acheter)', 'achetèrent'),
        T('Au passé simple : il {{1}} tôt le matin. (voyager)', 'voyagea'),
        A('Relie chaque forme à son temps.', ('il chanta', 'passé simple'),
          ('il a chanté', 'passé composé'), ('il chantait', 'imparfait')),
        Q('Laquelle de ces formes est au passé simple ?', 'ils chantèrent', 'ils ont chanté',
          'ils chantaient', n=4),
        V('Au passé simple, on écrit « nous chantâmes ».', True, n=4)),
      ),

    # ------------------------------------------------------------ 22 octobre
    L(FR, 'Le 2e groupe aux temps simples de l’indicatif', CONJ, '2026-10-22',
      'Les verbes du 2e groupe se conjuguent comme finir. Au présent : is, is, it, issons, '
      'issez, issent. Au futur simple on garde l’infinitif. À l’imparfait : issais, issais, '
      'issait, issions, issiez, issaient. Au passé simple : is, is, it, îmes, îtes, irent.',
      'bf-p2-couv', ['je finis', 'je finissais', 'je finirai', 'ils finirent'],

      N('liste',
        'Au présent, on enlève ir et on ajoute is, is, it, issons, issez, issent. Je finis, nous '
        'finissons, ils finissent.',
        'bf-p2-present', F('Le présent', 'je finis, tu finis', 'il finit',
                           'nous finissons, vous finissez', 'ils finissent'),
        ('simple', 'Au pluriel, le 2e groupe ajoute toujours iss : finissons, finissez, '
                   'finissent.'),
        ('visuel', 'Les spectateurs applaudissent : applaud + issent.'),
        Q('Complète au présent : « nous … ».', 'finissons', 'finons', 'finirons'),
        V('Au présent, on écrit « ils finissent ».', True),
        T('Au présent : les spectateurs {{1}} le lion. (applaudir)', 'applaudissent'),
        Q('Les verbes du 2e groupe se conjuguent comme…', 'finir', 'chanter', 'aller', n=3),
        V('Au présent, on écrit « nous finons ».', False, n=4, e='Non : nous finissons.')),

      N('liste',
        'Au futur simple, on ne change rien à l’infinitif et on ajoute ai, as, a, ons, ez, ont. '
        'Je finirai, nous finirons, ils finiront.',
        'bf-p2-futur', F('Le futur simple', 'je finirai, tu finiras', 'il finira',
                         'nous finirons, vous finirez', 'ils finiront'),
        ('simple', 'Finir + ai donne finirai. L’infinitif reste entier.'),
        ('visuel', 'Ne confonds pas : nous finissons, c’est maintenant ; nous finirons, c’est '
                   'demain.'),
        Q('Complète au futur simple : « ils … ».', 'finiront', 'finissent', 'finirent'),
        V('« Je finirai » est au futur simple.', True),
        T('Au futur simple : demain, nous {{1}} le travail. (finir)', 'finirons'),
        Q('Laquelle de ces formes est au futur simple ?', 'tu finiras', 'tu finis',
          'tu finissais', n=3),
        V('« Nous finissons » est au futur simple.', False, n=4, e='Non. C’est le présent.')),

      N('liste',
        'À l’imparfait, on enlève ir et on ajoute issais, issais, issait, issions, issiez, '
        'issaient. Je bondissais, nous bondissions, ils bondissaient.',
        'bf-p2-imparfait', F('L’imparfait', 'je bondissais, tu bondissais', 'il bondissait',
                             'nous bondissions', 'vous bondissiez, ils bondissaient'),
        ('simple', 'À l’imparfait du 2e groupe, le iss est là à toutes les personnes.'),
        ('visuel', 'Bond + issais : je bondissais.'),
        Q('Complète à l’imparfait : « il … ».', 'bondissait', 'bondit', 'bondira'),
        V('À l’imparfait, on écrit « nous bondissions ».', True),
        T('À l’imparfait : autrefois, je {{1}} très haut. (bondir)', 'bondissais'),
        Q('Quelle est la terminaison de l’imparfait du 2e groupe avec ils ?', 'issaient',
          'issent', 'irent', n=3),
        V('« Il bondissait » est à l’imparfait.', True, n=4)),

      N('liste',
        'Au passé simple, on enlève ir et on ajoute is, is, it, îmes, îtes, irent. J’applaudis, '
        'il applaudit, nous applaudîmes, ils applaudirent.',
        'bf-p2-passe', F('Le passé simple', 'j’applaudis, tu applaudis', 'il applaudit',
                         'nous applaudîmes', 'vous applaudîtes, ils applaudirent', vif=(3, 4)),
        ('simple', 'Au singulier, le passé simple ressemble au présent : il finit. C’est le '
                   'pluriel qui change.'),
        ('visuel', 'Ils applaudissent, c’est maintenant. Ils applaudirent, c’était hier, dans '
                   'une histoire.'),
        Q('Complète au passé simple : « ils … ».', 'applaudirent', 'applaudissent',
          'ont applaudi'),
        V('Au passé simple, on écrit « nous applaudîmes ».', True),
        T('Au passé simple : les spectateurs {{1}} longtemps. (applaudir)', 'applaudirent'),
        A('Relie chaque forme à son temps.', ('ils finissent', 'présent'),
          ('ils finirent', 'passé simple'), ('ils finiront', 'futur simple')),
        Q('Laquelle de ces formes est au passé simple ?', 'vous applaudîtes',
          'vous applaudissez', 'vous avez applaudi', n=4),
        V('« Ils ont applaudi » est au passé simple.', False, n=4,
          e='Non. Deux mots : c’est le passé composé.')),
      ),

    # ------------------------------------------------------------ 26 octobre
    L(FR, 'Le 1er groupe aux temps composés de l’indicatif', CONJ, '2026-10-26',
      'Les temps composés se forment toujours avec deux mots : l’auxiliaire, être ou avoir, et '
      'le participe passé du verbe. Passé composé : j’ai mangé. Futur antérieur : tu auras '
      'dansé. Plus-que-parfait : elle était tombée. Passé antérieur : j’eus mangé.',
      'bf-c1-couv', ['j’ai mangé', 'j’avais mangé', 'j’aurai mangé'],

      N('definition',
        'Les temps composés se forment toujours avec deux mots : l’auxiliaire, être ou avoir, '
        'et le participe passé du verbe à conjuguer.',
        'bf-c1-deux', P('Deux mots', ('l’auxiliaire', 'ai'), ('le participe passé', 'mangé')),
        ('simple', 'L’auxiliaire, c’est être ou avoir. Le participe passé du 1er groupe finit '
                   'par é.'),
        ('visuel', 'J’ai mangé : ai est l’auxiliaire avoir, mangé est le participe passé.'),
        Q('Avec combien de mots se forme un temps composé ?', 'Deux', 'Un seul', 'Quatre'),
        V('L’auxiliaire est toujours être ou avoir.', True),
        T('Un temps composé = l’auxiliaire + le {{1}} passé du verbe.', 'participe'),
        Q('Dans « nous avons mangé », quel mot est l’auxiliaire ?', 'avons', 'mangé', 'nous',
          n=3),
        V('Un temps composé s’écrit en un seul mot.', False, n=4, e='Non. Toujours deux mots.')),

      N('relation',
        'Le passé composé : l’auxiliaire au présent et le participe passé du verbe. J’ai mangé, '
        'nous avons mangé.',
        'bf-c1-pc', F('Le passé composé', 'auxiliaire au présent', '+ participe passé',
                      'j’ai mangé', 'nous avons mangé'),
        ('simple', 'Ai, as, a, avons, avez, ont : c’est avoir au présent. On ajoute mangé.'),
        ('visuel', 'Elles ont acheté : passé composé. Elles achetèrent : passé simple.'),
        Q('Au passé composé, l’auxiliaire est conjugué…', 'au présent', 'à l’imparfait',
          'au futur simple'),
        V('« Nous avons mangé » est au passé composé.', True),
        T('Au passé composé : j’{{1}} mangé.', 'ai'),
        Q('Laquelle de ces formes est au passé composé ?', 'elles ont acheté',
          'elles achetèrent', 'elles achetaient', n=3),
        V('« Il voyagea » est au passé composé.', False, n=4,
          e='Non. Un seul mot : c’est le passé simple.')),

      N('relation',
        'Le futur antérieur : l’auxiliaire au futur simple et le participe passé. Tu auras '
        'dansé, vous aurez dansé.',
        'bf-c1-fa', F('Le futur antérieur', 'auxiliaire au futur simple', '+ participe passé',
                      'tu auras dansé', 'vous aurez dansé'),
        ('simple', 'Aurai, auras, aura : c’est avoir au futur. On ajoute dansé.'),
        ('visuel', 'Tu danseras : futur simple, un mot. Tu auras dansé : futur antérieur, deux '
                   'mots.'),
        Q('Au futur antérieur, l’auxiliaire est conjugué…', 'au futur simple', 'au présent',
          'à l’imparfait'),
        V('« Vous aurez dansé » est au futur antérieur.', True),
        T('Au futur antérieur : tu {{1}} dansé.', 'auras'),
        Q('Laquelle de ces formes est au futur antérieur ?', 'tu auras dansé', 'tu danseras',
          'tu as dansé', n=3),
        V('« Tu danseras » est au futur antérieur.', False, n=4,
          e='Non. Un seul mot : c’est le futur simple.')),

      N('relation',
        'Le plus-que-parfait : l’auxiliaire à l’imparfait et le participe passé. Elle était '
        'tombée, ils étaient tombés.',
        'bf-c1-pqp', F('Le plus-que-parfait', 'auxiliaire à l’imparfait', '+ participe passé',
                       'elle était tombée', 'ils étaient tombés'),
        ('simple', 'Était, c’est être à l’imparfait. On ajoute tombée.'),
        ('visuel', 'Avec être, le participe s’accorde : elle était tombée, ils étaient tombés.'),
        Q('Au plus-que-parfait, l’auxiliaire est conjugué…', 'à l’imparfait', 'au présent',
          'au passé simple'),
        V('« Elle était tombée » est au plus-que-parfait.', True),
        T('Au plus-que-parfait : ils {{1}} tombés.', 'étaient'),
        Q('Laquelle de ces formes est au plus-que-parfait ?', 'elle était tombée',
          'elle est tombée', 'elle tombait', n=3),
        V('« Elle est tombée » est au plus-que-parfait.', False, n=4,
          e='Non. Est, c’est le présent : passé composé.')),

      N('relation',
        'Le passé antérieur : l’auxiliaire au passé simple et le participe passé. J’eus mangé, '
        'nous eûmes mangé, ils eurent mangé.',
        'bf-c1-pa', F('Le passé antérieur', 'auxiliaire au passé simple', '+ participe passé',
                      'j’eus mangé', 'ils eurent mangé'),
        ('simple', 'Eus, eut, eurent : c’est avoir au passé simple. On ajoute mangé.'),
        ('visuel', 'Eus se prononce « u ». J’eus mangé se dit « j’u mangé ».'),
        Q('Au passé antérieur, l’auxiliaire est conjugué…', 'au passé simple', 'à l’imparfait',
          'au futur simple'),
        V('« Ils eurent mangé » est au passé antérieur.', True),
        T('Au passé antérieur : ils {{1}} mangé.', 'eurent'),
        A('Relie chaque forme à son temps.', ('j’ai mangé', 'passé composé'),
          ('j’avais mangé', 'plus-que-parfait'), ('j’aurai mangé', 'futur antérieur'),
          ('j’eus mangé', 'passé antérieur')),
        V('« J’eus mangé » est au passé antérieur.', True, n=4),
        Q('Laquelle de ces formes est au passé antérieur ?', 'ils eurent mangé',
          'ils avaient mangé', 'ils ont mangé', n=4)),
      ),

    # ------------------------------------------------------------ 27 octobre
    L(FR, 'Être et avoir aux temps simples de l’indicatif', CONJ, '2026-10-27',
      'Les auxiliaires être et avoir se conjuguent aux quatre temps simples. Être : je suis, '
      'j’étais, je serai, je fus. Avoir : j’ai, j’avais, j’aurai, j’eus.',
      'bf-ea-couv', ['je suis', 'j’étais', 'j’ai', 'j’avais'],

      N('liste',
        'Être au présent : je suis, tu es, il est, nous sommes, vous êtes, ils sont. À '
        'l’imparfait : j’étais, tu étais, il était, nous étions, vous étiez, ils étaient.',
        'bf-ea-etre1', P('Être', ('je suis', 'j’étais'), ('il est', 'il était'),
                         ('nous sommes', 'nous étions'), ('ils sont', 'ils étaient')),
        ('simple', 'Le présent dit ce qui est maintenant, l’imparfait ce qui était avant.'),
        ('visuel', 'La forêt est verdoyante : est, c’est être au présent.'),
        Q('Complète avec être au présent : « nous … ».', 'sommes', 'sont', 'êtes'),
        V('« Ils étaient » est le verbe être à l’imparfait.', True),
        T('Être au présent : ils {{1}}.', 'sont'),
        T('Être à l’imparfait : nous {{1}}.', 'étions', n=3),
        Q('Complète avec être à l’imparfait : « vous … ».', 'étiez', 'êtes', 'serez', n=4)),

      N('liste',
        'Être au futur simple : je serai, tu seras, il sera, nous serons, vous serez, ils '
        'seront. Au passé simple : je fus, tu fus, il fut, nous fûmes, vous fûtes, ils furent.',
        'bf-ea-etre2', P('Être', ('je serai', 'je fus'), ('il sera', 'il fut'),
                         ('nous serons', 'nous fûmes'), ('ils seront', 'ils furent')),
        ('simple', 'Au futur, être commence par ser. Au passé simple, il commence par fu.'),
        ('visuel', 'Il fut roi : c’est être au passé simple, dans une histoire.'),
        Q('Complète avec être au futur simple : « ils … ».', 'seront', 'sont', 'furent'),
        V('« Il fut » est le verbe être au passé simple.', True),
        T('Être au futur simple : nous {{1}}.', 'serons'),
        T('Être au passé simple : ils {{1}}.', 'furent', n=3),
        Q('« Je fus » est le verbe être…', 'au passé simple', 'au futur simple', 'au présent',
          n=4)),

      N('liste',
        'Avoir au présent : j’ai, tu as, il a, nous avons, vous avez, ils ont. À l’imparfait : '
        'j’avais, tu avais, il avait, nous avions, vous aviez, ils avaient.',
        'bf-ea-avoir1', P('Avoir', ('j’ai', 'j’avais'), ('il a', 'il avait'),
                          ('nous avons', 'nous avions'), ('ils ont', 'ils avaient')),
        ('simple', 'Il a une montre aujourd’hui. Il avait une montre autrefois.'),
        ('visuel', 'Ils ont, c’est avoir. Ils sont, c’est être. Une seule lettre les sépare.'),
        Q('Complète avec avoir au présent : « ils … ».', 'ont', 'sont', 'avaient'),
        V('« Nous avions » est le verbe avoir à l’imparfait.', True),
        T('Avoir au présent : vous {{1}}.', 'avez'),
        T('Avoir à l’imparfait : ils {{1}}.', 'avaient', n=3),
        V('« Ils sont » est le verbe avoir au présent.', False, n=4,
          e='Non. Ils sont, c’est être. Avoir : ils ont.')),

      N('liste',
        'Avoir au futur simple : j’aurai, tu auras, il aura, nous aurons, vous aurez, ils '
        'auront. Au passé simple : j’eus, tu eus, il eut, nous eûmes, vous eûtes, ils eurent.',
        'bf-ea-avoir2', P('Avoir', ('j’aurai', 'j’eus'), ('il aura', 'il eut'),
                          ('nous aurons', 'nous eûmes'), ('ils auront', 'ils eurent')),
        ('simple', 'Au futur, avoir commence par aur. Au passé simple, il s’écrit eu et se dit '
                   '« u ».'),
        ('visuel', 'Il aura une belle montre : c’est avoir au futur simple.'),
        Q('Complète avec avoir au futur simple : « nous … ».', 'aurons', 'avons', 'avions'),
        V('« Ils eurent » est le verbe avoir au passé simple.', True),
        T('Avoir au futur simple : ils {{1}}.', 'auront'),
        A('Relie chaque forme à son verbe.', ('ils furent', 'être'), ('ils eurent', 'avoir'),
          ('ils seront', 'être aussi'), ('ils auront', 'avoir aussi')),
        Q('« Il eut » est le verbe avoir…', 'au passé simple', 'à l’imparfait',
          'au futur simple', n=4)),
      ),

    # ------------------------------------------------------------ 28 octobre
    L(FR, 'Le 2e groupe aux temps composés de l’indicatif', CONJ, '2026-10-28',
      'Les verbes du 2e groupe se conjuguent aux temps composés avec l’auxiliaire avoir ou '
      'être et le participe passé. Passé composé : j’ai fini. Plus-que-parfait : j’avais '
      'applaudi. Futur antérieur : j’aurai grandi. Passé antérieur : elle eut choisi.',
      'bf-c2-couv', ['j’ai fini', 'j’avais fini', 'j’aurai fini'],

      N('relation',
        'Passé composé : l’auxiliaire avoir ou être au présent de l’indicatif et le participe '
        'passé du verbe. J’ai fini, nous avons fini.',
        'bf-c2-pc', F('Le passé composé', 'auxiliaire au présent', '+ participe passé',
                      'j’ai fini', 'nous avons fini'),
        ('simple', 'Le participe passé du 2e groupe finit par i : fini, applaudi, grandi, '
                   'choisi.'),
        ('visuel', 'J’ai fini : ai est au présent, fini est le participe passé.'),
        Q('Quel est le participe passé du verbe finir ?', 'fini', 'finir', 'finissant'),
        V('« Nous avons fini » est au passé composé.', True),
        T('Au passé composé : j’ai {{1}}. (finir)', 'fini'),
        Q('Laquelle de ces formes est au passé composé ?', 'nous avons fini', 'nous finîmes',
          'nous finissions', n=3),
        V('Le participe passé de finir s’écrit « finit ».', False, n=4,
          e='Non : fini, sans t. « Il finit » est le verbe conjugué.')),

      N('relation',
        'Le plus-que-parfait : l’auxiliaire avoir ou être à l’imparfait et le participe passé. '
        'J’avais applaudi, vous aviez applaudi.',
        'bf-c2-pqp', F('Le plus-que-parfait', 'auxiliaire à l’imparfait', '+ participe passé',
                       'j’avais applaudi', 'vous aviez applaudi'),
        ('simple', 'Avais, avait, aviez : c’est avoir à l’imparfait. On ajoute applaudi.'),
        ('visuel', 'J’ai applaudi : passé composé. J’avais applaudi : plus-que-parfait.'),
        Q('Complète au plus-que-parfait : « vous … applaudi ».', 'aviez', 'avez', 'aurez'),
        V('« J’avais applaudi » est au plus-que-parfait.', True),
        T('Au plus-que-parfait : j’{{1}} applaudi.', 'avais'),
        Q('Laquelle de ces formes est au plus-que-parfait ?', 'vous aviez applaudi',
          'vous avez applaudi', 'vous applaudissiez', n=3),
        V('« Vous avez applaudi » est au plus-que-parfait.', False, n=4,
          e='Non. Avez est au présent : passé composé.')),

      N('relation',
        'Le futur antérieur : l’auxiliaire avoir ou être au futur simple et le participe '
        'passé. J’aurai grandi, ils auront grandi.',
        'bf-c2-fa', F('Le futur antérieur', 'auxiliaire au futur simple', '+ participe passé',
                      'j’aurai grandi', 'ils auront grandi'),
        ('simple', 'Aurai, auront : c’est avoir au futur. On ajoute grandi.'),
        ('visuel', 'Ils grandiront : un mot, futur simple. Ils auront grandi : deux mots, futur '
                   'antérieur.'),
        Q('Complète au futur antérieur : « ils … grandi ».', 'auront', 'ont', 'avaient'),
        V('« J’aurai grandi » est au futur antérieur.', True),
        T('Au futur antérieur : ils {{1}} grandi.', 'auront'),
        Q('Laquelle de ces formes est au futur antérieur ?', 'j’aurai grandi', 'je grandirai',
          'j’ai grandi', n=3),
        V('« Ils grandiront » est au futur antérieur.', False, n=4,
          e='Non. Un seul mot : c’est le futur simple.')),

      N('relation',
        'Le passé antérieur : l’auxiliaire avoir ou être au passé simple et le participe '
        'passé. Elle eut choisi, nous eûmes choisi.',
        'bf-c2-pa', F('Le passé antérieur', 'auxiliaire au passé simple', '+ participe passé',
                      'elle eut choisi', 'nous eûmes choisi'),
        ('simple', 'Eut, eûmes : c’est avoir au passé simple. On ajoute choisi.'),
        ('visuel', 'Elle choisit : passé simple, un mot. Elle eut choisi : passé antérieur, '
                   'deux mots.'),
        Q('Complète au passé antérieur : « elle … choisi ».', 'eut', 'a', 'avait'),
        V('« Elle eut choisi » est au passé antérieur.', True),
        T('Au passé antérieur : elle {{1}} choisi.', 'eut'),
        A('Relie chaque forme à son temps.', ('j’ai fini', 'passé composé'),
          ('j’avais fini', 'plus-que-parfait'), ('j’aurai fini', 'futur antérieur'),
          ('j’eus fini', 'passé antérieur')),
        Q('Laquelle de ces formes est au passé antérieur ?', 'elle eut choisi',
          'elle avait choisi', 'elle a choisi', n=4)),
      ),
]
