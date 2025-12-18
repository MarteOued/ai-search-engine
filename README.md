Moteur de Recherche d'Information sur l'Intelligence Artificielle

Auteurs 

Julien & Martine

Description 

Ce projet implémente un moteur de recherche d'information complet sur le thème de l'Intelligence Artificielle. Les données proviennent de Reddit et Arxiv. L'objectif est de structurer ces données, de les analyser textuellement et de permettre une recherche pertinente par mots-clés en utilisant un modèle vectoriel. Le projet inclut désormais une interface graphique web permettant la visualisation des données et le filtrage dynamique des résultats.

Fonctionnalités 

Acquisition de données depuis les API Reddit et Arxiv 

Structuration du code avec des classes (POO) et patterns (Singleton, Factory) 

Analyse textuelle : nettoyage, calcul de fréquences 

Moteur de recherche vectoriel : matrice TF-IDF et similarité Cosinus 

Interface Web interactive (Streamlit) : recherche, filtrage par date/source 

Visualisation de données : graphiques temporels, répartition des sources et analyse lexicale 

Sauvegarde et chargement de données au format CSV

Statistiques 

200 documents récupérés (100 depuis Reddit + 100 depuis Arxiv) 

Filtrage et nettoyage automatique des textes Indexation vectorielle sur l'ensemble du vocabulaire enrichi

Installation 

Avant de lancer le projet, assurez-vous d’avoir Python installé sur votre ordinateur. Installez ensuite les bibliothèques nécessaires à l’aide du fichier requirements.txt. 

Attention : Ce projet nécessite des versions spécifiques de certaines librairies pour l'interface graphique. 

pip install -r requirements.txt

Utilisation Le projet peut être utilisé de deux manières :

    Mode Console (Génération des données) Pour récupérer les données, construire le corpus et voir une démonstration textuelle : python main.py

    Mode Interface Web (Recherche et Visualisation) Pour lancer l'application graphique dans votre navigateur : streamlit run interface.py

Structure du projet

 ├── main.py # Programme principal (Acquisition & Démo console) 
 
 ├── interface.py # Application Web et Visualisation (Streamlit) 
 
 ├── SearchEngine.py # Moteur de recherche (Logique TF-IDF, Cosinus) 
 
 ├── Corpus.py # Classe Corpus (Singleton, Gestion des données) 
 
 ├── Document.py # Classes Document, RedditDocument, ArxivDocument 
 
 ├── Author.py # Classe Author 
 
 ├── DocumentFactory.py # Factory Pattern pour création d'objets 
 
 ├── corpus_v1.csv # Base de données documentaire obtenu en lancant main.py
 
 ├── frequences.csv # Statistiques textuelles pour la DataVisualisation obtenu en lancant main.py
 
 ├── requirements.txt # Bibliothèques nécessaires (versions figées) 
 
 ├── .gitignore # Fichiers à ignorer par Git 
 
 └── README.md # Documentation du projet

Versions 

Version 1 : TD3-5 — Acquisition, Structuration et Héritage. 

Version 2 : TD6-7 — Analyse textuelle, Indexation et Moteur de recherche. 

Version 3 : TD8-10 — Interface Graphique Web et Visualisation de données.

Licence Projet universitaire – Université Lumière Lyon 2. Ce projet a été réalisé dans le cadre d’un travail académique et n’est pas destiné à un usage commercial.