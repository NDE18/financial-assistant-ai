# Financial Assistant AI (POC)

Backend: FastAPI + SQLModel + CrewAI/OpenAI
Frontend: React + TypeScript + TailwindCSS

## Prérequis
- Python 3.11+
- Node.js 18+

## Backend
```
cd backend
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Éditez .env et ajoutez OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

Endpoints clés:
- POST /transactions, GET /transactions, POST /transactions/categorize
- GET /reports/monthly?year=YYYY&month=M
- POST /documents/upload

## Frontend
```
cd frontend
npm install
npm run dev
```

## Architecture
- backend/app
  - core (config)
  - agents (CrewAI)
  - services (LLM, catégorisation, reporting)
  - routers (transactions, budgets, reports, ...)
  - models (SQLModel)
- frontend/src
  - pages (Dashboard, Transactions, Budgets, Reports, ...)
  - lib/api.ts (Axios)
  - components

## Notes
- La catégorisation et le résumé mensuel utilisent le modèle OpenAI gpt-4o-mini.
- La couleur primaire UI est configurée sur la palette "emerald" (vert).
- Multi-devises: base EUR, table `ExchangeRate`. Utilisez l'API `/fx/rates` pour définir par ex. USD→EUR.
