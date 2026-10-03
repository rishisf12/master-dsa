import React from 'react';

export const AISummary = ({
  summary,
  pythonTimeComplexity,
  pythonSpaceComplexity,
  cppTimeComplexity,
  cppSpaceComplexity,
  notes,
}) => {
  return (
    <div className="space-y-4">
      {/* ✅ Show the user's input values */}
      <div className="grid grid-cols-2 gap-4 p-4 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600">
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            🐍 Python Complexity
          </h4>
          <div className="text-sm">
            <span className="text-gray-500 dark:text-gray-400">Time:</span>
            <span className="ml-2 font-mono text-gray-900 dark:text-white">
              {pythonTimeComplexity || 'Not specified'}
            </span>
          </div>
          <div className="text-sm">
            <span className="text-gray-500 dark:text-gray-400">Space:</span>
            <span className="ml-2 font-mono text-gray-900 dark:text-white">
              {pythonSpaceComplexity || 'Not specified'}
            </span>
          </div>
        </div>
        <div>
          <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            ⚡ C++ Complexity
          </h4>
          <div className="text-sm">
            <span className="text-gray-500 dark:text-gray-400">Time:</span>
            <span className="ml-2 font-mono text-gray-900 dark:text-white">
              {cppTimeComplexity || 'Not specified'}
            </span>
          </div>
          <div className="text-sm">
            <span className="text-gray-500 dark:text-gray-400">Space:</span>
            <span className="ml-2 font-mono text-gray-900 dark:text-white">
              {cppSpaceComplexity || 'Not specified'}
            </span>
          </div>
        </div>
      </div>

      {/* AI Summary Content */}
      <div className="prose dark:prose-invert max-w-none">
        {typeof summary === 'string' ? (
          <div className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap text-sm leading-relaxed">
            {summary}
          </div>
        ) : (
          <div className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap text-sm leading-relaxed">
            {summary?.text || 'No summary available'}
          </div>
        )}
      </div>
    </div>
  );
};