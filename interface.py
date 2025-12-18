import streamlit as st
import pandas as pd
import plotly.express as px  
from datetime import datetime

# Importation de nos classes
from Corpus import Corpus
from SearchEngine import SearchEngine

# CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Moteur de recherche sur corpus",
    page_icon="🤖",
    layout="wide"
)

# --- FONCTION DE CHARGEMENT (CACHE) ---
# Cette fonction ne s'exécute qu'une seule fois au démarrage afin d'éviter de recharger le CSV et recalculer la matrice à chaque action de l'utilisateur
@st.cache_resource
def load_resources():
    try:
        # On essaie de charger le corpus existant (généré par main.py)
        corpus = Corpus.load("corpus_v1.csv")
        
        # On initialise le moteur (construit la matrice TF-IDF)
        engine = SearchEngine(corpus)
        return corpus, engine
    except FileNotFoundError:
        return None, None
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return None, None

# CHARGEMENT DES DONNÉES
with st.spinner('Démarrage du moteur et indexation des documents...'):
    corpus, engine = load_resources()

#  INTERFACE 

st.title("Moteur de Recherche sur le sujet de l'Intelligence Artificielle")
st.markdown("Exploration des discussions **Reddit** et articles **Arxiv** via un modèle vectoriel TF-IDF.")

# Nous verifions si le corpus a été chargé(trouvé)
if corpus is None:
    st.warning("⚠️ Le fichier 'corpus_v1.csv' est introuvable.")
    st.info("Veuillez d'abord exécuter 'main.py' pour récupérer les données et créer le corpus.")
    st.stop() # On arrête l'exécution ici

# Barre latérale
with st.sidebar:
    st.header("📊 Statistiques Corpus")
    st.metric("Documents", corpus.ndoc)
    st.metric("Auteurs", corpus.naut)
    
    st.divider()
    st.write("Filtres de recherche")
    # Filtrage des Sources
    source_filter = st.selectbox("Source", ["Toutes", "Reddit", "Arxiv"])
    
    # Filtre Date (Calcul des min/max du corpus pour le slider)
    all_dates = [doc.date for doc in corpus.id2doc.values() if isinstance(doc.date, datetime)]
    if all_dates:
        min_date, max_date = min(all_dates).date(), max(all_dates).date()
        date_range = st.slider(
            "Période",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date)
        )
    else:
        date_range = None

# ONGLETS PRINCIPAUX
tab1, tab2 = st.tabs(["🔍 Recherche", "📈 Visualisation des Données"])

# ONGLET 1 : RECHERCHE 
with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        query = st.text_input("Mots-clés", placeholder="Ex: artificial intelligence jobs")
    with col2:
        st.write("") # Espacement
        st.write("") 
        search_btn = st.button("Rechercher ", use_container_width=True)

    if query:
        st.markdown("### Analyse de la requête")
        
        # On nettoie la requête comme le moteur le fait (pour correspondre au vocabulaire)
        # Note : On accède à la méthode statique via l'objet corpus
        mots_requete = corpus.nettoyer_texte(query).split()
        
        cols_vocab = st.columns(len(mots_requete))
        
        found_words = False
        
        for i, mot in enumerate(mots_requete):
            # On vérifie si le mot est dans notre vocabulaire enrichi
            if mot in engine.vocab:
                found_words = True
                infos = engine.vocab[mot]
                with cols_vocab[i % len(cols_vocab)]: # Gestion des colonnes si trop de mots
                    st.metric(
                        label=f"Mot : '{mot}'",
                        value=f"Present dans {infos['nb_docs']} doc(s)",
                        delta=f"{infos['nb_occ']} occurences"
                    )
            else:
                with cols_vocab[i % len(cols_vocab)]:
                    st.metric(
                        label=f"Mot : '{mot}'",
                        value="Inconnu",
                        delta="0",
                        delta_color="off"
                    )
        
        st.divider()
        # 1. Interrogation du moteur (on demande 50 résultats pour pouvoir filtrer après)
        df_results = engine.search(query, n_results=50)
        
        if not df_results.empty:
            # 2. Application des filtres
            # Filtre Source
            if source_filter != "Toutes":
                df_results = df_results[df_results['Source'].str.lower() == source_filter.lower()]
            
            # Filtre Date
            if date_range:
                # Conversion pour comparaison
                start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
                # On s'assure que la colonne Date est bien au format datetime
                df_results['Date'] = pd.to_datetime(df_results['Date'])
                df_results = df_results[
                    (df_results['Date'].dt.date >= date_range[0]) & 
                    (df_results['Date'].dt.date <= date_range[1])
                ]

            # 3. Affichage des résultats
            st.success(f"{len(df_results)} document(s) contenant le mot '{mot}' trouvés")
            
            for index, row in df_results.head(10).iterrows(): # On affiche le top 10 filtré
                with st.expander(f"{row['Score']:.2f} - {row['Titre']}"):
                    st.markdown(f"**Source :** {row['Source']} | **Date :** {row['Date'].strftime('%Y-%m-%d')}")
                    st.markdown(f"**Auteur :** {row['Auteur']}")            
        else:
            st.info("Aucun résultat trouvé pour cette requête.")

# ONGLET 2 : data visualisation
with tab2:
    st.subheader("Analyse du Corpus")
    
    # 1. Chargement des statistiques textuelles (TD6)
    try:
        # On lit le fichier généré par le TD6 (séparateur tabulation \t)
        df_freq = pd.read_csv("frequences.csv", sep='\t')
        has_freq = True
    except FileNotFoundError:
        st.warning("Fichier 'frequences.csv' introuvable. Lancez main.py pour le générer.")
        has_freq = False
    
    # 2. Préparation des métadonnées (Corpus)
    data_viz = []
    for doc in corpus.id2doc.values():
        data_viz.append({
            "Date": doc.date,
            "Source": doc.get_type(),
            "Auteur": doc.auteur,
            "Titre": doc.titre
        })
    df_viz = pd.DataFrame(data_viz)
    
    # PREMIÈRE LIGNE : Indicateurs Clés
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Nombre de Documents", corpus.ndoc)
    col_kpi1.metric("Nombre d'Auteurs", corpus.naut)
    
    if has_freq:
        # On affiche la taille du vocabulaire (nombre de lignes du fichier freq)
        col_kpi2.metric("Taille du Vocabulaire", f"{len(df_freq)} mots")
        # On affiche le mot le plus fréquent (1ère ligne)
        top_word = df_freq.iloc[0]['mot']
        top_count = df_freq.iloc[0]['occurrences']
        col_kpi2.metric("Mot le plus fréquent", f"'{top_word}'", f"{top_count} fois")

    st.divider()

    # DEUXIÈME LIGNE : Graphiques Texte
    if has_freq:
        st.write("### 🔤 Analyse Lexicale (Top 20 mots)")
        # On prend les 20 premiers mots
        top_20 = df_freq.head(20).sort_values(by='occurrences', ascending=True) # Tri inversé pour l'affichage horizontal
        
        fig_words = px.bar(
            top_20, 
            x='occurrences', 
            y='mot', 
            orientation='h',
            title="Mots les plus fréquents dans le corpus (Stop-words exclus)",
            labels={'occurrences': "Nombre d'apparitions", 'mot': "Terme"},
            color='occurrences',
            color_continuous_scale='Bluyl' 
        )
        st.plotly_chart(fig_words, use_container_width=True)

    # TROISIÈME LIGNE : Graphiques Temporels et Sources
    col_viz1, col_viz2 = st.columns(2)
    
    with col_viz1:
        st.write("### Évolution temporelle")
        if not df_viz.empty:
            df_viz['Mois'] = pd.to_datetime(df_viz['Date']).dt.to_period('M').astype(str)
            counts_per_month = df_viz.groupby(['Mois', 'Source']).size().reset_index(name='Nombre')
            
            fig_time = px.bar(counts_per_month, x='Mois', y='Nombre', color='Source', 
                              title="Publication des articles par mois", barmode='group')
            st.plotly_chart(fig_time, use_container_width=True)

    with col_viz2:
        st.write("### Répartition des sources")
        if not df_viz.empty:
            counts_source = df_viz['Source'].value_counts().reset_index()
            counts_source.columns = ['Source', 'Compte']
            
            fig_pie = px.pie(counts_source, values='Compte', names='Source', 
                             title="Distribution Reddit vs Arxiv", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)