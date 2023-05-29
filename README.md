# Projet-BDD

Pour ce projet, il nous était demandé de faire une base de donnée (BDD) ainsi que l'interface graphique l'accompagnant.

J'ai donc choisi de partir sur la construction d'une base de donnée permettant de faciliter la gestion des stages pour les étudiants, les enseignant encadrant cette recherche ainsi que les chercheurs eux mêmes.

## Fonctionnnement
### Lancement
Ce projet à été codé en python 3.8.3, pour l'exécuter tout interpréteur de python d'une version ulterieure devait faire l'affaire. Je préviens malgré tout que j'utilise plusieurs versions du module `tkinter` qui a eu la bonne idée de faire une nouvelle version non rétro-compatibile, si vous avez des problèmes pensez à regarder de ce côté là.

### Utilisation:
#### Page d'accueil
Je n'ai pas eu la foie de faire deux pages: une pour s'inscrire et une pour se connecter... Il n'y a donc qu'une page et un bouton pour chaque activité. Si vous voulez vous connecter remplissez les champs demandés. J'ai codé pour cela un outil de cookie qui va se souvenir de vos connexions passées et vous permet de vous connecter plus rapidement. Cette opération est entièrement sécurisée: le fichier commence par le mot "encrypted" donc personne ne peut le lire :)

#### Page des chercheurs
Je tiens tout d'abord à m'excuser pour la vision réductrice que le site renvoie des chercheurs. Cela ne représente en rien ma pensée profonde mais uniquement des exercices pour un projet.

Venons en aux faite: un chercheur, sur ce site, peut actualiser ses données ou proposer un stage. Pardonnez aussi la mise en page il était tard... 

- **proposer un stage**: pour cela il vous suffit de remplir le formulaire donné comprenant: 
    - un titre unique
    - un descriptif un peu plus détaillé
    - d'autres informations utiles pour un stage... 
- **changer ses informations personnelles**: pour que un jeune étudiant puisse vous trouver de façon efficace, à actualiser manuellement et de façon très peu efficace pour les dates (j'ai pas fais ça de façon très propre il est vrai).

#### Page des élèves
Les deux points intéressants pour les élèves sont: chercher un stage et noter un chercheur (je le rappelle, ceci n'a pas vocation à être représentatif de ma pensée, noter quelqu'un gratuitement n'est pas toujours une bonne chose).
- **recherche de stage**: l'élève peut sélectionner parmis quelques filtres (tel que le pays / ville / laboratoire, les dates ou le sujet) des options afin de trier sa recherche de façon précise. Il peut au final regarder les offres disponibles et communiquer facilement avec le chercheur en question.
- **notation**: un élève peut chercher le profile d'un chercheur et une fois dessus il peut lui attribuer une note (par exemple si son stage lui a plu). 


## Excuses
Je tiens finalement à m'excuser auprès de la communauté python. Au cours de ce projet j'ai estimé que mon objectif se prêtait plus à une programmation fonctionnelle. J'ai donc codé cela avec très peu de classes et aussi peu de style "pythonique" que possible. Cela n'aurait pas nécessairement rendu mon code plus lisible (l'avantage c'est que la chimère que j'ai écrite se lit de façon très linéaire) mais je reconnais qu'il y aurait eu un grand gain d'efficacité à conserver quelque part les identifiants afin de ne pas les rechercher à chaques fois... 

Cela étant dit, il y a de nombreux points où mon code peut être amélioré (notemment au nievau de la gestion de la base de donnée: je fais beaucoup trop de requêtes inutiles). Cela sera peeut être corrigé si je continue ce projet les années prochaines :)
