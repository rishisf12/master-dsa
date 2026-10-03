from datetime import datetime, timedelta
from dateutil import parser


def get_month_days(year: int, month: int):
    """Get all days in a month."""
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    
    first_day = datetime(year, month, 1)
    days = []
    
    current_day = first_day
    while current_day < next_month:
        days.append(current_day)
        current_day += timedelta(days=1)
    
    return days


def get_week_number(date: datetime) -> int:
    """Get week number of the month for a given date."""
    first_day = datetime(date.year, date.month, 1)
    delta = date - first_day
    return (delta.days // 7) + 1


def format_date(date: datetime) -> str:
    """Format date as YYYY-MM-DD."""
    return date.strftime("%Y-%m-%d")


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime."""
    return parser.parse(date_str)