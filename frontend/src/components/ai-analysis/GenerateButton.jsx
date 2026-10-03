import React from 'react';
import { Button } from '@components/ui/Button';

export const GenerateButton = ({ onClick, isGenerating, isDisabled }) => {
  return (
    <Button
      onClick={onClick}
      disabled={isDisabled || isGenerating}
      variant="primary"
      loading={isGenerating}
    >
      {isGenerating ? 'Generating...' : '🤖 Generate Summary & Comparison'}
    </Button>
  );
};