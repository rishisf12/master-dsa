import { create } from 'zustand';
import { createCalendarSlice } from './slices/calendarSlice';
import { createSolutionSlice } from './slices/solutionSlice';
import { createUISlice } from './slices/uiSlice';

export const useStore = create((...args) => ({
  ...createCalendarSlice(...args),
  ...createSolutionSlice(...args),
  ...createUISlice(...args),
}));