import datetime

DAY_FORMAT = "%Y-%m-%d"
DEFAULT_TO_DAY = datetime.datetime.now().strftime(DAY_FORMAT)
DEFAULT_DAY = datetime.datetime(year=datetime.datetime.now().year, month=1, day=1).strftime(DAY_FORMAT)
DEFAULT_FROM_DAY = DEFAULT_DAY
