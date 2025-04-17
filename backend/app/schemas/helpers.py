import re


def validate_email_username(value: str) -> str:
    """
    Ensures the part before @ in email is alphanumeric lowercase.
    """
    # Split the email to get the username part (before @)
    if "@" not in value:
        raise ValueError("Email must contain '@'")

    username = value.split("@")[0]
    # Check if username contains only lowercase alphanumeric characters
    if not re.match(r"^[a-z0-9]+$", username):
        raise ValueError("Email username must contain only lowercase alphanumeric characters")

    return value.lower()


def validate_password_strength(value: str) -> str:
    """
    Validates password strength with common requirements:
    - At least 8 characters
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long")

    if not re.search(r"[A-Z]", value):
        raise ValueError("Password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", value):
        raise ValueError("Password must contain at least one lowercase letter")

    if not re.search(r"[0-9]", value):
        raise ValueError("Password must contain at least one digit")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValueError("Password must contain at least one special character")

    return value
