import React from 'react';
import { Input } from '@components/ui/Input';
import { Select } from '@components/ui/Select';
import { DIFFICULTIES, PATTERNS } from '@utils/constants';

export const ProblemMetadata = ({ formData, setFormData, isEditing }) => {
  const difficultyOptions = DIFFICULTIES.map(d => ({
    value: d,
    label: d.charAt(0).toUpperCase() + d.slice(1)
  }));

  const patternOptions = PATTERNS.map(p => ({
    value: p.toLowerCase().replace(/\s/g, '-'),
    label: p
  }));

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Problem Details
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Problem Name"
          value={formData.problemName}
          onChange={(e) => setFormData({ ...formData, problemName: e.target.value })}
          placeholder="e.g., Two Sum"
          disabled={!isEditing}
        />
        <Input
          label="Problem URL"
          value={formData.problemUrl}
          onChange={(e) => setFormData({ ...formData, problemUrl: e.target.value })}
          placeholder="https://leetcode.com/problems/..."
          disabled={!isEditing}
        />
        <Select
          label="Difficulty"
          value={formData.difficulty}
          onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
          options={difficultyOptions}
          disabled={!isEditing}
        />
        <Select
          label="Pattern"
          value={formData.pattern}
          onChange={(e) => setFormData({ ...formData, pattern: e.target.value })}
          options={patternOptions}
          placeholder="Select pattern..."
          disabled={!isEditing}
        />
      </div>
    </div>
  );
};