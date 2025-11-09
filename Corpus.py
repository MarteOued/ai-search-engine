# -*- coding: utf-8 -*-
"""
================================================================================
                            FICHIER : Corpus.py
================================================================================


                            DESCRIPTION

Ce fichier contient la classe Corpus qui gère l'ensemble de la collection
de documents et d'auteurs du projet.

RÔLE DE LA CLASSE CORPUS :
    - Stocker tous les documents dans un dictionnaire (id2doc)
    - Gérer automatiquement les auteurs et leurs productions
    - Fournir des méthodes de tri et d'affichage
    - Permettre la sauvegarde et le chargement depuis CSV
    - Implémenter le pattern Singleton (TD5)

ATTRIBUTS PRINCIPAUX :
    - nom (str)        : Nom du corpus
    - authors (dict)   : Dictionnaire {nom_auteur: objet Author}
    - id2doc (dict)    : Dictionnaire {id_document: objet Document}
    - ndoc (int)       : Compteur de documents
    - naut (int)       : Compteur d'auteurs

MÉTHODES PRINCIPALES :
    - add_document()       : Ajoute un document au corpus
    - show()              : Affiche les documents
    - trier_par_date()    : Tri chronologique
    - trier_par_titre()   : Tri alphabétique
    - save()              : Sauvegarde en CSV
    - load()              : Chargement depuis CSV

PATTERN SINGLETON (TD5) :
    On garantit qu'il n'existe qu'une seule instance de Corpus dans le
    programme. Si on essaie de créer un deuxième Corpus, on récupère
    automatiquement l'instance existante.

================================================================================
"""
                       # IMPORTATION DES LIBRAIRIES

import pandas as pd           # Pour manipuler les tableaux de données
from datetime import datetime # Pour gérer les dates

# CLASSE CORPUS (SINGLETON)

class Corpus:                 # Classe représentant un corpus de documents.
                              # Implémente le pattern Singleton : une seule instance possible.
    
    
    # Variable de classe pour stocker l'instance unique (Singleton)
    _instance = None
    
  # TD5 - PATTERN SINGLETON : Contrôle de la création d'instance
   
    def __new__(cls, nom="Corpus"):
        """
        Méthode spéciale appelée AVANT __init__ lors de la création d'un objet.
        Implémente le pattern Singleton.
        
        Principe :
            - Si aucune instance n'existe (_instance = None), on en crée une
            - Si une instance existe déjà, on la retourne
            - Résultat : il n'y aura toujours qu'UNE SEULE instance de Corpus
        
        Paramètres:
            nom (str): Le nom du corpus (ignoré si instance déjà créée)
        
        Retourne:
            Corpus: L'instance unique du Corpus
        """
        if cls._instance is None:
            # Première création : on crée une nouvelle instance
            print(f"[Singleton] Création de l'instance unique du Corpus")
            cls._instance = super().__new__(cls)
            # On ajoute un flag pour savoir si l'initialisation a été faite
            cls._instance._initialized = False
        else:
            # Instance déjà existante : on la réutilise
            print(f"[Singleton] Instance du Corpus déjà existante, réutilisation")
        
        return cls._instance
    
   # CONSTRUCTEUR
   
    def __init__(self, nom="Corpus"):
        """
        Constructeur de la classe Corpus.
        N'initialise qu'une seule fois grâce au flag _initialized.
        
        Paramètres:
            nom (str): Le nom du corpus
        
        Note :
            Grâce au Singleton, même si __init__ est appelé plusieurs fois,
            les attributs ne sont initialisés qu'une seule fois.
        """
        # On vérifie si l'initialisation a déjà été faite
        if not self._initialized:
            # Première initialisation
            self.nom = nom
            self.authors = {}  # Dictionnaire des auteurs {nom: Author}
            self.id2doc = {}   # Dictionnaire des documents {id: Document}
            self.ndoc = 0      # Compteur de documents
            self.naut = 0      # Compteur d'auteurs
            self._initialized = True
            print(f"[Singleton] Corpus '{self.nom}' initialisé")
    
   # MÉTHODE PRINCIPALE : AJOUT D'UN DOCUMENT
    
    def add_document(self, document):        # On ajoute un document au corpus
        
        # Étape 1 : Générer un ID unique pour le document
        doc_id = self.ndoc
        
        # Étape 2 : Ajouter le document au dictionnaire id2doc
        self.id2doc[doc_id] = document
        self.ndoc += 1
        
        # Étape 3 : Gérer l'auteur
        auteur_nom = document.auteur
        
        # Étape 4 : Si l'auteur n'existe pas encore, on le crée
        if auteur_nom not in self.authors:
            from Author import Author
            self.authors[auteur_nom] = Author(auteur_nom)
            self.naut += 1
        
        # Étape 5 : Ajouter le document à la production de l'auteur
        self.authors[auteur_nom].add(doc_id, document)
    
    # MÉTHODES D'AFFICHAGE
    
    def __repr__(self):           # Représentation textuelle du corpus.
        
        return f"Corpus '{self.nom}': {self.ndoc} documents, {self.naut} auteurs"
    
    def show(self, n=10):

        print("="*70)
        print(f"Corpus: {self.nom}")
        print(f"Nombre de documents: {self.ndoc}")
        print(f"Nombre d'auteurs: {self.naut}")
        print("="*70)
        
        print(f"\n Affichage des {min(n, self.ndoc)} premiers documents:\n")
        
        # On parcourt le dictionnaire et on compte jusqu'à n
        compteur = 0
        for doc_id, doc in self.id2doc.items():
            if compteur >= n:
                break
            print(f"{compteur+1}. {doc}")  # Utilise la méthode __str__ du document
            compteur += 1
    
    # MÉTHODES DE TRI
   
    def trier_par_date(self, n=10, ordre_croissant=True):
        """
        Trie et affiche les documents par date de publication.
        
        Comment:
            1. On transforme le dictionnaire en liste de tuples (id, document)
            2. On trie cette liste selon la date du document
            3. On affiche les n premiers résultats
        """
        # Étape 1 : Créer une liste de tuples (doc_id, document)
        docs_liste = list(self.id2doc.items())
        
        # Étape 2 : Trier par date
        # reverse=not ordre_croissant : si ordre_croissant=False, reverse=True
        docs_tries = sorted(docs_liste, 
                           key=lambda x: x[1].date, 
                           reverse=not ordre_croissant)
        
        # Étape 3 : Afficher les résultats
        print("="*70)
        print(f"Documents triés par date ({'croissant' if ordre_croissant else 'décroissant'}):")
        print("="*70)
        
        for i, (doc_id, doc) in enumerate(docs_tries[:n]):
            # strftime('%Y-%m-%d') : formatte la date en YYYY-MM-DD
            print(f"{i+1}. [{doc.date.strftime('%Y-%m-%d')}] {doc.titre} ({doc.type})")
    
    def trier_par_titre(self, n=10):        # Trie et affiche les documents par titre (ordre alphabétique).
        
                                               # .lower() permet un tri insensible à la casse
       
        # Étape 1 : Créer une liste de tuples (doc_id, document)
        docs_liste = list(self.id2doc.items())
        
        # Étape 2 : Trier par titre (en minuscules pour ignorer la casse)
        docs_tries = sorted(docs_liste, key=lambda x: x[1].titre.lower())
        
        # Étape 3 : Afficher les résultats
        print("="*70)
        print(f"Documents triés par titre (alphabétique):")
        print("="*70)
        
        for i, (doc_id, doc) in enumerate(docs_tries[:n]):
            print(f"{i+1}. {doc.titre} ({doc.type})")
    
  # MÉTHODES DE SAUVEGARDE ET CHARGEMENT
    
    def save(self, nom_fichier):
        
        # Étape 1 : Créer une liste de dictionnaires
        data = []
        for doc_id, doc in self.id2doc.items():
            data.append({
                'id': doc_id,
                'titre': doc.titre,
                'auteur': doc.auteur,
                'date': doc.date,
                'url': doc.url,
                'texte': doc.texte,
                'type': doc.type
            })
        
        # Étape 2 : Créer un DataFrame pandas
        df = pd.DataFrame(data)
        
        # Étape 3 : Sauvegarder en CSV
        # sep='\t' : séparateur = tabulation
        # index=False : ne pas sauvegarder l'index de pandas
        df.to_csv(nom_fichier, sep='\t', index=False)
        print(f" Corpus sauvegardé dans '{nom_fichier}'")
    
    @staticmethod
    def load(nom_fichier):
            # @staticmethod signifie qu'on peut appeler cette méthode
            # sans avoir créé d'instance de Corpus.
           
        from Document import Document
        
        # Étape 1 : Charger le CSV
        df = pd.read_csv(nom_fichier, sep='\t')
        
        # Étape 2 : Créer un nouveau corpus
        corpus = Corpus("Corpus chargé")
        
        # Étape 3 : Pour chaque ligne du CSV
        for index, row in df.iterrows():
            # Convertir la date (qui est en format texte dans le CSV)
            date = pd.to_datetime(row['date'])
            
            # Créer un objet Document
            doc = Document(
                titre=row['titre'],
                auteur=row['auteur'],
                date=date,
                url=row['url'],
                texte=row['texte'],
                type_doc=row['type']
            )
            
            # Étape 4 : Ajouter au corpus
            # La méthode add_document() gère automatiquement les auteurs
            corpus.add_document(doc)
        
        print(f" Corpus chargé depuis '{nom_fichier}'")
        return corpus


