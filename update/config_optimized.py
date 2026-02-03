"""
Enhanced Configuration for PLANORA Autoscaling System
Optimized for demo performance and visual appeal
"""
import os

# ═══════════════════════════════════════════════
# VISUAL THEME (Enhanced Cyberpunk)
# ═══════════════════════════════════════════════
THEME = {
    'primary': '#00f0ff',      # Cyan
    'secondary': '#a855f7',    # Purple
    'success': '#00ff88',      # Green
    'warning': '#ffd60a',      # Amber
    'danger': '#ff2e63',       # Red
    'bg_deep': '#0a0e1a',
    'bg_card': '#0f1419',
    'text_primary': '#f0f4f8',
    'text_secondary': '#7c8d9e'
}

# ═══════════════════════════════════════════════
# SIMULATION SETTINGS (Optimized for Demo)
# ═══════════════════════════════════════════════
SIMULATION_SPEED_DEFAULT = 0.5  # Seconds per tick (balanced for demo)
SIMULATION_STEPS = 200
HISTORY_WINDOW = 60  # Keep last N points for performance

# ═══════════════════════════════════════════════
# AUTOSCALING PARAMETERS (3-Layer Defense)
# ═══════════════════════════════════════════════
# Layer 1: Predictive Scaling
DEFAULT_SCALE_OUT_THRESHOLD = 150  # req/min per replica
DEFAULT_SCALE_IN_THRESHOLD = 50    # req/min per replica

# Layer 2: Reactive Scaling (Safety Net)
REACTIVE_MULTIPLIER = 1.0  # Direct capacity calculation

# Layer 3: Stability Rules
DEFAULT_COOLDOWN_PERIOD = 3  # Ticks to wait before scale-in
MIN_REPLICAS = 1
MAX_REPLICAS = 20
INITIAL_REPLICAS = 5
FIXED_REPLICAS = 10  # For cost comparison

# ═══════════════════════════════════════════════
# COST MODEL (For Demo Metrics)
# ═══════════════════════════════════════════════
COST_PER_REPLICA_PER_TICK = 0.1  # Currency units
COST_CURRENCY = "USD"

# ═══════════════════════════════════════════════
# ANOMALY DETECTION THRESHOLDS
# ═══════════════════════════════════════════════
ANOMALY_SPIKE_MULTIPLIER = 1.5  # 50% above forecast
ANOMALY_DROP_MULTIPLIER = 0.5   # 50% below forecast
ANOMALY_DROP_THRESHOLD = 30     # Absolute minimum for drop detection

# ═══════════════════════════════════════════════
# PERFORMANCE OPTIMIZATION
# ═══════════════════════════════════════════════
ENABLE_CACHING = True
CACHE_TTL = 3600  # Seconds
MAX_CHART_POINTS = 100  # Limit chart data points for smooth rendering

# ═══════════════════════════════════════════════
# FILE PATHS (Auto-detection)
# ═══════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "processed")
MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), "data", "models")

# Fallback paths for different project structures
POSSIBLE_DATA_DIRS = [
    DATA_DIR,
    os.path.join(BASE_DIR, "data"),
    os.path.join(BASE_DIR, "..", "data"),
    os.path.join(BASE_DIR, "..", "..", "data"),
]

POSSIBLE_MODEL_DIRS = [
    MODEL_DIR,
    os.path.join(BASE_DIR, "models"),
    os.path.join(BASE_DIR, "..", "models"),
    os.path.join(BASE_DIR, "..", "..", "models"),
]

# ═══════════════════════════════════════════════
# MODEL CONFIGURATION
# ═══════════════════════════════════════════════
MODEL_TYPES = {
    'lstm': {
        'display_name': 'LSTM (Deep Learning)',
        'description': 'Long Short-Term Memory neural network',
        'look_back': 30,
        'requires_scaling': True
    },
    'arima': {
        'display_name': 'ARIMA (Statistical)',
        'description': 'AutoRegressive Integrated Moving Average',
        'order': (2, 1, 2),
        'requires_scaling': False
    },
    'prophet': {
        'display_name': 'Prophet (Facebook)',
        'description': 'Time series forecasting by Facebook',
        'requires_scaling': False
    }
}

# ═══════════════════════════════════════════════
# CHART CONFIGURATION (Better Performance)
# ═══════════════════════════════════════════════
CHART_CONFIG = {
    'main': {
        'height': 380,
        'updatemenus': None,  # Disable for performance
        'template': 'plotly_dark'
    },
    'secondary': {
        'height': 280,
        'template': 'plotly_dark'
    }
}

# ═══════════════════════════════════════════════
# DEMO MODE SETTINGS
# ═══════════════════════════════════════════════
DEMO_MODE = {
    'enable_synthetic_data': True,
    'synthetic_data_points': 1000,
    'synthetic_pattern': 'sine_wave',  # 'sine_wave', 'random_walk', 'spike'
    'enable_animations': True,
    'show_debug_info': False
}

# ═══════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ═══════════════════════════════════════════════
# FEATURE FLAGS (For Progressive Enhancement)
# ═══════════════════════════════════════════════
FEATURES = {
    'enable_3layer_defense': True,
    'enable_anomaly_detection': True,
    'enable_cost_tracking': True,
    'enable_server_grid_animation': True,
    'enable_real_time_metrics': True,
    'enable_forecast_confidence_bands': False,  # Advanced feature
    'enable_multi_model_ensemble': False  # Future feature
}

# ═══════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════
def get_data_path(filename: str) -> str:
    """Find data file in possible directories."""
    for base_dir in POSSIBLE_DATA_DIRS:
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            return path
    return None

def get_model_path(filename: str) -> str:
    """Find model file in possible directories."""
    for base_dir in POSSIBLE_MODEL_DIRS:
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            return path
    return None
