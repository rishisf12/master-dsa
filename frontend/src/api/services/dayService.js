import apiClient from '../client';
import { API_ENDPOINTS } from '../endpoints';

export const dayService = {
  // Get a specific day by ID
  getDay: async (dayId) => {
    const response = await apiClient.get(API_ENDPOINTS.DAY(dayId));
    return response.data;
  },

  // Get solutions for a day
  getDaySolutions: async (dayId) => {
    const response = await apiClient.get(API_ENDPOINTS.DAY_SOLUTIONS(dayId));
    return response.data;
  },

  // ✅ Get day by date (YYYY-MM-DD)
  getDayByDate: async (date) => {
    const response = await apiClient.get(`/api/v1/days/by-date/${date}`);
    return response.data;
  },
};