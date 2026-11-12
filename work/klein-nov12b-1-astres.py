# -*- coding: utf-8 -*-
# Les astres — une leçon. Chargé par lecons-klein-cahier-nov12b.py.
#
# La page ne porte pas de date : elle précède la révision du 1er octobre, et
# donc date de septembre. Le paquet la range au 28 septembre pour l-ordre ; la
# date n-est pas écrite en base.
#
# Le rôle de chaque astre vient de la révision du 1er octobre, où la maîtresse
# a validé les trois liaisons : la terre nous abrite et nous nourrit, le
# soleil nous éclaire le jour, la lune nous éclaire la nuit.

GEO = 'Géographie'

LECONS = [
    L(GEO, 'Les astres', 'Géographie', '2026-09-28',
      'Parmi les astres, nous avons la terre, le soleil, la lune et les étoiles. La terre est '
      'une énorme boule qui tourne sur elle-même en 24 heures et autour du soleil en 365 jours ; '
      'c’est la seule planète habitable. Le soleil éclaire et réchauffe la terre. La lune tourne '
      'autour de la terre et se voit la nuit.',
      'kz-astres-couv', ['la terre', 'le soleil', 'la lune'],

      N('definition',
        'La terre est une énorme boule, légèrement aplatie aux pôles. C’est la seule planète '
        'habitable : elle nous abrite et nous nourrit.',
        'kz-astres-terre', F('La terre', 'une énorme boule', 'aplatie aux pôles',
                             'la seule planète habitable'),
        ('simple', 'Nous vivons sur la terre. Elle nous donne une maison et de quoi manger.'),
        ('visuel', 'Un grand ballon un peu écrasé en haut et en bas : c’est la terre.'),
        Q('Quelle est la seule planète habitable ?', 'la terre', 'la lune', 'le soleil'),
        V('La terre nous abrite et nous nourrit.', True),
        T('La terre est la seule planète {{1}}.', 'habitable'),
        Q('Quelle forme a la terre ?', 'une énorme boule', 'un carré', 'un triangle', n=3),
        V('On peut habiter sur toutes les planètes.', False, n=4,
          e='Non. La terre est la seule planète habitable.')),

      N('relation',
        'La terre tourne sur elle-même en 24 heures, et autour du soleil pendant 365 jours.',
        'kz-astres-tours', P('La terre tourne', ('sur elle-même', '24 heures'),
                             ('autour du soleil', '365 jours')),
        ('simple', 'Un tour sur elle-même, c’est un jour. Un tour du soleil, c’est une année.'),
        ('visuel', 'Une toupie qui tourne tout en faisant le tour d’une lampe.'),
        Q('En combien de temps la terre tourne-t-elle sur elle-même ?', '24 heures',
          '365 jours', '7 jours'),
        V('La terre tourne autour du soleil pendant 365 jours.', True),
        T('La terre tourne sur elle-même en {{1}} heures.', '24'),
        A('Relie chaque tour à sa durée.', ('sur elle-même', '24 heures'),
          ('autour du soleil', '365 jours'), n=3),
        V('La terre tourne autour du soleil en 24 heures.', False, n=4,
          e='Non. En 24 heures, elle tourne sur elle-même. Autour du soleil : 365 jours.')),

      N('relation',
        'Le soleil éclaire et réchauffe la terre : il nous éclaire le jour.',
        'kz-astres-soleil', F('Le soleil', 'il éclaire la terre', 'il la réchauffe',
                              'le jour'),
        ('simple', 'Sans le soleil, il ferait noir et froid.'),
        ('visuel', 'Le linge sèche dehors au soleil, en pleine journée.'),
        Q('Que fait le soleil ?', 'Il éclaire et réchauffe la terre', 'Il tourne autour de la lune',
          'Il éclaire seulement la nuit'),
        V('Le soleil réchauffe la terre.', True),
        T('Le soleil éclaire et {{1}} la terre.', 'réchauffe'),
        Q('Quel astre nous éclaire le jour ?', 'le soleil', 'la lune', 'les étoiles', n=3),
        V('Le soleil refroidit la terre.', False, n=4, e='Non. Le soleil la réchauffe.')),

      N('relation',
        'La lune tourne autour de la terre. Elle n’est facilement visible que la nuit : elle '
        'nous éclaire la nuit.',
        'kz-astres-lune', F('La lune', 'elle tourne autour', 'de la terre',
                            'elle éclaire la nuit'),
        ('simple', 'La nuit, quand le soleil est parti, c’est la lune qu’on voit dans le ciel.'),
        ('visuel', 'Un croissant de lune au-dessus des maisons endormies.'),
        Q('Autour de quoi tourne la lune ?', 'autour de la terre', 'autour de la lune',
          'autour des étoiles'),
        V('La lune se voit facilement la nuit.', True),
        T('La lune tourne autour de la {{1}}.', 'terre'),
        A('Relie chaque astre à son rôle.', ('la terre', 'nous abrite et nourrit'),
          ('le soleil', 'nous éclaire le jour'), ('la lune', 'nous éclaire la nuit'), n=3),
        V('La lune réchauffe la terre pendant la journée.', False, n=4,
          e='Non. C’est le soleil. La lune se voit la nuit.'),
        Q('Quel astre nous éclaire la nuit ?', 'la lune', 'le soleil', 'la terre', n=4))),
]
