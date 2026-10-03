import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FiHome, FiCalendar, FiUser } from 'react-icons/fi';
import { useStore } from '@store/store';
import { useAuth } from '@hooks/useAuth';
import { AdminModal } from '@components/admin/AdminModal';
import { ThemeToggle } from '@components/ui/ThemeToggle'; // ✅ Import ThemeToggle

export const Header = () => {
  const navigate = useNavigate();
  const { isAdminVerified } = useStore();
  const { logout } = useAuth();
  const [isAdminModalOpen, setIsAdminModalOpen] = useState(false);

  const handleAdminClick = () => {
    setIsAdminModalOpen(true);
  };

  return (
    <>
      <header className="sticky top-0 z-40 bg-linear-to-r from-blue-600 via-indigo-600 to-purple-600 shadow-lg dark:from-gray-800 dark:via-gray-900 dark:to-gray-950 transition-all duration-500">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2">
              <span className="text-2xl">🚀</span>
              <span className="text-xl font-bold text-white">
                Master DSA
              </span>
            </Link>

            {/* Navigation Buttons */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => navigate('/')}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white/90 hover:text-white hover:bg-white/20 rounded-lg transition-all duration-200"
              >
                <FiHome className="w-4 h-4" />
                Home
              </button>

              <button
                onClick={() => navigate('/calendar')}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white/90 hover:text-white hover:bg-white/20 rounded-lg transition-all duration-200"
              >
                <FiCalendar className="w-4 h-4" />
                Calendar
              </button>

              {/* ✅ Theme Toggle Button */}
              <ThemeToggle />

              <button
                onClick={handleAdminClick}
                className={`flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
                  isAdminVerified
                    ? 'bg-white/30 text-white hover:bg-white/40'
                    : 'text-white/90 hover:text-white hover:bg-white/20'
                }`}
              >
                <FiUser className="w-4 h-4" />
                {isAdminVerified ? 'Admin' : 'Login'}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Admin Modal */}
      <AdminModal
        isOpen={isAdminModalOpen}
        onClose={() => setIsAdminModalOpen(false)}
      />
    </>
  );
};