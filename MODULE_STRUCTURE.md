# PLANORA Module Structure Documentation

## 📁 Cấu trúc thư mục

```
AUTOSCALING ANALYSIS/
├── app.py                          # Main entry point (NEW - modular version)
├── test.py                         # Original monolithic version (backup)
│
├── config/
│   └── settings.py                 # Configuration constants
│
├── utils/
│   ├── __init__.py
│   ├── ai_models.py                # AI prediction logic
│   ├── scaling_logic.py            # Autoscaling decisions
│   ├── data_loader.py              # Load & validate data (NEW)
│   └── model_manager.py            # Load/save ML models (NEW)
│
├── components/
│   ├── __init__.py
│   ├── sidebar.py                  # Sidebar UI
│   ├── metrics.py                  # KPI cards
│   ├── charts.py                   # Plotly charts
│   ├── tabs.py                     # Analysis tabs
│   └── production_mode.py          # Production mode controls (NEW)
│
├── styles/
│   └── aws_theme.py                # AWS CSS theme
│
├── DATA/
│   └── sample_data.csv             # Sample CSV data (NEW)
│
├── models/
│   ├── README.md                   # Model documentation (NEW)
│   └── (your trained models here)
│
├── requirements.txt
└── README.md
```

---

## 🎯 Chức năng từng module

### 📦 config/settings.py

**Mục đích**: Centralize tất cả configuration constants

**Nội dung**:
- AWS color palette
- Default thresholds (scale-out, scale-in, cooldown)
- Simulation parameters
- Chart configurations
- Anomaly detection thresholds

**Sử dụng**:
```python
from config.settings import AWS_ORANGE, DEFAULT_SCALE_OUT_THRESHOLD
```

---

### 🤖 utils/ai_models.py

**Mục đích**: AI prediction và anomaly detection logic

**Functions**:
- `get_ai_prediction_multi_horizon(current_load, iteration)` - Dự báo 1m, 5m, 15m
- `detect_anomaly(actual_load, forecast_1m)` - Phát hiện DDoS/spike
- `generate_simulated_load(iteration)` - Tạo tải giả lập

**Placeholder cho model thật**:
```python
# CHỖ TRỐNG ĐỂ LẮP MODEL:
predictions = model.predict(features, horizons=[1,5,15])
```

---

### ⚙️ utils/scaling_logic.py

**Mục đích**: Autoscaling decision logic

**Functions**:
- `scaling_logic(forecast_5m, actual_load, session_state, ...)` - Quyết định scale up/down
- `calculate_cpu_utilization(actual_load, replicas)` - Tính CPU %
- `calculate_cost_savings(total_cost_ai, total_cost_fixed)` - Tính tiết kiệm

---

### 📊 utils/data_loader.py (NEW)

**Mục đích**: Load và validate dữ liệu từ nhiều nguồn

**Classes**:
- `DataLoader`:
  - `load_from_csv(file_path)` - Load từ CSV file
  - `load_from_uploaded_file(uploaded_file)` - Load từ Streamlit upload
  - `validate_data(df)` - Validate data format
  - `generate_sample_data(num_points)` - Tạo sample data

- `DataPreprocessor`:
  - `extract_features(df)` - Extract time features (hour, day_of_week, etc.)
  - `create_lag_features(df, target_col, lags)` - Tạo lag features

**Sử dụng**:
```python
from utils import DataLoader

# Load CSV
df = DataLoader.load_from_csv('DATA/sample_data.csv')

# Validate
validation = DataLoader.validate_data(df)
if validation['is_valid']:
    print("✅ Data valid!")
```

---

### 🧠 utils/model_manager.py (NEW)

**Mục đích**: Quản lý ML models (load, save, predict)

**Classes**:
- `ModelManager`:
  - `load_model(model_path)` - Load model từ .pkl/.joblib
  - `save_model(model, model_name, format)` - Save model
  - `predict_multi_horizon(features, horizons)` - Dự báo đa thời điểm
  - `get_model_info()` - Lấy thông tin model

- `ModelTrainer`:
  - `train_xgboost(X_train, y_train, params)` - Train XGBoost
  - `train_arima(data, order)` - Train ARIMA

**Sử dụng**:
```python
from utils import ModelManager

# Load model
manager = ModelManager()
manager.load_model('models/xgboost_model.joblib')

# Predict
predictions = manager.predict_multi_horizon(features, horizons=[1,5,15])
```

---

### 🎨 components/sidebar.py

**Mục đích**: Render sidebar controls

**Functions**:
- `render_sidebar()` - Render sidebar, return settings dict

**Returns**:
```python
{
    'sim_speed': 0.5,
    'threshold_up': 150,
    'threshold_down': 50,
    'cooldown': 3,
    'model_type': 'XGBoost (Simulated)'
}
```

---

### 📈 components/metrics.py

**Mục đích**: KPI metric cards

**Functions**:
- `create_kpi_placeholders()` - Tạo 6 placeholder objects
- `render_kpi_cards(placeholders, data, history)` - Update KPI values

---

### 📊 components/charts.py

**Mục đích**: Plotly chart creation

**Functions**:
- `create_traffic_chart(history, threshold_up, threshold_down)` - Main traffic chart
- `create_resource_gauge(cpu_util)` - CPU gauge
- `create_error_distribution(predictions_history)` - Error histogram

---

### 📋 components/tabs.py

**Mục đích**: Analysis tabs rendering

**Functions**:
- `render_scaling_events_tab(history, placeholder)` - Tab 1
- `render_model_performance_tab(predictions_history, placeholder, iteration)` - Tab 2
- `render_security_tab(history, is_anomaly, anomaly_msg, placeholder)` - Tab 3

---

### 🎯 components/production_mode.py (NEW)

**Mục đích**: Production mode UI controls

**Functions**:
- `render_production_mode_controls()` - Render mode selection UI
- `render_data_info(df)` - Display data information
- `render_model_info(model_manager)` - Display model information

**Returns**:
```python
{
    'mode': 'Production (Real Data)',
    'data_source': 'Upload CSV',
    'model_path': 'models/xgboost_model.joblib',
    'uploaded_data': <UploadedFile>
}
```

---

### 🎨 styles/aws_theme.py

**Mục đích**: AWS CSS styling

**Functions**:
- `get_aws_css()` - Return complete AWS CSS string

---

## 🚀 Cách sử dụng

### Mode 1: Simulation (Default)

```bash
streamlit run app.py
```

- Sidebar: Để mode mặc định "Simulation"
- Dữ liệu: Tự động generate theo hàm sin
- AI: Sử dụng simulation logic

### Mode 2: Production với Real Data

1. **Chuẩn bị dữ liệu CSV**:
   ```csv
   timestamp,requests_per_minute
   2026-01-23 00:00:00,85
   2026-01-23 00:01:00,92
   ...
   ```

2. **Chạy app**:
   ```bash
   streamlit run app.py
   ```

3. **Trong sidebar**:
   - Chọn "Production (Real Data)"
   - Data Source: "Upload CSV" hoặc "Load from File"
   - Upload file hoặc nhập path: `DATA/sample_data.csv`

### Mode 3: Production với Trained Model

1. **Train model** (ví dụ XGBoost):
   ```python
   import xgboost as xgb
   import joblib
   
   # Train
   model = xgb.XGBRegressor(max_depth=6, learning_rate=0.1)
   model.fit(X_train, y_train)
   
   # Save
   joblib.dump(model, 'models/xgboost_model.joblib')
   ```

2. **Trong sidebar**:
   - Chọn "Production (Real Data)"
   - Check "Use Trained Model"
   - Model Path: `models/xgboost_model.joblib`

---

## 📝 So sánh test.py vs app.py

| Aspect | test.py (Old) | app.py (New) |
|--------|---------------|--------------|
| **Lines of Code** | 532 dòng | ~230 dòng |
| **Structure** | Monolithic | Modular |
| **Maintainability** | Khó | Dễ |
| **Testability** | Khó unit test | Dễ unit test |
| **Reusability** | Không | Cao |
| **Production Ready** | Không | Có |
| **Data Source** | Chỉ simulation | CSV, Upload, API |
| **Model Support** | Không | XGBoost, ARIMA, etc. |

---

## 🎓 Best Practices

### 1. Thêm model mới

Tạo file trong `utils/model_manager.py`:
```python
@staticmethod
def train_lstm(data, params):
    # Your LSTM training logic
    pass
```

### 2. Thêm data source mới

Tạo method trong `utils/data_loader.py`:
```python
@staticmethod
def load_from_api(api_url):
    # Your API loading logic
    pass
```

### 3. Thêm chart mới

Tạo function trong `components/charts.py`:
```python
def create_custom_chart(data):
    # Your chart logic
    return fig
```

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Ensure you're in the right directory
cd "d:\Study\Year4\ki2\AUTOSCALING ANALYSIS"

# Activate venv
.venv\Scripts\Activate.ps1
```

### Error: "Model file not found"
- Check path trong sidebar
- Ensure model file exists trong `models/` folder

### Error: "Invalid CSV format"
- Check CSV có columns: `timestamp`, `requests_per_minute`
- Timestamp format: `YYYY-MM-DD HH:MM:SS`

---

**Made with ❤️ for modular, scalable, production-ready applications**
