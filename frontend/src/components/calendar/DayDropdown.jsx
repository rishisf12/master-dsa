import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { QBox } from './QBox';
import { getDateKey } from '@utils/dateUtils';
import { useStore } from '@store/store';
import { showToast } from '@utils/errorHandler';
import apiClient from '@api/client';
import { API_ENDPOINTS } from '@api/endpoints';

export const DayDropdown = ({ 
  date, 
  solutions,    
  onClose,
  onRefresh     
}) => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const dateKey = getDateKey(date);
  const { setSelectedDayId } = useStore();

  const getSolutionForProblem = (problemNumber) => {
    if (!solutions || solutions.length === 0) return null;
    return solutions.find(s => s.problem_number === problemNumber);
  };

  const handleQClick = async (qNumber) => {
    setIsLoading(true);
    try {
      const dateStr = date.toISOString().split('T')[0];
      const response = await apiClient.get(API_ENDPOINTS.DAY_BY_DATE(dateStr));
      const actualDayId = response.data.id;
      
      setSelectedDayId(actualDayId);
      navigate(`/problem/${dateKey}/${qNumber}`);
      onClose();
      
    } catch (error) {
      showToast.error('Day not found in database. Please create the day first.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="absolute left-0 right-0 mt-1 z-50 bg-white/95 dark:bg-gray-800/95 backdrop-blur-sm rounded-lg shadow-xl border border-gray-200/50 dark:border-gray-700/50 p-2 min-w-30">
      <div className="space-y-0.5">
        {[1, 2, 3].map((qNumber) => {
          const solution = getSolutionForProblem(qNumber);
          return (
            <QBox 
              key={qNumber}
              qNumber={qNumber}
              onClick={() => handleQClick(qNumber)}
              disabled={isLoading}
              isSolved={!!solution}
              solution={solution}
              hasAI={!!solution?.ai_summary}
            />
          );
        })}
        {isLoading && (
          <div className="text-center text-xs text-gray-500 py-1">
            Loading...
          </div>
        )}
      </div>
    </div>
  );
};