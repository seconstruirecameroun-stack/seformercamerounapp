-- La manche de validation.
--
-- Franchir les quatre étapes fait avancer ; valider la leçon certifie. Ce ne
-- sont pas les mêmes exigences, et jusqu'ici l'app n'en connaissait qu'une.
--
-- Une leçon n'est validée que par une manche sans faute, portant sur TOUTES
-- ses questions — vingt pour « Le cube », qui a quatre notions à cinq
-- questions. C'est volontairement dur : une leçon sue ne se récite pas à huit
-- sur dix.
--
-- Cette table ne porte pas l'état « validée ». Elle journalise les manches
-- jouées, et l'état s'en déduit, comme l'étape courante se déduit déjà des
-- tentatives. La raison est la même : une colonne d'état tenue à la main finit
-- par mentir, et celle-ci devrait être corrigée à chaque erreur en révision.
--
--   validée  = il existe une manche réussie, et aucune réponse fausse sur une
--              notion de la leçon depuis.
--   perdue   = il en existe une, mais une notion a été ratée après.
--
-- notions_ratees sert la reprise : quand l'enfant revient le lendemain, l'app
-- doit pouvoir lui redonner ce qu'il a raté, et non les vingt questions.

create table if not exists manches (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  child_id   uuid not null references children (id) on delete cascade,
  lesson_id  uuid not null references lessons (id) on delete cascade,
  -- Le compte de la manche, tel qu'il a été joué. Les questions d'une leçon
  -- peuvent changer ensuite ; ce qui a été réussi ce jour-là, non.
  questions  int  not null check (questions > 0),
  justes     int  not null check (justes >= 0),
  reussie    boolean not null,
  notions_ratees uuid[] not null default '{}',
  created_at timestamptz not null default now(),
  -- Une manche réussie est une manche sans faute. La base le vérifie, parce
  -- que c'est toute la règle : une ligne reussie avec justes < questions
  -- validerait une leçon qui ne l'est pas.
  constraint manches_sans_faute check (reussie = (justes = questions))
);

create index if not exists manches_enfant_lecon_idx
  on manches (child_id, lesson_id, created_at desc);

alter table manches enable row level security;

do $$
begin
  if not exists (select 1 from pg_policies where tablename = 'manches'
                 and policyname = 'parent lit ses manches') then
    create policy "parent lit ses manches" on manches
      for select using (parent_id = auth.uid());
  end if;
  if not exists (select 1 from pg_policies where tablename = 'manches'
                 and policyname = 'parent ajoute ses manches') then
    create policy "parent ajoute ses manches" on manches
      for insert with check (parent_id = auth.uid());
  end if;
end $$;

-- Rien n'est jamais modifié ni supprimé : c'est un journal. Une manche perdue
-- le reste, et le rapport du parent doit pouvoir dire « il l'avait sue le 18 ».
