from datetime import datetime

import pytz


def get_date_and_time_with_timezone(timezone: pytz = pytz.UTC) -> datetime:
    timestamp = datetime.now()
    return timestamp.astimezone(timezone)
