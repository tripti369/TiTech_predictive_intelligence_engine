from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.analysis_agent import AnalysisAgent
from agents.forecasting_agent import ForecastingAgent
from agents.scenario_agent import ScenarioAgent
from agents.rag_agent import RAGAgent
from agents.decision_agent import DecisionAgent

app = FastAPI(
    title="Predictive Intelligence Engine API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Predictive Intelligence Engine Running"
    }


@app.get("/predict")
def predict():

    analysis_agent = AnalysisAgent()

    analysis_result = analysis_agent.analyze_dataset(
        "customer_churn_cleaned.csv"
    )

    forecasting_agent = ForecastingAgent()

    forecast_result = forecasting_agent.forecast_dataset(
        filename="retail_warehouse_sales_cleaned.csv",
        date_columns=["year", "month"],
        target_column="retail_sales",
        forecast_periods=12
    )

    scenario_agent = ScenarioAgent()

    scenario_result = scenario_agent.simulate(
        forecast_result["forecast"]
    )

    rag_agent = RAGAgent()

    rag_agent.build_index()

    rag_result = rag_agent.answer(
        "forecasting customer churn payment delay business"
    )

    decision_agent = DecisionAgent()

    decision = decision_agent.generate_decision(
        analysis_result,
        forecast_result,
        rag_result
    )

    return {
        "analysis": analysis_result,
        "forecast": forecast_result,
        "scenario": scenario_result,
        "rag": rag_result,
        "decision": decision
    }