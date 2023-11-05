from babel.dates import format_date, format_datetime, format_time
import iso8601
from datetime import datetime

def parseFullMonth(date: str):

    dt = datetime.strptime(date, "%Y-%m-%d")
    suffix = ('st' if dt.day in [1,21,31] else 'nd' if dt.day in [2, 22]  else 'rd' if dt.day in [3, 23] else 'th')
    date = iso8601.parse_date(date)
    new_format = format_datetime(date, "MMMM dd", locale='en')
    day = new_format.split(" ")[1] if new_format.split(" ")[1][0] != '0' else new_format.split(" ")[1][1]
    return new_format.split(" ")[0] + " " + day + suffix

def parseHalfMonth(date: str):
    date = datetime.strptime(date, "%Y-%m-%d")
    return format_datetime(date).split(",")[0]
