-- Se Former Cameroun — stockage des films de leçon
--
-- Les films précédents vivaient sur un CDN extérieur, hérité de la chaîne de
-- production. Ils rejoignent le projet : une leçon et son film doivent
-- survivre ensemble, sans dépendre d'un hébergement de passage.
--
-- Lecture publique, comme les illustrations : ce sont des films pédagogiques
-- sans donnée personnelle, et une URL publique se met en cache. L'écriture
-- reste réservée au propriétaire du dossier.

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'films',
  'films',
  true,
  104857600, -- 100 Mo : une minute de 720p pèse quelques méga-octets
  array['video/mp4', 'video/webm']
)
on conflict (id) do update
  set public = excluded.public,
      file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

create policy "films_depot_proprietaire"
  on storage.objects for insert to authenticated
  with check (bucket_id = 'films' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "films_remplacement_proprietaire"
  on storage.objects for update to authenticated
  using (bucket_id = 'films' and (storage.foldername(name))[1] = auth.uid()::text)
  with check (bucket_id = 'films' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "films_suppression_proprietaire"
  on storage.objects for delete to authenticated
  using (bucket_id = 'films' and (storage.foldername(name))[1] = auth.uid()::text);
