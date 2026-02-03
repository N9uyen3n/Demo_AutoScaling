import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict

# Internal Imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import config
    from core.autoscaler import Autoscaler
    from core.anomaly import AnomalyDetector
    from engine.loader import ModelLoader
    from engine.predictor_factory import PredictorFactory
    from utils.simulation import TimeTraveler
except ImportError as e:
    st.error(f"Import Error: {e}. Please run from 'src' directory.")
    st.stop()

# ──────────────────────────────────────────────
# 0.  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Planora Autoscaling",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# 1.  CUSTOM CSS (CYBERPUNK THEME)
# ──────────────────────────────────────────────
st.markdown("""
<style>
/* Font Imports */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;500;700&display=swap');

:root {
    --bg-deep: #04060d;
    --bg-card: #0b0f1a;
    --bg-card2: #111828;
    --cyan: #00e5ff;
    --green: #39ff14;
    --amber: #ffb300;
    --red: #ff3b5c;
    --text-hi: #e8edf5;
    --text-lo: #6b7a99;
}

/* App Background */
.stApp {
    background-color: var(--bg-deep);
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-hi);
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid #1e2a45;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.05);
}
div[data-testid="stMetric"] label {
    font-family: 'Orbitron', sans-serif;
    color: var(--cyan);
    font-size: 0.8rem;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.8rem;
    color: var(--text-hi);
}

/* Server Grid Cards */
.server-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 8px;
    margin-top: 10px;
}
.server-card {
    background-color: var(--bg-card2);
    border: 1px solid #1e2a45;
    border-radius: 6px;
    padding: 8px;
    text-align: center;
    transition: all 0.3s ease;
}
.server-card.active {
    border-color: var(--green);
    box-shadow: 0 0 8px rgba(57, 255, 20, 0.2);
}
.server-card.inactive {
    opacity: 0.3;
    border-color: #333;
}
.cpu-bar {
    height: 4px;
    width: 100%;
    background: #333;
    margin-top: 5px;
    border-radius: 2px;
}
.cpu-fill {
    height: 100%;
    background: var(--cyan);
    border-radius: 2px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--bg-card);
    border-right: 1px solid #1e2a45;
}

/* Titles */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--cyan) !important;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 2.  HELPER FUNCTIONS
# ──────────────────────────────────────────────
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_hybrid_data(resolution: str) -> pd.DataFrame:
    """Loads pre-calculated predictions."""
    res_map = {'1m': '1min_request_count', '5m': '5min_request_count', '15m': '15min_request_count'}
    folder_name = res_map.get(resolution)
    if not folder_name: return None
    
    path = os.path.join("models", "result_lstm", folder_name, "LSTM", "predictions.csv")
    possible_roots = ["", "../", "../../"]
    
    for root in possible_roots:
        full_path = os.path.join(root, path)
        if os.path.exists(full_path):
            try:
                df = pd.read_csv(full_path)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.rename(columns={'actual': 'requests', 'predicted': 'forecast'}, inplace=True)
                return df
            except Exception:
                continue
    return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_prophet_data(resolution: str) -> pd.DataFrame:
    """Loads pre-calculated Prophet predictions."""
    res_map = {'1m': '1min_request_count', '5m': '5min_request_count', '15m': '15min_request_count'}
    folder_name = res_map.get(resolution)
    if not folder_name: return None
    
    path = os.path.join("models", "results_prophet", folder_name, "predictions.csv")
    possible_roots = ["", "../", "../../"]
    
    for root in possible_roots:
        full_path = os.path.join(root, path)
        if os.path.exists(full_path):
            try:
                df = pd.read_csv(full_path)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df.rename(columns={'actual': 'requests', 'predicted': 'forecast'}, inplace=True)
                return df
            except Exception:
                continue
    return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_raw_data(resolution: str) -> pd.DataFrame:
    """Loads raw test data."""
    filename = f"test_{resolution.replace('m', 'min')}.csv"
    path = os.path.join("data", filename)
    possible_roots = ["", "../", "../../"]
    for root in possible_roots:
        full_path = os.path.join(root, path)
        if os.path.exists(full_path):
            try:
                df = pd.read_csv(full_path)
                if 'timestamp' not in df.columns:
                    df.rename(columns={df.columns[0]: 'timestamp'}, inplace=True)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                if 'request_count' in df.columns:
                    df.rename(columns={'request_count': 'requests'}, inplace=True)
                return df
            except Exception:
                continue
    return None

@st.cache_data(ttl=3600)
def load_train_data(resolution: str, last_n: int = 30) -> pd.DataFrame:
    """Loads last N points from train data for warm-start."""
    filename = f"train_{resolution.replace('m', 'min')}.csv"
    path = os.path.join("data", filename)
    possible_roots = ["", "../", "../../"]
    
    for root in possible_roots:
        full_path = os.path.join(root, path)
        if os.path.exists(full_path):
            try:
                df = pd.read_csv(full_path)
                if 'timestamp' not in df.columns:
                    df.rename(columns={df.columns[0]: 'timestamp'}, inplace=True)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                if 'request_count' in df.columns:
                    df.rename(columns={'request_count': 'requests'}, inplace=True)
                return df.tail(last_n).reset_index(drop=True)
            except Exception:
                continue
    return None

@st.cache_data(ttl=3600)
def load_model_predictions(model_name: str, resolution: str) -> pd.DataFrame:
    """Loads pre-calculated predictions for any model (LSTM/ARIMA/Prophet)."""
    res_map = {'1m': '1min_request_count', '5m': '5min_request_count', '15m': '15min_request_count'}
    folder_name = res_map.get(resolution)
    if not folder_name: return None
    
    # Path mapping
    if model_name == "LSTM":
        path = os.path.join("models", "result_lstm", folder_name, "LSTM", "predictions.csv")
    elif model_name == "Prophet":
        path = os.path.join("models", "results_prophet", folder_name, "predictions.csv")
    elif model_name == "Hybrid":
        path = os.path.join("models", "results_hybrid", folder_name, "hybrid_predictions.csv")
    elif model_name == "ARIMA":
        path = os.path.join("models", "results_arima", folder_name, "predictions.csv")
    else:
        return None
    
    possible_roots = ["", "../", "../../"]
    
    for root in possible_roots:
        full_path = os.path.join(root, path)
        if os.path.exists(full_path):
            try:
                df = pd.read_csv(full_path)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Rename columns to standard format
                if 'actual' in df.columns:
                    df.rename(columns={'actual': 'requests'}, inplace=True)
                
                if 'predicted' in df.columns:
                    df.rename(columns={'predicted': 'forecast'}, inplace=True)
                elif 'hybrid_pred' in df.columns:
                    df.rename(columns={'hybrid_pred': 'forecast'}, inplace=True)
                elif 'yhat' in df.columns:  # Prophet format
                    df.rename(columns={'ds': 'timestamp', 'y': 'requests', 'yhat': 'forecast'}, inplace=True)
                
                return df
            except Exception:
                continue
    return None

def get_workload_status(current_load: int, active_replicas: int, forecast: int):
    """Classifies workload into 4 tiers based on capacity utilization."""
    capacity = active_replicas * config.DEFAULT_SCALE_OUT_THRESHOLD
    if capacity == 0:
        return "CRITICAL", "#ff2e63", "🔥"
    
    utilization = (current_load / capacity) * 100
    
    # Check for spike (actual >> forecast)
    if forecast > 0:
        spike_ratio = current_load / forecast
        if spike_ratio > 1.5:  # 50% higher than forecast
            return "SPIKE", "#ff2e63", "⚡"
    
    # Normal classification
    if utilization < 40:
        return "LOW", "#00ff88", "📉"
    elif utilization < 80:
        return "NORMAL", "#00e5ff", "✅"
    elif utilization < 110:
        return "HIGH", "#ffd60a", "📈"
    else:
        return "CRITICAL", "#ff2e63", "🔥"

def render_server_grid(active_replicas: int, max_replicas: int = 12):
    """Generates HTML for the visual server grid."""
    cards = []
    for i in range(max_replicas):
        is_active = i < active_replicas
        cls = "active" if is_active else "inactive"
        icon = "🟢" if is_active else "⚪"
        # Simulate CPU load for visual effect
        cpu = int(np.random.normal(60, 15)) if is_active else 0
        cpu = max(0, min(100, cpu))
        color = "#39ff14" if cpu < 70 else "#ff3b5c"
        
        # Use on-line string concatenation or simple string to avoid indentation issues with Markdown
        card_html = f"""
<div class="server-card {cls}">
    <div style="font-size:1.2rem;">{icon}</div>
    <div style="font-family:'Share Tech Mono'; font-size:0.8rem; color:#e8edf5;">NODE-{i+1}</div>
    <div class="cpu-bar">
        <div class="cpu-fill" style="width:{cpu}%; background:{color};"></div>
    </div>
    <div style="font-size:0.6rem; color:#6b7a99; margin-top:2px">{cpu}% Load</div>
</div>"""
        cards.append(card_html)
    
    return f'<div class="server-grid">{"".join(cards)}</div>'

# ──────────────────────────────────────────────
# 3.  APP LOGIC
# ──────────────────────────────────────────────

# Sidebar
with st.sidebar:
    st.title("⚙️ SYSTEM CONTROL")
    st.markdown("---")
    
    simulation_speed = st.slider("Cycle Duration (s)", 0.1, 2.0, config.SIMULATION_SPEED_DEFAULT)
    resolution = st.selectbox("Resolution", ["1m", "5m", "15m"], index=0)
    
    # Model Selection (All Pre-calculated)
    st.markdown("### 🤖 AI Forecasting Model")
    model_type = st.selectbox(
        "Select Model",
        ["LSTM", "Prophet", "Hybrid", "ARIMA"],
        index=2, # Default to Hybrid (best)
        help="""
        **Hybrid**: LSTM + Prophet (Best Accuracy)
        **LSTM**: Deep Learning (Good for short-term)
        **Prophet**: Facebook's TS Model (Good for seasonality)
        """
    )
    
    is_running = st.checkbox("▶  ACTIVATE SYSTEM", value=True)
    
    st.markdown("---")
    st.markdown("### 🛡️ SAFEGUARDS")
    min_replicas = st.number_input("Min Replicas", 1, 10, config.MIN_REPLICAS)
    max_replicas = st.number_input("Max Replicas", 10, 50, config.MAX_REPLICAS)

# Initialize State
if 'history' not in st.session_state:
    st.session_state.history = {'timestamp': [], 'requests': [], 'replicas': [], 'forecast': []}

# Data Loading (Always Pre-calculated)
if ('resolution' not in st.session_state or 
    st.session_state.resolution != resolution or 
    'model_type' not in st.session_state or 
    st.session_state.model_type != model_type or 
    'simulator' not in st.session_state):
    
    with st.spinner(f'🔄 Loading {model_type} predictions...'):
        st.session_state.resolution = resolution
        st.session_state.model_type = model_type
        
        # Hybrid only supports 5m/15m -> Fallback to LSTM for 1m
        target_model = model_type
        if model_type == "Hybrid" and resolution == "1m":
            st.warning("⚠️ Hybrid model available for 5m/15m only. Showing LSTM for 1m.")
            target_model = "LSTM"
        
        # Load pre-calculated predictions
        df = load_model_predictions(target_model, resolution)
        
        if df is not None:
            st.toast(f"✅ {model_type} Predictions Loaded: {resolution}", icon="📈")
        else:
            st.warning(f"⚠️ {model_type} predictions not found, using synthetic data")
            dates = pd.date_range(start='2024-01-01', periods=1000, freq=resolution.replace('m', 'min'))
            reqs = 1000 + 500 * np.sin(np.arange(1000)/20) + np.random.normal(0, 50, 1000)
            forecasts = reqs + np.random.normal(0, 30, 1000)
            df = pd.DataFrame({
                'timestamp': dates, 
                'requests': list(map(int, reqs)),
                'forecast': list(map(int, forecasts))
            })
        
        st.session_state.simulator = TimeTraveler(df)
        st.session_state.history = {
            'timestamp': [], 
            'requests': [], 
            'replicas': [], 
            'forecast': []
        }

if 'autoscaler' not in st.session_state:
    st.session_state.autoscaler = Autoscaler(min_servers=min_replicas, max_servers=max_replicas)

if 'anomaly_detector' not in st.session_state:
    st.session_state.anomaly_detector = AnomalyDetector(window_size=30)

# No model loading needed - all predictions are pre-calculated

# Layout
st.markdown("## ⚡ PLANORA MISSION CONTROL")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
placeholder_metrics = st.empty()
placeholder_charts = st.empty()

def update():
    sim = st.session_state.simulator
    hist = st.session_state.history
    
    data = sim.next_tick()
    if not data:
        st.info("Simulation Complete")
        st.stop()
        
    curr_req = data.get('requests', 0)
    curr_time = data.get('timestamp', pd.Timestamp.now())
    
    # Forecast Logic (All Pre-calculated)
    fcast = data.get('forecast', curr_req)

    # Scaling
    # Get last replicas or initial config
    current_replicas = hist['replicas'][-1] if hist['replicas'] else config.INITIAL_REPLICAS
    replicas, reason, cost, details = st.session_state.autoscaler.calculate_replicas(curr_req, fcast, current_replicas)
    
    # Anomaly Detection (Statistical Z-Score)
    anomaly = st.session_state.anomaly_detector.detect(curr_req, fcast)
    
    # Update History
    hist['timestamp'].append(curr_time)
    hist['requests'].append(curr_req)
    hist['replicas'].append(replicas)
    hist['forecast'].append(fcast)
    
    if len(hist['timestamp']) > 60:
        for k in hist: hist[k] = hist[k][-60:]
        
    # UI Render
    # Calculate Workload Status
    # Get workload classification and anomaly status
    wl_status, wl_color, wl_icon = get_workload_status(curr_req, replicas, fcast)
    
    with col1:
        delta_req = curr_req - hist['requests'][-2] if len(hist['requests']) > 1 else 0
        st.metric("🌊 TRAFFIC", f"{int(curr_req):,}", f"{delta_req:+.0f}")
    
    with col2:
        delta_fcast = fcast - curr_req
        st.metric("🔮 FORECAST", f"{int(fcast):,}", f"{delta_fcast:+.0f}", delta_color="off")
    
    with col3:
        delta_replicas = replicas - current_replicas
        st.metric("🖥️ NODES", f"{replicas}", f"{delta_replicas:+d}" if delta_replicas != 0 else None)
    
    with col4:
        # Show workload status with color
        anomaly_icon = "🚨" if anomaly != "NORMAL" else "✅"
        st.metric(f"{wl_icon} WORKLOAD", wl_status, f"{anomaly_icon} {anomaly}")
        
    # ──────────────────────────────────────────────
    # DECISION INTELLIGENCE PANEL
    # ──────────────────────────────────────────────
    st.markdown("### 🧠 DECISION INTELLIGENCE (3-LAYER DEFENSE)")
    
    # Visual Comparison of Layers
    c_d1, c_d2, c_d3 = st.columns(3)
    
    with c_d1:
        st.info(f"**L1: Predictive (Attack)**\nTarget: **{details['predictive_target']}** Nodes\n*Strategy: Pre-warm based on AI Forecast*")
        
    with c_d2:
        # Highlight Reactive Override
        is_override = details['reactive_target'] > details['predictive_target']
        if is_override:
            st.error(f"**L2: Reactive (Defense)**\nTarget: **{details['reactive_target']}** Nodes\n*⚠️ OVERRIDE TRIGGERED: Load Spike Detected!*")
        else:
            st.success(f"**L2: Reactive (Defense)**\nTarget: **{details['reactive_target']}** Nodes\n*Status: Safe (Below Forecast)*")
            
    with c_d3:
        # Cooldown Status
        if details['cooldown'] > 0:
            st.warning(f"**L3: Stability Rule**\n❄️ Cooldown Active: **{details['cooldown']}** cycles\n*Action: Scale In Blocked to prevent flapping*")
        else:
            st.caption(f"**L3: Stability Rule**\n✅ Cooldown Inactive\n*Action: Ready to scale*")

    st.markdown("---")

    with placeholder_charts.container():
        # Row 1: Main Chart
        fig = go.Figure()
        
        # Actual uses current timestamps
        fig.add_trace(go.Scatter(
            x=hist['timestamp'], 
            y=hist['requests'], 
            name='Actual', 
            line=dict(color='#00e5ff', width=2), 
            fill='tozeroy', 
            fillcolor='rgba(0, 229, 255, 0.1)'
        ))
        
        # Forecast: Shift timestamps FORWARD by 1 interval (shows future prediction)
        # Calculate interval from resolution
        interval_map = {'1m': pd.Timedelta(minutes=1), '5m': pd.Timedelta(minutes=5), '15m': pd.Timedelta(minutes=15)}
        interval = interval_map.get(resolution, pd.Timedelta(minutes=1))
        
        # Shift forecast timestamps forward
        forecast_timestamps = [t + interval for t in hist['timestamp']]
        
        fig.add_trace(go.Scatter(
            x=forecast_timestamps,  # FUTURE timestamps
            y=hist['forecast'], 
            name='Forecast', 
            line=dict(color='#ffb300', dash='dash', width=2)
        ))
        fig.update_layout(
            title="TRAFFIC LOAD VS PREDICTION",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(11, 15, 26, 0.5)',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width='stretch')
        
        # Row 2: Server Grid + Residuals
        c_grid, c_res = st.columns([1, 1])
        with c_grid:
            st.markdown("### 🖥️ SERVER FLEET STATUS")
            st.markdown(render_server_grid(replicas, max_replicas=12), unsafe_allow_html=True)
            
        with c_res:
            res_val = np.array(hist['requests'], dtype=float) - np.array(hist['forecast'], dtype=float)
            fig2 = go.Figure(go.Bar(x=hist['timestamp'], y=res_val, marker_color='#ff3b5c'))
            fig2.update_layout(
                title="FORECAST ERROR RESIDUALS",
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(11, 15, 26, 0.5)',
                height=250,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig2, width='stretch')

if is_running:
    update()
    time.sleep(simulation_speed)
    st.rerun()
else:
    st.info("SYSTEM PAUSED")
