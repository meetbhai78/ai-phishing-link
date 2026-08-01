import re
import math
from urllib.parse import urlparse
from collections import Counter

def extract_features(url):
    """
    Extracts 30 advanced features from a URL for phishing detection.
    CyberShield v3.0 - High Accuracy Model
    """
    features = {}

    # Safe URL parsing
    try:
        parsed = urlparse(url if '://' in url else 'http://' + url)
        domain = parsed.netloc.lower().replace('www.', '')
        path    = parsed.path   or ''
        query   = parsed.query  or ''
        scheme  = parsed.scheme or ''
    except Exception:
        domain, path, query, scheme = url, '', '', ''

    url_lower = url.lower()

    # ── Lexical / Length Features ──────────────────────────────────────
    # 1. Full URL length
    features['url_length'] = len(url)

    # 2. Domain length
    features['domain_length'] = len(domain)

    # 3. Path length
    features['path_length'] = len(path)

    # 4. Query string length
    features['query_length'] = len(query)

    # ── Protocol / Security ────────────────────────────────────────────
    # 5. HTTPS present
    features['has_https'] = 1 if scheme == 'https' else 0

    # 6. HTTP present (non-https)
    features['has_http'] = 1 if scheme == 'http' else 0

    # ── Count Features ─────────────────────────────────────────────────
    # 7. Number of dots
    features['num_dots'] = url.count('.')

    # 8. Number of dots in domain
    features['num_dots_domain'] = domain.count('.')

    # 9. Number of hyphens
    features['num_hyphens'] = url.count('-')

    # 10. Number of underscores
    features['num_underscores'] = url.count('_')

    # 11. Number of slashes
    features['num_slashes'] = url.count('/')

    # 12. Number of question marks
    features['num_question_marks'] = url.count('?')

    # 13. Number of equal signs
    features['num_equal_signs'] = url.count('=')

    # 14. Number of ampersands
    features['num_ampersands'] = url.count('&')

    # 15. Number of hash symbols
    features['num_hashes'] = url.count('#')

    # 16. Number of percent signs (URL encoding)
    features['num_percent'] = url.count('%')

    # 17. Number of digits in URL
    features['num_digits'] = sum(c.isdigit() for c in url)

    # 18. Digit-to-letter ratio
    letters = sum(c.isalpha() for c in url)
    digits  = features['num_digits']
    features['digit_to_letter_ratio'] = round(digits / (letters + 1), 4)

    # ── Subdomain Features ─────────────────────────────────────────────
    # 19. Number of subdomains
    parts = domain.split('.')
    features['num_subdomains'] = max(0, len(parts) - 2)

    # ── Suspicious Patterns ────────────────────────────────────────────
    # 20. Has IP address
    ip_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5]))'
    )
    features['has_ip'] = 1 if ip_pattern.search(url) else 0

    # 21. Has @ symbol
    features['has_at_symbol'] = 1 if '@' in url else 0

    # 22. Has double slash in path (not protocol)
    features['has_double_slash'] = 1 if '//' in url[7:] else 0

    # 23. Domain has hyphen (typosquatting indicator)
    features['domain_has_hyphen'] = 1 if '-' in domain else 0

    # 24. Suspicious keyword count
    suspicious_words = [
        'login', 'verify', 'account', 'secure', 'update', 'bank',
        'paypal', 'signin', 'confirm', 'password', 'suspend', 'alert',
        'wallet', 'free', 'lucky', 'winner', 'click', 'offer',
        'prize', 'credit', 'debit', 'billing', 'ebay', 'amazon',
        'support', 'service', 'urgent', 'limited', 'expire', 'reset'
    ]
    features['suspicious_word_count'] = sum(1 for w in suspicious_words if w in url_lower)

    # 25. Has 'http' in path/query (phishing trick: real domain after fake)
    features['http_in_path'] = 1 if 'http' in path.lower() or 'http' in query.lower() else 0

    # 26. Sensitive brand names in non-brand domains
    brands = ['paypal', 'amazon', 'google', 'facebook', 'apple', 'microsoft',
              'netflix', 'instagram', 'whatsapp', 'twitter', 'linkedin', 'ebay']
    domain_without_tld = '.'.join(parts[:-1]) if len(parts) > 1 else domain
    features['brand_in_subdomain'] = 1 if any(b in domain_without_tld for b in brands) else 0

    # 27. URL shortener detected
    shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly', 'short.link',
                  'tiny.cc', 'is.gd', 'buff.ly', 'rebrand.ly', 'shorte.st']
    features['is_shortened'] = 1 if any(s in url_lower for s in shorteners) else 0

    # ── Entropy / Randomness ───────────────────────────────────────────
    # 28. URL entropy (overall randomness)
    def entropy(text):
        if not text:
            return 0.0
        freq = Counter(text)
        n = len(text)
        return round(-sum((c/n) * math.log2(c/n) for c in freq.values()), 4)

    features['url_entropy'] = entropy(url)

    # 29. Domain entropy (random-looking domains are phishing)
    features['domain_entropy'] = entropy(domain)

    # ── TLD Feature ────────────────────────────────────────────────────
    # 30. Suspicious TLD
    suspicious_tlds = ['.xyz', '.top', '.club', '.online', '.site', '.info',
                       '.tk', '.ml', '.ga', '.cf', '.gq', '.pw', '.work',
                       '.click', '.link', '.download', '.loan', '.win']
    features['suspicious_tld'] = 1 if any(url_lower.endswith(t) or ('.' + t.strip('.') + '/') in url_lower
                                           for t in suspicious_tlds) else 0

    return features
