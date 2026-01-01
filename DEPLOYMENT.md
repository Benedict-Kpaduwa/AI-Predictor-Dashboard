# Vercel Deployment Guide

This guide will help you deploy the AI Maintenance Predictor application to Vercel.

## Prerequisites

1. A [Vercel account](https://vercel.com/signup) (free tier works)
2. [Vercel CLI](https://vercel.com/docs/cli) installed (optional, but recommended)
3. Git repository (GitHub, GitLab, or Bitbucket)

## Project Structure

```
predictor/
├── api/                    # Vercel serverless functions
│   └── index.py           # Python API handler
├── backend/               # FastAPI backend code
│   ├── main.py           # Main FastAPI application
│   ├── ml_model.py       # ML model logic
│   ├── data_processor.py # Data processing
│   ├── pdf_generator.py  # PDF report generation
│   ├── models/           # Pre-trained ML models
│   └── data/             # Sample data
├── frontend/             # React frontend
│   └── src/             # Source code
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── .vercelignore        # Files to exclude from deployment
```

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New Project"
   - Import your Git repository
   - Vercel will auto-detect the configuration from `vercel.json`

3. **Configure Environment Variables** (Optional)
   - In Vercel Dashboard > Project Settings > Environment Variables
   - Add any custom environment variables if needed:
     - `STATIC_PATH` (default: "static")
     - Any API keys or secrets

4. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete (~2-5 minutes)
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   # For development deployment
   vercel

   # For production deployment
   vercel --prod
   ```

4. **Follow the prompts**
   - Choose your scope (personal or team)
   - Confirm project settings
   - Wait for deployment

## Configuration Details

### vercel.json

The `vercel.json` file configures:
- **Build Command**: Builds the React frontend
- **Output Directory**: Where the built frontend files are located
- **Rewrites**: Routes `/api/*` requests to the Python backend

### API Structure

- Frontend is served from `/` (root)
- API endpoints are available at `/api/*`
- Example: `https://your-app.vercel.app/api/assets/`

### Environment Variables

The app uses these environment variables:
- `NODE_ENV`: Automatically set by Vercel (`production` or `development`)
- `STATIC_PATH`: Path to static files (optional)

## Post-Deployment

### Testing Your Deployment

1. **Check the homepage**
   ```
   https://your-project.vercel.app
   ```

2. **Test API endpoints**
   ```
   https://your-project.vercel.app/api/
   https://your-project.vercel.app/api/assets/
   ```

3. **Upload a CSV file**
   - Use the sample CSV from `backend/data/sample_sensors.csv`
   - Test the prediction functionality

### Monitoring

- View logs in Vercel Dashboard > Project > Logs
- Monitor performance in Vercel Analytics
- Set up alerts for errors

## Troubleshooting

### Build Failures

**Frontend build fails:**
```bash
# Locally test the build
cd frontend
pnpm install
pnpm run build
```

**Python dependencies fail:**
- Check `requirements.txt` for incompatible versions
- Vercel uses Python 3.9 by default
- Some packages may need system dependencies

### Runtime Errors

**API returns 500 errors:**
- Check Vercel logs for Python errors
- Ensure all imports are correct
- Verify file paths are relative

**CORS errors:**
- The API is configured with `allow_origins=["*"]`
- Should work for any frontend domain

**Model not loading:**
- Ensure `backend/models/maintenance_model.pkl` exists
- The app will use random predictions if model isn't found
- You can train a model via `/api/train/` endpoint

### Common Issues

1. **Large model files**
   - Vercel has a 250MB limit for serverless functions
   - Consider using Vercel Blob storage for large models

2. **Cold starts**
   - Serverless functions may have cold starts (~1-2 seconds)
   - Use Vercel Pro for reduced cold starts

3. **API timeouts**
   - Serverless functions timeout after 10s (Hobby) or 60s (Pro)
   - Long-running tasks should use background processing

## Updating Your Deployment

### Automatic Deployments

Once connected to Git:
- Push to `main` branch → Production deployment
- Push to other branches → Preview deployment

### Manual Deployments

```bash
# Deploy to production
vercel --prod

# Deploy to preview
vercel
```

## Custom Domain

1. Go to Vercel Dashboard > Project > Settings > Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Vercel automatically provisions SSL certificate

## Performance Optimization

1. **Frontend**
   - Static files are served via Vercel CDN
   - Automatic compression and caching

2. **Backend**
   - API responses are cached when appropriate
   - Use Vercel Edge Network for global distribution

3. **ML Model**
   - Pre-trained model is loaded on cold start
   - Consider model optimization for faster loading

## Cost Considerations

**Vercel Free Tier includes:**
- 100 GB bandwidth
- Unlimited deployments
- Automatic SSL
- Serverless functions (100 GB-hours)

**Upgrade to Pro if you need:**
- More bandwidth
- Longer function execution time
- Priority support
- Team collaboration

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vite on Vercel](https://vercel.com/docs/frameworks/vite)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## Support

For issues specific to this application:
1. Check Vercel logs for errors
2. Review this deployment guide
3. Test locally first: `cd frontend && pnpm dev` and `cd backend && python main.py`

For Vercel-specific issues:
- [Vercel Support](https://vercel.com/support)
- [Vercel Community](https://github.com/vercel/vercel/discussions)

