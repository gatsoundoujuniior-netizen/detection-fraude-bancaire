# 💳 Système de Détection de Fraude Bancaire

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Aperçu du Projet

Système intelligent de détection de fraude bancaire utilisant le Machine Learning (Random Forest) avec une interface web moderne développée en Streamlit.

 **des photos du projet sont disponible car je ne l'ai pas encore deploier mais je le ferais d'ici la  !** ⭐

###  Performances du Modèle

- **Précision (Fraude)** : 94%
- **Recall** : 81%
- **F1-Score** : 87%
- **Seuil de décision** : 35%
- **Seuil d'alerte** : 80%

**Statut** : ✅ Conforme aux standards bancaires internationaux (85-95%)

##  Fonctionnalités

-  Prédiction en temps réel des transactions frauduleuses
-  Dashboard interactif avec visualisations Plotly
-  Système d'alerte à double seuillage (35% et 80%)
-  Statistiques et métriques de performance
-  Conformité aux normes bancaires
-  API RESTful avec FastAPI
-  Interface moderne avec gradient violet

##  Technologies Utilisées

### Backend
- **FastAPI** - API REST haute performance
- **Scikit-learn** - Random Forest Classifier
- **Pandas** - Manipulation de données
- **NumPy** - Calculs numériques
- **Joblib** - Sérialisation du modèle

### Frontend
- **Streamlit** - Framework d'application web
- **Plotly** - Visualisations interactives

### Déploiement
- **Streamlit Cloud** - Hébergement gratuit
- **GitHub** - Contrôle de version

##  Structure du Projet

```
projet-fraude-bancaire/
├── photo_du_projet
├── API_FRAUDE.py                          # API FastAPI
├── application_pour_fraude_bancaire.py    # Interface Streamlit
├── model_wrapper.py                       # Wrapper du modèle
├── rf_fraude_final_with_threshold.pkl     # Modèle ML entraîné
├── creditcard.csv                         # Dataset (non inclus)
├── requirements.txt                       # Dépendances Python
├── README.md                              # Documentation
└── Rapport_Test_Validation_Fraude_Bancaire.pdf  # Rapport technique
```

##  Installation Locale

### 1. Cloner le Repository

```bash
git clone https://github.com/gatsoundoujuniior-netizen/detection-fraude-bancaire.git
cd detection-fraude-bancaire
```

### 2. Créer un Environnement Virtuel

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'Application

**Option A : Application Streamlit uniquement**
```bash
streamlit run application_pour_fraude_bancaire.py
```

**Option B : Avec API FastAPI (recommandé)**

Terminal 1 - API :
```bash
uvicorn API_FRAUDE:app --reload
```

Terminal 2 - Streamlit :
```bash
streamlit run application_pour_fraude_bancaire.py
```

L'application sera accessible sur `http://localhost:8501`

## 📊 Utilisation

### Interface Web

1. Ouvrez l'application Streamlit
2. Remplissez les 30 champs de features (Time, V1-V28, Amount)
3. Cliquez sur "🔍 Analyser la Transaction"
4. Consultez les résultats :
   - ✅ **LÉGITIME** (probabilité < 35%)
   - ⚠️ **FRAUDE** (probabilité ≥ 35%)
   - 🚨 **ALERTE INTERVENTION** (probabilité ≥ 80%)

### API REST

**Endpoint de prédiction :**

```bash
POST http://127.0.0.1:8000/predict
Content-Type: application/json

{
  "features": [0.0, -1.358, -0.073, 2.536, ...]  // 30 valeurs
}
```

**Réponse :**

```json
{
  "prediction": 0,
  "probability": 0.023,
  "alert_human_intervention": false
}
```

##  Tests

### Exemples de Transactions Test

**Transaction Légitime :**
```python
Time: 406.0, V1: -1.358, V2: -0.073, ..., Amount: 149.62
# Résultat attendu : 0% de fraude
```

**Transaction Frauduleuse :**
```python
Time: 40650, V1: -6.902, V2: 6.451, ..., Amount: 1499.99
# Résultat attendu : 93% de fraude + Alerte
```

## 🚀 Déploiement sur Streamlit Cloud

### 1. Préparer le Repository

Assurez-vous d'avoir :
-  `requirements.txt`
-  `application_pour_fraude_bancaire.py`
-  `model_wrapper.py`
-  `rf_fraude_final_with_threshold.pkl`

### 2. Déployer

1. Allez sur [share.streamlit.io](https://share.streamlit.io)
2. Connectez votre compte GitHub
3. Sélectionnez votre repository
4. Choisissez le fichier principal : `application_pour_fraude_bancaire.py`
5. Cliquez sur "Deploy!"

⏱️ Le déploiement prend ~2-5 minutes.

## 📈 Métriques de Performance

| Métrique | Valeur | Standard Bancaire | Statut |
|----------|--------|-------------------|--------|
| Accuracy | 100% | 95-99% | ✅ Excellent |
| Precision | 94% | 85-95% | ✅ Conforme |
| Recall | 81% | 70-85% | ✅ Très bon |
| F1-Score | 87% | 75-90% | ✅ Optimal |
| ROC-AUC | 0.90+ | > 0.85 | ✅ Excellent |

## Conformité et Sécurité

-  Respect des normes bancaires internationales
-  Scores probabilistes (jamais 100% - principe de prudence)
-  Double seuillage pour minimiser faux positifs/négatifs
-  Traçabilité et audit possibles
-  Compatible RGPD

##  Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout fonctionnalité X'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

##  License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

##  Auteur

**GATSOUNDOU Junior**  
Responsable Technique

- 📧 Email: gatsoundoujuniior@gmail.com
- 💼 LinkedIn: [gatsoundou-junior-stevy](https://www.linkedin.com/in/junior-stevy-gatsoundou-20339b25b/))
- 🐙 GitHub: [gatsoundoujuniior-netizen](https://github.com/gatsoundoujuniior-netizen))

## Remerciements

- Dataset : [Credit Card Fraud Detection - Kaggle](https://www.kaggle.com/mlg-ulb/creditcardfraud)
- Framework : Streamlit, FastAPI, Scikit-learn
- Inspiration : Normes de détection de fraude du secteur bancaire

##  Documentation Complémentaire

- [Rapport de Test et Validation (PDF)](./Rapport_Test_Validation_Fraude_Bancaire.pdf)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Streamlit](https://docs.streamlit.io/)

---

⭐ **Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !** ⭐

