from nicegui import ui

from services import data_service
from components import layout, charts, tables

def render_kpi_card(title, value, subtitle, icon, icon_color="#161E54"):
    with ui.card().classes(
        "rounded-[30px] bg-white border border-slate-100 "
        "shadow-[0_10px_28px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        ui.label(title).classes(
            "w-full text-center text-[18px] font-extrabold text-[#161E54] "
            "pt-5 pb-3 border-b border-slate-100"
        )

        with ui.row().classes(
            "w-full items-center justify-center gap-5 px-6 pt-6 pb-2"
        ):
            ui.icon(icon).classes(
                f"text-[46px] text-[{icon_color}]"
            )
            ui.label(str(value)).classes(
                "text-[38px] leading-none font-extrabold text-[#161E54] tracking-wide"
            )

        ui.label(subtitle).classes(
            "w-full text-center text-[14px] font-semibold text-[#161E54]/60 pb-6"
        )
# ==============================================================================
# PAGE 1: OVERVIEW
# ==============================================================================
@ui.page("/")
def overview_page():
    """Overview page - Premium Admin Dashboard"""

    layout.render_sidebar(active_page="/")

    main_content = layout.render_page_container()

    with main_content:
        # ==========================================================
        # PAGE HEADER
        # ==========================================================
        with ui.row().classes(
            "relative w-full items-center justify-center mb-6 px-1 min-h-[64px]"
        ):
            # Center title
            with ui.column().classes(
                "absolute left-1/2 -translate-x-1/2 items-center gap-1"
            ):
                ui.label("Bảng Điều Khiển").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("Tổng Quan Về Trí Tuệ Rủi Ro Viễn Thám Xe Cộ").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

            # Right actions
            with ui.row().classes(
                "absolute right-0 items-center gap-3"
            ):
                ui.input(placeholder="Tìm kiếm...").props(
                    "outlined dense"
                ).classes(
                    "w-64 bg-white rounded-xl shadow-sm border border-slate-200"
                )

                ui.button(icon="notifications").props(
                    "flat round dense"
                ).classes(
                    "text-[#161E54]/70 hover:bg-[#BBE0EF]/35"
                )

                ui.button(icon="person").props(
                    "flat round dense"
                ).classes(
                    "text-[#161E54]/70 hover:bg-[#BBE0EF]/35"
                )
        # ==========================================================
        # KPI CARDS ROW - Premium Admin Dashboard Style
        # ==========================================================
        summary = data_service.get_dashboard_summary()

        with ui.grid(columns=4).classes("w-full gap-6 mb-6"):
            render_kpi_card(
                title="Tổng Số Xe",
                value=summary["total_vehicles"],
                subtitle="Đơn vị đội xe hoạt động",
                icon="directions_car",
                icon_color="#161E54",
            )

            render_kpi_card(
                title="Tổng Số Bản Ghi",
                value=summary["total_records"],
                subtitle="Nhật ký cảm biến được xử lý",
                icon="analytics",
                icon_color="#161E54",
            )

            render_kpi_card(
                title="Tỷ Lệ Rủi Ro Cao",
                value=summary["high_risk_rate"],
                subtitle="Cần chú ý",
                icon="warning",
                icon_color="#F16D34",
            )

            render_kpi_card(
                title="Cảnh Báo Bảo Trì",
                value=summary["maintenance_alerts"],
                subtitle="Xe cần kiểm tra",
                icon="construction",
                icon_color="#FF986A",
            )
        # ==========================================================
        # ROW 1: RISK DISTRIBUTION + FLEET RISK RANKING
        # ==========================================================
        with ui.grid(columns=2).classes("w-full gap-6 mb-6"):
            risk_dist = data_service.get_risk_distribution()
            fig_risk = charts.risk_distribution_chart(risk_dist)
            charts.render_chart_card(
                title="Phân Bố Mức Độ Rủi Ro",
                fig=fig_risk,
                height=360,
            )

            fleet_risk = data_service.get_fleet_risk()
            fig_fleet = charts.fleet_risk_chart(fleet_risk)
            charts.render_chart_card(
                title="Xếp Hạng Rủi Ro Đội Xe",
                fig=fig_fleet,
                action_text="Đội Xe Hàng Đầu",
                height=360,
            )


        # ==========================================================
        # ROW 2: VEHICLE TYPE RISK + QUICK ACTIONS
        # Left: 7 parts | Right: 3 parts
        # ==========================================================
        with ui.grid(columns=10).classes("w-full gap-6 mb-6 items-stretch"):
            # ------------------------------------------------------
            # VEHICLE TYPE RISK - LEFT / 7 COLUMNS
            # ------------------------------------------------------
            with ui.column().classes("col-span-7 w-full h-full"):
                vehicle_risk = data_service.get_vehicle_type_risk()
                fig_vehicle = charts.vehicle_type_risk_chart(vehicle_risk)
                charts.render_chart_card(
                    title="Điểm Rủi Ro Trung Bình Theo Loại Xe",
                    fig=fig_vehicle,
                    height=360,
                )

            # ------------------------------------------------------
            # QUICK ACTIONS - RIGHT / 3 COLUMNS
            # ------------------------------------------------------
            with ui.card().classes(
                "col-span-3 w-full h-full rounded-[30px] bg-white border border-slate-100 "
                "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
            ):
                # Header
                with ui.row().classes(
                    "relative w-full items-center justify-end px-6 py-5 border-b border-slate-100"
                ):
                    ui.label("Hành Động Nhanh").classes(
                        "absolute left-1/2 -translate-x-1/2 text-[21px] font-extrabold text-[#161E54]"
                    )
                    ui.icon("bolt").classes(
                        "text-[26px] text-[#F16D34] bg-[#F16D34]/10 rounded-[14px] p-2"
                    )

                ui.label("Mở các mô-đun chính một cách nhanh chóng").classes(
                    "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
                )

                # Actions fill full remaining height
                with ui.column().classes("w-full flex-1 gap-4 px-5 py-5 h-full justify-between"):
                    # Prediction
                    with ui.card().classes(
                        "w-full flex-1 rounded-[24px] bg-[#BBE0EF]/28 border border-[#BBE0EF]/70 "
                        "shadow-none p-0 cursor-pointer hover:bg-[#BBE0EF]/45 "
                        "transition-all duration-200"
                    ).on("click", lambda: ui.navigate.to("/prediction")):
                        with ui.column().classes("w-full h-full justify-center px-5 py-4"):
                            with ui.row().classes("w-full items-center gap-4"):
                                ui.icon("auto_awesome").classes(
                                    "text-[30px] text-[#161E54] bg-white rounded-[16px] p-3 "
                                    "shadow-[0_8px_18px_rgba(22,30,84,0.08)]"
                                )

                                with ui.column().classes("gap-1 flex-1"):
                                    ui.label("Công Cụ Dự Đoán").classes(
                                        "text-[18px] font-extrabold text-[#161E54]"
                                    )
                                    ui.label("Dự đoán rủi ro xe đơn và đa mô hình").classes(
                                        "text-[12px] font-medium text-[#161E54]/60 leading-snug"
                                    )

                                ui.icon("arrow_forward_ios").classes(
                                    "text-[18px] text-[#161E54]/45"
                                )

                            # ui.label("Run prediction workflows for vehicle risk scoring and model-based evaluation.").classes(
                            #     "text-[12px] text-[#161E54]/55 leading-relaxed mt-3 pl-[58px]"
                            # )

                    # Model Lab
                    with ui.card().classes(
                        "w-full flex-1 rounded-[24px] bg-[#F16D34]/9 border border-[#F16D34]/20 "
                        "shadow-none p-0 cursor-pointer hover:bg-[#F16D34]/14 "
                        "transition-all duration-200"
                    ).on("click", lambda: ui.navigate.to("/model-lab")):
                        with ui.column().classes("w-full h-full justify-center px-5 py-4"):
                            with ui.row().classes("w-full items-center gap-4"):
                                ui.icon("smart_toy").classes(
                                    "text-[30px] text-[#F16D34] bg-white rounded-[16px] p-3 "
                                    "shadow-[0_8px_18px_rgba(22,30,84,0.08)]"
                                )

                                with ui.column().classes("gap-1 flex-1"):
                                    ui.label("Các Mô Hình ML").classes(
                                        "text-[18px] font-extrabold text-[#161E54]"
                                    )
                                    ui.label(f"Mô hình tốt nhất: {summary['best_model']}").classes(
                                        "text-[12px] font-medium text-[#161E54]/60 leading-snug"
                                    )

                                ui.icon("arrow_forward_ios").classes(
                                    "text-[18px] text-[#161E54]/45"
                                )

                            # ui.label("Compare algorithms, inspect metrics, and review current best-performing models.").classes(
                            #     "text-[12px] text-[#161E54]/55 leading-relaxed mt-3 pl-[58px]"
                            # )

                    # Reports
                    with ui.card().classes(
                        "w-full flex-1 rounded-[24px] bg-[#FF986A]/12 border border-[#FF986A]/25 "
                        "shadow-none p-0 cursor-pointer hover:bg-[#FF986A]/18 "
                        "transition-all duration-200"
                    ).on("click", lambda: ui.notify("Export feature coming soon", type="info")):
                        with ui.column().classes("w-full h-full justify-center px-5 py-4"):
                            with ui.row().classes("w-full items-center gap-4"):
                                ui.icon("bar_chart").classes(
                                    "text-[30px] text-[#FF986A] bg-white rounded-[16px] p-3 "
                                    "shadow-[0_8px_18px_rgba(22,30,84,0.08)]"
                                )

                                with ui.column().classes("gap-1 flex-1"):
                                    ui.label("Báo Cáo").classes(
                                        "text-[18px] font-extrabold text-[#161E54]"
                                    )
                                    ui.label("Tóm tắt đội xe & lịch bảo trì").classes(
                                        "text-[12px] font-medium text-[#161E54]/60 leading-snug"
                                    )

                                ui.icon("arrow_forward_ios").classes(
                                    "text-[18px] text-[#161E54]/45"
                                )

                            # ui.label("Generate operational summaries and export risk and maintenance reporting outputs.").classes(
                            #     "text-[12px] text-[#161E54]/55 leading-relaxed mt-3 pl-[58px]"
                            # )
        # ==========================================================
        # ROW 3: DASHBOARD SUMMARY - FULL WIDTH
        # Designed like KPI cards row
        # ==========================================================
        with ui.card().classes(
            "w-full rounded-[30px] bg-white border border-slate-100 "
            "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
        ):
            # Header
            with ui.row().classes(
                "relative w-full items-center justify-end px-7 py-5 border-b border-slate-100"
            ):
                ui.label("Tóm Tắt Bảng Điều Khiển").classes(
                    "absolute left-1/2 -translate-x-1/2 text-[22px] font-extrabold text-[#161E54]"
                )

                ui.label("THÔNG TIN CHI TIẾT").classes(
                    "px-4 py-2 rounded-full text-[12px] font-extrabold tracking-wide "
                    "bg-[#BBE0EF]/55 text-[#161E54]"
                )

            ui.label("Thông tin về tình trạng đội xe và tổng quan bảo trì hiện tại").classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

            # Summary KPI mini cards
            with ui.grid(columns=4).classes("w-full gap-6 px-7 py-6"):
                # Anomaly Rate
                with ui.card().classes(
                    "rounded-[28px] bg-[#BBE0EF]/22 border border-[#BBE0EF]/70 shadow-none p-0 overflow-hidden"
                ):
                    ui.label("Tỷ Lệ Bất Thường").classes(
                        "w-full text-center text-[16px] font-extrabold text-[#161E54] pt-5 pb-3 border-b border-[#BBE0EF]/60"
                    )

                    with ui.row().classes("w-full items-center justify-center gap-5 px-5 pt-6 pb-2"):
                        ui.icon("hub").classes("text-[42px] text-[#161E54]")
                        ui.label(str(summary["anomaly_rate"])).classes(
                            "text-[36px] leading-none font-extrabold text-[#161E54]"
                        )

                    ui.label("Các mô hình lái xe bất thường").classes(
                        "w-full text-center text-[13px] font-semibold text-[#161E54]/55 pb-6"
                    )

                # High Risk Rate
                with ui.card().classes(
                    "rounded-[28px] bg-[#F16D34]/8 border border-[#F16D34]/25 shadow-none p-0 overflow-hidden"
                ):
                    ui.label("Tỷ Lệ Rủi Ro Cao").classes(
                        "w-full text-center text-[16px] font-extrabold text-[#161E54] pt-5 pb-3 border-b border-[#F16D34]/20"
                    )

                    with ui.row().classes("w-full items-center justify-center gap-5 px-5 pt-6 pb-2"):
                        ui.icon("warning_amber").classes("text-[42px] text-[#F16D34]")
                        ui.label(str(summary["high_risk_rate"])).classes(
                            "text-[36px] leading-none font-extrabold text-[#161E54]"
                        )

                    ui.label("Bản ghi cần kiểm tra").classes(
                        "w-full text-center text-[13px] font-semibold text-[#161E54]/55 pb-6"
                    )

                # Maintenance Alerts
                with ui.card().classes(
                    "rounded-[28px] bg-[#FF986A]/10 border border-[#FF986A]/25 shadow-none p-0 overflow-hidden"
                ):
                    ui.label("Cảnh Báo Bảo Trì").classes(
                        "w-full text-center text-[16px] font-extrabold text-[#161E54] pt-5 pb-3 border-b border-[#FF986A]/25"
                    )

                    with ui.row().classes("w-full items-center justify-center gap-5 px-5 pt-6 pb-2"):
                        ui.icon("home_repair_service").classes("text-[42px] text-[#FF986A]")
                        ui.label(str(summary["maintenance_alerts"])).classes(
                            "text-[36px] leading-none font-extrabold text-[#161E54]"
                        )

                    ui.label("Xe cần chú ý").classes(
                        "w-full text-center text-[13px] font-semibold text-[#161E54]/55 pb-6"
                    )

                # Best Model
                with ui.card().classes(
                    "rounded-[28px] bg-[#161E54]/5 border border-[#161E54]/10 shadow-none p-0 overflow-hidden"
                ):
                    ui.label("Mô Hình Tốt Nhất").classes(
                        "w-full text-center text-[16px] font-extrabold text-[#161E54] pt-5 pb-3 border-b border-[#161E54]/10"
                    )

                    with ui.column().classes("w-full items-center justify-center px-5 pt-6 pb-2 gap-3"):
                        ui.icon("emoji_events").classes("text-[42px] text-[#161E54]")
                        ui.label(str(summary["best_model"])).classes(
                            "text-[20px] leading-tight text-center font-extrabold text-[#161E54]"
                        )
                        ui.label(f"F1: {summary['best_f1']}").classes(
                            "text-[14px] font-extrabold text-[#F16D34]"
                        )

                    ui.label("Mô hình Machine Learning được chọn").classes(
                        "w-full text-center text-[13px] font-semibold text-[#161E54]/55 pb-6"
                    )

            # Footer navigation buttons
            with ui.row().classes("w-full gap-5 px-7 pb-7"):
                ui.button(
                    "Hàng Đợi Bảo Trì",
                    icon="playlist_add_check",
                    on_click=lambda: ui.navigate.to("/maintenance")
                ).classes(
                    "flex-1 rounded-[20px] bg-[#BBE0EF]/55 hover:bg-[#BBE0EF]/80 text-[#161E54] font-extrabold py-3 shadow-none"
                )

                ui.button(
                    "Công Cụ Xếp Hạng Rủi Ro",
                    icon="speed",
                    on_click=lambda: ui.navigate.to("/risk-scoring")
                ).classes(
                    "flex-1 rounded-[20px] bg-[#161E54] hover:bg-[#161E54]/90 text-white font-extrabold py-3 shadow-none"
                )

        # ==========================================================
        # RECENT HIGH-RISK RECORDS
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
                ui.label("Bản Ghi Rủi Ro Cao Gần Đây").classes(
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

            ui.label("Bản ghi mới nhất có tín hiệu rủi ro cao và ưu tiên bảo trì").classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

            # Table wrapper
            with ui.column().classes(
                "w-full px-6 pt-5 pb-6 recent-risk-table-wrapper"
            ):
                top_anomalies = data_service.get_top_anomalies(limit=10)
                tables.render_top_anomaly_table(top_anomalies, max_rows=10)