"""
Analysis Tabs Component for Outliers Demo Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
from components.charts import create_error_distribution


def render_scaling_events_tab(history, placeholder):
    """
    Render Scaling Events tab
    
    Args:
        history: DataFrame with historical data
        placeholder: Streamlit placeholder object
    """
    scaling_events = history[history['Status'] != "KEEP"].tail(10)
    
    if len(scaling_events) > 0:
        scaling_events_display = scaling_events[['Time', 'Status', 'Replicas', 'Reason']].copy()
        scaling_events_display['Status'] = scaling_events_display['Status'].apply(
            lambda x: f"🔼 {x}" if x == "SCALE_UP" else f"🔽 {x}"
        )
        placeholder.dataframe(
            scaling_events_display, 
            use_container_width=True,
            hide_index=True
        )
    else:
        placeholder.info("⏳ Chưa có sự kiện scaling nào...")


def render_model_performance_tab(predictions_history, placeholder, iteration):
    """
    Render Model Performance tab
    
    Args:
        predictions_history: List of prediction history dicts
        placeholder: Streamlit placeholder object
        iteration: Current iteration for chart key
    """
    if len(predictions_history) > 5:
        preds_df = pd.DataFrame(predictions_history)
        
        # Tính MAE, RMSE, MAPE cho forecast 1m và 5m
        mae_1m = np.mean(np.abs(preds_df['actual'] - preds_df['predicted_1m']))
        rmse_1m = np.sqrt(np.mean((preds_df['actual'] - preds_df['predicted_1m'])**2))
        mape_1m = np.mean(np.abs((preds_df['actual'] - preds_df['predicted_1m']) / preds_df['actual'])) * 100
        
        mae_5m = np.mean(np.abs(preds_df['actual'] - preds_df['predicted_5m']))
        rmse_5m = np.sqrt(np.mean((preds_df['actual'] - preds_df['predicted_5m'])**2))
        mape_5m = np.mean(np.abs((preds_df['actual'] - preds_df['predicted_5m']) / preds_df['actual'])) * 100
        
        col1, col2 = placeholder.columns(2)
        
        with col1:
            st.markdown("#### 📊 Forecast +1m Metrics")
            st.metric("MAE (Mean Absolute Error)", f"{mae_1m:.2f}")
            st.metric("RMSE (Root Mean Squared Error)", f"{rmse_1m:.2f}")
            st.metric("MAPE (Mean Absolute % Error)", f"{mape_1m:.2f}%")
        
        with col2:
            st.markdown("#### 📊 Forecast +5m Metrics")
            st.metric("MAE (Mean Absolute Error)", f"{mae_5m:.2f}")
            st.metric("RMSE (Root Mean Squared Error)", f"{rmse_5m:.2f}")
            st.metric("MAPE (Mean Absolute % Error)", f"{mape_5m:.2f}%")
        
        # Biểu đồ Error Distribution
        fig_error = create_error_distribution(predictions_history)
        placeholder.plotly_chart(fig_error, use_container_width=True, key=f"error_chart_{iteration}")
    else:
        placeholder.info("⏳ Đang thu thập dữ liệu để tính metrics...")


def render_security_tab(history, is_anomaly, anomaly_msg, placeholder):
    """
    Render Security & Anomaly tab
    
    Args:
        history: DataFrame with historical data
        is_anomaly: Boolean indicating current anomaly status
        anomaly_msg: Anomaly message string
        placeholder: Streamlit placeholder object
    """
    anomaly_events = history[history['Anomaly'] != "✅ Normal"].tail(10)
    
    col_a1, col_a2 = placeholder.columns([1, 2])
    
    with col_a1:
        st.markdown("#### 🚨 Current Status")
        if is_anomaly:
            st.error(f"**{anomaly_msg}**")
            st.metric("Anomaly Score", "HIGH", delta="⚠️")
        else:
            st.success("**✅ System Normal**")
            st.metric("Anomaly Score", "LOW", delta="✅")
    
    with col_a2:
        st.markdown("#### 📜 Recent Anomalies")
        if len(anomaly_events) > 0:
            st.dataframe(
                anomaly_events[['Time', 'Actual', 'Forecast_1m', 'Anomaly']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("✅ Không phát hiện bất thường nào!")
