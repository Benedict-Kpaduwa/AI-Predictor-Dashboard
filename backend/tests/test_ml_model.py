import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_model import MaintenancePredictor

def test_model_initialization():
    """Test model initialization"""
    model = MaintenancePredictor()
    assert model is not None
    assert model.scaler is not None

def test_model_prediction():
    """Test model prediction (untrained)"""
    model = MaintenancePredictor()
    
    X = np.random.randn(5, 16)
    predictions = model.predict(X)
    
    assert len(predictions) == 5
    assert all(0 <= p <= 1 for p in predictions)

def test_model_training():
    """Test model training"""
    model = MaintenancePredictor()
    
    X, y = model.generate_synthetic_training_data(n_samples=100)
    
    assert X.shape[0] == 100
    assert y.shape[0] == 100
    
    model.train(X, y)
    assert model.is_trained == True

def test_synthetic_data_generation():
    """Test synthetic data generation"""
    model = MaintenancePredictor()
    X, y = model.generate_synthetic_training_data(n_samples=500)
    
    assert X.shape == (500, 16)
    assert y.shape == (500,)
    assert set(np.unique(y)) == {0, 1}