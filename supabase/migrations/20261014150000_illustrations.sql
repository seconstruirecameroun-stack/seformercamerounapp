-- Se Former Cameroun — illustrations de leçon
--
-- Une leçon porte une scène, une notion porte une vignette.
--
-- La colonne accepte deux formes :
--   'prehistoire-grotte'          → une illustration livrée avec l'app,
--                                   résolue en /illustrations/<clé>.webp
--   'https://…/scene.webp'        → une illustration générée pour cette
--                                   leçon et déposée sur le stockage
--
-- La première forme ne coûte aucune requête réseau et fonctionne hors-ligne ;
-- la seconde servira aux leçons produites à partir des cours importés.

alter table lessons add column if not exists illustration text;
alter table notions add column if not exists illustration text;

-- Rattache les illustrations livrées à la leçon de démonstration.
--
-- Le rapprochement se fait sur le texte des notions plutôt que sur leur
-- identifiant : chaque famille possède sa propre copie de la leçon, créée par
-- seed_demo_prehistoire, et les identifiants diffèrent d'une copie à l'autre.
create or replace function public.illustrer_demo()
returns void
language plpgsql
security invoker
set search_path = public
as $$
begin
  update lessons
     set illustration = 'prehistoire-grotte'
   where title = 'La Préhistoire'
     and illustration is null;

  update notions n
     set illustration = case
       when n.statement like '%apparition des premiers humains%' then 'roue-memoire'
       when n.statement like '%3 000 avant J.-C.%'               then 'tablette-ecriture'
       when n.statement like '%pierre taillée%'                  then 'biface'
       when n.statement like '%chasse, de la pêche%'             then 'chasse-peche-cueillette'
       when n.statement like '%pierre polie%'                    then 'hache-ble'
       when n.statement like '%cuivre, bronze et fer%'           then 'metaux'
       when n.statement like '%trois époques se suivent%'        then 'roue-memoire'
       else n.illustration
     end
    from lessons l
   where n.lesson_id = l.id
     and l.title = 'La Préhistoire';
end;
$$;

revoke all on function public.illustrer_demo() from public, anon;
grant execute on function public.illustrer_demo() to authenticated;

-- Applique sur les copies déjà créées. La migration s'exécute hors session
-- parent, donc sans RLS : toutes les familles ayant déjà chargé la
-- démonstration en profitent.
update lessons
   set illustration = 'prehistoire-grotte'
 where title = 'La Préhistoire'
   and illustration is null;

update notions n
   set illustration = case
     when n.statement like '%apparition des premiers humains%' then 'roue-memoire'
     when n.statement like '%3 000 avant J.-C.%'               then 'tablette-ecriture'
     when n.statement like '%pierre taillée%'                  then 'biface'
     when n.statement like '%chasse, de la pêche%'             then 'chasse-peche-cueillette'
     when n.statement like '%pierre polie%'                    then 'hache-ble'
     when n.statement like '%cuivre, bronze et fer%'           then 'metaux'
     when n.statement like '%trois époques se suivent%'        then 'roue-memoire'
     else n.illustration
   end
  from lessons l
 where n.lesson_id = l.id
   and l.title = 'La Préhistoire'
   and n.illustration is null;
