# -*- coding: utf-8 -*-
# TIC, en français — cinq leçons. Chargé par lecons-brayne-francais-oct.py.
#
# La première est écrite depuis un devoir corrigé, et non depuis une page de
# cours : les périphériques, la saisie kilométrique et l-ENIAC datent de
# septembre et n-ont pas été photographiés. Les réponses sont celles que la
# maîtresse a validées.
#
# Les deux pages « insérer une image » ne portent pas de date : elles sont
# entre le 23 et le 28 octobre, et la leçon prend la date du 23.

TIC = 'TIC'
ENV = 'Environnement informatique de travail'
OUTILS = 'Production avec les outils TIC'
CODE = 'Code de conduite'

LECONS = [
    # ---------------------------------------------------------------- devoir
    L(TIC, 'Les périphériques, la saisie kilométrique et l’ENIAC', ENV, '2026-10-02',
      'La souris, le clavier, le moniteur, l’imprimante, la clé USB et la disquette sont les '
      'périphériques de l’ordinateur. La saisie kilométrique est le fait d’écrire un texte '
      'sans se soucier des fautes. Le premier ordinateur, inventé en 1946, est l’ENIAC.',
      'bt-dv-couv', ['entrée', 'sortie', 'stockage'],

      N('liste',
        'La souris, le clavier, le moniteur, l’imprimante, la clé USB et la disquette sont les '
        'périphériques de l’ordinateur. La souris et le clavier sont des périphériques '
        'd’entrée.',
        'bt-dv-entree', F('Périphériques d’entrée', 'la souris', 'le clavier',
                          'ils font entrer l’information'),
        ('simple', 'Avec la souris et le clavier, c’est toi qui donnes quelque chose à '
                   'l’ordinateur.'),
        ('visuel', 'Tu tapes une lettre : elle entre dans l’ordinateur. Le clavier est une '
                   'entrée.'),
        Q('Que représentent la souris, le clavier et l’imprimante ?',
          'Les périphériques de l’ordinateur', 'Les logiciels de l’ordinateur',
          'Les fichiers de l’ordinateur'),
        V('Le clavier est un périphérique d’entrée.', True),
        T('La souris et le {{1}} sont des périphériques d’entrée.', 'clavier'),
        Q('Lequel est un périphérique d’entrée ?', 'la souris', 'l’imprimante',
          'le moniteur', n=3),
        V('L’imprimante est un périphérique d’entrée.', False, n=4,
          e='Non. L’imprimante fait sortir le texte : périphérique de sortie.')),

      N('liste',
        'Le moniteur et l’imprimante sont des périphériques de sortie. La clé USB et la '
        'disquette sont des périphériques de stockage.',
        'bt-dv-sortie', P('Sortie et stockage', ('le moniteur', 'sortie'),
                          ('l’imprimante', 'sortie'), ('la clé USB', 'stockage'),
                          ('la disquette', 'stockage')),
        ('simple', 'La sortie montre le travail. Le stockage le garde pour plus tard.'),
        ('visuel', 'Sur une clé USB on range un fichier, comme un cahier dans un cartable.'),
        Q('La clé USB est un périphérique…', 'de stockage', 'd’entrée', 'de sortie'),
        Q('La disquette est un périphérique…', 'de stockage', 'd’entrée', 'de sortie'),
        V('Le moniteur est un périphérique de sortie.', True),
        T('La clé USB et la disquette sont des périphériques de {{1}}.', 'stockage'),
        A('Range chaque périphérique dans sa famille.', ('le clavier', 'entrée'),
          ('l’imprimante', 'sortie'), ('la clé USB', 'stockage')),
        V('La clé USB est un périphérique d’entrée.', False, n=4,
          e='Non. Elle garde les fichiers : périphérique de stockage.'),
        Q('Lequel est un périphérique de sortie ?', 'le moniteur', 'la disquette',
          'la souris', n=4)),

      N('definition',
        'La saisie kilométrique est le fait d’écrire un texte sans se soucier des fautes. On '
        'corrige quand le texte est fini. Elle permet de saisir rapidement et de saisir de '
        'longs textes.',
        'bt-dv-saisie', F('La saisie kilométrique', 'écrire sans s’arrêter aux fautes',
                          'corriger à la fin', 'on saisit rapidement', 'de longs textes'),
        ('simple', 'On tape tout d’un trait, comme on roule sur des kilomètres sans s’arrêter.'),
        ('pas_a_pas', 'D’abord tout le texte. Ensuite seulement, on revient corriger les '
                      'fautes.'),
        Q('Qu’est-ce qu’une saisie kilométrique ?',
          'Écrire un texte sans se soucier des fautes', 'Mesurer un texte en kilomètres',
          'Imprimer un texte très long'),
        V('Dans une saisie kilométrique, on corrige quand le texte est fini.', True),
        T('La saisie {{1}} est le fait d’écrire un texte sans se soucier des fautes.',
          'kilométrique'),
        Q('Quel est un avantage de la saisie kilométrique ?', 'On saisit rapidement',
          'On ne fait aucune faute', 'On n’a pas besoin de clavier', n=3),
        V('Dans une saisie kilométrique, on corrige chaque faute tout de suite.', False, n=4,
          e='Non. On écrit d’abord tout le texte, on corrige à la fin.')),

      N('liste',
        'Pour produire un texte kilométrique : je clique sur Démarrer, je clique sur Tous les '
        'programmes, je clique sur Microsoft Word, je saisis mon texte.',
        'bt-dv-etapes', F('Quatre étapes', '1. Démarrer', '2. Tous les programmes',
                          '3. Microsoft Word', '4. je saisis mon texte'),
        ('simple', 'On ouvre d’abord le logiciel. On ne peut pas saisir avant qu’il soit '
                   'ouvert.'),
        ('visuel', 'Saisir le texte vient toujours en dernier.'),
        Q('Quelle est la première étape ?', 'Je clique sur Démarrer', 'Je saisis mon texte',
          'Je clique sur Microsoft Word'),
        V('Je saisis mon texte après avoir ouvert Microsoft Word.', True),
        T('Après Démarrer et Tous les programmes, je clique sur Microsoft {{1}}.', 'word'),
        C('Remets les étapes en ordre.', 'je clique sur Démarrer',
          'je clique sur Tous les programmes', 'je clique sur Microsoft Word',
          'je saisis mon texte'),
        Q('Quelle est la dernière étape ?', 'Je saisis mon texte', 'Je clique sur Démarrer',
          'Je clique sur Tous les programmes', n=4)),

      N('date',
        'L’informatique est la science du traitement automatique de l’information par des '
        'machines appelées ordinateurs. Le premier ordinateur, inventé en 1946, est l’ENIAC.',
        'bt-dv-eniac', F('L’informatique', 'traitement automatique', 'de l’information',
                         'par des ordinateurs', '1946 : l’ENIAC', vif=(3,)),
        ('simple', 'L’informatique, c’est faire traiter l’information par une machine.'),
        ('visuel', 'ENIAC est le nom du tout premier ordinateur. Il date de 1946.'),
        Q('Comment s’appelle le premier ordinateur ?', 'L’ENIAC', 'Le laptop', 'Le desktop'),
        V('Le premier ordinateur a été inventé en 1946.', True),
        T('Le premier ordinateur, l’ENIAC, a été inventé en {{1}}.', '1946'),
        Q('Les machines qui traitent l’information s’appellent…', 'des ordinateurs',
          'des imprimantes', 'des disquettes', n=3),
        V('Le premier ordinateur s’appelle le laptop.', False, n=4,
          e='Non. C’est l’ENIAC. Le laptop est l’ordinateur portable.')),

      N('relation',
        'De nos jours on distingue le desktop, ou ordinateur de bureau, et le laptop, ou '
        'ordinateur portable.',
        'bt-dv-types', P('Deux ordinateurs', ('le desktop', 'de bureau'),
                         ('le laptop', 'portable')),
        ('simple', 'Le desktop reste sur le bureau. Le laptop se porte sous le bras.'),
        ('visuel', 'Desk veut dire bureau en anglais. Lap veut dire les genoux : on le pose '
                   'dessus.'),
        Q('Comment appelle-t-on l’ordinateur de bureau ?', 'Le desktop', 'Le laptop',
          'L’ENIAC'),
        V('Le laptop est l’ordinateur portable.', True),
        T('L’ordinateur portable s’appelle le {{1}}.', 'laptop'),
        A('Relie chaque nom à ce qu’il désigne.', ('le desktop', 'ordinateur de bureau'),
          ('le laptop', 'ordinateur portable'), ('l’ENIAC', 'le premier ordinateur')),
        V('Le desktop est l’ordinateur portable.', False, n=4,
          e='Non. Le desktop est l’ordinateur de bureau.'),
        Q('Comment appelle-t-on l’ordinateur portable ?', 'Le laptop', 'Le desktop',
          'Le moniteur', n=4)),
      ),

    # ------------------------------------------------------------ 23 octobre
    L(TIC, 'Les composantes d’un logiciel de traitement de texte', ENV, '2026-10-23',
      'Un logiciel de traitement de texte est un programme qui permet d’écrire sur '
      'l’ordinateur. Ses principales composantes sont : la barre de titre, la barre des menus, '
      'la zone de travail, les règles, les barres de défilement et la barre d’état.',
      'bt-tt-couv', ['barre de titre', 'zone de travail', 'barre d’état'],

      N('definition',
        'Un logiciel de traitement de texte est un programme qui permet d’écrire sur '
        'l’ordinateur.',
        'bt-tt-def', F('Le traitement de texte', 'un programme', 'pour écrire',
                       'sur l’ordinateur', 'exemple : Word'),
        ('simple', 'C’est le logiciel qu’on ouvre quand on veut taper un texte.'),
        ('visuel', 'Word est un logiciel de traitement de texte.'),
        Q('À quoi sert un logiciel de traitement de texte ?', 'À écrire sur l’ordinateur',
          'À écouter de la musique', 'À regarder des films'),
        V('Un logiciel de traitement de texte est un programme.', True),
        T('Un logiciel de traitement de {{1}} permet d’écrire sur l’ordinateur.', 'texte'),
        Q('Lequel est un logiciel de traitement de texte ?', 'Word', 'la souris',
          'la clé USB', n=3),
        V('Un logiciel de traitement de texte sert à dessiner des cartes.', False, n=4,
          e='Non. Il sert à écrire sur l’ordinateur.')),

      N('definition',
        'La barre de titre affiche le nom du document, par exemple Word ou Document. Elle '
        'contient les boutons réduire, agrandir, fermer.',
        'bt-tt-titre', F('La barre de titre', 'le nom du document', 'réduire', 'agrandir',
                         'fermer'),
        ('simple', 'Tout en haut de la fenêtre : le nom du document, et trois boutons.'),
        ('visuel', 'Les trois boutons sont à droite : réduire, agrandir, fermer.'),
        Q('Qu’affiche la barre de titre ?', 'Le nom du document', 'Le nombre de mots',
          'Les marges de la page'),
        V('La barre de titre contient les boutons réduire, agrandir, fermer.', True),
        T('La barre de {{1}} affiche le nom du document.', 'titre'),
        Q('Lequel est un bouton de la barre de titre ?', 'fermer', 'insérer', 'imprimer', n=3),
        V('La barre de titre indique le numéro de page.', False, n=4,
          e='Non. C’est la barre d’état qui l’indique.')),

      N('relation',
        'La barre des menus, c’est le cerveau du logiciel. La zone de travail ou page, c’est '
        'la feuille blanche où l’on saisit le texte.',
        'bt-tt-menus', P('Deux composantes', ('la barre des menus', 'le cerveau'),
                         ('la zone de travail', 'la feuille blanche')),
        ('simple', 'Les menus commandent. La page reçoit ce qu’on tape.'),
        ('visuel', 'La zone de travail est le grand rectangle blanc au milieu de l’écran.'),
        Q('Quelle composante est le cerveau du logiciel ?', 'La barre des menus',
          'La barre d’état', 'Les règles'),
        V('La zone de travail est la feuille blanche où l’on saisit le texte.', True),
        T('La barre des {{1}} est le cerveau du logiciel.', 'menus'),
        Q('Où saisit-on le texte ?', 'Dans la zone de travail', 'Dans la barre de titre',
          'Dans la barre d’état', n=3),
        V('La zone de travail s’appelle aussi la page.', True, n=4)),

      N('relation',
        'Les règles servent à régler les marges et les tabulations. Les barres de défilement '
        'servent à monter et descendre dans le document quand il est long.',
        'bt-tt-regles', P('Deux composantes', ('les règles', 'les marges'),
                          ('le défilement', 'monter, descendre')),
        ('simple', 'Les règles mesurent la page. Les barres de défilement la font bouger.'),
        ('visuel', 'Quand le texte dépasse l’écran, on tire la barre de défilement pour voir '
                   'la suite.'),
        Q('À quoi servent les règles ?', 'À régler les marges et les tabulations',
          'À fermer le document', 'À compter les mots'),
        V('Les barres de défilement servent à monter et descendre dans le document.', True),
        T('Les règles servent à régler les {{1}} et les tabulations.', 'marges'),
        Q('Quelle composante sert à descendre dans un long document ?',
          'Les barres de défilement', 'La barre de titre', 'La barre des menus', n=3),
        V('Les règles servent à monter et descendre dans le document.', False, n=4,
          e='Non. Ce sont les barres de défilement.')),

      N('definition',
        'La barre d’état indique le numéro de page, par exemple 1/8, le nombre de mots et la '
        'langue.',
        'bt-tt-etat', F('La barre d’état', 'le numéro de page : 1/8', 'le nombre de mots',
                        'la langue'),
        ('simple', 'Tout en bas de la fenêtre, elle dit où on en est.'),
        ('visuel', '1/8 veut dire : page 1 sur 8.'),
        Q('Qu’indique la barre d’état ?', 'Le numéro de page', 'Le nom du document',
          'Les boutons fermer'),
        V('La barre d’état indique le nombre de mots.', True),
        T('La barre d’{{1}} indique le numéro de page, le nombre de mots et la langue.',
          'état'),
        A('Relie chaque composante à son rôle.', ('la barre de titre', 'le nom du document'),
          ('la barre d’état', 'le numéro de page'), ('les règles', 'les marges'),
          ('la zone de travail', 'le texte')),
        Q('Dans la barre d’état, que veut dire 1/8 ?', 'Page 1 sur 8', '1 mot sur 8',
          '8 documents ouverts', n=4),
        V('La barre d’état indique la langue.', True, n=4)),
      ),

    # ------------------------------------------------- entre le 23 et le 28
    L(TIC, 'Insérer une image dans un document Word', OUTILS, '2026-10-23',
      'Pendant une saisie, on peut avoir envie d’insérer une image dans le texte. Il y a six '
      'étapes : cliquer à l’endroit voulu, cliquer sur l’onglet Insertion, cliquer sur l’icône '
      'Image, rechercher l’image dans les dossiers, cliquer sur l’image, cliquer sur Insérer.',
      'bt-im-couv', ['Insertion', 'Image', 'Insérer'],

      N('liste',
        'Les trois premières étapes : cliquer sur l’endroit où l’on veut insérer l’image, '
        'cliquer sur l’onglet Insertion, cliquer sur l’icône Image.',
        'bt-im-debut', F('Pour commencer', '1. l’endroit voulu', '2. l’onglet Insertion',
                         '3. l’icône Image'),
        ('simple', 'On dit d’abord où, puis on ouvre Insertion, puis on choisit Image.'),
        ('visuel', 'Un onglet est un titre en haut de la fenêtre : Accueil, Insertion.'),
        Q('Quelle est la première étape pour insérer une image ?',
          'Cliquer à l’endroit voulu', 'Cliquer sur Insérer', 'Cliquer sur l’icône Image'),
        V('Pour insérer une image, on clique sur l’onglet Insertion.', True),
        T('On clique sur l’onglet Insertion, puis sur l’icône {{1}}.', 'image'),
        C('Range les trois premières étapes dans l’ordre.', 'cliquer à l’endroit voulu',
          'cliquer sur l’onglet Insertion', 'cliquer sur l’icône Image'),
        V('L’icône Image se trouve dans l’onglet Insertion.', True, n=4)),

      N('liste',
        'Les trois dernières étapes : rechercher l’image dans l’arborescence des dossiers de '
        'l’ordinateur, cliquer sur l’image choisie, cliquer sur Insérer.',
        'bt-im-fin', F('Pour finir', '4. rechercher l’image', '5. cliquer sur l’image',
                       '6. cliquer sur Insérer'),
        ('simple', 'On cherche l’image, on la choisit, on valide.'),
        ('visuel', 'L’arborescence, ce sont les dossiers rangés les uns dans les autres, comme '
                   'les branches d’un arbre.'),
        Q('Quelle est la dernière étape pour insérer une image ?', 'Cliquer sur Insérer',
          'Cliquer sur l’onglet Insertion', 'Rechercher l’image'),
        V('On recherche l’image dans l’arborescence des dossiers de l’ordinateur.', True),
        T('On recherche l’image dans l’arborescence des {{1}} de l’ordinateur.', 'dossiers'),
        C('Range les trois dernières étapes dans l’ordre.', 'rechercher l’image',
          'cliquer sur l’image choisie', 'cliquer sur Insérer'),
        Q('Combien d’étapes faut-il pour insérer une image ?', 'Six', 'Deux', 'Dix', n=4),
        V('On clique sur Insérer avant de choisir l’image.', False, n=4,
          e='Non. On choisit l’image, puis on clique sur Insérer.')),
      ),

    # ------------------------------------------------------------ 28 octobre
    L(TIC, 'Insérer un tableau dans un document Word', OUTILS, '2026-10-28',
      'Pour insérer un tableau dans un document Word, il faut : cliquer à l’endroit voulu, '
      'cliquer sur l’onglet Insertion, cliquer sur l’icône Tableau, cliquer sur Insérer un '
      'tableau, préciser le nombre de lignes et de colonnes, puis cliquer sur OK.',
      'bt-tb-couv', ['Insertion', 'Tableau', 'OK'],

      N('liste',
        'Les trois premières étapes : cliquer sur l’endroit où on veut insérer le tableau, '
        'cliquer sur l’onglet Insertion, cliquer sur l’icône Tableau.',
        'bt-tb-debut', F('Pour commencer', '1. l’endroit voulu', '2. l’onglet Insertion',
                         '3. l’icône Tableau'),
        ('simple', 'Comme pour l’image : l’endroit, puis Insertion. Seule l’icône change.'),
        ('visuel', 'L’image et le tableau se trouvent tous les deux dans l’onglet Insertion.'),
        Q('Sur quel onglet clique-t-on pour insérer un tableau ?', 'Insertion', 'Accueil',
          'Affichage'),
        V('Pour insérer un tableau, on clique sur l’icône Tableau.', True),
        T('On clique sur l’onglet Insertion, puis sur l’icône {{1}}.', 'tableau'),
        C('Range les trois premières étapes dans l’ordre.', 'cliquer à l’endroit voulu',
          'cliquer sur l’onglet Insertion', 'cliquer sur l’icône Tableau'),
        V('L’icône Tableau se trouve dans l’onglet Insertion.', True, n=4)),

      N('liste',
        'Les trois dernières étapes : cliquer sur Insérer un tableau, préciser le nombre de '
        'lignes et de colonnes dans la boîte de dialogue qui apparaît, cliquer sur OK.',
        'bt-tb-fin', F('Pour finir', '4. Insérer un tableau', '5. lignes et colonnes',
                       '6. cliquer sur OK'),
        ('simple', 'Le logiciel demande combien de lignes et de colonnes. On répond, puis OK.'),
        ('visuel', 'Une boîte de dialogue est une petite fenêtre qui pose une question.'),
        Q('Que précise-t-on dans la boîte de dialogue ?',
          'Le nombre de lignes et de colonnes', 'Le nom du document',
          'La couleur de la page'),
        V('On termine en cliquant sur OK.', True),
        T('On précise le nombre de lignes et de {{1}}.', 'colonnes'),
        C('Range les trois dernières étapes dans l’ordre.', 'cliquer sur Insérer un tableau',
          'préciser les lignes et les colonnes', 'cliquer sur OK'),
        Q('Où précise-t-on le nombre de lignes et de colonnes ?',
          'Dans la boîte de dialogue', 'Dans la barre de titre', 'Dans la barre d’état',
          n=4),
        V('On clique sur OK avant de préciser les lignes et les colonnes.', False, n=4,
          e='Non. On précise d’abord, on clique sur OK ensuite.')),
      ),

    # ------------------------------------------------------------ 29 octobre
    L(TIC, 'Le code de conduite en communication', CODE, '2026-10-29',
      'Communiquer, c’est échanger des informations avec les autres. Avec les outils modernes '
      'de communication, nous devons respecter certaines règles de conduite : être poli, ne '
      'pas lire les communications d’autrui, ne pas converser avec les inconnus.',
      'bt-cc-couv', ['être poli', 'demander', 'rendre en bon état'],

      N('definition',
        'Communiquer, c’est échanger des informations avec les autres. Avec les outils '
        'modernes de communication, nous devons respecter certaines règles de conduite.',
        'bt-cc-def', F('Communiquer', 'échanger des informations', 'avec les autres',
                       'en respectant des règles'),
        ('simple', 'Parler au téléphone, écrire un message : c’est communiquer.'),
        ('visuel', 'Le téléphone est un outil moderne de communication.'),
        Q('Que veut dire communiquer ?', 'Échanger des informations avec les autres',
          'Jouer tout seul sur un téléphone', 'Éteindre son appareil'),
        V('Avec les outils de communication, on doit respecter des règles de conduite.', True),
        T('Communiquer, c’est {{1}} des informations avec les autres.', 'échanger'),
        Q('Lequel est un outil moderne de communication ?', 'le téléphone', 'le canari',
          'la règle', n=3),
        V('Avec un téléphone, on peut faire tout ce qu’on veut.', False, n=4,
          e='Non. Il y a des règles de conduite à respecter.')),

      N('liste',
        'Trois règles : être poli au téléphone ; ne pas écouter ni lire les communications '
        'd’autrui ; ne pas utiliser le téléphone d’autrui sans autorisation.',
        'bt-cc-regles1', F('Trois règles', 'être poli au téléphone',
                           'ne pas lire les messages d’autrui', 'demander l’autorisation'),
        ('simple', 'Autrui, c’est une autre personne que toi.'),
        ('visuel', 'Avant de prendre le téléphone de ton frère, tu demandes.'),
        Q('Comment doit-on être au téléphone ?', 'Poli', 'Pressé', 'Bruyant'),
        V('On ne doit pas lire les communications d’autrui.', True),
        T('On n’utilise pas le téléphone d’autrui sans {{1}}.', 'autorisation'),
        Q('Que veut dire « autrui » ?', 'Une autre personne', 'Un appareil neuf',
          'Un message secret', n=3),
        V('On peut utiliser le téléphone d’autrui sans rien demander.', False, n=4,
          e='Non. Il faut son autorisation.')),

      N('liste',
        'Ne pas converser avec les inconnus ; éviter d’accéder aux informations '
        'personnelles ; garder soigneusement l’appareil et le remettre à son propriétaire '
        'dans son état initial.',
        'bt-cc-regles2', F('Trois autres règles', 'pas de conversation avec un inconnu',
                           'pas d’accès aux photos, messages', 'rendre l’appareil en bon état'),
        ('simple', 'Les vidéos, les photos et les messages d’une personne sont à elle.'),
        ('visuel', 'État initial veut dire : comme il était quand on te l’a prêté.'),
        Q('Avec qui ne doit-on pas converser ?', 'Avec les inconnus', 'Avec ses parents',
          'Avec sa maîtresse'),
        V('On doit remettre l’appareil à son propriétaire dans son état initial.', True),
        T('On ne converse pas avec les {{1}}.', 'inconnus'),
        Q('Lesquelles sont des informations personnelles ?', 'Les vidéos, photos et messages',
          'Les leçons du cahier', 'Les titres des journaux', n=3),
        V('On peut regarder les photos d’un téléphone qu’on nous a prêté.', False, n=4,
          e='Non. On évite d’accéder aux informations personnelles.'),
        Q('Comment rend-on un appareil qu’on nous a prêté ?', 'Dans son état initial',
          'Avec de nouveaux jeux', 'Sans sa batterie', n=4)),
      ),
]
