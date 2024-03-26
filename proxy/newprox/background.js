// Proxy configuration
var config = {
    mode: "fixed_servers",
    rules: {
      singleProxy: {
        scheme: "http",
        host: "45.205.69.76",
        port: parseInt(7777)
      },
      bypassList: ["localhost"]
    }
  };
  
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

// Authentication handling
chrome.webRequest.onAuthRequired.addListener(
    function(details, callbackFn) {
        console.log("Proxy auth required");
        return {
            authCredentials: {
                username: "lu9118235",
                password: "dcPbzD"
            }
        };
    },
    {urls: ["<all_urls>"]},
    ["blocking"]
);
