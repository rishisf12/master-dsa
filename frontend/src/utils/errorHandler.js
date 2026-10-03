import toast from 'react-hot-toast'

export const handleApiError = (error) => {
  console.error('API Error:', error)
  
  let message = 'Something went wrong'
  
  if (error.response) {
    message = error.response.data?.detail || error.response.data?.message || `Error ${error.response.status}`
  } else if (error.request) {
    message = 'Network error - Please check your connection'
  } else {
    message = error.message || 'Unknown error occurred'
  }
  
  toast.error(message)
  return message
}

export const showToast = {
  success: (message) => toast.success(message),
  error: (message) => toast.error(message),
  info: (message) => toast(message),
}