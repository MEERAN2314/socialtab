# Deployment Guide - Render.com

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **MongoDB Atlas Account** - Free tier at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)

## Step 1: Setup MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account or login
3. Click "Build a Database"
4. Choose "FREE" tier (M0 Sandbox)
5. Select a cloud provider and region (choose closest to your users)
6. Click "Create Cluster"
7. Wait for cluster to be created (2-3 minutes)

### Configure Database Access

1. Click "Database Access" in left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create username and password (save these!)
5. Set "Database User Privileges" to "Read and write to any database"
6. Click "Add User"

### Configure Network Access

1. Click "Network Access" in left sidebar
2. Click "Add IP Address"
3. Click "Allow Access from Anywhere" (0.0.0.0/0)
4. Click "Confirm"

### Get Connection String

1. Click "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Copy the connection string
5. Replace `<password>` with your database user password
6. Replace `<dbname>` with `socialtab`

Example:
```
mongodb+srv://myuser:mypassword@cluster0.xxxxx.mongodb.net/socialtab?retryWrites=true&w=majority
```

## Step 2: Push Code to GitHub

1. Initialize git repository (if not already):
```bash
git init
git add .
git commit -m "Initial commit - SocialTab"
```

2. Create a new repository on GitHub

3. Push your code:
```bash
git remote add origin https://github.com/yourusername/socialtab.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click "Apply"

### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: socialtab
   - **Region**: Choose closest to you
   - **Branch**: main
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

## Step 4: Configure Environment Variables

1. In your Render service dashboard, go to "Environment"
2. Add the following environment variables:

| Key | Value |
|-----|-------|
| `MONGODB_URL` | Your MongoDB Atlas connection string |
| `SECRET_KEY` | Generate a random 32+ character string |
| `ALGORITHM` | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 10080 |

### Generate SECRET_KEY

Run this in your terminal:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Or use this online: [randomkeygen.com](https://randomkeygen.com/)

3. Click "Save Changes"

## Step 5: Deploy

1. Render will automatically deploy your app
2. Wait for build to complete (3-5 minutes)
3. Once deployed, you'll get a URL like: `https://socialtab.onrender.com`
4. Click the URL to open your app!

## Step 6: Test Your Deployment

1. Open your Render URL
2. Click "Sign Up"
3. Create a test account
4. Try creating a debt
5. Test all features

## Troubleshooting

### Build Fails

**Check logs in Render dashboard:**
- Go to "Logs" tab
- Look for error messages
- Common issues:
  - Missing dependencies in `requirements.txt`
  - Python version mismatch
  - Syntax errors

**Solution:**
```bash
# Test locally first
pip install -r requirements.txt
python main.py
```

### App Crashes on Start

**Check environment variables:**
- Ensure `MONGODB_URL` is correct
- Ensure `SECRET_KEY` is set
- Check MongoDB Atlas IP whitelist (should be 0.0.0.0/0)

**Check logs:**
```
# In Render dashboard, go to Logs tab
# Look for connection errors
```

### Database Connection Issues

**Verify MongoDB Atlas:**
1. Check cluster is running
2. Check database user exists
3. Check network access allows 0.0.0.0/0
4. Test connection string locally:
```bash
# In your .env file, use the same connection string
python main.py
```

### Static Files Not Loading

**Check CORS settings:**
- Render URL should be allowed in CORS
- Check browser console for errors

**Solution:**
Update `main.py` CORS settings if needed:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://socialtab.onrender.com"],  # Your Render URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### App Sleeps (Free Tier)

Render free tier apps sleep after 15 minutes of inactivity.

**Solutions:**
1. Upgrade to paid plan ($7/month)
2. Use a service like [UptimeRobot](https://uptimerobot.com/) to ping your app every 5 minutes
3. Accept the sleep behavior (first request after sleep takes 30-60 seconds)

## Performance Tips

### 1. Enable Caching
Add Redis for session caching (requires paid plan)

### 2. Optimize Database Queries
- Add indexes in MongoDB Atlas
- Use projection to limit returned fields

### 3. Use CDN for Static Files
- Upload static files to Cloudflare or AWS S3
- Update static file URLs

### 4. Monitor Performance
- Use Render metrics dashboard
- Set up alerts for downtime
- Monitor MongoDB Atlas metrics

## Custom Domain (Optional)

1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Render dashboard, go to "Settings"
3. Click "Add Custom Domain"
4. Follow DNS configuration instructions
5. Wait for SSL certificate (automatic, 5-10 minutes)

## Updating Your App

### Automatic Deployment

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will detect the push and redeploy automatically.

### Manual Deployment

1. Go to Render dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

## Monitoring

### View Logs

1. Go to Render dashboard
2. Click "Logs" tab
3. See real-time logs

### View Metrics

1. Go to Render dashboard
2. Click "Metrics" tab
3. See CPU, Memory, Request metrics

## Backup Strategy

### Database Backups

MongoDB Atlas automatically backs up your data:
1. Go to MongoDB Atlas dashboard
2. Click "Backup" tab
3. Configure backup schedule
4. Free tier: Limited backups

### Code Backups

Your code is backed up on GitHub:
- Push regularly
- Use branches for features
- Tag releases

## Security Checklist

- [ ] Strong SECRET_KEY (32+ characters)
- [ ] MongoDB user has strong password
- [ ] Environment variables not in code
- [ ] HTTPS enabled (automatic on Render)
- [ ] CORS configured properly
- [ ] Rate limiting enabled (optional)
- [ ] Input validation working
- [ ] Error messages don't leak sensitive info

## Cost Breakdown

### Free Tier
- **Render**: Free (with limitations)
- **MongoDB Atlas**: Free (512MB storage)
- **Total**: $0/month

### Limitations:
- App sleeps after 15 min inactivity
- 750 hours/month (enough for 1 app)
- Limited bandwidth
- Limited database storage

### Paid Tier (Recommended for Production)
- **Render Starter**: $7/month
- **MongoDB Atlas M10**: $0.08/hour (~$57/month)
- **Total**: ~$64/month

### Benefits:
- No sleeping
- Better performance
- More storage
- Better support

## Support

### Render Support
- [Render Docs](https://render.com/docs)
- [Render Community](https://community.render.com/)
- Email: support@render.com

### MongoDB Support
- [MongoDB Docs](https://docs.mongodb.com/)
- [MongoDB Community](https://www.mongodb.com/community/forums/)

## Next Steps

1. ✅ Deploy to Render
2. ✅ Test all features
3. 📱 Share with judges
4. 🎉 Win HackForge'25!

---

**Good luck with your hackathon! 💚**
