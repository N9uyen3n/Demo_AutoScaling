"""
Proactive Autoscaling Dashboard
Main Application Entry Point
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Import configurations
from config.settings import (
    SIMULATION_STEPS, INITIAL_REPLICAS, COST_PER_REPLICA, FIXED_REPLICAS
)

# Import utilities
from utils import (
    get_ai_prediction_multi_horizon,
    detect_anomaly,
    generate_simulated_load,
    scaling_logic,
    calculate_cpu_utilization,
    calculate_cost_savings
)

# Import components
from components import (
    render_sidebar,
    create_kpi_placeholders,
    render_kpi_cards,
    create_traffic_chart,
    create_forecast_indicator,
    render_scaling_events_tab,
    render_model_performance_tab,
    render_security_tab
)

# Import styles
from styles.aws_theme import get_aws_css


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PLANORA - Proactive Autoscaling AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- APPLY AWS THEME ---
st.markdown(get_aws_css(), unsafe_allow_html=True)


# --- INITIALIZE SESSION STATE ---
def initialize_session_state():
    """Initialize Streamlit session state"""
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


# --- MAIN APPLICATION ---
def main():
    """Main application logic"""
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get settings
    settings = render_sidebar()
    
    # Main header
    st.title("🚀 PLANORA: Proactive Autoscaling Dashboard")
    st.markdown("**AWS-Style Auto Scaling | AI-Powered Load Forecasting & Resource Optimization**")
    
    # ========== LAYER 1: KPI METRICS ==========
    kpi_placeholders = create_kpi_placeholders()
    st.divider()
    
    # ========== LAYER 2: MAIN VISUALS ==========
    st.markdown("### 🔮 Real-time Window")
    
    # Main chart placeholder (full width)
    chart_placeholder = st.empty()
    
    st.markdown("#### 🧠 AI Forecasts (req/min)")
    col1, col2, col3 = st.columns(3)
    with col1:
        forecast_1m_placeholder = st.empty()
    with col2:
        forecast_5m_placeholder = st.empty()
    with col3:
        forecast_15m_placeholder = st.empty()
    
    st.divider()
    
    # ========== LAYER 3: ANALYSIS TABS ==========
    st.markdown("### 📋 Deep Analysis")
    tab1, tab2, tab3 = st.tabs([
        "📜 Scaling Events",
        "📈 Model Performance",
        "🔒 Security & Anomaly"
    ])
    
    with tab1:
        scaling_log_placeholder = st.empty()
    
    with tab2:
        model_perf_placeholder = st.empty()
    
    with tab3:
        anomaly_placeholder = st.empty()
    
    # ========== SIMULATION LOOP ==========
    for i in range(SIMULATION_STEPS):
        now = datetime.now().strftime("%H:%M:%S")
        
        # 1. Generate simulated load
        actual_load = generate_simulated_load(i)
        
        # 2. Get AI predictions (multi-horizon)
        forecast_1m, forecast_5m, forecast_15m = get_ai_prediction_multi_horizon(actual_load, i)
        
        # 3. Detect anomalies
        is_anomaly, anomaly_msg = detect_anomaly(actual_load, forecast_1m)
        
        # 4. Make scaling decision
        replicas, status, reason = scaling_logic(
            forecast_5m,
            actual_load,
            st.session_state,
            settings['threshold_up'],
            settings['threshold_down'],
            settings['cooldown']
        )
        
        # 5. Calculate CPU utilization
        cpu_util = calculate_cpu_utilization(actual_load, replicas)
        
        # 6. Calculate costs
        st.session_state.total_cost_ai += (replicas * COST_PER_REPLICA)
        st.session_state.total_cost_fixed += (FIXED_REPLICAS * COST_PER_REPLICA)
        savings = calculate_cost_savings(
            st.session_state.total_cost_ai,
            st.session_state.total_cost_fixed
        )
        
        # 7. Save history
        new_data = {
            'Time': now,
            'Actual': actual_load,
            'Forecast_1m': forecast_1m,
            'Forecast_5m': forecast_5m,
            'Forecast_15m': forecast_15m,
            'Replicas': replicas,
            'CPU_Util': cpu_util,
            'Cost_AI': st.session_state.total_cost_ai,
            'Cost_Fixed': st.session_state.total_cost_fixed,
            'Status': status,
            'Reason': reason,
            'Anomaly': anomaly_msg
        }
        st.session_state.history = pd.concat(
            [st.session_state.history, pd.DataFrame([new_data])],
            ignore_index=True
        )
        
        # Save prediction history for metrics
        if len(st.session_state.history) > 1:
            st.session_state.predictions_history.append({
                'actual': actual_load,
                'predicted_1m': forecast_1m,
                'predicted_5m': forecast_5m
            })
        
        # ========== UPDATE UI ==========
        
        # Update KPI cards
        render_kpi_cards(
            kpi_placeholders,
            {
                'actual': actual_load,
                'forecast_1m': forecast_1m,
                'forecast_5m': forecast_5m,
                'forecast_15m': forecast_15m,
                'replicas': replicas,
                'status': status,
                'savings': savings
            },
            st.session_state.history
        )
        
        # Update main traffic chart
        fig_main = create_traffic_chart(
            st.session_state.history,
            settings['threshold_up'],
            settings['threshold_down']
        )
        chart_placeholder.plotly_chart(fig_main, use_container_width=True, key=f"main_chart_{i}")

        # Update forecast indicator charts
        fig_1m = create_forecast_indicator(st.session_state.history, 'Forecast_1m', 'Dự báo 1 phút', '#ffd700')
        forecast_1m_placeholder.plotly_chart(fig_1m, use_container_width=True)

        fig_5m = create_forecast_indicator(st.session_state.history, 'Forecast_5m', 'Dự báo 5 phút', '#ff9e00')
        forecast_5m_placeholder.plotly_chart(fig_5m, use_container_width=True)

        fig_15m = create_forecast_indicator(st.session_state.history, 'Forecast_15m', 'Dự báo 15 phút', '#ff4444')
        forecast_15m_placeholder.plotly_chart(fig_15m, use_container_width=True)
        
        # Update tabs
        with tab1:
            render_scaling_events_tab(st.session_state.history, scaling_log_placeholder)
        
        with tab2:
            render_model_performance_tab(
                st.session_state.predictions_history,
                model_perf_placeholder,
                i
            )
        
        with tab3:
            render_security_tab(
                st.session_state.history,
                is_anomaly,
                anomaly_msg,
                anomaly_placeholder
            )
        
        # Sleep based on simulation speed
        time.sleep(settings['sim_speed'])


if __name__ == "__main__":
    main()
