from nicegui import ui

from components import layout, prediction_form


# ==============================================================================
# PAGE 7: PREDICTION PLAYGROUND
# ==============================================================================
@ui.page("/prediction")
def prediction_page():
    """Prediction Playground - Single and multi-model predictions"""

    layout.render_sidebar(active_page="/prediction")

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
                ui.label("Prediction Playground").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("Mô phỏng dự đoán mức rủi ro bảo trì từ dữ liệu vận hành").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

        # ==========================================================
        # INTRO / WARNING CARD
        # ==========================================================
        with ui.card().classes(
            "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
            "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
        ):
            with ui.row().classes(
                "w-full items-start gap-4 px-7 py-5 bg-[#BBE0EF]/20 "
                "border-b border-[#BBE0EF]/50"
            ):
                ui.icon("auto_awesome").classes(
                    "text-[32px] bg-white rounded-[18px] p-3 "
                    "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
                ).style("color: #161E54;")

                with ui.column().classes("gap-1 flex-1"):
                    ui.label("Prediction Simulation").classes(
                        "text-[22px] font-extrabold text-[#161E54]"
                    )
                    ui.label(
                        "Trang này dùng để nhập hoặc mô phỏng các đặc trưng vận hành của phương tiện, "
                        "sau đó chạy mô hình học máy để dự đoán risk level. Kết quả nên được hiểu là "
                        "hỗ trợ ra quyết định, không phải kết luận bảo trì tuyệt đối."
                    ).classes(
                        "text-[14px] font-semibold leading-relaxed text-[#161E54]/65"
                    )

                ui.label("ML INFERENCE").classes(
                    "px-4 py-2 rounded-full bg-[#161E54] text-white "
                    "text-[12px] font-extrabold tracking-wide"
                )

        # ==========================================================
        # PREDICTION FORM CARD
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
                ui.label("Vehicle Risk Prediction").classes(
                    "absolute left-1/2 -translate-x-1/2 "
                    "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
                )

                ui.icon("psychology").classes(
                    "text-[28px] text-[#161E54]/55"
                )

            ui.label("Nhập dữ liệu vận hành để dự đoán mức rủi ro của bản ghi hoặc phương tiện").classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

            # Form wrapper
            with ui.column().classes(
                "w-full px-7 pt-5 pb-7 gap-5"
            ):
                prediction_form.render_prediction_playground()