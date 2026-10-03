import React from 'react';
import { CodeEditor } from './CodeEditor';

export const CppEditor = ({ code, onChange, onRun, isEditing }) => {
  return (
    <CodeEditor
      language="cpp"
      value={code}
      onChange={onChange}
      onRun={onRun}
      isEditing={isEditing}
      label="⚡ C++"
    />
  );
};