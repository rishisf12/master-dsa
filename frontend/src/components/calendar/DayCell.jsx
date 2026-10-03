import React, { useState } from 'react';
import { isToday } from '@utils/dateUtils';
import { DayDropdown } from './DayDropdown';
import { useStore } from '@store/store';

export const DayCell = ({ day, onDayClick, selectedDate }) => {
  const [isOpen, setIsOpen] = useState(false);
  const storeSolutions = useStore((state) => state.solutions);

  if (!day) {
    return <div className="w-full h-8" />;
  }

  const isCurrentDay = isToday(day);
  const dayNumber = day.getDate();
  const daySolutions = storeSolutions[dayNumber] || [];

  const handleClick = () => {
    setIsOpen(!isOpen);
    if (onDayClick) {
      onDayClick(day);
    }
  };

  const hasSolutions = daySolutions && daySolutions.length > 0;

  return (
    <div className="relative">
      <button
        onClick={handleClick}
        className={`
          w-full h-8 rounded-lg transition-all duration-200
          flex items-center justify-center text-sm font-medium
          hover:shadow-md transform hover:scale-105
          relative
          ${isCurrentDay 
            ? 'bg-linear-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 shadow-md' 
            : hasSolutions
              ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 hover:bg-green-200 dark:hover:bg-green-900/50'
              : 'bg-gray-50 dark:bg-gray-700/50 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-600'
          }
        `}
      >
        {dayNumber}
        {hasSolutions && (
          <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-green-500 rounded-full animate-pulse" />
        )}
      </button>

      {isOpen && (
        <DayDropdown 
          date={day}
          solutions={daySolutions}
          onClose={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};