# Data Directory

This folder contains sample sensor data files for testing the maintenance predictor.

## CSV Format

The expected CSV format includes these columns:

- `asset_name`: Unique identifier for the asset (e.g., "Pump-A101")
- `timestamp`: Date and time of the reading (YYYY-MM-DD HH:MM:SS)
- `temperature`: Temperature in Celsius
- `vibration`: Vibration in mm/s
- `pressure`: Pressure in PSI
- `runtime`: Total runtime hours
- `last_maintenance`: Date of last maintenance (YYYY-MM-DD)

## Files

- `sample_sensors.csv`: Basic sample data for testing
- `high_risk_sensors.csv`: Sample data with high-risk readings
- `normal_sensors.csv`: Sample data with normal readings

## Usage

Upload these CSV files through the API endpoint:
```bash
curl -X POST -F "file=@data/sample_sensors.csv" http://localhost:8000/upload-csv/
```