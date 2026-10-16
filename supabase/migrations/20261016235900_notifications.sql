-- Les rappels du soir.
--
-- Un enfant de sept ans ne pense pas à ouvrir une app de révision. Ce qui le
-- ramène, c'est quelque chose qui vient le chercher — une seule fois par
-- jour, le soir, et jamais s'il a déjà joué.
--
-- Trois partis pris :
--
-- 1. Un abonnement par couple (appareil, enfant). Les deux frères partagent
--    souvent le même téléphone : chacun doit recevoir son propre message,
--    avec son prénom et ses propres faits.
--
-- 2. Le SQL ne calcule que des faits bruts — la dernière journée jouée, les
--    questions réussies de la semaine. Les phrases, elles, vivent dans la
--    fonction d'envoi. Réécrire ici la règle des étapes ou celle de la série
--    produirait deux vérités qui divergeraient au premier changement.
--
-- 3. Aucune clé d'administration nulle part : pg_cron tourne dans la base,
--    sélectionne lui-même les destinataires, et n'envoie à la fonction que
--    ce qu'elle doit signer.

create table push_subscriptions (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  child_id   uuid not null references children (id) on delete cascade,
  -- L'adresse que le navigateur donne au service de push du constructeur.
  endpoint   text not null,
  p256dh     text not null,
  auth       text not null,
  appareil   text,
  created_at timestamptz not null default now(),
  -- Un envoi refusé par le service de push signale un abonnement mort.
  echecs     int not null default 0,
  unique (endpoint, child_id)
);

create index push_subscriptions_child_idx on push_subscriptions (child_id);

alter table push_subscriptions enable row level security;

create policy "parent lit ses abonnements" on push_subscriptions
  for select using (parent_id = auth.uid());
create policy "parent ajoute ses abonnements" on push_subscriptions
  for insert with check (parent_id = auth.uid());
create policy "parent supprime ses abonnements" on push_subscriptions
  for delete using (parent_id = auth.uid());

-- ───────────────────────── la configuration du rappel ─────────────────────────

-- Volontairement sans la moindre politique : PostgREST refuse donc tout accès
-- depuis l'extérieur, et seuls les travaux planifiés, qui tournent dans la
-- base, peuvent la lire.
create table app_config (
  cle    text primary key,
  valeur text not null
);

alter table app_config enable row level security;

-- ───────────────────────── le travail du soir ─────────────────────────

create or replace function rappels_du_soir()
returns int
language plpgsql
security definer
set search_path = public, extensions, net
as $$
declare
  charge   jsonb;
  secret   text;
  adresse  text;
  -- Le Cameroun vit à UTC+1 : la journée d'un enfant se compte là-bas, pas
  -- à Greenwich. Sans ce décalage, une leçon jouée à 23 h compterait pour
  -- le lendemain et la série sauterait.
  aujourdhui date := (now() at time zone 'Africa/Douala')::date;
  lundi      date := aujourdhui - ((extract(isodow from aujourdhui)::int) - 1);
begin
  select valeur into secret from app_config where cle = 'rappel_secret';
  select valeur into adresse from app_config where cle = 'rappel_url';
  if secret is null or adresse is null then
    return 0;
  end if;

  with jours as (
    select child_id, max((created_at at time zone 'Africa/Douala')::date) as dernier
    from attempts
    group by child_id
  ),
  semaine as (
    select child_id, count(*) as reussites
    from attempts
    where correct
      and (created_at at time zone 'Africa/Douala')::date >= lundi
    group by child_id
  )
  select jsonb_agg(
    jsonb_build_object(
      'endpoint', s.endpoint,
      'p256dh', s.p256dh,
      'auth', s.auth,
      'childId', c.id,
      'prenom', c.first_name,
      'dernierJour', j.dernier,
      'reussitesSemaine', coalesce(sem.reussites, 0),
      'meilleurRival', (
        select coalesce(max(sem2.reussites), 0)
        from children c2
        left join semaine sem2 on sem2.child_id = c2.id
        where c2.parent_id = c.parent_id and c2.id <> c.id
      ),
      'prenomRival', (
        select c2.first_name
        from children c2
        left join semaine sem2 on sem2.child_id = c2.id
        where c2.parent_id = c.parent_id and c2.id <> c.id
        order by coalesce(sem2.reussites, 0) desc
        limit 1
      )
    )
  )
  into charge
  from push_subscriptions s
  join children c on c.id = s.child_id
  left join jours j on j.child_id = c.id
  left join semaine sem on sem.child_id = c.id
  -- Rien pour qui a déjà joué aujourd'hui : un rappel qui arrive après
  -- l'effort apprend à l'enfant que le rappel ne veut rien dire.
  where s.echecs < 5
    and (j.dernier is null or j.dernier < aujourdhui);

  if charge is null then
    return 0;
  end if;

  perform net.http_post(
    url := adresse,
    body := jsonb_build_object('rappels', charge),
    headers := jsonb_build_object('Content-Type', 'application/json', 'x-rappel-secret', secret)
  );

  return jsonb_array_length(charge);
end;
$$;

revoke all on function rappels_du_soir() from public, anon, authenticated;
