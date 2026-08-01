// ==========================================
// CyberShield - Popup Script (v3.0)
// 30 Advanced Features
// ==========================================

const API_URL = "http://127.0.0.1:8000/predict";

document.addEventListener('DOMContentLoaded', function () {

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    let currentUrl = tabs[0].url;
    document.getElementById("current-url").innerText = currentUrl;
  });

  document.getElementById("scan-btn").addEventListener("click", function () {
    let statusBox     = document.getElementById("status-box");
    let statusIcon    = document.getElementById("status-icon");
    let statusMessage = document.getElementById("status-message");
    let confidenceText = document.getElementById("confidence-text");
    let featuresBox   = document.getElementById("features-box");
    let scanBtn       = document.getElementById("scan-btn");
    let urlToScan     = document.getElementById("current-url").innerText;

    // Scanning state
    statusBox.className       = "status-box status-scanning";
    statusIcon.innerText      = "...";
    statusMessage.innerText   = "Analyzing with AI Model (30 features)...";
    confidenceText.innerText  = "Please wait...";
    featuresBox.style.display = "none";
    scanBtn.disabled          = true;
    scanBtn.innerText         = "Scanning...";

    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: urlToScan })
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
    })
    .then(function() {
      scanBtn.disabled  = false;
      scanBtn.innerText = "Scan URL";
    });
  });
});
