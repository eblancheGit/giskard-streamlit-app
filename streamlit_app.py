import streamlit as st
import giskard
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Giskard Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS modernisés
st.markdown("""
    <style>
    /* Variables globales */
    :root {
        --primary-color: #FF6B00;
        --primary-light: #FF8533;
        --dark: #1E1E1E;
        --gray-dark: #2D2D2D;
        --gray-light: #E5E5E5;
        --white: #FFFFFF;
        --radius: 12px;
    }
    
    /* Reset et base */
    .stApp {
        background: linear-gradient(135deg, #f6f6f6 0%, #ffffff 100%);
    }
    
    /* Header principal */
    .main-header {
        background: var(--dark);
        color: var(--white);
        padding: 2rem;
        border-radius: var(--radius);
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, var(--gray-dark) 0%, var(--dark) 100%);
    }
    
    .version-tag {
        background: var(--primary-color);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-left: 1rem;
        display: inline-block;
    }
    
    /* Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: var(--radius);
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Boutons */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 2rem !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(255, 107, 0, 0.2) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px rgba(255, 107, 0, 0.3) !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        border-radius: 8px !important;
        border: 2px solid #eee !important;
        padding: 1rem !important;
    }
    
    .stTextArea>div>div>textarea {
        border-radius: 8px !important;
        border: 2px solid #eee !important;
        padding: 1rem !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent !important;
        padding: 0.5rem !important;
        border-radius: var(--radius);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--white) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        color: var(--dark) !important;
        border: none !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%) !important;
        color: white !important;
    }
    
    /* Métriques */
    .metric-container {
        background: var(--white);
        padding: 1.5rem;
        border-radius: var(--radius);
        text-align: center;
        border: 1px solid var(--gray-light);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--gray-light);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
    <div class="main-header">
        <h1 style="display: flex; align-items: center; gap: 1rem;">
            <span>🔍 Giskard Scanner</span>
            <span class="version-tag">v2.16.0</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# Navigation principale avec des icônes modernes
tabs = st.tabs([
    "🎯 Scanner",
    "⚡ Tests rapides",
    "📊 Résultats",
    "⚙️ Configuration"
])

# Onglet Scanner
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📝 Nouvelle analyse")
        
        # Sélection du type de test avec un design amélioré
        test_type = st.selectbox(
            "Type d'analyse",
            ["🎯 Qualité de réponse", "🔍 Détection d'hallucination", "🛠️ Test personnalisé"]
        )
        
        # Zone de texte pour la réponse
        response_text = st.text_area(
            "Texte à analyser",
            height=200,
            placeholder="Collez ici le texte à analyser..."
        )
        
        # Référence optionnelle
        with st.expander("➕ Ajouter une référence"):
            reference_text = st.text_area(
                "Texte de référence",
                height=150,
                placeholder="Texte de référence pour comparaison..."
            )
        
        # Bouton d'analyse
        st.button("🚀 Lancer l'analyse", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Carte des résultats
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 Résultats")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">98%</div>
                    <div>Score qualité</div>
                </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
                <div class="metric-container">
                    <div class="metric-value">0.2s</div>
                    <div>Temps d'analyse</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Historique
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📜 Historique récent")
        for i in range(3):
            st.markdown(f"""
                <div style="padding: 0.5rem; border-bottom: 1px solid #eee;">
                    <div style="color: var(--primary-color); font-weight: bold;">Test #{i+1}</div>
                    <div style="font-size: 0.9rem; color: #666;">Il y a {i+1} minute(s)</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Sidebar personnalisée
with st.sidebar:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### ℹ️ Informations")
    st.write(f"Version: {giskard.__version__}")
    st.write(f"Session démarrée: {datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)
