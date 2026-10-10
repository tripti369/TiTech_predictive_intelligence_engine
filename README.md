# Predictive Intelligence Engine

deployed link - https://titech-predictive-intelligence-engine-2.onrender.com

Ek full-stack Business Intelligence project — real CSV data par forecasting,
churn/attrition analysis, Monte Carlo scenario simulation aur ek RAG-based
knowledge search karta hai. Backend aur Frontend do bilkul alag folders mein
hain taaki dono independently run/deploy ho sakein.

```
predictive-intelligence-engine/
├── backend/            # FastAPI + SQLite — core API, database, and real datasets
│   ├── app/
│   │   ├── agents/      # 5 Autonomous AI agents (analysis, forecast, scenario, rag, decision)
│   │   ├── routes/      # Clean REST endpoints (/predict, /analysis, /scenario, /upload, etc.)
│   │   ├── database.py  # SQLite connection & session management
│   │   ├── models.py    # SQLAlchemy database schema
│   │   ├── schemas.py   # Pydantic data validation
│   │   └── main.py      # FastAPI application & static mount
│   ├── data/
│   │   ├── cleaned/     # Pre-processed real-world CSV datasets
│   │   ├── uploaded/    # User CSV uploads directory
│   │   └── knowledge/   # Domain markdown knowledge base for ChromaDB RAG
│   ├── requirements.txt # Backend dependencies
│   └── run.py           # Backend convenience launcher
│
├── frontend/           # Modern SPA web interface (HTML5, Vanilla CSS, JS, Chart.js)
│   ├── index.html       # Single Page Application
│   ├── css/             # Design system tokens and styles
│   ├── js/              # Dynamic charts, API connectors, simulation controllers
│   └── assets/          # Icons and branding
│
├── docs/               # Detailed documentation, guides, and presentation notes
│   ├── PRESENTATION_GUIDE.md  # Minor project presentation & viva prep
│   ├── API_DOCS.md            # Complete API documentation
│   ├── PROJECT_STRUCTURE.md   # System architecture
│   └── TESTING.md             # Quality assurance guide
│
├── tests/              # Automated test suites
│   ├── test_gemini_integration.py
│   └── test_realtime_system.py
│
├── Dockerfile          # Production Docker configuration
├── render.yaml         # 1-Click Render.com deployment blueprint
├── requirements.txt    # Universal root dependencies
└── main.py             # Root application entrypoint (python main.py)
```

## Kya real hai is project mein (fake mock-data nahi)

- Har number backend ke real CSV datasets (customer churn, employee HR
  attrition, retail/warehouse sales) se compute hota hai.
- **Database**: SQLite (`backend/data/app.db`) — har prediction run, scenario
  simulation aur upload database mein log hota hai. "Reports & History" page
  yeh real history dikhata hai.
- **RAG Knowledge Base**: `backend/data/knowledge/*.md` files mein asli
  computed insights likhe hain (jaise "Pune attrition 50.9%"), aur RAG agent
  in par persistent ChromaDB search karta hai. Gemini answers isi retrieved
  evidence par grounded hain, with local fallback when the provider is busy.
- **Forecasting**: Holt-Winters exponential smoothing (jab enough data ho),
  warna safe weighted-moving-average fallback — kabhi crash nahi karega.

---

## Kaise Run Karein

### 1. Backend start karo (pehle yeh)

```bash
cd backend
python -m venv venv                     # optional but recommended
source venv/bin/activate                # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Backend `http://127.0.0.1:8000` par chalega. Check karne ke liye browser
mein `http://127.0.0.1:8000/docs` kholo — Swagger UI mein saare endpoints
dikhenge aur wahin se test bhi kar sakte ho.

### 2. Frontend kholo (dusra terminal)

Sabse simple tarika — `frontend/index.html` ko seedha double-click karke
browser mein khol do. Backend `http://127.0.0.1:8000` par already CORS
allow karta hai (`allow_origins=["*"]`), isliye yeh direct file-open se bhi
chalega.

Agar aap ek local server se serve karna chahte ho (recommended, kuch
browsers file:// se fetch block karte hain):

```bash
cd frontend
python -m http.server 5500
```

Phir browser mein `http://127.0.0.1:5500` kholo.

### 3. Ek-Click Live Deployment (Render / Docker)

Is repo mein **single-service deployment** configured hai — backend hi frontend ko serve karta hai!

#### A. Render.com par Deploy (Recommended - Free):
1. **[dashboard.render.com](https://dashboard.render.com)** par jao aur GitHub se sign in karo.
2. **New +** -> **Web Service** choose karo.
3. Apna repository select karo: `tripti369/TiTech_predictive_intelligence_engine`
4. Settings fill karo:
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120`
5. Environment Variables mein add karo (optional):
   - `GEMINI_API_KEY`: *(Apni Google Gemini API key)*
6. Click **Deploy Web Service** — 2-3 minute mein live link mil jayega!

#### B. Docker se Deploy:
```bash
docker build -t predictive-intelligence .
docker run -p 8000:8000 predictive-intelligence
```
Browser mein `http://localhost:8000` kholo!

---

## API Endpoints (backend)

| Method | Endpoint          | Kya karta hai |
|--------|-------------------|---------------|
| GET    | `/api/health`     | Backend zinda hai ya nahi |
| GET    | `/api/predict`    | Dashboard KPIs + forecast + decision (main endpoint) |
| GET    | `/api/analysis`   | Correlation, outliers, descriptive stats |
| GET    | `/api/scenario`   | Monte Carlo revenue simulation |
| POST   | `/api/upload`     | CSV upload → classify → DB me save |
| GET    | `/api/knowledge`  | RAG search (query param `q`) |
| GET    | `/api/history`    | Database se past runs |
| GET    | `/api/datasets`   | Available datasets ki list |

Poori interactive documentation: `http://127.0.0.1:8000/docs`

---

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy + SQLite, pandas, numpy, scikit-learn,
  statsmodels
- **Frontend**: Plain HTML/CSS/JS (no framework, no build step), Chart.js
  for graphs
- **Database**: SQLite (file-based, zero setup)

## Hackathon Demo Tips

1. Sabse pehle Dashboard page dikhao — real-time KPIs, forecast chart.
2. Data Upload page pe apni koi CSV daal ke dikhao ki backend usko
   auto-classify kar deta hai.
3. Scenario Simulator ke sliders move karke live Monte Carlo dikhao.
4. Knowledge Base me kuch pucho jaise "why do customers churn" — RAG agent
   se real answer aayega.
5. Reports page pe jitni baar tumne demo ke dauraan endpoints hit kiye
   honge, sab history yahan dikh jayegi — proof ki database sach me kaam
   kar raha hai.
