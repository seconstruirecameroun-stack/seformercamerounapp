-- Se Former Cameroun — la date du cours
--
-- Le cahier la porte en haut de chaque page : « Mardi 13 Octobre 2026 ».
-- Elle ne survivait nulle part. Elle sert à deux choses : ranger les leçons
-- d'une matière dans l'ordre où elles ont été faites, et retrouver un cours
-- par le jour où il a été donné — « le cours de mardi » est la façon dont un
-- enfant le nomme.
--
-- Nullable, et c'est important : toutes les pages n'en portent pas. Deviner
-- le jour d'un cours serait pire que de l'ignorer, donc une page sans date
-- reste importable et se range après celles qui en ont une.

alter table lessons   add column if not exists taught_on date;
alter table documents add column if not exists taught_on date;

create index if not exists lessons_taught_on on lessons (parent_id, taught_on desc);

-- Les dates réellement écrites sur les pages photographiées. Les deux leçons
-- dont la page n'en porte pas restent sans date : « Le droit à l'identité »,
-- qui suit la page du 13 sans en reprendre l'en-tête, et « Le sol ».
-- « La Préhistoire » est la leçon d'exemple, elle n'a pas de cahier.

update lessons set taught_on = date '2026-10-13'
 where title = 'Les grandes inventions et les grandes découvertes';

update lessons set taught_on = date '2026-10-13' where title = 'L’obéissance';
update lessons set taught_on = date '2026-10-14' where title = 'L’intégration nationale';
update lessons set taught_on = date '2026-10-14' where title = 'Les techniques de filtrage de l’eau';
update lessons set taught_on = date '2026-10-15' where title = 'La paix';
