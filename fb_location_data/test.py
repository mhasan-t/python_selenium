import pytz
from datetime import datetime

datetime = datetime.fromtimestamp(int(input()))
tz = pytz.timezone("Australia/Melbourne")
datetime_aus = datetime.astimezone(tz)
datetime_str = datetime_aus.strftime("%d-%m-%Y %H:%M:%S")
print(datetime_str)