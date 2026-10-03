import React from 'react';
import { Spinner } from '@components/ui/Spinner';

export const LoadingState = () => {
  return (
    <div className="py-8">
      <div className="flex items-center justify-center gap-4">
        <Spinner size="lg" />
        <div>
          <p className="text-gray-700 dark:text-gray-300 font-medium">
            Analyzing your code...
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Comparing Python and C++ implementations
          </p>
        </div>
      </div>
    </div>
  );
};