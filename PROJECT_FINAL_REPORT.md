# CyberShield: AI-Based Real-Time Phishing Detection System
## Final Project Documentation & Engineering Report

---

### **Executive Summary**
* **Project Title:** CyberShield - AI-Powered Multi-Platform Real-Time Phishing Detection & Threat Intelligence Ecosystem
* **Institution:** CHARUSAT University (7th Semester Engineering Project)
* **Team Size:** 5 Members
* **Architecture:** Multi-Platform (Browser Extension + Flutter Mobile App + FastAPI Microservice + Scikit-Learn Local AI + MongoDB Atlas Telemetry)

---

## 1. Problem Statement & Motivation
Phishing attacks remain the #1 attack vector in social engineering and cybercrime worldwide. Traditional blacklist-based defenses fail against zero-hour (newly registered) domains, randomized URLs, URL shorteners, and brand impersonation attacks. 

**CyberShield** addresses these limitations by providing a fully localized, hybrid AI phishing detection ecosystem:
1. **Lexical & Structural URL Feature Extraction (30 Features)** using Machine Learning.
2. **Real-Time Web Scraping & Content Verification Robot** to detect credential theft and brand spoofing.
3. **Deep SSL/TLS Certificate Telemetry Inspection** verifying issuer credibility and certificate expiration.
4. **Dual Database Architecture (MongoDB Atlas Cloud + Local SQLite Fallback)** logging telemetry across all client devices.
5. **No Third-Party AI APIs:** Zero reliance on external paid APIs (OpenAI, Gemini), ensuring complete privacy, zero latency billing, and localized training.

---

## 2. System Architecture & Component Breakdown

```
+-------------------------------------------------------------------------------+
|                            CYBERSHIELD CLIENTS                                |
|  [ Chrome / Edge Extension (Manifest V3) ]    [ Flutter Android / iOS App ]   |
|         - Real-time Active Tab Scan                  - URL & QR Code Scanner  |
|         - Danger Warning Overlays                    - Threat Badges & History|
+---------------------------------------+---------------------------------------+
                                        | (HTTP POST /predict)
                                        v
+-------------------------------------------------------------------------------+
|                       FASTAPI BACKEND PREDICTION ENGINE                       |
|                                                                               |
|  [ 1. Trusted Whitelist & Custom Policy Check (Domain Rules) ]                |
|  [ 2. 30-Feature Lexical & Statistical Extractor (Shannon Entropy, Ratios) ]  |
|  [ 3. Local Random Forest ML Model (100 Trees, Scikit-Learn, .pkl) ]          |
|  [ 4. Content Robot (Page Titles, Password Fields, External Form Posts) ]     |
|  [ 5. SSL/TLS Certificate Inspector (Native Socket Handshake) ]               |
|  [ 6. Automated Threat Classification (Banking, Social, E-Commerce, etc.) ]   |
+---------------------------------------+---------------------------------------+
                                        |
                 +----------------------+----------------------+
                 v                                             v
+------------------------------------+       +----------------------------------+
|      MONGODB ATLAS CLOUD DB        |       |   CYBERSHIELD THREAT DASHBOARD   |
| - Collection: `scan_logs`          |       | - Real-time Stats & Telemetry    |
| - Collection: `custom_rules`       |       | - Chart.js Activity Analytics    |
| - Live sync with Local SQLite DB   |       | - Policy Management & QR Lab     |
+------------------------------------+       +----------------------------------+
```

---

## 3. Machine Learning & Feature Engineering (30 Features)

The AI Model uses a **Random Forest Classifier** trained on malicious and benign URL datasets from Kaggle (`malicious_phish.csv`).

### Feature Vector Composition:
| Category | Features | Description |
| :--- | :--- | :--- |
| **Length Metrics (4)** | `url_length`, `domain_length`, `path_length`, `query_length` | Character count of individual URL components |
| **Protocol (2)** | `has_https`, `has_http` | Secure vs Insecure protocol indicators |
| **Character Counts (9)** | `num_dots`, `num_dots_domain`, `num_hyphens`, `num_underscores`, `num_slashes`, `num_question_marks`, `num_equal_signs`, `num_ampersands`, `num_hashes` | Syntactic density and delimiter abuse |
| **Numerical Density (2)** | `num_digits`, `digit_to_letter_ratio` | Identifies obfuscated and randomized hashes |
| **Structural Anomalies (5)**| `has_ip`, `has_at_symbol`, `has_double_slash`, `domain_has_hyphen`, `num_subdomains` | Direct IP hosting, credential stuffing (@), redirect bugs |
| **Deceptive Signals (3)** | `suspicious_word_count`, `http_in_path`, `brand_in_subdomain` | Keyword matching (`login`, `kyc`, `otp`) and subdomain brand spoofing |
| **Shortener & TLD (2)** | `is_shortened`, `suspicious_tld` | `bit.ly`, `tinyurl` detection & `.xyz`, `.top`, `.tk` flags |
| **Information Entropy (2)** | `url_entropy`, `domain_entropy` | Shannon Entropy calculation measuring URL randomness |

---

## 4. Multi-Layered Hybrid Detection Pipeline

To achieve **zero false positives on verified services** and **catch sophisticated zero-day attacks**, CyberShield executes 5 cascading layers:

1. **Layer 1: Verified Trusted Whitelist** (`.gov.in`, `.edu.in`, `google.com`, `charusat.ac.in`, `sbi.co.in`, etc.) → Instant **100% Safe**.
2. **Layer 2: User Custom Policy Rules** (Custom Whitelist / Custom Blacklist from MongoDB/Dashboard) → Deterministic override.
3. **Layer 3: Random Forest Machine Learning Model** → Predicts base lexical phishing probability.
4. **Layer 4: Real-Time Content Analysis Robot** → Checks live webpage title, external password form submissions, and brand name mismatches.
5. **Layer 5: Native SSL/TLS Inspector** → Verifies SSL validity, issuer organization, and remaining certificate lifespan.

---

## 5. End-to-End Verification & Test Results

The automated integration test suite (`backend/test_integration.py`) validates the entire stack:

```text
=======================================================
[START] RUNNING CYBERSHIELD INTEGRATION TEST SUITE
=======================================================
[PASS] Test 1  - Root Health Check: PASSED (Model Loaded, 30 Features, SSL Active)
[PASS] Test 2  - Feature Extraction (30 Features): PASSED
[PASS] Test 3  - Trusted Whitelist Domain Prediction: PASSED (100% Safe)
[PASS] Test 4  - Phishing URL Detection & Category: PASSED (Banking & Financial Phishing)
[PASS] Test 5  - Suspicious TLD & Brand Spoof: PASSED (DANGER - PHISHING PATTERN)
[PASS] Test 6  - /api/stats Endpoint: PASSED (Live MongoDB Calculations)
[PASS] Test 7  - /api/scans Endpoint: PASSED (Multi-Client History Logged)
[PASS] Test 8  - /dashboard Route: PASSED (HTML UI Served)
[PASS] Test 9  - Client Type Logging (Extension vs Mobile App): PASSED
[PASS] Test 10 - SSL Inspector: PASSED (Native Socket Handshake Verified)
[PASS] Test 11 - Custom Policy Rules Manager (Blacklist/Whitelist): PASSED
----------------------------------------------------------------------
Ran 11 tests: ALL 11 PASSED (100% Success Rate)
```

---

## 6. Project Roadmap Completion Summary (Weeks 1 to 8)

* [x] **Week 1: Planning & Research:** SRS, System Architecture, Synopsis submitted.
* [x] **Week 2: Browser Extension Basics:** Manifest V3, modern dark-mode popup, activeTab capture.
* [x] **Week 3: AI Model Basics:** Kaggle dataset preprocessing, 30 features, Random Forest trained (`.pkl`).
* [x] **Week 4: Backend API Integration:** FastAPI microservice, `/predict` endpoint, `fetch()` integration.
* [x] **Week 5: Content Detection & Mobile App:** Scraper robot, Flutter Android project, QR scanner.
* [x] **Week 6: Database & Dashboard:** MongoDB Atlas cloud cluster, SQLite dual-logging, Glassmorphism Dashboard.
* [x] **Week 7: Integration & Refinement:** SSL inspection, threat categorization, custom rules policy, test suite.
* [x] **Week 8: Final Delivery & Reports:** Comprehensive project documentation, PPT slides outline, presentation demo readiness.

---

## 7. Conclusion & Future Enhancements
CyberShield delivers a complete, enterprise-grade, localized phishing protection platform. Future work may include:
* Graph Neural Network (GNN) analysis on domain redirection chains.
* Offline On-Device TensorFlow Lite model running inside Flutter for zero-connectivity scanning.
* Enterprise SIEM integration (Splunk / Elastic) for organization-wide phishing threat feeds.
