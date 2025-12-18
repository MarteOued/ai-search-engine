import math
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix


class SearchEngine:
    def __init__(self, corpus):
        """
        Initialise le moteur de recherche avec un objet Corpus.
        Construit automatiquement :
        - le vocabulaire enrichi
        - la matrice TF (mat_TF)
        - la matrice TF-IDF (mat_TFxIDF)
        """
        self.corpus = corpus
        self.vocab = {}             # le dictionnaire
        self.mat_TF = None          # matrice TF
        self.mat_TFxIDF = None      # matrice TF×IDF

        self._construire_matrices()

    # CONSTRUCTION DU VOCAB + MATRICES
    def _construire_matrices(self):
        print("[SearchEngine] Construction du vocabulaire et des matrices...")

        # Récupération de l'integralité des mots du corpus
        mots_uniques = set()
        docs_list = list(self.corpus.id2doc.values())

        for doc in docs_list:
            texte = self.corpus.nettoyer_texte(doc.texte)
            mots_uniques.update(texte.split())

        # Création du vocabulaire trié
        for idx, mot in enumerate(sorted(mots_uniques)):
            self.vocab[mot] = {
                "id": idx,
                "nb_occ": 0,      # nombre d'occurrence totale
                "nb_docs": 0      # nombre de documents contenant ce mot
            }

        n_docs = len(docs_list)
        n_mots = len(self.vocab)

        # Listes pour remplir la matrice TF
        rows, cols, data = [], [], []

        # Compteur temporaire : savoir si un doc contient un mot au moins une fois
        doc_contains = {mot: 0 for mot in self.vocab}

        # Construction de mat_TF
        for doc_idx, doc in enumerate(docs_list):
            texte = self.corpus.nettoyer_texte(doc.texte)
            mots = texte.split()

            # Comptage TF local au document
            tf_local = {}
            for mot in mots:
                if mot in self.vocab:
                    tf_local[mot] = tf_local.get(mot, 0) + 1

            # Alimentation de la matrice
            for mot, count in tf_local.items():
                mot_id = self.vocab[mot]["id"]

                rows.append(doc_idx)
                cols.append(mot_id)
                data.append(count)

                # Mise à jour du vocab
                self.vocab[mot]["nb_occ"] += count
                self.vocab[mot]["nb_docs"] += 1

        # Construction sparse matrix TF
        self.mat_TF = csr_matrix((data, (rows, cols)), shape=(n_docs, n_mots))


        # 2) CONSTRUCTION MATRICE TF-IDF
        idf = np.zeros(n_mots)
        for mot, info in self.vocab.items():
            df = info["nb_docs"]
            mot_id = info["id"]
            idf[mot_id] = math.log(n_docs / df) if df > 0 else 0

        # Calcul TF×IDF
        data_tfidf = [data[i] * idf[cols[i]] for i in range(len(data))]
        self.mat_TFxIDF = csr_matrix((data_tfidf, (rows, cols)), shape=(n_docs, n_mots))

        print("[SearchEngine] Matrices TF et TF-IDF prêtes !")

     
    # 3) MOTEUR DE RECHERCHE AVEC COSINUS
    def search(self, query, n_results=5):
        """
        Recherche en utilisant la similarité cosinus.
        Retourne un DataFrame pandas.
        """
        # Nettoyage et vectorisation de la requête
        mots_requete = self.corpus.nettoyer_texte(query).split()
        vec_requete = np.zeros(len(self.vocab))

        for mot in mots_requete:
            if mot in self.vocab:
                vec_requete[self.vocab[mot]["id"]] += 1

        # Normalisation de la requête pour cosinus
        norme_requete = np.linalg.norm(vec_requete)
        if norme_requete > 0:
            vec_requete = vec_requete / norme_requete

        # Normalisation des vecteurs documents TF-IDF
        mat_norm = self.mat_TFxIDF.copy()

        # Calcul norme document par ligne
        norms = np.sqrt(mat_norm.multiply(mat_norm).sum(axis=1))
        norms = np.array(norms).flatten()

        # Division ligne par ligne
        for i in range(mat_norm.shape[0]):
            if norms[i] > 0:
                mat_norm.data[mat_norm.indptr[i]:mat_norm.indptr[i+1]] /= norms[i]

        # Produit scalaire _ similarité cosinus
        scores = mat_norm.dot(vec_requete)

        # Tri décroissant
        indices = np.argsort(scores)[::-1]

        # Préparation DataFrame
        results = []
        docs_list = list(self.corpus.id2doc.values())

        for i in range(min(n_results, len(docs_list))):
            idx = indices[i]
            score = scores[idx]

            if score > 0:
                doc = docs_list[idx]
                results.append({
                    "Titre": doc.titre,
                    "Auteur": doc.auteur,
                    "Date": doc.date,
                    "Source": doc.get_type(),
                    "Score": float(score)
                })

        return pd.DataFrame(results)
