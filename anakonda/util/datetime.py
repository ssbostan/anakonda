from datetime import datetime

from pytz import timezone

from anakonda.config import Config


def now():
    return datetime.now(tz=timezone(Config.TIMEZONE))
