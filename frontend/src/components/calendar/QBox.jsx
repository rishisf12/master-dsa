import React from 'react';

export const QBox = ({ 
  qNumber, 
  onClick, 
  disabled = false,
  isSolved = false,      // ✅ Add this
  solution = null,       // ✅ Add this
  hasAI = false,         // ✅ Add this
}) => {
  console.log(`QBox ${qNumber} rendered, solved: ${isSolved}, hasAI: ${hasAI}`);
  
  // ✅ Determine icon based on status
  const getIcon = () => {
    if (isSolved && hasAI) return '✅';  // Solved with AI analysis
    if (isSolved) return '✔️';           // Solved without AI
    return '📝';                         // Not solved
  };
  
  // ✅ Determine color based on status
  const getStatusColor = () => {
    if (isSolved && hasAI) return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 hover:bg-green-200 dark:hover:bg-green-900/50';
    if (isSolved) return 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-900/30';
    return 'hover:bg-gray-100 dark:hover:bg-gray-700/50 text-gray-700 dark:text-gray-300';
  };

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`
        w-full px-3 py-1.5 text-sm font-medium text-left rounded-md 
        transition-all duration-200
        flex items-center justify-between
        ${disabled 
          ? 'opacity-50 cursor-not-allowed text-gray-400' 
          : `${getStatusColor()} hover:shadow-sm`
        }
      `}
    >
      <span>Q{qNumber}</span>
      <span className="text-base">{getIcon()}</span>
    </button>
  );
};