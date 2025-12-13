# Tests Directory

Unit tests for the maintenance predictor API.

## Running Tests
```bash
pip install pytest pytest-cov

pytest

pytest --cov=. --cov-report=html

pytest tests/test_api.py

pytest -v
```

## Test Files

- `test_api.py`: API endpoint tests
- `test_data_processor.py`: Data processing tests
- `test_ml_model.py`: ML model tests

## Coverage

After running tests with coverage, view the report:
```bash
open htmlcov/index.html 
xdg-open htmlcov/index.html 
```