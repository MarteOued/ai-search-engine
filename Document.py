# -*- coding: utf-8 -*-
"""
Document.py


Ce fichier contient les classes pour représenter les documents du corpus.
On utilise l'héritage pour gérer les spécificités de chaque source.

HIÉRARCHIE DES CLASSES :
    Document (classe mère)
         RedditDocument (classe fille)
         ArxivDocument (classe fille)
"""
                     # CLASSE MÈRE : DOCUMENT    Fait par Julien       
                     
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
    
    def afficher(self):          # affiche toutes les informtions du document de façon détaillée.
        
        
        print("="*50)
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f"Type: {self.type}")
        print(f"Texte (extrait): {self.texte[:200]}...")
        print("="*50)
    
    # ACCESSEUR
    
    def get_type(self):      # retourne le type du document
                                # cette méthode sera redéfinie dans les classes filles
                                # pour retourner des valeurs plus spécifiques
        return self.type

                      # CLASSE FILLE 1 : RedditDocument             

"""
Classe représentant un document provenant de Reddit.
Hérite de la classe Document et ajoute des attributs spécifiques à Reddit.

"""
class RedditDocument(Document):
    
   # CONSTRUCTEUR
   
    def __init__(self, titre, auteur, date, url, texte, nb_commentaires=0):
        
        # on appelle le constructeur de la classe mère (Document)
        # le type est automatiquement défini à "reddit"
        super().__init__(titre, auteur, date, url, texte, "reddit")
        
        # on ajoute l'attribut spécifique à Reddit
        self.nb_commentaires = nb_commentaires
   
    # Accesseurs et Mutateurs 
    
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

        print(f" DOCUMENT REDDIT")
        print(f"Titre: {self.titre}")
        print(f"Auteur: {self.auteur}")
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f" Commentaires: {self.nb_commentaires}")
        print(f"Texte (extrait): {self.texte[:200]}...")
        

                  # CLASSE FILLE 2 : ARXIVDOCUMENT   
"""
Classe représentant un document provenant d'Arxiv.
Hérite de la classe Document et ajoute des attributs spécifiques à Arxiv.

"""

class ArxivDocument(Document):
   
    # CONSTRUCTEUR
   
    def __init__(self, titre, auteur, date, url, texte, co_auteurs=None):
        
        # on appelle le constructeur de la classe mère (Document)
        # le type est automatiquement défini à "arxiv"
        super().__init__(titre, auteur, date, url, texte, "arxiv")
        
        # on initialise la liste des co-auteurs
        # si co_auteurs est None, on crée une liste vide
        # sinon, on utilise la liste fournie
        self.co_auteurs = co_auteurs if co_auteurs is not None else []
    
  # Accesseurs et Mutateurs 
    
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
        
        print(f" DOCUMENT ARXIV")
        print(f"Titre: {self.titre}")
        print(f"Auteur principal: {self.auteur}")
        
        # Affichage des co-auteurs
        if self.co_auteurs:
            print(f" Co-auteurs: {', '.join(self.co_auteurs)}")    # transforme la liste en texte séparé par des virgules
        else:
            print(f" Co-auteurs: Aucun")
        
        print(f"Date: {self.date}")
        print(f"URL: {self.url}")
        print(f"Texte (extrait): {self.texte[:200]}...")
        




