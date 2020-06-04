from datetime import datetime


def convert_timestamp_to_datetime(timestamp):
    """
    Converter from timestamp unit to datetime unit.
    :param timestamp: Timestamp to be converted.
    :return: Datetime object.
    """
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
    """
    Converts datetime object to timestamp.
    :param _datetime: Datetime object to be converted.
    :return: Timestamp unit.
    """
    return datetime.strftime(_datetime, '%Y-%m-%d %H:%M:%S')
