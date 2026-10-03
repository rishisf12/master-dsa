import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useSolution } from '@hooks/useSolution';
import { useAI } from '@hooks/useAI';
import { useStore } from '@store/store';
import { ProblemMetadata } from './ProblemMetadata';
import { PythonEditor } from './CodeEditor/PythonEditor';
import { CppEditor } from './CodeEditor/CppEditor';
import { OutputPanel } from './OutputPanel';
import { ComplexityInput } from './ComplexityInput';
import { SolutionNavigation } from './SolutionNavigation';
import { SaveEditButtons } from './SaveEditButtons';
import { StatusBadge } from './StatusBadge';
import { AIAnalysis } from '@components/ai-analysis/AIAnalysis';
import { showToast } from '@utils/errorHandler';
import { getDefaultCode } from '@utils/codeUtils';

export const ProblemEditor = ({ date, problemNumber, dayId, existingSolution }) => {
  const navigate = useNavigate();
  const { isAdminVerified } = useStore();
  const { createSolution, updateSolution, isLoading } = useSolution(null, dayId, problemNumber);
  const { executeCode } = useAI();

  const [formData, setFormData] = useState({
    problemName: '',
    problemUrl: '',
    difficulty: 'easy',
    pattern: '',
    pythonCode: getDefaultCode('python'),
    cppCode: getDefaultCode('cpp'),
    pythonTimeComplexity: '',
    pythonSpaceComplexity: '',
    cppTimeComplexity: '',
    cppSpaceComplexity: '',
    notes: '',
  });

  const [output, setOutput] = useState({ python: '', cpp: '' });
  const [isSaving, setIsSaving] = useState(false);
  const [isEditing, setIsEditing] = useState(true);
  const [isComplete, setIsComplete] = useState(false);
  const [solutionId, setSolutionId] = useState(null);
  const [aiSummary, setAiSummary] = useState(null);

  // Load existing solution when available
  useEffect(() => {
    if (existingSolution) {
      console.log('Loading existing solution:', existingSolution);
      
      setFormData({
        problemName: existingSolution.problem_name || '',
        problemUrl: existingSolution.problem_url || '',
        difficulty: existingSolution.difficulty || 'easy',
        pattern: existingSolution.pattern || '',
        pythonCode: existingSolution.python_code || getDefaultCode('python'),
        cppCode: existingSolution.cpp_code || getDefaultCode('cpp'),
        pythonTimeComplexity: existingSolution.python_time_complexity || '',
        pythonSpaceComplexity: existingSolution.python_space_complexity || '',
        cppTimeComplexity: existingSolution.cpp_time_complexity || '',
        cppSpaceComplexity: existingSolution.cpp_space_complexity || '',
        notes: existingSolution.notes || '',
      });
      
      setSolutionId(existingSolution.id);
      setIsComplete(existingSolution.is_complete || false);
      setAiSummary(existingSolution.ai_summary || null);
      
      setIsEditing(false);
    } else {
      setFormData({
        problemName: '',
        problemUrl: '',
        difficulty: 'easy',
        pattern: '',
        pythonCode: getDefaultCode('python'),
        cppCode: getDefaultCode('cpp'),
        pythonTimeComplexity: '',
        pythonSpaceComplexity: '',
        cppTimeComplexity: '',
        cppSpaceComplexity: '',
        notes: '',
      });
      setSolutionId(null);
      setIsComplete(false);
      setAiSummary(null);
      setIsEditing(true);
    }
  }, [existingSolution]);

  const handleRunPython = async (executionInfo) => {
    const usePython3 = executionInfo?.usePython3 !== undefined ? executionInfo.usePython3 : true;
    const result = await executeCode('python', formData.pythonCode, '', usePython3);
    setOutput(prev => ({ ...prev, python: result.stdout || result.stderr }));
  };

  const handleRunCpp = async () => {
    const result = await executeCode('cpp', formData.cppCode);
    setOutput(prev => ({ ...prev, cpp: result.stdout || result.stderr }));
  };

  const handleSave = async () => {
    if (!isAdminVerified) {
      showToast.error('Please verify as admin to save');
      return;
    }

    if (!formData.problemName.trim()) {
      showToast.error('Please enter a problem name');
      return;
    }

    if (!dayId) {
      showToast.error('Invalid day. Please go back and select a day again.');
      return;
    }

    setIsSaving(true);
    try {
      const data = {
        problem_number: problemNumber,
        problem_name: formData.problemName,
        problem_url: formData.problemUrl,
        difficulty: formData.difficulty,
        pattern: formData.pattern,
        python_code: formData.pythonCode,
        cpp_code: formData.cppCode,
        python_time_complexity: formData.pythonTimeComplexity,
        python_space_complexity: formData.pythonSpaceComplexity,
        cpp_time_complexity: formData.cppTimeComplexity,
        cpp_space_complexity: formData.cppSpaceComplexity,
        notes: formData.notes,
        day_id: dayId,
        is_saved: true,
        is_complete: isComplete,
      };

      let result;
      if (solutionId) {
        result = await updateSolution({ id: solutionId, data });
        showToast.success('Solution updated successfully!');
      } else {
        result = await createSolution(data);
        setSolutionId(result.id);
        showToast.success('Solution saved successfully!');
      }
      
      setIsEditing(false);
    } catch (error) {
      console.error('Save error:', error);
      
      if (error?.response?.status === 409) {
        showToast.error('A solution already exists for this day. Try editing it.');
      } else {
        showToast.error(error?.response?.data?.detail || 'Failed to save solution');
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    if (solutionId) {
      setIsEditing(false);
      if (existingSolution) {
        setFormData({
          problemName: existingSolution.problem_name || '',
          problemUrl: existingSolution.problem_url || '',
          difficulty: existingSolution.difficulty || 'easy',
          pattern: existingSolution.pattern || '',
          pythonCode: existingSolution.python_code || getDefaultCode('python'),
          cppCode: existingSolution.cpp_code || getDefaultCode('cpp'),
          pythonTimeComplexity: existingSolution.python_time_complexity || '',
          pythonSpaceComplexity: existingSolution.python_space_complexity || '',
          cppTimeComplexity: existingSolution.cpp_time_complexity || '',
          cppSpaceComplexity: existingSolution.cpp_space_complexity || '',
          notes: existingSolution.notes || '',
        });
        setAiSummary(existingSolution.ai_summary || null);
        setIsComplete(existingSolution.is_complete || false);
      }
    } else {
      setFormData({
        problemName: '',
        problemUrl: '',
        difficulty: 'easy',
        pattern: '',
        pythonCode: getDefaultCode('python'),
        cppCode: getDefaultCode('cpp'),
        pythonTimeComplexity: '',
        pythonSpaceComplexity: '',
        cppTimeComplexity: '',
        cppSpaceComplexity: '',
        notes: '',
      });
      setAiSummary(null);
      setIsComplete(false);
      setIsEditing(true);
    }
  };

  const handleMarkComplete = () => {
    setIsComplete(!isComplete);
    showToast.success(isComplete ? 'Marked as incomplete' : 'Marked as complete!');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <button
            onClick={() => navigate('/calendar')}
            className="text-blue-600 dark:text-blue-400 hover:underline text-sm"
          >
            ← Back to Calendar
          </button>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
            {date.toLocaleDateString('en-US', {
              month: 'long',
              day: 'numeric',
              year: 'numeric'
            })} - {date.toLocaleDateString('en-US', { weekday: 'long' })}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Problem {problemNumber} of 3
          </p>
        </div>
        <StatusBadge
          isSaved={!isEditing && solutionId}
          isComplete={isComplete}
        />
      </div>

      {/* Problem Metadata */}
      <ProblemMetadata
        formData={formData}
        setFormData={setFormData}
        isEditing={isEditing}
      />

      {/* Code Editors */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <PythonEditor
          code={formData.pythonCode}
          onChange={(value) => setFormData({ ...formData, pythonCode: value })}
          onRun={handleRunPython}
          isEditing={isEditing}
        />
        <CppEditor
          code={formData.cppCode}
          onChange={(value) => setFormData({ ...formData, cppCode: value })}
          onRun={handleRunCpp}
          isEditing={isEditing}
        />
      </div>

      {/* Output Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <OutputPanel
          language="Python"
          output={output.python}
        />
        <OutputPanel
          language="C++"
          output={output.cpp}
        />
      </div>

      {/* Complexity Input */}
      <ComplexityInput
        formData={formData}
        setFormData={setFormData}
        isEditing={isEditing}
      />

      {/* AI Analysis */}
      <AIAnalysis
        solutionId={solutionId}
        pythonCode={formData.pythonCode}
        cppCode={formData.cppCode}
        problemName={formData.problemName}
        pythonTimeComplexity={formData.pythonTimeComplexity}
        pythonSpaceComplexity={formData.pythonSpaceComplexity}
        cppTimeComplexity={formData.cppTimeComplexity}
        cppSpaceComplexity={formData.cppSpaceComplexity}
        notes={formData.notes}
        isEditing={isEditing}
        isAdminVerified={isAdminVerified}
        existingSummary={aiSummary}
      />

      {/* Save/Edit Buttons */}
      <SaveEditButtons
        isEditing={isEditing}
        isSaving={isSaving}
        isLoading={isLoading}
        isAdminVerified={isAdminVerified}
        onSave={handleSave}
        onEdit={handleEdit}
        onCancel={handleCancel}
      />

      {/* Navigation */}
      <SolutionNavigation
        currentProblem={problemNumber}
        date={date}
        onMarkComplete={handleMarkComplete}
        isComplete={isComplete}
      />
    </div>
  );
};