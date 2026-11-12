# -*- coding: utf-8 -*-
# The English notebook of KLEIN, social studies — history, civics, rights and
# morals. Loaded by lecons-klein-cahier-nov12.py.
#
# Short notebook lessons that follow each other on the same subject are kept
# together: written history and its importance; security and its agents; love
# and respect; the child’s right to use the road and the right to transport.
#
# The drawing of a basket (13 October) is not a lesson and is not turned into
# questions.

HIST = 'Histoire'
CIV = 'Éducation civique'
DROITS = 'Droits humains'
MORALE = 'Éducation morale'

LECONS = [
    # -------------------------------------------------------------- 14 October
    L(HIST, 'Written history and its importance', 'History', '2026-10-14',
      'Written history is written down in books and papers and kept. It is the best kind of '
      'history because it does not change: the Bible, the Koran, textbooks, newspapers. History '
      'helps us to know the past, to correct its errors and to know important people and places.',
      'kz-hist-couv', ['books', 'the past'],

      N('definition',
        'Written history is the kind of history which is written down in books and papers and '
        'kept. It is the best kind because it does not change.',
        'kz-hist-written', F('Written history', 'written in books', 'and papers', 'it does not change'),
        ('simple', 'When we write the story down, nobody can change it later.'),
        ('visuel', 'An old book on a shelf keeps the same words for many years.'),
        Q('What is written history?', 'History written down in books and papers',
          'History told by songs only', 'History drawn on the sand'),
        V('Written history does not change.', True),
        T('Written history is written down in {{1}} and papers.', 'books'),
        Q('Why is written history the best kind?', 'It does not change', 'It is very short',
          'It is always funny', n=3),
        V('Written history changes every day.', False, n=4,
          e='No. It is the best kind because it does not change.')),

      N('liste',
        'Examples of written history: the Bible, the Koran, textbooks and newspapers.',
        'kz-hist-examples', F('Examples', 'the Bible', 'the Koran', 'textbooks', 'newspapers'),
        ('simple', 'Everything that keeps the past on paper is written history.'),
        ('visuel', 'A newspaper from last year still tells what happened that day.'),
        Q('Which one is written history?', 'a newspaper', 'a football', 'a cooking pot'),
        V('A textbook is an example of written history.', True),
        T('The Bible and the Koran are examples of written {{1}}.', 'history'),
        Q('Which one is NOT written history?', 'a song nobody wrote down', 'a school textbook',
          'the Holy Bible', n=3),
        V('A newspaper is an example of written history.', True, n=4)),

      N('liste',
        'History helps us to know what happened in the past, to correct the errors of the past '
        'and to know about important people and places.',
        'kz-hist-importance', F('History helps us to', 'know the past', 'correct its errors',
                                'know important people', 'and places'),
        ('simple', 'If we know the mistakes of yesterday, we do not make them again.'),
        ('analogie', 'History is like the memory of a country.'),
        Q('History helps us to know…', 'what happened in the past', 'the weather of tomorrow',
          'the price of bread'),
        V('History helps us to correct the errors of the past.', True),
        T('History helps us to know about important people and {{1}}.', 'places'),
        Q('Which one is an importance of history?', 'Correct the errors of the past',
          'Cook food faster', 'Grow taller', n=3),
        V('History tells us only about the future.', False, n=4,
          e='No. History tells us about the past.'))),

    L(CIV, 'Road safety rules', 'Civics', '2026-10-14',
      'There are rules that guide road users to be safe on the road: look left and right before '
      'crossing, cross on the zebra crossing, do not make or receive calls when driving, respect '
      'road signs and traffic lights, walk on the pedestrian path.',
      'kz-road-couv', ['zebra crossing', 'traffic lights'],

      N('liste',
        'Look left and right before crossing the road, and cross on the zebra crossing.',
        'kz-road-cross', F('Crossing the road', 'look left and right', 'cross on the zebra',
                           'crossing'),
        ('pas_a_pas', 'Stop. Look left. Look right. If no car is coming, cross on the zebra.'),
        ('visuel', 'The zebra crossing has white stripes, like a zebra.'),
        Q('What do you do before crossing the road?', 'Look left and right', 'Close your eyes',
          'Run very fast'),
        V('We cross the road on the zebra crossing.', True),
        T('Cross the road on the {{1}} crossing.', 'zebra'),
        C('Put in order.', 'stop at the road', 'look left and right', 'cross on the zebra', n=3),
        V('We can cross the road without looking.', False, n=4,
          e='No. Look left and right before crossing.')),

      N('liste',
        'Do not make or receive calls when driving. Respect road signs and traffic lights, and '
        'walk on the pedestrian path.',
        'kz-road-rules', F('More rules', 'no calls when driving', 'respect road signs',
                           'respect traffic lights', 'walk on the pedestrian path'),
        ('simple', 'A driver on the phone does not look at the road.'),
        ('visuel', 'Red light: the cars stop and the children cross.'),
        Q('Where do pedestrians walk?', 'on the pedestrian path', 'in the middle of the road',
          'on the cars'),
        V('We must respect traffic lights.', True),
        T('Walk on the {{1}} path.', 'pedestrian'),
        Q('What must a driver NOT do?', 'make calls when driving', 'respect road signs',
          'stop at the red light', n=3),
        V('A driver can receive calls when driving.', False, n=4,
          e='No. Do not make or receive calls when driving.'))),

    L(CIV, 'Security and its agents', 'Civics', '2026-10-14',
      'Security is the state of being free from danger. It prevents crimes, creates a safe '
      'environment, promotes order and peace of mind, and keeps property safe. Police officers, '
      'soldiers, gendarmes, security guards and teachers are agents of peace and security.',
      'kz-secu-couv', ['safe', 'police', 'order'],

      N('definition',
        'Security is the state of being free from danger.',
        'kz-secu-def', F('Security', 'being free', 'from danger'),
        ('simple', 'When you are safe, nothing bad can happen to you.'),
        ('visuel', 'A child sleeping quietly in a locked house.'),
        Q('What is security?', 'Being free from danger', 'Being very rich',
          'Being very fast'),
        V('Security is the state of being free from danger.', True),
        T('Security is the state of being free from {{1}}.', 'danger'),
        Q('Which one shows security?', 'a locked gate at night', 'an open fire in the house',
          'a broken bridge', n=3),
        V('Security means being in danger.', False, n=4,
          e='No. It means being free from danger.')),

      N('liste',
        'Security prevents crimes, creates a safe environment, promotes order and peace of mind, '
        'and keeps property safe.',
        'kz-secu-importance', F('Security', 'prevents crimes', 'a safe environment',
                                'order, peace of mind', 'keeps property safe'),
        ('simple', 'With security, people live calmly and their things are not stolen.'),
        ('analogie', 'A fence around the yard keeps the goats in and the thieves out.'),
        Q('What does security prevent?', 'crimes', 'rain', 'school'),
        V('Security keeps property safe.', True),
        T('Security promotes {{1}}.', 'order'),
        Q('Which one is an importance of security?', 'It creates a safe environment',
          'It makes people sick', 'It stops the rain', n=3),
        V('Security brings disorder.', False, n=4, e='No. Security promotes order.')),

      N('liste',
        'Agents of peace and security: police officers, soldiers, gendarmes, security guards, '
        'human right officers, detention officers, teachers and the peace corps.',
        'kz-secu-agents', F('Agents', 'police officers', 'soldiers, gendarmes',
                            'security guards', 'teachers'),
        ('simple', 'Many people work so that we are safe: not only the police.'),
        ('visuel', 'The gendarme on the road, the guard at the gate, the teacher in class.'),
        Q('Which one is an agent of peace and security?', 'a police officer', 'a thief',
          'a tailor'),
        V('A gendarme is an agent of peace and security.', True),
        T('Police officers and {{1}} are agents of security.', 'soldiers'),
        Q('A detention officer is also called…', 'a warder', 'a farmer', 'a driver', n=3),
        V('Teachers are agents of peace and security too.', True, n=4))),

    # -------------------------------------------------------------- 16 October
    L(DROITS, 'Pupils’ right to know themselves', 'Rights', '2026-10-16',
      'Pupils have the right to know their name and age, their family and family members, their '
      'nationality, their place of origin (village), and their likes and dislikes.',
      'kz-know-couv', ['name', 'family', 'village'],

      N('liste',
        'Pupils have the right to know their name and age, and their family and family members.',
        'kz-know-name', F('I have the right to know', 'my name', 'my age', 'my family'),
        ('simple', 'Every child must know who he is and who his family is.'),
        ('visuel', 'A child holding a photo of his family.'),
        Q('Pupils have the right to know their…', 'name and age', 'teacher’s salary',
          'neighbour’s secrets'),
        V('Pupils have the right to know their family members.', True),
        T('Pupils have the right to know their name and {{1}}.', 'age'),
        Q('Which one is a pupil’s right?', 'to know his family', 'to never go to school',
          'to take other people’s things', n=3),
        V('A pupil has no right to know his age.', False, n=4,
          e='No. He has the right to know his name and age.')),

      N('liste',
        'Pupils have the right to know their nationality, their place of origin, which is their '
        'village, and their likes and dislikes.',
        'kz-know-origin', F('And also', 'my nationality', 'my village', 'my likes',
                            'and dislikes'),
        ('simple', 'Where do I come from? What do I like? I have the right to know.'),
        ('visuel', 'The flag of my country, the road to my village.'),
        Q('A pupil’s place of origin is his…', 'village', 'classroom', 'desk'),
        V('Pupils have the right to know their nationality.', True),
        T('Pupils have the right to know their likes and {{1}}.', 'dislikes'),
        Q('Which one is a pupil’s right?', 'to know his nationality', 'to drive a car',
          'to sell the school', n=3),
        V('A pupil has no right to know his village.', False, n=4,
          e='No. He has the right to know his place of origin.'))),

    # -------------------------------------------------------------- 21 October
    L(CIV, 'Family income', 'The family', '2026-10-21',
      'Family income is all the money a family receives during a particular period of time: a '
      'salary, the sale of articles like food crops, overtime labour, gifts from friends and '
      'well wishers, and rent of properties like houses.',
      'kz-income-couv', ['salary', 'money', 'family'],

      N('definition',
        'Family income is all the money a family receives during a particular period of time.',
        'kz-income-def', F('Family income', 'all the money', 'a family receives'),
        ('simple', 'All the money that comes into the house is the family income.'),
        ('visuel', 'Coins and notes entering a little house.'),
        Q('What is family income?', 'All the money a family receives', 'All the food in the house',
          'All the children in the family'),
        V('Family income is money a family receives.', True),
        T('Family income is all the {{1}} a family receives.', 'money'),
        Q('Family income is counted during…', 'a particular period of time', 'only one second',
          'a short dream', n=3),
        V('Family income is the money a family spends.', False, n=4,
          e='No. It is the money a family receives.')),

      N('liste',
        'Sources of family income: a salary, the sale of articles like food crops, overtime '
        'labour, gifts from friends and well wishers, and rent of properties like houses.',
        'kz-income-sources', F('Where it comes from', 'a salary', 'sale of food crops',
                               'gifts from friends', 'rent of houses'),
        ('simple', 'Papa’s salary, maize sold at the market, a gift: all this is income.'),
        ('visuel', 'A mother selling tomatoes at the market brings money home.'),
        Q('Which one is a source of family income?', 'a salary', 'a broken chair',
          'a school bag'),
        V('Selling food crops brings family income.', True),
        T('A worker receives a {{1}} every month.', 'salary'),
        Q('Renting a house to someone brings…', 'income', 'rain', 'a disease', n=3),
        V('Gifts from friends are never family income.', False, n=4,
          e='No. Gifts from friends and well wishers are family income.'))),

    # -------------------------------------------------------------- 25 October
    L(DROITS, 'The right to use the judiciary', 'Rights', '2026-10-25',
      'The judiciary is an arm of the government that helps to implement the laws. Everyone has '
      'the right to sue or be sued, to defend himself or herself, to be protected by the law, '
      'and everyone is equal before the law.',
      'kz-judi-couv', ['the law', 'equal'],

      N('definition',
        'The judiciary is an arm of the government that helps to implement the laws.',
        'kz-judi-def', F('The judiciary', 'an arm of the government', 'it applies the laws'),
        ('simple', 'The judges and the courts make sure the laws are respected.'),
        ('visuel', 'A judge in a court, with a small wooden hammer.'),
        Q('What is the judiciary?', 'An arm of the government for the laws', 'A kind of primary school',
          'A big market in the town'),
        V('The judiciary helps to implement the laws.', True),
        T('The judiciary is an arm of the {{1}}.', 'government'),
        Q('The judiciary helps to implement…', 'the laws', 'the roads', 'the crops', n=3),
        V('The judiciary is a football team.', False, n=4,
          e='No. It is an arm of the government for the laws.')),

      N('liste',
        'Everyone has the right to sue or be sued, to defend himself or herself, and to be '
        'protected by the law. Everyone is equal before the law.',
        'kz-judi-rights', F('Everyone has the right', 'to sue or be sued', 'to defend himself',
                            'to be protected', 'equal before the law'),
        ('simple', 'Rich or poor, child or adult: the law is the same for everybody.'),
        ('analogie', 'In a game, the same rule is for all the players.'),
        Q('Before the law, everyone is…', 'equal', 'alone', 'quiet'),
        V('Everyone has the right to be protected by the law.', True),
        T('Everyone is {{1}} before the law.', 'equal'),
        Q('Which one is a right before the judiciary?', 'to defend yourself',
          'to punish people yourself', 'to break the law', n=3),
        V('Only rich people are equal before the law.', False, n=4,
          e='No. Everyone is equal before the law.'))),

    # -------------------------------------------------------------- 26 October
    L(HIST, 'The days of the week', 'History', '2026-10-26',
      'There are 7 days in the week: five school days, Monday, Tuesday, Wednesday, Thursday '
      'and Friday, and two weekend days, Saturday and Sunday.',
      'kz-days-couv', ['7 days', 'weekend'],

      N('liste',
        'There are 7 days in the week. Five are school days: Monday, Tuesday, Wednesday, '
        'Thursday and Friday.',
        'kz-days-school', F('Five school days', 'Monday, Tuesday', 'Wednesday', 'Thursday',
                            'Friday'),
        ('simple', 'From Monday to Friday, we go to school.'),
        ('visuel', 'Five school bags in a row, one for each school day.'),
        Q('How many days are in a week?', '7', '5', '10'),
        V('Wednesday is a school day.', True),
        T('There are {{1}} days in a week.', '7'),
        C('Put the school days in order.', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
          'Friday', n=3),
        Q('Which day comes after Thursday?', 'Friday', 'Monday', 'Sunday', n=4),
        V('Saturday is a school day.', False, n=4, e='No. Saturday is a weekend day.')),

      N('liste',
        'There are two weekend days: Saturday and Sunday.',
        'kz-days-weekend', F('Two weekend days', 'Saturday', 'Sunday'),
        ('simple', 'At the weekend, there is no school.'),
        ('visuel', 'Saturday and Sunday: a ball and a rest at home.'),
        Q('Which one is a weekend day?', 'Sunday', 'Monday', 'Friday'),
        V('Saturday is a weekend day.', True),
        T('Saturday and Sunday are the {{1}} days.', 'weekend'),
        Q('How many weekend days are there?', 'two', 'five', 'seven', n=3),
        V('Monday is a weekend day.', False, n=4, e='No. Monday is a school day.'))),

    L(DROITS, 'The right to use the road and transport', 'Rights', '2026-10-26',
      'A child has the right to be educated on road signs and on how to use the road, to be '
      'helped by the hand while crossing, to have equal rights on the road and to walk on the '
      'pedestrian track. All human beings have equal rights to transport, with no racial or '
      'gender discrimination.',
      'kz-right-couv', ['the road', 'transport'],

      N('liste',
        'A child has the right to be educated on road signs and on how to use the road, and to '
        'be helped by the hand while crossing the road.',
        'kz-right-child', F('A child has the right', 'to learn road signs',
                            'to learn to use the road', 'to be helped to cross'),
        ('simple', 'A grown-up must teach the child the road and hold his hand to cross.'),
        ('visuel', 'A mother holding her child’s hand on the zebra crossing.'),
        Q('A child has the right to be helped…', 'by the hand while crossing',
          'to drive a car', 'to run on the road'),
        V('A child has the right to learn road signs.', True),
        T('A child has the right to be helped by the {{1}} while crossing.', 'hand'),
        Q('Which one is a child’s right on the road?', 'to walk on the pedestrian track',
          'to play in the middle of the road', 'to stop the cars', n=3),
        V('A child has no rights on the road.', False, n=4,
          e='No. He has equal rights on the use of the road.')),

      N('liste',
        'All human beings have equal rights to transport by land. There should be no racial or '
        'gender discrimination when travelling.',
        'kz-right-transport', F('The right to transport', 'equal for everyone',
                                'no racial discrimination', 'no gender discrimination'),
        ('simple', 'In the bus, a boy, a girl, everyone has the same right to a seat.'),
        ('visuel', 'People of all kinds sitting together in the same bus.'),
        Q('Who has the right to transport?', 'All human beings', 'Only men', 'Only rich people'),
        V('There should be no discrimination when travelling.', True),
        T('All human beings have {{1}} rights to transport.', 'equal'),
        Q('Refusing a girl in a bus because she is a girl is…', 'gender discrimination',
          'road safety', 'a road sign', n=3),
        V('Only boys have the right to travel by bus.', False, n=4,
          e='No. There should be no gender discrimination.'))),

    L(MORALE, 'Love and respect', 'Good behaviour', '2026-10-26',
      'Love is the strong feeling we have for one another; it brings peace and unity among '
      'people. Respect is a good action shown towards someone: remove your cap, offer your seat '
      'to elders, greet people, do not cross your legs before elders, talk politely.',
      'kz-love-couv', ['love', 'respect', 'peace'],

      N('definition',
        'Love is the strong feeling we have for one another. Love brings peace and unity among '
        'people.',
        'kz-love-def', F('Love', 'a strong feeling', 'it brings peace', 'and unity'),
        ('simple', 'When we love each other, we do not fight.'),
        ('visuel', 'Children holding hands in a circle.'),
        Q('What is love?', 'A strong feeling for one another', 'A kind of food',
          'A game of football'),
        V('Love brings peace and unity among people.', True),
        T('Love brings peace and {{1}} among people.', 'unity'),
        Q('What does love bring?', 'peace', 'war', 'hatred', n=3),
        V('Love brings quarrels among people.', False, n=4,
          e='No. Love brings peace and unity.')),

      N('definition',
        'Respect is a good action shown towards someone.',
        'kz-love-respect', F('Respect', 'a good action', 'towards someone'),
        ('simple', 'Respect is how we show others that they count.'),
        ('histoire', 'Ama greets her neighbour every morning: she shows respect.'),
        Q('What is respect?', 'A good action shown towards someone', 'A bad word said to someone',
          'A kind of cap for elders'),
        V('Respect is a good action.', True),
        T('Respect is a good {{1}} shown towards someone.', 'action'),
        Q('Which one shows respect?', 'greeting people', 'shouting at elders',
          'pushing a friend', n=3),
        V('Insulting someone is a way of showing respect.', False, n=4)),

      N('liste',
        'Ways of showing respect: remove your cap when talking to elders, offer your seat to '
        'elders, greet people, do not cross your legs before elders, talk to people politely.',
        'kz-love-ways', F('Showing respect', 'remove your cap', 'offer your seat',
                          'greet people', 'talk politely'),
        ('simple', 'Small gestures every day show respect to the elders.'),
        ('visuel', 'A boy stands up and gives his seat to an old woman.'),
        Q('When you talk to an elder, you…', 'remove your cap', 'cross your legs',
          'turn your back'),
        V('Offering your seat to elders shows respect.', True),
        T('Talk to people {{1}}.', 'politely'),
        Q('Which one is NOT respectful?', 'crossing your legs before elders',
          'greeting people', 'offering your seat', n=3),
        V('Keeping your cap on when talking to elders shows respect.', False, n=4,
          e='No. Remove your cap when talking to elders.'))),

    # -------------------------------------------------------------- 30 October
    L(MORALE, 'Working together', 'Good behaviour', '2026-10-30',
      'Working together means working in a group to achieve a common goal. It makes work easy '
      'and faster, helps us to learn from one another, and brings better ideas and results.',
      'kz-work-couv', ['group', 'common goal'],

      N('definition',
        'Working together means working in a group to achieve a common goal.',
        'kz-work-def', F('Working together', 'in a group', 'for a common goal'),
        ('simple', 'Many hands for the same work.'),
        ('visuel', 'Children carrying a big table together.'),
        Q('What does working together mean?', 'Working in a group for a common goal',
          'Working alone at night', 'Not working at all'),
        V('Working together means working in a group.', True),
        T('Working together means working in a {{1}}.', 'group'),
        Q('When we work together, we have…', 'a common goal', 'no goal', 'many quarrels', n=3),
        V('Working together means working alone.', False, n=4,
          e='No. It means working in a group.')),

      N('liste',
        'Working together makes work easy and faster, helps us to learn from one another, and '
        'brings better ideas and results.',
        'kz-work-adv', F('Advantages', 'easy and faster', 'we learn from each other',
                         'better ideas', 'better results'),
        ('simple', 'Together we finish quicker, and each one teaches the others.'),
        ('analogie', 'One finger cannot lift a stone; the whole hand can.'),
        Q('Working together makes work…', 'easy and faster', 'longer and harder', 'impossible'),
        V('Working together brings better ideas.', True),
        T('Working together makes work easy and {{1}}.', 'faster'),
        Q('Which one is an advantage of working together?', 'We learn from one another',
          'We fight more', 'We finish later', n=3),
        V('Working together makes work slower.', False, n=4,
          e='No. It makes work easy and faster.'))),
]
