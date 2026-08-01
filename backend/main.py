import os
import re
import math
import joblib
import pandas as pd
from urllib.parse import urlparse
from collections import Counter
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ==========================================
# CyberShield - FastAPI Prediction Backend
# v3.0 - 30 Advanced Features
# ==========================================

app = FastAPI(
    title="CyberShield Prediction API",
    description="AI-Based Real-Time Phishing Detection API",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# Trusted Domains Whitelist
# ==========================================
TRUSTED_TLDS    = ['.gov.in', '.edu.in', '.ac.in', '.gov', '.edu', '.mil', '.nic.in']
TRUSTED_DOMAINS = [
    'google.com', 'youtube.com', 'facebook.com', 'amazon.com', 'amazon.in',
    'github.com', 'linkedin.com', 'microsoft.com', 'apple.com', 'twitter.com',
    'instagram.com', 'wikipedia.org', 'reddit.com', 'stackoverflow.com',
    'netflix.com', 'flipkart.com', 'whatsapp.com', 'telegram.org',
    'mygov.in', 'india.gov.in', 'nic.in', 'irctc.co.in',
    'charusat.ac.in', 'gmail.com', 'outlook.com', 'yahoo.com',
    'paytm.com', 'phonepe.com', 'gpay.com', 'nsdl.co.in', 'sbi.co.in',
    'hdfcbank.com', 'icicibank.com', 'axisbank.com',
    'render.com', 'heroku.com', 'vercel.com', 'netlify.com', 'railway.app',
    'aws.amazon.com', 'cloud.google.com', 'azure.microsoft.com',
    'digitalocean.com', 'cloudflare.com', 'firebase.google.com',
]

def is_trusted_domain(domain: str) -> bool:
    domain = domain.lower()
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

    # Digit features
    digits  = sum(c.isdigit() for c in url)
    letters = sum(c.isalpha() for c in url)
    features['num_digits']           = digits
    features['digit_to_letter_ratio'] = round(digits / (letters + 1), 4)

    # Subdomain
    parts = domain.split('.')
    features['num_subdomains'] = max(0, len(parts) - 2)

    # IP address
    ip_pat = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5]))'
    )
    features['has_ip']          = 1 if ip_pat.search(url) else 0
    features['has_at_symbol']   = 1 if '@' in url else 0
    features['has_double_slash'] = 1 if '//' in url[7:] else 0
    features['domain_has_hyphen'] = 1 if '-' in domain else 0

    suspicious_words = [
        'login','verify','account','secure','update','bank','paypal','signin',
        'confirm','password','suspend','alert','wallet','free','lucky','winner',
        'click','offer','prize','credit','debit','billing','ebay','amazon',
        'support','service','urgent','limited','expire','reset'
    ]
    features['suspicious_word_count'] = sum(1 for w in suspicious_words if w in url_lower)
    features['http_in_path'] = 1 if 'http' in path.lower() or 'http' in query.lower() else 0

    brands = ['paypal','amazon','google','facebook','apple','microsoft',
              'netflix','instagram','whatsapp','twitter','linkedin','ebay']
    domain_without_tld = '.'.join(parts[:-1]) if len(parts) > 1 else domain
    features['brand_in_subdomain'] = 1 if any(b in domain_without_tld for b in brands) else 0

    shorteners = ['bit.ly','tinyurl','goo.gl','t.co','ow.ly','short.link',
                  'tiny.cc','is.gd','buff.ly','rebrand.ly','shorte.st']
    features['is_shortened'] = 1 if any(s in url_lower for s in shorteners) else 0

    def entropy(text):
        if not text: return 0.0
        freq = Counter(text)
        n = len(text)
        return round(-sum((c/n)*math.log2(c/n) for c in freq.values()), 4)

    features['url_entropy']    = entropy(url)
    features['domain_entropy'] = entropy(domain)

    suspicious_tlds = ['.xyz','.top','.club','.online','.site','.info',
                       '.tk','.ml','.ga','.cf','.gq','.pw','.work',
                       '.click','.link','.download','.loan','.win']
    features['suspicious_tld'] = 1 if any(
        url_lower.endswith(t) or ('.' + t.strip('.') + '/') in url_lower
        for t in suspicious_tlds
    ) else 0

    return features

# ==========================================
# Pydantic Models
# ==========================================
class URLRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    url: str
    is_phishing: bool
    confidence: float
    risk_level: str
    features: dict

# ==========================================
# Endpoints
# ==========================================
@app.get("/")
def root():
    return {
        "status": "online",
        "service": "CyberShield Prediction API",
        "version": "3.0.0",
        "model_loaded": model is not None,
        "features_count": 30
    }

@app.post("/predict", response_model=PredictionResponse)
def predict_url(request: URLRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="ML Model not loaded.")

    url = request.url.strip()
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    features = extract_features(url)

    if is_trusted_domain(domain):
        return PredictionResponse(
            url=url, is_phishing=False, confidence=100.0,
            risk_level="SAFE (VERIFIED DOMAIN)", features=features
        )

    feature_df    = pd.DataFrame([features])
    probabilities = model.predict_proba(feature_df)[0]
    
    # probabilities[0] = P(Safe), probabilities[1] = P(Phishing)
    phishing_prob = probabilities[1]
    safe_prob     = probabilities[0]
    
    # ==========================================
    # Confidence Threshold: 70%
    # Only flag as DANGER if model is >70% sure
    # This reduces false positives on legit sites
    # ==========================================
    PHISHING_THRESHOLD = 0.70
    
    if phishing_prob >= PHISHING_THRESHOLD:
        is_phishing = True
        confidence  = round(phishing_prob * 100, 2)
        risk_level  = "DANGER"
    else:
        is_phishing = False
        confidence  = round(safe_prob * 100, 2)
        risk_level  = "SAFE"
    
    return PredictionResponse(
        url=url,
        is_phishing=is_phishing,
        confidence=confidence,
        risk_level=risk_level,
        features=features
    )
