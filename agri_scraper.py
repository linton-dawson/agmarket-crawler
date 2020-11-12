import time
import os
import glob
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import geckodriver_autoinstaller

geckodriver_autoinstaller.install()

url = "https://agmarknet.gov.in/PriceTrends/SA_WeeK_PriD.aspx"
download_path = os.getcwd();
print(download_path)
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir',download_path)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'xls')
print('Setting Profile Preferences...')
driver = webdriver.Firefox(profile,firefox_binary="/usr/bin/firefox")
driver.get(url)

crop_list = ['Wheat', 'Cotton', 'Orange']
year = ['2018','2019']
month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
week = ['First', 'Second', 'Third', 'Fourth']

def setDir(crop) :
    filepath = download_path + '/*.xls'
    list_of_files = glob.glob(filepath, recursive = True)
    curr_file = max(list_of_files,key = os.path.getctime)
    if os.path.isdir(download_path + '/' + crop) == False :
        os.mkdir(download_path + '/' + crop)
    filename = curr_file[curr_file.rfind('/') : ]
    if os.path.isfile( download_path + '/' + crop + '/' + filename) :
        print('File already present ! Skipping...')
        return
    os.rename(curr_file,download_path + '/' + crop + '/' + filename)

for yidx in year :
    for midx in month :
        for widx in week :
            for crop in crop_list :
                wait = WebDriverWait(driver,120)
                time.sleep(2)

                selectCommodity = Select(driver.find_element_by_xpath('//*[@id="cphBody_Commod_List"]'))
                selectCommodity.select_by_visible_text(crop)
                try :
                    wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="cphBody_State_list"]')))
                except :
                    time.sleep(2)

                selectState = Select(driver.find_element_by_xpath('//*[@id="cphBody_State_list"]'))
                selectState.select_by_visible_text("Maharashtra")
                try :
                    wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="cphBody_Year2_List"]')))
                except :
                    time.sleep(2)

                selectYear = Select(driver.find_element_by_xpath('//*[@id="cphBody_Year2_List"]'))
                selectYear.select_by_visible_text(yidx)
                try :
                    wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="cphBody_Month2_List"]')))
                except :
                    time.sleep(2)

                selectMonth = Select(driver.find_element_by_xpath('//*[@id="cphBody_Month2_List"]'))
                selectMonth.select_by_visible_text(midx)
                try :
                    wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="cphBody_Week1_List"]')))
                except :
                    time.sleep(2)

                selectWeek = Select(driver.find_element_by_xpath('//*[@id="cphBody_Week1_List"]'))
                selectWeek.select_by_visible_text(widx)
                try :
                    wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="cphBody_Button_Sub"]')))
                except :
                    time.sleep(2)


                driver.find_element_by_xpath('//*[@id="cphBody_Button_Sub"]').click()
                try:
                    wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="cphBody_Button1"]')))
                except :
                    time.sleep(2)

                driver.find_element_by_xpath('//*[@id="cphBody_Button1"]').click()
                time.sleep(5)
                setDir(crop)
                print(crop,'data acquired for', widx,'week of', midx, yidx)
                driver.find_element_by_xpath('//*[@id="cphBody_btnBack"]').click()
