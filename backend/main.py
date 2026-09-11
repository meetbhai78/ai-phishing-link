import sys
import os
import re
import math
import joblib
import pandas as pd
from urllib.parse import urlparse
from collections import Counter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend.content_analyzer import fetch_webpage_html, analyze_webpage_content
    from backend.ssl_inspector import inspect_ssl_certificate
    import backend.database as db
except ImportError:
    from content_analyzer import fetch_webpage_html, analyze_webpage_content
    from ssl_inspector import inspect_ssl_certificate
    import database as db

# ==========================================
# CyberShield - FastAPI Prediction Backend
# v3.7 - 30 Features + Content Robot + SSL Inspector + Custom Rules
# ==========================================

app = FastAPI(
    title="CyberShield Prediction API & Threat Intelligence",
    description="AI-Based Real-Time Phishing Detection API with MongoDB Atlas Logging & SSL Inspector",
    version="3.7.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Dashboard Static Directory
DASHBOARD_DIR = os.path.join(os.path.dirname(__file__), '..', 'dashboard')
if os.path.exists(DASHBOARD_DIR):
    app.mount("/dashboard-static", StaticFiles(directory=DASHBOARD_DIR), name="dashboard-static")

# ==========================================
# Load ML Model
# ==========================================
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml_model', 'random_forest_model.pkl')

try:
    model = joblib.load(MODEL_PATH)
    print(f"[SUCCESS] ML Model v3.0 loaded (30 features) from: {MODEL_PATH}")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")
    model = None

# ==========================================
# Trusted Domains Whitelist & High Authority Roots
# ==========================================
TRUSTED_TLDS    = ['.gov.in', '.edu.in', '.ac.in', '.gov', '.edu', '.mil', '.nic.in', '.res.in', '.org.in']
TRUSTED_DOMAINS = [
    'google.com', 'google.co.in', 'youtube.com', 'facebook.com', 'amazon.com', 'amazon.in',
    'github.com', 'linkedin.com', 'microsoft.com', 'apple.com', 'twitter.com', 'x.com',
    'instagram.com', 'wikipedia.org', 'reddit.com', 'stackoverflow.com', 'medium.com',
    'netflix.com', 'flipkart.com', 'whatsapp.com', 'telegram.org', 'discord.com', 'spotify.com',
    'mygov.in', 'india.gov.in', 'nic.in', 'irctc.co.in', 'uidai.gov.in', 'incometax.gov.in',
    'charusat.ac.in', 'gmail.com', 'outlook.com', 'yahoo.com', 'bing.com', 'duckduckgo.com',
    'paytm.com', 'phonepe.com', 'gpay.com', 'nsdl.co.in', 'sbi.co.in', 'onlinesbi.sbi',
    'hdfcbank.com', 'icicibank.com', 'axisbank.com', 'kotak.com', 'pnbindia.in', 'bankofbaroda.in',
    'zerodha.com', 'groww.in', 'upstox.com', 'npci.org.in', 'rbi.org.in',
    'openai.com', 'chatgpt.com', 'anthropic.com', 'claude.ai', 'gemini.google.com',
    'opera.com', 'mozilla.org', 'brave.com', 'cloudflare.com', 'fastapi.tiangolo.com',
    'render.com', 'heroku.com', 'vercel.com', 'netlify.com', 'railway.app', 'github.io',
    'aws.amazon.com', 'cloud.google.com', 'azure.microsoft.com', 'digitalocean.com', 'firebase.google.com'
]

def is_trusted_domain(domain: str) -> bool:
    domain = domain.lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]
    for tld in TRUSTED_TLDS:
        if domain.endswith(tld):
            return True
    for td in TRUSTED_DOMAINS:
        if domain == td or domain.endswith('.' + td):
            return True
    return False

# ==========================================
# Feature Extraction - 30 Features
# ==========================================
def extract_features(url: str) -> dict:
    features = {}

    try:
        parsed = urlparse(url if '://' in url else 'http://' + url)
        domain = parsed.netloc.lower().replace('www.', '')
        path   = parsed.path  or ''
        query  = parsed.query or ''
        scheme = parsed.scheme or ''
    except Exception:
        domain, path, query, scheme = url, '', '', ''

    url_lower = url.lower()

    # Length Features
    features['url_length']     = len(url)
    features['domain_length']  = len(domain)
    features['path_length']    = len(path)
    features['query_length']   = len(query)

    # Protocol
    features['has_https'] = 1 if scheme == 'https' else 0
    features['has_http']  = 1 if scheme == 'http'  else 0

    # Count Features
    features['num_dots']           = url.count('.')
    features['num_dots_domain']    = domain.count('.')
    features['num_hyphens']        = url.count('-')
    features['num_underscores']    = url.count('_')
    features['num_slashes']        = url.count('/')
    features['num_question_marks'] = url.count('?')
    features['num_equal_signs']    = url.count('=')
    features['num_ampersands']     = url.count('&')
    features['num_hashes']         = url.count('#')
    features['num_percent']        = url.count('%')
    features['num_digits']         = sum(c.isdigit() for c in url)

    # Ratio
    letters = sum(c.isalpha() for c in url)
    features['digit_to_letter_ratio'] = round(features['num_digits'] / (letters + 1), 4)

    # Subdomain
    parts = domain.split('.')
    features['num_subdomains'] = max(0, len(parts) - 2)

    # Structural / Pattern Red-Flags
    ip_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]))'
    )
    features['has_ip']           = 1 if ip_pattern.search(url) else 0
    features['has_at_symbol']    = 1 if '@' in url else 0
    features['has_double_slash'] = 1 if '//' in url[8:] else 0
    features['domain_has_hyphen']= 1 if '-' in domain else 0

    # Suspicious Keywords
    suspicious_words = [
        'login', 'signin', 'verify', 'account', 'update', 'secure', 'banking',
        'confirm', 'password', 'credential', 'support', 'service', 'alert',
        'free', 'bonus', 'claim', 'winner', 'gift', 'prize', 'kyc', 'otp'
    ]
    features['suspicious_word_count'] = sum(1 for w in suspicious_words if w in url_lower)

    # Deceptive Patterns
    features['http_in_path'] = 1 if 'http' in path.lower() else 0

    # Brand Hijacking check in subdomains
    brands = ['google', 'apple', 'microsoft', 'amazon', 'paypal', 'netflix', 'facebook', 'instagram', 'sbi', 'hdfc', 'paytm']
    features['brand_in_subdomain'] = 0
    if features['num_subdomains'] > 0:
        for brand in brands:
            if brand in domain and not domain.endswith(brand + '.com') and not domain.endswith(brand + '.in'):
                features['brand_in_subdomain'] = 1
                break

    # URL Shorteners
    shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly', 'adf.ly']
    features['is_shortened'] = 1 if any(s in domain for s in shorteners) else 0

    # Entropy
    def shannon_entropy(s: str) -> float:
        if not s:
            return 0.0
        counts = Counter(s)
        n = len(s)
        return round(-sum((c / n) * math.log2(c / n) for c in counts.values()), 4)

    features['url_entropy']    = shannon_entropy(url)
    features['domain_entropy'] = shannon_entropy(domain)

    # Suspicious TLDs
    suspicious_tlds = ['.xyz', '.top', '.club', '.info', '.biz', '.cc', '.tk', '.ga', '.cf', '.gq', '.ml', '.work', '.click', '.loan']
    features['suspicious_tld'] = 1 if any(domain.endswith(tld) for tld in suspicious_tlds) else 0

    return features

# ==========================================
# Phishing Threat Categorization
# ==========================================
def categorize_threat(url: str, content_res: dict, is_phishing: bool) -> str:
    if not is_phishing:
        return "Legitimate / Verified Clean"
    
    url_lower = url.lower()
    brand = (content_res.get("title_brand") or "").lower()
    
    # 1. Banking & Finance
    banking_keywords = ['bank', 'sbi', 'hdfc', 'icici', 'axis', 'paypal', 'paytm', 'phonepe', 'gpay', 'kyc', 'otp', 'card', 'cvv', 'banking', 'wallet', 'crypto', 'binance', 'coinbase']
    if any(k in url_lower for k in banking_keywords) or any(k in brand for k in ['sbi', 'hdfc', 'icici', 'axis', 'paypal', 'paytm']):
        return "Banking & Financial Phishing"
        
    # 2. Social Media
    social_keywords = ['instagram', 'facebook', 'twitter', 'linkedin', 'tiktok', 'snapchat', 'whatsapp', 'telegram', 'discord', 'social']
    if any(k in url_lower for k in social_keywords) or any(k in brand for k in social_keywords):
        return "Social Media Credential Harvesting"
        
    # 3. E-Commerce & Services
    ecom_keywords = ['amazon', 'flipkart', 'netflix', 'spotify', 'ebay', 'walmart', 'prime', 'disney', 'apple', 'microsoft']
    if any(k in url_lower for k in ecom_keywords) or any(k in brand for k in ecom_keywords):
        return "E-Commerce & Service Spoof"
        
    # 4. Lottery / Reward / Giveaway
    lottery_keywords = ['lottery', 'prize', 'winner', 'gift', 'bonus', 'claim', 'free', 'reward', 'spin', 'airdrop']
    if any(k in url_lower for k in lottery_keywords):
        return "Lottery / Prize / Giveaway Scam"
        
    # 5. Account Takeover
    account_keywords = ['login', 'signin', 'password', 'verify', 'account', 'update', 'credential', 'auth']
    if any(k in url_lower for k in account_keywords) or content_res.get("has_password_field"):
        return "Account Takeover / Credential Phishing"
        
    return "Generic Suspicious Threat"

# ==========================================
# Pydantic Schemas
# ==========================================
class URLRequest(BaseModel):
    url: str
    client_type: Optional[str] = "extension"

class CustomRuleRequest(BaseModel):
    domain: str
    rule_type: str # 'whitelist' or 'blacklist'
    notes: Optional[str] = ""

class PredictionResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    risk_level: str
    features: dict
    hybrid_score: float = 0.0
    threat_category: str = "Generic"
    ssl_info: Dict[str, Any] = {}
    content_analysis: dict = {}

# ==========================================
# Endpoints
# ==========================================
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "CyberShield Prediction API",
        "version": "3.7.0",
        "model_loaded": model is not None,
        "features_count": 30,
        "content_robot_active": True,
        "ssl_inspector_active": True,
        "custom_rules_active": True,
        "database_mode": "MongoDB Atlas / SQLite Dual Logging",
        "dashboard_url": "http://127.0.0.1:8000/dashboard"
    }

@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    dashboard_path = os.path.join(DASHBOARD_DIR, 'index.html')
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return HTMLResponse("<h1>CyberShield Dashboard Loading...</h1>")

@app.get("/api/stats")
def get_stats_api():
    """Returns real-time scan statistics for the dashboard."""
    return db.get_stats()

@app.get("/api/scans")
def get_scans_api(limit: int = 100):
    """Returns recent scan history logs for the dashboard."""
    return db.get_recent_scans(limit=limit)

@app.delete("/api/scans")
def clear_scans_api():
    """Clears all scan history."""
    success = db.clear_scans()
    return {"success": success, "message": "Scan history cleared."}

# ==========================================
# Custom Domain Rules Endpoints
# ==========================================
@app.get("/api/rules")
def get_rules_api():
    """Gets all custom whitelist / blacklist domain rules."""
    return db.get_custom_rules()

@app.post("/api/rules")
def add_rule_api(req: CustomRuleRequest):
    """Adds a custom domain rule."""
    if not req.domain.strip():
        raise HTTPException(status_code=400, detail="Domain cannot be empty.")
    rule = db.add_custom_rule(req.domain, req.rule_type, req.notes or "")
    return {"success": True, "rule": rule}

@app.delete("/api/rules/{domain}")
def delete_rule_api(domain: str):
    """Deletes a custom domain rule."""
    success = db.delete_custom_rule(domain)
    return {"success": success, "domain": domain}

# ==========================================
# Week 9 Advanced Features: ML Evaluation, Feedback & Batch Scanner
# ==========================================
class FeedbackRequest(BaseModel):
    url: str
    reported_label: str  # 'safe' or 'phishing'
    user_comment: Optional[str] = ""

class BatchScanRequest(BaseModel):
    urls: list[str]
    client_type: Optional[str] = "batch_scan"

@app.get("/api/metrics")
def get_model_metrics_api():
    """Evaluates ML model performance metrics (Accuracy, Precision, Recall, F1, Confusion Matrix)."""
    from backend.metrics import evaluate_model
    return evaluate_model()

@app.post("/api/feedback")
def submit_feedback_api(req: FeedbackRequest):
    """Logs user feedback (false-positive / false-negative report) to database."""
    if not req.url.strip():
        raise HTTPException(status_code=400, detail="URL cannot be empty.")
    record = db.add_user_feedback(req.url, req.reported_label, req.user_comment or "")
    return {"success": True, "feedback": record, "message": "Feedback submitted successfully for active AI retraining."}

@app.get("/api/feedback")
def get_feedback_api(limit: int = 50):
    """Retrieves all user feedback reports."""
    return db.get_user_feedback(limit=limit)

@app.post("/api/batch-scan")
def batch_scan_urls_api(req: BatchScanRequest):
    """Scans multiple URLs in a single batch request for enterprise threat hunting."""
    results = []
    for u in req.urls[:20]:  # Cap at 20 URLs per batch
        if u and u.strip():
            try:
                res = predict_url(URLRequest(url=u.strip(), client_type=req.client_type))
                results.append(res)
            except Exception as e:
                results.append({"url": u, "error": str(e)})
    return {"total_scanned": len(results), "results": results}


# ==========================================
# Main Prediction Endpoint
# ==========================================
@app.post("/predict", response_model=PredictionResponse)
def predict_url(request: URLRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="ML Model not loaded.")

    url = request.url.strip()
    client_type = request.client_type or "extension"
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    parsed_url = urlparse(url if '://' in url else 'http://' + url)
    domain = parsed_url.netloc.lower().replace('www.', '')

    features = extract_features(url)

    # 1. SSL Certificate Inspection
    ssl_res = inspect_ssl_certificate(url, timeout=2.5)

    # 2. Check Custom Whitelist / Blacklist Rules
    custom_rules = db.get_custom_rules()
    for rule in custom_rules:
        r_dom = rule.get("domain", "").lower()
        if r_dom and (domain == r_dom or domain.endswith("." + r_dom)):
            if rule.get("rule_type") == "blacklist":
                resp = PredictionResponse(
                    url=url, is_phishing=True, confidence=100.0,
                    risk_level="CRITICAL DANGER (CUSTOM BLACKLIST RULE)",
                    features=features, hybrid_score=100.0,
                    threat_category="Custom Blacklisted Threat",
                    ssl_info=ssl_res, content_analysis={}
                )
                db.log_scan({
                    "url": url, "is_phishing": True, "confidence": 100.0,
                    "risk_level": "CRITICAL DANGER (CUSTOM BLACKLIST RULE)",
                    "hybrid_score": 100.0, "client_type": client_type,
                    "brand_detected": "Blacklisted Rule", "scraped_title": "",
                    "threat_category": "Custom Blacklisted Threat", "ssl_valid": ssl_res.get("valid", False)
                })
                return resp
            elif rule.get("rule_type") == "whitelist":
                resp = PredictionResponse(
                    url=url, is_phishing=False, confidence=100.0,
                    risk_level="SAFE (CUSTOM WHITELIST RULE)",
                    features=features, hybrid_score=0.0,
                    threat_category="Custom Whitelisted Clean",
                    ssl_info=ssl_res, content_analysis={}
                )
                db.log_scan({
                    "url": url, "is_phishing": False, "confidence": 100.0,
                    "risk_level": "SAFE (CUSTOM WHITELIST RULE)",
                    "hybrid_score": 0.0, "client_type": client_type,
                    "brand_detected": "Whitelisted Rule", "scraped_title": "",
                    "threat_category": "Custom Whitelisted Clean", "ssl_valid": ssl_res.get("valid", False)
                })
                return resp

    # 3. Robot Scraping Step
    html_text, success, err_msg = fetch_webpage_html(url, timeout=3)
    content_res = analyze_webpage_content(url, html_text)

    # 4. Default Verified Domains Whitelist Check
    if is_trusted_domain(domain):
        category = "Legitimate / Verified Clean"
        resp = PredictionResponse(
            url=url, is_phishing=False, confidence=100.0,
            risk_level="SAFE (VERIFIED DOMAIN)", features=features,
            hybrid_score=0.0, threat_category=category,
            ssl_info=ssl_res, content_analysis=content_res
        )
        db.log_scan({
            "url": url,
            "is_phishing": False,
            "confidence": 100.0,
            "risk_level": "SAFE (VERIFIED DOMAIN)",
            "hybrid_score": 0.0,
            "client_type": client_type,
            "brand_detected": content_res.get("title_brand", ""),
            "scraped_title": content_res.get("page_title", ""),
            "threat_category": category,
            "ssl_valid": ssl_res.get("valid", False)
        })
        return resp

    # 5. Machine Learning Prediction
    feature_df    = pd.DataFrame([features])
    probabilities = model.predict_proba(feature_df)[0]
    
    phishing_prob = probabilities[1]
    ml_phishing_pct = round(phishing_prob * 100, 2)
    content_score = content_res.get('content_risk_score', 0.0)

    # Check for structural / content red-flags
    has_red_flags = bool(
        features['has_ip'] or features['has_at_symbol'] or 
        features['brand_in_subdomain'] or features['suspicious_word_count'] > 0 or 
        features['is_shortened'] or features['suspicious_tld'] or 
        content_res.get('has_password_field') or content_res.get('external_form_action') or 
        content_res.get('brand_mismatch')
    )

    if content_res.get('scraped_successfully'):
        if not has_red_flags and ssl_res.get('valid', False) and content_score == 0.0:
            # Clean webpage with trusted SSL and zero red flags -> safely calibrate to clean
            hybrid_score = round(min(ml_phishing_pct * 0.15, 15.0), 2)
        else:
            hybrid_score = round(0.6 * ml_phishing_pct + 0.4 * content_score, 2)
    else:
        if not has_red_flags and ssl_res.get('valid', False):
            hybrid_score = round(min(ml_phishing_pct * 0.3, 25.0), 2)
        else:
            hybrid_score = ml_phishing_pct

    # SSL penalty: if self-signed or invalid SSL on supposed login page
    if not ssl_res.get("valid", True) and (content_res.get('has_password_field') or 'login' in url.lower()):
        hybrid_score = min(100.0, hybrid_score + 25.0)

    # 6. Hybrid & Deterministic Red-Flag Evaluation
    # Rule A: Brand Impersonation (e.g. 'paypal' in domain/subdomain but not official domain)
    if features['brand_in_subdomain'] or content_res.get('brand_mismatch'):
        is_phishing = True
        confidence  = 98.5
        risk_level  = "CRITICAL DANGER (BRAND IMPERSONATION)"
    # Rule B: Unauthorized External Form Post / Password theft
    elif content_res.get('has_password_field') and content_res.get('external_form_action'):
        is_phishing = True
        confidence  = 96.0
        risk_level  = "DANGER (UNAUTHORIZED FORM POST)"
    # Rule C: Suspicious IP Address host
    elif features['has_ip'] and not is_trusted_domain(domain):
        is_phishing = True
        confidence  = 100.0
        risk_level  = "DANGER (SUSPICIOUS IP HOST)"
    # Rule D: Obvious Scam Keywords on suspicious TLD
    elif features['suspicious_word_count'] >= 2 and features['suspicious_tld']:
        is_phishing = True
        confidence  = 95.0
        risk_level  = "DANGER (PHISHING PATTERN)"
    # Rule E: Machine Learning & Hybrid Score Threshold
    elif hybrid_score >= 50.0:
        is_phishing = True
        confidence  = max(hybrid_score, 75.0)
        risk_level  = "DANGER" if hybrid_score >= 70.0 else "SUSPICIOUS (RISK DETECTED)"
    else:
        is_phishing = False
        # Clean Safe Confidence (calibrated between 85.0% and 99.5%)
        confidence  = round(max(85.0, 100.0 - hybrid_score), 2)
        risk_level  = "SAFE"

    threat_category = categorize_threat(url, content_res, is_phishing)

    resp = PredictionResponse(
        url=url,
        is_phishing=is_phishing,
        confidence=confidence,
        risk_level=risk_level,
        features=features,
        hybrid_score=hybrid_score,
        threat_category=threat_category,
        ssl_info=ssl_res,
        content_analysis=content_res
    )

    # Log to Database
    db.log_scan({
        "url": url,
        "is_phishing": is_phishing,
        "confidence": confidence,
        "risk_level": risk_level,
        "hybrid_score": hybrid_score,
        "client_type": client_type,
        "brand_detected": content_res.get("title_brand", ""),
        "scraped_title": content_res.get("page_title", ""),
        "threat_category": threat_category,
        "ssl_valid": ssl_res.get("valid", False)
    })

    return resp
