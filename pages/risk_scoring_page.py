from nicegui import ui

from services import data_service
from components import layout, charts, tables


# ==============================================================================
# HELPERS
# ==============================================================================

def render_risk_weight_card(
    title,
    value,
    subtitle,
    icon,
    color="#161E54",
    bg="#BBE0EF",
):
    """Render one risk flag weight card."""

    with ui.card().classes(
        "rounded-[30px] bg-white border border-slate-100 "
        "shadow-[0_10px_28px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        ui.label(title).classes(
            "w-full text-center text-[16px] font-extrabold text-[#161E54] "
            "pt-5 pb-3 border-b border-slate-100"
        )

        with ui.row().classes(
            "w-full items-center justify-center gap-5 px-5 pt-6 pb-2"
        ):
            ui.icon(icon).classes(
                "text-[38px] rounded-[18px] p-3"
            ).style(
                f"color: {color}; background: {bg}33;"
            )

            ui.label(str(value)).classes(
                "text-[34px] leading-none font-extrabold text-[#161E54] tracking-wide"
            )

        ui.label(subtitle).classes(
            "w-full text-center text-[13px] font-semibold text-[#161E54]/60 pb-6 px-4"
        )


def render_risk_score_table_card(
    title,
    subtitle,
    content_func,
    badge_text=None,
    action_text=None,
    action=None,
):
    """Render Risk Scoring table card with Pipeline-like table style."""

    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
    ):
        # Header
        with ui.row().classes(
            "relative w-full items-center justify-end px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            ui.label(title).classes(
                "absolute left-1/2 -translate-x-1/2 "
                "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
            )

            if action_text and action:
                ui.button(
                    action_text,
                    on_click=action,
                ).props(
                    "flat dense no-caps"
                ).classes(
                    "rounded-full px-4 py-2 bg-white/70 text-[#161E54] "
                    "font-extrabold hover:bg-white shadow-sm"
                )
            elif badge_text:
                ui.label(badge_text).classes(
                    "rounded-full px-4 py-2 bg-white/70 text-[#161E54] "
                    "font-extrabold text-[11px] tracking-wide shadow-sm"
                )

        if subtitle:
            ui.label(subtitle).classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

        # Table wrapper
        with ui.column().classes(
            "w-full px-6 pt-5 pb-6 app-data-table"
        ):
            content_func()

def render_formula_card():
    """Render risk score formula card - center aligned."""

    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
    ):
        # Header - centered
        with ui.column().classes(
            "w-full items-center justify-center gap-3 px-7 py-6 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            ui.icon("functions").classes(
                "text-[34px] bg-white rounded-[18px] p-3 "
                "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
            ).style("color: #161E54;")

            ui.label("Công Thức Tính Điểm Rủi Ro Bản Ghi").classes(
                "text-[24px] font-extrabold text-[#161E54] text-center"
            )

            ui.label("Tổng hợp các tín hiệu rủi ro thành điểm rủi ro cấp bản ghi").classes(
                "text-[13px] font-medium text-[#161E54]/55 text-center"
            )

            ui.label("RULE ENGINE").classes(
                "px-4 py-2 rounded-full bg-[#161E54] text-white "
                "text-[12px] font-extrabold tracking-wide mt-1"
            )

        # Body
        with ui.column().classes("w-full items-center gap-5 px-7 py-6"):
            ui.label(
                "record_risk_score = 0.25 × high_stress_flag + 0.25 × iso_anomaly + "
                "0.15 × high_fuel_flag + 0.10 × aggressive_throttle_flag + "
                "0.10 × high_rpm_flag + 0.05 × harsh_brake_flag + "
                "0.05 × harsh_accel_flag + 0.05 × low_efficiency_flag"
            ).classes(
                "w-full rounded-[24px] bg-[#BBE0EF]/25 border border-[#BBE0EF]/70 "
                "px-6 py-5 text-[15px] font-extrabold leading-relaxed "
                "text-[#161E54] text-center"
            )

            with ui.grid(columns=3).classes("w-full gap-5"):
                with ui.card().classes(
                    "rounded-[22px] bg-white border border-slate-100 shadow-none p-5"
                ):
                    with ui.column().classes("w-full items-center text-center gap-2"):
                        ui.label("Range").classes(
                            "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/45 text-center"
                        )
                        ui.label("0.0 → 1.0").classes(
                            "text-[26px] font-extrabold text-[#161E54] text-center"
                        )
                        ui.label("0 là thấp nhất, 1 là cao nhất").classes(
                            "text-[13px] font-semibold text-[#161E54]/55 text-center"
                        )

                with ui.card().classes(
                    "rounded-[22px] bg-[#BBE0EF]/20 border border-[#BBE0EF]/60 shadow-none p-5"
                ):
                    with ui.column().classes("w-full items-center text-center gap-2"):
                        ui.label("Rủi Ro Thấp").classes(
                            "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/45 text-center"
                        )
                        ui.label("0.00 - 0.25").classes(
                            "text-[26px] font-extrabold text-[#161E54] text-center"
                        )
                        ui.label("Vận hành bình thường").classes(
                            "text-[13px] font-semibold text-[#161E54]/55 text-center"
                        )

                with ui.card().classes(
                    "rounded-[22px] bg-[#F16D34]/10 border border-[#F16D34]/25 shadow-none p-5"
                ):
                    with ui.column().classes("w-full items-center text-center gap-2"):
                        ui.label("Medium / High").classes(
                            "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/45 text-center"
                        )
                        ui.label("> 0.25").classes(
                            "text-[26px] font-extrabold text-[#F16D34] text-center"
                        )
                        ui.label("Cần theo dõi hoặc ưu tiên xử lý").classes(
                            "text-[13px] font-semibold text-[#161E54]/55 text-center"
                        )

def render_chart_card(title, icon, content_func):
    """Render chart inside a consistent card."""

    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-slate-100 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        with ui.row().classes(
            "relative w-full items-center justify-end px-7 py-5 border-b border-slate-100"
        ):
            ui.label(title).classes(
                "absolute left-1/2 -translate-x-1/2 "
                "text-[20px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
            )
            ui.icon(icon).classes("text-[28px] text-[#161E54]/55")

        with ui.column().classes("w-full px-5 py-5"):
            content_func()


# ==============================================================================
# PAGE 5: RISK SCORING ENGINE
# ==============================================================================

@ui.page("/risk-scoring")
def risk_scoring_page():
    """Risk Scoring Engine - Risk formula and scoring logic."""

    layout.render_sidebar(active_page="/risk-scoring")

    main_content = layout.render_page_container()

    with main_content:
        # ==========================================================
        # PAGE HEADER
        # ==========================================================
        with ui.row().classes(
            "relative w-full items-center justify-center mb-6 px-1 min-h-[64px]"
        ):
            with ui.column().classes(
                "absolute left-1/2 -translate-x-1/2 items-center gap-1"
            ):
                ui.label("Công Cụ Xếp Hạng Rủi Ro").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("Tổng hợp các tín hiệu rủi ro thành điểm ưu tiên bảo trì").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

        # ==========================================================
        # FORMULA CARD
        # ==========================================================
        render_formula_card()

        # ==========================================================
        # RISK FLAG WEIGHTS - 4 CARDS PER ROW
        # ==========================================================
        with ui.card().classes(
            "w-full rounded-[30px] bg-white border border-slate-100 "
            "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
        ):
            with ui.row().classes(
                "relative w-full items-center justify-end px-7 py-5 border-b border-slate-100"
            ):
                ui.label("Trọng Số Các Cờ Rủi Ro").classes(
                    "absolute left-1/2 -translate-x-1/2 "
                    "text-[22px] font-extrabold text-[#161E54] whitespace-nowrap"
                )
                ui.icon("tune").classes("text-[28px] text-[#161E54]/55")

            with ui.grid(columns=4).classes("w-full gap-6 px-7 py-6"):
                render_risk_weight_card(
                    title="High Stress Flag",
                    value="25%",
                    subtitle="Trạng thái động cơ căng tải",
                    icon="warning_amber",
                    color="#F16D34",
                    bg="#F16D34",
                )

                render_risk_weight_card(
                    title="Iso Anomaly",
                    value="25%",
                    subtitle="Bất thường thống kê",
                    icon="radar",
                    color="#F16D34",
                    bg="#FF986A",
                )

                render_risk_weight_card(
                    title="High Fuel Flag",
                    value="15%",
                    subtitle="Mức tiêu hao nhiên liệu cao",
                    icon="local_gas_station",
                    color="#FF986A",
                    bg="#FF986A",
                )

                render_risk_weight_card(
                    title="Throttle Flag",
                    value="10%",
                    subtitle="Hành vi tăng ga mạnh",
                    icon="speed",
                    color="#161E54",
                    bg="#BBE0EF",
                )

                render_risk_weight_card(
                    title="RPM Flag",
                    value="10%",
                    subtitle="Tải động cơ cao",
                    icon="settings",
                    color="#161E54",
                    bg="#BBE0EF",
                )

                render_risk_weight_card(
                    title="Brake Flag",
                    value="5%",
                    subtitle="Phanh gấp",
                    icon="front_hand",
                    color="#161E54",
                    bg="#BBE0EF",
                )

                render_risk_weight_card(
                    title="Accel Flag",
                    value="5%",
                    subtitle="Tăng tốc đột ngột",
                    icon="trending_up",
                    color="#161E54",
                    bg="#BBE0EF",
                )

                render_risk_weight_card(
                    title="Efficiency Flag",
                    value="5%",
                    subtitle="Hiệu suất nhiên liệu thấp",
                    icon="eco",
                    color="#161E54",
                    bg="#BBE0EF",
                )

        # ==========================================================
        # RISK FLAG THRESHOLDS TABLE
        # ==========================================================
        render_risk_score_table_card(
            title="Ngưỡng Cờ Rủi Ro",
            subtitle="Các ngưỡng dùng để bật/tắt từng cờ rủi ro trong công thức tính điểm",
            badge_text="THRESHOLDS",
            content_func=lambda: tables.render_risk_threshold_table(),
        )

        # ==========================================================
        # LOAD DATA FOR CHARTS
        # ==========================================================
        df_clean = data_service.load_df_clean()

        # ==========================================================
        # CHARTS
        # ==========================================================
        with ui.grid(columns=2).classes("w-full gap-6 mb-6"):
            render_chart_card(
                title="Phân Bố Điểm Rủi Ro Bản Ghi",
                icon="bar_chart",
                content_func=lambda: charts.render_plotly_chart(
                    charts.record_risk_score_histogram(df_clean)
                ).classes("w-full h-[360px]"),
            )

            render_chart_card(
                title="Phân Bố Mức Rủi Ro",
                icon="donut_large",
                content_func=lambda: charts.render_plotly_chart(
                    charts.risk_distribution_chart(
                        data_service.get_risk_distribution()
                    )
                ).classes("w-full h-[360px]"),
            )

        # ==========================================================
        # RISK LEVEL CLASSIFICATION TABLE
        # ==========================================================
        render_risk_score_table_card(
            title="Phân Loại Mức Rủi Ro",
            subtitle="Mapping điểm rủi ro sang các mức LOW / MEDIUM / HIGH",
            badge_text="CLASSIFICATION",
            content_func=lambda: tables.render_risk_level_mapping_table(),
        )

        # ==========================================================
        # CROSS-TABULATIONS
        # ==========================================================
        risk_by_status = data_service.get_risk_level_by_engine_status()
        risk_by_anom = data_service.get_risk_level_by_iso_anomaly()

        with ui.grid(columns=2).classes("w-full gap-6 mb-6"):
            render_risk_score_table_card(
                title="Rủi Ro Theo Trạng Thái Động Cơ",
                subtitle="Phân bố risk level theo trạng thái động cơ",
                badge_text="ENGINE STATUS",
                content_func=lambda: (
                    tables.render_dataframe_table(risk_by_status.head(10))
                    if risk_by_status is not None and not risk_by_status.empty
                    else ui.label(
                        "Không có dữ liệu risk level theo engine status."
                    ).classes(
                        "text-[14px] font-medium text-[#161E54]/55"
                    )
                ),
            )

            render_risk_score_table_card(
                title="Rủi Ro Theo Trạng Thái Bất Thường",
                subtitle="Phân bố risk level theo trạng thái anomaly",
                badge_text="ANOMALY STATUS",
                content_func=lambda: (
                    tables.render_dataframe_table(risk_by_anom.head(10))
                    if risk_by_anom is not None and not risk_by_anom.empty
                    else ui.label(
                        "Không có dữ liệu risk level theo anomaly status."
                    ).classes(
                        "text-[14px] font-medium text-[#161E54]/55"
                    )
                ),
            )