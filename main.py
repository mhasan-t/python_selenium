
import os
from sys import platform
from time import sleep
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import xlsxwriter


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


# options.add_argument("--headless")
options.add_argument("user-data-dir="+os.getcwd()+"/userdata")
options.add_argument("--window-size=1500,1000")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(driverpath, options=options,)
print("getting dropbox...")
driver.get("https://www.dropbox.com/sh/vhgppdzeq3gj7s8/AACpbksn7nXGEUrant_bBkMla/INDEX%20OF%20CORRESPONDENCE?dl=0")
sleep(5)
folders = driver.find_elements_by_class_name("sl-link--folder")
folder_links = []
for folder in folders:
	folder_link = folder.get_attribute("href")
	folder_name = folder.find_elements_by_class_name("sl-grid-filename")[0].text
	folder_links.append([folder_name, folder_link])


workbook = xlsxwriter.Workbook('index_of_correspondence.xlsx')
worksheet = workbook.add_worksheet()
row=1
col=0

while folder_links:
	name_link= folder_links[0]
	driver.get(name_link[1])
	sleep(3)

	files = driver.find_elements_by_class_name("sl-link--file")
	files = [file.get_attribute("href") for file in files]
	pdf_links = []
	output = []


	for file in files:
		if file.endswith(".pdf?dl=0"):
			pdf_name= unquote(file).rsplit('/', 1)[-1][:-5]
			datas = pdf_name.split("-")
			if len(datas)!=9:
				worksheet.write(row, col, "INVALID FORMAT")
				worksheet.write(row, col+1, file)
				row+=1
			else:
				worksheet.write(row, col, datas[0]+"-"+datas[1]+"-"+datas[2]+"-"+datas[3])
				worksheet.write(row, col+1, datas[4])
				worksheet.write(row, col+2, datas[5])
				worksheet.write(row, col+3, datas[6])
				worksheet.write(row, col+4, datas[7])
				worksheet.write(row, col+5, datas[8])
				worksheet.write(row, col+1, "ELECTRONICCOPY")
				worksheet.write(row, col+1, file)
				row += 1
	



	subfolders = driver.find_elements_by_class_name("sl-link--folder")
	if subfolders:
		del folder_links[0]
		for subfolder in subfolders:
			subfolder_link = subfolder.get_attribute("href")
			subfolder_name = subfolder.find_elements_by_class_name("sl-grid-filename")[0].text
			folder_links.insert(0, [subfolder_name, subfolder_link])
	else:
		del folder_links[0]

	print(row)


workbook.close()
driver.close()
