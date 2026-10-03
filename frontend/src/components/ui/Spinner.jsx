import React from 'react';
import clsx from 'clsx';

export const Spinner = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: 'h-4 w-4 border-2',
    md: 'h-8 w-8 border-3',
    lg: 'h-12 w-12 border-4',
  };

  return (
    <div
      className={clsx(
        'inline-block animate-spin rounded-full border-solid border-current border-r-transparent text-blue-600',
        sizes[size],
        className
      )}
      role="status"
    >
      <span className="sr-only">Loading...</span>
    </div>
  );
};