# Models Directory

This folder stores trained machine learning models.

## Files

- `maintenance_model.pkl`: Trained predictive maintenance model
- `scaler.pkl`: Feature scaler (if saved separately)

## Training

Models are automatically trained and saved when you run the training script:
```bash
python train_model.py
```

## Model Info

- Algorithm: Gradient Boosting Classifier
- Features: 16 extracted features from sensor data
- Target: Binary classification (failure/no failure)
- Performance: Check model_metrics.json for latest metrics

## Note

`.pkl` files are gitignored - they should not be committed to version control.