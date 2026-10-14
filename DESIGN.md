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
110 ko pour les onze illustrations livrées. Une leçon illustrée doit coûter
moins qu'une photo.

Le champ `illustration` accepte une clé livrée avec l'app
(`prehistoire-grotte`) ou une URL de stockage : les leçons générées à partir
d'un cours importé utiliseront la seconde forme.

## Mouvement

150 à 250 ms, `ease-out-quint`. Aucun rebond. Le mouvement dit un état : la
tuile s'enfonce sous le doigt, le retour du guide monte de dix pixels, les
points gagnés s'élèvent et s'effacent. `prefers-reduced-motion` coupe tout.

## Règles tenues

- **Les galets, pas la barre de progression.** Un enfant qui ne lit pas encore
  les pourcentages compte des galets.
- **Le guide ne parle que quand il a quelque chose à dire.** Un personnage
  présent en permanence devient un décor qu'on ne lit plus.
- **La vignette se pose contre l'énoncé, jamais contre l'exercice entier**,
  sinon les réponses perdent la largeur et passent sur deux lignes.
- **Le ton suit le fond.** On ne félicite pas une erreur avec une couleur de
  réussite.

## Ce qu'on ne fait pas

- Pas de police web : elle coûterait 30 à 50 ko pour un gain d'allure. La
  personnalité vient de l'échelle, du poids, de la couleur et des
  illustrations.
- Pas de vert fluo ni de série qui culpabilise : on encourage, on ne harcèle
  pas.
- Pas d'arc-en-ciel primaire : illisible au soleil, et vu mille fois.
- Pas de grille de cartes identiques.
