-- Se Former Cameroun — la composition.
--
-- Au Cameroun, la composition est l-épreuve de fin de séquence : le maître
-- annonce les leçons, et l-enfant compose dessus. L-app savait faire
-- réviser une leçon et la valider ; elle ne savait pas faire COMPOSER sur
-- plusieurs leçons à la fois, ce qui est pourtant la forme que prend
-- l-évaluation à l-école.
--
-- CE QUI EST STOCKÉ, ET CE QUI NE L-EST PAS. La composition est une
-- INTENTION DU PARENT : ces leçons-là, ce nombre de questions-là. Cela ne
-- se déduit de rien et doit donc être écrit. Les réponses de l-enfant, en
-- revanche, ne sont pas recopiées ici : elles vont dans `attempts` comme
-- toutes les autres, parce que le père a choisi qu-une composition compte
-- comme une révision - étoiles, étapes, images, et la validation qui se
-- perd si une leçon validée est ratée. Le détail de la copie se relit donc
-- dans le journal, entre `commencee_le` et `finie_le`.
--
-- `justes` est la seule exception : le compte final est écrit ici, parce
-- qu-une composition ne se joue qu-une fois et que la note est ce que le
-- parent viendra lire. La déduire à chaque affichage reviendrait à relire
-- tout le journal pour un nombre qui ne bougera plus.

create table if not exists compositions (
  id uuid primary key default gen_random_uuid(),
  parent_id uuid not null references auth.users (id) on delete cascade,
  child_id uuid not null references children (id) on delete cascade,
  titre text not null,
  -- Les leçons annoncées, dans l-ordre où le parent les a cochées.
  lessons uuid[] not null,
  -- Les questions tirées, dans l-ordre où elles seront posées. Figées à la
  -- création : une composition qui changerait de questions entre deux
  -- ouvertures ne serait plus une épreuve.
  questions uuid[] not null,
  commencee_le timestamptz,
  finie_le timestamptz,
  justes integer,
  created_at timestamptz not null default now(),
  constraint composition_non_vide check (array_length(questions, 1) > 0)
);

create index if not exists compositions_enfant on compositions (child_id, created_at desc);

alter table compositions enable row level security;

-- La même règle que partout : le parent ne voit et ne touche que ses lignes.
drop policy if exists "compositions du parent" on compositions;
create policy "compositions du parent" on compositions
  for all using (parent_id = auth.uid()) with check (parent_id = auth.uid());
