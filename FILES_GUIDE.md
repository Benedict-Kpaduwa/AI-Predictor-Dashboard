# Files to Keep/Delete for Vercel Deployment

## ✅ REQUIRED - Keep These Files

### Deployment Configuration
```
✓ vercel.json              # Vercel configuration
✓ requirements.txt          # Python dependencies
✓ .vercelignore            # Files to exclude
✓ .gitignore               # Git exclusions
```

### API Handler
```
✓ api/
  ✓ __init__.py
  ✓ index.py               # Serverless function handler
```

### Backend
```
✓ backend/
  ✓ main.py                # FastAPI app
  ✓ ml_model.py            # ML model
  ✓ data_processor.py      # Data processing
  ✓ pdf_generator.py       # PDF generation
  ✓ requirements.txt       # Python deps (backup)
  ✓ models/
    ✓ maintenance_model.pkl # Trained model (if available)
  ✓ data/
    ✓ sample_sensors.csv   # Sample data
```

### Frontend
```
✓ frontend/
  ✓ package.json
  ✓ vite.config.ts
  ✓ index.html
  ✓ tsconfig.json
  ✓ src/                   # All source files
  ✓ components.json
```

## ❌ OPTIONAL - Can Delete for Vercel

### Docker Files (Not Used on Vercel)
```
❌ Dockerfile              # For Docker deployment
❌ docker-compose.yml      # For Docker deployment
❌ backend/Dockerfile      # For Docker deployment
❌ backend/docker-compose.yml
```

### Local Environment
```
❌ backend/venv/           # Virtual environment (already gitignored)
❌ backend/__pycache__/    # Python cache (already gitignored)
❌ frontend/node_modules/  # Node modules (already gitignored)
❌ frontend/dist/          # Build output (already gitignored)
```

### Test Files (Optional)
```
? backend/tests/           # Keep if you want to run tests
? test_vercel_setup.py     # Helper script (can delete after testing)
```

## 📋 Documentation Files

These are helpful but not required for deployment:

```
📄 README.md               # Project documentation
📄 DEPLOYMENT.md           # Deployment guide (helpful!)
📄 CHECKLIST.md            # Deployment checklist (helpful!)
📄 VERCEL_README.md        # Quick start guide (helpful!)
📄 THIS_FILE.md            # This file (optional)
```

## File Size Considerations

### Vercel Limits:
- **Serverless function size:** 250 MB max (compressed)
- **Deployment size:** Practically unlimited for static files

### What Counts Toward Function Size:
- `api/` folder
- `backend/` folder (imported by api/index.py)
- `requirements.txt` dependencies
- `models/` folder (ML models)

### Current Estimates:
```
api/                    ~2 KB
backend/                ~50 KB (code only)
models/*.pkl            ~1-5 MB (ML model)
Python dependencies:    ~200 MB (NumPy, Pandas, scikit-learn)
--------------------------------------------
Total:                  ~205 MB ✅ (under 250 MB limit)
```

## Quick Cleanup Commands

### To delete Docker files:
```bash
rm Dockerfile docker-compose.yml
rm backend/Dockerfile backend/docker-compose.yml
```

### To delete test helpers:
```bash
rm test_vercel_setup.py
rm -rf backend/tests/
```

### To clean Python cache:
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### To clean Node modules (will reinstall on Vercel):
```bash
rm -rf frontend/node_modules/
rm -rf frontend/dist/
```

## What Gets Deployed

### Frontend (Static Build):
```
frontend/dist/           → Served at /
  ├── index.html
  ├── assets/
  │   ├── index-[hash].js
  │   └── index-[hash].css
  └── ...
```

### Backend (Serverless Function):
```
api/index.py            → Runs at /api/*
  └── imports from backend/
      ├── main.py (FastAPI app)
      ├── ml_model.py
      ├── data_processor.py
      └── pdf_generator.py
```

## Deployment Size Optimization

### If you need to reduce size:

1. **Remove unused models:**
   ```bash
   # Keep only the trained model
   rm backend/models/README.md
   ```

2. **Remove sample data:**
   ```bash
   # After testing, remove large CSV files
   rm backend/data/high_risk_sensors.csv
   ```

3. **Optimize dependencies:**
   ```
   # Use lighter alternatives if needed:
   - Instead of: scikit-learn (60MB)
   - Consider: scikit-learn-intelex (optimized)
   ```

4. **Compress models:**
   ```python
   # Use joblib compression
   joblib.dump(model, 'model.pkl', compress=3)
   ```

## Summary

### Minimum Required Structure:
```
your-project/
├── vercel.json
├── requirements.txt
├── api/
│   └── index.py
├── backend/
│   ├── main.py
│   ├── ml_model.py
│   ├── data_processor.py
│   └── pdf_generator.py
└── frontend/
    ├── package.json
    ├── vite.config.ts
    └── src/
```

Everything else is optional or automatically excluded by `.vercelignore`!

## Verification Command

Check what will be deployed:
```bash
# Install Vercel CLI
npm i -g vercel

# Dry run to see what gets uploaded
vercel --prod --debug
# (Cancel before actually deploying)
```

Or use the test script:
```bash
python test_vercel_setup.py
```

