# 🚀 Proactive Autoscaling Dashboard
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**PLANORA** là hệ thống dashboard giám sát và điều phối tài nguyên tự động (autoscaling) dựa trên dự báo AI, được thiết kế theo phong cách AWS CloudWatch/Auto Scaling Console.

---

## 📋 Mục lục

- [Tính năng chính](#-tính-năng-chính)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Hướng dẫn cài đặt](#-hướng-dẫn-cài-đặt)
- [Hướng dẫn chạy ứng dụng](#-hướng-dẫn-chạy-ứng-dụng)
- [Cấu trúc Dashboard](#-cấu-trúc-dashboard)
- [Giải thích các tính năng](#-giải-thích-các-tính-năng)
- [Roadmap](#-roadmap)
- [Liên hệ](#-liên-hệ)

---

## ✨ Tính năng chính

### 🎯 **Dự báo đa thời điểm (Multi-Horizon Forecasting)**
- **Forecast +1m**: Dự báo tải sau 1 phút
- **Forecast +5m**: Dự báo tải sau 5 phút (dùng cho quyết định scaling)
- **Forecast +15m**: Dự báo tải sau 15 phút (planning dài hạn)

### 📊 **Real-time Monitoring**
- **Current Throughput**: Tải hiện tại (requests/minute)
- **Active Nodes**: Số lượng server đang chạy
- **Cost Efficiency**: Phần trăm tiết kiệm chi phí so với cấu hình cố định
- **CPU Utilization**: Mức độ sử dụng CPU trung bình

### 🤖 **Intelligent Autoscaling**
- Tự động tăng/giảm số lượng server dựa trên dự báo AI
- Cooldown period để tránh scaling liên tục (flapping)
- Ngưỡng tùy chỉnh cho scale-out và scale-in

### 📈 **Model Performance Metrics**
- **MAE** (Mean Absolute Error)
- **RMSE** (Root Mean Squared Error)
- **MAPE** (Mean Absolute Percentage Error)
- Error distribution visualization

### 🔒 **Security & Anomaly Detection**
- Phát hiện DDoS attacks
- Cảnh báo traffic spike bất thường
- Lịch sử các anomaly events

---

## 💻 Yêu cầu hệ thống

### Phần mềm cần thiết:
- **Python**: 3.8 hoặc cao hơn
- **pip**: Package manager của Python
- **Virtual Environment**: (khuyến nghị)

### Thư viện Python:
```
streamlit >= 1.30.0
pandas >= 1.4.0
numpy >= 1.21.0
plotly >= 5.14.0
```

---

## 🔧 Hướng dẫn cài đặt

### Bước 1: Clone hoặc tải project về

```bash
# Nếu có Git
git clone <repository-url>
cd "AUTOSCALING ANALYSIS"

# Hoặc tải ZIP và giải nén
```

### Bước 2: Tạo Virtual Environment (Khuyến nghị)

**Windows:**
```powershell
# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
# Tạo virtual environment
python3 -m venv .venv

# Kích hoạt virtual environment
source .venv/bin/activate
```

### Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

Nếu chưa có file `requirements.txt`, cài thủ công:

```bash
pip install streamlit pandas numpy plotly
```

---

## 🚀 Hướng dẫn chạy ứng dụng

### Cách 1: Chạy trực tiếp (đã kích hoạt virtual environment)

```bash
streamlit run app.py
```

### Cách 2: Chạy với virtual environment (Windows)

```powershell
.venv\Scripts\Activate.ps1 ; streamlit run app.py
```

### Cách 3: Chạy với virtual environment (macOS/Linux)

```bash
source .venv/bin/activate && streamlit run app.py
```

### Truy cập Dashboard

Sau khi chạy lệnh, Streamlit sẽ tự động mở browser tại:
- **Local URL**: http://localhost:8501
- **Network URL**: http://<your-ip>:8501

Nếu browser không tự động mở, copy URL từ terminal và paste vào browser.

---

## 🎨 Cấu trúc Dashboard

Dashboard được chia thành **3 tầng chính** theo phong cách AWS CloudWatch:

### 📊 **Tầng 1: Survival Metrics (KPI Header)**
Hiển thị 6 chỉ số quan trọng nhất:
1. **Current Throughput**: Tải hiện tại
2. **AI Forecast (1m)**: Dự báo 1 phút
3. **AI Forecast (5m)**: Dự báo 5 phút
4. **AI Forecast (15m)**: Dự báo 15 phút
5. **Active Nodes**: Số server đang chạy
6. **Cost Efficiency**: % tiết kiệm chi phí

### 🔮 **Tầng 2: Future Window (Main Visuals)**

**Cột trái (70%)**: Biểu đồ Traffic Monitoring
- Đường **Actual Load** (xanh cyan): Tải thực tế
- Đường **Forecast +1m** (vàng): Dự báo 1 phút
- Đường **Forecast +5m** (cam): Dự báo 5 phút
- Đường **Forecast +15m** (đỏ): Dự báo 15 phút
- Ngưỡng Scale-out/Scale-in

**Cột phải (30%)**: Resource Utilization
- Gauge chart hiển thị CPU %
- Màu sắc thay đổi theo mức độ: Xanh (0-50%), Vàng (50-80%), Đỏ (80-100%)

### 📋 **Tầng 3: Deep Analysis (3 Tabs)**

**Tab 1: Scaling Events**
- Lịch sử 10 sự kiện scaling gần nhất
- Hiển thị thời gian, hành động (SCALE_UP/SCALE_DOWN), số replicas, và lý do

**Tab 2: Model Performance**
- Metrics: MAE, RMSE, MAPE cho forecast +1m và +5m
- Biểu đồ phân phối lỗi (Error Distribution)

**Tab 3: Security & Anomaly**
- Trạng thái hiện tại (Normal/Anomaly)
- Anomaly Score
- Lịch sử các anomaly events

---

## 🎮 Giải thích các tính năng

### ⚙️ Sidebar Controls

**Simulation Settings:**
- **Simulation Speed**: Tốc độ cập nhật dashboard (0.1-2.0 giây)

**Autoscaling Thresholds:**
- **Scale-out Threshold**: Ngưỡng tải để tăng server (mặc định: 150 req/min)
- **Scale-in Threshold**: Ngưỡng tải để giảm server (mặc định: 50 req/min)
- **Cooldown Period**: Thời gian chờ giữa các lần scaling (mặc định: 3 phút)

**AI Model Settings:**
- Chọn loại model dự báo (hiện tại: Simulated)

### 🤖 AI Prediction Logic

**Hiện tại**: Sử dụng mô phỏng với hàm sin + nhiễu ngẫu nhiên

**Tương lai** (Placeholder để tích hợp):
```python
# Trong hàm get_ai_prediction_multi_horizon()
# CHỖ TRỐNG ĐỂ LẮP MODEL:
predictions = model.predict(features, horizons=[1, 5, 15])
```

Bạn có thể thay thế bằng:
- **XGBoost**: Time series forecasting
- **ARIMA**: Statistical forecasting
- **LSTM**: Deep learning approach

### 🔄 Scaling Logic

Quyết định scaling dựa trên:
1. **Dự báo 5 phút** (forecast_5m)
2. **Cooldown period**: Tránh scale liên tục
3. **Ngưỡng**:
   - Nếu `forecast_5m > threshold_up` → **SCALE_UP**
   - Nếu `forecast_5m < threshold_down` → **SCALE_DOWN**
   - Ngược lại → **KEEP**

### 🚨 Anomaly Detection

Phát hiện bất thường khi:
- **DDoS Attack**: `actual_load > forecast_1m * 1.5`
- **Unusual Drop**: `actual_load < forecast_1m * 0.5` và `actual_load < 30`

---

## 🗺️ Roadmap

### Phase 1: ✅ Core Features (Hoàn thành)
- [x] UI/UX theo AWS CloudWatch style
- [x] Multi-horizon forecasting simulation
- [x] Model performance metrics
- [x] Anomaly detection
- [x] Documentation (README.md)

### Phase 2: 🔄 AI Integration (Đang phát triển)
- [ ] Tích hợp XGBoost model
- [ ] Tích hợp ARIMA model
- [ ] Feature engineering (time, seasonality, trends)
- [ ] Model training pipeline

### Phase 3: 🚀 Advanced Features (Tương lai)
- [ ] Database integration (lưu lịch sử)
- [ ] Alert notifications (email, Slack)
- [ ] Multi-region support
- [ ] Cost optimization recommendations
- [ ] A/B testing framework

---

## 📧 Liên hệ

**Developer**: Giang Nguyen  
**Email**: pgianguyen1234@gmail.com  
**Project**: PLANORA - Proactive Autoscaling Dashboard  
**Year**: 2026

---

## 📝 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

---

## 🙏 Acknowledgments

- **AWS CloudWatch** - Design inspiration
- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **Icons8** - Icons and graphics

---

**Made with ❤️ for intelligent infrastructure management**
