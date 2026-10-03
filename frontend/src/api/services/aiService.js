// src/api/services/aiService.js
import apiClient from '../client';

export const aiService = {
  generateSummary: async (
    solutionId,
    problemName,
    pythonCode,
    cppCode,
    pythonTimeComplexity,
    pythonSpaceComplexity,
    cppTimeComplexity,
    cppSpaceComplexity,
    notes = null
  ) => {
    const payload = {
      problem_name: problemName,
      python_code: pythonCode,
      cpp_code: cppCode,
      python_time_complexity: pythonTimeComplexity || null,
      python_space_complexity: pythonSpaceComplexity || null,
      cpp_time_complexity: cppTimeComplexity || null,
      cpp_space_complexity: cppSpaceComplexity || null,
      notes: notes || null
    };
    
    console.log('📤 Sending AI payload:', payload);
    
    // ✅ Change api to apiClient
    const response = await apiClient.post(`/solutions/${solutionId}/ai-summary`, payload);
    return response.data;
  },
  
  executeCode: async (language, code, stdin = '', usePython3 = true) => {
    // ✅ Change api to apiClient
    const response = await apiClient.post('/execute', {
      language,
      code,
      stdin,
      usePython3
    });
    return response.data;
  }
};