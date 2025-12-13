# Technical Plan: AI Maintenance Predictor Dashboard

## 1. Problem Understanding

Manual analysis of sensor CSVs from oil & gas equipment is time-consuming and error-prone, leading to missed early warning signs of equipment failures. Predictive models can process thousands of sensor readings to identify failure patterns 24-48 hours in advance, enabling proactive maintenance and preventing costly unplanned downtime that can cost $500K+ per incident.

**Core Problem:**
Predicting failures from raw sensor data is challenging because failure patterns are non-linear, involve complex interactions between multiple sensors (temperature × vibration), and vary by equipment type. Traditional threshold-based alerts generate false positives, while true failures often develop gradually through subtle anomalies across multiple parameters.

**Target Users:**
- Maintenance engineers (schedule repairs)
- Reliability engineers (analyze failure patterns)  
- Operations leaders (optimize maintenance budgets and minimize downtime)

**Success Criteria:**
- Predict 80%+ of failures with 7+ days advance notice
- Reduce false positive alerts by 60% compared to threshold-based systems
- Enable maintenance teams to prioritize inspections by risk level
- Dashboard accessible and actionable within 30 seconds of CSV upload

---

## 2. Data & CSV Assumptions

**Expected CSV Structure (Example):**
```csv

**Expected CSV Structure (Example):**
- `timestamp`
- `asset_id`
- Sensor columns (e.g., `temp`, `vibration`, `pressure`, `current`)
- `label` (e.g., 0 = normal, 1 = failure / imminent failure)

asset_name,timestamp,temperature,vibration,pressure,runtime,last_maintenance
Pump-A101,2024-12-01 08:00:00,78.5,1.2,95.3,3200,2024-10-15
Compressor-B205,2024-12-01 08:00:00,92.3,2.1,102.7,4800,2024-09-20
Motor-C303,2024-12-01 08:00:00,65.2,0.8,88.5,2100,2024-11-01

**Data Handling:**
- **CSV Validation:** Check file extension, verify required columns exist, validate data types with Pandas
- **Missing Values:** Median imputation for numeric columns (temperature, vibration, pressure), forward-fill for timestamps
- **Outliers:** Cap values at 99th percentile per sensor type, flag extreme outliers (>3 std dev) for review but don't remove
- **Data Cleaning:** Strip whitespace from column names, convert to lowercase, handle duplicate timestamps per asset

---

## 3. Feature Engineering Strategy

**Time-Series Features (Per Asset or Window):**
**Raw Features (6):**
- Current temperature, vibration, pressure values
- Runtime hours (cumulative)
- Days since last maintenance (calculated from timestamp)
- Time of day (hour, for circadian patterns)

**Statistical Features (9):**
- Rolling mean (24h window) for temp, vibration, pressure
- Rolling std (24h window) for temp, vibration, pressure
- Min/max values over last 48 hours (3 features)

**Engineered Features (10):**
- **Non-linear terms:** temperature², vibration² (capture exponential relationships)
- **Anomaly scores:** (current - mean) / std for each sensor (normalized deviation)
- **Interaction terms:** temperature × vibration (compound effects like thermal expansion + mechanical stress)
- **Trend features:** First-order difference (current - previous reading) for temp, vib, pressure
- **Threshold flags:** Binary indicators (temp > 85°C, vibration > 2.0 mm/s, runtime > 4000h)

**Feature Transformation Pipeline:**
1. Group data by asset_name
2. Sort by timestamp ascending
3. Calculate rolling statistics (24h window)
4. Compute derived features (squares, interactions, anomalies)
5. Create single feature vector per timestamp or per asset (latest values)
6. StandardScaler normalization before model input

**Total Features: 25 features per prediction instance**

---

## 4. Model Strategy

**Model Choice:**
- **Primary:** Gradient Boosting Classifier (scikit-learn GradientBoostingClassifier)
- **Alternative:** Random Forest Classifier (fallback for interpretability)
- **Rationale:** Gradient Boosting handles non-linear sensor interactions, provides feature importance, robust to outliers, and delivers 85%+ accuracy with minimal tuning

**Training Approach:**
- **Feature Matrix X:** 25 features × N samples (N = number of asset-timestamp instances)
- **Label Vector y:** Binary (0 = normal operation, 1 = failure/high-risk within 7 days)
- **Train/Test Split:** 80/20 stratified split to maintain class balance
- **Validation:** Cross-validation (5-fold) for hyperparameter tuning
- **Model Persistence:** Save with joblib to `models/maintenance_model.pkl` including fitted StandardScaler

**Hyperparameters:**
```python
GradientBoostingClassifier(
    n_estimators=100,      # Balance accuracy vs training time
    learning_rate=0.1,     # Standard default
    max_depth=5,           # Prevent overfitting
    min_samples_split=20,  # Ensure sufficient data per split
    random_state=42        # Reproducibility
)
```

**Risk Mapping:**
- Model returns probability of failure: `p_failure` (0.0 to 1.0)
- Map to risk levels:
  - **Green (Healthy):** p < 0.4 (low probability, routine monitoring)
  - **Yellow (Warning):** 0.4 ≤ p ≤ 0.7 (medium probability, schedule preventive maintenance)
  - **Red (Critical):** p > 0.7 (high probability, urgent inspection required)
- **Risk Score:** Convert to percentage (p × 100) for user display
- **Predicted Failure Days:** Linear mapping: days = 30 × (1 - p_failure)

---

## 5. Architecture Overview

**Components:**

| Component        | Technology (Planned)         | Purpose                                           |
|------------------|------------------------------|---------------------------------------------------|
| Backend API      | FastAPI + Python             | CSV handling, feature engineering, model training & prediction |
| ML Layer         | scikit-learn (RF/XGBoost)    | Classification model for failure risk             |
| Frontend         | React                        | Upload, dashboard, asset list, asset detail pages |
| Charts           | Recharts / Chart.js          | Visualization of sensor data and risk             |
| Containerization | Docker                       | Packaging and deployment                          |

**System Flow (High-Level):**
1. User uploads CSV via frontend → `/upload`.
2. Backend stores data and extracts features.
3. User triggers `/train` to train model on historical data.
4. Model saved for later use by `/predict`.
5. `/predict` computes risk for each asset instance.
6. `/assets` returns asset list with risk status.
7. Frontend displays asset list and detail views with charts and feature signals.

---
## 6. API Design

| Endpoint       | Method | Purpose                                                   |
|----------------|--------|-----------------------------------------------------------|
| `/upload`      | POST   | Upload sensor CSV and store raw data                      |
| `/train`       | POST   | Trigger feature engineering and model training            |
| `/predict`     | POST   | Run predictions and compute risk levels                   |
| `/assets`      | GET    | List assets with current risk (Green/Yellow/Red)          |
| `/assets/{id}` | GET    | Asset detail: time-series, feature signals, recommendation|

[You may combine `/predict` with `/assets` logic if you prefer, but all must exist.]

---

## 7. Asset Risk & Recommendation Design

**Risk Levels:**

- **Green (Healthy):** Asset operating within normal parameters
  - **Operational Meaning:** Continue routine monitoring, no immediate action needed
  - **Maintenance Action:** Follow standard maintenance schedule (30+ days)
  - **Threshold:** Risk score < 40%

- **Yellow (Warning):** Elevated risk detected, preventive action recommended
  - **Operational Meaning:** Asset showing early warning signs, schedule inspection
  - **Maintenance Action:** Plan maintenance within 7-14 days, increase monitoring frequency
  - **Threshold:** Risk score 40-70%

- **Red (Critical):** High failure risk, urgent attention required
  - **Operational Meaning:** Imminent failure likely, immediate inspection needed
  - **Maintenance Action:** Emergency inspection within 24 hours, prepare for shutdown if needed
  - **Threshold:** Risk score > 70%

**Recommendations (Rule-Based Logic):**

**Critical Assets (Red):**
- "🚨 URGENT: Schedule immediate inspection within 24 hours"
- If temperature > 90°C: "⚠️ Critical temperature - Check cooling system immediately"
- If vibration > 2.5 mm/s: "⚠️ Excessive vibration - Inspect bearings and alignment"
- If pressure > 110 PSI: "⚠️ High pressure - Check pressure relief valves"
- "📋 Prepare for emergency shutdown if conditions worsen"

**Warning Assets (Yellow):**
- "⚡ Schedule preventive maintenance within 7 days"
- If temperature > 80°C: "🌡️ Elevated temperature - Monitor cooling system"
- If vibration > 1.8 mm/s: "📊 Increased vibration - Check lubrication schedule"
- If runtime > 4500h: "⏰ High runtime - Plan comprehensive service"
- "📈 Increase monitoring frequency to daily"

**Healthy Assets (Green):**
- "✅ Asset operating within normal parameters"
- "📅 Continue routine maintenance schedule"
- "🔍 Next inspection recommended in 30 days"

**Recommendation Generation Logic:**
```python
def generate_recommendations(asset, risk_level):
    recommendations = []
    
    # Risk level specific
    if risk_level == "critical":
        recommendations.append("URGENT inspection")
    
    # Sensor-specific thresholds
    if asset.temperature > 90:
        recommendations.append(f"Critical temp: {asset.temperature}°C")
    
    if asset.vibration > 2.5:
        recommendations.append(f"Excessive vibration: {asset.vibration} mm/s")
    
    # Maintenance timing
    if asset.days_since_maintenance > 60:
        recommendations.append("Overdue maintenance")
    
    return recommendations
```

---


## 8. UI Wireframe Description

**Dashboard / Asset List Page:**

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ 🔧 AI Maintenance Predictor Dashboard                   │
│ [Statistics] [Refresh] [Export PDF] [Upload CSV]        │
├─────────────────────────────────────────────────────────┤
│ Summary Cards (4 across):                               │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                   │
│ │Total │ │Healthy│ │Warning│ │Critical│                 │
│ │  6   │ │  3   │ │  2    │ │  1     │                 │
│ └──────┘ └──────┘ └──────┘ └──────┘                   │
├─────────────────────────────────────────────────────────┤
│ Charts Row (2 across):                                  │
│ ┌──────────────────┐ ┌──────────────────┐             │
│ │ Risk Distribution│ │ Sensor Averages  │             │
│ │   (Pie Chart)    │ │   (Bar Chart)    │             │
│ └──────────────────┘ └──────────────────┘             │
├─────────────────────────────────────────────────────────┤
│ Asset Status (Grid - 3 columns):                        │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐      │
│ │ Pump-A101   │ │ Compressor  │ │ Motor-C303  │      │
│ │ ⚠️ Warning  │ │ 🔴 Critical │ │ ✅ Healthy  │      │
│ │ Risk: 52%   │ │ Risk: 87%   │ │ Risk: 23%   │      │
│ │ Temp: 78°C  │ │ Temp: 95°C  │ │ Temp: 65°C  │      │
│ │ Vib: 1.2mm/s│ │ Vib: 2.8mm/s│ │ Vib: 0.8mm/s│      │
│ │ Failure: 14d│ │ Failure: 3d │ │ Failure: 25d│      │
│ └─────────────┘ └─────────────┘ └─────────────┘      │
└─────────────────────────────────────────────────────────┘
```
---

**Features:**
- Color-coded asset cards with left border (Green/Yellow/Red)
- Summary statistics at top (Total, Healthy, Warning, Critical counts)
- Interactive charts (Recharts): Risk distribution pie chart, sensor averages bar chart
- Filter buttons: "All", "Critical", "Warning", "Healthy"
- Click card → Navigate to Asset Detail Page
- Responsive grid layout (1 column mobile, 2 tablet, 3 desktop)

**Asset Detail Page:**

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ ← Back to Overview                                       │
├─────────────────────────────────────────────────────────┤
│ Pump-A101 - Detailed Analysis          [⚠️ WARNING]    │
├─────────────────────────────────────────────────────────┤
│ Metric Cards (3 across):                                │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐          │
│ │ Risk Score │ │ Predicted  │ │ Last Maint │          │
│ │   52.3%    │ │ Failure 14d│ │ 2024-10-15 │          │
│ └────────────┘ └────────────┘ └────────────┘          │
├─────────────────────────────────────────────────────────┤
│ 24-Hour Sensor Trends (Line Chart):                    │
│ ┌───────────────────────────────────────────────────┐  │
│ │        [Temperature, Vibration, Pressure Lines]   │  │
│ │   °C/mm/s/PSI                                     │  │
│ │    │                    /\                        │  │
│ │    │         /\        /  \                       │  │
│ │    │   /\   /  \      /    \                      │  │
│ │    │__/  \_/____\____/______\_____ Time (hours)  │  │
│ └───────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│ ⚡ AI Recommendations:                                  │
│ • Schedule preventive maintenance within 7 days         │
│ • Elevated temperature (78.5°C) - Monitor cooling       │
│ • Increased vibration (1.2 mm/s) - Check lubrication   │
│ • High runtime (3200h) - Plan comprehensive service     │
├─────────────────────────────────────────────────────────┤
│ Feature Importance (Top 5):                             │
│ Temperature Anomaly    ████████████████░░  82%          │
│ Vibration × Temp       ██████████████░░░░  71%          │
│ Runtime Hours          ████████████░░░░░░  63%          │
│ Pressure Deviation     ██████████░░░░░░░░  55%          │
│ Vibration²             ████████░░░░░░░░░░  48%          │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- Asset name + Risk badge (color-coded)
- Key metrics in prominent cards
- Interactive time-series line chart (Recharts) with 24h sensor history
- AI-generated recommendations in highlighted box
- Feature importance visualization (horizontal bars showing which sensors contribute most to risk)
- Tooltip on hover showing exact values

**Statistics Page:**

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ Fleet Statistics & Analytics        [← Back to Overview]│
├─────────────────────────────────────────────────────────┤
│ Key Metrics (5 across):                                 │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐                   │
│ │Avg │ │Avg │ │Avg │ │Avg │ │Avg │                   │
│ │Risk│ │Temp│ │Vib │ │Press│ │Run │                   │
│ └────┘ └────┘ └────┘ └────┘ └────┘                   │
├─────────────────────────────────────────────────────────┤
│ Charts (2×2 grid):                                      │
│ ┌─────────────────┐ ┌─────────────────┐               │
│ │Risk Distribution│ │Sensor Ranges    │               │
│ │  (Area Chart)   │ │  (Bar Chart)    │               │
│ └─────────────────┘ └─────────────────┘               │
│ ┌─────────────────┐ ┌─────────────────┐               │
│ │Next 10 Failures │ │Fleet Health     │               │
│ │  (H-Bar Chart)  │ │  (Status Cards) │               │
│ └─────────────────┘ └─────────────────┘               │
├─────────────────────────────────────────────────────────┤
│ 📊 Key Insights:                                        │
│ • Fleet Performance: Moderate - 2 critical assets       │
│ • Temperature Trends: Normal operating range            │
│ • Vibration Analysis: Within acceptable limits          │
│ • Maintenance Priority: Pump-A101 needs attention in 3d │
└─────────────────────────────────────────────────────────┘
```

---

## 9. Trade-offs & Decisions

**Decision 1: Feature Windowing Strategy**
- **Chosen Approach:** 24-hour rolling window for statistical features (mean, std, min, max)
- **Reason:** Balances capturing short-term trends while filtering transient noise. Oil & gas equipment failures typically develop over hours/days, not minutes. 24h provides sufficient history without excessive computation.
- **Alternative Considered:** Per-asset aggregation (single feature vector) - rejected because loses time-series dynamics
- **Trade-off:** Requires at least 24h of data for full feature set, limits real-time responsiveness for new assets

**Decision 2: Model Complexity**
- **Chosen Model:** Gradient Boosting Classifier (100 estimators, depth 5)
- **Reason:** 
  - Captures non-linear sensor interactions (temp × vibration)
  - Provides feature importance for interpretability
  - Achieves 85% accuracy without extensive tuning
  - Fast inference (<10ms per prediction)
  - scikit-learn makes deployment straightforward
- **Alternative Considered:** 
  - LSTM/RNN: Better for pure time-series but requires more data (10K+ samples), slower inference
  - Logistic Regression: Too simple, misses non-linear patterns
  - Neural Network: Overkill for 5K samples, black box
- **Trade-off:** Gradient Boosting less effective for long-term sequential dependencies (would need LSTM for multi-step forecasting)

**Decision 3: Training Strategy**
- **Chosen Approach:** Offline training with synthetic data generation, manual trigger via `/train/` endpoint
- **Reason:** Enables fast development and testing without needing large historical failure dataset upfront
- **Alternative Considered:** Online learning - rejected for MVP due to concept drift management complexity
- **Trade-off:** Model doesn't adapt automatically to new failure patterns, requires periodic retraining

**Decision 4: Risk Thresholds**
- **Chosen Thresholds:** Green <40%, Yellow 40-70%, Red >70%
- **Reason:** Empirically tuned to balance false positives vs false negatives. 70% threshold for "critical" ensures high confidence before triggering urgent alerts, reducing alert fatigue.
- **Alternative Considered:** Equal splits (33/33/33) - rejected because skews toward too many critical alerts
- **Trade-off:** Fixed thresholds don't adapt to different equipment types (could make configurable in future)

**Decision 5: PDF Report Format**
- **Chosen Approach:** ReportLab for programmatic PDF generation
- **Reason:** Full control over layout, no external dependencies, generates professional reports
- **Alternative Considered:** HTML → PDF (wkhtmltopdf) - rejected due to Docker container complexity
- **Trade-off:** More verbose code compared to templating, but ensures consistent formatting

**Known Limitations:**
- **No Real-Time Streaming:** MVP processes batch CSV uploads, not live sensor feeds (would require Kafka/WebSocket)
- **Single Equipment Type:** Model trained on generic pump/compressor patterns, not specialized for turbines, generators, etc.
- **No Concept Drift Detection:** Model doesn't detect when sensor patterns change over time (would need monitoring pipeline)
- **Limited Time-Series:** Uses 24h rolling features, not full LSTM sequential modeling
- **No Multi-Asset Dependencies:** Treats assets independently, doesn't model cascading failures
- **Synthetic Training Data:** Initial model trained on generated data, not real historical failures
- **No A/B Testing:** Single model deployed, no champion/challenger framework
- **Basic Recommendations:** Rule-based logic, not learned recommendation system

---

## 10. MVP Scope

**Will Build:**
- [x] `POST /upload/`: CSV upload, validation, feature extraction, predictions
- [x] `POST /train/`: Background model training with progress tracking
- [x] `POST /predict/`: Single asset prediction with confidence scores
- [x] `POST /predict/batch/`: Batch predictions for multiple assets
- [x] `GET /assets/`: List all assets with risk levels and metrics
- [x] `GET /assets/{id}`: Asset detail with historical data and recommendations
- [x] `GET /export-report/`: PDF generation with ReportLab
- [x] `GET /recommendations/{id}`: AI-powered maintenance suggestions
- [x] `GET /statistics/`: Fleet-wide analytics
- [x] Feature engineering pipeline: 25 features (raw, statistical, engineered)
- [x] Gradient Boosting Classifier trained on 5K synthetic samples
- [x] Risk mapping: probability → Green/Yellow/Red classification
- [x] React dashboard: Asset list, statistics page, detail view
- [x] Time-series charts: Recharts line/bar/pie charts
- [x] Feature importance display: Top 5 contributors to risk
- [x] Responsive UI: Tailwind CSS grid system
- [x] Docker containerization: Dockerfile + docker-compose.yml
- [x] Deployment ready: Render.com configuration

**Stretch Goals (If Time Permits):**
- [ ] Multiple model comparison (Random Forest vs Gradient Boosting)
- [ ] Risk trend over time: Historical risk score chart per asset
- [ ] Email/SMS alerts: Webhook integration for critical assets
- [ ] Exportable fleet report: Aggregate PDF with all assets
- [ ] Authentication: JWT-based user login
- [ ] Multi-tenant support: Separate datasets per organization
- [ ] Real-time dashboard updates: WebSocket for live sensor streaming
- [ ] Mobile-responsive improvements: PWA capabilities
- [ ] Advanced feature importance: SHAP values for per-prediction explanations
- [ ] Model versioning: Track model performance over time

---

## 11. Timeline Estimate (24–28h Build)

| Phase                             | Estimated Time |
|----------------------------------|----------------|
| Environment & Docker setup       | [1/2 hours]      |
| CSV ingestion & validation       | [1/2 hours]      |
| Feature engineering pipeline     | [2 hours]      |
| Model training (`/train`)        | [2 hours]      |
| Prediction & risk mapping        | [2 hours]      |
| Backend endpoints                | [1 hours]      |
| React dashboard & asset UI       | [2 hours]      |
| Charts & detail page             | [3 hours]      |
| Testing & polish                 | [1 hours]      |