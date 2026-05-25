"""
Card Components - Reusable card UI elements
"""
from nicegui import ui


def _render_clustering_kpi_card(title, value, subtitle, icon, icon_color="#161E54", bg_color="#BBE0EF"):
    with ui.card().classes(
        "rounded-[30px] bg-white border border-slate-100 "
        "shadow-[0_10px_28px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        ui.label(title).classes(
            "w-full text-center text-[17px] font-extrabold text-[#161E54] "
            "pt-5 pb-3 border-b border-slate-100"
        )

        with ui.row().classes(
            "w-full items-center justify-center gap-5 px-6 pt-6 pb-2"
        ):
            ui.icon(icon).classes(
                "text-[42px] rounded-[18px] p-3"
            ).style(
                f"color: {icon_color}; background: {bg_color}33;"
            )

            ui.label(str(value)).classes(
                "text-[34px] leading-none font-extrabold text-[#161E54] tracking-wide"
            )

        ui.label(subtitle).classes(
            "w-full text-center text-[13px] font-semibold text-[#161E54]/60 pb-6 px-4"
        )


def _render_reason_card(title, content, icon, color="#161E54", bg="#BBE0EF"):
    with ui.card().classes(
        "rounded-[24px] bg-white border border-slate-100 "
        "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
    ):
        with ui.row().classes("w-full items-start gap-4 px-5 py-5"):
            ui.icon(icon).classes(
                "text-[30px] rounded-[16px] p-3"
            ).style(
                f"color: {color}; background: {bg}22;"
            )

            with ui.column().classes("gap-2 flex-1"):
                ui.label(title).classes(
                    "text-[16px] font-extrabold text-[#161E54]"
                )
                ui.label(content).classes(
                    "text-[13px] font-semibold leading-relaxed text-[#161E54]/65"
                )


def _render_cluster_profile_card(title, description, icon, color, bg, metrics):
    with ui.card().classes(
        "rounded-[24px] bg-white border border-slate-100 "
        "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
    ):
        with ui.row().classes("w-full items-start gap-4 px-5 py-5"):
            ui.icon(icon).classes(
                "text-[32px] rounded-[16px] p-3"
            ).style(
                f"color: {color}; background: {bg}22;"
            )

            with ui.column().classes("gap-2 flex-1"):
                ui.label(title).classes(
                    "text-[17px] font-extrabold text-[#161E54]"
                )
                ui.label(description).classes(
                    "text-[13px] font-semibold leading-relaxed text-[#161E54]/65"
                )

                with ui.column().classes("gap-1 mt-2"):
                    for metric in metrics:
                        with ui.row().classes("items-center gap-2"):
                            ui.icon("radio_button_checked").classes(
                                "text-[12px]"
                            ).style(f"color: {color};")
                            ui.label(metric).classes(
                                "text-[12px] font-semibold text-[#161E54]/60"
                            )


def render_metric_card(title, value, subtitle=None, icon=None, tone="cyan"):
    """Render a metric card with title, value, and optional subtitle"""
    
    tone_class_map = {
        "cyan": "tone-cyan",
        "violet": "tone-violet",
        "green": "tone-green",
        "amber": "tone-amber",
        "red": "tone-red",
    }
    
    tone_css = tone_class_map.get(tone, "tone-cyan")
    
    with ui.card().classes(f"metric-card {tone_css}"):
        ui.label(title).classes("metric-label")
        ui.label(str(value)).classes("metric-value")
        if subtitle:
            ui.label(subtitle).classes("metric-subtitle")


def render_glass_card(title=None, subtitle=None):
    """Create a glass-morphism card for content"""
    
    card = ui.card().classes("glass-card w-full")
    
    with card:
        if title:
            with ui.column().classes("w-full pb-4 mb-4"):
                ui.label(title).classes("section-title")
                if subtitle:
                    ui.label(subtitle).classes("section-subtitle")
    
    return card


def render_risk_badge(risk_level):
    """Render a risk level badge"""
    
    badge_config = {
        "LOW_RISK": {"class": "badge badge-low-risk", "icon": "✓"},
        "MEDIUM_RISK": {"class": "badge badge-medium-risk", "icon": "⚠"},
        "HIGH_RISK": {"class": "badge badge-high-risk", "icon": "⛔"},
    }
    
    config = badge_config.get(risk_level, badge_config["LOW_RISK"])
    
    with ui.row().classes(config["class"]):
        ui.label(f"{config['icon']} {risk_level}")


def render_maintenance_badge(priority):
    """Render a maintenance priority badge"""
    
    badge_config = {
        "NORMAL_MONITORING": {"class": "badge badge-normal", "icon": "📊"},
        "NEED_ATTENTION": {"class": "badge badge-attention", "icon": "⚡"},
        "MAINTENANCE_ALERT": {"class": "badge badge-alert", "icon": "🚨"},
    }
    
    config = badge_config.get(priority, badge_config["NORMAL_MONITORING"])
    
    with ui.row().classes(config["class"]):
        ui.label(f"{config['icon']} {priority}")


def render_algorithm_badge(name):
    """Render an algorithm badge"""
    
    with ui.row().classes("badge bg-violet-100 text-violet-800 border border-violet-300"):
        ui.label(f"⚙ {name}")


def render_empty_state(title, message):
    """Render an empty state card"""
    
    with ui.card().classes("glass-card w-full py-12"):
        with ui.column().classes("w-full items-center justify-center text-center"):
            ui.label("📭").classes("text-6xl mb-4")
            ui.label(title).classes("text-xl font-bold text-slate-700 mb-2")
            ui.label(message).classes("text-sm text-slate-500")


def render_info_card(title, content, icon="ℹ"):
    """Render an info card with custom content"""
    
    with ui.card().classes("info-card"):
        ui.label(icon).classes("info-card-icon")
        ui.label(title).classes("info-card-title")
        ui.html(content).classes("info-card-content")


def render_warning_card(title, content):
    """Render a warning card"""
    with ui.card().classes("warning-card info-card"):
        ui.label("⚠️").classes("info-card-icon")
        ui.label(title).classes("info-card-title")
        ui.html(content).classes("info-card-content")


def render_success_card(title, content):
    """Render a success card"""
    with ui.card().classes("success-card info-card"):
        ui.label("✅").classes("info-card-icon")
        ui.label(title).classes("info-card-title")
        ui.html(content).classes("info-card-content")


def render_kpi_card(title, value, subtitle=None, icon=None, icon_color="#161E54", icon_bg="#BBE0EF"):
    """
    Render a premium KPI card for admin dashboard.
    
    Args:
        title: Card title (e.g., "Total Vehicles")
        value: Main KPI value (e.g., "1,234")
        subtitle: Optional subtitle (e.g., "vs previous month +12%")
        icon: Icon name or emoji
        icon_color: Icon foreground color (default: #161E54 - dark blue)
        icon_bg: Icon background color (default: #BBE0EF - light cyan)
    """
    with ui.card().classes("bg-white rounded-3xl shadow-sm border border-slate-100 p-6 hover:shadow-md transition-shadow"):
        with ui.column().classes("w-full gap-4"):
            # Title
            ui.label(title).classes("text-sm font-semibold text-slate-600 uppercase tracking-wide")
            
            # Main content row: icon + value
            with ui.row().classes("w-full items-center justify-between"):
                # Icon in background circle
                if icon:
                    with ui.element("div").classes("flex items-center justify-center rounded-full p-3").style(f"background-color: {icon_bg}; width: 60px; height: 60px; flex-shrink: 0;"):
                        ui.label(icon).classes("text-2xl").style(f"color: {icon_color};")
                
                # Main value - centered and prominent
                ui.label(str(value)).classes("text-4xl font-extrabold").style("color: #161E54;")
            
            # Subtitle
            if subtitle:
                ui.label(subtitle).classes("text-xs text-slate-500")
