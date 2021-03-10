"""This is a practice file to get timedelta working.
   This is so as to find the nearest Monday for data from the CDC APIs on vaccinations.
   These are organized by Monday dates."""

## TIMEDELTA TUTORIAL
## https://www.guru99.com/date-time-and-datetime-classes-in-python.html#5
#
## Help with the idea of weekday[index]
## https://stackoverflow.com/questions/1622038/find-mondays-date-with-python

from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

def get_most_recent_past_monday(phrase_date_str):
    """Takes in the date as a string, such as '2021-02-04' 
       and returns the most recent past Monday. 
       The string is in form'%Y-%m-%d'.
       
       >>> get_most_recent_past_monday('2021-02-04')
       2021-02-01
       """

    date_str = phrase_date_str
    date_str_obj = datetime.strptime(date_str, '%Y-%m-%d') #create datetime obj
    #print(date_str_obj)
    day = date_str_obj.weekday() # index of weekday, with Monday at '0' index
    #print(day)
    days = (0 - day) # how many days from Monday
    # print(days)
    new_date=str(date_str_obj + timedelta(days=days)) # datetime obj into a datetime.datetime obj
    #print(new_date)
    mon_date=new_date[:11]                            # so as to use with timedelta
    #print(mon_date)
    return mon_date

print((get_most_recent_past_monday('2021-01-02')))
