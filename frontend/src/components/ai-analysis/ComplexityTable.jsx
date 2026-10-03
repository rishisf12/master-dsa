import React from 'react';

export const ComplexityTable = ({ timeComplexity, spaceComplexity }) => {
  return (
    <div className="mt-4">
      <h4 className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
        ✅ Complexity Verification
      </h4>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 dark:bg-gray-700/50">
              <th className="px-4 py-2 text-left text-gray-600 dark:text-gray-400 font-medium">Metric</th>
              <th className="px-4 py-2 text-left text-gray-600 dark:text-gray-400 font-medium">Python</th>
              <th className="px-4 py-2 text-left text-gray-600 dark:text-gray-400 font-medium">C++</th>
              <th className="px-4 py-2 text-left text-gray-600 dark:text-gray-400 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            <tr>
              <td className="px-4 py-2 text-gray-700 dark:text-gray-300 font-medium">Time</td>
              <td className="px-4 py-2 font-mono text-gray-900 dark:text-white">
                {timeComplexity || '—'}
              </td>
              <td className="px-4 py-2 font-mono text-gray-900 dark:text-white">
                {timeComplexity || '—'}
              </td>
              <td className="px-4 py-2">
                {timeComplexity ? (
                  <span className="text-green-600 dark:text-green-400">✅ Verified</span>
                ) : (
                  <span className="text-gray-400">—</span>
                )}
              </td>
            </tr>
            <tr>
              <td className="px-4 py-2 text-gray-700 dark:text-gray-300 font-medium">Space</td>
              <td className="px-4 py-2 font-mono text-gray-900 dark:text-white">
                {spaceComplexity || '—'}
              </td>
              <td className="px-4 py-2 font-mono text-gray-900 dark:text-white">
                {spaceComplexity || '—'}
              </td>
              <td className="px-4 py-2">
                {spaceComplexity ? (
                  <span className="text-green-600 dark:text-green-400">✅ Verified</span>
                ) : (
                  <span className="text-gray-400">—</span>
                )}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};