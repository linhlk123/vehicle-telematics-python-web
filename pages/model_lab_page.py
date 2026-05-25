from nicegui import ui

from services import data_service
from components import layout, charts, tables


# ==============================================================================
# HELPERS
# ==============================================================================

def render_model_table_card(title, subtitle, content_func, badge_text=None):
    """Render table card with app-data-table style."""

    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
    ):
        with ui.row().classes(
            "relative w-full items-center justify-end px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            ui.label(title).classes(
                "absolute left-1/2 -translate-x-1/2 "
                "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
            )

            if badge_text:
                ui.label(badge_text).classes(
                    "rounded-full px-4 py-2 bg-white/70 text-[#161E54] "
                    "font-extrabold text-[11px] tracking-wide shadow-sm"
                )

        if subtitle:
            ui.label(subtitle).classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

        with ui.column().classes("w-full px-6 pt-5 pb-6 app-data-table"):
            content_func()


def render_model_chart_card(title, subtitle, icon, content_func):
    """Render chart card."""

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

        if subtitle:
            ui.label(subtitle).classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

        with ui.column().classes("w-full px-5 py-5"):
            content_func()


def render_selected_model_card(best_model):
    """Render selected model explanation card."""

    model_name = best_model.get("model", "Unknown Model")
    accuracy = best_model.get("accuracy", 0)
    f1_macro = best_model.get("f1_macro", 0)
    f1_weighted = best_model.get("f1_weighted", 0)

    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
    ):
        with ui.row().classes(
            "w-full items-center justify-between px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon("emoji_events").classes(
                    "text-[34px] bg-white rounded-[18px] p-3 "
                    "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
                ).style("color: #F16D34;")

                with ui.column().classes("gap-1"):
                    ui.label(f"Selected Model: {model_name}").classes(
                        "text-[22px] font-extrabold text-[#161E54]"
                    )
                    ui.label("Mô hình có F1 Macro tốt nhất và phù hợp cho phân loại risk level.").classes(
                        "text-[13px] font-medium text-[#161E54]/55"
                    )

            ui.label("BEST MODEL").classes(
                "px-4 py-2 rounded-full bg-[#161E54] text-white "
                "text-[12px] font-extrabold tracking-wide"
            )

        with ui.grid(columns=3).classes("w-full gap-5 px-7 py-6"):
            render_model_metric_box(
                title="Accuracy",
                value=f"{accuracy:.4f}",
                subtitle="Độ chính xác tổng thể",
                icon="verified",
                color="#161E54",
                bg="#BBE0EF",
            )

            render_model_metric_box(
                title="F1 Macro",
                value=f"{f1_macro:.4f}",
                subtitle="Chỉ số chính để chọn model",
                icon="leaderboard",
                color="#F16D34",
                bg="#F16D34",
            )

            render_model_metric_box(
                title="F1 Weighted",
                value=f"{f1_weighted:.4f}",
                subtitle="Hiệu năng có xét phân bố lớp",
                icon="analytics",
                color="#FF986A",
                bg="#FF986A",
            )

        with ui.grid(columns=3).classes("w-full gap-5 px-7 pb-7"):
            render_reason_box(
                title="Không bỏ sót rủi ro cao",
                content="Mô hình hạn chế việc phân loại HIGH_RISK thành LOW_RISK, giúp tránh bỏ sót cảnh báo bảo trì quan trọng.",
                icon="warning_amber",
                color="#F16D34",
                bg="#F16D34",
            )

            render_reason_box(
                title="Phù hợp dữ liệu bảng",
                content="Hist Gradient Boosting hoạt động tốt trên dữ liệu tabular telematics với nhiều đặc trưng kỹ thuật.",
                icon="table_chart",
                color="#161E54",
                bg="#BBE0EF",
            )

            render_reason_box(
                title="Cân bằng giữa các lớp",
                content="Model có hiệu năng ổn định trên các mức LOW, MEDIUM và HIGH risk.",
                icon="balance",
                color="#FF986A",
                bg="#FF986A",
            )


def render_model_metric_box(title, value, subtitle, icon, color="#161E54", bg="#BBE0EF"):
    with ui.card().classes(
        "rounded-[24px] bg-white border border-slate-100 "
        "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
    ):
        with ui.row().classes("w-full items-center gap-4 px-5 py-5"):
            ui.icon(icon).classes(
                "text-[32px] rounded-[16px] p-3"
            ).style(
                f"color: {color}; background: {bg}22;"
            )

            with ui.column().classes("gap-1"):
                ui.label(title).classes(
                    "text-[13px] font-extrabold uppercase tracking-wide text-[#161E54]/45"
                )
                ui.label(value).classes(
                    "text-[28px] font-extrabold text-[#161E54]"
                )
                ui.label(subtitle).classes(
                    "text-[12px] font-semibold text-[#161E54]/55"
                )


def render_reason_box(title, content, icon, color="#161E54", bg="#BBE0EF"):
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


def render_warning_note_card():
    """Render MLP note card."""

    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#FF986A]/35 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
    ):
        with ui.row().classes(
            "w-full items-start gap-4 px-7 py-5 bg-[#FF986A]/10 border-b border-[#FF986A]/20"
        ):
            ui.icon("science").classes(
                "text-[32px] bg-white rounded-[18px] p-3 "
                "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
            ).style("color: #F16D34;")

            with ui.column().classes("gap-1 flex-1"):
                ui.label("Mạng Neural MLP - Thử Nghiệm").classes(
                    "text-[20px] font-extrabold text-[#161E54]"
                )
                ui.label(
                    "MLP chưa được chọn làm mô hình chính. Với dữ liệu telematics dạng bảng, "
                    "các mô hình truyền thống như Hist Gradient Boosting và Random Forest đã đạt kết quả mạnh, "
                    "dễ kiểm soát và dễ giải thích hơn. Deep learning có thể được xem như hướng mở rộng trong tương lai."
                ).classes(
                    "text-[14px] font-semibold leading-relaxed text-[#161E54]/65"
                )


# ==============================================================================
# PAGE 6: ML MODEL LAB
# ==============================================================================

@ui.page("/model-lab")
def model_lab_page():
    """ML Model Lab - Compare all trained models."""

    layout.render_sidebar(active_page="/model-lab")

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
                ui.label("Các Mô Hình ML ML").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("So sánh hiệu năng các mô hình dự đoán mức rủi ro bảo trì").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

        # ==========================================================
        # LOAD DATA
        # ==========================================================
        model_results = data_service.load_model_results()

        if model_results is None or model_results.empty:
            ui.label("Không tìm thấy dữ liệu kết quả mô hình.").classes(
                "text-[15px] font-semibold text-[#161E54]/60"
            )
            return

        # ==========================================================
        # MODEL LEADERBOARD TABLE
        # ==========================================================
        render_model_table_card(
            title="Bảng Xếp Hạng Mô Hình",
            subtitle="Bảng xếp hạng mô hình theo Accuracy, F1 Macro và F1 Weighted",
            badge_text="MODEL RESULTS",
            content_func=lambda: tables.render_model_leaderboard_table(model_results),
        )

        # ==========================================================
        # MODEL METRICS CHARTS
        # ==========================================================
        with ui.grid(columns=2).classes("w-full gap-6 mb-6"):
            render_model_chart_card(
                title="So Sánh F1 Macro",
                subtitle="So sánh F1 Macro giữa các mô hình",
                icon="leaderboard",
                content_func=lambda: charts.render_plotly_chart(
                    charts.model_metric_chart(model_results)
                ).classes("w-full h-[360px]"),
            )

            render_model_chart_card(
                title="So Sánh Độ Chính Xác",
                subtitle="So sánh Accuracy giữa các mô hình",
                icon="verified",
                content_func=lambda: charts.render_plotly_chart(
                    charts.accuracy_comparison_chart(model_results)
                ).classes("w-full h-[360px]"),
            )

        # ==========================================================
        # BEST MODEL DETAIL
        # ==========================================================
        best_model = model_results.loc[model_results["f1_macro"].idxmax()]
        render_selected_model_card(best_model)

        # ==========================================================
        # CONFUSION MATRIX
        # ==========================================================
        with ui.card().classes(
            "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
            "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
        ):
            with ui.row().classes(
                "relative w-full items-center justify-end px-7 py-5 "
                "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
            ):
                ui.label("Ma Trận Nhầm Lẫn").classes(
                    "absolute left-1/2 -translate-x-1/2 "
                    "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
                )

                ui.label("MÔ HÌNH TỐT NHẤT").classes(
                    "rounded-full px-4 py-2 bg-white/70 text-[#161E54] "
                    "font-extrabold text-[11px] tracking-wide shadow-sm"
                )

            ui.label("Ma trận nhầm lẫn của mô hình được chọn, dùng để kiểm tra các lỗi phân loại giữa LOW, MEDIUM và HIGH risk.").classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

            with ui.column().classes(
                "w-full px-6 pt-5 pb-6 items-center"
            ):
                fig_cm = charts.confusion_matrix_chart()

                # Nếu chart function đã đẹp sẵn, chỉ cần render.
                # Card đã xử lý layout, padding và background.
                charts.render_plotly_chart(fig_cm).classes("w-full h-[460px]")
