-- Se Former Cameroun — les six leçons du cahier de KLEIN (CE1)
--
-- Transcrites depuis six photos du cahier, du mardi 13 au jeudi 15 octobre
-- 2026. La fonction d'extraction n'étant pas encore déployée, la
-- transcription et la structuration sont faites à la main, dans le format
-- exact qu'elle produira.
--
-- Rien n'est ajouté au cahier : les mots, les listes et les chiffres sont
-- ceux des pages. Les corrections sont orthographiques et grammaticales
-- (« Une enfant obéissant » → « Un enfant obéissant », accents rétablis), et
-- la dernière phrase de l'obéissance, laissée en suspens, est rétablie au
-- plus près de ce qui est écrit.
--
-- KLEIN est en CE1, pas en CM1 : questions plus courtes, mots plus simples,
-- jamais plus de deux mots à écrire. Chaque notion a ses trois étapes.
--
-- Six matières nouvelles naissent ici, nommées comme le cahier les nomme :
-- Éducation morale, Droits et devoirs, Éducation civique, Technologies,
-- Éducation à la paix, Géographie.
--
-- Les leçons naissent en 'approved' : elles ont été relues par le parent qui
-- les a photographiées, au moment de les fournir.

create or replace function public.seed_lecons_klein(p_parent uuid)
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
begin
  select id into v_class from classes where subsystem = 'francophone' and code = 'CE1';

  -- ─────────────────────────────────────────────────────────────
  -- Éducation morale — L’obéissance
  -- ─────────────────────────────────────────────────────────────
  insert into subjects (parent_id, label, color) values (p_parent, 'Éducation morale', '#c2708f')
  on conflict (parent_id, label) do update set color = excluded.color
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'L’obéissance',
    'L’obéissance, c’est exécuter les ordres et les consignes d’un aîné sans discuter. Un enfant obéissant est aimé de tout le monde. Si nous voulons réussir dans la vie, obéissons.',
    'fr', 'Éducation morale', 1, 'approved', 'ob-ecoute',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A child listening attentively to a kind adult who is pointing at a tidy room, both smiling, warm morning light.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'L’obéissance est le fait d’exécuter les ordres et les consignes d’un aîné sans discuter.', 1, 'approved', 'ob-consigne',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A grown-up hand gently pointing the way and a small child nodding, simple scene, plain soft background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Obéir, c’est faire ce qu’un aîné demande, tout de suite et sans discuter.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme au football : quand l’arbitre siffle, on s’arrête sans discuter.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Obéir, c’est…", "options": ["faire ce qu’un aîné demande", "discuter longtemps", "partir en courant"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Obéir, c’est faire ce qu’on demande.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quand un aîné donne une consigne, j’obéis…", "options": ["sans discuter", "en discutant", "demain"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Sans discuter.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Qui donne les consignes que l’on doit suivre ?", "options": ["Un aîné", "Un bébé", "Un chat", "Personne"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Un aîné : un plus grand que nous.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Que fait un enfant obéissant ?", "options": ["Il exécute les ordres sans discuter", "Il refuse les ordres", "Il discute chaque consigne", "Il fait semblant d’écouter"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il exécute sans discuter.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "L’obéissance, c’est exécuter les ordres d’un {{1}} sans {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["aîné", "discuter"]}'::jsonb, 'D’un aîné, sans discuter.', 'approved'),
    (p_parent, v_notion, 'qcm', 3,
     '{"question": "Ton grand frère te demande de ranger. Que fais-tu ?", "options": ["Je range tout de suite", "Je discute longtemps", "Je fais autre chose", "Je me cache"]}'::jsonb,
     '{"index": 0}'::jsonb, 'On exécute la consigne d’un aîné.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Un enfant obéissant est aimé de tout le monde.', 2, 'approved', 'ob-aime',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A smiling child surrounded by three happy family members, soft hearts floating, plain soft background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Quand tu obéis, les autres sont contents de toi et t’aiment.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Un enfant obéissant est…", "options": ["aimé de tout le monde", "grondé tous les jours", "oublié"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il est aimé de tout le monde.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Qui aime un enfant obéissant ?", "options": ["Tout le monde", "Personne", "Les animaux seulement"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Tout le monde.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Pourquoi aime-t-on un enfant obéissant ?", "options": ["Il fait ce qu’on lui demande", "Il crie très fort", "Il court très vite", "Il mange beaucoup"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Parce qu’il fait ce qu’on lui demande.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Un enfant obéissant est {{1}} de tout le monde.", "blanks": 1}'::jsonb,
     '{"values": ["aimé"]}'::jsonb, 'Aimé de tout le monde.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Si nous voulons réussir dans la vie, obéissons.', 3, 'approved', 'ob-reussir',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A child climbing three soft steps towards a glowing star, simple and encouraging, plain soft background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Obéir aujourd’hui aide à réussir plus tard.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Pour réussir dans la vie, il faut…", "options": ["obéir", "désobéir", "dormir toute la journée"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il faut obéir.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Que nous apporte l’obéissance ?", "options": ["Elle nous aide à réussir dans la vie", "Elle fait perdre du temps", "Elle fâche les aînés", "Elle rend triste"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Elle aide à réussir.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Si nous voulons {{1}} dans la vie, obéissons.", "blanks": 1}'::jsonb,
     '{"values": ["réussir"]}'::jsonb, 'Réussir.', 'approved');

  -- ─────────────────────────────────────────────────────────────
  -- Droits et devoirs — Le droit à l’identité
  -- ─────────────────────────────────────────────────────────────
  insert into subjects (parent_id, label, color) values (p_parent, 'Droits et devoirs', '#5b8ac2')
  on conflict (parent_id, label) do update set color = excluded.color
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'Le droit à l’identité',
    'Chaque enfant a droit à une identité. L’identité lui confère un nom et une nationalité.',
    'fr', 'Droits et devoirs', 2, 'approved', 'id-identite',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A friendly open booklet with a child portrait drawn on it and a small flag beside, plain soft background.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Chaque enfant a droit à une identité.', 1, 'approved', 'id-enfant',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Three children of different looks standing side by side, each with a soft glowing badge on the chest, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Tous les enfants, sans exception, ont droit à une identité.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme une étiquette sur ton cartable : elle dit que ce cartable est à toi.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Qui a droit à une identité ?", "options": ["Chaque enfant", "Seulement les grands", "Personne"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Chaque enfant.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Avoir une identité, c’est un…", "options": ["droit", "jeu", "cadeau de fête"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est un droit.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "L’identité est…", "options": ["un droit de chaque enfant", "un cadeau d’anniversaire", "une punition", "un jouet"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Un droit, pour chaque enfant.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Chaque enfant a droit à une {{1}}.", "blanks": 1}'::jsonb,
     '{"values": ["identité"]}'::jsonb, 'Une identité.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'L’identité confère un nom et une nationalité.', 2, 'approved', 'id-nom-nation',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A name card next to a small waving flag, joined by a soft ribbon, plain soft background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Ton identité te donne deux choses : un nom et une nationalité.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’identité donne un nom et une…", "options": ["nationalité", "voiture", "maison"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Un nom et une nationalité.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Mon nom fait partie de…", "options": ["mon identité", "mon école", "mon jeu"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le nom fait partie de l’identité.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Que confère l’identité ?", "options": ["Un nom et une nationalité", "Un nom et une maison", "Une nationalité et un vélo", "Un âge et une taille"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Un nom et une nationalité.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Être camerounais, c’est quelle partie de l’identité ?", "options": ["La nationalité", "Le nom", "L’âge", "La taille"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est la nationalité.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "L’identité confère un {{1}} et une {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["nom", "nationalité"]}'::jsonb, 'Un nom et une nationalité.', 'approved');

  -- ─────────────────────────────────────────────────────────────
  -- Éducation civique — L’intégration nationale
  -- ─────────────────────────────────────────────────────────────
  insert into subjects (parent_id, label, color) values (p_parent, 'Éducation civique', '#3f9d8f')
  on conflict (parent_id, label) do update set color = excluded.color
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'L’intégration nationale',
    'L’intégration nationale est un mélange des cultures et des traditions au sein d’une population. Au Cameroun, plus de 250 ethnies vivent dans la paix et l’harmonie, à travers les mariages interethniques, la cohabitation des peuples et les affectations des travailleurs.',
    'fr', 'Éducation civique', 3, 'approved', 'in-cameroun',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A joyful crowd of children in varied traditional clothes holding hands in a wide circle, plain soft background.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'L’intégration nationale est un mélange des cultures et des traditions au sein d’une population.', 1, 'approved', 'in-melange',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Several coloured ribbons braiding together into one wide ribbon, plain soft background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'C’est quand des cultures et des traditions différentes se mélangent dans un même pays.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme un plat de famille : chacun apporte un ingrédient, et on mange ensemble.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’intégration nationale, c’est un mélange de…", "options": ["cultures et de traditions", "voitures", "animaux"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Des cultures et des traditions.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’intégration nationale concerne…", "options": ["une population", "une seule famille", "un seul enfant"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Toute une population.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Qu’est-ce que l’intégration nationale ?", "options": ["Le mélange des cultures et des traditions d’une population", "Un jeu d’équipe", "Un voyage à l’étranger", "Une fête d’école"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Un mélange des cultures et des traditions.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "L’intégration nationale est un mélange des {{1}} et des {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["cultures", "traditions"]}'::jsonb, 'Des cultures et des traditions.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Au Cameroun, plus de 250 ethnies vivent dans la paix et l’harmonie.', 2, 'approved', 'in-ethnies',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A soft map shape of a country filled with many small coloured houses living side by side, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Le Cameroun compte plus de 250 ethnies, et elles vivent en paix.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Au Cameroun, il y a plus de…", "options": ["250 ethnies", "2 ethnies", "10 ethnies"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Plus de 250 ethnies.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Au Cameroun, les ethnies vivent dans…", "options": ["la paix", "la dispute", "la peur"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Dans la paix et l’harmonie.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Combien d’ethnies compte le Cameroun ?", "options": ["Plus de 250", "Moins de 10", "Exactement 50", "Une seule"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Plus de 250.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Au Cameroun, plus de {{1}} ethnies vivent dans la paix.", "blanks": 1}'::jsonb,
     '{"values": ["250"]}'::jsonb, 'Plus de 250.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'L’intégration nationale se fait à travers les mariages interethniques, la cohabitation des peuples et les affectations des travailleurs.', 3, 'approved', 'in-moyens',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Three simple pictures side by side: two hands with wedding rings, two neighbouring houses, and a travelling bag with a bus, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Trois choses rapprochent les peuples : les mariages entre ethnies, le fait de vivre côte à côte, et les travailleurs envoyés dans d’autres régions.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quand deux personnes de deux ethnies se marient, cela aide…", "options": ["l’intégration nationale", "la dispute", "personne"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est un mariage interethnique.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Vivre côte à côte avec d’autres peuples, c’est la…", "options": ["cohabitation", "séparation", "dispute"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est la cohabitation.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel n’aide PAS l’intégration nationale ?", "options": ["Refuser les autres ethnies", "Les mariages interethniques", "La cohabitation des peuples", "Les affectations des travailleurs"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Refuser les autres sépare au lieu de rassembler.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets les trois moyens dans l’ordre du cahier.", "tokens": ["Les mariages interethniques", "La cohabitation des peuples", "Les affectations des travailleurs"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Mariages, cohabitation, affectations.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "La {{1}} des peuples aide l’intégration nationale.", "blanks": 1}'::jsonb,
     '{"values": ["cohabitation"]}'::jsonb, 'La cohabitation.', 'approved');

  -- ─────────────────────────────────────────────────────────────
  -- Technologies — Les techniques de filtrage de l’eau
  -- ─────────────────────────────────────────────────────────────
  insert into subjects (parent_id, label, color) values (p_parent, 'Technologies', '#d08a3c')
  on conflict (parent_id, label) do update set color = excluded.color
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'Les techniques de filtrage de l’eau',
    'On peut réaliser un filtre à eau avec une demi-bouteille, du sable, du coton, du charbon et du gravier. L’eau non potable entre par le haut, traverse le gravier, le charbon, le sable puis le coton, et l’eau potable sort en bas.',
    'fr', 'Technologies', 4, 'approved', 'fi-filtre',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A half plastic bottle turned upside down as a water filter, layers of gravel, charcoal, sand and cotton, a clean drop falling into a glass below, plain background.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'On peut réaliser un filtre à eau avec une demi-bouteille, du sable, du coton, du charbon et du gravier.', 1, 'approved', 'fi-materiel',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Five small piles side by side: a half bottle, sand, cotton, charcoal and gravel, neatly arranged, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Le matériel : une demi-bouteille, du sable, du coton, du charbon et du gravier.', 'approved'),
    (p_parent, v_notion, 'pas_a_pas', 'On coupe la bouteille, on la retourne, puis on met le coton, le sable, le charbon et le gravier.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Pour faire un filtre, on utilise une…", "options": ["demi-bouteille", "assiette", "cuillère"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Une demi-bouteille.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Lequel sert à filtrer l’eau ?", "options": ["Le sable", "Le sucre", "Le savon"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le sable fait partie du filtre.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quels matériaux met-on dans le filtre ?", "options": ["Du gravier, du charbon, du sable et du coton", "Du sucre, du sel et de l’huile", "Du papier et de la colle", "Des feuilles et des cailloux peints"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Gravier, charbon, sable et coton.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "On fabrique le filtre avec une demi-{{1}}, du sable, du coton, du charbon et du {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["bouteille", "gravier"]}'::jsonb, 'Une demi-bouteille et du gravier.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'Dans le filtre, l’eau traverse le gravier, le charbon, le sable puis le coton.', 2, 'approved', 'fi-couches',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A cut-away view of four stacked layers in a bottle, from top to bottom gravel, charcoal, sand, cotton, with a blue arrow going down, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'De haut en bas : gravier, charbon, sable, coton.', 'approved'),
    (p_parent, v_notion, 'visuel', 'Le gravier arrête les gros morceaux, le coton retient les plus petites saletés.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Dans le filtre, l’eau passe d’abord par…", "options": ["le gravier", "le coton", "la bouteille vide"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le gravier est en haut.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Que traverse l’eau en dernier ?", "options": ["Le coton", "Le gravier", "Le charbon"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le coton est tout en bas.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Dans quel ordre l’eau traverse-t-elle le filtre ?", "options": ["Gravier, charbon, sable, coton", "Coton, sable, charbon, gravier", "Sable, gravier, coton, charbon", "Charbon, coton, gravier, sable"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Gravier, charbon, sable, coton.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets les couches du filtre, du haut vers le bas.", "tokens": ["Gravier", "Charbon", "Sable", "Coton"]}'::jsonb,
     '{"order": [0, 1, 2, 3]}'::jsonb, 'Gravier, charbon, sable, coton.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'L’eau non potable entre dans le filtre et l’eau potable en sort.', 3, 'approved', 'fi-eau-potable',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. On the left a glass of cloudy water, on the right a glass of clear water, an arrow between them, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'L’eau sale entre en haut, l’eau propre sort en bas.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’eau qui entre dans le filtre est…", "options": ["non potable", "potable", "sucrée"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Elle est non potable : on ne peut pas la boire.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’eau qui sort du filtre est…", "options": ["potable", "plus sale", "brûlante"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Elle est potable.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "À quoi sert un filtre à eau ?", "options": ["À rendre l’eau potable", "À chauffer l’eau", "À colorer l’eau", "À geler l’eau"]}'::jsonb,
     '{"index": 0}'::jsonb, 'À rendre l’eau potable.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "L’eau non potable entre dans le filtre et l’eau {{1}} en sort.", "blanks": 1}'::jsonb,
     '{"values": ["potable"]}'::jsonb, 'L’eau potable.', 'approved');

  -- ─────────────────────────────────────────────────────────────
  -- Éducation à la paix — La paix
  -- ─────────────────────────────────────────────────────────────
  insert into subjects (parent_id, label, color) values (p_parent, 'Éducation à la paix', '#7a76c4')
  on conflict (parent_id, label) do update set color = excluded.color
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'La paix',
    'Pour maintenir la paix, je pratique le vivre-ensemble au village ou en ville, en acceptant les autres, en étant tolérant, en les assistant et en collaborant avec eux.',
    'fr', 'Éducation à la paix', 5, 'approved', 'pa-village',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Neighbours of a small village helping each other carry baskets under a calm sky, dove flying above, plain background.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Pour maintenir la paix, je pratique le vivre-ensemble au village ou en ville.', 1, 'approved', 'pa-ensemble',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Two small houses, one rural and one in town, joined by a path with children walking together, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'La paix se construit là où l’on vit : au village comme en ville.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Pour maintenir la paix, je pratique le…", "options": ["vivre-ensemble", "chacun pour soi", "silence toute la journée"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le vivre-ensemble.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Où pratique-t-on le vivre-ensemble ?", "options": ["Au village ou en ville", "Seulement à l’école", "Nulle part"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Au village ou en ville.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Que faut-il faire pour maintenir la paix ?", "options": ["Pratiquer le vivre-ensemble", "Se disputer", "Rester tout seul", "Crier plus fort"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Pratiquer le vivre-ensemble.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Pour maintenir la {{1}}, je pratique le vivre-{{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["paix", "ensemble"]}'::jsonb, 'La paix, le vivre-ensemble.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'Le vivre-ensemble, c’est accepter les autres, être tolérant, les assister et collaborer avec eux.', 2, 'approved', 'pa-mains',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Four hands of different skin tones joining together over a soft circle, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Quatre gestes : accepter, tolérer, assister, collaborer.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme porter une table à plusieurs : si un seul lâche, tout tombe.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Vivre ensemble, c’est d’abord…", "options": ["accepter les autres", "refuser les autres", "ignorer les autres"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Accepter les autres.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Aider quelqu’un, c’est l’…", "options": ["assister", "oublier", "éviter"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est l’assister.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel ne fait PAS partie du vivre-ensemble ?", "options": ["Refuser les autres", "Être tolérant", "Assister les autres", "Collaborer avec eux"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Refuser les autres éloigne de la paix.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets les trois façons de vivre ensemble, dans l’ordre du cahier.", "tokens": ["Être tolérant", "Assister les autres", "Collaborer avec eux"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Tolérer, assister, collaborer.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Je vis en paix en étant {{1}} avec les autres.", "blanks": 1}'::jsonb,
     '{"values": ["tolérant"]}'::jsonb, 'En étant tolérant.', 'approved');

  -- ─────────────────────────────────────────────────────────────
  -- Géographie — Le sol
  -- ─────────────────────────────────────────────────────────────
  insert into subjects (parent_id, label, color) values (p_parent, 'Géographie', '#6f9a3f')
  on conflict (parent_id, label) do update set color = excluded.color
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'Le sol',
    'Le sol est la partie superficielle de la terre. Il diffère en fonction de sa structure : sablonneux, ferralitique, basaltique ou argileux.',
    'fr', 'Géographie', 6, 'approved', 'so-terre',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A gentle cut-away of the ground showing a thin top layer with grass and a small plant, plain soft background.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Le sol est la partie superficielle de la terre.', 1, 'approved', 'so-coupe',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A simple slice of ground with the very top layer highlighted in a warm colour, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Le sol, c’est la couche du dessus, celle sur laquelle on marche.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme la peau de la terre : fine, mais c’est là que tout pousse.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Où se trouve le sol ?", "options": ["À la surface de la terre", "Au centre de la Terre", "Dans le ciel"]}'::jsonb,
     '{"index": 0}'::jsonb, 'À la surface : c’est la partie superficielle.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le sol est la partie… de la terre", "options": ["superficielle", "profonde", "invisible"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Superficielle veut dire « du dessus ».', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Qu’est-ce que le sol ?", "options": ["La partie superficielle de la terre", "Le ciel au-dessus de nous", "L’eau de la rivière", "Le centre de la Terre"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La partie superficielle de la terre.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le sol est la partie {{1}} de la terre.", "blanks": 1}'::jsonb,
     '{"values": ["superficielle"]}'::jsonb, 'Superficielle.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Le sol diffère en fonction de sa structure.', 2, 'approved', 'so-structures',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Four small jars of earth of different colours and grain sizes lined up, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Tous les sols ne se ressemblent pas : cela dépend de leur structure.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Tous les sols sont-ils pareils ?", "options": ["Non, ils sont différents", "Oui, tous pareils"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Ils diffèrent selon leur structure.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Qu’est-ce qui fait la différence entre les sols ?", "options": ["Leur structure", "Leur prix", "Leur nom", "Leur âge"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Leur structure.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le sol diffère en fonction de sa {{1}}.", "blanks": 1}'::jsonb,
     '{"values": ["structure"]}'::jsonb, 'Sa structure.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Le sol sablonneux est fait de grains de roche.', 3, 'approved', 'so-sablonneux',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A close view of pale sandy soil with visible grains, a small shell shape, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Sablonneux : il est fait de grains de roche, comme du sable.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le sol sablonneux est fait de…", "options": ["grains de roche", "eau", "fer"]}'::jsonb,
     '{"index": 0}'::jsonb, 'De grains de roche.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quel sol est fait de grains de roche ?", "options": ["Le sol sablonneux", "Le sol argileux", "Le sol basaltique", "Le sol ferralitique"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le sol sablonneux.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le sol {{1}} est fait de grains de roche.", "blanks": 1}'::jsonb,
     '{"values": ["sablonneux"]}'::jsonb, 'Sablonneux.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Le sol ferralitique est rouge et riche en fer.', 4, 'approved', 'so-ferralitique',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A close view of deep red earth with a small iron-coloured pebble, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Ferralitique : il est rouge parce qu’il contient beaucoup de fer.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le sol ferralitique est de quelle couleur ?", "options": ["Rouge", "Noir", "Blanc"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il est rouge.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Pourquoi le sol ferralitique est-il rouge ?", "options": ["Il est riche en fer", "Il est riche en eau", "Il a été brûlé", "Il a été peint"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Parce qu’il est riche en fer.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le sol ferralitique est rouge et riche en {{1}}.", "blanks": 1}'::jsonb,
     '{"values": ["fer"]}'::jsonb, 'En fer.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Le sol basaltique est noir et fertile.', 5, 'approved', 'so-basaltique',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A close view of dark black earth with a healthy green sprout growing, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Basaltique : il est noir, et les plantes y poussent bien.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le sol basaltique est…", "options": ["noir", "rouge", "jaune"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il est noir.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quel sol est noir et fertile ?", "options": ["Le basaltique", "L’argileux", "Le sablonneux", "Le ferralitique"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le basaltique.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le sol basaltique est {{1}} et fertile.", "blanks": 1}'::jsonb,
     '{"values": ["noir"]}'::jsonb, 'Noir.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Le sol argileux est mou et pas fertile.', 6, 'approved', 'so-argileux',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A close view of soft grey clay earth, a finger print pressed into it, no plant, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Argileux : il est mou, et les plantes y poussent mal.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le sol argileux est…", "options": ["mou", "dur comme la pierre", "brûlant"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il est mou.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quel sol n’est pas fertile ?", "options": ["L’argileux", "Le basaltique", "Le ferralitique", "Aucun"]}'::jsonb,
     '{"index": 0}'::jsonb, 'L’argileux n’est pas fertile.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le sol argileux est mou et pas {{1}}.", "blanks": 1}'::jsonb,
     '{"values": ["fertile"]}'::jsonb, 'Pas fertile.', 'approved');

  return 1;
end;
$$;

-- Rattache les leçons à la famille déjà présente, une seule fois.
select public.seed_lecons_klein(parent_id)
  from children
 where first_name = 'KLEIN'
   and not exists (select 1 from lessons where title = 'Le sol')
 limit 1;
