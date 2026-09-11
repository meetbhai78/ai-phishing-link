# CyberShield: Complete Project Screenshots & Evaluation Guide (Week 9)
## All Screenshots Required for Project Report, PPT & University Viva

Follow this checklist to take high-quality screenshots (`Windows Key + Shift + S`) for your final project report and evaluation.

---

### 📸 Screenshot Checklist & Where to Take Each One:

| # | Feature / Screen | Where to Open | What to Capture |
| :---: | :--- | :--- | :--- |
| **1** | **Live Threat Dashboard & Telemetry** | [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard) | Top stats cards (Total Scans, Phishing Blocked, Safe Sites) + Live Activity & Doughnut Charts. |
| **2** | **🧠 ML Performance & Confusion Matrix (New!)** | [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard) | Accuracy (95.1%), Precision (90.5%), Recall (96.3%), F1-Score, ROC-AUC + Confusion Matrix Breakdown (TN, FP, FN, TP). |
| **3** | **⚡ Enterprise Batch URL Scanner (New!)** | [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard) | Paste 3-4 URLs in Batch Scanner, click "Run Batch Threat Scan" and capture the multi-URL instant verdict output. |
| **4** | **📢 User False-Positive / Threat Feedback (New!)** | [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard) | Report Form with URL input, False-Positive dropdown selection, comment, and green submission confirmation. |
| **5** | **🛡️ Custom Policy Whitelist / Blacklist Manager** | [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard) | Domain rule input field (`⛔ Blacklist` / `✅ Whitelist`) + Active rules list table. |
| **6** | **📥 1-Click CSV Threat Telemetry Export** | [http://127.0.0.1:8000/dashboard](http://127.0.0.1:8000/dashboard) | Click "📥 Download CSV" button + show the downloaded `.csv` report opened in Excel/Notepad. |
| **7** | **🔒 SSL Certificate Inspector (Browser Extension)** | Chrome Extension Popup on `https://google.com` | Blue SSL card showing Valid SSL (HTTPS), Issuer Org (Google Trust Services), and Expiry Days. |
| **8** | **⚠️ Phishing Detection Overlay (Browser Extension)** | Chrome Extension Popup on `http://192.168.1.1/paypal/login` | Red DANGER popup with Banking Threat Category & 30-Feature Lexical breakdown table. |
| **9** | **📱 Mobile App URL & QR Code Scanner** | Flutter App or [qr_test.html](file:///d:/5TH%20SEM/extention/qr_test.html) | Mobile UI scanning `phishing_qr.png` / `safe_qr.png` showing instant risk verdict. |
| **10** | **🧪 11/11 Automated Test Suite Passed in Terminal** | Command Prompt (`cmd.exe`) | Run `"D:\5TH SEM\extention\ml_model\venv\Scripts\python.exe" backend/test_integration.py` → Capture `Ran 11 tests ... OK`. |
| **11** | **⚡ Swagger Interactive API Documentation** | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) | Fast, interactive API endpoints (`/predict`, `/api/metrics`, `/api/batch-scan`, `/api/feedback`, `/api/rules`). |
| **12** | **☁️ MongoDB Atlas Cloud Database Telemetry** | [MongoDB Atlas Web Console](https://cloud.mongodb.com/) | Live `cybershield_db.scan_logs` showing scan telemetry stored in the cloud. |

---

### 🚀 How to Launch the System for Screenshots:

Double-click **`run_server.bat`** or run in CMD:
```cmd
D:
cd "D:\5TH SEM\extention"
"D:\5TH SEM\extention\ml_model\venv\Scripts\python.exe" -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
Open **`http://127.0.0.1:8000/dashboard`** in Chrome to capture all dashboard features!
