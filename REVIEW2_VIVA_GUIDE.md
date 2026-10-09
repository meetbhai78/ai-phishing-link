# CyberShield — Review 2 Viva Q&A Preparation Guide

**Project:** AI-Based Real-Time Phishing Detection System
**University:** CHARUSAT | **Semester:** 7th | **Version:** v4.0

---

## 🟢 BASIC QUESTIONS

### Q1. What is the problem your project solves?
**A:** Phishing attacks are the #1 cyber threat globally. Users receive fake URLs via WhatsApp, SMS, and email that look like legitimate websites (banks, Amazon, PayPal) but steal credentials. Our project "CyberShield" detects these phishing URLs in real-time using Machine Learning before the user gets tricked.

### Q2. What are limitations of existing phishing detection systems?
**A:** Existing solutions like Google Safe Browsing rely on blacklist databases that can't detect new/zero-day phishing URLs. They are reactive (only block known threats), not proactive. CyberShield uses ML-based analysis of URL structure + web content + SSL certificates, so it can detect never-before-seen phishing URLs.

### Q3. What does CyberShield do?
**A:** CyberShield is a multi-platform phishing detection ecosystem with:
- A Chrome/Edge browser extension that auto-scans every website
- A Flutter mobile app with URL and QR code scanning
- A FastAPI backend powered by a custom-trained Random Forest ML model
- Real-time threat intelligence dashboard
- Community phishing reporting system

### Q4. Why did your team choose this project?
**A:** Phishing is the most common and damaging cyberattack vector. According to APWG, there were over 5 million phishing attacks in 2023 alone. We wanted to build a practical, deployable solution that uses AI/ML to protect users proactively, not just rely on outdated blacklists.

### Q5. Who are the end users?
**A:** General internet users (browser extension), mobile users (Flutter app), and security analysts (dashboard + batch scanner).

---

## 🟡 TECHNICAL QUESTIONS

### Q6. Which ML algorithm did you use and why?
**A:** Random Forest Classifier with 300 decision trees. We chose it because:
1. It handles both numerical and categorical features well
2. It's resistant to overfitting due to ensemble nature
3. It provides feature importance rankings
4. It works well with our 30-feature URL analysis without needing deep learning

### Q7. What are the 30 features you extract from URLs?
**A:** They fall into 6 categories:
- **Length Features (4):** url_length, domain_length, path_length, query_length
- **Protocol (2):** has_https, has_http
- **Count Features (11):** dots, hyphens, underscores, slashes, question marks, equals, ampersands, hashes, percent signs, digits, dots in domain
- **Structural (6):** digit_to_letter_ratio, num_subdomains, has_ip, has_at_symbol, has_double_slash, domain_has_hyphen
- **Pattern (5):** suspicious_word_count, http_in_path, brand_in_subdomain, is_shortened, suspicious_tld
- **Statistical (2):** url_entropy (Shannon entropy), domain_entropy

### Q8. What dataset did you use?
**A:** We used the "Malicious and Phishing URLs" dataset from Kaggle containing 600,000+ labeled URLs. We trained on a balanced subset of 100,000 URLs (50K benign + 50K malicious) with an 80/20 train-test split.

### Q9. What is your model's accuracy?
**A:** On the evaluation sample:
- Accuracy: ~95%
- Precision: ~90%
- Recall: ~96%
- F1-Score: ~93%
- ROC-AUC: ~98%

These are validated using 5-fold stratified cross-validation to ensure no overfitting.

### Q10. What is the hybrid detection pipeline?
**A:** CyberShield uses 4 layers of detection:
1. **ML Model** — 30-feature Random Forest prediction
2. **Content Robot** — Web scraping to check for password fields, external form actions, brand mismatches
3. **SSL Inspector** — Socket-level SSL certificate validation (issuer, expiry, self-signed check)
4. **Custom Rules** — Admin whitelist/blacklist policy enforcement

The final hybrid score is a weighted combination: 60% ML + 40% Content Score.

### Q11. What does the Content Robot (Web Scraper) do?
**A:** It fetches the webpage HTML and analyzes:
- Presence of password input fields (credential harvesting indicator)
- External form action URLs (data being sent to a different domain)
- Page title brand mismatch (title says "PayPal" but domain is not paypal.com)
- Hidden iframes, JavaScript redirects, and other suspicious elements

### Q12. How does the SSL Inspector work?
**A:** It performs a native Python socket SSL handshake with the domain, extracts:
- Certificate validity (valid/expired/self-signed)
- Issuer (Let's Encrypt, DigiCert, etc.)
- Days remaining until expiry
- If a login page has invalid SSL, the hybrid score gets a +25% penalty.

### Q13. What is FastAPI's role?
**A:** FastAPI is our prediction backend that:
- Loads the trained `.pkl` model
- Exposes `/predict` endpoint for URL analysis
- Runs the hybrid detection pipeline
- Logs all scans to MongoDB Atlas + SQLite
- Serves the dashboard, APIs for stats/rules/feedback/community reports

### Q14. How is MongoDB used?
**A:** MongoDB Atlas (cloud) stores:
- `scan_logs` — every URL scan with result, confidence, threat category
- `custom_rules` — whitelist/blacklist domain rules
- `user_feedback` — false positive/negative reports
- `community_reports` — crowdsourced phishing intelligence
SQLite acts as a local fallback if MongoDB is unavailable.

### Q15. How does the browser extension work?
**A:** It uses Chrome Manifest V3:
- `popup.js` gets current tab URL and calls FastAPI `/predict`
- `background.js` (service worker) auto-scans every tab change
- Shows badge icon (green OK = safe, red ! = danger)
- Sends Chrome notification for phishing detections

### Q16. How does the Flutter app connect to the backend?
**A:** The app uses `http` package to make REST API calls to FastAPI's `/predict` endpoint. For physical phones, the API URL is set to the computer's local IP (e.g., `http://192.168.X.X:8000/predict`). For Android emulator, it uses `http://10.0.2.2:8000/predict`.

---

## 🔴 ADVANCED QUESTIONS

### Q17. What is a False Positive?
**A:** When the system incorrectly flags a safe/legitimate URL as phishing. Example: A new startup's website with a suspicious-looking domain gets blocked. This is bad because it blocks legitimate access.

### Q18. What is a False Negative?
**A:** When the system misses a phishing URL and marks it as safe. This is MORE dangerous because the user proceeds to enter credentials on a fake site. That's why our system prioritizes high recall (catch as many phishing URLs as possible).

### Q19. Explain the Confusion Matrix.
**A:**
```
                  Predicted
               Safe    Phishing
Actual Safe  [  TN  ]  [  FP  ]
Actual Phish [  FN  ]  [  TP  ]
```
- TN: Correctly identified safe → Good
- TP: Correctly identified phishing → Good
- FP: Safe URL flagged as phishing → Annoying but not dangerous
- FN: Phishing URL missed → Dangerous!

### Q20. What is ROC-AUC?
**A:** ROC (Receiver Operating Characteristic) curve plots True Positive Rate vs False Positive Rate at various thresholds. AUC (Area Under Curve) measures overall model discrimination ability. Our 98.9% ROC-AUC means the model almost perfectly separates phishing from safe URLs.

### Q21. Why use Whitelist/Blacklist alongside ML?
**A:** ML is probabilistic — it gives confidence scores, not absolute answers. Whitelist ensures trusted domains (google.com, charusat.ac.in) are NEVER blocked. Blacklist allows admins to permanently block known-bad domains with 100% confidence. This prevents both false positives and false negatives for known domains.

### Q22. How will user feedback help future model improvement?
**A:** When users report false positives/negatives via the Feedback API, these URLs get logged with their correct labels. In future retraining cycles, these user-corrected URLs can be added to the training dataset, directly addressing the model's weaknesses. The Community Reports also collect additional context (source, brand impersonation, suspicion level) which enriches training data quality.

### Q23. What happens if a website is unreachable?
**A:** The Content Robot has a 3-second timeout. If the webpage can't be fetched:
- Content analysis is skipped (content_risk_score = 0)
- SSL check has a 2.5-second timeout
- The system falls back to ML-only prediction
- If the URL has no red flags and valid SSL, the hybrid score is capped at 25%

### Q24. Why hybrid approach instead of ML alone?
**A:** ML alone can be fooled by carefully crafted URLs. Our hybrid approach catches cases ML misses:
- Brand impersonation in subdomains (content robot catches this)
- Password fields on non-HTTPS pages (SSL inspector catches this)
- Known malicious domains (blacklist catches this)
- Zero-day phishing with normal-looking URLs but malicious content (content robot catches this)

### Q25. What is Shannon Entropy and why is it a feature?
**A:** Shannon entropy measures the randomness/unpredictability of characters in a string. Phishing URLs often have high entropy because they use random character strings (e.g., `x7k2m9p4q1z8.xyz`). Legitimate domains tend to be readable words with lower entropy.

### Q26. How do you prevent overfitting?
**A:** Multiple safeguards:
1. 80/20 stratified train-test split (no data leakage)
2. Random Forest's inherent bagging reduces overfitting
3. `class_weight='balanced'` handles class imbalance
4. 5-fold cross-validation confirms consistent performance
5. CV accuracy closely matches test accuracy (within ±2%)

### Q27. What threat categories does the system detect?
**A:** 6 categories:
1. Banking & Financial Phishing (SBI, PayPal, HDFC keywords)
2. Social Media Credential Harvesting (Instagram, Facebook, WhatsApp)
3. E-Commerce & Service Spoof (Amazon, Netflix, Apple)
4. Lottery / Prize / Giveaway Scam (free, winner, bonus)
5. Account Takeover / Credential Phishing (login, verify, password)
6. Generic Suspicious Threat (everything else)

### Q28. What is the Community Report feature?
**A:** Users can paste suspicious URLs and report them as phishing/safe/unsure. The system auto-scans the URL with AI, then asks 5 optional training questions (link source, personal info request, brand impersonation, data entry, suspicion level). Users can skip any question. This crowdsourced data helps improve future model accuracy.

### Q29. How does Batch Scanning work?
**A:** The `/api/batch-scan` endpoint accepts up to 20 URLs in a single request. Each URL is independently processed through the full hybrid pipeline. This is useful for enterprise security teams who need to check multiple URLs simultaneously.

### Q30. What are the system's limitations?
**A:**
1. Requires active internet for SSL inspection and content scraping
2. ML model needs periodic retraining as phishing techniques evolve
3. URL shorteners may not be fully resolved before analysis
4. Very new/sophisticated phishing sites may initially bypass detection
5. Backend must be running locally for the extension/app to work

### Q31. What is the tech stack?
**A:**
- ML: Python, Scikit-learn, Pandas, NumPy, Joblib
- Backend: FastAPI, Uvicorn, Python
- Extension: HTML, CSS, JavaScript, Chrome Manifest V3
- Mobile: Flutter, Dart
- Database: MongoDB Atlas (cloud) + SQLite (local fallback)
- Dashboard: HTML, CSS, JavaScript (Chart.js)

### Q32. How many automated tests do you have?
**A:** 22 automated integration tests covering: API health, feature extraction, trusted domains, phishing detection, database stats, scan history, dashboard, client type logging, SSL inspector, custom rules, batch scanner, feedback API, ML metrics, community questions, community reports, community stats, threat categorization, URL shortener detection, Shannon entropy validation, and safe URL confidence calibration.

---

## 💡 TIPS FOR VIVA

1. **Demo first, explain after** — Show the working system before diving into technical details
2. **Know your numbers** — Accuracy, Precision, Recall, F1, ROC-AUC, 30 features, 300 trees, 100K training samples
3. **Acknowledge limitations honestly** — Shows maturity
4. **Mention future scope** — Deep learning models, real-time URL resolution, browser notification blocking, community-driven blacklists
5. **Be ready for live testing** — Keep server running, extension loaded, test URLs handy

---

*CyberShield v4.0 — Review 2 Viva Preparation Guide*
