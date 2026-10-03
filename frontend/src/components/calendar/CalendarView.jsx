import React, { useState, useEffect } from 'react';
import { MonthGrid } from './MonthGrid';

export const CalendarView = () => {
  const currentYear = 2026;
  const [months, setMonths] = useState([
    { index: 7, name: 'August' },
    { index: 8, name: 'September' },
    { index: 9, name: 'October' },
    { index: 10, name: 'November' },
  ]);

  return (
    <div className="space-y-8 max-h-[calc(100vh-200px)] overflow-y-auto px-2 pb-8">
      <div className="text-center mb-6">
        <div className="inline-block p-4 px-8 rounded-xl bg-linear-to-r from-blue-600 to-indigo-600 shadow-lg">
          <h2 className="text-2xl font-bold text-white">📅 Your Practice Calendar</h2>
          <p className="text-blue-100 text-sm mt-1">August - November 2026</p>
        </div>
      </div>
      
      {months.map((month) => (
        <MonthGrid
          key={month.index}
          year={currentYear}
          monthIndex={month.index}
          monthName={month.name}
        />
      ))}
    </div>
  );
};