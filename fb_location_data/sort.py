import csv

data_list = []
with open("location_data_refined.csv") as output_csv, open("output.csv", mode='w', newline="") as final:
    csv_reader = csv.reader(output_csv)
    csv_writer = csv.writer(final, delimiter=",")
    csv_writer.writerow(next(csv_reader))
    csv_writer.writerows(reversed(list(csv_reader)))