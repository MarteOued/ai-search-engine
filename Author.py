# -*- coding: utf-8 -*-
"""
Author.py

Ce fichier contient la classe Author qui représente un auteur et ses
publications dans le corpus.

"""

                                # CLASSE AUTHOR : Fait par Martine
 
class Author:
   
    # CONSTRUCTEUR
   
    def __init__(self, name):
    
        self.name = name
        self.ndoc = 0  # Nombre de documents 
        self.production = {}  # Dictionnaire vide pour stocker les documents
    
    
    # MÉTHODE D'AJOUT DE DOCUMENT
    
    def add(self, doc_id, document):    # on ajoute un document à la production de l'auteur
                                        # doc_id (int)       : L'identifiant unique du document
                                        # document: L'objet Document à ajouter
                                        # on utilise doc_id comme clé pour pouvoir facilement retrouver
        # Ajout de document au dictionaire
        self.production[doc_id] = document
        
        # Incrémentation du compteur
        self.ndoc += 1
   
    # Les methodes d'affichage
    
    def __str__(self):              # permet de représente textuellement  l'auteur.
                                    # et est appelée automatiquement par print(auteur).
        
        return f"Auteur: {self.name}, {self.ndoc} document(s)"
    
    def afficher_stats(self):         # permet d'afficher les statistiques détaillées de l'auteur.
                                        # cette méthode ne fonctionne que si l'auteur a au moins
                                        # un document (ndoc > 0).
        
        print(f"Nom: {self.name}")
        print(f"Nombre de documents: {self.ndoc}")
        
        if self.ndoc > 0:
            # calcul de la taille moyenne des documents
            
            tailles = [len(doc.texte) for doc in self.production.values()]
            
            # calcule la moyenne
            
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
        
        




