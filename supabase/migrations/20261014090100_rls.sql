-- Se Former Cameroun — RLS et verrou parent (lot 0)
--
-- Règle unique pour presque tout : parent_id = auth.uid().
-- Trois exceptions, toutes justifiées plus bas :
--   classes          lecture seule, partagée par toutes les familles
--   attempts         ajout seul, jamais de modification ni de suppression
--   parent_settings  la colonne pin_hash n'est jamais lisible par le client

-- ───────────────────────── droits de base ─────────────────────────

grant usage on schema public to authenticated;

grant select, insert, update, delete on
  children, subjects, documents, lessons, notions, explanations, items,
  videos, jobs, lesson_progress, mastery, rewards, assignments
to authenticated;

grant select, insert on attempts to authenticated;
grant usage, select on sequence attempts_id_seq to authenticated;
grant select on classes to authenticated;
grant select, insert, update on parent_settings to authenticated;

-- ───────────────────── politique commune ─────────────────────
-- Les treize tables ci-dessous suivent exactement la même règle. Une boucle
-- évite cinquante-deux politiques copiées à la main, et donc l'oubli d'une
-- seule d'entre elles.

do $$
declare
  t text;
begin
  foreach t in array array[
    'children', 'subjects', 'documents', 'lessons', 'notions', 'explanations',
    'items', 'videos', 'jobs', 'lesson_progress', 'mastery', 'rewards',
    'assignments'
  ]
  loop
    execute format('alter table %I enable row level security', t);

    execute format(
      'create policy %I on %I for select to authenticated using (parent_id = auth.uid())',
      t || '_select', t);

    execute format(
      'create policy %I on %I for insert to authenticated with check (parent_id = auth.uid())',
      t || '_insert', t);

    execute format(
      'create policy %I on %I for update to authenticated using (parent_id = auth.uid()) with check (parent_id = auth.uid())',
      t || '_update', t);

    execute format(
      'create policy %I on %I for delete to authenticated using (parent_id = auth.uid())',
      t || '_delete', t);
  end loop;
end
$$;

-- ───────────────────── les trois exceptions ─────────────────────

-- Référentiel partagé : tout parent connecté le lit, personne ne l'écrit.
alter table classes enable row level security;

create policy classes_select on classes
  for select to authenticated using (true);

-- Journal brut : on ajoute et on lit, on ne réécrit pas l'histoire.
-- L'absence de politique update et delete est ici la fonctionnalité.
alter table attempts enable row level security;

create policy attempts_select on attempts
  for select to authenticated using (parent_id = auth.uid());

create policy attempts_insert on attempts
  for insert to authenticated with check (parent_id = auth.uid());

-- Réglages : le parent lit et modifie les siens, mais pas le hash du code.
alter table parent_settings enable row level security;

create policy parent_settings_select on parent_settings
  for select to authenticated using (parent_id = auth.uid());

create policy parent_settings_insert on parent_settings
  for insert to authenticated with check (parent_id = auth.uid());

create policy parent_settings_update on parent_settings
  for update to authenticated
  using (parent_id = auth.uid()) with check (parent_id = auth.uid());

-- Le privilège de table est retiré puis réaccordé colonne par colonne :
-- en PostgreSQL un privilège de table l'emporte sur un retrait de colonne,
-- il faut donc passer par là pour que pin_hash devienne inaccessible.
revoke select, update on parent_settings from authenticated;

grant select (parent_id, interface_lang, generation_quota, video_quota, created_at)
  on parent_settings to authenticated;

grant update (interface_lang)
  on parent_settings to authenticated;

-- ───────────────────────── verrou parent ─────────────────────────
--
-- Le code sert à empêcher un enfant d'aller voir les réponses ou de modifier
-- sa progression. Ce n'est pas un secret cryptographique : quatre chiffres
-- font dix mille combinaisons. Il est néanmoins haché, et la vérification se
-- fait en base, pour que le hash ne parte jamais vers le navigateur.

create or replace function public.set_parent_pin(new_pin text)
returns void
language plpgsql
security definer
set search_path = public, extensions
as $$
begin
  if auth.uid() is null then
    raise exception 'authentification requise';
  end if;

  if new_pin !~ '^[0-9]{4}$' then
    raise exception 'le code doit comporter exactement quatre chiffres';
  end if;

  insert into parent_settings (parent_id, pin_hash)
  values (auth.uid(), crypt(new_pin, gen_salt('bf')))
  on conflict (parent_id) do update set pin_hash = excluded.pin_hash;
end;
$$;

create or replace function public.verify_parent_pin(candidate text)
returns boolean
language plpgsql
security definer
set search_path = public, extensions
as $$
declare
  stored text;
begin
  if auth.uid() is null then
    return false;
  end if;

  select pin_hash into stored
    from parent_settings
   where parent_id = auth.uid();

  -- Pas de code défini : l'espace parent reste ouvert, à charge pour
  -- l'interface de proposer d'en créer un.
  if stored is null then
    return true;
  end if;

  return stored = crypt(candidate, stored);
end;
$$;

create or replace function public.parent_pin_is_set()
returns boolean
language sql
security definer
set search_path = public
as $$
  select exists (
    select 1 from parent_settings
     where parent_id = auth.uid() and pin_hash is not null
  );
$$;

revoke all on function public.set_parent_pin(text)    from public, anon;
revoke all on function public.verify_parent_pin(text)  from public, anon;
revoke all on function public.parent_pin_is_set()      from public, anon;

grant execute on function public.set_parent_pin(text)   to authenticated;
grant execute on function public.verify_parent_pin(text) to authenticated;
grant execute on function public.parent_pin_is_set()     to authenticated;
