# 📋 9-Week Comprehensive Project Progress & Contribution Report
## Project Title: TiTech Predictive Intelligence Engine (PIE)
**Academic Level**: Minor Project / Capstone Evaluation  
**Architecture**: Autonomous Multi-Agent Predictive System with RAG & Real-Time Analytics  

---

## 👥 Team Roles & Responsibilities Overview

| Role | Member Designation | Primary Domain | Core Technologies |
| :--- | :--- | :--- | :--- |
| **Person 1** | **Frontend Engineer** | UI/UX, Component Design, Single Page Application (SPA), Visual Analytics | HTML5, Modern Vanilla CSS, JavaScript (ES6+), Chart.js |
| **Person 2** | **Backend Engineer** | REST API Architecture, Database Schema, Data Models & Persistence | Python, FastAPI, SQLAlchemy, SQLite, Pydantic, Gunicorn |
| **Person 3** | **AI / ML Engineer** | Statistical Profiling, Time-Series Forecasting, Stochastic Simulation | Pandas, NumPy, Scikit-Learn, Statsmodels (Holt-Winters), Monte Carlo |
| **Person 4** | **Integration & DevOps** | Vector Search (RAG), LLM Grounding, CI/CD, Containerization & Cloud Deployment | ChromaDB, Google Gemini AI API, Docker, Docker-Compose, Render.com |

---

## 📅 Week-by-Week Contribution Log (Weeks 1 to 9)

```
W1: Requirement & Architecture ──► W2: Foundation & Data Cleaning ──► W3: Core Algorithms & Models
                                                                              │
W6: RAG, Gemini & Storage     ◄── W5: Frontend-Backend Fusion    ◄── W4: API Routing & Interactive UI
       │
       ▼
W7: System Optimization & Cache ──► W8: End-to-End Testing & QA  ──► W9: Production Deployment & Viva Prep
```

---

### 🗓️ Week 1: Problem Definition, Feasibility Study & System Architecture
* **Theme**: Requirements Engineering, Domain Research & System Design

#### 🔹 Person 1 (Frontend):
- Conducted UI/UX benchmarking across modern enterprise BI tools (Datadog, Tableau, Snowflake).
- Designed low-fidelity wireframes for a 10-view dashboard: Executive Dashboard, AI Workspace, Dataset Manager, Knowledge Chat, Forecasting, Analytics, Scenario Simulator, Agent Constellation, Reports, and Settings.
- Defined typography (Inter, JetBrains Mono) and established an accessible dark-mode color token system (`#080b14` background, `#3E7BFA` accent, `#7ff3c4` status indicators).

#### 🔹 Person 2 (Backend):
- Drafted system architecture document comparing Flask, Django, and FastAPI; selected FastAPI for asynchronous throughput and native OpenAPI documentation.
- Designed high-level directory layout separating domain concerns (`app/agents/`, `app/routes/`, `app/models/`, `data/`).
- Initialized FastAPI application skeleton with global CORS middleware policies (`allow_origins=["*"]`).

#### 🔹 Person 3 (AI/ML):
- Procured enterprise datasets across 3 key business verticals: Customer Churn (Telecom), Employee HR Attrition, and Warehouse/Retail Sales.
- Verified data viability, identified missing values, duplicate records, and target variables (`Churn`, `LeaveOrNot`, `Total_Sales`).
- Formulated the statistical objectives: forecasting sales trajectories, predicting customer retention risk, and modeling price sensitivity.

#### 🔹 Person 4 (Integration & DevOps):
- Setup Git version control repository (`main` branch workflow) with strict `.gitignore` patterns preventing repository bloat.
- Conducted environment isolation testing across Python 3.10 and 3.11 virtual environments.
- Researched LLM integration viability using Gemini Flash and ChromaDB vector store for low-latency RAG retrieval.

* **Sprint Milestone 1**: System Architecture Blueprint, Git Repository setup, and raw dataset viability approved.

---

### 🗓️ Week 2: Data Preprocessing, Database Schema & Design System
* **Theme**: Foundation Engineering & Data Hygiene

#### 🔹 Person 1 (Frontend):
- Developed the foundational CSS layout system (`css/variables.css`, `css/layout.css`, `css/components.css`).
- Built modular card components, metric badges (`info`, `warning`, `success`), and custom scrollbars.
- Implemented the responsive desktop app shell featuring a 260px fixed sidebar and sticky top header with dynamic breadcrumb navigation.

#### 🔹 Person 2 (Backend):
- Implemented SQLAlchemy engine in `backend/app/database.py` with declarative Base and SQLite thread-safe connection pooling.
- Designed relational database schemas in `backend/app/models.py`:
  - `PredictionRun`: Records forecast accuracy, growth rate, churn rate, attrition rate, risk grade, and timestamps.
  - `ScenarioSimulation`: Records simulation parameters (growth, elasticity, cost, VaR 95%).
  - `UploadedDataset`: Records metadata, row counts, column names, and file paths.
- Authored automated table creation hooks triggered on application startup.

#### 🔹 Person 3 (AI/ML):
- Engineered cleaning and preprocessing pipelines for raw enterprise data:
  - Cleaned `customer_churn_cleaned.csv` (64,374 rows, 12 verified columns).
  - Cleaned `employee_hr_cleaned.csv` (2,764 rows, zero missing records).
  - Cleaned `retail_warehouse_sales_cleaned.csv` (30,000 transaction records).
- Encapsulated data loader utility functions and verified zero-variance columns removal.

#### 🔹 Person 4 (Integration & DevOps):
- Constructed `backend/app/utils.py` with unified path resolution logic for `DATA_DIR`, `UPLOAD_DIR`, and `REALTIME_DIR`.
- Structured the domain knowledge documents (`churn_insights.md`, `hr_attrition_insights.md`, `retail_sales_insights.md`) converting raw data statistics into structured textual evidence.
- Authored initial `requirements.txt` specifying exact package pins for reproducibility.

* **Sprint Milestone 2**: 3 clean datasets verified, SQLite database operational, core CSS design system completed.

---

### 🗓️ Week 3: Statistical Analysis Agent, Holt-Winters Forecaster & Chart Framework
* **Theme**: Core Machine Learning & Data Visualization

#### 🔹 Person 1 (Frontend):
- Integrated Chart.js (v4.4.0) into the single-page application framework.
- Built reusable canvas gradient generator helper (`chartGrad`) for dynamic area fills.
- Constructed interactive Dashboard KPI trend line chart comparing Monthly Revenue against Operating Profit with custom tooltip formatting.

#### 🔹 Person 2 (Backend):
- Built Pydantic validation schemas in `backend/app/schemas.py` for API requests and response contracts.
- Configured file upload handlers capable of receiving multipart form data, validating `.csv` MIME types, and streaming data safely to disk.
- Connected database session lifecycle dependencies using FastAPI's `Depends(get_db)`.

#### 🔹 Person 3 (AI/ML):
- Implemented `AnalysisAgent` (`backend/app/agents/analysis_agent.py`):
  - Basic profiling: row/column counts, missing value tallies, memory footprint, data types.
  - Descriptive statistics: Mean, standard deviation, quartiles ($25\%$, $50\%$, $75\%$), min/max.
  - Outlier detection using Tukey's Interquartile Range (IQR) rule ($1.5 \times \text{IQR}$).
  - Full Pearson correlation matrix computation across continuous features.
- Implemented `ForecastingAgent` (`backend/app/agents/forecasting_agent.py`):
  - Triple Exponential Smoothing (Holt-Winters) handling level, trend, and seasonal additive components.
  - Calculated Symmetric Mean Absolute Percentage Error (sMAPE) for model accuracy evaluation.

#### 🔹 Person 4 (Integration & DevOps):
- Identified platform-level C-extension dependency issues on Windows with `statsmodels`.
- Engineered an adaptive damped weighted moving average fallback inside `ForecastingAgent` to guarantee $100\%$ zero-crash fault tolerance when data length is sub-seasonal.
- Set up local unit test harness verifying agent execution outputs against known mathematical baseline numbers.

* **Sprint Milestone 3**: Statistical agent profiling functional, Holt-Winters forecasting operational with robust math fallbacks.

---

### 🗓️ Week 4: REST API Endpoints, Dynamic Routing & Interactive Sliders
* **Theme**: API Exposure & User Interaction

#### 🔹 Person 1 (Frontend):
- Developed the Scenario Simulator UI (`frontend/js/scenario.js`):
  - Dynamic slider controls for Target Growth ($-20\%$ to $+50\%$), Price Elasticity ($0.5\text{x}$ to $3.0\text{x}$), and Cost Inflation ($0\%$ to $25\%$).
  - Dynamic real-time parameter feedback counters.
- Built the interactive Monte Carlo outcome distribution histogram using Chart.js color-banded bins (red for downside risk, green for upside opportunity).

#### 🔹 Person 2 (Backend):
- Implemented modular route files in `backend/app/routes/`:
  - `analysis.py`: `GET /api/analysis` delivering descriptive stats and correlation matrices.
  - `scenario.py`: `GET /api/scenario` accepting simulation parameters and returning statistical projections.
  - `datasets.py`: `GET /api/datasets` cataloging available datasets with file sizes and row counts.
- Implemented universal dual-prefix mounting in `main.py` allowing endpoints to be reached via both `/api/*` and root `/*`.

#### 🔹 Person 3 (AI/ML):
- Implemented `ScenarioAgent` (`backend/app/agents/scenario_agent.py`):
  - Best-case, base-case, and worst-case deterministic multi-variable projections.
  - Stochastic Monte Carlo simulation running $N = 3,000$ iterations with Gaussian disturbance distribution.
  - Parametric 95% Value-at-Risk ($\text{VaR}_{95}$) calculation to quantify maximum probable quarterly revenue downside.
  - Elasticity sensitivity coefficient calculation.

#### 🔹 Person 4 (Integration & DevOps):
- Standardized API response headers and CORS cross-origin configuration.
- Validated REST API endpoints using Swagger UI (`/docs`) and Redoc (`/redoc`).
- Structured end-to-end integration test script `tests/test_realtime_system.py` verifying response schema validity and status codes.

* **Sprint Milestone 4**: Scenario simulator functional end-to-end; REST API endpoints serving live computed statistical outputs.

---

### 🗓️ Week 5: Multi-Agent Pipeline Orchestration & End-to-End View Integration
* **Theme**: Client-Server Integration & Workflow Pipelines

#### 🔹 Person 1 (Frontend):
- Developed the AI Workspace view (`view-workspace`) featuring an interactive 9-step animated pipeline timeline:
  - Steps: Upload ➔ Classification ➔ AI Processing ➔ Forecasting ➔ Analytics ➔ Knowledge ➔ Scenario ➔ Validation ➔ Recommendations.
- Built live agent event execution logs with millisecond timestamps and color-coded status pills.
- Connected the "Run pipeline" button to invoke the live `/api/predict` pipeline endpoint.

#### 🔹 Person 2 (Backend):
- Implemented `backend/app/routes/predict.py`:
  - Synthesizes metrics across customer churn, employee attrition, and warehouse sales.
  - Assembles unified JSON payload containing revenue history, Holt-Winters 6-month projections, subscription breakdown, and city attrition ratios.
  - Persists executed pipeline runs into SQLite database table `prediction_runs`.

#### 🔹 Person 3 (AI/ML):
- Implemented `DecisionAgent` (`backend/app/agents/decision_agent.py`):
  - Multi-criteria risk scoring engine fusing forecast error, customer churn rates ($>45\%$), and city attrition rates ($>35\%$).
  - Outputs composite risk classifications: `Low`, `Medium`, or `High`.
  - Generates itemized, context-aware operational recommendations for executive leadership.

#### 🔹 Person 4 (Integration & DevOps):
- Connected the frontend API client (`frontend/js/config.js` and `frontend/js/api.js`) to support dynamic backend URL resolution via `<meta name="backend-url">`, environment variables, or relative server origin.
- Conducted multi-browser compatibility testing across Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari.

* **Sprint Milestone 5**: Full end-to-end pipeline execution functional; Dashboard and Workspace reflecting real computed data.

---

### 🗓️ Week 6: Vector Search (ChromaDB), Gemini AI Grounding & Knowledge Base
* **Theme**: Retrieval-Augmented Generation (RAG) & Semantic Search

#### 🔹 Person 1 (Frontend):
- Built the Knowledge Base chat interface (`view-knowledge`):
  - User query input, interactive message bubble stream, and auto-scrolling conversation area.
  - Document provenance badges displaying source citations (e.g., `📄 churn_insights.md`) and cosine relevance confidence percentages.
  - Engine status indicator showing whether response was generated by Google Gemini 3.8 Flash or Local RAG fallback.

#### 🔹 Person 2 (Backend):
- Created `backend/app/routes/knowledge.py`:
  - `GET /api/knowledge` accepting semantic search parameter `q`.
  - `GET /api/ask` delivering unified synthesis with citations.
- Implemented database logging for user queries and knowledge retrieval events.

#### 🔹 Person 3 (AI/ML):
- Implemented `RAGAgent` (`backend/app/agents/rag_agent.py`):
  - Integrated ChromaDB persistent vector database indexer.
  - Extracted chunked document embeddings and created cosine distance search collection.
  - Engineered keyword relevance score weighting to maintain high recall on specific numerical queries (e.g., "Pune attrition rate").

#### 🔹 Person 4 (Integration & DevOps):
- Integrated Google GenAI Python SDK (`google-genai>=1.0.0`) with Gemini 3.8 Flash.
- Implemented secure API key management via environment variables (`GEMINI_API_KEY`).
- Engineered zero-downtime offline fallback: when Gemini API key is missing or quota is exhausted, system automatically formats evidence-grounded answers from retrieved vector context without raising exceptions.
- Authored test suite `tests/test_gemini_integration.py`.

* **Sprint Milestone 6**: RAG Knowledge Base operational with vector similarity search and dual-mode Gemini / Local synthesis.

---

### 🗓️ Week 7: In-Memory Caching, Cold-Start Resilience & UI Polish
* **Theme**: Performance Optimization, Latency Reduction & Fault Tolerance

#### 🔹 Person 1 (Frontend):
- Implemented smart retry resilience in `frontend/index.html`:
  - Auto-retry mechanism (2 attempts, 2.5s interval) for `loadDatasets` and `loadHistory` to transparently absorb cloud cold starts.
  - Interactive `[⚡ Retry Pipeline]` and `[Retry]` buttons providing user control during network wake-up periods.
  - Implemented Canvas constellation visualizer (`initConstellation`) showing real-time agent interconnectivity.

#### 🔹 Person 2 (Backend):
- Implemented high-performance in-memory caching (`_DEFAULT_PREDICT_CACHE`) in `backend/app/routes/predict.py`.
  - Reduces repeated default pipeline execution time from ~8,000ms down to **< 10ms** ($99.8\%$ latency reduction).
  - Eliminates redundant recalculation of 64,000+ customer records during continuous UI navigation.

#### 🔹 Person 3 (AI/ML):
- Optimized memory footprint of DataFrame operations:
  - Downcasted numerical column types where appropriate.
  - Replaced repetitive full-table scans with cached grouped aggregations for city metrics and subscription tiers.
- Validated numerical consistency across the Monte Carlo and Holt-Winters calculation pipelines.

#### 🔹 Person 4 (Integration & DevOps):
- Analyzed and resolved Render HTTP 502 Bad Gateway timeouts occurring during cold starts.
- Tuned Gunicorn worker settings (`--workers 1 --timeout 120`) to allow long-running analytical operations without premature connection termination.
- Verified persistent ChromaDB cache files in `backend/data/rag_index_cache.json`.

* **Sprint Milestone 7**: API latency reduced by $99.8\%$; 502 gateway cold-start handling resolved with automated UI retries.

---

### 🗓️ Week 8: System Verification, Containerization & End-to-End QA
* **Theme**: Packaging, Container Testing & Quality Assurance

#### 🔹 Person 1 (Frontend):
- Built dynamic report exporter supporting instant client-side download of Executive Decision Briefs in JSON and text summary formats.
- Added personalized greeting system based on login credentials and current system time.
- Conducted full responsive design audit on mobile, tablet, and widescreen viewports.

#### 🔹 Person 2 (Backend):
- Consolidated root entrypoints `app.py` and `main.py` to seamlessly expose the FastAPI application across any ASGI container or command-line runner (`uvicorn main:app`, `python main.py`).
- Completed database audit verifying that every prediction, scenario run, and file upload is accurately logged with referential integrity.

#### 🔹 Person 3 (AI/ML):
- Executed stress testing on data upload classification engine (`classifyDataset`):
  - Verified automatic detection of CRM/Churn, HR/Employee, Retail, and Financial ledger formats with $>90\%$ accuracy.
  - Validated graceful handling of corrupted or empty CSV files.

#### 🔹 Person 4 (Integration & DevOps):
- Built multi-stage production `Dockerfile`:
  - Based on `python:3.11-slim` with minimal build dependencies.
  - Dynamic port binding supporting `$PORT` environment variable (`CMD ["sh", "-c", "gunicorn ... --bind 0.0.0.0:${PORT:-8000}"]`).
- Created `docker-compose.yml` for unified local development and multi-container validation.
- Executed all automated integration test scripts (`test_gemini_integration.py`, `test_realtime_system.py`) with $100\%$ pass rates.

* **Sprint Milestone 8**: Docker image tested successfully; automated test suite fully green; root runners verified.

---

### 🗓️ Week 9: Production Deployment, Single-Branch Consolidation & Viva Preparation
* **Theme**: Production Release, Documentation & Final Presentation Readiness

#### 🔹 Person 1 (Frontend):
- Finalized presentation assets and verified chart animation smoothness during screen sharing.
- Prepared frontend talking points: UI design philosophy, Chart.js optimization, responsive glassmorphism aesthetic, and accessibility compliance.
- Authored frontend walkthrough section for minor project submission.

#### 🔹 Person 2 (Backend):
- Synchronized `backend/requirements.txt` and root `requirements.txt` to guarantee universal package parity across all cloud hosting providers.
- Prepared backend talking points: FastAPI ASGI architecture, SQLAlchemy ORM modeling, dual API routing strategy, and in-memory caching.
- Authored API documentation in `docs/API_DOCS.md`.

#### 🔹 Person 3 (AI/ML):
- Formulated mathematical defense for viva examination:
  - Derivation and equations for Holt-Winters Additive model (Level $\ell_t$, Trend $b_t$, Seasonality $s_t$).
  - Mathematical definition of Tukey's IQR outlier boundaries.
  - Monte Carlo stochastic methodology and Value-at-Risk ($\text{VaR}_{95}$) percentiles.
- Prepared AI/ML talking points and comparative performance evaluation metrics.

#### 🔹 Person 4 (Integration & DevOps):
- Deployed live production service to Render.com:  
  🌐 **Live URL**: `https://titech-predictive-intelligence-engine-2.onrender.com`
- Consolidated GitHub repository into **exactly one branch (`main`)**, deleted deprecated remote branches (`clean-backend`, `backend-deploy`), and eliminated duplicate root files.
- Authored comprehensive project presentation documentation in `docs/PRESENTATION_GUIDE.md` with complete question-and-answer preparation for external examiners.

* **Sprint Milestone 9**: Live deployment verified on Render.com, GitHub repository consolidated to clean single branch, full project report and viva defense prepared.

---

## 📊 Summary of Individual Technical Contributions

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                           TEAM CONTRIBUTION MATRIX                             │
├────────────────────┬───────────────────────────────────────────────────────────┤
│ Team Member        │ Key Code Files Owned & Technical Deliverables             │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Person 1 (Frontend)│ • frontend/index.html (Single-Page Application Shell)     │
│                    │ • frontend/css/ (variables.css, layout.css, components)   │
│                    │ • frontend/js/ (charts.js, scenario.js, nav.js, upload)   │
│                    │ • Chart.js visualizations, responsive UI & retry logic    │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Person 2 (Backend) │ • backend/app/main.py (FastAPI application & mount)       │
│                    │ • backend/app/routes/ (predict, analysis, scenario, etc.) │
│                    │ • backend/app/database.py & models.py (SQLite/SQLAlchemy) │
│                    │ • backend/app/schemas.py (Pydantic validation)            │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Person 3 (AI / ML) │ • backend/app/agents/analysis_agent.py (IQR, Stats)       │
│                    │ • backend/app/agents/forecasting_agent.py (Holt-Winters)  │
│                    │ • backend/app/agents/scenario_agent.py (Monte Carlo, VaR) │
│                    │ • backend/app/agents/decision_agent.py (Risk Scoring)     │
├────────────────────┼───────────────────────────────────────────────────────────┤
│ Person 4 (DevOps & │ • backend/app/agents/rag_agent.py (ChromaDB Vector Store) │
│           Integr.) │ • Google Gemini 3.8 Flash SDK Integration & Fallback      │
│                    │ • Dockerfile, docker-compose.yml, render.yaml             │
│                    │ • Live Cloud Deployment on Render.com & Test Suites       │
└────────────────────┴───────────────────────────────────────────────────────────┘
```

---

## 🎓 Viva-Voce & Examiner Defense Guide

### Q1. Why did you use Holt-Winters instead of an LSTM or Deep Learning model?
* **Person 3 (AI/ML) Answers**:
> "For tabular business time-series with monthly frequency and clear seasonal components, Holt-Winters Triple Exponential Smoothing is computationally lightweight, explainable, and converges instantaneously without requiring thousands of training epochs or GPU infrastructure. Furthermore, we designed an adaptive damped moving average fallback that guarantees the system never crashes on short or non-seasonal data series."

### Q2. How is RAG implemented in this project and why is it grounded?
* **Person 4 (Integration) Answers**:
> "Our RAG agent indexes domain-specific business knowledge documents into a ChromaDB persistent vector database using cosine distance metrics. When a user asks a query, relevant text chunks with verified statistical figures (e.g., Pune's 50.9% attrition rate) are retrieved and injected into the prompt context for Google Gemini 3.8 Flash. This eliminates hallucinations because the LLM is restricted to evidence retrieved directly from our verified data."

### Q3. Why use FastAPI over Flask or Django?
* **Person 2 (Backend) Answers**:
> "FastAPI is natively asynchronous (ASGI), provides automatic data validation via Pydantic, generates interactive OpenAPI documentation out-of-the-box, and delivers significantly higher throughput compared to synchronous WSGI frameworks like Flask. It is also lightweight and pairs cleanly with SQLAlchemy for SQLite persistence."

### Q4. How does the frontend maintain real-time responsiveness without heavy frameworks like React or Angular?
* **Person 1 (Frontend) Answers**:
> "We implemented a vanilla JavaScript Single-Page Application (SPA) architecture with modular CSS design tokens and Chart.js. By avoiding heavy framework bundle overhead, initial page load is near-instantaneous (~85 KB total footprint). We also implemented asynchronous promise-based fetch handlers with automated retry logic to seamlessly recover from cloud container cold starts."
