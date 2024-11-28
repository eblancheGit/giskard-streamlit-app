import streamlit as st
import giskard
from giskard import Model, Dataset
from giskard.scanner import scan
import pandas as pd
import json

# Configuration du style personnalisé
st.set_page_config(
    page_title="Giskard Scanner App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé inspiré de Dinootoo
st.markdown("""
    <style>
    /* Couleurs principales */
    :root {
        --primary-color: #FF6B00;
        --secondary-color: #2D2D2D;
        --background-color: #FFFFFF;
        --text-color: #1E1E1E;
    }
    
    /* Header */
    .stApp > header {
        background-color: var(--secondary-color);
        color: white;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: var(--background-color);
    }
    
    /* Boutons */
    .stButton>button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    /* Cards */
    .element-container {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    
    /* Titres */
    h1, h2, h3 {
        color: var(--secondary-color);
        font-weight: 600;
    }
    
    /* Menu de navigation */
    .stSelectbox label {
        color: var(--text-color);
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Header personnalisé
st.markdown("""
    <div style="display: flex; align-items: center; background-color: #2D2D2D; padding: 1rem; margin-bottom: 2rem;">
        <img src="https://your-logo-url.com" style="height: 40px; margin-right: 1rem;"/>
        <h1 style="color: white; margin: 0;">Giskard Scanner App</h1>
    </div>
""", unsafe_allow_html=True)

# Navigation principale
tabs = st.tabs(["📊 Scanner", "⚙️ Configurations", "📚 Bibliothèque de tests"])

with tabs[0]:
    # Zone principale divisée en colonnes
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
            <div class="card">
                <h3>📤 Chargement des données</h3>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Charger un dataset (CSV)",
            type=['csv'],
            help="Format accepté : CSV"
        )

        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                with st.expander("Aperçu des données"):
                    st.dataframe(df.head(), use_container_width=True)
                
                if len(df.columns) > 0:
                    target_column = st.selectbox(
                        "Colonne cible",
                        df.columns,
                        help="Sélectionnez la colonne à analyser"
                    )
            except Exception as e:
                st.error(f"Erreur de chargement : {str(e)}")

    with col2:
        st.markdown("""
            <div class="card">
                <h3>⚙️ Configuration du scan</h3>
            </div>
        """, unsafe_allow_html=True)
        
        scan_type = st.selectbox(
            "Type de modèle",
            ["LLM", "Tabular", "NLP", "Vision"],
            help="Sélectionnez le type de modèle à scanner"
        )

        if uploaded_file:
            if st.button("🚀 Lancer le scan", key="scan_button"):
                with st.spinner('Scan en cours...'):
                    try:
                        dataset = Dataset(df, target=target_column)
                        results = scan(None, dataset)
                        
                        # Affichage des résultats dans un conteneur stylisé
                        st.markdown("""
                            <div class="results-card">
                                <h3>📊 Résultats du scan</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        if isinstance(results, dict):
                            st.json(results)
                        else:
                            st.write(results)
                            
                    except Exception as e:
                        st.error(f"Erreur : {str(e)}")

# Sidebar avec informations complémentaires
with st.sidebar:
    st.markdown("""
        <div style="background-color: white; padding: 1rem; border-radius: 8px;">
            <h4>ℹ️ Information</h4>
            <p>Giskard version: {}</p>
        </div>
    """.format(giskard.__version__), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Powered by Giskard - <a href="https://docs.giskard.ai/">Documentation</a></p>
    </div>
""", unsafe_allow_html=True)
