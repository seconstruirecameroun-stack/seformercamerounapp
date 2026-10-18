-- Se Former Cameroun — les trois leçons de sciences du cahier de KLEIN (CE1)
--
-- Transcrites depuis trois photos : la reproduction des animaux (lundi
-- 12 octobre 2026), les soins aux animaux domestiques (vendredi 16 octobre
-- 2026), et les milieux de vie des végétaux (page sans date).
--
-- Rien n'est ajouté au cahier. Les mots, les listes et les exemples sont ceux
-- des pages. Les corrections sont orthographiques : accents rétablis,
-- « gresson » lu cresson, « hibzous » lu hibiscus, et « qui idorent leurs
-- œufs » lu « qui incubent leurs œufs ».
--
-- Les trois pages portent des en-têtes différents — Sciences de la vie,
-- Activités agro-pastorales, Éducation à l'environnement — mais relèvent de
-- la même matière au programme de CE1 : Sciences et technologies. L'en-tête
-- du cahier devient le chapitre.
--
-- Chaque notion a ses quatre étapes : Découverte, Entraînement, Maîtrise et
-- Défi. Une étape sans question serait infranchissable, et la leçon
-- resterait bloquée pour toujours.
--
-- Les leçons naissent en 'approved' : elles ont été relues par le parent qui
-- les a photographiées, au moment de les fournir.
--
-- Réexécutable : la fonction ne s'applique qu'une fois.

create or replace function public.seed_sciences_klein(p_parent uuid)
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

  -- La matière existe déjà : le référentiel de l'école la crée pour le CE1.
  -- On la retrouve par son libellé et sa classe plutôt que de la recréer, pour
  -- ne pas éparpiller les leçons dans deux dossiers du même nom.
  select id into v_subject from subjects
   where parent_id = p_parent and label = 'Sciences et technologies'
     and (class_id = v_class or class_id is null)
   order by class_id nulls last
   limit 1;
  if v_subject is null then
    insert into subjects (parent_id, class_id, label, color)
    values (p_parent, v_class, 'Sciences et technologies', '#d08a3c')
    returning id into v_subject;
  end if;

  -- La reproduction des animaux (Sciences de la vie)
  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, taught_on,
     sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'La reproduction des animaux',
    'Il y a trois modes de reproduction chez les animaux. Les ovipares pondent des œufs. Les vivipares donnent directement naissance aux petits. Les ovovivipares gardent leurs œufs dans le ventre avant de donner naissance.',
    'fr', 'Sciences de la vie', date '2026-10-12', 7, 'approved', 'rp-reproduction',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A hen beside her eggs on the left, a goat with her kid in the middle, and a coiled snake on the right, on a soft plain background, calm and friendly.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'Il y a trois modes de reproduction chez les animaux : ovipare, vivipare et ovovivipare.', 1, 'approved', 'rp-trois',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Three simple rounded panels side by side on a plain background: a clutch of eggs, a mother animal with her baby, and a snake with a soft glow at its belly.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Les animaux ne font pas tous leurs petits de la même façon. Il y a trois façons.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme aller à l’école : à pied, en voiture ou à moto. Trois chemins, une seule arrivée.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Combien y a-t-il de modes de reproduction ?", "options": ["Trois", "Deux", "Cinq"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le cahier en compte trois.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Un mode de reproduction cité est…", "options": ["ovipare", "carnivore", "herbivore"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Ovipare, vivipare, ovovivipare.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel n’est pas un mode de reproduction ?", "options": ["Le mode herbivore", "Le mode ovipare", "Le mode vivipare", "Le mode ovovivipare"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Herbivore dit ce que l’animal mange, pas comment il fait ses petits.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets les trois modes dans l’ordre du cahier.", "tokens": ["ovipare", "vivipare", "ovovivipare"], "consigne": "Touche les mots dans l’ordre."}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Ovipare, vivipare, puis ovovivipare.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Il y a {{1}} modes de reproduction chez les {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["trois", "animaux"]}'::jsonb, 'Trois modes, chez les animaux.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Tous les animaux se reproduisent de la même façon."}'::jsonb,
     '{"value": false}'::jsonb, 'Non : il y a trois modes.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Les ovipares se reproduisent en pondant des œufs : la poule, les poissons, l’escargot.', 2, 'approved', 'rp-ovipare',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A hen sitting beside a small nest of eggs, with a fish and a snail nearby, plain soft background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Un ovipare pond des œufs. Le petit grandit dans l’œuf, puis il sort.', 'approved'),
    (p_parent, v_notion, 'visuel', 'Pense à la poule du quartier : elle pond, elle couve, et les poussins sortent.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Les ovipares se reproduisent en…", "options": ["pondant des œufs", "donnant naissance", "changeant de peau"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Ovipare veut dire qui pond des œufs.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "La poule est un animal…", "options": ["ovipare", "vivipare", "ovovivipare"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La poule pond des œufs.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Lequel de ces animaux est ovipare ?", "options": ["Le poisson", "La vache", "La chèvre", "La chatte"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le poisson pond des œufs.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "Les ovipares pondent des œufs.", "langue": "fr"}'::jsonb,
     '{"phrase": "Les ovipares pondent des œufs."}'::jsonb, 'Ovipare : qui pond des œufs.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Un canard pond des œufs. Il est donc…", "options": ["ovipare", "vivipare", "ovovivipare"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Il pond : il est ovipare.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Les vivipares donnent directement naissance aux petits : la chèvre, la vache, la chatte.', 3, 'approved', 'rp-vivipare',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A goat standing beside her kid, a cow with her calf behind, soft plain background, gentle warm light.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Un vivipare met son petit au monde tout formé. Il n’y a pas d’œuf à casser.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme la chatte de la maison : ses chatons naissent déjà vivants.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Les vivipares donnent…", "options": ["directement naissance aux petits", "des œufs", "seulement du lait"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le petit naît déjà formé.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "La vache est un animal…", "options": ["vivipare", "ovipare", "ovovivipare"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La vache met bas un veau.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Clique sur un animal vivipare.", "images": ["rp-vivipare", "rp-ovipare", "rp-ovovivipare", "rp-trois"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La chèvre et son petit.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Les {{1}} donnent directement naissance aux {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["vivipares", "petits"]}'::jsonb, 'Vivipares : naissance directe.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "La chatte pond des œufs."}'::jsonb,
     '{"value": false}'::jsonb, 'Non : elle est vivipare.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Les ovovivipares gardent leurs œufs dans le ventre avant de donner naissance : la vipère.', 4, 'approved', 'rp-ovovivipare',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A coiled snake on warm sand with a soft glow showing small eggs inside her body, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'L’œuf reste dans le ventre de la mère. Le petit en sort déjà vivant.', 'approved'),
    (p_parent, v_notion, 'pas_a_pas', 'La mère fabrique un œuf, elle le garde en elle, l’œuf s’ouvre dedans, le petit naît.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Où l’ovovivipare garde-t-il ses œufs ?", "options": ["Dans son ventre", "Dans un nid", "Dans l’eau"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Les œufs restent dans le ventre.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "La vipère est un animal…", "options": ["ovovivipare", "ovipare", "vivipare"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est l’exemple du cahier.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie chaque animal à son mode.", "gauche": ["La poule", "La vache", "La vipère"], "droite": ["Ovipare", "Vivipare", "Ovovivipare"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Pond, met bas, garde ses œufs en elle.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "La vipère est ovovivipare.", "langue": "fr"}'::jsonb,
     '{"phrase": "La vipère est ovovivipare."}'::jsonb, 'Un seul mot à bien écrire.', 'approved'),
    (p_parent, v_notion, 'qcm', 4,
     '{"question": "Il garde ses œufs dans le ventre puis met bas. Il est…", "options": ["ovovivipare", "ovipare", "vivipare"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Les deux à la fois : œuf dedans, petit vivant.', 'approved');

  -- Les soins aux animaux domestiques (Activités agro-pastorales)
  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, taught_on,
     sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'Les soins aux animaux domestiques',
    'Les animaux peuvent être atteints de maladies : les maladies de la peau, la grippe, la rage, les infections pulmonaires, l’insuffisance rénale, la peste, les vers et la newcastle. Pour les éviter, il faut les vacciner, nettoyer leur habitat et les conduire chez un vétérinaire.',
    'fr', 'Activités agro-pastorales', date '2026-10-16', 8, 'approved', 'sa-soins',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A calm farmyard with a goat, a hen and a dog, a clean water trough and a swept shelter, warm morning light.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'Les maladies de la peau de l’animal sont la gale et la teigne.', 1, 'approved', 'sa-gale',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A close friendly view of a goat with a few dull patches on its coat, a soft brush and a bowl of clean water beside it.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'La gale et la teigne abîment la peau et le poil de l’animal.', 'approved'),
    (p_parent, v_notion, 'visuel', 'On les voit : le poil tombe par plaques et la peau devient rugueuse.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "La gale est une maladie…", "options": ["de la peau", "des poumons", "des yeux"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La gale touche la peau.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quelle maladie touche la peau ?", "options": ["La teigne", "La grippe", "La peste"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La teigne est une maladie de la peau.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quelles sont les deux maladies de la peau ?", "options": ["La gale et la teigne", "La toux et la bave", "La peste et les vers", "La rage et la grippe"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le cahier en cite deux.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Les maladies de la peau sont la {{1}} et la {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["gale", "teigne"]}'::jsonb, 'Gale et teigne.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "La gale se voit sur la peau de l’animal."}'::jsonb,
     '{"value": true}'::jsonb, 'Oui : c’est une maladie de la peau.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'La grippe de l’animal se reconnaît à la toux, à la bave et à la fatigue.', 2, 'approved', 'sa-grippe',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A hen resting with drooping wings beside a bowl of water, a soft blanket of warm light, plain background.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Un animal grippé tousse, bave et n’a plus de force.', 'approved'),
    (p_parent, v_notion, 'analogie', 'C’est comme toi quand tu es grippé : tu tousses et tu es fatigué.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quel signe montre la grippe ?", "options": ["La toux", "La peau rouge", "Les cornes"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La toux est un signe de la grippe.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "La grippe donne à l’animal…", "options": ["de la fatigue", "de la force", "de la joie"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Elle fatigue l’animal.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quels sont les trois signes de la grippe ?", "options": ["Toux, bave, fatigue", "Toux, cornes, poils", "Bave, dents, queue", "Fatigue, plumes, lait"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Toux, bave et fatigue.', 'approved'),
    (p_parent, v_notion, 'chronologie', 3,
     '{"question": "Remets la phrase dans le bon ordre.", "tokens": ["La grippe", "se reconnaît", "à la toux", "et à la bave"], "consigne": "Touche les mots dans l’ordre de la phrase."}'::jsonb,
     '{"order": [0, 1, 2, 3]}'::jsonb, 'La grippe se reconnaît à la toux et à la bave.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Un animal qui tousse et qui bave peut avoir la grippe."}'::jsonb,
     '{"value": true}'::jsonb, 'Ce sont deux des trois signes.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'La rage se reconnaît à une sécrétion excessive de salive et à l’agressivité.', 3, 'approved', 'sa-rage',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A dog standing alone behind a low fence, mouth wet, a small warning distance kept by a calm empty foreground.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Un animal enragé bave beaucoup et devient méchant. On ne s’en approche pas.', 'approved'),
    (p_parent, v_notion, 'histoire', 'Quand un chien du quartier bave et grogne sans raison, on prévient un adulte.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "La rage rend l’animal…", "options": ["agressif", "calme", "joyeux"]}'::jsonb,
     '{"index": 0}'::jsonb, 'L’agressivité est un signe de la rage.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quel liquide coule beaucoup avec la rage ?", "options": ["La salive", "Le lait", "L’eau"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Une sécrétion excessive de salive.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Quels sont les deux signes de la rage ?", "options": ["Beaucoup de salive et l’agressivité", "La toux et la bave", "La gale et la teigne", "Les vers et la peste"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Salive et agressivité.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "La rage rend l’animal agressif.", "langue": "fr"}'::jsonb,
     '{"phrase": "La rage rend l’animal agressif."}'::jsonb, 'Agressif prend deux s.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Un chien qui bave beaucoup et grogne peut avoir la rage."}'::jsonb,
     '{"value": true}'::jsonb, 'Ce sont les deux signes du cahier.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'L’animal peut aussi avoir une infection pulmonaire, une insuffisance rénale, la peste, les vers ou la newcastle.', 4, 'approved', 'sa-autres',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Four small rounded cards on a plain background: a pair of lungs, a kidney, a lying hen, and a small worm shape, all soft and friendly.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'D’autres maladies touchent les poumons, les reins, ou viennent des vers.', 'approved'),
    (p_parent, v_notion, 'visuel', 'L’insuffisance rénale fatigue l’animal et lui donne la diarrhée.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "L’infection pulmonaire touche…", "options": ["les poumons", "la peau", "les dents"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Pulmonaire vient de poumon.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Laquelle est une maladie de l’animal ?", "options": ["La newcastle", "La propreté", "La gentillesse"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La newcastle est dans la liste du cahier.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "L’insuffisance rénale donne…", "options": ["de la fatigue et la diarrhée", "de la toux", "des taches sur la peau", "beaucoup de salive"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Fatigue et diarrhée.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "L’animal peut avoir la {{1}}, les vers ou la {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["peste", "newcastle"]}'::jsonb, 'La peste et la newcastle.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "La newcastle est une maladie des animaux."}'::jsonb,
     '{"value": true}'::jsonb, 'Elle est citée dans le cahier.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'relation', 'Pour éviter ces maladies, il faut vacciner les animaux, nettoyer leur habitat et les conduire chez un vétérinaire.', 5, 'approved', 'sa-prevention',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A clean swept animal shelter with fresh straw, a bucket of clean water, and a small medical bag resting on a stool.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'On vaccine, on nettoie, et on va voir le vétérinaire. Trois gestes.', 'approved'),
    (p_parent, v_notion, 'pas_a_pas', 'D’abord vacciner, ensuite nettoyer l’habitat, et si l’animal est malade, le vétérinaire.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Que faut-il faire pour éviter les maladies ?", "options": ["Vacciner les animaux", "Les laisser seuls", "Les faire courir"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le vaccin protège.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Chez qui conduit-on un animal malade ?", "options": ["Chez un vétérinaire", "Chez le boulanger", "Chez le tailleur"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le vétérinaire soigne les animaux.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie chaque geste à ce qui va avec.", "gauche": ["Vacciner", "Nettoyer", "Conduire"], "droite": ["Le vaccin", "L’habitat", "Le vétérinaire"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Trois gestes, trois mots.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Il faut {{1}} les animaux et nettoyer leur {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["vacciner", "habitat"]}'::jsonb, 'Vacciner et nettoyer.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Un habitat sale protège les animaux des maladies."}'::jsonb,
     '{"value": false}'::jsonb, 'Au contraire : il faut le nettoyer.', 'approved');

  -- Les milieux de vie des végétaux (Éducation à l’environnement)
  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, taught_on,
     sort_order, status, illustration, illustration_prompt)
  values (p_parent, v_subject, v_class, 'Les milieux de vie des végétaux',
    'Les végétaux sont des êtres vivants qui ont des racines. Certains poussent sur la terre, d’autres poussent dans l’eau, et d’autres encore poussent dans la boue.',
    'fr', 'Éducation à l’environnement', null, 9, 'approved', 'mv-milieux',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. One wide calm scene: a mango tree on dry red earth on the left, water lilies on a pond in the middle, and mangrove roots in dark mud on the right.')
  returning id into v_lesson;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'definition', 'Les végétaux sont des êtres vivants qui ont des racines.', 1, 'approved', 'mv-vegetaux',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A small plant shown whole on a plain background, with its roots visible below the soil line, soft and clear.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Un végétal est vivant : il grandit, il boit, il a des racines.', 'approved'),
    (p_parent, v_notion, 'visuel', 'Les racines sont la partie cachée, sous la terre ou sous l’eau.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Les végétaux sont des êtres…", "options": ["vivants", "morts", "en pierre"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Ils sont vivants.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Qu’ont tous les végétaux ?", "options": ["Des racines", "Des ailes", "Des dents"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Tous ont des racines.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Les végétaux ont tous…", "options": ["des racines", "des plumes", "des pattes", "des écailles"]}'::jsonb,
     '{"index": 0}'::jsonb, 'C’est ce qui les définit dans le cahier.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "Les végétaux sont des êtres vivants.", "langue": "fr"}'::jsonb,
     '{"phrase": "Les végétaux sont des êtres vivants."}'::jsonb, 'Végétaux prend un accent.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Une pierre est un végétal."}'::jsonb,
     '{"value": false}'::jsonb, 'Une pierre n’est pas vivante.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'Certains végétaux poussent sur la terre : le manguier, le palmier, l’hibiscus.', 2, 'approved', 'mv-terrestre',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A mango tree and an oil palm growing on red laterite earth, a hibiscus flower in front, dry warm light.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Ceux-là poussent sur la terre ferme. On dit qu’ils sont terrestres.', 'approved'),
    (p_parent, v_notion, 'visuel', 'Le manguier de la cour est un végétal terrestre.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le manguier pousse…", "options": ["sur la terre", "dans l’eau", "dans la boue"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le manguier est terrestre.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Un végétal terrestre est…", "options": ["le palmier", "le nénuphar", "le palétuvier"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le palmier pousse sur la terre.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Clique sur un végétal qui pousse sur la terre.", "images": ["mv-terrestre", "mv-aquatique", "mv-marecage", "mv-vegetaux"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le manguier et le palmier.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le {{1}} et le palmier poussent sur la {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["manguier", "terre"]}'::jsonb, 'Manguier, palmier : la terre.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Un arbre planté dans la cour est un végétal terrestre."}'::jsonb,
     '{"value": true}'::jsonb, 'Il pousse sur la terre.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'D’autres poussent dans l’eau : le roseau, le nénuphar, l’algue, le cresson.', 3, 'approved', 'mv-aquatique',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. A calm pond with water lilies floating, tall reeds at the edge and green algae under the clear water.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Ceux-là poussent dans l’eau. On dit qu’ils sont aquatiques.', 'approved'),
    (p_parent, v_notion, 'analogie', 'Le nénuphar est posé sur l’eau comme une assiette verte.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le nénuphar pousse…", "options": ["dans l’eau", "sur la terre", "dans la boue"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le nénuphar est aquatique.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Un végétal aquatique est…", "options": ["l’algue", "le manguier", "le raphia"]}'::jsonb,
     '{"index": 0}'::jsonb, 'L’algue pousse dans l’eau.', 'approved'),
    (p_parent, v_notion, 'association', 2,
     '{"question": "Relie chaque végétal à son milieu.", "gauche": ["Le manguier", "Le nénuphar", "Le palétuvier"], "droite": ["La terre", "L’eau", "La boue"]}'::jsonb,
     '{"order": [0, 1, 2]}'::jsonb, 'Terre, eau, boue.', 'approved'),
    (p_parent, v_notion, 'dictee', 3,
     '{"phrase": "Le nénuphar pousse dans l’eau.", "langue": "fr"}'::jsonb,
     '{"phrase": "Le nénuphar pousse dans l’eau."}'::jsonb, 'Nénuphar prend deux accents.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Le roseau est un végétal aquatique."}'::jsonb,
     '{"value": true}'::jsonb, 'Il pousse dans l’eau.', 'approved');

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status,
     illustration, illustration_prompt)
  values (p_parent, v_lesson, 'liste', 'D’autres poussent dans la boue : le papyrus, le raphia, le palétuvier.', 4, 'approved', 'mv-marecage',
    'Pastel flat 2D children illustration, soft gradient background, sand, mint and lilac palette, no black outlines, rounded friendly shapes, gentle shading, no text, no letters, no numbers, no watermark, no real person, no brand. Mangrove trees with arching stilt roots in dark shining mud, tall papyrus stems behind, soft humid light.')
  returning id into v_notion;

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, v_notion, 'simple', 'Ceux-là poussent dans la boue d’un marécage.', 'approved'),
    (p_parent, v_notion, 'visuel', 'Le palétuvier tient debout sur des racines en arceaux, les pieds dans la boue.', 'approved');

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Le palétuvier pousse…", "options": ["dans la boue", "sur un rocher", "dans le sable sec"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le palétuvier pousse dans la boue.', 'approved'),
    (p_parent, v_notion, 'qcm', 1,
     '{"question": "Quel végétal pousse dans la boue ?", "options": ["Le raphia", "Le manguier", "L’algue"]}'::jsonb,
     '{"index": 0}'::jsonb, 'Le raphia pousse dans la boue.', 'approved'),
    (p_parent, v_notion, 'qcm', 2,
     '{"question": "Les végétaux de la boue poussent dans…", "options": ["un marécage", "un désert", "une maison", "une rivière rapide"]}'::jsonb,
     '{"index": 0}'::jsonb, 'La boue, c’est le marécage.', 'approved'),
    (p_parent, v_notion, 'texte_a_trous', 3,
     '{"text": "Le {{1}} et le raphia poussent dans la {{2}}.", "blanks": 2}'::jsonb,
     '{"values": ["papyrus", "boue"]}'::jsonb, 'Papyrus, raphia, palétuvier.', 'approved'),
    (p_parent, v_notion, 'vrai_faux', 4,
     '{"statement": "Le palétuvier pousse dans un marécage."}'::jsonb,
     '{"value": true}'::jsonb, 'Le marécage, c’est la boue.', 'approved');

  return 1;
end;
$$;

select public.seed_sciences_klein(parent_id)
  from children
 where first_name = 'KLEIN'
   and not exists (select 1 from lessons where title = 'La reproduction des animaux')
 limit 1;
