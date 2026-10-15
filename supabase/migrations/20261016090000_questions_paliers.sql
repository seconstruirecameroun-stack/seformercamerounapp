-- Se Former Cameroun — les questions des trois étapes
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
    ('La Préhistoire', 1, 'qcm', 1,
     '{"question": "Par quoi commence la Préhistoire ?", "options": ["L’apparition des premiers humains", "L’invention de l’écriture", "La construction des villes"]}',
     '{"index": 0}', 'Elle commence avec les premiers humains.'),

    ('La Préhistoire', 1, 'qcm', 1,
     '{"question": "La Préhistoire est le temps des premiers…", "options": ["humains", "rois", "machines"]}',
     '{"index": 0}', 'C’est le temps des premiers humains.'),

    ('La Préhistoire', 1, 'qcm', 2,
     '{"question": "La Préhistoire s’arrête à quelle invention ?", "options": ["L’écriture", "La roue", "Le feu", "Les métaux"]}',
     '{"index": 0}', 'Elle s’arrête à l’invention de l’écriture.'),

    ('La Préhistoire', 1, 'qcm', 2,
     '{"question": "Combien d’époques compte la Préhistoire ?", "options": ["Trois", "Deux", "Cinq", "Dix"]}',
     '{"index": 0}', 'Trois : Paléolithique, Néolithique, âge des métaux.'),

    ('La Préhistoire', 1, 'qcm', 3,
     '{"question": "Pourquoi dit-on « Préhistoire » ?", "options": ["Parce que c’est avant l’Histoire écrite", "Parce que les humains ne parlaient pas", "Parce qu’il n’y avait pas d’animaux", "Parce qu’il faisait très froid"]}',
     '{"index": 0}', '« Pré » veut dire avant : avant l’écriture.'),

    ('La Préhistoire', 1, 'texte_a_trous', 3,
     '{"text": "La Préhistoire va de l’apparition des premiers {{1}} à l’invention de l’{{2}}.", "blanks": 2}',
     '{"values": ["humains", "écriture"]}', 'Des premiers humains à l’écriture.'),

    ('La Préhistoire', 2, 'qcm', 1,
     '{"question": "L’écriture marque la fin de quelle période ?", "options": ["La Préhistoire", "Le Moyen Âge", "L’époque des machines"]}',
     '{"index": 0}', 'L’écriture termine la Préhistoire.'),

    ('La Préhistoire', 2, 'qcm', 2,
     '{"question": "Vers quelle date l’écriture est-elle inventée ?", "options": ["Vers 3 000 avant J.-C.", "Vers 300 avant J.-C.", "Vers 3 000 après J.-C.", "Vers 30 avant J.-C."]}',
     '{"index": 0}', 'Vers 3 000 avant J.-C.'),

    ('La Préhistoire', 2, 'texte_a_trous', 3,
     '{"text": "L’invention de l’{{1}} marque la fin de la {{2}}.", "blanks": 2}',
     '{"values": ["écriture", "Préhistoire"]}', 'L’écriture termine la Préhistoire.'),

    ('La Préhistoire', 3, 'qcm', 1,
     '{"question": "Le Paléolithique est l’âge de la pierre…", "options": ["taillée", "polie", "peinte"]}',
     '{"index": 0}', 'Paléolithique : pierre taillée.'),

    ('La Préhistoire', 3, 'qcm', 1,
     '{"question": "À quoi sert la pierre taillée ?", "options": ["À fabriquer des outils", "À faire du pain", "À écrire"]}',
     '{"index": 0}', 'On taille la pierre pour en faire des outils.'),

    ('La Préhistoire', 3, 'qcm', 2,
     '{"question": "Quel outil est typique du Paléolithique ?", "options": ["Le biface, une pierre taillée", "La charrue", "Le marteau en fer", "Le stylo"]}',
     '{"index": 0}', 'Le biface est une pierre taillée des deux côtés.'),

    ('La Préhistoire', 3, 'texte_a_trous', 3,
     '{"text": "Le {{1}} est l’âge de la pierre {{2}}.", "blanks": 2}',
     '{"values": ["Paléolithique", "taillée"]}', 'Paléolithique : pierre taillée.'),

    ('La Préhistoire', 3, 'qcm', 3,
     '{"question": "Pourquoi dit-on pierre « taillée » ?", "options": ["Parce qu’on la casse pour lui donner un bord coupant", "Parce qu’on la frotte pour la rendre lisse", "Parce qu’on la cuit au feu", "Parce qu’on la peint"]}',
     '{"index": 0}', 'Tailler, c’est casser la pierre pour la rendre coupante.'),

    ('La Préhistoire', 4, 'qcm', 1,
     '{"question": "Au Paléolithique, comment se nourrit-on ?", "options": ["En chassant et en cueillant", "En cultivant des champs", "En achetant au marché"]}',
     '{"index": 0}', 'Chasse, pêche et cueillette.'),

    ('La Préhistoire', 4, 'qcm', 1,
     '{"question": "Au Paléolithique, cultive-t-on la terre ?", "options": ["Non, on chasse et on cueille", "Oui, on cultive du blé"]}',
     '{"index": 0}', 'L’agriculture viendra plus tard, au Néolithique.'),

    ('La Préhistoire', 4, 'qcm', 2,
     '{"question": "Laquelle de ces activités n’existe PAS au Paléolithique ?", "options": ["L’agriculture", "La chasse", "La pêche", "La cueillette"]}',
     '{"index": 0}', 'L’agriculture commence au Néolithique.'),

    ('La Préhistoire', 4, 'qcm', 3,
     '{"question": "Pourquoi les humains du Paléolithique se déplacent-ils souvent ?", "options": ["Ils suivent les animaux et les fruits sauvages", "Ils cherchent du métal", "Ils vont d’une ville à l’autre", "Ils fuient la pluie"]}',
     '{"index": 0}', 'Ils suivent leur nourriture : ils sont nomades.'),

    ('La Préhistoire', 5, 'qcm', 1,
     '{"question": "Le Néolithique est l’âge de la pierre…", "options": ["polie", "taillée", "peinte"]}',
     '{"index": 0}', 'Néolithique : pierre polie.'),

    ('La Préhistoire', 5, 'qcm', 2,
     '{"question": "Qu’est-ce qui change au Néolithique ?", "options": ["Les humains cultivent et élèvent des animaux", "Les humains inventent l’écriture", "Les humains fabriquent du fer", "Les humains arrêtent de fabriquer des outils"]}',
     '{"index": 0}', 'Au Néolithique commence l’agriculture.'),

    ('La Préhistoire', 5, 'texte_a_trous', 3,
     '{"text": "Le {{1}} est l’âge de la pierre {{2}}.", "blanks": 2}',
     '{"values": ["Néolithique", "polie"]}', 'Néolithique : pierre polie.'),

    ('La Préhistoire', 5, 'qcm', 3,
     '{"question": "Pourquoi l’agriculture change-t-elle la vie des humains ?", "options": ["Ils se fixent et construisent des villages", "Ils deviennent nomades", "Ils arrêtent de fabriquer des outils", "Ils inventent l’écriture"]}',
     '{"index": 0}', 'On reste près de ses champs : les villages naissent.'),

    ('La Préhistoire', 6, 'qcm', 1,
     '{"question": "À l’âge des métaux, avec quoi fabrique-t-on les outils ?", "options": ["Avec du métal", "Avec du papier", "Avec du verre"]}',
     '{"index": 0}', 'Des outils en métal, pas en pierre.'),

    ('La Préhistoire', 6, 'qcm', 1,
     '{"question": "Quel est un métal de cette époque ?", "options": ["Le cuivre", "Le plastique", "Le carton"]}',
     '{"index": 0}', 'Cuivre, bronze et fer.'),

    ('La Préhistoire', 6, 'qcm', 2,
     '{"question": "Quels métaux les humains utilisent-ils à cette époque ?", "options": ["Le cuivre, le bronze et le fer", "L’or, l’argent et le plastique", "Le fer, le verre et le bois", "Le bronze, le papier et la pierre"]}',
     '{"index": 0}', 'Cuivre, bronze, puis fer.'),

    ('La Préhistoire', 6, 'chronologie', 3,
     '{"question": "Remets ces métaux dans l’ordre où on les a utilisés.", "tokens": ["Cuivre", "Bronze", "Fer"]}',
     '{"order": [0, 1, 2]}', 'Cuivre, puis bronze, puis fer.'),

    ('La Préhistoire', 6, 'texte_a_trous', 3,
     '{"text": "À l’âge des métaux, on fabrique des outils et des bijoux en {{1}}, en bronze et en {{2}}.", "blanks": 2}',
     '{"values": ["cuivre", "fer"]}', 'Cuivre, bronze et fer.'),

    ('La Préhistoire', 7, 'qcm', 1,
     '{"question": "Combien d’époques se suivent dans la Préhistoire ?", "options": ["Trois", "Deux", "Six"]}',
     '{"index": 0}', 'Paléolithique, Néolithique, âge des métaux.'),

    ('La Préhistoire', 7, 'qcm', 2,
     '{"question": "Quelle période vient juste après le Paléolithique ?", "options": ["Le Néolithique", "L’âge des métaux", "L’écriture", "La pierre taillée"]}',
     '{"index": 0}', 'Paléolithique, puis Néolithique.'),

    ('La Préhistoire', 7, 'qcm', 2,
     '{"question": "Quelle période vient en dernier ?", "options": ["L’âge des métaux", "Le Néolithique", "Le Paléolithique", "La pierre polie"]}',
     '{"index": 0}', 'L’âge des métaux termine la Préhistoire.'),

    ('La Préhistoire', 7, 'texte_a_trous', 3,
     '{"text": "Les trois époques sont le {{1}}, le {{2}} et l’âge des {{3}}.", "blanks": 3}',
     '{"values": ["Paléolithique", "Néolithique", "métaux"]}', 'Dans cet ordre.'),

    ('Les grandes inventions et les grandes découvertes', 1, 'qcm', 1,
     '{"question": "Inventer, c’est…", "options": ["créer quelque chose de nouveau", "copier quelque chose", "acheter quelque chose"]}',
     '{"index": 0}', 'Inventer, c’est créer ce qui n’existait pas.'),

    ('Les grandes inventions et les grandes découvertes', 1, 'qcm', 2,
     '{"question": "Laquelle de ces phrases décrit une invention ?", "options": ["Fabriquer le premier bateau à voile", "Trouver une pièce par terre", "Lire un livre", "Marcher jusqu’à la rivière"]}',
     '{"index": 0}', 'On crée un objet qui n’existait pas.'),

    ('Les grandes inventions et les grandes découvertes', 1, 'qcm', 2,
     '{"question": "Quelle est la différence entre inventer et découvrir ?", "options": ["Inventer, c’est créer ; découvrir, c’est trouver ce qui existait déjà", "Inventer, c’est trouver ; découvrir, c’est créer", "Il n’y a aucune différence", "Inventer, c’est copier"]}',
     '{"index": 0}', 'On invente un objet, on découvre un lieu.'),

    ('Les grandes inventions et les grandes découvertes', 1, 'texte_a_trous', 3,
     '{"text": "Une {{1}} est la création d’un objet qui n’existait pas avant.", "blanks": 1}',
     '{"values": ["invention"]}', 'Une invention.'),

    ('Les grandes inventions et les grandes découvertes', 1, 'qcm', 3,
     '{"question": "Christophe Colomb a-t-il inventé l’Amérique ?", "options": ["Non, il l’a découverte : elle existait déjà", "Oui, il l’a inventée", "Oui, avec Gutenberg", "Non, il a inventé la caravelle"]}',
     '{"index": 0}', 'On découvre une terre, on ne l’invente pas.'),

    ('Les grandes inventions et les grandes découvertes', 2, 'qcm', 1,
     '{"question": "Qui invente la poudre à canon ?", "options": ["Les Chinois", "Les Français", "Les Portugais"]}',
     '{"index": 0}', 'Les Chinois, au 1ᵉʳ siècle.'),

    ('Les grandes inventions et les grandes découvertes', 2, 'qcm', 2,
     '{"question": "Qu’inventent les Chinois au 1ᵉʳ siècle ?", "options": ["Le papier et la poudre à canon", "La caravelle et l’imprimerie", "La boussole et le gouvernail", "Le fer et le bronze"]}',
     '{"index": 0}', 'Le papier et la poudre à canon.'),

    ('Les grandes inventions et les grandes découvertes', 2, 'qcm', 2,
     '{"question": "À quel siècle le papier est-il inventé ?", "options": ["Au 1ᵉʳ siècle", "Au VIIᵉ siècle", "Au XIIᵉ siècle", "En 1440"]}',
     '{"index": 0}', 'Au 1ᵉʳ siècle.'),

    ('Les grandes inventions et les grandes découvertes', 2, 'texte_a_trous', 3,
     '{"text": "Les Chinois inventent le {{1}} et la {{2}} à canon au 1ᵉʳ siècle.", "blanks": 2}',
     '{"values": ["papier", "poudre"]}', 'Le papier et la poudre.'),

    ('Les grandes inventions et les grandes découvertes', 2, 'chronologie', 3,
     '{"question": "Remets ces inventions chinoises dans l’ordre.", "tokens": ["Le papier, 1ᵉʳ siècle", "La boussole, VIIᵉ siècle", "Le gouvernail, XIIᵉ siècle"]}',
     '{"order": [0, 1, 2]}', 'Papier, boussole, gouvernail.'),

    ('Les grandes inventions et les grandes découvertes', 3, 'qcm', 1,
     '{"question": "Qui invente la boussole ?", "options": ["Les Chinois", "Les Portugais", "Les Allemands"]}',
     '{"index": 0}', 'Les Chinois, au VIIᵉ siècle.'),

    ('Les grandes inventions et les grandes découvertes', 3, 'qcm', 1,
     '{"question": "La boussole indique…", "options": ["le nord", "l’heure", "la pluie"]}',
     '{"index": 0}', 'Elle montre toujours le nord.'),

    ('Les grandes inventions et les grandes découvertes', 3, 'qcm', 2,
     '{"question": "À quel siècle la boussole est-elle inventée ?", "options": ["Au VIIᵉ siècle", "Au 1ᵉʳ siècle", "Au XIIᵉ siècle", "En 1492"]}',
     '{"index": 0}', 'Au VIIᵉ siècle.'),

    ('Les grandes inventions et les grandes découvertes', 3, 'texte_a_trous', 3,
     '{"text": "Les Chinois inventent la {{1}} au VIIᵉ siècle.", "blanks": 1}',
     '{"values": ["boussole"]}', 'La boussole.'),

    ('Les grandes inventions et les grandes découvertes', 3, 'qcm', 3,
     '{"question": "Pourquoi la boussole est-elle utile aux marins ?", "options": ["Elle donne la direction même quand on ne voit plus la terre", "Elle fait avancer le bateau", "Elle imprime les cartes", "Elle sert à pêcher"]}',
     '{"index": 0}', 'En pleine mer, elle montre où est le nord.'),

    ('Les grandes inventions et les grandes découvertes', 4, 'qcm', 1,
     '{"question": "Le gouvernail sert à…", "options": ["diriger le bateau", "écrire", "cuisiner"]}',
     '{"index": 0}', 'Il dirige le bateau.'),

    ('Les grandes inventions et les grandes découvertes', 4, 'qcm', 1,
     '{"question": "Qui invente le gouvernail ?", "options": ["Les Chinois", "Les Allemands", "Les Portugais"]}',
     '{"index": 0}', 'Les Chinois, au XIIᵉ siècle.'),

    ('Les grandes inventions et les grandes découvertes', 4, 'qcm', 2,
     '{"question": "À quel siècle le gouvernail est-il inventé ?", "options": ["Au XIIᵉ siècle", "Au VIIᵉ siècle", "Au 1ᵉʳ siècle", "En 1450"]}',
     '{"index": 0}', 'Au XIIᵉ siècle.'),

    ('Les grandes inventions et les grandes découvertes', 4, 'texte_a_trous', 3,
     '{"text": "Les Chinois inventent le {{1}} au XIIᵉ siècle.", "blanks": 1}',
     '{"values": ["gouvernail"]}', 'Le gouvernail.'),

    ('Les grandes inventions et les grandes découvertes', 4, 'qcm', 3,
     '{"question": "Boussole et gouvernail : que permettent-ils ensemble ?", "options": ["Trouver la direction et la suivre", "Imprimer des livres", "Fabriquer du papier", "Cultiver la terre"]}',
     '{"index": 0}', 'L’une montre la route, l’autre la suit.'),

    ('Les grandes inventions et les grandes découvertes', 5, 'qcm', 1,
     '{"question": "La caravelle est…", "options": ["un bateau", "un livre", "une arme"]}',
     '{"index": 0}', 'Un bateau rapide et solide.'),

    ('Les grandes inventions et les grandes découvertes', 5, 'qcm', 1,
     '{"question": "Qui invente la caravelle ?", "options": ["Les Portugais", "Les Chinois", "Les Allemands"]}',
     '{"index": 0}', 'Les Portugais, en 1440.'),

    ('Les grandes inventions et les grandes découvertes', 5, 'qcm', 2,
     '{"question": "En quelle année la caravelle est-elle inventée ?", "options": ["1440", "1450", "1487", "1492"]}',
     '{"index": 0}', 'En 1440.'),

    ('Les grandes inventions et les grandes découvertes', 5, 'texte_a_trous', 3,
     '{"text": "Les {{1}} inventent la caravelle en {{2}}.", "blanks": 2}',
     '{"values": ["Portugais", "1440"]}', 'Les Portugais, en 1440.'),

    ('Les grandes inventions et les grandes découvertes', 5, 'qcm', 3,
     '{"question": "Pourquoi la caravelle change-t-elle les voyages ?", "options": ["Elle est solide et rapide : elle peut aller très loin", "Elle est plus petite qu’une barque", "Elle avance sans vent", "Elle sert à imprimer des cartes"]}',
     '{"index": 0}', 'Elle tient la haute mer, longtemps.'),

    ('Les grandes inventions et les grandes découvertes', 6, 'qcm', 1,
     '{"question": "Qui invente l’imprimerie ?", "options": ["Gutenberg", "Colomb", "Magellan"]}',
     '{"index": 0}', 'L’Allemand Gutenberg, en 1450.'),

    ('Les grandes inventions et les grandes découvertes', 6, 'qcm', 1,
     '{"question": "L’imprimerie sert à…", "options": ["copier des livres rapidement", "naviguer", "cultiver la terre"]}',
     '{"index": 0}', 'Elle copie les livres vite.'),

    ('Les grandes inventions et les grandes découvertes', 6, 'qcm', 2,
     '{"question": "En quelle année l’imprimerie est-elle inventée ?", "options": ["1450", "1440", "1487", "1498"]}',
     '{"index": 0}', 'En 1450.'),

    ('Les grandes inventions et les grandes découvertes', 6, 'qcm', 3,
     '{"question": "Pourquoi l’imprimerie est-elle importante ?", "options": ["Les livres et les cartes se copient vite et circulent partout", "Elle permet de traverser l’océan", "Elle remplace la boussole", "Elle fabrique le papier"]}',
     '{"index": 0}', 'Le savoir voyage avec les livres.'),

    ('Les grandes inventions et les grandes découvertes', 7, 'qcm', 1,
     '{"question": "Grâce à ces inventions, les marins peuvent…", "options": ["aller plus loin", "rester au port", "voler"]}',
     '{"index": 0}', 'Ils partent plus loin, plus sûrement.'),

    ('Les grandes inventions et les grandes découvertes', 7, 'qcm', 1,
     '{"question": "Ces inventions ont surtout aidé…", "options": ["la navigation", "la cuisine", "l’école"]}',
     '{"index": 0}', 'Elles ont aidé la navigation.'),

    ('Les grandes inventions et les grandes découvertes', 7, 'qcm', 2,
     '{"question": "Quelles inventions aident les marins à partir loin ?", "options": ["La boussole, le gouvernail et la caravelle", "Le papier et la poudre", "L’imprimerie et le papier", "La charrue et la roue"]}',
     '{"index": 0}', 'Direction, pilotage et bon bateau.'),

    ('Les grandes inventions et les grandes découvertes', 7, 'qcm', 3,
     '{"question": "Pourquoi les grandes découvertes viennent-elles après les grandes inventions ?", "options": ["Il fallait d’abord des bateaux et des instruments pour partir loin", "Les marins n’avaient pas envie avant", "Parce que l’écriture venait d’être inventée", "Parce que la Terre a changé de forme"]}',
     '{"index": 0}', 'Sans ces outils, le grand large est impossible.'),

    ('Les grandes inventions et les grandes découvertes', 7, 'texte_a_trous', 3,
     '{"text": "Ces inventions ont favorisé la {{1}} et les grands {{2}}.", "blanks": 2}',
     '{"values": ["navigation", "voyages"]}', 'La navigation et les grands voyages.'),

    ('Les grandes inventions et les grandes découvertes', 8, 'qcm', 1,
     '{"question": "Qui atteint le cap de Bonne-Espérance ?", "options": ["Bartholomeu Dias", "Christophe Colomb", "Gutenberg"]}',
     '{"index": 0}', 'Bartholomeu Dias, en 1487.'),

    ('Les grandes inventions et les grandes découvertes', 8, 'qcm', 1,
     '{"question": "Où se trouve le cap de Bonne-Espérance ?", "options": ["Au sud de l’Afrique", "En Amérique", "En Chine"]}',
     '{"index": 0}', 'Tout au sud de l’Afrique.'),

    ('Les grandes inventions et les grandes découvertes', 8, 'qcm', 2,
     '{"question": "En quelle année Dias atteint-il le cap de Bonne-Espérance ?", "options": ["1487", "1492", "1498", "1519"]}',
     '{"index": 0}', 'En 1487.'),

    ('Les grandes inventions et les grandes découvertes', 8, 'texte_a_trous', 3,
     '{"text": "Bartholomeu {{1}} atteint le cap de Bonne-Espérance en {{2}}.", "blanks": 2}',
     '{"values": ["Dias", "1487"]}', 'Dias, en 1487.'),

    ('Les grandes inventions et les grandes découvertes', 8, 'qcm', 3,
     '{"question": "Pourquoi le cap de Bonne-Espérance compte-t-il autant ?", "options": ["Il ouvre la route vers l’océan Indien, au sud de l’Afrique", "C’est le point le plus au nord du monde", "C’est là que Colomb est arrivé", "C’est une ville d’Allemagne"]}',
     '{"index": 0}', 'En le passant, on peut filer vers les Indes.'),

    ('Les grandes inventions et les grandes découvertes', 9, 'qcm', 1,
     '{"question": "Christophe Colomb découvre…", "options": ["l’Amérique", "la Chine", "l’Australie"]}',
     '{"index": 0}', 'L’Amérique, en 1492.'),

    ('Les grandes inventions et les grandes découvertes', 9, 'qcm', 1,
     '{"question": "En quelle année Colomb arrive-t-il en Amérique ?", "options": ["1492", "1892", "1192"]}',
     '{"index": 0}', 'En 1492.'),

    ('Les grandes inventions et les grandes découvertes', 9, 'qcm', 2,
     '{"question": "Que cherchait Christophe Colomb en partant vers l’ouest ?", "options": ["La route des Indes", "L’Amérique", "Le cap de Bonne-Espérance", "L’Allemagne"]}',
     '{"index": 0}', 'Il cherchait les Indes, il trouve l’Amérique.'),

    ('Les grandes inventions et les grandes découvertes', 9, 'qcm', 3,
     '{"question": "Pourquoi dit-on que Colomb a « découvert » l’Amérique ?", "options": ["Les Européens ne la connaissaient pas, mais des peuples y vivaient déjà", "Parce qu’il l’a inventée", "Parce que personne n’y habitait", "Parce qu’il y est né"]}',
     '{"index": 0}', 'Découverte pour les Européens seulement.'),

    ('Les grandes inventions et les grandes découvertes', 10, 'qcm', 1,
     '{"question": "Qui trouve la route des Indes ?", "options": ["Vasco de Gama", "Bartholomeu Dias", "Gutenberg"]}',
     '{"index": 0}', 'Vasco de Gama, en 1498.'),

    ('Les grandes inventions et les grandes découvertes', 10, 'qcm', 1,
     '{"question": "Aux Indes, les marins vont chercher…", "options": ["des épices", "de la neige", "du charbon"]}',
     '{"index": 0}', 'Les épices valaient très cher.'),

    ('Les grandes inventions et les grandes découvertes', 10, 'qcm', 2,
     '{"question": "En quelle année Vasco de Gama arrive-t-il aux Indes ?", "options": ["1498", "1487", "1492", "1522"]}',
     '{"index": 0}', 'En 1498.'),

    ('Les grandes inventions et les grandes découvertes', 10, 'texte_a_trous', 3,
     '{"text": "Vasco de {{1}} trouve la route des Indes en {{2}}.", "blanks": 2}',
     '{"values": ["Gama", "1498"]}', 'Vasco de Gama, en 1498.'),

    ('Les grandes inventions et les grandes découvertes', 10, 'qcm', 3,
     '{"question": "Pourquoi cherchait-on une route vers les Indes ?", "options": ["Pour acheter des épices et des tissus", "Pour visiter l’Amérique", "Pour fuir l’Europe", "Pour imprimer des livres"]}',
     '{"index": 0}', 'Pour le commerce des épices.'),

    ('Les grandes inventions et les grandes découvertes', 11, 'qcm', 1,
     '{"question": "Magellan et son équipage font le premier…", "options": ["tour du monde", "livre imprimé", "bateau en métal"]}',
     '{"index": 0}', 'Le premier tour du monde.'),

    ('Les grandes inventions et les grandes découvertes', 11, 'qcm', 1,
     '{"question": "Faire le tour du monde, c’est…", "options": ["revenir au point de départ en faisant le tour de la Terre", "aller tout droit sans revenir", "rester au port"]}',
     '{"index": 0}', 'On part, on fait le tour, on revient.'),

    ('Les grandes inventions et les grandes découvertes', 11, 'qcm', 2,
     '{"question": "De quelle année à quelle année dure le premier tour du monde ?", "options": ["De 1519 à 1522", "De 1492 à 1498", "De 1440 à 1450", "De 1487 à 1492"]}',
     '{"index": 0}', 'De 1519 à 1522.'),

    ('Les grandes inventions et les grandes découvertes', 11, 'texte_a_trous', 3,
     '{"text": "Magellan et son équipage font le premier tour du monde de {{1}} à {{2}}.", "blanks": 2}',
     '{"values": ["1519", "1522"]}', 'De 1519 à 1522.')
  ) as v(lecon, ordre, kind, level, payload, answer, explain)
  join lessons l on l.title = v.lecon
  join notions n on n.lesson_id = l.id and n.sort_order = v.ordre and n.status = 'approved'
 where not exists (
   select 1 from items i
    where i.notion_id = n.id
      and i.payload = v.payload::jsonb
 );
