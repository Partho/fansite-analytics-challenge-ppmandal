"""
A time utility class providing basic functionalities like
converting string to datetime, finding difference between
two timestamps etc.

"""
from datetime import datetime, timedelta
import time

class TimeUtility:
    # Convert string to datetime  of format 01/Jul/1995:00:00:01 -0400
    @staticmethod
    def str_to_date(date_str):
        time_struct = time.strptime(date_str, "%d/%b/%Y:%H:%M:%S -0400") 
        date = datetime.fromtimestamp(time.mktime(time_struct))
        return date

    # convert datetime format to string 
    @staticmethod
    def date_to_str(datetime_str):  
        return datetime_str.strftime("%d/%b/%Y:%H:%M:%S -0400")

    # add second to datetime object
    @staticmethod
    def add_second(date_str,sec):   
        return date_str + timedelta(seconds=sec)

    # find difference between two times
    @staticmethod
    def time_diff(date2, date1): 
        return (date2 - date1).seconds