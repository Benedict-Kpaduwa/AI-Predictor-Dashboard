import pandas as pd
import numpy as np
from typing import Dict, List

class DataProcessor:
    def __init__(self):
        self.expected_columns = [
            'asset_name', 'timestamp', 'temperature', 'vibration', 
            'pressure', 'runtime', 'last_maintenance'
        ]
    
    def process_sensor_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process uploaded sensor CSV data"""
        df.columns = df.columns.str.strip().str.lower()
        df = self.handle_missing_values(df)
        df = self.convert_data_types(df)
        df = self.add_derived_features(df)
        return df
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the dataset"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col].fillna(df[col].median(), inplace=True)
        return df
    
    def convert_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert columns to appropriate data types"""
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        numeric_cols = ['temperature', 'vibration', 'pressure', 'runtime']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def add_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add derived features for better predictions"""
        if 'temperature' in df.columns:
            temp_mean = df['temperature'].mean()
            temp_std = df['temperature'].std()
            if temp_std > 0:
                df['temp_anomaly'] = (df['temperature'] - temp_mean).abs() / temp_std
            else:
                df['temp_anomaly'] = 0
        
        if 'vibration' in df.columns:
            df['vibration_severity'] = pd.cut(
                df['vibration'], 
                bins=[0, 1, 2, 10], 
                labels=['low', 'medium', 'high']
            )
        
        if 'last_maintenance' in df.columns:
            df['last_maintenance'] = pd.to_datetime(df['last_maintenance'], errors='coerce')
            df['days_since_maintenance'] = (pd.Timestamp.now() - df['last_maintenance']).dt.days
        
        return df
    
    def extract_features(self, data: Dict) -> List[float]:
        """Extract features from a single data point"""
        features = [
            data.get('temperature', 0),
            data.get('vibration', 0),
            data.get('pressure', 0),
            data.get('runtime', 0),
        ]
        return features
    
    def create_sample_csv(self, filepath: str, n_assets: int = 10):
        """Create a sample CSV file for testing"""
        data = {
            'asset_name': [f'Asset-{i}' for i in range(n_assets)],
            'timestamp': pd.date_range(start='2024-01-01', periods=n_assets, freq='D'),
            'temperature': np.random.uniform(60, 100, n_assets),
            'vibration': np.random.uniform(0.5, 3.0, n_assets),
            'pressure': np.random.uniform(80, 120, n_assets),
            'runtime': np.random.randint(1000, 6000, n_assets),
            'last_maintenance': pd.date_range(start='2023-10-01', periods=n_assets, freq='W')
        }
        
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"Sample CSV created at {filepath}")