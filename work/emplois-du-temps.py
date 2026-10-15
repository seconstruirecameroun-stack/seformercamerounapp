# -*- coding: utf-8 -*-
"""
Les emplois du temps de la New Century Bilingual School (Yaoundé).

Transcrits depuis les deux feuilles photographiées : CM1 (« Class 5 ») pour
BRAYNE, CE1 (« CL3 ») pour KLEIN.

À quoi ça sert : un cahier n'écrit pas le nom officiel de la matière. Il
écrit « Éducation morale », « Droits et devoirs », « Technologies ». L'école,
elle, a une liste fermée de matières, et elle les nomme dans les deux
langues. Sans ce référentiel, chaque import invente sa propre matière — on
l'a vu : six matières créées en une fois, dont deux qui n'existent pas au
tableau.

Ce fichier porte donc trois choses :

  1. le catalogue des matières de chaque classe, avec le libellé officiel
     français et anglais, et les intitulés de cahier qui y renvoient ;
  2. l'emploi du temps complet, créneau par créneau ;
  3. le rattachement des huit leçons déjà importées.

La langue d'un créneau est celle dans laquelle l'école l'écrit : c'est ainsi
qu'un établissement bilingue signale la langue d'enseignement. « Maths » le
lundi et « Mathématiques » le mercredi, c'est la même matière dans deux
langues — et c'est exactement ce que le produit doit savoir distinguer.

Usage :  python work/emplois-du-temps.py
"""

import io
import json
import os

# ───────────────────────────── catalogue ─────────────────────────────
# (libellé enfant, couleur, officiel fr, officiel en, intitulés de cahier)

MATIERES_CM1 = [
    ('Histoire-Géographie', '#d66d4d', 'Histoire / Géographie', 'Social Studies I (Hist/Geo)',
     ['Histoire', 'Géographie', 'Hist/Géo', 'Histoire-Géo']),
    ('ECM', '#b4584f', 'Histoire / Géographie / ECM', 'Social Studies 2 (Civics, Moral Educ, Human Rights)',
     ['Éducation civique', 'Éducation morale', 'Droits et devoirs', 'Éducation à la paix', 'ECM']),
    ('Français', '#5b8ac2', 'Français', 'French', ['Français', 'Dictée', 'Grammaire', 'Conjugaison']),
    ('Anglais', '#4f7fae', 'Anglais', 'English Language',
     ['English', 'Anglais', 'Vocabulary', 'Grammar', 'Reading comprehension']),
    ('Mathématiques', '#3f7d6a', 'Mathématiques', 'Maths', ['Maths', 'Mathématiques', 'Calcul']),
    ('Sciences', '#3f9d8f', 'Sciences', 'Science', ['Sciences', 'SVT', 'Environnement', 'Santé']),
    ('Technologie', '#d08a3c', 'Technologie', 'Technology', ['Technologie', 'Technologies']),
    ('TIC', '#7a76c4', 'TIC', 'ICT', ['TIC', 'TICE', 'Informatique', 'ICT']),
    ('Musique', '#c2708f', 'Musique', 'Music', ['Musique', 'Chant']),
    ('Dessin', '#c98f5a', 'Dessin', 'Drawing', ['Dessin', 'Arts plastiques']),
    ('EPS', '#6f9a3f', 'EPS', 'PE', ['EPS', 'Sport']),
    ('Langues et cultures nationales', '#8a6fb0', 'Langues et cultures nationales',
     'National languages and cultures', ['Langues nationales', 'Culture nationale']),
    ('Développement personnel', '#a0714d', 'Développement personnel', 'Personal development',
     ['Développement personnel']),
    ('Métiers', '#9a8450', 'Métiers', 'Vocational studies (home economics)',
     ['Économie familiale', 'Travaux manuels']),
]

MATIERES_CE1 = [
    ('Histoire', '#d66d4d', 'Sciences humaines et sociales (histoire)', 'Social studies (history)',
     ['Histoire']),
    ('Géographie', '#c97c52', 'Sciences humaines et sociales (géographie)', 'Social studies (geography)',
     ['Géographie']),
    ('Éducation civique', '#3f9d8f', 'Sciences humaines et sociales (éducation civique)',
     'Social studies (civics)', ['Éducation civique', 'Instruction civique']),
    ('Éducation morale', '#c2708f', 'Sciences humaines et sociales (éducation morale)',
     'Social studies (moral education)', ['Éducation morale', 'Éducation à la paix', 'Morale']),
    ('Droits humains', '#5b8ac2', 'Sciences humaines et sociales (droits humains)',
     'Social studies (human rights)', ['Droits et devoirs', 'Droits humains', 'Droits de l’enfant']),
    ('Français', '#4f7fae', 'Français', 'French',
     ['Français', 'Littérature', 'Grammaire', 'Conjugaison', 'Orthographe', 'Vocabulaire', 'Dictée']),
    ('Anglais', '#3f6f9e', 'Anglais', 'English language',
     ['English', 'Anglais', 'Vocabulary', 'Grammar', 'Spelling', 'Reading']),
    ('Mathématiques', '#3f7d6a', 'Mathématiques', 'Mathematics',
     ['Maths', 'Mathématiques', 'Nombres et calculs', 'Mesures et grandeurs', 'Géométrie']),
    ('Sciences et technologies', '#d08a3c', 'Sciences et technologies', 'Science and technology',
     ['Sciences', 'Technologies', 'Technologie', 'Environnement', 'Santé']),
    ('TIC', '#7a76c4', 'T.I.C.E (informatique)', 'I.C.T', ['TIC', 'TICE', 'Informatique', 'ICT']),
    ('Éducation artistique', '#b36fa0', 'Éducation artistique (musique, dessin)', 'Art and craft',
     ['Musique', 'Dessin', 'Art', 'Chant']),
    ('EPS', '#6f9a3f', 'EPS', 'P.E', ['EPS', 'Sport']),
    ('Langue et culture nationale', '#8a6fb0', 'Langue et culture nationale',
     'National language and culture', ['Langues nationales', 'Culture nationale']),
    ('Développement personnel', '#a0714d', 'Développement personnel', 'Personal development',
     ['Développement personnel']),
    ('Métiers', '#9a8450', 'Métiers', 'Vocational studies',
     ['Économie familiale', 'Agropastoral', 'Travaux manuels']),
    ('Bibliothèque', '#7d8a6a', 'Bibliothèque / littérature', 'Library / literature',
     ['Bibliothèque', 'Lecture suivie']),
]

# ───────────────────────── emplois du temps ─────────────────────────
# jour: 1 lundi … 5 vendredi.  (debut, fin, genre, langue, libellé, matière)
# genre : cours | pause | rassemblement | club
# matière : le libellé enfant du catalogue, ou None pour ce qui n'est pas un cours.

P = 'pause'
R = 'rassemblement'
C = 'cours'
K = 'club'

CM1 = {
    1: [
        ('07:20', '07:40', R, None, 'Morning devotion', None),
        ('07:40', '08:00', C, 'en', 'Social Studies 2 (Civics)', 'ECM'),
        ('08:00', '08:30', C, 'en', 'Maths', 'Mathématiques'),
        ('08:30', '09:00', C, 'en', 'Maths', 'Mathématiques'),
        ('09:00', '09:30', C, 'en', 'Social Studies I (Hist/Geo)', 'Histoire-Géographie'),
        ('10:00', '10:30', C, 'en', 'English Language (Reading Comp)', 'Anglais'),
        ('10:30', '11:00', C, 'fr', 'Technologie', 'Technologie'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '12:40', C, 'fr', 'Français', 'Français'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'fr', 'Français', 'Français'),
        ('13:40', '14:10', C, 'fr', 'Histoire / Géo', 'Histoire-Géographie'),
        ('14:10', '14:40', C, 'fr', 'Sciences', 'Sciences'),
        ('14:40', '15:10', C, 'fr', 'TIC', 'TIC'),
    ],
    2: [
        ('07:20', '07:40', R, None, 'Devotion', None),
        ('07:40', '08:00', C, 'fr', 'Histoire / Géographie / ECM', 'ECM'),
        ('08:00', '08:30', C, 'fr', 'Français', 'Français'),
        ('08:30', '09:00', C, 'fr', 'Sciences', 'Sciences'),
        ('09:00', '09:30', C, 'fr', 'Maths', 'Mathématiques'),
        ('09:30', '10:00', C, 'fr', 'Français', 'Français'),
        ('10:30', '11:00', C, 'fr', 'Français', 'Français'),
        ('11:00', '11:10', P, None, 'Petite pause', None),
        ('11:10', '11:40', C, 'en', 'Maths', 'Mathématiques'),
        ('11:40', '12:10', C, 'en', 'English Language (Vocabulary)', 'Anglais'),
        ('12:10', '12:40', C, 'en', 'Sciences (Health Educ)', 'Sciences'),
        ('12:40', '13:10', P, None, 'Long break', None),
        ('13:10', '13:40', C, 'en', 'Vocational Studies (Home Economics)', 'Métiers'),
        ('14:10', '14:40', C, 'en', 'English Language (Vocabulary)', 'Anglais'),
        ('14:40', '15:10', C, 'en', 'Social Studies II (Moral Educ)', 'ECM'),
    ],
    3: [
        ('07:20', '07:40', R, None, 'Rassemblement', None),
        ('07:40', '08:00', C, 'en', 'Maths', 'Mathématiques'),
        ('08:00', '08:30', C, 'en', 'Maths', 'Mathématiques'),
        ('08:30', '09:00', C, 'en', 'Social Studies I (Hist/Geo)', 'Histoire-Géographie'),
        ('09:00', '09:30', C, 'en', 'Social Studies I (Hist/Geo)', 'Histoire-Géographie'),
        ('09:30', '10:00', C, 'en', 'English Language (Vocabulary)', 'Anglais'),
        ('10:00', '10:30', C, 'en', 'English Language (Grammar)', 'Anglais'),
        ('10:30', '11:00', C, 'fr', 'Sciences (Environ Educ)', 'Sciences'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '11:40', C, 'fr', 'Français', 'Français'),
        ('11:40', '12:10', C, 'fr', 'Sciences', 'Sciences'),
        ('12:10', '12:40', C, 'fr', 'Mathématiques', 'Mathématiques'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'fr', 'Musique', 'Musique'),
        ('13:40', '14:10', C, 'fr', 'TIC', 'TIC'),
        ('14:10', '14:40', C, 'fr', 'Français', 'Français'),
        ('14:40', '15:10', C, 'fr', 'Français', 'Français'),
    ],
    4: [
        ('07:20', '07:40', R, None, 'Matinal', None),
        ('07:40', '08:00', C, 'fr', 'Histoire / Géo - ECM', 'ECM'),
        ('08:00', '09:30', C, 'fr', 'Français', 'Français'),
        ('09:30', '10:00', C, 'fr', 'Mathématiques', 'Mathématiques'),
        ('10:00', '10:30', C, 'fr', 'Français', 'Français'),
        ('10:30', '11:00', C, 'fr', 'Musique', 'Musique'),
        ('11:00', '11:10', P, None, 'Petite pause', None),
        ('11:10', '11:40', C, 'en', 'Maths', 'Mathématiques'),
        ('11:40', '12:10', C, 'en', 'English Language (Guided Writing)', 'Anglais'),
        ('12:10', '12:40', C, 'en', 'Sciences (Environ Educ)', 'Sciences'),
        ('12:40', '13:10', P, None, 'Long break', None),
        ('13:10', '13:40', C, 'en', 'Sciences (Health Educ)', 'Sciences'),
        ('13:40', '14:10', C, 'en', 'Drawing', 'Dessin'),
        ('14:10', '14:40', K, None, 'Club activities', None),
        ('14:40', '15:10', K, None, 'Club activities', None),
    ],
    5: [
        ('07:20', '07:40', C, 'en', 'Social Studies 2 (Human Rights)', 'ECM'),
        ('07:40', '08:00', C, 'en', 'Maths', 'Mathématiques'),
        ('08:00', '08:30', C, 'en', 'Maths', 'Mathématiques'),
        ('08:30', '09:00', C, 'en', 'English Language (Productive Writing)', 'Anglais'),
        ('09:00', '09:30', C, 'en', 'English Language (Productive Writing)', 'Anglais'),
        ('09:30', '10:00', C, 'en', 'English Language (Spelling/Dictation)', 'Anglais'),
        ('10:00', '10:30', C, 'en', 'ICT', 'TIC'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '11:40', C, 'fr', 'Sciences', 'Sciences'),
        ('11:40', '12:10', C, 'fr', 'Dictée', 'Français'),
        ('12:10', '12:40', C, 'fr', 'Développement personnel', 'Développement personnel'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'fr', 'Langues et cultures nationales', 'Langues et cultures nationales'),
        ('13:40', '14:10', C, 'fr', 'Mathématiques', 'Mathématiques'),
        ('14:10', '14:40', C, 'fr', 'EPS', 'EPS'),
        ('14:40', '15:10', C, 'fr', 'EPS', 'EPS'),
    ],
}

CE1 = {
    1: [
        ('07:20', '07:40', R, None, 'Morning devotion and inspection', None),
        ('07:40', '08:00', C, 'en', 'Mathematics', 'Mathématiques'),
        ('08:00', '08:30', C, 'en', 'English language (vocabulary)', 'Anglais'),
        ('08:30', '09:00', C, 'en', 'Vocational studies (home economics)', 'Métiers'),
        ('09:00', '09:30', C, 'en', 'Social studies (geography)', 'Géographie'),
        ('09:30', '10:00', C, 'en', 'English language (grammar)', 'Anglais'),
        ('10:00', '10:30', C, 'en', 'English language (spelling and dictation)', 'Anglais'),
        ('10:30', '11:00', C, 'en', 'Science and technology (environ education)', 'Sciences et technologies'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '11:40', C, 'fr', 'Français (littérature)', 'Français'),
        ('11:40', '12:10', C, 'fr', 'Français (vocabulaire)', 'Français'),
        ('12:10', '12:40', C, 'fr', 'Français (grammaire)', 'Français'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'fr', 'Mathématiques (nombres et calculs)', 'Mathématiques'),
        ('13:40', '14:10', C, 'fr', 'Mathématiques (nombres et calculs)', 'Mathématiques'),
        ('14:10', '14:40', C, 'fr', 'Sciences et technologies', 'Sciences et technologies'),
        ('14:40', '15:10', C, 'fr', 'Sciences humaines et sociales (histoire)', 'Histoire'),
    ],
    2: [
        ('07:20', '07:40', R, None, 'Morning devotion and inspection', None),
        ('07:40', '08:00', C, 'fr', 'Sciences humaines et sociales (éducation civique)', 'Éducation civique'),
        ('08:00', '08:30', C, 'fr', 'Français (littérature)', 'Français'),
        ('08:30', '09:00', C, 'fr', 'Français (production d’écrits)', 'Français'),
        ('09:00', '09:30', C, 'fr', 'Français (production d’écrits)', 'Français'),
        ('09:30', '10:00', C, 'fr', 'Musique', 'Éducation artistique'),
        ('10:00', '10:30', C, 'fr', 'Mathématiques (mesures et grandeurs)', 'Mathématiques'),
        ('10:30', '11:00', C, 'fr', 'Sciences et technologies', 'Sciences et technologies'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '11:40', C, 'en', 'Literature', 'Anglais'),
        ('11:40', '12:10', C, 'en', 'Mathematics', 'Mathématiques'),
        ('12:10', '12:40', C, 'en', 'Science and technology (environmental education)', 'Sciences et technologies'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'en', 'ICT', 'TIC'),
        ('13:40', '14:10', C, 'en', 'Vocational studies (home economics)', 'Métiers'),
        ('14:10', '14:40', C, 'en', 'Art (drama and sing)', 'Éducation artistique'),
        ('14:40', '15:10', C, 'en', 'Art and craft (drawing)', 'Éducation artistique'),
    ],
    3: [
        ('07:20', '07:40', R, None, 'Morning devotion and inspection', None),
        ('07:40', '08:00', C, 'en', 'Social studies (civics)', 'Éducation civique'),
        ('08:00', '08:30', C, 'en', 'Mathematics', 'Mathématiques'),
        ('08:30', '09:00', C, 'en', 'English language (vocabulary)', 'Anglais'),
        ('09:00', '09:30', C, 'en', 'English language (guided writing and handwriting)', 'Anglais'),
        ('09:30', '10:00', C, 'en', 'Social studies (history)', 'Histoire'),
        ('10:00', '10:30', C, 'en', 'I.C.T', 'TIC'),
        ('10:30', '11:00', C, 'en', 'Science and technology (tech and engineering)', 'Sciences et technologies'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '11:40', C, 'fr', 'Français (littérature)', 'Français'),
        ('11:40', '12:10', C, 'fr', 'Mathématiques (géométrie et espace)', 'Mathématiques'),
        ('12:10', '12:40', C, 'fr', 'Mathématiques (géométrie et espace)', 'Mathématiques'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'fr', 'Français (conjugaison)', 'Français'),
        ('13:40', '14:10', C, 'fr', 'Sciences humaines et sociales (éducation civique)', 'Éducation civique'),
        ('14:10', '14:40', C, 'fr', 'Sciences et technologies', 'Sciences et technologies'),
        ('14:40', '15:10', C, 'fr', 'Bibliothèque / littérature', 'Bibliothèque'),
    ],
    4: [
        ('07:20', '07:40', R, None, 'Morning devotion and inspection', None),
        ('07:40', '08:00', C, 'fr', 'Sciences humaines et sociales (éducation morale)', 'Éducation morale'),
        ('08:00', '08:30', C, 'fr', 'Français (littérature)', 'Français'),
        ('08:30', '09:00', C, 'fr', 'Mathématiques (mesures et grandeurs)', 'Mathématiques'),
        ('09:00', '09:30', C, 'fr', 'Français (grammaire)', 'Français'),
        ('09:30', '10:00', C, 'fr', 'Français (orthographe)', 'Français'),
        ('10:00', '10:30', C, 'fr', 'Développement personnel', 'Développement personnel'),
        ('10:30', '11:00', C, 'fr', 'EPS', 'EPS'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '11:40', C, 'en', 'English language (grammar)', 'Anglais'),
        ('11:40', '12:10', C, 'en', 'Mathematics', 'Mathématiques'),
        ('12:10', '12:40', C, 'en', 'National language and culture', 'Langue et culture nationale'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'en', 'English language (spelling and dictation)', 'Anglais'),
        ('13:40', '14:10', C, 'en', 'English language (extensive reading)', 'Anglais'),
        ('14:10', '14:40', K, None, 'Clubs', None),
        ('14:40', '15:10', K, None, 'Clubs', None),
    ],
    5: [
        ('07:20', '07:40', R, None, 'Morning devotion and inspection', None),
        ('07:40', '08:00', C, 'en', 'Social studies (moral education)', 'Éducation morale'),
        ('08:00', '08:30', C, 'en', 'Mathematics', 'Mathématiques'),
        ('08:30', '09:00', C, 'en', 'English language (vocabulary)', 'Anglais'),
        ('09:00', '09:30', C, 'en', 'Social studies (human rights)', 'Droits humains'),
        ('09:30', '10:00', C, 'en', 'English language (reading comprehension)', 'Anglais'),
        ('10:00', '10:30', C, 'en', 'Science and technology (health education)', 'Sciences et technologies'),
        ('10:30', '11:00', C, 'en', 'Vocational studies (agropastoral farming)', 'Métiers'),
        ('11:00', '11:10', P, None, 'Short break', None),
        ('11:10', '11:40', C, 'fr', 'Mathématiques (mesures et grandeurs)', 'Mathématiques'),
        ('11:40', '12:10', C, 'fr', 'Mathématiques (mesures et grandeurs)', 'Mathématiques'),
        ('12:10', '12:40', C, 'fr', 'Sciences et technologies', 'Sciences et technologies'),
        ('12:40', '13:10', P, None, 'Récréation', None),
        ('13:10', '13:40', C, 'fr', 'Éducation artistique (musique, dessin)', 'Éducation artistique'),
        ('13:40', '14:10', C, 'fr', 'Français (NCBS dictée)', 'Français'),
        ('14:10', '14:40', C, 'fr', 'T.I.C.E (informatique)', 'TIC'),
        ('14:40', '15:10', C, 'fr', 'Langue et culture nationale', 'Langue et culture nationale'),
    ],
}

# ─────────────── rattachement des leçons déjà importées ───────────────
# (titre, classe, matière du catalogue, chapitre = l'intitulé du cahier)
LECONS = [
    ('La Préhistoire', 'CM1', 'Histoire-Géographie', 'Histoire'),
    ('Les grandes inventions et les grandes découvertes', 'CM1', 'Histoire-Géographie', 'Histoire'),
    ('L’obéissance', 'CE1', 'Éducation morale', 'Éducation morale'),
    ('Le droit à l’identité', 'CE1', 'Droits humains', 'Droits et devoirs'),
    ('L’intégration nationale', 'CE1', 'Éducation civique', 'Éducation civique'),
    ('Les techniques de filtrage de l’eau', 'CE1', 'Sciences et technologies', 'Technologies'),
    # « Éducation à la paix » n'est pas une matière de l'emploi du temps : le
    # cahier la traite sous l'éducation morale. On garde son intitulé en
    # chapitre plutôt que d'inventer une matière que l'école n'a pas.
    ('La paix', 'CE1', 'Éducation morale', 'Éducation à la paix'),
    ('Le sol', 'CE1', 'Géographie', 'Géographie'),
]

CLASSES = [('CM1', MATIERES_CM1, CM1), ('CE1', MATIERES_CE1, CE1)]


def verifier():
    creneaux = 0
    for code, matieres, edt in CLASSES:
        libelles = {m[0] for m in matieres}
        assert len(libelles) == len(matieres), 'matière en double en ' + code
        for jour, liste in edt.items():
            assert 1 <= jour <= 5
            precedent = None
            for debut, fin, genre, langue, libelle, matiere in liste:
                creneaux += 1
                assert genre in (C, P, R, K), genre
                assert debut < fin, (code, jour, libelle)
                if precedent:
                    assert debut >= precedent, 'créneaux qui se chevauchent : %s j%d %s' % (code, jour, libelle)
                precedent = fin
                if genre == C:
                    assert matiere in libelles, 'matière inconnue en %s : %s' % (code, matiere)
                    assert langue in ('fr', 'en'), (code, libelle)
                else:
                    assert matiere is None and langue is None, (code, libelle)
    for titre, classe, matiere, chapitre in LECONS:
        cat = dict((c, [m[0] for m in ms]) for c, ms, _ in CLASSES)
        assert matiere in cat[classe], 'leçon « %s » : matière %s absente de %s' % (titre, matiere, classe)
    return creneaux


def json_sortie():
    return {
        'ecole': 'New Century Bilingual School, Yaoundé',
        'classes': [
            {
                'code': code,
                'equivalent_anglophone': 'Class 5' if code == 'CM1' else 'Class 3',
                'matieres': [
                    {'libelle': l, 'couleur': c, 'officiel_fr': f, 'officiel_en': e, 'intitules_cahier': a}
                    for l, c, f, e, a in matieres
                ],
                'emploi_du_temps': {
                    str(j): [
                        {'debut': d, 'fin': f, 'genre': g, 'langue': la, 'libelle': li, 'matiere': m}
                        for d, f, g, la, li, m in liste
                    ]
                    for j, liste in edt.items()
                },
            }
            for code, matieres, edt in CLASSES
        ],
        'lecons': [
            {'titre': t, 'classe': c, 'matiere': m, 'chapitre': ch} for t, c, m, ch in LECONS
        ],
    }


if __name__ == '__main__':
    creneaux = verifier()
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    io.open(os.path.join(racine, 'work', 'emplois-du-temps.json'), 'w', encoding='utf-8', newline='\n').write(
        json.dumps(json_sortie(), ensure_ascii=False, indent=1)
    )
    for code, matieres, edt in CLASSES:
        cours = sum(1 for j in edt.values() for c in j if c[2] == C)
        fr = sum(1 for j in edt.values() for c in j if c[2] == C and c[3] == 'fr')
        print('%s : %d matières, %d créneaux de cours (%d en français, %d en anglais)'
              % (code, len(matieres), cours, fr, cours - fr))
    print('%d créneaux au total, 8 leçons rattachées' % creneaux)
