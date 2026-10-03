import React from 'react';
import { Badge } from '@components/ui/Badge';

export const StatusBadge = ({ isSaved, isComplete }) => {
  if (isComplete) {
    return <Badge variant="success">✅ Complete</Badge>;
  }
  if (isSaved) {
    return <Badge variant="info">💾 Saved</Badge>;
  }
  return <Badge variant="warning">📝 Draft</Badge>;
};