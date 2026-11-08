-- La manche se joue en séries.
--
-- La règle du sans-faute ne change pas d'un iota : chaque question doit tomber
-- juste. C'est la DISTANCE sur laquelle on l'exige qui change.
--
-- Les quarante premières manches ont mesuré le problème. Les leçons récentes
-- font 25 à 32 questions ; 12 manches ont été gagnées, 28 ratées, dont NEUF
-- par une seule faute. De ces chiffres on déduit la justesse par question :
-- si 28 questions passent sans faute 3 fois sur 10, chaque question tombe
-- juste à 96 %. L'enfant sait sa leçon — c'est la longueur qui l'écrase.
--
--   10 questions à 96 %  →  65 % de sans-faute
--   20 questions         →  42 %
--   30 questions         →  27 %
--   40 questions         →  18 %
--
-- Un enfant à 96 % échouait donc 7 fois sur 10, et chaque échec lui coûtait
-- 30 questions avant de recommencer les 30 mêmes : environ 93 questions pour
-- valider une leçon.
--
-- La leçon se découpe donc en séries d'une dizaine de questions, sur les
-- frontières de notions — une notion n'est jamais coupée en deux. Chaque
-- série se joue sans faute. Une série gagnée reste gagnée, et se reperd par
-- la même règle qu'avant : une faute postérieure sur une de ses notions. La
-- leçon est validée quand toutes les séries sont tenues. Coût moyen : une
-- quarantaine de questions, et il ne rejoue jamais que la série manquée.
--
-- D'où cette colonne : le journal doit dire ce que la série COUVRAIT, sinon
-- rien ne se déduit. Une ligne réussie sans savoir sur quoi ne vaut rien.
--
-- Le tableau vide a un sens, et c'est celui des lignes déjà écrites : « toute
-- la leçon ». Les manches d'avant portaient bien toutes les questions, donc
-- elles tiennent toutes les séries — ce qui est exactement vrai, et non une
-- indulgence. Rien n'est à réécrire.
alter table manches
  add column if not exists notions uuid[] not null default '{}';

comment on column manches.notions is
  'Les notions couvertes par la série jouée. Tableau vide = toute la leçon, '
  'ce qui est le cas des manches d''avant le découpage en séries.';
