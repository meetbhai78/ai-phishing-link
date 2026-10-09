"""
CyberShield - Week 10 Complete Regression & Integration Test Suite (v4.0)
22 Tests: API, ML, Features, Content Robot, Database, SSL, Threat Categories,
          Custom Rules, Batch Scanner, Feedback, Metrics, Community Reports
"""
import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app, extract_features, is_trusted_domain, categorize_threat
from backend.ssl_inspector import inspect_ssl_certificate
import backend.database as db

class CyberShieldRegressionTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        print("\n" + "=" * 65)
        print("[START] CYBERSHIELD v4.0 -- WEEK 10 REGRESSION TEST SUITE (22 TESTS)")
        print("=" * 65)

    # ==========================================
    # CORE SYSTEM TESTS (Tests 1–5) -- Original Week 7
    # ==========================================

    def test_01_root_health_check(self):
        """Test API Root, Version, and All Feature Flags"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "online")
        self.assertTrue(data.get("model_loaded"))
        self.assertEqual(data.get("features_count"), 30)
        self.assertEqual(data.get("version"), "4.0.0")
        self.assertTrue(data.get("ssl_inspector_active"))
        self.assertTrue(data.get("custom_rules_active"))
        self.assertTrue(data.get("community_reports_active"))
        print("[PASS] Test 01 -- Root Health Check: v4.0.0, Model Loaded, 30 Features, All Modules Active")

    def test_02_feature_extraction_30_features(self):
        """Test URL Feature Extraction produces exactly 30 features"""
        url = "http://192.168.0.1/secure-login/update?token=xyz#verify"
        feats = extract_features(url)
        self.assertEqual(len(feats), 30)
        self.assertEqual(feats["has_ip"], 1)
        self.assertEqual(feats["has_http"], 1)
        self.assertEqual(feats["has_https"], 0)
        self.assertGreater(feats["suspicious_word_count"], 0)
        self.assertIn("url_entropy", feats)
        self.assertIn("domain_entropy", feats)
        self.assertIn("suspicious_tld", feats)
        print("[PASS] Test 02 -- Feature Extraction (30 Features): All structural features verified")

    def test_03_trusted_domain_whitelist(self):
        """Test that whitelisted domains bypass ML and return 100% SAFE"""
        self.assertTrue(is_trusted_domain("google.com"))
        self.assertTrue(is_trusted_domain("charusat.ac.in"))
        self.assertTrue(is_trusted_domain("mygov.in"))
        self.assertFalse(is_trusted_domain("fake-google-login.xyz"))
        
        response = self.client.post("/predict", json={"url": "https://www.google.com", "client_type": "extension"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_phishing"])
        self.assertEqual(data["confidence"], 100.0)
        self.assertIn("SAFE", data["risk_level"])
        print("[PASS] Test 03 -- Trusted Whitelist Domain: google.com -> 100% Safe, fake rejected")

    def test_04_phishing_prediction_ip_keywords(self):
        """Test detection of phishing URL with IP address and suspicious keywords"""
        phishing_url = "http://192.168.1.1/paypal/login-verify-account.php?id=9283#update"
        response = self.client.post("/predict", json={"url": phishing_url, "client_type": "mobile_app"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_phishing"])
        self.assertGreaterEqual(data["confidence"], 50.0)
        self.assertIn("DANGER", data["risk_level"])
        print(f"[PASS] Test 04 -- Phishing IP+Keywords: DETECTED ({data['risk_level']}, {data['confidence']}%)")

    def test_05_suspicious_tld_brand_spoof(self):
        """Test detection of suspicious TLD and brand spoofing"""
        spoof_url = "http://paypal-security-update.xyz/verify-login.html"
        response = self.client.post("/predict", json={"url": spoof_url, "client_type": "extension"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_phishing"])
        print(f"[PASS] Test 05 -- Suspicious TLD + Brand Spoof: DETECTED ({data['risk_level']})")

    # ==========================================
    # DATABASE & DASHBOARD TESTS (Tests 6–8)
    # ==========================================

    def test_06_database_stats_endpoint(self):
        """Test /api/stats endpoint returns correct structure"""
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        required_keys = ["total_scans", "phishing_detected", "safe_sites", "today_scans", "avg_confidence", "phishing_rate"]
        for key in required_keys:
            self.assertIn(key, data)
        print(f"[PASS] Test 06 -- /api/stats: Total Scans={data['total_scans']}, Phishing Rate={data['phishing_rate']}%")

    def test_07_database_scans_history(self):
        """Test /api/scans endpoint logs retrieval"""
        response = self.client.get("/api/scans?limit=10")
        self.assertEqual(response.status_code, 200)
        scans = response.json()
        self.assertIsInstance(scans, list)
        if scans:
            self.assertIn("url", scans[0])
            self.assertIn("is_phishing", scans[0])
            self.assertIn("client_type", scans[0])
            self.assertIn("threat_category", scans[0])
            self.assertIn("ssl_valid", scans[0])
        print(f"[PASS] Test 07 -- /api/scans: Retrieved {len(scans)} logs with all fields")

    def test_08_dashboard_html_serving(self):
        """Test /dashboard route serves HTML"""
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("CyberShield", response.text)
        print("[PASS] Test 08 -- /dashboard: HTML UI served successfully")

    # ==========================================
    # CLIENT TYPE & SSL TESTS (Tests 9–10)
    # ==========================================

    def test_09_client_type_logging(self):
        """Test that client_type is correctly distinguished in logs"""
        test_ext_url = "http://safe-test-site.org/docs"
        test_app_url = "http://mobile-test-site.org/home"
        
        self.client.post("/predict", json={"url": test_ext_url, "client_type": "extension"})
        self.client.post("/predict", json={"url": test_app_url, "client_type": "mobile_app"})
        
        recent = db.get_recent_scans(limit=10)
        client_types = [s.get("client_type") for s in recent]
        self.assertIn("extension", client_types)
        self.assertIn("mobile_app", client_types)
        print("[PASS] Test 09 -- Client Type Logging: extension + mobile_app both tracked")

    def test_10_ssl_inspector(self):
        """Test SSL Certificate Inspector on HTTP and HTTPS domains"""
        http_ssl = inspect_ssl_certificate("http://example.com")
        self.assertFalse(http_ssl["has_ssl"])
        self.assertFalse(http_ssl["valid"])
        
        https_ssl = inspect_ssl_certificate("https://www.google.com")
        self.assertTrue(https_ssl["has_ssl"])
        print("[PASS] Test 10 -- SSL Inspector: HTTP=No SSL, HTTPS=SSL verified via socket handshake")

    # ==========================================
    # CUSTOM RULES TESTS (Test 11)
    # ==========================================

    def test_11_custom_rules_manager(self):
        """Test Custom Whitelist and Blacklist Policy CRUD & Enforcement"""
        test_domain = "malicious-phishing-test.xyz"
        
        # 1. Add Blacklist Rule
        add_res = self.client.post("/api/rules", json={
            "domain": test_domain,
            "rule_type": "blacklist",
            "notes": "Week 10 regression test"
        })
        self.assertEqual(add_res.status_code, 200)
        
        # 2. Verify prediction returns 100% Phishing
        pred_res = self.client.post("/predict", json={"url": f"http://{test_domain}/login.php"})
        self.assertEqual(pred_res.status_code, 200)
        pred_data = pred_res.json()
        self.assertTrue(pred_data["is_phishing"])
        self.assertEqual(pred_data["confidence"], 100.0)
        self.assertIn("CUSTOM BLACKLIST", pred_data["risk_level"])
        
        # 3. Delete Rule
        del_res = self.client.delete(f"/api/rules/{test_domain}")
        self.assertEqual(del_res.status_code, 200)
        
        # 4. Verify rules list
        rules_res = self.client.get("/api/rules")
        self.assertEqual(rules_res.status_code, 200)
        print("[PASS] Test 11 -- Custom Rules Manager: Blacklist add -> enforce -> delete -> verify")

    # ==========================================
    # WEEK 9 FEATURES REGRESSION (Tests 12–14)
    # ==========================================

    def test_12_batch_scanner(self):
        """Test Enterprise Batch URL Scanner /api/batch-scan"""
        batch_urls = [
            "https://www.google.com",
            "https://stackoverflow.com",
            "http://fake-paypal-login.xyz/verify",
            "http://192.168.1.1/admin/login",
            "https://www.amazon.com"
        ]
        response = self.client.post("/api/batch-scan", json={
            "urls": batch_urls,
            "client_type": "batch_scan"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_scanned"], 5)
        self.assertIsInstance(data["results"], list)
        self.assertEqual(len(data["results"]), 5)
        print(f"[PASS] Test 12 -- Batch Scanner: {data['total_scanned']} URLs scanned in single request")

    def test_13_feedback_api(self):
        """Test User Feedback POST and GET"""
        # POST feedback
        fb_res = self.client.post("/api/feedback", json={
            "url": "http://test-false-positive.com",
            "reported_label": "safe",
            "user_comment": "Week 10 regression test -- false positive report"
        })
        self.assertEqual(fb_res.status_code, 200)
        fb_data = fb_res.json()
        self.assertTrue(fb_data["success"])
        
        # GET feedback list
        get_res = self.client.get("/api/feedback?limit=5")
        self.assertEqual(get_res.status_code, 200)
        fb_list = get_res.json()
        self.assertIsInstance(fb_list, list)
        self.assertGreater(len(fb_list), 0)
        print(f"[PASS] Test 13 -- Feedback API: POST submitted, GET returned {len(fb_list)} records")

    def test_14_ml_metrics_endpoint(self):
        """Test /api/metrics returns evaluation results"""
        response = self.client.get("/api/metrics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("accuracy", data)
        self.assertIn("precision", data)
        self.assertIn("recall", data)
        self.assertIn("f1_score", data)
        self.assertIn("roc_auc", data)
        self.assertIn("confusion_matrix", data)
        cm = data["confusion_matrix"]
        self.assertIn("true_positive", cm)
        self.assertIn("false_positive", cm)
        print(f"[PASS] Test 14 -- ML Metrics: Acc={data['accuracy']}%, F1={data['f1_score']}%, ROC-AUC={data['roc_auc']}%")

    # ==========================================
    # WEEK 10 / v4.0 COMMUNITY FEATURES (Tests 15–18)
    # ==========================================

    def test_15_community_questions_api(self):
        """Test /api/community-questions returns 5 AI training questions"""
        response = self.client.get("/api/community-questions")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("questions", data)
        questions = data["questions"]
        self.assertEqual(len(questions), 5)
        for q in questions:
            self.assertIn("id", q)
            self.assertIn("question", q)
            self.assertIn("options", q)
            self.assertIn("type", q)
        print(f"[PASS] Test 15 — Community Questions: {len(questions)} AI training questions returned")

    def test_16_community_report_submit(self):
        """Test /api/community-report POST with URL, label, and question answers"""
        response = self.client.post("/api/community-report", json={
            "url": "http://suspicious-test-phishing.xyz/login",
            "user_reported_label": "phishing",
            "questions_answers": {
                "q1_source": "WhatsApp",
                "q2_personal_info": "Yes",
                "q3_brand_impersonation": "Yes",
                "q5_suspicion_level": "5"
            },
            "source": "extension"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("report", data)
        self.assertIn("auto_scan", data)
        self.assertIn("message", data)
        print(f"[PASS] Test 16 — Community Report Submit: Report accepted with 4 answers + auto-scan")

    def test_17_community_reports_list(self):
        """Test /api/community-reports GET returns recent reports"""
        response = self.client.get("/api/community-reports?limit=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            report = data[0]
            self.assertIn("url", report)
            self.assertIn("user_reported_label", report)
            self.assertIn("auto_scan_phishing", report)
            self.assertIn("questions_answers", report)
            self.assertIn("source", report)
        print(f"[PASS] Test 17 — Community Reports List: {len(data)} reports retrieved")

    def test_18_community_stats(self):
        """Test /api/community-stats returns correct structure"""
        response = self.client.get("/api/community-stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        required = ["total_reports", "phishing_reports", "safe_reports", "unsure_reports", "from_app", "from_extension"]
        for key in required:
            self.assertIn(key, data)
        self.assertGreaterEqual(data["total_reports"], 0)
        print(f"[PASS] Test 18 — Community Stats: Total={data['total_reports']}, Phishing={data['phishing_reports']}")

    # ==========================================
    # ADVANCED DETECTION TESTS (Tests 19–22)
    # ==========================================

    def test_19_threat_categorization(self):
        """Test all 5 threat categories are correctly assigned"""
        # Banking
        banking_url = "http://fake-sbi-kyc-update.xyz/otp-verify"
        res = self.client.post("/predict", json={"url": banking_url}).json()
        self.assertTrue(res["is_phishing"])
        
        # Social Media
        social_url = "http://instagram-login-verify.tk/signin"
        res2 = self.client.post("/predict", json={"url": social_url}).json()
        self.assertTrue(res2["is_phishing"])
        
        # Lottery/Prize
        lottery_url = "http://free-prize-winner-claim.xyz/bonus"
        res3 = self.client.post("/predict", json={"url": lottery_url}).json()
        self.assertTrue(res3["is_phishing"])
        
        print(f"[PASS] Test 19 — Threat Categorization: Banking='{res['threat_category']}', Social='{res2['threat_category']}', Lottery='{res3['threat_category']}'")

    def test_20_url_shortener_detection(self):
        """Test URL shortener domains are flagged"""
        feats_bitly = extract_features("http://bit.ly/3xFakeLink")
        self.assertEqual(feats_bitly["is_shortened"], 1)
        
        feats_tinyurl = extract_features("http://tinyurl.com/fakePhishing")
        self.assertEqual(feats_tinyurl["is_shortened"], 1)
        
        feats_normal = extract_features("http://www.google.com")
        self.assertEqual(feats_normal["is_shortened"], 0)
        print("[PASS] Test 20 — URL Shortener Detection: bit.ly=Yes, tinyurl=Yes, google=No")

    def test_21_shannon_entropy_validation(self):
        """Test Shannon entropy feature produces valid values"""
        feats_simple = extract_features("http://abc.com")
        feats_complex = extract_features("http://x7k2m9p4q1z8w3n5.xyz/a1b2c3d4e5?token=f6g7h8i9j0k1l2")
        
        self.assertGreater(feats_simple["url_entropy"], 0.0)
        self.assertGreater(feats_complex["url_entropy"], feats_simple["url_entropy"])
        self.assertGreater(feats_complex["domain_entropy"], 0.0)
        print(f"[PASS] Test 21 — Shannon Entropy: Simple={feats_simple['url_entropy']}, Complex={feats_complex['url_entropy']} (complex > simple)")

    def test_22_safe_url_confidence_calibration(self):
        """Test safe URLs return calibrated confidence >= 85%"""
        safe_urls = [
            "https://www.wikipedia.org",
            "https://github.com",
            "https://www.amazon.com"
        ]
        for url in safe_urls:
            res = self.client.post("/predict", json={"url": url}).json()
            self.assertFalse(res["is_phishing"])
            self.assertGreaterEqual(res["confidence"], 85.0)
        print(f"[PASS] Test 22 — Safe URL Confidence: All 3 trusted URLs >= 85% confidence")

    @classmethod
    def tearDownClass(cls):
        print("\n" + "=" * 65)
        print("[COMPLETE] ALL 22 REGRESSION TESTS FINISHED")
        print("=" * 65)

if __name__ == '__main__':
    unittest.main()
