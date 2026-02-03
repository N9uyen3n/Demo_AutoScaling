import os
import joblib
import pickle
import logging

class ModelLoader:
    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self.logger = logging.getLogger(__name__)

    def load_keras_model(self, model_name: str):
        """
        Loads a Keras model from model_dir.
        """
        path = os.path.join(self.model_dir, model_name)
        if not os.path.exists(path):
            self.logger.warning(f"Model not found at {path}")
            return None
            
        try:
            from tensorflow.keras.models import load_model
            return load_model(path)
        except (ImportError, OSError):
            # Fallback for Mock models (pickled)
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e2:
                self.logger.error(f"Error loading model {model_name}: {e2}")
                return None
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")
            return None

    def load_scaler(self, scaler_name: str):
        """
        Loads a scaler (sklearn) from model_dir.
        """
        path = os.path.join(self.model_dir, scaler_name)
        if not os.path.exists(path):
            self.logger.warning(f"Scaler not found at {path}")
            return None
            
        try:
            # Try joblib first
            return joblib.load(path)
        except:
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self.logger.error(f"Error loading scaler: {e}")
                return None

    def load_generic_model(self, model_name: str):
        """
        Loads generic models (ARIMA, Prophet) from pickle/joblib.
        """
        path = os.path.join(self.model_dir, model_name)
        if not os.path.exists(path):
            return None
            
        try:
            return joblib.load(path)
        except:
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                self.logger.error(f"Error loading generic model {model_name}: {e}")
                return None
