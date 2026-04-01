from __future__ import annotations

from pathlib import Path
import os

import numpy as np
import pandas as pd

# Handle both local and Streamlit cloud deployments
def get_data_path():
    # Try multiple path resolution strategies
    
    # Strategy 1: From __file__ (works in local development)
    try:
        script_dir = Path(__file__).resolve().parent
        deployment_dir = script_dir.parent
        repo_dir = deployment_dir.parent
        
        if (repo_dir / "dataset" / "HR_Attrition.csv").exists():
            return repo_dir / "dataset" / "HR_Attrition.csv"
    except:
        pass
    
    # Strategy 2: From environment/working directory (works in Streamlit cloud)
    cwd = Path.cwd()
    if (cwd / "dataset" / "HR_Attrition.csv").exists():
        return cwd / "dataset" / "HR_Attrition.csv"
    
    # Strategy 3: Check if running from deployment directory
    if (cwd / ".." / "dataset" / "HR_Attrition.csv").exists():
        return (cwd / ".." / "dataset" / "HR_Attrition.csv").resolve()
    
    # Fallback: assume standard structure
    return Path(__file__).resolve().parent.parent.parent / "dataset" / "HR_Attrition.csv"

DATA_PATH = get_data_path()
ROOT_DIR = DATA_PATH.parent.parent

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
    if not Path(path).exists():
        raise FileNotFoundError(f"Dataset not found at {path}. Looking in: {Path(path).resolve()}")
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
