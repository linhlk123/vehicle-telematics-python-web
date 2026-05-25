"""
Pipeline Components - Algorithm pipeline visualization
Vietnamese clean dashboard style with clickable step details
"""

from nicegui import ui
import pandas as pd

from services import data_service


# ==============================================================================
# DESIGN TOKENS
# ==============================================================================

BRAND_NAVY = "#161E54"
BRAND_BLUE = "#BBE0EF"
BRAND_ORANGE = "#F16D34"
BRAND_LIGHT_ORANGE = "#FF986A"


# ==============================================================================
# PIPELINE DATA
# ==============================================================================

PIPELINE_STEPS = [
    {
        "id": "raw_data",
        "name": "Dữ liệu thô",
        "icon": "dataset",
        "short": "Thu thập dữ liệu cảm biến từ xe.",
        "purpose": "Thu thập dữ liệu telemetry từ các phương tiện trong đội xe để làm nguồn đầu vào cho toàn bộ pipeline.",
        "input": "Cảm biến xe: tốc độ, vòng tua máy, nhiệt độ động cơ, ga, mức tiêu hao nhiên liệu, tăng tốc, phanh.",
        "process": "Đọc dữ liệu từ file / nguồn dữ liệu, chuẩn hóa cấu trúc bảng và xác định các cột quan trọng.",
        "output": "Các bản ghi telemetry dạng chuỗi thời gian theo từng xe.",
    },
    {
        "id": "cleaning",
        "name": "Làm sạch dữ liệu",
        "icon": "cleaning_services",
        "short": "Xử lý nhiễu, thiếu dữ liệu và giá trị bất thường.",
        "purpose": "Đảm bảo dữ liệu đủ sạch và nhất quán trước khi đưa vào phân tích, phân cụm và mô hình học máy.",
        "input": "Dữ liệu telemetry thô.",
        "process": "Xử lý missing values, loại bản ghi lỗi, chuẩn hóa kiểu dữ liệu và kiểm tra miền giá trị hợp lệ.",
        "output": "Dữ liệu đã làm sạch và sẵn sàng cho feature engineering.",
    },
    {
        "id": "feature_engineering",
        "name": "Tạo đặc trưng",
        "icon": "build_circle",
        "short": "Tạo các biến phân tích từ dữ liệu gốc.",
        "purpose": "Biến đổi dữ liệu cảm biến thành các đặc trưng có ý nghĩa hơn cho bài toán rủi ro và bảo trì.",
        "input": "Các chỉ số vận hành như tốc độ, RPM, nhiệt độ, nhiên liệu, phanh và tăng tốc.",
        "process": "Tạo các đặc trưng như stress index, thermal stress, fuel efficiency và các chỉ số hành vi lái xe.",
        "output": "Bộ đặc trưng mở rộng phục vụ clustering, anomaly detection và risk scoring.",
    },
    {
        "id": "kmeans",
        "name": "Phân cụm K-Means",
        "icon": "scatter_plot",
        "short": "Chia trạng thái vận hành thành bình thường và căng tải cao.",
        "purpose": "Phân đoạn trạng thái hoạt động của động cơ thành các nhóm dễ diễn giải.",
        "input": "Các đặc trưng đã tạo từ bước feature engineering.",
        "process": "Huấn luyện K-Means với K=2 để phân loại trạng thái vận hành thành NORMAL_OPERATION và HIGH_STRESS.",
        "output": "Cột engine_status_k2_all biểu diễn trạng thái vận hành của động cơ.",
    },
    {
        "id": "comparison",
        "name": "So sánh thuật toán cụm",
        "icon": "query_stats",
        "short": "Đánh giá K-Means và BIRCH.",
        "purpose": "So sánh K-Means và BIRCH để chọn thuật toán phân cụm phù hợp nhất cho việc nhận diện trạng thái vận hành của xe.",
        "input": "Bộ đặc trưng sau xử lý.",
        "process": "Tính các chỉ số đánh giá như Silhouette Score, Davies-Bouldin Index và Calinski-Harabasz Index cho K-Means và BIRCH.",
        "output": "Bảng metric so sánh giữa K-Means và BIRCH, từ đó chọn K-Means cho bước tạo trạng thái vận hành.",
    },
    {
        "id": "isolation_forest",
        "name": "Phát hiện bất thường",
        "icon": "radar",
        "short": "Tìm các hành vi vận hành bất thường.",
        "purpose": "Phát hiện các pattern telemetry khác thường về mặt thống kê, không nhất thiết là lỗi xe.",
        "input": "Các đặc trưng vận hành đã chuẩn hóa.",
        "process": "Sử dụng Isolation Forest để tính anomaly score và gắn cờ bản ghi bất thường.",
        "output": "Các cột iso_anomaly_score và iso_anomaly.",
    },
    {
        "id": "risk_flags",
        "name": "Tạo cờ rủi ro",
        "icon": "flag",
        "short": "Chuyển tín hiệu rủi ro thành các biến nhị phân.",
        "purpose": "Tạo các flag để biểu diễn những điều kiện vận hành có khả năng liên quan đến rủi ro bảo trì.",
        "input": "Feature engineering, trạng thái cụm và kết quả anomaly detection.",
        "process": "Tạo các cờ như high_stress_flag, iso_anomaly, high_rpm_flag, high_fuel_flag, harsh_brake_flag.",
        "output": "Tập các risk flags dùng cho công thức tính điểm rủi ro.",
    },
    {
        "id": "risk_scoring",
        "name": "Tính điểm rủi ro",
        "icon": "speed",
        "short": "Tổng hợp các cờ thành điểm rủi ro.",
        "purpose": "Gộp nhiều tín hiệu rủi ro thành một điểm số record-level để dễ ưu tiên theo mức độ nghiêm trọng.",
        "input": "Các risk flags và trọng số tương ứng.",
        "process": "Áp dụng công thức trọng số để tính record_risk_score trong khoảng 0.0 đến 1.0.",
        "output": "record_risk_score và risk_level gồm LOW_RISK, MEDIUM_RISK, HIGH_RISK.",
    },
    {
        "id": "ml_models",
        "name": "Mô hình học máy",
        "icon": "psychology",
        "short": "Huấn luyện model dự đoán mức rủi ro.",
        "purpose": "Dùng supervised learning để dự đoán mức rủi ro bảo trì từ dữ liệu vận hành.",
        "input": "Dữ liệu gốc và đặc trưng đã tạo, tránh leakage từ các cột target.",
        "process": "Huấn luyện và so sánh các model như Random Forest, Hist Gradient Boosting và các model khác.",
        "output": "Dự đoán risk_level và bảng đánh giá model bằng Accuracy, F1 Macro, F1 Weighted.",
    },
    {
        "id": "maintenance",
        "name": "Ưu tiên bảo trì",
        "icon": "home_repair_service",
        "short": "Tổng hợp rủi ro theo xe để xếp lịch bảo trì.",
        "purpose": "Chuyển kết quả phân tích record-level thành quyết định ưu tiên bảo trì ở cấp phương tiện.",
        "input": "Risk score, risk level và dữ liệu tổng hợp theo vehicle_id.",
        "process": "Tổng hợp các chỉ số rủi ro theo xe và phân loại mức ưu tiên bảo trì.",
        "output": "Maintenance priority: NORMAL_MONITORING, NEED_ATTENTION, MAINTENANCE_ALERT.",
    },
]


# ==============================================================================
# DATA HELPERS
# ==============================================================================

def _pretty_column_name(col):
    """Format column name for table display."""
    mapping = {
        "vehicle_id": "Vehicle ID",
        "vehicle_type": "Vehicle Type",
        "fleet": "Fleet",
        "road_class": "Road Class",
        "engine_status_k2_all": "Engine Status",
        "iso_anomaly_score": "Anomaly Score",
        "iso_anomaly": "Anomaly Flag",
        "record_risk_score": "Risk Score",
        "risk_level": "Risk Level",
        "maintenance_priority": "Maintenance Priority",
        "avg_record_risk_score": "Avg Risk Score",
        "avg_risk_score": "Avg Risk Score",
        "high_stress_flag": "High Stress",
        "high_fuel_flag": "High Fuel",
        "aggressive_throttle_flag": "Aggressive Throttle",
        "high_rpm_flag": "High RPM",
        "harsh_brake_flag": "Harsh Brake",
        "harsh_accel_flag": "Harsh Accel",
        "low_efficiency_flag": "Low Efficiency",
        "model": "Model",
        "accuracy": "Accuracy",
        "f1_macro": "F1 Macro",
        "f1_weighted": "F1 Weighted",
        "Algorithm": "Algorithm",
        "Silhouette Score": "Silhouette Score",
        "Davies-Bouldin Index": "Davies-Bouldin Index",
        "Calinski-Harabasz Index": "Calinski-Harabasz Index",
    }

    if col in mapping:
        return mapping[col]

    return str(col).replace("_", " ").replace("-", " ").title()


def _select_existing_columns(df, columns):
    """Only keep columns that actually exist in dataframe."""
    if df is None or df.empty:
        return []

    return [col for col in columns if col in df.columns]


def _safe_call(func_name, default=None):
    """Safely call a data_service function if it exists."""
    func = getattr(data_service, func_name, None)
    if not callable(func):
        return default

    try:
        return func()
    except Exception:
        return default


def _load_df_clean():
    """Load cleaned/project dataframe from data_service with fallback names."""
    for func_name in [
        "load_df_clean"
    ]:
        df = _safe_call(func_name)
        if df is not None:
            return df

    return pd.DataFrame()


def _load_clustering_results():
    """Load clustering comparison results from data_service."""
    for func_name in [
        "load_clustering_results"
    ]:
        df = _safe_call(func_name)
        if df is not None:
            return df

    return pd.DataFrame()


def _load_model_results():
    """Load model evaluation results from data_service."""
    for func_name in [
        "load_model_results"
    ]:
        df = _safe_call(func_name)
        if df is not None:
            return df

    return pd.DataFrame()


def _load_maintenance_queue():
    """Load maintenance priority data from data_service."""
    for func_name in [
        "get_maintenance_queue"
    ]:
        df = _safe_call(func_name)
        if df is not None:
            return df

    return pd.DataFrame()


def _get_real_step_table(step_id, limit=8):
    """
    Get real project data for the selected pipeline step.

    Early steps may not have a stored intermediate table.
    From K-Means onward, this function tries to use actual project outputs.
    """

    try:
        # ======================================================
        # RAW / CLEANING / FEATURE ENGINEERING
        # ======================================================
        if step_id in {"raw_data", "cleaning", "feature_engineering"}:
            df = _load_df_clean()

            if df is None or df.empty:
                return "Dữ liệu hiện có trong project", pd.DataFrame()

            common_cols = _select_existing_columns(df, [
                "vehicle_id",
                "vehicle_type",
                "fleet",
                "road_class",
                "speed",
                "rpm",
                "engine_temp",
                "fuel_rate",
                "stress_index",
                "thermal_stress",
                "fuel_efficiency",
            ])

            if not common_cols:
                common_cols = list(df.columns[:8])

            return "Bảng dữ liệu thật hiện có trong project", (
                df[common_cols]
                .head(limit)
                .reset_index(drop=True)
            )

        # ======================================================
        # K-MEANS OUTPUT
        # ======================================================
        if step_id == "kmeans":
            df = _load_df_clean()

            columns = _select_existing_columns(df, [
                "vehicle_id",
                "vehicle_type",
                "fleet",
                "road_class",
                "engine_status_k2_all",
                "record_risk_score",
                "risk_level",
            ])

            if not columns:
                return "Bảng thật sau bước K-Means Clustering", pd.DataFrame()

            return "Bảng thật sau bước K-Means Clustering", (
                df[columns]
                .drop_duplicates()
                .head(limit)
                .reset_index(drop=True)
            )

        # ======================================================
        # CLUSTERING COMPARISON OUTPUT
        # ======================================================
        if step_id == "comparison":
            df = _load_clustering_results()

            if df is None or df.empty:
                return "Bảng thật so sánh K-Means và BIRCH", pd.DataFrame()

            table_df = df.copy()

            # Lọc chỉ giữ K-Means và BIRCH, bỏ GMM để tránh gây nhiễu phần giải thích
            algorithm_col = None
            for candidate in ["Algorithm", "algorithm", "model", "Model"]:
                if candidate in table_df.columns:
                    algorithm_col = candidate
                    break

            if algorithm_col:
                table_df = table_df[
                    table_df[algorithm_col]
                    .astype(str)
                    .str.lower()
                    .isin(["k-means", "kmeans", "birch"])
                ]

            return "Bảng thật so sánh K-Means và BIRCH", (
                table_df.head(limit)
                .reset_index(drop=True)
            )

        # ======================================================
        # ISOLATION FOREST OUTPUT
        # ======================================================
        if step_id == "isolation_forest":
            df = _load_df_clean()

            columns = _select_existing_columns(df, [
                "vehicle_id",
                "vehicle_type",
                "fleet",
                "road_class",
                "engine_status_k2_all",
                "iso_anomaly_score",
                "iso_anomaly",
                "record_risk_score",
                "risk_level",
            ])

            if not columns:
                return "Bảng thật từ Isolation Forest", pd.DataFrame()

            table_df = df

            if "iso_anomaly" in table_df.columns:
                anomaly_df = table_df[table_df["iso_anomaly"] == 1]
                if not anomaly_df.empty:
                    table_df = anomaly_df

            if "iso_anomaly_score" in table_df.columns:
                table_df = table_df.sort_values(
                    by="iso_anomaly_score",
                    ascending=True,
                )

            return "Bảng thật các bản ghi bất thường từ Isolation Forest", (
                table_df[columns]
                .head(limit)
                .reset_index(drop=True)
            )

        # ======================================================
        # RISK FLAGS OUTPUT
        # ======================================================
        if step_id == "risk_flags":
            df = _load_df_clean()

            columns = _select_existing_columns(df, [
                "vehicle_id",
                "engine_status_k2_all",
                "iso_anomaly",
                "high_stress_flag",
                "high_fuel_flag",
                "aggressive_throttle_flag",
                "high_rpm_flag",
                "harsh_brake_flag",
                "harsh_accel_flag",
                "low_efficiency_flag",
            ])

            if not columns:
                return "Bảng thật các cờ rủi ro được tạo ra", pd.DataFrame()

            table_df = df

            sort_candidates = [
                "high_stress_flag",
                "iso_anomaly",
                "high_fuel_flag",
                "high_rpm_flag",
            ]

            for sort_col in sort_candidates:
                if sort_col in table_df.columns:
                    table_df = table_df.sort_values(by=sort_col, ascending=False)
                    break

            return "Bảng thật các cờ rủi ro được tạo ra", (
                table_df[columns]
                .head(limit)
                .reset_index(drop=True)
            )

        # ======================================================
        # RISK SCORING OUTPUT
        # ======================================================
        if step_id == "risk_scoring":
            df = _load_df_clean()

            columns = _select_existing_columns(df, [
                "vehicle_id",
                "vehicle_type",
                "fleet",
                "engine_status_k2_all",
                "iso_anomaly",
                "record_risk_score",
                "risk_level",
            ])

            if not columns:
                return "Bảng thật các record có điểm rủi ro cao nhất", pd.DataFrame()

            table_df = df

            if "record_risk_score" in table_df.columns:
                table_df = table_df.sort_values(
                    by="record_risk_score",
                    ascending=False,
                )

            return "Bảng thật các record có điểm rủi ro cao nhất", (
                table_df[columns]
                .head(limit)
                .reset_index(drop=True)
            )

        # ======================================================
        # ML MODELS OUTPUT
        # ======================================================
        if step_id == "ml_models":
            df = _load_model_results()

            if df is None or df.empty:
                return "Bảng thật đánh giá các mô hình học máy", pd.DataFrame()

            table_df = df

            if "f1_macro" in table_df.columns:
                table_df = table_df.sort_values(by="f1_macro", ascending=False)

            return "Bảng thật đánh giá các mô hình học máy", (
                table_df.head(limit)
                .reset_index(drop=True)
            )

        # ======================================================
        # MAINTENANCE OUTPUT
        # ======================================================
        if step_id == "maintenance":
            df = _load_maintenance_queue()

            if df is None or df.empty:
                return "Bảng thật ưu tiên bảo trì theo phương tiện", pd.DataFrame()

            table_df = df

            for sort_col in [
                "avg_record_risk_score",
                "avg_risk_score",
                "record_risk_score",
                "maintenance_score",
            ]:
                if sort_col in table_df.columns:
                    table_df = table_df.sort_values(by=sort_col, ascending=False)
                    break

            return "Bảng thật ưu tiên bảo trì theo phương tiện", (
                table_df.head(limit)
                .reset_index(drop=True)
            )

        return "Dữ liệu thật", pd.DataFrame()

    except Exception as e:
        return "Lỗi tải dữ liệu thật", pd.DataFrame([{
            "error": f"Không thể tải dữ liệu cho bước này: {e}"
        }])


# ==============================================================================
# TABLE RENDERER
# ==============================================================================

def _render_dataframe_table(df):
    """Render a pandas DataFrame as a NiceGUI table."""

    if df is None or df.empty:
        ui.label("Chưa có bảng dữ liệu thật cho bước này.").classes(
            "text-[14px] font-medium text-[#161E54]/55"
        )
        return

    display_df = df.copy()

    for col in display_df.columns:
        if pd.api.types.is_float_dtype(display_df[col]):
            display_df[col] = display_df[col].round(4)

    columns = [
        {
            "name": col,
            "label": _pretty_column_name(col),
            "field": col,
            "align": "left",
        }
        for col in display_df.columns
    ]

    rows = display_df.to_dict("records")

    ui.table(
        columns=columns,
        rows=rows,
        row_key=display_df.columns[0],
        pagination={"rowsPerPage": 8},
    ).classes(
        "w-full sample-pipeline-table"
    ).props(
        "flat bordered separator=cell"
    )


# ==============================================================================
# UI HELPERS
# ==============================================================================

def _render_detail_info_card(title, content, icon, accent="#161E54", bg="#BBE0EF"):
    """Small card for one detail section."""

    with ui.card().classes(
        "rounded-[24px] bg-white border border-slate-100 "
        "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
    ):
        with ui.row().classes("w-full items-start gap-4 px-5 py-5"):
            ui.icon(icon).classes(
                "text-[30px] rounded-[16px] p-3"
            ).style(
                f"color: {accent}; background: {bg}22;"
            )

            with ui.column().classes("gap-2 flex-1"):
                ui.label(title).classes(
                    "text-[13px] font-extrabold uppercase tracking-[0.12em] text-[#161E54]/50"
                )
                ui.label(content).classes(
                    "text-[14px] font-semibold leading-relaxed text-[#161E54]/75"
                )


def _step_card(step, active=False):
    """Render one compact pipeline step in light style."""

    name = step.get("name", "Không có tiêu đề")
    short = step.get("short", "")
    icon = step.get("icon", "settings")

    if active:
        card_bg = BRAND_NAVY
        border = f"2px solid {BRAND_ORANGE}"
        icon_bg = "rgba(255,255,255,0.12)"
        icon_color = "#161E54"
        title_color = "#161E54"
        subtitle_color = "rgba(22,30,84,0.58)"
        shadow = "0 10px 24px rgba(22,30,84,0.18)"
    else:
        card_bg = "#FFFFFF"
        border = "1px solid rgba(187,224,239,0.95)"
        icon_bg = "rgba(187,224,239,0.45)"
        icon_color = BRAND_NAVY
        title_color = BRAND_NAVY
        subtitle_color = "rgba(22,30,84,0.55)"
        shadow = "0 6px 18px rgba(22,30,84,0.06)"

    with ui.column().classes("items-center w-full"):
        with ui.card().classes(
            "rounded-[24px] p-0 overflow-hidden transition-all duration-200"
        ).style(
            f"""
            width: 96px;
            height: 96px;
            background: {card_bg};
            border: {border};
            box-shadow: {shadow};
            """
        ):
            with ui.column().classes("w-full h-full items-center justify-center"):
                ui.icon(icon).classes(
                    "text-[36px] rounded-[16px] p-2"
                ).style(
                    f"color: {icon_color}; background: {icon_bg};"
                )

        ui.label(name).classes(
            "mt-3 text-[13px] font-extrabold text-center leading-tight"
        ).style(f"color: {title_color};")

        ui.label(short).classes(
            "text-[11px] font-medium text-center mt-1 leading-snug"
        ).style(f"color: {subtitle_color};")


def _render_detail_light(step):
    """Render selected step detail and real project table."""

    name = step.get("name", "Không có tiêu đề")
    short = step.get("short", "")
    purpose = step.get("purpose", "Chưa có mô tả.")
    input_data = step.get("input", "Chưa có dữ liệu đầu vào.")
    process = step.get("process", "Chưa có mô tả xử lý.")
    output = step.get("output", "Chưa có dữ liệu đầu ra.")
    icon = step.get("icon", "settings")

    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_14px_36px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        # Header
        with ui.row().classes(
            "w-full items-center justify-between px-7 py-6 "
            "border-b border-[#BBE0EF]/45 bg-[#BBE0EF]/18"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon(icon).classes(
                    "text-[30px] bg-white rounded-[18px] p-3 "
                    "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
                ).style(f"color: {BRAND_NAVY};")

                with ui.column().classes("gap-1"):
                    ui.label(name).classes(
                        "text-[24px] font-extrabold text-[#161E54]"
                    )
                    ui.label(short).classes(
                        "text-[13px] font-semibold text-[#161E54]/55"
                    )

            ui.label("CHI TIẾT BƯỚC").classes(
                "px-4 py-2 rounded-full bg-[#161E54] text-white "
                "text-[12px] font-extrabold tracking-wide"
            )

        # Explanation cards
        with ui.grid(columns=2).classes("w-full gap-5 px-7 py-6"):
            _render_detail_info_card(
                title="Mục tiêu",
                content=purpose,
                icon="flag",
                accent=BRAND_NAVY,
                bg=BRAND_BLUE,
            )

            _render_detail_info_card(
                title="Dữ liệu đầu vào",
                content=input_data,
                icon="login",
                accent=BRAND_ORANGE,
                bg=BRAND_ORANGE,
            )

            _render_detail_info_card(
                title="Cách xử lý",
                content=process,
                icon="settings_suggest",
                accent=BRAND_LIGHT_ORANGE,
                bg=BRAND_LIGHT_ORANGE,
            )

            _render_detail_info_card(
                title="Kết quả đầu ra",
                content=output,
                icon="logout",
                accent=BRAND_NAVY,
                bg=BRAND_BLUE,
            )

        # Real project table
        table_title, table_df = _get_real_step_table(step.get("id"), limit=8)

        with ui.column().classes("w-full px-7 pb-7 gap-3"):
            with ui.row().classes("w-full items-center justify-between"):
                ui.label(table_title).classes(
                    "text-[17px] font-extrabold text-[#161E54]"
                )

                ui.label("DỮ LIỆU THẬT").classes(
                    "px-4 py-2 rounded-full bg-[#BBE0EF]/55 text-[#161E54] "
                    "text-[11px] font-extrabold tracking-wide"
                )

            _render_dataframe_table(table_df)


# ==============================================================================
# MAIN PIPELINE COMPONENT
# ==============================================================================

@ui.refreshable
def render_pipeline_overview(selected_step_id=None):
    """Render compact light pipeline. Click a step to show detail below."""

    if selected_step_id is None:
        selected_step_id = PIPELINE_STEPS[0]["id"]

    selected_step = next(
        (s for s in PIPELINE_STEPS if s["id"] == selected_step_id),
        PIPELINE_STEPS[0],
    )

    def on_select(step):
        render_pipeline_overview.refresh(step["id"])

    with ui.card().classes(
        "w-full rounded-[30px] p-0 overflow-hidden "
        "bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_30px_rgba(22,30,84,0.08)]"
    ):
        with ui.column().classes("w-full px-6 py-6 gap-6"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("gap-1"):
                    ui.label("Pipeline xử lý dữ liệu").classes(
                        "text-[22px] font-extrabold text-[#161E54]"
                    )
                    ui.label("Chọn từng bước để xem mô tả và dữ liệu thật bên dưới").classes(
                        "text-[13px] font-medium text-[#161E54]/55"
                    )

                ui.label(f"{len(PIPELINE_STEPS)} BƯỚC").classes(
                    "px-4 py-2 rounded-full bg-[#BBE0EF]/55 "
                    "text-[#161E54] text-[12px] font-extrabold tracking-wide"
                )

            with ui.grid(columns=5).classes("w-full gap-x-6 gap-y-8"):
                for step in PIPELINE_STEPS:
                    step_wrapper = ui.element("div").classes(
                        "cursor-pointer transition-transform duration-200 hover:scale-[1.02]"
                    )

                    with step_wrapper:
                        _step_card(
                            step,
                            active=(step["id"] == selected_step_id),
                        )

                    step_wrapper.on(
                        "click",
                        lambda e=None, s=step: on_select(s),
                    )

    ui.space().classes("h-5")
    _render_detail_light(selected_step)


def render_algorithm_pipeline():
    """Main entry point used by pages."""

    render_pipeline_overview()


# ==============================================================================
# BACKWARD-COMPATIBLE HELPERS
# ==============================================================================

def render_pipeline_step_card(step):
    """Render one standalone pipeline step card."""

    with ui.card().classes(
        "w-full rounded-[26px] bg-white border border-slate-100 "
        "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
    ):
        with ui.row().classes("w-full items-start gap-4 px-5 py-5"):
            ui.icon(step.get("icon", "settings")).classes(
                "text-[32px] bg-[#BBE0EF]/40 rounded-[18px] p-3"
            ).style(f"color: {BRAND_NAVY}")

            with ui.column().classes("flex-1 gap-2"):
                ui.label(step.get("name", "Không có tiêu đề")).classes(
                    "text-[18px] font-extrabold text-[#161E54]"
                )
                ui.label(step.get("purpose", "Chưa có mô tả.")).classes(
                    "text-[14px] font-medium text-[#161E54]/65 leading-relaxed"
                )
                ui.label(f"Đầu vào: {step.get('input', '')}").classes(
                    "text-[13px] font-semibold text-[#161E54]/55"
                )
                ui.label(f"Đầu ra: {step.get('output', '')}").classes(
                    "text-[13px] font-extrabold text-[#F16D34]"
                )


def render_pipeline_detail_modal(step_name):
    """Backward-compatible modal detail."""

    step = next((s for s in PIPELINE_STEPS if s["name"] == step_name), None)

    if not step:
        return None

    with ui.dialog() as dialog:
        with ui.card().classes(
            "w-[560px] rounded-[28px] bg-white p-0 overflow-hidden"
        ):
            with ui.row().classes(
                "w-full items-center gap-4 px-6 py-5 border-b border-slate-100"
            ):
                ui.icon(step.get("icon", "settings")).classes(
                    "text-[34px]"
                ).style(f"color: {BRAND_NAVY}")

                ui.label(step.get("name", "Không có tiêu đề")).classes(
                    "text-[22px] font-extrabold text-[#161E54]"
                )

            with ui.column().classes("w-full gap-4 px-6 py-5"):
                ui.label("Mục tiêu").classes(
                    "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/50"
                )
                ui.label(step.get("purpose", "Chưa có mô tả.")).classes(
                    "text-[14px] font-medium text-[#161E54]/70"
                )

                ui.label("Đầu vào").classes(
                    "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/50"
                )
                ui.label(step.get("input", "")).classes(
                    "text-[14px] font-medium text-[#161E54]/70"
                )

                ui.label("Đầu ra").classes(
                    "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/50"
                )
                ui.label(step.get("output", "")).classes(
                    "text-[14px] font-extrabold text-[#F16D34]"
                )

                ui.button("Đóng", on_click=dialog.close).classes(
                    "w-full rounded-[18px] bg-[#161E54] text-white font-bold py-3"
                )

    return dialog
 