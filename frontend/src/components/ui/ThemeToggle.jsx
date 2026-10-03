import React from 'react';
import { FiSun, FiMoon } from 'react-icons/fi';
import { useStore } from '@store/store';

export const ThemeToggle = () => {
  const { isDarkMode, toggleDarkMode } = useStore();

  React.useEffect(() => {
    // Apply dark mode class to html element
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  return (
    <button
      onClick={toggleDarkMode}
      className="relative flex items-center justify-center w-10 h-10 rounded-full bg-white/20 hover:bg-white/30 text-white transition-all duration-300 transform hover:scale-110"
      aria-label="Toggle theme"
    >
      <div className="relative w-5 h-5">
        {/* Sun Icon */}
        <FiSun 
          className={`absolute inset-0 w-5 h-5 transition-all duration-300 transform ${
            isDarkMode 
              ? 'opacity-0 rotate-90 scale-50' 
              : 'opacity-100 rotate-0 scale-100'
          }`}
        />
        {/* Moon Icon */}
        <FiMoon 
          className={`absolute inset-0 w-5 h-5 transition-all duration-300 transform ${
            isDarkMode 
              ? 'opacity-100 rotate-0 scale-100' 
              : 'opacity-0 -rotate-90 scale-50'
          }`}
        />
      </div>
    </button>
  );
};