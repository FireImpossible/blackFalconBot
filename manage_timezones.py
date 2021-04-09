import time
import datetime
import pytz
from pytz import timezone
from tzlocal import get_localzone
#print(time.tzname)
def convertDateTime(inputDate):
    eastern = timezone("US/Eastern")
    local_tz = get_localzone()
    #print(dt)#datetime(2002, 10, 27, 6, 0, 0)
    #inputDate = datetime.datetime(2021, 10, 8, 6, 0, 0)#replace with the time we input
    convertDate = eastern.localize(inputDate.replace(tzinfo=None)).astimezone(local_tz) #will set it to the local system time
    print(inputDate)
    print(convertDate)
    return convertDate.replace(tzinfo=None)
