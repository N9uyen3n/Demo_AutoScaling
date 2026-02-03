"""
Quick Data Generator for PLANORA Demo
Tạo synthetic data khi không có data thật
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_traffic_pattern(
    start_date='2024-08-23',
    periods=1000,
    freq='1min',
    pattern='realistic'
):
    """
    Generate synthetic traffic data với patterns khác nhau
    
    Args:
        start_date: Start timestamp
        periods: Số data points
        freq: '1min', '5min', '15min'
        pattern: 'realistic', 'spike', 'smooth'
    
    Returns:
        DataFrame with timestamp, requests
    """
    timestamps = pd.date_range(start=start_date, periods=periods, freq=freq)
    
    if pattern == 'realistic':
        # Hourly pattern (cao vào giờ làm việc)
        hour_component = np.array([
            50 + 80 * np.sin((i % 1440) / 1440 * 2 * np.pi - np.pi/2)
            for i in range(periods)
        ])
        
        # Weekly pattern (thấp vào cuối tuần)
        day_component = np.array([
            20 * np.sin((i % 10080) / 10080 * 2 * np.pi)
            for i in range(periods)
        ])
        
        # Random spikes (5% probability)
        spikes = np.random.choice([0, 200], size=periods, p=[0.95, 0.05])
        
        # Noise
        noise = np.random.normal(0, 15, periods)
        
        requests = 100 + hour_component + day_component + spikes + noise
        requests = np.maximum(requests, 20)  # Min 20 req/min
        
    elif pattern == 'spike':
        # Base load với random spikes
        base = 80 + np.random.normal(0, 10, periods)
        spikes = np.zeros(periods)
        
        # Inject 10 spikes
        spike_positions = np.random.choice(periods, 10, replace=False)
        for pos in spike_positions:
            spike_duration = np.random.randint(5, 20)
            spike_magnitude = np.random.randint(150, 300)
            spikes[pos:min(pos+spike_duration, periods)] = spike_magnitude
        
        requests = base + spikes
        
    elif pattern == 'smooth':
        # Smooth sine wave
        requests = 100 + 50 * np.sin(np.arange(periods) / 50) + np.random.normal(0, 5, periods)
        
    else:
        # Random walk
        requests = np.cumsum(np.random.normal(0, 10, periods)) + 100
    
    requests = requests.astype(int)
    
    df = pd.DataFrame({
        'timestamp': timestamps,
        'requests': requests
    })
    
    return df

def generate_with_forecast(df, model='lstm', noise_level=0.15):
    """
    Add forecast column to existing DataFrame
    
    Args:
        df: DataFrame with timestamp, requests
        model: 'lstm', 'prophet', 'arima'
        noise_level: Forecast error magnitude (0-1)
    
    Returns:
        DataFrame with forecast column
    """
    df = df.copy()
    
    if model == 'lstm':
        # LSTM tends to smooth out spikes
        forecast = df['requests'].rolling(window=5, min_periods=1).mean()
        forecast += np.random.normal(0, df['requests'].std() * noise_level, len(df))
        
    elif model == 'prophet':
        # Prophet catches trends well
        trend = df['requests'].rolling(window=10, min_periods=1).mean()
        forecast = trend + np.random.normal(0, df['requests'].std() * noise_level, len(df))
        
    elif model == 'arima':
        # ARIMA more reactive
        forecast = df['requests'].shift(1) + np.random.normal(0, df['requests'].std() * noise_level, len(df))
    
    df['forecast'] = forecast.fillna(df['requests'])
    df['forecast'] = df['forecast'].astype(int)
    
    return df

def save_demo_data(output_dir='../data'):
    """
    Generate and save demo data for all resolutions
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1min resolution (1000 points = ~16 hours)
    print("Generating 1min data...")
    df_1min = generate_traffic_pattern(periods=1000, freq='1min', pattern='realistic')
    df_1min_pred = generate_with_forecast(df_1min, model='lstm')
    
    df_1min.to_csv(f'{output_dir}/test_1min.csv', index=False)
    df_1min_pred.to_csv(f'{output_dir}/test_1min_with_forecast.csv', index=False)
    print(f"✅ Saved: test_1min.csv ({len(df_1min)} rows)")
    
    # 5min resolution (500 points = ~41 hours)
    print("Generating 5min data...")
    df_5min = generate_traffic_pattern(periods=500, freq='5min', pattern='realistic')
    df_5min_pred = generate_with_forecast(df_5min, model='lstm')
    
    df_5min.to_csv(f'{output_dir}/test_5min.csv', index=False)
    df_5min_pred.to_csv(f'{output_dir}/test_5min_with_forecast.csv', index=False)
    print(f"✅ Saved: test_5min.csv ({len(df_5min)} rows)")
    
    # 15min resolution (300 points = ~75 hours)
    print("Generating 15min data...")
    df_15min = generate_traffic_pattern(periods=300, freq='15min', pattern='realistic')
    df_15min_pred = generate_with_forecast(df_15min, model='lstm')
    
    df_15min.to_csv(f'{output_dir}/test_15min.csv', index=False)
    df_15min_pred.to_csv(f'{output_dir}/test_15min_with_forecast.csv', index=False)
    print(f"✅ Saved: test_15min.csv ({len(df_15min)} rows)")
    
    print("\n🎉 Demo data generated successfully!")
    print(f"Location: {output_dir}/")

def preview_data(filepath):
    """Quick preview of generated data"""
    df = pd.read_csv(filepath)
    print(f"\n📊 Preview: {filepath}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nStats:")
    print(df.describe())

if __name__ == "__main__":
    import sys
    
    # Allow custom output directory
    output_dir = sys.argv[1] if len(sys.argv) > 1 else '../data'
    
    print("=" * 50)
    print("PLANORA Demo Data Generator")
    print("=" * 50)
    
    save_demo_data(output_dir)
    
    # Preview generated files
    for res in ['1min', '5min', '15min']:
        filepath = f'{output_dir}/test_{res}.csv'
        if os.path.exists(filepath):
            preview_data(filepath)
