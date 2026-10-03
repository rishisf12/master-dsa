import React from 'react';
import clsx from 'clsx';

export const Card = ({
  children,
  className = '',
  variant = 'default',
  ...props
}) => {
  const variants = {
    default: 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700',
    elevated: 'bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-shadow',
    outline: 'bg-transparent border-2 border-gray-200 dark:border-gray-700',
  };

  return (
    <div
      className={clsx(
        'rounded-xl p-6',
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};