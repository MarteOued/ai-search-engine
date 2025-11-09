# -*- coding: utf-8 -*-
"""
================================================================================
                        FICHIER : DocumentFactory.py
================================================================================

                           DESCRIPTION

Ce fichier implémente le pattern Factory pour la création automatique
de documents selon leur type (TD5).

PATTERN FACTORY - PRINCIPE :
    Au lieu de faire des if/else partout dans le code pour créer le bon
    type de document (RedditDocument ou ArxivDocument), on centralise
    cette logique dans une classe Factory.
    
    Le code appelant n'a plus besoin de savoir quel type créer,
    il demande simplement à la Factory et elle s'en charge !

AVANTAGES DU PATTERN FACTORY :
     Centralisation : toute la logique de création est au même endroit
     Simplicité : le code appelant devient plus simple et lisible
     Extensibilité : facile d'ajouter de nouveaux types de documents
     Maintenance : si on change la logique, on ne modifie qu'un seul endroit

FONCTIONNEMENT :
    1. On donne à la Factory le type de document ('reddit' ou 'arxiv')
    2. On donne aussi tous les paramètres nécessaires
    3. La Factory crée automatiquement le bon objet (RedditDocument ou ArxivDocument)
    4. On récupère l'objet créé, prêt à utiliser !

MÉTHODES PRINCIPALES :
    - create_document()   : Crée un document à partir de paramètres individuels
    - create_from_dict()  : Crée un document à partir d'un dictionnaire

UTILISATION DANS LE PROJET :
    Dans main.py, on utilise la Factory pour créer automatiquement
    le bon type de document lors de l'ajout au corpus :
    
        doc = DocumentFactory.create_from_dict(doc_dict)
        corpus.add_document(doc)
    
    Sans Factory, il faudrait faire :
        if doc_dict['origine'] == 'reddit':
            doc = RedditDocument(...)
        else:
            doc = ArxivDocument(...)

PRINCIPE SOLID RESPECTÉ :
    - Open/Closed Principle : Le code est ouvert à l'extension (on peut
      ajouter de nouveaux types) mais fermé à la modification (pas besoin
      de changer la Factory si on ajoute un type).

================================================================================
"""

                     # IMPORTATION DES CLASSES

from Document import Document, RedditDocument, ArxivDocument

# CLASSE DOCUMENTFACTORY
"""
Factory pour créer des documents selon leur type.

Pattern de conception : Factory Method

Cette classe ne contient que des méthodes statiques car on n'a pas
besoin de créer une instance de DocumentFactory. On l'utilise
directement : DocumentFactory.create_document(...)
"""

class DocumentFactory:
    
   # MÉTHODE 1 : CRÉATION AVEC PARAMÈTRES INDIVIDUELS
     
    @staticmethod
    def create_document(doc_type, titre, auteur, date, url, texte, **kwargs):
       
       # Crée un document du bon type selon doc_type.
       # On regarde le type demandé et on crée l'objet correspondant.
       # **kwargs: Paramètres supplémentaires variables
          #  - nb_commentaires (int) : pour Reddit
          # - co_auteurs (list)     : pour Arxiv
          
        # CAS 1 : Document Reddit
        if doc_type.lower() == 'reddit':
            # On récupère nb_commentaires dans kwargs
            # .get('nb_commentaires', 0) signifie :
            # - Si 'nb_commentaires' existe dans kwargs, on le prend
            # - Sinon, on utilise 0 par défaut
            nb_commentaires = kwargs.get('nb_commentaires', 0)
            
            # On crée et retourne un RedditDocument
            return RedditDocument(titre, auteur, date, url, texte, nb_commentaires)
        
        # CAS 2 : Document Arxiv
        elif doc_type.lower() == 'arxiv':
            # On récupère co_auteurs dans kwargs
            # Si absent, on utilise une liste vide []
            co_auteurs = kwargs.get('co_auteurs', [])
            
            # On crée et retourne un ArxivDocument
            return ArxivDocument(titre, auteur, date, url, texte, co_auteurs)
        
        # CAS 3 : Type inconnu
        else:
            # Si le type n'est ni 'reddit' ni 'arxiv', on crée un Document générique
            print(f" Type '{doc_type}' inconnu, création d'un Document générique")
            return Document(titre, auteur, date, url, texte, doc_type)
    
    # MÉTHODE 2 : CRÉATION À PARTIR D'UN DICTIONNAIRE
    
    @staticmethod
    def create_from_dict(doc_dict):     #  Crée un document à partir d'un dictionnaire
                                        # Cette méthode est celle qu'on utilise dans main.py car nos
                                        # documents sont stockés sous forme de dictionnaires après
                                        # la récupération depuis les APIs.
    
    
        # On appelle create_document() en extrayant les valeurs du dictionnaire
        return DocumentFactory.create_document(
            doc_type=doc_dict['origine'],           # Type : 'reddit' ou 'arxiv'
            titre=doc_dict['titre'],                # Titre du document
            auteur=doc_dict['auteur'],              # Nom de l'auteur
            date=doc_dict['date'],                  # Date de publication
            url=doc_dict['url'],                    # URL source
            texte=doc_dict['texte'],                # Contenu textuel
            nb_commentaires=doc_dict.get('nb_commentaires', 0),  # Pour Reddit
            co_auteurs=doc_dict.get('co_auteurs', [])            # Pour Arxiv
        )



"""
COMPARAISON : AVEC ET SANS FACTORY

                                 SANS FACTORY 

Dans main.py, il faudrait faire :

    for doc_dict in docs:
        if doc_dict['origine'] == 'reddit':
            doc = RedditDocument(
                titre=doc_dict['titre'],
                auteur=doc_dict['auteur'],
                date=doc_dict['date'],
                url=doc_dict['url'],
                texte=doc_dict['texte'],
                nb_commentaires=doc_dict.get('nb_commentaires', 0)
            )
        elif doc_dict['origine'] == 'arxiv':
            doc = ArxivDocument(
                titre=doc_dict['titre'],
                auteur=doc_dict['auteur'],
                date=doc_dict['date'],
                url=doc_dict['url'],
                texte=doc_dict['texte'],
                co_auteurs=doc_dict.get('co_auteurs', [])
            )
        
        corpus.add_document(doc)

 Problèmes :
    - Code répétitif et verbeux
    - Logique de création dispersée dans le code
    - Difficile à maintenir (si on ajoute un type, il faut modifier partout)

╔════════════════════════════════════════════════════════════════════════╗
║                          AVEC FACTORY                                  ║
╚════════════════════════════════════════════════════════════════════════╝

Dans main.py, on fait simplement :

    for doc_dict in docs:
        doc = DocumentFactory.create_from_dict(doc_dict)
        corpus.add_document(doc)

 Avantages :
    - Code concis et lisible
    - Logique centralisée dans la Factory
    - Facile à maintenir (on modifie seulement la Factory)
    - Respect du principe de responsabilité unique


EXTENSIBILITÉ : AJOUTER UN NOUVEAU TYPE

Si demain on veut ajouter un nouveau type de document (par exemple YouTube),
il suffit de :

1. Créer la classe fille :
    class YoutubeDocument(Document):
        def __init__(self, titre, auteur, date, url, texte, nb_vues):
            super().__init__(titre, auteur, date, url, texte, "youtube")
            self.nb_vues = nb_vues

2. Modifier la Factory (un seul endroit !) :
    def create_document(doc_type, ...):
        if doc_type.lower() == 'reddit':
            ...
        elif doc_type.lower() == 'arxiv':
            ...
        elif doc_type.lower() == 'youtube':  #  NOUVEAU
            nb_vues = kwargs.get('nb_vues', 0)
            return YoutubeDocument(titre, auteur, date, url, texte, nb_vues)

3. C'est tout ! Le reste du code (main.py, Corpus, etc.) n'a pas besoin
   d'être modifié. C'est le pouvoir du pattern Factory !


PRINCIPE SOLID : OPEN/CLOSED

    - Open (Ouvert) : On peut étendre les fonctionnalités (ajouter des types)
    - Closed (Fermé) : Sans modifier le code existant (main.py reste intact)

La Factory respecte ce principe car on peut ajouter de nouveaux types de
documents sans toucher au code qui utilise la Factory.
"""

