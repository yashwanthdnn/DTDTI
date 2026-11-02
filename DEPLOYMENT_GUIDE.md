# 🚀 Streamlit Deployment Guide

This guide provides simple, step-by-step instructions to deploy **H&N Punjabi Food Junction – Smart Restaurant Management System** on **Streamlit Community Cloud** (recommended, free) and alternative platforms.

---

## Option 1: Streamlit Community Cloud (Recommended & 100% Free)

Streamlit Community Cloud is the official hosting platform for Streamlit apps. It connects directly to your GitHub repository and automatically deploys your updates whenever you push code.

### Step 1: Push Your Code to GitHub

1. If you haven't initialized Git yet, open PowerShell/Terminal in this project folder (`DTDTI`):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Streamlit deployment"
   ```

2. Create a new public (or private) repository on GitHub:
   - Go to [https://github.com/new](https://github.com/new)
   - Name it (for example: `dtdti-restaurant-system`)
   - Leave "Initialize with README" unchecked

3. Link and push your local code:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/dtdti-restaurant-system.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and click **Sign in with GitHub**.
2. Click the **"New app"** or **"Create app"** button.
3. Fill in the deployment form:
   - **Repository**: `<YOUR_GITHUB_USERNAME>/dtdti-restaurant-system`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py` (or `app.py`)
   - **App URL**: Choose a custom subdomain if available (e.g., `hn-punjabi-food.streamlit.app`)
4. Click **Deploy!**

> ⏱️ Within 1 to 2 minutes, Streamlit will install the dependencies from `requirements.txt` and launch your live application at your custom URL!

---

## Option 2: Run Locally (Windows / macOS / Linux)

### On Windows:
Simply double-click the included `run_app.bat` script, or run in PowerShell:
```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

### On macOS / Linux:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
Open your browser at `http://localhost:8501`.

---

## Option 3: Deploy on Hugging Face Spaces (Alternative Free Host)

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) and click **"Create new Space"**.
2. Choose **Space SDK**: **Streamlit**.
3. Choose **Public** visibility.
4. Clone the Hugging Face repo or push this codebase to it.
5. Hugging Face Spaces automatically reads `requirements.txt` and `streamlit_app.py` and deploys your live app.

---

## Option 4: Deploy with Docker (Render / Cloud Run / Railway / VPS)

The project includes a production-ready `Dockerfile`:

1. Build the Docker image:
   ```bash
   docker build -t hn-punjabi-food .
   ```
2. Run the container:
   ```bash
   docker run -p 8501:8501 hn-punjabi-food
   ```
3. For cloud container services (like Render or Google Cloud Run):
   - Connect your GitHub repo.
   - Choose Docker runtime.
   - Set container port to `8501`.

---

## Key Files Summary for Deployment

| File | Purpose |
| :--- | :--- |
| `streamlit_app.py` | Primary Streamlit application with all 14 modules, RBAC persona switcher & live order pipeline |
| `app.py` | Universal entrypoint wrapper (mirrors `streamlit_app.py` for cloud auto-discovery) |
| `requirements.txt` | Minimal, high-performance Python dependencies (`streamlit`, `pandas`, `plotly`) |
| `.streamlit/config.toml` | Theme tokens (Brand Maroon, Warm Cream, Gold) and headless server configuration |
| `.gitignore` | Prevents cache files, secrets, and `node_modules` from being pushed to Git |
| `Dockerfile` | Containerization configuration for Docker, Render, and Cloud Run |
| `run_app.bat` | 1-click Windows local execution script |
