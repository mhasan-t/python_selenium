import os
from sys import platform
from time import sleep

import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

options = Options()
driverpath = ""
chromebinarypath=""
if platform == "darwin":
    driverpath = os.getcwd()+"/chromedriver"
elif platform == "win32":
    driverpath = os.getcwd()+"\chromedriver.exe"
    chromebinarypath = os.getcwd()+"\Chrome\Application\chrome.exe" # path to chrome binary executable
    options.binary_location = chromebinarypath
else:
    print("COULD NOT DETECT OS TYPE, PLEASE SELECT YOUR OPERATING SYSTEM\n"
          "Enter 1 for Windows 10 and enter 2 for OSX -")
    os_type = input()
    if os_type==1:
        driverpath = os.getcwd()+"\chromedriver.exe"
        chromebinarypath = os.getcwd()+"\Chrome\Application\chrome.exe"
        options.binary_location = chromebinarypath
    elif os_type==2:
        driverpath = os.getcwd()+"/chromedriver"

print("please wait...")

# options.add_argument("--headless")
options.add_argument("user-data-dir="+os.getcwd()+"/userdata")
options.add_argument("--window-size=1500,1000")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(driverpath, options=options,)
driver.get("https://www.instagram.com/")
sleep(5)
loginBtn=-1

try:
    loginBtn = driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button")
except NoSuchElementException:
    pass


if loginBtn!=-1:
    print("logging in...")
    username = "locationid1234"   # ENTER YOUR USERNAME
    password = "locationid12345678"     # ENTER YOUR PASSWORD
    usernameBtn = driver.find_element_by_name("username")
    usernameBtn.send_keys(username)
    passwordBtn = driver.find_element_by_name("password")
    passwordBtn.send_keys(password)
    loginBtn.click()
    sleep(6)
    do_not_saveInfoBtn = driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div/div/button")
    print("Please wait a few more seconds...")
    do_not_saveInfoBtn.click()

print("logged in...")
sleep(5)
notNow = -1
try:
    notNow =driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
except:
    pass
if notNow!=-1:
    notNow.click()
sleep(1)

sleep(1)
searchBox = driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")

driver.minimize_window()
numOfLocations = input("Enter the number of locations (type 'exit' to exit) - ")
if numOfLocations == "exit":
    driver.quit()
    sys.exit()

driver.minimize_window()
print("Enter the locations - ")
locations = []
for _ in range(int(numOfLocations)):
    temp = input()
    locations.append(temp)

print("locating...")
for location in locations:
    searchBox.clear()
    searchBox.send_keys(location)
    driver.minimize_window()
    sleep(1)
    box = driver.find_element_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/div[4]/div")
    all_results = box.find_elements_by_tag_name("a")
    location_id_link = -1
    for res in all_results:
        link = res.get_attribute("href")
        if link.startswith("https://www.instagram.com/explore/locations/"):
            location_id_link = link
            break

    if location_id_link==-1:
        print("--->Sorry, that location could not be found.\n\n")
        continue
    else:
        location_id_list = location_id_link.split("/")
        locationID = location_id_list[5]
        print("--->Location ID for "+location+" is : "+locationID)

driver.quit()
