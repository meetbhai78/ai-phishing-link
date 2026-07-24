// Background service worker for CyberShield
console.log("CyberShield Background Service Worker loaded.");

chrome.runtime.onInstalled.addListener(() => {
  console.log("CyberShield Extension Installed Successfully.");
});

// We can add background listeners here later (e.g., intercepting navigation to check URLs in real-time)
