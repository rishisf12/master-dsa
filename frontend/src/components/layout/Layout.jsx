import React from 'react';
import { Header } from './Header';

export const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-linear-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-slate-800 dark:to-gray-900 transition-colors duration-300">
      <Header />
      <main className="flex-1">
        {children}
      </main>
    </div>
  );
};