"""
Vehicle Telematics Predictive Maintenance & Algorithm Simulation Platform
Premium AI Command Center for Fleet Risk Intelligence

Main Application Entry Point
"""

from nicegui import app, ui
from pathlib import Path
import os
from pages import overview, pipeline_page, clustering_page, anomaly_page, risk_scoring_page, model_lab_page, prediction_page, maintenance_page
# Add services to path
import sys

sys.path.insert(0, str(Path(__file__).parent))

# Import services
from services import data_service, model_service, risk_service
from components import layout, cards, charts, tables, pipeline, prediction_form

# Load CSS - add to app level
# Load CSS directly
css_path = Path(__file__).parent / "assets" / "styles.css"

print("CSS PATH:", css_path.resolve())
print("CSS EXISTS:", css_path.exists())

if css_path.exists():
    ui.add_css(css_path.read_text(encoding="utf-8"),shared=True)
    print("✅ CSS loaded with ui.add_css")
else:
    print("❌ styles.css not found")

# Add CSS link to all pages using head HTML injection for each @ui.page
def _inject_css():
    ui.add_head_html('<link rel="stylesheet" href="/styles.css" type="text/css">')

# ==============================================================================
# APP STARTUP
# ==============================================================================

import os

if __name__ in {"__main__", "__mp_main__"}:
    port = int(os.environ.get("PORT", 8081))

    ui.run(
        host="0.0.0.0",
        port=port,
        reload=False,
        title="Telematics Risk Intelligence",
    )