import React from 'react';
import { FiChevronLeft, FiChevronRight } from 'react-icons/fi';

export const MonthNavigation = ({ 
  monthName, 
  year, 
  onPrev, 
  onNext, 
  canPrev, 
  canNext 
}) => {
  return (
    <div className="flex items-center justify-between mb-4">
      <button
        onClick={onPrev}
        disabled={!canPrev}
        className={`
          p-2 rounded-lg transition-colors
          ${canPrev 
            ? 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300' 
            : 'opacity-50 cursor-not-allowed text-gray-400 dark:text-gray-600'
          }
        `}
      >
        <FiChevronLeft className="w-5 h-5" />
      </button>

      <h2 className="text-xl font-bold text-gray-900 dark:text-white">
        {monthName} {year}
      </h2>

      <button
        onClick={onNext}
        disabled={!canNext}
        className={`
          p-2 rounded-lg transition-colors
          ${canNext 
            ? 'hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300' 
            : 'opacity-50 cursor-not-allowed text-gray-400 dark:text-gray-600'
          }
        `}
      >
        <FiChevronRight className="w-5 h-5" />
      </button>
    </div>
  );
};