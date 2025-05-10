from datetime import datetime
from zoneinfo import ZoneInfo

utc_timezone = ZoneInfo('UTC')


def datetime_now_with_timezone(timezone: ZoneInfo = utc_timezone) -> datetime:
    if not isinstance(timezone, ZoneInfo):
        raise TypeError(f"Expected pytz timezone, got {type(timezone).__name__}")

    now_utc = datetime.now(timezone)

    if timezone.key == 'UTC':
        return now_utc

    return now_utc.astimezone(timezone)
