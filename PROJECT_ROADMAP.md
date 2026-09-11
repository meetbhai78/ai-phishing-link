# CyberShield: AI-Based Real-Time Phishing Detection System
**Project Context Document for AI Assistants**

**Student Project Context:**
This is a 7th-semester engineering project for CHARUSAT University. The team consists of 5 members. The goal is to build an end-to-end Machine Learning based phishing detection ecosystem from scratch without relying on external commercial AI APIs (like OpenAI or Gemini).

---

## 1. System Architecture & Tech Stack
The project is a multi-platform security solution composed of:
1.  **AI Machine Learning Model (Python, Scikit-Learn):** A custom-trained Random Forest Classifier that predicts if a URL is phishing or safe based on URL characteristics.
2.  **Prediction API Backend (Python, FastAPI):** Acts as the bridge. It receives URLs from clients, runs them through the ML model, and returns a risk score/confidence level.
3.  **Browser Extension (HTML, CSS, JS, Manifest V3):** A Chrome/Edge extension that reads the current active tab's URL and displays warning popups if the Prediction API flags it as phishing.
4.  **Android App (Flutter):** A mobile app capable of scanning URLs and QR codes for phishing threats.
5.  **Database (MongoDB Atlas):** Stores scan history, threat statistics, and recent scans.

**Important Constraints & Guidelines:**
*   **NO Third-Party AI APIs:** Do NOT use OpenAI, Gemini, or Claude. The ML model MUST be built and trained locally.
*   **From Scratch:** Do not provide copy-paste boilerplate from other repos. Build file-by-file.
*   **Out of Scope (MVP):** Do NOT implement Login systems, OTP, Payment gateways, Chat systems, AI screenshot analysis, or Email inbox integrations. Keep it strictly focused on URL/QR phishing detection.

---

## 2. Progress Tracker (8-Week Roadmap)

### ✅ Phase 1 (Completed)
- **Week 1: Planning & Research**
  - [x] Finalized title, objectives, and scope.
  - [x] SRS, System Architecture, and Workflow designed.
  - [x] Project Proposal (Synopsis) submitted.
  - [x] OWASP phishing guidelines study.

- **Week 2: Browser Extension Basics**
  - [x] Setup `manifest.json` (Manifest V3) with `activeTab` permissions.
  - [x] Created `popup.html` and `popup.css` for a premium UI.
  - [x] Implemented `popup.js` to extract current tab URL.
  - [x] Added `background.js` service worker boilerplate.

### 🚧 Phase 2 (Pending)
- **Week 3: AI Model Basics**
  - [x] Set up Python environment.
  - [x] Gather & preprocess phishing and legitimate URL datasets (e.g., from Kaggle).
  - [x] Extract features (Length, HTTPS, Dots, IP presence, special chars).
  - [x] Train the Random Forest Classifier.
  - [x] Test model accuracy and save as `.pkl`.

- **Week 4: Backend API Integration**
  - [x] Set up FastAPI backend.
  - [x] Load the `.pkl` ML model into the API.
  - [x] Expose an endpoint (e.g., `/predict`) receiving JSON URLs.
  - [x] Connect the Browser Extension (`popup.js`) to call this API via `fetch()`.

### ✅ Phase 3 (Completed)
- **Week 5: Content Detection & Android App Setup**
  - [x] Implement Content-Based Detection (Web Scraping bot for page titles, password forms, brand mismatches) in FastAPI.
  - [x] Initialize Flutter project inside `mobile_app`.
  - [x] Create UI for URL scanning and QR code scanning.
  - [x] Connect mobile app to the FastAPI backend (`api_service.dart`).



### ✅ Phase 4 (Completed)
- **Week 6: Database & Dashboard**
  - [x] Setup MongoDB Atlas connection with local dual-mode fallback.
  - [x] Modify FastAPI to log all scans (URL, result, confidence, date, client type).
  - [x] Build CyberShield Threat Intelligence Dashboard interface with real-time analytics & charts.

- **Week 7: Integration & Refinement**
  - [x] End-to-end integration testing (Extension + App + API + DB).
  - [x] Bug fixing and UI/UX improvements.
  - [x] Automated test suite created (`backend/test_integration.py`).
  - [x] Client type tracking integrated (`extension` & `mobile_app`).

### ✅ Phase 5 (Completed)
- **Week 8: Final Delivery**
  - [x] Final project testing (11/11 automated tests passed).
  - [x] Prepared Project Report (`PROJECT_FINAL_REPORT.md`) and Presentation Slides (`PROJECT_PRESENTATION_SLIDES.md`).
  - [x] Final Demo readiness & Viva Guide created (`FINAL_DEMO_GUIDE.md`).

### ✅ Phase 6 (Completed)
- **Week 9: Scientific ML Performance Evaluation & Advanced Features**
  - [x] Added Scientific ML Evaluation Module (`backend/metrics.py`) with Confusion Matrix & ROC-AUC.
  - [x] Added Enterprise Batch URL Scanner (`/api/batch-scan`).
  - [x] Added User Threat Feedback & False-Positive Reporting (`/api/feedback` with MongoDB/SQLite logging).
  - [x] Enhanced Live Threat Dashboard with real-time model evaluation, batch hunting console, and reporting.

---

**Instructions for any AI reading this:**
When assisting the user, first check the **Progress Tracker** above to understand the current state. Always follow the **Constraints & Guidelines** strictly. Do not rush to future weeks; execute the plan step-by-step as requested by the user.
