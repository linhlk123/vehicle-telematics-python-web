from nicegui import ui

from components import layout, pipeline


# ==============================================================================
# PAGE 2: ALGORITHM PIPELINE
# ==============================================================================
@ui.page("/pipeline")
def algorithm_pipeline_page():
    """Algorithm Pipeline - Interactive visualization of the complete data pipeline"""

    layout.render_sidebar(active_page="/pipeline")

    main_content = layout.render_page_container()

    with main_content:
        # Page Header
        with ui.row().classes(
            "relative w-full items-center justify-center mb-6 px-1 min-h-[64px]"
        ):
            with ui.column().classes(
                "absolute left-1/2 -translate-x-1/2 items-center gap-1"
            ):
                ui.label("Pipeline").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("Quy trình xử lý dữ liệu và mô hình dự đoán rủi ro bảo trì").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

        # Chỉ gọi một hàm thôi, vì render_algorithm_pipeline()
        # đã gọi lại render_pipeline_overview()
        pipeline.render_algorithm_pipeline()