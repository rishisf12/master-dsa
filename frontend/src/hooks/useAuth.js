import { useState } from 'react';
import { useStore } from '@store/store';
import { showToast } from '@utils/errorHandler';
import apiClient from '@api/client';
import { API_ENDPOINTS } from '@api/endpoints';

export const useAuth = () => {
  const [isVerifying, setIsVerifying] = useState(false);
  const { isAdminVerified, adminUsername, setAdminVerified, setAdminUsername } = useStore();

  const verifyUsername = async (username) => {
    setIsVerifying(true);
    try {
      const response = await apiClient.post(API_ENDPOINTS.VERIFY_ADMIN, { username });
      
      if (response.data.valid) {
        setAdminVerified(true);
        setAdminUsername(username);
        showToast.success(`Welcome back, ${username}!`);
        return true;
      } else {
        showToast.error('Invalid username. Please try again.');
        return false;
      }
    } catch (error) {
      showToast.error('Failed to verify username');
      console.error(error);
      return false;
    } finally {
      setIsVerifying(false);
    }
  };

  const logout = () => {
    setAdminVerified(false);
    setAdminUsername('');
    showToast.info('Logged out');
  };

  return {
    isAdminVerified,
    adminUsername,
    isVerifying,
    verifyUsername,
    logout,
  };
};