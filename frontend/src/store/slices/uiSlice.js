export const createUISlice = (set, get) => ({
  // State
  isAdminVerified: false,
  adminUsername: '',
  isDarkMode: false, // ✅ Add this
  isModalOpen: false,
  modalContent: null,
  toastMessage: null,

  // Actions
  setAdminVerified: (status) => set({ isAdminVerified: status }),
  
  setAdminUsername: (username) => set({ adminUsername: username }),
  
  // ✅ Add dark mode actions
  toggleDarkMode: () => set((state) => ({ 
    isDarkMode: !state.isDarkMode 
  })),
  
  setDarkMode: (isDark) => set({ isDarkMode: isDark }),
  
  openModal: (content) => set({ isModalOpen: true, modalContent: content }),
  
  closeModal: () => set({ isModalOpen: false, modalContent: null }),
  
  setToast: (message) => set({ toastMessage: message }),
  
  clearToast: () => set({ toastMessage: null }),
});