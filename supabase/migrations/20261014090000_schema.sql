-- Se Former Cameroun — schéma initial (lot 0)
--
-- Deux partis pris, valables pour tout le fichier :
--
-- 1. parent_id est répété sur chaque table, même quand il serait déductible
--    par jointure. C'est volontaire : la politique RLS devient
--    « parent_id = auth.uid() », sans sous-requête ni récursion. Le coût est
--    une colonne redondante, le gain est une sécurité lisible et rapide.
--
-- 2. lang est porté par la leçon et par rien en dessous. Un cours est dans une
--    seule langue, donc notions, explications, items et vidéo en héritent.

create extension if not exists pgcrypto;

-- ───────────────────────────────── types ─────────────────────────────────

create type subsystem        as enum ('francophone', 'anglophone');
create type doc_kind         as enum ('cours', 'devoir', 'autre');
create type content_status   as enum ('pending', 'approved', 'rejected');
create type media_status     as enum ('queued', 'script_ready', 'rendering', 'ready', 'published', 'failed');
create type job_status       as enum ('queued', 'running', 'ready', 'failed');
create type notion_kind      as enum ('definition', 'date', 'liste', 'relation');
create type explain_register as enum ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas');
create type item_kind        as enum ('qcm', 'association', 'chronologie', 'texte_a_trous',
                                      'vrai_faux', 'restitution_audio', 'defi_chrono');

-- ──────────────────────── référentiel des classes ────────────────────────
-- Seule table partagée par toutes les familles. Elle situe l'enfant ; elle ne
-- détermine aucun contenu.

create table classes (
  id        uuid primary key default gen_random_uuid(),
  subsystem subsystem not null,
  code      text      not null,
  rank      smallint  not null check (rank between 1 and 6),
  unique (subsystem, code),
  unique (subsystem, rank)
);

insert into classes (subsystem, code, rank) values
  ('francophone', 'SIL',     1),
  ('francophone', 'CP',      2),
  ('francophone', 'CE1',     3),
  ('francophone', 'CE2',     4),
  ('francophone', 'CM1',     5),
  ('francophone', 'CM2',     6),
  ('anglophone',  'Class 1', 1),
  ('anglophone',  'Class 2', 2),
  ('anglophone',  'Class 3', 3),
  ('anglophone',  'Class 4', 4),
  ('anglophone',  'Class 5', 5),
  ('anglophone',  'Class 6', 6);

-- ───────────────────────────── espace parent ─────────────────────────────

create table parent_settings (
  parent_id        uuid primary key references auth.users (id) on delete cascade,
  pin_hash         text,
  interface_lang   text not null default 'fr' check (interface_lang in ('fr', 'en')),
  generation_quota int  not null default 20,
  video_quota      int  not null default 2,
  created_at       timestamptz not null default now()
);

-- Une ligne de réglages par parent, créée à l'inscription.
create or replace function public.handle_new_parent()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.parent_settings (parent_id)
  values (new.id)
  on conflict (parent_id) do nothing;
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_parent();

create table children (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  first_name text not null check (char_length(btrim(first_name)) between 1 and 40),
  class_id   uuid references classes (id),
  avatar     text,
  created_at timestamptz not null default now()
);

create index children_parent_idx on children (parent_id);

-- Intitulés libres : ce sont ceux de l'école de l'enfant, pas ceux d'un
-- référentiel national.
create table subjects (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  label      text not null check (char_length(btrim(label)) between 1 and 60),
  color      text,
  created_at timestamptz not null default now(),
  unique (parent_id, label)
);

-- ────────────────────────── documents et contenu ──────────────────────────

create table documents (
  id           uuid primary key default gen_random_uuid(),
  parent_id    uuid not null references auth.users (id) on delete cascade,
  child_id     uuid references children (id) on delete set null,
  subject_id   uuid references subjects (id) on delete set null,
  kind         doc_kind       not null default 'cours',
  storage_path text,
  raw_text     text,
  status       content_status not null default 'pending',
  created_at   timestamptz    not null default now()
);

create index documents_parent_idx on documents (parent_id);

create table lessons (
  id          uuid primary key default gen_random_uuid(),
  parent_id   uuid not null references auth.users (id) on delete cascade,
  document_id uuid references documents (id) on delete set null,
  subject_id  uuid references subjects (id) on delete set null,
  class_id    uuid references classes (id),
  title       text not null,
  summary     text,
  lang        text not null check (lang in ('fr', 'en')),
  chapter     text,
  sort_order  smallint       not null default 0,
  status      content_status not null default 'pending',
  created_at  timestamptz    not null default now()
);

create index lessons_parent_idx on lessons (parent_id);

create table notions (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  lesson_id  uuid not null references lessons (id) on delete cascade,
  kind       notion_kind    not null,
  statement  text           not null,
  sort_order smallint       not null default 0,
  status     content_status not null default 'pending',
  created_at timestamptz    not null default now()
);

create index notions_lesson_idx on notions (lesson_id, sort_order);

create table explanations (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  notion_id  uuid not null references notions (id) on delete cascade,
  register   explain_register not null,
  body       text             not null,
  status     content_status   not null default 'pending',
  created_at timestamptz      not null default now()
);

create index explanations_notion_idx on explanations (notion_id);

-- payload porte l'énoncé et les choix, answer porte la réponse attendue.
-- Les deux sont en jsonb parce que leur forme dépend de item_kind.
create table items (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  notion_id  uuid not null references notions (id) on delete cascade,
  kind       item_kind      not null,
  level      smallint       not null check (level between 1 and 4),
  payload    jsonb          not null,
  answer     jsonb          not null,
  explain    text,
  status     content_status not null default 'pending',
  created_at timestamptz    not null default now()
);

create index items_notion_idx on items (notion_id, level);

-- Le manifeste reste en base : il permet de régénérer une vidéo à l'identique,
-- ou avec une seule ligne corrigée.
create table videos (
  id           uuid primary key default gen_random_uuid(),
  parent_id    uuid not null references auth.users (id) on delete cascade,
  lesson_id    uuid not null references lessons (id) on delete cascade,
  manifest     jsonb,
  voice_preset text,
  storage_path text,
  external_url text,
  poster_url   text,
  duration_s   int,
  status       media_status not null default 'queued',
  created_at   timestamptz  not null default now()
);

create index videos_lesson_idx on videos (lesson_id);

-- File de travaux : OCR, extraction, génération de texte, rendu vidéo.
create table jobs (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  kind       text       not null,
  target_id  uuid,
  status     job_status not null default 'queued',
  attempts   int        not null default 0,
  error      text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index jobs_status_idx on jobs (parent_id, status);

-- ──────────────────────────── progression ────────────────────────────

create table lesson_progress (
  child_id     uuid not null references children (id) on delete cascade,
  lesson_id    uuid not null references lessons (id) on delete cascade,
  parent_id    uuid not null references auth.users (id) on delete cascade,
  seen_at      timestamptz,
  completed_at timestamptz,
  primary key (child_id, lesson_id)
);

create table mastery (
  child_id    uuid not null references children (id) on delete cascade,
  notion_id   uuid not null references notions (id) on delete cascade,
  parent_id   uuid not null references auth.users (id) on delete cascade,
  level       smallint not null default 1 check (level between 1 and 4),
  score       smallint not null default 0 check (score between 0 and 100),
  streak      smallint not null default 0,
  next_review date,
  updated_at  timestamptz not null default now(),
  primary key (child_id, notion_id)
);

create index mastery_due_idx on mastery (child_id, next_review);

-- Journal brut, en ajout seul : aucune politique update ou delete n'est créée
-- pour cette table (voir la migration RLS). mastery en est la vue agrégée,
-- recalculable depuis ce journal si la formule de progression change.
create table attempts (
  id          bigint generated always as identity primary key,
  parent_id   uuid not null references auth.users (id) on delete cascade,
  child_id    uuid not null references children (id) on delete cascade,
  item_id     uuid not null references items (id) on delete cascade,
  answer      jsonb,
  correct     boolean not null,
  duration_ms int,
  created_at  timestamptz not null default now()
);

create index attempts_child_idx on attempts (child_id, created_at desc);

create table rewards (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  child_id   uuid not null references children (id) on delete cascade,
  kind       text not null,
  value      int  not null default 0,
  created_at timestamptz not null default now()
);

create index rewards_child_idx on rewards (child_id);

create table assignments (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  child_id   uuid not null references children (id) on delete cascade,
  subject_id uuid references subjects (id) on delete set null,
  title      text not null,
  due_on     date,
  done       boolean not null default false,
  created_at timestamptz not null default now()
);

create index assignments_due_idx on assignments (child_id, due_on);
