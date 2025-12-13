from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import io
from datetime import datetime, timedelta
import traceback
import os


from ml_model import MaintenancePredictor
from data_processor import DataProcessor
from fastapi.responses import StreamingResponse
from pdf_generator import MaintenanceReportGenerator

app = FastAPI(title="AI Maintenance Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = os.getenv("STATIC_PATH", "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

model = MaintenancePredictor()
processor = DataProcessor()

uploaded_assets = []

class Asset(BaseModel):
    id: int
    name: str
    riskLevel: str
    riskScore: float
    temperature: float
    vibration: float
    pressure: float
    runtime: int
    lastMaintenance: str
    predictedFailure: int

class PredictionResponse(BaseModel):
    assets: List[Asset]
    summary: Dict

class TrainRequest(BaseModel):
    retrain: bool = False
    n_samples: Optional[int] = 5000

class TrainResponse(BaseModel):
    status: str
    message: str
    metrics: dict
    training_time: float

training_status = {
    "is_training": False,
    "progress": 0,
    "message": "No training in progress"
}

@app.get("/")
def read_root():
    return {
        "message": "AI Maintenance Predictor API", 
        "status": "running", 
        "version": "1.0",
        "assets_count": len(uploaded_assets),
        "model_trained": model.is_trained
    }

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    """Upload sensor CSV data and get predictions"""
    global uploaded_assets
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        print(f"Received CSV with {len(df)} rows and columns: {df.columns.tolist()}")
        
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="CSV file is empty")

        processed_data = processor.process_sensor_data(df)
        print(f"Processed data: {len(processed_data)} rows")
        
        if model.is_trained:
            print("Using trained ML model for predictions...")
            feature_list = []
            
            for _, row in processed_data.iterrows():
                features = [
                    row.get('temperature', 0),
                    row.get('temperature', 0) ** 2,
                    processed_data['temperature'].std() if 'temperature' in processed_data.columns else 10,
                    processed_data['temperature'].max() if 'temperature' in processed_data.columns else 85,
                    row.get('vibration', 0),
                    row.get('vibration', 0) ** 2,
                    processed_data['vibration'].max() if 'vibration' in processed_data.columns else 2.5,
                    row.get('pressure', 0),
                    processed_data['pressure'].std() if 'pressure' in processed_data.columns else 5,
                    row.get('runtime', 0),
                    abs(row.get('temperature', 0) - 75) / 10, 
                    abs(row.get('vibration', 0) - 1.0) / 0.3, 
                    abs(row.get('pressure', 0) - 95) / 5,
                    row.get('temperature', 0) * row.get('vibration', 0),
                    row.get('runtime', 0) / 6000,        
                    int(row.get('runtime', 0) > 4000)        
                ]
                feature_list.append(features)

            X_features = np.array(feature_list)
            predictions = model.predict(X_features)
            print(f"Generated {len(predictions)} predictions using trained model")
        else:
            print("Warning: Model not trained, using random predictions for demo")
            predictions = np.random.random(len(processed_data))
            print(f"Generated {len(predictions)} random predictions")

        assets = generate_asset_predictions(processed_data, predictions)
        print(f"Generated {len(assets)} assets")
        
        uploaded_assets = assets

        summary = {
            "total_assets": len(assets),
            "healthy": sum(1 for a in assets if a['riskLevel'] == 'healthy'),
            "warning": sum(1 for a in assets if a['riskLevel'] == 'warning'),
            "critical": sum(1 for a in assets if a['riskLevel'] == 'critical'),
            "avg_risk_score": round(np.mean([a['riskScore'] for a in assets]), 2),
            "model_used": "trained" if model.is_trained else "random"
        }
        
        return {"assets": assets, "summary": summary}
    
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/assets/")
def get_all_assets():
    """Get all uploaded assets"""
    return uploaded_assets

@app.get("/assets/{asset_id}")
def get_asset_detail(asset_id: int):
    """Get detailed information for a specific asset"""
    asset = next((a for a in uploaded_assets if a['id'] == asset_id), None)
    
    if not asset:
        raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")
    
    asset_with_history = asset.copy()
    asset_with_history['historicalData'] = generate_historical_data()
    
    return asset_with_history

@app.delete("/assets/")
def clear_all_assets():
    """Clear all uploaded assets"""
    global uploaded_assets
    count = len(uploaded_assets)
    uploaded_assets = []
    return {"message": f"Cleared {count} assets", "status": "success"}

@app.post("/predict/")
def predict_single(data: Dict):
    """Make prediction for a single asset"""
    try:
        features = np.array([[
            data.get('temperature', 0),
            data.get('temperature', 0) ** 2,
            10, 85,
            data.get('vibration', 0),
            data.get('vibration', 0) ** 2,
            2.5,
            data.get('pressure', 0),
            5,
            data.get('runtime', 0),
            abs(data.get('temperature', 0) - 75) / 10,
            abs(data.get('vibration', 0) - 1.0) / 0.3,
            abs(data.get('pressure', 0) - 95) / 5,
            data.get('temperature', 0) * data.get('vibration', 0),
            data.get('runtime', 0) / 6000,
            int(data.get('runtime', 0) > 4000)
        ]])
        
        prediction = model.predict(features)[0]
        
        return {
            "riskScore": float(prediction * 100),
            "riskLevel": get_risk_level(prediction),
            "predictedFailure": int(30 * (1 - prediction)),
            "model_used": "trained" if model.is_trained else "random"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

def get_risk_level(score: float) -> str:
    """Convert risk score to level"""
    if score > 0.7:
        return "critical"
    elif score > 0.4:
        return "warning"
    return "healthy"

def generate_asset_predictions(data: pd.DataFrame, predictions: np.ndarray) -> List[Dict]:
    """Generate asset list with predictions"""
    assets = []
    
    for idx, (_, row) in enumerate(data.iterrows()):
        if idx >= len(predictions):
            break
            
        risk_score = predictions[idx] * 100
        risk_level = get_risk_level(predictions[idx])
        
        try:
            asset = {
                "id": idx + 1,
                "name": str(row.get('asset_name', f'Asset-{idx+1}')),
                "riskLevel": risk_level,
                "riskScore": round(float(risk_score), 2),
                "temperature": float(row.get('temperature', 0)),
                "vibration": float(row.get('vibration', 0)),
                "pressure": float(row.get('pressure', 0)),
                "runtime": int(row.get('runtime', 0)),
                "lastMaintenance": str(row.get('last_maintenance', datetime.now().strftime('%Y-%m-%d'))),
                "predictedFailure": int(30 * (1 - predictions[idx]))
            }
            assets.append(asset)
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
    
    return assets

@app.get("/export-report/")
def export_report():
    """Export current assets as PDF report"""
    if not uploaded_assets:
        raise HTTPException(status_code=400, detail="No assets available. Upload CSV first.")
    
    try:
        summary = {
            "total_assets": len(uploaded_assets),
            "healthy": sum(1 for a in uploaded_assets if a['riskLevel'] == 'healthy'),
            "warning": sum(1 for a in uploaded_assets if a['riskLevel'] == 'warning'),
            "critical": sum(1 for a in uploaded_assets if a['riskLevel'] == 'critical'),
            "avg_risk_score": round(np.mean([a['riskScore'] for a in uploaded_assets]), 2)
        }

        generator = MaintenanceReportGenerator()
        pdf_bytes = generator.generate_report(uploaded_assets, summary)

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=maintenance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
        )
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

def generate_historical_data() -> List[Dict]:
    """Generate 24-hour historical sensor data"""
    data = []
    for i in range(24):
        data.append({
            "time": f"{i}:00",
            "temperature": 65 + np.random.random() * 20 + np.sin(i / 3) * 10,
            "vibration": 1 + np.random.random() * 1 + np.sin(i / 4) * 0.5,
            "pressure": 95 + np.random.random() * 15 + np.cos(i / 5) * 8
        })
    return data


@app.post("/train/", response_model=TrainResponse)
async def train_model_endpoint(
    request: TrainRequest,
    background_tasks: BackgroundTasks
):
    """
    Train or retrain the ML model
    
    Args:
        request: TrainRequest with training parameters
        background_tasks: FastAPI background tasks
        
    Returns:
        TrainResponse with training status and metrics
    
    Example:
        POST /train/
        {
            "retrain": true,
            "n_samples": 5000
        }
    """
    global training_status

    if training_status["is_training"]:
        raise HTTPException(
            status_code=409, 
            detail="Training already in progress. Please wait for completion."
        )

    if not (100 <= request.n_samples <= 50000):
        raise HTTPException(
            status_code=400,
            detail="n_samples must be between 100 and 50,000"
        )

    background_tasks.add_task(
        train_model_background,
        request.n_samples,
        request.retrain
    )
    
    return TrainResponse(
        status="started",
        message=f"Model training initiated with {request.n_samples} samples",
        metrics={},
        training_time=0.0
    )


def train_model_background(n_samples: int, retrain: bool):
    """Background task for model training"""
    global training_status, model
    
    try:
        training_status["is_training"] = True
        training_status["progress"] = 0
        training_status["message"] = "Generating training data..."
        
        start_time = time.time()

        print(f"Generating {n_samples} training samples...")
        X, y = model.generate_synthetic_training_data(n_samples=n_samples)
        training_status["progress"] = 30
        training_status["message"] = "Training model..."

        print(f"Training Gradient Boosting model...")
        model.train(X, y)
        training_status["progress"] = 80
        training_status["message"] = "Saving model..."
  
        print(f"Saving trained model...")
        model.save_model("models/maintenance_model.pkl")
        training_status["progress"] = 100
        
        training_time = time.time() - start_time
        
        training_status["is_training"] = False
        training_status["message"] = f"Training completed in {training_time:.2f}s"
        
        print(f"Model training completed successfully!")
        
    except Exception as e:
        training_status["is_training"] = False
        training_status["progress"] = 0
        training_status["message"] = f"Training failed: {str(e)}"
        print(f"Training error: {str(e)}")


@app.get("/train/status/")
def get_training_status():
    """
    Get current training status
    
    Returns:
        Current training progress and status
    """
    return {
        "is_training": training_status["is_training"],
        "progress": training_status["progress"],
        "message": training_status["message"],
        "model_loaded": model.is_trained,
        "model_path": "models/maintenance_model.pkl"
    }

@app.get("/")
async def serve_react_app():
    """Serve React app"""
    static_path = os.getenv("STATIC_PATH", "static")
    index_file = os.path.join(static_path, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        return {
            "message": "AI Maintenance Predictor API", 
            "status": "running",
            "docs": "/docs"
        }

@app.get("/{full_path:path}")
async def serve_react_routes(full_path: str):
    """Serve React app for all routes"""
    static_path = os.getenv("STATIC_PATH", "static")
    file_path = os.path.join(static_path, full_path)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    
    return {"error": "Not found", "api_docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    print("Starting AI Maintenance Predictor API...")
    print("Note: Assets list starts empty until CSV is uploaded")
    print(f"Model Status: {'Trained ✓' if model.is_trained else 'Not Trained (using random predictions)'}")
    uvicorn.run(app, host="0.0.0.0", port=5000)