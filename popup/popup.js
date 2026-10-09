// ==========================================
// CyberShield - Popup Script (v4.0)
// 30 Features + Robot + SSL + Report + History
// ==========================================

const API_BASE = "http://127.0.0.1:8000";
const API_URL = API_BASE + "/predict";

document.addEventListener('DOMContentLoaded', function () {

  // Load current tab URL
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    if (tabs && tabs.length > 0) {
      let currentUrl = tabs[0].url;
      document.getElementById("current-url").innerText = currentUrl;
      // Pre-fill report URL with current tab
      var reportInput = document.getElementById("report-url-input");
      if (reportInput) reportInput.value = currentUrl;
    }
  });

  // Load scan history
  loadScanHistory();

  // ==============================
  // SCAN BUTTON
  // ==============================
  document.getElementById("scan-btn").addEventListener("click", function () {
    var statusBox      = document.getElementById("status-box");
    var statusIcon     = document.getElementById("status-icon");
    var statusMessage  = document.getElementById("status-message");
    var confidenceText = document.getElementById("confidence-text");
    var categoryBadge  = document.getElementById("category-badge");
    var sslBox         = document.getElementById("ssl-box");
    var featuresBox    = document.getElementById("features-box");
    var robotBox       = document.getElementById("robot-box");
    var robotSignals   = document.getElementById("robot-signals-box");
    var scanBtn        = document.getElementById("scan-btn");
    var urlToScan      = document.getElementById("current-url").innerText;

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
    scanBtn.innerText          = "⚡ Scanning...";

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
        statusIcon.innerText     = "⚠️ DANGER";
        statusMessage.innerText  = "WARNING: PHISHING DETECTED!";
      } else {
        statusBox.className      = "status-box status-safe";
        statusIcon.innerText     = "✅ SAFE";
        statusMessage.innerText  = "Website is SAFE";
      }
      confidenceText.innerText = "Confidence: " + data.confidence + "% | " + data.risk_level;

      // Render Threat Category
      if (categoryBadge && data.threat_category) {
        categoryBadge.innerText = "🏷️ " + data.threat_category;
        categoryBadge.style.display = "inline-block";
      }

      // Render SSL Inspector Card
      if (sslBox && data.ssl_info) {
        var ssl = data.ssl_info;
        document.getElementById("ssl-status").innerText = ssl.valid ? "✅ Valid & Trusted" : (ssl.has_ssl ? "⚠️ Invalid / Handshake Error" : "❌ No HTTPS");
        document.getElementById("ssl-issuer").innerText = ssl.issuer || "None";
        document.getElementById("ssl-expiry").innerText = ssl.valid ? (ssl.days_remaining + " days left") : ssl.details;
        sslBox.style.display = "block";
      }

      // Render Robot Webpage Inspection
      if (data.content_analysis && robotBox) {
        var ca = data.content_analysis;
        var setEl = function(id, val) {
          var el = document.getElementById(id);
          if (el) el.innerText = val;
        };
        setEl("robot-pwd",   ca.has_password_field ? "🔴 DETECTED (Risk)" : "🟢 None");
        setEl("robot-form",  ca.external_form_action ? "🔴 UNAUTHORIZED POST" : "🟢 Safe / Internal");
        setEl("robot-brand", ca.brand_mismatch ? "🔴 " + ca.brand_mismatch : "🟢 Verified / Clean");
        setEl("robot-score", ca.content_risk_score + "%");

        if (robotSignals) {
          robotSignals.innerHTML = "";
          if (ca.risk_signals && ca.risk_signals.length > 0) {
            ca.risk_signals.forEach(function(sig) {
              var tag = document.createElement("span");
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
        var setF = function(id, val) {
          var el = document.getElementById(id);
          if (el) el.innerText = val;
        };
        setF("feat-url-length",    f.url_length);
        setF("feat-domain-length", f.domain_length);
        setF("feat-path-length",   f.path_length);
        setF("feat-query-length",  f.query_length);
        setF("feat-https",         f.has_https ? "Yes ✅" : "No ❌");
        setF("feat-dots",          f.num_dots);
        setF("feat-dots-domain",   f.num_dots_domain);
        setF("feat-hyphens",       f.num_hyphens);
        setF("feat-underscores",   f.num_underscores);
        setF("feat-slashes",       f.num_slashes);
        setF("feat-digits",        f.num_digits);
        setF("feat-digit-ratio",   f.digit_to_letter_ratio);
        setF("feat-subdomains",    f.num_subdomains);
        setF("feat-ip",            f.has_ip ? "Yes ❌" : "No ✅");
        setF("feat-at",            f.has_at_symbol ? "Yes ❌" : "No ✅");
        setF("feat-double-slash",  f.has_double_slash ? "Yes ❌" : "No ✅");
        setF("feat-domain-hyphen", f.domain_has_hyphen ? "Yes" : "No");
        setF("feat-suspicious",    f.suspicious_word_count);
        setF("feat-http-path",     f.http_in_path ? "Yes ❌" : "No ✅");
        setF("feat-brand",         f.brand_in_subdomain ? "Yes ❌" : "No ✅");
        setF("feat-shortened",     f.is_shortened ? "Yes ❌" : "No ✅");
        setF("feat-url-entropy",   f.url_entropy);
        setF("feat-domain-entropy",f.domain_entropy);
        setF("feat-suspicious-tld",f.suspicious_tld ? "Yes ❌" : "No ✅");
        featuresBox.style.display = "block";
      }

      // Save to scan history (chrome.storage)
      saveScanToHistory({
        url: urlToScan,
        is_phishing: data.is_phishing,
        confidence: data.confidence,
        risk_level: data.risk_level,
        timestamp: new Date().toISOString()
      });
    })
    .catch(function(error) {
      console.error("CyberShield API Error:", error);
      statusBox.className       = "status-box status-error";
      statusIcon.innerText      = "🔌 OFFLINE";
      statusMessage.innerText   = "Server Offline";
      confidenceText.innerText  = "Run: uvicorn backend.main:app --reload";
      featuresBox.style.display = "none";
      if (robotBox) robotBox.style.display = "none";
      if (sslBox) sslBox.style.display = "none";
    })
    .finally(function() {
      scanBtn.disabled  = false;
      scanBtn.innerText = "🔍 Scan URL & Webpage";
    });
  });

  // ==============================
  // REPORT SECTION
  // ==============================
  var reportToggleBtn = document.getElementById("report-toggle-btn");
  var reportForm      = document.getElementById("report-form");
  var reportUrlInput  = document.getElementById("report-url-input");
  var submitReportBtn = document.getElementById("submit-report-btn");
  var reportStatus    = document.getElementById("report-status");
  var selectedLabel   = "";
  var questionAnswers = {};

  // Toggle report form
  reportToggleBtn.addEventListener("click", function() {
    reportForm.classList.toggle("active");
    if (reportForm.classList.contains("active")) {
      reportToggleBtn.innerText = "✖ Close Report Form";
      loadQuestions();
    } else {
      reportToggleBtn.innerText = "🚨 Report Suspicious Link";
    }
  });

  // Label Selector Chips
  document.querySelectorAll(".label-chip").forEach(function(chip) {
    chip.addEventListener("click", function() {
      // Remove all selected classes
      document.querySelectorAll(".label-chip").forEach(function(c) {
        c.classList.remove("selected-phishing", "selected-safe", "selected-unsure");
      });
      selectedLabel = this.getAttribute("data-label");
      this.classList.add("selected-" + selectedLabel);
      updateSubmitState();
    });
  });

  function updateSubmitState() {
    submitReportBtn.disabled = !(selectedLabel && reportUrlInput.value.trim());
  }

  reportUrlInput.addEventListener("input", updateSubmitState);

  // Load AI Training Questions from server
  function loadQuestions() {
    var container = document.getElementById("questions-container");
    container.innerHTML = '<p style="font-size:10px; color:#4a5568; text-align:center;">Loading questions...</p>';

    fetch(API_BASE + "/api/community-questions")
      .then(function(r) { return r.json(); })
      .then(function(data) {
        container.innerHTML = "";
        if (!data.questions || data.questions.length === 0) return;

        data.questions.forEach(function(q, idx) {
          var card = document.createElement("div");
          card.className = "question-card";
          card.innerHTML =
            '<div class="q-title">' +
              '<span>' + q.question + '</span>' +
              '<span class="q-number">Q' + (idx + 1) + '</span>' +
            '</div>' +
            '<div class="q-options" data-qid="' + q.id + '"></div>';

          var optionsDiv = card.querySelector(".q-options");

          q.options.forEach(function(opt) {
            var chip = document.createElement("span");
            chip.className = "q-option-chip";
            chip.innerText = opt;
            chip.addEventListener("click", function() {
              // Deselect siblings
              optionsDiv.querySelectorAll(".q-option-chip").forEach(function(c) {
                c.classList.remove("selected");
              });
              optionsDiv.querySelector(".q-skip-btn").classList.remove("skipped");
              this.classList.add("selected");
              questionAnswers[q.id] = opt;
            });
            optionsDiv.appendChild(chip);
          });

          // Skip button
          var skipBtn = document.createElement("span");
          skipBtn.className = "q-skip-btn";
          skipBtn.innerText = "Skip";
          skipBtn.addEventListener("click", function() {
            optionsDiv.querySelectorAll(".q-option-chip").forEach(function(c) {
              c.classList.remove("selected");
            });
            this.classList.add("skipped");
            questionAnswers[q.id] = "skipped";
          });
          optionsDiv.appendChild(skipBtn);

          container.appendChild(card);
        });
      })
      .catch(function() {
        container.innerHTML = '<p style="font-size:10px; color:#4a5568; text-align:center;">Could not load questions (server offline)</p>';
      });
  }

  // Submit Report
  submitReportBtn.addEventListener("click", function() {
    var url = reportUrlInput.value.trim();
    if (!url || !selectedLabel) return;

    submitReportBtn.disabled = true;
    submitReportBtn.innerText = "⏳ Submitting...";
    reportStatus.className = "report-status";
    reportStatus.style.display = "none";

    // Filter out skipped answers for cleaner data
    var cleanAnswers = {};
    for (var key in questionAnswers) {
      if (questionAnswers[key] !== "skipped") {
        cleanAnswers[key] = questionAnswers[key];
      }
    }

    fetch(API_BASE + "/api/community-report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: url,
        user_reported_label: selectedLabel,
        questions_answers: cleanAnswers,
        source: "extension"
      })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.success) {
        reportStatus.className = "report-status success";
        reportStatus.innerText = "✅ Report submitted! Thank you for helping train our AI.";
        // Reset form
        selectedLabel = "";
        questionAnswers = {};
        document.querySelectorAll(".label-chip").forEach(function(c) {
          c.classList.remove("selected-phishing", "selected-safe", "selected-unsure");
        });
      } else {
        reportStatus.className = "report-status error";
        reportStatus.innerText = "❌ Error: " + (data.detail || "Failed to submit");
      }
    })
    .catch(function(err) {
      reportStatus.className = "report-status error";
      reportStatus.innerText = "❌ Server offline. Please try again.";
    })
    .finally(function() {
      submitReportBtn.disabled = false;
      submitReportBtn.innerText = "📤 Submit Report";
    });
  });

  // ==============================
  // SCAN HISTORY (chrome.storage.local)
  // ==============================
  function saveScanToHistory(scanData) {
    chrome.storage.local.get({ scan_history: [] }, function(result) {
      var history = result.scan_history;
      history.unshift(scanData);
      // Keep only last 10
      if (history.length > 10) history = history.slice(0, 10);
      chrome.storage.local.set({ scan_history: history }, function() {
        renderScanHistory(history);
      });
    });
  }

  function loadScanHistory() {
    chrome.storage.local.get({ scan_history: [] }, function(result) {
      renderScanHistory(result.scan_history);
    });
  }

  function renderScanHistory(history) {
    var listEl = document.getElementById("history-list");
    if (!history || history.length === 0) {
      listEl.innerHTML = '<div class="history-empty">No scans yet. Scan a URL to start.</div>';
      return;
    }

    listEl.innerHTML = "";
    // Show last 5
    var shown = history.slice(0, 5);
    shown.forEach(function(item) {
      var div = document.createElement("div");
      div.className = "history-item";

      var badge = document.createElement("span");
      badge.className = "history-badge " + (item.is_phishing ? "danger" : "safe");
      badge.innerText = item.is_phishing ? "RISK" : "SAFE";

      var urlSpan = document.createElement("span");
      urlSpan.className = "history-url";
      // Truncate URL for display
      var displayUrl = item.url;
      if (displayUrl.length > 40) displayUrl = displayUrl.substring(0, 40) + "...";
      urlSpan.innerText = displayUrl;

      var timeSpan = document.createElement("span");
      timeSpan.className = "history-time";
      timeSpan.innerText = formatTimeAgo(item.timestamp);

      div.appendChild(badge);
      div.appendChild(urlSpan);
      div.appendChild(timeSpan);
      listEl.appendChild(div);
    });
  }

  function formatTimeAgo(isoStr) {
    try {
      var d = new Date(isoStr);
      var now = new Date();
      var diff = Math.floor((now - d) / 1000);
      if (diff < 60) return "just now";
      if (diff < 3600) return Math.floor(diff / 60) + "m ago";
      if (diff < 86400) return Math.floor(diff / 3600) + "h ago";
      return Math.floor(diff / 86400) + "d ago";
    } catch (e) {
      return "";
    }
  }
});
