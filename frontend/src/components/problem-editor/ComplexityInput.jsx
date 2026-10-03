import React from 'react';
import { Input } from '@components/ui/Input';

export const ComplexityInput = ({ formData, setFormData, isEditing }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        📊 Complexity & Intuition
      </h3>
      <div className="space-y-4">
        {/* Python Complexity */}
        <div className="p-4 bg-blue-50 dark:bg-blue-900/10 rounded-lg border border-blue-200 dark:border-blue-800">
          <h4 className="text-sm font-semibold text-blue-700 dark:text-blue-300 mb-3">
            🐍 Python
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Time Complexity"
              value={formData.pythonTimeComplexity || ''}
              onChange={(e) => setFormData({ ...formData, pythonTimeComplexity: e.target.value })}
              placeholder="e.g., O(n)"
              disabled={!isEditing}
            />
            <Input
              label="Space Complexity"
              value={formData.pythonSpaceComplexity || ''}
              onChange={(e) => setFormData({ ...formData, pythonSpaceComplexity: e.target.value })}
              placeholder="e.g., O(1)"
              disabled={!isEditing}
            />
          </div>
        </div>

        {/* C++ Complexity */}
        <div className="p-4 bg-purple-50 dark:bg-purple-900/10 rounded-lg border border-purple-200 dark:border-purple-800">
          <h4 className="text-sm font-semibold text-purple-700 dark:text-purple-300 mb-3">
            ⚡ C++
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Time Complexity"
              value={formData.cppTimeComplexity || ''}
              onChange={(e) => setFormData({ ...formData, cppTimeComplexity: e.target.value })}
              placeholder="e.g., O(n)"
              disabled={!isEditing}
            />
            <Input
              label="Space Complexity"
              value={formData.cppSpaceComplexity || ''}
              onChange={(e) => setFormData({ ...formData, cppSpaceComplexity: e.target.value })}
              placeholder="e.g., O(1)"
              disabled={!isEditing}
            />
          </div>
        </div>

        {/* Notes - Shared */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Notes / Intuition
          </label>
          <textarea
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            placeholder="Explain your approach..."
            disabled={!isEditing}
            className="w-full px-4 py-2 border rounded-lg transition-colors duration-200 bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 disabled:cursor-not-allowed min-h-20"
          />
        </div>
      </div>
    </div>
  );
};