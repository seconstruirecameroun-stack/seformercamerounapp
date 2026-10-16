# La charte des films

Un film dure une minute et se regarde avant la première question. Il n'est pas
là pour décorer la leçon : il est là pour que l'enfant ait **déjà vu** ce qu'on
va lui demander. Tout ce qui suit découle de cela.

Deux règles ont été ajoutées le 16 octobre 2026, après le premier lot de films.
Elles ne sont pas des préférences de style : chacune corrige une faute
constatée à l'écran.

---

## 1. Niba explique

Jusqu'ici les films étaient une voix sur des images. L'enfant écoutait
quelqu'un qu'il ne connaissait pas.

Niba est le seul personnage auquel il s'attache — c'est lui qui le félicite,
c'est lui qui dit « tu m'as manqué » après trois jours. Si le film est
expliqué par Niba, la leçon n'arrive plus d'un inconnu : elle arrive de
quelqu'un avec qui l'enfant a déjà une histoire.

**Niba est dessiné, jamais généré.** Il existe en SVG dans
`app/src/components/jeu/Mascotte.tsx`, et c'est cette définition-là qui fait
foi. Un générateur d'images rendrait un lionceau différent à chaque plan ;
l'enfant verrait six lions, pas Niba. Le film doit donc être composé en code,
avec le même tracé :

| Élément    | Définition                                                                 |
|------------|----------------------------------------------------------------------------|
| Crinière   | 9 cercles r=16, centres sur un cercle r=36 autour de (60,62), `clay` / `gold` en alternance |
| Oreilles   | r=12 en (28,33) et (92,33), `clay-dark`, pastille interne r=6 `sand`        |
| Face       | cercle r=34 en (60,62), `sand`                                              |
| Yeux       | points r=5 en (47,58) et (73,58), `ink`, reflet blanc en haut à gauche      |
| Museau     | ellipse 26×18 en (60,72), `white-warm`, truffe `clay-dark`                  |
| Moustaches | deux traits par côté, `ink-2`, opacité 0,55                                 |

Humeurs disponibles : `content`, `fete`, `encourage`, `manque`, `dort`. Le
clignement est **irrégulier** — à intervalle fixe, l'œil devient un métronome
et le personnage a l'air mécanique.

Ce qu'il ne fait pas : il ne récite pas la leçon à la place de l'image. Quand
il nomme la Sanaga, la Sanaga est à l'écran au moment où le mot tombe. Sa
bulle porte la phrase, l'image porte la preuve.

---

## 2. Un lieu nommé est le vrai lieu

Le film sur les bassins hydrographiques disait « le Logone arrose Maroua » et
montrait *a broad river in a dry savannah passing beside a small town with low
houses, acacia trees and boats*. C'est une savane. Ce n'est pas Maroua, ce
n'est pas l'Extrême-Nord, ce n'est nulle part.

Un enfant de Yaoundé qui apprend son pays mérite mieux qu'un décor
interchangeable. Et un enfant de Maroua qui regarde ce plan ne reconnaît pas
chez lui — ce qui est pire que de ne rien montrer.

**Donc : dès qu'une leçon nomme un lieu, le plan montre ce lieu.** Pas « une
ville africaine ». Pas « un fleuve en Afrique ». Le Cameroun a cinq paysages
distincts et un enfant d'ici les distingue du premier coup d'œil.

### Les cinq paysages

**Extrême-Nord — sahélien.** Plaine plate couleur ocre, ciel pâle chargé de
poussière, acacias épineux à cime plate et clairsemés, dômes de granit des
monts Mandara à l'ouest, cases coniques en terre à toit de chaume pointu,
greniers à mil, zébus à bosse et longues cornes. *Maroua, Kousséri, Mokolo,
le Logone, le lac Tchad.*

**Nord — soudanien.** Hautes herbes dorées, arbres larges et espacés, fleuve
large découvrant des bancs de sable en saison sèche, pirogues de bois à
l'embarcadère. *Garoua, la Bénoué, Lagdo.*

**Adamaoua — plateau.** Hauts plateaux verts et vallonnés, troupeaux, air plus
frais, sources des grands fleuves. *Ngaoundéré, le Djérem, la Vina.*

**Centre, Sud, Littoral — forestier et côtier.** Forêt dense verte, palmiers à
huile, terre latéritique rouge, fleuve large et brun, mangroves à
l'embouchure, cône sombre du mont Cameroun sur l'horizon côtier. *Yaoundé,
Douala, Édéa, Kribi, la Sanaga, le Nyong, le Wouri.*

**Est — équatorial.** Forêt très dense et sombre, arbres émergents très hauts,
eau lente et noire sous l'ombre. *Yokadouma, le Dja, la Ngoko, la Sangha.*

### Les cours d'eau, tels qu'ils coulent

Une carte dessinée en code est **juste par construction** ; une carte générée
est une supposition. Pour les leçons de géographie, on dessine.

- **Logone** — naît sur l'Adamaoua, remonte vers le **nord** le long de la
  frontière orientale, rejoint le Chari puis le lac Tchad à la pointe du pays.
- **Bénoué** — naît sur l'Adamaoua au nord-est de Ngaoundéré, monte vers le
  nord jusqu'à Lagdo, puis **oblique vers l'ouest** à Garoua et sort au
  Nigeria. Affluents : le Faro par le sud, le Mayo Rey et le **Mayo Kébi** par
  l'est.
- **Sanaga** — naît sur l'Adamaoua, traverse le centre vers le **sud-ouest**,
  passe Édéa, atteint l'Atlantique juste au sud de Douala. C'est le plus long
  fleuve du pays.
- **Dja** — descend vers le **sud-est** sous la forêt, devient la Ngoko, puis
  la Sangha, et s'en va vers le Congo.

Repères (longitude, latitude) : lac Tchad 14,4 / 12,9 · Maroua 14,3 / 10,6 ·
Garoua 13,4 / 9,3 · Ngaoundéré 13,6 / 7,3 · Yaoundé 11,5 / 3,9 · Douala
9,7 / 4,0 · Édéa 10,1 / 3,8 · Yokadouma 15,0 / 3,5 · mont Cameroun 9,2 / 4,2.
Le pays tient entre 8,5° et 16,2° de longitude est, 1,6° et 13,1° de latitude
nord : étroit et pointu au nord, large au sud, renflé à l'ouest sur la côte.

---

## Ce qui ne change pas

- **Une seule idée par plan**, et ce qui est dit est montré.
- **Pas de texte dans une image générée.** Les mots sont posés par-dessus :
  on corrige un mot sans repayer une image, et le même plan sert en français
  comme en anglais.
- **Aucune personne réelle, aucune marque, aucune enseigne lisible.**
- **Le film se comprend sans le son.** Il sera regardé sur un téléphone
  partagé, souvent en silence, parfois dans un transport.
- **Rien sous 17 px.** Un enfant lit à bout de bras, en plein jour.
- Palette : `ink`, `ink-2`, `white-warm`, `sand`, `clay`, `clay-dark`, `gold`,
  `leaf`, `sky`, `mint`, `lilac`. Pas d'autre couleur.

---

## Chaîne de production

L'ancienne chaîne passait par des images générées puis une voix off. Le
connecteur de génération d'images n'est plus accessible depuis l'atelier, et
de toute façon il ne savait tenir ni Niba ni la géographie.

La chaîne retenue compose **en code** : Niba exact à chaque image, fleuves à
leur place, texte net et corrigeable. Le prix à payer est la voix, qui ne se
génère pas par ce canal — Niba parle donc en bulles, ce que la règle « le film
se comprend sans le son » rendait de toute façon nécessaire.

Les scripts verrouillés restent dans `work/video-*/script.md`, et
`work/films-*.py` reste la source : on y écrit la narration, le plan et les
mots affichés, et le script régénère le manifeste.
