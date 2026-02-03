"""
Configuration Center for Autoscaling Analysis
"""
import os

# --- AWS Color Palette ---
AWS_SQUID_INK = "#232F3E"
AWS_ORANGE = "#FF9900"
AWS_BLUE = "#146EB4"
AWS_LIGHT_BLUE = "#00A8E1"
AWS_DARK_BG = "#16191f"

# --- Simulation Settings ---
SIMULATION_SPEED_DEFAULT = 0.5  # seconds per tick
SIMULATION_STEPS = 200

# --- Autoscaling Parameters ---
DEFAULT_SCALE_OUT_THRESHOLD = 150  # req/min
DEFAULT_SCALE_IN_THRESHOLD = 50    # req/min
DEFAULT_COOLDOWN_PERIOD = 3        # minutes (ticks)
MIN_REPLICAS = 1
MAX_REPLICAS = 20
INITIAL_REPLICAS = 5
FIXED_REPLICAS = 10

# --- Cost Model ---
COST_PER_REPLICA_PER_TICK = 0.1 # Currency unit

# --- Anomaly Detection ---
ANOMALY_SPIKE_MULTIPLIER = 1.5
ANOMALY_DROP_MULTIPLIER = 0.5
ANOMALY_DROP_THRESHOLD = 30

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")  # Fix: models/ not data/models/
