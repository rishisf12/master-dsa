import re


def validate_url(url: str) -> bool:
    """Validate if the string is a valid URL."""
    if not url:
        return True  # URL is optional
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return bool(url_pattern.match(url))


def validate_complexity(complexity: str) -> bool:
    """Validate time/space complexity format."""
    if not complexity:
        return True  # Complexity is optional
    pattern = re.compile(r'^O\([a-zA-Z0-9\s]+\)$')
    return bool(pattern.match(complexity.strip()))


def validate_code(code: str) -> bool:
    """Validate code is not empty."""
    if code is None:
        return False
    return len(code.strip()) > 0