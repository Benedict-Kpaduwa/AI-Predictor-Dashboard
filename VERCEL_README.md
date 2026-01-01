# 🚀 Vercel Deployment - Quick Start

Your AI Maintenance Predictor is now **ready for deployment on Vercel**!

## What's Been Done

✅ **All configuration files are ready:**
- `vercel.json` - Deployment configuration
- `api/index.py` - Serverless Python handler (using Mangum)
- `requirements.txt` - Python dependencies updated
- `.gitignore` / `.vercelignore` - Proper file exclusions
- Frontend configured to use `/api` in production

✅ **Code fixes applied:**
- Fixed backend imports and routes
- Removed duplicate endpoints
- Updated API URL detection in frontend
- Configured Vite build settings

## Deploy Now (3 Easy Steps)

### 1️⃣ Push to GitHub

```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### 2️⃣ Import to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your repository
3. Vercel auto-detects everything ✨
4. Click **"Deploy"**

### 3️⃣ Test Your App

After deployment (2-3 minutes):
- Visit: `https://your-project.vercel.app`
- Test API: `https://your-project.vercel.app/api/`
- Upload CSV: Use `backend/data/sample_sensors.csv`

## Files Changed

| File | What Changed |
|------|-------------|
| `vercel.json` | Build & routing configuration |
| `api/index.py` | Serverless handler setup |
| `backend/main.py` | Fixed imports, removed duplicates |
| `frontend/vite.config.ts` | Added build config |
| `frontend/src/MaintenanceDashboard.tsx` | Production API detection |
| `requirements.txt` | Added mangum, python-dotenv |

## Architecture

```
Your App URL (/)
    ↓
Frontend (React/Vite)
    ↓
API Requests (/api/*)
    ↓
Python Backend (FastAPI via Mangum)
    ↓
ML Model + Predictions
```

## Important Notes

### ✅ What Works on Vercel Free Tier
- Static frontend (React)
- Python API (serverless)
- CSV uploads
- Predictions
- PDF export
- Model loading from disk

### ⚠️ What to Know
- **Serverless timeout:** 10s (free) / 60s (pro)
- **Cold starts:** First request ~1-2s
- **File persistence:** Use Vercel Blob for large files
- **Model training:** May timeout on free tier (train locally instead)

## If Model Training Times Out

Train the model locally and commit it:

```bash
cd backend
python train_real_model.py  # or train_model.py
git add models/maintenance_model.pkl
git commit -m "Add trained model"
git push
```

Or use the smaller sample model that's already there.

## Troubleshooting

### Build Fails?
```bash
# Test frontend build
cd frontend && pnpm install && pnpm build

# Test Python imports
cd backend && pip install -r requirements.txt
```

### API Not Working?
- Check Vercel logs (Dashboard → Logs)
- Verify `api/index.py` exists
- Check rewrites in `vercel.json`

### Test Script Available
```bash
python test_vercel_setup.py
```

## Documentation

- **Full guide**: See [`DEPLOYMENT.md`](DEPLOYMENT.md)
- **Checklist**: See [`CHECKLIST.md`](CHECKLIST.md)
- **Project info**: See [`README.md`](README.md)

## Next Steps After Deployment

1. **Test everything:**
   - Upload CSV
   - View predictions
   - Check asset details
   - Export PDF

2. **Optional enhancements:**
   - Add custom domain
   - Set up environment variables
   - Enable Vercel Analytics
   - Upgrade to Pro (if needed)

## Support

**For Vercel issues:**
- [Vercel Docs](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

**For app issues:**
- Check Vercel logs
- Review error messages
- Test locally first

---

## 🎉 That's It!

Your app is ready to deploy. Just push to GitHub and import to Vercel!

**Estimated deployment time:** 2-3 minutes

**Need help?** Check `DEPLOYMENT.md` for detailed instructions.

