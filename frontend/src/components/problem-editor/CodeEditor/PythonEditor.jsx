import React from 'react';
import { CodeEditor } from './CodeEditor';

export const PythonEditor = ({ code, onChange, onRun, isEditing }) => {
  return (
    <CodeEditor
      language="python"
      value={code}
      onChange={onChange}
      onRun={onRun}  // Now receives executionInfo
      isEditing={isEditing}
      label="🐍 Python"
      showVersionSwitch={true}  // ✅ Show Python version toggle
    />
  );
};