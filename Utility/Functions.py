from datetime import datetime
import time

def timeConvert(ms):
    return datetime.fromtimestamp(ms/1000.0)


def current_milli_time():
    return round(time.time() * 1000)