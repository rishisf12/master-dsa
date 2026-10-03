// src/api/client.js
import axios from 'axios';
import { API_BASE_URL } from '@config/environment';

// ✅ Add /api/v1 here
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    if (import.meta.env.DEV) {
      console.log(`📤 ${config.method?.toUpperCase()} ${config.url}`, config.data);
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.log(`📥 ${response.status} ${response.config.url}`, response.data);
    }
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      console.error('Unauthorized - redirecting to login');
    } else if (error.response?.status === 404) {
      console.error('Resource not found:', error.config?.url);
    } else if (error.code === 'ECONNABORTED') {
      console.error('Request timeout - please try again');
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;