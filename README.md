# ⚡ PLANORA: Intelligent Autoscaling System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![Status](https://img.shields.io/badge/Status-Demo_Ready-green)

A demonstration of **AI-Driven Autoscaling** for cloud infrastructure, implementing a **3-Layer Defense Strategy** (Predictive, Reactive, Stability).

---

## � Quick Start (Chạy trong 1 nốt nhạc)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/autoscaling-analysis.git
cd autoscaling-analysis
```

### 2. Setup Environment
```bash
# Tạo môi trường ảo (Khuyên dùng)
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Cài đặt thư viện
pip install -r src/requirements.txt
```

### 3. Run Demo
```bash
cd src
streamlit run app.py
```
> � **Note:** Access the dashboard at `http://localhost:8501`.

---

## 📂 Project Structure

```text
autoscaling-analysis/
├── src/
│   ├── app.py                # Main Dashboard logic using Streamlit
│   ├── config.py             # Configuration parameters
│   ├── models/               # AI Models & Predictions
│   │   ├── result_lstm/      # LSTM Models & Predictions
│   │   ├── results_prophet/  # Prophet Parameters & Predictions
│   │   └── results_arima/    # ARIMA Predictions
│   ├── data/                 # Raw Dataset (NASA Logs)
│   ├── core/
│   │   ├── autoscaler.py     # 3-Layer Scaling Logic
│   │   └── anomaly.py        # Z-Score Anomaly Detector
│   └── requirements.txt      # Dependencies
└── README.md
```

---

## 🧠 Core Features

### 1. 3-Layer Defense Autoscaling
The system decides the number of replicas based on three layers:
-   **Layer 1 (Predictive):** AI Models (LSTM/Prophet/ARIMA) predict future load to "pre-warm" servers.
-   **Layer 2 (Reactive):** Instant override if Real-time Load > Forecast (Flash Crowd protection).
-   **Layer 3 (Stability):** Cooldown mechanism to prevent scaling "flapping".

### 2. Advanced Anomaly Detection
-   Uses **Statistical Z-Score** (Rolling Window) to detect anomalies dynamically.
-   **⚡ SPIKE:** `Z-Score > 3` (3-Sigma Event) → Possible DDoS.
-   **📉 DROP:** `Z-Score < -3` → System failure or connection loss.

### 3. Real-time Visualization
-   **Capacity vs Demand Chart:** Visualizes system "headroom".
-   **Live Decision Log:** Explains *why* the system scaled (e.g., "Scaled out due to Reactive Override").
-   **Workload Classification:** 4-Tier status (Low/Normal/High/Spike).

---

## �️ Technology Stack
-   **Frontend:** Streamlit, Plotly
-   **Core:** Python, NumPy, Pandas
-   **AI/ML:** TensorFlow (Keras), Prophet, Statsmodels
