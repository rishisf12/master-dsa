export const createCalendarSlice = (set, get) => ({
  // State
  months: [],
  currentMonthIndex: 0, // 0 = August, 1 = September, etc.
  selectedDate: null,
  selectedDayId: null, // ✅ Add this - stores the database ID of the selected day
  isLoading: false,
  error: null,

  // Actions
  setMonths: (months) => set({ months }),
  
  setCurrentMonthIndex: (index) => set({ currentMonthIndex: index }),
  
  setSelectedDate: (date) => set({ selectedDate: date }),
  
  // ✅ Add this action
  setSelectedDayId: (dayId) => set({ selectedDayId: dayId }),
  
  nextMonth: () => set((state) => ({
    currentMonthIndex: Math.min(state.currentMonthIndex + 1, 3)
  })),
  
  prevMonth: () => set((state) => ({
    currentMonthIndex: Math.max(state.currentMonthIndex - 1, 0)
  })),
  
  setLoading: (isLoading) => set({ isLoading }),
  
  setError: (error) => set({ error }),
  
  clearError: () => set({ error: null }),
});