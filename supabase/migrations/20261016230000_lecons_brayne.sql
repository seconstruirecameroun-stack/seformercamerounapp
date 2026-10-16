-- Se Former Cameroun — les deux leçons du cahier de BRAYNE (CM1)
--
--   Géographie physique — Les bassins hydrographiques du Cameroun (16 oct.)
--   Géographie          — Les activités de l'homme au village et en ville (15 oct.)
--
-- Transcrites depuis quatre photos. Les noms de fleuves et de villes sont
-- ceux du cahier, pas ceux d'un atlas : si l'enfant a écrit « Berbérati »,
-- c'est « Berbérati » qu'il doit retrouver dans ses révisions.
--
-- Trois passages restent douteux sur les photos — l'encre rouge passe sur le
-- bleu — et ils sont écartés plutôt que devinés : le troisième affluent de
-- la Bénoué, le troisième affluent de la Sanaga, et le nom de la ville
-- arrosée par la Sangha, lu « Berbérati » sans certitude.
--
-- Les deux leçons rejoignent la matière « Histoire-Géographie » du CM1,
-- celle de l'emploi du temps. Le chapitre garde l'intitulé du cahier, et la
-- date celle écrite en haut de la page.

create or replace function public.seed_lecons_brayne(p_parent uuid)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  v_class   uuid;
  v_subject uuid;
  v_lesson  uuid;
  v_notion  uuid;
  n         integer := 0;
begin
  select id into v_class from classes where subsystem = 'francophone' and code = 'CM1';
  select id into v_subject from subjects
   where parent_id = p_parent and class_id = v_class and label = 'Histoire-Géographie';


  -- ───────────────────────── Les bassins hydrographiques du Cameroun ─────────────────────────
  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, taught_on,
     sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'Les bassins hydrographiques du Cameroun',
    'L’hydrographie est l’ensemble des cours d’eau d’une région. Un bassin hydrographique est une région arrosée par un fleuve principal et ses affluents. Le Cameroun compte quatre bassins : le Tchad, le Niger, l’Atlantique et le Congo.',
    'fr', 'Géographie physique', date '2026-10-16', 3, 'approved', 'bh-bassins',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A wide calm river seen from above, winding through green hills, with three smaller streams joining it, soft morning light.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'L’hydrographie est l’ensemble des cours d’eau d’une région.', 1, 'approved', 'bh-hydrographie',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. Several small blue streams running across a green plain, seen from above.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'L’hydrographie, c’est tous les cours d’eau d’une région réunis.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’hydrographie, c’est l’ensemble des…", "options": ["cours d’eau", "montagnes", "routes"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Tous les cours d’eau d’une région.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’hydrographie concerne…", "options": ["une région", "une maison", "une école"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Une région entière.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Que regroupe l’hydrographie d’une région ?", "options": ["Tous ses cours d’eau", "Tous ses villages", "Toutes ses routes", "Tous ses arbres"]}'::jsonb,
     '{"index": 0}'::jsonb, 'L’ensemble des cours d’eau.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "L’hydrographie est l’ensemble des cours d’eau.", "langue": "fr"}'::jsonb,
     '{"phrase": "L’hydrographie est l’ensemble des cours d’eau."}'::jsonb, 'La phrase du cahier.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "L’{{1}} est l’ensemble des cours d’{{2}} d’une région.", "blanks": 2}'::jsonb,
     '{"values": ["hydrographie", "eau"]}'::jsonb, 'Hydrographie, eau.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "L’hydrographie étudie les montagnes."}'::jsonb,
     '{"value": false}'::jsonb, 'Non : les cours d’eau.', 'approved');
  n := n + 6;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Un bassin hydrographique est une région arrosée par un fleuve principal et ses affluents.', 2, 'approved', 'bh-bassin',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A green valley with one big river in the middle and small rivers joining it from the hills.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Un bassin, c’est toute la région qu’un fleuve et ses affluents arrosent.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme un arbre couché : le tronc est le fleuve, les branches sont les affluents.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Un bassin hydrographique est une région…", "options": ["arrosée par un fleuve", "couverte de sable", "sans eau"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Arrosée par un fleuve et ses affluents.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Clique sur un bassin : un fleuve et ses affluents.", "images": ["bh-bassin", "bh-quatre", "bh-hydrographie"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le fleuve et tout ce qu’il arrose.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Qu’est-ce qui arrose un bassin hydrographique ?", "options": ["Un fleuve principal et ses affluents", "La pluie seulement", "Un lac sans rivière", "La mer"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le fleuve principal et ses affluents.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Un bassin", "est arrosé", "par un fleuve", "et ses affluents"], "consigne": "Touche les mots dans l’ordre de la phrase."}'::jsonb,
     '{"order": [0, 1, 2, 3]}'::jsonb, 'La définition du cahier.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Un bassin hydrographique peut n’avoir aucun cours d’eau."}'::jsonb,
     '{"value": false}'::jsonb, 'Il est arrosé par un fleuve.', 'approved');
  n := n + 5;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Un affluent est un fleuve qui se jette dans un fleuve plus grand que lui pour le grossir.', 3, 'approved', 'bh-affluent',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A narrow river flowing into a much wider river, the two waters meeting.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'L’affluent rejoint un plus grand fleuve et lui apporte son eau.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Un affluent se jette dans…", "options": ["un fleuve plus grand", "la forêt", "un puits"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Dans un fleuve plus grand que lui.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "À quoi sert un affluent ?", "options": ["À grossir un fleuve", "À vider un fleuve", "À arrêter un fleuve"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il apporte son eau.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel est vrai pour un affluent ?", "options": ["Il rejoint un fleuve plus grand", "Il rejoint la mer directement", "Il reste tout seul", "Il coule à l’envers"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il rejoint un plus grand que lui.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Clique sur l’affluent qui rejoint un grand fleuve.", "images": ["bh-affluent", "bh-tchad", "bh-congo"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La petite rivière rejoint la grande.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "Un affluent se jette dans un fleuve plus grand.", "langue": "fr"}'::jsonb,
     '{"phrase": "Un affluent se jette dans un fleuve plus grand."}'::jsonb, 'La phrase du cahier.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Un {{1}} se jette dans un fleuve plus {{2}} que lui.", "blanks": 2}'::jsonb,
     '{"values": ["affluent", "grand"]}'::jsonb, 'Affluent, grand.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Le Faro rejoint la Bénoué. Le Faro est donc…", "options": ["un affluent", "un fleuve principal", "un lac"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il se jette dans plus grand que lui.', 'approved');
  n := n + 7;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'Le Cameroun compte quatre bassins hydrographiques : le Tchad, le Niger, l’Atlantique et le Congo.', 4, 'approved', 'bh-quatre',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. Four separate blue ribbons of water flowing in four different directions on a soft background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Quatre bassins : Tchad, Niger, Atlantique, Congo.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Combien de bassins hydrographiques au Cameroun ?", "options": ["Quatre", "Deux", "Dix"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Quatre.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quels sont les quatre bassins du Cameroun ?", "options": ["Tchad, Niger, Atlantique, Congo", "Tchad, Niger, Nil, Congo", "Niger, Congo, Nil, Zambèze", "Tchad, Atlantique, Sahara, Congo"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Tchad, Niger, Atlantique, Congo.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets les quatre bassins dans l’ordre du cahier.", "tokens": ["Le Tchad", "Le Niger", "L’Atlantique", "Le Congo"]}'::jsonb,
     '{"order": [0, 1, 2, 3]}'::jsonb, 'L’ordre de la leçon.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Le Cameroun compte quatre bassins hydrographiques."}'::jsonb,
     '{"value": true}'::jsonb, 'Oui : Tchad, Niger, Atlantique, Congo.', 'approved');
  n := n + 4;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Le bassin du Tchad a pour fleuve principal le Logone, qui arrose la ville de Maroua.', 5, 'approved', 'bh-tchad',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A river arriving into a wide shallow lake in a dry savannah, acacia trees on the banks.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Le Logone arrose Maroua. Ses affluents : le Chari, la Vina, le Mbéré.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quel est le fleuve principal du bassin du Tchad ?", "options": ["Le Logone", "La Sanaga", "La Sangha"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le Logone.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quelle ville le Logone arrose-t-il ?", "options": ["Maroua", "Garoua", "Édéa", "Douala"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Maroua.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie le bassin du Tchad à ce qui lui appartient.", "gauche": ["Son fleuve principal", "Sa ville", "Un de ses affluents"], "droite": ["Le Logone", "Maroua", "Le Chari"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Logone, Maroua, Chari.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le bassin du Tchad a pour fleuve principal le {{1}}, qui arrose {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["Logone", "Maroua"]}'::jsonb, 'Logone, Maroua.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Tu es à Maroua, au bord du fleuve. Quel bassin ?", "options": ["Le Tchad", "Le Congo", "L’Atlantique"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Maroua est arrosée par le Logone.', 'approved');
  n := n + 5;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Le bassin du Niger a pour fleuve principal la Bénoué, qui arrose la ville de Garoua.', 6, 'approved', 'bh-niger',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A broad river passing beside a small savannah town with low houses and boats on the bank.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'La Bénoué arrose Garoua. Ses affluents : le Faro et le Mayo Kébi.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quel est le fleuve principal du bassin du Niger ?", "options": ["La Bénoué", "Le Logone", "La Sangha"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La Bénoué.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quelle ville la Bénoué arrose-t-elle ?", "options": ["Garoua", "Maroua", "Édéa", "Yaoundé"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Garoua.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie le bassin du Niger à ce qui lui appartient.", "gauche": ["Son fleuve principal", "Sa ville", "Un de ses affluents"], "droite": ["La Bénoué", "Garoua", "Le Faro"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Bénoué, Garoua, Faro.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel est un affluent de la Bénoué ?", "options": ["Le Mayo Kébi", "Le Chari", "Le Dja", "Le Mbam"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le Faro et le Mayo Kébi.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "La Bénoué arrose la ville de Garoua.", "langue": "fr"}'::jsonb,
     '{"phrase": "La Bénoué arrose la ville de Garoua."}'::jsonb, 'La phrase du cahier.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Le Mayo Kébi se jette dans la Bénoué."}'::jsonb,
     '{"value": true}'::jsonb, 'Oui, c’est un de ses affluents.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Un bateau descend la Bénoué depuis Garoua. Quel bassin ?", "options": ["Le Niger", "Le Tchad", "Le Congo"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La Bénoué appartient au bassin du Niger.', 'approved');
  n := n + 7;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Le bassin de l’Atlantique a pour fleuve principal la Sanaga, qui traverse trois régions et arrose la ville d’Édéa.', 7, 'approved', 'bh-atlantique',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A large river widening towards the ocean, palm trees and a waterfall on the way.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'La Sanaga traverse trois régions et arrose Édéa. Ses affluents : le Wouri, le Mbam.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quel est le fleuve principal du bassin de l’Atlantique ?", "options": ["La Sanaga", "Le Logone", "La Bénoué"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La Sanaga.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Combien de régions la Sanaga traverse-t-elle ?", "options": ["Trois", "Une", "Dix", "Deux"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Trois régions.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quelle ville la Sanaga arrose-t-elle ?", "options": ["Édéa", "Garoua", "Maroua", "Bertoua"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Édéa.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "La {{1}} traverse trois régions et arrose la ville d’{{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["Sanaga", "Édéa"]}'::jsonb, 'Sanaga, Édéa.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Un fleuve finit dans l’océan près d’Édéa. Lequel ?", "options": ["La Sanaga", "Le Logone", "La Sangha"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La Sanaga, bassin de l’Atlantique.', 'approved');
  n := n + 5;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Le bassin du Congo a pour fleuve principal la Sangha, qui arrose la ville de Berbérati.', 8, 'approved', 'bh-congo',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A dark calm river flowing through a dense green rainforest, tall trees on both banks.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'La Sangha arrose Berbérati. Ses affluents : la Kadeï, le Dja, la Boumba et le Ngoko.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quel est le fleuve principal du bassin du Congo ?", "options": ["La Sangha", "La Sanaga", "La Bénoué"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La Sangha.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel est un affluent de la Sangha ?", "options": ["Le Dja", "Le Chari", "Le Faro", "Le Mbam"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le Dja, avec la Kadeï, la Boumba et le Ngoko.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie chaque bassin à son fleuve principal.", "gauche": ["Le Tchad", "Le Niger", "L’Atlantique", "Le Congo"], "droite": ["Le Logone", "La Bénoué", "La Sanaga", "La Sangha"]}'::jsonb,
     '{"order": [0, 1, 2, 3]}'::jsonb, 'Les quatre fleuves principaux.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["La Sangha", "est le fleuve", "du bassin", "du Congo"], "consigne": "Touche les mots dans l’ordre de la phrase."}'::jsonb,
     '{"order": [0, 1, 2, 3]}'::jsonb, 'La Sangha, bassin du Congo.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Attention : Sanaga ou Sangha ? Laquelle est dans le bassin du Congo ?", "options": ["La Sangha", "La Sanaga"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La Sangha, au Congo. La Sanaga va à l’Atlantique.', 'approved');
  n := n + 5;


  -- ───────────────────────── Les activités de l’homme au village et en ville ─────────────────────────
  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, taught_on,
     sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'Les activités de l’homme au village et en ville',
    'Au village, les activités de l’homme sont nombreuses et variées : l’artisanat, la pêche, l’élevage, l’agriculture, les danses traditionnelles et la cuisine. En ville, on travaille dans l’administration, le transport, l’industrie, l’éducation, le commerce et la santé, ainsi que dans les petits métiers.',
    'fr', 'Géographie', date '2026-10-15', 4, 'approved', 'av-village-ville',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. On the left a small village with fields and a fisherman, on the right a town with low buildings and a bus, a road joining the two.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'Au village, les activités de l’homme sont l’artisanat, la pêche, l’élevage, l’agriculture, les danses traditionnelles et la cuisine.', 1, 'approved', 'av-village',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A village scene with a potter at work, a fisherman with a net, goats, and a field being hoed.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Au village : artisanat, pêche, élevage, agriculture, danses, cuisine.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Au village, on pratique…", "options": ["la pêche", "l’industrie", "l’administration"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Pêche, artisanat, élevage, agriculture.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Fabriquer un panier à la main, c’est…", "options": ["l’artisanat", "le commerce", "le transport"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est l’artisanat.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Laquelle n’est PAS une activité du village ?", "options": ["L’industrie", "La pêche", "L’élevage", "L’agriculture"]}'::jsonb,
     '{"index": 0}'::jsonb, 'L’industrie est en ville.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie chaque activité du village à son geste.", "gauche": ["L’agriculture", "L’élevage", "La pêche"], "droite": ["Cultiver un champ", "Garder des animaux", "Prendre du poisson"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Trois activités du village.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "Au village, les activités sont nombreuses et variées.", "langue": "fr"}'::jsonb,
     '{"phrase": "Au village, les activités sont nombreuses et variées."}'::jsonb, 'La phrase du cahier.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["Au village", "on pratique", "l’artisanat", "et la pêche"], "consigne": "Touche les mots dans l’ordre de la phrase."}'::jsonb,
     '{"order": [0, 1, 2, 3]}'::jsonb, 'Des activités du village.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Ton oncle garde des chèvres au village. Quelle activité ?", "options": ["L’élevage", "La pêche", "L’artisanat"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Garder des animaux, c’est l’élevage.', 'approved');
  n := n + 7;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'En ville, l’homme travaille dans l’administration, le transport, l’industrie, l’éducation, le commerce et la santé.', 2, 'approved', 'av-ville',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A town street with an office building, a bus, a school, a shop and a small clinic side by side.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'En ville : bureaux, transport, usines, écoles, boutiques, hôpitaux.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "En ville, on travaille dans…", "options": ["l’administration", "la cueillette", "la chasse"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Administration, transport, industrie, éducation, commerce, santé.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quel secteur soigne les malades ?", "options": ["La santé", "Le commerce", "Le transport", "L’industrie"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le secteur de la santé.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie chaque secteur de la ville à son lieu.", "gauche": ["L’éducation", "La santé", "Le commerce"], "droite": ["L’école", "L’hôpital", "Le marché"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Trois secteurs de la ville.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "En ville, on travaille dans l’{{1}}, le transport et l’{{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["administration", "industrie"]}'::jsonb, 'Administration, industrie.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Un chauffeur de bus travaille dans quel secteur ?", "options": ["Le transport", "La santé", "L’éducation"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le transport.', 'approved');
  n := n + 5;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'En ville, on trouve aussi les petits métiers : le call box, les vendeurs ambulants, les gardiens et les ménagères.', 3, 'approved', 'av-petits-metiers',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand, no map, no country outline. A street corner with a small phone booth stand with a parasol, a vendor carrying goods on his head, and a guard at a gate.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Les petits métiers : call box, vendeurs ambulants, gardiens, ménagères.', 'approved'),
    (p_parent, v_notion, 'analogie', 'Ce sont les métiers du trottoir : on les croise tous les jours en allant à l’école.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le call box est…", "options": ["un petit métier", "une usine", "une école"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Un petit métier de la ville.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Clique sur les petits métiers de la ville.", "images": ["av-petits-metiers", "av-village", "av-ville"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Call box, vendeurs ambulants, gardiens.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel est un petit métier ?", "options": ["Le vendeur ambulant", "Le médecin", "L’ingénieur", "Le professeur"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le vendeur ambulant.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "Le call box est un petit métier de la ville.", "langue": "fr"}'::jsonb,
     '{"phrase": "Le call box est un petit métier de la ville."}'::jsonb, 'La phrase du cahier.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Le gardien fait partie des petits métiers."}'::jsonb,
     '{"value": true}'::jsonb, 'Oui, comme le call box.', 'approved');
  n := n + 5;

  return n;
end;
$$;

select public.seed_lecons_brayne(parent_id)
  from children
 where first_name = 'BRAYNE'
   and not exists (select 1 from lessons where title = 'Les bassins hydrographiques du Cameroun')
 limit 1;
