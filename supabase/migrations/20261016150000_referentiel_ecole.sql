-- Se Former Cameroun — le référentiel de l'école
--
-- Transcrit des deux emplois du temps de la New Century Bilingual School :
-- CM1 (« Class 5 ») et CE1 (« CL3 »).
--
-- Pourquoi : un cahier n'écrit pas le nom officiel de la matière. Il écrit
-- « Éducation morale », « Droits et devoirs », « Technologies ». Sans liste
-- fermée, chaque import invente sa matière — six ont été créées en une
-- fois, dont deux qui n'existent pas au tableau de l'école.
--
-- Trois apports :
--   1. les matières appartiennent désormais à une classe, et portent leur
--      libellé officiel dans les deux langues plus les intitulés de cahier
--      qui y renvoient ;
--   2. l'emploi du temps entre en base, avec la langue de chaque créneau —
--      « Maths » le lundi et « Mathématiques » le mercredi sont la même
--      matière enseignée dans deux langues, et le produit doit le savoir ;
--   3. les huit leçons déjà importées rejoignent les matières de leur
--      classe ; leur intitulé de cahier descend dans le chapitre.

-- ───────────────────────── matières par classe ─────────────────────────

alter table subjects add column if not exists class_id    uuid references classes (id);
alter table subjects add column if not exists official_fr text;
alter table subjects add column if not exists official_en text;
alter table subjects add column if not exists aliases     text[] not null default '{}';

-- Une même matière peut exister dans deux classes avec des libellés
-- identiques : l'unicité se joue désormais par classe.
alter table subjects drop constraint if exists subjects_parent_id_label_key;
create unique index if not exists subjects_parent_classe_label
  on subjects (parent_id, class_id, label);

-- ─────────────────────────── emploi du temps ───────────────────────────

create table if not exists timetable_slots (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  class_id   uuid not null references classes (id),
  subject_id uuid references subjects (id) on delete set null,
  -- 1 lundi … 5 vendredi
  day        smallint not null check (day between 1 and 5),
  debut      time not null,
  fin        time not null check (fin > debut),
  kind       text not null check (kind in ('cours', 'pause', 'rassemblement', 'club')),
  -- Le libellé exact de la feuille : c'est lui qui fait foi en cas de doute.
  label      text not null,
  lang       text check (lang in ('fr', 'en')),
  created_at timestamptz not null default now(),
  unique (parent_id, class_id, day, debut)
);

alter table timetable_slots enable row level security;

do $$
begin
  if not exists (select 1 from pg_policies where tablename = 'timetable_slots' and policyname = 'timetable_select') then
    create policy timetable_select on timetable_slots
      for select to authenticated using (parent_id = auth.uid());
    create policy timetable_insert on timetable_slots
      for insert to authenticated with check (parent_id = auth.uid());
    create policy timetable_update on timetable_slots
      for update to authenticated using (parent_id = auth.uid()) with check (parent_id = auth.uid());
    create policy timetable_delete on timetable_slots
      for delete to authenticated using (parent_id = auth.uid());
  end if;
end
$$;

-- ──────────────────────────── le contenu ────────────────────────────

create or replace function public.seed_referentiel_ecole(p_parent uuid)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  v_class   uuid;
  v_subject uuid;
  v_lesson  uuid;
  n         integer := 0;
begin

  -- ───────────────────────────── CM1 ─────────────────────────────
  select id into v_class from classes where subsystem = 'francophone' and code = 'CM1';

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Histoire-Géographie', '#d66d4d', 'Histoire / Géographie', 'Social Studies I (Hist/Geo)', array['Histoire', 'Géographie', 'Hist/Géo', 'Histoire-Géo']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'ECM', '#b4584f', 'Histoire / Géographie / ECM', 'Social Studies 2 (Civics, Moral Educ, Human Rights)', array['Éducation civique', 'Éducation morale', 'Droits et devoirs', 'Éducation à la paix', 'ECM']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Français', '#5b8ac2', 'Français', 'French', array['Français', 'Dictée', 'Grammaire', 'Conjugaison']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Anglais', '#4f7fae', 'Anglais', 'English Language', array['English', 'Anglais', 'Vocabulary', 'Grammar', 'Reading comprehension']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Mathématiques', '#3f7d6a', 'Mathématiques', 'Maths', array['Maths', 'Mathématiques', 'Calcul']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Sciences', '#3f9d8f', 'Sciences', 'Science', array['Sciences', 'SVT', 'Environnement', 'Santé']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Technologie', '#d08a3c', 'Technologie', 'Technology', array['Technologie', 'Technologies']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'TIC', '#7a76c4', 'TIC', 'ICT', array['TIC', 'TICE', 'Informatique', 'ICT']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Musique', '#c2708f', 'Musique', 'Music', array['Musique', 'Chant']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Dessin', '#c98f5a', 'Dessin', 'Drawing', array['Dessin', 'Arts plastiques']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'EPS', '#6f9a3f', 'EPS', 'PE', array['EPS', 'Sport']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Langues et cultures nationales', '#8a6fb0', 'Langues et cultures nationales', 'National languages and cultures', array['Langues nationales', 'Culture nationale']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Développement personnel', '#a0714d', 'Développement personnel', 'Personal development', array['Développement personnel']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Métiers', '#9a8450', 'Métiers', 'Vocational studies (home economics)', array['Économie familiale', 'Travaux manuels']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  -- L'emploi du temps est réécrit en entier : la feuille fait foi.
  delete from timetable_slots where parent_id = p_parent and class_id = v_class;

  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '07:20', '07:40', 'rassemblement', 'Morning devotion', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'ECM';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '07:40', '08:00', 'cours', 'Social Studies 2 (Civics)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '08:00', '08:30', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '08:30', '09:00', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire-Géographie';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '09:00', '09:30', 'cours', 'Social Studies I (Hist/Geo)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '10:00', '10:30', 'cours', 'English Language (Reading Comp)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Technologie';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '10:30', '11:00', 'cours', 'Technologie', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '11:10', '12:40', 'cours', 'Français', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '13:10', '13:40', 'cours', 'Français', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire-Géographie';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '13:40', '14:10', 'cours', 'Histoire / Géo', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '14:10', '14:40', 'cours', 'Sciences', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'TIC';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '14:40', '15:10', 'cours', 'TIC', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '07:20', '07:40', 'rassemblement', 'Devotion', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'ECM';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '07:40', '08:00', 'cours', 'Histoire / Géographie / ECM', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '08:00', '08:30', 'cours', 'Français', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '08:30', '09:00', 'cours', 'Sciences', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '09:00', '09:30', 'cours', 'Maths', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '09:30', '10:00', 'cours', 'Français', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '10:30', '11:00', 'cours', 'Français', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '11:00', '11:10', 'pause', 'Petite pause', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '11:10', '11:40', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '11:40', '12:10', 'cours', 'English Language (Vocabulary)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '12:10', '12:40', 'cours', 'Sciences (Health Educ)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '12:40', '13:10', 'pause', 'Long break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Métiers';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '13:10', '13:40', 'cours', 'Vocational Studies (Home Economics)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '14:10', '14:40', 'cours', 'English Language (Vocabulary)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'ECM';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '14:40', '15:10', 'cours', 'Social Studies II (Moral Educ)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '07:20', '07:40', 'rassemblement', 'Rassemblement', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '07:40', '08:00', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '08:00', '08:30', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire-Géographie';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '08:30', '09:00', 'cours', 'Social Studies I (Hist/Geo)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire-Géographie';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '09:00', '09:30', 'cours', 'Social Studies I (Hist/Geo)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '09:30', '10:00', 'cours', 'English Language (Vocabulary)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '10:00', '10:30', 'cours', 'English Language (Grammar)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '10:30', '11:00', 'cours', 'Sciences (Environ Educ)', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '11:10', '11:40', 'cours', 'Français', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '11:40', '12:10', 'cours', 'Sciences', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '12:10', '12:40', 'cours', 'Mathématiques', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Musique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '13:10', '13:40', 'cours', 'Musique', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'TIC';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '13:40', '14:10', 'cours', 'TIC', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '14:10', '14:40', 'cours', 'Français', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '14:40', '15:10', 'cours', 'Français', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '07:20', '07:40', 'rassemblement', 'Matinal', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'ECM';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '07:40', '08:00', 'cours', 'Histoire / Géo - ECM', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '08:00', '09:30', 'cours', 'Français', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '09:30', '10:00', 'cours', 'Mathématiques', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '10:00', '10:30', 'cours', 'Français', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Musique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '10:30', '11:00', 'cours', 'Musique', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '11:00', '11:10', 'pause', 'Petite pause', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '11:10', '11:40', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '11:40', '12:10', 'cours', 'English Language (Guided Writing)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '12:10', '12:40', 'cours', 'Sciences (Environ Educ)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '12:40', '13:10', 'pause', 'Long break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '13:10', '13:40', 'cours', 'Sciences (Health Educ)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Dessin';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '13:40', '14:10', 'cours', 'Drawing', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '14:10', '14:40', 'club', 'Club activities', null);
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '14:40', '15:10', 'club', 'Club activities', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'ECM';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '07:20', '07:40', 'cours', 'Social Studies 2 (Human Rights)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '07:40', '08:00', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '08:00', '08:30', 'cours', 'Maths', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '08:30', '09:00', 'cours', 'English Language (Productive Writing)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '09:00', '09:30', 'cours', 'English Language (Productive Writing)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '09:30', '10:00', 'cours', 'English Language (Spelling/Dictation)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'TIC';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '10:00', '10:30', 'cours', 'ICT', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '11:10', '11:40', 'cours', 'Sciences', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '11:40', '12:10', 'cours', 'Dictée', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Développement personnel';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '12:10', '12:40', 'cours', 'Développement personnel', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Langues et cultures nationales';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '13:10', '13:40', 'cours', 'Langues et cultures nationales', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '13:40', '14:10', 'cours', 'Mathématiques', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'EPS';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '14:10', '14:40', 'cours', 'EPS', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'EPS';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '14:40', '15:10', 'cours', 'EPS', 'fr');
  n := n + 1;

  -- ───────────────────────────── CE1 ─────────────────────────────
  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Histoire', '#d66d4d', 'Sciences humaines et sociales (histoire)', 'Social studies (history)', array['Histoire']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Géographie', '#c97c52', 'Sciences humaines et sociales (géographie)', 'Social studies (geography)', array['Géographie']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Éducation civique', '#3f9d8f', 'Sciences humaines et sociales (éducation civique)', 'Social studies (civics)', array['Éducation civique', 'Instruction civique']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Éducation morale', '#c2708f', 'Sciences humaines et sociales (éducation morale)', 'Social studies (moral education)', array['Éducation morale', 'Éducation à la paix', 'Morale']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Droits humains', '#5b8ac2', 'Sciences humaines et sociales (droits humains)', 'Social studies (human rights)', array['Droits et devoirs', 'Droits humains', 'Droits de l’enfant']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Français', '#4f7fae', 'Français', 'French', array['Français', 'Littérature', 'Grammaire', 'Conjugaison', 'Orthographe', 'Vocabulaire', 'Dictée']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Anglais', '#3f6f9e', 'Anglais', 'English language', array['English', 'Anglais', 'Vocabulary', 'Grammar', 'Spelling', 'Reading']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Mathématiques', '#3f7d6a', 'Mathématiques', 'Mathematics', array['Maths', 'Mathématiques', 'Nombres et calculs', 'Mesures et grandeurs', 'Géométrie']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Sciences et technologies', '#d08a3c', 'Sciences et technologies', 'Science and technology', array['Sciences', 'Technologies', 'Technologie', 'Environnement', 'Santé']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'TIC', '#7a76c4', 'T.I.C.E (informatique)', 'I.C.T', array['TIC', 'TICE', 'Informatique', 'ICT']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Éducation artistique', '#b36fa0', 'Éducation artistique (musique, dessin)', 'Art and craft', array['Musique', 'Dessin', 'Art', 'Chant']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'EPS', '#6f9a3f', 'EPS', 'P.E', array['EPS', 'Sport']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Langue et culture nationale', '#8a6fb0', 'Langue et culture nationale', 'National language and culture', array['Langues nationales', 'Culture nationale']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Développement personnel', '#a0714d', 'Développement personnel', 'Personal development', array['Développement personnel']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Métiers', '#9a8450', 'Métiers', 'Vocational studies', array['Économie familiale', 'Agropastoral', 'Travaux manuels']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)
  values (p_parent, v_class, 'Bibliothèque', '#7d8a6a', 'Bibliothèque / littérature', 'Library / literature', array['Bibliothèque', 'Lecture suivie']::text[])
  on conflict (parent_id, class_id, label) do update
    set color = excluded.color, official_fr = excluded.official_fr,
        official_en = excluded.official_en, aliases = excluded.aliases;

  -- L'emploi du temps est réécrit en entier : la feuille fait foi.
  delete from timetable_slots where parent_id = p_parent and class_id = v_class;

  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '07:20', '07:40', 'rassemblement', 'Morning devotion and inspection', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '07:40', '08:00', 'cours', 'Mathematics', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '08:00', '08:30', 'cours', 'English language (vocabulary)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Métiers';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '08:30', '09:00', 'cours', 'Vocational studies (home economics)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Géographie';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '09:00', '09:30', 'cours', 'Social studies (geography)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '09:30', '10:00', 'cours', 'English language (grammar)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '10:00', '10:30', 'cours', 'English language (spelling and dictation)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '10:30', '11:00', 'cours', 'Science and technology (environ education)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '11:10', '11:40', 'cours', 'Français (littérature)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '11:40', '12:10', 'cours', 'Français (vocabulaire)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '12:10', '12:40', 'cours', 'Français (grammaire)', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '13:10', '13:40', 'cours', 'Mathématiques (nombres et calculs)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '13:40', '14:10', 'cours', 'Mathématiques (nombres et calculs)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '14:10', '14:40', 'cours', 'Sciences et technologies', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 1, '14:40', '15:10', 'cours', 'Sciences humaines et sociales (histoire)', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '07:20', '07:40', 'rassemblement', 'Morning devotion and inspection', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation civique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '07:40', '08:00', 'cours', 'Sciences humaines et sociales (éducation civique)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '08:00', '08:30', 'cours', 'Français (littérature)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '08:30', '09:00', 'cours', 'Français (production d’écrits)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '09:00', '09:30', 'cours', 'Français (production d’écrits)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation artistique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '09:30', '10:00', 'cours', 'Musique', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '10:00', '10:30', 'cours', 'Mathématiques (mesures et grandeurs)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '10:30', '11:00', 'cours', 'Sciences et technologies', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '11:10', '11:40', 'cours', 'Literature', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '11:40', '12:10', 'cours', 'Mathematics', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '12:10', '12:40', 'cours', 'Science and technology (environmental education)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'TIC';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '13:10', '13:40', 'cours', 'ICT', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Métiers';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '13:40', '14:10', 'cours', 'Vocational studies (home economics)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation artistique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '14:10', '14:40', 'cours', 'Art (drama and sing)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation artistique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 2, '14:40', '15:10', 'cours', 'Art and craft (drawing)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '07:20', '07:40', 'rassemblement', 'Morning devotion and inspection', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation civique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '07:40', '08:00', 'cours', 'Social studies (civics)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '08:00', '08:30', 'cours', 'Mathematics', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '08:30', '09:00', 'cours', 'English language (vocabulary)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '09:00', '09:30', 'cours', 'English language (guided writing and handwriting)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '09:30', '10:00', 'cours', 'Social studies (history)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'TIC';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '10:00', '10:30', 'cours', 'I.C.T', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '10:30', '11:00', 'cours', 'Science and technology (tech and engineering)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '11:10', '11:40', 'cours', 'Français (littérature)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '11:40', '12:10', 'cours', 'Mathématiques (géométrie et espace)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '12:10', '12:40', 'cours', 'Mathématiques (géométrie et espace)', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '13:10', '13:40', 'cours', 'Français (conjugaison)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation civique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '13:40', '14:10', 'cours', 'Sciences humaines et sociales (éducation civique)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '14:10', '14:40', 'cours', 'Sciences et technologies', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Bibliothèque';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 3, '14:40', '15:10', 'cours', 'Bibliothèque / littérature', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '07:20', '07:40', 'rassemblement', 'Morning devotion and inspection', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation morale';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '07:40', '08:00', 'cours', 'Sciences humaines et sociales (éducation morale)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '08:00', '08:30', 'cours', 'Français (littérature)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '08:30', '09:00', 'cours', 'Mathématiques (mesures et grandeurs)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '09:00', '09:30', 'cours', 'Français (grammaire)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '09:30', '10:00', 'cours', 'Français (orthographe)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Développement personnel';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '10:00', '10:30', 'cours', 'Développement personnel', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'EPS';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '10:30', '11:00', 'cours', 'EPS', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '11:10', '11:40', 'cours', 'English language (grammar)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '11:40', '12:10', 'cours', 'Mathematics', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Langue et culture nationale';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '12:10', '12:40', 'cours', 'National language and culture', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '13:10', '13:40', 'cours', 'English language (spelling and dictation)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '13:40', '14:10', 'cours', 'English language (extensive reading)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '14:10', '14:40', 'club', 'Clubs', null);
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 4, '14:40', '15:10', 'club', 'Clubs', null);
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '07:20', '07:40', 'rassemblement', 'Morning devotion and inspection', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation morale';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '07:40', '08:00', 'cours', 'Social studies (moral education)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '08:00', '08:30', 'cours', 'Mathematics', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '08:30', '09:00', 'cours', 'English language (vocabulary)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Droits humains';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '09:00', '09:30', 'cours', 'Social studies (human rights)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Anglais';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '09:30', '10:00', 'cours', 'English language (reading comprehension)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '10:00', '10:30', 'cours', 'Science and technology (health education)', 'en');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Métiers';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '10:30', '11:00', 'cours', 'Vocational studies (agropastoral farming)', 'en');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '11:00', '11:10', 'pause', 'Short break', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '11:10', '11:40', 'cours', 'Mathématiques (mesures et grandeurs)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Mathématiques';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '11:40', '12:10', 'cours', 'Mathématiques (mesures et grandeurs)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '12:10', '12:40', 'cours', 'Sciences et technologies', 'fr');
  n := n + 1;
  v_subject := null;
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '12:40', '13:10', 'pause', 'Récréation', null);
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation artistique';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '13:10', '13:40', 'cours', 'Éducation artistique (musique, dessin)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Français';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '13:40', '14:10', 'cours', 'Français (NCBS dictée)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'TIC';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '14:10', '14:40', 'cours', 'T.I.C.E (informatique)', 'fr');
  n := n + 1;
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Langue et culture nationale';
  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)
  values (p_parent, v_class, v_subject, 5, '14:40', '15:10', 'cours', 'Langue et culture nationale', 'fr');
  n := n + 1;

  -- ───────────── rattachement des leçons déjà importées ─────────────
  select id into v_class from classes where subsystem = 'francophone' and code = 'CM1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire-Géographie';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Histoire' where title = 'La Préhistoire';

  select id into v_class from classes where subsystem = 'francophone' and code = 'CM1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Histoire-Géographie';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Histoire' where title = 'Les grandes inventions et les grandes découvertes';

  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation morale';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Éducation morale' where title = 'L’obéissance';

  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Droits humains';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Droits et devoirs' where title = 'Le droit à l’identité';

  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation civique';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Éducation civique' where title = 'L’intégration nationale';

  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Sciences et technologies';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Technologies' where title = 'Les techniques de filtrage de l’eau';

  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Éducation morale';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Éducation à la paix' where title = 'La paix';

  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';
  select id into v_subject from subjects where parent_id = p_parent and class_id = v_class and label = 'Géographie';
  update lessons set subject_id = v_subject, class_id = v_class, chapter = 'Géographie' where title = 'Le sol';

  -- Les matières inventées au fil des cahiers, désormais sans leçon,
  -- disparaissent : elles ne doivent plus être proposées à l'import.
  delete from subjects s
   where s.parent_id = p_parent and s.class_id is null
     and not exists (select 1 from lessons l where l.subject_id = s.id);

  return n;
end;
$$;

select public.seed_referentiel_ecole(parent_id)
  from children
 where first_name = 'KLEIN'
 limit 1;
