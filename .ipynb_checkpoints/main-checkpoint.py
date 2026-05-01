# -*- coding: utf-8 -*-
"""
                   PROJET : MOTEUR DE RECHERCHE D'INFORMATION

Auteurs : Julien et Martine
Date    : Novembre 2025
Thématique : Intelligence Artificielle



Ce programme implémente un moteur de recherche d'information sur le thème de
l'Intelligence Artificielle. Il est divisé en plusieurs parties :

TD3, TD4, TD5, TD6; TD7

"""
                            # IMPORTATION DES LIBRAIRIES


import praw                        # pour se connecter à Reddit
import urllib.request              # pour faire des requêtes web (Arxiv)
import xmltodict                   # pour lire les réponses d'Arxiv (XML)
import pandas as pd                # pour manipuler les données (tableaux)
from datetime import datetime      # pour gérer les dates
from SearchEngine import SearchEngine

                        # TD3 - PARTIE 1 : ACQUISITION DES DONNÉES

print("           TD3 - ACQUISITION DES DONNÉES")


# 1.1 RÉCUPÉRATION DES DONNÉES REDDIT

print("\n Connexion à l'API Reddit ")

# on se connecte à Reddit avec nos identifiants développeur

reddit = praw.Reddit(
    client_id="LE2COTSsmlNvVRBivOkeqA",
    client_secret="vKXo3JAwS-Jt9I0_yW68GCQzkPlN-A",
    user_agent="JuleMarte_Recherche"
)
print(" Connexion à Reddit réussie !")

# liste qui va contenir tous nos documents (Reddit + Arxiv)
docs = []

# Thématique que nous avons choisie : Intelligence Artificielle

query = "artificial intelligence"
limit = 100  # nombre de posts à récupérer

print(f"\n Recherche de posts Reddit sur '{query}'...")
print(f"Limite fixée : {limit} posts")

# on lance la recherche sur Reddit (tous les subreddits)
subreddit = reddit.subreddit("all")
hot_posts = subreddit.search(query, limit=limit)

# on parcourt tous les posts trouvés
compteur_reddit = 0
for post in hot_posts:
    # extraction des informations de base
    titre = post.title
    auteur = str(post.author)
    date = datetime.fromtimestamp(post.created_utc)
    url = f"https://www.reddit.com{post.permalink}"
    texte = post.selftext
    
    # nettoyage : on remplace les sauts de ligne par des espaces
    texte = texte.replace("\n", " ")
    
    # TD5 : on récupère aussi le nombre de commentaires (spécifique à Reddit)
    nb_commentaires = post.num_comments if hasattr(post, "num_comments") else 0

    
    # on crée un dictionnaire avec toutes les métadonnées
    document = {
        "titre": titre,
        "auteur": auteur,
        "date": date,
        "url": url,
        "texte": texte,
        "origine": "reddit",
        "nb_commentaires": nb_commentaires  # Spécifique Reddit (TD5)
    }
    
    # on ajoute ce document à notre list
    docs.append(document)
    compteur_reddit += 1

print(f" {compteur_reddit} posts Reddit récupérés")

# 1.2 RÉCUPÉRATION DES ARTICLES ARXIV


print("\n" + "="*70)
print(" Récupération des articles Arxiv...")

# Construction de l'URL pour interroger l'API Arxiv

query_arxiv = "artificial+intelligence"  # les espaces deviennent des +
url = f"http://export.arxiv.org/api/query?search_query=all:{query_arxiv}&start=0&max_results=100"

print(f"URL : {url}")

# on fait la requête HTTP à l'API Arxiv
try:
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    
    # on transforme le XML reçu en dictionnaire Python
    arxiv_data = xmltodict.parse(data)
    entries = arxiv_data['feed']['entry']
    
    print(f" {len(entries)} articles Arxiv trouvés")
    
    # on parcourt tous les articles
    compteur_arxiv = 0
    for entry in entries:
        # extrai du titre
        titre = entry['title']
        
        # TD5 : Gestion des co-auteurs (spécifique à Arxiv)
        # un article peut avoir un ou plusieurs auteurs
        co_auteurs = []
        if isinstance(entry['author'], list):
            # Cas 1 : Plusieurs auteurs
            auteur = entry['author'][0]['name']  # le premier est l'auteur principal
            # les autres sont des co-auteurs
            co_auteurs = [a['name'] for a in entry['author'][1:]]
        else:
            # Cas 2 : Un seul auteur
            auteur = entry['author']['name']
            co_auteurs = []  # Pas de co-auteurs
        
        # on converti la date (format ISO)
        date_str = entry['published']
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        
        # récupere l'URL et le résumé
        url = entry['id']
        texte = entry['summary']
        texte = texte.replace("\n", " ")
        
        # on crée un dictionnaire avec toutes les métadonnées
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

print("           VÉRIFICATION DES DONNÉES")


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

print("           TD4 - STRUCTURATION AVEC LES CLASSES")


# Importation de nos classes personnalisées
from Document import Document
from Author import Author
from Corpus import Corpus

# Création du corpus principal
# a noté que : Le pattern Singleton (TD5) garantit qu'il n'y aura qu'une seule instance
corpus = Corpus("Corpus Intelligence Artificielle")
print(f"\n Création du corpus '{corpus.nom}'")

# FILTRAGE ET AJOUT DES DOCUMENTS AU CORPUS

print("\n Filtrage des documents et ajout au corpus")

# Importation de la Factory (TD5)
from DocumentFactory import DocumentFactory

compteur_ajoutes = 0
compteur_ignores = 0

# on parcourt tous les documents récupérés
for doc_dict in docs:
    # on ignore les documents avec un texte trop court
    # décision du binôme : seuil minimal de 10 caractères
    texte = doc_dict['texte']
    if not texte or len(texte.strip()) < 10:
        compteur_ignores += 1
        continue  # on passe au document suivant
    
    # TD5 - FACTORY PATTERN : Création automatique du bon type de document
    # la Factory décide automatiquement si c'est un RedditDocument ou ArxivDocument
    # selon le champ 'origine' du dictionnaire
    doc = DocumentFactory.create_from_dict(doc_dict)
    
    # ajout au corpus
    corpus.add_document(doc)
    compteur_ajoutes += 1

print(f"\n {compteur_ajoutes} documents ajoutés au corpus")
if compteur_ignores > 0:
    print(f"  {compteur_ignores} documents ignorés (texte < 10 caractères)")

print(f"\n Résumé du corpus :")
print(corpus)

# AFFICHAGE ET MANIPULATION DU CORPUS

print("           EXPLORATION DU CORPUS")


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
    # on prend le premier auteur du dictionnaire pour l'exemple
    premier_auteur_nom = list(corpus.authors.keys())[0]
    premier_auteur = corpus.authors[premier_auteur_nom]
    premier_auteur.afficher_stats()

# SAUVEGARDE DU CORPUS

print("           SAUVEGARDE DES DONNÉES")

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

print("           TD5 - VÉRIFICATION DES CLASSES FILLES")

#on importe les classes filles pour les tests
from Document import RedditDocument, ArxivDocument

# compte des documents par type
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

print("           TD5 - PATRONS DE CONCEPTION")

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

# on crée un dictionnaire de test pour un document Reddit
test_dict_reddit = {
    'origine': 'reddit',
    'titre': 'Test Factory Reddit',
    'auteur': 'TestUser',
    'date': datetime.now(),
    'url': 'http://test.com',
    'texte': 'Texte de test pour la factory',
    'nb_commentaires': 99
}

# la Factory crée automatiquement un RedditDocument
doc_test = DocumentFactory.create_from_dict(test_dict_reddit)

print(f"   Document créé : {doc_test}")
print(f"   Type de l'objet : {type(doc_test).__name__}")
print(f"   Méthode get_type() : {doc_test.get_type()}")

# Explication : La Factory regarde le champ 'origine' et crée
# automatiquement le bon type de document (RedditDocument ou ArxivDocument).
# On n'a pas besoin de faire de if/else dans le code !

# FIN DU PROGRAMME

print("           TD3, TD4 et TD5 TERMINÉS ")

print("\n Récapitulatif final :")
print(f"   - Documents récupérés : {len(docs)}")
print(f"   - Documents dans le corpus : {corpus.ndoc}")
print(f"   - Auteurs identifiés : {corpus.naut}")
print(f"   - RedditDocument : {nb_reddit}")
print(f"   - ArxivDocument : {nb_arxiv}")
print(f"   - Fichier sauvegardé : {nom_fichier}")

#                    TD6 - ANALYSE DU CONTENU TEXTUEL

print("           TD6 - ANALYSE DU CONTENU TEXTUEL")

# TEST 1 : RECHERCHE D'UN MOT-CLÉ

print("\n Test 1 : Recherche du mot 'intelligence'")
passages = corpus.search("intelligence")
print(f"\nAffichage des 3 premiers passages :")
for i, passage in enumerate(passages[:3], 1):
    print(f"\n{i}. ...{passage}...")

# TEST 2 : CONCORDANCIER

print(" Test 2 : Concordancier pour 'artificial'")
concordancier = corpus.concorde("artificial", taille_contexte=40)
print("\nAffichage des 10 premières lignes :")
print(concordancier.head(10))

# TEST 3 : STATISTIQUES TEXTUELLES


print("Test 3 : Statistiques textuelles")
freq_table = corpus.stats(20)

# on sauvegarde le tableau des fréquences 
freq_table.to_csv("frequences.csv", sep='\t', index=False)
print("\n Tableau des fréquences sauvegardé dans 'frequences.csv'")

# TEST 4 : NETTOYAGE DE TEXTE

print(" Test 4 : Démonstration du nettoyage de texte")
texte_test = "Hello, World! This is a TEST 123. New line:\nSecond line."
texte_nettoye = Corpus.nettoyer_texte(texte_test)
print(f"Avant : {texte_test}")
print(f"Après : {texte_nettoye}")
print("                 TD6 TERMINÉ : Analyse textuelle complétée !")


#                    TD7 - IMPLEMENTATION MOTEUR DE RECHERCHE
print("\n--- TD7 : MOTEUR DE RECHERCHE ---")

# 1. Instanciation du moteur (Prend le corpus en paramètre)
# La matrice est construite automatiquement ici grâce au __init__
engine = SearchEngine(corpus)

# 2. Affichage du vocabulaire enrichi (limité à 20 mots pour lisibilité)
print("\n--- Aperçu du vocabulaire enrichi de tout le corpus (20 mots) ---")
for i, (mot, infos) in enumerate(engine.vocab.items()):
    if i >= 20:
        print("... (vocabulaire limité a 20 pour éviter un affichage trop long)")
        break
    print(f"{mot} => {infos}")

# 3. Lancement d'une recherche
requete = "artificial intelligence jobs"
print(f"\nRecherche pour : '{requete}'")

# 4. Récupération des résultats sous forme de DataFrame
df_resultats = engine.search(requete, n_results=5)

# 5. bel affichage avec Pandas
if not df_resultats.empty:
    print("\nRésultats trouvés :")
    # On affiche juste quelques colonnes intéressantes
    print(df_resultats[['Score', 'Titre', 'Source']])
else:
    print("Aucun résultat trouvé.")