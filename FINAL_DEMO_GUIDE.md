# CyberShield: Complete Viva & Final Demonstration Guide
## Quick Reference for Final Presentation & Live Evaluation

---

### 1. One-Click System Startup
Run the following command or double-click `run_server.bat` to launch the entire CyberShield backend ecosystem:

```powershell
.\run_server.bat
```
* **FastAPI Server:** `http://127.0.0.1:8000`
* **Threat Dashboard:** `http://127.0.0.1:8000/dashboard`
* **Interactive API (Swagger UI):** `http://127.0.0.1:8000/docs`

---

### 2. Live Demo URLs (Safe vs Phishing)

| Type | Test URL | Expected System Reaction |
| :--- | :--- | :--- |
| **Verified Safe** | `https://www.charusat.ac.in` | 🛡️ **SAFE (VERIFIED DOMAIN)** - 100% Confidence |
| **Verified Safe** | `https://www.google.com` | 🛡️ **SAFE (VERIFIED DOMAIN)** - 100% Confidence |
| **IP Phishing** | `http://192.168.1.1/paypal/login-verify.php` | ⚠️ **DANGER** - Banking Phishing Flagged |
| **Suspicious TLD** | `http://free-apple-gift.xyz/claim-now` | ⚠️ **DANGER** - Suspicious TLD & Brand Spoof |
| **Obfuscated / Shortened**| `http://bit.ly/secure-banking-login` | ⚠️ **DANGER** - Shortened URL & Keyword Alert |

---

### 3. QR Code Demo (Mobile App)
* **Safe QR Code:** [safe_qr.png](file:///d:/5TH%20SEM/extention/safe_qr.png) (Points to `https://www.charusat.ac.in`)
* **Phishing QR Code:** [phishing_qr.png](file:///d:/5TH%20SEM/extention/phishing_qr.png) (Points to `http://192.168.1.1/secure-banking-login`)
* **Browser QR Testbench:** Open [qr_test.html](file:///d:/5TH%20SEM/extention/qr_test.html) in your browser to scan QR codes on-screen.

---

### 4. Running the Automated Test Suite
To demonstrate automated testing and verification to examiners, run:

```powershell
& "d:\5TH SEM\extention\ml_model\venv\Scripts\python.exe" backend/test_integration.py
```
* Output: **11/11 Tests Passed** (Validates 30 features, ML model, SSL inspector, MongoDB logging, and custom rule enforcement).

---

### 5. Frequently Asked Questions (Viva Preparation)

**Q1: Why Random Forest over Deep Learning (e.g. LSTM / BERT)?**
> *Answer:* Random Forest operates with microsecond inference latency (~2ms), consumes negligible CPU memory, runs locally without high-end GPUs, and provides high interpretability over structural and lexical URL features.

**Q2: How does the system handle zero-day phishing sites not in any blacklist?**
> *Answer:* CyberShield uses a multi-layered hybrid defense: lexical feature extraction (30 dimensions) + real-time page content scraping (detecting unauthorized password forms and brand mismatches) + native SSL certificate telemetry.

**Q3: Is the system reliant on third-party commercial AI APIs like OpenAI?**
> *Answer:* No. In strict compliance with project guidelines, all ML training, feature extraction, scraping bots, and inference pipelines are 100% locally engineered.
