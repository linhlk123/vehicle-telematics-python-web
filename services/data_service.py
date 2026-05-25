"""
Data Service - Load and process telematics data
"""
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Cache for loaded dataframes
_cache = {}


def load_df_clean():
    """Load clean telemetry data"""
    if 'df_clean' in _cache:
        return _cache['df_clean']
    
    csv_path = DATA_DIR / "df_clean.csv"
    
    df = pd.read_csv(csv_path)
    _cache['df_clean'] = df
    return df


def load_vehicle_risk():
    """Load vehicle-level risk aggregation"""
    if 'vehicle_risk' in _cache:
        return _cache['vehicle_risk']
    
    csv_path = DATA_DIR / "vehicle_risk.csv"
    df = pd.read_csv(csv_path)
    _cache['vehicle_risk'] = df
    return df


def load_model_results():
    """Load ML model evaluation results"""
    if 'model_results' in _cache:
        return _cache['model_results']
    
    csv_path = DATA_DIR / "model_results.csv"
    df = pd.read_csv(csv_path)
    _cache['model_results'] = df
    return df


def load_clustering_results():
    """Load clustering comparison results"""
    if 'clustering_results' in _cache:
        return _cache['clustering_results']
    
    csv_path = DATA_DIR / "clustering_results.csv"
    df = pd.read_csv(csv_path)
    _cache['clustering_results'] = df
    return df


def get_dashboard_summary():
    """Get key metrics for dashboard overview"""
    df_clean = load_df_clean()
    vehicle_risk = load_vehicle_risk()
    model_results = load_model_results()
    
    total_vehicles = df_clean['vehicle_id'].nunique() if 'vehicle_id' in df_clean.columns else 0
    total_records = len(df_clean)
    
    high_risk_count = (df_clean['risk_level'] == 'HIGH_RISK').sum() if 'risk_level' in df_clean.columns else 0
    high_risk_rate = (high_risk_count / total_records * 100) if total_records > 0 else 0
    
    anomaly_count = df_clean['iso_anomaly'].sum() if 'iso_anomaly' in df_clean.columns else 0
    anomaly_rate = (anomaly_count / total_records * 100) if total_records > 0 else 0
    
    maintenance_alerts = (vehicle_risk['maintenance_priority'] == 'MAINTENANCE_ALERT').sum() if 'maintenance_priority' in vehicle_risk.columns else 0
    
    best_model = model_results.loc[model_results['f1_macro'].idxmax()] if len(model_results) > 0 else None
    best_model_name = best_model['model'] if best_model is not None else 'N/A'
    best_f1 = f"{best_model['f1_macro']:.4f}" if best_model is not None else 'N/A'
    
    return {
        'total_vehicles': total_vehicles,
        'total_records': total_records,
        'high_risk_rate': f"{high_risk_rate:.2f}%",
        'anomaly_rate': f"{anomaly_rate:.2f}%",
        'maintenance_alerts': maintenance_alerts,
        'best_model': best_model_name,
        'best_f1': best_f1,
    }


def get_risk_distribution():
    """Get distribution of risk levels"""
    df_clean = load_df_clean()
    if 'risk_level' not in df_clean.columns:
        return pd.DataFrame({'risk_level': [], 'count': []})
    
    dist = df_clean['risk_level'].value_counts().reset_index()
    dist.columns = ['risk_level', 'count']
    return dist


def get_vehicle_type_risk():
    """Get average risk by vehicle type"""
    df_clean = load_df_clean()
    if 'vehicle_type' not in df_clean.columns or 'record_risk_score' not in df_clean.columns:
        return pd.DataFrame()
    
    result = df_clean.groupby('vehicle_type')['record_risk_score'].mean().reset_index()
    result.columns = ['vehicle_type', 'avg_risk_score']
    result = result.sort_values('avg_risk_score', ascending=False)
    return result


def get_fleet_risk():
    """Get risk ranking by fleet"""
    df_clean = load_df_clean()
    if 'fleet' not in df_clean.columns or 'record_risk_score' not in df_clean.columns:
        return pd.DataFrame()
    
    result = df_clean.groupby('fleet')['record_risk_score'].mean().reset_index()
    result.columns = ['fleet', 'avg_risk_score']
    result = result.sort_values('avg_risk_score', ascending=False)
    return result


def get_top_anomalies(limit=10):
    df = load_df_clean()

    if df is None or df.empty:
        return df

    # Ưu tiên hiển thị record có risk score cao nhất
    sort_col = "record_risk_score"

    if sort_col not in df.columns:
        return df.head(limit)

    columns_to_show = [
        "vehicle_id",
        "vehicle_type",
        "fleet",
        "road_class",
        "engine_status_k2_all",
        "iso_anomaly_score",
        "risk_level",
        "record_risk_score",
    ]

    columns_to_show = [col for col in columns_to_show if col in df.columns]

    return (
        df[columns_to_show]
        .sort_values(by=sort_col, ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )


def get_maintenance_queue(priority=None, vehicle_type=None, fleet=None, search=None):
    """Get maintenance queue with filters"""
    vehicle_risk = load_vehicle_risk()
    
    result = vehicle_risk.copy()
    
    if priority:
        result = result[result['maintenance_priority'] == priority]
    
    if vehicle_type:
        # Need to join with df_clean to get vehicle_type
        df_clean = load_df_clean()
        if 'vehicle_type' in df_clean.columns:
            vehicle_types = df_clean[['vehicle_id', 'vehicle_type']].drop_duplicates()
            result = result.merge(vehicle_types, on='vehicle_id', how='left')
            result = result[result['vehicle_type'] == vehicle_type]
    
    if fleet:
        df_clean = load_df_clean()
        if 'fleet' in df_clean.columns:
            fleets = df_clean[['vehicle_id', 'fleet']].drop_duplicates()
            result = result.merge(fleets, on='vehicle_id', how='left')
            result = result[result['fleet'] == fleet]
    
    if search:
        result = result[result['vehicle_id'].str.contains(search, case=False, na=False)]
    
    result = result.sort_values('avg_risk_score', ascending=False)
    
    display_cols = [
        'vehicle_id', 'avg_risk_score', 'high_risk_rate', 'anomaly_rate',
        'high_stress_rate', 'maintenance_priority', 'recommendation'
    ]
    available_cols = [col for col in display_cols if col in result.columns]
    return result[available_cols].head(100)


def get_vehicle_detail(vehicle_id):
    """Get detailed data for a specific vehicle"""
    df_clean = load_df_clean()
    vehicle_risk = load_vehicle_risk()
    
    vehicle_data = df_clean[df_clean['vehicle_id'] == vehicle_id]
    vehicle_risk_data = vehicle_risk[vehicle_risk['vehicle_id'] == vehicle_id]
    
    return {
        'vehicle_records': vehicle_data.sort_values('timestamp', ascending=False).head(100),
        'vehicle_summary': vehicle_risk_data.to_dict('records')[0] if len(vehicle_risk_data) > 0 else None,
    }


def get_risk_level_by_engine_status():
    """Cross-tabulation: risk_level vs engine_status"""
    df_clean = load_df_clean()
    if 'risk_level' not in df_clean.columns or 'engine_status_k2_all' not in df_clean.columns:
        return pd.DataFrame()
    
    crosstab = pd.crosstab(df_clean['engine_status_k2_all'], df_clean['risk_level'])
    return crosstab.reset_index()


def get_risk_level_by_iso_anomaly():
    """Cross-tabulation: risk_level vs iso_anomaly"""
    df_clean = load_df_clean()
    if 'risk_level' not in df_clean.columns or 'iso_anomaly' not in df_clean.columns:
        return pd.DataFrame()
    
    crosstab = pd.crosstab(df_clean['iso_anomaly'], df_clean['risk_level'])
    return crosstab.reset_index()


def get_anomaly_by_vehicle_type():
    """Anomaly rate by vehicle type"""
    df_clean = load_df_clean()
    if 'vehicle_type' not in df_clean.columns or 'iso_anomaly' not in df_clean.columns:
        return pd.DataFrame()
    
    result = df_clean.groupby('vehicle_type')['iso_anomaly'].agg(['sum', 'count']).reset_index()
    result.columns = ['vehicle_type', 'anomaly_count', 'total_count']
    result['anomaly_rate'] = result['anomaly_count'] / result['total_count']
    result['anomaly_rate_pct'] = result['anomaly_rate'] * 100
    return result.sort_values('anomaly_rate_pct', ascending=False)


def get_anomaly_by_road_class():
    """Anomaly rate by road class"""
    df_clean = load_df_clean()
    if 'road_class' not in df_clean.columns or 'iso_anomaly' not in df_clean.columns:
        return pd.DataFrame()
    
    result = df_clean.groupby('road_class')['iso_anomaly'].agg(['sum', 'count']).reset_index()
    result.columns = ['road_class', 'anomaly_count', 'total_count']
    result['anomaly_rate'] = result['anomaly_count'] / result['total_count']
    result['anomaly_rate_pct'] = result['anomaly_rate'] * 100
    return result.sort_values('anomaly_rate_pct', ascending=False)


def get_anomaly_by_engine_status():
    """Anomaly rate by engine status"""
    df_clean = load_df_clean()
    if 'engine_status_k2_all' not in df_clean.columns or 'iso_anomaly' not in df_clean.columns:
        return pd.DataFrame()
    
    result = df_clean.groupby('engine_status_k2_all')['iso_anomaly'].agg(['sum', 'count']).reset_index()
    result.columns = ['engine_status', 'anomaly_count', 'total_count']
    result['anomaly_rate'] = result['anomaly_count'] / result['total_count']
    result['anomaly_rate_pct'] = result['anomaly_rate'] * 100
    return result
