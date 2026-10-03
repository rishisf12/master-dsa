export const formatComplexity = (complexity) => {
  if (!complexity) return 'Not specified'
  return complexity
}

export const truncateText = (text, maxLength = 50) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}