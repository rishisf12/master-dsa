import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { Layout } from '@components/layout/Layout';
import { HomePage } from '@pages/HomePage';
import { CalendarPage } from '@pages/CalendarPage';
import { ProblemPage } from '@pages/ProblemPage';
import { useStore } from '@store/store';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
});

function App() {
  const { isDarkMode } = useStore();

  // ✅ Apply dark mode on initial load
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/calendar" element={<CalendarPage />} />
            <Route path="/problem/:date/:qNumber" element={<ProblemPage />} />
          </Routes>
        </Layout>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: isDarkMode ? '#1f2937' : '#ffffff',
              color: isDarkMode ? '#f9fafb' : '#1f2937',
              borderRadius: '8px',
              padding: '12px 16px',
            },
            success: {
              style: {
                background: isDarkMode ? '#065f46' : '#d1fae5',
                color: isDarkMode ? '#ecfdf5' : '#065f46',
              },
            },
            error: {
              style: {
                background: isDarkMode ? '#991b1b' : '#fef2f2',
                color: isDarkMode ? '#fef2f2' : '#991b1b',
              },
            },
          }}
        />
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;