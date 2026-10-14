# Se Former Cameroun — design

## La scène

Un enfant de neuf ans à Yaoundé, 18 h, sur le téléphone Android partagé de la
famille, dans un salon très clair, l'écran en partie au soleil.

Cette phrase tranche le reste : **thème clair**, contraste élevé, typographie
large, cibles tactiles d'au moins 54 px, et aucun glisser-déposer.

## Deux registres

| | Espace parent | Espace enfant |
|---|---|---|
| Rôle du design | servir la tâche | donner envie d'ouvrir l'app |
| Couleur | sobre, un accent | engagée : l'illustration porte l'écran |
| Densité | compacte | aérée, une chose à la fois |
| Typographie | échelle normale | échelle `kid`, un cran au-dessus |

## Couleur

En OKLCH. Aucun gris pur, aucun blanc pur : tous les neutres sont teintés vers
l'encre. Le texte sur fond tient au-dessus de 7:1, parce que l'écran est
souvent lu en plein jour.

| Jeton | Rôle |
|---|---|
| `ink`, `ink-2`, `muted` | texte, du plus appuyé au plus discret |
| `paper`, `white-warm`, `line` | fonds et séparations |
| `clay`, `clay-dark` | action principale, et elle seule |
| `gold` | récompense : points, galets franchis, badges |
| `leaf` | réussite |
| `sky`, `sand`, `mint`, `lilac` | échos des illustrations, en aplats légers |

`clay` ne décore jamais : s'il apparaît, c'est qu'il y a quelque chose à
toucher. `gold` ne signale jamais une action, seulement un gain.

## Typographie

**Fredoka** dans l'espace enfant, servie depuis l'app : 33 ko une fois, en
cache, et disponible hors-ligne. Licence SIL OFL, jointe dans `public/fonts`.
Ses formes rondes donnent un ton qu'aucune police système n'a. L'espace parent
reste en police système : il sert une tâche, pas une humeur.

**Plancher à 17 px. Rien ne descend en dessous**, jamais. Les petites
capitales de 12 px des interfaces d'adultes ont été supprimées une à une : un
enfant de neuf ans lit à bout de bras, sur un téléphone partagé, souvent au
soleil.

| Jeton | Taille | Emploi |
|---|---|---|
| `text-kid-xs` | 17 px | étiquettes, le plus petit admis |
| `text-kid-sm` | 18 px | texte secondaire |
| `text-kid` | 21 px | texte courant, réponses |
| `text-kid-lg` | 26 px | énoncé d'une notion |
| `text-kid-xl` | 32 px | question posée |
| `text-kid-2xl` | 40 px | titre de leçon |

## Écrire court

Une explication tient en **une phrase courte, deux au maximum**, sous une
centaine de caractères. Un résumé tient en deux ou trois phrases.

Ce n'est pas une préférence de style : à neuf ans, un paragraphe se saute.
Une phrase lue vaut mieux qu'un paragraphe exact ignoré. La contrainte est
écrite dans le schéma d'extraction, pas seulement dans les textes de la
démonstration — sinon elle ne tiendrait qu'une leçon.

## Illustration

Style unique, celui de la chaîne vidéo : **Pastel Flat 2D**, sans contour noir,
ciels dégradés, sable, menthe, lilas. Tout mélange avec un autre rendu est à
proscrire : l'historique de production contient aussi des images en pâte à
modeler 3D, elles ne sont pas utilisées.

Trois emplois, trois formats :

| Emploi | Format | Où |
|---|---|---|
| Scène | 960 × 540 | bandeau de leçon, titre incrusté dessus |
| Objet | 320 × 320 | vignette de notion, contre l'énoncé |
| Guide | 360 × 540 | le personnage qui commente une réponse |

**Le poids est une contrainte de design, pas une optimisation.** Les sources
font 1,3 à 2 Mo ; `scripts/illustrations.mjs` les ramène à du WebP, soit
153 ko pour les quinze illustrations livrées. Une leçon illustrée doit coûter
moins qu'une photo.

**Aucune illustration ne sert à deux endroits.** La roue-mémoire a longtemps
bouché trois trous — l'écran de fin, l'état vide, la septième notion. Deux
cases identiques dans la collection, et aucun indice sur ce qu'il fallait
retenir. Chaque emploi a maintenant son image : médaille, chat endormi, et les
trois objets alignés dans l'ordre des époques.

Le champ `illustration` accepte une clé livrée avec l'app
(`prehistoire-grotte`) ou une URL de stockage : les leçons générées à partir
d'un cours importé utiliseront la seconde forme.

## Mouvement

150 à 250 ms, `ease-out-quint`. Aucun rebond. Le mouvement dit un état : la
tuile s'enfonce sous le doigt, le retour du guide monte de dix pixels, les
points gagnés s'élèvent et s'effacent. `prefers-reduced-motion` coupe tout.

## Le retour se fait en fenêtre

Après chaque réponse, une fenêtre s'ouvre par-dessus l'écran : bandeau coloré
selon le résultat, le guide ou la vignette gagnée, l'explication, les points,
et un seul gros bouton sous le pouce. Elle se ferme aussi au clic sur le fond,
à Échap et à Entrée.

C'est la convention du jeu, et elle vaut mieux ici qu'un message en bas de
page : un texte posé sous la question se lit distraitement, une fenêtre qui
s'ouvre se regarde. Le bandeau tient le résultat, le bouton tient la suite,
et il n'y a jamais de choix à faire.

Cela déroge au principe « le modal n'est pas la première réponse » posé pour
l'espace parent. La dérogation est assumée et limitée à l'espace enfant : là,
le retour *est* la récompense.

## Lecture à voix haute

Le résumé et chaque explication portent un bouton « Écouter », servi par la
synthèse du navigateur. Un enfant de primaire lit lentement, et un cours peut
arriver dans une langue qui n'est pas celle parlée à la maison. Cela ne coûte
ni octet ni génération, et fonctionne hors-ligne. La voix s'arrête quand on
change d'explication ou d'écran : elle ne poursuit pas l'enfant.

## La leçon est un paquet de fiches

Une fiche à l'écran, qu'on fait glisser du doigt ou avec un gros bouton
« Suivant ». Le film et le résumé sont les deux premières fiches : ce sont des
fiches comme les autres, elles n'ont pas à vivre dans des blocs empilés
au-dessus.

La version précédente alignait sept cartes dans une page qui défilait. C'était
complet et illisible : l'enfant faisait défiler sans rien regarder.

Deux conséquences tenues :

- **Jouer reste à portée.** « Passer et jouer » sous les fiches, et la
  dernière fiche propose « Jouer maintenant ». Apprendre n'est pas une salle
  d'attente avant le jeu.
- **Le bandeau de la leçon rétrécit** pendant la lecture : la fiche a besoin
  de la place, pas le titre.

## Règles tenues

- **Les galets, pas la barre de progression.** Un enfant qui ne lit pas encore
  les pourcentages compte des galets.
- **Le guide ne parle que quand il a quelque chose à dire.** Un personnage
  présent en permanence devient un décor qu'on ne lit plus.
- **La vignette se pose contre l'énoncé, jamais contre l'exercice entier**,
  sinon les réponses perdent la largeur et passent sur deux lignes.
- **Le ton suit le fond.** On ne félicite pas une erreur avec une couleur de
  réussite.
- **Le registre d'explication est nommé** à l'enfant : « En deux mots »,
  « C'est comme… », « Une petite histoire ». Sans cela, « Explique autrement »
  ressemble à une roue qu'on tourne au hasard.
- **Une notion maîtrisée porte une étoile** à la place de son numéro, dans la
  leçon comme dans la collection.

## Ce qu'on ne fait pas

- Pas de police web : elle coûterait 30 à 50 ko pour un gain d'allure. La
  personnalité vient de l'échelle, du poids, de la couleur et des
  illustrations.
- Pas de vert fluo ni de série qui culpabilise : on encourage, on ne harcèle
  pas.
- Pas d'arc-en-ciel primaire : illisible au soleil, et vu mille fois.
- Pas de grille de cartes identiques.
