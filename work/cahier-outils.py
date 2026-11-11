# -*- coding: utf-8 -*-
"""
L-outillage commun aux cahiers du jour : l-écriture courte des questions, le
chargement d-un lot en plusieurs parties, le vérificateur et le paquet.

Écrit pour le cahier de BRAYNE, repris tel quel pour celui de KLEIN : deux
lots qui auraient chacun leur vérificateur finiraient par ne plus vérifier la
même chose. Chaque lot garde son propre fichier, mince, qui dit seulement à
qui il est, quelles parties il charge et où il écrit.
"""

import io
import json
import os

NIVEAUX_ATTENDUS = {1, 2, 3, 4}

# Ce que le clavier de l-app sait écrire. Le « û » n-y est pas : « fûmes » et
# « eûmes » ne peuvent donc pas être des réponses à taper.
TAPABLE = set('abcdefghijklmnopqrstuvwxyzéèêàçùœâîôëïü0123456789.,-’')

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


def S(titre, *couples):
    """Deux colonnes dont celle de gauche porte un SIGNE, écrit en grand.

    À la taille d-un mot, un point, une virgule et deux points sont trois
    grains de poussière : on ne les distingue pas, alors que la fiche est là
    pour les faire reconnaître.
    """
    return ('signes', titre, list(couples))


def N(kind, phrase, cle, figure, e1, e2, *items):
    return (kind, phrase, cle, figure, [e1, e2], list(items))


def L(matiere, titre, chapitre, date, resume, cle, mots, *notions):
    return (matiere, titre, chapitre, date, resume, cle, list(mots), list(notions))


def charger(dossier, parties):
    """Lit les parties d-un lot. Chacune pose une liste LECONS."""
    lecons = []
    outils = dict(Q=Q, V=V, T=T, A=A, C=C, F=F, P=P, S=S, N=N, L=L)
    # Pendant l-écriture d-une partie, on peut ne charger qu-elle :
    #   PARTIES_SEULES=1 python work/lecons-….py
    seules = os.environ.get('PARTIES_SEULES')
    for nom in parties:
        if seules and not any(('-%s-' % n) in nom for n in seules.split(',')):
            continue
        espace = dict(outils)
        chemin = os.path.join(dossier, nom)
        exec(compile(io.open(chemin, encoding='utf-8').read(), chemin, 'exec'), espace)
        lecons.extend(espace['LECONS'])
    return lecons


def _decrire(figure):
    if figure[0] == 'fiche':
        return 'Fiche « %s » : %s.' % (figure[1], ' ; '.join(figure[2]))
    return 'Deux colonnes « %s » : %s.' % (
        figure[1], ' ; '.join('%s et %s' % c for c in figure[2]))


def verifier(LECONS, matieres, dates):
    """Une erreur ici deviendrait une question fausse posée à un enfant."""
    cles, total, notions_vues, trous = set(), 0, 0, 0
    titres = [l[1] for l in LECONS]
    assert len(set(titres)) == len(titres), 'titre en double'

    for matiere, titre, chapitre, date, resume, img, mots, notions in LECONS:
        assert matiere in matieres, matiere
        assert len(titre) <= 60, 'titre trop long : ' + titre
        assert len(resume) <= 400, 'résumé trop long (%d) : %s' % (len(resume), titre)
        assert len(date) == 10 and date.startswith(dates), date
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


def paquet(LECONS, matiere, classe, enfant, figure, langue='fr'):
    return {
        'matiere': matiere, 'classe': classe, 'enfant': enfant, 'lang': langue,
        'lecons': [
            {
                'title': titre, 'chapter': chapitre, 'taught_on': date, 'sort_order': rang,
                'summary': resume, 'illustration': img,
                'illustration_prompt': figure + 'Couverture : ' + ', '.join(mots) + '.',
                'notions': [
                    {
                        'kind': k, 'statement': p, 'illustration': ni,
                        'illustration_prompt': figure + _decrire(fig),
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
