// ==========================================
// CyberShield - Popup Script (v3.7)
// 30 Features + Robot + SSL + Threat Category
// ==========================================

const API_URL = "http://127.0.0.1:8000/predict";

document.addEventListener('DOMContentLoaded', function () {

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    if (tabs && tabs.length > 0) {
      let currentUrl = tabs[0].url;
      document.getElementById("current-url").innerText = currentUrl;
    }
  });

  document.getElementById("scan-btn").addEventListener("click", function () {
    let statusBox      = document.getElementById("status-box");
    let statusIcon     = document.getElementById("status-icon");
    let statusMessage  = document.getElementById("status-message");
    let confidenceText = document.getElementById("confidence-text");
    let categoryBadge  = document.getElementById("category-badge");
    let sslBox         = document.getElementById("ssl-box");
    let featuresBox    = document.getElementById("features-box");
    let robotBox       = document.getElementById("robot-box");
    let robotSignals   = document.getElementById("robot-signals-box");
    let scanBtn        = document.getElementById("scan-btn");
    let urlToScan      = document.getElementById("current-url").innerText;

    // Scanning state
    statusBox.className        = "status-box status-scanning";
    statusIcon.innerText       = "🤖";
    statusMessage.innerText    = "Analyzing URL, SSL & Webpage Content...";
    confidenceText.innerText   = "Please wait...";
    if (categoryBadge) categoryBadge.style.display = "none";
    if (sslBox) sslBox.style.display = "none";
    featuresBox.style.display  = "none";
    if (robotBox) robotBox.style.display = "none";
    scanBtn.disabled           = true;
    scanBtn.innerText          = "Scanning...";

    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlToScan, client_type: "extension" })
    })
    .then(function(response) {
      if (!response.ok) throw new Error("Server error: " + response.status);
      return response.json();
    })
    .then(function(data) {
      if (data.is_phishing) {
        statusBox.className      = "status-box status-danger";
        statusIcon.innerText     = "DANGER";
        statusMessage.innerText  = "WARNING: PHISHING DETECTED!";
      } else {
        statusBox.className      = "status-box status-safe";
        statusIcon.innerText     = "SAFE";
        statusMessage.innerText  = "Website is SAFE";
      }
      confidenceText.innerText = "Confidence: " + data.confidence + "% | " + data.risk_level;

      // Render Threat Category
      if (categoryBadge && data.threat_category) {
        categoryBadge.innerText = "🏷️ Category: " + data.threat_category;
        categoryBadge.style.display = "inline-block";
      }

      // Render SSL Inspector Card
      if (sslBox && data.ssl_info) {
        let ssl = data.ssl_info;
        document.getElementById("ssl-status").innerText = ssl.valid ? "✅ Valid & Trusted" : (ssl.has_ssl ? "⚠️ Invalid / Handshake Error" : "❌ No HTTPS");
        document.getElementById("ssl-issuer").innerText = ssl.issuer || "None";
        document.getElementById("ssl-expiry").innerText = ssl.valid ? (ssl.days_remaining + " days left") : ssl.details;
        sslBox.style.display = "block";
      }

      // Render Robot Webpage Inspection
      if (data.content_analysis && robotBox) {
        let ca = data.content_analysis;
        var setEl = function(id, val) {
          var el = document.getElementById(id);
          if (el) el.innerText = val;
        };
        setEl("robot-pwd",   ca.has_password_field ? "DETECTED (Risk)" : "None");
        setEl("robot-form",  ca.external_form_action ? "UNAUTHORIZED POST" : "Safe / Internal");
        setEl("robot-brand", ca.brand_mismatch ? ca.brand_mismatch : "Verified / Clean");
        setEl("robot-score", ca.content_risk_score + "%");

        if (robotSignals) {
          robotSignals.innerHTML = "";
          if (ca.risk_signals && ca.risk_signals.length > 0) {
            ca.risk_signals.forEach(function(sig) {
              let tag = document.createElement("span");
              tag.className = "robot-signal-tag";
              tag.innerText = "⚠️ " + sig;
              robotSignals.appendChild(tag);
            });
          }
        }
        robotBox.style.display = "block";
      }

      if (data.features) {
        var f = data.features;
        var setEl = function(id, val) {
          var el = document.getElementById(id);
          if (el) el.innerText = val;
        };
        setEl("feat-url-length",    f.url_length);
        setEl("feat-domain-length", f.domain_length);
        setEl("feat-path-length",   f.path_length);
        setEl("feat-query-length",  f.query_length);
        setEl("feat-https",         f.has_https ? "Yes (Safe)" : "No (Risk)");
        setEl("feat-dots",          f.num_dots);
        setEl("feat-dots-domain",   f.num_dots_domain);
        setEl("feat-hyphens",       f.num_hyphens);
        setEl("feat-underscores",   f.num_underscores);
        setEl("feat-slashes",       f.num_slashes);
        setEl("feat-digits",        f.num_digits);
        setEl("feat-digit-ratio",   f.digit_to_letter_ratio);
        setEl("feat-subdomains",    f.num_subdomains);
        setEl("feat-ip",            f.has_ip ? "Yes (Risk)" : "No (Safe)");
        setEl("feat-at",            f.has_at_symbol ? "Yes (Risk)" : "No (Safe)");
        setEl("feat-double-slash",  f.has_double_slash ? "Yes (Risk)" : "No (Safe)");
        setEl("feat-domain-hyphen", f.domain_has_hyphen ? "Yes" : "No");
        setEl("feat-suspicious",    f.suspicious_word_count);
        setEl("feat-http-path",     f.http_in_path ? "Yes (Risk)" : "No (Safe)");
        setEl("feat-brand",         f.brand_in_subdomain ? "Yes (Risk)" : "No (Safe)");
        setEl("feat-shortened",     f.is_shortened ? "Yes (Risk)" : "No (Safe)");
        setEl("feat-url-entropy",   f.url_entropy);
        setEl("feat-domain-entropy",f.domain_entropy);
        setEl("feat-suspicious-tld",f.suspicious_tld ? "Yes (Risk)" : "No (Safe)");
        featuresBox.style.display = "block";
      }
    })
    .catch(function(error) {
      console.error("CyberShield API Error:", error);
      statusBox.className       = "status-box status-error";
      statusIcon.innerText      = "OFFLINE";
      statusMessage.innerText   = "Server Offline";
      confidenceText.innerText  = "Run: uvicorn backend.main:app --reload";
      featuresBox.style.display = "none";
      if (robotBox) robotBox.style.display = "none";
      if (sslBox) sslBox.style.display = "none";
    })
    .then(function() {
      scanBtn.disabled  = false;
      scanBtn.innerText = "Scan URL & Webpage";
    });
  });
});
