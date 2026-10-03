import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useStore } from '@store/store';
import { FiCalendar, FiCheckCircle, FiTrendingUp, FiCode } from 'react-icons/fi';
import { useQuery } from '@tanstack/react-query';
import { solutionService } from '@api/services/solutionService';
import { Loader } from '@components/common/Loader';

export const HomePage = () => {
  const navigate = useNavigate();
  const { isAdminVerified } = useStore();

  const { data: stats, isLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      try {
        const result = await solutionService.getStats();
        return result;
      } catch (err) {
        return { total: 0, solved: 0, streak: 0 };
      }
    },
    refetchOnWindowFocus: true,
    refetchInterval: 10000,
  });

  const statsData = stats || { total: 0, solved: 0, streak: 0 };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12">
        <Loader message="Loading your progress..." />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* ✅ Gradient Header with Glass Effect */}
      <div className="text-center mb-12">
        <div className="inline-block p-8 rounded-2xl bg-linear-to-r from-blue-600 via-purple-600 to-indigo-600 shadow-xl">
          <h1 className="text-4xl font-bold text-white mb-2">
            📊 Your Progress Dashboard
          </h1>
          <p className="text-blue-100">
            {isAdminVerified ? '🔓 Admin Mode - Full Access' : '👀 View Mode'}
          </p>
          <p className="text-blue-200 text-sm mt-2">
            {statsData.total === 0 
              ? '🚀 Start solving 3 problems daily to track your progress!' 
              : `⭐ You've solved ${statsData.solved} out of ${statsData.total} problems`}
          </p>
        </div>
      </div>

      {/* ✅ Gradient Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {/* Total Problems - Blue Gradient */}
        <div className="relative overflow-hidden bg-linear-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full -ml-12 -mb-12"></div>
          <div className="relative flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-blue-100">Total Problems</p>
              <p className="text-3xl font-bold text-white mt-1">
                {statsData.total}
              </p>
            </div>
            <div className="bg-white/20 p-3 rounded-lg backdrop-blur-sm">
              <FiCode className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Solved - Green Gradient */}
        <div className="relative overflow-hidden bg-linear-to-br from-emerald-500 to-emerald-600 rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full -ml-12 -mb-12"></div>
          <div className="relative flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-emerald-100">Solved</p>
              <p className="text-3xl font-bold text-white mt-1">
                {statsData.solved}
              </p>
            </div>
            <div className="bg-white/20 p-3 rounded-lg backdrop-blur-sm">
              <FiCheckCircle className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>

        {/* Streak - Orange/Red Gradient */}
        <div className="relative overflow-hidden bg-linear-to-br from-orange-500 to-red-500 rounded-xl shadow-lg p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
          <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -mr-16 -mt-16"></div>
          <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full -ml-12 -mb-12"></div>
          <div className="relative flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-orange-100">Current Streak</p>
              <p className="text-3xl font-bold text-white mt-1">
                {statsData.streak} days
              </p>
            </div>
            <div className="bg-white/20 p-3 rounded-lg backdrop-blur-sm">
              <FiTrendingUp className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>
      </div>

      {/* Empty State */}
      {statsData.total === 0 && (
        <div className="text-center mb-8 p-12 rounded-2xl bg-linear-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 border border-blue-100 dark:border-gray-600">
          <div className="text-6xl mb-4">🚀</div>
          <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
            Ready to start your DSA journey?
          </h3>
          <p className="text-gray-500 dark:text-gray-400 mt-2">
            Solve 3 problems daily in Python and C++.
          </p>
        </div>
      )}

      {/* ✅ Gradient Button */}
      <div className="flex justify-center">
        <button
          onClick={() => navigate('/calendar')}
          className="flex items-center gap-3 px-8 py-4 bg-linear-to-r from-blue-600 via-purple-600 to-indigo-600 hover:from-blue-700 hover:via-purple-700 hover:to-indigo-700 text-white font-semibold rounded-lg transition-all duration-300 shadow-lg hover:shadow-xl text-lg transform hover:-translate-y-1"
        >
          <FiCalendar className="w-5 h-5" />
          {statsData.total === 0 ? 'Start Solving Today' : 'Continue Practicing'}
        </button>
      </div>
    </div>
  );
};