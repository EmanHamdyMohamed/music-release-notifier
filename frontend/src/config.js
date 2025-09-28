// API Configuration
const config = {
  // API Base URL - can be overridden by environment variables
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/',
  
  // API Endpoints
  endpoints: {
    subscribe: '/subscribe',
    artists: '/artists',
    searchArtists: '/search_artists',
  },
  
  // Helper function to get full API URL
  getApiUrl: (endpoint) => {
    return `${config.apiBaseUrl}${endpoint}`;
  }
};

export default config;
