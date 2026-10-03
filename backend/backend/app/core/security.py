from app.core.config import settings


def verify_admin_username(username: str) -> bool:
    """
    Verify if the provided username matches the admin username.

    Args:
        username: The username to verify

    Returns:
        True if username matches admin, False otherwise
    """
    return username == settings.ADMIN_USERNAME


def get_admin_username() -> str:
    """Get the configured admin username."""
    return settings.ADMIN_USERNAME