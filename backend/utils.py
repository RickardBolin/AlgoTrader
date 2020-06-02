from datetime import datetime
from time import mktime


# ONLY WORKS FOR DAILY DATA SO FAR!
'''
def convert_timestamp_to_unix(timestamp):
    date = datetime.strptime(str(timestamp)[:19], '%Y-%m-%d %H:%M:%S')

    #return int(mktime(date.timetuple()))
'''


def convert_timestamp_to_datetime(timestamp):
    return datetime.strptime(str(timestamp)[:19], '%Y-%m-%d %H:%M:%S')


def convert_datetime_to_timestamp(_datetime):
    return datetime.strftime(_datetime, '%Y-%m-%d %H:%M:%S')
'''


## ONLY WORKS FOR DAILY DATA SO FAR!
def convert_timestamp_to_unix(timestamp):
    date = datetime.strptime(str(timestamp)[:10], '%Y-%m-%d')
    return int(mktime(date.timetuple()))
'''
'''
def convert_unix_to_timestamp(unix_time):
    return datetime.fromtimestamp(unix_time)
'''
