import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_get_assets():
    """Test getting all assets"""
    response = client.get("/assets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_asset_detail():
    """Test getting a specific asset"""
    response = client.get("/assets/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "riskLevel" in data
    assert "historicalData" in data

def test_get_nonexistent_asset():
    """Test getting an asset that doesn't exist"""
    response = client.get("/assets/9999")
    assert response.status_code == 404

def test_upload_csv():
    """Test CSV upload endpoint"""
    csv_content = """asset_name,timestamp,temperature,vibration,pressure,runtime,last_maintenance
Test-Asset,2024-12-01 08:00:00,75.5,1.2,95.3,3200,2024-10-15"""
    
    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/upload-csv/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "assets" in data
    assert "summary" in data

def test_upload_invalid_file():
    """Test uploading non-CSV file"""
    files = {"file": ("test.txt", "not a csv", "text/plain")}
    response = client.post("/upload-csv/", files=files)
    assert response.status_code == 400

def test_predict_single():
    """Test single prediction endpoint"""
    data = {
        "temperature": 80.0,
        "vibration": 1.5,
        "pressure": 100.0,
        "runtime": 3000
    }
    response = client.post("/predict/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert "riskScore" in result
    assert "riskLevel" in result
    assert "predictedFailure" in result