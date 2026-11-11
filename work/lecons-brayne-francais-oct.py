# -*- coding: utf-8 -*-
"""
Le cahier du jour de BRAYNE (CM1), du 2 au 29 octobre 2026 — soixante-dix-sept
pages photographiées le 11 novembre : vingt-cinq leçons de français et cinq de
TIC.

RIEN N-EST AJOUTÉ AU CAHIER : chaque notion reprend une phrase qu-il a copiée,
avec ses exemples.

DEUX LEÇONS SONT ÉCRITES DEPUIS DES DEVOIRS CORRIGÉS, et pas depuis une page
de cours : l-infinitif et les groupes de verbes, puis en TIC les
périphériques, la saisie kilométrique et l-ENIAC. Ces cours datent de
septembre et n-ont pas été photographiés ; les corrections de la maîtresse
donnent les réponses. Ces deux leçons ne disent rien que la copie corrigée ne
dise.

LES QUESTIONS PÈSENT SUR LES CONFUSIONS QUE LES EXERCICES TRAVAILLENT : le
passé simple contre le passé composé, « on n- » devant « rien », les
homonymes, les périphériques de stockage contre ceux d-entrée.

LES NOTES DE LECTURE DU CAHIER NE SONT PAS DANS LE DÉPÔT. Elles contiennent
les copies de l-enfant et restent sur la machine du parent.

UNE SEULE SOURCE POUR LES QUESTIONS ET POUR LES IMAGES. Chaque notion porte
ici la description de sa fiche ; work/figures-brayne-francais-oct.py la
dessine depuis ce même fichier. Une image ne peut donc pas dire autre chose
que la leçon.

Le rang écrit dans le paquet n-est qu-un ordre : le script d-insertion le
recale après le dernier rang de la classe, qu-il lit en base.

Usage :  python work/lecons-brayne-francais-oct.py
"""

import io
import json
import os

FIGURE = ('Figure composée, non générée, dessinée par '
          'work/figures-brayne-francais-oct.py. ')

CLASSE = 'CM1'
ENFANT = 'BRAYNE'
LANGUE = 'fr'
NIVEAUX_ATTENDUS = {1, 2, 3, 4}

# Ce que le clavier de l-app sait écrire. Le « û » n-y est pas : « fûmes » et
# « eûmes » ne peuvent donc pas être des réponses à taper.
TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

_ICI = os.path.dirname(os.path.abspath(__file__))
PARTIES = [
    'brayne-fr-oct-1-conjugaison.py',
    'brayne-fr-oct-2-grammaire.py',
    'brayne-fr-oct-3-orthographe.py',
    'brayne-fr-oct-4-vocabulaire-ecrits.py',
    'brayne-fr-oct-5-tic.py',
]


# --------------------------------------------------------------------------
# L-écriture courte des questions. La bonne réponse d-un QCM est toujours la
# première : l-application mélange les choix avant de les montrer.

def _phrase(mot):
    return mot[:1].upper() + mot[1:] + ('' if mot[-1:] in '.!?…' else '.')


def Q(question, bonne, *autres, n=1, e=None):
    return ('qcm', n, {'question': question, 'options': [bonne] + list(autres)},
            {'index': 0}, e or _phrase(bonne))


def V(affirmation, vrai, n=1, e=None):
    return ('vrai_faux', n, {'statement': affirmation}, {'value': vrai},
            e or ('Oui.' if vrai else 'Non.'))


def T(texte, *valeurs, n=2, e=None):
    plein = texte
    for i, v in enumerate(valeurs):
        plein = plein.replace('{{%d}}' % (i + 1), v)
    return ('texte_a_trous', n, {'text': texte, 'blanks': len(valeurs)},
            {'values': list(valeurs)}, e or plein)


def A(question, *couples, n=3, e=None):
    return ('association', n,
            {'question': question, 'gauche': [g for g, _d in couples],
             'droite': [d for _g, d in couples]},
            {'order': list(range(len(couples)))},
            e or ' ; '.join('%s → %s' % c for c in couples) + '.')


def C(question, *jetons, n=3, e=None):
    return ('chronologie', n, {'question': question, 'tokens': list(jetons)},
            {'order': list(range(len(jetons)))}, e or ', puis '.join(jetons) + '.')


def F(titre, *lignes, vif=()):
    """La fiche : un titre et des lignes, comme au cahier."""
    return ('fiche', titre, list(lignes), tuple(vif))


def P(titre, *couples):
    """Deux colonnes reliées."""
    return ('paire', titre, list(couples))


def N(kind, phrase, cle, figure, e1, e2, *items):
    return (kind, phrase, cle, figure, [e1, e2], list(items))


def L(matiere, titre, chapitre, date, resume, cle, mots, *notions):
    return (matiere, titre, chapitre, date, resume, cle, list(mots), list(notions))


def charger():
    lecons = []
    outils = dict(Q=Q, V=V, T=T, A=A, C=C, F=F, P=P, N=N, L=L)
    # Pendant l-écriture d-une partie, on peut ne charger qu-elle :
    #   PARTIES_SEULES=1 python work/lecons-brayne-francais-oct.py
    seules = os.environ.get('PARTIES_SEULES')
    for nom in PARTIES:
        if seules and not any(('-%s-' % n) in nom for n in seules.split(',')):
            continue
        espace = dict(outils)
        chemin = os.path.join(_ICI, nom)
        exec(compile(io.open(chemin, encoding='utf-8').read(), chemin, 'exec'), espace)
        lecons.extend(espace['LECONS'])
    return lecons


LECONS = charger()


def _decrire(figure):
    if figure[0] == 'fiche':
        return 'Fiche « %s » : %s.' % (figure[1], ' ; '.join(figure[2]))
    return 'Deux colonnes « %s » : %s.' % (
        figure[1], ' ; '.join('%s et %s' % c for c in figure[2]))


def verifier():
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues, trous = set(), 0, 0, 0
    titres = [l[1] for l in LECONS]
    assert len(set(titres)) == len(titres), 'titre en double'

    for matiere, titre, chapitre, date, resume, img, mots, notions in LECONS:
        assert matiere in ('Français', 'TIC'), matiere
        assert len(titre) <= 60, 'titre trop long : ' + titre
        assert len(resume) <= 400, 'résumé trop long (%d) : %s' % (len(resume), titre)
        assert len(date) == 10 and date.startswith('2026-10-'), date
        assert img not in cles, 'image en double : ' + img
        assert all(c.islower() or c.isdigit() or c == '-' for c in img), img
        cles.add(img)
        assert 2 <= len(mots) <= 4, 'couverture : deux à quatre mots : ' + titre
        for m in mots:
            assert len(m) <= 22, 'mot de couverture trop long : ' + m
        assert 2 <= len(notions) <= 6, 'nombre de notions : ' + titre
        for kind, phrase, nimg, figure, expl, items in notions:
            notions_vues += 1
            assert kind in ('definition', 'date', 'liste', 'relation'), kind
            assert len(phrase) <= 180, 'notion trop longue (%d) : %s' % (len(phrase), phrase)
            assert nimg not in cles, 'image en double : ' + nimg
            assert all(c.islower() or c.isdigit() or c == '-' for c in nimg), nimg
            cles.add(nimg)
            if figure[0] == 'fiche':
                assert len(figure[1]) <= 30, 'titre de fiche trop long : ' + figure[1]
                assert 1 <= len(figure[2]) <= 5, 'fiche : une à cinq lignes : ' + nimg
                for ligne in figure[2]:
                    assert len(ligne) <= 38, 'ligne de fiche trop longue : ' + ligne
            else:
                assert len(figure[1]) <= 30, 'titre de paire trop long : ' + figure[1]
                assert 2 <= len(figure[2]) <= 4, 'paire : deux à quatre lignes : ' + nimg
                for g, d in figure[2]:
                    assert len(g) <= 20 and len(d) <= 20, 'mot de paire trop long : %s / %s' % (g, d)
            assert len(expl) == 2, phrase
            for registre, corps in expl:
                assert registre in ('simple', 'analogie', 'histoire', 'visuel', 'pas_a_pas'), \
                    registre
                assert len(corps) <= 200, 'explication trop longue : ' + corps
            niveaux = set()
            questions = set()
            for ikind, niveau, payload, answer, explain in items:
                total += 1
                niveaux.add(niveau)
                textes = json.dumps([payload, answer, explain], ensure_ascii=False)
                assert "'" not in textes, 'apostrophe droite interdite : ' + textes
                enonce = json.dumps(payload, ensure_ascii=False, sort_keys=True)
                assert enonce not in questions, 'question en double : ' + enonce
                questions.add(enonce)
                if niveau == 4:
                    assert ikind in ('qcm', 'vrai_faux'), 'type trop lent pour le Défi : ' + ikind
                if ikind == 'qcm':
                    assert len(payload['question']) <= 90, \
                        'question trop longue (%d) : %s' % (len(payload['question']),
                                                            payload['question'])
                    options = payload['options']
                    assert 2 <= len(options) <= 4, payload
                    assert len(set(options)) == len(options), 'option en double : ' + str(payload)
                    for o in options:
                        assert len(o) <= 70, 'option trop longue : ' + o
                    bonne = len(options[0])
                    autres = [len(o) for o in options[1:]]
                    assert bonne <= max(autres) * 2, \
                        'bonne réponse bien plus longue que les autres : ' + payload['question']
                elif ikind == 'vrai_faux':
                    assert isinstance(answer['value'], bool), payload
                    assert len(payload['statement']) <= 110, \
                        'affirmation trop longue (%d) : %s' % (len(payload['statement']),
                                                               payload['statement'])
                elif ikind == 'texte_a_trous':
                    trous += 1
                    n = payload['text'].count('{{')
                    assert n == len(answer['values']) == payload['blanks'], payload
                    assert 1 <= n <= 2, 'un ou deux trous : ' + payload['text']
                    for v in answer['values']:
                        assert v == v.strip() != '', 'réponse mal cadrée : ' + repr(v)
                        assert set(v) <= TAPABLE, 'réponse non tapable au clavier : ' + v
                elif ikind == 'chronologie':
                    assert 3 <= len(payload['tokens']) <= 6, payload
                    assert len(set(payload['tokens'])) == len(payload['tokens']), \
                        'jeton en double : ' + str(payload['tokens'])
                elif ikind == 'association':
                    assert 2 <= len(payload['gauche']) <= 4, payload
                    assert len(set(payload['droite'])) == len(payload['droite']), \
                        'deux étiquettes identiques à droite : ' + str(payload['droite'])
                    assert len(set(payload['gauche'])) == len(payload['gauche']), payload
                else:
                    raise AssertionError('type non jouable : ' + ikind)
            assert niveaux == NIVEAUX_ATTENDUS, \
                'étapes manquantes sur « %s » : %s' % (phrase, sorted(niveaux))
    return len(cles), total, notions_vues, trous


def paquet(matiere):
    return {
        'matiere': matiere, 'classe': CLASSE, 'enfant': ENFANT, 'lang': LANGUE,
        'lecons': [
            {
                'title': titre, 'chapter': chapitre, 'taught_on': date, 'sort_order': rang,
                'summary': resume, 'illustration': img,
                'illustration_prompt': FIGURE + 'Couverture : ' + ', '.join(mots) + '.',
                'notions': [
                    {
                        'kind': k, 'statement': p, 'illustration': ni,
                        'illustration_prompt': FIGURE + _decrire(fig),
                        'explanations': [{'register': r, 'body': b} for r, b in ex],
                        'items': [{'kind': ik, 'level': lv, 'payload': pl,
                                   'answer': an, 'explain': exp}
                                  for ik, lv, pl, an, exp in it],
                    }
                    for k, p, ni, fig, ex, it in notions
                ],
            }
            for rang, (m, titre, chapitre, date, resume, img, mots, notions) in enumerate(
                sorted((l for l in LECONS if l[0] == matiere), key=lambda l: l[3]), 1)
        ],
    }


if __name__ == '__main__':
    images, items, notions, trous = verifier()
    racine = os.path.dirname(_ICI)
    for matiere, fichier in (('Français', 'seed-brayne-francais-oct.json'),
                             ('TIC', 'seed-brayne-tic-oct.json')):
        chemin = os.path.join(racine, 'app', 'public', fichier)
        io.open(chemin, 'w', encoding='utf-8', newline='\n').write(
            json.dumps(paquet(matiere), ensure_ascii=False))
        print(chemin)

    print('%d lecons - %d notions - %d questions dont %d a trous - %d images'
          % (len(LECONS), notions, items, trous, images))
    for m, titre, chapitre, date, _r, _i, _mots, ns in sorted(LECONS, key=lambda l: (l[0], l[3])):
        print('  %-9s %s  %-52s %d notions  %2d questions'
              % (m, date, titre, len(ns), sum(len(n[5]) for n in ns)))
