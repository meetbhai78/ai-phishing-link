# 🛡️ CyberShield — AI-Based Real-Time Phishing Detection System

> Multi-platform phishing detection ecosystem powered by Machine Learning, Web Content Analysis, SSL Inspection, and Community Intelligence.

**Version:** 4.0.0 | **University:** CHARUSAT | **Semester:** 7th

---

## 🎯 Overview

CyberShield is an end-to-end AI-powered phishing detection system that protects users across **Browser Extension**, **Mobile App**, and **Admin Dashboard** — all powered by a custom-trained Random Forest ML model with 30 URL-based features.

### Key Features
- 🤖 **30-Feature ML Model** — Random Forest Classifier trained on 100K+ URLs
- 🌐 **Browser Extension** — Chrome/Edge auto-scan with real-time badges & notifications
- 📱 **Flutter Mobile App** — URL scanning + QR code scanning
- 🔒 **SSL Inspector** — Socket-level certificate validation
- 🕷️ **Content Robot** — Web scraping for password fields, brand impersonation
- 📊 **Threat Intelligence Dashboard** — Real-time analytics & charts
- 🚨 **Community Phishing Reports** — Crowdsourced threat intelligence with AI training questions
- 🏷️ **6 Threat Categories** — Banking, Social Media, E-Commerce, Lottery, Account Takeover, Generic
- ✅ **Whitelist/Blacklist** — Custom domain policy enforcement
- 🗄️ **Dual Database** — MongoDB Atlas (cloud) + SQLite (local fallback)

---

## 🏗️ System Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Browser    │    │  Flutter     │    │  Dashboard   │
│  Extension   │    │  Mobile App  │    │   (Web UI)   │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │   FastAPI   │
                    │  Backend    │
                    │  (v4.0.0)   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
      ┌───────▼──┐  ┌──────▼─────┐  ┌──▼────────┐
      │ ML Model │  │  Content   │  │   SSL      │
      │(30 feat) │  │  Robot     │  │ Inspector  │
      └──────────┘  └────────────┘  └───────────┘
                           │
              ┌────────────┼────────────┐
              │                         │
      ┌───────▼──────┐      ┌──────────▼──┐
      │ MongoDB Atlas│      │   SQLite    │
      │   (Cloud)    │      │  (Fallback) │
      └──────────────┘      └─────────────┘
```

---

## 📁 Project Structure

```
CyberShield/
├── backend/                    # FastAPI Backend
│   ├── main.py                 # API endpoints & hybrid detection pipeline
│   ├── database.py             # MongoDB + SQLite dual database layer
│   ├── content_analyzer.py     # Web scraping robot
│   ├── ssl_inspector.py        # SSL certificate inspector
│   ├── metrics.py              # ML performance evaluator
│   ├── test_integration.py     # 22 automated tests
│   └── requirements.txt
├── popup/                      # Browser Extension
│   ├── popup.html
│   ├── popup.css
│   └── popup.js
├── background/
│   └── background.js           # Auto-Shield service worker
├── dashboard/                  # Threat Intelligence Dashboard
│   ├── index.html
│   ├── dashboard.css
│   └── dashboard.js
├── ml_model/                   # Machine Learning
│   ├── train_model.py          # Model training script
│   ├── feature_extraction.py   # 30-feature extractor
│   ├── ml_validation_report.py # Cross-validation & analysis
│   └── archive/                # Dataset (gitignored)
├── mobile_app/                 # Flutter App
│   └── lib/
│       ├── main.dart
│       ├── screens/
│       │   ├── home_screen.dart
│       │   ├── qr_scan_screen.dart
│       │   ├── report_phishing_screen.dart
│       │   └── threat_feed_screen.dart
│       └── services/
│           └── api_service.dart
├── icons/                      # Extension icons
├── manifest.json               # Chrome Manifest V3
├── PROJECT_ROADMAP.md
├── PROJECT_FINAL_REPORT.md
├── ML_VALIDATION_REPORT.md
├── REVIEW2_VIVA_GUIDE.md
└── README.md
```

---

## 🚀 Quick Start

### 1. Backend Setup
```bash
# Create virtual environment
cd ml_model
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# Install dependencies
pip install fastapi uvicorn scikit-learn pandas numpy joblib python-dotenv pymongo

# Start server
cd ..
uvicorn backend.main:app --reload
```

### 2. Browser Extension
1. Open `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked" → Select project root folder
4. Extension icon appears in toolbar

### 3. Flutter Mobile App
```bash
cd mobile_app
flutter pub get
flutter run
```

### 4. Dashboard
Open `http://127.0.0.1:8000/dashboard` in browser.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check & system info |
| `POST` | `/predict` | Scan URL (hybrid AI pipeline) |
| `GET` | `/dashboard` | Threat Intelligence Dashboard |
| `GET` | `/api/stats` | Real-time scan statistics |
| `GET` | `/api/scans` | Recent scan history |
| `GET/POST` | `/api/rules` | Whitelist/Blacklist management |
| `GET` | `/api/metrics` | ML model performance metrics |
| `POST` | `/api/batch-scan` | Enterprise batch URL scanner |
| `GET/POST` | `/api/feedback` | User false-positive reports |
| `GET` | `/api/community-questions` | AI training questions |
| `POST` | `/api/community-report` | Submit community phishing report |
| `GET` | `/api/community-reports` | Recent community reports |
| `GET` | `/api/community-stats` | Community contribution statistics |

---

## 🧪 Testing

```bash
# Run all 22 integration tests
python backend/test_integration.py

# Generate ML validation report
python ml_model/ml_validation_report.py
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| ML Model | Python, Scikit-learn (Random Forest, 300 trees) |
| Backend | FastAPI, Uvicorn |
| Extension | HTML, CSS, JS, Chrome Manifest V3 |
| Mobile App | Flutter, Dart |
| Database | MongoDB Atlas + SQLite |
| Dashboard | HTML, CSS, JavaScript, Chart.js |

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | ~95% |
| Precision | ~90% |
| Recall | ~96% |
| F1-Score | ~93% |
| ROC-AUC | ~98% |

*Validated via 5-fold stratified cross-validation*

---

## 👥 Team

**CHARUSAT University** — 7th Semester Engineering Project (5 members)

---

*CyberShield v4.0 — AI-Based Real-Time Phishing Detection System*
