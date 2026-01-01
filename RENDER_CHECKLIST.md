# ✅ Render Deployment Checklist

## Files Ready

- ✅ `render.yaml` - Render configuration
- ✅ `build.sh` - Build script (executable)
- ✅ `requirements.txt` - Python dependencies
- ✅ `backend/main.py` - Updated for Render (PORT env, static serving)
- ✅ `frontend/src/MaintenanceDashboard.tsx` - Same-origin API calls

## Quick Deploy Steps

### 1️⃣ Push to GitHub

```bash
cd /Users/benedictkpaduwa/Documents/Projects/predictor

git add .
git commit -m "Configure for Render deployment"

# If SSH works:
git push origin master

# If SSH doesn't work (use HTTPS):
git remote set-url origin https://github.com/Benedict-Kpaduwa/AI-Predictor-Dashboard.git
git push origin master
```

### 2️⃣ Deploy on Render

1. Go to **[render.com](https://render.com)** → Sign up/Login
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub and select **`AI-Predictor-Dashboard`**
4. Render detects `render.yaml` automatically
5. Click **"Apply"** 
6. Wait 3-5 minutes ⏱️

### 3️⃣ Test Your App

Your app will be at: `https://ai-maintenance-predictor.onrender.com`

Test:
- [ ] Homepage loads (React dashboard)
- [ ] API docs work (`/docs`)
- [ ] Upload CSV (`backend/data/sample_sensors.csv`)
- [ ] View predictions
- [ ] Export PDF

## What Happens During Build

```
==> Cloning repository...
==> Running build.sh
    → Installing Python dependencies
    → Building frontend with npm
==> Starting service
    → uvicorn main:app --host 0.0.0.0 --port $PORT
==> Service is live! 🎉
```

## Environment

- **Python:** 3.11.0
- **Region:** Oregon (US West)
- **Plan:** Free
- **Branch:** master

## After Deployment

### Automatic Updates
Every time you push to `master`, Render will:
1. Pull latest code
2. Run build script
3. Restart service
4. Deploy new version

### View Logs
- Render Dashboard → Your Service → Logs

### Monitor
- CPU usage
- Memory usage
- Response times

## Troubleshooting

### Build fails?
```bash
# Test locally
./build.sh

# Check:
- requirements.txt has all dependencies
- frontend/package.json is valid
- npm install works
```

### Service won't start?
- Check logs in Render dashboard
- Verify PORT environment variable is used
- Test locally: `cd backend && uvicorn main:app --port 8000`

### Frontend not loading?
- Check `frontend/dist/` was created during build
- Verify static path in main.py: `../frontend/dist`
- Check logs for file not found errors

## Free Tier Notes

⚠️ **Service spins down after 15 min of inactivity**
- First request after spin-down: ~30-60 seconds
- Subsequent requests: fast

✅ **Upgrade to $7/month for always-on service**

## Success Criteria

- ✅ Build completes without errors
- ✅ Service shows "Live" status
- ✅ Homepage loads
- ✅ API endpoints work
- ✅ Can upload CSV and get predictions
- ✅ PDF export works

## Next Steps After Successful Deploy

1. **Share your URL**: `https://your-app.onrender.com`
2. **Set up custom domain** (optional, requires paid plan)
3. **Enable automatic deploys** (already configured)
4. **Monitor usage** in Render dashboard

## Commands Summary

```bash
# Push to GitHub
git add .
git commit -m "Configure for Render deployment"
git push origin master

# That's it! Render does the rest automatically
```

## Quick Links

- **Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
- **Documentation**: See `RENDER_DEPLOY.md`
- **Support**: [Render Docs](https://render.com/docs)

---

## 🎉 You're Ready!

Just push to GitHub and deploy on Render. It's that simple!

**Estimated time:** 5 minutes (3 min to push + 2 min initial setup on Render)
**Build time:** 3-5 minutes
**Total:** ~10 minutes to live deployment

