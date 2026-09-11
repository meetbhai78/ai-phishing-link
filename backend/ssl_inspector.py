"""
CyberShield - SSL Certificate & Security Inspector
Inspects TLS/SSL certificates using native Python ssl and socket libraries (No paid APIs).
"""
import ssl
import socket
import datetime
from urllib.parse import urlparse
from typing import Dict, Any

def inspect_ssl_certificate(url: str, timeout: float = 3.0) -> Dict[str, Any]:
    """
    Connects to HTTPS hostname and retrieves certificate metadata:
    - Validity status
    - Issuer Organization
    - Days until expiration
    - Self-signed flag
    """
    try:
        parsed = urlparse(url if '://' in url else 'http://' + url)
        hostname = parsed.netloc.split(':')[0]
        scheme = parsed.scheme.lower()
    except Exception:
        hostname = url
        scheme = 'http'

    result = {
        "has_ssl": scheme == "https",
        "valid": False,
        "issuer": "None",
        "subject": hostname,
        "days_remaining": 0,
        "is_self_signed": False,
        "details": "Non-HTTPS URL"
    }

    if scheme != "https" or not hostname:
        return result

    try:
        context = ssl.create_default_context()
        context.timeout = timeout
        
        with socket.create_connection((hostname, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Expiry Calculation
                not_after_str = cert.get('notAfter')
                if not_after_str:
                    # Format: 'May 26 12:00:00 2026 GMT'
                    expiry_date = datetime.datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z').replace(tzinfo=datetime.timezone.utc)
                    days_remaining = (expiry_date - datetime.datetime.now(datetime.timezone.utc)).days
                else:
                    days_remaining = 0

                # Extract Issuer Org
                issuer_dict = dict(x[0] for x in cert.get('issuer', []))
                issuer_org = issuer_dict.get('organizationName') or issuer_dict.get('commonName', 'Unknown Issuer')

                # Extract Subject Org
                subject_dict = dict(x[0] for x in cert.get('subject', []))
                subject_org = subject_dict.get('organizationName') or subject_dict.get('commonName', hostname)

                is_self_signed = issuer_dict == subject_dict

                result["valid"] = True
                result["issuer"] = str(issuer_org)
                result["subject"] = str(subject_org)
                result["days_remaining"] = max(0, days_remaining)
                result["is_self_signed"] = is_self_signed
                result["details"] = f"Valid SSL ({issuer_org}, {days_remaining}d remaining)"
                return result

    except ssl.SSLCertVerificationError as e:
        result["valid"] = False
        result["details"] = f"SSL Verification Failed: {e.verify_message}"
        result["is_self_signed"] = "self-signed" in str(e).lower()
        return result
    except Exception as e:
        result["valid"] = False
        result["details"] = f"Could not establish SSL handshake: {str(e)[:60]}"
        return result
