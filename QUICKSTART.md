# 🚀 Quick Start Guide

## Installation & Running (2 minutes)

### Option 1: Local Python

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:8080
```

### Option 2: Docker

```bash
# Build and run
docker compose up --build

# Open http://localhost:8080
```

---

## ✅ What You Get

### 8 Interactive Pages
- 📊 **Overview** - Fleet metrics & dashboards
- 🔄 **Pipeline** - Data mining workflow
- 🧮 **Clustering** - Algorithm comparison
- 🎯 **Anomaly** - Unusual patterns detection
- ⚠️ **Risk Scoring** - Maintenance risk formula
- 🤖 **ML Models** - 6 trained models
- 🔮 **Prediction** - Interactive predictions
- 🔧 **Maintenance** - Vehicle prioritization

### Algorithms Implemented
- ✅ K-Means Clustering (2 operational states)
- ✅ GMM & BIRCH Comparison
- ✅ Isolation Forest (Anomaly Detection)
- ✅ 8 Risk Flags (Weighted Formula)
- ✅ 6 ML Models (Hist Gradient Boosting best)
- ✅ Vehicle Risk Aggregation

### UI Features
- 🎨 Premium glassmorphism design
- 🌑 Dark mode dashboard
- 📈 Interactive Plotly charts
- 🎯 Responsive sidebar navigation
- 📱 Mobile-friendly components

---

## 📊 Data Structure

Place these CSV files in `data/` folder:

### Required Columns

**df_clean.csv** (Telemetry Records)
```
vehicle_id, timestamp, vehicle_type, fleet, fuel_type, road_class,
speed_kmh, rpm, engine_temp_c, throttle_pct, fuel_rate_lph, accel_ms2, brake_pct,
stress_index, thermal_stress, fuel_efficiency_kml,
kmeans_cluster_k2_compare, engine_status_k2_all,
iso_anomaly_score, iso_anomaly,
high_stress_flag, high_rpm_flag, high_fuel_flag, aggressive_throttle_flag,
harsh_brake_flag, harsh_accel_flag, low_efficiency_flag,
record_risk_score, risk_level
```

**vehicle_risk.csv** (Vehicle-Level Aggregation)
```
vehicle_id, total_records, avg_risk_score, high_risk_count, medium_risk_count, low_risk_count,
high_risk_rate, medium_risk_rate, low_risk_rate, anomaly_rate, high_stress_rate,
high_risk_rate_pct, anomaly_rate_pct, high_stress_rate_pct,
maintenance_priority, recommendation
```

**model_results.csv** (ML Model Evaluation)
```
model, accuracy, precision_macro, recall_macro, f1_macro, f1_weighted, status
```

**clustering_results.csv** (Clustering Comparison)
```
Algorithm, Approach, n_clusters, Silhouette Score, Davies-Bouldin Index, Calinski-Harabasz Index
```

---

## 🤖 ML Models

Place trained models in `models/` folder:

```
models/
├── logistic_regression_model.joblib
├── decision_tree_model.joblib
├── random_forest_model.joblib
├── extra_trees_model.joblib
├── hist_gradient_boosting_model.joblib  (Best)
└── adaboost_model.joblib
```

**Note**: If models are missing, the app will show warnings but continue running with mock data.

---

## 🎨 Explore the UI

### Page Navigation
Click menu items in the left sidebar to navigate between pages.

### Try These Actions

1. **Overview Page**
   - View fleet KPI cards
   - Check risk distribution chart
   - Click "View Model Lab" quick action

2. **Clustering Studio**
   - Compare 3 clustering algorithms
   - Review metrics comparison
   - See centroid profiles

3. **Anomaly Observatory**
   - Explore anomaly patterns by vehicle type
   - Analyze by road class
   - View top anomalous records

4. **Prediction Playground**
   - Adjust telemetry inputs
   - Select different ML models
   - Toggle "Compare All Models"
   - View generated features
   - See probabilities

5. **Maintenance Queue**
   - Search vehicles
   - Filter by priority level
   - Sort by risk score

---

## 🔧 Key Features to Explore

### Risk Scoring
- View the weighted formula (25% stress + 25% anomaly + ...)
- See threshold table for each flag
- Review risk level distribution

### ML Models
- Model leaderboard sorted by F1 Macro
- Confusion matrix for best model
- Performance comparison charts

### Anomaly Detection
- 5% contamination rate
- Anomaly breakdown by vehicle type, road class
- Top anomalies with details

### Algorithm Pipeline
- 10-step visualization
- Detailed explanation for each step
- Input/output specifications

---

## 🚨 Troubleshooting

### Port 8080 Already in Use
```bash
# Change port in app.py last line:
ui.run(host="0.0.0.0", port=8081, ...)
```

### Missing Data Files
- App creates mock data automatically
- Check console for ⚠️ warnings
- Place real CSV files in `data/` folder

### Model Files Not Found
- Models are optional, app warns but continues
- Place joblib files in `models/` folder
- Unavailable models disabled in selector

### Docker Issues
```bash
# Rebuild image
docker compose down
docker compose up --build --force-recreate
```

---

## 📈 Performance Tips

- **Large datasets**: Load only recent data
- **Slow queries**: Use filters in Maintenance Queue
- **Caching**: Data is cached after first load
- **Charts**: Plotly charts are interactive - hover for details

---

## 🔐 Security Notes

- No authentication in MVP (add later)
- Run behind reverse proxy in production
- Validate file uploads if added
- Use HTTPS for external deployments

---

## 📚 Learn More

- See `README.md` for full documentation
- Check `app.py` for page structure
- Review `services/` for business logic
- Explore `components/` for UI patterns

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Prepare data files
3. ✅ Place model files
4. ✅ Run the app
5. ✅ Explore all pages
6. ✅ Try predictions
7. ✅ Deploy with Docker

**You're ready to go! 🚀**

```bash
python app.py
# Open http://localhost:8080
```
