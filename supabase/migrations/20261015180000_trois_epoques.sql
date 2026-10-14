-- Se Former Cameroun — une vignette propre pour la notion des trois époques
--
-- Elle réutilisait la roue-mémoire, déjà portée par la première notion : deux
-- cases identiques dans la collection, et aucun indice visuel sur ce qu'il
-- fallait retenir.
--
-- La nouvelle image montre la chose elle-même : silex taillé, galet poli,
-- bracelet de bronze, alignés de gauche à droite. L'ordre est dans l'image.

update notions n
   set illustration = 'trois-epoques'
  from lessons l
 where n.lesson_id = l.id
   and l.title = 'La Préhistoire'
   and n.statement like '%trois époques se suivent%';

-- Et dans la fonction qui rattache les illustrations de la démonstration, pour
-- que les prochaines familles obtiennent la même chose.
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
       when n.statement like '%trois époques se suivent%'        then 'trois-epoques'
       else n.illustration
     end
    from lessons l
   where n.lesson_id = l.id
     and l.title = 'La Préhistoire';
end;
$$;
