import React, { useState } from 'react';
import { Modal } from '@components/ui/Modal';
import { Input } from '@components/ui/Input';
import { Button } from '@components/ui/Button';
import { useAuth } from '@hooks/useAuth';
import { useStore } from '@store/store';
import { AdminVerified } from './AdminVerified';

export const AdminModal = ({ isOpen, onClose }) => {
  const [username, setUsername] = useState('');
  const { isAdminVerified, adminUsername } = useStore();
  const { verifyUsername, isVerifying } = useAuth();

  const handleVerify = async () => {
    if (!username.trim()) {
      return;
    }
    const success = await verifyUsername(username.trim());
    if (success) {
      setUsername('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleVerify();
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="👤 Admin Access"
    >
      {isAdminVerified ? (
        <AdminVerified onClose={onClose} />
      ) : (
        <div className="space-y-4">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Enter your admin username to unlock editing capabilities
          </p>

          <div className="flex gap-3">
            <Input
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1"
              disabled={isVerifying}
            />
            <Button
              onClick={handleVerify}
              isLoading={isVerifying}
              disabled={isVerifying || !username.trim()}
              variant="primary"
            >
              {isVerifying ? 'Verifying...' : '🔓 Verify'}
            </Button>
          </div>

          <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700/30 rounded-lg">
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-500 dark:text-gray-400">🔒 Status:</span>
              <span className="text-gray-700 dark:text-gray-300 font-medium">
                Read-Only Mode
              </span>
            </div>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
              Verify to create, edit, and delete solutions
            </p>
          </div>

          <div className="flex justify-end">
            <Button
              onClick={onClose}
              variant="secondary"
            >
              Cancel
            </Button>
          </div>
        </div>
      )}
    </Modal>
  );
};