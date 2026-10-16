-- La fiche de l'enfant.
--
-- On ne connaissait de lui qu'un prénom, un emoji et une classe. Trois
-- renseignements manquaient, tous utiles plus tard et tous demandés une fois
-- pour toutes à la création :
--
--   · la date de naissance, dont découle l'âge. Elle sert à choisir le
--     vocabulaire d'une explication, et à repérer un enfant en avance ou en
--     retard sur sa classe ;
--   · le genre, parce que le français s'accorde. « Tu es prêt ? » et « tu es
--     prête ? » ne se disent pas au hasard, et un enfant de sept ans le
--     remarque ;
--   · l'école, parce que le programme et l'emploi du temps en dépendent —
--     c'est déjà le principe retenu pour les matières, qui ne sont pas
--     figées dans un référentiel national.
--
-- Les trois sont facultatifs. Un parent pressé crée un profil avec un prénom
-- et complète plus tard ; rien dans l'app n'exige ces champs pour marcher.

alter table children add column if not exists birth_date date;
alter table children add column if not exists sex text;
alter table children add column if not exists school text;

do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'children_sex_check'
  ) then
    alter table children
      add constraint children_sex_check check (sex in ('fille', 'garcon'));
  end if;
end $$;

-- Une date de naissance dans le futur, ou un enfant de plus de trente ans,
-- est une faute de frappe : mieux vaut la refuser que la ranger.
do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'children_birth_date_check'
  ) then
    alter table children
      add constraint children_birth_date_check
      check (birth_date is null or (birth_date > current_date - interval '30 years'
             and birth_date < current_date));
  end if;
end $$;

comment on column children.birth_date is 'Facultative. L''âge en découle, jamais stocké.';
comment on column children.sex is 'Facultatif. Sert aux accords du français, pas à trier.';
comment on column children.school is 'Facultative. Le programme et l''emploi du temps en dépendent.';
