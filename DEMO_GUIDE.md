# 🎯 Hướng dẫn Hoàn thành Demo với Dữ liệu & Model Thật

## 📋 Checklist tổng quan

- [ ] **Bước 1**: Chuẩn bị dữ liệu thật
- [ ] **Bước 2**: Train model với dữ liệu thật
- [ ] **Bước 3**: Tích hợp vào dashboard
- [ ] **Bước 4**: Test và verify
- [ ] **Bước 5**: Chuẩn bị presentation

---

## 🔥 BƯỚC 1: Chuẩn bị Dữ liệu Thật

### Option A: Nếu bạn đã có dữ liệu

**Format yêu cầu**: CSV file với columns:
```csv
timestamp,requests_per_minute
2026-01-20 00:00:00,85
2026-01-20 00:01:00,92
2026-01-20 00:02:00,98
...
```

**Validation script**:
```python
# validate_data.py
from utils import DataLoader

# Load data
df = DataLoader.load_from_csv('DATA/your_real_data.csv')

# Validate
validation = DataLoader.validate_data(df)

if validation['is_valid']:
    print("✅ Data is valid!")
    print(f"Total records: {len(df)}")
    print(f"Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Avg load: {df['requests_per_minute'].mean():.1f} req/m")
else:
    print("❌ Data has errors:")
    for error in validation['errors']:
        print(f"  - {error}")
    for warning in validation['warnings']:
        print(f"  ⚠️ {warning}")
```

**Chạy validation**:
```bash
.venv\Scripts\Activate.ps1
python validate_data.py
```

### Option B: Nếu chưa có dữ liệu

**Collect từ hệ thống thật**:
1. Monitoring system (Prometheus, CloudWatch, etc.)
2. Application logs
3. Load balancer metrics

**Hoặc generate realistic data**:
```python
# generate_realistic_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_realistic_traffic(days=7):
    """Generate realistic traffic pattern"""
    timestamps = []
    loads = []
    
    start_time = datetime.now() - timedelta(days=days)
    
    for i in range(days * 24 * 60):  # minutes in 'days' days
        current_time = start_time + timedelta(minutes=i)
        timestamps.append(current_time)
        
        # Pattern: Low at night, high during day
        hour = current_time.hour
        day_of_week = current_time.weekday()
        
        # Base load
        if 0 <= hour < 6:  # Night
            base = 50
        elif 6 <= hour < 9:  # Morning ramp-up
            base = 80 + (hour - 6) * 20
        elif 9 <= hour < 17:  # Business hours
            base = 140
        elif 17 <= hour < 22:  # Evening
            base = 100
        else:  # Late night
            base = 60
        
        # Weekend reduction
        if day_of_week >= 5:
            base *= 0.7
        
        # Add noise and occasional spikes
        noise = np.random.normal(0, 10)
        spike = 50 if np.random.random() < 0.02 else 0  # 2% chance of spike
        
        load = max(30, int(base + noise + spike))
        loads.append(load)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'requests_per_minute': loads
    })
    
    return df

# Generate and save
df = generate_realistic_traffic(days=7)
df.to_csv('DATA/realistic_data.csv', index=False)
print(f"✅ Generated {len(df)} records")
print(f"Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Avg load: {df['requests_per_minute'].mean():.1f} req/m")
```

**Chạy**:
```bash
python generate_realistic_data.py
```

---

## 🤖 BƯỚC 2: Train Model với Dữ liệu Thật

### Script train_model.py

Tạo file `train_model.py`:

```python
"""
Train XGBoost model for load forecasting
"""
import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from utils import DataLoader, DataPreprocessor

def train_forecasting_model(data_path, horizons=[1, 5, 15]):
    """
    Train XGBoost models for multi-horizon forecasting
    
    Args:
        data_path: Path to CSV data
        horizons: List of forecast horizons (minutes)
    """
    print("📊 Loading data...")
    df = DataLoader.load_from_csv(data_path)
    
    # Validate
    validation = DataLoader.validate_data(df)
    if not validation['is_valid']:
        print("❌ Data validation failed!")
        return
    
    print(f"✅ Loaded {len(df)} records")
    
    # Extract features
    print("🔧 Extracting features...")
    df = DataPreprocessor.extract_features(df)
    df = DataPreprocessor.create_lag_features(
        df, 
        'requests_per_minute', 
        lags=[1, 5, 15, 30, 60]
    )
    
    # Prepare features
    feature_cols = [
        'hour', 'day_of_week', 'is_weekend', 'minute',
        'requests_per_minute_lag_1',
        'requests_per_minute_lag_5',
        'requests_per_minute_lag_15',
        'requests_per_minute_lag_30',
        'requests_per_minute_lag_60'
    ]
    
    X = df[feature_cols]
    
    # Train model for each horizon
    models = {}
    
    for horizon in horizons:
        print(f"\n🎯 Training model for {horizon}m forecast...")
        
        # Create target (shift backwards to predict future)
        y = df['requests_per_minute'].shift(-horizon)
        
        # Remove NaN
        mask = ~(X.isna().any(axis=1) | y.isna())
        X_clean = X[mask]
        y_clean = y[mask]
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X_clean, y_clean, test_size=0.2, shuffle=False
        )
        
        # Train XGBoost
        model = xgb.XGBRegressor(
            objective='reg:squarederror',
            max_depth=6,
            learning_rate=0.1,
            n_estimators=100,
            subsample=0.8,
            colsample_bytree=0.8
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        # Evaluate
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        print(f"  MAE: {mae:.2f}")
        print(f"  RMSE: {rmse:.2f}")
        print(f"  MAPE: {mape:.2f}%")
        
        # Save model
        model_path = f'models/xgboost_{horizon}m.joblib'
        joblib.dump(model, model_path)
        print(f"  ✅ Saved to {model_path}")
        
        models[horizon] = {
            'model': model,
            'mae': mae,
            'rmse': rmse,
            'mape': mape
        }
    
    # Save feature columns for later use
    joblib.dump(feature_cols, 'models/feature_columns.joblib')
    
    print("\n🎉 Training complete!")
    print("\nModel Performance Summary:")
    for horizon, metrics in models.items():
        print(f"  {horizon}m: MAE={metrics['mae']:.2f}, RMSE={metrics['rmse']:.2f}, MAPE={metrics['mape']:.2f}%")
    
    return models

if __name__ == "__main__":
    # Train with your data
    models = train_forecasting_model('DATA/realistic_data.csv')
```

### Cài đặt dependencies

```bash
.venv\Scripts\Activate.ps1
pip install xgboost scikit-learn
```

### Chạy training

```bash
python train_model.py
```

**Output mong đợi**:
```
📊 Loading data...
✅ Loaded 10080 records
🔧 Extracting features...

🎯 Training model for 1m forecast...
  MAE: 8.45
  RMSE: 12.32
  MAPE: 7.23%
  ✅ Saved to models/xgboost_1m.joblib

🎯 Training model for 5m forecast...
  MAE: 12.67
  RMSE: 18.91
  MAPE: 10.45%
  ✅ Saved to models/xgboost_5m.joblib

🎯 Training model for 15m forecast...
  MAE: 18.23
  RMSE: 25.44
  MAPE: 14.67%
  ✅ Saved to models/xgboost_15m.joblib

🎉 Training complete!
```

---

## 🔌 BƯỚC 3: Tích hợp vào Dashboard

### Update app.py để sử dụng real model

Tạo file `app_production.py` (hoặc update `app.py`):

```python
"""
PLANORA - Production Mode with Real Data & Model
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import time

from config.settings import SIMULATION_STEPS, INITIAL_REPLICAS, COST_PER_REPLICA, FIXED_REPLICAS
from utils import (
    DataLoader, ModelManager,
    scaling_logic, calculate_cpu_utilization, calculate_cost_savings
)
from components import (
    render_sidebar, render_production_mode_controls,
    create_kpi_placeholders, render_kpi_cards,
    create_traffic_chart, create_resource_gauge,
    render_scaling_events_tab, render_model_performance_tab, render_security_tab,
    render_data_info, render_model_info
)
from styles.aws_theme import get_aws_css

# Page config
st.set_page_config(
    page_title="PLANORA - Production Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_aws_css(), unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = pd.DataFrame(columns=[
            'Time', 'Actual', 'Forecast_1m', 'Forecast_5m', 'Forecast_15m',
            'Replicas', 'CPU_Util', 'Cost_AI', 'Cost_Fixed', 'Status', 'Reason', 'Anomaly'
        ])
        st.session_state.current_replicas = INITIAL_REPLICAS
        st.session_state.last_scale_time = datetime.now()
        st.session_state.total_cost_ai = 0
        st.session_state.total_cost_fixed = 0
        st.session_state.predictions_history = []
        st.session_state.data_loaded = False
        st.session_state.model_loaded = False

def main():
    initialize_session_state()
    
    # Sidebar
    settings = render_sidebar()
    prod_settings = render_production_mode_controls()
    
    # Main header
    st.title("🚀 PLANORA: Production Autoscaling Dashboard")
    st.markdown("**AWS-Style Auto Scaling | AI-Powered Load Forecasting**")
    
    # Load data if production mode
    data_df = None
    if prod_settings['mode'] == "Production (Real Data)":
        if prod_settings['data_source'] == "Upload CSV" and prod_settings['uploaded_data']:
            data_df = DataLoader.load_from_uploaded_file(prod_settings['uploaded_data'])
            st.session_state.data_loaded = True
        elif prod_settings['data_source'] == "Load from File" and prod_settings.get('data_path'):
            data_df = DataLoader.load_from_csv(prod_settings['data_path'])
            st.session_state.data_loaded = True
        
        if data_df is not None and not data_df.empty:
            render_data_info(data_df)
    
    # Load model if specified
    model_manager = ModelManager()
    if prod_settings.get('model_path'):
        if model_manager.load_model(prod_settings['model_path']):
            st.session_state.model_loaded = True
            render_model_info(model_manager)
    
    # Rest of dashboard...
    # (KPI cards, charts, tabs - same as before)
    
    st.info("💡 **Tip**: Dashboard đang chạy với production mode. Dữ liệu và model đã được load!")

if __name__ == "__main__":
    main()
```

### Hoặc đơn giản hơn: Chỉ dùng UI

**Không cần code gì thêm!** Chỉ cần:

1. Chạy `streamlit run app.py`
2. Trong sidebar:
   - Chọn "Production (Real Data)"
   - Data Source: "Load from File"
   - Data Path: `DATA/realistic_data.csv`
   - Check "Use Trained Model"
   - Model Path: `models/xgboost_5m.joblib`

---

## ✅ BƯỚC 4: Test và Verify

### Test Checklist

```bash
# 1. Test simulation mode
streamlit run app.py
# → Verify: Dashboard chạy với dữ liệu giả lập

# 2. Test với real data
# Trong sidebar: Production mode + Upload CSV
# → Verify: Data info hiển thị đúng

# 3. Test với model
# Trong sidebar: Check "Use Trained Model"
# → Verify: Model info hiển thị, predictions khác simulation

# 4. Test metrics
# → Verify: MAE, RMSE, MAPE hiển thị trong tab "Model Performance"

# 5. Test scaling decisions
# → Verify: Scaling events log có lý do rõ ràng
```

---

## 🎬 BƯỚC 5: Chuẩn bị Presentation/Demo

### A. Chụp Screenshots

```python
# capture_screenshots.py
import time
from selenium import webdriver

# Mở dashboard
driver = webdriver.Chrome()
driver.get('http://localhost:8502')
time.sleep(5)

# Chụp full page
driver.save_screenshot('screenshots/dashboard_overview.png')

# Scroll và chụp từng phần
# ... (code selenium)
```

### B. Record Video Demo

**Option 1**: OBS Studio
- Download OBS Studio
- Record màn hình dashboard
- Highlight các features

**Option 2**: Streamlit built-in recording
- Dashboard tự động record thành WebP video trong artifacts

### C. Chuẩn bị Slide Presentation

**Outline đề xuất**:

1. **Problem Statement** (1 slide)
   - Vấn đề: Autoscaling thủ công không hiệu quả
   - Solution: AI-powered proactive autoscaling

2. **Data** (1 slide)
   - Nguồn dữ liệu: [Mô tả nguồn]
   - Features: timestamp, requests_per_minute
   - Preprocessing: Time features, lag features

3. **Model** (2 slides)
   - Architecture: XGBoost multi-horizon forecasting
   - Training: 80/20 split, time-series aware
   - Performance: MAE, RMSE, MAPE cho 1m/5m/15m

4. **Dashboard** (2 slides)
   - Screenshot: KPI metrics
   - Screenshot: Traffic monitoring chart
   - Screenshot: Model performance tab

5. **Results** (1 slide)
   - Cost savings: X% vs fixed infrastructure
   - Accuracy: MAPE < 15%
   - Response time: Proactive scaling

6. **Demo** (Live)
   - Show dashboard running
   - Upload real data
   - Show predictions
   - Show scaling decisions

---

## 📝 Quick Reference Commands

```bash
# Activate environment
.venv\Scripts\Activate.ps1

# Generate realistic data
python generate_realistic_data.py

# Train model
python train_model.py

# Run dashboard
streamlit run app.py

# Access dashboard
# → http://localhost:8502
```

---

## 🎯 Final Checklist

- [ ] Dữ liệu thật đã chuẩn bị (CSV format đúng)
- [ ] Model đã train xong (3 models: 1m, 5m, 15m)
- [ ] Dashboard chạy được với production mode
- [ ] Screenshots đã chụp
- [ ] Video demo đã record (optional)
- [ ] Slide presentation đã chuẩn bị
- [ ] Đã test tất cả features

---

**🎉 Chúc bạn demo thành công!**
