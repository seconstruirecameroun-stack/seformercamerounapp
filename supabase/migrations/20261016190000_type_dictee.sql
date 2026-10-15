-- Se Former Cameroun — la dictée entre dans les types de questions.
--
-- Le navigateur sait parler sans réseau ni coût, et les deux emplois du
-- temps de l'école réservent des créneaux à la dictée.
--
-- ALTER TYPE ... ADD VALUE doit être validé avant d'être utilisé : cette
-- migration ne fait que cela, les questions viennent dans la suivante.

alter type item_kind add value if not exists 'dictee';
