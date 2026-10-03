import apiClient from '../client';
import { API_ENDPOINTS } from '../endpoints';

export const monthService = {
  // Get all months
  getMonths: async () => {
    const response = await apiClient.get(API_ENDPOINTS.MONTHS);
    return response.data;
  },

  // Get days for a specific month
  getMonthDays: async (monthId) => {
    const response = await apiClient.get(API_ENDPOINTS.MONTH_DAYS(monthId));
    return response.data;
  },
};