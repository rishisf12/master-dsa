import React, { useState } from 'react';
import Editor from '@monaco-editor/react';

export const CodeEditor = ({ 
  language, 
  value, 
  onChange, 
  onRun, 
  isEditing,
  label,
  showVersionSwitch = false, // New prop to show Python version toggle
}) => {
  const editorRef = React.useRef(null);
  const [usePython3, setUsePython3] = useState(true); // Default to Python3

  const handleEditorDidMount = (editor) => {
    editorRef.current = editor;
  };

  const handleRunClick = () => {
    // Pass the python version info to the parent
    const executionInfo = {
      language: language,
      usePython3: usePython3,
    };
    onRun(executionInfo);
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div className="flex items-center justify-between px-4 py-2 bg-gray-50 dark:bg-gray-700/50 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {label}
          </span>
          {/* Python Version Switch */}
          {showVersionSwitch && language === 'python' && (
            <div className="flex items-center gap-1 bg-gray-200 dark:bg-gray-600 rounded-md p-0.5">
              <button
                onClick={() => setUsePython3(false)}
                className={`px-2 py-0.5 text-xs rounded transition-colors ${
                  !usePython3 
                    ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' 
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                }`}
              >
                Python 2
              </button>
              <button
                onClick={() => setUsePython3(true)}
                className={`px-2 py-0.5 text-xs rounded transition-colors ${
                  usePython3 
                    ? 'bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm' 
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                }`}
              >
                Python 3
              </button>
            </div>
          )}
        </div>
        <button
          onClick={handleRunClick}
          disabled={!isEditing}
          className={`
            px-3 py-1 text-sm font-medium rounded-lg transition-colors
            ${isEditing 
              ? 'bg-green-600 hover:bg-green-700 text-white' 
              : 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
            }
          `}
        >
          ▶ Run
        </button>
      </div>
      <Editor
        height="300px"
        language={language}
        value={value}
        onChange={onChange}
        onMount={handleEditorDidMount}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          tabSize: 2,
          wordWrap: 'on',
          readOnly: !isEditing,
          automaticLayout: true,
        }}
      />
    </div>
  );
};