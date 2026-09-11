"""
CyberShield - Week 7 End-to-End Integration & System Verification Test Suite (v3.7)
Tests: API, ML Model, Feature Extraction, Content Robot, Database Dual Logging,
       SSL Inspector, Threat Categorization, Custom Whitelist/Blacklist Rules
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

class CyberShieldIntegrationTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        print("\n=======================================================")
        print("[START] RUNNING CYBERSHIELD WEEK 7 INTEGRATION TEST SUITE")
        print("=======================================================")

    def test_01_root_health_check(self):
        """Test API Root and System Info"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "online")
        self.assertTrue(data.get("model_loaded"))
        self.assertEqual(data.get("features_count"), 30)
        self.assertTrue(data.get("ssl_inspector_active"))
        self.assertTrue(data.get("custom_rules_active"))
        print("[PASS] Test 1 - Root Health Check: PASSED (Model Loaded, 30 Features, SSL & Rules Active)")

    def test_02_feature_extraction(self):
        """Test URL Feature Extraction produces exactly 30 features"""
        url = "http://192.168.0.1/secure-login/update?token=xyz#verify"
        feats = extract_features(url)
        self.assertEqual(len(feats), 30)
        self.assertEqual(feats["has_ip"], 1)
        self.assertEqual(feats["has_http"], 1)
        self.assertEqual(feats["has_https"], 0)
        self.assertGreater(feats["suspicious_word_count"], 0)
        print("[PASS] Test 2 - Feature Extraction (30 Features): PASSED")

    def test_03_trusted_domain_whitelist(self):
        """Test that whitelisted domains bypass ML and return 100% SAFE"""
        self.assertTrue(is_trusted_domain("google.com"))
        self.assertTrue(is_trusted_domain("charusat.ac.in"))
        self.assertTrue(is_trusted_domain("mygov.in"))
        
        response = self.client.post("/predict", json={"url": "https://www.google.com", "client_type": "extension"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["is_phishing"])
        self.assertEqual(data["confidence"], 100.0)
        self.assertIn("SAFE", data["risk_level"])
        print("[PASS] Test 3 - Trusted Whitelist Domain Prediction: PASSED (100% Safe)")

    def test_04_phishing_prediction_with_ip_and_keywords(self):
        """Test detection of an obvious phishing URL with IP address and suspicious keywords"""
        phishing_url = "http://192.168.1.1/paypal/login-verify-account.php?id=9283#update"
        response = self.client.post("/predict", json={"url": phishing_url, "client_type": "mobile_app"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_phishing"])
        self.assertGreaterEqual(data["confidence"], 50.0)
        self.assertIn("DANGER", data["risk_level"])
        self.assertEqual(data["threat_category"], "Banking & Financial Phishing")
        print(f"[PASS] Test 4 - Phishing URL Detection & Category: PASSED ({data['threat_category']})")

    def test_05_suspicious_tld_and_brand_subdomain(self):
        """Test detection of suspicious TLD and brand spoofing"""
        spoof_url = "http://paypal-security-update.xyz/verify-login.html"
        response = self.client.post("/predict", json={"url": spoof_url, "client_type": "extension"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["is_phishing"])
        print(f"[PASS] Test 5 - Suspicious TLD & Brand Spoof: PASSED ({data['risk_level']})")

    def test_06_database_stats_endpoint(self):
        """Test /api/stats endpoint calculation"""
        response = self.client.get("/api/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_scans", data)
        self.assertIn("phishing_detected", data)
        self.assertIn("safe_sites", data)
        self.assertIn("today_scans", data)
        self.assertIn("avg_confidence", data)
        self.assertIn("phishing_rate", data)
        print(f"[PASS] Test 6 - /api/stats Endpoint: PASSED (Total Scans: {data['total_scans']})")

    def test_07_database_scans_history_endpoint(self):
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
        print(f"[PASS] Test 7 - /api/scans Endpoint: PASSED ({len(scans)} logs retrieved)")

    def test_08_dashboard_html_serving(self):
        """Test /dashboard route serves HTML"""
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)
        self.assertIn("CyberShield", response.text)
        self.assertIn("Threat Intelligence", response.text)
        print("[PASS] Test 8 - /dashboard Route: PASSED (HTML UI loaded)")

    def test_09_mobile_vs_extension_client_logging(self):
        """Test that client_type is correctly distinguished in logs"""
        test_ext_url = "http://safe-test-site.org/docs"
        test_app_url = "http://mobile-test-site.org/home"
        
        self.client.post("/predict", json={"url": test_ext_url, "client_type": "extension"})
        self.client.post("/predict", json={"url": test_app_url, "client_type": "mobile_app"})
        
        recent = db.get_recent_scans(limit=10)
        client_types = [s.get("client_type") for s in recent]
        self.assertIn("extension", client_types)
        self.assertIn("mobile_app", client_types)
        print("[PASS] Test 9 - Client Type Logging (Extension vs Mobile App): PASSED")

    def test_10_ssl_inspector(self):
        """Test SSL Certificate Inspector on HTTP and HTTPS domains"""
        http_ssl = inspect_ssl_certificate("http://example.com")
        self.assertFalse(http_ssl["has_ssl"])
        self.assertFalse(http_ssl["valid"])
        
        https_ssl = inspect_ssl_certificate("https://www.google.com")
        self.assertTrue(https_ssl["has_ssl"])
        print("[PASS] Test 10 - SSL Inspector: PASSED (Native Socket Handshake Verified)")

    def test_11_custom_rules_manager_api(self):
        """Test Custom Whitelist and Blacklist Policy CRUD & Enforcement"""
        test_domain = "malicious-phishing-test.xyz"
        
        # 1. Add Blacklist Rule
        add_res = self.client.post("/api/rules", json={
            "domain": test_domain,
            "rule_type": "blacklist",
            "notes": "Testing auto-block rule"
        })
        self.assertEqual(add_res.status_code, 200)
        
        # 2. Verify Predict identifies it as 100% Phishing due to rule
        pred_res = self.client.post("/predict", json={"url": f"http://{test_domain}/login.php"})
        self.assertEqual(pred_res.status_code, 200)
        pred_data = pred_res.json()
        self.assertTrue(pred_data["is_phishing"])
        self.assertEqual(pred_data["confidence"], 100.0)
        self.assertIn("CUSTOM BLACKLIST", pred_data["risk_level"])
        
        # 3. Delete Rule
        del_res = self.client.delete(f"/api/rules/{test_domain}")
        self.assertEqual(del_res.status_code, 200)
        print("[PASS] Test 11 - Custom Policy Rules Manager (Blacklist/Whitelist): PASSED")

if __name__ == '__main__':
    unittest.main()
