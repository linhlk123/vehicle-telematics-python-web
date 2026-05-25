"""
Drawer Components - Side panels and modals for detailed views
"""
from nicegui import ui
from services import data_service


def render_vehicle_detail_drawer(vehicle_id):
    """Render a drawer with detailed vehicle information"""
    
    vehicle_detail = data_service.get_vehicle_detail(vehicle_id)
    vehicle_summary = vehicle_detail.get('vehicle_summary', {})
    vehicle_records = vehicle_detail.get('vehicle_records', [])
    
    with ui.dialog() as dialog:
        with ui.card().classes("glass-card w-full"):
            # Header
            with ui.row().classes("w-full items-center justify-between mb-4"):
                ui.label(f"Vehicle: {vehicle_id}").classes("text-2xl font-bold text-cyan-400")
                ui.button("×", on_click=dialog.close).props("flat dense").classes("text-2xl")
            
            # Summary Section
            if vehicle_summary:
                ui.label("Risk Summary").classes("text-lg font-bold text-cyan-400 mt-4")
                
                with ui.grid(columns=3).classes("w-full gap-4"):
                    from components.cards import render_metric_card
                    
                    avg_risk = vehicle_summary.get('avg_risk_score', 0)
                    high_rate = vehicle_summary.get('high_risk_rate_pct', 0)
                    anom_rate = vehicle_summary.get('anomaly_rate_pct', 0)
                    
                    render_metric_card("Avg Risk Score", f"{avg_risk:.3f}", tone="cyan")
                    render_metric_card("High Risk Rate", f"{high_rate:.1f}%", tone="amber")
                    render_metric_card("Anomaly Rate", f"{anom_rate:.1f}%", tone="violet")
                
                # Maintenance Status
                priority = vehicle_summary.get('maintenance_priority', 'UNKNOWN')
                recommendation = vehicle_summary.get('recommendation', 'No recommendation')
                
                from components.cards import render_maintenance_badge, render_info_card
                
                ui.label("Maintenance Status").classes("text-lg font-bold text-cyan-400 mt-6")
                render_maintenance_badge(priority)
                
                render_info_card("Recommendation", recommendation, "💡")
            
            # Recent Records
            ui.label("Recent Telemetry Records").classes("text-lg font-bold text-cyan-400 mt-6")
            
            if vehicle_records is not None and len(vehicle_records) > 0:
                from components.tables import render_dataframe_table
                render_dataframe_table(vehicle_records.head(10))
            else:
                ui.label("No records available").classes("text-slate-400")
            
            # Close Button
            ui.button("Close", on_click=dialog.close).classes("w-full mt-6")
    
    return dialog


def render_model_detail_drawer(model_name):
    """Render a drawer with detailed model information"""
    
    from services import data_service
    
    model_results = data_service.load_model_results()
    model_info = model_results[model_results['model'] == model_name].iloc[0] if len(model_results) > 0 else None
    
    with ui.dialog() as dialog:
        with ui.card().classes("glass-card w-full"):
            # Header
            with ui.row().classes("w-full items-center justify-between mb-4"):
                ui.label(f"Model: {model_name}").classes("text-2xl font-bold text-cyan-400")
                ui.button("×", on_click=dialog.close).props("flat dense").classes("text-2xl")
            
            if model_info is not None:
                # Metrics
                ui.label("Performance Metrics").classes("text-lg font-bold text-cyan-400 mt-4")
                
                with ui.grid(columns=2).classes("w-full gap-4"):
                    from components.cards import render_metric_card
                    
                    render_metric_card("Accuracy", f"{model_info['accuracy']:.4f}", tone="green")
                    render_metric_card("F1 Macro", f"{model_info['f1_macro']:.4f}", tone="cyan")
                    render_metric_card("F1 Weighted", f"{model_info['f1_weighted']:.4f}", tone="violet")
                    render_metric_card("Status", model_info['status'], tone="cyan")
                
                # Description
                from components.cards import render_info_card
                
                if model_name == "Hist Gradient Boosting":
                    render_info_card(
                        "Best Model",
                        "This is the selected production model. It achieves the highest F1 Macro score and ensures no HIGH_RISK records are misclassified as LOW_RISK.",
                        "🏆"
                    )
                elif model_name == "Random Forest":
                    render_info_card(
                        "Strong Baseline",
                        "Excellent ensemble performance with high accuracy and good interpretability. Suitable as backup model.",
                        "🌲"
                    )
                elif model_name == "Decision Tree":
                    render_info_card(
                        "Explainable",
                        "Most interpretable model for business stakeholders. Good for understanding decision logic.",
                        "🌳"
                    )
                else:
                    render_info_card(
                        "Model Details",
                        f"Status: {model_info['status']}",
                        "ℹ️"
                    )
            
            ui.button("Close", on_click=dialog.close).classes("w-full mt-6")
    
    return dialog


def render_alert_drawer():
    """Render drawer for alerts and notifications"""
    
    from services import data_service
    
    vehicle_risk = data_service.load_vehicle_risk()
    alerts = vehicle_risk[vehicle_risk['maintenance_priority'] == 'MAINTENANCE_ALERT']
    
    with ui.dialog() as dialog:
        with ui.card().classes("glass-card w-full"):
            # Header
            with ui.row().classes("w-full items-center justify-between mb-4"):
                ui.label(f"🚨 Maintenance Alerts ({len(alerts)})").classes("text-2xl font-bold text-red-400")
                ui.button("×", on_click=dialog.close).props("flat dense").classes("text-2xl")
            
            # Alerts List
            if len(alerts) > 0:
                from components.tables import render_dataframe_table
                
                display_cols = ['vehicle_id', 'avg_risk_score', 'high_risk_rate_pct', 'anomaly_rate_pct']
                available_cols = [col for col in display_cols if col in alerts.columns]
                
                render_dataframe_table(alerts[available_cols], max_rows=20)
            else:
                ui.label("No active alerts").classes("text-green-400 font-semibold")
            
            ui.button("Close", on_click=dialog.close).classes("w-full mt-6")
    
    return dialog
