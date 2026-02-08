

import streamlit as st
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Détection de Fraude Bancaire", page_icon="💳", layout="wide")

# 🎨 CSS personnalisé pour style moderne avec gradient violet
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main title */
    h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Card style */
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        margin-bottom: 20px;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Button style */
    .stButton>button {
        background: linear-gradient(90deg, #FFA07A, #FF6B9D);
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 25px;
        height: 55px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.6);
    }
    
    /* Input fields */
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        padding: 10px;
    }
    
    .stNumberInput label {
        color: white;
        font-weight: 500;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stNumberInput label {
        color: white;
    }
    
    /* Alert boxes */
    .alert-success {
        background: rgba(76, 175, 80, 0.2);
        border-left: 4px solid #4CAF50;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    .alert-danger {
        background: rgba(244, 67, 54, 0.2);
        border-left: 4px solid #F44336;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    .alert-warning {
        background: rgba(255, 152, 0, 0.2);
        border-left: 4px solid #FF9800;
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    
    /* Percentage circles */
    .circle-container {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }
    
    /* Season tabs */
    .season-tabs {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    
    .season-tab {
        color: rgba(255, 255, 255, 0.6);
        padding: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .season-tab.active {
        color: white;
        border-bottom: 2px solid white;
    }
</style>
""", unsafe_allow_html=True)

# 🎯 Header avec icône
col_header1, col_header2, col_header3 = st.columns([1, 2, 1])
with col_header2:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <div style='font-size: 3rem; margin-bottom: 10px;'>💳</div>
            <h1>Détection de Fraude Bancaire</h1>
        </div>
    """, unsafe_allow_html=True)

# 🔹 Sidebar pour saisir les valeurs de transaction
st.sidebar.markdown("""
    <div style='text-align: center; padding: 20px; color: white;'>
        <h2 style='color: white; font-size: 1.5rem;'>📊 Analytics</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>Entrez les paramètres de la transaction</p>
    </div>
""", unsafe_allow_html=True)

# Tabs pour organiser les features
tab_options = ["TEMPOREL", "ANALYSE 1", "ANALYSE 2", "MONTANT"]
selected_tab = st.sidebar.radio("📂 Catégorie de données", tab_options, horizontal=True)

features = []
columns = ["Time","V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12",
           "V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24",
           "V25","V26","V27","V28","Amount"]

# Diviser les colonnes en 4 groupes de manière équilibrée
groups = {
    "TEMPOREL": columns[0:8],      # Time, V1-V7 (8 champs)
    "ANALYSE 1": columns[8:16],     # V8-V15 (8 champs)
    "ANALYSE 2": columns[16:24],    # V16-V23 (8 champs)
    "MONTANT": columns[24:30]       # V24-V28, Amount (6 champs)
}

# Stocker les valeurs dans session_state
if 'feature_values' not in st.session_state:
    st.session_state.feature_values = {col: 0.0 for col in columns}

# Afficher les inputs du groupe sélectionné avec compteur
st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 10px; background: rgba(255,255,255,0.1); 
    border-radius: 10px; margin-bottom: 15px; color: white;'>
        <strong>{selected_tab}</strong> - {len(groups[selected_tab])} champs
    </div>
""", unsafe_allow_html=True)

for col in groups[selected_tab]:
    val = st.sidebar.number_input(
        col, 
        value=st.session_state.feature_values[col], 
        format="%.4f",
        key=f"input_{col}"
    )
    st.session_state.feature_values[col] = val

# Récupérer toutes les valeurs dans l'ordre
features = [st.session_state.feature_values[col] for col in columns]

# Afficher un résumé des champs remplis
filled_count = sum(1 for v in st.session_state.feature_values.values() if v != 0.0)
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div style='text-align: center; color: white; padding: 10px;'>
        <p style='font-size: 0.9rem; margin: 5px 0;'>📊 Total des champs</p>
        <p style='font-size: 1.5rem; font-weight: bold; margin: 5px 0;'>{filled_count} / 30</p>
        <div style='background: rgba(255,255,255,0.2); height: 8px; border-radius: 10px; overflow: hidden;'>
            <div style='background: linear-gradient(90deg, #FFA07A, #FF6B9D); 
            height: 100%; width: {(filled_count/30)*100}%; transition: width 0.3s ease;'></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Ajouter des métriques dans la sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div class='metric-card'>
        <div class='metric-label'>Credits</div>
        <div class='metric-value'>2,650</div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div class='metric-card' style='margin-top: 15px;'>
        <div class='metric-label'>Available stock</div>
        <div class='metric-value'>550</div>
    </div>
""", unsafe_allow_html=True)

# 🔹 Zone principale avec graphiques
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: white; text-align: center;'>📈 Statistiques des Transactions</h3>", unsafe_allow_html=True)
    
    # Graphique avec Plotly
    months = ['April', 'May', 'Jun', 'Jul']
    values = [np.random.randint(50, 150) for _ in range(4)]
    
    fig = go.Figure()
    
    # Barres colorées
    colors = ['#FFA07A', '#FF6B9D', '#FFD93D', '#6BCF7F']
    for i, (month, val) in enumerate(zip(months, values)):
        fig.add_trace(go.Bar(
            x=[month],
            y=[val],
            marker_color=colors[i % len(colors)],
            name=month,
            showlegend=False
        ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: white; text-align: center;'>🎯 Taux de Détection</h3>", unsafe_allow_html=True)
    
    # Graphiques circulaires
    col_circle1, col_circle2 = st.columns(2)
    
    with col_circle1:
        fig1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=75,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "USD/EUR", 'font': {'color': 'white', 'size': 14}},
            number={'suffix': "%", 'font': {'color': 'white', 'size': 32}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#FFA07A"},
                'bgcolor': "rgba(255,255,255,0.1)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [0, 100], 'color': 'rgba(255,255,255,0.1)'}
                ],
            }
        ))
        fig1.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            height=250,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_circle2:
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=63,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "GBP/USD", 'font': {'color': 'white', 'size': 14}},
            number={'suffix': "%", 'font': {'color': 'white', 'size': 32}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#FF6B9D"},
                'bgcolor': "rgba(255,255,255,0.1)",
                'borderwidth': 2,
                'bordercolor': "white",
                'steps': [
                    {'range': [0, 100], 'color': 'rgba(255,255,255,0.1)'}
                ],
            }
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            height=250,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 🔹 Bouton Prédire centré
st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    predict_button = st.button("🔍 Analyser la Transaction")

# 🔹 Résultats de la prédiction
if predict_button:
    with st.spinner('Analyse en cours...'):
        try:
            # 🔹 Appel à ton API FastAPI
            url = "http://127.0.0.1:8000/predict"
            data = {"features": features}
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                result = response.json()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Résultats dans des cards
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-label'>Statut Transaction</div>
                            <div class='metric-value' style='color: {"#F44336" if result["prediction"] == 1 else "#4CAF50"};'>
                                {"⚠️ FRAUDE" if result["prediction"] == 1 else "✅ LÉGITIME"}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_res2:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-label'>Probabilité de Fraude</div>
                            <div class='metric-value'>{result["probability"]*100:.1f}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_res3:
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-label'>Intervention Humaine</div>
                            <div class='metric-value' style='font-size: 2rem;'>
                                {"🚨 OUI" if result["alert_human_intervention"] else "✓ NON"}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Message d'alerte
                st.markdown("<br>", unsafe_allow_html=True)
                if result["prediction"] == 1:
                    st.markdown("""
                        <div class='alert-danger'>
                            <strong>⚠️ ALERTE FRAUDE DÉTECTÉE</strong><br>
                            Cette transaction présente des caractéristiques suspectes. Une vérification manuelle est recommandée.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class='alert-success'>
                            <strong>✅ Transaction Approuvée</strong><br>
                            Cette transaction semble légitime. Aucune anomalie détectée.
                        </div>
                    """, unsafe_allow_html=True)
                    
            else:
                st.markdown("""
                    <div class='alert-danger'>
                        <strong>❌ Erreur</strong><br>
                        Impossible de contacter l'API. Vérifiez que le serveur FastAPI est en cours d'exécution.
                    </div>
                """, unsafe_allow_html=True)
                
        except requests.exceptions.ConnectionError:
            st.markdown("""
                <div class='alert-warning'>
                    <strong>⚠️ Connexion impossible</strong><br>
                    Le serveur FastAPI n'est pas accessible à l'adresse http://127.0.0.1:8000/predict<br>
                    Veuillez démarrer votre API avec: <code>uvicorn main:app --reload</code>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
                <div class='alert-danger'>
                    <strong>❌ Erreur inattendue</strong><br>
                    {str(e)}
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.6); padding: 20px;'>
        <p>🔒 Système de Détection de Fraude Bancaire - Version 2.0</p>
        <p style='font-size: 0.8rem;'>Powered by Machine Learning & AI</p>
    </div>
""", unsafe_allow_html=True)
