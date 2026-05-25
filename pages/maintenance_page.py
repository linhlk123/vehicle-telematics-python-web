from nicegui import ui

from services import data_service
from components import layout, tables


# ==============================================================================
# PAGE 8: MAINTENANCE QUEUE
# ==============================================================================
@ui.page("/maintenance")
def maintenance_page():
    """Maintenance Queue - Vehicle-level maintenance priority and alerts"""

    layout.render_sidebar(active_page="/maintenance")

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
                ui.label("Danh Sách Bảo Trì").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("Tổng hợp rủi ro theo phương tiện và ưu tiên bảo trì").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

        # ==========================================================
        # FILTER CARD
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
                ui.label("Bộ Lọc").classes(
                    "absolute left-1/2 -translate-x-1/2 "
                    "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
                )

                ui.icon("filter_alt").classes(
                    "text-[28px] text-[#161E54]/55"
                )

            ui.label("Tìm kiếm phương tiện hoặc lọc theo mức ưu tiên bảo trì").classes(
                "w-full text-center text-[13px] font-medium text-[#161E54]/55 pt-3"
            )

            with ui.row().classes("w-full items-end gap-5 px-7 py-6"):
                search_input = ui.input(
                    label="Tìm Kiếm ID Phương Tiện"
                ).props(
                    "borderless dense clearable"
                ).classes(
                    "flex-grow maintenance-inner-filter-field"
                )

                priority_select = ui.select(
                    label="Ưu Tiên",
                    options=[
                        None,
                        "NORMAL_MONITORING",
                        "NEED_ATTENTION",
                        "MAINTENANCE_ALERT",
                    ],
                    value=None,
                ).props(
                    "outlined dense clearable"
                ).classes(
                    "w-[280px] maintenance-filter-field"
                )

                table_container = ui.column().classes("w-full")

                def apply_filters():
                    search_term = search_input.value if search_input.value else None
                    priority = priority_select.value

                    queue_data = data_service.get_maintenance_queue(
                        priority=priority,
                        search=search_term,
                    )

                    table_container.clear()
                    with table_container:
                        tables.render_maintenance_queue_table(
                            queue_data,
                            max_rows=100,
                        )

                ui.button(
                    "Áp Dụng Bộ Lọc",
                    icon="search",
                    on_click=apply_filters,
                ).props(
                    "unelevated no-caps"
                ).classes(
                    "rounded-[18px] px-6 py-3 bg-[#161E54] text-white "
                    "font-extrabold shadow-[0_10px_24px_rgba(22,30,84,0.18)] "
                    "hover:bg-[#24306f]"
                )

        # ==========================================================
        # MAINTENANCE QUEUE TABLE
        # ==========================================================
        table_container = ui.column().classes("w-full")

        with table_container:
            queue_data = data_service.get_maintenance_queue()
            tables.render_maintenance_queue_table(
                queue_data,
                max_rows=50,
            )