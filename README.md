Moteur de Recherche d'Information - Intelligence Artificielle

Auteurs 
Julien & Martine

Description 
Ce projet implémente un moteur de recherche d'information complet sur le thème de l'Intelligence Artificielle. Les données proviennent de Reddit et Arxiv. L'objectif est de structurer ces données, de les analyser textuellement et de permettre une recherche pertinente par mots-clés en utilisant un modèle vectoriel.

Fonctionnalités 
Acquisition de données depuis les API Reddit et Arxiv 
Structuration du code avec des classes (POO) 
Mise en œuvre de l'héritage et du polymorphisme Utilisation de patterns de conception (Singleton, Factory) Analyse textuelle : nettoyage, calcul de fréquences et concordancier 
Moteur de recherche vectoriel : construction de matrice TF-IDF et calcul de similarité Cosinus 
Indexation vectorielle sur l'ensemble du vocabulaire du corpus
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
Pour exécuter le programme principal (acquisition, analyse et démonstration de recherche), lancez la commande suivante depuis le dossier du projet : 
python main.py

Structure du projet 
├── main.py # Programme principal et tests 
├── SearchEngine.py # Moteur de recherche (TF-IDF, Cosinus) 
├── Corpus.py # Classe Corpus (Singleton, Gestion des données) 
├── Document.py # Classes Document, RedditDocument, ArxivDocument 
├── Author.py # Classe Author 
├── DocumentFactory.py # Factory Pattern pour création d'objets  
├── .gitignore # Fichiers à ignorer par Git
├── requirements.txt # Bibliothèques nécessaires 
└── README.md # Documentation du projet

Version 1 : TD3-5 — Acquisition, Structuration et Héritage. 
Version 2 : TD6-7 — Analyse textuelle, Indexation et Moteur de recherche.

Licence 
Projet universitaire – Université Lumière Lyon 2. 
Ce projet a été réalisé dans le cadre d’un travail académique et n’est pas destiné à un usage commercial.