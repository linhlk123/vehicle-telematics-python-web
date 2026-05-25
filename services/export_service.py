"""
Export Service - Export data and reports
"""
import pandas as pd
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
EXPORT_DIR = BASE_DIR / "exports"


def ensure_export_dir():
    """Ensure exports directory exists"""
    if not EXPORT_DIR.exists():
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def export_dataframe_to_csv(df, filename):
    """Export DataFrame to CSV file"""
    ensure_export_dir()
    
    filepath = EXPORT_DIR / filename
    
    try:
        df.to_csv(filepath, index=False)
        return {
            'success': True,
            'message': f"Successfully exported to {filepath}",
            'filepath': str(filepath)
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Failed to export: {e}",
            'error': str(e)
        }


def export_vehicle_risk_report():
    """Export vehicle risk report"""
    from services.data_service import load_vehicle_risk
    
    vehicle_risk = load_vehicle_risk()
    return export_dataframe_to_csv(
        vehicle_risk,
        f"vehicle_risk_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )


def export_model_comparison_report():
    """Export model comparison report"""
    from services.data_service import load_model_results
    
    model_results = load_model_results()
    return export_dataframe_to_csv(
        model_results,
        f"model_comparison_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )


def get_export_list():
    """Get list of exported files"""
    ensure_export_dir()
    
    if not EXPORT_DIR.exists():
        return []
    
    files = []
    for f in EXPORT_DIR.iterdir():
        if f.is_file() and f.suffix == '.csv':
            files.append({
                'name': f.name,
                'path': str(f),
                'size': f.stat().st_size,
            })
    
    return sorted(files, key=lambda x: x['name'], reverse=True)
