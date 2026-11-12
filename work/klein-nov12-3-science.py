# -*- coding: utf-8 -*-
# The English notebook of KLEIN, science, home economics and ICT.
# Loaded by lecons-klein-cahier-nov12.py.
#
# « Cooking and why we cook food » is not a copy of « Cooking methods »,
# already in the app: that lesson gives the methods (boiling, frying…), this
# one gives the definition and the reasons for cooking.
#
# « Soil and the soil profile » is not a copy of « Uses of the soil » or of
# « Le sol »: it gives the kinds of soil in English and the soil profile.
#
# The health personnel page has no date: it follows the 16 October page and
# takes its date.

SC = 'Sciences et technologies'
METIERS = 'Métiers'
ICT = 'ICT'

LECONS = [
    # -------------------------------------------------------------- 12 October
    L(SC, 'Seasons', 'Weather', '2026-10-12',
      'A season is a particular period of the year when the weather changes. There are two '
      'seasons in Cameroon: the dry season, from October to March, and the rainy season, from '
      'March to October. In Europe, there are four: summer, spring, winter and autumn.',
      'kz-season-couv', ['dry season', 'rainy season'],

      N('definition',
        'A season is a particular period of the year when the weather changes.',
        'kz-season-def', F('A season', 'a period of the year', 'the weather changes'),
        ('simple', 'Some months are hot and dry, other months are wet: those are seasons.'),
        ('visuel', 'A calendar: sun on some months, rain clouds on others.'),
        Q('What is a season?', 'A period of the year when the weather changes',
          'One single day of the week', 'A kind of tree in the forest'),
        V('A season is a particular period of the year.', True),
        T('A season is a period of the year when the {{1}} changes.', 'weather'),
        Q('In a season, what changes?', 'the weather', 'the days of the week', 'our names', n=3),
        V('A season lasts only one hour.', False, n=4, e='No. It is a period of the year.')),

      N('relation',
        'There are two seasons in Cameroon: the dry season, from October to March, and the '
        'rainy season, from March to October.',
        'kz-season-cameroon', P('In Cameroon', ('dry season', 'October to March'),
                                ('rainy season', 'March to October')),
        ('simple', 'In Cameroon, it is either dry or rainy.'),
        ('visuel', 'Dusty roads in the dry season, full rivers in the rainy season.'),
        Q('How many seasons are there in Cameroon?', 'two', 'four', 'one'),
        V('The rainy season begins in March.', True),
        T('In Cameroon, there is the dry season and the {{1}} season.', 'rainy'),
        A('Match each season with its months.', ('the dry season', 'October to March'),
          ('the rainy season', 'March to October'), n=3),
        V('The dry season begins in March.', False, n=4,
          e='No. In the notebook, the dry season begins in October.')),

      N('liste',
        'In Europe, there are four seasons: summer, spring, winter and autumn.',
        'kz-season-europe', F('In Europe', 'summer', 'spring', 'winter', 'autumn'),
        ('simple', 'Europe has four seasons; Cameroon has two.'),
        ('visuel', 'In winter, in Europe, snow can fall.'),
        Q('How many seasons are there in Europe?', 'four', 'two', 'seven'),
        V('Winter is a season in Europe.', True),
        T('In Europe, there are {{1}} seasons.', '4'),
        Q('Which one is a season in Europe?', 'autumn', 'the dry season', 'Monday', n=3),
        V('There are four seasons in Cameroon.', False, n=4,
          e='No. Four in Europe, two in Cameroon.'))),

    # -------------------------------------------------------------- 13 October
    L(METIERS, 'Cooking and why we cook food', 'Food', '2026-10-13',
      'Cooking is the preparation of food so that the body gets the best out of it. We cook '
      'food to soften it and ease digestion, to kill germs, to make it tasteful and delicious, '
      'and to make it more attractive.',
      'kz-cook-couv', ['cooking', 'germs', 'delicious'],

      N('definition',
        'Cooking is the preparation of food so that the body gets the best out of it.',
        'kz-cook-def', F('Cooking', 'preparing food', 'for the body'),
        ('simple', 'We cook food so that it is good for our body.'),
        ('visuel', 'A pot on the fire, rice boiling inside.'),
        Q('What is cooking?', 'The preparation of food for the body', 'Washing the plates',
          'Buying food at the market'),
        V('Cooking helps the body to get the best out of food.', True),
        T('Cooking is the preparation of {{1}}.', 'food'),
        Q('Cooking is done so that the body…', 'gets the best out of food', 'gets very tired',
          'gets very cold', n=3),
        V('Cooking means eating food raw.', False, n=4, e='No. Cooking prepares the food.')),

      N('liste',
        'We cook food to soften it and ease digestion, to kill germs, to make it tasteful and '
        'delicious, and to make it more attractive.',
        'kz-cook-reasons', F('Why we cook food', 'to soften it', 'to kill germs',
                             'to make it delicious', 'to make it attractive'),
        ('simple', 'Cooked food is soft, clean and good to eat.'),
        ('visuel', 'A hard raw yam, then a soft cooked yam on the plate.'),
        Q('Why do we cook food?', 'To kill germs', 'To make it dirty', 'To make it hard'),
        V('Cooking makes food easier to digest.', True),
        T('We cook food to kill {{1}}.', 'germs'),
        Q('Which one is a reason for cooking food?', 'to make it more attractive',
          'to make it smell bad', 'to throw it away', n=3),
        V('Cooking food adds germs to it.', False, n=4, e='No. Cooking kills germs.'))),

    L(ICT, 'The television and the radio', 'ICT tools', '2026-10-13',
      'A television is an audio-visual modern ICT tool: it is used for watching moving images, '
      'listening, and playing games and music. A radio is an audio modern ICT tool: it is used '
      'for playing music, recording audio and listening to news and other programmes.',
      'kz-tv-couv', ['television', 'radio'],

      N('definition',
        'A television is an audio-visual modern ICT tool. It is used for watching moving images '
        '(video), listening, and playing games and music.',
        'kz-tv-tv', F('The television', 'audio-visual', 'watch moving images',
                      'games and music'),
        ('simple', 'Audio-visual: we hear the sound and we see the images.'),
        ('visuel', 'A cartoon on the TV screen, with its music.'),
        Q('A television is a… tool.', 'audio-visual', 'audio only', 'cooking'),
        V('We use a television to watch moving images.', True),
        T('A television is an audio-{{1}} tool.', 'visual'),
        Q('What do we watch on a television?', 'moving images', 'the weather outside',
          'our homework', n=3),
        V('A television is an old local ICT tool.', False, n=4,
          e='No. It is a modern ICT tool.')),

      N('definition',
        'A radio is an audio modern ICT tool. It is used for playing music, recording audio and '
        'listening to news and other programmes.',
        'kz-tv-radio', F('The radio', 'audio only', 'music, news', 'recording audio'),
        ('simple', 'With the radio, we only hear: there are no images.'),
        ('visuel', 'Papa listens to the news on his small radio.'),
        Q('A radio is an… tool.', 'audio', 'audio-visual', 'agricultural'),
        V('We use a radio to listen to the news.', True),
        T('A radio is an {{1}} modern ICT tool.', 'audio'),
        A('Match each tool with what it gives.', ('the television', 'sound and images'),
          ('the radio', 'sound only'), n=3),
        V('We watch moving images on the radio.', False, n=4,
          e='No. The radio gives only sound.'))),

    # -------------------------------------------------------------- 16 October
    L(SC, 'Health personnel', 'Health', '2026-10-16',
      'Health personnel are trained workers in the health unit. The doctor does consultations '
      'and prescriptions, the nurse looks after patients, the pharmacist prepares and sells '
      'medicines, the midwife takes care of deliveries and new born babies, the surgeon does '
      'operations.',
      'kz-health-couv', ['doctor', 'nurse', 'midwife'],

      N('definition',
        'Health personnel are trained workers in the health unit.',
        'kz-health-def', F('Health personnel', 'trained workers', 'in the health unit'),
        ('simple', 'The people who look after us at the hospital learned their work.'),
        ('visuel', 'A hospital with a doctor, a nurse and a pharmacist.'),
        Q('Who are health personnel?', 'Trained workers in the health unit',
          'Children at school', 'Farmers in the field'),
        V('Health personnel work in the health unit.', True),
        T('Health personnel are {{1}} workers in the health unit.', 'trained'),
        Q('Where do health personnel work?', 'in the health unit', 'in the market',
          'in the forest', n=3),
        V('Health personnel have never learned their work.', False, n=4,
          e='No. They are trained workers.')),

      N('relation',
        'The doctor does consultations and prescriptions. The nurse looks after patients. The '
        'pharmacist prepares and sells medicines in a pharmacy.',
        'kz-health-who', P('Who does what', ('the doctor', 'consultation'),
                           ('the nurse', 'looks after patients'),
                           ('the pharmacist', 'sells medicines')),
        ('simple', 'The doctor finds the illness, the pharmacist gives the medicine.'),
        ('visuel', 'The doctor listens to the heart; the nurse gives the injection.'),
        Q('Who sells medicines in a pharmacy?', 'the pharmacist', 'the nurse', 'the surgeon'),
        V('The nurse looks after patients.', True),
        T('The {{1}} does consultations and prescriptions.', 'doctor'),
        A('Match each worker with his work.', ('the doctor', 'consultation'),
          ('the nurse', 'looks after patients'), ('the pharmacist', 'sells medicines'), n=3),
        V('The pharmacist does operations.', False, n=4,
          e='No. The surgeon does operations.')),

      N('relation',
        'The midwife takes care of deliveries and new born babies. The surgeon does operations. '
        'Others are the dentist, the laboratory technician and the paediatrician.',
        'kz-health-more', P('More workers', ('the midwife', 'new born babies'),
                            ('the surgeon', 'operations'), ('the dentist', 'the teeth')),
        ('simple', 'Each health worker has his own job.'),
        ('visuel', 'The midwife holds a new born baby.'),
        Q('Who takes care of new born babies?', 'the midwife', 'the surgeon', 'the dentist'),
        V('The surgeon does operations.', True),
        T('The {{1}} takes care of deliveries and new born babies.', 'midwife'),
        Q('Which one is also a health worker?', 'the dentist', 'the carpenter', 'the driver',
          n=3),
        V('The midwife does operations on the heart.', False, n=4,
          e='No. The midwife takes care of deliveries and new born babies.'))),

    # -------------------------------------------------------------- 19 October
    L(SC, 'Soil and the soil profile', 'The soil', '2026-10-19',
      'Soil is the upper layer of the earth on which plants grow. There are humus, sandy, clay, '
      'volcanic, loam, laterite and silty soils. The soil profile is the vertical arrangement '
      'of the soil: top soil, subsoil, parent rock, bed rock.',
      'kz-soil-couv', ['top soil', 'subsoil', 'bed rock'],

      N('definition',
        'Soil is the upper layer of the earth on which plants grow.',
        'kz-soil-def', F('Soil', 'the upper layer', 'of the earth', 'plants grow on it'),
        ('simple', 'Soil is the ground under our feet, where plants grow.'),
        ('visuel', 'A seedling coming out of the dark soil.'),
        Q('What is soil?', 'The upper layer of the earth', 'The water of the sea',
          'The air in the sky'),
        V('Plants grow on the soil.', True),
        T('Soil is the upper {{1}} of the earth.', 'layer'),
        Q('What grows on the soil?', 'plants', 'clouds', 'stars', n=3),
        V('Soil is the deepest part of the earth.', False, n=4,
          e='No. Soil is the upper layer.')),

      N('liste',
        'Examples of soil: humus soil, sandy soil, clay soil, volcanic soil, loam soil, laterite '
        'soil and silty soil.',
        'kz-soil-kinds', F('Kinds of soil', 'humus, sandy', 'clay, volcanic', 'loam, laterite',
                           'silty'),
        ('simple', 'Soils are not all the same: seven kinds in the notebook.'),
        ('visuel', 'Sand on the beach, red laterite on the road, black humus in the forest.'),
        Q('Which one is a kind of soil?', 'sandy soil', 'rainy soil', 'happy soil'),
        V('Clay soil is a kind of soil.', True),
        T('Humus, sandy and {{1}} are kinds of soil.', 'clay'),
        Q('Which one is NOT a kind of soil in the notebook?', 'glass soil', 'loam soil',
          'silty soil', n=3),
        V('Volcanic soil is a kind of soil.', True, n=4)),

      N('relation',
        'The soil profile is the vertical arrangement of the soil: top soil, subsoil, parent '
        'rock and bed rock.',
        'kz-soil-profile', F('The soil profile', '1. top soil', '2. subsoil', '3. parent rock',
                             '4. bed rock'),
        ('pas_a_pas', 'From the top to the bottom: top soil, subsoil, parent rock, bed rock.'),
        ('visuel', 'Dig a deep hole: you see the layers one under the other.'),
        Q('What is at the top of the soil profile?', 'top soil', 'bed rock', 'parent rock'),
        V('The bed rock is at the bottom of the soil profile.', True),
        T('The soil profile is the {{1}} arrangement of the soil.', 'vertical'),
        C('Put the layers in order, from the top.', 'top soil', 'subsoil', 'parent rock',
          'bed rock', n=3),
        V('The subsoil is above the top soil.', False, n=4,
          e='No. The top soil is at the top; the subsoil is under it.'))),

    # -------------------------------------------------------------- 25 October
    L(SC, 'Vaccination', 'Health', '2026-10-25',
      'Vaccination is the act of introducing a vaccine into the body for protection against a '
      'particular disease. It keeps the body healthy, prevents us from contracting diseases and '
      'keeps the immune system active. A vaccination campaign gives vaccines to a large '
      'population in a given time.',
      'kz-vacc-couv', ['vaccine', 'protection'],

      N('definition',
        'Vaccination is the act of introducing a vaccine into the body for protection against a '
        'particular disease.',
        'kz-vacc-def', F('Vaccination', 'a vaccine in the body', 'protection',
                         'against a disease'),
        ('simple', 'The vaccine teaches the body to fight a disease before it comes.'),
        ('visuel', 'A nurse gives a small injection in the arm.'),
        Q('What is vaccination?', 'Putting a vaccine into the body for protection',
          'Washing the hands with soap', 'Eating many fresh fruits'),
        V('Vaccination protects us against a disease.', True),
        T('Vaccination is introducing a {{1}} into the body.', 'vaccine'),
        Q('Vaccination protects us against…', 'a particular disease', 'the heavy rain', 'being hungry', n=3),
        V('Vaccination gives us a disease.', False, n=4,
          e='No. It protects us against a disease.')),

      N('liste',
        'Vaccination keeps the body healthy, prevents us from contracting diseases, and keeps '
        'the immune system active and powerful.',
        'kz-vacc-importance', F('Importance', 'keeps the body healthy', 'prevents diseases',
                                'a strong immune system'),
        ('simple', 'Vaccinated, the body is ready to defend itself.'),
        ('analogie', 'The vaccine is like a guard trained in advance.'),
        Q('Vaccination keeps the body…', 'healthy', 'sick', 'tired'),
        V('Vaccination keeps the immune system active.', True),
        T('Vaccination keeps the body {{1}}.', 'healthy'),
        Q('Which one is an importance of vaccination?', 'It prevents diseases',
          'It makes us hungry', 'It makes us grow taller', n=3),
        V('Vaccination makes the immune system weak.', False, n=4,
          e='No. It keeps it active and powerful.')),

      N('definition',
        'A vaccination campaign is the giving of vaccine doses to a large population in a given '
        'time period.',
        'kz-vacc-campaign', F('A vaccination campaign', 'vaccines for many people',
                              'in a given time'),
        ('simple', 'During a campaign, many children are vaccinated in a few days.'),
        ('visuel', 'A long line of mothers and babies in front of the health centre.'),
        Q('What is a vaccination campaign?', 'Vaccines for many people in a given time',
          'A big football match', 'A long school holiday'),
        V('A vaccination campaign reaches a large population.', True),
        T('A vaccination campaign gives vaccines to a large {{1}}.', 'population'),
        Q('A vaccination campaign happens…', 'in a given time period', 'every second',
          'never', n=3),
        V('A vaccination campaign is for one person only.', False, n=4,
          e='No. It is for a large population.'))),
]
