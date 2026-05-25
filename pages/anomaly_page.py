from nicegui import ui

from services import data_service
from components import layout, charts, tables, cards


# ==============================================================================
# PAGE 4: ANOMALY OBSERVATORY
# ==============================================================================
@ui.page("/anomaly")
def anomaly_page():
    """Anomaly Observatory - Isolation Forest anomaly detection analysis"""

    layout.render_sidebar(active_page="/anomaly")

    main_content = layout.render_page_container()

    with main_content:
        # ==========================================================
        # PAGE HEADER - CENTERED
        # ==========================================================
        with ui.row().classes(
            "relative w-full items-center justify-center mb-6 px-1 min-h-[64px]"
        ):
            with ui.column().classes(
                "absolute left-1/2 -translate-x-1/2 items-center gap-1"
            ):
                ui.label("Tính Toán Bất Thường").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("Phân tích các mẫu vận hành bất thường bằng Isolation Forest").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

        # ==========================================================
        # LOAD DATA
        # ==========================================================
        df_clean = data_service.load_df_clean()

        anomaly_count = 0
        anomaly_rate = 0

        if df_clean is not None and len(df_clean) > 0 and "iso_anomaly" in df_clean.columns:
            anomaly_count = int(df_clean["iso_anomaly"].sum())
            anomaly_rate = anomaly_count / len(df_clean) * 100

        # ==========================================================
        # SUMMARY STATS
        # ==========================================================
        with ui.grid(columns=4).classes("w-full gap-6 mb-6"):
            cards.render_metric_card("Tổng Số Bất Thường", int(anomaly_count), tone="amber")
            cards.render_metric_card("Tỷ Lệ Bất Thường", f"{anomaly_rate:.2f}%", tone="amber")
            cards.render_metric_card("Tỷ Lệ Nhiễm", "5%", tone="cyan")
            cards.render_metric_card("Thuật Toán", "Isolation Forest", tone="violet")

        # ==========================================================
        # ANOMALY ANALYSIS - 5 : 2.5 : 2.5
        # ==========================================================
        with ui.card().classes(
            "w-full rounded-[30px] bg-white border border-slate-100 "
            "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
        ):
            # Section header
            with ui.row().classes(
                "relative w-full items-center justify-end px-7 py-5 border-b border-slate-100"
            ):
                ui.label("Phân Tích Bất Thường").classes(
                    "absolute left-1/2 -translate-x-1/2 text-[22px] font-extrabold text-[#161E54]"
                )
                ui.icon("query_stats").classes(
                    "text-[28px] text-[#161E54]/55"
                )

            # Custom 5 : 2.5 : 2.5 layout
            with ui.element("div").classes("w-full gap-6 px-6 py-6").style(
                "display: grid; grid-template-columns: 5fr 2.5fr 2.5fr; gap: 24px;"
            ):
                # --------------------------------------------------
                # Chart 1: By Vehicle Type - 5 parts
                # --------------------------------------------------
                with ui.card().classes(
                    "rounded-[26px] bg-white border border-[#BBE0EF]/60 "
                    "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
                ):
                    with ui.row().classes(
                        "relative w-full items-center justify-end px-5 py-4 border-b border-[#BBE0EF]/40"
                    ):
                        ui.label("Theo loại phương tiện").classes(
                            "absolute left-1/2 -translate-x-1/2 text-[15px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
                        )
                        ui.icon("directions_car").classes(
                            "text-[24px] text-[#161E54]/55"
                        )

                    with ui.column().classes("w-full px-4 py-4"):
                        anomaly_by_vtype = data_service.get_anomaly_by_vehicle_type()
                        fig_vtype = charts.anomaly_by_vehicle_type_chart(anomaly_by_vtype)
                        charts.render_plotly_chart(fig_vtype).classes("w-full h-[330px]")

                # --------------------------------------------------
                # Chart 2: By Road Class - 2.5 parts
                # --------------------------------------------------
                with ui.card().classes(
                    "rounded-[26px] bg-white border border-[#BBE0EF]/60 "
                    "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
                ):
                    with ui.row().classes(
                        "relative w-full items-center justify-end px-5 py-4 border-b border-[#BBE0EF]/40"
                    ):
                        ui.label("Theo loại đường").classes(
                            "absolute left-1/2 -translate-x-1/2 "
                            "text-[15px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
                        )
                        ui.icon("route").classes(
                            "text-[24px] text-[#161E54]/55"
                        )

                    with ui.column().classes("w-full px-4 py-4"):
                        anomaly_by_road = data_service.get_anomaly_by_road_class()
                        fig_road = charts.anomaly_by_road_class_chart(anomaly_by_road)
                        charts.render_plotly_chart(fig_road).classes("w-full h-[330px]")

                # --------------------------------------------------
                # Chart 3: By Engine Status - 2.5 parts
                # --------------------------------------------------
                with ui.card().classes(
                    "rounded-[26px] bg-white border border-[#BBE0EF]/60 "
                    "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
                ):
                    with ui.row().classes(
                        "relative w-full items-center justify-end px-5 py-4 border-b border-[#BBE0EF]/40"
                    ):
                        ui.label("Theo trạng thái động cơ").classes(
                            "absolute left-1/2 -translate-x-1/2 "
                            "text-[15px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
                        )
                        ui.icon("monitor_heart").classes(
                            "text-[24px] text-[#161E54]/55"
                        )

                    with ui.column().classes("w-full px-4 py-4"):
                        anomaly_by_status = data_service.get_anomaly_by_engine_status()

                        if anomaly_by_status is not None and not anomaly_by_status.empty:
                            status_df = anomaly_by_status.rename(
                                columns={
                                    "engine_status": "vehicle_type",
                                    "anomaly_rate_pct": "anomaly_rate_pct",
                                }
                            )
                            fig_status = charts.anomaly_by_vehicle_type_chart(status_df)
                            charts.render_plotly_chart(fig_status).classes("w-full h-[330px]")
                        else:
                            ui.label("Không có dữ liệu anomaly theo trạng thái động cơ.").classes(
                                "text-[14px] font-medium text-[#161E54]/55"
                            )

        # ==========================================================
        # TOP ANOMALOUS RECORDS
        # ==========================================================
        with ui.card().classes(
            "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
            "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
        ):
            # Header
            with ui.row().classes(
                "relative w-full items-center justify-end px-7 py-5 "
                "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
            ):
                ui.label("Các Bản Ghi Bất Thường Hàng Đầu").classes(
                    "absolute left-1/2 -translate-x-1/2 "
                    "text-[22px] font-extrabold text-[#161E54]"
                )

                ui.button(
                    "Xem Tất Cả",
                    on_click=lambda: ui.navigate.to("/maintenance")
                ).props(
                    "flat dense no-caps"
                ).classes(
                    "rounded-full px-4 py-2 bg-white/70 text-[#161E54] "
                    "font-extrabold hover:bg-white shadow-sm"
                )

            ui.label("Các bản ghi bất thường nhất theo anomaly score và risk signal").classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

            # Table wrapper
            with ui.column().classes(
                "w-full px-6 pt-5 pb-6 recent-risk-table-wrapper"
            ):
                top_anomalies = data_service.get_top_anomalies(limit=10)
                tables.render_top_anomaly_table(top_anomalies, max_rows=10)