
import streamlit as st


def render_kpi_cards(placeholders, data, history):
    """
    Render 6 KPI metric cards
    
    Args:
        placeholders: Dict of placeholder objects
        data: Current data dict
        history: DataFrame with historical data
    """
    # Calculate delta for current throughput
    delta_throughput = 0
    if len(history) > 1:
        delta_throughput = data['actual'] - history['Actual'].iloc[-2]
    
    placeholders['kpi1'].metric(
        "🌊 Current Throughput", 
        f"{data['actual']} req/m",
        delta=f"{delta_throughput:+d}"
    )
    
    placeholders['kpi2'].metric(
        "🔮 AI Forecast (1m)", 
        f"{data['forecast_1m']} req/m",
        delta=f"{data['forecast_1m'] - data['actual']:+d}"
    )
    
    placeholders['kpi3'].metric(
        "🔮 AI Forecast (5m)", 
        f"{data['forecast_5m']} req/m",
        delta=f"{data['forecast_5m'] - data['actual']:+d}"
    )
    
    placeholders['kpi4'].metric(
        "🔮 AI Forecast (15m)", 
        f"{data['forecast_15m']} req/m",
        delta=f"{data['forecast_15m'] - data['actual']:+d}"
    )
    
    placeholders['kpi5'].metric(
        "🖥️ Active Nodes", 
        f"{data['replicas']}/20",
        delta=data['status'] if data['status'] != "KEEP" else None
    )
    
    placeholders['kpi6'].metric(
        "💰 Cost Efficiency", 
        f"{data['savings']:.1f}%",
        delta="vs Fixed",
        delta_color="normal"
    )


def create_kpi_placeholders():
    """
    Create placeholder objects for KPI cards
    
    Returns:
        dict: Dictionary of placeholder objects
    """
    st.markdown("### 📊 Survival Metrics")
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    
    return {
        'kpi1': kpi1.empty(),
        'kpi2': kpi2.empty(),
        'kpi3': kpi3.empty(),
        'kpi4': kpi4.empty(),
        'kpi5': kpi5.empty(),
        'kpi6': kpi6.empty()
    }
