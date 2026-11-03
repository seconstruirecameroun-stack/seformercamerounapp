# -*- coding: utf-8 -*-
"""
Le montage des deux films de géographie.

Même principe que work/monter-sciences.py : chaque plan est rendu de toutes
pièces, à la durée exacte que demande sa réplique. Seules les scènes
changent — work/motion-geo.py allume des régions là où les sciences
faisaient tourner un cycle de l-eau.

La voix prime : un plan ne descend jamais sous cinq secondes, et s-allonge
autant qu-il faut pour que la phrase soit dite en entier. Les mouvements de
motion-geo.py sont calés pour être terminés vers trois secondes et demie,
donc l-image se stabilise avant la fin de la phrase — un plan qui bouge
encore quand la voix se tait donne l-impression qu-on a coupé trop tôt.

Les voix vivent à côté de leur script, dans `work/video-<film>/vo1.mp3` …
`vo9.mp3`, comme pour tous les films précédents. Elles sont hors de git —
trop lourdes — mais pas hors du projet : une voix rangée dans un dossier
temporaire se perd, et refaire le film coûterait une seconde fois des
crédits pour redire exactement les mêmes phrases.

Le script refuse de monter s-il en manque une : un film amputé d-un plan
enseignerait une liste trouée, et c-est exactement ce qu-on cherche à
éviter en géographie.

Usage :  python work/monter-geo.py [dossier-de-sortie]
"""

import importlib.util
import io
import json
import os
import re
import subprocess
import sys

_ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ICI)

_spec = importlib.util.spec_from_file_location(
    'motion_geo', os.path.join(_ICI, 'motion-geo.py'))
motion = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(motion)

import imageio_ffmpeg  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
RESPIRATION = 1.0
DUREE_MIN = 5.0
FILMS = ('vivrieres', 'rente')


def duree(fichier):
    sortie = subprocess.run([FFMPEG, '-i', fichier], capture_output=True,
                            text=True, errors='ignore').stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', sortie).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def voix(cle, i):
    return os.path.join(_ICI, 'video-' + cle, 'vo%d.mp3' % i)


def verifier_voix():
    """Toutes les voix doivent être là avant qu-on commence à monter."""
    manquantes = []
    for cle in FILMS:
        manifeste = json.load(io.open(
            os.path.join(_ICI, 'video-' + cle, 'script_manifest.json'), encoding='utf-8'))
        for i in range(1, len(manifeste['blocks']) + 1):
            if not os.path.exists(voix(cle, i)):
                manquantes.append('video-%s/vo%d.mp3' % (cle, i))
    assert not manquantes, 'voix manquantes : ' + ', '.join(manquantes)


def monter(cle, blocs, travail, sortie):
    morceaux, total = [], 0.0
    for i, bloc in enumerate(blocs, start=1):
        son = voix(cle, i)
        base = os.path.join(travail, '%s-%d' % (cle, i))
        longueur = max(DUREE_MIN, duree(son) + RESPIRATION)
        total += longueur

        muet = base + '-muet.mp4'
        motion.rendre_plan(bloc, longueur, muet)

        plan = base + '-monte.mp4'
        subprocess.run([
            FFMPEG, '-y', '-loglevel', 'error',
            '-i', muet, '-i', son,
            '-filter_complex',
            # La voix part après un souffle : le premier mot doit être à
            # l-écran avant d-être prononcé.
            '[1:a]adelay=250|250,apad,atrim=0:%.2f,asetpts=N/SR/TB[a]' % longueur,
            '-map', '0:v', '-map', '[a]', '-t', '%.2f' % longueur,
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k', '-ar', '44100',
            plan,
        ], check=True)
        morceaux.append(plan)

    liste = os.path.join(travail, cle + '-liste.txt')
    io.open(liste, 'w', encoding='utf-8', newline='\n').write(
        '\n'.join("file '%s'" % os.path.abspath(m).replace('\\', '/') for m in morceaux) + '\n')
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                    '-i', liste, '-c', 'copy', sortie], check=True)
    return total


if __name__ == '__main__':
    travail = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_ICI, 'video-sortie')
    os.makedirs(travail, exist_ok=True)
    motion.controler()
    verifier_voix()
    for cle in FILMS:
        manifeste = json.load(io.open(
            os.path.join(_ICI, 'video-' + cle, 'script_manifest.json'), encoding='utf-8'))
        sortie = os.path.join(travail, 'film-' + cle + '.mp4')
        secondes = monter(cle, manifeste['blocks'], travail, sortie)
        print('%-10s %2d plans  %5.1f s  %6.1f Ko  %s'
              % (cle, len(manifeste['blocks']), secondes,
                 os.path.getsize(sortie) / 1024, manifeste['title']))
