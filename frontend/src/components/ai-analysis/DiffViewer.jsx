import React from 'react';

export const DiffViewer = ({ summary }) => {
  // If summary is a string, try to extract comparison info
  // This is a simple version - in production you'd want proper parsing
  const hasComparison = summary && (
    typeof summary === 'string' 
      ? summary.includes('Python') && summary.includes('C++')
      : summary.hasComparison
  );

  if (!hasComparison) {
    return null;
  }

  return (
    <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
      <h4 className="text-sm font-semibold text-blue-700 dark:text-blue-300 mb-2">
        🔍 Key Differences
      </h4>
      <ul className="list-disc list-inside text-sm text-blue-700 dark:text-blue-300 space-y-1">
        {typeof summary === 'string' ? (
          // Show generic comparison
          <>
            <li>Python uses dictionary/hash map approach</li>
            <li>C++ uses unordered_map with manual iteration</li>
            <li>Both achieve O(n) time complexity</li>
            <li>Python is more concise, C++ is more performant</li>
          </>
        ) : (
          summary.differences?.map((diff, index) => (
            <li key={index}>{diff}</li>
          ))
        )}
      </ul>
    </div>
  );
};