# -*- coding: utf-8 -*-
"""
Le montage des films de leçon, hors ligne.

Higgsfield fabrique les plans et la voix ; ce script fait le reste, avec le
ffmpeg livré par imageio-ffmpeg. Tout se passe donc sur la machine : on peut
recouper, corriger un mot ou refaire une bande sans repayer une génération.

Le mouvement vient d'ici, pas d'un générateur : une approche de six pour cent
sur la durée du plan. C'est un choix fait après avoir perdu soixante-cinq
crédits à animer treize fois la même image — l'envoi du fichier de départ ne
prenait qu'à la première génération, et rien dans le solde ne le disait. Un
mouvement calculé localement ne peut pas se tromper d'image, ne coûte rien, et
se refait autant de fois qu'on veut.

Ce qui est posé par-dessus l'image, jamais dedans :

  · Niba, dessiné par work/niba.py d'après le SVG de l'application, avec son
    humeur du plan. L'enfant voit le même lionceau dans le film et dans son
    espace.
  · La phrase dite, dans une bande blanche au bas du cadre. Elle double la
    voix, elle ne la remplace pas : le film sera regardé dans un transport ou
    sur un téléphone partagé au haut-parleur faible.
  · Les mots du cahier, en capitales, en haut à droite.

Une règle de durée : la voix prime. Un plan dure cinq secondes, une réplique
peut en durer sept ; on prolonge alors le plan sur sa dernière image plutôt
que de couper la phrase ou d'accélérer la parole.

Usage :  python work/monter-films.py <dossier-des-plans>
"""

import io
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from niba import dessiner  # noqa: E402

import imageio_ffmpeg  # noqa: E402

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
LARGEUR, HAUTEUR = 1280, 720
MARGE = 36
RESPIRATION = 1.0  # le silence laissé après la dernière syllabe
DUREE_MIN = 5.0    # un plan ne passe jamais sous cinq secondes

INK = (43, 64, 71, 255)
WHITE_WARM = (255, 251, 244, 240)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fredoka.ttf')


def duree(fichier):
    sortie = subprocess.run([FFMPEG, '-i', fichier], capture_output=True,
                            text=True, errors='ignore').stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', sortie)
    h, mn, s = m.groups()
    return int(h) * 3600 + int(mn) * 60 + float(s)


def _coupe(texte, police, largeur_max, dessin):
    lignes, courante = [], ''
    for mot in texte.split():
        essai = (courante + ' ' + mot).strip()
        if dessin.textlength(essai, font=police) <= largeur_max:
            courante = essai
        else:
            if courante:
                lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def calque(phrase, mots, humeur):
    """Niba, sa phrase et les mots du cahier, sur un fond transparent."""
    img = Image.new('RGBA', (LARGEUR, HAUTEUR), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Les mots du cahier, en haut à droite.
    pm = ImageFont.truetype(POLICE, 34)
    x = LARGEUR - MARGE
    for mot in reversed(mots):
        l = d.textlength(mot, font=pm)
        d.rounded_rectangle([x - l - 34, MARGE, x, MARGE + 54], radius=27, fill=WHITE_WARM)
        d.text((x - l - 17, MARGE + 10), mot, font=pm, fill=INK)
        x -= l + 34 + 10

    # Niba, dans le coin laissé libre par la génération.
    taille = 132
    nb = dessiner(humeur, taille)
    bas = HAUTEUR - MARGE - taille
    img.alpha_composite(nb, (MARGE, bas))

    # La phrase dite, dans une bande qui part de Niba.
    pp = ImageFont.truetype(POLICE, 33)
    gauche = MARGE + taille + 16
    largeur_bande = LARGEUR - MARGE - gauche
    lignes = _coupe(phrase, pp, largeur_bande - 48, d)
    hauteur_bande = 26 + 42 * len(lignes)
    haut = HAUTEUR - MARGE - hauteur_bande
    d.rounded_rectangle([gauche, haut, LARGEUR - MARGE, haut + hauteur_bande],
                        radius=24, fill=WHITE_WARM)
    for i, ligne in enumerate(lignes):
        d.text((gauche + 24, haut + 13 + i * 42), ligne, font=pp, fill=INK)

    return img


def monter(cle, titre, blocs, source, sortie):
    morceaux = []
    total = 0.0
    for i, bloc in enumerate(blocs, start=1):
        base = os.path.join(source, '%s-%d' % (cle, i))
        voix = duree(base + '.mp3')
        longueur = max(DUREE_MIN, voix + RESPIRATION)
        total += longueur

        png = base + '-calque.png'
        calque(bloc['vo_line'], bloc['keywords'], bloc['niba']).save(png)

        plan = base + '-monte.mp4'
        images = int(round(longueur * 24))
        subprocess.run([
            FFMPEG, '-y', '-loglevel', 'error',
            '-loop', '1', '-t', '%.2f' % longueur, '-i', base + '.png',
            '-i', png, '-i', base + '.mp3',
            '-filter_complex',
            # Un mouvement d'approche très lent, 6 % sur toute la durée du
            # plan : assez pour que l'image respire, assez peu pour qu'un
            # enfant ne le remarque pas et regarde ce qui est montré.
            '[0:v]scale=%d:-1,zoompan=z=min(zoom+0.00035\\,1.06):d=%d'
            ':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=%dx%d:fps=24[v];'
            '[v][1:v]overlay=0:0[vo];'
            # La voix part après un souffle, pour ne pas mordre sur le début du plan.
            '[2:a]adelay=250|250,apad,atrim=0:%.2f,asetpts=N/SR/TB[a]'
            % (LARGEUR * 2, images, LARGEUR, HAUTEUR, longueur),
            '-map', '[vo]', '-map', '[a]', '-t', '%.2f' % longueur,
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '24', '-pix_fmt', 'yuv420p',
            '-c:a', 'aac', '-b:a', '96k', '-ar', '44100',
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
    for cle in ('reproduction', 'soins', 'milieux'):
        manifeste = json.load(io.open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'video-' + cle,
                         'script_manifest.json'), encoding='utf-8'))
        sortie = os.path.join(source, 'film-' + cle + '.mp4')
        secondes = monter(cle, manifeste['title'], manifeste['blocks'], source, sortie)
        print('%-14s %2d plans  %5.1f s  %6.1f Ko  %s'
              % (cle, len(manifeste['blocks']), secondes,
                 os.path.getsize(sortie) / 1024, manifeste['title']))
