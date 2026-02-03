import config

class AnomalyDetector:
    def __init__(self):
        pass
        
    def detect(self, current_load: float, forecast_load: float) -> str:
        """
        Checks for anomalies.
        Returns: 'NORMAL', 'DDoS SPIKE', 'UNDERLOAD'
        """
        # 1. DDoS / Sudden Spike
        # If current load is significantly higher than forecast (if forecast is reliable)
        # OR if current load > Average + 3 Sigma (Dynamic)
        # Simple Logic for Demo: Threshold based on forecast
        
        if forecast_load > 0:
            ratio = current_load / forecast_load
            if ratio > config.ANOMALY_SPIKE_MULTIPLIER:
                return "DDoS / SPIKE DETECTED"
            if ratio < config.ANOMALY_DROP_MULTIPLIER and current_load > 100: # Ignore low load noise
                return "SUDDEN DROP DETECTED"
                
        # Absolute threshold fallback
        # config.ANOMALY_DROP_THRESHOLD
        
        return "NORMAL"
