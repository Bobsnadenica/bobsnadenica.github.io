(function() {
  var pages = [
    'index1.html',
    'index2.html',
    'candybox.html',
    'Chatgpt.html',
    'DeepSeek.html',
    'Gemini.html',
    'Grok.html',
    'Meta.html'
  ];
  
  var choice = pages[Math.floor(Math.random() * pages.length)];
  
  // Add timestamp to target to bypass cache there too
  var url = choice + '?nocache=' + Date.now();
  
  // Redirect without adding to history
  window.location.replace(url);
})();
