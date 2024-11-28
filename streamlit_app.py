import streamlit as st
import giskard
from giskard import Model, Dataset
from giskard.scanner import scan
import pandas as pd
import json
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Giskard Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS
st.markdown("""
    <style>
    /* Variables globales */
    :root {
        --primary-color: #FF6B00;
        --secondary-color: #2D2D2D;
        --background-color: #FFFFFF;
        --text-color: #1E1E1E;
        --border-radius: 8px;
        --spacing: 1rem;
    }
    
    /* Reset et base */
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Header */
    .header-section {
        background-color: var(--secondary-color);
        color: white;
        padding: var(--spacing);
        margin-bottom: var(--spacing);
        border-radius: var(--border-radius);
    }
    
    /* Cards */
    .card {
        background-color: white;
        padding: var(--spacing);
        margin-bottom: var(--spacing);
        border-radius: var(--border-radius);
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
    
    /* Boutons */
    .stButton>button {
        background-color: var(--primary-color) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 4px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 4rem;
    }
    
    /* Métriques */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: var(--border-radius);
        text-align: center;
    }
    
    /* Navigation */
    .navigation {
        display: flex;
        gap: 1rem;
        padding: 1rem;
        background: var(--secondary-color);
        margin-bottom: 2rem;
    }
    
    /* Results */
    .results-section {
        background: white;
        padding: var(--spacing);
        border-radius: var(--border-radius);
        margin-top: var(--spacing);
    }
    
    /* Utils */
    .flex {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Classe pour les tests Giskard
class GiskardTestSuite:
    def __init__(self):
        self.results = {}
    
    def run_quality_test(self, response, reference=None):
        try:
            # Simulation de test de qualité
            quality_score = 0.85
            self.results["quality"] = {
                "score": quality_score,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return quality_score
        except Exception as e:
            st.error(f"Erreur lors du test de qualité: {str(e)}")
            return None

    def run_hallucination_test(self, response, knowledge_base=None):
        try:
            # Simulation de test d'hallucination
            hallucination_score = 0.92
            self.results["hallucination"] = {
                "score": hallucination_score,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return hallucination_score
        except Exception as e:
            st.error(f"Erreur lors du test d'hallucination: {str(e)}")
            return None

# État de session
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Scanner"
if 'test_suite' not in st.session_state:
    st.session_state.test_suite = GiskardTestSuite()
if 'test_history' not in st.session_state:
    st.session_state.test_history = []

# Header principal
st.markdown("""
    <div class="header-section">
        <div class="flex">
            <h1>🔍 Giskard Scanner</h1>
            <span style="color: #FF6B00;">v{}</span>
        </div>
    </div>
""".format(giskard.__version__), unsafe_allow_html=True)

# Navigation principale
tabs = st.tabs(["📊 Scanner", "⚙️ Configurations", "📚 Bibliothèque", "❓ Aide"])

# Onglet Scanner
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📤 Configuration du test")
        
        # Type de test
        test_type = st.selectbox(
            "Type de test",
            ["Qualité de réponse", "Détection d'hallucination", "Test personnalisé"]
        )
        
        # Zone de texte pour la réponse
        response_text = st.text_area(
            "Réponse à tester",
            height=150,
            help="Collez ici la réponse du LLM à tester"
        )
        
        # Zone de texte pour la référence
        reference_text = st.text_area(
            "Texte de référence (optionnel)",
            height=150,
            help="Collez ici le texte de référence si nécessaire"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Bouton de test
        if st.button("🚀 Lancer le test"):
            with st.spinner('Test en cours...'):
                if test_type == "Qualité de réponse":
                    score = st.session_state.test_suite.run_quality_test(
                        response_text,
                        reference_text
                    )
                elif test_type == "Détection d'hallucination":
                    score = st.session_state.test_suite.run_hallucination_test(
                        response_text,
                        reference_text
                    )
                
                if score:
                    st.session_state.test_history.append({
                        "type": test_type,
                        "score": score,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Résultats")
        
        if st.session_state.test_suite.results:
            for test_type, result in st.session_state.test_suite.results.items():
                st.metric(
                    f"Score de {test_type}",
                    f"{result['score']*100:.1f}%"
                )
                st.caption(f"Testé le {result['timestamp']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Historique des tests
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📜 Historique des tests")
        
        for test in reversed(st.session_state.test_history[-5:]):
            st.markdown(f"""
                **{test['type']}**  
                Score: {test['score']*100:.1f}%  
                {test['timestamp']}
                ---
            """)
        st.markdown('</div>', unsafe_allow_html=True)

# Onglet Configurations
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("⚙️ Configurations des tests")
    
    # Paramètres des tests
    st.slider(
        "Seuil de qualité minimum",
        0.0, 1.0, 0.7,
        help="Seuil minimal pour considérer un test comme réussi"
    )
    
    st.multiselect(
        "Tests activés",
        ["Qualité", "Hallucination", "Cohérence", "Toxicité"],
        default=["Qualité", "Hallucination"]
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Onglet Bibliothèque
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📚 Bibliothèque de tests")
    
    st.write("Templates de tests disponibles :")
    test_templates = {
        "Template 1": "Test de base pour la qualité de réponse",
        "Template 2": "Test avancé pour la détection d'hallucination",
        "Template 3": "Test personnalisé pour cas spécifiques"
    }
    
    for name, description in test_templates.items():
        st.markdown(f"**{name}**")
        st.write(description)
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Onglet Aide
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("❓ Aide")
    
    st.write("""
    ### Guide d'utilisation
    
    1. **Configuration du test**
       - Choisissez le type de test
       - Entrez la réponse à tester
       - Ajoutez une référence si nécessaire
    
    2. **Lancement du test**
       - Cliquez sur 'Lancer le test'
       - Attendez les résultats
    
    3. **Analyse des résultats**
       - Consultez les scores
       - Vérifiez l'historique
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("ℹ️ Informations")
    st.write(f"Version Giskard: {giskard.__version__}")
    st.write("Session active depuis:", datetime.now().strftime("%H:%M:%S"))
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Powered by Giskard - <a href="https://docs.giskard.ai/" target="_blank">Documentation</a></p>
    </div>
""", unsafe_allow_html=True)
