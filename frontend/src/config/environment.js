// ✅ Use WITHOUT /api/v1 - client.js will add it
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://master-dsa-backend.onrender.com'

export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Master DSA'
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0'
export const IS_DEV = import.meta.env.DEV
export const IS_PROD = import.meta.env.PROD