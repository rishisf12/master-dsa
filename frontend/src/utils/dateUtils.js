import { format, startOfMonth, endOfMonth, eachDayOfInterval, getDay } from 'date-fns'

export const getMonthDays = (year, month) => {
  const start = startOfMonth(new Date(year, month))
  const end = endOfMonth(new Date(year, month))
  return eachDayOfInterval({ start, end })
}

export const getWeeksInMonth = (year, month) => {
  const days = getMonthDays(year, month)
  const weeks = []
  let currentWeek = []

  const firstDay = getDay(days[0])
  const padding = firstDay === 0 ? 6 : firstDay - 1
  
  for (let i = 0; i < padding; i++) {
    currentWeek.push(null)
  }

  days.forEach((day) => {
    currentWeek.push(day)
    if (currentWeek.length === 7) {
      weeks.push(currentWeek)
      currentWeek = []
    }
  })

  while (currentWeek.length < 7 && currentWeek.length > 0) {
    currentWeek.push(null)
  }
  if (currentWeek.length > 0) {
    weeks.push(currentWeek)
  }

  return weeks
}

export const formatDate = (date) => {
  return format(date, 'MMM d, yyyy')
}

export const getDateKey = (date) => {
  return format(date, 'yyyy-MM-dd')
}

export const isToday = (date) => {
  const today = new Date()
  return date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear()
}

export const getMonthName = (monthIndex) => {
  const months = ['August', 'September', 'October', 'November']
  return months[monthIndex] || 'Unknown'
}