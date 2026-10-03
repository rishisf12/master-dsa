import React, { useState } from 'react';
import { WeekRow } from './WeekRow';
import { getWeeksInMonth } from '@utils/dateUtils';

export const MonthGrid = ({ year, monthIndex, monthName }) => {
  const weeks = getWeeksInMonth(year, monthIndex);

  return (
    <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl shadow-lg border border-gray-200/50 dark:border-gray-700/50 p-4 hover:shadow-xl transition-shadow duration-300">
      <h2 className="text-xl font-bold text-transparent bg-clip-text bg-linear-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 text-center mb-4">
        {monthName} {year}
      </h2>
      
      <div className="space-y-0.5">
        {/* Day headers */}
        <div className="grid grid-cols-7 gap-0.5 mb-1">
          {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => (
            <div
              key={day}
              className="text-center text-[10px] font-semibold text-gray-600 dark:text-gray-400 py-1"
            >
              {day}
            </div>
          ))}
        </div>

        {/* Weeks */}
        {weeks.map((week, index) => (
          <WeekRow 
            key={index} 
            week={week}
          />
        ))}
      </div>
    </div>
  );
};