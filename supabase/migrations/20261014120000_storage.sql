-- Se Former Cameroun — stockage des documents importés (lot 1)
--
-- Un seul compartiment privé. Le chemin de chaque fichier commence par
-- l'identifiant du parent :
--
--     cours/<parent_id>/<document_id>/<nom du fichier>
--
-- C'est ce premier segment qui porte la sécurité : les politiques comparent
-- storage.foldername(name)[1] à auth.uid(). Un parent ne peut donc ni lire ni
-- écrire dans le dossier d'un autre, même en devinant un chemin.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'cours',
  'cours',
  false,
  20971520, -- 20 Mo : une photo de cahier, pas une vidéo
  array['image/jpeg', 'image/png', 'image/webp', 'image/heic', 'application/pdf']
)
on conflict (id) do update
  set file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

create policy "cours_lecture_proprietaire"
  on storage.objects for select to authenticated
  using (bucket_id = 'cours' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "cours_depot_proprietaire"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'cours' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "cours_remplacement_proprietaire"
  on storage.objects for update to authenticated
  using (bucket_id = 'cours' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'cours' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "cours_suppression_proprietaire"
  on storage.objects for delete to authenticated
  using (bucket_id = 'cours' and (storage.foldername(name))[1] = auth.uid()::text);

-- ─────────────────── ce que l'import doit retenir ───────────────────

alter table documents add column if not exists original_name text;
alter table documents add column if not exists mime text;
alter table documents add column if not exists size_bytes int;
alter table documents add column if not exists page_no smallint not null default 1;
alter table documents add column if not exists batch_id uuid;
alter table documents add column if not exists lang text check (lang in ('fr', 'en'));
alter table documents add column if not exists title_guess text;

-- Plusieurs photos peuvent former un seul cours : batch_id les regroupe, et
-- page_no les ordonne. C'est la question de granularité laissée ouverte dans
-- le document de structure — le parent tranche à l'import, l'app propose.
create index if not exists documents_batch_idx on documents (batch_id, page_no);

-- ─────────────────── état d'avancement du traitement ───────────────────
--
-- documents.status disait seulement pending / approved / rejected. Un import
-- passe par plus d'étapes que cela, et le parent doit les voir.

do $$
begin
  if not exists (select 1 from pg_type where typname = 'doc_stage') then
    create type doc_stage as enum (
      'importe',      -- le fichier est dans le compartiment
      'en_lecture',   -- OCR et extraction en cours
      'a_valider',    -- le contenu attend le parent
      'publie',       -- visible par l'enfant
      'echec'
    );
  end if;
end
$$;

alter table documents add column if not exists stage doc_stage not null default 'importe';
alter table documents add column if not exists stage_error text;
