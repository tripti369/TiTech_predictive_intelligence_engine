"""
Agents Package
==============
Exposes the core predictive intelligence agents:
- AnalysisAgent: Data exploration, descriptive statistics, outlier & correlation analysis
- ForecastingAgent: Time series prediction (Holt-Winters and moving average models)
- ScenarioAgent: Monte Carlo and best/base/worst scenario simulation
- RAGAgent: Knowledge retrieval using vector database and local documents
- DecisionAgent: Executive synthesis and risk-graded recommendations
"""

from .analysis_agent import AnalysisAgent
from .forecasting_agent import ForecastingAgent
from .scenario_agent import ScenarioAgent
from .rag_agent import RAGAgent
from .decision_agent import DecisionAgent

__all__ = [
    "AnalysisAgent",
    "ForecastingAgent",
    "ScenarioAgent",
    "RAGAgent",
    "DecisionAgent",
]
