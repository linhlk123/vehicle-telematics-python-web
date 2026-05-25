from nicegui import ui
import pandas as pd

from services import model_service, risk_service
from components.tables import render_dataframe_table


BRAND_NAVY = "#161E54"
BRAND_BLUE = "#BBE0EF"
BRAND_ORANGE = "#F16D34"
BRAND_LIGHT_ORANGE = "#FF986A"


SAFE_MODEL_OPTIONS = [
    "Hist Gradient Boosting",
    "MLP Neural Network",
    "Random Forest",
    "Decision Tree",
    "Extra Trees",
    "Logistic Regression",
]

VEHICLE_TYPE_LABELS = {
    "Motorcycle": "motorcycle",
    "Sedan": "sedan",
    "Van": "van",
    "Minibus": "minibus",
    "BRT Bus": "brt_bus",
    "Rigid Truck": "rigid_truck",
    "Articulated Truck": "articulated_truck",
    "Reefer Truck": "reefer_truck",
}

FUEL_TYPE_LABELS = {
    "LPG": "lpg",
    "Diesel": "diesel",
    "Petrol": "petrol",
    "Hybrid": "hybrid",
    "Electric": "electric",
}

ROAD_CLASS_LABELS = {
    "Urban": "urban",
    "Rural": "rural",
    "Expressway": "expressway",
}


def styled_number(label, value=0):
    """Styled number input for prediction form."""
    return ui.number(
        label=label,
        value=value,
    ).props(
        "borderless stack-label"
    ).classes(
        "w-full prediction-inner-field"
    )


def styled_select(label, options, value=None):
    """Styled select input for prediction form."""
    return ui.select(
        options=options,
        value=value,
        label=label,
    ).props(
        "borderless stack-label"
    ).classes(
        "w-full prediction-field prediction-select"
    )

def render_result_metric_card(title, value, subtitle, icon, color="#161E54", bg="#BBE0EF"):
    """Small result metric card."""
    with ui.card().classes(
        "rounded-[24px] bg-white border border-slate-100 "
        "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
    ):
        with ui.row().classes("w-full items-center gap-4 px-5 py-5"):
            ui.icon(icon).classes(
                "text-[30px] rounded-[16px] p-3"
            ).style(
                f"color: {color}; background: {bg}33;"
            )

            with ui.column().classes("gap-1"):
                ui.label(title).classes(
                    "text-[12px] font-extrabold uppercase tracking-wide text-[#161E54]/45"
                )
                ui.label(str(value)).classes(
                    "text-[24px] font-extrabold text-[#161E54]"
                )
                ui.label(subtitle).classes(
                    "text-[12px] font-semibold text-[#161E54]/55"
                )


def render_prediction_badge(prediction):
    """Render predicted risk badge."""
    prediction_text = str(prediction)

    if "HIGH" in prediction_text.upper():
        bg = "#F16D34"
        color = "white"
        icon = "warning_amber"
    elif "MEDIUM" in prediction_text.upper():
        bg = "#FF986A"
        color = "white"
        icon = "priority_high"
    else:
        bg = "#BBE0EF"
        color = "#161E54"
        icon = "check_circle"

    with ui.row().classes(
        "items-center gap-3 rounded-full px-5 py-3"
    ).style(
        f"background: {bg}; color: {color};"
    ):
        ui.icon(icon).classes("text-[24px]")
        ui.label(prediction_text).classes(
            "text-[18px] font-extrabold"
        )


def render_prediction_result_card(selected_model, prediction, recommendation, probabilities=None):
    """Render single model prediction result."""
    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        with ui.row().classes(
            "w-full items-center justify-between px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon("psychology").classes(
                    "text-[32px] bg-white rounded-[18px] p-3 "
                    "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
                ).style("color: #161E54;")

                with ui.column().classes("gap-1"):
                    ui.label("Prediction Result").classes(
                        "text-[22px] font-extrabold text-[#161E54]"
                    )
                    ui.label(f"Model: {selected_model}").classes(
                        "text-[13px] font-medium text-[#161E54]/55"
                    )

            ui.label("RESULT").classes(
                "px-4 py-2 rounded-full bg-[#161E54] text-white "
                "text-[12px] font-extrabold tracking-wide"
            )

        with ui.grid(columns=2).classes("w-full gap-6 px-7 py-6"):
            with ui.card().classes(
                "rounded-[24px] bg-white border border-slate-100 "
                "shadow-[0_8px_24px_rgba(22,30,84,0.06)] p-0 overflow-hidden"
            ):
                with ui.column().classes("w-full items-center gap-3 px-5 py-6"):
                    ui.label("Predicted Risk").classes(
                        "text-[13px] font-extrabold uppercase tracking-wide text-[#161E54]/45"
                    )
                    render_prediction_badge(prediction)

            with ui.card().classes(
                "rounded-[24px] bg-[#BBE0EF]/18 border border-[#BBE0EF]/65 "
                "shadow-none p-0 overflow-hidden"
            ):
                with ui.column().classes("w-full gap-2 px-5 py-6"):
                    ui.label("Recommendation").classes(
                        "text-[13px] font-extrabold uppercase tracking-wide text-[#161E54]/45"
                    )
                    ui.label(recommendation).classes(
                        "text-[14px] font-semibold leading-relaxed text-[#161E54]/70"
                    )

        if probabilities:
            with ui.column().classes("w-full px-7 pb-7 gap-3"):
                ui.label("Class Probabilities").classes(
                    "text-[17px] font-extrabold text-[#161E54]"
                )

                for class_name, prob in sorted(
                    probabilities.items(),
                    key=lambda item: item[1],
                    reverse=True,
                ):
                    with ui.row().classes("w-full items-center gap-4"):
                        ui.label(str(class_name)).classes(
                            "w-[130px] text-[13px] font-extrabold text-[#161E54]/70"
                        )

                        with ui.column().classes("flex-1 gap-1"):
                            ui.linear_progress(value=float(prob)).classes(
                                "w-full h-[10px] rounded-full"
                            ).props("rounded color=blue")
                            ui.label(f"{float(prob) * 100:.1f}%").classes(
                                "text-[12px] font-semibold text-[#161E54]/55"
                            )


def render_generated_features_card(generated):
    """Render generated features from input."""
    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        with ui.row().classes(
            "relative w-full items-center justify-end px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            ui.label("Generated Features").classes(
                "absolute left-1/2 -translate-x-1/2 "
                "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
            )
            ui.icon("auto_graph").classes("text-[28px] text-[#161E54]/55")

        with ui.grid(columns=3).classes("w-full gap-5 px-7 py-6"):
            render_result_metric_card(
                "Stress Index",
                f"{generated.get('stress_index', 0):.4f}",
                "Tổng hợp tải vận hành",
                "speed",
                BRAND_NAVY,
                BRAND_BLUE,
            )

            render_result_metric_card(
                "Thermal Stress",
                f"{generated.get('thermal_stress', 0):.4f}",
                "Áp lực nhiệt động cơ",
                "device_thermostat",
                BRAND_ORANGE,
                BRAND_ORANGE,
            )

            render_result_metric_card(
                "Fuel Efficiency",
                f"{generated.get('fuel_efficiency_kml', 0):.2f} km/l",
                "Hiệu suất nhiên liệu",
                "eco",
                BRAND_LIGHT_ORANGE,
                BRAND_LIGHT_ORANGE,
            )


def render_prediction_playground():
    """Render complete prediction playground."""

    # ==========================================================
    # TELEMETRY INPUT CARD
    # ==========================================================
    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
    ):
        with ui.row().classes(
            "w-full items-center justify-between px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon("sensors").classes(
                    "text-[32px] bg-white rounded-[18px] p-3 "
                    "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
                ).style("color: #161E54;")

                with ui.column().classes("gap-1"):
                    ui.label("Telemetry Input").classes(
                        "text-[22px] font-extrabold text-[#161E54]"
                    )
                    ui.label("Nhập thông số vận hành để dự đoán mức rủi ro").classes(
                        "text-[13px] font-medium text-[#161E54]/55"
                    )

            ui.label("INPUT FEATURES").classes(
                "px-4 py-2 rounded-full bg-[#161E54] text-white "
                "text-[12px] font-extrabold tracking-wide"
            )

        with ui.column().classes("w-full px-7 py-7 gap-6"):
            with ui.grid(columns=2).classes("w-full gap-5"):
                speed_input = styled_number("Speed (km/h)", 81)
                rpm_input = styled_number("RPM", 2500)
                temp_input = styled_number("Engine Temp (°C)", 85)
                throttle_input = styled_number("Throttle (%)", 40)
                fuel_input = styled_number("Fuel Rate (L/h)", 10)
                accel_input = styled_number("Acceleration (m/s²)", 0)
                brake_input = styled_number("Brake (%)", 20)

            with ui.grid(columns=3).classes("w-full gap-5"):
                vehicle_type_input = styled_select(
                    "Vehicle Type",
                    list(VEHICLE_TYPE_LABELS.keys()),
                    "Rigid Truck",
                )

                fuel_type_input = styled_select(
                    "Fuel Type",
                    list(FUEL_TYPE_LABELS.keys()),
                    "Hybrid",
                )

                road_class_input = styled_select(
                    "Road Class",
                    list(ROAD_CLASS_LABELS.keys()),
                    "Urban",
                )

    # ==========================================================
    # MODEL SELECTION CARD
    # ==========================================================
    with ui.card().classes(
        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden mt-6"
    ):
        with ui.row().classes(
            "w-full items-center justify-between px-7 py-5 "
            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
        ):
            with ui.row().classes("items-center gap-4"):
                ui.icon("model_training").classes(
                    "text-[32px] bg-white rounded-[18px] p-3 "
                    "shadow-[0_8px_20px_rgba(22,30,84,0.08)]"
                ).style("color: #161E54;")

                with ui.column().classes("gap-1"):
                    ui.label("Model Selection").classes(
                        "text-[22px] font-extrabold text-[#161E54]"
                    )
                    ui.label("Chọn mô hình dùng để dự đoán risk level").classes(
                        "text-[13px] font-medium text-[#161E54]/55"
                    )

            ui.label("SAFE MODELS").classes(
                "px-4 py-2 rounded-full bg-[#BBE0EF]/55 text-[#161E54] "
                "text-[12px] font-extrabold tracking-wide"
            )

        with ui.row().classes("w-full items-center gap-6 px-7 py-6"):
            model_select = styled_select(
                "Select Model",
                SAFE_MODEL_OPTIONS,
                "Hist Gradient Boosting",
            ).classes("flex-1")

            compare_all = ui.checkbox(
                "Compare All Models",
                value=False,
            ).classes(
                "text-[#161E54] font-bold"
            )

    # ==========================================================
    # RESULTS AREA
    # ==========================================================
    results_container = ui.column().classes("w-full gap-6 mt-6")

    def clear_form():
        """Reset form values and clear results."""
        speed_input.value = 81
        rpm_input.value = 2500
        temp_input.value = 85
        throttle_input.value = 40
        fuel_input.value = 10
        accel_input.value = 0
        brake_input.value = 20
        vehicle_type_input.value = "Rigid Truck"
        fuel_type_input.value = "Hybrid"
        road_class_input.value = "Urban"
        model_select.value = "Hist Gradient Boosting"
        compare_all.value = False
        results_container.clear()

    def build_input_payload():
        """Build input payload for model service."""
        return {
            "speed_kmh": speed_input.value,
            "rpm": rpm_input.value,
            "engine_temp_c": temp_input.value,
            "throttle_pct": throttle_input.value,
            "fuel_rate_lph": fuel_input.value,
            "accel_ms2": accel_input.value,
            "brake_pct": brake_input.value,
            "vehicle_type": VEHICLE_TYPE_LABELS.get(vehicle_type_input.value, vehicle_type_input.value),
            "fuel_type": FUEL_TYPE_LABELS.get(fuel_type_input.value, fuel_type_input.value),
            "road_class": ROAD_CLASS_LABELS.get(road_class_input.value, road_class_input.value),
        }

    def run_prediction():
        """Execute prediction."""
        input_data = build_input_payload()

        results_container.clear()

        with results_container:
            try:
                generated = model_service.calculate_generated_features(input_data)
                render_generated_features_card(generated)
            except Exception as e:
                ui.notify(f"Cannot calculate generated features: {e}", type="warning")

            if compare_all.value:
                comparison_data = []

                for model_name in SAFE_MODEL_OPTIONS:
                    try:
                        result = model_service.predict_single(model_name, input_data)

                        if result.get("success"):
                            comparison_data.append({
                                "Model": model_name,
                                "Prediction": result.get("prediction"),
                                "Confidence": "Available" if result.get("probabilities") else "N/A",
                            })
                        else:
                            comparison_data.append({
                                "Model": model_name,
                                "Prediction": "Failed",
                                "Confidence": result.get("error", "Unknown error"),
                            })

                    except Exception as e:
                        comparison_data.append({
                            "Model": model_name,
                            "Prediction": "Failed",
                            "Confidence": str(e),
                        })

                if comparison_data:
                    df = pd.DataFrame(comparison_data)

                    with ui.card().classes(
                        "w-full rounded-[30px] bg-white border border-[#BBE0EF]/70 "
                        "shadow-[0_12px_32px_rgba(22,30,84,0.08)] p-0 overflow-hidden"
                    ):
                        with ui.row().classes(
                            "relative w-full items-center justify-end px-7 py-5 "
                            "border-b border-[#BBE0EF]/50 bg-[#BBE0EF]/20"
                        ):
                            ui.label("All Models Predictions").classes(
                                "absolute left-1/2 -translate-x-1/2 "
                                "text-[22px] font-extrabold text-[#161E54] text-center whitespace-nowrap"
                            )
                            ui.label("COMPARISON").classes(
                                "rounded-full px-4 py-2 bg-white/70 text-[#161E54] "
                                "font-extrabold text-[11px] tracking-wide shadow-sm"
                            )

                        with ui.column().classes("w-full px-6 pt-5 pb-6 app-data-table"):
                            render_dataframe_table(df)

                return

            selected_model = model_select.value or "Hist Gradient Boosting"

            try:
                result = model_service.predict_single(selected_model, input_data)
            except Exception as e:
                ui.notify(f"Prediction failed: {e}", type="negative")
                return

            if not result.get("success"):
                ui.notify(
                    f"Prediction failed: {result.get('error', 'Unknown error')}",
                    type="negative",
                )
                return

            prediction = result.get("prediction")
            recommendation = risk_service.assign_recommendation(prediction)

            render_prediction_result_card(
                selected_model=selected_model,
                prediction=prediction,
                recommendation=recommendation,
                probabilities=result.get("probabilities"),
            )

    # ==========================================================
    # ACTION BUTTONS
    # ==========================================================
    with ui.row().classes("w-full justify-center gap-4 mt-7"):
        ui.button(
            "Run Prediction",
            icon="play_arrow",
            on_click=run_prediction,
        ).props(
            "unelevated no-caps"
        ).classes(
            "rounded-[18px] px-8 py-3 bg-[#161E54] text-white "
            "font-extrabold shadow-[0_10px_24px_rgba(22,30,84,0.20)] "
            "hover:bg-[#24306f]"
        )

        ui.button(
            "Clear",
            icon="refresh",
            on_click=clear_form,
        ).props(
            "flat no-caps"
        ).classes(
            "rounded-[18px] px-7 py-3 bg-[#BBE0EF]/45 text-[#161E54] "
            "font-extrabold hover:bg-[#BBE0EF]/70"
        )