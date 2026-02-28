# Cloud Deployment Guide

Deploy your IKEA dashboard to the cloud for FREE using Streamlit Community Cloud.

## Option 1: Streamlit Community Cloud (Recommended) ⭐

### Prerequisites
- GitHub account with the project repository
- Streamlit Community Cloud account (free)

### Step-by-Step Deployment

#### 1. Create Streamlit Community Cloud Account
```
1. Go to https://share.streamlit.io/
2. Click "Sign up" 
3. Choose "Sign up with GitHub"
4. Authorize Streamlit
```

#### 2. Deploy Your App
```
1. Click "Create app" button
2. Select your repository: batakers/IKEA-Global-Pricing-
3. Set branch: main
4. Set main file path: dashboard/app.py
5. Click "Deploy"
```

The app will be live in ~2-3 minutes!

**Your public URL will be:**
```
https://share.streamlit.io/batakers/IKEA-Global-Pricing-/main/dashboard/app.py
```

### Features After Deployment
- ✅ Live dashboard accessible to anyone
- ✅ Auto-updates when you push to GitHub
- ✅ Free tier includes community support
- ✅ Custom domain available (paid)

---

## Option 2: Render.com (Alternative)

### Step-by-Step

#### 1. Sign Up
```
Go to https://render.com
Sign up with GitHub account
```

#### 2. Create Web Service
```
1. Click "New +" → "Web Service"
2. Connect GitHub account
3. Select your repository
4. Settings:
   - Name: ikea-pricing-dashboard
   - Environment: Python 3
   - Build Command: pip install -r requirements.txt
   - Start Command: streamlit run dashboard/app.py --server.port=10000 --server.address=0.0.0.0
5. Plan: Free tier
6. Click "Create Web Service"
```

Your app will be live at:
```
https://ikea-pricing-dashboard.onrender.com
```

---

## Testing Your Deployment

After deployment, test the dashboard:

1. **Open the live URL**
   ```
   https://share.streamlit.io/batakers/IKEA-Global-Pricing-/main/dashboard/app.py
   ```

2. **Verify all 3 pages work:**
   - Executive Overview (KPI cards, world map)
   - Pricing Strategy (charts, benchmarks)
   - Market Adaptation (affordability, online availability)

3. **Test interactive elements:**
   - Click country rankings
   - Use dropdown selectors
   - Hover on visualizations

---

## Adding to Your CV/Portfolio

Add this to your portfolio website or CV:

```markdown
### IKEA Global Pricing Dashboard
- **Live Demo**: [View Dashboard](https://share.streamlit.io/batakers/IKEA-Global-Pricing-/main/dashboard/app.py)
- **Technologies**: Python, Streamlit, Plotly, Pandas
- **Features**: 41-country analysis, price indexing, affordability metrics
```

Or add as a button:
```
🔗 [Live Dashboard](https://share.streamlit.io/batakers/IKEA-Global-Pricing-/main/dashboard/app.py)
```

---

## Troubleshooting

### Dashboard doesn't load
- Check that `data/` folder is included in GitHub
- Verify `dashboard/app.py` path is correct
- Check requirements.txt includes all dependencies

### Data is missing
- Ensure `data/*.csv` files are in your GitHub repo
- The dashboard needs: country_metrics.csv and processed_catalog.csv
- Run pipeline locally before deploying

### Slow loading
- Streamlit caches data automatically
- First load takes ~10-15 seconds
- Subsequent loads are instant

---

## Auto-Deployment

Once deployed:
- Every `git push` to main branch triggers auto-deployment
- Changes live in 2-3 minutes
- No manual redeploy needed

Perfect for showing recruiters live, updated work! 🚀

---

## REST API Option

To also deploy the FastAPI backend:

### Using Railway.app (Free tier with credit)
```
1. Go to https://railway.app
2. Connect GitHub
3. Create new project from repository
4. Add variables:
   - PORT=8000
5. Start command: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Your API will be at: `https://your-project.railway.dev/docs`

---

**Recommendation**: Start with Streamlit Community Cloud (1-2 minutes) → Then consider API deployment if needed.
