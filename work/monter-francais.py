# -*- coding: utf-8 -*-
"""
Le montage des films de français.

Même principe que work/monter-films.py, à ceci près qu'il n'y a pas d'image à
recadrer : chaque plan est rendu de toutes pièces par work/motion-texte.py, à
la durée exacte que demande sa réplique.

La voix prime, comme pour les films de science : un plan ne descend jamais
sous cinq secondes, et s'allonge autant qu'il faut pour que la phrase soit
dite en entier.

Usage :  python work/monter-francais.py <dossier-des-voix>
"""

import io
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util

_spec = importlib.util.spec_from_file_location(
    'motion_texte', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'motion-texte.py'))
motion = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(motion)

import imageio_ffmpeg  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
RESPIRATION = 1.0
DUREE_MIN = 5.0
FILMS = ('pronoms', 'phrase', 'pluriel')


def duree(fichier):
    sortie = subprocess.run([FFMPEG, '-i', fichier], capture_output=True,
                            text=True, errors='ignore').stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', sortie).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


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
            # l'écran avant d'être prononcé.
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
    racine = os.path.dirname(os.path.abspath(__file__))
    for cle in FILMS:
        manifeste = json.load(io.open(
            os.path.join(racine, 'video-' + cle, 'script_manifest.json'), encoding='utf-8'))
        sortie = os.path.join(source, 'film-' + cle + '.mp4')
        secondes = monter(cle, manifeste['blocks'], source, sortie)
        print('%-10s %2d plans  %5.1f s  %6.1f Ko  %s'
              % (cle, len(manifeste['blocks']), secondes,
                 os.path.getsize(sortie) / 1024, manifeste['title']))
