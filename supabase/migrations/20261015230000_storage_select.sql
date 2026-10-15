-- Se Former Cameroun — réparation du dépôt de fichiers
--
-- Les dépôts échouaient sur « new row violates row-level security policy »,
-- pour « illustrations » comme pour « films ».
--
-- La cause n'était ni le service de stockage, ni la clé, ni le jeton : les
-- politiques d'insertion étaient bonnes et leur condition s'évaluait à vrai.
-- Il manquait une politique de LECTURE.
--
-- L'API de stockage relit la ligne qu'elle vient d'écrire. Une insertion avec
-- RETURNING exige, en PostgreSQL, de satisfaire aussi la politique SELECT.
-- Sans elle, l'insertion est refusée — avec le message d'une violation de
-- politique d'insertion, ce qui envoie chercher au mauvais endroit.
--
-- Vérifié : la même insertion passe sans RETURNING et échoue avec.
--
-- Le compartiment « cours » avait sa politique de lecture dès l'origine ; les
-- deux autres l'ont été oubliées en chemin.

create policy "illustrations_lecture_proprietaire"
  on storage.objects for select to authenticated
  using (bucket_id = 'illustrations' and (storage.foldername(name))[1] = auth.uid()::text);

create policy "films_lecture_proprietaire"
  on storage.objects for select to authenticated
  using (bucket_id = 'films' and (storage.foldername(name))[1] = auth.uid()::text);

-- La ligne laissée par le test de diagnostic est retirée par l'API de
-- stockage, et non ici : un garde-fou de Supabase interdit la suppression
-- directe dans storage.objects.
