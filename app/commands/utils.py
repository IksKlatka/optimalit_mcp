from datetime import datetime, timezone


def is_rfc3339(date_string: str) -> bool:
    try:
        if date_string.endswith("Z"):
            datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        else:
            datetime.fromisoformat(date_string)
        return True
    except ValueError: return False

def end_after_start_date(start_date: str, end_date: str) -> bool:
    return start_date > end_date

def start_date_in_future(start_date: str) -> bool:
    start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    now_utc = datetime.now(timezone.utc)
    return start_dt >= now_utc

def is_string_non_empty(data: list[str]) -> bool:
    for value in data:
        if not isinstance(value, str) or not value.strip():
            return False
    return True