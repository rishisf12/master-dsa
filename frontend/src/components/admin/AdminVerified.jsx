import React from 'react';
import { Button } from '@components/ui/Button';
import { useAuth } from '@hooks/useAuth';
import { useStore } from '@store/store';

export const AdminVerified = ({ onClose }) => {
  const { adminUsername } = useStore();
  const { logout } = useAuth();

  const handleLock = () => {
    logout();
    onClose();
  };

  return (
    <div className="space-y-4">
      <div className="text-center py-2">
        <p className="text-lg font-semibold text-green-600 dark:text-green-400">
          ✅ Welcome back, {adminUsername}!
        </p>
      </div>

      <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
        <div className="flex items-center gap-2 text-sm">
          <span className="text-green-600 dark:text-green-400">✅ Status:</span>
          <span className="text-green-700 dark:text-green-300 font-medium">
            Full Access Granted
          </span>
        </div>
        <div className="mt-2 text-sm text-green-600 dark:text-green-400">
          <p>✅ Create new solutions</p>
          <p>✅ Edit existing solutions</p>
          <p>✅ Save changes</p>
          <p>✅ Delete solutions</p>
          <p>✅ Generate AI summaries</p>
        </div>
      </div>

      <div className="flex gap-3 justify-end">
        <Button
          onClick={handleLock}
          variant="warning"
        >
          🔒 Lock & Close
        </Button>
      </div>
    </div>
  );
};