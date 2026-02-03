import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict
from datetime import datetime

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

# ══════════════════════════════════════════════
# 0. PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="⚡ PLANORA - Autoscaling Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════
# 1. ENHANCED CYBERPUNK THEME (More Polished)
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;500;700&display=swap');

:root {
    --bg-deep: #0a0e1a;
    --bg-card: #0f1419;
    --bg-card2: #141b24;
    --cyan: #00f0ff;
    --green: #00ff88;
    --amber: #ffd60a;
    --red: #ff2e63;
    --purple: #a855f7;
    --text-hi: #f0f4f8;
    --text-lo: #7c8d9e;
    --border: #1e293b;
}

/* ===== SMOOTH TRANSITIONS ===== */
* {
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ===== APP BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, var(--bg-deep) 0%, #0d1117 100%);
    font-family: 'Rajdhani', sans-serif;
    color: var(--text-hi);
}

/* ===== HEADER STYLING ===== */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    background: linear-gradient(135deg, var(--cyan), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--cyan) !important;
    font-weight: 700;
}

/* ===== METRIC CARDS (ENHANCED) ===== */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card2) 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    box-shadow: 0 4px 20px rgba(0, 240, 255, 0.08);
    position: relative;
    overflow: hidden;
}

div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--cyan), var(--purple));
    opacity: 0;
    transition: opacity 0.3s;
}

div[data-testid="stMetric"]:hover::before {
    opacity: 1;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0, 240, 255, 0.15);
    border-color: var(--cyan);
}

div[data-testid="stMetric"] label {
    font-family: 'Orbitron', sans-serif;
    color: var(--text-lo);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}

div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2rem;
    color: var(--text-hi);
    font-weight: 700;
    text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
}

/* ===== SERVER GRID (IMPROVED) ===== */
.server-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
    gap: 12px;
    margin-top: 1rem;
}

.server-card {
    background: var(--bg-card2);
    border: 2px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.server-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 50% 0%, var(--cyan) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 0.3s;
}

.server-card.active {
    border-color: var(--green);
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    animation: pulse 2s infinite;
}

.server-card.active::before {
    opacity: 0.1;
}

.server-card.inactive {
    opacity: 0.4;
    border-color: #333;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(0, 255, 136, 0.3); }
    50% { box-shadow: 0 0 30px rgba(0, 255, 136, 0.5); }
}

.cpu-bar {
    height: 5px;
    width: 100%;
    background: #222;
    margin-top: 8px;
    border-radius: 3px;
    overflow: hidden;
}

.cpu-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--cyan), var(--green));
    box-shadow: 0 0 10px currentColor;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-deep) 100%);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label {
    color: var(--cyan) !important;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
}

/* ===== INFO BOXES ===== */
.info-box {
    background: var(--bg-card);
    border-left: 4px solid var(--cyan);
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.success-box {
    border-left-color: var(--green);
    background: linear-gradient(90deg, rgba(0, 255, 136, 0.05), transparent);
}

.warning-box {
    border-left-color: var(--amber);
    background: linear-gradient(90deg, rgba(255, 214, 10, 0.05), transparent);
}

.error-box {
    border-left-color: var(--red);
    background: linear-gradient(90deg, rgba(255, 46, 99, 0.05), transparent);
}

/* ===== LOADING ANIMATION ===== */
.loading-spinner {
    border: 3px solid var(--border);
    border-top: 3px solid var(--cyan);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* ===== PLOTLY CHARTS ===== */
.js-plotly-plot {
    border-radius: 12px;
    overflow: hidden;
}

/* ===== DECISION PANEL ===== */
.decision-panel {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    margin: 1rem 0;
}

.decision-header {
    font-family: 'Orbitron', sans-serif;
    color: var(--cyan);
    font-size: 1.1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .server-grid {
        grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
        gap: 8px;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 2. CACHING FUNCTIONS (PERFORMANCE BOOST)
# ══════════════════════════════════════════════
@st.cache_data(ttl=3600)
def load_hybrid_data(resolution: str) -> pd.DataFrame:
    """Loads pre-calculated predictions with caching."""
    res_map = {'1m': '1min_request_count', '5m': '5min_request_count', '15m': '15min_request_count'}
    folder_name = res_map.get(resolution)
    if not folder_name: 
        return None
    
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

@st.cache_data(ttl=3600)
def load_prophet_data(resolution: str) -> pd.DataFrame:
    """Loads pre-calculated Prophet predictions with caching."""
    res_map = {'1m': '1min_request_count', '5m': '5min_request_count', '15m': '15min_request_count'}
    folder_name = res_map.get(resolution)
    if not folder_name: 
        return None
    
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

@st.cache_data(ttl=3600)
def load_raw_data(resolution: str) -> pd.DataFrame:
    """Loads raw test data with caching."""
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

# ══════════════════════════════════════════════
# 3. OPTIMIZED UI COMPONENTS
# ══════════════════════════════════════════════
def render_server_grid(active_replicas: int, max_replicas: int = 12):
    """Generates HTML for visual server grid (optimized)."""
    cards_html = []
    
    for i in range(max_replicas):
        is_active = i < active_replicas
        cls = "active" if is_active else "inactive"
        icon = "🟢" if is_active else "⚪"
        
        # Simulate CPU load
        cpu = int(np.random.normal(65, 12)) if is_active else 0
        cpu = max(0, min(100, cpu))
        
        # Color gradient based on CPU
        if cpu < 50:
            color = "var(--green)"
        elif cpu < 80:
            color = "var(--amber)"
        else:
            color = "var(--red)"
        
        card_html = f"""
<div class="server-card {cls}">
    <div style="font-size:1.4rem; margin-bottom:4px;">{icon}</div>
    <div style="font-family:'Share Tech Mono'; font-size:0.75rem; color:var(--text-hi); font-weight:600;">NODE-{i+1:02d}</div>
    <div class="cpu-bar">
        <div class="cpu-fill" style="width:{cpu}%; background:{color};"></div>
    </div>
    <div style="font-size:0.65rem; color:var(--text-lo); margin-top:4px; font-family:'Share Tech Mono';">{cpu}% CPU</div>
</div>"""
        cards_html.append(card_html)
    
    return f'<div class="server-grid">{"".join(cards_html)}</div>'

def get_workload_status(current_load, active_replicas):
    """Classifies workload with better visual feedback."""
    capacity = active_replicas * config.DEFAULT_SCALE_OUT_THRESHOLD
    if capacity == 0: 
        return "CRITICAL", "var(--red)", "🔥"
    
    utilization = (current_load / capacity) * 100
    
    if utilization < 40:
        return "LOW", "var(--cyan)", "💤"
    elif utilization < 70:
        return "OPTIMAL", "var(--green)", "✅"
    elif utilization < 90:
        return "HIGH", "var(--amber)", "⚠️"
    else:
        return "CRITICAL", "var(--red)", "🔥"

def create_enhanced_chart(history):
    """Create optimized main chart with better styling."""
    fig = go.Figure()
    
    # Actual Load with gradient fill
    fig.add_trace(go.Scatter(
        x=history['timestamp'], 
        y=history['requests'], 
        name='Actual Traffic',
        line=dict(color='#00f0ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 240, 255, 0.1)',
        mode='lines',
        hovertemplate='<b>Time:</b> %{x}<br><b>Requests:</b> %{y}<extra></extra>'
    ))
    
    # Forecast with dashed line
    fig.add_trace(go.Scatter(
        x=history['timestamp'], 
        y=history['forecast'], 
        name='AI Forecast',
        line=dict(color='#a855f7', dash='dash', width=2.5),
        hovertemplate='<b>Time:</b> %{x}<br><b>Forecast:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': "📊 TRAFFIC MONITORING & PREDICTION",
            'font': {'family': 'Orbitron', 'size': 18, 'color': '#00f0ff'}
        },
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15, 20, 25, 0.6)',
        height=380,
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family='Rajdhani', size=12)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            title='Time',
            title_font=dict(family='Orbitron', size=12)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            title='Requests/min',
            title_font=dict(family='Orbitron', size=12)
        )
    )
    
    return fig

# ══════════════════════════════════════════════
# 4. MAIN APP LOGIC
# ══════════════════════════════════════════════

# Sidebar with enhanced styling
with st.sidebar:
    st.markdown("# ⚙️ CONTROL CENTER")
    st.markdown("---")
    
    st.markdown("### ⏱️ Simulation Settings")
    simulation_speed = st.slider(
        "Update Interval (seconds)", 
        0.1, 2.0, 
        config.SIMULATION_SPEED_DEFAULT,
        help="How fast the simulation runs"
    )
    
    resolution = st.selectbox(
        "Data Resolution", 
        ["1m", "5m", "15m"], 
        index=0,
        help="Time granularity for analysis"
    )
    
    model_type = st.selectbox(
        "Forecasting Model", 
        ["LSTM (Pre-calculated)", "Prophet (Pre-calculated)", "LSTM (Live)", "ARIMA", "Prophet"],
        index=0,
        help="AI model for traffic prediction"
    )
    
    is_running = st.checkbox("▶️  START SIMULATION", value=True)
    
    st.markdown("---")
    st.markdown("### 🛡️ Scaling Configuration")
    
    min_replicas = st.number_input("Min Replicas", 1, 10, config.MIN_REPLICAS)
    max_replicas = st.number_input("Max Replicas", 10, 50, config.MAX_REPLICAS)
    
    st.markdown("---")
    
    # System Info
    if 'history' in st.session_state and st.session_state.history['timestamp']:
        progress = len(st.session_state.history['timestamp']) / 60 * 100
        st.progress(min(progress / 100, 1.0))
        st.caption(f"📊 Data Points: {len(st.session_state.history['timestamp'])}/60")

# Initialize State
if 'history' not in st.session_state:
    st.session_state.history = {
        'timestamp': [], 
        'requests': [], 
        'replicas': [], 
        'forecast': []
    }

# Data Loading (with state management)
if ('resolution' not in st.session_state or 
    st.session_state.resolution != resolution or 
    'model_type' not in st.session_state or 
    st.session_state.model_type != model_type or 
    'simulator' not in st.session_state):
    
    with st.spinner('🔄 Loading data...'):
        st.session_state.resolution = resolution
        st.session_state.model_type = model_type
        
        df = None
        if model_type == "LSTM (Pre-calculated)":
            df = load_hybrid_data(resolution)
            if df is not None: 
                st.toast(f"✅ LSTM Data Loaded: {resolution}", icon="✅")
        elif model_type == "Prophet (Pre-calculated)":
            df = load_prophet_data(resolution)
            if df is not None: 
                st.toast(f"✅ Prophet Data Loaded: {resolution}", icon="✅")
            
        if df is None:
            df = load_raw_data(resolution)
            if df is not None:
                st.toast(f"📂 Raw Data Loaded: {resolution}", icon="📂")
            else:
                st.warning("⚠️ Using synthetic data for demo")
                dates = pd.date_range(start='2024-01-01', periods=1000, freq=resolution.replace('m', 'min'))
                reqs = 1000 + 500 * np.sin(np.arange(1000)/20) + np.random.normal(0, 50, 1000)
                df = pd.DataFrame({
                    'timestamp': dates, 
                    'requests': list(map(int, reqs))
                })
        
        st.session_state.simulator = TimeTraveler(df)
        st.session_state.history = {
            'timestamp': [], 
            'requests': [], 
            'replicas': [], 
            'forecast': []
        }

if 'autoscaler' not in st.session_state:
    st.session_state.autoscaler = Autoscaler(
        min_servers=min_replicas, 
        max_servers=max_replicas
    )

# Load Models (for live prediction)
is_precalc = "Pre-calculated" in model_type
if not is_precalc and 'models' not in st.session_state:
    with st.spinner("🤖 Loading AI Models..."):
        loader = ModelLoader(config.MODEL_DIR)
        st.session_state.models = {
            'lstm': loader.load_keras_model("lstm_model.h5"),
            'arima': loader.load_generic_model("arima_model.pkl"),
            'prophet': loader.load_generic_model("prophet_model.pkl")
        }
        st.session_state.scaler = loader.load_scaler("scaler.pkl")

# ══════════════════════════════════════════════
# 5. MAIN DASHBOARD LAYOUT
# ══════════════════════════════════════════════

# Header
st.markdown("# ⚡ PLANORA AUTOSCALING INTELLIGENCE")
st.markdown("**Real-time Traffic Prediction & Intelligent Resource Management**")
st.markdown("---")

# Metrics Row (Placeholder)
col1, col2, col3, col4 = st.columns(4)
placeholder_charts = st.empty()

# ══════════════════════════════════════════════
# 6. UPDATE FUNCTION (OPTIMIZED)
# ══════════════════════════════════════════════
def update():
    sim = st.session_state.simulator
    hist = st.session_state.history
    
    data = sim.next_tick()
    if not data:
        st.info("✅ Simulation Complete")
        st.balloons()
        st.stop()
        
    curr_req = data.get('requests', 0)
    curr_time = data.get('timestamp', pd.Timestamp.now())
    
    # Forecast Logic
    if "Pre-calculated" in model_type:
        fcast = data.get('forecast', curr_req)
    else:
        if 'predictor' not in st.session_state or st.session_state.get('pred_type') != model_type:
            st.session_state.predictor = PredictorFactory.get_predictor(
                model_type, 
                st.session_state.models, 
                st.session_state.scaler
            )
            st.session_state.pred_type = model_type
        
        recent = hist['requests'][-30:] + [curr_req]
        if len(recent) < 30: 
            recent = [curr_req] * 30
        fcast = st.session_state.predictor.predict(recent)[0]

    # Scaling Decision
    current_replicas = hist['replicas'][-1] if hist['replicas'] else config.INITIAL_REPLICAS
    replicas, reason, cost, details = st.session_state.autoscaler.calculate_replicas(
        curr_req, fcast, current_replicas
    )
    
    anomaly = AnomalyDetector().detect(curr_req, fcast)
    
    # Update History
    hist['timestamp'].append(curr_time)
    hist['requests'].append(curr_req)
    hist['replicas'].append(replicas)
    hist['forecast'].append(fcast)
    
    # Keep last 60 points
    if len(hist['timestamp']) > 60:
        for k in hist: 
            hist[k] = hist[k][-60:]
    
    # ═══════════════════════════════════
    # UI RENDERING
    # ═══════════════════════════════════
    wl_status, wl_color, wl_icon = get_workload_status(curr_req, replicas)
    
    # Metrics
    with col1:
        delta_req = curr_req - hist['requests'][-2] if len(hist['requests']) > 1 else 0
        st.metric(
            "🌊 CURRENT TRAFFIC", 
            f"{int(curr_req):,}",
            delta=f"{delta_req:+.0f}",
            help="Real-time request load"
        )
    
    with col2:
        delta_fcast = fcast - curr_req
        st.metric(
            "🔮 AI FORECAST", 
            f"{int(fcast):,}",
            delta=f"{delta_fcast:+.0f}",
            delta_color="off",
            help="Next interval prediction"
        )
    
    with col3:
        delta_replicas = replicas - current_replicas
        st.metric(
            "🖥️ ACTIVE NODES", 
            f"{replicas}/{max_replicas}",
            delta=f"{delta_replicas:+d}" if delta_replicas != 0 else None,
            help=f"Action: {details['action']}"
        )
    
    with col4:
        anomaly_delta = "ALERT" if anomaly != "NORMAL" else "OK"
        st.metric(
            f"{wl_icon} WORKLOAD", 
            wl_status,
            delta=anomaly_delta,
            delta_color="inverse" if anomaly != "NORMAL" else "off",
            help=f"Capacity: {int((curr_req/replicas/config.DEFAULT_SCALE_OUT_THRESHOLD)*100)}%"
        )
    
    # ═══════════════════════════════════
    # DECISION INTELLIGENCE PANEL
    # ═══════════════════════════════════
    st.markdown("---")
    st.markdown("### 🧠 3-LAYER DEFENSE SYSTEM")
    
    c_d1, c_d2, c_d3 = st.columns(3)
    
    with c_d1:
        st.markdown(f"""
        <div class="info-box success-box">
            <div style="font-family:Orbitron; font-size:0.9rem; color:var(--green); margin-bottom:0.5rem;">
                <b>⚡ L1: PREDICTIVE (Attack)</b>
            </div>
            <div style="font-family:Share Tech Mono; font-size:1.3rem; color:var(--text-hi);">
                {details['predictive_target']} Nodes
            </div>
            <div style="font-size:0.75rem; color:var(--text-lo); margin-top:0.3rem;">
                Pre-warming based on AI forecast
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c_d2:
        is_override = details['reactive_target'] > details['predictive_target']
        box_class = "error-box" if is_override else "success-box"
        status_text = "⚠️ OVERRIDE ACTIVE" if is_override else "✅ SAFE"
        
        st.markdown(f"""
        <div class="info-box {box_class}">
            <div style="font-family:Orbitron; font-size:0.9rem; color:var(--amber); margin-bottom:0.5rem;">
                <b>🛡️ L2: REACTIVE (Defense)</b>
            </div>
            <div style="font-family:Share Tech Mono; font-size:1.3rem; color:var(--text-hi);">
                {details['reactive_target']} Nodes
            </div>
            <div style="font-size:0.75rem; color:var(--text-lo); margin-top:0.3rem;">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c_d3:
        cooldown_status = "❄️ ACTIVE" if details['cooldown'] > 0 else "✅ READY"
        box_class = "warning-box" if details['cooldown'] > 0 else "info-box"
        
        st.markdown(f"""
        <div class="info-box {box_class}">
            <div style="font-family:Orbitron; font-size:0.9rem; color:var(--cyan); margin-bottom:0.5rem;">
                <b>⏱️ L3: STABILITY RULE</b>
            </div>
            <div style="font-family:Share Tech Mono; font-size:1.3rem; color:var(--text-hi);">
                {cooldown_status}
            </div>
            <div style="font-size:0.75rem; color:var(--text-lo); margin-top:0.3rem;">
                Cooldown: {details['cooldown']} cycles
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ═══════════════════════════════════
    # CHARTS & VISUALIZATIONS
    # ═══════════════════════════════════
    with placeholder_charts.container():
        # Main Chart
        fig = create_enhanced_chart(pd.DataFrame(hist))
        st.plotly_chart(fig, use_container_width=True, key=f"main_chart_{len(hist['timestamp'])}")
        
        # Server Grid & Residuals
        c_grid, c_res = st.columns([1.2, 1])
        
        with c_grid:
            st.markdown("### 🖥️ SERVER FLEET STATUS")
            st.markdown(render_server_grid(replicas, max_replicas=12), unsafe_allow_html=True)
        
        with c_res:
            if len(hist['requests']) > 0:
                residuals = np.array(hist['requests']) - np.array(hist['forecast'])
                
                # Color based on error magnitude
                colors = ['#ff2e63' if abs(r) > 50 else '#ffd60a' if abs(r) > 20 else '#00ff88' 
                         for r in residuals]
                
                fig2 = go.Figure(go.Bar(
                    x=hist['timestamp'],
                    y=residuals,
                    marker_color=colors,
                    name='Forecast Error',
                    hovertemplate='<b>Error:</b> %{y:.0f}<extra></extra>'
                ))
                
                fig2.update_layout(
                    title={
                        'text': "📉 FORECAST ERROR",
                        'font': {'family': 'Orbitron', 'size': 14, 'color': '#00f0ff'}
                    },
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(15, 20, 25, 0.6)',
                    height=280,
                    margin=dict(l=20, r=20, t=40, b=20),
                    showlegend=False,
                    yaxis=dict(title='Error', gridcolor='rgba(255,255,255,0.05)'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
                )
                
                st.plotly_chart(fig2, use_container_width=True, key=f"error_chart_{len(hist['timestamp'])}")

# ══════════════════════════════════════════════
# 7. RUN SIMULATION
# ══════════════════════════════════════════════
if is_running:
    update()
    time.sleep(simulation_speed)
    st.rerun()
else:
    st.info("⏸️ SIMULATION PAUSED - Click START to resume")
