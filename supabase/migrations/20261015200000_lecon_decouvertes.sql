-- Se Former Cameroun — leçon « Les grandes inventions et les grandes découvertes »
--
-- Premier vrai cours importé, transcrit depuis trois photos du cahier
-- (mardi 13 octobre 2026). La fonction d'extraction n'étant pas encore
-- déployée, la transcription et la structuration sont faites à la main, mais
-- elles suivent exactement le format que cette fonction produira : un résumé
-- court, des notions typées d'une phrase, des explications d'une ligne, des
-- items par niveau, et une consigne d'image par notion.
--
-- Rien n'est ajouté au cahier. Les dates, les noms et l'orthographe des
-- périodes sont ceux de la page. Les seules corrections sont typographiques
-- (accents, majuscules des noms propres).
--
-- La leçon naît en 'approved' : elle a été relue par le parent qui l'a
-- photographiée, ici au moment de la fournir.

create or replace function public.seed_grandes_decouvertes(p_parent uuid)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  v_class   uuid;
  v_subject uuid;
  v_lesson  uuid;
  n_def     uuid;
  n_papier  uuid;
  n_bouss   uuid;
  n_gouv    uuid;
  n_carav   uuid;
  n_impr    uuid;
  n_cause   uuid;
  n_dias    uuid;
  n_colomb  uuid;
  n_gama    uuid;
  n_magel   uuid;
begin
  select id into v_class from classes where subsystem = 'francophone' and code = 'CM1';

  insert into subjects (parent_id, label, color)
  values (p_parent, 'Histoire', '#d66d4d')
  on conflict (parent_id, label) do update set label = excluded.label
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status,
     illustration, illustration_prompt)
  values (
    p_parent, v_subject, v_class,
    'Les grandes inventions et les grandes découvertes',
    'Une invention crée un objet ou une technique qui n’existait pas. Les Chinois inventent '
    || 'le papier, la poudre, la boussole et le gouvernail. Les Européens ajoutent la caravelle '
    || 'et l’imprimerie. Ces inventions permettent les grandes découvertes.',
    'fr', 'Les grandes découvertes', 2, 'approved',
    'gd-caravelle-mer',
    'Pastel flat 2D children illustration, soft gradient sky, sand, mint and lilac palette, '
    || 'no black outlines, rounded friendly shapes, gentle shading, no text, no letters, '
    || 'no numbers, no watermark, no real person, no brand. A small wooden caravel sailing on '
    || 'a calm sea at sunrise, seen from the shore, with a rolled map and a compass on the sand.'
  )
  returning id into v_lesson;

  -- ───────────────────────────── notions ─────────────────────────────

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'definition',
     'Une invention est la création d’un objet ou d’une technique qui n’existait pas avant.',
     1, 'approved', 'gd-invention',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A glowing light bulb above an open wooden toolbox on a plain soft background.')
  returning id into n_def;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Les Chinois inventent le papier et la poudre à canon au 1ᵉʳ siècle.',
     2, 'approved', 'gd-papier-poudre',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A rolled sheet of paper next to a small clay jar of dark powder with a tiny spark, plain soft background.')
  returning id into n_papier;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Les Chinois inventent la boussole au VIIᵉ siècle.',
     3, 'approved', 'gd-boussole',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A round brass compass with a red needle, centred on a plain soft background.')
  returning id into n_bouss;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Les Chinois inventent le gouvernail au XIIᵉ siècle.',
     4, 'approved', 'gd-gouvernail',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A wooden ship rudder and tiller at the back of a boat, plain soft background.')
  returning id into n_gouv;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Les Portugais inventent la caravelle en 1440.',
     5, 'approved', 'gd-caravelle',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A small wooden caravel ship with three triangular sails, centred on a plain soft background.')
  returning id into n_carav;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'L’Allemand Gutenberg invente l’imprimerie en 1450.',
     6, 'approved', 'gd-imprimerie',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A wooden printing press with a stack of blank printed sheets, plain soft background.')
  returning id into n_impr;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'relation',
     'Ces inventions ont favorisé la navigation et les grands voyages à travers le monde.',
     7, 'approved', 'gd-navigation',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A compass, a rolled map and a small sailing ship arranged together, plain soft background.')
  returning id into n_cause;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Bartholomeu Dias atteint le cap de Bonne-Espérance en 1487.',
     8, 'approved', 'gd-cap',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A rocky green cape at the southern tip of a coast with waves meeting around it, plain soft background.')
  returning id into n_dias;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Christophe Colomb découvre l’Amérique en 1492.',
     9, 'approved', 'gd-amerique',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. Three small caravel ships arriving near a green tropical shore, plain soft background.')
  returning id into n_colomb;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Vasco de Gama trouve la route des Indes en 1498.',
     10, 'approved', 'gd-indes',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A sailing ship beside baskets of colourful spices and a rolled sea route map, plain soft background.')
  returning id into n_gama;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status, illustration, illustration_prompt) values
    (p_parent, v_lesson, 'date',
     'Magellan et son équipage font le premier tour du monde de 1519 à 1522.',
     11, 'approved', 'gd-tour-du-monde',
     'Pastel flat 2D children illustration, no black outlines, no text, no letters, no numbers. A round globe encircled by a dotted ribbon path with a tiny ship on it, plain soft background.')
  returning id into n_magel;

  -- ─────────────────────────── explications ───────────────────────────

  insert into explanations (parent_id, notion_id, register, body, status) values
    (p_parent, n_def, 'simple',    'Inventer, c’est faire une chose qui n’existait pas.', 'approved'),
    (p_parent, n_def, 'analogie',  'Comme fabriquer un jouet que personne n’avait jamais vu.', 'approved'),

    (p_parent, n_papier, 'simple', 'Deux inventions chinoises très anciennes : le papier et la poudre.', 'approved'),
    (p_parent, n_papier, 'visuel', 'Une feuille blanche et un pot de poudre noire.', 'approved'),

    (p_parent, n_bouss, 'simple',  'La boussole montre toujours le nord.', 'approved'),
    (p_parent, n_bouss, 'analogie','C’est la flèche qui dit « par là » quand on est perdu.', 'approved'),

    (p_parent, n_gouv, 'simple',   'Le gouvernail sert à diriger le bateau.', 'approved'),
    (p_parent, n_gouv, 'analogie', 'C’est le volant du bateau.', 'approved'),

    (p_parent, n_carav, 'simple',  'La caravelle est un bateau rapide des Portugais.', 'approved'),
    (p_parent, n_carav, 'visuel',  'Un petit bateau en bois à voiles triangulaires.', 'approved'),

    (p_parent, n_impr, 'simple',   'L’imprimerie copie les livres vite, sans les recopier à la main.', 'approved'),
    (p_parent, n_impr, 'histoire', 'Avant, un moine mettait des mois à copier un livre. Après, on en fait cent.', 'approved'),

    (p_parent, n_cause, 'simple',  'Mieux équipés, les marins osent partir plus loin.', 'approved'),
    (p_parent, n_cause, 'pas_a_pas','1. On sait se diriger. 2. On a de bons bateaux. 3. On part explorer.', 'approved'),

    (p_parent, n_dias, 'simple',   'Dias passe la pointe sud de l’Afrique en 1487.', 'approved'),

    (p_parent, n_colomb, 'simple', 'Colomb arrive en Amérique en 1492.', 'approved'),
    (p_parent, n_colomb, 'visuel', 'Trois bateaux devant une côte inconnue.', 'approved'),

    (p_parent, n_gama, 'simple',   'Vasco de Gama ouvre la route maritime vers les Indes en 1498.', 'approved'),

    (p_parent, n_magel, 'simple',  'Son équipage fait le tour complet de la Terre en trois ans.', 'approved'),
    (p_parent, n_magel, 'analogie','Partir d’un point et revenir au même, en faisant le tour du globe.', 'approved');

  -- ────────────────────────────── items ──────────────────────────────
  -- Niveau 1 : reconnaître. Niveau 2 : choisir sans indice. Niveau 3 : produire.

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    (p_parent, n_def, 'qcm', 1,
     jsonb_build_object('question', 'Qu’est-ce qu’une invention ?',
       'options', jsonb_build_array('Une chose qui existait déjà', 'La création d’un objet nouveau', 'Un voyage en bateau')),
     jsonb_build_object('index', 1), 'Une invention crée ce qui n’existait pas avant.', 'approved'),

    (p_parent, n_papier, 'qcm', 1,
     jsonb_build_object('question', 'Qui a inventé le papier ?',
       'options', jsonb_build_array('Les Chinois', 'Les Portugais', 'Les Allemands')),
     jsonb_build_object('index', 0), 'Le papier et la poudre à canon sont chinois.', 'approved'),

    (p_parent, n_bouss, 'qcm', 2,
     jsonb_build_object('question', 'À quoi sert la boussole ?',
       'options', jsonb_build_array('À écrire', 'À trouver le nord', 'À diriger le bateau', 'À imprimer')),
     jsonb_build_object('index', 1), 'La boussole indique le nord.', 'approved'),

    (p_parent, n_gouv, 'qcm', 2,
     jsonb_build_object('question', 'À quoi sert le gouvernail ?',
       'options', jsonb_build_array('À diriger le bateau', 'À trouver le nord', 'À copier les livres', 'À porter les voiles')),
     jsonb_build_object('index', 0), 'Le gouvernail dirige le bateau.', 'approved'),

    (p_parent, n_carav, 'qcm', 2,
     jsonb_build_object('question', 'Qui invente la caravelle en 1440 ?',
       'options', jsonb_build_array('Les Chinois', 'Les Portugais', 'Les Allemands', 'Les Espagnols')),
     jsonb_build_object('index', 1), 'La caravelle est portugaise, en 1440.', 'approved'),

    (p_parent, n_impr, 'qcm', 2,
     jsonb_build_object('question', 'Qui invente l’imprimerie en 1450 ?',
       'options', jsonb_build_array('Gutenberg', 'Magellan', 'Vasco de Gama', 'Christophe Colomb')),
     jsonb_build_object('index', 0), 'L’Allemand Gutenberg, en 1450.', 'approved'),

    (p_parent, n_cause, 'qcm', 2,
     jsonb_build_object('question', 'Ces inventions ont aidé les marins à voyager plus loin.',
       'options', jsonb_build_array('Vrai', 'Faux')),
     jsonb_build_object('index', 0), 'Elles ont favorisé la navigation et les grands voyages.', 'approved'),

    (p_parent, n_colomb, 'qcm', 2,
     jsonb_build_object('question', 'Qui découvre l’Amérique en 1492 ?',
       'options', jsonb_build_array('Vasco de Gama', 'Christophe Colomb', 'Magellan', 'Bartholomeu Dias')),
     jsonb_build_object('index', 1), 'Christophe Colomb, en 1492.', 'approved'),

    (p_parent, n_dias, 'qcm', 2,
     jsonb_build_object('question', 'Qui atteint le cap de Bonne-Espérance en 1487 ?',
       'options', jsonb_build_array('Bartholomeu Dias', 'Christophe Colomb', 'Gutenberg', 'Magellan')),
     jsonb_build_object('index', 0), 'Bartholomeu Dias, en 1487.', 'approved'),

    (p_parent, n_gama, 'qcm', 2,
     jsonb_build_object('question', 'Qui trouve la route des Indes en 1498 ?',
       'options', jsonb_build_array('Magellan', 'Christophe Colomb', 'Vasco de Gama', 'Les Portugais')),
     jsonb_build_object('index', 2), 'Vasco de Gama, en 1498.', 'approved'),

    (p_parent, n_magel, 'qcm', 2,
     jsonb_build_object('question', 'Qui fait le premier tour du monde ?',
       'options', jsonb_build_array('Colomb', 'Magellan et son équipage', 'Dias', 'Gutenberg')),
     jsonb_build_object('index', 1), 'Magellan et son équipage, de 1519 à 1522.', 'approved'),

    -- niveau 3 : produire
    (p_parent, n_magel, 'chronologie', 3,
     jsonb_build_object('question', 'Remets les voyages dans l’ordre.',
       'tokens', jsonb_build_array('Colomb en Amérique', 'Dias au cap de Bonne-Espérance',
                                   'Magellan autour du monde', 'Vasco de Gama aux Indes')),
     jsonb_build_object('order', jsonb_build_array(1, 0, 3, 2)),
     '1487 Dias, 1492 Colomb, 1498 Vasco de Gama, 1519 Magellan.', 'approved'),

    (p_parent, n_impr, 'texte_a_trous', 3,
     jsonb_build_object('text', 'L’{{1}} est inventée en {{2}} par l’Allemand Gutenberg.', 'blanks', 2),
     jsonb_build_object('values', jsonb_build_array('imprimerie', '1450')),
     'L’imprimerie, en 1450.', 'approved'),

    (p_parent, n_colomb, 'texte_a_trous', 3,
     jsonb_build_object('text', 'Christophe {{1}} découvre l’Amérique en {{2}}.', 'blanks', 2),
     jsonb_build_object('values', jsonb_build_array('Colomb', '1492')),
     'Christophe Colomb, en 1492.', 'approved');

  return v_lesson;
end;
$$;

-- Rattache la leçon à la famille déjà présente.
select public.seed_grandes_decouvertes(parent_id)
  from lessons
 where title = 'La Préhistoire'
 limit 1;
