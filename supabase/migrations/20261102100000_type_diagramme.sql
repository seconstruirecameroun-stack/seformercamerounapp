-- Se Former Cameroun — placer les éléments dans un diagramme.
--
-- Le cahier de BRAYNE demande « Draw a venn diagram and represent sets A, B
-- and C ». Aucun type de question ne savait le faire : on pouvait lui
-- demander OÙ va le 15, pas le lui faire poser. Or c-est précisément le
-- geste de l-exercice, et celui qu-il rate.
--
-- Le type reste général : un énoncé, des ensembles nommés, des étiquettes à
-- ranger dans les régions. Un diagramme de Venn aujourd-hui, un tableau à
-- double entrée demain si besoin — la forme du payload ne nomme nulle part
-- les cercles.
--
-- ALTER TYPE ... ADD VALUE doit être validé avant d-être utilisé : cette
-- migration ne fait que cela, les questions viennent après.

alter type item_kind add value if not exists 'diagramme';
