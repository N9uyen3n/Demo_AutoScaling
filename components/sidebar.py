
import streamlit as st
from config.settings import (
    DEFAULT_SIMULATION_SPEED,
    DEFAULT_SCALE_OUT_THRESHOLD,
    DEFAULT_SCALE_IN_THRESHOLD,
    DEFAULT_COOLDOWN_PERIOD
)


def render_sidebar():
    """
    Render sidebar with controls
    
    Returns:
        dict: User settings from sidebar
    """
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/amazon-web-services.png", width=80)
        st.title("Outliers Demo")
        st.caption("AWS-Style Autoscaling Dashboard")
        
        st.markdown("### 🎮 Simulation Settings")
        sim_speed = st.slider(
            "Simulation Speed (s)", 
            0.1, 2.0, 
            DEFAULT_SIMULATION_SPEED, 
            help="Tốc độ cập nhật dashboard"
        )
        
        st.markdown("### 📊 Autoscaling Thresholds")
        threshold_up = st.slider(
            "Scale-out Threshold (Req/min)", 
            100, 200, 
            DEFAULT_SCALE_OUT_THRESHOLD, 
            help="Ngưỡng tăng server"
        )
        threshold_down = st.slider(
            "Scale-in Threshold (Req/min)", 
            20, 80, 
            DEFAULT_SCALE_IN_THRESHOLD, 
            help="Ngưỡng giảm server"
        )
        cooldown = st.number_input(
            "Cooldown Period (min)", 
            1, 10, 
            DEFAULT_COOLDOWN_PERIOD, 
            help="Thời gian chờ giữa các lần scale"
        )
        
        st.markdown("### 🤖 AI Model Settings")
        model_type = st.selectbox(
            "Forecast Model", 
            ["XGBoost (Simulated)", "ARIMA (Simulated)", "LSTM (Future)"]
        )
        
        st.divider()
        st.info("💡 **Next Step**: Tích hợp model XGBoost/ARIMA thật vào `utils/ai_models.py`")
    
    return {
        'sim_speed': sim_speed,
        'threshold_up': threshold_up,
        'threshold_down': threshold_down,
        'cooldown': cooldown,
        'model_type': model_type
    }
