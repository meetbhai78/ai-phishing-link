# CyberShield v4.0 — Week 10 Screenshot Evidence Guide

**Purpose:** Systematically capture 20 screenshots for Review-2, Final Report, and Viva.

> **Tip:** Save all screenshots in a `screenshots/` folder with numbered filenames.

---

## Pre-requisites
1. Start FastAPI server: `uvicorn backend.main:app --reload`
2. Load Chrome extension (chrome://extensions → Load Unpacked)
3. Keep MongoDB Atlas connected (check terminal logs)

---

## 📸 Screenshot Checklist

### A. Browser Extension Screenshots

| # | Screenshot | How to Capture |
|---|-----------|---------------|
| 1 | **Extension SAFE Result** | Open `https://www.google.com` → Click extension icon → Click "Scan URL" → Take screenshot showing ✅ SAFE with green status |
| 2 | **Extension PHISHING Result** | Enter `http://192.168.1.1/paypal/login-verify` in address bar → Scan → Take screenshot showing ⚠️ DANGER with red status |
| 3 | **Auto-Shield Badge** | Navigate to any safe URL → Notice "OK" green badge on extension icon. Navigate to phishing URL → Notice "!" red badge |
| 4 | **SSL Inspector Card** | Scan `https://www.google.com` → Scroll to SSL section showing "Valid & Trusted", issuer, days remaining |
| 5 | **Robot Webpage Analysis** | Scan any URL → Show Robot inspection card with password field check, external action, brand check |
| 6 | **30-Feature Analysis Table** | After scan → Scroll down to "URL Analysis (30 Features)" table showing all extracted features |
| 7 | **Report Suspicious Link Form** | Click "🚨 Report Suspicious Link" → Show the expanded form with URL input, label chips (Phishing/Safe/Unsure), and question cards |
| 8 | **Scan History** | After 2-3 scans → Show "Recent Scans" section with colored SAFE/RISK badges |

### B. Mobile App Screenshots

| # | Screenshot | How to Capture |
|---|-----------|---------------|
| 9 | **App SAFE Scan** | Open Flutter app → Enter `https://www.google.com` → Tap "SCAN" → Screenshot of green SAFE result card |
| 10 | **App PHISHING Scan** | Enter phishing URL → Scan → Screenshot of red PHISHING result with threat category |
| 11 | **QR Scanner** | Go to QR tab → Scan a QR code → Show scan result |
| 12 | **Report Phishing Screen** | Go to Report tab → Show form with URL input, label chips, and AI training questions |
| 13 | **Threat Feed Screen** | Go to Threat Feed tab → Show community stats and recent reports list |

### C. Dashboard & API Screenshots

| # | Screenshot | How to Capture |
|---|-----------|---------------|
| 14 | **Dashboard Overview** | Open `http://127.0.0.1:8000/dashboard` → Full screenshot with stats and charts |
| 15 | **Swagger API Docs** | Open `http://127.0.0.1:8000/docs` → Show all available endpoints |
| 16 | **ML Metrics API** | Open `http://127.0.0.1:8000/api/metrics` in browser → Show accuracy, precision, recall, F1, confusion matrix |

### D. Database & Backend Screenshots

| # | Screenshot | How to Capture |
|---|-----------|---------------|
| 17 | **MongoDB Atlas Data** | Login to MongoDB Atlas → Navigate to `cybershield_db` → `scan_logs` collection → Show actual documents |
| 18 | **Terminal — Server Running** | Show terminal with FastAPI startup logs: "ML Model loaded", "MongoDB Connected", "Uvicorn running" |

### E. Testing Screenshots

| # | Screenshot | How to Capture |
|---|-----------|---------------|
| 19 | **Test Suite Results** | Run `python backend/test_integration.py` → Screenshot of terminal showing 22/22 PASSED |
| 20 | **ML Validation Report** | Open `ML_VALIDATION_REPORT.md` → Screenshot showing metrics, confusion matrix, cross-validation |

---

## 📁 Suggested File Naming

```
screenshots/
├── 01_extension_safe.png
├── 02_extension_phishing.png
├── 03_auto_shield_badge.png
├── 04_ssl_inspector.png
├── 05_robot_analysis.png
├── 06_30_features_table.png
├── 07_report_form.png
├── 08_scan_history.png
├── 09_app_safe.png
├── 10_app_phishing.png
├── 11_qr_scanner.png
├── 12_report_screen.png
├── 13_threat_feed.png
├── 14_dashboard.png
├── 15_swagger_docs.png
├── 16_ml_metrics.png
├── 17_mongodb_atlas.png
├── 18_terminal_server.png
├── 19_test_results.png
└── 20_ml_validation.png
```

---

*CyberShield v4.0 — Week 10 Evidence Collection Guide*
