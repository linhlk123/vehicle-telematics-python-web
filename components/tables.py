"""
Table Components - Reusable table UI elements
"""
from nicegui import ui
import pandas as pd


def _get_risk_badge_class(risk_level):
    """Get badge class based on risk level"""
    if risk_level == 'LOW_RISK':
        return 'badge-low-risk'
    elif risk_level == 'MEDIUM_RISK':
        return 'badge-medium-risk'
    elif risk_level == 'HIGH_RISK':
        return 'badge-high-risk'
    return 'badge'


def render_dataframe_table(df, title=None, max_rows=20):
    """Render a DataFrame as an HTML table with light mode styling"""
    
    if df is None or len(df) == 0:
        from components.cards import render_empty_state
        return render_empty_state("No Data", "No records found to display")
    
    # Limit rows for display
    display_df = df.head(max_rows)
    
    with ui.column().classes("w-full space-y-2"):
        if title:
            ui.label(title).classes("section-title")
        
        # Create HTML table with light mode styling
        html_table = display_df.to_html(
            index=False,
            escape=False,
            classes="w-full text-sm border-collapse",
        ).replace('<table class="w-full text-sm border-collapse">', 
                 '<table class="w-full text-sm border-collapse" style="border-spacing: 0;">').replace(
                    '<thead>', '<thead class="table-header">'
                ).replace(
                    '<tr>', '<tr class="table-row">'
                ).replace(
                    '<th>', '<th class="table-header" style="padding: 12px; text-align: left; font-weight: 600;">'
                ).replace(
                    '<td>', '<td class="table-cell" style="padding: 12px;">'
                )
        
        ui.html(html_table).classes("table-container w-full overflow-x-auto")
        
        if len(df) > max_rows:
            ui.label(f"Showing {max_rows} of {len(df)} records").classes("text-xs text-slate-500 text-right")


def render_top_anomaly_table(df, max_rows=20):
    """Render top anomaly records table with light mode"""
    
    if df is None or len(df) == 0:
        from components.cards import render_empty_state
        return render_empty_state("No Anomalies", "No anomalous records found")
    
    # Select key columns
    display_cols = [
        'vehicle_id', 'vehicle_type', 'fleet', 'road_class', 'engine_status_k2_all',
        'iso_anomaly_score', 'risk_level', 'record_risk_score'
    ]
    
    available_cols = [col for col in display_cols if col in df.columns]
    display_df = df[available_cols].head(max_rows).copy()
    
    # Format numeric columns
    numeric_cols = display_df.select_dtypes(include=['float64', 'float32']).columns
    for col in numeric_cols:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
    
    render_dataframe_table(display_df, max_rows=max_rows)


def render_model_leaderboard_table(model_results):
    """Render ML model leaderboard"""
    
    if model_results is None or len(model_results) == 0:
        from components.cards import render_empty_state
        return render_empty_state("No Models", "No model results found")
    
    # Sort by f1_macro
    sorted_results = model_results.sort_values('f1_macro', ascending=False).copy()
    
    # Select columns
    display_cols = ['model', 'accuracy', 'f1_macro', 'f1_weighted', 'status']
    available_cols = [col for col in display_cols if col in sorted_results.columns]
    display_df = sorted_results[available_cols]
    
    # Format numeric columns
    numeric_cols = display_df.select_dtypes(include=['float64', 'float32']).columns
    for col in numeric_cols:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
    
    render_dataframe_table(display_df, max_rows=10)


def render_clustering_comparison_table(clustering_results):
    """Render clustering algorithm comparison"""
    
    if clustering_results is None or len(clustering_results) == 0:
        from components.cards import render_empty_state
        return render_empty_state("No Results", "No clustering results found")
    
    display_df = clustering_results.copy()
    
    # Format numeric columns
    numeric_cols = display_df.select_dtypes(include=['float64', 'float32']).columns
    for col in numeric_cols:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
    
    render_dataframe_table(display_df, max_rows=10)


def render_maintenance_queue_table(df, max_rows=50):
    """Render maintenance queue table with vehicle info - styled like anomaly table"""

    if df is None or len(df) == 0:
        from components.cards import render_empty_state
        return render_empty_state("Empty Queue", "No vehicles in maintenance queue")

    display_df = df.head(max_rows).copy()

    # Format column names: bỏ dấu "_" và viết đẹp hơn
    display_df.columns = [
        str(col).replace("_", " ").replace("-", " ").title()
        for col in display_df.columns
    ]

    # Format numeric columns
    numeric_cols = display_df.select_dtypes(include=["float64", "float32", "float", "int64", "int32"]).columns
    for col in numeric_cols:
        display_df[col] = display_df[col].apply(
            lambda x: f"{x:.4f}" if isinstance(x, float) and abs(x) < 1 else f"{x:.2f}" if isinstance(x, float) else x
        )

    # Card giống style trang anomaly
    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
    ):
        # Header title ở giữa
        with ui.row().classes(
            "relative w-full items-center justify-end px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            ui.label("Maintenance Queue").classes(
                "absolute left-1/2 -translate-x-1/2 "
                "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
            )

            ui.label("PRIORITY LIST").classes(
                "rounded-full px-4 py-2 bg-white/70 text-[#161E54] "
                "font-extrabold text-[11px] tracking-wide shadow-sm"
            )

        ui.label("Vehicles ranked by maintenance priority and risk indicators").classes(
            "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
        )

        # Table wrapper
        with ui.column().classes("w-full px-6 pt-5 pb-6 app-data-table"):
            columns = [
                {
                    "name": col,
                    "label": col,
                    "field": col,
                    "align": "center",
                    "sortable": True,
                }
                for col in display_df.columns
            ]

            rows = display_df.to_dict("records")

            ui.table(
                columns=columns,
                rows=rows,
                row_key=display_df.columns[0],
                pagination={"rowsPerPage": max_rows},
            ).classes(
                "w-full app-data-table"
            ).props(
                "flat bordered separator=cell"
            )

            if len(df) > max_rows:
                ui.label(f"Showing {max_rows} of {len(df)} records").classes(
                    "w-full text-right text-[12px] font-semibold text-[#161E54]/50 mt-2"
                )

def render_risk_threshold_table():
    """Render risk flag threshold reference table"""
    
    from services.risk_service import RISK_THRESHOLDS
    
    thresholds_data = []
    for flag, threshold in RISK_THRESHOLDS.items():
        thresholds_data.append({'Flag': flag.replace('_', ' ').title(), 'Threshold': threshold})
    
    df = pd.DataFrame(thresholds_data)
    render_dataframe_table(df, max_rows=20)


def render_risk_level_mapping_table():
    """Render risk level to score mapping table"""
    
    data = {
        'Risk Level': ['LOW_RISK', 'MEDIUM_RISK', 'HIGH_RISK'],
        'Score Range': ['0.00 - 0.25', '0.25 - 0.50', '0.50 - 1.00'],
        'Action': ['Routine Monitoring', 'Close Observation', 'Maintenance Alert'],
    }
    
    df = pd.DataFrame(data)
    render_dataframe_table(df, max_rows=10)
