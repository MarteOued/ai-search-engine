# -*- coding: utf-8 -*-
"""
Corpus.py

Ce fichier contient la classe Corpus qui gère l'ensemble de la collection
de documents et d'auteurs du proje et Implémente le pattern Singleton : une seule instance possible.

"""
                       # IMPORTATION DES LIBRAIRIES

import pandas as pd                            # pour manipuler les tableaux de données
from datetime import datetime                  # pour gérer les dates

                      # CLASSE CORPUS (SINGLETON)      Par Julien

class Corpus:                 
                         
    _instance = None            # variable de classe pour stocker l'instance unique (Singleton)
    
  # TD5 - PATTERN SINGLETON : Contrôle de la création d'instance
   
    def __new__(cls, nom="Corpus"):
        
        if cls._instance is None:
            # première création : on crée une nouvelle instance
            print(f"[Singleton] Création de l'instance unique du Corpus")
            cls._instance = super().__new__(cls)
            # on ajoute un flag pour savoir si l'initialisation a été faite
            cls._instance._initialized = False
        else:
            # instance déjà existante : on la réutilise
            print(f" Instance du Corpus déjà existante, réutilisation")
        
        return cls._instance
    
   # CONSTRUCTEUR
   
    def __init__(self, nom="Corpus"):
        
        # on vérifie si l'initialisation a déjà été faite
        if not self._initialized:
            # première initialisation
            self.nom = nom
            self.authors = {}  # dictionnaire des auteurs {nom: Author}
            self.id2doc = {}   # dictionnaire des documents {id: Document}
            self.ndoc = 0      # compteur de documents
            self.naut = 0      # compteur d'auteurs
            self._initialized = True
            self.vocabulaire = {} # dictionnaire mot -> identifiant (int)
            self.matrice_tfidf = None # La matrice finale
            print(f" Corpus '{self.nom}' initialisé")
    
   # MÉTHODE PRINCIPALE : AJOUT D'UN DOCUMENT            Par Martine
    
    def add_document(self, document):        # on ajoute un document au corpus
        
        # on gener un ID unique pour le document
        doc_id = self.ndoc
        
        # on ajoute le document au dictionnaire id2doc
        self.id2doc[doc_id] = document
        self.ndoc += 1
        
        # on gere l'auteur
        auteur_nom = document.auteur
        
        # si l'auteur n'existe pas encore, on le crée
        if auteur_nom not in self.authors:
            from Author import Author
            self.authors[auteur_nom] = Author(auteur_nom)
            self.naut += 1
        
        # on ajoute le document à la production de l'auteur
        self.authors[auteur_nom].add(doc_id, document)
    
    # MÉTHODES D'AFFICHAGE
    
    def __repr__(self):           
        
        return f"Corpus '{self.nom}': {self.ndoc} documents, {self.naut} auteurs"
    
    def show(self, n=10):

        print(f"Corpus: {self.nom}")
        print(f"Nombre de documents: {self.ndoc}")
        print(f"Nombre d'auteurs: {self.naut}")
        
        
        print(f"\n Affichage des {min(n, self.ndoc)} premiers documents:\n")
        
        # on parcourt le dictionnaire et on compte jusqu'à n
        compteur = 0
        for doc_id, doc in self.id2doc.items():
            if compteur >= n:
                break
            print(f"{compteur+1}. {doc}")  # utilise la méthode __str__ du document
            compteur += 1
    
    # MÉTHODES DE Trie et affiche les documents par date de publication.    Par Julien
   
    def trier_par_date(self, n=10, ordre_croissant=True):
       
        # on crée une liste de tuples (doc_id, document)
        docs_liste = list(self.id2doc.items())
        
        # Trie par date
        # reverse=not ordre_croissant : si ordre_croissant=False, reverse=True
        docs_tries = sorted(docs_liste, 
                           key=lambda x: x[1].date, 
                           reverse=not ordre_croissant)
        
        # affichage des résultats
        print(f"Documents triés par date ({'croissant' if ordre_croissant else 'décroissant'}):")
       
        
        for i, (doc_id, doc) in enumerate(docs_tries[:n]):
            # strftime('%Y-%m-%d') : formatte la date en YYYY-MM-DD
            print(f"{i+1}. [{doc.date.strftime('%Y-%m-%d')}] {doc.titre} ({doc.type})")
    
    def trier_par_titre(self, n=10):
       
        # on crée une liste de tuples (doc_id, document)
        docs_liste = list(self.id2doc.items())
        
        # trie par titre (en minuscules pour ignorer la casse)
        docs_tries = sorted(docs_liste, key=lambda x: x[1].titre.lower())
        
        # affichage des résultats
        print(f"Documents triés par titre (alphabétique):")
        
        
        for i, (doc_id, doc) in enumerate(docs_tries[:n]):
            print(f"{i+1}. {doc.titre} ({doc.type})")
    
  # MÉTHODES DE SAUVEGARDE ET CHARGEMENT          Par Martine
    
    def save(self, nom_fichier):
        
        # on crée une liste de dictionnaires
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
        
        # Et ensuite on crée un DataFrame pandas
        df = pd.DataFrame(data)
        
        # En fin on sauvegarder en CSV
        # sep='\t' : séparateur = tabulation
        # index=False : ne pas sauvegarder l'index de pandas
        df.to_csv(nom_fichier, sep='\t', index=False)
        print(f" Corpus sauvegardé dans '{nom_fichier}'")
    
    @staticmethod
    def load(nom_fichier):
        from DocumentFactory import DocumentFactory
    
        # chargement du CSV
        df = pd.read_csv(nom_fichier, sep='\t')
    
        # on réer un nouveau corpus vide
        corpus = Corpus("Corpus chargé")
        corpus.id2doc.clear()
        corpus.authors.clear()
        corpus.ndoc = 0
        corpus.naut = 0
    
        # on parcourt les lignes et recréer les bons objets
        for _, row in df.iterrows():
            date = pd.to_datetime(row['date'])
            doc = DocumentFactory.create_document(
                doc_type=row['type'],   # "reddit" ou "arxiv"
                titre=row['titre'],
                auteur=row['auteur'],
                date=date,
                url=row['url'],
                texte=row['texte']
            )
            corpus.add_document(doc)
    
        print(f" Corpus chargé depuis '{nom_fichier}'")
        return corpus


    # TD6 - PARTIE 1 : EXPRESSIONS RÉGULIÈRES   Par Julien
    
    """
    On construit une chaîne unique contenant tous les textes du corpus.
    Cette méthode est appelée automatiquement la première fois qu'on
    fait une recherche, puis le résultat est stocké en cache.
    """
    
    def build_full_text(self):
        
        if not hasattr(self, '_full_text') or self._full_text is None:
            print("Construction de la chaîne complète (première fois)...")
            # on joint tous les textes avec un espace
            textes = [doc.texte for doc in self.id2doc.values()]
            self._full_text = ' '.join(textes)
            print(f" Chaîne construite : {len(self._full_text)} caractères")
        return self._full_text
    
    def search(self, mot_cle):
        import re
        
        # on construit la chaîne complète (une seule fois)
        full_text = self.build_full_text()
        
        # on crée le pattern de recherche (insensible à la casse)
        # \b = frontière de mot
        pattern = re.compile(r'\b' + re.escape(mot_cle) + r'\b', re.IGNORECASE)
        
        # on trouve toutes les occurrences
        resultats = pattern.finditer(full_text)
        
        # on extrait les passages (avec un peu de contexte)
        passages = []
        taille_contexte = 50  # 50 caractères avant et après
        
        for match in resultats:
            debut = max(0, match.start() - taille_contexte)
            fin = min(len(full_text), match.end() + taille_contexte)
            passage = full_text[debut:fin]
            passages.append(passage)
        
        print(f"'{mot_cle}' trouvé {len(passages)} fois")
        return passages
    
        """
        On construit un concordancier pour une expression donnée.
        Un concordancier affiche le mot recherché avec son contexte
        gauche et droit dans un tableau structuré.
        
        """
    def concorde(self, expression, taille_contexte=30):
        
        import re
        import pandas as pd
        
        # on construit la chaîne complète
        full_text = self.build_full_text()
        
        # pattern de recherche (insensible à la casse)
        pattern = re.compile(r'\b' + re.escape(expression) + r'\b', re.IGNORECASE)
        
        # on trouve toutes les occurrences
        resultats = pattern.finditer(full_text)
        
        # on construit le concordancier
        data = []
        for match in resultats:
            # contexte gauche
            debut_gauche = max(0, match.start() - taille_contexte)
            contexte_gauche = full_text[debut_gauche:match.start()]
            
            # motif trouvé (le mot lui-même)
            motif = match.group()
            
            # contexte droit
            fin_droit = min(len(full_text), match.end() + taille_contexte)
            contexte_droit = full_text[match.end():fin_droit]
            
            # On ajoute à la liste
            data.append({
                'contexte_gauche': contexte_gauche.strip(),
                'motif_trouve': motif,
                'contexte_droit': contexte_droit.strip()
            })
        
        # on crée le DataFrame
        concordancier = pd.DataFrame(data)
        
        print(f"Concorde '{expression}' trouvé {len(data)} fois")
        return concordancier
    
   # TD6 - PARTIE 2 : STATISTIQUES TEXTUELLES  Par Martine
    
    
    @staticmethod
    def nettoyer_texte(texte):            # on nettoie et normalise un texte pour l'analyse.
        import re
        
        # on met en minuscules
        texte = texte.lower()
        
        # on remplace les sauts de ligne
        texte = texte.replace('\n', ' ')
        texte = texte.replace('\r', ' ')
        
        # on supprime la ponctuation (on garde les espaces)
        texte = re.sub(r'[^\w\s]', ' ', texte)
        
        # on supprime les chiffres
        texte = re.sub(r'\d+', ' ', texte)
        
        # on supprime les espaces multiples
        texte = re.sub(r'\s+', ' ', texte)
        
        # on supprime les espaces en début/fin
        texte = texte.strip()
        
        return texte
    
    def stats(self, n=10):
        import pandas as pd
        from collections import Counter
        
        print("           STATISTIQUES TEXTUELLES DU CORPUS")
        
        
        # dictionnaire pour compter les occurrences totales
        term_frequency = Counter()
        
        # dictionnaire pour compter dans combien de documents chaque mot apparaît
        document_frequency = Counter()
        
        # on parcourt tous les documents une seule fois 
        for doc_id, doc in self.id2doc.items():
            # on nettoie le texte
            texte_propre = self.nettoyer_texte(doc.texte)
            # Stop words anglais courants
            stop_words = {'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'for', 
                          'it', 'as', 'on', 'with', 'be', 'this', 'are', 'by', 'at', 
                          'an', 'or', 'from', 'can', 'has', 'have', 'will', 'would'}

            # on sépare en mots
            mots = texte_propre.split()
            
            # filtrer les stop words
            mots = [mot for mot in mots if mot not in stop_words and len(mot) > 2]

            
            # on compte les occurrences totales
            term_frequency.update(mots)
            
            # on compte la présence dans ce document (un mot = une fois par doc max)
            mots_uniques = set(mots)  # on élimine les doublons dans ce document
            document_frequency.update(mots_uniques)
        
        # on crée le DataFrame et on trie par occurrences
        data = []
        for mot, tf in term_frequency.items():
            df = document_frequency[mot]
            data.append({
                'mot': mot,
                'occurrences': tf,
                'documents': df
            })
        
        freq_table = pd.DataFrame(data)
        freq_table = freq_table.sort_values('occurrences', ascending=False)
        freq_table = freq_table.reset_index(drop=True)
        
        # on affiche les statistiques
        print(f"\n Nombre de mots différents : {len(freq_table)}")
        print(f"\n Top {n} des mots les plus fréquents :")
        print(freq_table.head(n).to_string(index=False))
        
        print("\n" + "="*70)
        
        return freq_table
