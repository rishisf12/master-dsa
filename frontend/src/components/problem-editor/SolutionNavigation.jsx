import React from 'react';
import { useNavigate } from 'react-router-dom';
import { getDateKey } from '@utils/dateUtils';

export const SolutionNavigation = ({ 
  currentProblem, 
  date, 
  onMarkComplete, 
  isComplete 
}) => {
  const navigate = useNavigate();
  const dateKey = getDateKey(date);

  const handlePrev = () => {
    if (currentProblem > 1) {
      navigate(`/problem/${dateKey}/${currentProblem - 1}`);
    }
  };

  const handleNext = () => {
    if (currentProblem < 3) {
      navigate(`/problem/${dateKey}/${currentProblem + 1}`);
    }
  };

  return (
    <div className="flex items-center justify-between">
      <button
        onClick={handlePrev}
        disabled={currentProblem <= 1}
        className={`
          px-4 py-2 text-sm font-medium rounded-lg transition-colors
          ${currentProblem > 1 
            ? 'text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20' 
            : 'text-gray-400 dark:text-gray-600 cursor-not-allowed'
          }
        `}
      >
        ← Previous Problem
      </button>

      <button
        onClick={onMarkComplete}
        className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
          isComplete
            ? 'bg-green-600 hover:bg-green-700 text-white'
            : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
        }`}
      >
        {isComplete ? '✅ Marked Complete' : 'Mark Complete'}
      </button>

      <button
        onClick={handleNext}
        disabled={currentProblem >= 3}
        className={`
          px-4 py-2 text-sm font-medium rounded-lg transition-colors
          ${currentProblem < 3 
            ? 'text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20' 
            : 'text-gray-400 dark:text-gray-600 cursor-not-allowed'
          }
        `}
      >
        Next Problem →
      </button>
    </div>
  );
};