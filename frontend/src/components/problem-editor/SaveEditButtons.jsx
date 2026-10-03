import React from 'react';
import { Button } from '@components/ui/Button';

export const SaveEditButtons = ({ 
  isEditing, 
  isSaving, 
  isloading, 
  isAdminVerified,
  onSave, 
  onEdit, 
  onCancel 
}) => {
  if (isEditing) {
    return (
      <div className="flex gap-3">
        <Button
          onClick={onSave}
          loading={isSaving || isloading}
          disabled={!isAdminVerified || isSaving}
          variant="success"
        >
          💾 Save Problem
        </Button>
        <Button
          onClick={onCancel}
          variant="secondary"
        >
          Cancel
        </Button>
        {!isAdminVerified && (
          <p className="text-sm text-red-500 flex items-center">
            ⚠️ Please verify as admin to save
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="flex gap-3">
      <Button
        onClick={onEdit}
        variant="primary"
      >
        ✏️ Edit Problem
      </Button>
    </div>
  );
};