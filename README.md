# Deploying Redhunllef Leaderboard on DigitalOcean App Platform

## **Steps to Deploy**

### **1. Prepare Your Project**
1. Clone or copy the project files into your directory.
2. Ensure these critical files are present:
   - `main.py` (Flask backend)
   - `shuffle_api.py`, `chicken_api.py` (API integration)
   - `requirements.txt`, `Procfile`, `runtime.txt` (Deployment configs)
   - Static files (`style.css`, images) and templates (`shuffle.html`, `chicken.html`, `404.html`).

---

### **2. Install Dependencies**
#### Option 1: Install via `requirements.txt`
Run this command in your project directory:
```bash
pip install -r requirements.txt
```

#### Option 2: Install Dependencies Manually
Use the following commands to install dependencies individually:
```bash
pip install Flask
pip install Flask-CORS
pip install requests
```

---

### **3. Push to GitHub**
1. Initialize Git and commit the project:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Redhunllef Leaderboard"
   ```
2. Push the project to a GitHub repository:
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git branch -M main
   git push -u origin main
   ```

---

### **4. Deploy on DigitalOcean**
1. Log in to **DigitalOcean** and go to **App Platform**.
2. Click **"Create App"**, link your GitHub repository, and select the branch (e.g., `main`).
3. Configure the app:
   - **Run Command**: `python main.py`
   - Add API keys as environment variables:
     - `SHUFFLE_API_KEY`: Shuffle.com API key.
     - `CHICKEN_API_KEY`: Chicken.gg API key.
4. Click **"Create Resources"** to deploy.

---

### **5. Verify and Test**
- Visit the provided app URL and test:
  - `/shuffle`: Displays the Shuffle.com leaderboard.
  - `/chicken`: Displays the Chicken.gg leaderboard.
- Check logs in the DigitalOcean App Platform or the local `logs/app.log` file for debugging.

---

## **For Updates**
1. Make changes locally, commit, and push:
   ```bash
   git add .
   git commit -m "Update leaderboard functionality"
   git push
   ```
2. DigitalOcean will automatically redeploy your app.