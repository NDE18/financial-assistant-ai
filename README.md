# Assistant Financier - Agentic AI avec CrewAI

POC d'un assistant financier intelligent utilisant l'orchestration collaborative d'agents IA via CrewAI.

## 🚀 Fonctionnalités

### MVP Implémenté
1. **Gestion des Transactions**
   - Création/modification/suppression
   - Classification automatique par IA (GPT-3.5)
   - Détection de transactions récurrentes
   - Scores de confiance

2. **Extraction OCR de Factures**
   - Upload de factures (PDF, JPG, PNG)
   - Extraction automatique via GPT-4 Vision
   - Création automatique de transactions
   - Validation des données extraites

3. **Analyse Financière**
   - KPIs en temps réel
   - Répartition par catégorie
   - Tendances et graphiques
   - Insights générés par IA
   - Alertes budgétaires

4. **Génération de Rapports**
   - Rapports mensuels/trimestriels
   - Analyse complète par IA (GPT-4)
   - Recommandations personnalisées
   - Export et archivage

### Architecture Agentic AI

**Orchestration Collaborative (CrewAI)**
- **Orchestrator Agent**: Coordinateur principal
- **Classifier Agent**: Catégorisation des transactions
- **Analyst Agent**: Analyse financière approfondie
- **Reporter Agent**: Génération de rapports
- **OCR Agent**: Extraction de données de factures

## 📦 Stack Technique

### Backend
- FastAPI 0.104+
- SQLAlchemy 2.0 + PostgreSQL
- CrewAI 0.28+ (orchestration)
- OpenAI API (GPT-4, GPT-3.5, GPT-4 Vision)
- LangChain

### Frontend
- React 18 + TypeScript
- TailwindCSS 3
- Recharts (visualisations)
- React Router
- Axios

## 🛠️ Installation & Démarrage

### Prérequis
- Docker & Docker Compose
- Clé API OpenAI

### Démarrage rapide

1. **Cloner le projet**
```bash
git clone <repo-url>
cd financial-assistant-ai
```

2. **Configuration**
```bash
# Backend
cp backend/.env.example backend/.env
# Éditer backend/.env et ajouter votre OPENAI_API_KEY
```

3. **Lancement avec Docker**
```bash
docker-compose up --build
```

4. **Accès**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Documentation API: http://localhost:8000/docs

### Installation manuelle (sans Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Créer la base de données
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"

# Lancer le serveur
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📊 Utilisation

### 1. Ajouter des Transactions
- Manuellement via le formulaire
- Import CSV (batch avec classification IA)

### 2. Scanner des Factures
- Glisser-déposer une facture
- L'OCR Agent extrait automatiquement les données
- Une transaction est créée automatiquement

### 3. Consulter les Analyses
- Dashboard avec KPIs en temps réel
- Graphiques de tendances
- Répartition par catégorie
- Insights générés par l'IA

### 4. Générer des Rapports
- Sélectionner une période
- L'IA analyse les données
- Rapport complet avec recommandations

## 🤖 Agents CrewAI

### Classifier Agent (GPT-3.5)
- Catégorise les transactions
- Détecte les doublons
- Score de confiance
- Tags automatiques

### Analyst Agent (GPT-4)
- Analyse des tendances
- Calcul de KPIs
- Détection d'anomalies
- Prévisions de trésorerie

### Reporter Agent (GPT-4)
- Synthèse des données
- Insights narratifs
- Recommandations personnalisées
- Format professionnel

### OCR Agent (GPT-4 Vision)
- Extraction de texte
- Validation des données
- Structuration JSON
- Gestion d'erreurs

## 🔮 Évolutions Futures

### Phase 2
- Authentification JWT
- Multi-utilisateurs/organisations
- Intégration bancaire (Plaid, Bridge)
- Notifications temps réel (WebSocket)

### Phase 3
- Réconciliation bancaire automatique
- Prévisions ML avancées
- Assistant conversationnel (chatbot)
- Export comptable (FEC, CSV)

### Phase 4
- Conformité fiscale
- Aide à l'audit
- Tableaux de bord personnalisables
- API publique