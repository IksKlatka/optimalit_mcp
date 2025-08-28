from datetime import datetime


def is_rfc3339(date_string: str) -> bool:
    try:
        if date_string.endswith("Z"):
            datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        else:
            datetime.fromisoformat(date_string)
        return True
    except ValueError: return False


def is_string_non_empty(data: list[str]) -> bool:
    for value in data:
        if not isinstance(value, str) or not value.strip():
            return False
    return True
