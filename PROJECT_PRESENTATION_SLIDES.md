# CyberShield: Presentation & Viva Slides Deck (Week 8)
## 7th Semester B.Tech Project Presentation Outline

---

### **Slide 1: Title Slide**
* **Project Name:** CyberShield: AI-Based Real-Time Phishing Detection & Threat Intelligence System
* **Department:** Department of Computer Science & Engineering, CHARUSAT University
* **Team Members:** [Team of 5 Members]
* **Project Guide:** [Faculty Guide Name]
* **Tech Stack:** Python, FastAPI, Scikit-Learn, Flutter, Manifest V3 JS, MongoDB Atlas

---

### **Slide 2: Problem Statement & Motivation**
* **Cybersecurity Threat:** Phishing accounts for 90%+ of all social engineering data breaches worldwide.
* **Limitations of Existing Tools:**
  * Static blacklists cannot stop zero-hour (freshly hosted) phishing domains.
  * Commercial AI APIs (OpenAI/Gemini) introduce privacy concerns, subscription costs, and API latency.
  * QR Code phishing (Quishing) targets mobile users where URL inspection is difficult.
* **Our Solution:** CyberShield — A unified, localized, multi-platform ecosystem with real-time AI classification and deep content inspection.

---

### **Slide 3: System Architecture & Workflow**
* **Multi-Platform Ecosystem:**
  * **Browser Extension (Manifest V3):** Passive & active monitoring of web browsing tabs.
  * **Flutter Mobile Application:** URL and QR code scanner with camera capture and instant risk scoring.
  * **FastAPI Backend Engine:** Microservice handling ML inference, scraping bots, and SSL inspection.
  * **MongoDB Atlas + SQLite:** Cloud telemetry logging and offline resilience.
  * **Threat Intelligence Dashboard:** Live glassmorphism web console for network-wide telemetry.

---

### **Slide 4: AI & Feature Engineering (30 Lexical Features)**
* **Model Type:** Random Forest Classifier (100 Decision Trees trained locally on Kaggle malicious dataset).
* **30 Extracted Feature Dimensions:**
  * **Lexical & Length:** URL length, domain length, path length, query parameter length.
  * **Protocol & Delimiters:** HTTPS vs HTTP flags, dot count, hyphen count, slash count, digit-to-letter ratio.
  * **Structural & Security Anomalies:** IP address hosting, `@` symbol credential theft, double slash redirections, subdomain nesting.
  * **Heuristics & Entropy:** Shannon Entropy (detects algorithmic domain generation/DGA), brand hijacking in subdomains, suspicious TLDs (`.xyz`, `.top`, `.tk`), URL shortener detection (`bit.ly`, `tinyurl`).

---

### **Slide 5: Hybrid Cascading Detection Pipeline**
* **Multi-Layer Defense:**
  1. **Trusted Whitelist Filter:** Immediate 100% verification for verified domains (`.gov.in`, `.edu.in`, banking portals).
  2. **Custom Domain Policy:** Blacklist / Whitelist rules defined by network administrators.
  3. **Machine Learning Model Inference:** Random forest probability score.
  4. **Content Scraping Robot:** Validates page titles, catches unauthorized password forms, and flags brand mismatches.
  5. **Native SSL Inspector:** Live socket handshake verifying certificate validity, issuer authority, and expiration timeline.

---

### **Slide 6: Automated Threat Classification Categories**
* Phishing attacks are categorized in real-time into targeted danger types:
  * 🏦 **Banking & Financial Phishing:** KYC updates, OTP requests, banking domain spoofing.
  * 📱 **Social Media & Email Credential Phishing:** Fake login portals (Google, Instagram, Microsoft).
  * 🛒 **E-Commerce & Delivery Scams:** Fake courier delivery, payment gateways.
  * 🎁 **Lottery, Crypto & Reward Scams:** Free claims, prizes, fake token airdrops.
  * 🛡️ **Generic Phishing Pattern:** Suspicious TLDs, IP hosting, structural anomalies.

---

### **Slide 7: Verification & Testing Results**
* Automated Unit & Integration Test Suite (`backend/test_integration.py`):
  * **11 Out of 11 Test Suites Passed (100% Success Rate)**
  * Verified model accuracy, endpoint responses, MongoDB dual-logging, SSL verification, and client tagging.
* **Cross-Platform Readiness:**
  * Extension tested on Google Chrome / Microsoft Edge.
  * Mobile UI verified for camera QR scanning and manual text input.
  * Web Dashboard rendering live analytics at `http://127.0.0.1:8000/dashboard`.

---

### **Slide 8: Key Highlights & Innovation**
* **100% Independent AI:** No third-party AI APIs (OpenAI/Claude) used — zero recurring costs and complete data sovereignty.
* **Zero False Positives on Verified Services:** Multi-layer trusted whitelist safeguards government and verified institutions.
* **Dual Database Sync:** Seamless failover between MongoDB Atlas Cloud and Local SQLite.
* **Multi-Device Unified Telemetry:** One backend protecting browser tabs, mobile QR codes, and dashboard admins.

---

### **Slide 9: Live Demo Script (Step-by-Step for Viva)**
1. **Demo 1 (FastAPI Server & Docs):** Start `run_server.bat` → Show Swagger UI at `http://127.0.0.1:8000/docs`.
2. **Demo 2 (Threat Dashboard):** Open `http://127.0.0.1:8000/dashboard` → Show real-time telemetry, charts, and test scanner.
3. **Demo 3 (Chrome Extension):** Open a safe site (`charusat.ac.in`) → Show green SAFE badge. Open a test phishing link (`http://192.168.1.1/paypal/login`) → Show red DANGER overlay with 30 features breakdown.
4. **Demo 4 (Mobile App & QR):** Scan `phishing_qr.png` and `safe_qr.png` in Flutter app → Show real-time threat categorization.
5. **Demo 5 (MongoDB Atlas):** Refresh MongoDB Atlas collection to show live logs from all 3 clients.

---

### **Slide 10: Conclusion & Q&A**
* **Project Milestone:** All 8 Weeks of the project roadmap completed successfully.
* **Thank You!** Questions & Feedback from the Examiners.
