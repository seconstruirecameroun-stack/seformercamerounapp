-- Se Former Cameroun — l'affiche du film passe en version légère
--
-- poster_url pointait vers le PNG d'origine : 22,8 Mo, affichés avant même que
-- l'enfant ne lance la vidéo. Sur une connexion facturée au volume, une seule
-- ouverture de la leçon coûtait plus cher que tout le reste de l'app réuni.
--
-- La colonne accepte désormais les deux formes déjà retenues pour illustration :
-- une clé livrée avec l'app, ou une URL. On bascule la démonstration sur la
-- clé, dont la version WebP pèse 35 ko.

update videos
   set poster_url = 'prehistoire-film'
 where poster_url like 'https://d8j0ntlcm91z4.cloudfront.net/%'
   and lesson_id in (select id from lessons where title = 'La Préhistoire');
