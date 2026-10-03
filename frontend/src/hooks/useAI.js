import { useState } from 'react';
import { aiService } from '@api/services/aiService';
import { showToast } from '@utils/errorHandler';

export const useAI = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [aiSummary, setAISummary] = useState(null);
  const [error, setError] = useState(null);

  // ✅ Updated to accept ALL parameters
  const generateSummary = async (
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
    setIsGenerating(true);
    setError(null);
    try {
      const response = await aiService.generateSummary(
        solutionId,
        problemName,
        pythonCode,
        cppCode,
        pythonTimeComplexity,
        pythonSpaceComplexity,
        cppTimeComplexity,
        cppSpaceComplexity,
        notes
      );
      setAISummary(response.summary);
      return response.summary;
    } catch (err) {
      setError('Failed to generate AI summary');
      showToast.error('AI generation failed');
      console.error(err);
      return null;
    } finally {
      setIsGenerating(false);
    }
  };

  const executeCode = async (language, code, stdin = '', usePython3 = true) => {
    try {
      const response = await aiService.executeCode(language, code, stdin, usePython3);
      return response;
    } catch (err) {
      showToast.error('Code execution failed');
      console.error(err);
      return { stdout: '', stderr: 'Execution failed' };
    }
  };

  return {
    isGenerating,
    aiSummary,
    error,
    generateSummary,
    executeCode,
  };
};