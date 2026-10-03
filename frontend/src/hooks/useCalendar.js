import { useEffect } from 'react';
import { useStore } from '@store/store';
import { monthService } from '@api/services/monthService';
import { showToast } from '@utils/errorHandler';
import { getWeeksInMonth, getMonthName } from '@utils/dateUtils';

export const useCalendar = () => {
  const {
    months,
    currentMonthIndex,
    isLoading,
    error,
    setMonths,
    setLoading,
    setError,
    clearError,
  } = useStore();

  const currentYear = 2026;

  // Fetch months data
  const fetchMonths = async () => {
    setLoading(true);
    try {
      const data = await monthService.getMonths();
      setMonths(data);
      clearError();
    } catch (err) {
      setError('Failed to load calendar data');
      showToast.error('Failed to load calendar');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Get weeks for current month
  const getCurrentMonthWeeks = () => {
    const monthIndex = currentMonthIndex;
    // August = 7 (0-indexed: January = 0)
    const month = 7 + monthIndex;
    return getWeeksInMonth(currentYear, month);
  };

  // Get current month name
  const getCurrentMonthName = () => {
    return getMonthName(currentMonthIndex);
  };

  // Get current month year
  const getCurrentMonthYear = () => {
    return currentYear;
  };

  // Get days for current month
  const getCurrentMonthDays = () => {
    const weeks = getCurrentMonthWeeks();
    return weeks.flat().filter(day => day !== null);
  };

  // Load months on mount
  useEffect(() => {
    if (months.length === 0) {
      fetchMonths();
    }
  }, []);

  return {
    months,
    currentMonthIndex,
    isLoading,
    error,
    currentYear,
    getCurrentMonthWeeks,
    getCurrentMonthName,
    getCurrentMonthYear,
    getCurrentMonthDays,
    fetchMonths,
  };
};