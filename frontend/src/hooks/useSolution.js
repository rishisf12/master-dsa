import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { solutionService } from '@api/services/solutionService';
import { useStore } from '@store/store';
import { showToast } from '@utils/errorHandler';

export const useSolution = (solutionId, dayId, problemNumber) => {
  const queryClient = useQueryClient();
  const { 
    addSolution, 
    addSolutions,
    updateSolution, 
    removeSolution,
    setCurrentSolution,
  } = useStore();

  // ✅ GET ALL SOLUTIONS FOR A DAY - WITH PROPER 404 HANDLING
  const getSolutionsByDay = useQuery({
    queryKey: ['solutions', 'day', dayId],
    queryFn: async () => {
      if (!dayId) return [];
      const data = await solutionService.getSolutionsByDay(dayId);
      // Store solutions in the store
      if (data && data.length > 0) {
        addSolutions(dayId, data);
      }
      return data || [];
    },
    enabled: !!dayId,
    retry: false,
    staleTime: 1000 * 60 * 5, // 5 minutes - prevents infinite refetching
    onError: (error) => {
      if (error?.response?.status !== 404) {
        console.error('Error fetching solutions for day:', error);
        showToast.error('Failed to load solutions');
      }
    },
  });

  // ✅ Get solution by day and problem number - SILENTLY handle 404
  const getSolutionByDayAndProblem = useQuery({
    queryKey: ['solution', dayId, problemNumber],
    queryFn: async () => {
      try {
        const data = await solutionService.getSolutionByDayAndProblem(dayId, problemNumber);
        return data;
      } catch (error) {
        // ✅ SILENTLY return null for 404 - NO ERROR TOAST!
        if (error?.response?.status === 404) {
          return null;
        }
        // Only show error for other errors
        showToast.error('Failed to load solution');
        throw error;
      }
    },
    enabled: !!dayId && !!problemNumber,
    retry: false,
    staleTime: 1000 * 60 * 5, // 5 minutes
    onError: (error) => {
      if (error?.response?.status !== 404) {
        console.error('Error fetching solution:', error);
      }
    },
  });

  // Get solution by ID
  const getSolution = useQuery({
    queryKey: ['solution', solutionId],
    queryFn: () => solutionService.getSolution(solutionId),
    enabled: !!solutionId,
    retry: false,
  });

  // Create solution
  const createSolution = useMutation({
    mutationFn: (data) => solutionService.createSolution(data),
    onSuccess: (data) => {
      showToast.success('Solution created successfully!');
      addSolution(data.day_id, data);
      setCurrentSolution(data);
      queryClient.invalidateQueries({ queryKey: ['solutions', 'day', data.day_id] });
      queryClient.invalidateQueries({ queryKey: ['solution', data.day_id, data.problem_number] });
      queryClient.invalidateQueries({ queryKey: ['day', data.day_id] });
    },
    onError: (error) => {
      showToast.error(error?.response?.data?.detail || 'Failed to create solution');
      console.error(error);
    },
  });

  // Update solution
  const updateSolutionMutation = useMutation({
    mutationFn: ({ id, data }) => solutionService.updateSolution(id, data),
    onSuccess: (data) => {
      showToast.success('Solution updated successfully!');
      updateSolution(data.day_id, data);
      setCurrentSolution(data);
      queryClient.invalidateQueries({ queryKey: ['solutions', 'day', data.day_id] });
      queryClient.invalidateQueries({ queryKey: ['solution', data.day_id, data.problem_number] });
      queryClient.invalidateQueries({ queryKey: ['solution', data.id] });
      queryClient.invalidateQueries({ queryKey: ['day', data.day_id] });
    },
    onError: (error) => {
      showToast.error(error?.response?.data?.detail || 'Failed to update solution');
      console.error(error);
    },
  });

  // Delete solution
  const deleteSolution = useMutation({
    mutationFn: (id) => solutionService.deleteSolution(id),
    onSuccess: (_, variables) => {
      showToast.success('Solution deleted');
      removeSolution(variables.dayId, variables.solutionId);
      queryClient.invalidateQueries({ queryKey: ['solutions', 'day', variables.dayId] });
      queryClient.invalidateQueries({ queryKey: ['solution', variables.dayId, variables.problemNumber] });
      queryClient.invalidateQueries({ queryKey: ['day', variables.dayId] });
    },
    onError: (error) => {
      showToast.error('Failed to delete solution');
      console.error(error);
    },
  });

  // Generate AI summary
  const generateAISummary = useMutation({
    mutationFn: (id) => solutionService.generateAISummary(id),
    onSuccess: (data) => {
      showToast.success('AI summary generated!');
      queryClient.invalidateQueries({ queryKey: ['solutions'] });
      queryClient.invalidateQueries({ queryKey: ['solution', dayId, problemNumber] });
    },
    onError: (error) => {
      showToast.error('Failed to generate AI summary');
      console.error(error);
    },
  });

  return {
    // ✅ Return solutions list
    solutions: getSolutionsByDay.data || [],
    solutionsLoading: getSolutionsByDay.isLoading,
    solutionsError: getSolutionsByDay.error,
    refetchSolutions: getSolutionsByDay.refetch,
    
    solution: getSolutionByDayAndProblem.data, // ✅ null for 404
    solutionById: getSolution.data,
    isLoading: getSolutionByDayAndProblem.isLoading || getSolution.isLoading || getSolutionsByDay.isLoading,
    error: getSolutionByDayAndProblem.error || getSolution.error,
    
    createSolution: createSolution.mutateAsync,
    updateSolution: updateSolutionMutation.mutateAsync,
    deleteSolution: deleteSolution.mutateAsync,
    generateAISummary: generateAISummary.mutateAsync,
    
    isCreating: createSolution.isPending,
    isUpdating: updateSolutionMutation.isPending,
    isDeleting: deleteSolution.isPending,
    isGeneratingAI: generateAISummary.isPending,
  };
};