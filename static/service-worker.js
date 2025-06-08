self.addEventListener('install', (event) => {
    console.log('Service worker installé');
    self.skipWaiting();
  });
  
  self.addEventListener('fetch', () => {
    // Optionnel : cache ou redirection
  });
  