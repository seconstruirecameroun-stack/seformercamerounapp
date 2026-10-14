-- Se Former Cameroun — des textes à la taille d'un enfant de neuf ans
--
-- Les explications de la démonstration faisaient deux à trois lignes. Affichées
-- en grand sur un téléphone, elles remplissaient la fiche et personne ne les
-- lisait. La règle désormais tenue : une explication tient en une phrase
-- courte, deux au maximum, et sous une centaine de caractères.
--
-- Mieux vaut une phrase que l'enfant lit qu'un paragraphe exact qu'il saute.

update lessons
   set summary = 'La Préhistoire va des premiers humains à l’invention de l’écriture, '
              || 'vers 3 000 avant J.-C. Trois époques : Paléolithique, Néolithique, '
              || 'âge des métaux.'
 where title = 'La Préhistoire';

update explanations e
   set body = c.corps
  from (values
    ('apparition des premiers humains', 'simple',    'Le très long temps d’avant l’écriture.'),
    ('apparition des premiers humains', 'analogie',  'C’est comme un livre : avant la première page écrite.'),
    ('apparition des premiers humains', 'pas_a_pas', '1. Les humains arrivent. 2. Ils vivent sans écrire. 3. L’écriture arrive : c’est fini.'),
    ('3 000 avant J.-C.',               'simple',    'Vers 3 000 avant J.-C., l’écriture apparaît. La Préhistoire s’arrête.'),
    ('3 000 avant J.-C.',               'visuel',    'Sur la frise : à gauche la Préhistoire, à droite l’Histoire.'),
    ('pierre taillée',                  'simple',    'Paléolithique = pierre ancienne. On casse la pierre pour couper.'),
    ('pierre taillée',                  'analogie',  'Comme casser une craie pour obtenir une pointe.'),
    ('chasse, de la pêche',             'simple',    'Trois mots : chasse, pêche, cueillette.'),
    ('chasse, de la pêche',             'histoire',  'Ona pêche, son frère chasse, leur mère cueille. Le soir, on partage.'),
    ('pierre polie',                    'simple',    'Néolithique = pierre polie. On frotte la pierre, et on cultive la terre.'),
    ('pierre polie',                    'analogie',  'Comme poncer du bois : on frotte au lieu de casser.'),
    ('cuivre, bronze et fer',           'simple',    'Cuivre, bronze, fer : des outils et des bijoux.'),
    ('trois époques se suivent',        'simple',    'Tailler, puis polir, puis fondre le métal.'),
    ('trois époques se suivent',        'visuel',    'Pierre pointue, pierre lisse, bijou en métal.')
  ) as c (fragment, registre, corps)
 where e.notion_id in (
         select n.id
           from notions n
           join lessons l on l.id = n.lesson_id
          where l.title = 'La Préhistoire'
            and n.statement like '%' || c.fragment || '%'
       )
   and e.register::text = c.registre;
