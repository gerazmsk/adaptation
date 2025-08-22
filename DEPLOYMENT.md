# 🚀 Cloud Deployment Guide

## Deploy Your Financial Advisor Bot to the Cloud

This guide will help you deploy your bot to Railway (recommended) or Render so it runs 24/7 without your computer.

## 🎯 **Option 1: Railway (Recommended)**

### **Step 1: Sign Up for Railway**
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Add a credit card for verification ($5/month)

### **Step 2: Deploy from GitHub**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `gerazmsk/usa-adaptation`
4. Railway will automatically detect it's a Python project

### **Step 3: Set Environment Variables**
In Railway dashboard, go to **Variables** tab and add:
```
TELEGRAM_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
```

### **Step 4: Deploy**
1. Click **"Deploy"**
2. Wait for build to complete
3. Your bot will be live at the provided URL

## 🎯 **Option 2: Render (Free Tier)**

### **Step 1: Sign Up for Render**
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. No credit card required for free tier

### **Step 2: Create New Web Service**
1. Click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository: `gerazmsk/usa-adaptation`

### **Step 3: Configure Service**
- **Name**: `financial-advisor-bot`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python3 bot.py`

### **Step 4: Set Environment Variables**
Add these environment variables:
```
TELEGRAM_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
PORT=10000
```

### **Step 5: Deploy**
1. Click **"Create Web Service"**
2. Wait for build and deployment
3. Your bot will be live!

## 🔧 **What Happens After Deployment**

✅ **Bot runs 24/7** - No need to keep your computer on  
✅ **Automatic updates** - When you push to GitHub, bot updates automatically  
✅ **Health monitoring** - Cloud service monitors if bot is running  
✅ **Scalability** - Can handle multiple users simultaneously  

## 📱 **Test Your Deployed Bot**

1. **Wait for deployment** to complete (usually 2-5 minutes)
2. **Go to Telegram** and find your bot
3. **Send `/start`** to test
4. **Ask questions** to verify AI responses

## 🚨 **Important Notes**

- **Keep your API keys secure** - Don't share them publicly
- **Monitor usage** - OpenAI charges per API call
- **Check logs** - Cloud services provide logs for debugging
- **Update regularly** - Push improvements to GitHub

## 🆘 **Troubleshooting**

### **Bot not responding:**
- Check Railway/Render logs
- Verify environment variables are set
- Ensure GitHub repository is connected

### **Build errors:**
- Check `requirements.txt` is correct
- Verify Python version compatibility
- Check for syntax errors in code

## 🎉 **You're Done!**

Once deployed, your bot will run continuously in the cloud, providing financial advice to users 24/7!

**Need help?** Check the logs in your cloud service dashboard or refer to their documentation.
