from nicegui import ui

from services import data_service
from components import layout, charts, tables, cards
from nicegui import ui
# ==============================================================================
# PAGE 3: CLUSTERING STUDIO
# ==============================================================================
@ui.page("/clustering")
def clustering_page():
    """Clustering Studio - Compare K-Means and BIRCH algorithms"""

    # Nếu app.py đã dùng ui.add_css(..., shared=True) thì KHÔNG gọi _inject_css()
    # _inject_css()

    layout.render_sidebar(active_page="/clustering")

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
                ui.label("Phân Cụm").classes(
                    "text-3xl font-extrabold text-[#161E54] tracking-tight text-center"
                )
                ui.label("So sánh K-Means và BIRCH cho phân loại trạng thái vận hành động cơ").classes(
                    "text-sm font-medium text-[#161E54]/55 text-center"
                )

        # ==========================================================
        # LOAD DATA
        # ==========================================================
        clustering_results = data_service.load_clustering_results()
        df_clean = data_service.load_df_clean()

        # Lọc chỉ giữ K-Means và BIRCH
        if clustering_results is not None and not clustering_results.empty:
            algorithm_col = None
            for candidate in ["Algorithm", "algorithm", "model", "Model"]:
                if candidate in clustering_results.columns:
                    algorithm_col = candidate
                    break

            if algorithm_col:
                clustering_results = clustering_results[
                    clustering_results[algorithm_col]
                    .astype(str)
                    .str.lower()
                    .isin(["k-means", "kmeans", "birch"])
                ].reset_index(drop=True)

        # ==========================================================
        # KPI CARDS ROW
        # ==========================================================
        selected_algorithm = "K-Means"
        cluster_count = 2

        silhouette_value = "N/A"
        dbi_value = "N/A"

        if clustering_results is not None and not clustering_results.empty:
            algorithm_col = next(
                (col for col in ["Algorithm", "algorithm", "model", "Model"] if col in clustering_results.columns),
                None,
            )

            kmeans_row = clustering_results

            if algorithm_col:
                kmeans_row = clustering_results[
                    clustering_results[algorithm_col].astype(str).str.lower().isin(["k-means", "kmeans"])
                ]

            if not kmeans_row.empty:
                row = kmeans_row.iloc[0]

                for col in ["Silhouette Score", "silhouette_score", "silhouette"]:
                    if col in row.index:
                        silhouette_value = round(float(row[col]), 4)
                        break

                for col in ["Davies-Bouldin Index", "davies_bouldin_index", "dbi"]:
                    if col in row.index:
                        dbi_value = round(float(row[col]), 4)
                        break

        with ui.grid(columns=4).classes("w-full gap-6 mb-6"):
            cards._render_clustering_kpi_card(
                title="Thuật toán chọn",
                value=selected_algorithm,
                subtitle="Dùng cho engine_status_k2_all",
                icon="scatter_plot",
                icon_color="#161E54",
                bg_color="#BBE0EF",
            )

            cards._render_clustering_kpi_card(
                title="Số cụm",
                value=cluster_count,
                subtitle="NORMAL_OPERATION / HIGH_STRESS",
                icon="account_tree",
                icon_color="#161E54",
                bg_color="#BBE0EF",
            )

            cards._render_clustering_kpi_card(
                title="Silhouette Score",
                value=silhouette_value,
                subtitle="Độ tách biệt giữa các cụm",
                icon="analytics",
                icon_color="#F16D34",
                bg_color="#F16D34",
            )

            cards._render_clustering_kpi_card(
                title="Davies-Bouldin",
                value=dbi_value,
                subtitle="Chỉ số càng thấp càng tốt",
                icon="speed",
                icon_color="#FF986A",
                bg_color="#FF986A",
            )

        # ==========================================================
        # EXPLANATION CARD
        # ==========================================================
        with ui.card().classes(
            "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
            "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mb-6"
        ):
            with ui.row().classes(
                "w-full items-center justify-between px-7 py-5 "
                "border-b border-[#BBE0EF]/45 bg-[#BBE0EF]/18"
            ):
                with ui.row().classes("items-center gap-4"):
                    ui.icon("psychology_alt").classes(
                        "text-[32px] bg-white rounded-[18px] p-3 "
                        "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
                    ).style("color: #161E54;")

                    with ui.column().classes("gap-1"):
                        ui.label("Vì sao chọn K-Means K=2?").classes(
                            "text-[22px] font-extrabold text-[#161E54]"
                        )
                        ui.label("K-Means được chọn vì dễ giải thích và phù hợp với bước risk scoring phía sau.").classes(
                            "text-[13px] font-medium text-[#161E54]/55"
                        )

                ui.label("ĐÃ CHỮN").classes(
                    "px-4 py-2 rounded-full bg-[#161E54] text-white "
                    "text-[12px] font-extrabold tracking-wide"
                )

            with ui.grid(columns=3).classes("w-full gap-5 px-7 py-6"):
                cards._render_reason_card(
                    title="Dễ diễn giải",
                    content="K-Means tạo cụm rõ ràng, dễ ánh xạ thành NORMAL_OPERATION và HIGH_STRESS.",
                    icon="visibility",
                    color="#161E54",
                    bg="#BBE0EF",
                )

                cards._render_reason_card(
                    title="Phù hợp pipeline",
                    content="Output engine_status_k2_all có thể dùng trực tiếp cho risk flags và risk scoring.",
                    icon="hub",
                    color="#F16D34",
                    bg="#F16D34",
                )

                cards._render_reason_card(
                    title="Ổn định và nhanh",
                    content="K-Means nhẹ, dễ tái chạy, phù hợp dashboard và hệ thống phân tích vận hành.",
                    icon="bolt",
                    color="#FF986A",
                    bg="#FF986A",
                )

        # ==========================================================
        # METRICS TABLE + CHART
        # ==========================================================
        with ui.grid(columns=2).classes("w-full gap-6 mb-6"):
            with ui.card().classes(
                "w-full rounded-[30px] bg-white border border-slate-100 "
                "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
            ):
                with ui.row().classes(
                    "relative w-full items-center justify-end px-7 py-5 border-b border-slate-100"
                ):
                    ui.label("Bảng so sánh thuật toán").classes(
                        "absolute left-1/2 -translate-x-1/2 text-[20px] font-extrabold text-[#161E54]"
                    )
                    ui.icon("table_chart").classes(
                        "text-[26px] text-[#161E54]/60"
                    )

                with ui.column().classes("w-full px-5 py-5 clustering-table-wrapper"):
                    tables.render_clustering_comparison_table(clustering_results)

            with ui.card().classes(
                "w-full rounded-[30px] bg-white border border-slate-100 "
                "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
            ):
                with ui.row().classes(
                    "relative w-full items-center justify-end px-7 py-5 border-b border-slate-100"
                ):
                    ui.label("So Sánh Chỉ Số").classes(
                        "absolute left-1/2 -translate-x-1/2 text-[20px] font-extrabold text-[#161E54]"
                    )
                    ui.icon("query_stats").classes(
                        "text-[26px] text-[#161E54]/60"
                    )

                with ui.column().classes("w-full px-5 py-5"):
                    fig_metrics = charts.clustering_metrics_chart(clustering_results)
                    charts.render_plotly_chart(fig_metrics).classes("w-full h-[360px]")

        # ==========================================================
        # CLUSTER DISTRIBUTION + CENTROID PROFILE
        # ==========================================================
        with ui.grid(columns=2).classes("w-full gap-6 mb-6"):
            with ui.card().classes(
                "w-full rounded-[30px] bg-white border border-slate-100 "
                "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
            ):
                with ui.row().classes(
                    "relative w-full items-center justify-end px-7 py-5 border-b border-slate-100"
                ):
                    ui.label("Trạng thái động cơ").classes(
                        "absolute left-1/2 -translate-x-1/2 text-[20px] font-extrabold text-[#161E54]"
                    )
                    ui.icon("donut_large").classes(
                        "text-[26px] text-[#161E54]/60"
                    )

                with ui.column().classes("w-full px-5 py-5"):
                    if df_clean is not None and "engine_status_k2_all" in df_clean.columns:
                        cluster_dist = df_clean["engine_status_k2_all"].value_counts().reset_index()
                        cluster_dist.columns = ["engine_status", "count"]

                        fig_dist = charts.engine_status_distribution_chart(cluster_dist)
                        charts.render_plotly_chart(fig_dist).classes("w-full h-[360px]")
                    else:
                        ui.label("Không tìm thấy cột engine_status_k2_all trong dữ liệu.").classes(
                            "text-[14px] font-medium text-[#161E54]/55"
                        )

            with ui.card().classes(
                "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
                "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
            ):
                with ui.row().classes(
                    "w-full items-center justify-between px-7 py-5 "
                    "border-b border-[#BBE0EF]/45 bg-[#BBE0EF]/18"
                ):
                    with ui.row().classes("items-center gap-4"):
                        ui.icon("scatter_plot").classes(
                            "text-[30px] bg-white rounded-[18px] p-3"
                        ).style("color: #161E54;")

                        with ui.column().classes("gap-1"):
                            ui.label("Mô Hình K-Means").classes(
                                "text-[20px] font-extrabold text-[#161E54]"
                            )
                            ui.label("Mô tả trực quan hai cụm vận hành chính").classes(
                                "text-[13px] font-medium text-[#161E54]/55"
                            )

                with ui.column().classes("w-full gap-5 px-7 py-6"):
                    cards._render_cluster_profile_card(
                        title="Cluster 0 - NORMAL_OPERATION",
                        description="Vận hành ổn định, mức stress thấp hơn, phù hợp với điều kiện di chuyển thông thường.",
                        icon="check_circle",
                        color="#161E54",
                        bg="#BBE0EF",
                        metrics=[
                            "Speed trung bình ổn định",
                            "RPM và nhiệt độ thấp hơn",
                            "Fuel efficiency tốt hơn",
                        ],
                    )

                    cards._render_cluster_profile_card(
                        title="Cluster 1 - HIGH_STRESS",
                        description="Trạng thái vận hành căng tải, thường liên quan đến RPM cao, nhiệt độ cao hoặc điều kiện đường khó.",
                        icon="warning_amber",
                        color="#D23466",
                        bg="#D23466",
                        metrics=[
                            "RPM cao hơn",
                            "Thermal stress cao hơn",
                            "Có khả năng tăng risk score",
                        ],
                    )