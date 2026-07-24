import re

def extract_features(url):
    """
    Extracts features from a URL for phishing detection.
    Features:
    - length: Length of the URL
    - has_https: 1 if https is in the URL, else 0
    - num_dots: Number of dots in the URL
    - has_ip: 1 if an IP address is present in the URL, else 0
    - has_special_chars: 1 if special characters (like @, -) are present, else 0
    """
    features = {}
    
    # 1. Length of URL
    features['length'] = len(url)
    
    # 2. Presence of HTTPS
    features['has_https'] = 1 if url.startswith('https://') else 0
    
    # 3. Number of dots
    features['num_dots'] = url.count('.')
    
    # 4. Presence of IP address
    # Regex to match IPv4 address
    ip_pattern = re.compile(r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]))')
    features['has_ip'] = 1 if ip_pattern.search(url) else 0
    
    # 5. Presence of special characters (@ or -)
    features['has_special_chars'] = 1 if '@' in url or '-' in url else 0
    
    return features
