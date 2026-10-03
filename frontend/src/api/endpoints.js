// src/api/endpoints.js
export const API_ENDPOINTS = {
  // Months
  MONTHS: '/months',  // ✅ Remove /api/v1
  MONTH_DAYS: (monthId) => `/months/${monthId}/days`,
  
  // Days
  DAY: (dayId) => `/days/${dayId}`,
  DAY_SOLUTIONS: (dayId) => `/days/${dayId}/solutions`,  // ✅ Remove /api/v1
  DAY_BY_DATE: (date) => `/days/by-date/${date}`,
  
  // Solutions
  SOLUTIONS: '/solutions',  // ✅ Remove /api/v1
  SOLUTION: (solutionId) => `/solutions/${solutionId}`,
  SOLUTION_BY_DAY_AND_PROBLEM: (dayId, problemNumber) => 
    `/solutions/by-day/${dayId}/problem/${problemNumber}`,  // ✅ Remove /api/v1
  SOLUTION_AI: (solutionId) => `/solutions/${solutionId}/ai-summary`,
  
  // Execution
  EXECUTE: '/execute',
  
  // Auth
  VERIFY_ADMIN: '/auth/verify',
  
  // Stats
  STATS: '/solutions/stats',
};