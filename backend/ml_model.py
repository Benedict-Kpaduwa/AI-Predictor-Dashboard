import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import joblib
from typing import List, Tuple
import os

class MaintenancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = "models/maintenance_model.pkl"

        if os.path.exists(self.model_path):
            try:
                self.load_model(self.model_path)
            except:
                print("Could not load existing model, will create new one")
        
    def create_model(self):
        """Create ensemble model"""
        self.model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
    
    def extract_features(self, data: pd.DataFrame) -> np.ndarray:
        """Extract features from sensor data"""
        features = []
        
        features.extend([
            data['temperature'].mean(),
            data['temperature'].std(),
            data['temperature'].max(),
            data['temperature'].min(),
            data['vibration'].mean(),
            data['vibration'].std(),
            data['vibration'].max(),
            data['pressure'].mean(),
            data['pressure'].std(),
            data['runtime'].max() if 'runtime' in data.columns else 0
        ])
        
        if len(data) > 1:
            features.extend([
                data['temperature'].diff().mean(),
                data['vibration'].diff().mean(),
                data['pressure'].diff().mean()
            ])
        else:
            features.extend([0, 0, 0])
   
        window = min(10, len(data))
        features.extend([
            data['temperature'].rolling(window).mean().iloc[-1],
            data['vibration'].rolling(window).mean().iloc[-1],
            data['pressure'].rolling(window).mean().iloc[-1]
        ])
        
        return np.array(features)
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the model"""
        self.create_model()
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        print(f"Model trained with {len(X)} samples")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions - returns probability of failure (0-1)"""
        if not self.is_trained:
            return np.random.random(len(X))
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict_proba(X_scaled)[:, 1]
        return predictions
    
    def save_model(self, filepath: str):
        """Save model to disk"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load model from disk"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.is_trained = True
        print(f"Model loaded from {filepath}")
    
    def generate_synthetic_training_data(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for demonstration"""
        np.random.seed(42)
 
        X = np.random.randn(n_samples, 16)

        y = np.zeros(n_samples)
 
        y[(X[:, 0] > 1.5) | (X[:, 4] > 1.5)] = 1
        
        noise_idx = np.random.choice(n_samples, size=int(n_samples * 0.1))
        y[noise_idx] = 1 - y[noise_idx]
        
        return X, y