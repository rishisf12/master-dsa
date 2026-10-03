import apiClient from '../client';
import { API_ENDPOINTS } from '../endpoints';

export const solutionService = {
  // Get solution by ID
  getSolution: async (id) => {
    const response = await apiClient.get(API_ENDPOINTS.SOLUTION(id));
    return response.data;
  },

  // ✅ Get solution by day_id and problem_number - SILENTLY return null on 404
  getSolutionByDayAndProblem: async (dayId, problemNumber) => {
    try {
      const response = await apiClient.get(
        API_ENDPOINTS.SOLUTION_BY_DAY_AND_PROBLEM(dayId, problemNumber)
      );
      return response.data;
    } catch (error) {
      // ✅ SILENTLY return null for 404 - user sees empty editor
      if (error.response?.status === 404) {
        return null;
      }
      // Re-throw other errors
      throw error;
    }
  },

  // ✅ FIXED: Handle 404 in getSolutionsByDay
  getSolutionsByDay: async (dayId) => {
    try {
      const response = await apiClient.get(API_ENDPOINTS.DAY_SOLUTIONS(dayId));
      return response.data;
    } catch (error) {
      // ✅ Return empty array on 404
      if (error.response?.status === 404) {
        return [];
      }
      throw error;
    }
  },

  // ✅ Keep alias for backward compatibility
  getDaySolutions: async (dayId) => {
    return solutionService.getSolutionsByDay(dayId);
  },

  // Create solution
  createSolution: async (data) => {
    const response = await apiClient.post(API_ENDPOINTS.SOLUTIONS, data);
    return response.data;
  },

  // Update solution
  updateSolution: async (id, data) => {
    const response = await apiClient.put(API_ENDPOINTS.SOLUTION(id), data);
    return response.data;
  },

  // Delete solution
  deleteSolution: async (id) => {
    const response = await apiClient.delete(API_ENDPOINTS.SOLUTION(id));
    return response.data;
  },

  // Generate AI summary
  generateAISummary: async (id) => {
    const response = await apiClient.post(API_ENDPOINTS.SOLUTION_AI(id));
    return response.data;
  },
};