# -*- coding: utf-8 -*-
"""
================================================================================
                            FICHIER : Author.py
================================================================================


Ce fichier contient la classe Author qui représente un auteur et ses
publications dans le corpus.

RÔLE DE LA CLASSE AUTHOR :
    - Stocker les informations d'un auteur (nom, nombre de publications)
    - Gérer la liste de tous les documents écrits par cet auteur
    - Calculer des statistiques (nombre de docs, taille moyenne)
    - Permettre l'ajout facile de nouveaux documents

ATTRIBUTS PRINCIPAUX :
    - name (str)          : Nom de l'auteur
    - ndoc (int)          : Nombre de documents publiés
    - production (dict)   : Dictionnaire {id_doc: Document}

MÉTHODES PRINCIPALES :
    - add()              : Ajoute un document à la production
    - afficher_stats()   : Affiche les statistiques de l'auteur
    - __str__()          : Représentation textuelle de l'auteur

UTILISATION DANS LE PROJET :
    La classe Corpus crée automatiquement des objets Author quand elle
    rencontre de nouveaux auteurs lors de l'ajout de documents.
    
    Chaque auteur garde la trace de tous ses documents, ce qui permet
    de facilement calculer des statistiques par auteur.

EXEMPLE D'UTILISATION :
    auteur = Author("Dr. Smith")
    auteur.add(1, document1)
    auteur.add(2, document2)
    auteur.afficher_stats()

================================================================================
"""

                                # CLASSE AUTHOR

"""
 Classe représentant un auteur avec ses documents.
 
 Un auteur est identifié par son nom et possède une collection
 de tous les documents qu'il a écrits.
Constructeur de la classe Author.
 
 Paramètres:
     name (str): Le nom de l'auteur
 
 Initialisation:
     - name        : stocke le nom de l'auteur
     - ndoc        : compteur initialisé à 0
     - production  : dictionnaire vide qui va contenir tous les documents
 
 Note sur le dictionnaire production:
     Clé   = ID du document (entier unique)
     Valeur = Objet Document
     
     Exemple: production = {
         0: Document("Article 1", ...),
         1: Document("Article 2", ...),
         2: Document("Article 3", ...)
     }
 
 Exemple d'utilisation:
     auteur = Author("Alice Dupont")
"""
 
class Author:
   
    # CONSTRUCTEUR
   
    def __init__(self, name):
    
        self.name = name
        self.ndoc = 0  # Nombre de documents (commence à 0)
        self.production = {}  # Dictionnaire vide pour stocker les documents
    
    
    # MÉTHODE D'AJOUT DE DOCUMENT
    
    def add(self, doc_id, document):    # Ajoute un document à la production de l'auteur
                                        # doc_id (int)       : L'identifiant unique du document
                                        # document (Document): L'objet Document à ajouter
                                        # On utilise doc_id comme clé pour pouvoir facilement retrouver
        # Étape 1 : Ajouter le document au dictionnaire
        self.production[doc_id] = document
        
        # Étape 2 : Incrémenter le compteur
        self.ndoc += 1
   
    # MÉTHODES D'AFFICHAGE
    
    def __str__(self):              # Représentation textuelle courte de l'auteur.
                                    # Appelée automatiquement par print(auteur).
        
        return f"Auteur: {self.name}, {self.ndoc} document(s)"
    
    def afficher_stats(self):         # Affiche les statistiques détaillées de l'auteur.
                                        # Cette méthode ne fonctionne que si l'auteur a au moins
                                        # un document (ndoc > 0).
        print("="*50)
        print(f"Nom: {self.name}")
        print(f"Nombre de documents: {self.ndoc}")
        
        if self.ndoc > 0:
            # Calcul de la taille moyenne des documents
            # Étape 1 : On récupère la longueur de chaque texte
            # self.production.values() = tous les documents
            # len(doc.texte) = longueur du texte de chaque document
            # [...] = on crée une liste avec toutes ces longueurs
            tailles = [len(doc.texte) for doc in self.production.values()]
            
            # Étape 2 : On calcule la moyenne
            # sum(tailles) = somme de toutes les longueurs
            # len(tailles) = nombre de documents
            # moyenne = somme / nombre
            taille_moyenne = sum(tailles) / len(tailles)
            
            print(f"Taille moyenne des documents: {taille_moyenne:.2f} caractères")
            
            # Affichage de la liste des documents
            print(f"\nDocuments de {self.name}:")
            for doc_id, doc in self.production.items():
                # doc.type peut être "reddit" ou "arxiv"
                print(f"  - {doc.titre} ({doc.type})")
        else:
            # Si l'auteur n'a aucun document
            print("Aucun document publié")
        
        print("="*50)

"""

RELATION AVEC LA CLASSE CORPUS :

    Quand on ajoute un document au corpus:
        corpus.add_document(doc)
    
    Le corpus fait automatiquement:
        1. Récupère le nom de l'auteur : auteur_nom = doc.auteur
        2. Vérifie si l'auteur existe : if auteur_nom not in self.authors
        3. Si non, crée un nouvel auteur : self.authors[auteur_nom] = Author(auteur_nom)
        4. Ajoute le document à l'auteur : self.authors[auteur_nom].add(doc_id, doc)
    
    Résultat : Les auteurs et leurs productions sont gérés automatiquement !

EXEMPLE D'UTILISATION COMPLÈTE :

    # Création d'un auteur
    auteur = Author("Dr. Alice Smith")
    
    # Ajout de documents
    doc1 = Document("Article sur l'IA", "Dr. Alice Smith", ...)
    doc2 = Document("Article sur le ML", "Dr. Alice Smith", ...)
    
    auteur.add(0, doc1)
    auteur.add(1, doc2)
    
    # Affichage court
    print(auteur)  # Auteur: Dr. Alice Smith, 2 document(s)
    
    # Affichage détaillé
    auteur.afficher_stats()
    # ==================================================
    # Nom: Dr. Alice Smith
    # Nombre de documents: 2
    # Taille moyenne des documents: 256.50 caractères
    #
    # Documents de Dr. Alice Smith:
    #   - Article sur l'IA (arxiv)
    #   - Article sur le ML (arxiv)
    # ==================================================
"""


