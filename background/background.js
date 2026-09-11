// ========================================================
// CyberShield - Background Service Worker (Auto-Shield v3.0)
// Automatically scans active tabs & updates badges in real time
// ========================================================

const API_ENDPOINT = "http://127.0.0.1:8000/predict";
const scannedUrlCache = new Map();

chrome.runtime.onInstalled.addListener(() => {
  console.log("[CyberShield] Background Auto-Shield Service Worker Initialized.");
});

// Helper to set badge status
function updateBadge(tabId, status) {
  if (!tabId) return;
  if (status === "scanning") {
    chrome.action.setBadgeText({ tabId: tabId, text: "..." });
    chrome.action.setBadgeBackgroundColor({ tabId: tabId, color: "#6B7280" });
  } else if (status === "danger") {
    chrome.action.setBadgeText({ tabId: tabId, text: "!" });
    chrome.action.setBadgeBackgroundColor({ tabId: tabId, color: "#EF4444" });
  } else if (status === "safe") {
    chrome.action.setBadgeText({ tabId: tabId, text: "OK" });
    chrome.action.setBadgeBackgroundColor({ tabId: tabId, color: "#10B981" });
  } else {
    chrome.action.setBadgeText({ tabId: tabId, text: "" });
  }
}

// Perform Auto-Scan in background
async function checkUrlThreat(tabId, url) {
  if (!url || (!url.startsWith("http://") && !url.startsWith("https://"))) {
    updateBadge(tabId, "clear");
    return;
  }

  // Check internal cache to reduce redundant API calls
  if (scannedUrlCache.has(url)) {
    const cached = scannedUrlCache.get(url);
    updateBadge(tabId, cached.is_phishing ? "danger" : "safe");
    return;
  }

  updateBadge(tabId, "scanning");

  try {
    const response = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url, client_type: "extension" })
    });

    if (!response.ok) {
      updateBadge(tabId, "clear");
      return;
    }

    const data = await response.json();
    scannedUrlCache.set(url, data);

    if (data.is_phishing) {
      updateBadge(tabId, "danger");
      
      // Trigger Notification for Critical Threat
      if (chrome.notifications) {
        try {
          chrome.notifications.create({
            type: "basic",
            iconUrl: chrome.runtime.getURL("icons/icon128.png"),
            title: "🚨 CyberShield Threat Alert!",
            message: `Warning! Dangerous Phishing Site Detected:\n${data.risk_level}\nCategory: ${data.threat_category}`,
            priority: 2
          }, () => {
            if (chrome.runtime.lastError) {
              console.warn("[CyberShield] Notification note:", chrome.runtime.lastError.message);
            }
          });
        } catch (e) {
          console.warn("[CyberShield] Notification error ignored:", e);
        }
      }
    } else {
      updateBadge(tabId, "safe");
    }
  } catch (err) {
    console.warn("[CyberShield] Background scan offline or backend unreachable:", err);
    updateBadge(tabId, "clear");
  }
}

// Listener: When tab URL changes or completes loading
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    checkUrlThreat(tabId, tab.url);
  }
});

// Listener: When user switches active tabs
chrome.tabs.onActivated.addListener((activeInfo) => {
  chrome.tabs.get(activeInfo.tabId, (tab) => {
    if (tab && tab.url) {
      checkUrlThreat(activeInfo.tabId, tab.url);
    }
  });
});
