import streamlit as st
import giskard
from giskard import Model, Dataset
from giskard.scanner import scan
import pandas as pd
import json

st.set_page_config(page_title="Giskard Scanner App", layout="wide")

st.title("🔍 Giskard Model Scanner")

# Sidebar pour les configurations
with st.sidebar:
    st.header("Configuration")
    scan_type = st.selectbox(
        "Type de modèle",
        ["LLM", "Tabular", "NLP", "Vision"]
    )

    st.write("### ℹ️ Info")
    st.write(f"Giskard version: {giskard.__version__}")

# Layout principal en deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.write("### 📤 Chargement des données")
    uploaded_file = st.file_uploader("Charger un dataset (CSV)", type=['csv'])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Aperçu des données :")
            st.dataframe(df.head(), use_container_width=True)
            
            # Sélection des colonnes
            if len(df.columns) > 0:
                target_column = st.selectbox(
                    "Sélectionnez la colonne cible",
                    df.columns
                )
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier: {str(e)}")

with col2:
    st.write("### ⚙️ Paramètres du scan")
    
    if uploaded_file:
        if st.button("🚀 Lancer le scan"):
            with st.spinner('Scan en cours...'):
                try:
                    # Création du dataset Giskard
                    dataset = Dataset(
                        df,
                        target=target_column
                    )
                    
                    # Pour l'exemple, nous utilisons un scan basique
                    # Dans un cas réel, vous devrez configurer votre modèle
                    results = scan(None, dataset)
                    
                    st.success("✅ Scan terminé!")
                    
                    # Affichage des résultats
                    st.write("### 📊 Résultats")
                    if isinstance(results, dict):
                        st.json(results)
                    else:
                        st.write(results)
                    
                except Exception as e:
                    st.error(f"❌ Erreur pendant le scan: {str(e)}")

# Section d'aide
with st.expander("📖 Guide d'utilisation"):
    st.write("""
    1. **Configuration**
       - Sélectionnez le type de modèle dans la barre latérale
       
    2. **Chargement des données**
       - Chargez votre fichier CSV
       - Sélectionnez la colonne cible
       
    3. **Scan**
       - Cliquez sur 'Lancer le scan' pour analyser
       - Les résultats s'afficheront automatiquement
    """)

# Footer
st.markdown("---")
st.markdown("*Powered by Giskard - Pour plus d'informations, visitez [Giskard Documentation](https://docs.giskard.ai/)*")
