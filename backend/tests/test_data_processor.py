import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processor import DataProcessor

def test_process_sensor_data():
    """Test data processing"""
    processor = DataProcessor()
    
    df = pd.DataFrame({
        'asset_name': ['Test-1'],
        'timestamp': ['2024-12-01 08:00:00'],
        'temperature': [75.5],
        'vibration': [1.2],
        'pressure': [95.3],
        'runtime': [3200],
        'last_maintenance': ['2024-10-15']
    })
    
    processed = processor.process_sensor_data(df)
    assert not processed.empty
    assert 'temperature' in processed.columns

def test_handle_missing_values():
    """Test missing value handling"""
    processor = DataProcessor()
    
    df = pd.DataFrame({
        'temperature': [75.5, None, 80.0],
        'vibration': [1.2, 1.5, None]
    })
    
    processed = processor.handle_missing_values(df)
    assert processed['temperature'].notna().all()
    assert processed['vibration'].notna().all()

def test_extract_features():
    """Test feature extraction"""
    processor = DataProcessor()
    
    data = {
        'temperature': 80.0,
        'vibration': 1.5,
        'pressure': 100.0,
        'runtime': 3000
    }
    
    features = processor.extract_features(data)
    assert isinstance(features, list)
    assert len(features) > 0