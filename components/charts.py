"""
Chart Components - Plotly visualizations
Clean admin dashboard style
Palette:
- #BBE0EF
- #161E54
- #F16D34
- #FF986A
"""

import plotly.graph_objects as go
from nicegui import ui
import pandas as pd
import numpy as np


# ==============================================================================
# COLOR SYSTEM
# ==============================================================================

COLOR_PALETTE = {
    "light_blue": "#BBE0EF",
    "navy": "#161E54",
    "orange": "#F16D34",
    "light_orange": "#FF986A",

    "white": "#FFFFFF",
    "card_border": "rgba(22, 30, 84, 0.10)",
    "grid": "rgba(22, 30, 84, 0.08)",
    "text_dark": "#161E54",
    "text_muted": "rgba(22, 30, 84, 0.62)",
}


CHART_FONT = "Inter, Arial, sans-serif"


# ==============================================================================
# HELPERS
# ==============================================================================

def pretty_label(value):
    """Convert labels like LOW_RISK or reefer_truck into clean display labels."""
    if value is None:
        return ""

    text = str(value)

    mapping = {
        "LOW_RISK": "Low Risk",
        "MEDIUM_RISK": "Medium Risk",
        "HIGH_RISK": "High Risk",

        "NORMAL_MONITORING": "Normal Monitoring",
        "NEED_ATTENTION": "Need Attention",
        "MAINTENANCE_ALERT": "Maintenance Alert",

        "reefer_truck": "Reefer Truck",
        "articulated_truck": "Articulated Truck",
        "rigid_truck": "Rigid Truck",
        "brt_bus": "BRT Bus",
        "minibus": "Minibus",
        "van": "Van",
        "sedan": "Sedan",
        "motorcycle": "Motorcycle",

        "avg_risk_score": "Average Risk Score",
        "avg_record_risk_score": "Average Risk Score",
        "risk_level": "Risk Level",
        "vehicle_type": "Vehicle Type",
    }

    if text in mapping:
        return mapping[text]

    return text.replace("_", " ").replace("-", " ").title()


def _first_existing_column(df, candidates, fallback_index=0):
    """Return the first existing column from candidates, otherwise fallback by index."""
    for col in candidates:
        if col in df.columns:
            return col

    if len(df.columns) > fallback_index:
        return df.columns[fallback_index]

    return None


def _safe_max(series, default=1):
    try:
        value = float(series.max())
        if np.isnan(value) or value <= 0:
            return default
        return value
    except Exception:
        return default


def apply_premium_chart_style(
    fig,
    title=None,
    height=380,
    show_legend=False,
    margin=None,
):
    """Apply one consistent clean admin-dashboard style to Plotly charts."""

    if margin is None:
        margin = dict(l=48, r=32, t=46 if title else 24, b=46)

    fig.update_layout(
        title=dict(
            text=title or "",
            x=0.0,
            xanchor="left",
            font=dict(
                size=16,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
        ),
        height=height,
        margin=margin,
        template="plotly_white",

        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",

        font=dict(
            family=CHART_FONT,
            size=12,
            color=COLOR_PALETTE["text_muted"],
        ),

        showlegend=show_legend,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="left",
            x=0,
            font=dict(
                size=12,
                color=COLOR_PALETTE["text_muted"],
                family=CHART_FONT,
            ),
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0,
        ),

        hoverlabel=dict(
            bgcolor=COLOR_PALETTE["white"],
            bordercolor=COLOR_PALETTE["card_border"],
            font=dict(
                color=COLOR_PALETTE["text_dark"],
                size=12,
                family=CHART_FONT,
            ),
            namelength=-1,
        ),
    )

    fig.update_xaxes(
        title=None,
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(
            size=12,
            color=COLOR_PALETTE["text_muted"],
            family=CHART_FONT,
        ),
    )

    fig.update_yaxes(
        title=None,
        showgrid=True,
        gridwidth=1,
        gridcolor=COLOR_PALETTE["grid"],
        zeroline=False,
        showline=False,
        tickfont=dict(
            size=12,
            color=COLOR_PALETTE["text_muted"],
            family=CHART_FONT,
        ),
    )

    return fig


# ==============================================================================
# NICEGUI CARD RENDERERS
# ==============================================================================

def render_chart_card(title, fig, action_text=None, action=None, height=380):
    with ui.card().classes(
        "w-full rounded-[28px] bg-white border border-slate-100 "
        "shadow-[0_10px_30px_rgba(22,30,84,0.08)] overflow-hidden p-0"
    ):
        with ui.row().classes(
            "relative w-full items-center justify-end px-6 py-4 border-b border-slate-100"
        ):
            ui.label(title).classes(
                "absolute left-1/2 -translate-x-1/2 text-[18px] font-bold text-[#161E54]"
            )

            if action_text:
                ui.button(action_text, on_click=action).props(
                    "flat dense rounded"
                ).classes(
                    "text-[#161E54] bg-[#BBE0EF]/40 px-3 py-1 font-semibold"
                )
            else:
                ui.button(icon="more_horiz").props("flat round dense").classes(
                    "text-[#161E54]/50"
                )

        with ui.column().classes("w-full px-5 py-4"):
            return ui.plotly(fig).classes(f"w-full h-[{height}px]")
        
        
def render_plotly_chart(fig):
    """
    Backward-compatible renderer.
    Existing pages can keep using:
        charts.render_plotly_chart(fig)
    """
    return ui.plotly(fig).classes("w-full rounded-2xl")


# ==============================================================================
# OVERVIEW CHARTS
# ==============================================================================

def risk_distribution_chart(data):
    """
    Risk Level Distribution - Donut chart.
    Expected columns:
    - risk_level
    - count
    """

    if data is None or len(data) == 0:
        data = pd.DataFrame({
            "risk_level": ["LOW_RISK", "MEDIUM_RISK", "HIGH_RISK"],
            "count": [100, 50, 20],
        })

    df = data.copy()

    label_col = _first_existing_column(
        df,
        ["risk_level", "risk", "label", "level"],
        fallback_index=0,
    )
    value_col = _first_existing_column(
        df,
        ["count", "records", "total", "value"],
        fallback_index=1,
    )

    df["display_label"] = df[label_col].apply(pretty_label)

    risk_color_map = {
        "Low Risk": COLOR_PALETTE["light_blue"],
        "Medium Risk": COLOR_PALETTE["orange"],
        "High Risk": COLOR_PALETTE["navy"],
    }

    colors = [
        risk_color_map.get(label, COLOR_PALETTE["light_orange"])
        for label in df["display_label"]
    ]

    total = int(df[value_col].sum()) if value_col in df.columns else 0

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=df["display_label"],
            values=df[value_col],
            hole=0.58,
            sort=False,
            direction="clockwise",
            marker=dict(
                colors=colors,
                line=dict(color="#FFFFFF", width=4),
            ),
            textinfo="label+percent",
            textposition="inside",
            insidetextorientation="radial",
            textfont=dict(
                size=13,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Records: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            ),
        )
    )

    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:12px'>Records</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=20,
            color=COLOR_PALETTE["navy"],
            family=CHART_FONT,
        ),
        align="center",
    )

    fig.update_layout(
        height=380,
        margin=dict(l=24, r=24, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family=CHART_FONT,
            size=12,
            color=COLOR_PALETTE["text_muted"],
        ),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=0.92,
            font=dict(
                size=12,
                color=COLOR_PALETTE["text_muted"],
                family=CHART_FONT,
            ),
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0,
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=COLOR_PALETTE["card_border"],
            font=dict(
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
                size=12,
            ),
        ),
    )

    return fig


def fleet_risk_chart(data):
    """
    Fleet Risk Ranking - horizontal bar chart.
    Expected columns can be:
    - fleet / fleet_id
    - avg_risk_score / avg_record_risk_score
    """

    if data is None or len(data) == 0:
        data = pd.DataFrame({
            "fleet": ["Fleet A", "Fleet B", "Fleet C"],
            "avg_risk_score": [0.35, 0.28, 0.42],
        })

    df = data.copy()

    fleet_col = _first_existing_column(
        df,
        ["fleet", "fleet_id", "fleet_name", "vehicle_group"],
        fallback_index=0,
    )
    score_col = _first_existing_column(
        df,
        ["avg_risk_score", "avg_record_risk_score", "record_risk_score", "risk_score"],
        fallback_index=1,
    )

    df["fleet_display"] = df[fleet_col].apply(pretty_label)
    df = df.sort_values(score_col, ascending=True)

    max_score = _safe_max(df[score_col])

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=df["fleet_display"],
            x=df[score_col],
            orientation="h",
            marker=dict(
                color=COLOR_PALETTE["navy"],
                line=dict(color="rgba(255,255,255,0.95)", width=2),
            ),
            width=0.58,
            text=[f"{v:.3f}" for v in df[score_col]],
            textposition="outside",
            textfont=dict(
                size=12,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Average Risk Score: %{x:.3f}<extra></extra>"
            ),
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=380,
        show_legend=False,
        margin=dict(l=120, r=70, t=24, b=42),
    )

    fig.update_xaxes(
        range=[0, max_score * 1.18],
        tickformat=".2f",
        showgrid=True,
        gridcolor=COLOR_PALETTE["grid"],
    )

    fig.update_yaxes(
        showgrid=False,
        categoryorder="array",
        categoryarray=df["fleet_display"].tolist(),
    )

    return fig


def vehicle_type_risk_chart(data):
    """
    Average Risk Score by Vehicle Type - vertical bar chart.
    Expected columns:
    - vehicle_type
    - avg_risk_score / avg_record_risk_score
    """

    if data is None or len(data) == 0:
        data = pd.DataFrame({
            "vehicle_type": ["truck", "van", "car", "motorcycle"],
            "avg_risk_score": [0.35, 0.28, 0.22, 0.42],
        })

    df = data.copy()

    vehicle_col = _first_existing_column(
        df,
        ["vehicle_type", "type", "vehicle"],
        fallback_index=0,
    )
    score_col = _first_existing_column(
        df,
        ["avg_risk_score", "avg_record_risk_score", "record_risk_score", "risk_score"],
        fallback_index=1,
    )

    df["vehicle_display"] = df[vehicle_col].apply(pretty_label)
    df = df.sort_values(score_col, ascending=False)

    max_score = _safe_max(df[score_col])

    colors = [
        COLOR_PALETTE["orange"] if i == 0 else COLOR_PALETTE["navy"]
        for i in range(len(df))
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["vehicle_display"],
            y=df[score_col],
            marker=dict(
                color=colors,
                line=dict(color="rgba(255,255,255,0.95)", width=2),
            ),
            width=0.55,
            text=[f"{v:.3f}" for v in df[score_col]],
            textposition="outside",
            textfont=dict(
                size=12,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Average Risk Score: %{y:.3f}<extra></extra>"
            ),
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=380,
        show_legend=False,
        margin=dict(l=54, r=32, t=24, b=72),
    )

    fig.update_xaxes(
        showgrid=False,
        tickangle=-12,
    )

    fig.update_yaxes(
        range=[0, max_score * 1.22],
        tickformat=".2f",
    )

    return fig


# ==============================================================================
# ANOMALY CHARTS
# ==============================================================================

def anomaly_by_vehicle_type_chart(data):
    """Anomaly Rate by Vehicle Type."""

    if data is None or len(data) == 0:
        data = pd.DataFrame({
            "vehicle_type": ["truck", "van", "car", "motorcycle"],
            "anomaly_rate_pct": [5.5, 4.2, 3.8, 8.5],
        })

    df = data.copy()

    label_col = _first_existing_column(
        df,
        ["vehicle_type", "engine_status", "type"],
        fallback_index=0,
    )
    value_col = _first_existing_column(
        df,
        ["anomaly_rate_pct", "rate", "value"],
        fallback_index=1,
    )

    df["display_label"] = df[label_col].apply(pretty_label)
    max_value = _safe_max(df[value_col])

    colors = [
        COLOR_PALETTE["navy"] if value == max_value else COLOR_PALETTE["light_blue"]
        for value in df[value_col]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["display_label"],
            y=df[value_col],
            marker=dict(
                color=colors,
                line=dict(color="white", width=2),
            ),
            width=0.55,
            text=[f"{v:.2f}%" for v in df[value_col]],
            textposition="outside",
            textfont=dict(
                size=11,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate="<b>%{x}</b><br>Anomaly Rate: %{y:.2f}%<extra></extra>",
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=350,
        margin=dict(l=50, r=32, t=24, b=60),
    )

    fig.update_xaxes(showgrid=False, tickangle=-10)
    fig.update_yaxes(range=[0, max_value * 1.2])

    return fig


def anomaly_by_road_class_chart(data):
    """Anomaly Rate by Road Class."""

    if data is None or len(data) == 0:
        data = pd.DataFrame({
            "road_class": ["highway", "expressway", "city", "rural"],
            "anomaly_rate_pct": [4.5, 10.6, 5.2, 3.1],
        })

    df = data.copy()

    label_col = _first_existing_column(
        df,
        ["road_class", "road", "class"],
        fallback_index=0,
    )
    value_col = _first_existing_column(
        df,
        ["anomaly_rate_pct", "rate", "value"],
        fallback_index=1,
    )

    df["display_label"] = df[label_col].apply(pretty_label)
    max_value = _safe_max(df[value_col])

    colors = [
        COLOR_PALETTE["orange"] if value == max_value else COLOR_PALETTE["light_blue"]
        for value in df[value_col]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["display_label"],
            y=df[value_col],
            marker=dict(
                color=colors,
                line=dict(color="white", width=2),
            ),
            width=0.55,
            text=[f"{v:.2f}%" for v in df[value_col]],
            textposition="outside",
            textfont=dict(
                size=11,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate="<b>%{x}</b><br>Anomaly Rate: %{y:.2f}%<extra></extra>",
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=350,
        margin=dict(l=50, r=32, t=24, b=60),
    )

    fig.update_xaxes(showgrid=False, tickangle=-10)
    fig.update_yaxes(range=[0, max_value * 1.2])

    return fig


# ==============================================================================
# MODEL CHARTS
# ==============================================================================

def model_metric_chart(model_results):
    """Model F1 Macro Score Comparison."""

    if model_results is None or len(model_results) == 0:
        return go.Figure()

    df = model_results.copy().nlargest(6, "f1_macro")
    df["model_display"] = df["model"].apply(pretty_label)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["model_display"],
            y=df["f1_macro"],
            marker=dict(
                color=COLOR_PALETTE["navy"],
                line=dict(color="white", width=2),
            ),
            width=0.55,
            text=[f"{v:.4f}" for v in df["f1_macro"]],
            textposition="outside",
            textfont=dict(
                size=11,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate="<b>%{x}</b><br>F1 Macro: %{y:.4f}<extra></extra>",
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=350,
        margin=dict(l=50, r=32, t=24, b=90),
    )

    fig.update_xaxes(showgrid=False, tickangle=-35)
    fig.update_yaxes(range=[0.7, 1.02])

    return fig


def accuracy_comparison_chart(model_results):
    """Model Accuracy Comparison."""

    if model_results is None or len(model_results) == 0:
        return go.Figure()

    df = model_results.copy().nlargest(6, "accuracy")
    df["model_display"] = df["model"].apply(pretty_label)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["model_display"],
            y=df["accuracy"],
            marker=dict(
                color=COLOR_PALETTE["orange"],
                line=dict(color="white", width=2),
            ),
            width=0.55,
            text=[f"{v:.4f}" for v in df["accuracy"]],
            textposition="outside",
            textfont=dict(
                size=11,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate="<b>%{x}</b><br>Accuracy: %{y:.4f}<extra></extra>",
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=350,
        margin=dict(l=50, r=32, t=24, b=90),
    )

    fig.update_xaxes(showgrid=False, tickangle=-35)
    fig.update_yaxes(range=[0.8, 1.02])

    return fig


def confusion_matrix_chart():
    """Confusion Matrix - Hist Gradient Boosting Model."""

    confusion_data = [
        [1712, 0, 128],
        [0, 33838, 162],
        [51, 237, 23783],
    ]

    labels = ["High Risk", "Low Risk", "Medium Risk"]

    fig = go.Figure(
        data=go.Heatmap(
            z=confusion_data,
            x=labels,
            y=labels,
            colorscale=[
                [0.0, COLOR_PALETTE["light_blue"]],
                [0.5, COLOR_PALETTE["light_orange"]],
                [1.0, COLOR_PALETTE["navy"]],
            ],
            text=confusion_data,
            texttemplate="%{text}",
            textfont=dict(
                size=12,
                color=COLOR_PALETTE["text_dark"],
                family=CHART_FONT,
            ),
            hovertemplate=(
                "Actual: %{y}<br>"
                "Predicted: %{x}<br>"
                "Count: %{z:,}<extra></extra>"
            ),
            colorbar=dict(
                title="Count",
                tickfont=dict(color=COLOR_PALETTE["text_muted"]),
            ),
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=400,
        margin=dict(l=80, r=60, t=24, b=60),
    )

    fig.update_xaxes(title_text="Predicted", showgrid=False)
    fig.update_yaxes(title_text="Actual", showgrid=False)

    return fig


# ==============================================================================
# RISK SCORE / CLUSTERING
# ==============================================================================

def record_risk_score_histogram(df_clean):
    """Record Risk Score Distribution - Histogram."""

    if (
        df_clean is None
        or len(df_clean) == 0
        or "record_risk_score" not in df_clean.columns
    ):
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=df_clean["record_risk_score"],
            nbinsx=45,
            marker=dict(
                color=COLOR_PALETTE["light_blue"],
                line=dict(color="white", width=0.8),
            ),
            hovertemplate="Risk Score: %{x}<br>Count: %{y:,}<extra></extra>",
        )
    )

    fig.add_vline(
        x=0.25,
        line_dash="dash",
        line_color=COLOR_PALETTE["orange"],
        annotation_text="Medium",
        annotation_position="top right",
        annotation_font_color=COLOR_PALETTE["text_dark"],
    )

    fig.add_vline(
        x=0.50,
        line_dash="dash",
        line_color=COLOR_PALETTE["navy"],
        annotation_text="High",
        annotation_position="top right",
        annotation_font_color=COLOR_PALETTE["text_dark"],
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=350,
        margin=dict(l=54, r=32, t=24, b=50),
    )

    fig.update_xaxes(title_text="Record Risk Score")
    fig.update_yaxes(title_text="Frequency")

    return fig


def clustering_metrics_chart(clustering_results):
    """Clustering Algorithm Metrics Comparison."""

    if clustering_results is None or len(clustering_results) == 0:
        return go.Figure()

    df = clustering_results.copy()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Algorithm"],
            y=df["Silhouette Score"],
            name="Silhouette Score",
            mode="lines+markers",
            marker=dict(
                size=10,
                color=COLOR_PALETTE["orange"],
                line=dict(color="white", width=2),
            ),
            line=dict(
                width=3,
                color=COLOR_PALETTE["navy"],
                shape="spline",
            ),
            hovertemplate="<b>%{x}</b><br>Silhouette: %{y:.4f}<extra></extra>",
        )
    )

    apply_premium_chart_style(
        fig,
        title=None,
        height=350,
        show_legend=False,
        margin=dict(l=54, r=32, t=24, b=54),
    )

    fig.update_xaxes(showgrid=False)

    return fig


def engine_status_distribution_chart(data):
    """
    Engine Status Distribution - Donut chart for K-Means K=2.
    Expected columns:
    - engine_status
    - count
    """

    import pandas as pd
    import plotly.graph_objects as go

    if data is None or len(data) == 0:
        data = pd.DataFrame({
            "engine_status": ["NORMAL_OPERATION", "HIGH_STRESS"],
            "count": [0, 0],
        })

    df = data.copy()

    label_col = "engine_status" if "engine_status" in df.columns else df.columns[0]
    value_col = "count" if "count" in df.columns else df.columns[1]

    label_map = {
        "NORMAL_OPERATION": "Normal Operation",
        "HIGH_STRESS": "High Stress",
    }

    color_map = {
        "NORMAL_OPERATION": "#BBE0EF",
        "HIGH_STRESS": "#F16D34",
    }

    df["display_label"] = df[label_col].apply(
        lambda x: label_map.get(str(x), str(x).replace("_", " ").title())
    )

    colors = [
        color_map.get(str(value), "#161E54")
        for value in df[label_col]
    ]

    total = int(df[value_col].sum())

    fig = go.Figure()

    fig.add_trace(
        go.Pie(
            labels=df["display_label"],
            values=df[value_col],
            hole=0.58,
            sort=False,
            marker=dict(
                colors=colors,
                line=dict(color="#FFFFFF", width=4),
            ),
            textinfo="label+percent",
            textposition="inside",
            textfont=dict(
                size=13,
                color="#161E54",
                family="Inter, Arial, sans-serif",
            ),
            hovertemplate=(
                "<b>%{label}</b><br>"
                "Records: %{value:,}<br>"
                "Share: %{percent}<extra></extra>"
            ),
        )
    )

    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:12px'>Records</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=20,
            color="#161E54",
            family="Inter, Arial, sans-serif",
        ),
        align="center",
    )

    fig.update_layout(
        height=360,
        margin=dict(l=24, r=24, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, Arial, sans-serif",
            size=12,
            color="rgba(22,30,84,0.62)",
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(
                size=12,
                color="rgba(22,30,84,0.70)",
                family="Inter, Arial, sans-serif",
            ),
            bgcolor="rgba(255,255,255,0)",
            borderwidth=0,
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="rgba(22,30,84,0.10)",
            font=dict(
                color="#161E54",
                family="Inter, Arial, sans-serif",
                size=12,
            ),
        ),
    )

    return fig