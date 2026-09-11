import re
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

# Major Known Brands for Brand Impersonation Check
POPULAR_BRANDS = {
    'paypal': ['paypal.com'],
    'amazon': ['amazon.com', 'amazon.in', 'aws.amazon.com'],
    'google': ['google.com', 'accounts.google.com', 'gmail.com'],
    'facebook': ['facebook.com', 'fb.com'],
    'apple': ['apple.com', 'icloud.com'],
    'microsoft': ['microsoft.com', 'outlook.com', 'live.com', 'office.com'],
    'netflix': ['netflix.com'],
    'instagram': ['instagram.com'],
    'whatsapp': ['whatsapp.com'],
    'twitter': ['twitter.com', 'x.com'],
    'linkedin': ['linkedin.com'],
    'sbi': ['sbi.co.in', 'onlinesbi.sbi'],
    'hdfc': ['hdfcbank.com'],
    'icici': ['icicibank.com'],
    'paytm': ['paytm.com'],
}

SUSPICIOUS_CONTENT_KEYWORDS = [
    'login to your account', 'verify your account', 'update billing',
    'confirm password', 'account suspended', 'urgent action required',
    'security alert', 'unauthorized access', 'verify identity',
    'enter credit card', 'unusual activity', 'claim prize', 'congratulations winner'
]

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'en-US,en;q=0.9',
}

import socket

def fetch_webpage_html(url: str, timeout: float = 1.5) -> tuple[str, bool, str]:
    """
    Robot Web Scraper: Safely fetches target URL HTML within 1.5s timeout.
    Pre-checks DNS resolution so non-existent domains fail instantly (<0.1s).
    """
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    try:
        parsed_url = urlparse(url)
        host_domain = parsed_url.netloc.split(':')[0]

        # Fast DNS check to avoid 10s Windows DNS hang
        socket.setdefaulttimeout(1.5)
        socket.gethostbyname(host_domain)
    except Exception as e:
        return "", False, f"Domain DNS Lookup Failed (Offline): {str(e)}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            return response.text, True, "OK"
        else:
            return "", False, f"HTTP Status {response.status_code}"
    except requests.exceptions.Timeout:
        return "", False, "Request Timeout (Site offline/slow)"
    except requests.exceptions.RequestException as e:
        return "", False, f"Connection Failed: {str(e)}"
    except Exception as e:
        return "", False, f"Error: {str(e)}"


def analyze_webpage_content(url: str, html: str) -> dict:
    """
    Inspects HTML DOM for phishing indicators:
    - Password inputs
    - External form posting actions
    - Brand mismatch in title/headings
    - Suspicious credential-harvesting text
    - Null / hash link clutter
    """
    risk_signals = []
    content_risk_score = 0.0

    try:
        parsed_url = urlparse(url if '://' in url else 'http://' + url)
        host_domain = parsed_url.netloc.lower().replace('www.', '')
    except Exception:
        host_domain = url.lower()

    if not html:
        return {
            "scraped_successfully": False,
            "has_password_field": False,
            "external_form_action": False,
            "brand_mismatch": None,
            "suspicious_keywords": [],
            "content_risk_score": 0.0,
            "risk_signals": ["Page could not be scraped (offline or timed out)"]
        }

    soup = BeautifulSoup(html, 'html.parser')

    # 1. Password Field Detection
    password_inputs = soup.find_all('input', {'type': re.compile(r'password', re.I)})
    has_password_field = len(password_inputs) > 0
    if has_password_field:
        content_risk_score += 25.0
        risk_signals.append("Password input field detected on page")

    # 2. Form Actions & External Form Submissions
    forms = soup.find_all('form')
    external_form_action = False
    for form in forms:
        action = form.get('action', '')
        if action:
            action_url = urljoin(url, action)
            try:
                action_domain = urlparse(action_url).netloc.lower().replace('www.', '')
                if action_domain and action_domain != host_domain and not host_domain.endswith(action_domain):
                    external_form_action = True
                    break
            except Exception:
                pass

    if external_form_action:
        content_risk_score += 35.0
        risk_signals.append("Form submits sensitive data to an EXTERNAL domain")

    # 3. Brand Impersonation Check (Title & Headings vs Host Domain)
    page_title = soup.title.string.strip() if soup.title and soup.title.string else ""
    headings_text = " ".join([h.get_text() for h in soup.find_all(['h1', 'h2'])])
    combined_head_text = (page_title + " " + headings_text).lower()

    detected_brand_mismatch = None
    for brand, official_domains in POPULAR_BRANDS.items():
        if brand in combined_head_text:
            # Brand mentioned in title/heading, check if host_domain is official
            is_official = any(host_domain == d or host_domain.endswith('.' + d) for d in official_domains)
            if not is_official:
                detected_brand_mismatch = f"Brand '{brand.capitalize()}' in title/heading, but host is '{host_domain}'"
                content_risk_score += 40.0
                risk_signals.append(f"BRAND IMPERSONATION: {detected_brand_mismatch}")
                break

    # 4. Credential Harvesting & Suspicious Keywords
    page_text = soup.get_text().lower()
    found_keywords = [kw for kw in SUSPICIOUS_CONTENT_KEYWORDS if kw in page_text]
    if found_keywords:
        kw_score = min(20.0, len(found_keywords) * 7.0)
        content_risk_score += kw_score
        risk_signals.append(f"Suspicious phrases found: {', '.join(found_keywords[:3])}")

    # 5. Link Structure (Empty / Hash links)
    links = soup.find_all('a', href=True)
    total_links = len(links)
    empty_links = sum(1 for a in links if a['href'].strip() in ['#', '#javascript:void(0)', 'javascript:void(0);', ''])
    if total_links > 5 and (empty_links / total_links) > 0.5:
        content_risk_score += 15.0
        risk_signals.append(f"High percentage of suspicious/null links ({empty_links}/{total_links})")

    # Cap content risk score at 100%
    content_risk_score = min(100.0, round(content_risk_score, 2))

    return {
        "scraped_successfully": True,
        "has_password_field": has_password_field,
        "external_form_action": external_form_action,
        "brand_mismatch": detected_brand_mismatch,
        "suspicious_keywords": found_keywords,
        "content_risk_score": content_risk_score,
        "risk_signals": risk_signals
    }
