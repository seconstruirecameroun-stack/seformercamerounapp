# -*- coding: utf-8 -*-
# BRAYNE, English notebooks: home economics and citizenship — three lessons.
# Loaded by lecons-brayne-cahier-nov12c.py.
#
# « Diet, meals and feeding » is already in the app: it only defines a meal.
# This lesson adds the three types of meal and meal planning.
#
# WHAT IS NOT ASKED, because it cannot be read surely on the photo:
#   - the exact hours of breakfast and supper, and whether supper is heavy
#     (the order of the three meals is asked instead);
#   - the exact first meaning of red (« independence » is asked, from the
#     theme) and the sentence after the motto (the coat of arms is asked);
#   - the name of the president of the Senate, and the end of the last note
#     on the Speaker of the National Assembly.
#
# The citizenship lessons are numbered 2 and 3 in the notebook: number 1 was
# not photographed.

SC = 'Sciences'
ECM = 'ECM'

LECONS = [
    # -------------------------------------------------------------- 13 October
    L(SC, 'The types of meals and meal planning', 'Food', '2026-10-13',
      'A meal is the type of food we eat at a particular time. There are three types: '
      'breakfast in the morning, lunch in the afternoon, which is usually heavy, and supper or '
      'dinner in the evening. Meal planning is preparing to serve food and feed the family on '
      'time, daily, weekly or monthly.',
      'bc-meal-couv', ['breakfast', 'lunch', 'supper'],

      N('definition',
        'A meal is the type of food we eat at a particular time.',
        'bc-meal-def', F('A meal', 'food we eat', 'at a particular time'),
        ('simple', 'Morning, afternoon, evening: each time we sit down to eat is a meal.'),
        ('visuel', 'A plate on the table at lunchtime: that is a meal.'),
        Q('What is a meal?', 'The food we eat at a particular time', 'A kind of cooking pot',
          'A market where food is sold'),
        V('A meal is the type of food we eat at a particular time.', True),
        T('A meal is the type of food we eat at a particular {{1}}.', 'time'),
        Q('How many types of meal does the notebook give?', 'three', 'two', 'five', n=3),
        V('A meal is food we eat at any time, without any order.', False, n=4,
          e='No. A meal is eaten at a particular time.')),

      N('relation',
        'Breakfast is taken in the morning: bread and tea, chips and eggs. Lunch is taken in '
        'the afternoon, from 12 pm to 3 pm: rice and beans, corn fufu. It is usually heavy.',
        'bc-meal-breakfast', P('Morning and afternoon', ('breakfast', 'the morning'),
                               ('lunch', 'the afternoon'), ('bread and tea', 'breakfast'),
                               ('rice and beans', 'lunch')),
        ('simple', 'Breakfast wakes up the body; lunch is the big meal of the day.'),
        ('visuel', 'Tea and bread at 7 o’clock, rice and beans at 1 o’clock.'),
        Q('When is breakfast taken?', 'in the morning', 'in the afternoon', 'in the evening'),
        V('Lunch is usually heavy.', True),
        T('Lunch is taken in the {{1}}.', 'afternoon'),
        Q('Which food is given as an example of lunch?', 'rice and beans', 'bread and tea',
          'plantain chips and eggs', n=3),
        Q('Lunch is usually taken…', 'from 12 pm to 3 pm', 'from 6 pm to 9 pm',
          'from 3 am to 5 am', n=4),
        V('Breakfast is taken in the evening.', False, n=4,
          e='No. Breakfast is taken in the morning.')),

      N('definition',
        'Supper, or dinner, is the meal which is taken in the evening: ndolé and plantain, '
        'jollof rice.',
        'bc-meal-supper', F('Supper or dinner', 'in the evening', 'ndolé and plantain',
                            'jollof rice'),
        ('simple', 'The last meal of the day, before going to bed.'),
        ('visuel', 'The family around the table in the evening, ndolé and plantain on the plate.'),
        Q('What is another name for supper?', 'dinner', 'breakfast', 'lunch'),
        V('Supper is taken in the evening.', True),
        T('Supper is also called {{1}}.', 'dinner'),
        A('Match each meal with its time.', ('breakfast', 'the morning'),
          ('lunch', 'the afternoon'), ('supper', 'the evening'), n=3),
        V('Supper is the first meal of the day.', False, n=4,
          e='No. Breakfast is the first; supper is taken in the evening.')),

      N('definition',
        'Meal planning is the preparation to serve food and feed the family on time. Meals can '
        'be planned daily, weekly or monthly.',
        'bc-meal-planning', F('Meal planning', 'serve food on time', 'daily, weekly',
                              'or monthly'),
        ('simple', 'Planning means deciding before: what we will eat, and when.'),
        ('analogie', 'Like a timetable for school, but for the meals of the family.'),
        Q('What is meal planning?', 'Preparing to serve food and feed the family on time',
          'Eating everything at once', 'Buying food without thinking'),
        V('Meals can be planned weekly.', True),
        T('Meals can be planned daily, weekly or {{1}}.', 'monthly'),
        Q('Meal planning helps to feed the family…', 'on time', 'late', 'once a month', n=3),
        V('Meals can only be planned for one day.', False, n=4,
          e='No. Daily, weekly or monthly.')),

      N('liste',
        'When choosing the food, we must consider the health, the age, the occupation, the '
        'culture of the people, the availability in the market and the season.',
        'bc-meal-principles', F('Think about', 'health and age', 'occupation, culture',
                                'what the market has', 'the season'),
        ('simple', 'A baby, a sick person and a farmer do not need the same meal.'),
        ('visuel', 'In mango season, mangoes are on every stall at the market.'),
        Q('Which one must be considered in meal planning?', 'the age', 'the colour of the plate',
          'the name of the cook'),
        V('The season must be considered in meal planning.', True),
        T('We must consider the {{1}} of the people: are they young or old?', 'age'),
        Q('Why consider the availability in the market?', 'Some foods are not always sold',
          'The market is always closed', 'Food has no price', n=3),
        V('The health of the family does not matter in meal planning.', False, n=4,
          e='No. The health is the first principle given in the notebook.')),

      # The hours of breakfast and supper are not readable: the order of the
      # three meals is, and it is what matters.
      N('relation',
        'Breakfast is the first meal of the day, lunch the second, and supper the last. Meals '
        'are taken at regular times.',
        'bc-meal-order', F('The order of meals', '1. breakfast', '2. lunch', '3. supper'),
        ('simple', 'Morning, afternoon, evening: always in this order.'),
        ('analogie', 'Like the lessons of the day: each one at its time.'),
        Q('Which is the first meal of the day?', 'breakfast', 'supper', 'lunch'),
        V('Supper is the last meal of the day.', True),
        T('The first meal of the day is {{1}}.', 'breakfast'),
        C('Put the meals in order.', 'breakfast', 'lunch', 'supper', n=3),
        V('Lunch is taken before breakfast.', False, n=4,
          e='No. Breakfast first, then lunch, then supper.'))),

    # -------------------------------------------------------------- 19 October
    L(ECM, 'The flag and the motto of Cameroon', 'National symbols', '2026-10-19',
      'The Cameroon flag has three colours, green, red and yellow, with a golden star on the red '
      'strip. Green stands for the vegetation of the south, red for power and authority, yellow '
      'for the sun and the north, the star for unity. The motto of Cameroon is Peace, Work, '
      'Fatherland.',
      'bc-flag-couv', ['green', 'red', 'yellow'],

      N('definition',
        'The Cameroon flag has three colours, which are green, red and yellow. It has a golden '
        'star on the red strip.',
        'bc-flag-colours', F('The flag', 'green, red, yellow', 'a golden star',
                             'on the red strip'),
        ('visuel', 'Three vertical strips: green, red, yellow, and a star in the middle.'),
        ('simple', 'Three colours and one star: that is our flag.'),
        Q('What are the colours of the Cameroon flag?', 'green, red and yellow',
          'blue, white and red', 'black, red and green'),
        V('The golden star is on the red strip.', True),
        T('The star on the Cameroon flag is {{1}}.', 'golden'),
        Q('On which strip is the star?', 'the red strip', 'the green strip', 'the yellow strip',
          n=3),
        V('The Cameroon flag has four colours.', False, n=4,
          e='No. Three: green, red and yellow.')),

      N('relation',
        'Green stands for the rich and abundant vegetation of the southern regions. Red stands '
        'for power and authority. Yellow stands for the north and the riches of the sun.',
        'bc-flag-meaning', P('What colours mean', ('green', 'vegetation'),
                             ('red', 'power, authority'), ('yellow', 'the sun, the north')),
        ('visuel', 'The green forest of the south, the yellow sun over the north.'),
        ('simple', 'Each colour tells something about the country.'),
        Q('What does green stand for?', 'the vegetation of the south', 'the sun of the north',
          'power and authority'),
        V('Red stands for power and authority.', True),
        T('Green stands for the rich and abundant {{1}} of the south.', 'vegetation'),
        A('Match each colour with its meaning.', ('green', 'vegetation'),
          ('red', 'power and authority'), ('yellow', 'the sun'), n=3),
        V('Yellow stands for the forests of the south.', False, n=4,
          e='No. Yellow stands for the north and the sun; green for the vegetation.')),

      N('definition',
        'The golden star stands for unity and oneness: Cameroon is one and indivisible.',
        'bc-flag-star', F('The golden star', 'unity and oneness', 'one and indivisible'),
        ('simple', 'One star, one country: Cameroon cannot be divided.'),
        ('analogie', 'Like one family under one roof.'),
        Q('What does the golden star stand for?', 'unity', 'the rain', 'the army'),
        V('The star means that Cameroon is one and indivisible.', True),
        T('The golden star stands for {{1}} and oneness.', 'unity'),
        Q('« Indivisible » means that the country…', 'cannot be divided', 'is very small',
          'has no flag', n=3),
        V('The star stands for the vegetation.', False, n=4, e='No. It stands for unity.')),

      N('liste',
        'The flag can be seen at the presidency, at schools, at police stations and at '
        'government offices.',
        'bc-flag-places', F('Where we see it', 'at the presidency', 'at schools',
                            'at police stations', 'at government offices'),
        ('simple', 'Wherever the State works, the flag flies.'),
        ('visuel', 'Every morning, the flag goes up in the school yard.'),
        Q('Where can the flag be seen?', 'at schools', 'in the river', 'in the forest'),
        V('The flag can be seen at police stations.', True),
        T('The flag can be seen at government {{1}}.', 'offices'),
        Q('Which place is NOT given in the notebook?', 'the market', 'the presidency',
          'the police station', n=3),
        V('The flag can only be seen at the presidency.', False, n=4,
          e='No. Also at schools, police stations and government offices.')),

      N('definition',
        'The motto of Cameroon is Peace, Work, Fatherland.',
        'bc-flag-motto', F('The motto', 'Peace', 'Work', 'Fatherland'),
        ('simple', 'Three words that every Cameroonian should live by.'),
        ('pas_a_pas', 'First Peace, then Work, then Fatherland: always in this order.'),
        Q('What is the motto of Cameroon?', 'Peace, Work, Fatherland', 'Unity, Strength, Glory',
          'Green, Red, Yellow'),
        V('Work is one of the three words of the motto.', True),
        T('The motto of Cameroon is Peace, {{1}}, Fatherland.', 'work'),
        C('Put the motto in order.', 'Peace', 'Work', 'Fatherland', n=3),
        V('The motto of Cameroon is Unity, Work, Progress.', False, n=4,
          e='No. It is Peace, Work, Fatherland.')),

      # The first meaning of red is hard to read; the notebook speaks of the
      # independence of the country. The motto is on the coat of arms.
      N('relation',
        'Red also recalls the struggle for the independence of the country. The motto, Peace, '
        'Work, Fatherland, is written on the coat of arms of Cameroon.',
        'bc-flag-red', F('More to know', 'red: independence', 'the motto is written',
                         'on the coat of arms'),
        ('simple', 'Red reminds us that Cameroon became free and independent.'),
        ('visuel', 'The coat of arms of Cameroon carries the three words of the motto.'),
        Q('What does red also recall?', 'the independence of the country', 'the rain of the south',
          'the forest of the south'),
        V('The motto is written on the coat of arms of Cameroon.', True),
        T('Red recalls the struggle for the {{1}} of the country.', 'independence'),
        Q('Where is the motto written?', 'on the coat of arms', 'on the banknotes only',
          'on the roads', n=3),
        V('Red stands for the vegetation of the south.', False, n=4,
          e='No. Green stands for the vegetation; red for power, authority and independence.'))),

    # -------------------------------------------------------------- 20 October
    L(ECM, 'The legislative arm of government', 'The government', '2026-10-20',
      'The legislature is the law-making body of Cameroon. It has two houses: the Senate, the '
      'upper house, with 100 senators, 70 elected and 30 appointed; and the National Assembly, '
      'the lower house, with 180 members elected for 5 years. It makes the laws, amends the '
      'constitution and votes the budget.',
      'bc-legis-couv', ['Senate', 'National Assembly', 'laws'],

      N('definition',
        'The legislature is the law-making body of Cameroon. It is made up of two houses: the '
        'upper house and the lower house.',
        'bc-legis-def', F('The legislature', 'it makes the laws', 'two houses',
                          'upper and lower'),
        ('simple', 'The legislature is where the laws of the country are made.'),
        ('analogie', 'Like the class council that writes the class rules, but for the country.'),
        Q('What is the legislature?', 'The law-making body of the country', 'The army of the country',
          'The police of the town'),
        V('The legislature has two houses.', True),
        T('The legislature is the law-{{1}} body of Cameroon.', 'making'),
        Q('What are the two houses called?', 'the upper house and the lower house',
          'the big house and the small house', 'the old house and the new house', n=3),
        V('The legislature is the arm that judges people in court.', False, n=4,
          e='No. It makes the laws. The courts are the judiciary.')),

      N('relation',
        'The Senate is the upper house: 100 senators, 70 elected and 30 appointed by the '
        'President of the Republic. The first senatorial election took place on 14th April 2013.',
        'bc-legis-senate', F('The Senate', 'upper house', '100 senators',
                             '70 elected, 30 appointed', 'first election: 2013'),
        ('pas_a_pas', '100 senators: 70 are voted, and the President appoints the other 30.'),
        ('simple', 'The Senate is the upper house; its members are senators.'),
        Q('How many senators are there in Cameroon?', '100', '180', '30'),
        V('30 senators are appointed by the President of the Republic.', True),
        T('The members of the Senate are called {{1}}.', 'senators'),
        Q('How many senators are elected?', '70', '30', '100', n=3),
        Q('When did the first senatorial election take place?', 'on 14th April 2013',
          'on 20th May 1972', 'on 1st January 1960', n=4),
        V('All the senators are appointed by the President.', False, n=4,
          e='No. 70 are elected, 30 are appointed.')),

      N('relation',
        'The National Assembly is the lower house. It has 180 members of parliament, elected '
        'for a mandate of 5 years. The parliament meets three times in a year.',
        'bc-legis-assembly', F('The National Assembly', 'lower house', '180 members',
                               'a mandate of 5 years', 'meets 3 times a year'),
        ('simple', 'The members of parliament are chosen by the people, every five years.'),
        ('pas_a_pas', 'Elected for 5 years, they meet three times each year to work on the laws.'),
        Q('How many members has the National Assembly?', '180', '100', '70'),
        V('Members of parliament are elected for 5 years.', True),
        T('The National Assembly has {{1}} members.', '180'),
        A('Match each house with its number of members.', ('the Senate', '100'),
          ('the National Assembly', '180'), n=3),
        Q('How many times a year does the parliament meet?', 'three times', 'once',
          'every day', n=4),
        V('The National Assembly is the upper house.', False, n=4,
          e='No. It is the lower house; the Senate is the upper house.')),

      N('liste',
        'The legislature makes the laws of the country, revises or amends the constitution, and '
        'votes the country’s budget.',
        'bc-legis-functions', F('Its functions', 'make the laws', 'amend the constitution',
                                'vote the budget'),
        ('simple', 'Laws, constitution, budget: three jobs for the legislature.'),
        ('analogie', 'It writes the rules and decides how the country’s money is spent.'),
        Q('Which one is a function of the legislature?', 'It votes the budget',
          'It arrests thieves', 'It teaches pupils'),
        V('The legislature can amend the constitution.', True),
        T('The legislature votes the country’s {{1}}.', 'budget'),
        Q('« To amend » the constitution means to…', 'change it', 'burn it', 'read it aloud',
          n=3),
        V('The legislature only votes the budget and makes no laws.', False, n=4,
          e='No. Its first function is to make the laws.')),

      N('definition',
        'The president of the Senate is the constitutional successor of the Head of State.',
        'bc-legis-successor', F('N.B.', 'the president of the Senate', 'succeeds the',
                                'Head of State'),
        ('simple', 'If the Head of State can no longer govern, the president of the Senate takes over.'),
        ('analogie', 'Like the class prefect who replaces the teacher for a short while.'),
        Q('Who is the constitutional successor of the Head of State?',
          'the president of the Senate', 'the oldest minister', 'the mayor of Yaoundé'),
        V('The president of the Senate succeeds the Head of State.', True),
        T('The president of the Senate is the constitutional {{1}} of the Head of State.', 'successor'),
        Q('« Successor » means the person who…', 'comes after and takes the place',
          'votes the budget', 'judges in court', n=3),
        V('The Speaker of the National Assembly is the successor of the Head of State.', False,
          n=4, e='No. It is the president of the Senate.')),

      # The name of the president of the Senate is not readable, and it
      # changes: how each leader is chosen is asked instead.
      N('definition',
        'The president of the Senate is elected by the senators. The Speaker of the National '
        'Assembly is elected by the members of parliament.',
        'bc-legis-presidents', P('Who chooses them', ('Senate president', 'the senators'),
                                 ('the Speaker', 'the MPs')),
        ('simple', 'Each house chooses its own leader.'),
        ('analogie', 'Like a class choosing its own prefect.'),
        Q('Who elects the president of the Senate?', 'the senators', 'the pupils',
          'the mayors'),
        V('The Speaker is elected by the members of parliament.', True),
        T('The president of the Senate is elected by the {{1}}.', 'senators'),
        A('Match each leader with those who elect him.', ('the Senate president', 'the senators'),
          ('the Speaker', 'the members of parliament'), n=3),
        V('The president of the Senate is chosen by the pupils of Cameroon.', False, n=4,
          e='No. He is elected by the senators.'))),
]
