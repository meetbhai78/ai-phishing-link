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

### ✅ Phase 7 (Completed)
- **Week 10: v4.0 Community Features + Final Integration & Review-2 Preparation**
  - [x] Added Community Phishing Report system with 5 AI training questions (skippable).
  - [x] Added Threat Intelligence Feed screen in Flutter app.
  - [x] Added Report Phishing screen with interactive question cards.
  - [x] Upgraded to 4-tab navigation (Scanner, QR, Report, Threat Feed).
  - [x] Added Scan History in browser extension (chrome.storage.local).
  - [x] Premium glassmorphism UI upgrade for extension (v4.0).
  - [x] Expanded integration test suite from 11 → 22 tests (complete regression).
  - [x] ML Model validation with 5-fold cross-validation, feature importance analysis.
  - [x] Created ML_VALIDATION_REPORT.md with scientific analysis.
  - [x] Created REVIEW2_VIVA_GUIDE.md (32+ Q&A for viva preparation).
  - [x] Created WEEK10_EVIDENCE_GUIDE.md (20 screenshots checklist).
  - [x] Created professional README.md for project.
  - [x] Project structure cleanup and .gitignore update.

### 📋 Phase 8 (In Progress)
- **Week 11: Review-2 Deliverables Preparation (21/09/2026 – 27/09/2026)**
  - [ ] Compile Review-2 Presentation Master PPT (16 slides flow).
  - [ ] Compile Review-2 Technical Report draft with architecture & UML diagrams.
  - [ ] Structure 5-minute Live Demo script for 5-member team.
  - [ ] Weekly report logbook entry for mentor review.

### 🔒 Phase 9 (Upcoming)
- **Week 12: Final Project Freeze & Review-2 Rehearsal (28/09/2026 – 04/10/2026)**
  - [ ] **28 Sep:** Final Project Freeze 🔒 (Zero new features, 22/22 regression verified).
  - [ ] **29 Sep:** Final Report Editing & Proofreading.
  - [ ] **30 Sep:** Evidence/ Folder 16-screenshot collection and formatting.
  - [ ] **01 Oct:** Final PPT polish and slide timing rehearsal.
  - [ ] **02 Oct:** Viva Q&A practice (32 questions revision).
  - [ ] **03 Oct:** Complete End-to-End Live Demo Rehearsal (Backend -> Ext -> Mobile -> QR -> DB).
  - [ ] **04 Oct:** Final project backup, clean zip, and Git tag release.
  - [ ] **05–11 Oct:** 🎯 **CHARUSAT Review-2 Presentation Day!**

---

**Instructions for any AI reading this:**
When assisting the user, first check the **Progress Tracker** above to understand the current state. Always follow the **Constraints & Guidelines** strictly. Do not rush to future weeks; execute the plan step-by-step as requested by the user.

