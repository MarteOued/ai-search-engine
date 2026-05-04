<h1 align="center">🔍 AI Search Engine</h1>

<p align="center">
  <i>Moteur de recherche d'information vectoriel sur l'Intelligence Artificielle, construit <b>from scratch</b> en Python.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/NLP-TF--IDF-success?style=flat" />
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Viz-Plotly-3F4F75?style=flat&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Data-Reddit%20%2B%20Arxiv-orange?style=flat" />
  <img src="https://img.shields.io/badge/Status-Production-brightgreen?style=flat" />
</p>

<p align="center">
  <a href="https://youtu.be/tBKR8ohQx30">▶️ Voir la démo vidéo</a> ·
  <a href="https://portfoliomarte.vercel.app">🌐 Portfolio</a>
</p>

---

## 🎯 Aperçu

Ce projet est un **moteur de recherche d'information complet** sur le thème de l'Intelligence Artificielle. À partir de documents collectés sur **Reddit** et **Arxiv**, il permet :

- 🔍 La **recherche vectorielle** par mots-clés via un modèle TF-IDF implémenté from scratch
- 📊 L'**exploration analytique** du corpus (distribution temporelle, top termes, sources)
- 🎨 Une **interface web moderne** en Streamlit avec dashboard Plotly

> **Pourquoi ce projet ?** Pour comprendre en profondeur comment fonctionne la recherche d'information moderne (avant l'ère des embeddings), en codant chaque brique sans bibliothèques NLP haut niveau.

## ✨ Fonctionnalités

- 🌐 **Acquisition multi-sources** — APIs Reddit (PRAW) & Arxiv
- 🏗️ **Architecture POO** — patterns Singleton (Corpus) et Factory (Documents)
- 🔡 **Pipeline NLP complet** — tokenisation, nettoyage, vectorisation
- 📐 **Modèle vectoriel TF-IDF** — from scratch avec similarité cosinus
- 🖥️ **Interface web moderne** — design professionnel, dashboard cards, filtres dynamiques
- 📊 **Dashboard analytique** — KPI, distribution sources, timeline, top termes
- 🎛️ **Filtres dynamiques** — par source, par période, par nombre de résultats
- 💾 **Persistance** — sauvegarde / chargement du corpus en CSV

## 🛠️ Stack Technique

| Catégorie | Technologies |
|-----------|--------------|
| **Langage** | Python 3.10+ |
| **NLP** | TF-IDF (from scratch), similarité cosinus |
| **APIs** | PRAW (Reddit), arxiv-py |
| **Interface** | Streamlit |
| **Visualisation** | Plotly Express, Plotly Graph Objects |
| **Data** | Pandas, NumPy |
| **Architecture** | POO (Singleton, Factory) |

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/MarteOued/ai-search-engine.git
cd ai-search-engine
pip install -r requirements.txt
```

### Acquisition des données (à faire 1 fois)

```bash
python main.py
```

Cette étape récupère les documents depuis Reddit & Arxiv, construit le corpus, calcule la matrice TF-IDF et sauvegarde le tout dans `corpus_v1.csv`.

### Lancer l'interface web

```bash
streamlit run interface.py
```

L'application s'ouvre sur `http://localhost:8501`.

## 📂 Structure du projet

```
ai-search-engine/
├── main.py                  # Acquisition des données & génération du corpus
├── interface.py             # Application Streamlit (recherche + analytics)
├── SearchEngine.py          # Moteur TF-IDF + similarité cosinus
├── Corpus.py                # Classe Corpus (Singleton, gestion des docs)
├── Document.py              # Document, RedditDocument, ArxivDocument
├── DocumentFactory.py       # Factory Pattern pour la création d'objets
├── Author.py                # Classe Author
├── corpus_v1.csv            # Corpus persistant (généré)
├── frequences.csv           # Statistiques pour la dataviz
├── requirements.txt         # Dépendances
└── README.md
```

## 🧠 Concepts clés

- **TF-IDF from scratch** — implémentation de Term Frequency × Inverse Document Frequency
- **Similarité cosinus** — mesure de proximité entre vecteur requête et vecteurs documents
- **Design Patterns** — Singleton (Corpus unique), Factory (création polymorphe de Documents)
- **Pipeline NLP** — tokenisation → nettoyage → vectorisation → ranking

## 📈 Évolution du projet

| Version | Période | Contenu |
|---------|---------|---------|
| **v1** | TD 3-5 | Acquisition Reddit & Arxiv, structuration POO, héritage |
| **v2** | TD 6-7 | Analyse textuelle, vectorisation TF-IDF, moteur de recherche |
| **v3** | TD 8-10 | Interface web Streamlit, visualisation Plotly, filtres dynamiques |
| **v4** ✨ | 2026 | Refonte UI complète, dashboard analytique, design moderne |

## 🎬 Démo

▶️ [**Voir la démo vidéo sur YouTube**](https://youtu.be/tBKR8ohQx30)

## 👩‍💻 Auteurs

Projet réalisé en binôme dans le cadre du **Master 1 Informatique** — **Université Lumière Lyon 2**.

- **Martine Ouedraogo** — [LinkedIn](https://www.linkedin.com/in/marte-oued) · [Portfolio](https://portfoliomarte.vercel.app) · [GitHub](https://github.com/MarteOued)


## 📜 Licence

Projet universitaire — Université Lumière Lyon 2.
Réalisé dans le cadre d'un travail académique, non destiné à un usage commercial.