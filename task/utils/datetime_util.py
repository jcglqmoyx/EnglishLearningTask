import datetime


def get_date_str():
    yesterday_now = datetime.datetime.now() - datetime.timedelta(days=1)
    year, month, day = yesterday_now.year, yesterday_now.month, yesterday_now.day
    res = '%d-' % year
    if month < 10:
        res += '0'
    res += '%d-' % month
    if day < 10:
        res += '0'
    res += '%d' % day
    return res


def get_beginning_of_day(time: datetime.datetime):
    hour, minute, second, microsecond = time.hour, time.minute, time.second, time.microsecond
    beginning_of_day = time - datetime.timedelta(
        hours=hour,
        minutes=minute,
        seconds=second,
        microseconds=microsecond,
    )
    return beginning_of_day
