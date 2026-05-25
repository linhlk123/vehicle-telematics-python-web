"""
Risk Service - Risk scoring and recommendation logic
"""


def assign_risk_level(score):
    """Assign risk level based on score"""
    if score >= 0.50:
        return "HIGH_RISK"
    elif score >= 0.25:
        return "MEDIUM_RISK"
    else:
        return "LOW_RISK"


def assign_recommendation(risk_level):
    """Get recommendation based on risk level"""
    if risk_level == "HIGH_RISK":
        return "Ưu tiên kiểm tra/bảo trì. Bản ghi có mức rủi ro cao."
    elif risk_level == "MEDIUM_RISK":
        return "Theo dõi phương tiện sát sao."
    elif risk_level == "LOW_RISK":
        return "Theo dõi bình thường. Chưa có dấu hiệu rủi ro đáng kể."
    else:
        return "Không xác định được mức rủi ro."


def calculate_record_risk_score_from_flags(flags):
    """Calculate record risk score from individual flags"""
    return (
        0.25 * flags.get("high_stress_flag", 0)
        + 0.25 * flags.get("iso_anomaly", 0)
        + 0.15 * flags.get("high_fuel_flag", 0)
        + 0.10 * flags.get("aggressive_throttle_flag", 0)
        + 0.10 * flags.get("high_rpm_flag", 0)
        + 0.05 * flags.get("harsh_brake_flag", 0)
        + 0.05 * flags.get("harsh_accel_flag", 0)
        + 0.05 * flags.get("low_efficiency_flag", 0)
    )


def explain_risk_flags(flags):
    """Create human-readable explanation of risk flags"""
    explanations = []
    
    flag_info = {
        'high_stress_flag': ('High Stress', 'Engine operating in high-stress state'),
        'iso_anomaly': ('Anomaly Detected', 'Statistically unusual telemetry pattern'),
        'high_fuel_flag': ('High Fuel Rate', 'Fuel consumption exceeds 95th percentile'),
        'aggressive_throttle_flag': ('Aggressive Throttle', 'Throttle position exceeds 95th percentile'),
        'high_rpm_flag': ('High RPM', 'Engine RPM exceeds 95th percentile'),
        'harsh_brake_flag': ('Harsh Braking', 'Brake application exceeds 95th percentile'),
        'harsh_accel_flag': ('Harsh Acceleration', 'Acceleration exceeds 95th percentile'),
        'low_efficiency_flag': ('Low Efficiency', 'Fuel efficiency below 5th percentile'),
    }
    
    for flag_key, (flag_name, description) in flag_info.items():
        if flags.get(flag_key, 0) == 1:
            explanations.append(f"🚩 {flag_name}: {description}")
    
    if not explanations:
        explanations.append("✅ No risk flags detected")
    
    return explanations


def explain_prediction(input_data, prediction):
    """Create human-readable explanation of model prediction"""
    generated_features = {
        'stress_index': input_data.get('stress_index', 0),
        'thermal_stress': input_data.get('thermal_stress', 0),
        'fuel_efficiency_kml': input_data.get('fuel_efficiency_kml', 0),
    }
    
    explanation = f"""
    **Prediction: {prediction['prediction']}**
    
    Input Parameters:
    - Speed: {input_data.get('speed_kmh', 0):.1f} km/h
    - RPM: {input_data.get('rpm', 0):.0f}
    - Engine Temp: {input_data.get('engine_temp_c', 0):.1f}°C
    - Vehicle Type: {input_data.get('vehicle_type', 'N/A')}
    - Road Class: {input_data.get('road_class', 'N/A')}
    
    Generated Features:
    - Stress Index: {generated_features['stress_index']:.4f}
    - Thermal Stress: {generated_features['thermal_stress']:.4f}
    - Fuel Efficiency: {generated_features['fuel_efficiency_kml']:.2f} km/l
    """
    
    if 'probabilities' in prediction and prediction['probabilities']:
        explanation += "\nClass Probabilities:\n"
        for class_name, prob in sorted(prediction['probabilities'].items(), key=lambda x: x[1], reverse=True):
            bar_length = int(prob * 20)
            bar = "█" * bar_length
            explanation += f"- {class_name}: {bar} {prob*100:.1f}%\n"
    
    return explanation.strip()


# Risk scoring formula for reference
RISK_FORMULA = """
**Record Risk Score Formula:**

record_risk_score = 
  0.25 × high_stress_flag (engine stress)
+ 0.25 × iso_anomaly (statistical anomaly)
+ 0.15 × high_fuel_flag (fuel consumption)
+ 0.10 × aggressive_throttle_flag (driving behavior)
+ 0.10 × high_rpm_flag (engine loading)
+ 0.05 × harsh_brake_flag (braking intensity)
+ 0.05 × harsh_accel_flag (acceleration intensity)
+ 0.05 × low_efficiency_flag (fuel efficiency)

**Risk Level Classification:**
- 0.00 - 0.25: LOW_RISK (Green)
- 0.25 - 0.50: MEDIUM_RISK (Amber)
- 0.50 - 1.00: HIGH_RISK (Red)
"""


# Risk flag thresholds
RISK_THRESHOLDS = {
    'high_rpm_flag': 'RPM > 95th percentile (~4000 RPM)',
    'high_fuel_flag': 'Fuel Rate > 95th percentile (~20 L/h)',
    'aggressive_throttle_flag': 'Throttle > 95th percentile (~80%)',
    'harsh_brake_flag': 'Brake > 95th percentile (~80%)',
    'harsh_accel_flag': 'Acceleration > 95th percentile (~8 m/s²)',
    'low_efficiency_flag': 'Fuel Efficiency < 5th percentile (~2 km/l)',
    'high_stress_flag': 'Engine Status = HIGH_STRESS',
    'iso_anomaly': 'Isolation Forest Anomaly Score > 0.5',
}
