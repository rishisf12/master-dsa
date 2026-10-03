import { useStore } from '@store/store';
import { showToast } from '@utils/errorHandler';

export const useToast = () => {
  const { toastMessage, setToast, clearToast } = useStore();

  const showSuccess = (message) => {
    showToast.success(message);
    setToast({ type: 'success', message });
    setTimeout(clearToast, 4000);
  };

  const showError = (message) => {
    showToast.error(message);
    setToast({ type: 'error', message });
    setTimeout(clearToast, 4000);
  };

  const showInfo = (message) => {
    showToast.info(message);
    setToast({ type: 'info', message });
    setTimeout(clearToast, 4000);
  };

  return {
    toastMessage,
    showSuccess,
    showError,
    showInfo,
    clearToast,
  };
};