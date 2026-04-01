from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

ACTIVE_COLOR = "#6C8EAD"
EXITED_COLOR = "#C75A5A"
ACCENT_COLOR = "#D68C45"
TEXT_COLOR = "#1F2A36"
GRID_COLOR = "#D9E2EC"
PLOT_BG = "#FCFBF8"


def apply_chart_theme(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=TEXT_COLOR, family="Arial"),
        margin=dict(l=16, r=16, t=56, b=16),
        hoverlabel=dict(bgcolor="white", font=dict(color=TEXT_COLOR)),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor=GRID_COLOR, zeroline=False)
    return fig


def make_attrition_rate_chart(
    table: pd.DataFrame,
    title: str,
    baseline_rate: float,
    *,
    category_title: str = "",
) -> go.Figure:
    color_map = [
        EXITED_COLOR if value >= baseline_rate else ACTIVE_COLOR
        for value in table["attrition_rate"]
    ]

    fig = go.Figure()
    fig.add_bar(
        x=table["category"],
        y=table["attrition_rate"],
        marker_color=color_map,
        customdata=table[["exited_employees", "total_employees"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Attrition rate: %{y:.1f}%<br>"
            "Exited employees: %{customdata[0]}<br>"
            "Total employees: %{customdata[1]}<extra></extra>"
        ),
    )
    fig.add_hline(
        y=baseline_rate,
        line_dash="dash",
        line_color=ACCENT_COLOR,
        annotation_text=f"Baseline {baseline_rate:.1f}%",
        annotation_position="top right",
    )
    fig.update_layout(
        title=title,
        xaxis_title=category_title,
        yaxis_title="Attrition rate (%)",
        yaxis_range=[0, max(40, table["attrition_rate"].max() * 1.2 if not table.empty else 40)],
        showlegend=False,
    )
    return apply_chart_theme(fig)


def make_monthly_exit_chart(monthly: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=monthly["month"],
            y=monthly["exits"],
            mode="lines+markers",
            line=dict(color=ACCENT_COLOR, width=3),
            marker=dict(size=8, color=EXITED_COLOR),
            hovertemplate="%{x|%b %Y}<br>Recorded exits: %{y}<extra></extra>",
        )
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Recorded exits",
        showlegend=False,
    )
    return apply_chart_theme(fig)


def make_income_boxplot(df: pd.DataFrame) -> go.Figure:
    fig = px.box(
        df,
        x="AttritionLabel",
        y="MonthlyIncome",
        color="AttritionLabel",
        color_discrete_map={
            "Active Employees": ACTIVE_COLOR,
            "Exited Employees": EXITED_COLOR,
        },
        points=False,
        title="Monthly income distribution by employee status",
    )
    fig.update_layout(
        xaxis_title="Employee status",
        yaxis_title="Monthly income",
        showlegend=False,
    )
    return apply_chart_theme(fig)


def make_effect_size_chart(stats: pd.DataFrame, limit: int = 12) -> go.Figure:
    chart_df = stats[stats["Significant"]].copy().sort_values("Effect Magnitude", ascending=True).tail(limit)
    color_map = chart_df["Effect Size"].apply(lambda value: EXITED_COLOR if value >= 0 else ACTIVE_COLOR)

    fig = go.Figure()
    fig.add_bar(
        x=chart_df["Effect Size"],
        y=chart_df["Feature"],
        orientation="h",
        marker_color=color_map,
        customdata=chart_df[["Signal Strength"]],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Effect size: %{x:.3f}<br>"
            "Interpretation: %{customdata[0]}<extra></extra>"
        ),
    )
    fig.add_vline(x=0, line_color=ACCENT_COLOR, line_width=1.5)
    fig.update_layout(
        title="Most visible statistical signals from the notebook",
        xaxis_title="Effect size",
        yaxis_title="Feature",
        showlegend=False,
    )
    return apply_chart_theme(fig)
