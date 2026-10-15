# -*- coding: utf-8 -*-
"""
Les questions des trois étapes, pour les deux leçons déjà importées.

Écrites à la main parce que la fonction d'extraction n'est pas encore
déployée. Elles suivent exactement le format qu'elle produira, et la même
règle de niveaux :

  niveau 1 — Découverte     reconnaître. Trois choix, la réponse est dans le
                            résumé, aucun piège.
  niveau 2 — Entraînement   comprendre. Quatre choix, les distracteurs sont
                            plausibles (les autres dates, les autres peuples).
  niveau 3 — Défi           restituer. Texte à trous, chronologie, ou une
                            question de raisonnement.

Deux formulations par niveau et par notion : un enfant qui se trompe doit
revoir la notion, pas réapprendre la position de la bonne case.

Les notions sont désignées par (titre de la leçon, sort_order) : stable, et
lisible dans la migration produite.

Usage :  python work/questions-paliers.py
         → écrit la migration SQL et le fichier JSON d'application.
"""

import io
import json
import os

# (kind, level, payload, answer, explain)
PREHISTOIRE = {
    1: [  # La Préhistoire va de l'apparition des premiers humains à l'écriture.
        ('qcm', 1, {'question': 'Par quoi commence la Préhistoire ?',
                    'options': ['L’apparition des premiers humains', 'L’invention de l’écriture', 'La construction des villes']},
         {'index': 0}, 'Elle commence avec les premiers humains.'),
        ('qcm', 1, {'question': 'La Préhistoire est le temps des premiers…',
                    'options': ['humains', 'rois', 'machines']},
         {'index': 0}, 'C’est le temps des premiers humains.'),
        ('qcm', 2, {'question': 'La Préhistoire s’arrête à quelle invention ?',
                    'options': ['L’écriture', 'La roue', 'Le feu', 'Les métaux']},
         {'index': 0}, 'Elle s’arrête à l’invention de l’écriture.'),
        ('qcm', 2, {'question': 'Combien d’époques compte la Préhistoire ?',
                    'options': ['Trois', 'Deux', 'Cinq', 'Dix']},
         {'index': 0}, 'Trois : Paléolithique, Néolithique, âge des métaux.'),
        ('qcm', 3, {'question': 'Pourquoi dit-on « Préhistoire » ?',
                    'options': ['Parce que c’est avant l’Histoire écrite', 'Parce que les humains ne parlaient pas',
                                'Parce qu’il n’y avait pas d’animaux', 'Parce qu’il faisait très froid']},
         {'index': 0}, '« Pré » veut dire avant : avant l’écriture.'),
        ('texte_a_trous', 3, {'text': 'La Préhistoire va de l’apparition des premiers {{1}} à l’invention de l’{{2}}.', 'blanks': 2},
         {'values': ['humains', 'écriture']}, 'Des premiers humains à l’écriture.'),
    ],
    2: [  # L'écriture, vers 3 000 avant J.-C.
        ('qcm', 1, {'question': 'L’écriture marque la fin de quelle période ?',
                    'options': ['La Préhistoire', 'Le Moyen Âge', 'L’époque des machines']},
         {'index': 0}, 'L’écriture termine la Préhistoire.'),
        ('qcm', 2, {'question': 'Vers quelle date l’écriture est-elle inventée ?',
                    'options': ['Vers 3 000 avant J.-C.', 'Vers 300 avant J.-C.', 'Vers 3 000 après J.-C.', 'Vers 30 avant J.-C.']},
         {'index': 0}, 'Vers 3 000 avant J.-C.'),
        ('texte_a_trous', 3, {'text': 'L’invention de l’{{1}} marque la fin de la {{2}}.', 'blanks': 2},
         {'values': ['écriture', 'Préhistoire']}, 'L’écriture termine la Préhistoire.'),
    ],
    3: [  # Le Paléolithique, pierre taillée.
        ('qcm', 1, {'question': 'Le Paléolithique est l’âge de la pierre…',
                    'options': ['taillée', 'polie', 'peinte']},
         {'index': 0}, 'Paléolithique : pierre taillée.'),
        ('qcm', 1, {'question': 'À quoi sert la pierre taillée ?',
                    'options': ['À fabriquer des outils', 'À faire du pain', 'À écrire']},
         {'index': 0}, 'On taille la pierre pour en faire des outils.'),
        ('qcm', 2, {'question': 'Quel outil est typique du Paléolithique ?',
                    'options': ['Le biface, une pierre taillée', 'La charrue', 'Le marteau en fer', 'Le stylo']},
         {'index': 0}, 'Le biface est une pierre taillée des deux côtés.'),
        ('texte_a_trous', 3, {'text': 'Le {{1}} est l’âge de la pierre {{2}}.', 'blanks': 2},
         {'values': ['Paléolithique', 'taillée']}, 'Paléolithique : pierre taillée.'),
        ('qcm', 3, {'question': 'Pourquoi dit-on pierre « taillée » ?',
                    'options': ['Parce qu’on la casse pour lui donner un bord coupant', 'Parce qu’on la frotte pour la rendre lisse',
                                'Parce qu’on la cuit au feu', 'Parce qu’on la peint']},
         {'index': 0}, 'Tailler, c’est casser la pierre pour la rendre coupante.'),
    ],
    4: [  # Chasse, pêche, cueillette.
        ('qcm', 1, {'question': 'Au Paléolithique, comment se nourrit-on ?',
                    'options': ['En chassant et en cueillant', 'En cultivant des champs', 'En achetant au marché']},
         {'index': 0}, 'Chasse, pêche et cueillette.'),
        ('qcm', 1, {'question': 'Au Paléolithique, cultive-t-on la terre ?',
                    'options': ['Non, on chasse et on cueille', 'Oui, on cultive du blé']},
         {'index': 0}, 'L’agriculture viendra plus tard, au Néolithique.'),
        ('qcm', 2, {'question': 'Laquelle de ces activités n’existe PAS au Paléolithique ?',
                    'options': ['L’agriculture', 'La chasse', 'La pêche', 'La cueillette']},
         {'index': 0}, 'L’agriculture commence au Néolithique.'),
        ('qcm', 3, {'question': 'Pourquoi les humains du Paléolithique se déplacent-ils souvent ?',
                    'options': ['Ils suivent les animaux et les fruits sauvages', 'Ils cherchent du métal',
                                'Ils vont d’une ville à l’autre', 'Ils fuient la pluie']},
         {'index': 0}, 'Ils suivent leur nourriture : ils sont nomades.'),
    ],
    5: [  # Le Néolithique, pierre polie, agriculture.
        ('qcm', 1, {'question': 'Le Néolithique est l’âge de la pierre…',
                    'options': ['polie', 'taillée', 'peinte']},
         {'index': 0}, 'Néolithique : pierre polie.'),
        ('qcm', 2, {'question': 'Qu’est-ce qui change au Néolithique ?',
                    'options': ['Les humains cultivent et élèvent des animaux', 'Les humains inventent l’écriture',
                                'Les humains fabriquent du fer', 'Les humains arrêtent de fabriquer des outils']},
         {'index': 0}, 'Au Néolithique commence l’agriculture.'),
        ('texte_a_trous', 3, {'text': 'Le {{1}} est l’âge de la pierre {{2}}.', 'blanks': 2},
         {'values': ['Néolithique', 'polie']}, 'Néolithique : pierre polie.'),
        ('qcm', 3, {'question': 'Pourquoi l’agriculture change-t-elle la vie des humains ?',
                    'options': ['Ils se fixent et construisent des villages', 'Ils deviennent nomades',
                                'Ils arrêtent de fabriquer des outils', 'Ils inventent l’écriture']},
         {'index': 0}, 'On reste près de ses champs : les villages naissent.'),
    ],
    6: [  # L'âge des métaux.
        ('qcm', 1, {'question': 'À l’âge des métaux, avec quoi fabrique-t-on les outils ?',
                    'options': ['Avec du métal', 'Avec du papier', 'Avec du verre']},
         {'index': 0}, 'Des outils en métal, pas en pierre.'),
        ('qcm', 1, {'question': 'Quel est un métal de cette époque ?',
                    'options': ['Le cuivre', 'Le plastique', 'Le carton']},
         {'index': 0}, 'Cuivre, bronze et fer.'),
        ('qcm', 2, {'question': 'Quels métaux les humains utilisent-ils à cette époque ?',
                    'options': ['Le cuivre, le bronze et le fer', 'L’or, l’argent et le plastique',
                                'Le fer, le verre et le bois', 'Le bronze, le papier et la pierre']},
         {'index': 0}, 'Cuivre, bronze, puis fer.'),
        ('chronologie', 3, {'question': 'Remets ces métaux dans l’ordre où on les a utilisés.',
                            'tokens': ['Cuivre', 'Bronze', 'Fer']},
         {'order': [0, 1, 2]}, 'Cuivre, puis bronze, puis fer.'),
        ('texte_a_trous', 3, {'text': 'À l’âge des métaux, on fabrique des outils et des bijoux en {{1}}, en bronze et en {{2}}.', 'blanks': 2},
         {'values': ['cuivre', 'fer']}, 'Cuivre, bronze et fer.'),
    ],
    7: [  # L'ordre des trois époques.
        ('qcm', 1, {'question': 'Combien d’époques se suivent dans la Préhistoire ?',
                    'options': ['Trois', 'Deux', 'Six']},
         {'index': 0}, 'Paléolithique, Néolithique, âge des métaux.'),
        ('qcm', 2, {'question': 'Quelle période vient juste après le Paléolithique ?',
                    'options': ['Le Néolithique', 'L’âge des métaux', 'L’écriture', 'La pierre taillée']},
         {'index': 0}, 'Paléolithique, puis Néolithique.'),
        ('qcm', 2, {'question': 'Quelle période vient en dernier ?',
                    'options': ['L’âge des métaux', 'Le Néolithique', 'Le Paléolithique', 'La pierre polie']},
         {'index': 0}, 'L’âge des métaux termine la Préhistoire.'),
        ('texte_a_trous', 3, {'text': 'Les trois époques sont le {{1}}, le {{2}} et l’âge des {{3}}.', 'blanks': 3},
         {'values': ['Paléolithique', 'Néolithique', 'métaux']}, 'Dans cet ordre.'),
    ],
}

DECOUVERTES = {
    1: [  # Une invention.
        ('qcm', 1, {'question': 'Inventer, c’est…',
                    'options': ['créer quelque chose de nouveau', 'copier quelque chose', 'acheter quelque chose']},
         {'index': 0}, 'Inventer, c’est créer ce qui n’existait pas.'),
        ('qcm', 2, {'question': 'Laquelle de ces phrases décrit une invention ?',
                    'options': ['Fabriquer le premier bateau à voile', 'Trouver une pièce par terre',
                                'Lire un livre', 'Marcher jusqu’à la rivière']},
         {'index': 0}, 'On crée un objet qui n’existait pas.'),
        ('qcm', 2, {'question': 'Quelle est la différence entre inventer et découvrir ?',
                    'options': ['Inventer, c’est créer ; découvrir, c’est trouver ce qui existait déjà',
                                'Inventer, c’est trouver ; découvrir, c’est créer',
                                'Il n’y a aucune différence', 'Inventer, c’est copier']},
         {'index': 0}, 'On invente un objet, on découvre un lieu.'),
        ('texte_a_trous', 3, {'text': 'Une {{1}} est la création d’un objet qui n’existait pas avant.', 'blanks': 1},
         {'values': ['invention']}, 'Une invention.'),
        ('qcm', 3, {'question': 'Christophe Colomb a-t-il inventé l’Amérique ?',
                    'options': ['Non, il l’a découverte : elle existait déjà', 'Oui, il l’a inventée',
                                'Oui, avec Gutenberg', 'Non, il a inventé la caravelle']},
         {'index': 0}, 'On découvre une terre, on ne l’invente pas.'),
    ],
    2: [  # Papier et poudre, 1er siècle.
        ('qcm', 1, {'question': 'Qui invente la poudre à canon ?',
                    'options': ['Les Chinois', 'Les Français', 'Les Portugais']},
         {'index': 0}, 'Les Chinois, au 1ᵉʳ siècle.'),
        ('qcm', 2, {'question': 'Qu’inventent les Chinois au 1ᵉʳ siècle ?',
                    'options': ['Le papier et la poudre à canon', 'La caravelle et l’imprimerie',
                                'La boussole et le gouvernail', 'Le fer et le bronze']},
         {'index': 0}, 'Le papier et la poudre à canon.'),
        ('qcm', 2, {'question': 'À quel siècle le papier est-il inventé ?',
                    'options': ['Au 1ᵉʳ siècle', 'Au VIIᵉ siècle', 'Au XIIᵉ siècle', 'En 1440']},
         {'index': 0}, 'Au 1ᵉʳ siècle.'),
        ('texte_a_trous', 3, {'text': 'Les Chinois inventent le {{1}} et la {{2}} à canon au 1ᵉʳ siècle.', 'blanks': 2},
         {'values': ['papier', 'poudre']}, 'Le papier et la poudre.'),
        ('chronologie', 3, {'question': 'Remets ces inventions chinoises dans l’ordre.',
                            'tokens': ['Le papier, 1ᵉʳ siècle', 'La boussole, VIIᵉ siècle', 'Le gouvernail, XIIᵉ siècle']},
         {'order': [0, 1, 2]}, 'Papier, boussole, gouvernail.'),
    ],
    3: [  # La boussole, VIIe siècle.
        ('qcm', 1, {'question': 'Qui invente la boussole ?',
                    'options': ['Les Chinois', 'Les Portugais', 'Les Allemands']},
         {'index': 0}, 'Les Chinois, au VIIᵉ siècle.'),
        ('qcm', 1, {'question': 'La boussole indique…',
                    'options': ['le nord', 'l’heure', 'la pluie']},
         {'index': 0}, 'Elle montre toujours le nord.'),
        ('qcm', 2, {'question': 'À quel siècle la boussole est-elle inventée ?',
                    'options': ['Au VIIᵉ siècle', 'Au 1ᵉʳ siècle', 'Au XIIᵉ siècle', 'En 1492']},
         {'index': 0}, 'Au VIIᵉ siècle.'),
        ('texte_a_trous', 3, {'text': 'Les Chinois inventent la {{1}} au VIIᵉ siècle.', 'blanks': 1},
         {'values': ['boussole']}, 'La boussole.'),
        ('qcm', 3, {'question': 'Pourquoi la boussole est-elle utile aux marins ?',
                    'options': ['Elle donne la direction même quand on ne voit plus la terre',
                                'Elle fait avancer le bateau', 'Elle imprime les cartes', 'Elle sert à pêcher']},
         {'index': 0}, 'En pleine mer, elle montre où est le nord.'),
    ],
    4: [  # Le gouvernail, XIIe siècle.
        ('qcm', 1, {'question': 'Le gouvernail sert à…',
                    'options': ['diriger le bateau', 'écrire', 'cuisiner']},
         {'index': 0}, 'Il dirige le bateau.'),
        ('qcm', 1, {'question': 'Qui invente le gouvernail ?',
                    'options': ['Les Chinois', 'Les Allemands', 'Les Portugais']},
         {'index': 0}, 'Les Chinois, au XIIᵉ siècle.'),
        ('qcm', 2, {'question': 'À quel siècle le gouvernail est-il inventé ?',
                    'options': ['Au XIIᵉ siècle', 'Au VIIᵉ siècle', 'Au 1ᵉʳ siècle', 'En 1450']},
         {'index': 0}, 'Au XIIᵉ siècle.'),
        ('texte_a_trous', 3, {'text': 'Les Chinois inventent le {{1}} au XIIᵉ siècle.', 'blanks': 1},
         {'values': ['gouvernail']}, 'Le gouvernail.'),
        ('qcm', 3, {'question': 'Boussole et gouvernail : que permettent-ils ensemble ?',
                    'options': ['Trouver la direction et la suivre', 'Imprimer des livres',
                                'Fabriquer du papier', 'Cultiver la terre']},
         {'index': 0}, 'L’une montre la route, l’autre la suit.'),
    ],
    5: [  # La caravelle, 1440.
        ('qcm', 1, {'question': 'La caravelle est…',
                    'options': ['un bateau', 'un livre', 'une arme']},
         {'index': 0}, 'Un bateau rapide et solide.'),
        ('qcm', 1, {'question': 'Qui invente la caravelle ?',
                    'options': ['Les Portugais', 'Les Chinois', 'Les Allemands']},
         {'index': 0}, 'Les Portugais, en 1440.'),
        ('qcm', 2, {'question': 'En quelle année la caravelle est-elle inventée ?',
                    'options': ['1440', '1450', '1487', '1492']},
         {'index': 0}, 'En 1440.'),
        ('texte_a_trous', 3, {'text': 'Les {{1}} inventent la caravelle en {{2}}.', 'blanks': 2},
         {'values': ['Portugais', '1440']}, 'Les Portugais, en 1440.'),
        ('qcm', 3, {'question': 'Pourquoi la caravelle change-t-elle les voyages ?',
                    'options': ['Elle est solide et rapide : elle peut aller très loin',
                                'Elle est plus petite qu’une barque', 'Elle avance sans vent',
                                'Elle sert à imprimer des cartes']},
         {'index': 0}, 'Elle tient la haute mer, longtemps.'),
    ],
    6: [  # L'imprimerie, 1450, Gutenberg.
        ('qcm', 1, {'question': 'Qui invente l’imprimerie ?',
                    'options': ['Gutenberg', 'Colomb', 'Magellan']},
         {'index': 0}, 'L’Allemand Gutenberg, en 1450.'),
        ('qcm', 1, {'question': 'L’imprimerie sert à…',
                    'options': ['copier des livres rapidement', 'naviguer', 'cultiver la terre']},
         {'index': 0}, 'Elle copie les livres vite.'),
        ('qcm', 2, {'question': 'En quelle année l’imprimerie est-elle inventée ?',
                    'options': ['1450', '1440', '1487', '1498']},
         {'index': 0}, 'En 1450.'),
        ('qcm', 3, {'question': 'Pourquoi l’imprimerie est-elle importante ?',
                    'options': ['Les livres et les cartes se copient vite et circulent partout',
                                'Elle permet de traverser l’océan', 'Elle remplace la boussole',
                                'Elle fabrique le papier']},
         {'index': 0}, 'Le savoir voyage avec les livres.'),
    ],
    7: [  # Ces inventions favorisent la navigation.
        ('qcm', 1, {'question': 'Grâce à ces inventions, les marins peuvent…',
                    'options': ['aller plus loin', 'rester au port', 'voler']},
         {'index': 0}, 'Ils partent plus loin, plus sûrement.'),
        ('qcm', 1, {'question': 'Ces inventions ont surtout aidé…',
                    'options': ['la navigation', 'la cuisine', 'l’école']},
         {'index': 0}, 'Elles ont aidé la navigation.'),
        ('qcm', 2, {'question': 'Quelles inventions aident les marins à partir loin ?',
                    'options': ['La boussole, le gouvernail et la caravelle', 'Le papier et la poudre',
                                'L’imprimerie et le papier', 'La charrue et la roue']},
         {'index': 0}, 'Direction, pilotage et bon bateau.'),
        ('qcm', 3, {'question': 'Pourquoi les grandes découvertes viennent-elles après les grandes inventions ?',
                    'options': ['Il fallait d’abord des bateaux et des instruments pour partir loin',
                                'Les marins n’avaient pas envie avant', 'Parce que l’écriture venait d’être inventée',
                                'Parce que la Terre a changé de forme']},
         {'index': 0}, 'Sans ces outils, le grand large est impossible.'),
        ('texte_a_trous', 3, {'text': 'Ces inventions ont favorisé la {{1}} et les grands {{2}}.', 'blanks': 2},
         {'values': ['navigation', 'voyages']}, 'La navigation et les grands voyages.'),
    ],
    8: [  # Dias, 1487.
        ('qcm', 1, {'question': 'Qui atteint le cap de Bonne-Espérance ?',
                    'options': ['Bartholomeu Dias', 'Christophe Colomb', 'Gutenberg']},
         {'index': 0}, 'Bartholomeu Dias, en 1487.'),
        ('qcm', 1, {'question': 'Où se trouve le cap de Bonne-Espérance ?',
                    'options': ['Au sud de l’Afrique', 'En Amérique', 'En Chine']},
         {'index': 0}, 'Tout au sud de l’Afrique.'),
        ('qcm', 2, {'question': 'En quelle année Dias atteint-il le cap de Bonne-Espérance ?',
                    'options': ['1487', '1492', '1498', '1519']},
         {'index': 0}, 'En 1487.'),
        ('texte_a_trous', 3, {'text': 'Bartholomeu {{1}} atteint le cap de Bonne-Espérance en {{2}}.', 'blanks': 2},
         {'values': ['Dias', '1487']}, 'Dias, en 1487.'),
        ('qcm', 3, {'question': 'Pourquoi le cap de Bonne-Espérance compte-t-il autant ?',
                    'options': ['Il ouvre la route vers l’océan Indien, au sud de l’Afrique',
                                'C’est le point le plus au nord du monde', 'C’est là que Colomb est arrivé',
                                'C’est une ville d’Allemagne']},
         {'index': 0}, 'En le passant, on peut filer vers les Indes.'),
    ],
    9: [  # Colomb, 1492.
        ('qcm', 1, {'question': 'Christophe Colomb découvre…',
                    'options': ['l’Amérique', 'la Chine', 'l’Australie']},
         {'index': 0}, 'L’Amérique, en 1492.'),
        ('qcm', 1, {'question': 'En quelle année Colomb arrive-t-il en Amérique ?',
                    'options': ['1492', '1892', '1192']},
         {'index': 0}, 'En 1492.'),
        ('qcm', 2, {'question': 'Que cherchait Christophe Colomb en partant vers l’ouest ?',
                    'options': ['La route des Indes', 'L’Amérique', 'Le cap de Bonne-Espérance', 'L’Allemagne']},
         {'index': 0}, 'Il cherchait les Indes, il trouve l’Amérique.'),
        ('qcm', 3, {'question': 'Pourquoi dit-on que Colomb a « découvert » l’Amérique ?',
                    'options': ['Les Européens ne la connaissaient pas, mais des peuples y vivaient déjà',
                                'Parce qu’il l’a inventée', 'Parce que personne n’y habitait',
                                'Parce qu’il y est né']},
         {'index': 0}, 'Découverte pour les Européens seulement.'),
    ],
    10: [  # Vasco de Gama, 1498.
        ('qcm', 1, {'question': 'Qui trouve la route des Indes ?',
                    'options': ['Vasco de Gama', 'Bartholomeu Dias', 'Gutenberg']},
         {'index': 0}, 'Vasco de Gama, en 1498.'),
        ('qcm', 1, {'question': 'Aux Indes, les marins vont chercher…',
                    'options': ['des épices', 'de la neige', 'du charbon']},
         {'index': 0}, 'Les épices valaient très cher.'),
        ('qcm', 2, {'question': 'En quelle année Vasco de Gama arrive-t-il aux Indes ?',
                    'options': ['1498', '1487', '1492', '1522']},
         {'index': 0}, 'En 1498.'),
        ('texte_a_trous', 3, {'text': 'Vasco de {{1}} trouve la route des Indes en {{2}}.', 'blanks': 2},
         {'values': ['Gama', '1498']}, 'Vasco de Gama, en 1498.'),
        ('qcm', 3, {'question': 'Pourquoi cherchait-on une route vers les Indes ?',
                    'options': ['Pour acheter des épices et des tissus', 'Pour visiter l’Amérique',
                                'Pour fuir l’Europe', 'Pour imprimer des livres']},
         {'index': 0}, 'Pour le commerce des épices.'),
    ],
    11: [  # Magellan, 1519-1522.
        ('qcm', 1, {'question': 'Magellan et son équipage font le premier…',
                    'options': ['tour du monde', 'livre imprimé', 'bateau en métal']},
         {'index': 0}, 'Le premier tour du monde.'),
        ('qcm', 1, {'question': 'Faire le tour du monde, c’est…',
                    'options': ['revenir au point de départ en faisant le tour de la Terre',
                                'aller tout droit sans revenir', 'rester au port']},
         {'index': 0}, 'On part, on fait le tour, on revient.'),
        ('qcm', 2, {'question': 'De quelle année à quelle année dure le premier tour du monde ?',
                    'options': ['De 1519 à 1522', 'De 1492 à 1498', 'De 1440 à 1450', 'De 1487 à 1492']},
         {'index': 0}, 'De 1519 à 1522.'),
        ('texte_a_trous', 3, {'text': 'Magellan et son équipage font le premier tour du monde de {{1}} à {{2}}.', 'blanks': 2},
         {'values': ['1519', '1522']}, 'De 1519 à 1522.'),
    ],
}

LECONS = [
    ('La Préhistoire', PREHISTOIRE),
    ('Les grandes inventions et les grandes découvertes', DECOUVERTES),
]


def lignes():
    for titre, notions in LECONS:
        for ordre in sorted(notions):
            for kind, level, payload, answer, explain in notions[ordre]:
                yield {
                    'lecon': titre, 'ordre': ordre, 'kind': kind, 'level': level,
                    'payload': payload, 'answer': answer, 'explain': explain,
                }


def verifier(tout):
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    for r in tout:
        textes = json.dumps([r['payload'], r['answer'], r['explain']], ensure_ascii=False)
        assert "'" not in textes, 'apostrophe droite interdite : ' + textes
        if r['kind'] == 'qcm':
            options = r['payload']['options']
            assert 2 <= len(options) <= 4, r
            assert len(set(options)) == len(options), 'option en double : ' + str(r)
            assert 0 <= r['answer']['index'] < len(options), r
        elif r['kind'] == 'texte_a_trous':
            trous = r['payload']['text'].count('{{')
            assert trous == len(r['answer']['values']), 'trous et réponses discordants : ' + str(r)
            assert trous == r['payload']['blanks'], r
        elif r['kind'] == 'chronologie':
            assert sorted(r['answer']['order']) == list(range(len(r['payload']['tokens']))), r
        else:
            raise AssertionError('type inconnu : ' + r['kind'])
    # Deux questions identiques ne doivent pas coexister.
    vus = set()
    for r in tout:
        cle = (r['lecon'], r['ordre'], json.dumps(r['payload'], ensure_ascii=False, sort_keys=True))
        assert cle not in vus, 'question en double : ' + str(cle)
        vus.add(cle)


def sql(tout):
    valeurs = []
    for r in tout:
        valeurs.append(
            "    ('%s', %d, '%s', %d,\n     '%s',\n     '%s', '%s')"
            % (r['lecon'], r['ordre'], r['kind'], r['level'],
               json.dumps(r['payload'], ensure_ascii=False),
               json.dumps(r['answer'], ensure_ascii=False),
               r['explain'])
        )
    return ENTETE + ',\n\n'.join(valeurs) + PIED


ENTETE = """-- Se Former Cameroun — les questions des trois étapes
--
-- L'enfant retombait toujours sur le facile, et c'était mérité : la plupart
-- des notions n'avaient qu'une seule question, à un seul niveau. Le moteur
-- n'avait rien de plus difficile à servir, donc il reposait la même chose.
--
-- Chaque notion des deux leçons a désormais ses trois niveaux, et deux
-- formulations par niveau là où c'est utile : un enfant qui se trompe doit
-- revoir la notion, pas retenir la position de la bonne case.
--
--   niveau 1  Découverte     reconnaître  — trois choix, réponse dans le résumé
--   niveau 2  Entraînement   comprendre   — quatre choix, distracteurs plausibles
--   niveau 3  Défi           restituer    — texte à trous, chronologie, raisonnement
--
-- Rien n'est ajouté au cahier : les dates, les noms et les faits sont ceux
-- des leçons déjà validées. Les notions sont désignées par leur rang dans la
-- leçon, qui ne bouge pas.
--
-- Réexécutable : une question déjà présente n'est pas réinsérée.

insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status)
select n.parent_id, n.id, v.kind, v.level, v.payload::jsonb, v.answer::jsonb, v.explain, 'approved'
  from (values
"""

PIED = """
  ) as v(lecon, ordre, kind, level, payload, answer, explain)
  join lessons l on l.title = v.lecon
  join notions n on n.lesson_id = l.id and n.sort_order = v.ordre and n.status = 'approved'
 where not exists (
   select 1 from items i
    where i.notion_id = n.id
      and i.payload = v.payload::jsonb
 );
"""

if __name__ == '__main__':
    tout = list(lignes())
    verifier(tout)

    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    chemin_sql = os.path.join(racine, 'supabase', 'migrations', '20261016090000_questions_paliers.sql')
    io.open(chemin_sql, 'w', encoding='utf-8', newline='\n').write(sql(tout))
    io.open(os.path.join(racine, 'work', 'questions-paliers.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(tout, ensure_ascii=False, indent=1)
    )

    par_niveau = {}
    for r in tout:
        par_niveau[r['level']] = par_niveau.get(r['level'], 0) + 1
    print('%d questions : %s' % (len(tout), ' '.join('N%d=%d' % (k, par_niveau[k]) for k in sorted(par_niveau))))
    print(chemin_sql)
