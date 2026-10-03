export const isValidUrl = (string) => {
  try {
    new URL(string)
    return true
  } catch (_) {
    return false
  }
}

export const isValidComplexity = (complexity) => {
  if (!complexity) return false
  const pattern = /^O\([a-zA-Z0-9 ]+\)$/
  return pattern.test(complexity.trim())
}

export const isValidCode = (code) => {
  return code && code.trim().length > 0
}