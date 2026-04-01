from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, mannwhitneyu

from .data import CATEGORY_ORDERS

RECOMMENDATIONS = [
    {
        "title": "Prioritize the first 1-3 years of employment",
        "why": (
            "Attrition is concentrated among younger, lower-tenure employees, so onboarding, buddy support, "
            "and structured 3/6/12-month check-ins are the most direct retention lever."
        ),
    },
    {
        "title": "Audit high-risk roles instead of broad departments",
        "why": (
            "The notebook shows much sharper separation at the job-role level, especially for Sales Representative, "
            "Laboratory Technician, and Human Resources."
        ),
    },
    {
        "title": "Reduce chronic overtime and travel strain",
        "why": (
            "OverTime and BusinessTravel are among the clearest workload signals, pointing to work rhythm and mobility "
            "as a practical source of attrition pressure."
        ),
    },
    {
        "title": "Strengthen value for lower-income and lower-level employees",
        "why": (
            "MonthlyIncome and StockOptionLevel matter more than PercentSalaryHike, so the value proposition should go "
            "beyond routine annual salary increases."
        ),
    },
    {
        "title": "Use experience scores as early warning signals",
        "why": (
            "Lower WorkLifeBalance, EnvironmentSatisfaction, JobSatisfaction, and JobInvolvement tend to show up more often "
            "among employees who leave."
        ),
    },
]

STORYLINE_POINTS = [
    "Attrition is concentrated in the early-career stage rather than spread evenly across the workforce.",
    "Role design and workload pressure matter more than formal performance scores.",
    "Compensation value and day-to-day work experience reinforce the attrition pattern.",
]

WEAK_SIGNALS = [
    "Education",
    "Gender",
    "HourlyRate",
    "MonthlyRate",
    "PercentSalaryHike",
    "PerformanceRating",
    "RelationshipSatisfaction",
]

BUSINESS_INTERPRETATIONS = {
    "OverTime": "Employees working overtime leave far more often, making workload strain one of the clearest intervention points.",
    "JobRole": "Attrition varies sharply by role, so retention should be targeted below the department level.",
    "MaritalStatus": "Single employees show noticeably higher attrition, which aligns with the early-career mobility pattern.",
    "BusinessTravel": "Frequent travel is associated with higher attrition, likely because it adds routine disruption and fatigue.",
    "DistanceFromHome": "Longer commuting distance appears to add everyday friction that can compound attrition risk.",
    "EducationField": "Field of study adds context, but it is more supportive than central compared with role and workload variables.",
    "Department": "Department matters, but role-level analysis is much sharper and more actionable.",
    "TotalWorkingYears": "Attrition drops as employees become more established in their careers.",
    "MonthlyIncome": "Lower income is consistently associated with higher attrition, especially in earlier career stages.",
    "YearsAtCompany": "Employees are most vulnerable before they become fully established in the company.",
    "JobLevel": "Lower job levels face more attrition pressure than senior roles.",
    "YearsInCurrentRole": "Stability in role tenure is associated with lower attrition.",
    "YearsWithCurrManager": "Longer manager continuity tends to align with lower attrition.",
    "Age": "Younger employees are more likely to leave than older groups.",
    "StockOptionLevel": "The absence of stock options matters more than fine differences between higher stock-option levels.",
    "JobInvolvement": "Lower involvement scores point to weaker attachment and higher attrition risk.",
    "JobSatisfaction": "Lower satisfaction shows up more often among employees who leave.",
    "EnvironmentSatisfaction": "Lower environment satisfaction acts like an early warning signal.",
    "WorkLifeBalance": "Poor work-life balance is one of the clearest employee-experience warning signals.",
    "TrainingTimesLastYear": "Training appears supportive, but the pattern is uneven and not strong enough for a simple policy rule.",
    "YearsSinceLastPromotion": "Promotion timing has a weaker but still noticeable relationship with retention.",
    "DailyRate": "Daily rate is statistically detectable, but the practical signal is modest compared with broader compensation measures.",
}


def apply_filters(df: pd.DataFrame, filters: dict[str, list[str]]) -> pd.DataFrame:
    filtered = df.copy()

    if any(len(values) == 0 for values in filters.values()):
        return filtered.iloc[0:0].copy()

    if filters["departments"]:
        filtered = filtered[filtered["Department"].isin(filters["departments"])]
    if filters["job_roles"]:
        filtered = filtered[filtered["JobRole"].isin(filters["job_roles"])]
    if filters["marital_status"]:
        filtered = filtered[filtered["MaritalStatus"].isin(filters["marital_status"])]
    if filters["overtime"]:
        filtered = filtered[filtered["OverTime"].isin(filters["overtime"])]
    if filters["business_travel"]:
        filtered = filtered[filtered["BusinessTravel"].isin(filters["business_travel"])]

    return filtered


def compute_metrics(df: pd.DataFrame) -> dict[str, float]:
    total_employees = int(len(df))
    exited_employees = int(df["AttritionFlag"].sum())
    active_employees = total_employees - exited_employees
    attrition_rate = (exited_employees / total_employees * 100) if total_employees else 0.0

    early_stage = df[df["YearsAtCompany"] <= 3]
    early_stage_rate = (early_stage["AttritionFlag"].mean() * 100) if not early_stage.empty else 0.0

    overtime_yes = df[df["OverTime"] == "Yes"]["AttritionFlag"]
    overtime_no = df[df["OverTime"] == "No"]["AttritionFlag"]
    overtime_gap = 0.0
    if not overtime_yes.empty and not overtime_no.empty:
        overtime_gap = (overtime_yes.mean() - overtime_no.mean()) * 100

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "exited_employees": exited_employees,
        "attrition_rate": attrition_rate,
        "early_stage_rate": early_stage_rate,
        "overtime_gap": overtime_gap,
    }


def compute_attrition_table(
    df: pd.DataFrame,
    column: str,
    *,
    keep_order: bool = False,
) -> pd.DataFrame:
    grouped = (
        df.groupby(column, dropna=False)
        .agg(
            total_employees=("AttritionFlag", "size"),
            exited_employees=("AttritionFlag", "sum"),
        )
        .reset_index()
        .rename(columns={column: "category"})
    )
    grouped = grouped[grouped["category"].notna()].copy()
    grouped["active_employees"] = grouped["total_employees"] - grouped["exited_employees"]
    grouped["attrition_rate"] = grouped["exited_employees"] / grouped["total_employees"] * 100

    if keep_order and column in CATEGORY_ORDERS:
        grouped["category"] = pd.Categorical(
            grouped["category"],
            categories=CATEGORY_ORDERS[column],
            ordered=True,
        )
        grouped = grouped.sort_values("category")
        grouped["category"] = grouped["category"].astype(str)
    else:
        grouped = grouped.sort_values("attrition_rate", ascending=False)

    return grouped.reset_index(drop=True)


def compute_monthly_exits(df: pd.DataFrame) -> pd.DataFrame:
    exited = df[df["AttritionFlag"] & df["Attrition Date"].notna()].copy()
    if exited.empty:
        return pd.DataFrame(columns=["month", "exits"])

    exited["month"] = exited["Attrition Date"].dt.to_period("M").dt.to_timestamp()
    monthly = exited.groupby("month").size().reset_index(name="exits")
    return monthly


def compute_recent_exits(
    df: pd.DataFrame,
    *,
    start_date: pd.Timestamp | None = None,
    end_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    available = df.copy()

    if "EmployeeNumber" not in available.columns:
        available["EmployeeNumber"] = pd.NA

    recent = available[available["AttritionFlag"] & available["Attrition Date"].notna()].copy()

    if start_date is not None:
        recent = recent[recent["Attrition Date"] >= pd.Timestamp(start_date)]
    if end_date is not None:
        recent = recent[recent["Attrition Date"] <= pd.Timestamp(end_date)]

    recent = (
        recent.sort_values("Attrition Date", ascending=False)
        .loc[:, ["EmployeeNumber", "JobRole", "MonthlyIncome", "Attrition Date"]]
        .copy()
    )
    return recent


def _cramers_v(confusion_matrix: pd.DataFrame) -> float:
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.to_numpy().sum()
    rows, cols = confusion_matrix.shape
    return float(np.sqrt(chi2 / (n * min(rows - 1, cols - 1))))


def _rank_biserial(series_yes: pd.Series, series_no: pd.Series) -> tuple[float, float]:
    u_stat, p_value = mannwhitneyu(series_yes, series_no, alternative="two-sided")
    effect = (2 * u_stat) / (len(series_yes) * len(series_no)) - 1
    return float(p_value), float(effect)


def effect_strength_label(effect_size: float) -> str:
    magnitude = abs(effect_size)
    if magnitude >= 0.2:
        return "Strong signal"
    if magnitude >= 0.1:
        return "Meaningful signal"
    return "Supporting signal"


def compute_statistical_results(df: pd.DataFrame) -> pd.DataFrame:
    analysis_df = df.drop(
        columns=[
            "Attrition Date",
            "AttritionFlag",
            "AttritionLabel",
            "AgeGroup",
            "TenureGroup",
            "IncomeGroup",
            "SalaryHikeGroup",
            "StockOptionBand",
            "TravelIntensity",
            "EmployeeNumber",
        ],
        errors="ignore",
    )

    results: list[dict[str, Any]] = []
    target = "Attrition"

    for column in analysis_df.columns:
        if column == target:
            continue

        if pd.api.types.is_numeric_dtype(analysis_df[column]):
            yes = analysis_df.loc[analysis_df[target] == "Yes", column]
            no = analysis_df.loc[analysis_df[target] == "No", column]
            p_value, effect_size = _rank_biserial(yes, no)
            test_name = "Mann-Whitney U"
            effect_test = "Rank-biserial"
        else:
            contingency = pd.crosstab(analysis_df[column], analysis_df[target])
            _, p_value, _, _ = chi2_contingency(contingency)
            effect_size = _cramers_v(contingency)
            test_name = "Chi-square"
            effect_test = "Cramer's V"

        results.append(
            {
                "Feature": column,
                "Data Type": "numeric" if pd.api.types.is_numeric_dtype(analysis_df[column]) else "categorical",
                "Test": test_name,
                "p-value": p_value,
                "Effect Size Test": effect_test,
                "Effect Size": effect_size,
            }
        )

    stats = pd.DataFrame(results)
    stats["Significant"] = stats["p-value"] < 0.05
    stats["Direction"] = np.where(
        stats["Effect Size"] >= 0,
        "Higher attrition when this factor is more present",
        "Lower attrition as employees become more established on this factor",
    )
    stats["Effect Magnitude"] = stats["Effect Size"].abs()
    stats["Signal Strength"] = stats["Effect Size"].apply(effect_strength_label)
    stats["Business Meaning"] = stats["Feature"].map(BUSINESS_INTERPRETATIONS).fillna(
        "This variable helps separate who leaves from who stays, but it is not one of the central drivers."
    )

    return stats.sort_values(["Significant", "Effect Magnitude"], ascending=[False, False]).reset_index(drop=True)


def build_statistical_highlights(stats: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    significant = stats[stats["Significant"]].copy()
    highlight = significant.sort_values("Effect Magnitude", ascending=False).head(limit).copy()
    highlight["Effect Size"] = highlight["Effect Size"].round(3)
    return highlight[
        [
            "Feature",
            "Effect Size",
            "Signal Strength",
            "Direction",
            "Business Meaning",
        ]
    ]


def build_filter_summary(filters: dict[str, list[str]]) -> list[str]:
    summary: list[str] = []

    if filters["departments"]:
        summary.append(f"Departments: {', '.join(filters['departments'])}")
    if filters["job_roles"]:
        summary.append(f"Job roles: {', '.join(filters['job_roles'])}")
    if filters["marital_status"]:
        summary.append(f"Marital status: {', '.join(filters['marital_status'])}")
    if filters["overtime"]:
        summary.append(f"Overtime: {', '.join(filters['overtime'])}")
    if filters["business_travel"]:
        summary.append(f"Business travel: {', '.join(filters['business_travel'])}")

    return summary
