# Darukaa.Earth — AI Biodiversity Intelligence

AI-powered, knowledge-grounded biodiversity intelligence chatbot using environmental metrics, retrieval, multi-metric reasoning, and scientific evidence.

## Challenge alignment
- Structured knowledge for soil health, land use/land cover, biodiversity, climate and human impact.
- Text and JSON environmental inputs.
- Clarifying questions for missing context.
- Multi-turn conversation memory.
- Multi-metric reasoning across at least three variables.
- Recommendations containing action, mechanism, impacted metrics, time horizon, confidence and evidence.
- RAG-ready knowledge layer rather than an LLM-only design.

## Architecture
User → React → FastAPI → conversation/environment context → knowledge retrieval → multi-metric reasoning → evidence-backed recommendations.

The included demo uses deterministic retrieval from `data/knowledge.json`, so it runs without an external AI key. The retrieval interface is intentionally isolated and can be replaced by embeddings + pgvector in production.

## Knowledge layer
Knowledge records cover:
- Soil pH, organic carbon and moisture
- Land use / land cover
- Species richness and habitat diversity
- Temperature and rainfall
- Pollution and deforestation

Each record contains source organization, source URL, evidence statement, ecological mechanism and keywords.

## Database
The backend stores users, conversations, messages and environmental observations in SQLite by default for easy local demonstration. Set `DATABASE_URL` to PostgreSQL for deployment. `pgvector` is included in requirements for an embedding-backed production implementation.

## Local setup

### Backend
```bash
cd backend
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Set `VITE_API_URL=http://localhost:8000`.

## API
- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `POST /chat`
- `POST /analyze`

Example `/chat` input:
```json
{
  "conversation_id": null,
  "message": "Biodiversity is declining on my land. What should I change?",
  "environment": {
    "soil_organic_carbon": "0.3%",
    "rainfall": "low",
    "land_use": "monoculture",
    "crop": "wheat",
    "region": "semi-arid",
    "soil_moisture": "low"
  }
}
```

## Recommendation format
Every generated recommendation contains:
1. What to do
2. Why it works
3. Impacted environmental metrics
4. Time horizon
5. Confidence
6. Scientific evidence links

The demo intentionally avoids unsupported quantitative claims. Add source-specific quantitative evidence to `data/knowledge.json` before publishing numerical estimates.

## CI/CD
GitHub Actions compiles the Python backend and builds the React frontend on pushes and pull requests. Connect the repository to Render and Vercel for automatic deployment after successful repository changes.

## Deployment
Frontend: Vercel.
Backend: Render.
Configure:
- Backend: `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGINS`
- Frontend: `VITE_API_URL`

Never commit `.env` or real secrets.

## Demo flow
Register → Login → enter environmental metrics → ask question → inspect retrieved knowledge → inspect recommendation and evidence → ask a follow-up question using the same conversation.

## Repository structure
```text
darukaa-earth-biodiversity-ai/
├── backend/
├── frontend/
├── data/
├── tests/
├── .github/workflows/
├── Dockerfile
└── README.md
```
