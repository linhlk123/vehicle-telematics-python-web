# 🔧 Environment Setup Guide

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git (optional, for version control)
- Docker (optional, for containerized deployment)

Check your Python version:
```bash
python --version
# or
python3 --version
```

---

## Option 1: Local Setup (Recommended for Development)

### 1. Create Virtual Environment

**Windows (CMD/PowerShell):**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your terminal
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal
```

### 2. Upgrade pip

```bash
# Windows, macOS, Linux
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# From project directory
pip install -r requirements.txt
```

**Expected output** (7 packages):
```
Successfully installed nicegui-1.4.0
Successfully installed pandas-2.0.0
Successfully installed numpy-1.24.0
Successfully installed plotly-5.0.0
Successfully installed scikit-learn-1.3.0
Successfully installed joblib-1.3.0
Successfully installed python-multipart-0.0.6
```

### 4. Verify Installation

```bash
# Check packages
pip list

# Should show:
# nicegui        1.4.0+
# pandas         2.0.0+
# plotly         5.0.0+
# scikit-learn   1.3.0+
# joblib         1.3.0+
```

### 5. Run Application

```bash
python app.py
```

**Expected output:**
```
Uvicorn running on http://0.0.0.0:8080
```

Open browser and visit: **http://localhost:8080**

---

## Option 2: Docker Setup (Production-Ready)

### Prerequisites
- Docker Desktop installed and running
- docker-compose command available

### 1. Build Image

```bash
# From project directory
docker build -t telematics-app:latest .
```

### 2. Run with Docker Compose

```bash
# Start all services
docker compose up --build

# In background
docker compose up -d --build
```

### 3. Access Application

Open browser: **http://localhost:8080**

### 4. View Logs

```bash
# Follow logs
docker compose logs -f telematics-app

# Stop services
docker compose down
```

---

## Data & Model Setup

### 1. Prepare CSV Files

Create these files in `data/` folder:

**df_clean.csv** (~50,000 rows)
```csv
vehicle_id,timestamp,speed_kmh,rpm,engine_temp_c,throttle_pct,fuel_rate_lph,accel_ms2,brake_pct,vehicle_type,fleet,fuel_type,road_class,stress_index,thermal_stress,fuel_efficiency_kml,kmeans_cluster_k2_compare,engine_status_k2_all,iso_anomaly_score,iso_anomaly,high_stress_flag,high_rpm_flag,high_fuel_flag,high_throttle_flag,high_accel_flag,high_brake_flag,low_efficiency_flag,abnormal_pattern_flag,record_risk_score,risk_level,maintenance_priority,recommendation
VH001,2024-01-01 00:00:00,50,2000,85,25,15.5,0.5,10,truck,Fleet-A,diesel,highway,0.025,0.017,3.23,0,1,0.15,False,False,False,False,False,False,False,False,0.12,LOW,NORMAL,Keep current schedule
...
```

**vehicle_risk.csv** (1 row per vehicle)
```csv
vehicle_id,avg_risk_score,high_risk_rate_pct,anomaly_rate_pct,high_stress_rate_pct,maintenance_priority,recommendation,vehicle_type,fleet
VH001,0.18,5.2,3.1,2.8,NORMAL,Keep current schedule,truck,Fleet-A
...
```

**model_results.csv** (6 rows - one per model)
```csv
model,accuracy,f1_macro,f1_weighted,status
logistic_regression_model,0.8245,0.8156,0.8234,Available
decision_tree_model,0.8512,0.8421,0.8501,Available
random_forest_model,0.8923,0.8834,0.8912,Available
extra_trees_model,0.8834,0.8745,0.8823,Available
hist_gradient_boosting_model,0.9145,0.9056,0.9134,Available
adaboost_model,0.8756,0.8667,0.8745,Available
```

**clustering_results.csv**
```csv
algorithm,approach,n_clusters,silhouette_score,davies_bouldin_index,calinski_harabasz_index
K-Means,Centroid-based,2,0.58,0.92,1842.5
GMM,Model-based,2,0.52,1.05,1642.3
BIRCH,Hierarchical,2,0.55,0.98,1745.8
```

### 2. Add Trained ML Models

Place joblib files in `models/` folder:

```
models/
├── logistic_regression_model.joblib
├── decision_tree_model.joblib
├── random_forest_model.joblib
├── extra_trees_model.joblib
├── hist_gradient_boosting_model.joblib
├── adaboost_model.joblib
└── mlp_neural_network_model.joblib (optional)
```

**Model Requirements:**
- Trained scikit-learn models
- Must have `.predict()` method
- Optionally have `.predict_proba()` method
- Saved with joblib: `joblib.dump(model, 'model_name.joblib')`

---

## Troubleshooting

### Python Not Found

**Error:** `python: command not found` or `'python' is not recognized`

**Solution:**
- Install Python 3.11+ from python.org
- Add Python to PATH
- Use `python3` instead of `python`
- Restart terminal after installation

### Virtual Environment Issues

**Error:** `(venv) not showing in terminal`

**Solution:**
```bash
# Windows - Try PowerShell
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1

# Or use CMD
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

### Dependency Installation Fails

**Error:** `ERROR: Could not find a version that satisfies the requirement`

**Solution:**
```bash
# Update pip first
pip install --upgrade pip

# Try installing packages individually
pip install nicegui>=1.4.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install plotly>=5.0.0
pip install scikit-learn>=1.3.0
pip install joblib>=1.3.0
pip install python-multipart>=0.0.6
```

### Port 8080 Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port
# Windows
netstat -ano | findstr :8080

# macOS/Linux
lsof -i :8080

# Kill process
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>

# Or use different port (modify app.py):
# ui.run(host="0.0.0.0", port=8081, ...)
```

### Docker Build Fails

**Error:** `ERROR: failed to solve: error fetching`

**Solution:**
```bash
# Clean Docker resources
docker system prune -a

# Build again
docker build -t telematics-app:latest .

# Or use compose
docker compose up --build --no-cache
```

### Missing Data Files

**Error:** `FileNotFoundError: data/df_clean.csv`

**Solution:**
- App generates mock data automatically
- Check app console for warnings
- Create actual CSV files for real data
- Verify file paths in `services/data_service.py`

---

## Advanced Setup

### Using conda (Alternative)

```bash
# Create conda environment
conda create -n telematics python=3.11

# Activate
conda activate telematics

# Install requirements
pip install -r requirements.txt

# Run
python app.py
```

### Using pyenv (Multiple Python Versions)

```bash
# Install Python 3.11
pyenv install 3.11.0

# Create virtual environment
pyenv local 3.11.0
python -m venv venv

# Activate and install
source venv/bin/activate
pip install -r requirements.txt
```

### IDE Setup

**VS Code:**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
}
```

**PyCharm:**
1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Existing Environment"
4. Browse to `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)

---

## Performance Optimization

### Memory Usage

```bash
# Monitor memory (optional)
pip install psutil

# Check usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
```

### Data Optimization

```python
# In data_service.py - Already implemented:
# - Data caching (avoid re-reading CSVs)
# - Type optimization (int32 instead of int64)
# - String columns categorized
```

### Chart Optimization

```python
# In components/charts.py - Already implemented:
# - Client-side rendering
# - Lazy loading
# - Responsive sizing
```

---

## Next Steps After Setup

1. **Test Application**
   ```bash
   python app.py
   # Visit http://localhost:8080
   ```

2. **Verify All Pages**
   - [ ] Overview page loads
   - [ ] Algorithm pipeline visible
   - [ ] Charts render
   - [ ] Tables show data
   - [ ] Prediction form works

3. **Add Your Data**
   - Place CSV files in `data/`
   - Add ML models to `models/`
   - Restart app

4. **Customize**
   - Edit `assets/styles.css` for colors
   - Modify `services/risk_service.py` for logic
   - Update `app.py` for pages

5. **Deploy**
   - Use Docker Compose for production
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md)
   - Set up monitoring and logs

---

## Environment Variables (Optional)

Create `.env` file for configuration:

```bash
# .env
HOST=0.0.0.0
PORT=8080
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
```

Load in application:
```python
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))
```

---

## Health Check

```bash
# Verify setup
python -c "
import nicegui
import pandas
import numpy
import plotly
import sklearn
import joblib

print('✅ All dependencies installed successfully!')
print(f'NiceGUI: {nicegui.__version__}')
print(f'Pandas: {pandas.__version__}')
print(f'NumPy: {numpy.__version__}')
print(f'Plotly: {plotly.__version__}')
print(f'scikit-learn: {sklearn.__version__}')
"
```

---

## Getting Help

1. **Documentation**: See [README.md](README.md)
2. **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
3. **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
4. **Verify Install**: Run health check above

---

## Summary

```bash
# Complete setup in 5 steps:

# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py

# 5. Open browser
# http://localhost:8080
```

**You're ready to go! 🚀**
