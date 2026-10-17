# La charte des films

Un film dure une minute et se regarde avant la première question. Il n'est pas
là pour décorer la leçon : il est là pour que l'enfant ait **déjà vu** ce qu'on
va lui demander. Tout ce qui suit découle de cela.

Deux règles ont été ajoutées le 16 octobre 2026, après le premier lot de films.
Elles ne sont pas des préférences de style : chacune corrige une faute
constatée à l'écran.

---

## 1. Niba explique

Jusqu'ici le film était une voix sur des images, et rien à l'écran ne
rattachait la leçon au reste de l'application.

Niba est le seul personnage auquel l'enfant s'attache — c'est lui qui le
félicite, c'est lui qui dit « tu m'as manqué » après trois jours. Sa présence
dans le film raccroche la leçon à quelqu'un que l'enfant connaît déjà.

**La narration reste Céline, et c'est Céline qui parle.** Niba est à l'écran,
pas dans le haut-parleur : il montre, il réagit, sa bulle reprend la phrase.
Il ne prend pas la voix.

Les deux directions ont été essayées sur la même phrase, le 17 octobre 2026,
sur « le Logone arrose Maroua ». La direction tenue a été retenue, et elle ne
change pas :

> `[native French educational narrator, pure French pronunciation, clean
> diction, calm and steady, starts speaking immediately]`

Le lionceau joué à la voix ajoutait de la bonhomie et retirait de la clarté.
Céline porte déjà les huit films existants : en changer ferait sonner la suite
comme un autre produit, et un enfant qui révise a d'abord besoin d'entendre
« Bénoué » et « Logone » prononcés net. La voix porte la leçon, Niba porte
l'attachement. Chacun son travail.

La musique et les bruits restent eux aussi. Un film muet n'est pas un film,
et un enfant de huit ans décroche d'une image qui ne fait pas de bruit.

**Niba est dessiné, jamais généré.** Il existe en SVG dans
`app/src/components/jeu/Mascotte.tsx`, et c'est cette définition-là qui fait
foi. Un générateur d'images rendrait un lionceau différent à chaque plan ;
l'enfant verrait six lions, pas Niba. Il est donc posé par l'application
par-dessus le plan, comme les mots-clés, avec le même tracé :

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
la Sanaga est nommée, la Sanaga est à l'écran au moment où le mot tombe. La
voix porte la phrase, l'image porte la preuve.

Une bulle double la voix à l'écran. Elle n'est pas là en remplacement du son
mais en plus : le film sera regardé dans un transport, en classe, sur un
téléphone partagé dont le haut-parleur est faible ou coupé.

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
- **Le film a une voix, une musique et des bruits**, et il se comprend quand
  même sans le son. Les deux, pas l'un ou l'autre : le son porte le film, la
  bulle le rattrape quand le téléphone est partagé ou coupé.
- **Rien sous 17 px.** Un enfant lit à bout de bras, en plein jour.
- Palette : `ink`, `ink-2`, `white-warm`, `sand`, `clay`, `clay-dark`, `gold`,
  `leaf`, `sky`, `mint`, `lilac`. Pas d'autre couleur.

---

## Chaîne de production

Tout se fait sur **Higgsfield**, et la chaîne n'a pas changé de nature :

1. **L'image** du plan — `nano_banana_2`, 16:9, environ 2 crédits. C'est là
   que se joue la règle du vrai lieu : le paysage réel, et un coin laissé
   libre pour Niba.
2. **L'animation** du plan — `grok_video_v15_lite`, 5 à 9 s, 720p, environ
   5 crédits. Mouvement lent : l'eau qui coule, l'herbe qui plie, un animal
   qui lève la tête. Jamais de secousse de caméra, jamais de coupe.
3. **La voix** — Text to Speech, ElevenLabs v3, voix Céline, direction de
   narration inchangée, **0,6 à 0,75 crédit la réplique**. C'est le poste le
   moins cher du film, et celui sans lequel il n'y a pas de film.
4. **La musique et les bruits**, puis le montage.
5. **Niba, sa bulle et les mots affichés** sont posés par l'application
   par-dessus le plan, en SVG et en texte — jamais générés.

Un plan complet revient donc à une dizaine de crédits, un film de six plans à
une quarantaine.

Les scripts verrouillés restent dans `work/video-*/script.md`, et
`work/films-*.py` reste la source : on y écrit la narration, le plan et les
mots affichés, et le script régénère le manifeste.
