chrome.webRequest.onAuthRequired.addListener(
  function(details) {
    return {
      authCredentials: {
        username: "MODIFY", // Replace with your proxy username
        password: "MODIFY" // Replace with your proxy password
      }
    };
  },
  { urls: ["<all_urls>"] },
  ['blocking']
);