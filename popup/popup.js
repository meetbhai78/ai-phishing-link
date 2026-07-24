document.addEventListener('DOMContentLoaded', function () {
  // 1. Get the current active tab and read its URL
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    let currentTab = tabs[0];
    let currentUrl = currentTab.url;
    
    // Display the URL in the popup
    document.getElementById("current-url").innerText = currentUrl;
  });

  // 2. Handle the scan button click
  document.getElementById("scan-btn").addEventListener("click", function () {
    let statusBox = document.getElementById("status-box");
    let statusMessage = document.getElementById("status-message");
    
    statusMessage.innerText = "Analyzing URL...";
    statusBox.style.backgroundColor = "#f39c12"; // Orange for processing
    statusMessage.style.color = "#fff";

    // For Week 2, we simulate a scan since the API isn't built yet.
    // In Phase 2, we will call our FastAPI backend here.
    setTimeout(() => {
      statusMessage.innerText = "Prediction API not connected yet (Week 4 task).";
      statusBox.style.backgroundColor = "#34495e"; // Dark color for info
    }, 1500);
  });
});
