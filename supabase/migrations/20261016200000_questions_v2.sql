-- Se Former Cameroun — quatre façons d'interroger de plus, et une marche
--
-- Avant : 183 questions dont 139 QCM. L'enfant répondait presque toujours de
-- la même façon, et on mesurait sa capacité à reconnaître la bonne case plus
-- que ce qu'il savait.
--
-- Ce qui entre ici :
--   relier        les leçons sont faites de listes — quatre sols, trois
--                 époques, des inventions et leurs inventeurs. Un QCM les
--                 découpe et perd justement le lien.
--   vrai / faux   rapide, en série ; seul il laisse une chance sur deux.
--   image         une illustration existe déjà par notion : « clique sur le
--                 sol ferralitique » vaut mieux qu'un mot à lire pour un CE1.
--   dictée        le navigateur parle sans réseau et sans coût, et l'école a
--                 ses créneaux de dictée dans les deux emplois du temps.
--   mots en ordre reconstruire la phrase du résumé (moteur de la chronologie,
--                 autre consigne).
--
-- L'étape 4 « Défi » se joue au chronomètre : vingt secondes par question. On
-- n'y pose donc que du court — QCM ou vrai/faux — et on y demande du
-- transfert : appliquer ce qu'on sait à un cas qu'on n'a pas vu.
--
-- Chacune des 37 notions reçoit au moins une question de Défi : sans cela,
-- l'étape 4 serait infranchissable pour elle.
--
-- Le type « dictee » a été ajouté à l'énumération dans sa propre migration :
-- PostgreSQL exige qu'une valeur d'enum soit validée avant d'être utilisée.
--
-- Réexécutable : une question déjà présente n'est pas réinsérée.

insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status)
select n.parent_id, n.id, v.kind::item_kind, v.level, v.payload::jsonb, v.answer::jsonb, v.explain, 'approved'
  from (values
    ('La Préhistoire', 7, 'association', 2,
     '{"question": "Relie chaque époque à ce qu’on y fabrique.", "gauche": ["Paléolithique", "Néolithique", "Âge des métaux"], "droite": ["La pierre taillée", "La pierre polie", "Le cuivre et le fer"]}',
     '{"order": [0, 1, 2]}', 'Taillée, polie, puis les métaux.'),

    ('La Préhistoire', 3, 'qcm', 2,
     '{"question": "Clique sur l’outil du Paléolithique.", "images": ["biface", "hache-ble", "metaux", "tablette-ecriture"]}',
     '{"index": 0}', 'Le biface est une pierre taillée.'),

    ('La Préhistoire', 6, 'qcm', 2,
     '{"question": "Clique sur ce qu’on fabrique à l’âge des métaux.", "images": ["metaux", "biface", "chasse-peche-cueillette", "tablette-ecriture"]}',
     '{"index": 0}', 'Des outils et des bijoux en métal.'),

    ('La Préhistoire', 3, 'dictee', 3,
     '{"phrase": "Le Paléolithique est l’âge de la pierre taillée.", "langue": "fr"}',
     '{"phrase": "Le Paléolithique est l’âge de la pierre taillée."}', 'Pierre taillée.'),

    ('La Préhistoire', 5, 'dictee', 3,
     '{"phrase": "Au Néolithique, les humains commencent l’agriculture.", "langue": "fr"}',
     '{"phrase": "Au Néolithique, les humains commencent l’agriculture."}', 'Le Néolithique et l’agriculture.'),

    ('La Préhistoire', 2, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["L’écriture", "marque", "la fin", "de la Préhistoire"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2, 3]}', 'L’écriture clôt la Préhistoire.'),

    ('La Préhistoire', 1, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["La Préhistoire", "commence", "avec les premiers", "humains"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2, 3]}', 'Elle commence avec eux.'),

    ('La Préhistoire', 1, 'vrai_faux', 4,
     '{"statement": "La Préhistoire se termine quand on invente l’écriture."}',
     '{"value": true}', 'Oui, vers 3 000 avant J.-C.'),

    ('La Préhistoire', 2, 'vrai_faux', 4,
     '{"statement": "L’écriture est inventée après l’âge des métaux."}',
     '{"value": false}', 'Non : elle arrive à la fin de la Préhistoire, après l’âge des métaux dans le temps mais c’est elle qui la termine.'),

    ('La Préhistoire', 3, 'qcm', 4,
     '{"question": "On trouve une pierre cassée en pointe. Quelle époque ?", "options": ["Le Paléolithique", "Le Néolithique", "L’âge des métaux"]}',
     '{"index": 0}', 'Pierre taillée : Paléolithique.'),

    ('La Préhistoire', 4, 'qcm', 4,
     '{"question": "Un campement déplacé chaque mois. Que mangent-ils ?", "options": ["Ce qu’ils chassent et cueillent", "Le blé de leurs champs", "Des animaux d’élevage"]}',
     '{"index": 0}', 'Ils suivent leur nourriture.'),

    ('La Préhistoire', 5, 'qcm', 4,
     '{"question": "On trouve des grains de blé et une meule. Quelle époque ?", "options": ["Le Néolithique", "Le Paléolithique", "La Préhistoire n’en a pas"]}',
     '{"index": 0}', 'L’agriculture, donc le Néolithique.'),

    ('La Préhistoire', 6, 'qcm', 4,
     '{"question": "Un bracelet en bronze sort de terre. Quelle époque ?", "options": ["L’âge des métaux", "Le Paléolithique", "Le Néolithique"]}',
     '{"index": 0}', 'Le bronze est un métal.'),

    ('La Préhistoire', 7, 'qcm', 4,
     '{"question": "Quelle époque vient entre les deux autres ?", "options": ["Le Néolithique", "Le Paléolithique", "L’âge des métaux"]}',
     '{"index": 0}', 'Paléolithique, Néolithique, métaux.'),

    ('Les grandes inventions et les grandes découvertes', 6, 'association', 2,
     '{"question": "Relie chaque invention à son peuple.", "gauche": ["Le papier", "La caravelle", "L’imprimerie"], "droite": ["Les Chinois", "Les Portugais", "L’Allemand Gutenberg"]}',
     '{"order": [0, 1, 2]}', 'Chine, Portugal, Allemagne.'),

    ('Les grandes inventions et les grandes découvertes', 9, 'association', 2,
     '{"question": "Relie chaque navigateur à sa découverte.", "gauche": ["Bartholomeu Dias", "Christophe Colomb", "Vasco de Gama"], "droite": ["Le cap de Bonne-Espérance", "L’Amérique", "La route des Indes"]}',
     '{"order": [0, 1, 2]}', '1487, 1492, 1498.'),

    ('Les grandes inventions et les grandes découvertes', 11, 'association', 3,
     '{"question": "Relie chaque voyage à son année.", "gauche": ["Dias", "Colomb", "Vasco de Gama", "Magellan"], "droite": ["1487", "1492", "1498", "1519"]}',
     '{"order": [0, 1, 2, 3]}', 'Dans l’ordre : 1487, 1492, 1498, 1519.'),

    ('Les grandes inventions et les grandes découvertes', 3, 'qcm', 2,
     '{"question": "Clique sur la boussole.", "images": ["gd-boussole", "gd-gouvernail", "gd-caravelle", "gd-imprimerie"]}',
     '{"index": 0}', 'Elle montre le nord.'),

    ('Les grandes inventions et les grandes découvertes', 5, 'qcm', 2,
     '{"question": "Clique sur la caravelle.", "images": ["gd-caravelle", "gd-boussole", "gd-papier-poudre", "gd-imprimerie"]}',
     '{"index": 0}', 'Le bateau portugais de 1440.'),

    ('Les grandes inventions et les grandes découvertes', 1, 'dictee', 3,
     '{"phrase": "Une invention crée un objet qui n’existait pas.", "langue": "fr"}',
     '{"phrase": "Une invention crée un objet qui n’existait pas."}', 'Créer ce qui n’existait pas.'),

    ('Les grandes inventions et les grandes découvertes', 6, 'dictee', 3,
     '{"phrase": "Gutenberg invente l’imprimerie en 1450.", "langue": "fr"}',
     '{"phrase": "Gutenberg invente l’imprimerie en 1450."}', 'Gutenberg, 1450.'),

    ('Les grandes inventions et les grandes découvertes', 7, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Ces inventions", "ont favorisé", "la navigation"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2]}', 'Elles ont aidé les marins.'),

    ('Les grandes inventions et les grandes découvertes', 1, 'vrai_faux', 4,
     '{"statement": "Découvrir l’Amérique, c’est l’inventer."}',
     '{"value": false}', 'On découvre une terre, on ne l’invente pas.'),

    ('Les grandes inventions et les grandes découvertes', 2, 'vrai_faux', 4,
     '{"statement": "Le papier vient de Chine."}',
     '{"value": true}', 'Oui, au 1ᵉʳ siècle.'),

    ('Les grandes inventions et les grandes découvertes', 3, 'vrai_faux', 4,
     '{"statement": "La boussole sert à faire avancer le bateau."}',
     '{"value": false}', 'Elle donne la direction, pas la force.'),

    ('Les grandes inventions et les grandes découvertes', 4, 'vrai_faux', 4,
     '{"statement": "Le gouvernail sert à diriger le bateau."}',
     '{"value": true}', 'Oui, il le dirige.'),

    ('Les grandes inventions et les grandes découvertes', 5, 'vrai_faux', 4,
     '{"statement": "La caravelle est inventée après l’imprimerie."}',
     '{"value": false}', 'Caravelle 1440, imprimerie 1450.'),

    ('Les grandes inventions et les grandes découvertes', 7, 'vrai_faux', 4,
     '{"statement": "Sans la boussole, les marins seraient allés aussi loin."}',
     '{"value": false}', 'Sans direction en pleine mer, on ne s’éloigne pas des côtes.'),

    ('Les grandes inventions et les grandes découvertes', 6, 'qcm', 4,
     '{"question": "Grâce à quoi un même livre existe en mille exemplaires ?", "options": ["L’imprimerie", "La boussole", "La caravelle"]}',
     '{"index": 0}', 'L’imprimerie copie vite.'),

    ('Les grandes inventions et les grandes découvertes', 8, 'qcm', 4,
     '{"question": "Un marin contourne le sud de l’Afrique. Qui est-ce ?", "options": ["Bartholomeu Dias", "Christophe Colomb", "Magellan"]}',
     '{"index": 0}', 'Dias, au cap de Bonne-Espérance.'),

    ('Les grandes inventions et les grandes découvertes', 9, 'qcm', 4,
     '{"question": "Il part vers l’ouest chercher les Indes et trouve une autre terre.", "options": ["Christophe Colomb", "Vasco de Gama", "Dias"]}',
     '{"index": 0}', 'Colomb, en 1492.'),

    ('Les grandes inventions et les grandes découvertes', 10, 'qcm', 4,
     '{"question": "Il rapporte des épices par la mer, en passant au sud de l’Afrique.", "options": ["Vasco de Gama", "Colomb", "Gutenberg"]}',
     '{"index": 0}', 'Vasco de Gama, en 1498.'),

    ('Les grandes inventions et les grandes découvertes', 11, 'qcm', 4,
     '{"question": "Un bateau part à l’ouest et revient par l’est. Qu’a-t-il fait ?", "options": ["Le tour du monde", "Un aller-retour", "Un naufrage"]}',
     '{"index": 0}', 'C’est Magellan.'),

    ('L’obéissance', 1, 'vrai_faux', 2,
     '{"statement": "Obéir, c’est discuter avant de faire."}',
     '{"value": false}', 'Obéir, c’est faire sans discuter.'),

    ('L’obéissance', 2, 'vrai_faux', 2,
     '{"statement": "Un enfant obéissant est aimé de tout le monde."}',
     '{"value": true}', 'Oui, c’est ce que dit la leçon.'),

    ('L’obéissance', 1, 'association', 2,
     '{"question": "Relie chaque mot à ce qu’il veut dire.", "gauche": ["Obéir", "Un aîné", "Une consigne"], "droite": ["Faire ce qu’on demande", "Un plus grand que moi", "Ce qu’on me demande de faire"]}',
     '{"order": [0, 1, 2]}', 'Trois mots de la leçon.'),

    ('L’obéissance', 2, 'dictee', 3,
     '{"phrase": "Un enfant obéissant est aimé de tout le monde.", "langue": "fr"}',
     '{"phrase": "Un enfant obéissant est aimé de tout le monde."}', 'La phrase du cahier.'),

    ('L’obéissance', 3, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Pour réussir", "dans la vie", "il faut obéir"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2]}', 'La leçon finit là-dessus.'),

    ('L’obéissance', 1, 'qcm', 4,
     '{"question": "Ton maître te demande de ranger. Tu fais quoi ?", "options": ["Je range tout de suite", "Je demande pourquoi", "Je range demain"]}',
     '{"index": 0}', 'Sans discuter.'),

    ('L’obéissance', 2, 'qcm', 4,
     '{"question": "Pourquoi aime-t-on un enfant obéissant ?", "options": ["Il fait ce qu’on lui demande", "Il crie fort", "Il court vite"]}',
     '{"index": 0}', 'Parce qu’il écoute.'),

    ('L’obéissance', 3, 'vrai_faux', 4,
     '{"statement": "Obéir aujourd’hui aide à réussir plus tard."}',
     '{"value": true}', 'C’est ce que dit la leçon.'),

    ('Le droit à l’identité', 1, 'vrai_faux', 2,
     '{"statement": "Seuls les grands ont droit à une identité."}',
     '{"value": false}', 'Chaque enfant y a droit.'),

    ('Le droit à l’identité', 2, 'association', 2,
     '{"question": "Relie chaque chose à ce qu’elle est.", "gauche": ["Mon nom", "Ma nationalité"], "droite": ["Comment on m’appelle", "Le pays qui est le mien"]}',
     '{"order": [0, 1]}', 'Les deux font l’identité.'),

    ('Le droit à l’identité', 1, 'dictee', 3,
     '{"phrase": "Chaque enfant a droit à une identité.", "langue": "fr"}',
     '{"phrase": "Chaque enfant a droit à une identité."}', 'La phrase du cahier.'),

    ('Le droit à l’identité', 2, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["L’identité", "donne un nom", "et une nationalité"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2]}', 'Un nom et une nationalité.'),

    ('Le droit à l’identité', 1, 'qcm', 4,
     '{"question": "Un bébé qui vient de naître a-t-il droit à une identité ?", "options": ["Oui, dès sa naissance", "Non, à six ans", "Seulement à l’école"]}',
     '{"index": 0}', 'Chaque enfant, dès le début.'),

    ('Le droit à l’identité', 2, 'qcm', 4,
     '{"question": "Être camerounais, c’est quelle partie de mon identité ?", "options": ["Ma nationalité", "Mon nom", "Mon âge"]}',
     '{"index": 0}', 'C’est la nationalité.'),

    ('L’intégration nationale', 2, 'vrai_faux', 2,
     '{"statement": "Au Cameroun, il y a moins de dix ethnies."}',
     '{"value": false}', 'Il y en a plus de 250.'),

    ('L’intégration nationale', 3, 'association', 2,
     '{"question": "Relie chaque moyen à ce qu’il rapproche.", "gauche": ["Le mariage interethnique", "La cohabitation", "L’affectation"], "droite": ["Deux familles", "Des voisins", "Un travailleur et une région"]}',
     '{"order": [0, 1, 2]}', 'Trois façons de se rapprocher.'),

    ('L’intégration nationale', 2, 'qcm', 2,
     '{"question": "Clique sur le village où vivent plusieurs peuples.", "images": ["in-ethnies", "in-melange", "in-moyens"]}',
     '{"index": 0}', 'Beaucoup de maisons différentes, côte à côte.'),

    ('L’intégration nationale', 1, 'dictee', 3,
     '{"phrase": "L’intégration nationale mélange les cultures.", "langue": "fr"}',
     '{"phrase": "L’intégration nationale mélange les cultures."}', 'Un mélange de cultures.'),

    ('L’intégration nationale', 2, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Au Cameroun", "les ethnies", "vivent en paix"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2]}', 'Plus de 250, en paix.'),

    ('L’intégration nationale', 1, 'qcm', 4,
     '{"question": "Deux familles de régions différentes fêtent ensemble. C’est quoi ?", "options": ["De l’intégration nationale", "Une dispute", "Un voyage"]}',
     '{"index": 0}', 'Les cultures se mélangent.'),

    ('L’intégration nationale', 2, 'qcm', 4,
     '{"question": "Combien d’ethnies au Cameroun ?", "options": ["Plus de 250", "Environ 20", "Une seule"]}',
     '{"index": 0}', 'Plus de 250.'),

    ('L’intégration nationale', 3, 'vrai_faux', 4,
     '{"statement": "Refuser les gens d’une autre ethnie aide l’intégration."}',
     '{"value": false}', 'Cela sépare au lieu de rassembler.'),

    ('Les techniques de filtrage de l’eau', 1, 'association', 2,
     '{"question": "Relie chaque matière à son rôle.", "gauche": ["Le gravier", "Le charbon", "Le coton"], "droite": ["Il arrête les gros morceaux", "Il nettoie l’eau", "Il retient les petites saletés"]}',
     '{"order": [0, 1, 2]}', 'Chacun fait son travail.'),

    ('Les techniques de filtrage de l’eau', 2, 'qcm', 2,
     '{"question": "Clique sur le filtre et ses couches.", "images": ["fi-couches", "fi-materiel", "fi-eau-potable"]}',
     '{"index": 0}', 'Gravier, charbon, sable, coton.'),

    ('Les techniques de filtrage de l’eau', 3, 'dictee', 3,
     '{"phrase": "L’eau sale entre et l’eau propre sort.", "langue": "fr"}',
     '{"phrase": "L’eau sale entre et l’eau propre sort."}', 'Entrée sale, sortie propre.'),

    ('Les techniques de filtrage de l’eau', 2, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Le gravier", "puis le charbon", "puis le sable", "puis le coton"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2, 3]}', 'L’ordre des couches, de haut en bas.'),

    ('Les techniques de filtrage de l’eau', 1, 'qcm', 4,
     '{"question": "Il te manque le charbon. Ton filtre marchera-t-il aussi bien ?", "options": ["Non, il nettoie moins bien", "Oui, c’est pareil", "Oui, il ira plus vite"]}',
     '{"index": 0}', 'Chaque couche sert à quelque chose.'),

    ('Les techniques de filtrage de l’eau', 2, 'qcm', 4,
     '{"question": "Tu mets le coton tout en haut. Que se passe-t-il ?", "options": ["L’eau n’est pas bien filtrée", "Rien ne change", "L’eau devient sucrée"]}',
     '{"index": 0}', 'L’ordre compte : le coton est en bas.'),

    ('Les techniques de filtrage de l’eau', 3, 'vrai_faux', 4,
     '{"statement": "L’eau du puits est toujours potable."}',
     '{"value": false}', 'Pas toujours : c’est pour ça qu’on filtre.'),

    ('La paix', 2, 'association', 2,
     '{"question": "Relie chaque geste à son mot.", "gauche": ["Je porte le panier de mon voisin", "Je joue avec un enfant d’ailleurs", "On construit ensemble"], "droite": ["Assister", "Accepter", "Collaborer"]}',
     '{"order": [0, 1, 2]}', 'Trois gestes du vivre-ensemble.'),

    ('La paix', 1, 'vrai_faux', 2,
     '{"statement": "On vit ensemble seulement au village."}',
     '{"value": false}', 'Au village ou en ville.'),

    ('La paix', 1, 'dictee', 3,
     '{"phrase": "Je vis bien avec les autres.", "langue": "fr"}',
     '{"phrase": "Je vis bien avec les autres."}', 'La paix commence là.'),

    ('La paix', 2, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Accepter", "aider", "et collaborer"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2]}', 'Les gestes du vivre-ensemble.'),

    ('La paix', 1, 'qcm', 4,
     '{"question": "Deux camarades se disputent. Que fais-tu pour la paix ?", "options": ["Je les aide à se parler", "Je prends un camp", "Je m’en vais"]}',
     '{"index": 0}', 'On rapproche, on ne sépare pas.'),

    ('La paix', 2, 'qcm', 4,
     '{"question": "Un nouvel élève ne parle pas ta langue. Tu fais quoi ?", "options": ["Je l’accepte et je l’aide", "Je me moque", "Je l’ignore"]}',
     '{"index": 0}', 'Accepter, c’est le premier geste.'),

    ('Le sol', 2, 'association', 2,
     '{"question": "Relie chaque sol à ce qui le reconnaît.", "gauche": ["Sablonneux", "Ferralitique", "Basaltique", "Argileux"], "droite": ["Des grains de roche", "Rouge, riche en fer", "Noir et fertile", "Mou, pas fertile"]}',
     '{"order": [0, 1, 2, 3]}', 'Les quatre sols du cahier.'),

    ('Le sol', 4, 'qcm', 2,
     '{"question": "Clique sur le sol ferralitique.", "images": ["so-ferralitique", "so-basaltique", "so-sablonneux", "so-argileux"]}',
     '{"index": 0}', 'Il est rouge.'),

    ('Le sol', 5, 'qcm', 2,
     '{"question": "Clique sur le sol basaltique.", "images": ["so-basaltique", "so-ferralitique", "so-argileux", "so-sablonneux"]}',
     '{"index": 0}', 'Il est noir.'),

    ('Le sol', 3, 'qcm', 2,
     '{"question": "Clique sur le sol sablonneux.", "images": ["so-sablonneux", "so-argileux", "so-basaltique", "so-ferralitique"]}',
     '{"index": 0}', 'Fait de grains de roche.'),

    ('Le sol', 1, 'dictee', 3,
     '{"phrase": "Le sol est la partie du dessus de la terre.", "langue": "fr"}',
     '{"phrase": "Le sol est la partie du dessus de la terre."}', 'La couche du dessus.'),

    ('Le sol', 4, 'dictee', 3,
     '{"phrase": "Le sol ferralitique est rouge.", "langue": "fr"}',
     '{"phrase": "Le sol ferralitique est rouge."}', 'Rouge, riche en fer.'),

    ('Le sol', 6, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Le sol argileux", "est mou", "et pas fertile"], "consigne": "Touche les mots dans l’ordre de la phrase."}',
     '{"order": [0, 1, 2]}', 'Mou et pas fertile.'),

    ('Le sol', 1, 'vrai_faux', 4,
     '{"statement": "Le sol est la partie profonde de la terre."}',
     '{"value": false}', 'C’est la partie du dessus.'),

    ('Le sol', 2, 'vrai_faux', 4,
     '{"statement": "Tous les sols se ressemblent."}',
     '{"value": false}', 'Ils diffèrent par leur structure.'),

    ('Le sol', 3, 'qcm', 4,
     '{"question": "Tu marches sur une terre qui coule entre les doigts. Lequel ?", "options": ["Sablonneux", "Argileux", "Basaltique"]}',
     '{"index": 0}', 'Des grains de roche.'),

    ('Le sol', 4, 'qcm', 4,
     '{"question": "Une terre très rouge après la pluie. Lequel ?", "options": ["Ferralitique", "Basaltique", "Sablonneux"]}',
     '{"index": 0}', 'Rouge : riche en fer.'),

    ('Le sol', 5, 'qcm', 4,
     '{"question": "Dans quel sol le maïs poussera-t-il le mieux ?", "options": ["Le basaltique", "L’argileux", "Le sablonneux"]}',
     '{"index": 0}', 'Noir et fertile.'),

    ('Le sol', 6, 'qcm', 4,
     '{"question": "Un paysan évite une terre molle où rien ne pousse. Laquelle ?", "options": ["L’argileuse", "La basaltique", "La ferralitique"]}',
     '{"index": 0}', 'Molle et pas fertile.')
  ) as v(lecon, ordre, kind, level, payload, answer, explain)
  join lessons l on l.title = v.lecon
  join notions n on n.lesson_id = l.id and n.sort_order = v.ordre and n.status = 'approved'
 where not exists (
   select 1 from items i where i.notion_id = n.id and i.payload = v.payload::jsonb
 );
