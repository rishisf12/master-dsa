import React from 'react';

export const OutputPanel = ({ language, output }) => {
  return (
    <div className="bg-gray-900 dark:bg-gray-950 rounded-xl shadow-sm border border-gray-700 overflow-hidden">
      <div className="flex items-center px-4 py-2 bg-gray-800 dark:bg-gray-800 border-b border-gray-700">
        <span className="text-sm font-medium text-gray-300">
          {language} Output
        </span>
      </div>
      <pre className="p-4 text-sm font-mono text-gray-300 min-h-25 max-h-50 overflow-auto whitespace-pre-wrap">
        {output || 'Run your code to see output...'}
      </pre>
    </div>
  );
};