# -*- coding: utf-8 -*-
"""
================================================================================
                    PROJET : MOTEUR DE RECHERCHE D'INFORMATION
================================================================================

Auteurs : Julien et Martine
Date    : Novembre 2025
Thématique : Intelligence Artificielle

================================================================================
                            DESCRIPTION GÉNÉRALE
================================================================================

Ce programme implémente un moteur de recherche d'information sur le thème de
l'Intelligence Artificielle. Il est divisé en plusieurs parties :

TD3 - ACQUISITION DES DONNÉES :
    - Connexion aux APIs Reddit et Arxiv
    - Récupération de 200 documents (100 Reddit + 100 Arxiv)
    - Extraction des métadonnées (titre, auteur, date, texte, etc.)
    - Nettoyage et filtrage des données
    - Sauvegarde dans un fichier CSV

TD4 - STRUCTURATION AVEC LES CLASSES :
    - Création de la classe Document (représente un document)
    - Création de la classe Author (représente un auteur)
    - Création de la classe Corpus (gère la collection)
    - Refactorisation du code avec la POO
    - Organisation en modules séparés

TD5 - HÉRITAGE ET PATRONS DE CONCEPTION :
    - Création de RedditDocument et ArxivDocument (héritage)
    - Ajout d'attributs spécifiques (commentaires, co-auteurs)
    - Implémentation du pattern Singleton (Corpus unique)
    - Implémentation du pattern Factory (création automatique)
    - Tests et validation

RÉSULTAT FINAL :
    - 110 documents structurés dans un corpus
    - 96 auteurs identifiés
    - Classes hiérarchisées et patterns appliqués
    - Données sauvegardées et réutilisables

================================================================================
"""
                            # IMPORTATION DES LIBRAIRIES


import praw                        # Pour se connecter à Reddit
import urllib.request              # Pour faire des requêtes web (Arxiv)
import xmltodict                   # Pour lire les réponses d'Arxiv (XML)
import pandas as pd                # Pour manipuler les données (tableaux)
from datetime import datetime      # Pour gérer les dates
                          
                        # TD3 - PARTIE 1 : ACQUISITION DES DONNÉES


print("="*70)
print("           TD3 - ACQUISITION DES DONNÉES")
print("="*70)

# 1.1 RÉCUPÉRATION DES DONNÉES REDDIT


print("\n Connexion à l'API Reddit ")

# On se connecte à Reddit avec nos identifiants développeur

reddit = praw.Reddit(
    client_id="LE2COTSsmlNvVRBivOkeqA",
    client_secret="vKXo3JAwS-Jt9I0_yW68GCQzkPlN-A",
    user_agent="JuleMarte_Recherche"
)
print(" Connexion à Reddit réussie !")

# Liste qui va contenir tous nos documents (Reddit + Arxiv)
docs = []

# Thématique que nous avons choisie : Intelligence Artificielle

query = "artificial intelligence"
limit = 100  # Nombre de posts à récupérer

print(f"\n Recherche de posts Reddit sur '{query}'...")
print(f"Limite fixée : {limit} posts")

# On lance la recherche sur Reddit (tous les subreddits)
subreddit = reddit.subreddit("all")
hot_posts = subreddit.search(query, limit=limit)

# On parcourt tous les posts trouvés
compteur_reddit = 0
for post in hot_posts:
    # Extraction des informations de base
    titre = post.title
    auteur = str(post.author)
    date = datetime.fromtimestamp(post.created_utc)
    url = f"https://www.reddit.com{post.permalink}"
    texte = post.selftext
    
    # Nettoyage : on remplace les sauts de ligne par des espaces
    texte = texte.replace("\n", " ")
    
    # TD5 : On récupère aussi le nombre de commentaires (spécifique à Reddit)
    nb_commentaires = post.num_comments
    
    # On crée un dictionnaire avec toutes les métadonnées
    document = {
        "titre": titre,
        "auteur": auteur,
        "date": date,
        "url": url,
        "texte": texte,
        "origine": "reddit",
        "nb_commentaires": nb_commentaires  # Spécifique Reddit (TD5)
    }
    
    # On ajoute ce document à notre liste
    docs.append(document)
    compteur_reddit += 1

print(f" {compteur_reddit} posts Reddit récupérés")

# 1.2 RÉCUPÉRATION DES ARTICLES ARXIV


print("\n" + "="*70)
print(" Récupération des articles Arxiv...")

# Construction de l'URL pour interroger l'API Arxiv

query_arxiv = "artificial+intelligence"  # Les espaces deviennent des +
url = f"http://export.arxiv.org/api/query?search_query=all:{query_arxiv}&start=0&max_results=100"

print(f"URL : {url}")

# On fait la requête HTTP à l'API Arxiv
try:
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    
    # On transforme le XML reçu en dictionnaire Python
    arxiv_data = xmltodict.parse(data)
    entries = arxiv_data['feed']['entry']
    
    print(f" {len(entries)} articles Arxiv trouvés")
    
    # On parcourt tous les articles
    compteur_arxiv = 0
    for entry in entries:
        # Extraction du titre
        titre = entry['title']
        
        # TD5 : Gestion des co-auteurs (spécifique à Arxiv)
        # Un article peut avoir un ou plusieurs auteurs
        co_auteurs = []
        if isinstance(entry['author'], list):
            # Cas 1 : Plusieurs auteurs
            auteur = entry['author'][0]['name']  # Le premier est l'auteur principal
            # Les autres sont des co-auteurs
            co_auteurs = [a['name'] for a in entry['author'][1:]]
        else:
            # Cas 2 : Un seul auteur
            auteur = entry['author']['name']
            co_auteurs = []  # Pas de co-auteurs
        
        # Conversion de la date (format ISO)
        date_str = entry['published']
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        
        # Récupération de l'URL et du résumé
        url = entry['id']
        texte = entry['summary']
        texte = texte.replace("\n", " ")
        
        # On crée un dictionnaire avec toutes les métadonnées
        document = {
            "titre": titre,
            "auteur": auteur,
            "date": date,
            "url": url,
            "texte": texte,
            "origine": "arxiv",
            "co_auteurs": co_auteurs  # Spécifique Arxiv (TD5)
        }
        
        docs.append(document)
        compteur_arxiv += 1
    
    print(f" {compteur_arxiv} articles Arxiv ajoutés")
    
except Exception as e:
    print(f" Erreur lors de la récupération Arxiv : {e}")
# VÉRIFICATION DES DONNÉES RÉCUPÉRÉES


print("\n" + "="*70)
print("           VÉRIFICATION DES DONNÉES")
print("="*70)

print(f"\n Nombre total de documents récupérés : {len(docs)}")
print(f"   - Reddit : {compteur_reddit}")
print(f"   - Arxiv  : {compteur_arxiv}")

# Affichage d'un exemple de document Reddit
print("\n Exemple de document Reddit :")
for doc in docs:
    if doc['origine'] == 'reddit':
        print(f"   Titre  : {doc['titre']}")
        print(f"   Auteur : {doc['auteur']}")
        print(f"   Date   : {doc['date']}")
        print(f"   URL    : {doc['url']}")
        print(f"   Texte  : {doc['texte'][:150]}...")
        break

# Affichage d'un exemple de document Arxiv
print("\n Exemple de document Arxiv :")
for doc in docs:
    if doc['origine'] == 'arxiv':
        print(f"   Titre  : {doc['titre']}")
        print(f"   Auteur : {doc['auteur']}")
        print(f"   Date   : {doc['date']}")
        print(f"   URL    : {doc['url']}")
        print(f"   Texte  : {doc['texte'][:150]}...")
        break

                 # TD4 : STRUCTURATION AVEC LES CLASSES


print("\n" + "="*70)
print("           TD4 - STRUCTURATION AVEC LES CLASSES")
print("="*70)

# Importation de nos classes personnalisées
from Document import Document
from Author import Author
from Corpus import Corpus

# Création du corpus principal
# A noté que : Le pattern Singleton (TD5) garantit qu'il n'y aura qu'une seule instance
corpus = Corpus("Corpus Intelligence Artificielle")
print(f"\n Création du corpus '{corpus.nom}'")

# FILTRAGE ET AJOUT DES DOCUMENTS AU CORPUS

print("\n Filtrage des documents et ajout au corpus")

# Importation de la Factory (TD5)
from DocumentFactory import DocumentFactory

compteur_ajoutes = 0
compteur_ignores = 0

# On parcourt tous les documents récupérés
for doc_dict in docs:
    # Filtrage : on ignore les documents avec un texte trop court
    # Décision du binôme : seuil minimal de 10 caractères
    texte = doc_dict['texte']
    if not texte or len(texte.strip()) < 10:
        compteur_ignores += 1
        continue  # On passe au document suivant
    
    # TD5 - FACTORY PATTERN : Création automatique du bon type de document
    # La Factory décide automatiquement si c'est un RedditDocument ou ArxivDocument
    # selon le champ 'origine' du dictionnaire
    doc = DocumentFactory.create_from_dict(doc_dict)
    
    # Ajout au corpus
    # Note : La méthode add_document() gère automatiquement :
    # - La création des auteurs s'ils n'existent pas encore
    # - L'association document-auteur
    # - L'incrémentation des compteurs
    corpus.add_document(doc)
    compteur_ajoutes += 1

print(f"\n {compteur_ajoutes} documents ajoutés au corpus")
if compteur_ignores > 0:
    print(f"  {compteur_ignores} documents ignorés (texte < 10 caractères)")

print(f"\n Résumé du corpus :")
print(corpus)

# AFFICHAGE ET MANIPULATION DU CORPUS


print("\n" + "="*70)
print("           EXPLORATION DU CORPUS")
print("="*70)

# Affichage des 5 premiers documents
print("\n Affichage des 5 premiers documents :")
corpus.show(5)

# Tri par date (documents les plus récents en premier)
print("\n Tri par date (documents les plus récents) :")
corpus.trier_par_date(n=5, ordre_croissant=False)

# Tri alphabétique par titre
print("\n Tri alphabétique par titre :")
corpus.trier_par_titre(n=5)

# Statistiques d'un auteur (exemple)
print("\n Statistiques d'un auteur (exemple) :")
if corpus.authors:
    # On prend le premier auteur du dictionnaire pour l'exemple
    premier_auteur_nom = list(corpus.authors.keys())[0]
    premier_auteur = corpus.authors[premier_auteur_nom]
    premier_auteur.afficher_stats()

# SAUVEGARDE DU CORPUS

print("\n" + "="*70)
print("           SAUVEGARDE DES DONNÉES")
print("="*70)

nom_fichier = "corpus_v1.csv"
print(f"\n Sauvegarde du corpus dans '{nom_fichier}'...")
corpus.save(nom_fichier)

# Test de chargement pour vérifier que la sauvegarde fonctionne
print(f"\n Test de chargement depuis '{nom_fichier}'...")
corpus_charge = Corpus.load(nom_fichier)
print(f" Corpus rechargé : {corpus_charge}")

# Vérification de l'intégrité des données
if corpus_charge.ndoc == corpus.ndoc:
    print(" Vérification : nombre de documents identique")
else:
    print(" Attention : différence dans le nombre de documents")

                 
                    # TD5 : VÉRIFICATION DES CLASSES FILLES


print("\n" + "="*70)
print("           TD5 - VÉRIFICATION DES CLASSES FILLES")
print("="*70)

# On importe les classes filles pour les tests
from Document import RedditDocument, ArxivDocument

# Comptage des documents par type
nb_reddit = 0
nb_arxiv = 0

for doc_id, doc in corpus.id2doc.items():
    if isinstance(doc, RedditDocument):
        nb_reddit += 1
    elif isinstance(doc, ArxivDocument):
        nb_arxiv += 1

print(f"\n Répartition des documents :")
print(f"   - RedditDocument : {nb_reddit}")
print(f"   - ArxivDocument  : {nb_arxiv}")

# Affichage d'un exemple de RedditDocument
print("\n Exemple de RedditDocument :")
for doc_id, doc in corpus.id2doc.items():
    if isinstance(doc, RedditDocument):
        doc.afficher()
        break

# Affichage d'un exemple d'ArxivDocument
print("\n Exemple d'ArxivDocument :")
for doc_id, doc in corpus.id2doc.items():
    if isinstance(doc, ArxivDocument):
        doc.afficher()
        break

# Test de la méthode get_type() (polymorphisme)
print("\n Test de la méthode get_type() :")
compteur_test = 0
for doc_id, doc in corpus.id2doc.items():
    print(f"   {doc.get_type()}: {doc.titre[:50]}")
    compteur_test += 1
    if compteur_test >= 5:  # On affiche seulement les 5 premiers
        break

# TD5 : TEST DES PATRONS DE CONCEPTION

print("\n" + "="*70)
print("           TD5 - PATRONS DE CONCEPTION")
print("="*70)

# Test du pattern Singleton

print("\n Test du pattern Singleton :")
print("Tentative de créer un deuxième corpus")

# On essaie de créer une nouvelle instance de Corpus
corpus2 = Corpus("Deuxième corpus")

# Vérification : corpus et corpus2 doivent être la MÊME instance
print(f"corpus == corpus2 ? {corpus is corpus2}")  # Doit afficher True
print(f"Nom du corpus2 : {corpus2.nom}")
print(f"Nombre de documents dans corpus2 : {corpus2.ndoc}")

# Explication : Même si on essaie de créer un nouveau Corpus,
# le pattern Singleton nous renvoie toujours la même instance.
# C'est pour garantir qu'il n'y a qu'un seul corpus dans le programme.

# Test du pattern Factory

print("\n Test du pattern Factory :")
print(" Création de documents avec la Factory")

# On crée un dictionnaire de test pour un document Reddit
test_dict_reddit = {
    'origine': 'reddit',
    'titre': 'Test Factory Reddit',
    'auteur': 'TestUser',
    'date': datetime.now(),
    'url': 'http://test.com',
    'texte': 'Texte de test pour la factory',
    'nb_commentaires': 99
}

# La Factory crée automatiquement un RedditDocument
doc_test = DocumentFactory.create_from_dict(test_dict_reddit)

print(f"   Document créé : {doc_test}")
print(f"   Type de l'objet : {type(doc_test).__name__}")
print(f"   Méthode get_type() : {doc_test.get_type()}")

# Explication : La Factory regarde le champ 'origine' et crée
# automatiquement le bon type de document (RedditDocument ou ArxivDocument).
# On n'a pas besoin de faire de if/else dans le code !

# FIN DU PROGRAMME


print("\n" + "="*70)
print("           TD3, TD4 et TD5 TERMINÉS AVEC SUCCÈS ")
print("="*70)

print("\n Récapitulatif final :")
print(f"   - Documents récupérés : {len(docs)}")
print(f"   - Documents dans le corpus : {corpus.ndoc}")
print(f"   - Auteurs identifiés : {corpus.naut}")
print(f"   - RedditDocument : {nb_reddit}")
print(f"   - ArxivDocument : {nb_arxiv}")
print(f"   - Fichier sauvegardé : {nom_fichier}")
print("="*70)