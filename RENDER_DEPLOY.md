# 🚀 Render Deployment Guide

Your AI Maintenance Predictor is now configured for **Render** deployment!

## Why Render?

✅ **Better for Full-Stack Python Apps**
- Native Python support
- Serves both backend and frontend from one service
- No serverless function limits
- Free tier includes 750 hours/month
- Persistent file system for ML models
- Simple configuration

## What's Been Done

✅ **Configuration files created:**
- `render.yaml` - Render Blueprint configuration
- `build.sh` - Build script (builds frontend + installs Python deps)

✅ **Code updated:**
- `backend/main.py` - Serves frontend static files, uses PORT env variable
- `frontend/src/MaintenanceDashboard.tsx` - Uses same origin for API calls
- `requirements.txt` - All Python dependencies listed

## 🎯 Deploy Now (3 Easy Steps)

### Step 1: Push to GitHub

```bash
cd /Users/benedictkpaduwa/Documents/Projects/predictor

# Add all changes
git add .

# Commit
git commit -m "Configure for Render deployment"

# Push (use one of these methods)
git push origin master
# OR if SSH doesn't work:
git remote set-url origin https://github.com/Benedict-Kpaduwa/AI-Predictor-Dashboard.git
git push origin master
```

### Step 2: Create Render Account & Deploy

1. **Go to [Render.com](https://render.com)** and sign up/login
2. **Connect GitHub**: Authorize Render to access your repositories
3. **Click "New +" → "Blueprint"**
4. **Select your repository**: `AI-Predictor-Dashboard`
5. **Render will auto-detect** `render.yaml`
6. **Click "Apply"**

That's it! Render will:
- Install Python dependencies
- Build the React frontend
- Start the FastAPI server
- Deploy everything together

### Step 3: Wait for Deployment (~3-5 minutes)

You'll see:
```
==> Installing Python dependencies...
==> Building Frontend...
==> Starting application...
==> Your service is live at https://your-app.onrender.com
```

## 📋 How It Works

### Build Process (build.sh):
```bash
1. Install Python dependencies (pip install -r requirements.txt)
2. Install Node.js dependencies (npm install)
3. Build React app (npm run build) → frontend/dist/
```

### Runtime:
```bash
FastAPI server starts at port $PORT (Render auto-assigns)
├── Serves API endpoints: /upload/, /assets/, /predict/, etc.
├── Serves frontend: / → index.html
└── Serves static files: /assets/* → frontend/dist/assets/*
```

### Architecture:
```
https://your-app.onrender.com/
    ↓
FastAPI (Python) on Render
    ├── API Routes (/upload, /assets, /predict, etc.)
    └── Static Files (React app from /frontend/dist)
```

## 🔧 Configuration Details

### render.yaml
```yaml
services:
  - type: web
    name: ai-maintenance-predictor
    env: python
    region: oregon
    plan: free
    branch: master
    buildCommand: "./build.sh"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### Environment Variables (Auto-set):
- `PORT` - Render automatically sets this
- `PYTHON_VERSION` - 3.11.0
- `STATIC_PATH` - ../frontend/dist

## ✅ What Works on Render Free Tier

- ✅ 750 hours/month (enough for 24/7 if only one service)
- ✅ Automatic HTTPS
- ✅ Auto-deploy on git push
- ✅ Persistent disk (for ML models)
- ✅ Full Python environment
- ✅ No function timeout limits (unlike Vercel)
- ✅ No cold starts after first request
- ✅ Custom domains (with paid plan)

## ⚠️ Free Tier Limitations

- **Spin down after 15 minutes** of inactivity
- First request after spin-down takes ~30-60 seconds
- Limited to 512 MB RAM (should be enough)
- 0.1 CPU (shared)

**Solution for spin-down:** Upgrade to paid tier ($7/month) for always-on service

## 🧪 Testing Your Deployment

After deployment completes:

### 1. Check Homepage
```
https://your-app.onrender.com/
```
Should show your React dashboard

### 2. Check API
```
https://your-app.onrender.com/docs
```
Should show FastAPI Swagger documentation

### 3. Test Functionality
- Upload `backend/data/sample_sensors.csv`
- View predictions
- Check asset details
- Export PDF report

## 📊 Monitoring

### View Logs:
1. Go to Render Dashboard
2. Click your service
3. Click "Logs" tab
4. See real-time logs

### Check Metrics:
- CPU usage
- Memory usage
- Request count
- Response times

## 🔄 Updating Your App

Once deployed, updates are automatic:

```bash
# Make changes to your code
git add .
git commit -m "Update feature"
git push origin master

# Render automatically detects and redeploys!
```

## 🐛 Troubleshooting

### Build Fails?

**Check build logs** in Render dashboard.

Common issues:
1. **Missing dependencies** - Check `requirements.txt`
2. **Frontend build fails** - Test locally: `cd frontend && npm run build`
3. **Python version** - Render uses 3.7 by default, we specify 3.11.0

### Service Won't Start?

**Check runtime logs** in Render dashboard.

Common issues:
1. **Wrong port** - Make sure using `$PORT` environment variable
2. **Missing files** - Ensure `frontend/dist` was built
3. **Import errors** - Check all Python imports work

### API Not Working?

1. Check `/docs` endpoint works
2. Check logs for errors
3. Verify CORS settings (already configured for `*`)

## 🎨 Custom Domain (Optional)

1. Go to Render Dashboard → Your Service → Settings
2. Add custom domain
3. Update DNS records as instructed
4. Render provides free SSL

## 💰 Upgrade Options

### Free Tier
- ✅ Good for development/testing
- ⚠️ Spins down after inactivity

### Starter ($7/month)
- ✅ Always on (no spin-down)
- ✅ More RAM & CPU
- ✅ Priority support

### Pro ($25/month)
- ✅ Even more resources
- ✅ Multiple instances
- ✅ Advanced features

## 📁 Files Structure on Render

After build:
```
/opt/render/project/src/
├── backend/
│   ├── main.py (FastAPI server)
│   ├── ml_model.py
│   ├── models/
│   │   └── maintenance_model.pkl
│   └── ...
├── frontend/
│   └── dist/ (Built React app)
│       ├── index.html
│       └── assets/
├── requirements.txt
├── build.sh
└── render.yaml
```

## 🔑 Environment Variables (Optional)

Add custom env vars in Render Dashboard:

1. Go to Service → Environment
2. Add key-value pairs:
   - `MODEL_PATH` - Custom model path
   - `MAX_UPLOAD_SIZE` - Maximum CSV size
   - `DEBUG` - Enable debug mode

## 📚 Additional Resources

- [Render Docs](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-fastapi)
- [Render Blueprint](https://render.com/docs/blueprint-spec)

## ✨ Key Advantages Over Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| Python Support | ✅ Native | ⚠️ Serverless only |
| Function Timeout | ✅ No limit | ⚠️ 10s (free) / 60s (pro) |
| File System | ✅ Persistent | ❌ Ephemeral |
| Cold Starts | ✅ Minimal | ⚠️ 1-2s every time |
| Full Stack | ✅ One service | ⚠️ Separate frontend/backend |
| ML Models | ✅ Easy to load | ⚠️ Size limits |
| Model Training | ✅ Works | ❌ Timeouts |

## 🎉 Summary

Your app is ready for Render! Just:

1. **Push to GitHub**
2. **Connect to Render**
3. **Deploy as Blueprint**

**Estimated deployment time:** 3-5 minutes

**Your app will be live at:** `https://ai-maintenance-predictor.onrender.com` (or similar)

---

## 🆘 Need Help?

**Deployment issues:**
1. Check build logs in Render dashboard
2. Verify all files committed to GitHub
3. Test build locally: `./build.sh`

**Runtime issues:**
1. Check service logs in Render
2. Test API at `/docs`
3. Verify frontend built: `ls frontend/dist/`

**Questions?** Check [Render Docs](https://render.com/docs) or let me know!

