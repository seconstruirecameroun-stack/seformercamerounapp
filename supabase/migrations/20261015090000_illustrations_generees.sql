-- Se Former Cameroun — illustrations des cours importés
--
-- L'extraction produit déjà le résumé et les notions. Elle produit maintenant
-- aussi, pour chacune, une consigne d'illustration : la phrase à donner au
-- générateur d'images pour obtenir une vignette dans le style de la maison.
--
-- Le parent reste maître de l'étape : il génère, il regarde, il dépose. Une
-- image ratée ou hors sujet ne doit pas arriver à l'enfant par automatisme.

alter table lessons add column if not exists illustration_prompt text;
alter table notions add column if not exists illustration_prompt text;

-- ───────────────────────── stockage des images ─────────────────────────
--
-- Compartiment distinct de « cours » et, contrairement à lui, en lecture
-- publique. Deux raisons : ces images sont des dessins générés, sans donnée
-- personnelle, et une URL publique se met en cache par le navigateur comme
-- par un service worker. Les photos de cahier, elles, restent privées.
--
-- L'écriture reste réservée au propriétaire : le premier segment du chemin
-- est l'identifiant du parent, comme pour les cours.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'illustrations',
  'illustrations',
  true,
  2097152, -- 2 Mo : largement au-dessus des 30 ko d'une vignette WebP
  array['image/webp', 'image/png', 'image/jpeg']
)
on conflict (id) do update
  set public = excluded.public,
      file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

create policy "illustrations_depot_proprietaire"
  on storage.objects for insert to authenticated
  with check (
    bucket_id = 'illustrations' and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "illustrations_remplacement_proprietaire"
  on storage.objects for update to authenticated
  using (bucket_id = 'illustrations' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'illustrations' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "illustrations_suppression_proprietaire"
  on storage.objects for delete to authenticated
  using (bucket_id = 'illustrations' and (storage.foldername(name))[1] = auth.uid()::text);
