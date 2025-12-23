// API service for frontend-backend communication

// For Docusaurus environment, we need to handle the API differently
// process.env is not available in browser context in Docusaurus
const getApiBaseUrl = () => {
  // Check if we're in a browser environment and have access to window
  if (typeof window !== 'undefined') {
    // Allow configuration via global variable for flexibility
    if (window.DOCUSAURUS_API_CONFIG && window.DOCUSAURUS_API_CONFIG.baseUrl) {
      return window.DOCUSAURUS_API_CONFIG.baseUrl;
    }
    // Default to localhost:8080 for development (where our backend is running)
    return 'https://samra82-book-chatbot.hf.space/api/v1';
  }
  // Server-side (SSR): use default
  return 'https://samra82-book-chatbot.hf.space/api/v1';
};

class ApiService {
  constructor() {
    this.baseUrl = getApiBaseUrl();
  }

  // Method to make API requests
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add authorization header if available
    const token = localStorage.getItem('api_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Health check endpoint
  async healthCheck() {
    return this.request('/health');
  }

  // Chat endpoint
  async sendMessage(message, sessionId = null) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message, session_id: sessionId }),
    });
  }

  // Process URL endpoint
  async processUrl(url) {
    return this.request('/process-url', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  }

  // Retrieve context endpoint
  async retrieveContext(query, topK = 5) {
    return this.request('/retrieve', {
      method: 'POST',
      body: JSON.stringify({ query, top_k: topK }),
    });
  }

  // Method to test API connectivity
  async testConnection() {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch (error) {
      console.warn('API connection test failed:', error);
      return false;
    }
  }
}

export default new ApiService();