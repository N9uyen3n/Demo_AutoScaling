
import plotly.graph_objects as go
from config.settings import CHART_HEIGHT_MAIN, CHART_HEIGHT_GAUGE, CHART_HEIGHT_ERROR


def create_traffic_chart(history, threshold_up, threshold_down):
    """
    Create main traffic monitoring chart
    
    Args:
        history: DataFrame with historical data
        threshold_up: Scale-out threshold
        threshold_down: Scale-in threshold
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    # Đường Actual (Đậm, màu xanh cyan)
    fig.add_trace(go.Scatter(
        x=history['Time'], 
        y=history['Actual'], 
        name="Actual Load",
        line=dict(color='#00ebff', width=3),
        mode='lines+markers',
        marker=dict(size=4)
    ))
    
    # Thêm vùng ngưỡng
    fig.add_hline(
        y=threshold_up, 
        line_dash="dot", 
        line_color="red",
        annotation_text="Scale-out Threshold", 
        annotation_position="right"
    )
    fig.add_hline(
        y=threshold_down, 
        line_dash="dot", 
        line_color="green",
        annotation_text="Scale-in Threshold", 
        annotation_position="right"
    )
    
    fig.update_layout(
        title="📊 Real-time Traffic Monitoring",
        template="plotly_dark",
        height=CHART_HEIGHT_MAIN,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def create_error_distribution(predictions_history):
    """
    Create error distribution histogram
    
    Args:
        predictions_history: List of prediction history dicts
        
    Returns:
        plotly.graph_objects.Figure
    """
    import pandas as pd
    
    preds_df = pd.DataFrame(predictions_history)
    errors_1m = preds_df['actual'] - preds_df['predicted_1m']
    errors_5m = preds_df['actual'] - preds_df['predicted_5m']
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=errors_1m, 
        name="Error +1m", 
        opacity=0.7, 
        marker_color='#ffd700'
    ))
    fig.add_trace(go.Histogram(
        x=errors_5m, 
        name="Error +5m", 
        opacity=0.7, 
        marker_color='#ff9e00'
    ))
    
    fig.update_layout(
        title="Error Distribution",
        template="plotly_dark",
        height=CHART_HEIGHT_ERROR,
        barmode='overlay',
        xaxis_title="Prediction Error (Actual - Predicted)",
        yaxis_title="Frequency"
    )
    
    return fig

def create_forecast_indicator(history, forecast_col, title, color):
    """
    Create a single forecast indicator chart.
    
    Args:
        history (pd.DataFrame): The full history dataframe.
        forecast_col (str): The column name of the forecast (e.g., 'Forecast_1m').
        title (str): The title for the indicator.
        color (str): The color for the delta arrow.
        
    Returns:
        plotly.graph_objects.Figure
    """
    if len(history) < 2:
        latest_value = history.iloc[-1][forecast_col] if not history.empty else 0
        previous_value = latest_value
    else:
        latest_value = history.iloc[-1][forecast_col]
        previous_value = history.iloc[-2][forecast_col]

    fig = go.Figure(go.Indicator(
        mode="number+delta",
        value=latest_value,
        title={"text": title, "font": {"size": 16, "color": "white"}},
        number={'font': {'size': 36, "color": "white"}},
        delta={
            'reference': previous_value, 
            'increasing': {'color': color},
            'decreasing': {'color': color},
            'font': {'size': 14}
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    
    fig.update_layout(
        template="plotly_dark",
        height=120,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig