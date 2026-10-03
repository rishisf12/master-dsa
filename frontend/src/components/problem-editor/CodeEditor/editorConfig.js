export const EDITOR_CONFIG = {
  fontSize: 14,
  tabSize: 2,
  wordWrap: 'on',
  minimap: { enabled: false },
  automaticLayout: true,
  scrollbar: {
    vertical: 'visible',
    horizontal: 'visible',
  },
  padding: { top: 10, bottom: 10 },
};

export const LANGUAGE_CONFIG = {
  python: {
    language: 'python',
    defaultCode: `class Solution:\n    def solve(self):\n        # Write your solution here\n        pass`,
  },
  cpp: {
    language: 'cpp',
    defaultCode: `class Solution {\npublic:\n    void solve() {\n        // Write your solution here\n    }\n};`,
  },
};