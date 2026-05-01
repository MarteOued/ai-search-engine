"""
AI Search Engine — Interface Streamlit
Author: Martine Ouedraogo
Description: Professional UI for a TF-IDF search engine over Reddit & Arxiv corpora about AI.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from Corpus import Corpus
from SearchEngine import SearchEngine

# =====================================================================
# PAGE CONFIG
# =====================================================================
st.set_page_config(
    page_title="AI Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================================
# CUSTOM CSS — Clean professional light/dark hybrid theme
# =====================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Background ── */
    .stApp {
        background-color: #F8FAFC;
    }

    /* ── Main content padding ── */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }

    /* ── Header banner ── */
    .header-banner {
        background: linear-gradient(135deg, #1E3A5F 0%, #2563EB 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .header-banner h1 {
        color: #FFFFFF !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin: 0 0 0.4rem 0 !important;
        letter-spacing: -0.01em;
    }
    .header-banner p {
        color: #BFDBFE !important;
        font-size: 1rem !important;
        margin: 0 !important;
        font-weight: 400;
        line-height: 1.6;
    }
    .header-tag {
        display: inline-block;
        background: rgba(255,255,255,0.15);
        color: #FFFFFF;
        padding: 0.2rem 0.75rem;
        border-radius: 20px;
        margin: 0.6rem 0.3rem 0 0;
        font-size: 0.78rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.25);
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    [data-testid="stSidebar"] h2 {
        color: #93C5FD !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        color: #CBD5E1 !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #334155 !important;
    }

    /* ── Metric cards ── */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1E40AF !important;
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #16A34A !important;
        font-size: 0.8rem !important;
    }

    /* ── Text input ── */
    .stTextInput > div > div > input {
        background: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        color: #1E293B !important;
        font-size: 1rem !important;
        padding: 0.65rem 1rem !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #94A3B8 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 0.6rem 1.4rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: background 0.2s ease;
    }
    .stButton > button:hover {
        background: #1D4ED8 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #EFF6FF;
        padding: 4px;
        border-radius: 10px;
        border: 1px solid #DBEAFE;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: #475569 !important;
        border-radius: 7px !important;
        padding: 0.45rem 1.2rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* ── Section titles ── */
    h2, h3 {
        color: #1E293B !important;
        font-weight: 700;
    }

    /* ── Result card ── */
    .result-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.85rem;
        transition: box-shadow 0.2s ease;
    }
    .result-card:hover {
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.1);
    }
    .result-rank {
        font-size: 0.75rem;
        font-weight: 700;
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .result-title {
        color: #1E293B !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.4rem;
        line-height: 1.4;
    }
    .result-meta {
        color: #64748B !important;
        font-size: 0.83rem !important;
    }
    .score-pill {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        padding: 0.2rem 0.65rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        margin-right: 0.4rem;
    }
    .badge-reddit {
        display: inline-block;
        background: #FFF7ED;
        color: #C2410C;
        border: 1px solid #FED7AA;
        padding: 0.2rem 0.65rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.78rem;
    }
    .badge-arxiv {
        display: inline-block;
        background: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
        padding: 0.2rem 0.65rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.78rem;
    }

    /* ── Divider ── */
    hr {
        border-color: #E2E8F0 !important;
    }

    /* ── Info / warning boxes ── */
    .stAlert {
        border-radius: 8px !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #1E293B !important;
        background: #F8FAFC !important;
        border-radius: 8px !important;
    }

    /* ── Hide default footer and menu ── */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# DATA LOADING
# =====================================================================
@st.cache_resource
def load_resources():
    try:
        corpus = Corpus.load("corpus_v1.csv")
        engine = SearchEngine(corpus)
        return corpus, engine
    except FileNotFoundError:
        return None, None
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return None, None

with st.spinner("Chargement du corpus..."):
    corpus, engine = load_resources()

# =====================================================================
# HEADER
# =====================================================================
st.markdown("""
<div class="header-banner">
    <h1>🔍 AI Search Engine</h1>
    <p>Moteur de recherche vectoriel <strong>TF-IDF</strong> construit from scratch — corpus Reddit & Arxiv sur l'Intelligence Artificielle.</p>
    <div>
        <span class="header-tag">Python</span>
        <span class="header-tag">TF-IDF</span>
        <span class="header-tag">Similarité cosinus</span>
        <span class="header-tag">Streamlit</span>
        <span class="header-tag">Plotly</span>
    </div>
</div>
""", unsafe_allow_html=True)

if corpus is None:
    st.warning("Le fichier `corpus_v1.csv` est introuvable. Exécutez `python main.py` pour générer le corpus.")
    st.stop()

# =====================================================================
# SIDEBAR
# =====================================================================
with st.sidebar:
    st.markdown("## Statistiques")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Documents", f"{corpus.ndoc:,}", delta="indexés")
    with col_b:
        st.metric("Auteurs", f"{corpus.naut:,}", delta="uniques")

    if hasattr(engine, "vocab"):
        st.metric("Vocabulaire", f"{len(engine.vocab):,}", delta="termes")

    st.divider()

    st.markdown("## Filtres")

    source_filter = st.selectbox(
        "Source",
        ["Toutes", "Reddit", "Arxiv"],
        help="Filtrer les résultats par source"
    )

    all_dates = [doc.date for doc in corpus.id2doc.values() if isinstance(doc.date, datetime)]
    if all_dates:
        min_date, max_date = min(all_dates).date(), max(all_dates).date()
        date_range = st.slider(
            "Période",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
        )
    else:
        date_range = None

    n_results = st.slider("Nombre de résultats", 5, 50, 10)

    st.divider()

    with st.expander("À propos", expanded=False):
        st.markdown("""
        Moteur TF-IDF implémenté **from scratch** avec similarité cosinus.

        - **Données** : Reddit + Arxiv
        - **Stack** : Python · Pandas · Streamlit · Plotly
        - **Auteur** : [Martine Ouedraogo](https://www.linkedin.com/in/marte-oued)
        """)

# =====================================================================
# TABS
# =====================================================================
tab1, tab2, tab3 = st.tabs(["Recherche", "Analytiques", "À propos"])

# ─────────────────────────────────────────────────────────────────────
# TAB 1 — SEARCH
# ─────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Effectuez votre recherche")

    col1, col2 = st.columns([5, 1])
    with col1:
        query = st.text_input(
            "Requête",
            placeholder="Ex : large language models, neural networks, machine learning...",
            label_visibility="collapsed"
        )
    with col2:
        search_btn = st.button("Rechercher", use_container_width=True)

    st.markdown("**Suggestions :**")
    sug_cols = st.columns(5)
    suggestions = ["transformer", "deep learning", "GPT", "neural network", "reinforcement learning"]
    for i, sug in enumerate(suggestions):
        with sug_cols[i]:
            if st.button(sug, key=f"sug_{i}", use_container_width=True):
                query = sug

    if query:
        with st.expander("Analyse de la requête", expanded=True):
            mots_requete = corpus.nettoyer_texte(query).split()
            cols_vocab = st.columns(min(len(mots_requete), 5))
            for i, mot in enumerate(mots_requete):
                with cols_vocab[i % len(cols_vocab)]:
                    if mot in engine.vocab:
                        infos = engine.vocab[mot]
                        st.metric(
                            label=f"`{mot}`",
                            value=f"{infos['nb_docs']} doc(s)",
                            delta=f"{infos['nb_occ']} occ."
                        )
                    else:
                        st.metric(label=f"`{mot}`", value="—", delta="hors vocab", delta_color="off")

        with st.spinner("Recherche en cours..."):
            df_results = engine.search(query, n_results=50)

        if not df_results.empty:
            if source_filter != "Toutes":
                df_results = df_results[df_results['Source'].str.lower() == source_filter.lower()]
            if date_range:
                df_results['Date'] = pd.to_datetime(df_results['Date'])
                df_results = df_results[
                    (df_results['Date'].dt.date >= date_range[0]) &
                    (df_results['Date'].dt.date <= date_range[1])
                ]

            count = len(df_results)
            shown = min(n_results, count)
            st.success(f"{count} résultat(s) trouvé(s) — affichage du top {shown}")

            if count > 1:
                fig = px.bar(
                    df_results.head(n_results),
                    x='Score', y='Titre',
                    orientation='h',
                    color='Score',
                    color_continuous_scale='Blues',
                    title="Scores de pertinence",
                    height=max(320, n_results * 38)
                )
                fig.update_layout(
                    plot_bgcolor='#FFFFFF',
                    paper_bgcolor='#FFFFFF',
                    font_color='#1E293B',
                    font_family='Inter',
                    title_font_size=14,
                    yaxis={'categoryorder': 'total ascending'},
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=40, b=10),
                )
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("### Documents pertinents")
            for rank, (_, row) in enumerate(df_results.head(n_results).iterrows(), start=1):
                source = row.get('Source', '').lower()
                badge = f'<span class="badge-reddit">Reddit</span>' if source == 'reddit' else f'<span class="badge-arxiv">Arxiv</span>'
                date_str = row['Date'].strftime('%d/%m/%Y') if pd.notna(row['Date']) else 'N/A'
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-rank">#{rank}</div>
                    <div class="result-title">{row['Titre']}</div>
                    <div class="result-meta" style="margin-bottom:0.5rem;">
                        {row['Auteur']} &nbsp;·&nbsp; {date_str}
                    </div>
                    <span class="score-pill">Score : {row['Score']:.4f}</span>
                    {badge}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun résultat pour cette requête. Essayez d'autres termes.")

# ─────────────────────────────────────────────────────────────────────
# TAB 2 — ANALYTICS
# ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Vue d'ensemble du corpus")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Documents", f"{corpus.ndoc:,}")
    with kpi2:
        st.metric("Auteurs", f"{corpus.naut:,}")
    with kpi3:
        if hasattr(engine, "vocab"):
            st.metric("Vocabulaire", f"{len(engine.vocab):,}")
    with kpi4:
        if all_dates:
            timespan = (max(all_dates) - min(all_dates)).days
            st.metric("Période couverte", f"{timespan} jours")

    st.divider()

    sources, dates = [], []
    for doc in corpus.id2doc.values():
        src = type(doc).__name__.replace("Document", "") or "Autre"
        sources.append(src)
        if isinstance(doc.date, datetime):
            dates.append(doc.date)

    col_g1, col_g2 = st.columns(2)
    chart_layout = dict(
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font_color='#1E293B',
        font_family='Inter',
        title_font_size=13,
        margin=dict(l=10, r=10, t=40, b=10),
    )

    with col_g1:
        df_sources = pd.DataFrame({'Source': sources})
        fig_src = px.pie(
            df_sources['Source'].value_counts().reset_index(),
            values='count', names='Source',
            title="Répartition par source",
            color_discrete_sequence=['#2563EB', '#F97316', '#10B981'],
            hole=0.4,
        )
        fig_src.update_layout(**chart_layout)
        fig_src.update_traces(textfont_color='#1E293B')
        st.plotly_chart(fig_src, use_container_width=True)

    with col_g2:
        if dates:
            df_dates = pd.DataFrame({'Date': pd.to_datetime(dates)})
            df_dates['Mois'] = df_dates['Date'].dt.to_period('M').astype(str)
            timeline = df_dates.groupby('Mois').size().reset_index(name='Documents')
            fig_time = px.line(
                timeline, x='Mois', y='Documents',
                title="Publications par mois",
                markers=True,
                color_discrete_sequence=['#2563EB'],
            )
            fig_time.update_layout(**chart_layout)
            fig_time.update_traces(line_width=2, marker_size=6)
            st.plotly_chart(fig_time, use_container_width=True)

    if hasattr(engine, "vocab"):
        st.markdown("### Top 20 termes du vocabulaire")
        top_words = sorted(engine.vocab.items(), key=lambda x: x[1].get('nb_occ', 0), reverse=True)[:20]
        df_top = pd.DataFrame([
            {'Terme': w, 'Occurrences': v.get('nb_occ', 0), 'Documents': v.get('nb_docs', 0)}
            for w, v in top_words
        ])
        fig_top = px.bar(
            df_top, x='Occurrences', y='Terme', orientation='h',
            color='Occurrences', color_continuous_scale='Blues',
        )
        fig_top.update_layout(
            **chart_layout,
            yaxis={'categoryorder': 'total ascending'},
            height=560,
            coloraxis_showscale=False,
        )
        fig_top.update_traces(marker_line_width=0)
        st.plotly_chart(fig_top, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────
# TAB 3 — ABOUT
# ─────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### À propos du projet")

    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.markdown("""
        Ce **moteur de recherche d'information** a été développé en Python pour explorer un corpus
        de documents sur l'**Intelligence Artificielle**, collectés depuis :

        - **Reddit** — discussions communautaires (r/ArtificialIntelligence)
        - **Arxiv** — publications scientifiques

        L'objectif est de comprendre en profondeur la **recherche d'information vectorielle**
        en construisant chaque brique sans s'appuyer sur des bibliothèques NLP haut niveau.

        #### Technologies utilisées

        | Composant | Détail |
        |-----------|--------|
        | Langage | Python 3.10+ |
        | Indexation | TF-IDF from scratch |
        | Ranking | Similarité cosinus |
        | Design patterns | Singleton, Factory |
        | Interface | Streamlit |
        | Visualisation | Plotly |

        #### Équipe

        Réalisé dans le cadre du **Master 1 Informatique** à l'**Université Lumière Lyon 2**
        par **Martine Ouedraogo** et **Julien**.
        """)

    with col_t2:
        st.markdown("""
        #### Liens

        - [GitHub](https://github.com/MarteOued/ai-search-engine)
        - [Portfolio](https://portfoliomarte.vercel.app)
        - [LinkedIn](https://www.linkedin.com/in/marte-oued)
        """)

        st.divider()

        st.markdown("""
        #### Chiffres clés

        | | |
        |--|--|
        | Documents | 200+ |
        | Sources | 2 |
        | Modèle | TF-IDF |
        | Architecture | POO |
        """)

# =====================================================================
# FOOTER
# =====================================================================
st.markdown("""
<hr style="margin-top:3rem; border-color:#E2E8F0;">
<div style="text-align:center; padding:1rem 0; color:#94A3B8; font-size:0.82rem;">
    Martine Ouedraogo · Master 1 Informatique · Université Lumière Lyon 2 · 2026
</div>
""", unsafe_allow_html=True)
