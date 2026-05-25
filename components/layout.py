"""
Layout Components - Reusable layout structure and navigation
Clean admin dashboard layout with collapsible sidebar
"""

from nicegui import ui


BRAND_NAVY = "#161E54"
BRAND_BLUE = "#BBE0EF"
BRAND_ORANGE = "#F16D34"
BRAND_LIGHT_ORANGE = "#FF986A"


def render_sidebar(active_page="/"):
    """Render a clean collapsible sidebar with Material Icons."""

    nav_items = [
        {"icon": "dashboard", "label": " Tổng Quan", "page": "/"},
        {"icon": "account_tree", "label": " Pipeline", "page": "/pipeline"},
        {"icon": "track_changes", "label": " Gom Cụm", "page": "/clustering"},
        {"icon": "travel_explore", "label": " Tính Toán Bất Thường", "page": "/anomaly"},
        {"icon": "speed", "label": " Tính Điểm Risk", "page": "/risk-scoring"},
        {"icon": "model_training", "label": " Mô Hình Machine Learnings", "page": "/model-lab"},
        {"icon": "auto_awesome", "label": " Dự Đoán", "page": "/prediction"},
        {"icon": "home_repair_service", "label": " Danh Sách Bảo Trì", "page": "/maintenance"},
    ]

    # Drawer
    drawer = ui.left_drawer(value=True).props("bordered").classes(
        "bg-white text-[#161E54] w-[280px] "
        "border-r border-slate-100 shadow-[8px_0_30px_rgba(22,30,84,0.06)]"
    )

    # Floating open/close button
    ui.button(
        icon="menu",
        on_click=lambda: drawer.toggle()
    ).props(
        "flat round dense"
    ).classes(
        "fixed top-4 left-4 z-50 bg-white text-[#161E54] "
        "shadow-[0_8px_22px_rgba(22,30,84,0.12)] "
        "border border-slate-100"
    )

    with drawer:
        # Brand section
        with ui.column().classes(
            "w-full px-5 pt-5 pb-4 border-b border-slate-100"
        ):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.row().classes("items-center gap-3"):
                    ui.icon("directions_car").classes(
                        "text-[28px] text-[#161E54] bg-[#BBE0EF]/55 "
                        "rounded-[16px] p-3"
                    )

                    with ui.column().classes("gap-0"):
                        ui.label("Telematics").classes(
                            "text-[19px] leading-tight font-extrabold text-[#161E54]"
                        )
                        ui.label("Risk Intelligence").classes(
                            "text-[12px] font-semibold text-[#161E54]/55"
                        )

                ui.button(
                    icon="chevron_left",
                    on_click=lambda: drawer.toggle()
                ).props(
                    "flat round dense"
                ).classes(
                    "text-[#161E54]/60 hover:bg-[#BBE0EF]/35"
                )

        # Navigation section
        with ui.column().classes("w-full px-4 py-5 gap-2"):
            ui.label("Điều Hướng").classes(
                "px-3 pb-2 text-[11px] font-extrabold uppercase tracking-[0.18em] "
                "text-[#161E54]/35"
            )

            for item in nav_items:
                is_active = item["page"] == active_page

                if is_active:
                    button_classes = (
                        "w-full h-[48px] justify-start rounded-[18px] "
                        "bg-[#161E54] text-white "
                        "shadow-[0_10px_24px_rgba(22,30,84,0.18)] "
                        "font-bold text-[14px] px-4"
                    )
                else:
                    button_classes = (
                        "w-full h-[48px] justify-start rounded-[18px] "
                        "bg-transparent text-[#161E54]/70 "
                        "hover:bg-[#BBE0EF]/30 hover:text-[#161E54] "
                        "font-bold text-[14px] px-4"
                    )

                ui.button(
                    item["label"],
                    icon=item["icon"],
                    on_click=lambda p=item["page"]: ui.navigate.to(p),
                ).props(
                    "flat no-caps align=left"
                ).classes(button_classes)

        # Bottom panel
        with ui.column().classes("w-full mt-auto px-4 pb-5"):
            with ui.column().classes(
                "w-full rounded-[24px] bg-[#BBE0EF]/35 border border-[#BBE0EF]/70 "
                "px-4 py-4 gap-2"
            ):
                ui.label("Trạng Thái Hệ Thống").classes(
                    "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/50"
                )

                with ui.row().classes("items-center gap-2"):
                    ui.label("●").classes("text-[#F16D34] text-[16px]")
                    ui.label("Giám Sát Trực Tiếp").classes(
                        "text-[14px] font-extrabold text-[#161E54]"
                    )

                ui.label("Các mô-đun rủi ro đội xe đang hoạt động.").classes(
                    "text-[12px] font-medium text-[#161E54]/55 leading-snug"
                )


def render_top_header(title="", subtitle=None):
    """Render top header."""

    with ui.row().classes(
        "w-full items-center justify-between px-6 py-4 "
        "bg-white/70 backdrop-blur-xl border-b border-slate-100"
    ):
        with ui.column().classes("gap-0"):
            if title:
                ui.label(title).classes(
                    "text-[28px] font-extrabold text-[#161E54] tracking-tight"
                )
            if subtitle:
                ui.label(subtitle).classes(
                    "text-[14px] font-medium text-[#161E54]/55"
                )


def render_page_container():
    """Create a page container with spacing."""

    return ui.column().classes(
        "w-full max-w-full min-h-screen p-6 gap-6 "
        "bg-gradient-to-br from-[#BBE0EF]/35 via-white to-[#FF986A]/10"
    )


def render_section_header(title, subtitle=None):
    """Render section header."""

    with ui.column().classes("w-full gap-1"):
        ui.label(title).classes(
            "text-[22px] font-extrabold text-[#161E54]"
        )
        if subtitle:
            ui.label(subtitle).classes(
                "text-[14px] font-medium text-[#161E54]/55"
            )


def render_app_shell():
    """Render complete app shell structure."""

    app_container = ui.column().classes(
        "w-screen h-screen bg-gradient-to-br from-[#BBE0EF]/30 via-white to-[#FF986A]/10"
    )

    with app_container:
        with ui.row().classes("w-full h-full"):
            main_content = ui.column().classes("flex-grow overflow-auto")

    return main_content


def create_page_layout(title, subtitle=None, active_page="/"):
    """Create a standard page layout with sidebar and header."""

    render_sidebar(active_page)
    render_top_header(title, subtitle)

    return render_page_container()