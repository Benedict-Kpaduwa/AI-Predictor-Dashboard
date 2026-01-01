# Quick Deployment Checklist

## Pre-Deployment Checklist

- [x] Updated `vercel.json` with correct configuration
- [x] Fixed `api/index.py` handler
- [x] Updated `backend/main.py` with proper imports and removed duplicate routes
- [x] Added all required dependencies to `requirements.txt`
- [x] Created `.vercelignore` to exclude unnecessary files
- [x] Created `.gitignore` for version control
- [x] Updated frontend `vite.config.ts` with build configuration
- [x] Fixed API URL detection in `MaintenanceDashboard.tsx` (uses `import.meta.env.PROD`)
- [x] Ensured frontend builds to `dist` directory

## Files Changed/Created

### Modified Files
1. `vercel.json` - Vercel deployment configuration
2. `api/index.py` - Python serverless handler
3. `backend/main.py` - Fixed imports, removed duplicate routes
4. `requirements.txt` - Added missing dependencies
5. `backend/requirements.txt` - Updated with all dependencies
6. `frontend/vite.config.ts` - Added build configuration
7. `frontend/src/MaintenanceDashboard.tsx` - Fixed API URL detection

### New Files
1. `.vercelignore` - Exclude files from deployment
2. `.gitignore` - Version control ignore file
3. `DEPLOYMENT.md` - Comprehensive deployment guide
4. `CHECKLIST.md` - This file

## Deployment Steps

### 1. Commit Your Changes (if using Git)

```bash
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### 2. Deploy to Vercel

#### Option A: Via Vercel Dashboard (Easiest)

1. Go to https://vercel.com/new
2. Import your Git repository
3. Vercel will auto-detect the configuration
4. Click "Deploy"
5. Wait for build to complete

#### Option B: Via Vercel CLI

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### 3. Test Your Deployment

After deployment, test these URLs (replace `your-project` with your actual domain):

1. **Homepage**: `https://your-project.vercel.app`
2. **API Health**: `https://your-project.vercel.app/api/`
3. **API Docs**: `https://your-project.vercel.app/api/docs`
4. **Assets Endpoint**: `https://your-project.vercel.app/api/assets/`

### 4. Upload Test Data

1. Open the deployed app
2. Click "Upload CSV"
3. Upload `backend/data/sample_sensors.csv`
4. Verify predictions are generated

## Expected Behavior

### Frontend
- React app loads at root URL (`/`)
- All routes work correctly
- API calls go to `/api/*`

### Backend
- Python FastAPI running as serverless function
- Available at `/api/*`
- Swagger docs at `/api/docs`
- All endpoints functional

### API Endpoints Available

- `GET /api/` - Health check
- `POST /api/upload/` - Upload CSV for predictions
- `GET /api/assets/` - Get all assets
- `GET /api/assets/{id}` - Get specific asset
- `DELETE /api/assets/` - Clear all assets
- `POST /api/predict/` - Single prediction
- `GET /api/export-report/` - Export PDF report
- `POST /api/train/` - Train ML model
- `GET /api/train/status/` - Training status

## Troubleshooting

### Build Fails

**Frontend build error:**
```bash
cd frontend
pnpm install
pnpm run build
# Check for TypeScript or build errors
```

**Backend error:**
```bash
cd backend
python -m pip install -r requirements.txt
python main.py
# Test locally
```

### API Not Working

1. Check Vercel logs: Dashboard > Project > Logs
2. Verify rewrites in `vercel.json`
3. Check that `api/index.py` is present
4. Ensure all imports in backend work

### CORS Issues

The API is configured with `allow_origins=["*"]` so CORS should work.
If you see CORS errors, check browser console and Vercel logs.

### Model Not Loading

The app will work without a trained model (using random predictions).
To use a real model:
1. Train locally: `cd backend && python train_model.py`
2. Upload `models/maintenance_model.pkl` to Vercel
3. Or use the `/api/train/` endpoint after deployment

## Important Notes

### Limitations on Vercel Free Tier

1. **Serverless Function Timeout**
   - 10 seconds for Hobby plan
   - 60 seconds for Pro plan
   - Model training might timeout (use local training and upload model)

2. **File Size Limits**
   - Serverless functions: 250 MB max
   - ML models should be optimized

3. **Cold Starts**
   - First request may be slow (1-2 seconds)
   - Subsequent requests are faster

### Best Practices

1. **Keep Model Size Small**
   - Current model is ~1-5 MB (should be fine)
   - Consider model compression for larger models

2. **Use Environment Variables**
   - Store sensitive data in Vercel environment variables
   - Access via `os.getenv()`

3. **Monitor Performance**
   - Use Vercel Analytics
   - Check function logs regularly

4. **Version Control**
   - Keep `.gitignore` updated
   - Don't commit `.env` files
   - Don't commit large data files

## Post-Deployment Tasks

- [ ] Test all features
- [ ] Upload sample data
- [ ] Try PDF export
- [ ] Test model training (if needed)
- [ ] Set up custom domain (optional)
- [ ] Configure environment variables (if needed)
- [ ] Enable Vercel Analytics (optional)
- [ ] Set up error alerts (optional)

## Need Help?

1. Check `DEPLOYMENT.md` for detailed instructions
2. Review Vercel logs for errors
3. Test locally first
4. Check [Vercel Documentation](https://vercel.com/docs)

## Success Criteria

Your deployment is successful if:
- ✅ Frontend loads correctly
- ✅ API responds at `/api/`
- ✅ Can upload CSV file
- ✅ Predictions are generated
- ✅ Detail view works
- ✅ PDF export works
- ✅ No console errors

## What to Delete (Optional)

After successful deployment, you can delete these local-only files:
- `backend/docker-compose.yml`
- `backend/Dockerfile`
- `docker-compose.yml`
- `Dockerfile`

These are only needed for Docker deployment, not Vercel.

---

**Ready to Deploy!** 🚀

Your project is now configured for Vercel. Follow the deployment steps above!

