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

Les voix doivent être dans le dossier passé en argument, nommées
`vivrieres-1.mp3` … `vivrieres-9.mp3` et `rente-1.mp3` … `rente-9.mp3`.
Le script refuse de monter s-il en manque une : un film amputé d-un plan
enseignerait une liste trouée, et c-est exactement ce qu-on cherche à
éviter en géographie.

Usage :  python work/monter-geo.py <dossier-des-voix>
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


def verifier_voix(source):
    """Toutes les voix doivent être là avant qu-on commence à monter."""
    manquantes = []
    for cle in FILMS:
        manifeste = json.load(io.open(
            os.path.join(_ICI, 'video-' + cle, 'script_manifest.json'), encoding='utf-8'))
        for i in range(1, len(manifeste['blocks']) + 1):
            chemin = os.path.join(source, '%s-%d.mp3' % (cle, i))
            if not os.path.exists(chemin):
                manquantes.append(os.path.basename(chemin))
    assert not manquantes, 'voix manquantes : ' + ', '.join(manquantes)


def monter(cle, blocs, source, sortie):
    morceaux, total = [], 0.0
    for i, bloc in enumerate(blocs, start=1):
        base = os.path.join(source, '%s-%d' % (cle, i))
        voix = duree(base + '.mp3')
        longueur = max(DUREE_MIN, voix + RESPIRATION)
        total += longueur

        muet = base + '-muet.mp4'
        motion.rendre_plan(bloc, longueur, muet)

        plan = base + '-monte.mp4'
        subprocess.run([
            FFMPEG, '-y', '-loglevel', 'error',
            '-i', muet, '-i', base + '.mp3',
            '-filter_complex',
            # La voix part après un souffle : le premier mot doit être à
            # l-écran avant d-être prononcé.
            '[1:a]adelay=250|250,apad,atrim=0:%.2f,asetpts=N/SR/TB[a]' % longueur,
            '-map', '0:v', '-map', '[a]', '-t', '%.2f' % longueur,
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k', '-ar', '44100',
            plan,
        ], check=True)
        morceaux.append(plan)

    liste = os.path.join(source, cle + '-liste.txt')
    io.open(liste, 'w', encoding='utf-8', newline='\n').write(
        '\n'.join("file '%s'" % os.path.abspath(m).replace('\\', '/') for m in morceaux) + '\n')
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0',
                    '-i', liste, '-c', 'copy', sortie], check=True)
    return total


if __name__ == '__main__':
    source = sys.argv[1]
    motion.controler()
    verifier_voix(source)
    for cle in FILMS:
        manifeste = json.load(io.open(
            os.path.join(_ICI, 'video-' + cle, 'script_manifest.json'), encoding='utf-8'))
        sortie = os.path.join(source, 'film-' + cle + '.mp4')
        secondes = monter(cle, manifeste['blocks'], source, sortie)
        print('%-10s %2d plans  %5.1f s  %6.1f Ko  %s'
              % (cle, len(manifeste['blocks']), secondes,
                 os.path.getsize(sortie) / 1024, manifeste['title']))
