import datetime


def get_utc_plus_8_time_now(datetime_format: bool = False) -> str or datetime.datetime:
    time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    if datetime_format:
        return time_now
    else:
        return time_now.isoformat()


def iso_to_datetime(iso_str: str) -> datetime:
    return datetime.datetime.fromisoformat(iso_str)
