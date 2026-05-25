"""
Model Service - Load and manage ML models for prediction
"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"

# Model mappings
MODEL_MAPPING = {
    'Logistic Regression': 'logistic_regression_model.joblib',
    'Decision Tree': 'decision_tree_model.joblib',
    'Random Forest': 'random_forest_model.joblib',
    'Extra Trees': 'extra_trees_model.joblib',
    'Hist Gradient Boosting': 'hist_gradient_boosting_model.joblib',
    'AdaBoost': 'adaboost_model.joblib',
    'MLP Neural Network': 'mlp_neural_network_model.joblib',
}

# Cache for loaded models
_model_cache = {}
_available_models = None


def get_available_models():
    """Get list of available models (those with files that exist)"""
    global _available_models
    
    if _available_models is not None:
        return _available_models
    
    available = []
    for model_name, filename in MODEL_MAPPING.items():
        model_path = MODELS_DIR / filename
        if model_path.exists():
            available.append(model_name)
        else:
            print(f"⚠️  Model file not found: {model_path}")
    
    _available_models = available
    return available


def load_model(model_name):
    """Load a model from joblib file"""
    if model_name in _model_cache:
        return _model_cache[model_name]
    
    if model_name not in MODEL_MAPPING:
        raise ValueError(f"Unknown model: {model_name}")
    
    filename = MODEL_MAPPING[model_name]
    model_path = MODELS_DIR / filename
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        model = joblib.load(model_path)
        _model_cache[model_name] = model
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model {model_name}: {e}")


def calculate_generated_features(input_data):
    """Calculate derived features from input data"""
    # Input data should be a dict or pd.Series with raw features
    
    speed_kmh = float(input_data.get('speed_kmh', 0))
    rpm = float(input_data.get('rpm', 0))
    engine_temp_c = float(input_data.get('engine_temp_c', 0))
    fuel_rate_lph = float(input_data.get('fuel_rate_lph', 0))
    
    # Generate features
    stress_index = rpm / (speed_kmh + 1)
    thermal_stress = engine_temp_c / (speed_kmh + 1)
    fuel_efficiency_kml = speed_kmh / (fuel_rate_lph + 0.001)
    
    return {
        'stress_index': stress_index,
        'thermal_stress': thermal_stress,
        'fuel_efficiency_kml': fuel_efficiency_kml,
    }


def prepare_input_dataframe(input_data):
    """Prepare input data as a pandas DataFrame for model prediction"""
    
    # Calculate generated features
    generated = calculate_generated_features(input_data)
    
    # Combine raw and generated features
    combined_data = {
        'speed_kmh': float(input_data.get('speed_kmh', 0)),
        'rpm': float(input_data.get('rpm', 0)),
        'engine_temp_c': float(input_data.get('engine_temp_c', 0)),
        'throttle_pct': float(input_data.get('throttle_pct', 0)),
        'fuel_rate_lph': float(input_data.get('fuel_rate_lph', 0)),
        'accel_ms2': float(input_data.get('accel_ms2', 0)),
        'brake_pct': float(input_data.get('brake_pct', 0)),
        'stress_index': generated['stress_index'],
        'thermal_stress': generated['thermal_stress'],
        'fuel_efficiency_kml': generated['fuel_efficiency_kml'],
        'vehicle_type': input_data.get('vehicle_type', 'car'),
        'fuel_type': input_data.get('fuel_type', 'diesel'),
        'road_class': input_data.get('road_class', 'highway'),
    }
    
    return pd.DataFrame([combined_data]), combined_data


def predict_single(model_name, input_data):
    """Predict risk level using a single model"""
    
    try:
        model = load_model(model_name)
        df_input, prepared_data = prepare_input_dataframe(input_data)
        
        # Make prediction
        prediction = model.predict(df_input)[0]
        
        # Try to get probabilities
        probabilities = None
        if hasattr(model, 'predict_proba'):
            try:
                proba = model.predict_proba(df_input)[0]
                classes = model.classes_
                probabilities = {str(cls): float(prob) for cls, prob in zip(classes, proba)}
            except:
                pass
        
        return {
            'success': True,
            'model': model_name,
            'prediction': str(prediction),
            'probabilities': probabilities,
            'generated_features': {
                'stress_index': round(prepared_data['stress_index'], 4),
                'thermal_stress': round(prepared_data['thermal_stress'], 4),
                'fuel_efficiency_kml': round(prepared_data['fuel_efficiency_kml'], 4),
            }
        }
    except Exception as e:
        return {
            'success': False,
            'model': model_name,
            'error': str(e)
        }


def predict_all_models(input_data):
    """Get predictions from all available models"""
    results = []
    available_models = get_available_models()
    
    for model_name in available_models:
        result = predict_single(model_name, input_data)
        results.append(result)
    
    return results
