export const LANGUAGE_CONFIG = {
  python: {
    name: 'Python',
    extension: 'py',
    defaultCode: `class Solution:\n    def solve(self):\n        # Write your solution here\n        pass`,
  },
  cpp: {
    name: 'C++',
    extension: 'cpp',
    defaultCode: `class Solution {\npublic:\n    void solve() {\n        // Write your solution here\n    }\n};`,
  }
}

export const getDefaultCode = (language) => {
  return LANGUAGE_CONFIG[language]?.defaultCode || ''
}

export const getLanguageName = (language) => {
  return LANGUAGE_CONFIG[language]?.name || language
}