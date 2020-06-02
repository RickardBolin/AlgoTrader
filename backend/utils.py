from datetime import datetime
from time import mktime


def convert_timestamp_to_datetime(timestamp):
    timestamp_length = len(str(timestamp))
    if timestamp_length == 19:
        return datetime.strptime(str(timestamp), '%Y-%m-%d %H:%M:%S')
    elif timestamp_length == 25:
        dt = datetime.strptime(str(timestamp)[:19], '%Y-%m-%d %H:%M:%S')
        shift = datetime.strptime(str(timestamp)[19:], '-%H:%M')
        dt = datetime.replace(dt, hour=dt.hour + shift.hour, minute=dt.minute + shift.minute)
        return dt
    else:
        print("Wrong format/lengths! The length of the timestamp is " + str(timestamp_length) + ". Only 19 and 25 currently allowed.")


def convert_datetime_to_timestamp(_datetime):
    return datetime.strftime(_datetime, '%Y-%m-%d %H:%M:%S')
