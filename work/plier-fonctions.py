# -*- coding: utf-8 -*-
"""
Rend chaque fonction Edge autonome, à partir d-une source unique.

Le socle commun vit dans supabase/functions/_shared/maison.ts. C-est le
seul endroit où on l-écrit : les règles qu-il porte ont été apprises une par
une, et deux copies éditables finiraient par diverger sans que personne ne
le voie.

Mais l-éditeur du tableau de bord Supabase range les fichiers à plat sous la
fonction : un import « ../_shared/… » n-y existe pas. Chaque fonction reçoit
donc une COPIE du socle, posée à côté de son index.ts et importée en
« ./maison.ts ». Autonome, elle se déploie aussi bien par la ligne de
commande que par le navigateur.

La copie porte un en-tête qui dit de ne pas l-éditer, et `verifier()` refuse
si elle a dérivé de la source. C-est ce contrôle qui rend la duplication
acceptable : elle est visible et elle est tenue.

Usage :  python work/plier-fonctions.py           copie et vérifie
         python work/plier-fonctions.py --verifier vérifie seulement
"""

import io
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, 'supabase', 'functions', '_shared', 'maison.ts')
FONCTIONS = ('analyze-document', 'write-questions')

ENTETE = """// COPIE GÉNÉRÉE — NE PAS ÉDITER.
// La source est supabase/functions/_shared/maison.ts ; cette copie existe
// parce que l-éditeur du tableau de bord range les fichiers à plat sous la
// fonction et n-y connaît pas « ../_shared/ ».
// Régénérer avec :  python work/plier-fonctions.py
"""


def chemin(nom):
    return os.path.join(RACINE, 'supabase', 'functions', nom, 'maison.ts')


def attendu():
    return ENTETE + '\n' + io.open(SOURCE, encoding='utf-8').read()


def ecrire():
    contenu = attendu()
    for nom in FONCTIONS:
        io.open(chemin(nom), 'w', encoding='utf-8', newline='\n').write(contenu)
    return len(FONCTIONS)


def verifier():
    """Une copie qui a dérivé de sa source ne se corrige pas, elle se refait."""
    voulu = attendu()
    for nom in FONCTIONS:
        p = chemin(nom)
        assert os.path.exists(p), 'copie absente : ' + nom + '/maison.ts'
        assert io.open(p, encoding='utf-8').read() == voulu, \
            ('la copie %s/maison.ts a dérivé de la source. '
             'Éditer _shared/maison.ts, puis relancer work/plier-fonctions.py' % nom)

    # Et l-import doit pointer sur la copie, sinon le déploiement par le
    # navigateur casse sans rien dire ici.
    for nom in FONCTIONS:
        index = io.open(os.path.join(RACINE, 'supabase', 'functions', nom, 'index.ts'),
                        encoding='utf-8').read()
        assert "'../_shared/maison.ts'" not in index, \
            nom + '/index.ts importe encore ../_shared : il doit importer ./maison.ts'
        assert "'./maison.ts'" in index, nom + '/index.ts n-importe pas ./maison.ts'
    return len(FONCTIONS)


if __name__ == '__main__':
    if '--verifier' not in sys.argv:
        ecrire()
    n = verifier()
    print('%d fonctions autonomes, copies conformes a la source' % n)
