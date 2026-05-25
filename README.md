# Vehicle Telematics Risk Intelligence

A NiceGUI-based web application for analyzing vehicle telematics data, detecting abnormal driving and engine patterns, scoring maintenance risk, and simulating machine-learning predictions for predictive maintenance.

## Overview

This project simulates a **Predictive Maintenance Platform** for vehicle fleets.

In a real-world scenario, vehicles can be equipped with IoT or OBD-II devices to collect telemetry signals such as speed, RPM, engine temperature, fuel usage, acceleration, braking behavior, and road condition. The collected data is sent to a central system, where the pipeline analyzes abnormal patterns and estimates which vehicles may require maintenance attention.

The application provides an interactive dashboard for:

- Fleet-level risk monitoring
- Data processing pipeline visualization
- Engine-state clustering
- Anomaly detection using Isolation Forest
- Rule-based risk scoring
- ML model comparison
- Single-model and multi-model prediction simulation
- Maintenance queue prioritization

## Key Features

### 1. Overview Dashboard

Displays high-level fleet intelligence:

- Total vehicles
- Total telemetry records
- High-risk rate
- Maintenance alerts
- Risk level distribution
- Fleet risk ranking
- Vehicle type risk analysis
- Recent high-risk records

### 2. Algorithm Pipeline

Visualizes the end-to-end data mining workflow:

1. Raw telemetry data
2. Data cleaning
3. Feature engineering
4. K-Means clustering
5. Isolation Forest anomaly detection
6. Risk scoring
7. ML model prediction
8. Maintenance recommendation

Each pipeline step can display detailed explanations and sample data.

### 3. Clustering Studio

Compares clustering algorithms and explains why **K-Means K=2** is selected to classify engine status into:

- Normal Operation
- High Stress

The page includes:

- Clustering comparison metrics
- Engine status distribution
- Cluster profile interpretation

### 4. Anomaly Observatory

Uses **Isolation Forest** to detect statistically unusual telemetry records.

Important note:

> An anomaly does not necessarily mean that a vehicle is broken. It means the record behaves differently from the majority of the dataset.

The page analyzes anomaly rates by:

- Vehicle type
- Road class
- Engine status

### 5. Risk Scoring Engine

Combines multiple risk signals into a record-level risk score.

Risk formula:

```text
record_risk_score =
0.25 × high_stress_flag
+ 0.25 × iso_anomaly
+ 0.15 × high_fuel_flag
+ 0.10 × aggressive_throttle_flag
+ 0.10 × high_rpm_flag
+ 0.05 × harsh_brake_flag
+ 0.05 × harsh_accel_flag
+ 0.05 × low_efficiency_flag
```

Risk levels:

| Score Range | Risk Level |
|---|---|
| 0.00 - 0.25 | LOW_RISK |
| 0.25 - 0.50 | MEDIUM_RISK |
| 0.50 - 1.00 | HIGH_RISK |

### 6. ML Model Lab

Compares trained machine-learning models for risk-level prediction.

Models used:

| Model | Accuracy | F1 Macro | F1 Weighted |
|---|---:|---:|---:|
| Hist Gradient Boosting | 0.9904 | 0.9775 | 0.9903 |
| MLP Neural Network | 0.9898 | 0.9647 | 0.9897 |
| Random Forest | 0.9819 | 0.9633 | 0.9818 |
| Decision Tree | 0.9696 | 0.9411 | 0.9697 |
| Extra Trees | 0.9726 | 0.9372 | 0.9722 |
| Logistic Regression | 0.9281 | 0.8275 | 0.9331 |

The selected production model is **Hist Gradient Boosting**, based on the best F1 Macro score and strong overall performance.

### 7. Prediction Playground

Allows users to input telemetry values and simulate risk-level prediction.

Input features include:

- Speed
- RPM
- Engine temperature
- Throttle
- Fuel rate
- Acceleration
- Brake
- Vehicle type
- Fuel type
- Road class

The system can calculate generated features such as:

- Stress index
- Thermal stress
- Fuel efficiency

### 8. Maintenance Queue

Ranks vehicles by maintenance priority using aggregated risk signals.

Maintenance priorities may include:

- Normal Monitoring
- Need Attention
- Maintenance Alert

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | NiceGUI |
| Language | Python |
| Data Processing | pandas, NumPy |
| Visualization | Plotly |
| Machine Learning | scikit-learn |
| Model Serialization | joblib |
| Deployment | Docker, Railway |
| Styling | CSS, Tailwind utility classes via NiceGUI |

## Project Structure

```text
vehicle-telematics-python-web/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
│
├── assets/
│   └── styles.css
│
├── components/
│   ├── cards.py
│   ├── charts.py
│   ├── layout.py
│   ├── pipeline.py
│   ├── prediction_form.py
│   └── tables.py
│
├── data/
│   └── CSV/result data files
│
├── models/
│   └── trained model .pkl files
│
├── pages/
│   ├── overview_page.py
│   ├── pipeline_page.py
│   ├── clustering_page.py
│   ├── anomaly_page.py
│   ├── risk_scoring_page.py
│   ├── model_lab_page.py
│   ├── prediction_page.py
│   └── maintenance_page.py
│
└── services/
    ├── data_service.py
    ├── model_service.py
    └── risk_service.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/linhlk123/vehicle-telematics-python-web.git
cd vehicle-telematics-python-web
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Default local URL:

```text
http://localhost:8081
```

## Important Environment Note

The trained `.pkl` model files are sensitive to the `scikit-learn` version.

This project uses:

```text
scikit-learn==1.8.0
```

If you see an error like:

```text
Can't get attribute '_RemainderColsList'
```

it means the model was trained or saved using a different `scikit-learn` version.

Recommended fix:

1. Use the same `scikit-learn` version locally and during training.
2. Retrain and export the model using `scikit-learn==1.8.0`.
3. Replace the old `.pkl` files in the `models/` directory.

## Docker Deployment

### 1. Build the Docker image

```bash
docker build -t telematics-risk-app .
```

### 2. Run the container locally

```bash
docker run --rm -p 8081:8081 telematics-risk-app
```

Open:

```text
http://localhost:8081
```

## Railway Deployment

This project can be deployed to Railway using Docker.

### Required `app.py` production configuration

The app should read the port from the environment:

```python
import os

if __name__ in {"__main__", "__mp_main__"}:
    port = int(os.environ.get("PORT", 8081))

    ui.run(
        host="0.0.0.0",
        port=port,
        reload=False,
        title="Telematics Risk Intelligence",
    )
```

### Railway steps

1. Push the project to GitHub.
2. Go to Railway.
3. Create a new project.
4. Select **Deploy from GitHub repo**.
5. Choose this repository.
6. Railway will detect the `Dockerfile`.
7. Generate a public domain in the service settings.

## Notes for Real-World Application

In a real deployment, the system can be extended with:

- IoT or OBD-II devices installed on vehicles
- MQTT or HTTP telemetry ingestion
- Real-time streaming pipeline
- Database storage
- Scheduled model retraining
- Alert notification system
- Fleet management integration

## Interpretation Disclaimer

The system is designed for decision support.

- `Anomaly` means statistically unusual behavior.
- `High Risk` means the record or vehicle should be reviewed.
- The system does not directly confirm mechanical failure.
- Final maintenance decisions should be validated by technicians or domain experts.

## Author

Developed as a Vehicle Telematics Risk Intelligence and Predictive Maintenance project.
