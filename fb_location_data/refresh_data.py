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

with open("output_no_emptyline.csv") as ip, open("output_final.csv", mode='w', newline="") as op:
	csv_reader = csv.reader(ip)
	csv_writer = csv.writer(op, delimiter=",")
	line=1;
	for row in csv_reader:
		if row[2] ==  "Can not be found.":
			# print("in line "+str(line))
			lat=row[3]
			long=row[4]
			loc = lat+", "+long
			searchbox = driver.find_element_by_name("q")
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
				real_loc = "Invalid Co-ordinates."

			print(real_loc+" at line "+str(line))
			csv_writer.writerow([row[0], row[1], real_loc, row[3], row[4]])
		else:
			csv_writer.writerow(row)

		line+=1
driver.close()