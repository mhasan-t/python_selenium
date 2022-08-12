import csv
from datetime import datetime

import pytz

with open("location_data_refined.csv", mode='r') as csv_file_read, open("output.csv", mode="w", newline="") as csv_write:
    csv_reader = csv.reader(csv_file_read)
    csv_writer = csv.writer(csv_write, delimiter=",")
    for row in csv_reader:
        if row[0] == "Date":
            csv_writer.writerow(row)
            continue
        datetime_str = row[0] + " " + row[1]
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        tz = pytz.timezone("Australia/Melbourne")
        datetime_aus = datetime_obj.astimezone(tz)

        datetime_str_aus = datetime_aus.strftime("%Y-%m-%d %H:%M:%S")
        date = datetime_str_aus.split(" ")[0]
        time = datetime_str_aus.split(" ")[1]

        data = [date, time, row[2]]
        csv_writer.writerow(data)



