-- Se Former Cameroun — migration du contenu du prototype (lot 0)
--
-- La leçon Préhistoire était codée en dur dans le HTML du prototype. Elle
-- devient ici des lignes en base, ce qui est tout l'objet du lot 0.
--
-- Pourquoi une fonction et non des INSERT : chaque ligne a besoin d'un
-- parent_id, qui n'existe qu'une fois un parent inscrit. La fonction s'exécute
-- avec les droits de l'appelant, donc la RLS s'applique normalement et le
-- contenu appartient à celui qui la déclenche.
--
-- Appel depuis l'app :  supabase.rpc('seed_demo_prehistoire')
--
-- Tous les textes français utilisent l'apostrophe typographique ’ : cela évite
-- de doubler les apostrophes dans chaque littéral SQL.

create or replace function public.seed_demo_prehistoire()
returns uuid
language plpgsql
security invoker
set search_path = public
as $$
declare
  v_parent   uuid := auth.uid();
  v_class    uuid;
  v_subject  uuid;
  v_lesson   uuid;
  n_def      uuid;  -- définition de la Préhistoire
  n_date     uuid;  -- la date de fin
  n_paleo    uuid;  -- le Paléolithique
  n_vivre    uuid;  -- chasse, pêche, cueillette
  n_neo      uuid;  -- le Néolithique
  n_metaux   uuid;  -- l’âge des métaux
  n_ordre    uuid;  -- l’ordre des trois périodes
begin
  if v_parent is null then
    raise exception 'authentification requise';
  end if;

  select id into v_class from classes
   where subsystem = 'francophone' and code = 'CM1';

  -- Matière : l’intitulé est celui de l’école, le parent peut le renommer.
  insert into subjects (parent_id, label, color)
  values (v_parent, 'Histoire', '#d66d4d')
  on conflict (parent_id, label) do update set label = excluded.label
  returning id into v_subject;

  insert into lessons
    (parent_id, subject_id, class_id, title, summary, lang, chapter, sort_order, status)
  values (
    v_parent, v_subject, v_class,
    'La Préhistoire',
    'La Préhistoire est la période comprise entre l’apparition des premiers humains et '
    || 'l’invention de l’écriture, vers 3 000 avant J.-C. Elle se divise en trois époques : '
    || 'le Paléolithique (pierre taillée), le Néolithique (pierre polie) et l’âge des métaux.',
    'fr', 'Les débuts de l’humanité', 1, 'approved'
  )
  returning id into v_lesson;

  -- ───────────────────────────── notions ─────────────────────────────
  -- Sept notions, une seule chose à savoir par notion. Le type conditionne
  -- les jeux qu’on pourra générer : une liste donne un texte à trous, une
  -- relation donne une chronologie, une date donne un QCM.

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status) values
    (v_parent, v_lesson, 'definition',
     'La Préhistoire va de l’apparition des premiers humains à l’invention de l’écriture.', 1, 'approved')
  returning id into n_def;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status) values
    (v_parent, v_lesson, 'date',
     'L’écriture est inventée vers 3 000 avant J.-C. et marque la fin de la Préhistoire.', 2, 'approved')
  returning id into n_date;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status) values
    (v_parent, v_lesson, 'definition',
     'Le Paléolithique est l’âge de la pierre taillée.', 3, 'approved')
  returning id into n_paleo;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status) values
    (v_parent, v_lesson, 'liste',
     'Au Paléolithique, les humains vivent de la chasse, de la pêche et de la cueillette.', 4, 'approved')
  returning id into n_vivre;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status) values
    (v_parent, v_lesson, 'definition',
     'Le Néolithique est l’âge de la pierre polie : les humains commencent l’agriculture.', 5, 'approved')
  returning id into n_neo;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status) values
    (v_parent, v_lesson, 'liste',
     'À l’âge des métaux, les humains fabriquent outils et bijoux en cuivre, bronze et fer.', 6, 'approved')
  returning id into n_metaux;

  insert into notions (parent_id, lesson_id, kind, statement, sort_order, status) values
    (v_parent, v_lesson, 'relation',
     'Les trois époques se suivent dans cet ordre : Paléolithique, Néolithique, âge des métaux.', 7, 'approved')
  returning id into n_ordre;

  -- ───────────────────────── explications ─────────────────────────
  -- Plusieurs registres par notion : c’est ce qui alimente « Explique
  -- autrement ». Le lot 2 les générera, ici on amorce.

  insert into explanations (parent_id, notion_id, register, body, status) values
    (v_parent, n_def, 'simple',
     'La Préhistoire, c’est le très long temps d’avant l’écriture.', 'approved'),
    (v_parent, n_def, 'analogie',
     'Imagine un livre de la vie des humains : la Préhistoire, c’est tout ce qui s’est passé '
     || 'avant que quelqu’un ait l’idée d’écrire la première page.', 'approved'),
    (v_parent, n_def, 'pas_a_pas',
     '1. Les premiers humains apparaissent. 2. Ils vivent très longtemps sans écrire. '
     || '3. Le jour où ils inventent l’écriture, la Préhistoire s’arrête.', 'approved'),

    (v_parent, n_date, 'simple',
     'Vers 3 000 avant J.-C., l’écriture apparaît : la Préhistoire se termine.', 'approved'),
    (v_parent, n_date, 'visuel',
     'Sur une frise, place un repère à 3 000 avant J.-C. : tout ce qui est à gauche est la '
     || 'Préhistoire, tout ce qui est à droite est l’Histoire.', 'approved'),

    (v_parent, n_paleo, 'simple',
     'Paléolithique veut dire « pierre ancienne » : on casse la pierre pour la rendre '
     || 'tranchante.', 'approved'),
    (v_parent, n_paleo, 'analogie',
     'Tailler, c’est comme casser un morceau de craie pour obtenir une pointe : la pierre '
     || 'devient un outil qui coupe.', 'approved'),

    (v_parent, n_vivre, 'simple',
     'Trois mots à retenir : chasse, pêche, cueillette.', 'approved'),
    (v_parent, n_vivre, 'histoire',
     'Ona part pêcher au bord du fleuve, son frère chasse dans la plaine, leur mère cueille '
     || 'des baies. Le soir, tout le monde mange ce que chacun a trouvé.', 'approved'),

    (v_parent, n_neo, 'simple',
     'Néolithique veut dire « pierre nouvelle » : on frotte la pierre pour la rendre lisse, '
     || 'et on commence à cultiver la terre.', 'approved'),
    (v_parent, n_neo, 'analogie',
     'Polir, c’est comme poncer un morceau de bois : on frotte longtemps pour que ce soit '
     || 'lisse, au lieu de casser.', 'approved'),

    (v_parent, n_metaux, 'simple',
     'Trois métaux à retenir : cuivre, bronze, fer. On en fait des outils et des bijoux.', 'approved'),

    (v_parent, n_ordre, 'simple',
     'Retiens le geste : tailler, puis polir, puis fondre le métal.', 'approved'),
    (v_parent, n_ordre, 'visuel',
     'Trois cases de gauche à droite : une pierre pointue, une pierre lisse, un bijou en '
     || 'métal.', 'approved');

  -- ───────────────────────────── items ─────────────────────────────
  -- Niveau 1 : reconnaître, la leçon reste affichée.
  -- Niveau 2 : choisir sans indice (les cinq questions de l’interrogation).
  -- Niveau 3 : produire.

  insert into items (parent_id, notion_id, kind, level, payload, answer, explain, status) values
    -- niveau 1, reprise des trois défis du prototype
    (v_parent, n_ordre, 'qcm', 1,
     jsonb_build_object(
       'question', 'Quelle période vient en premier ?',
       'options', jsonb_build_array('Le Paléolithique', 'L’âge des métaux', 'Le Néolithique')),
     jsonb_build_object('index', 0),
     'Le Paléolithique est la première période étudiée.', 'approved'),

    (v_parent, n_neo, 'qcm', 1,
     jsonb_build_object(
       'question', 'Qui commence à pratiquer l’agriculture ?',
       'options', jsonb_build_array('Les humains du Paléolithique', 'Les humains du Néolithique',
                                    'Les humains de l’âge des métaux')),
     jsonb_build_object('index', 1),
     'L’agriculture est associée au Néolithique.', 'approved'),

    (v_parent, n_date, 'qcm', 1,
     jsonb_build_object(
       'question', 'L’invention de l’_____ marque la fin de la Préhistoire.',
       'options', jsonb_build_array('agriculture', 'métallurgie', 'écriture')),
     jsonb_build_object('index', 2),
     'L’écriture marque la fin de la Préhistoire.', 'approved'),

    -- niveau 2, les cinq questions de l’interrogation
    (v_parent, n_date, 'qcm', 2,
     jsonb_build_object(
       'question', 'Quel événement marque la fin de la Préhistoire ?',
       'options', jsonb_build_array('La découverte du feu', 'L’invention de l’écriture',
                                    'Le début de la chasse', 'La fabrication des bijoux')),
     jsonb_build_object('index', 1),
     'L’invention de l’écriture, vers 3 000 avant J.-C., marque la fin de la Préhistoire.', 'approved'),

    (v_parent, n_paleo, 'qcm', 2,
     jsonb_build_object(
       'question', 'Comment appelle-t-on l’âge de la pierre taillée ?',
       'options', jsonb_build_array('Le Paléolithique', 'Le Néolithique', 'L’âge du bronze',
                                    'L’Antiquité')),
     jsonb_build_object('index', 0),
     'Le Paléolithique correspond à l’âge de la pierre taillée.', 'approved'),

    (v_parent, n_vivre, 'qcm', 2,
     jsonb_build_object(
       'question', 'Quelles activités sont associées au Paléolithique ?',
       'options', jsonb_build_array('Écriture et commerce', 'Chasse, pêche et cueillette',
                                    'Agriculture uniquement', 'Fabrication de bijoux en bronze')),
     jsonb_build_object('index', 1),
     'Les humains du Paléolithique vivent de la chasse, de la pêche et de la cueillette.', 'approved'),

    (v_parent, n_neo, 'qcm', 2,
     jsonb_build_object(
       'question', 'À quelle période commence-t-on à pratiquer l’agriculture ?',
       'options', jsonb_build_array('Au Paléolithique', 'À l’âge des métaux', 'Au Néolithique',
                                    'Après l’invention de l’écriture')),
     jsonb_build_object('index', 2),
     'L’agriculture apparaît avec le Néolithique, l’âge de la pierre polie.', 'approved'),

    (v_parent, n_metaux, 'qcm', 2,
     jsonb_build_object(
       'question', 'Que fabrique-t-on pendant l’âge des métaux ?',
       'options', jsonb_build_array('Seulement des maisons', 'Des outils et des bijoux',
                                    'Des livres', 'Des outils en plastique')),
     jsonb_build_object('index', 1),
     'Les humains fabriquent des outils et des bijoux en métal.', 'approved'),

    -- niveau 3, produire
    (v_parent, n_ordre, 'chronologie', 3,
     jsonb_build_object(
       'question', 'Remets les trois époques dans l’ordre.',
       'tokens', jsonb_build_array('Le Néolithique', 'L’âge des métaux', 'Le Paléolithique')),
     jsonb_build_object('order', jsonb_build_array(2, 0, 1)),
     'Paléolithique, puis Néolithique, puis âge des métaux.', 'approved'),

    (v_parent, n_vivre, 'texte_a_trous', 3,
     jsonb_build_object(
       'text', 'Au Paléolithique, les humains vivent de la {{1}}, de la {{2}} et de la {{3}}.',
       'blanks', 3),
     jsonb_build_object('values', jsonb_build_array('chasse', 'pêche', 'cueillette')),
     'Les trois mots à retenir sont chasse, pêche et cueillette.', 'approved'),

    (v_parent, n_date, 'texte_a_trous', 3,
     jsonb_build_object(
       'text', 'La Préhistoire se termine avec l’invention de l’{{1}}, vers {{2}} avant J.-C.',
       'blanks', 2),
     jsonb_build_object('values', jsonb_build_array('écriture', '3 000')),
     'L’écriture, vers 3 000 avant J.-C.', 'approved');

  -- ───────────────────────────── vidéo ─────────────────────────────
  -- Le manifeste est conservé tel quel : il permet de régénérer la vidéo à
  -- l’identique, ou avec une seule ligne corrigée.
  --
  -- À noter : le bloc 4 place le feu au Néolithique, ce que l’espace parent
  -- signale comme douteux. La vidéo hébergée contient donc une approximation
  -- que la prochaine régénération devra corriger.

  insert into videos
    (parent_id, lesson_id, manifest, voice_preset, external_url, poster_url, duration_s, status)
  values (
    v_parent, v_lesson,
    jsonb_build_object(
      'title', 'Voyage dans la Préhistoire',
      'channel_type', 'Kids',
      'style', 'Pastel Flat 2D',
      'duration_seconds', 60,
      'aspect_ratio', '16:9',
      'language', 'fr',
      'talking_characters', false,
      'through_line', 'Une roue-mémoire se complète puis devient une tablette d’argile gravée.',
      'blocks', jsonb_build_array(
        jsonb_build_object('n', 1, 'block_kind', 'narration', 'vo_line',
          'Qu’est-ce que la Préhistoire ? Elle va des premiers hommes à l’écriture, vers trois mille ans avant Jésus-Christ.'),
        jsonb_build_object('n', 2, 'block_kind', 'narration', 'vo_line',
          'La première époque est le Paléolithique où l’homme taille la pierre et transforme les éclats en outils tranchants.'),
        jsonb_build_object('n', 3, 'block_kind', 'narration', 'vo_line',
          'Au Paléolithique les hommes vivent de pêche de chasse et de cueillette, retiens bien ces trois images.'),
        jsonb_build_object('n', 4, 'block_kind', 'narration', 'vo_line',
          'Au Néolithique la pierre devient lisse le feu brille et l’agriculture commence durant cette deuxième grande époque.'),
        jsonb_build_object('n', 5, 'block_kind', 'narration', 'vo_line',
          'Troisième époque l’âge des métaux où l’artisan chauffe cuivre bronze et fer pour fabriquer bijoux et outils.'),
        jsonb_build_object('n', 6, 'block_kind', 'narration', 'vo_line',
          'Puis une main grave des signes sur l’argile et l’écriture est inventée, voilà comment la Préhistoire se termine.')
      )
    ),
    '57ccb351-84d7-54ba-afd4-26b566ca6023',
    'https://d2ol7oe51mr4n9.cloudfront.net/user_3KZBSjYUBpq6aChUVJxyOvBy5SO/b3fdb117-8acd-4313-a339-7dd960299e73.mp4',
    'https://d8j0ntlcm91z4.cloudfront.net/user_3KZBSjYUBpq6aChUVJxyOvBy5SO/hf_20261014_202123_e5088508-c610-465e-b0a3-a12e80dd970e.png',
    62,
    'published'
  );

  return v_lesson;
end;
$$;

revoke all on function public.seed_demo_prehistoire() from public, anon;
grant execute on function public.seed_demo_prehistoire() to authenticated;
