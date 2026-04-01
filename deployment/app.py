from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.analysis import (
    RECOMMENDATIONS,
    STORYLINE_POINTS,
    WEAK_SIGNALS,
    apply_filters,
    build_filter_summary,
    build_statistical_highlights,
    compute_attrition_table,
    compute_metrics,
    compute_monthly_exits,
    compute_recent_exits,
    compute_statistical_results,
)
from src.charts import (
    make_attrition_rate_chart,
    make_effect_size_chart,
    make_income_boxplot,
    make_monthly_exit_chart,
)
from src.data import load_attrition_data

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def get_base_data():
    data_version = "employee-number-enabled-v2"
    return load_attrition_data(), data_version


@st.cache_data
def get_statistical_results():
    base_df, _ = get_base_data()
    return compute_statistical_results(base_df)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #f3efe5 0%, #f7f5ef 100%);
            }
            .hero-card {
                background: linear-gradient(135deg, rgba(214,140,69,0.14), rgba(108,142,173,0.08));
                border: 1px solid rgba(31,42,54,0.08);
                padding: 1.5rem 1.6rem;
                border-radius: 18px;
                margin-bottom: 1rem;
            }
            .hero-title {
                font-size: 2rem;
                line-height: 1.15;
                color: #1f2a36;
                margin-bottom: 0.45rem;
                font-weight: 700;
            }
            .hero-text {
                color: #43515d;
                font-size: 1rem;
                margin-bottom: 0;
            }
            .section-card {
                background: rgba(252, 251, 248, 0.92);
                border: 1px solid rgba(31,42,54,0.08);
                border-radius: 18px;
                padding: 1rem 1.1rem;
                margin-bottom: 1rem;
            }
            .insight-card {
                background: rgba(255,255,255,0.72);
                border-left: 4px solid #d68c45;
                padding: 0.9rem 1rem;
                border-radius: 12px;
                margin-bottom: 0.7rem;
            }
            .recommendation-card {
                background: rgba(255,255,255,0.78);
                border: 1px solid rgba(31,42,54,0.08);
                padding: 1rem;
                border-radius: 14px;
                min-height: 180px;
            }
            .recommendation-title {
                color: #1f2a36;
                font-weight: 700;
                margin-bottom: 0.35rem;
            }
            .muted-note {
                color: #5f6b76;
                font-size: 0.95rem;
            }
            div[data-testid="stMetricValue"] {
                color: #1f2a36;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(base_df):
    st.sidebar.title("Dashboard Controls")
    st.sidebar.caption(
        "Filters below redefine the workforce scope. The statistical section stays anchored to the full notebook analysis."
    )

    departments = sorted(base_df["Department"].dropna().unique().tolist())
    selected_departments = st.sidebar.multiselect("Department", departments, default=departments)

    job_role_pool = base_df[base_df["Department"].isin(selected_departments)] if selected_departments else base_df
    job_roles = sorted(job_role_pool["JobRole"].dropna().unique().tolist())
    selected_job_roles = st.sidebar.multiselect("Job Role", job_roles, default=job_roles)

    marital_status = sorted(base_df["MaritalStatus"].dropna().unique().tolist())
    selected_marital = st.sidebar.multiselect("Marital Status", marital_status, default=marital_status)

    overtime = sorted(base_df["OverTime"].dropna().unique().tolist())
    selected_overtime = st.sidebar.multiselect("OverTime", overtime, default=overtime)

    business_travel = sorted(base_df["BusinessTravel"].dropna().unique().tolist())
    selected_travel = st.sidebar.multiselect("Business Travel", business_travel, default=business_travel)

    filters = {
        "departments": selected_departments,
        "job_roles": selected_job_roles,
        "marital_status": selected_marital,
        "overtime": selected_overtime,
        "business_travel": selected_travel,
    }

    summary_filters = {
        "departments": selected_departments if len(selected_departments) != len(departments) else [],
        "job_roles": selected_job_roles if len(selected_job_roles) != len(job_roles) else [],
        "marital_status": selected_marital if len(selected_marital) != len(marital_status) else [],
        "overtime": selected_overtime if len(selected_overtime) != len(overtime) else [],
        "business_travel": selected_travel if len(selected_travel) != len(business_travel) else [],
    }

    summary = build_filter_summary(summary_filters)
    if summary:
        st.sidebar.markdown("**Current scope**")
        for item in summary:
            st.sidebar.caption(item)

    return filters


def render_story_cards():
    st.markdown("### Executive Overview")
    cols = st.columns(3)
    for column, text in zip(cols, STORYLINE_POINTS):
        with column:
            st.markdown(
                f"""
                <div class="insight-card">
                    <strong>{text}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )


def main():
    inject_styles()

    base_df, _ = get_base_data()
    stats_df = get_statistical_results()

    filters = render_sidebar(base_df)
    population_df = apply_filters(base_df, filters)

    if population_df.empty:
        st.warning("No employees match the current filter combination. Try widening the sidebar filters.")
        st.stop()

    baseline_metrics = compute_metrics(base_df)
    current_metrics = compute_metrics(population_df)

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">Employee Attrition Risk Dashboard</div>
            <p class="hero-text">
                A portfolio dashboard built directly from the notebook storyline: where attrition concentrates,
                which work conditions stand out, and which business actions matter most.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if len(population_df) != len(base_df):
        st.caption(
            f"Current filters keep {len(population_df):,} of {len(base_df):,} employees in scope."
        )

    metric_cols = st.columns(5)
    metric_cols[0].metric("Active employees", f"{current_metrics['active_employees']:,}")
    metric_cols[1].metric("Exited employees", f"{current_metrics['exited_employees']:,}")
    metric_cols[2].metric(
        "Attrition rate",
        f"{current_metrics['attrition_rate']:.1f}%",
        delta=f"{current_metrics['attrition_rate'] - baseline_metrics['attrition_rate']:+.1f} pts vs company",
    )
    metric_cols[3].metric("Early-tenure attrition", f"{current_metrics['early_stage_rate']:.1f}%")
    metric_cols[4].metric("Overtime risk gap", f"{current_metrics['overtime_gap']:.1f} pts")

    render_story_cards()

    overview_chart_col, overview_table_col = st.columns([1.2, 0.9])

    with overview_chart_col:
        st.markdown("#### Observed Exit Pattern")
        monthly_exits = compute_monthly_exits(population_df)
        if monthly_exits.empty:
            st.info("No recorded attrition dates are available for the current scope.")
        else:
            st.plotly_chart(
                make_monthly_exit_chart(monthly_exits),
                use_container_width=True,
            )
            st.caption(
                "Read this as an observed exit pattern, not as a formal monthly attrition rate. The notebook also notes that the final month may be incomplete."
            )

    with overview_table_col:
        st.markdown("#### Recent Exit")
        dated_exits = population_df[
            population_df["AttritionFlag"] & population_df["Attrition Date"].notna()
        ].copy()

        if dated_exits.empty:
            st.info("No recent exit records are available for the current scope.")
        else:
            min_exit_date = dated_exits["Attrition Date"].min().date()
            max_exit_date = dated_exits["Attrition Date"].max().date()

            date_col1, date_col2 = st.columns(2)
            with date_col1:
                start_date = st.date_input(
                    "From",
                    value=min_exit_date,
                    min_value=min_exit_date,
                    max_value=max_exit_date,
                    key="recent_exit_start",
                )
            with date_col2:
                end_date = st.date_input(
                    "To",
                    value=max_exit_date,
                    min_value=min_exit_date,
                    max_value=max_exit_date,
                    key="recent_exit_end",
                )

            if start_date > end_date:
                st.warning("Start date must be on or before end date.")
            else:
                recent_exits = compute_recent_exits(
                    population_df,
                    start_date=start_date,
                    end_date=end_date,
                )

                if recent_exits.empty:
                    st.info("No exit records fall inside the selected date range.")
                else:
                    st.dataframe(
                        recent_exits,
                        use_container_width=True,
                        hide_index=True,
                        height=520,
                        column_config={
                            "EmployeeNumber": st.column_config.NumberColumn("EmployeeNumber", format="%d"),
                            "JobRole": st.column_config.TextColumn("JobRole"),
                            "MonthlyIncome": st.column_config.NumberColumn("Monthly Income", format="$%d"),
                            "Attrition Date": st.column_config.DateColumn("Attrition Date", format="D MMM YYYY"),
                        },
                    )

    st.markdown("### Attrition Profile")
    profile_tabs = st.tabs(["Demographics", "Career stage", "Org structure"])

    with profile_tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                make_attrition_rate_chart(
                    compute_attrition_table(population_df, "AgeGroup", keep_order=True),
                    "Attrition by age group",
                    baseline_metrics["attrition_rate"],
                ),
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(
                make_attrition_rate_chart(
                    compute_attrition_table(population_df, "MaritalStatus"),
                    "Attrition by marital status",
                    baseline_metrics["attrition_rate"],
                ),
                use_container_width=True,
            )
        st.caption(
            "Notebook takeaway: younger and single employees stand out much more clearly than gender, reinforcing the early-career mobility story."
        )

    with profile_tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                make_attrition_rate_chart(
                    compute_attrition_table(population_df, "TenureGroup", keep_order=True),
                    "Attrition by years at company",
                    baseline_metrics["attrition_rate"],
                ),
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(
                make_attrition_rate_chart(
                    compute_attrition_table(population_df, "JobLevel", keep_order=True),
                    "Attrition by job level",
                    baseline_metrics["attrition_rate"],
                ),
                use_container_width=True,
            )
        st.caption(
            "The notebook's central pattern is that attrition drops as employees become more established in role, tenure, and seniority."
        )

    with profile_tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(
                make_attrition_rate_chart(
                    compute_attrition_table(population_df, "Department"),
                    "Attrition by department",
                    baseline_metrics["attrition_rate"],
                ),
                use_container_width=True,
            )
        with col2:
            st.plotly_chart(
                make_attrition_rate_chart(
                    compute_attrition_table(population_df, "JobRole"),
                    "Attrition by job role",
                    baseline_metrics["attrition_rate"],
                ),
                use_container_width=True,
            )
        st.caption(
            "Role-level separation is much sharper than department-level separation, so role design is the more actionable lens."
        )

    st.markdown("### Work Conditions and Experience")
    work_col, experience_col = st.columns(2)

    with work_col:
        work_factor = st.selectbox(
            "Work pattern factor",
            ["OverTime", "BusinessTravel", "JobInvolvement"],
            index=0,
        )
        st.plotly_chart(
            make_attrition_rate_chart(
                compute_attrition_table(
                    population_df,
                    work_factor,
                    keep_order=work_factor == "JobInvolvement",
                ),
                f"Attrition by {work_factor}",
                baseline_metrics["attrition_rate"],
            ),
            use_container_width=True,
        )
        if work_factor == "OverTime":
            st.caption("This is one of the strongest gaps in the notebook, with overtime employees leaving at roughly three times the rate of non-overtime employees.")
        elif work_factor == "BusinessTravel":
            st.caption("Frequent travel is associated with noticeably higher attrition, suggesting routine disruption and fatigue matter.")
        else:
            st.caption("Lower job involvement aligns with higher attrition, making it a useful early warning signal rather than a late-stage outcome.")

    with experience_col:
        experience_factor = st.selectbox(
            "Employee experience factor",
            ["WorkLifeBalance", "EnvironmentSatisfaction", "JobSatisfaction"],
            index=0,
        )
        st.plotly_chart(
            make_attrition_rate_chart(
                compute_attrition_table(population_df, experience_factor, keep_order=True),
                f"Attrition by {experience_factor}",
                baseline_metrics["attrition_rate"],
            ),
            use_container_width=True,
        )
        if experience_factor == "WorkLifeBalance":
            st.caption("Work-life balance is the clearest experience-side warning signal in the notebook.")
        elif experience_factor == "EnvironmentSatisfaction":
            st.caption("Employees who leave tend to report a less positive work environment, even if the distributions still overlap.")
        else:
            st.caption("Job satisfaction does not explain attrition on its own, but it consistently moves in the same direction as the broader risk pattern.")

    st.info(
        "Notebook caution: PerformanceRating is not emphasized here because the score only takes values 3 and 4 in the dataset. That compressed scale weakens its analytical value."
    )

    st.markdown("### Compensation and Benefits")
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        st.plotly_chart(
            make_attrition_rate_chart(
                compute_attrition_table(population_df, "IncomeGroup", keep_order=True),
                "Attrition by income group",
                baseline_metrics["attrition_rate"],
            ),
            use_container_width=True,
        )
    with comp_col2:
        st.plotly_chart(
            make_income_boxplot(population_df),
            use_container_width=True,
        )

    comp_col3, comp_col4 = st.columns(2)
    with comp_col3:
        st.plotly_chart(
            make_attrition_rate_chart(
                compute_attrition_table(population_df, "StockOptionLevel", keep_order=True),
                "Attrition by stock option level",
                baseline_metrics["attrition_rate"],
            ),
            use_container_width=True,
        )
    with comp_col4:
        st.plotly_chart(
            make_attrition_rate_chart(
                compute_attrition_table(population_df, "SalaryHikeGroup", keep_order=True),
                "Attrition by salary hike group",
                baseline_metrics["attrition_rate"],
            ),
            use_container_width=True,
        )

    st.caption(
        "Notebook takeaway: lower income and no stock options carry a clearer attrition signal than annual salary hike percentage. Stock option level 3 should be read carefully because the group is small and composition-sensitive."
    )

    st.markdown("### Statistical Insights")
    st.caption("This section is based on the full notebook analysis and does not change with the sidebar filters.")

    stat_metric_cols = st.columns(3)
    significant_total = int(stats_df["Significant"].sum())
    stat_metric_cols[0].metric("Significant variables", f"{significant_total} / {len(stats_df)}")
    stat_metric_cols[1].metric(
        "Top workload factor",
        "OverTime",
    )
    stat_metric_cols[2].metric("Top stabilizers", "Tenure and income")

    stat_left, stat_right = st.columns([1.05, 1])
    with stat_left:
        st.plotly_chart(
            make_effect_size_chart(stats_df),
            use_container_width=True,
        )
    with stat_right:
        highlights = build_statistical_highlights(stats_df)
        st.dataframe(
            highlights,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Feature": st.column_config.TextColumn("Feature"),
                "Effect Size": st.column_config.NumberColumn("Effect Size", format="%.3f"),
                "Signal Strength": st.column_config.TextColumn("Signal strength"),
                "Direction": st.column_config.TextColumn("Business direction"),
                "Business Meaning": st.column_config.TextColumn("Why it matters"),
            },
        )

    st.caption(
        "Muted or low-value signals in the notebook include "
        + ", ".join(WEAK_SIGNALS)
        + ". They are intentionally not overemphasized in the dashboard."
    )

    st.markdown("### Recommendations")
    recommendation_cols = st.columns(3)
    for index, recommendation in enumerate(RECOMMENDATIONS):
        with recommendation_cols[index % 3]:
            st.markdown(
                f"""
                <div class="recommendation-card">
                    <div class="recommendation-title">{recommendation['title']}</div>
                    <div class="muted-note">{recommendation['why']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
