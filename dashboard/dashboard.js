let pieChart = null;
let barChart = null;
let allScans = [];
let allRules = [];

const API_BASE = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function () {
  fetchStats();
  fetchRecentScans();
  fetchRules();
  fetchMetrics();

  // Auto-refresh every 10 seconds
  setInterval(() => {
    fetchStats();
    fetchRecentScans();
    fetchRules();
  }, 10000);

  // Search filter
  document.getElementById("scan-search").addEventListener("input", function (e) {
    const query = e.target.value.toLowerCase();
    const filtered = allScans.filter(s => 
      s.url.toLowerCase().includes(query) || 
      (s.risk_level && s.risk_level.toLowerCase().includes(query)) ||
      (s.threat_category && s.threat_category.toLowerCase().includes(query)) ||
      (s.brand_detected && s.brand_detected.toLowerCase().includes(query))
    );
    renderTable(filtered);
  });
});

async function fetchStats() {
  try {
    const res = await fetch(`${API_BASE}/api/stats`);
    if (!res.ok) throw new Error("Network response was not ok");
    const data = await res.json();

    document.getElementById("stat-total").innerText = data.total_scans.toLocaleString();
    document.getElementById("stat-phishing").innerText = data.phishing_detected.toLocaleString();
    document.getElementById("stat-safe").innerText = data.safe_sites.toLocaleString();
    document.getElementById("stat-today").innerText = data.today_scans.toLocaleString();
    document.getElementById("db-status-text").innerText = data.database_mode;

    updateCharts(data.safe_sites, data.phishing_detected);
  } catch (err) {
    console.error("Error fetching stats:", err);
  }
}

async function fetchRecentScans() {
  try {
    const res = await fetch(`${API_BASE}/api/scans?limit=100`);
    if (!res.ok) throw new Error("Network response was not ok");
    allScans = await res.json();
    renderTable(allScans);
  } catch (err) {
    console.error("Error fetching scans:", err);
  }
}

function renderTable(scans) {
  const tbody = document.getElementById("scans-table-body");
  if (!scans || scans.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-muted); padding: 24px;">No scan records found. Run a scan from the Extension, App, or Dashboard to see logs.</td></tr>`;
    return;
  }

  tbody.innerHTML = scans.map(s => {
    const isPhish = s.is_phishing;
    const badgeClass = isPhish ? "badge-danger" : "badge-safe";
    const badgeText = isPhish ? "PHISHING" : "SAFE";
    const dateFormatted = s.timestamp ? new Date(s.timestamp).toLocaleTimeString() + ", " + new Date(s.timestamp).toLocaleDateString() : "-";
    const client = s.client_type ? s.client_type.toUpperCase() : "EXTENSION";
    const category = s.threat_category || (isPhish ? "Generic Suspicious" : "Clean Domain");
    const sslBadge = s.ssl_valid 
      ? `<span class="ssl-pill ssl-valid">🔒 Valid</span>` 
      : `<span class="ssl-pill ssl-invalid">⚠️ No SSL / Risk</span>`;

    return `
      <tr>
        <td class="url-cell" title="${escapeHtml(s.url)}">${escapeHtml(s.url)}</td>
        <td><span class="badge ${badgeClass}">${badgeText}</span></td>
        <td><span class="category-pill">${escapeHtml(category)}</span></td>
        <td>${sslBadge}</td>
        <td><strong>${s.confidence || 0}%</strong></td>
        <td><span class="badge badge-source">${client}</span></td>
        <td style="color: var(--text-muted); font-size: 12px;">${dateFormatted}</td>
      </tr>
    `;
  }).join("");
}

// ==========================================
// Custom Domain Rules Manager
// ==========================================
async function fetchRules() {
  try {
    const res = await fetch(`${API_BASE}/api/rules`);
    if (!res.ok) return;
    allRules = await res.json();
    renderRulesTable(allRules);
  } catch (err) {
    console.error("Error fetching custom rules:", err);
  }
}

function renderRulesTable(rules) {
  const tbody = document.getElementById("rules-table-body");
  if (!tbody) return;

  if (!rules || rules.length === 0) {
    tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 16px;">No custom rules set. Add domains above to enforce instant allow or block policies.</td></tr>`;
    return;
  }

  tbody.innerHTML = rules.map(r => {
    const isWhite = r.rule_type === "whitelist";
    const badgeClass = isWhite ? "badge-whitelist" : "badge-blacklist";
    const badgeText = isWhite ? "WHITELIST (ALLOW)" : "BLACKLIST (BLOCK)";
    const dateFormatted = r.created_at ? new Date(r.created_at).toLocaleDateString() : "-";

    return `
      <tr>
        <td><strong>${escapeHtml(r.domain)}</strong></td>
        <td><span class="badge ${badgeClass}">${badgeText}</span></td>
        <td style="color: var(--text-muted); font-size: 13px;">${escapeHtml(r.notes || '-')}</td>
        <td style="color: var(--text-muted); font-size: 12px;">${dateFormatted}</td>
        <td><button class="btn-danger-sm" onclick="deleteCustomRule('${escapeHtml(r.domain)}')">🗑️ Remove</button></td>
      </tr>
    `;
  }).join("");
}

async function addCustomRule() {
  const domainInput = document.getElementById("rule-domain-input");
  const typeSelect = document.getElementById("rule-type-select");
  const notesInput = document.getElementById("rule-notes-input");

  const domain = domainInput.value.trim();
  const ruleType = typeSelect.value;
  const notes = notesInput.value.trim();

  if (!domain) {
    alert("Please enter a domain (e.g. evil-phishing.com)");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/rules`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain: domain, rule_type: ruleType, notes: notes })
    });

    if (res.ok) {
      domainInput.value = "";
      notesInput.value = "";
      fetchRules();
    } else {
      alert("Failed to add rule.");
    }
  } catch (err) {
    console.error("Error adding rule:", err);
  }
}

async function deleteCustomRule(domain) {
  if (!confirm(`Are you sure you want to remove rule for "${domain}"?`)) return;

  try {
    await fetch(`${API_BASE}/api/rules/${encodeURIComponent(domain)}`, { method: "DELETE" });
    fetchRules();
  } catch (err) {
    console.error("Error deleting rule:", err);
  }
}

// ==========================================
// 1-Click CSV Export Report
// ==========================================
function exportToCSV() {
  if (!allScans || allScans.length === 0) {
    alert("No scans available to export.");
    return;
  }

  const headers = ["ID", "URL", "Verdict", "Confidence_Percent", "Risk_Level", "Threat_Category", "SSL_Valid", "Client_Source", "Timestamp"];
  const rows = allScans.map(s => [
    s.id || s._id || "",
    `"${(s.url || '').replace(/"/g, '""')}"`,
    s.is_phishing ? "PHISHING" : "SAFE",
    s.confidence || 0,
    `"${(s.risk_level || '').replace(/"/g, '""')}"`,
    `"${(s.threat_category || '').replace(/"/g, '""')}"`,
    s.ssl_valid ? "VALID" : "INVALID_OR_NONE",
    s.client_type || "extension",
    `"${s.timestamp || ''}"`
  ]);

  const csvContent = [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
  const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  const filename = `CyberShield_Threat_Report_${new Date().toISOString().slice(0,10)}.csv`;

  link.setAttribute("href", url);
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function updateCharts(safe, phishing) {
  const ctxPie = document.getElementById("threatPieChart").getContext("2d");
  
  if (pieChart) {
    pieChart.data.datasets[0].data = [safe, phishing];
    pieChart.update();
  } else {
    pieChart = new Chart(ctxPie, {
      type: "doughnut",
      data: {
        labels: ["Safe Websites", "Phishing Threats"],
        datasets: [{
          data: [safe, phishing],
          backgroundColor: ["#10b981", "#ef4444"],
          borderWidth: 0,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: "#94a3b8", font: { family: "Inter", size: 12 } }
          }
        },
        cutout: "70%"
      }
    });
  }

  const ctxBar = document.getElementById("activityBarChart").getContext("2d");
  if (!barChart) {
    barChart = new Chart(ctxBar, {
      type: "bar",
      data: {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Today"],
        datasets: [
          {
            label: "Safe Scans",
            data: [12, 19, 15, 22, 28, 14, safe],
            backgroundColor: "rgba(16, 185, 129, 0.6)",
            borderRadius: 4
          },
          {
            label: "Phishing Blocks",
            data: [4, 7, 3, 8, 12, 6, phishing],
            backgroundColor: "rgba(239, 68, 68, 0.6)",
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { display: false }, ticks: { color: "#94a3b8" } },
          y: { grid: { color: "rgba(255,255,255,0.05)" }, ticks: { color: "#94a3b8" } }
        },
        plugins: {
          legend: {
            position: "top",
            labels: { color: "#94a3b8", font: { family: "Inter", size: 12 } }
          }
        }
      }
    });
  } else {
    barChart.data.datasets[0].data[6] = safe;
    barChart.data.datasets[1].data[6] = phishing;
    barChart.update();
  }
}

async function runLiveTestScan() {
  const input = document.getElementById("test-url-input");
  const url = input.value.trim();
  const resBox = document.getElementById("scanner-result-box");

  if (!url) {
    alert("Please enter a valid URL to scan.");
    return;
  }

  resBox.style.display = "flex";
  resBox.className = "scanner-result";
  resBox.innerHTML = `<span>Analyzing <strong>${escapeHtml(url)}</strong> with AI Model, SSL Inspector & Robot...</span>`;

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url, client_type: "dashboard" })
    });

    const data = await res.json();
    if (data.is_phishing) {
      resBox.className = "scanner-result phishing";
      resBox.innerHTML = `
        <span>⚠️ <strong>PHISHING DETECTED:</strong> ${escapeHtml(data.risk_level)} (${data.confidence}% Confidence)</span>
        <span>🏷️ Category: <strong>${escapeHtml(data.threat_category)}</strong> | Logged to Database ✅</span>
      `;
    } else {
      resBox.className = "scanner-result safe";
      resBox.innerHTML = `
        <span>🛡️ <strong>SAFE URL:</strong> Verified (${data.confidence}% Confidence)</span>
        <span>🏷️ Category: <strong>${escapeHtml(data.threat_category)}</strong> | Logged to Database ✅</span>
      `;
    }

    // Refresh tables & stats
    fetchStats();
    fetchRecentScans();
  } catch (err) {
    resBox.className = "scanner-result phishing";
    resBox.innerHTML = `<span>Error connecting to server. Make sure backend is running.</span>`;
  }
}

async function clearAllScans() {
  if (!confirm("Are you sure you want to clear scan logs from MongoDB Atlas and Local DB?")) return;
  await fetch(`${API_BASE}/api/scans`, { method: "DELETE" });
  fetchStats();
  fetchRecentScans();
}

// ==========================================
// Week 9 Functions: Metrics, Batch Scan & Feedback
// ==========================================
async function fetchMetrics() {
  try {
    const res = await fetch(`${API_BASE}/api/metrics`);
    if (!res.ok) throw new Error("Failed to load metrics");
    const m = await res.json();
    
    if (m.status === "success") {
      document.getElementById("metric-accuracy").innerText = `${m.accuracy}%`;
      document.getElementById("metric-precision").innerText = `${m.precision}%`;
      document.getElementById("metric-recall").innerText = `${m.recall}%`;
      document.getElementById("metric-f1").innerText = `${m.f1_score}%`;
      document.getElementById("metric-roc").innerText = `${m.roc_auc}%`;

      if (m.confusion_matrix) {
        document.getElementById("cm-tn").innerText = m.confusion_matrix.true_negative.toLocaleString();
        document.getElementById("cm-fp").innerText = m.confusion_matrix.false_positive.toLocaleString();
        document.getElementById("cm-fn").innerText = m.confusion_matrix.false_negative.toLocaleString();
        document.getElementById("cm-tp").innerText = m.confusion_matrix.true_positive.toLocaleString();
      }
    }
  } catch (err) {
    console.error("Error fetching ML metrics:", err);
  }
}

async function runBatchScan() {
  const textarea = document.getElementById("batch-urls-input");
  const urls = textarea.value.split("\n").map(u => u.trim()).filter(u => u.length > 0);
  const resultBox = document.getElementById("batch-results-box");

  if (urls.length === 0) {
    alert("Please enter at least one URL per line.");
    return;
  }

  resultBox.style.display = "block";
  resultBox.innerHTML = `<div style="color: var(--accent-cyan); font-size: 13px;">Analyzing ${urls.length} URLs in parallel...</div>`;

  try {
    const res = await fetch(`${API_BASE}/api/batch-scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ urls: urls, client_type: "batch_scanner" })
    });
    const data = await res.json();
    
    let html = `<div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; max-height: 200px; overflow-y: auto;">
      <strong style="font-size: 13px;">Batch Scan Results (${data.total_scanned} URLs):</strong>
      <div style="margin-top: 8px; display: flex; flex-direction: column; gap: 6px;">`;

    data.results.forEach(r => {
      const isPhish = r.is_phishing;
      const color = isPhish ? "var(--accent-danger)" : "var(--accent-safe)";
      const badge = isPhish ? "⚠️ PHISHING" : "🛡️ SAFE";
      html += `<div style="display: flex; justify-content: space-between; font-size: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding: 4px 0;">
        <span style="font-family: monospace; max-width: 60%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${escapeHtml(r.url)}</span>
        <span style="color: ${color}; font-weight: 600;">${badge} (${r.confidence || 0}%)</span>
      </div>`;
    });

    html += `</div></div>`;
    resultBox.innerHTML = html;

    // Refresh telemetry
    fetchStats();
    fetchRecentScans();
  } catch (err) {
    resultBox.innerHTML = `<div style="color: var(--accent-danger);">Batch scan failed: ${err.message}</div>`;
  }
}

async function submitUserFeedback() {
  const urlInput = document.getElementById("feedback-url-input");
  const labelSelect = document.getElementById("feedback-label-select");
  const commentInput = document.getElementById("feedback-comment-input");
  const statusBox = document.getElementById("feedback-status-box");

  const url = urlInput.value.trim();
  if (!url) {
    alert("Please enter a URL to report.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: url,
        reported_label: labelSelect.value,
        user_comment: commentInput.value.trim()
      })
    });
    
    if (res.ok) {
      statusBox.style.display = "block";
      statusBox.style.color = "var(--accent-safe)";
      statusBox.innerHTML = `✅ Thank you! Feedback for <strong>${escapeHtml(url)}</strong> submitted to database for AI retraining.`;
      urlInput.value = "";
      commentInput.value = "";
      setTimeout(() => { statusBox.style.display = "none"; }, 5000);
    }
  } catch (err) {
    statusBox.style.display = "block";
    statusBox.style.color = "var(--accent-danger)";
    statusBox.innerHTML = `❌ Failed to submit feedback: ${err.message}`;
  }
}

function escapeHtml(text) {
  if (!text) return "";
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

