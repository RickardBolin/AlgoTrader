from datetime import datetime
from time import mktime


## ONLY WORKS FOR DAILY DATA SO FAR!
def convert_timestamp_to_unix(timestamp):
    date = datetime.strptime(str(timestamp)[:10], '%Y-%m-%d')
    return int(mktime(date.timetuple()))


def convert_unix_to_timestamp(unix_time):
    return datetime.utcfromtimestamp(unix_time)
