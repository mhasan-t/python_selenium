import csv
import json
import os
from csv import DictWriter
from datetime import datetime
from sys import platform
from time import sleep

import pytz
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

options = Options()
driverpath = ""
if platform == "darwin":
    driverpath = os.getcwd()+"/chromedriver"
elif platform == "win32":
    driverpath = os.getcwd()+"\chromedriver.exe"
else:
    print("COULD NOT DETECT OS TYPE, PLEASE SELECT YOUR OPERATING SYSTEM\n"
          "Enter 1 for Windows 10 and enter 2 for OSX -")
    os_type = input()
    if os_type==1:
        driverpath = os.getcwd()+"\chromedriver.exe"
    elif os_type==2:
        driverpath = os.getcwd()+"/chromedriver"


options.add_argument("--headless")
options.add_argument("user-data-dir="+os.getcwd()+"/userdata")
options.add_argument("--window-size=1500,1000")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(driverpath, options=options,)
print("getting maps...")
driver.get("https://maps.google.com/")
sleep(5)

print("setting language...")
lang_btn = driver.find_element_by_xpath("//*[@id='omnibox-singlebox']/div[1]/div[1]/button")
lang_btn.click()
sleep(1)
lang = driver.find_element_by_xpath("//*[@id='settings']/div/div[2]/ul/ul[2]/li[2]/button")
lang.click()
sleep(1)
eng = driver.find_element_by_xpath("//*[@id='languages']/div/div[2]/div[2]/ul[1]/li[11]/a")
eng.click()
sleep(5)

print("starting to fetch data...")
final_data = []
with open("location_history.json") as json_file, open("location_data_refined.csv", mode='a', newline="") as output_csv:
    data = json.load(json_file)
    csv_writer = csv.writer(output_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    counter = 0
    saved = 0
    for location in data["location_history"]:
        lat = str(location["coordinate"]["latitude"])
        long = str(location["coordinate"]["longitude"])
        searchbox = driver.find_element_by_name("q")
        loc = lat + ", " + long
        searchbox.clear()
        searchbox.send_keys(loc)
        searchbox.send_keys(Keys.ENTER)
        sleep(2)
        try:
            real_loc = (driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[8]/div/div[1]/span[3]/span[3]")).text
        except:
                sleep(5)
        try:
            real_loc = (driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[8]/div/div[1]/span[3]/span[3]")).text
        except:
            real_loc = "Can not be found."
            with open("error_logs.txt", mode='a', newline="\n") as err_log:
                err_log.write(str(saved)+"th entry - "+ str((saved*8)+2) + "th line in json file.\n" )


        datetime = datetime.fromtimestamp(location["creation_timestamp"])
        tz = pytz.timezone("Australia/Melbourne")
        datetime_aus = datetime.astimezone(tz)
        datetime_str = datetime_aus.strftime("%d-%m-%Y %H:%M:%S")
        date = datetime_str.split(" ")[0]
        time = datetime_str.split(" ")[1]
        loc_data = [date, time, real_loc, lat, long]
        print(loc_data)
        csv_writer.writerow(loc_data)
        if counter == 100:
            output_csv.flush()
            counter = 0
            print("-----------saved "+str(saved)+" rows")
        counter += 1
        saved += 1

driver.close()

print("sorting the data according to date....")
# data_list = []
# with open("location_data_refined.csv") as output_csv, open("output.csv", mode='w', newline="") as final:
#     csv_reader = csv.reader(output_csv)
#     csv_writer = csv.writer(final, delimiter=",")
#     csv_writer.writerow(next(csv_reader))
#     csv_writer.writerows(reversed(list(csv_reader)))

print("\n\n\n-----FINISHED-----")