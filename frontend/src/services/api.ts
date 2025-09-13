import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth-storage');
    if (token) {
      const authData = JSON.parse(token);
      if (authData.state?.token) {
        config.headers.Authorization = `Bearer ${authData.state.token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth-storage');
      window.location.href = '/auth';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const apiEndpoints = {
  // Auth endpoints
  auth: {
    login: (email: string, password: string) =>
      api.post('/auth/login', { email, password }),
    register: (name: string, email: string, password: string) =>
      api.post('/auth/register', { name, email, password }),
  },

  // User endpoints
  user: {
    getProfile: () => api.get('/user/profile'),
    updateProfile: (data: any) => api.put('/user/profile', data),
  },

  // Waste analysis endpoints
  waste: {
    getWasteTypes: () => api.get('/api/waste-types'),
    getConversionSystems: () => api.get('/api/conversion-systems'),
    predictEnergy: (data: any) => api.post('/api/predict-energy', data),
  },

  // Simulation endpoints
  simulation: {
    runPersonalSimulation: (data: any) =>
      api.post('/api/simulate-personal', data),
    runSimulation: (data: any) => api.post('/api/simulate', data),
  },

  // Optimization endpoints
  optimization: {
    optimizeStrategy: (data: any) => api.post('/api/optimize', data),
  },

  // Impact endpoints
  impact: {
    getImpactAssessment: (simulationId: string) =>
      api.get(`/api/impact/${simulationId}`),
  },

  // Communities endpoints
  communities: {
    getCommunities: () => api.get('/api/communities'),
    getUserTypes: () => api.get('/api/user-types'),
  },
};

export default api;

