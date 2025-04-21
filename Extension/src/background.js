    function checkUrl() {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const activeTab = tabs[0];

        if (activeTab.url == "https://www.arnotts.ie/shopping-bag/"){
            console.log("yay")
            chrome.action.openPopup();
        }
    });}

  function keepAlive() {
    setInterval(() => {
      chrome.runtime.getPlatformInfo(function(info) {
        console.log('Keeping service worker alive. Platform: ' + info.os);
        checkUrl()
      });
    }, 5000); // Every 20 seconds
  }

  chrome.runtime.onInstalled.addListener(() => {
    keepAlive(); // Start keep-alive on install
  });

  chrome.runtime.onStartup.addListener(() => {
    keepAlive(); // Restart keep-alive on startup
  });

