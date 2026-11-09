-- Se Former Cameroun — annoter un schéma.
--
-- La révision du 9 novembre 2026 demande deux fois le même geste : « Annote
-- l-appareil reproducteur ci-dessous » et « Annote le schéma ci-dessous »,
-- avec des numéros posés sur le dessin et une liste à compléter en face.
-- C-est la forme la plus fréquente des épreuves de sciences de sa classe,
-- et aucun type de question ne savait la poser. On pouvait lui demander ce
-- que fait le réservoir ; on ne pouvait pas lui faire RECONNAÎTRE le
-- réservoir sur le dessin.
--
-- Le diagramme de Venn ne convenait pas : il calcule des régions de
-- cercles, et une lampe à pétrole n-a pas de région. Ici les repères sont
-- DESSINÉS dans la figure, numérotés à la source, et la question ne porte
-- que les noms à mettre en face.
--
-- ALTER TYPE ... ADD VALUE doit être validé avant d-être utilisé : cette
-- migration ne fait que cela, les questions viennent après.

alter type item_kind add value if not exists 'annotation';
