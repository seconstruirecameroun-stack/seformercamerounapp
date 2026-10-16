-- La planification du rappel du soir.
--
-- Séparée de la migration précédente parce qu'elle dépend de deux valeurs qui
-- n'ont pas leur place dans un dépôt : l'adresse de la fonction et le secret
-- partagé. Le secret a été produit dans le navigateur, sur la page des
-- secrets Supabase, et n'est passé ni par un fichier ni par une conversation.
--
-- Rejouer cette migration sur un nouveau projet demande donc de remplacer les
-- deux valeurs ci-dessous avant de l'exécuter.

create extension if not exists pg_cron;
create extension if not exists pg_net;

insert into app_config (cle, valeur) values
  ('rappel_url', 'https://VOTRE-PROJET.supabase.co/functions/v1/rappel-du-soir'),
  ('rappel_secret', 'LE-MEME-QUE-LE-SECRET-RAPPEL_SECRET-DE-LA-FONCTION')
on conflict (cle) do update set valeur = excluded.valeur;

-- Reprogrammer sans se soucier de l'existant : un travail déjà posé est
-- retiré d'abord, et son absence n'est pas une erreur.
do $$ begin perform cron.unschedule('rappel-du-soir'); exception when others then null; end $$;

-- 17 h UTC, soit 18 h à Douala : l'école est finie, le dîner n'a pas commencé,
-- et il reste assez de soirée pour une leçon de cinq minutes.
select cron.schedule('rappel-du-soir', '0 17 * * *', $$select rappels_du_soir();$$);
