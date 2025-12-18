# -*- coding: utf-8 -*-
"""
 DocumentFactory.py
                        
Ce fichier implémente le pattern Factory pour la création automatique
de documents selon leur type (TD5).

"""

                     # IMPORTATION DES CLASSES   Fait Par Martine

from Document import Document, RedditDocument, ArxivDocument

# CLASSE DOCUMENTFACTORY, Factory pour créer des documents selon leur type.


class DocumentFactory:
    
   # MÉTHODE 1 : CRÉATION AVEC PARAMÈTRES INDIVIDUELS
     
    @staticmethod
    def create_document(doc_type, titre, auteur, date, url, texte, **kwargs):
          
        # CAS 1 : Document Reddit
        if doc_type.lower() == 'reddit':
            # on récupère les nb_commentaire dans kwargs
            nb_commentaires = kwargs.get('nb_commentaires', 0)
            
            # on crée et retourne un RedditDocument
            return RedditDocument(titre, auteur, date, url, texte, nb_commentaires)
        
        # CAS 2 : Document Arxiv
        elif doc_type.lower() == 'arxiv':
            # on récupère co_auteurs dans kwargs
            co_auteurs = kwargs.get('co_auteurs', [])  # Si absent, on utilise une liste vide []
            
            # on cré et retourne un ArxivDocument
            return ArxivDocument(titre, auteur, date, url, texte, co_auteurs)
        
        # CAS 3 : Type inconnu
        else:
            # si le type n'est ni 'reddit' ni 'arxiv', on crée un Document générique
            print(f" Type '{doc_type}' inconnu, création d'un Document générique")
            return Document(titre, auteur, date, url, texte, doc_type)
    
    # MÉTHODE 2 : CRÉATION À PARTIR D'UN DICTIONNAIRE
    
    @staticmethod
    def create_from_dict(doc_dict):    
    
        # on appelle create_document() en extrayant les valeurs du dictionnaire
        return DocumentFactory.create_document(
            doc_type=doc_dict['origine'],           
            titre=doc_dict['titre'],                
            auteur=doc_dict['auteur'],              
            date=doc_dict['date'],                  
            url=doc_dict['url'],                    
            texte=doc_dict['texte'],                
            nb_commentaires=doc_dict.get('nb_commentaires', 0),  # Pour Reddit
            co_auteurs=doc_dict.get('co_auteurs', [])            # Pour Arxiv
        )




