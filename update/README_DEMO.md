# ⚡ PLANORA - Autoscaling Intelligence System

**Demo Dashboard cho DATAFLOW 2026: THE ALCHEMY OF MINDS**

## 🚀 Quick Start (5 Phút)

### 1. Cài đặt Dependencies
```bash
pip install streamlit pandas numpy plotly
pip install scikit-learn tensorflow  # Nếu dùng LSTM
pip install statsmodels prophet      # Nếu dùng ARIMA/Prophet
```

### 2. Chạy Demo
```bash
cd src
streamlit run app_optimized.py
```

hoặc nếu từ root directory:
```bash
streamlit run src/app_optimized.py
```

### 3. Mở Browser
- Dashboard sẽ tự động mở tại `http://localhost:8501`
- Nếu không, mở link manually

---

## 📁 Cấu trúc Project

```
PLANORA/
├── src/
│   ├── app_optimized.py          # ⭐ Main dashboard (CHẠY FILE NÀY)
│   ├── config_optimized.py       # Configuration
│   ├── core/
│   │   ├── autoscaler.py         # 3-Layer Defense Logic
│   │   └── anomaly.py            # Anomaly Detection
│   ├── engine/
│   │   ├── predictor_factory.py  # Model Factory
│   │   ├── loader.py             # Model Loader
│   │   └── arima_model.py        # ARIMA Implementation
│   └── utils/
│       └── simulation.py         # Data Simulator
├── data/                         # CSV files (test data)
├── models/                       # Trained models
│   ├── result_lstm/             # LSTM predictions
│   └── results_prophet/         # Prophet predictions
└── README.md
```

---

## 🎮 Cách Sử Dụng Dashboard

### Control Center (Sidebar)
1. **Update Interval**: Tốc độ simulation (0.1-2.0s)
2. **Data Resolution**: Chọn 1m, 5m, hoặc 15m
3. **Forecasting Model**: 
   - LSTM (Pre-calculated) ← **KHUYẾN NGHỊ CHO DEMO**
   - Prophet (Pre-calculated)
   - LSTM (Live) - Cần model file
   - ARIMA - Train on-the-fly
   - Prophet - Cần model file

4. **START SIMULATION**: Bật/tắt simulation

### Main Dashboard
- **Metrics Row**: Traffic, Forecast, Active Nodes, Workload Status
- **3-Layer Defense Panel**: 
  - L1: Predictive (AI Forecast)
  - L2: Reactive (Safety Net)
  - L3: Stability Rule (Cooldown)
- **Traffic Chart**: Real-time vs Forecast
- **Server Fleet**: Visual grid của active nodes
- **Forecast Error**: Residuals chart

---

## 🎯 Demo Scenarios

### Scenario 1: Normal Traffic Pattern
```
Resolution: 1m
Model: LSTM (Pre-calculated)
Observe: System scales smoothly
```

### Scenario 2: Traffic Spike
```
Resolution: 5m
Watch: L2 Reactive Defense triggers override
Result: Quick scale-out to handle spike
```

### Scenario 3: Cooldown Mechanism
```
After scale-out, watch L3 block scale-in
Shows: Stability rule prevents flapping
```

---

## 🔧 Troubleshooting

### Issue: "No data found"
**Fix**: 
1. Kiểm tra folder `data/` có file `test_1min.csv`, `test_5min.csv`, `test_15min.csv`
2. Nếu không có, dashboard sẽ tự generate synthetic data
3. Hoặc tải data từ models/result_lstm/ và models/results_prophet/

### Issue: "Import Error"
**Fix**: 
```bash
cd src  # Chắc chắn đang ở đúng folder
python -c "import config, core, engine, utils"  # Test imports
```

### Issue: Dashboard chậm
**Fix**:
1. Giảm Update Interval lên 1.0-2.0s
2. Đóng các tab browser khác
3. Chọn Pre-calculated models (nhanh hơn)

---

## 📊 Data Format

### Input CSV Format
```csv
timestamp,requests
2024-01-01 00:00:00,120
2024-01-01 00:01:00,135
2024-01-01 00:02:00,142
...
```

### Predictions CSV Format (Pre-calculated)
```csv
timestamp,actual,predicted
2024-01-01 00:00:00,120,118
2024-01-01 00:01:00,135,133
...
```

---

## 🎨 Customization

### Thay đổi Theme Colors
Edit `app_optimized.py`, section CSS:
```css
:root {
    --cyan: #00f0ff;     /* Primary color */
    --purple: #a855f7;   /* Secondary color */
    --green: #00ff88;    /* Success */
    --amber: #ffd60a;    /* Warning */
    --red: #ff2e63;      /* Danger */
}
```

### Thay đổi Scaling Thresholds
Edit `config_optimized.py`:
```python
DEFAULT_SCALE_OUT_THRESHOLD = 150  # req/min
DEFAULT_SCALE_IN_THRESHOLD = 50
DEFAULT_COOLDOWN_PERIOD = 3
```

---

## 🏆 Demo Tips cho Presentation

### 1. **Start Strong** (30s)
- Mở dashboard → Ngay lập tức show traffic chart đang chạy
- Highlight: "Real-time AI prediction vs Actual load"

### 2. **Show 3-Layer Defense** (1m)
- Point to decision panel
- Explain: "Predictive + Reactive + Stability"
- Show override khi spike xảy ra

### 3. **Visual Impact** (30s)
- Server grid animation
- Color changes (green → amber → red)
- Smooth transitions

### 4. **Technical Depth** (1m)
- Sidebar: Switch models (LSTM → ARIMA)
- Show metrics: MAE, RMSE từ error chart
- Explain cooldown mechanism

### 5. **Cost Savings** (30s)
- Compare: AI autoscaling vs Fixed replicas
- Show efficiency từ utilization %

---

## 📝 Evaluation Criteria Alignment

| Tiêu chí | Implementation |
|----------|----------------|
| **Tính đúng đắn** | ✅ 3-Layer Defense, ARIMA/LSTM models |
| **Hiệu quả** | ✅ Cached data loading, optimized charts |
| **Trình bày & Demo** | ✅ Cyberpunk theme, smooth animations |
| **Giải pháp kỹ thuật** | ✅ Multi-model support, API-ready |
| **Tính sáng tạo** | ✅ 3-Layer hybrid approach |
| **Tính hoàn thiện** | ✅ Clean code, comprehensive docs |

---

## 🔗 Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Charts**: https://plotly.com/python/
- **ARIMA Tutorial**: https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html

---

## 📧 Support

Nếu gặp vấn đề:
1. Check console output
2. Review error messages
3. Verify file paths trong sidebar

---

**Good luck với demo! 🚀**
