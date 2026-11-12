# -*- coding: utf-8 -*-
# Histoire-Géographie — six leçons. Chargé par lecons-brayne-cahier-nov12.py.
#
# CE QUI NE SE LISAIT PAS SUR LA PHOTO a été complété le 12 novembre, à la
# demande du père, depuis le thème de la leçon — et seulement par ce qui est
# sûr : l'ordre de l'abolition sans ses dates, le dieu Komba, les conséquences
# de la surpopulation que donnent tous les manuels. Reste non posé :
#   - les Européens sur la côte : le siècle où Anglais, Français et Allemands
#     rejoignent les Portugais (XIIe ou XVIIe sur la photo) ;
#   - les dates exactes de l'abolition.

HG = 'Histoire-Géographie'
HIST = 'Histoire'
GEO = 'Géographie'

LECONS = [
    # -------------------------------------------------------------- 20 octobre
    L(HG, 'La traite négrière', HIST, '2026-10-20',
      'La traite négrière est le commerce des esclaves noirs. Il se faisait en triangle entre '
      'l’Europe, l’Afrique et l’Amérique : c’est le commerce triangulaire. L’Afrique y a perdu '
      'ses hommes et ses richesses ; l’Europe et l’Amérique s’y sont enrichies.',
      'bn-traite-couv', ['l’Europe', 'l’Afrique', 'l’Amérique'],

      N('definition',
        'La traite négrière est le commerce des esclaves noirs.',
        'bn-traite-def', F('La traite négrière', 'le commerce', 'des esclaves noirs'),
        ('simple', 'Des hommes, des femmes et des enfants noirs étaient vendus et achetés comme '
                   'des marchandises.'),
        ('visuel', 'Des bateaux emportaient les captifs loin de chez eux, enchaînés.'),
        Q('Qu’est-ce que la traite négrière ?', 'Le commerce des esclaves noirs',
          'Le commerce du café', 'Une fête traditionnelle'),
        V('La traite négrière est le commerce des esclaves noirs.', True),
        T('La traite négrière est le commerce des {{1}} noirs.', 'esclaves'),
        Q('Dans la traite négrière, que vendait-on ?', 'des êtres humains', 'des tissus',
          'des armes', n=3),
        V('La traite négrière est le commerce de l’ivoire.', False, n=4,
          e='Non. C’est le commerce des esclaves noirs.')),

      N('relation',
        'Ce commerce se faisait en triangle entre trois continents, l’Europe, l’Afrique et '
        'l’Amérique : c’est le commerce triangulaire. Les esclaves partaient d’Afrique vers '
        'l’Amérique.',
        'bn-traite-triangle', F('Le commerce triangulaire', 'l’Europe', 'l’Afrique',
                                'l’Amérique', 'trois continents'),
        ('visuel', 'Trace un triangle : un coin en Europe, un en Afrique, un en Amérique. Les '
                   'bateaux faisaient le tour.'),
        ('pas_a_pas', 'Les bateaux partent d’Europe, chargent des esclaves en Afrique, les '
                      'emmènent en Amérique, puis rentrent en Europe.'),
        Q('Entre combien de continents se faisait la traite négrière ?', 'trois', 'deux',
          'cinq'),
        V('On parle de commerce triangulaire.', True),
        T('On l’appelle le commerce {{1}}, car il dessine un triangle.', 'triangulaire'),
        Q('De quel continent partaient les esclaves ?', 'l’Afrique', 'l’Europe', 'l’Amérique',
          n=3),
        V('Les esclaves partaient d’Afrique vers l’Amérique.', True, n=4),
        Q('Lequel ne fait pas partie du triangle ?', 'l’Asie', 'l’Afrique', 'l’Europe', n=4)),

      N('liste',
        'Pour l’Afrique, la traite négrière a entraîné la désorganisation des sociétés, le '
        'dépeuplement, l’appauvrissement du continent et la séparation des familles.',
        'bn-traite-afrique', F('Pour l’Afrique', 'la désorganisation', 'le dépeuplement',
                               'l’appauvrissement', 'la séparation des familles'),
        ('simple', 'L’Afrique a perdu ses forces : moins d’hommes pour cultiver, des familles '
                   'brisées.'),
        ('visuel', 'Un village dont on a emmené les jeunes : les champs restent vides.'),
        Q('Quelle conséquence la traite a-t-elle eue pour l’Afrique ?', 'le dépeuplement',
          'l’enrichissement', 'le développement'),
        V('La traite a séparé des familles africaines.', True),
        T('La traite a entraîné le {{1}} de l’Afrique : moins d’habitants.', 'dépeuplement'),
        Q('Laquelle n’est pas une conséquence pour l’Afrique ?', 'l’enrichissement',
          'l’appauvrissement', 'la désorganisation des sociétés', n=3),
        V('La traite a enrichi l’Afrique.', False, n=4,
          e='Non. Elle a appauvri l’Afrique et enrichi l’Europe et l’Amérique.')),

      N('relation',
        'Pour l’Amérique et l’Europe, la traite a apporté l’enrichissement et le développement '
        'sur le plan économique et social.',
        'bn-traite-europe', P('Qui a gagné, qui a perdu', ('l’Afrique', 'appauvrie'),
                              ('l’Europe', 'enrichie'), ('l’Amérique', 'enrichie')),
        ('simple', 'Ce que l’Afrique a perdu, l’Europe et l’Amérique l’ont gagné.'),
        ('analogie', 'Le travail des esclaves a fait la richesse des autres.'),
        Q('Qu’a apporté la traite à l’Europe et à l’Amérique ?', 'l’enrichissement',
          'le dépeuplement', 'l’appauvrissement'),
        V('La traite a aidé au développement de l’Europe et de l’Amérique.', True),
        T('Pour l’Europe et l’Amérique, la traite a apporté l’{{1}}.', 'enrichissement'),
        A('Relie chaque continent à ce que la traite lui a fait.',
          ('l’Afrique', 'le dépeuplement'), ('l’Europe', 'l’enrichissement'), n=3),
        V('L’Europe s’est appauvrie à cause de la traite.', False, n=4,
          e='Non. L’Europe s’est enrichie ; c’est l’Afrique qui s’est appauvrie.')),

      # Les dates de la photo sont floues : on garde ce qui s'y lit sûrement,
      # l'ordre — l'Angleterre d'abord, le reste du monde, le Cameroun en
      # dernier — et le nom de Lord Mansfield, sans poser de date.
      N('relation',
        'Cet odieux commerce a été aboli : d’abord en Angleterre, par Lord Mansfield, puis dans '
        'le reste du monde, et enfin au Cameroun.',
        'bn-traite-abolition', F('L’abolition', '1. en Angleterre', '2. dans le reste du monde',
                                 '3. au Cameroun'),
        ('simple', 'Abolir, c’est interdire pour toujours. La traite négrière est interdite.'),
        ('pas_a_pas', 'D’abord l’Angleterre, ensuite le reste du monde, enfin le Cameroun.'),
        Q('Que veut dire « abolir » la traite ?', 'L’interdire pour toujours',
          'La rendre plus rapide', 'La payer plus cher'),
        V('La traite négrière a été abolie.', True),
        T('La traite a d’abord été {{1}} en Angleterre.', 'abolie'),
        C('Remets dans l’ordre l’abolition de la traite.', 'en Angleterre',
          'dans le reste du monde', 'au Cameroun', n=3),
        Q('Qui a aboli la traite en Angleterre ?', 'Lord Mansfield', 'Fernando Poo',
          'Christophe Colomb', n=4),
        V('Le Cameroun a été le premier pays à abolir la traite.', False, n=4,
          e='Non. L’Angleterre d’abord ; le Cameroun vient en dernier.'))),

    # -------------------------------------------------------------- 21 octobre
    L(HG, 'Présentation générale du Cameroun', GEO, '2026-10-21',
      'Le Cameroun est en Afrique centrale, un peu au-dessus de l’équateur, entre le 2e et le '
      '13e degré de latitude Nord et le 9e et le 16e degré de longitude Est. Il a la forme d’un '
      'triangle : 475 650 km². Ses voisins sont le Tchad, la RCA, le Nigeria, le Gabon, le '
      'Congo et la Guinée équatoriale.',
      'bn-pres-couv', ['Afrique centrale', 'triangle', 'voisins'],

      N('definition',
        'Le Cameroun est situé en Afrique centrale, un peu au-dessus de l’équateur.',
        'bn-pres-situation', F('Le Cameroun', 'en Afrique centrale',
                               'un peu au-dessus', 'de l’équateur'),
        ('simple', 'Sur la carte de l’Afrique, le Cameroun est au milieu, juste au-dessus de la '
                   'ligne de l’équateur.'),
        ('visuel', 'Pose le doigt sur l’équateur, et monte un tout petit peu : tu es au '
                   'Cameroun.'),
        Q('Où est situé le Cameroun ?', 'En Afrique centrale', 'En Afrique du Nord',
          'En Europe'),
        V('Le Cameroun est un peu au-dessus de l’équateur.', True),
        T('Le Cameroun est situé en Afrique {{1}}.', 'centrale'),
        Q('Par rapport à l’équateur, le Cameroun est…', 'un peu au-dessus', 'très loin au sud',
          'juste en dessous', n=3),
        V('Le Cameroun est en Afrique de l’Ouest, sous l’équateur.', False, n=4,
          e='Non. Il est en Afrique centrale, un peu au-dessus de l’équateur.')),

      N('relation',
        'Le Cameroun est entre le 2e et le 13e degré de latitude Nord, et entre le 9e et le 16e '
        'degré de longitude Est.',
        'bn-pres-degres', P('Entre quels degrés', ('latitude Nord', '2e et 13e'),
                            ('longitude Est', '9e et 16e')),
        ('simple', 'La latitude dit à quelle hauteur on est ; la longitude, à quelle distance '
                   'vers l’est.'),
        ('pas_a_pas', 'Latitude : de 2 à 13 degrés Nord. Longitude : de 9 à 16 degrés Est.'),
        Q('Entre quelles latitudes est le Cameroun ?', 'entre 2° et 13° Nord',
          'entre 9° et 16° Nord', 'entre 2° et 13° Sud'),
        V('Le Cameroun est entre le 9e et le 16e degré de longitude Est.', True),
        T('Le Cameroun est entre le 2e et le {{1}}e degré de latitude Nord.', '13'),
        T('Le Cameroun est entre le 9e et le {{1}}e degré de longitude Est.', '16', n=3),
        V('Le Cameroun est entre le 2e et le 13e degré de longitude Est.', False, n=4,
          e='Non. 2e et 13e, c’est la latitude Nord. La longitude Est va du 9e au 16e.'),
        Q('La longitude du Cameroun va du 9e au…', '16e degré Est', '13e degré Est',
          '2e degré Est', n=4)),

      N('relation',
        'Le Cameroun a la forme d’un triangle de 1 200 km de hauteur et de 800 km de base.',
        'bn-pres-triangle', F('Un triangle', '1 200 km de hauteur', '800 km de base'),
        ('visuel', 'Regarde la carte : large en bas, pointue en haut vers le lac Tchad, comme '
                   'un triangle.'),
        ('simple', 'Du sud au nord, 1 200 km ; à la base, 800 km.'),
        Q('Quelle forme a le Cameroun ?', 'un triangle', 'un carré', 'un cercle'),
        V('Le Cameroun mesure 1 200 km de hauteur.', True),
        T('Le Cameroun a une base de {{1}} km.', '800'),
        Q('Combien mesure le Cameroun en hauteur ?', '1 200 km', '800 km', '475 km', n=3),
        V('Le Cameroun a 1 200 km de base et 800 km de hauteur.', False, n=4,
          e='Non. C’est l’inverse : 1 200 km de hauteur, 800 km de base.')),

      N('relation',
        'Le Cameroun a une superficie de 475 650 km² : 466 050 km² de terre ferme et 9 600 km² '
        'occupés par l’eau.',
        'bn-pres-superficie', F('La superficie', '475 650 km carrés en tout',
                                '466 050 de terre ferme', '9 600 occupés par l’eau'),
        ('pas_a_pas', '466 050 de terre, plus 9 600 d’eau : cela fait 475 650 km².'),
        ('simple', 'Presque tout le Cameroun est de la terre ferme ; un petit morceau est de '
                   'l’eau.'),
        Q('Quelle est la superficie du Cameroun ?', '475 650 km²', '466 050 km²', '9 600 km²'),
        V('La plus grande partie du Cameroun est de la terre ferme.', True),
        T('L’eau occupe {{1}} km² du Cameroun.', '9600'),
        Q('Combien de km² de terre ferme le Cameroun a-t-il ?', '466 050 km²', '475 650 km²',
          '9 600 km²', n=3),
        V('L’eau occupe plus de place que la terre ferme au Cameroun.', False, n=4,
          e='Non. 9 600 km² d’eau contre 466 050 km² de terre ferme.')),

      N('liste',
        'Les pays limitrophes du Cameroun sont le Tchad au nord, la République centrafricaine à '
        'l’est, le Nigeria à l’ouest, et au sud le Gabon, le Congo et la Guinée équatoriale.',
        'bn-pres-voisins', P('Les voisins', ('au nord', 'le Tchad'), ('à l’est', 'la RCA'),
                             ('à l’ouest', 'le Nigeria'), ('au sud', 'Gabon, Congo, Guinée')),
        ('simple', 'Limitrophe veut dire voisin : ces pays touchent le Cameroun.'),
        ('visuel', 'Sur la carte du cahier : le Tchad en haut, le Nigeria à gauche, la RCA à '
                   'droite, et trois pays en bas.'),
        Q('Quel pays est au nord du Cameroun ?', 'le Tchad', 'le Gabon', 'le Congo'),
        V('Le Nigeria est à l’ouest du Cameroun.', True),
        Q('Quel pays est à l’ouest du Cameroun ?', 'le Nigeria', 'le Tchad', 'le Gabon', n=2),
        A('Relie chaque direction à son voisin.', ('au nord', 'le Tchad'),
          ('à l’est', 'la République centrafricaine'), ('à l’ouest', 'le Nigeria'), n=3),
        Q('Lequel est un voisin du sud ?', 'la Guinée équatoriale', 'le Tchad', 'la République centrafricaine',
          n=4),
        V('Le Gabon est au nord du Cameroun.', False, n=4,
          e='Non. Le Gabon est au sud, avec le Congo et la Guinée équatoriale.'))),

    # -------------------------------------------------------------- 22 octobre
    L(HG, 'Les Pygmées', HIST, '2026-10-22',
      'Les Pygmées sont les premiers habitants de la forêt du Cameroun ; ils seraient venus '
      'd’Égypte. On les rencontre au Sud (Bipindi, Lolodorf) et à l’Est (Moloundou, Lomié). '
      'Organisés en familles, ils vivent de la chasse, de la pêche et de la cueillette.',
      'bn-pygmees-couv', ['la forêt', 'la chasse', 'la cueillette'],

      N('definition',
        'Les Pygmées sont les premiers habitants de la forêt du Cameroun. Ils seraient venus '
        'd’Égypte pour s’installer en Afrique centrale.',
        'bn-pygmees-def', F('Les Pygmées', 'les premiers habitants', 'de la forêt',
                            'venus d’Égypte'),
        ('simple', 'Avant tous les autres, les Pygmées vivaient déjà dans la forêt du '
                   'Cameroun.'),
        ('visuel', 'Une grande forêt, des cases de feuilles : c’est là que vivaient les '
                   'premiers habitants.'),
        Q('Qui sont les premiers habitants de la forêt du Cameroun ?', 'les Pygmées',
          'les Portugais', 'les Allemands'),
        V('Les Pygmées seraient venus d’Égypte.', True),
        T('Les Pygmées sont les premiers habitants de la {{1}} du Cameroun.', 'forêt'),
        Q('D’où les Pygmées seraient-ils venus ?', 'd’Égypte', 'd’Europe', 'd’Amérique', n=3),
        V('Les Pygmées sont arrivés au Cameroun après les Européens.', False, n=4,
          e='Non. Ce sont les premiers habitants de la forêt.')),

      N('liste',
        'On rencontre les Pygmées au Sud, à Bipindi et Lolodorf, et à l’Est, à Moloundou et '
        'Lomié.',
        'bn-pygmees-ou', P('Où les trouver', ('au Sud', 'Bipindi, Lolodorf'),
                           ('à l’Est', 'Moloundou, Lomié')),
        ('simple', 'Ils vivent là où il y a la grande forêt : au Sud et à l’Est.'),
        ('visuel', 'Sur la carte, regarde en bas et à droite : la forêt des Pygmées.'),
        Q('Dans quelles régions rencontre-t-on les Pygmées ?', 'au Sud et à l’Est',
          'au Nord et à l’Ouest', 'seulement au Littoral'),
        V('On rencontre des Pygmées à Lomié.', True),
        A('Relie chaque localité à sa région.', ('Bipindi', 'le Sud'), ('Moloundou', 'l’Est'),
          n=2),
        Q('Laquelle est une localité pygmée du Sud ?', 'Lolodorf', 'Moloundou', 'Lomié', n=3),
        V('Moloundou est au Sud.', False, n=4,
          e='Non. D’après le cahier, Moloundou et Lomié sont à l’Est.')),

      N('liste',
        'La société pygmée est organisée en familles. Elle vit de la chasse, de la pêche et de '
        'la cueillette.',
        'bn-pygmees-vie', F('La vie des Pygmées', 'en familles', 'la chasse', 'la pêche',
                            'la cueillette'),
        ('simple', 'Ils prennent ce que donne la forêt : le gibier, le poisson, les fruits.'),
        ('visuel', 'Le père chasse, les enfants pêchent, la mère cueille des fruits.'),
        Q('De quoi vivent les Pygmées ?', 'de la chasse, de la pêche et de la cueillette',
          'du commerce et de l’industrie', 'de l’élevage des bœufs'),
        V('La société pygmée est organisée en familles.', True),
        T('Les Pygmées vivent de la chasse, de la pêche et de la {{1}}.', 'cueillette'),
        Q('Ramasser des fruits dans la forêt, c’est…', 'la cueillette', 'la chasse',
          'la pêche', n=3),
        V('Les Pygmées vivent surtout de l’élevage.', False, n=4,
          e='Non. Ils vivent de la chasse, de la pêche et de la cueillette.')),

      # Le nom du dieu est illisible sur la photo. Komba est le dieu créateur
      # que les manuels du Cameroun donnent aux Pygmées.
      N('definition',
        'Les Pygmées croient en un dieu créateur appelé Komba. Ils respectent la forêt, qui les '
        'nourrit et les protège.',
        'bn-pygmees-komba', F('La croyance', 'un dieu créateur', 'appelé Komba',
                              'le respect de la forêt'),
        ('simple', 'Pour les Pygmées, la forêt est leur maison et leur garde-manger.'),
        ('visuel', 'Des chants et des danses au cœur de la forêt, pour remercier Komba.'),
        Q('Comment s’appelle le dieu des Pygmées ?', 'Komba', 'Ongola', 'Wouri'),
        V('Les Pygmées respectent la forêt.', True),
        T('Les Pygmées croient en un dieu {{1}} appelé Komba.', 'créateur'),
        Q('Pourquoi les Pygmées respectent-ils la forêt ?', 'Elle les nourrit et les protège',
          'Elle leur fait peur', 'Ils veulent la couper', n=3),
        V('Les Pygmées ne croient en aucun dieu.', False, n=4,
          e='Non. Ils croient en un dieu créateur, Komba.'))),

    # -------------------------------------------------------------- 27 octobre
    L(HG, 'Les grandes zones pastorales du Cameroun', GEO, '2026-10-27',
      'L’élevage consiste à prendre soin des animaux pour les vendre. Le gros bétail, les '
      'bovins, vit surtout sur le plateau de l’Adamaoua et dans les plaines du Nord. Le petit '
      'bétail : les chèvres au Nord, les moutons presque partout, les porcs à l’Ouest, au '
      'Centre et au Littoral ; la volaille dans toutes les régions.',
      'bn-elevage-couv', ['bovins', 'Adamaoua', 'volaille'],

      N('definition',
        'L’élevage est une activité économique qui consiste à prendre soin des animaux dans le '
        'but de les vendre.',
        'bn-elevage-def', F('L’élevage', 'prendre soin des animaux', 'pour les vendre'),
        ('simple', 'L’éleveur nourrit et soigne ses bêtes, puis il les vend.'),
        ('visuel', 'Le berger mène ses bœufs boire et manger, puis les conduit au marché.'),
        Q('Qu’est-ce que l’élevage ?', 'Prendre soin des animaux pour les vendre',
          'Cultiver des plantes', 'Pêcher en mer'),
        V('L’élevage est une activité économique.', True),
        T('L’élevage consiste à prendre soin des {{1}} pour les vendre.', 'animaux'),
        Q('Dans quel but l’éleveur prend-il soin de ses animaux ?', 'pour les vendre',
          'pour les relâcher', 'pour les dessiner', n=3),
        V('L’élevage consiste à cultiver le maïs.', False, n=4,
          e='Non. Ça, c’est l’agriculture. L’élevage s’occupe des animaux.')),

      N('relation',
        'Au Cameroun, on distingue l’élevage du gros bétail, les bovins (vache, bœuf, taureau, '
        'zébu), et l’élevage du petit bétail.',
        'bn-elevage-betail', P('Gros et petit bétail', ('gros bétail', 'les bovins'),
                               ('la vache, le zébu', 'gros bétail'),
                               ('la chèvre', 'petit bétail')),
        ('simple', 'Le gros bétail, ce sont les grosses bêtes : vaches, bœufs, zébus.'),
        ('analogie', 'Un zébu est bien plus gros qu’une chèvre : gros bétail, petit bétail.'),
        Q('Le gros bétail, ce sont…', 'les bovins', 'les poules', 'les porcs'),
        V('Le zébu fait partie du gros bétail.', True),
        T('Le gros bétail s’appelle aussi les {{1}}.', 'bovins'),
        Q('Lequel fait partie du gros bétail ?', 'le taureau', 'la chèvre', 'le mouton', n=3),
        V('La chèvre fait partie du gros bétail.', False, n=4,
          e='Non. La chèvre fait partie du petit bétail.')),

      N('relation',
        'L’élevage bovin est surtout pratiqué sur le plateau de l’Adamaoua et dans les plaines '
        'du Nord.',
        'bn-elevage-bovin', F('L’élevage bovin', 'le plateau de l’Adamaoua',
                              'les plaines du Nord'),
        ('simple', 'Les bœufs ont besoin de grands pâturages : on les trouve dans l’Adamaoua '
                   'et le Nord.'),
        ('visuel', 'De grandes prairies d’herbe sur un plateau : les troupeaux de zébus y '
                   'broutent.'),
        Q('Où l’élevage bovin est-il surtout pratiqué ?', 'sur le plateau de l’Adamaoua',
          'dans le Littoral', 'dans la forêt du Sud'),
        V('On élève beaucoup de bovins dans les plaines du Nord.', True),
        T('L’élevage bovin se pratique sur le {{1}} de l’Adamaoua.', 'plateau'),
        Q('Le plateau de l’Adamaoua est connu pour l’élevage…', 'bovin', 'porcin', 'avicole',
          n=3),
        V('L’élevage bovin se pratique surtout dans le Littoral.', False, n=4,
          e='Non. Il se pratique sur le plateau de l’Adamaoua et dans les plaines du Nord.')),

      N('relation',
        'L’élevage caprin (la chèvre) est pratiqué surtout au Nord, dans les monts Mandara. '
        'L’élevage ovin (le mouton) se fait presque dans tout le pays.',
        'bn-elevage-caprin', P('Chèvres et moutons', ('caprin', 'la chèvre'),
                               ('ovin', 'le mouton'), ('les monts Mandara', 'chèvres')),
        ('simple', 'Caprin pour la chèvre, ovin pour le mouton.'),
        ('analogie', 'Capri comme cabri, le petit de la chèvre : caprin.'),
        Q('L’élevage caprin, c’est l’élevage…', 'des chèvres', 'des moutons', 'des porcs'),
        V('L’élevage ovin se fait presque dans tout le pays.', True),
        T('L’élevage des moutons s’appelle l’élevage {{1}}.', 'ovin'),
        Q('Où l’élevage caprin est-il surtout pratiqué ?', 'au Nord, dans les monts Mandara',
          'au Littoral', 'au Sud, dans la forêt', n=3),
        V('L’élevage ovin, c’est l’élevage des chèvres.', False, n=4,
          e='Non. Ovin, c’est le mouton ; caprin, c’est la chèvre.')),

      N('relation',
        'L’élevage porcin (le porc) est pratiqué à l’Ouest, au Centre et dans le Littoral. '
        'L’élevage avicole (la volaille : poulet, canard) se fait dans toutes les régions.',
        'bn-elevage-porcin', P('Porcs et volaille', ('porcin', 'le porc'),
                               ('avicole', 'la volaille'), ('l’Ouest, le Centre', 'porcs')),
        ('simple', 'Porcin pour le porc ; avicole pour les oiseaux de la ferme.'),
        ('visuel', 'Un poulailler, on en trouve partout au Cameroun.'),
        Q('L’élevage avicole, c’est l’élevage…', 'de la volaille', 'des porcs',
          'des moutons'),
        V('L’élevage avicole se pratique dans toutes les régions.', True),
        T('L’élevage du porc s’appelle l’élevage {{1}}.', 'porcin'),
        A('Relie chaque élevage à son animal.', ('caprin', 'la chèvre'), ('ovin', 'le mouton'),
          ('porcin', 'le porc'), ('avicole', 'la volaille'), n=3),
        V('L’élevage porcin se pratique surtout dans les monts Mandara.', False, n=4,
          e='Non. Il se pratique à l’Ouest, au Centre et dans le Littoral.'),
        Q('Où l’élevage porcin est-il pratiqué ?', 'à l’Ouest, au Centre et au Littoral',
          'seulement dans l’Adamaoua', 'seulement au Nord', n=4))),

    # -------------------------------------------------------------- 28 octobre
    L(HG, 'Les villes du Cameroun', GEO, '2026-10-28',
      'Une ville est une agglomération importante où les habitants ont des activités '
      'professionnelles variées. Yaoundé est la capitale politique, Douala la capitale '
      'économique. Les grandes villes sont surpeuplées à cause de l’exode rural et de '
      'l’immigration.',
      'bn-villes-couv', ['Yaoundé', 'Douala', 'exode rural'],

      N('definition',
        'Une ville est une agglomération relativement importante où vivent des habitants aux '
        'activités professionnelles diversifiées.',
        'bn-villes-def', F('Une ville', 'une grande agglomération', 'des métiers variés'),
        ('simple', 'Une ville, c’est beaucoup de maisons et de gens, qui font des métiers très '
                   'différents.'),
        ('visuel', 'Au même carrefour : un médecin, un chauffeur, une vendeuse, un '
                   'fonctionnaire.'),
        Q('Qu’est-ce qu’une ville ?', 'Une agglomération importante aux métiers variés',
          'Un petit groupe de cases', 'Un champ de cultures'),
        V('En ville, les habitants ont des activités professionnelles variées.', True),
        T('Une ville est une {{1}} relativement importante.', 'agglomération'),
        Q('Ce qui caractérise les habitants d’une ville, ce sont…', 'des métiers diversifiés',
          'un seul métier pour tous', 'l’absence de travail', n=3),
        V('En ville, tous les habitants font le même métier.', False, n=4,
          e='Non. Leurs activités professionnelles sont diversifiées.')),

      N('relation',
        'Yaoundé est la capitale politique du Cameroun, et Douala sa capitale économique.',
        'bn-villes-capitales', P('Deux capitales', ('Yaoundé', 'capitale politique'),
                                 ('Douala', 'capitale économique')),
        ('simple', 'À Yaoundé, on gouverne le pays ; à Douala, on fait surtout du commerce.'),
        ('analogie', 'Yaoundé est la tête qui décide, Douala le marché qui fait tourner '
                     'l’argent.'),
        Q('Quelle est la capitale politique du Cameroun ?', 'Yaoundé', 'Douala', 'Garoua'),
        V('Douala est la capitale économique du Cameroun.', True),
        A('Relie chaque ville à son rôle.', ('Yaoundé', 'capitale politique'),
          ('Douala', 'capitale économique'), n=2),
        Q('Douala est la capitale…', 'économique', 'politique', 'agricole', n=3),
        V('Douala est la capitale politique du Cameroun.', False, n=4,
          e='Non. Douala est la capitale économique ; Yaoundé, la capitale politique.')),

      N('liste',
        'Parmi les autres villes du Cameroun, on peut citer Bafoussam, Ngaoundéré, Garoua, '
        'Bertoua, Kribi, Ebolowa, Bamenda et Limbé.',
        'bn-villes-autres', F('D’autres villes', 'Bafoussam, Ngaoundéré', 'Garoua, Bertoua',
                              'Kribi, Ebolowa', 'Bamenda, Limbé'),
        ('simple', 'Le Cameroun a beaucoup de villes, dans toutes ses régions.'),
        ('visuel', 'Sur la carte, chaque point noir est une ville : Garoua au nord, Kribi au '
                   'bord de la mer.'),
        Q('Laquelle est une ville du Cameroun ?', 'Bertoua', 'Lagos', 'Libreville'),
        V('Ngaoundéré est une ville du Cameroun.', True),
        Q('Laquelle n’est pas citée dans le cahier comme ville du Cameroun ?', 'Dakar',
          'Ebolowa', 'Bamenda', n=2),
        Q('Quelle ville le cahier cite-t-il avec Kribi ?', 'Ebolowa', 'Abidjan', 'Accra', n=3),
        V('Limbé est une ville du Cameroun.', True, n=4)),

      N('relation',
        'Les principales villes du Cameroun se caractérisent par une surpopulation, causée par '
        'l’exode rural et l’immigration. Elle entraîne l’insécurité et le manque de logements.',
        'bn-villes-surpop', F('La surpopulation', 'causes : l’exode rural',
                              'et l’immigration', 'effets : l’insécurité',
                              'le manque de logements'),
        ('simple', 'Trop de gens arrivent en ville : il n’y a plus assez de maisons, et '
                   'l’insécurité grandit.'),
        ('pas_a_pas', 'Les gens quittent le village : c’est l’exode rural. D’autres viennent '
                      'd’ailleurs : l’immigration. La ville déborde.'),
        Q('Qu’est-ce qui cause la surpopulation des villes ?', 'l’exode rural et l’immigration',
          'les vacances scolaires', 'la saison des pluies'),
        V('La surpopulation entraîne l’insécurité dans la ville.', True),
        T('Quand les gens quittent le village pour la ville, c’est l’exode {{1}}.', 'rural'),
        Q('Quelle est une conséquence de la surpopulation ?', 'le manque de logements',
          'trop de maisons vides', 'la fin du commerce', n=3),
        V('La surpopulation des villes vient seulement des naissances.', False, n=4,
          e='Non. Elle vient de l’exode rural et de l’immigration.')),

      # La fin de la liste est floue sur la photo : ce sont les conséquences
      # que donnent toutes les leçons sur la ville au Cameroun.
      N('liste',
        'La surpopulation entraîne aussi le chômage, les embouteillages, les quartiers '
        'insalubres et le manque d’eau, d’électricité, d’écoles et d’hôpitaux.',
        'bn-villes-consequences', F('Et aussi', 'le chômage', 'les embouteillages',
                                    'les quartiers insalubres', 'pas assez d’écoles'),
        ('simple', 'Trop de monde dans une ville, et tout devient difficile : le travail, la '
                   'route, l’eau.'),
        ('visuel', 'Des voitures bloquées au carrefour, des maisons serrées sans eau courante.'),
        Q('Laquelle est une conséquence de la surpopulation ?', 'le chômage',
          'des routes toujours vides', 'trop d’emplois pour tous'),
        V('La surpopulation provoque des embouteillages.', True),
        T('Quand il n’y a pas assez de travail pour tous, c’est le {{1}}.', 'chômage'),
        A('Relie chaque problème à ce qu’il veut dire.', ('le chômage', 'pas de travail'),
          ('les embouteillages', 'des routes bloquées'), ('l’insalubrité', 'un quartier sale'),
          n=3),
        V('La surpopulation donne assez d’écoles et d’hôpitaux pour tous.', False, n=4,
          e='Non. Elle en fait manquer.'))),

    # -------------------------------------------------------------- 29 octobre
    L(HG, 'Les Européens sur la côte du Cameroun', HIST, '2026-10-29',
      'Les premiers Européens sur la côte du Cameroun sont les Portugais, conduits par '
      'Fernando Poo en 1472. Ils ont appelé le Wouri Rio dos Camarões, la rivière des '
      'crevettes : ce nom a donné Cameroun. Puis Anglais, Français et Allemands ont ouvert des '
      'comptoirs de commerce.',
      'bn-europeens-couv', ['1472', 'le Wouri', 'les crevettes'],

      N('date',
        'Les premiers Européens à explorer les côtes camerounaises étaient les Portugais, sous '
        'la conduite de Fernando Poo, en 1472.',
        'bn-europeens-1472', F('Les premiers Européens', 'les Portugais', 'Fernando Poo',
                               'en 1472'),
        ('simple', 'En 1472, des bateaux portugais arrivent sur la côte du Cameroun.'),
        ('visuel', 'Une caravelle aux voiles blanches s’approche de la côte : ce sont les '
                   'Portugais.'),
        Q('Qui furent les premiers Européens sur la côte du Cameroun ?', 'les Portugais',
          'les Allemands', 'les Français'),
        V('Les Portugais sont arrivés sur la côte du Cameroun en 1472.', True),
        T('Les Portugais sont arrivés sur la côte du Cameroun en {{1}}.', '1472'),
        Q('Qui conduisait les Portugais ?', 'Fernando Poo', 'Christophe Colomb',
          'Vasco de Gama', n=3),
        V('Les premiers Européens sur nos côtes étaient les Anglais.', False, n=4,
          e='Non. C’étaient les Portugais, en 1472.')),

      N('relation',
        'Les Portugais ont découvert le fleuve Wouri au moment où les crevettes s’agitaient. Ils '
        'l’ont appelé Rio dos Camarões, la rivière des crevettes.',
        'bn-europeens-wouri', F('Le Wouri', 'plein de crevettes', 'la rivière des crevettes'),
        ('simple', 'Les marins ont vu des crevettes partout dans le fleuve, et lui ont donné '
                   'ce nom.'),
        ('visuel', 'L’eau du Wouri qui grouille de petites crevettes.'),
        Q('Quel fleuve les Portugais ont-ils découvert ?', 'le Wouri', 'la Sanaga', 'le Nyong'),
        V('Rio dos Camarões veut dire la rivière des crevettes.', True),
        T('Rio dos Camarões veut dire la rivière des {{1}}.', 'crevettes'),
        Q('Pourquoi ce nom de rivière des crevettes ?', 'Les crevettes s’agitaient dans le fleuve',
          'Le fleuve était rouge', 'Les marins pêchaient des requins', n=3),
        V('Rio dos Camarões veut dire la rivière des poissons.', False, n=4,
          e='Non. Camarões, ce sont les crevettes.')),

      N('relation',
        'Le nom Rio dos Camarões, déformé par les Anglais, donnera plus tard le nom Cameroun.',
        'bn-europeens-nom', F('D’où vient le nom', 'Rio dos Camarões', 'déformé par les Anglais',
                              'Cameroun'),
        ('pas_a_pas', 'Camarões en portugais, puis Cameroons pour les Anglais, puis Cameroun.'),
        ('simple', 'Notre pays porte le nom des crevettes du Wouri.'),
        Q('D’où vient le nom Cameroun ?', 'De Rio dos Camarões', 'Du mont Cameroun seul',
          'D’un roi allemand'),
        V('Le nom Cameroun vient des crevettes du Wouri.', True),
        T('Le nom Rio dos Camarões, {{1}} par les Anglais, a donné Cameroun.', 'déformé'),
        Q('Qui a déformé le nom Rio dos Camarões ?', 'les Anglais', 'les Pygmées',
          'les Égyptiens', n=3),
        V('Le nom Cameroun vient d’un mot allemand.', False, n=4,
          e='Non. Il vient du portugais Rio dos Camarões, déformé par les Anglais.')),

      N('relation',
        'Les Portugais se sont installés sur l’île de Bioko, au large du Cameroun, pour faire du '
        'commerce. Les Anglais, les Français et les Allemands les ont rejoints avec leurs '
        'comptoirs.',
        'bn-europeens-bioko', F('Le commerce', 'les Portugais à Bioko', 'puis les Anglais',
                                'les Français', 'les Allemands'),
        ('simple', 'Bioko est une île tout près de nos côtes. Les Portugais y faisaient du '
                   'commerce.'),
        ('visuel', 'Des comptoirs, c’est-à-dire des magasins au bord de la mer, pour échanger '
                   'avec les chefs.'),
        Q('Où les Portugais se sont-ils installés ?', 'sur l’île de Bioko', 'à Yaoundé',
          'dans l’Adamaoua'),
        V('Les Anglais, les Français et les Allemands ont rejoint les Portugais.', True),
        T('Les Portugais se sont installés sur l’{{1}} de Bioko.', 'île'),
        Q('Qu’installaient les Européens sur la côte ?', 'des comptoirs de commerce',
          'des écoles normales', 'des champs de cacao', n=3),
        V('Les Portugais se sont installés à Garoua.', False, n=4,
          e='Non. Ils se sont installés sur l’île de Bioko.')),

      N('relation',
        'Les Européens échangeaient des armes, des tissus et de l’alcool avec les chefs locaux, '
        'qui leur donnaient en retour de l’ivoire et des esclaves.',
        'bn-europeens-echanges', P('Les échanges', ('ils apportaient', 'armes, tissus'),
                                   ('et aussi', 'l’alcool'),
                                   ('ils recevaient', 'ivoire, esclaves')),
        ('simple', 'Des objets venus d’Europe contre l’ivoire et des êtres humains.'),
        ('histoire', 'Le bateau arrive plein de tissus et d’armes, et repart avec de l’ivoire '
                     'et des captifs.'),
        Q('Que donnaient les chefs locaux aux Européens ?', 'de l’ivoire et des esclaves',
          'des armes et de l’alcool', 'des tissus'),
        V('Les Européens apportaient des armes et des tissus.', True),
        T('Les chefs locaux donnaient de l’{{1}} et des esclaves.', 'ivoire'),
        A('Relie chaque groupe à ce qu’il donnait.', ('les Européens', 'des armes'),
          ('les chefs locaux', 'de l’ivoire'), n=3),
        V('Les chefs locaux donnaient de l’alcool aux Européens.', False, n=4,
          e='Non. C’est l’inverse : les Européens apportaient l’alcool.')),

      # Le siècle où les autres Européens arrivent est illisible ; celui des
      # Portugais se déduit de la date que le cahier donne.
      N('date',
        'Les Portugais sont arrivés en 1472, c’est-à-dire au XVe siècle. Les Anglais, les '
        'Français et les Allemands sont venus après eux.',
        'bn-europeens-siecle', F('Les siècles', '1472 : le XVe siècle', 'les Portugais d’abord',
                                 'les autres ensuite'),
        ('pas_a_pas', '1472 commence par 14 : on est au XVe siècle, comme 1400 à 1499.'),
        ('simple', 'Les Portugais ouvrent la route ; les autres Européens suivent.'),
        Q('En quel siècle les Portugais sont-ils arrivés ?', 'au XVe siècle', 'au XXe siècle',
          'au Xe siècle'),
        V('Les Anglais sont arrivés après les Portugais.', True),
        T('L’année 1472 est au XVe {{1}}.', 'siècle'),
        C('Remets dans l’ordre.', 'les Portugais arrivent en 1472',
          'les Anglais, Français et Allemands les rejoignent', 'leurs comptoirs s’installent',
          n=3),
        V('L’année 1472 est au XIVe siècle.', False, n=4,
          e='Non. 1472 est au XVe siècle, comme toutes les années de 1401 à 1500.'))),

]
