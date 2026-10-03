import React from 'react';
import { Button } from '@components/ui/Button';

export const EmptyState = ({
  icon = '📝',
  title = 'Nothing here yet',
  description = 'Start adding your solutions',
  actionLabel,
  onAction,
}) => {
  return (
    <div className="text-center py-12">
      <div className="text-6xl mb-4">{icon}</div>
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {title}
      </h3>
      <p className="text-gray-500 dark:text-gray-400 text-sm mb-4">
        {description}
      </p>
      {actionLabel && onAction && (
        <Button onClick={onAction} variant="primary">
          {actionLabel}
        </Button>
      )}
    </div>
  );
};