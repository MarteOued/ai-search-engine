Moteur de Recherche d'Information - Intelligence Artificielle

Auteurs



Julien \& Martine



Description



Ce projet implémente un moteur de recherche d'information sur le thème de l'Intelligence Artificielle.

Les données proviennent de Reddit et Arxiv.

L'objectif est de structurer, filtrer et analyser ces données à l'aide de concepts de programmation orientée objet (POO) et de design patterns.



Fonctionnalités (v1)



Acquisition de données depuis Reddit et Arxiv



Structuration du code avec des classes (POO)



Mise en œuvre de l'héritage et du polymorphisme



Utilisation de patterns de conception (Singleton, Factory)



Sauvegarde et chargement de données au format CSV



Statistiques



200 documents récupérés (100 depuis Reddit + 100 depuis Arxiv)



110 documents conservés après filtrage



96 auteurs identifiés



Installation



Avant de lancer le projet, assurez-vous d’avoir Python installé sur votre ordinateur.

Installez ensuite les bibliothèques nécessaires à l’aide du fichier requirements.txt :



pip install -r requirements.txt



Utilisation



Pour exécuter le programme principal, lancez la commande suivante depuis le dossier du projet :



python main.py



Structure du projet

├── main.py              # Programme principal

├── Document.py          # Classes Document, RedditDocument, ArxivDocument

├── Author.py            # Classe Author

├── Corpus.py            # Classe Corpus (Singleton)

├── DocumentFactory.py   # Factory Pattern

├── corpus\_v1.csv        # Données sauvegardées

├── requirements.txt     # Bibliothèques nécessaires

├── .gitignore           # Fichiers à ignorer par Git

└── README.md            # Documentation du projet



Versions



v1 : TD3-5 — Acquisition, Structuration et Héritage des classes principales.



Licence



Projet universitaire – Université Lumière Lyon 2.

Ce projet a été réalisé dans le cadre d’un travail académique et n’est pas destiné à un usage commercial.

