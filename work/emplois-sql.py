# -*- coding: utf-8 -*-
"""
Produit la migration du référentiel scolaire à partir de emplois-du-temps.py.

Deux choses entrent en base :

  le catalogue des matières, par classe, avec le libellé officiel dans les
  deux langues et les intitulés de cahier qui y renvoient ;

  l'emploi du temps, créneau par créneau, avec la langue d'enseignement.

Et une troisième se répare : les huit leçons déjà importées pointaient vers
des matières inventées au fil des cahiers (« Technologies », « Droits et
devoirs », « Éducation à la paix »). Elles rejoignent les matières de leur
classe, et leur intitulé de cahier descend dans le chapitre.

Usage :  python work/emplois-sql.py
"""

import importlib.util
import io
import os

racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('edt', os.path.join(racine, 'work', 'emplois-du-temps.py'))
edt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edt)


def litteral(texte):
    """Les apostrophes du contenu sont typographiques ; on vérifie, on ne devine pas."""
    assert "'" not in texte, 'apostrophe droite : ' + texte
    return "'" + texte + "'"


def tableau(valeurs):
    return 'array[' + ', '.join(litteral(v) for v in valeurs) + ']::text[]'


ENTETE = """-- Se Former Cameroun — le référentiel de l'école
--
-- Transcrit des deux emplois du temps de la New Century Bilingual School :
-- CM1 (« Class 5 ») et CE1 (« CL3 »).
--
-- Pourquoi : un cahier n'écrit pas le nom officiel de la matière. Il écrit
-- « Éducation morale », « Droits et devoirs », « Technologies ». Sans liste
-- fermée, chaque import invente sa matière — six ont été créées en une
-- fois, dont deux qui n'existent pas au tableau de l'école.
--
-- Trois apports :
--   1. les matières appartiennent désormais à une classe, et portent leur
--      libellé officiel dans les deux langues plus les intitulés de cahier
--      qui y renvoient ;
--   2. l'emploi du temps entre en base, avec la langue de chaque créneau —
--      « Maths » le lundi et « Mathématiques » le mercredi sont la même
--      matière enseignée dans deux langues, et le produit doit le savoir ;
--   3. les huit leçons déjà importées rejoignent les matières de leur
--      classe ; leur intitulé de cahier descend dans le chapitre.

-- ───────────────────────── matières par classe ─────────────────────────

alter table subjects add column if not exists class_id    uuid references classes (id);
alter table subjects add column if not exists official_fr text;
alter table subjects add column if not exists official_en text;
alter table subjects add column if not exists aliases     text[] not null default '{}';

-- Une même matière peut exister dans deux classes avec des libellés
-- identiques : l'unicité se joue désormais par classe.
alter table subjects drop constraint if exists subjects_parent_id_label_key;
create unique index if not exists subjects_parent_classe_label
  on subjects (parent_id, class_id, label);

-- ─────────────────────────── emploi du temps ───────────────────────────

create table if not exists timetable_slots (
  id         uuid primary key default gen_random_uuid(),
  parent_id  uuid not null references auth.users (id) on delete cascade,
  class_id   uuid not null references classes (id),
  subject_id uuid references subjects (id) on delete set null,
  -- 1 lundi … 5 vendredi
  day        smallint not null check (day between 1 and 5),
  debut      time not null,
  fin        time not null check (fin > debut),
  kind       text not null check (kind in ('cours', 'pause', 'rassemblement', 'club')),
  -- Le libellé exact de la feuille : c'est lui qui fait foi en cas de doute.
  label      text not null,
  lang       text check (lang in ('fr', 'en')),
  created_at timestamptz not null default now(),
  unique (parent_id, class_id, day, debut)
);

alter table timetable_slots enable row level security;

do $$
begin
  if not exists (select 1 from pg_policies where tablename = 'timetable_slots' and policyname = 'timetable_select') then
    create policy timetable_select on timetable_slots
      for select to authenticated using (parent_id = auth.uid());
    create policy timetable_insert on timetable_slots
      for insert to authenticated with check (parent_id = auth.uid());
    create policy timetable_update on timetable_slots
      for update to authenticated using (parent_id = auth.uid()) with check (parent_id = auth.uid());
    create policy timetable_delete on timetable_slots
      for delete to authenticated using (parent_id = auth.uid());
  end if;
end
$$;

-- ──────────────────────────── le contenu ────────────────────────────

create or replace function public.seed_referentiel_ecole(p_parent uuid)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  v_class   uuid;
  v_subject uuid;
  v_lesson  uuid;
  n         integer := 0;
begin
"""

PIED = """  return n;
end;
$$;

select public.seed_referentiel_ecole(parent_id)
  from children
 where first_name = 'KLEIN'
 limit 1;
"""


def sql():
    out = [ENTETE]

    for code, matieres, emploi in edt.CLASSES:
        out.append("  -- ───────────────────────────── %s ─────────────────────────────" % code)
        out.append("  select id into v_class from classes where subsystem = 'francophone' and code = %s;\n"
                   % litteral(code))

        for libelle, couleur, officiel_fr, officiel_en, intitules in matieres:
            out.append("  insert into subjects (parent_id, class_id, label, color, official_fr, official_en, aliases)")
            out.append("  values (p_parent, v_class, %s, %s, %s, %s, %s)"
                       % (litteral(libelle), litteral(couleur), litteral(officiel_fr),
                          litteral(officiel_en), tableau(intitules)))
            out.append("  on conflict (parent_id, class_id, label) do update")
            out.append("    set color = excluded.color, official_fr = excluded.official_fr,")
            out.append("        official_en = excluded.official_en, aliases = excluded.aliases;\n")

        out.append("  -- L'emploi du temps est réécrit en entier : la feuille fait foi.")
        out.append("  delete from timetable_slots where parent_id = p_parent and class_id = v_class;\n")

        for jour in sorted(emploi):
            for debut, fin, genre, langue, libelle, matiere in emploi[jour]:
                if matiere:
                    out.append("  select id into v_subject from subjects"
                               " where parent_id = p_parent and class_id = v_class and label = %s;"
                               % litteral(matiere))
                else:
                    out.append("  v_subject := null;")
                out.append("  insert into timetable_slots (parent_id, class_id, subject_id, day, debut, fin, kind, label, lang)")
                out.append("  values (p_parent, v_class, v_subject, %d, '%s', '%s', '%s', %s, %s);"
                           % (jour, debut, fin, genre, litteral(libelle),
                              litteral(langue) if langue else 'null'))
                out.append("  n := n + 1;")
        out.append("")

    out.append("  -- ───────────── rattachement des leçons déjà importées ─────────────")
    for titre, classe, matiere, chapitre in edt.LECONS:
        out.append("  select id into v_class from classes where subsystem = 'francophone' and code = %s;"
                   % litteral(classe))
        out.append("  select id into v_subject from subjects"
                   " where parent_id = p_parent and class_id = v_class and label = %s;" % litteral(matiere))
        out.append("  update lessons set subject_id = v_subject, class_id = v_class, chapter = %s"
                   " where title = %s;\n" % (litteral(chapitre), litteral(titre)))

    out.append("  -- Les matières inventées au fil des cahiers, désormais sans leçon,")
    out.append("  -- disparaissent : elles ne doivent plus être proposées à l'import.")
    out.append("  delete from subjects s")
    out.append("   where s.parent_id = p_parent and s.class_id is null")
    out.append("     and not exists (select 1 from lessons l where l.subject_id = s.id);\n")

    out.append(PIED)
    return '\n'.join(out)


if __name__ == '__main__':
    texte = sql()
    chemin = os.path.join(racine, 'supabase', 'migrations', '20261016150000_referentiel_ecole.sql')
    io.open(chemin, 'w', encoding='utf-8', newline='\n').write(texte)
    print('%d lignes de SQL' % len(texte.splitlines()))
    print(chemin)
