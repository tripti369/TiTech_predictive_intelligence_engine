"""
/api/predict
============
The main dashboard and prediction endpoint. Runs the Analysis, Forecasting, RAG and
Decision agents together on real CSV datasets and returns everything the frontend
dashboard and test suites need. Supports both GET and POST.
"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
import numpy as np
import pandas as pd

from app.database import get_db
from app import models
from app.agents.analysis_agent import AnalysisAgent
from app.agents.forecasting_agent import ForecastingAgent
from app.agents.rag_agent import RAGAgent
from app.agents.decision_agent import DecisionAgent
from app.utils import DATA_DIR, load_csv

router = APIRouter()

analysis_agent = AnalysisAgent()
forecasting_agent = ForecastingAgent()
rag_agent = RAGAgent()
decision_agent = DecisionAgent()


def _detect_dataset_type(df: pd.DataFrame) -> str:
    cols = set(df.columns.str.lower())
    if "churn" in cols or "subscription_type" in cols:
        return "churn"
    if "leaveornot" in cols or "joiningyear" in cols:
        return "hr"
    if "retail_sales" in cols or "warehouse_sales" in cols:
        return "retail"
    if "year" in cols and "month" in cols:
        return "timeseries"
    return "generic"


def _build_timeseries(df: pd.DataFrame, filename: str, target_col: str = None):
    """Return (series, labels, col_name) for any dataset, with graceful fallback."""
    cols = df.columns.str.lower()
    df.columns = cols
    if "year" in cols and "month" in cols:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        val_col = (
            target_col.lower()
            if target_col and target_col.lower() in numeric_cols
            else next(
                (c for c in numeric_cols if c not in ("year", "month")),
                numeric_cols[0] if numeric_cols else None,
            )
        )
        if val_col:
            monthly = (
                df.groupby(["year", "month"])[val_col]
                .sum()
                .reset_index()
                .sort_values(["year", "month"])
            )
            monthly["date"] = pd.to_datetime(
                monthly["year"].astype(str)
                + "-"
                + monthly["month"].astype(str).str.zfill(2)
            )
            series = monthly.set_index("date")[val_col]
            labels = monthly["date"].dt.strftime("%Y-%m").tolist()
            return series, labels, val_col

    # Fallback for non-monthly / other structured datasets
    numeric_df = df.select_dtypes(include=[np.number])
    if target_col and target_col.lower() in numeric_df.columns:
        num = numeric_df[target_col.lower()]
    elif not numeric_df.empty:
        num = numeric_df.iloc[:, 0]
    else:
        num = pd.Series([100.0, 115.0, 125.0, 140.0])

    series = num.head(48).reset_index(drop=True)
    labels = [f"T{i+1}" for i in range(len(series))]
    return series, labels, num.name or "value"


_DEFAULT_PREDICT_CACHE = None


def _execute_predict(
    dataset: str = None,
    target_column: str = None,
    forecast_periods: int = 6,
    db: Session = None,
):
    global _DEFAULT_PREDICT_CACHE
    is_default = (not dataset and not target_column and (forecast_periods in (None, 6)))
    if is_default and _DEFAULT_PREDICT_CACHE is not None:
        return _DEFAULT_PREDICT_CACHE

    if dataset:
        try:
            df_main = load_csv(dataset)
            ds_type = _detect_dataset_type(df_main)
        except Exception:
            df_main = None
            ds_type = "all"
    else:
        df_main = None
        ds_type = "all"

    # ---- Revenue / time-series ------------------------------------------
    if ds_type in ("retail", "timeseries", "generic") and df_main is not None:
        try:
            series, labels, value_col = _build_timeseries(
                df_main, dataset, target_column
            )
        except Exception:
            num = df_main.select_dtypes(include=[np.number]).iloc[:, 0]
            series = num.reset_index(drop=True)
            labels = [str(i) for i in range(len(series))]
    else:
        retail = load_csv("retail_warehouse_sales_cleaned.csv")
        retail.columns = retail.columns.str.lower()
        retail["total_sales"] = retail["retail_sales"].fillna(0) + retail[
            "warehouse_sales"
        ].fillna(0)
        monthly = (
            retail.groupby(["year", "month"])["total_sales"]
            .sum()
            .reset_index()
            .sort_values(["year", "month"])
        )
        monthly["date"] = pd.to_datetime(
            monthly["year"].astype(str)
            + "-"
            + monthly["month"].astype(str).str.zfill(2)
        )
        series = monthly.set_index("date")["total_sales"]
        labels = monthly["date"].dt.strftime("%Y-%m").tolist()

    periods = forecast_periods if forecast_periods and forecast_periods > 0 else 6
    forecast_result = forecasting_agent.forecast_series(
        series, forecast_periods=periods, seasonal_periods=12
    )

    first_val = float(series.iloc[0]) if len(series) > 0 else 1.0
    last_val = float(series.iloc[-1]) if len(series) > 0 else 1.0
    growth_rate = round(
        ((last_val - first_val) / max(abs(first_val), 1.0)) * 100, 1
    )

    # ---- Churn ----------------------------------------------------------
    if ds_type == "churn" and df_main is not None:
        churn_df = df_main
    else:
        churn_df = load_csv("customer_churn_cleaned.csv")
    churn_df.columns = churn_df.columns.str.lower()

    churn_rate = (
        round(float(churn_df["churn"].mean()) * 100, 1)
        if "churn" in churn_df.columns
        else 0.0
    )
    avg_spend = (
        round(float(churn_df["total_spend"].mean()), 1)
        if "total_spend" in churn_df.columns
        else 0.0
    )
    avg_tenure = (
        round(float(churn_df["tenure"].mean()), 1)
        if "tenure" in churn_df.columns
        else 0.0
    )
    churn_by_sub = (
        churn_df.groupby("subscription_type")["churn"]
        .mean()
        .mul(100)
        .round(1)
        .to_dict()
        if "subscription_type" in churn_df.columns and "churn" in churn_df.columns
        else {}
    )

    # ---- Attrition ------------------------------------------------------
    if ds_type == "hr" and df_main is not None:
        emp_df = df_main
    else:
        emp_df = load_csv("employee_hr_cleaned.csv")
    emp_df.columns = emp_df.columns.str.lower()

    attrition_rate = (
        round(float(emp_df["leaveornot"].mean()) * 100, 1)
        if "leaveornot" in emp_df.columns
        else 0.0
    )
    attrition_by_city = (
        emp_df.groupby("city")["leaveornot"].mean().mul(100).round(1).to_dict()
        if "city" in emp_df.columns and "leaveornot" in emp_df.columns
        else {}
    )

    city_metrics = {}
    if "city" in emp_df.columns:
        grouped_city = emp_df.groupby("city")
        for city, city_df in grouped_city:
            city_metrics[str(city)] = {
                "attrition_rate": (
                    round(float(city_df["leaveornot"].mean()) * 100, 1)
                    if "leaveornot" in city_df.columns
                    else 0.0
                ),
                "employees": int(len(city_df)),
                "avg_tenure": (
                    round(float(city_df["experienceincurrentdomain"].mean()), 1)
                    if "experienceincurrentdomain" in city_df.columns
                    else 0.0
                ),
            }

    # ---- Analysis + RAG + Decision --------------------------------------
    analysis_result = analysis_agent.analyze_dataset(
        dataset or "customer_churn_cleaned.csv"
    )
    rag_agent.build_index(rebuild=False)
    rag_result = rag_agent.answer("business forecasting risk churn attrition")
    decision = decision_agent.generate_decision(
        forecast_accuracy=forecast_result["forecast_accuracy"],
        churn_rate=churn_rate,
        attrition_rate=attrition_rate,
        rag_result=rag_result,
    )

    # ---- Persist to DB --------------------------------------------------
    if db is not None:
        try:
            run = models.PredictionRun(
                forecast_accuracy=forecast_result["forecast_accuracy"],
                growth_rate=growth_rate,
                churn_rate=churn_rate,
                attrition_rate=attrition_rate,
                risk_level=decision["risk_level"],
            )
            db.add(run)
            db.commit()
        except Exception:
            pass

    forecast_payload = {
        "labels": [f"M+{i+1}" for i in range(len(forecast_result["forecast"]))],
        "values": forecast_result["forecast"],
        "model": forecast_result.get("model", "Adaptive Moving Average"),
        "forecast_accuracy": forecast_result["forecast_accuracy"],
        "mape": forecast_result.get("mape", 12.0),
    }

    revenue_values = [round(float(v), 2) for v in series.tolist()[-12:]]
    revenue_labels = labels[-len(revenue_values) :]

    return {
        "status": "success",
        "dataset": dataset or "(all defaults)",
        "forecast_accuracy": forecast_result["forecast_accuracy"],
        "growth_rate": growth_rate,
        "churn_rate": churn_rate,
        "attrition_rate": attrition_rate,
        "avg_spend": avg_spend,
        "avg_tenure": avg_tenure,
        "revenue": {
            "labels": revenue_labels,
            "values": revenue_values,
        },
        "forecast": forecast_payload,
        "churn_by_subscription": churn_by_sub,
        "attrition_by_city": attrition_by_city,
        "city_metrics": city_metrics,
        "analysis": analysis_result,
        "rag": rag_result,
        "decision": decision,
    }

    if is_default:
        _DEFAULT_PREDICT_CACHE = result

    return result


@router.get("/predict")
def predict_get(
    dataset: str = Query(
        None, description="CSV filename to analyse (auto-detects type)"
    ),
    db: Session = Depends(get_db),
):
    return _execute_predict(dataset=dataset, db=db)


@router.post("/predict")
async def predict_post(
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        body = await request.json()
    except Exception:
        body = {}

    dataset = (
        body.get("forecast_dataset")
        or body.get("analysis_dataset")
        or body.get("dataset")
    )
    target_col = body.get("target_column")
    periods = body.get("forecast_periods", 6)

    return _execute_predict(
        dataset=dataset,
        target_column=target_col,
        forecast_periods=periods,
        db=db,
    )
