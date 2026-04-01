from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT_DIR / "dataset" / "HR_Attrition.csv"

DROP_COLUMNS = [
    "Random Number",
    "EmployeeCount",
    "Over18",
    "StandardHours",
]

CATEGORY_ORDERS = {
    "AgeGroup": ["18-25", "26-35", "36-45", "46-55", "56-65"],
    "TenureGroup": ["<=1 year", "2-3 years", "4-5 years", "6-10 years", "10+ years"],
    "IncomeGroup": ["Low", "Mid", "High"],
    "SalaryHikeGroup": ["Low Hike", "Mid Hike", "High Hike"],
    "JobInvolvement": [1, 2, 3, 4],
    "EnvironmentSatisfaction": [1, 2, 3, 4],
    "JobSatisfaction": [1, 2, 3, 4],
    "RelationshipSatisfaction": [1, 2, 3, 4],
    "WorkLifeBalance": [1, 2, 3, 4],
    "StockOptionLevel": [0, 1, 2, 3],
    "PerformanceRating": [3, 4],
}


def load_attrition_data(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """Load the dataset and recreate the notebook's business-facing helper columns."""
    df = pd.read_csv(path).copy()
    df = df.drop(columns=DROP_COLUMNS, errors="ignore")

    df["Attrition Date"] = pd.to_datetime(
        df["Attrition Date"],
        format="%m/%d/%Y %I:%M:%S %p",
        errors="coerce",
    )
    df["AttritionFlag"] = df["Attrition"].eq("Yes")
    df["AttritionLabel"] = np.where(df["AttritionFlag"], "Exited Employees", "Active Employees")

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[17, 25, 35, 45, 55, 65],
        labels=CATEGORY_ORDERS["AgeGroup"],
    )
    df["TenureGroup"] = pd.cut(
        df["YearsAtCompany"],
        bins=[-1, 1, 3, 5, 10, 40],
        labels=CATEGORY_ORDERS["TenureGroup"],
    )
    df["IncomeGroup"] = pd.qcut(
        df["MonthlyIncome"],
        q=3,
        labels=CATEGORY_ORDERS["IncomeGroup"],
        duplicates="drop",
    )
    df["SalaryHikeGroup"] = pd.qcut(
        df["PercentSalaryHike"],
        q=3,
        labels=CATEGORY_ORDERS["SalaryHikeGroup"],
        duplicates="drop",
    )
    df["StockOptionBand"] = np.where(df["StockOptionLevel"].eq(0), "No stock option", "Has stock option")
    df["TravelIntensity"] = df["BusinessTravel"].replace(
        {
            "Travel_Frequently": "Frequent travel",
            "Travel_Rarely": "Travel rarely",
            "Non-Travel": "Non-travel",
        }
    )

    for column, order in CATEGORY_ORDERS.items():
        if column in df.columns:
            df[column] = pd.Categorical(df[column], categories=order, ordered=True)

    return df
