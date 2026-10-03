export const createSolutionSlice = (set, get) => ({
  // State
  solutions: {}, // key: day_id (integer), value: array of solutions
  currentSolution: null,
  selectedDayId: null,  // ✅ ADD THIS
  isSaving: false,
  isEditing: false,

  // Actions
  setSelectedDayId: (dayId) => set({ selectedDayId: dayId }),  // ✅ ADD THIS
  
  setSolutions: (dayId, solutions) => set((state) => ({
    solutions: { ...state.solutions, [dayId]: solutions }
  })),
  
  addSolutions: (dayId, solutions) => set((state) => ({
    solutions: {
      ...state.solutions,
      [dayId]: solutions
    }
  })),
  
  setCurrentSolution: (solution) => set({ currentSolution: solution }),
  
  addSolution: (dayId, solution) => set((state) => ({
    solutions: {
      ...state.solutions,
      [dayId]: [...(state.solutions[dayId] || []), solution]
    }
  })),
  
  updateSolution: (dayId, updatedSolution) => set((state) => ({
    solutions: {
      ...state.solutions,
      [dayId]: state.solutions[dayId]?.map((s) =>
        s.id === updatedSolution.id ? updatedSolution : s
      ) || []
    },
    currentSolution: state.currentSolution?.id === updatedSolution.id
      ? updatedSolution
      : state.currentSolution
  })),
  
  removeSolution: (dayId, solutionId) => set((state) => ({
    solutions: {
      ...state.solutions,
      [dayId]: state.solutions[dayId]?.filter((s) => s.id !== solutionId) || []
    }
  })),
  
  clearSolutions: (dayId) => set((state) => ({
    solutions: {
      ...state.solutions,
      [dayId]: []
    }
  })),
  
  setIsSaving: (isSaving) => set({ isSaving }),
  
  setIsEditing: (isEditing) => set({ isEditing }),
  
  clearCurrentSolution: () => set({ currentSolution: null }),
  
  getSolutionsByDay: (dayId) => {
    const state = get();
    return state.solutions[dayId] || [];
  },
});