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

def get_workload_status(current_load, active_replicas):
    """Classifies workload into Low/Normal/High/Spike based on system capacity."""
    capacity = active_replicas * config.DEFAULT_SCALE_OUT_THRESHOLD
    if capacity == 0: return "SPIKE", "#ff0000", "🔥" # Avoid div by zero
    
    utilization = (current_load / capacity) * 100
    
    if utilization < 40:
        return "LOW", "#00e5ff", "💤"
    elif utilization < 80:
        return "NORMAL", "#39ff14", "✅"
    elif utilization < 110:
        return "HIGH", "#ffb300", "⚠️"
    else:
        return "SPIKE", "#ff3b5c", "🔥"

# ──────────────────────────────────────────────
# 3.  APP LOGIC
# ──────────────────────────────────────────────

# Sidebar
with st.sidebar:
    st.title("⚙️ SYSTEM CONTROL")
    st.markdown("---")
    
    simulation_speed = st.slider("Cycle Duration (s)", 0.1, 2.0, config.SIMULATION_SPEED_DEFAULT)
    resolution = st.selectbox("Resolution", ["1m", "5m", "15m"], index=0)
    model_type = st.selectbox("AI Model", ["LSTM (Pre-calculated)", "Prophet (Pre-calculated)", "LSTM (Live)", "ARIMA", "Prophet"], index=0)
    is_running = st.checkbox("▶  ACTIVATE SYSTEM", value=True)
    
    st.markdown("---")
    st.markdown("### 🛡️ SAFEGUARDS")
    min_replicas = st.number_input("Min Replicas", 1, 10, config.MIN_REPLICAS)
    max_replicas = st.number_input("Max Replicas", 10, 50, config.MAX_REPLICAS)

# Initialize State
if 'history' not in st.session_state:
    st.session_state.history = {'timestamp': [], 'requests': [], 'replicas': [], 'forecast': []}

# Load Data logic (Res/Simulator update)
# We check if resolution changed OR model type changed (if switching between different pre-calc sources)
# Actually, different pre-calc models imply different DATA SOURCES (df).
if 'resolution' not in st.session_state or st.session_state.resolution != resolution or \
   'model_type' not in st.session_state or st.session_state.model_type != model_type or \
   'simulator' not in st.session_state:
    
    st.session_state.resolution = resolution
    st.session_state.model_type = model_type
    
    df = None
    if model_type == "LSTM (Pre-calculated)":
        df = load_hybrid_data(resolution) # This loads LSTM/Hybrid logic
        if df is not None: st.toast(f"LSTM Data Loaded: {resolution}", icon="✅")
    elif model_type == "Prophet (Pre-calculated)":
        df = load_prophet_data(resolution)
        if df is not None: st.toast(f"Prophet Data Loaded: {resolution}", icon="✅")
        
    if df is None:
        # Fallback to Raw Data if not pre-calc, or if pre-calc failed
        df = load_raw_data(resolution)
        if df is not None:
            st.toast(f"Raw Data Loaded: {resolution}", icon="📂")
        else:
            st.warning("No data found, using synthetic.")
            dates = pd.date_range(start='2024-01-01', periods=1000, freq=resolution.replace('m', 'min'))
            reqs = 1000 + 500 * np.sin(np.arange(1000)/20) + np.random.normal(0, 50, 1000)
            df = pd.DataFrame({'timestamp': dates, 'requests': list(map(int, reqs))})
    
    st.session_state.simulator = TimeTraveler(df)
    st.session_state.history = {'timestamp': [], 'requests': [], 'replicas': [], 'forecast': []}

if 'autoscaler' not in st.session_state:
    st.session_state.autoscaler = Autoscaler(min_servers=min_replicas, max_servers=max_replicas)

# Load Models (Lazy) - Only for Live models
is_precalc = "Pre-calculated" in model_type
if not is_precalc and 'models' not in st.session_state:
    with st.spinner("Loading AI Models..."):
        loader = ModelLoader(config.MODEL_DIR)
        st.session_state.models = {
            'lstm': loader.load_keras_model("lstm_model.h5"),
            'arima': loader.load_generic_model("arima_model.pkl"),
            'prophet': loader.load_generic_model("prophet_model.pkl")
        }
        st.session_state.scaler = loader.load_scaler("scaler.pkl")

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
    
    # Forecast
    if "Pre-calculated" in model_type:
        fcast = data.get('forecast', curr_req)
    else:
        # Inference Logic
        if 'predictor' not in st.session_state or st.session_state.get('pred_type') != model_type:
            st.session_state.predictor = PredictorFactory.get_predictor(model_type, st.session_state.models, st.session_state.scaler)
            st.session_state.pred_type = model_type
        
        recent = hist['requests'][-30:] + [curr_req]
        if len(recent) < 30: recent = [curr_req]*30
        fcast = st.session_state.predictor.predict(recent)[0]

    # Scaling
    # Get last replicas or initial config
    current_replicas = hist['replicas'][-1] if hist['replicas'] else config.INITIAL_REPLICAS
    replicas, reason, cost, details = st.session_state.autoscaler.calculate_replicas(curr_req, fcast, current_replicas)
    anomaly = AnomalyDetector().detect(curr_req, fcast)
    
    # Update History
    hist['timestamp'].append(curr_time)
    hist['requests'].append(curr_req)
    hist['replicas'].append(replicas)
    hist['forecast'].append(fcast)
    
    if len(hist['timestamp']) > 60:
        for k in hist: hist[k] = hist[k][-60:]
        
    # UI Render
    # Calculate Workload Status
    wl_status, wl_color, wl_icon = get_workload_status(curr_req, replicas)
    
    with col1:
        st.metric("REAL-TIME TRAFFIC", f"{int(curr_req)}", f"{wl_icon} {wl_status}")
    with col2:
        st.metric("AI FORECAST", f"{int(fcast)}", delta_color="off")
    with col3:
        # Display Active Nodes with simplified reason
        st.metric("ACTIVE NODES", f"{replicas}", f"{details['action']}")
    with col4:
        st.metric("SYSTEM HEALTH", anomaly, delta="OK" if anomaly=="Normal" else "CRT", delta_color="inverse")
        
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
        fig.add_trace(go.Scatter(x=hist['timestamp'], y=hist['requests'], name='Actual', line=dict(color='#00e5ff', width=2), fill='tozeroy', fillcolor='rgba(0, 229, 255, 0.1)'))
        fig.add_trace(go.Scatter(x=hist['timestamp'], y=hist['forecast'], name='Forecast', line=dict(color='#ffb300', dash='dash', width=2)))
        fig.update_layout(
            title="TRAFFIC LOAD VS PREDICTION",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(11, 15, 26, 0.5)',
            height=350,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        
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
            st.plotly_chart(fig2, use_container_width=True)

if is_running:
    update()
    time.sleep(simulation_speed)
    st.rerun()
else:
    st.info("SYSTEM PAUSED")
