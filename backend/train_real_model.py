#!/usr/bin/env python3
"""
Train a real predictive maintenance model using actual patterns
"""

from ml_model import MaintenancePredictor
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

def generate_realistic_training_data(n_samples=5000):
    """Generate realistic sensor data with failure patterns"""
    np.random.seed(42)
    
    normal_temp = np.random.normal(75, 10, n_samples)
    normal_vib = np.random.normal(1.0, 0.3, n_samples)
    normal_pressure = np.random.normal(95, 5, n_samples)
    runtime = np.random.randint(100, 6000, n_samples)

    failures = np.zeros(n_samples)

    high_risk_mask = (normal_temp > 85) & (normal_vib > 1.8)
    failures[high_risk_mask] = 1
 
    pressure_risk = (normal_pressure > 105) | (normal_pressure < 85)
    failures[pressure_risk] = np.random.binomial(1, 0.6, pressure_risk.sum())
    
    runtime_risk = (runtime > 5000) & (normal_temp > 80)
    failures[runtime_risk] = np.random.binomial(1, 0.7, runtime_risk.sum())

    noise_idx = np.random.choice(n_samples, size=int(n_samples * 0.05))
    failures[noise_idx] = 1 - failures[noise_idx]

    features = []
    for i in range(n_samples):
        temp_anomaly = abs(normal_temp[i] - 75) / 10
        vib_anomaly = abs(normal_vib[i] - 1.0) / 0.3
        pressure_anomaly = abs(normal_pressure[i] - 95) / 5

        temp_vib_interaction = normal_temp[i] * normal_vib[i]
        runtime_normalized = runtime[i] / 6000
        
        feature_row = [
            normal_temp[i],      
            normal_temp[i]**2,
            normal_temp.std(),
            85,           
            normal_vib[i],    
            normal_vib[i]**2,
            2.5,               
            normal_pressure[i],
            normal_pressure.std(),
            runtime[i],        
            temp_anomaly,    
            vib_anomaly,        
            pressure_anomaly,   
            temp_vib_interaction, 
            runtime_normalized,
            int(runtime[i] > 4000)
        ]
        features.append(feature_row)
    
    X = np.array(features)
    y = failures
    
    return X, y

def main():
    print("=" * 60)
    print("Training Real Predictive Maintenance Model")
    print("=" * 60)

    print("\nGenerating realistic training data...")
    X, y = generate_realistic_training_data(n_samples=5000)
    
    print(f"Generated {len(X)} samples")
    print(f"   - Normal operations: {(y == 0).sum()}")
    print(f"   - Failure cases: {(y == 1).sum()}")
    print(f"   - Failure rate: {(y == 1).sum() / len(y) * 100:.1f}%")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nTraining set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")

    print("\n🔧 Training Gradient Boosting model...")
    model = MaintenancePredictor()
    model.train(X_train, y_train)

    print("\nEvaluating model performance...")
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    
    print("\n" + "=" * 60)
    print("Model Performance Report")
    print("=" * 60)
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Failure']))
    
    print("\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(f"True Negatives:  {cm[0, 0]:4d}  |  False Positives: {cm[0, 1]:4d}")
    print(f"False Negatives: {cm[1, 0]:4d}  |  True Positives:  {cm[1, 1]:4d}")
    
    accuracy = (cm[0, 0] + cm[1, 1]) / cm.sum()
    precision = cm[1, 1] / (cm[1, 1] + cm[0, 1]) if (cm[1, 1] + cm[0, 1]) > 0 else 0
    recall = cm[1, 1] / (cm[1, 1] + cm[1, 0]) if (cm[1, 1] + cm[1, 0]) > 0 else 0
    
    print(f"\nKey Metrics:")
    print(f"   Accuracy:  {accuracy:.2%}")
    print(f"   Precision: {precision:.2%}")
    print(f"   Recall:    {recall:.2%}")
    
    print("\nSaving trained model...")
    model.save_model("models/maintenance_model.pkl")
    
    print("\nTesting predictions on sample data:")
    test_samples = [
        {"desc": "Normal operation", "temp": 75, "vib": 1.0, "pressure": 95, "runtime": 2000},
        {"desc": "High temperature", "temp": 95, "vib": 1.2, "pressure": 98, "runtime": 3500},
        {"desc": "Critical condition", "temp": 92, "vib": 2.3, "pressure": 108, "runtime": 5500},
    ]
    
    for sample in test_samples:
        features = np.array([[
            sample['temp'], sample['temp']**2, 10, 85,
            sample['vib'], sample['vib']**2, 2.5,
            sample['pressure'], 5, sample['runtime'],
            0, 0, 0, 0, sample['runtime']/6000, int(sample['runtime'] > 4000)
        ]])
        
        risk = model.predict(features)[0]
        print(f"\n   {sample['desc']}:")
        print(f"      Risk Score: {risk:.1%}")
        print(f"      Status: {'CRITICAL' if risk > 0.7 else '🟡 WARNING' if risk > 0.4 else '🟢 HEALTHY'}")
    
    print("\n" + "=" * 60)
    print("Model training complete!")
    print("=" * 60)
    print(f"\nModel saved to: models/maintenance_model.pkl")
    print("Your API will now use this trained model for predictions!")

if __name__ == "__main__":
    main()