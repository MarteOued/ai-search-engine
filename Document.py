# -*- coding: utf-8 -*-
"""
================================================================================
                            FICHIER : Document.py
================================================================================
                      
                               DESCRIPTION

Ce fichier contient les classes pour représenter les documents du corpus.
On utilise l'héritage pour gérer les spécificités de chaque source.

HIÉRARCHIE DES CLASSES :
    Document (classe mère)
        ├── RedditDocument (classe fille)
        └── ArxivDocument (classe fille)

CLASSE MÈRE - DOCUMENT :
    Représente un document générique avec les attributs communs :
    - titre, auteur, date, url, texte, type

CLASSE FILLE - REDDITDOCUMENT :
    Hérite de Document et ajoute :
    - nb_commentaires : nombre de commentaires sur le post

CLASSE FILLE - ARXIVDOCUMENT :
    Hérite de Document et ajoute :
    - co_auteurs : liste des co-auteurs de l'article

PRINCIPE DE L'HÉRITAGE :
    Les classes filles héritent de toutes les méthodes et attributs de la
    classe mère, et peuvent en ajouter de nouveaux ou les redéfinir.
    
    Avantage : On évite la duplication de code !

POLYMORPHISME :
    Les trois classes ont toutes une méthode get_type() et __str__()
    mais avec des comportements différents selon le type.

================================================================================
"""
                     # CLASSE MÈRE : DOCUMENT
"""
 Classe mère représentant un document générique du corpus.
 
 Cette classe contient tous les attributs communs à tous les types
 de documents (Reddit, Arxiv, etc.).
 Constructeur de la classe Document.
 Appelé automatiquement quand on crée un nouvel objet Document.
 
 Paramètres:
     titre (str)     : Le titre du document
     auteur (str)    : Le nom de l'auteur principal
     date (datetime) : La date de publication
     url (str)       : L'URL source du document
     texte (str)     : Le contenu textuel
     type_doc (str)  : Le type de document ('reddit' ou 'arxiv')

"""

class Document:
    
   # CONSTRUCTEUR
    
    def __init__(self, titre, auteur, date, url, texte, type_doc):
        
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type_doc
    
    # MÉTHODES D'AFFICHAGE
    
    def __str__(self):           # str: est une représentation courte et lisible du document
        
        return f"{self.titre} ({self.type})"
    
    def afficher(self):          # Affiche toutes les informations du document de façon détaillée.
        
        
        print("="*50)
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f"Type: {self.type}")
        print(f"Texte (extrait): {self.texte[:200]}...")
        print("="*50)
    
    # ACCESSEUR
    
    def get_type(self):      # Retourne le type du document
                                # Cette méthode sera redéfinie dans les classes filles
                                # pour retourner des valeurs plus spécifiques
        return self.type

                      # CLASSE FILLE 1 : REDDITDOCUMENT

"""
Classe représentant un document provenant de Reddit.
Hérite de la classe Document et ajoute des attributs spécifiques à Reddit.

Attribut spécifique:
    - nb_commentaires : nombre de commentaires sur le post

Principe de l'héritage:
    RedditDocument possède TOUS les attributs et méthodes de Document
    (titre, auteur, date, etc.) PLUS ses propres attributs spécifiques.

 Constructeur de RedditDocument.
 
 On utilise super() pour appeler le constructeur de la classe mère
 (Document) et lui passer les paramètres communs.
 
 Paramètres:
     titre, auteur, date, url, texte : hérités de Document
     nb_commentaires (int) : nombre de commentaires (défaut: 0)
 
 Explication de super():
     super().__init__(...) appelle le constructeur de Document
     Cela évite de réécrire tout le code d'initialisation 
"""
class RedditDocument(Document):
    
   # CONSTRUCTEUR
   
    def __init__(self, titre, auteur, date, url, texte, nb_commentaires=0):
        
        # On appelle le constructeur de la classe mère (Document)
        # Le type est automatiquement défini à "reddit"
        super().__init__(titre, auteur, date, url, texte, "reddit")
        
        # On ajoute l'attribut spécifique à Reddit
        self.nb_commentaires = nb_commentaires
   
    # ACCESSEURS ET MUTATEURS
    
    def get_nb_commentaires(self):
        
        return self.nb_commentaires
    
    def set_nb_commentaires(self, nb):
        
        self.nb_commentaires = nb
    
    # MÉTHODES REDÉFINIES (POLYMORPHISME)
    
    def __str__(self):

        return f"{self.titre} (Reddit - {self.nb_commentaires} commentaires)"
    
    def get_type(self):           # str: "Reddit"
                                   # Cette méthode remplace celle de la classe mère.
                                   # C'est le principe du polymorphisme !
        
        return "Reddit"
    
    def afficher(self):
        
        print("="*50)
        print(f" DOCUMENT REDDIT")
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f" Commentaires: {self.nb_commentaires}")
        print(f"Texte (extrait): {self.texte[:200]}...")
        print("="*50)

                  # CLASSE FILLE 2 : ARXIVDOCUMENT
"""
Classe représentant un document provenant d'Arxiv.
Hérite de la classe Document et ajoute des attributs spécifiques à Arxiv.

Attribut spécifique:
    - co_auteurs : liste des co-auteurs de l'article

Particularité des articles scientifiques:
    Les articles Arxiv sont souvent écrits par plusieurs chercheurs.
    On garde le premier comme auteur principal et les autres comme
    co-auteurs dans une liste.

Constructeur de ArxivDocument.
 
 Paramètres:
     titre, auteur, date, url, texte : hérités de Document
     co_auteurs (list) : liste des co-auteurs (défaut: liste vide)
 
 Note sur co_auteurs=None:
     On utilise None par défaut plutôt qu'une liste vide []
     car en Python, les listes par défaut peuvent causer des bugs
     (liste partagée entre toutes les instances).
"""

class ArxivDocument(Document):
   
    # CONSTRUCTEUR
   
    def __init__(self, titre, auteur, date, url, texte, co_auteurs=None):
        
        # On appelle le constructeur de la classe mère (Document)
        # Le type est automatiquement défini à "arxiv"
        super().__init__(titre, auteur, date, url, texte, "arxiv")
        
        # On initialise la liste des co-auteurs
        # Si co_auteurs est None, on crée une liste vide
        # Sinon, on utilise la liste fournie
        self.co_auteurs = co_auteurs if co_auteurs is not None else []
    
  # ACCESSEURS ET MUTATEURS
    
    def get_co_auteurs(self):

        return self.co_auteurs
    
    def set_co_auteurs(self, co_auteurs):
       
        self.co_auteurs = co_auteurs
    
    def add_co_auteur(self, nom):
        
        if nom not in self.co_auteurs:
            self.co_auteurs.append(nom)
   
    # MÉTHODES REDÉFINIES (POLYMORPHISME)
    def __str__(self):

        nb_coauteurs = len(self.co_auteurs)
        if nb_coauteurs > 0:
            return f"{self.titre} (Arxiv - {nb_coauteurs} co-auteur(s))"
        else:
            return f"{self.titre} (Arxiv)"
    
    def get_type(self):        # Polymorphisme : même nom de méthode, comportement différent.
       
        return "Arxiv"
    
    def afficher(self):
        
        print("="*50)
        print(f" DOCUMENT ARXIV")
        print(f"Titre: {self.titre}")
        print(f"Auteur principal: {self.auteur}")
        
        # Affichage des co-auteurs
        if self.co_auteurs:
            # ', '.join() transforme la liste en texte séparé par des virgules
            print(f" Co-auteurs: {', '.join(self.co_auteurs)}")
        else:
            print(f" Co-auteurs: Aucun")
        
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f"Texte (extrait): {self.texte[:200]}...")
        print("="*50)

#                      RÉCAPITULATIF DE L'HÉRITAGE

"""
STRUCTURE HIÉRARCHIQUE :

    Document (classe mère)
        - Attributs : titre, auteur, date, url, texte, type
        - Méthodes : __init__, __str__, afficher(), get_type()
        
            ├── RedditDocument (classe fille)
            │       - Attributs hérités : titre, auteur, date, url, texte, type
            │       - Attribut ajouté : nb_commentaires
            │       - Méthodes redéfinies : __str__, get_type(), afficher()
            │       - Méthodes ajoutées : get_nb_commentaires(), set_nb_commentaires()
            │
            └── ArxivDocument (classe fille)
                    - Attributs hérités : titre, auteur, date, url, texte, type
                    - Attribut ajouté : co_auteurs
                    - Méthodes redéfinies : __str__, get_type(), afficher()
                    - Méthodes ajoutées : get_co_auteurs(), set_co_auteurs(), add_co_auteur()

AVANTAGES DE L'HÉRITAGE :
     On évite de répéter le code commun
     On peut facilement ajouter de nouveaux types de documents
     On peut traiter tous les documents de la même façon (polymorphisme)
     Le code est plus organisé et maintenable

POLYMORPHISME EN ACTION :
    On peut faire :
        docs = [RedditDocument(...), ArxivDocument(...), Document(...)]
        for doc in docs:
            print(doc.get_type())  # Chaque classe retourne sa propre valeur !
"""


