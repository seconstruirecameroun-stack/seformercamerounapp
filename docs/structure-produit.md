# Se Former Cameroun — structure du produit

> Document de travail. Il décrit la cible, pas l'état actuel.
> État actuel : un prototype statique mono-enfant, mono-leçon, en localStorage,
> et une chaîne de production vidéo pilotée à la main.

## 1. En une phrase

Le parent photographie les cours de ses enfants ; l'app en fabrique le résumé à
retenir, une vidéo explicative, des explications reformulables à volonté et des
jeux à difficulté progressive, et elle suit ce que chaque enfant maîtrise.

## 2. Périmètre et classement

### Le document fait loi

Il n'y a **aucun programme figé dans l'app**. Chaque école a le sien et sa
propre manière d'avancer. L'app ne décide donc jamais ce que l'enfant doit
savoir : elle part des documents que le parent donne, puis elle organise,
classe et fabrique les révisions.

Conséquence directe sur le modèle : la matière, le chapitre et l'ordre des
leçons sont des **étiquettes déduites du document**, proposées par l'app puis
corrigées par le parent. Ce ne sont pas les entrées d'un référentiel national.

Les matières ne sont donc pas une liste fermée par un programme national.
Elles le sont par **l'emploi du temps de l'école**, que le parent photographie
une fois : l'app en tire le catalogue des matières de chaque classe, avec le
libellé officiel dans les deux langues et les intitulés de cahier qui y
renvoient.

Ce catalogue guide sans enfermer. À l'import, l'app propose d'abord les
matières du jour — un parent photographie le cahier le soir même, et les
trois ou quatre matières de la journée couvrent presque toujours ce qu'il
envoie. Si le cahier porte un intitulé absent du tableau, le parent l'ajoute,
et il rejoint le catalogue de la classe pour la fois suivante.

Sans ce référentiel, chaque import inventait sa matière : six créées en une
seule fois pour un seul cahier, dont deux qui n'existaient nulle part à
l'école. Un cahier écrit « Technologies » ; l'école écrit « Sciences et
technologies » / « Science and technology ». C'est la même matière.

L'emploi du temps porte aussi la **langue de chaque créneau** : « Maths » le
lundi et « Mathématiques » le mercredi sont la même matière enseignée dans
deux langues. C'est ainsi qu'un établissement bilingue le signale, et c'est
ce qui permet de ranger un cours dans la bonne langue sans le demander.

### On commence par les cours à résumé

Le périmètre de départ est une **famille de mécanique**, pas une liste de
matières : tout cours dont la révision consiste à mémoriser puis restituer un
résumé structuré. En pratique histoire, géographie, ECM, sciences — mais l'app
ne le vérifie pas et ne l'impose pas.

Ce qui reste hors périmètre, c'est la **correction procédurale** : poser une
opération, accorder un participe. Cela demande un autre moteur. Un cours de ce
type importé devient quand même une leçon et des notions ; seuls certains types
de jeux ne se généreront pas pour lui.

### Les classes

Système camerounais, six niveaux de primaire dans chaque sous-système :

| Francophone | Anglophone | Âge indicatif |
|---|---|---|
| SIL | Class 1 | 5–6 ans |
| CP | Class 2 | 6–7 ans |
| CE1 | Class 3 | 7–8 ans |
| CE2 | Class 4 | 8–9 ans |
| CM1 | Class 5 | 9–10 ans |
| CM2 | Class 6 | 10–11 ans |

La table des classes porte un **sous-système** et un **rang** (1 à 6). Le rang
rapproche deux classes équivalentes, le sous-système interdit de les confondre
à l'affichage.

La classe sert à **situer l'enfant et à doser le ton**, pas à déterminer le
contenu : celui-ci vient du document. Un CM1 dont l'école avance plus vite que
la voisine ne doit pas être bridé par un référentiel.

### Le bilinguisme

**Chaque cours est dans une seule langue** : celle du document importé. L'app ne
traduit pas et ne double pas le contenu.

Le bilinguisme camerounais se joue donc au niveau de la bibliothèque : une même
famille a des cours en français et des cours en anglais, et l'app doit traiter
les deux **à égalité**.

- l'OCR lit les deux
- la langue est détectée à l'import et corrigeable par le parent
- la leçon, ses notions, ses explications, ses jeux et sa vidéo **héritent** de
  la langue du cours
- chaque langue a sa voix de synthèse et son preset de narration

C'est bien plus simple que la traduction systématique, et c'est fidèle à la
réalité : un cours d'anglais reste en anglais, un cours d'histoire francophone
reste en français.

La langue de l'**interface** est un réglage distinct de la langue des cours.

## 3. Les deux espaces

L'app a deux publics dans la même application : le parent administre, l'enfant
joue.

| | Espace parent | Espace enfant |
|---|---|---|
| Accès | compte e-mail + mot de passe | choix d'un profil, sans mot de passe |
| Protection | — | l'espace parent est reverrouillé par un code à 4 chiffres |
| Rôle | importer, valider, suivre | apprendre, jouer, progresser |
| Ton | sobre, informatif | ludique, encourageant |

Le code PIN est ce qui empêche l'enfant d'aller voir les réponses ou de
modifier sa progression. Sans lui, tout le reste est décoratif.

## 4. Modèle de domaine

```
parent
 └── enfant (prénom, classe, sous-système)
      └── matière (étiquette libre, déduite puis corrigée)
           └── document source (photos du cours, devoir)
                └── leçon (titre, résumé, langue)
                     └── notion                       ← le cœur du système
                          ├── explication × registre
                          ├── item d'exercice × type × niveau
                          ├── bloc de narration vidéo
                          └── maîtrise (par enfant)
```

La langue est portée par la **leçon** et héritée par tout ce qu'elle produit.
Rien en dessous ne porte de langue.

### La notion est la brique centrale

Une notion est **une seule chose à savoir**, formulée en une phrase :

> « La Préhistoire se termine avec l'invention de l'écriture, vers 3 000 av. J.-C. »

Tout s'accroche à elle : les explications, les exercices, les blocs de la
vidéo, le score de maîtrise, la planification des révisions.

C'est ce qui rend le système évolutif — ajouter une matière, une classe ou une
langue, c'est ajouter des notions, pas du code. Et c'est ce qui permet de
savoir *quoi* l'enfant ne comprend pas, au lieu de constater qu'il a eu 3/5.

### Pour une matière à résumé, une notion est l'un de ces quatre objets

1. une **définition** (« la Préhistoire est la période qui… »)
2. une **date ou un repère** (« vers 3 000 av. J.-C. »)
3. une **liste à retenir** (« pêche, chasse, cueillette »)
4. une **relation** (« le Néolithique vient après le Paléolithique »)

Ce typage n'est pas cosmétique : il détermine quels jeux sont générables. Une
liste donne un texte à trous ou une association ; une relation donne une
chronologie ; une date donne un QCM. Le type de notion pilote le moteur.

## 5. Difficulté et progression

### Quatre étapes par leçon

L'enfant gravit une leçon comme les niveaux d'un jeu : quatre étapes, dans
l'ordre, et la suivante reste fermée tant que la précédente n'est pas nette.

| Étape | Nom | Ce qu'on demande | Forme des questions |
|---|---|---|---|
| 1 | Découverte | reconnaître | 3 choix, la réponse est dans le résumé |
| 2 | Entraînement | comprendre | 4 choix, relier, images |
| 3 | Maîtrise | produire | texte à trous, dictée, mots à remettre en ordre |
| 4 | Défi | transférer, vite | 20 secondes par question, QCM court ou vrai/faux |

La dernière marche se joue au chronomètre. Partout ailleurs, presser un
enfant qui découvre une notion l'empêche de la comprendre ; ici la notion est
déjà sue, et c'est la vitesse qu'on vient chercher. Le temps écoulé vaut une
réponse manquée — la notion revient, sans drame.

On n'y pose que du court, et on y demande du transfert : « on trouve une
pierre cassée en pointe, quelle époque ? » plutôt que « qu'est-ce que le
Paléolithique ? ».

### Règle de franchissement

Une étape est franchie quand **chaque notion de la leçon** a reçu une bonne
réponse à ce niveau. Pas une moyenne, pas un pourcentage : une moyenne
laisserait passer un enfant qui ignore trois notions sur dix.

Tant qu'il reste des notions à valider, la séance suivante repose des
questions sur celles-là, et sur celles-là seulement — avec une autre
formulation quand elle existe, pour qu'il revoie la notion plutôt que de
retenir la position de la bonne case.

Rater ne fait pas reculer : ça fait revenir. Perdre un acquis décourage un
enfant de primaire bien plus que ça ne le motive.

### L'image se gagne à la troisième marche

Chaque notion porte une image, et l'enfant la gagne en validant cette notion
à l'étape **Maîtrise**. Pas avant : aux deux premières marches, il reconnaît
et il comprend, il n'a encore rien produit. Pas après non plus : le Défi joue
la vitesse d'une notion déjà sue, et faire attendre l'image jusque-là
reviendrait à la faire payer deux fois.

La collection suit donc l'escalier que l'enfant voit, et rien d'autre. Elle a
d'abord dépendu d'un second compte, invisible à l'écran, qui réclamait six
bonnes réponses sur la même notion : un enfant pouvait gravir les quatre
étapes d'une leçon entière et garder « 0 sur 19 ». Une récompense dont la
règle ne se voit pas ne récompense rien.

La maîtrise, elle, reste — mais seulement pour espacer les révisions. Deux
comptes, deux rôles : l'un fait avancer le jeu, l'autre décide du jour où la
notion revient.

Une leçon importée qui n'aurait que deux niveaux de questions donne son image
à la plus haute marche qu'elle porte, sinon l'image serait hors d'atteinte.

Deux erreurs sur la même notion déclenchent une autre explication. C'est la
réponse directe à « générer encore et encore des textes différents pour que
l'enfant comprenne mieux » : l'échec ne punit pas, il déclenche une nouvelle
façon d'expliquer.

L'étape se déduit entièrement du journal des tentatives : aucune colonne
« étape en cours » à tenir à jour, donc rien qui puisse mentir sur l'état
réel. La révision espacée continue en parallèle, et reprend la main une fois
les trois étapes franchies.

### Variantes d'explication

Chaque notion porte plusieurs explications, de registres différents :

1. **Simple** — la phrase du résumé, reformulée court
2. **Analogie** — « c'est comme… », rattaché au quotidien de l'enfant
3. **Histoire** — un mini-récit avec des personnages
4. **Visuel** — schéma, frise ou illustration légendée
5. **Pas à pas** — décomposée en 3 micro-étapes

Le bouton « Explique autrement » fait tourner ces variantes, et peut en
générer une nouvelle si l'enfant a épuisé les existantes.

### Révisions espacées

Une notion réussie revient à **J+1, J+3, J+7, J+21**. Une notion échouée
repart à J+1. C'est ce calendrier, et non le dernier score, qui construit la
« mission du jour ».

## Ce qui donne envie de revenir

Un enfant de sept ans ne revient pas pour réviser. Il revient pour une série
qu'il ne veut pas casser, un objectif à vingt étoiles près, un coffre qu'il
n'a pas encore ouvert. Le système ci-dessous ne sert qu'à ça : transformer le
travail réellement fait en raisons d'y retourner demain.

Rien n'y est stocké. La série, l'objectif, les quêtes, les rangs et les
trophées se déduisent du journal des tentatives et des récompenses — les deux
mêmes journaux que le reste de l'app. Aucun compteur ne peut donc annoncer ce
que l'enfant n'a pas fait.

### Les étoiles suivent l'étape, pas un chiffre caché

| Ce qui arrive | Étoiles |
|---|---|
| Bonne réponse | 5 × le numéro de l'étape (5 à 20) |
| Notion validée pour l'étape | + 10 |
| Image gagnée (étape 3) | + 40 |
| Étape franchie | + 50 |

Une question de Défi vaut quatre fois une question de Découverte, et ça se
lit sur la barre des étapes. Les étoiles dépendaient auparavant du niveau de
maîtrise, invisible : une bonne réponse rapportait dix ou soixante étoiles
sans que rien ne dise pourquoi.

### La série, avec un jour de pardon

La série compte les jours où l'enfant a **répondu**, pas ceux où il a ouvert
l'app. Elle tolère un seul trou, et seulement au-delà de trois jours tenus :
une série qui tombe à zéro pour un dimanche de baptême ne motive plus
personne, car l'enfant qui vient de perdre trente jours n'a plus de raison de
revenir lundi. Le rattrapage est annoncé à l'écran — le pardon n'est pas une
permission.

Paliers fêtés : 3, 7, 14, 30 et 100 jours.

### L'objectif du jour

Cent étoiles, soit une dizaine de questions. Assez pour que la journée
compte, assez peu pour qu'un soir chargé y suffise. L'anneau se remplit, et
la phrase d'accueil annonce toujours ce qui **manque** — « plus que 20
étoiles » appelle, « 80 étoiles gagnées » n'appelle à rien.

### Trois défis par jour

Tirés de la date, donc stables toute la journée et différents demain :
réussir douze questions, gagner une image, enchaîner cinq bonnes réponses,
jouer dans deux matières, gagner soixante étoiles, réussir trois questions du
Défi. Trois seulement : une liste qu'on ne finit jamais décourage au lieu
d'appeler.

### Les rangs

Lionceau, Petite griffe, Griffe d'or, Jeune crinière, Grande crinière, Lion
indomptable — 0, 250, 750, 1 800, 3 500 et 7 000 étoiles. Le dernier rang se
mérite sur un trimestre entier. Au Cameroun, un enfant sait ce qu'est un Lion
indomptable avant de savoir lire.

Chaque rang porte son médaillon, généré puis détouré en disque : un emblème
rond se pose aussi bien sur la carte d'accueil que dans la fenêtre de fête,
et six carrés pastel aux fonds légèrement différents auraient juré entre eux.
Franchir un rang ouvre sa propre fenêtre, avant même l'étape et l'image —
c'est la récompense la plus rare du lot.

### Le duel de la semaine

Deux enfants de classes différentes ne peuvent pas être comparés sur ce
qu'ils savent. Le duel porte donc sur l'effort : les **questions réussies**
de la semaine, remises à zéro chaque lundi. Un CE1 qui travaille plus bat un
CM1 qui travaille moins, et c'est tout l'intérêt.

On compte des questions et non des étoiles, parce qu'une question du Défi
vaut quatre fois une question de Découverte : l'aîné, qui a fini ses leçons
et rejoue au chronomètre, aurait creusé un écart que le cadet ne pouvait pas
combler en travaillant. Une question reste une question, quelle que soit
l'étape — c'est la seule mesure qui compare vraiment l'effort, et c'est aussi
l'unité que l'enfant sait rattraper : « il te mène de 4 questions » dit quoi
faire ce soir.

La remise à zéro est la deuxième protection : celui qui perd ne perd que sept
jours, jamais son avance cumulée. Un classement à vie décourage
définitivement le second. Le texte ne tombe jamais dans la moquerie — un
chiffre à rattraper appelle, « tu es dernier » n'appelle à rien.

### Les trophées

Neuf cases sur une étagère, et les vides comptent autant que les pleines :
c'est la case vide qui donne envie. Une case non gagnée affiche sa condition
(« Jouer 7 jours de suite »), pas son nom — l'enfant doit savoir quoi faire,
pas ce qu'il rate.

### Le rappel du soir

Toute la gamification suppose que l'enfant ouvre l'app. Or un enfant de sept
ans ne pense pas à ouvrir une application de révision : c'est à elle d'aller
le chercher.

Un seul message par jour, vers 18 h à Douala — l'école est finie, le dîner
n'a pas commencé — et **jamais s'il a déjà joué**. Un rappel qui arrive après
l'effort apprend à l'enfant que le rappel ne veut rien dire.

| Situation | Ce que le téléphone affiche |
|---|---|
| A joué hier | « KLEIN, ta série t'attend ! » · *Une leçon avant ce soir, et elle tient.* |
| Absent 2 jours | « KLEIN, on joue ? » · *Une leçon de cinq minutes, et une image de plus.* |
| Absent 3 jours ou plus | « Tu m'as manqué, KLEIN ! » · *Niba t'attend pour une leçon.* |
| N'a jamais joué | « KLEIN, on commence ? » · *Cinq minutes, et tu gagnes ta première image.* |
| Vendredi ou samedi, mené au duel | « BRAYNE te mène de 4 questions » · *La semaine se termine dimanche soir.* |

Jamais de reproche. « Tu n'as pas travaillé » ne fait revenir personne ; « ta
série t'attend » donne une raison, et une chose à faire ce soir. Et rien
n'est promis que l'app ne tienne : chaque message renvoie à ce que l'enfant
trouvera en ouvrant.

L'abonnement est pris **par enfant et par appareil** : les deux frères
partagent souvent le même téléphone, et chacun doit recevoir son message,
avec son prénom. Le réglage vit dans l'espace parent, derrière le code — un
enfant à qui le navigateur demande « autoriser les notifications ? » répond
oui sans savoir à quoi.

La chaîne, et ce qu'elle ne détient pas :

1. `pg_cron` réveille `rappels_du_soir()` dans la base. Il choisit lui-même
   les destinataires et ne calcule que des faits bruts — dernière journée
   jouée, questions réussies de la semaine.
2. `pg_net` envoie ces faits à la fonction `rappel-du-soir`, avec un secret
   partagé.
3. La fonction trouve la phrase, signe avec la clé VAPID et chiffre l'envoi.

Elle ne lit jamais la base : tout ce dont elle a besoin arrive dans la
requête. Aucune clé d'administration n'existe donc nulle part dans ce
chemin, et les phrases restent en TypeScript, là où se trouve déjà le reste
de la langue de l'app.

L'icône posée sur l'écran d'accueil est le second rappel, celui qui agit sans
rien envoyer : l'app est installable, et elle porte le visage de Niba.

### Une nouvelle à la fois

Une seule bonne réponse peut en déclencher trois d'un coup : l'image de la
notion, l'étape franchie, le rang atteint. Entassées dans un même message,
elles se noyaient — l'enfant lisait « tu passes en Défi » et ne voyait pas
qu'il avait changé de rang.

Elles défilent donc une par une, de la plus ordinaire à la plus rare :

| Fenêtre | Ce qu'elle montre | Étoiles |
|---|---|---|
| La réponse | Niba, et l'explication de la notion | 5 × l'étape, + 10 si la notion tombe |
| L'image | la vignette gagnée | + 40 |
| L'étape | la médaille, et l'étape suivante nommée | + 50 |
| Le rang | le médaillon du nouveau rang | — |

Chaque fenêtre porte **les étoiles de ce moment-là**, et non le total de la
réponse : un enfant comprend « +40 pour l'image » là où un « +115 » unique ne
lui apprenait rien. Le bouton dit « Super ! » tant qu'il reste une nouvelle à
venir, et seule la dernière rend la main au jeu. Le rang ne rapporte rien :
il récompense un chemin déjà payé.

### Le coffre de fin de séance

Le coffre n'ajoute aucune information : tout son contenu figurait déjà dans
l'ancien récapitulatif. Il ajoute une seconde d'attente et un geste à faire.
Il ne s'ouvre jamais seul — un coffre qui s'ouvre sans qu'on y touche n'est
plus une récompense, c'est une notification. Une étape franchie passe
désormais par le bilan avant l'étape suivante : c'est le moment de la séance
où le coffre vaut le plus.

### Niba

Le lionceau est le seul élément de l'app qui parle à l'enfant à la première
personne, et le seul qui change d'humeur selon ce qui vient de se passer.
C'est lui qui dit « tu m'as manqué » après trois jours d'absence — une phrase
qu'aucune statistique ne remplace.

Dessiné en SVG et non généré en image : il doit cligner des yeux, changer
d'expression et rester net du pouce au grand écran, sans peser sur le réseau
ni coûter une génération à chaque nouvelle humeur.

### Les icônes

Dessinées dans l'app, pas prises dans les émojis du système : un émoji change
de dessin d'un téléphone à l'autre, ignore la palette, et sur certains
appareils ne s'affiche pas du tout — un trophée remplacé par un carré vide ne
récompense rien.

### Les animations et les sons

Trois règles tenues partout : une seule chose bouge à la fois, rien ne dure
plus d'une seconde, tout s'arrête net pour qui demande moins de mouvement.
Une app d'enfant qui scintille en permanence fatigue au bout de trois jours,
or c'est au trentième qu'on l'attend.

Les sons sont synthétisés et non chargés : quatre fichiers audio pèseraient
plus que toute l'application et arriveraient en retard sur une connexion
camerounaise. Une bonne réponse monte, une erreur descend — sans dissonance :
on signale une réponse à revoir, on ne gronde pas.

## 6. Les jeux

Un type de jeu n'est pas un écran dédié : c'est une **façon d'interroger une
notion**. Le même contenu alimente tous les types.

| Type | Niveaux | Type de notion visé | État |
|---|---|---|---|
| QCM | 1–2 | définition, date | construit |
| QCM en images | 1–2 | tout ce qui s'illustre | construit |
| Association (colonnes à relier) | 2–3 | liste, définition | construit |
| Chronologie (remettre en ordre) | 2–3 | relation | construit |
| Mots d'une phrase à remettre en ordre | 3 | définition | construit |
| Texte à trous | 3 | liste, définition | construit |
| Dictée écoutée | 3 | définition | construit |
| Vrai / faux | 1–4 | relation | construit |
| Restitution audio (dire le résumé) | 2–4 | définition, liste | repoussé |

La restitution audio attend : enregistrer la voix de l'enfant demande le
micro, du stockage, et surtout quelqu'un pour juger la réponse. Sans
correction, c'est un bouton qui ne fait rien.

Le vrai / faux ne vaut qu'accompagné : seul, il laisse une chance sur deux.
On ne le pose donc jamais comme unique question d'une notion.

Le QCM en images réutilise les illustrations déjà produites pour chaque
notion : « clique sur le sol ferralitique » demande moins de lecture qu'un
mot comme « ferralitique », ce qui compte en CE1.

### Points et récompenses

- Bonne réponse : **10 points**, × le niveau de difficulté
- Notion montée d'un niveau : **50 points**
- Mission du jour terminée : **100 points**
- Série (jours consécutifs) : badge à 3, 7, 30 jours

Les points récompensent l'**effort et la progression**, jamais le seul fait de
cliquer juste au niveau 1 — sinon l'enfant rejoue le facile en boucle.

## 7. La vidéo explicative

### Ce qui existe déjà et qu'il faut industrialiser

La production actuelle est pilotée à la main mais sa structure est déjà la
bonne. Le manifeste de `work/faceless-pastel-v2/` contient exactement les
paramètres à conserver :

```json
{
  "title": "...", "channel_type": "Kids", "style": "Pastel Flat 2D",
  "duration_seconds": 60, "aspect_ratio": "16:9", "language": "fr",
  "talking_characters": false,
  "through_line": "Une roue-mémoire se complète puis devient une tablette gravée.",
  "blocks": [ { "n": 1, "block_kind": "narration", "vo_line": "..." } ]
}
```

Trois acquis à ne pas perdre :

- **6 blocs de 10 secondes** : c'est un format, pas une coïncidence. Il
  correspond à 6 notions, une par bloc.
- **`through_line`** : un fil visuel mnémonique qui traverse la vidéo. C'est ce
  qui différencie une vidéo pédagogique d'un diaporama animé.
- **`voice.lock`** : le même preset de voix est réutilisé d'une version à
  l'autre. La voix doit rester **la même sur toute l'app** — c'est un repère
  pour l'enfant, et une par langue.

### Le manifeste se génère depuis les notions

```
notions validées → manifeste (1 bloc = 1 notion) → Higgsfield → mp4 → Storage
```

Le `vo_line` d'un bloc est la notion dite à voix haute. Les mots-clés affichés
sont les termes de la notion. Une leçon de 6 notions donne une vidéo de 60
secondes ; au-delà, on découpe en plusieurs vidéos plutôt que d'allonger.

### Pourquoi la validation doit précéder la vidéo

**Un cas réel dans le projet actuel.** Le bloc 4 du script dit : *« Au
Néolithique la pierre devient lisse le feu brille et l'agriculture
commence »*. Or l'espace parent de l'app signale précisément ce point comme
douteux : la maîtrise du feu est généralement étudiée au Paléolithique.

La vidéo de 62 secondes déjà produite contient donc l'erreur que l'app
demande au parent de corriger. Et une vidéo ne se corrige pas d'un clic : il
faut la régénérer entièrement.

D'où la règle : **aucune génération vidéo avant validation des notions par le
parent.** C'est l'étape la plus coûteuse de la chaîne, elle doit être la
dernière.

### Mots-clés incrustés ou superposés ?

La vidéo est dans la langue du cours : pas de double production. Reste une
question de robustesse — les mots-clés affichés sont-ils **incrustés par
Higgsfield** dans l'image, ou **superposés par le lecteur de l'app** ?

| | Incrustés | Superposés |
|---|---|---|
| Rendu | plus fini | dépend du lecteur maison |
| Corriger un mot | régénérer toute la vidéo | éditer une ligne en base |
| Accessibilité | texte figé dans l'image | agrandissable, lisible au lecteur d'écran |

**Recommandation : superposés.** Dans une app où le parent valide et corrige,
pouvoir réparer un mot-clé sans repayer un rendu de 60 secondes compte plus que
le fini.

### La génération est asynchrone

Une vidéo prend des minutes, pas des millisecondes. Cela impose une file de
travaux avec des états explicites :

```
queued → script_ready → rendering → ready → published
                     ↘ failed (avec raison, et possibilité de relance)
```

Le parent voit l'avancement ; l'enfant ne voit la leçon que lorsqu'elle est
utilisable sans la vidéo, et la vidéo apparaît quand elle est prête. Une leçon
n'attend jamais sa vidéo pour être révisable.

## 8. Écrans

### Espace parent

1. **Tableau de bord** — une carte par enfant : maîtrise par matière, temps de
   révision, alertes (notion qui bloque, devoir pour demain)
2. **Mes enfants** — ajouter, classe, sous-système, langues activées
3. **Importer** — photos ou PDF → enfant + matière + type (cours / devoir)
4. **Bibliothèque** — documents importés et leur état de traitement
5. **À valider** — file des notions, explications et scripts vidéo générés
6. **Détail enfant** — progression notion par notion, erreurs récurrentes
7. **Réglages** — code PIN, quota de génération, abonnement

### Espace enfant

1. **Choix du profil** — avatars des enfants de la famille
2. **Accueil** — « Ta mission du jour » : 3 à 5 éléments à faire, points, série
3. **Leçon** — le résumé, la vidéo, les explications reformulables, l'audio
4. **Jeux** — parcours par niveaux, déverrouillage progressif
5. **Interrogation** — mode école, sans indice, correction expliquée
6. **Récompenses** — points, badges, collection

## 9. Chaîne de traitement d'un document

```
photos du cours
   ↓ 1. stockage              Supabase Storage
   ↓ 2. lecture (OCR)         modèle vision → texte brut
   ↓ 3. classement            langue, matière et chapitre proposés
   ↓ 4. extraction            texte → résumé + notions typées
   ↓ 5. VALIDATION PARENT     ← point de contrôle obligatoire
   ↓ 6. génération texte      explications × registres, items × niveaux
   ↓ 7. génération vidéo      manifeste → Higgsfield → mp4   (asynchrone)
   ↓ 8. publication           visible dans l'espace enfant
```

L'étape 5 n'est pas négociable, et l'ordre 5 → 7 non plus : voir le cas du feu
au Néolithique en §7.

### Maîtrise du coût de génération

La génération est le seul poste de coût variable, et la vidéo en est l'essentiel.

- **Mutualisation** : les notions d'un même cours servent tous les enfants de
  la famille qui suivent ce cours
- **Génération en lot** à l'import, puis à la demande seulement
- **Vidéo sur demande explicite** du parent, jamais automatique à l'import
- **Quota** visible par le parent (« 2 vidéos et 8 régénérations ce mois »)

## 10. Technique

### Pourquoi l'existant ne suffit pas

Le prototype est un `localStorage` dans trois fichiers statiques. Il ne peut
porter ni plusieurs enfants, ni l'upload, ni la génération, ni une file de
travaux vidéo, ni un suivi qui survit au changement d'appareil.

### Cible

| Couche | Choix | Raison |
|---|---|---|
| Front | Vite + React, Tailwind, shadcn/Radix, TanStack Query | stack déjà maîtrisée |
| Données | Supabase Postgres | relationnel, et déjà prévu pour les médias |
| Auth | Supabase Auth (parent uniquement) | les profils enfants sont des lignes, pas des comptes |
| Fichiers | Supabase Storage | photos, PDF, et les mp4 aujourd'hui sur CloudFront |
| IA texte | Edge Functions | **les clés d'API ne doivent jamais être dans le front** |
| IA vidéo | Edge Function + file de travaux | rendu long : webhook ou sondage, pas de requête bloquante |
| Hors-ligne | PWA + file de synchro | connexion irrégulière : les tentatives partent en différé |

### Tables

```
parents            (= auth.users)
children           parent_id, prénom, class_id
classes            sous_système, code, rang            -- SIL..CM2 / Class 1..6
subjects           parent_id, libellé, couleur         -- libre, propre à la famille
documents          child_id, subject_id, storage_path, type, statut
lessons            document_id, titre, résumé, lang, chapitre, ordre, statut
notions            lesson_id, type, énoncé, ordre      -- définition|date|liste|relation
explanations       notion_id, registre, contenu, statut
items              notion_id, type, niveau, payload (jsonb), réponse, statut
videos             lesson_id, manifeste (jsonb), voice_preset,
                   storage_path, poster_path, durée_s, statut
jobs               type, cible_id, statut, tentatives, erreur, créé_le
mastery            child_id, notion_id, niveau, score, prochaine_révision
attempts           child_id, item_id, réponse, correct, durée_ms, créé_le
rewards            child_id, type, valeur, créé_le
assignments        child_id, subject_id, intitulé, échéance, fait
```

Cinq principes :

- **RLS partout** : un parent ne lit que ses propres lignes, sans exception
- **`statut` sur tout contenu généré** : `pending` → `approved` ; l'espace
  enfant ne lit que l'`approved`
- **`lang` sur la leçon, et nulle part en dessous** : un cours est dans une
  langue, donc tout ce qu'il produit l'est aussi
- **`subjects` appartient à la famille, pas à un référentiel** : intitulés
  libres, renommables, fusionnables
- **`videos.manifeste` conservé en base** : il permet de régénérer une vidéo à
  l'identique, ou avec une seule ligne corrigée

`attempts` ne se modifie jamais : c'est le journal brut. `mastery` en est la
vue agrégée, recalculable. Si la formule de progression change, on la rejoue
sur l'historique au lieu de perdre les données.

## 11. Découpage en lots

| Lot | Contenu | Résultat visible |
|---|---|---|
| 0 | Supabase, auth parent, profils enfants, classes camerounaises, PIN, migration de la leçon Préhistoire | plusieurs enfants, données persistées |
| 1 | Import, Storage, OCR, détection de langue, classement proposé, extraction en notions typées, écran de validation | un vrai cours importé devient une leçon rangée |
| 2 | Explications × registres, « Explique autrement » | l'enfant obtient une autre explication |
| 3 | Moteur d'items, 4 niveaux, points, mission du jour | les jeux deviennent génératifs |
| 4 | File de travaux, manifeste auto, génération vidéo, lecteur maison | la vidéo se produit depuis l'app |
| 5 | Révisions espacées, tableau de bord parent | le parent voit la progression réelle |
| 6 | Devoirs et échéances, PWA hors-ligne | usage quotidien |

Le lot 0 est le seul qui jette du code existant. À partir du lot 1, chaque lot
s'ajoute sans défaire le précédent.

La vidéo arrive en lot 4 et non plus tôt, pour une raison simple : c'est la
brique la plus coûteuse et la plus lente, et elle dépend de notions déjà
validées (lot 1). D'ici là, la production vidéo continue à la main avec les
scripts PowerShell existants.

## 12. Questions ouvertes

1. **Mots-clés incrustés ou superposés ?** Higgsfield peut-il rendre les
   visuels sans texte incrusté, pour que le lecteur de l'app superpose les
   mots-clés ? Voir §7.
2. **Granularité d'une leçon.** Un document photographié = une leçon, ou un
   document peut-il en contenir plusieurs (et plusieurs photos former une seule
   leçon) ? C'est le découpage que l'app doit proposer à l'import.
3. **Qui déclenche la vidéo ?** Le parent à la demande (coût maîtrisé) ou
   automatiquement à chaque leçon validée (confort, mais facture) ?
4. **L'âge plancher.** Un enfant de SIL ou Class 1 ne lit pas de consignes :
   faut-il un mode entièrement audio dès le lot 3 ?
5. **Hors-ligne.** Indispensable dès le début, ou acceptable au lot 6 ? La
   vidéo hors-ligne suppose un téléchargement explicite.
6. **Modèle économique.** Gratuit, abonnement familial, par enfant ? Cela
   détermine la générosité du quota, surtout vidéo.
