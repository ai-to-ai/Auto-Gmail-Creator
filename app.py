import numpy
# from selenium import webdriver
from seleniumwire import webdriver
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import datetime
import requests
import csv

WAIT = 4
REQUEST_MAX_TRY = 10
combined_first_names = "All"
last_name = "Soft1210"
birthday = "10/12/1995"

def getProxy():
    proxy_list = [
        "http://kIOLw:B52RK@60.242.64.183:2002",
        "http://kIOLw:B52RK@60.242.64.183:2003",
        "http://kIOLw:B52RK@60.242.64.183:2004",
        ]

    # proxy_list = [
    #     "http://60.242.64.183:2002:B52RK:kIOLw",
    #     "http://60.242.64.183:2003:B52RK:kIOLw",
    #     "http://60.242.64.183:2004:B52RK:kIOLw"
    #     ]
    proxy = random.choice(proxy_list)

    if "2002" in proxy:
        url = "http://60.242.64.183/api/change_ip?index=2&rtoken=R2NbWa4IZxhnhJBUnk2FVUPbArIvJZ1QSbYNe8p1gJrmPhCbu4"
    if "2003" in proxy:
        url = "http://60.242.64.183/api/change_ip?index=3&rtoken=R2NbWa4IZxhnhJBUnk2FVUPbArIvJZ1QSbYNe8p1gJrmPhCbu4"
    if "2004" in proxy:
        url = "http://60.242.64.183/api/change_ip?index=4&rtoken=R2NbWa4IZxhnhJBUnk2FVUPbArIvJZ1QSbYNe8p1gJrmPhCbu4"

    # res = requests.get(url=url)
    print(proxy)
    return proxy
def setDriver():

    profile = {"plugins.plugins_list": [{"enabled": False,
                                         "name": "Chrome PDF Viewer"}],
               "download.extensions_to_open": "",
               "download.prompt_for_download": False,
               "plugins.always_open_pdf_externally": True}
    proxy = getProxy()

    options = {
        'proxy': {
            'http': proxy,
            'https': proxy,
            'no_proxy': 'localhost,127.0.0.1' # excludes
        },
        'ca_cert': './ca.crt',
        'exclude_hosts': ['google-analytics.com'],
        'verify_ssl': True
    }
    profile_path = ""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("disable-popup-blocking")
    chrome_options.add_argument("disable-notifications")
    chrome_options.add_argument("disable-popup-blocking")
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option('prefs', profile)
    # chrome_options.add_argument(r"--user-data-dir=C:\\Users\\nICE\\AppData\\Local\\Google\\Chrome\\User Data") #e.g. C:\Users\nICE\AppData\Local\Google\Chrome\User Data
    chrome_options.add_argument(r'--profile-directory=Profile 11')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options, seleniumwire_options=options)

    return driver


# print(magnet_links)

selectors = {
    "create_account":[
        "//span[contains(text(),'Create account')]",
        "//span[@class='VfPpkd-vQzf8d']"
        ], #VfPpkd-vQzf8d
    'for_my_personal_use':[
        "//span[contains(text(),'For my personal use')]",
        "//span[@class='VfPpkd-StrnGf-rymPhb-b9t22c']"
        ], #VfPpkd-StrnGf-rymPhb-b9t22c
    "first_name":"//*[@name='firstName']",#whsOnd zHQkBf
    "last_name":"//*[@name='lastName']",#whsOnd zHQkBf
    "username":"//*[@name='Username']", #whsOnd zHQkBf
    "password":"//*[@name='Passwd']", #whsOnd zHQkBf
    "confirm_password":"//*[@name='ConfirmPasswd']",#whsOnd zHQkBf
    "next":[
            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
            "//button[contains(text(),'Next')]",
            "//button[contains(text(),'I agree')]"
    ],#VfPpkd-vQzf8d,
    "phone_number":"//*[@id='phoneNumberId']",
    "phone_number_next":'//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]',
    "code":'//input[@name="code"]',
    "verify_next":'//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b"]',
    "acc_phone_number":'//input[@id="phoneNumberId"]',
    "acc_day":'//input[@name="day"]',
    "acc_month":'//select[@id="month"]',
    "acc_year":'//input[@name="year"]',
    "acc_gender":'//select[@id="gender"]'
}

sms_activate_url = "https://sms-activate.org/stubs/handler_api.php"
api_key = "" # Your API key

phone_request_params = {
    "api_key":api_key,
    "action":"getNumber",
    "country":"175", # Country code, see country table in sms-activate.
    "service":"go",
}

status_param = {
    "api_key":api_key,
    "action":"getStatus"
}

def main():

    with open("user.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        print(row)

        combined_first_names = row[0]
        last_name = row[1]
        mypw = row[2]
        birthday = row[3]

        print('Start...')
        # get driver.
        
        driver = setDriver()
        # driver.delete_all_cookies();

        driver.get("https://accounts.google.com")


        print('################# Go to account page ############################')
        for selector in selectors["create_account"]:
            try:
                print(selector)
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                break
            except:
                pass
        print('################# Click "For my personal use" ###################')
        for selector in selectors["for_my_personal_use"]:
            try:
                print(selector)
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                break
            except:
                pass
        # set the first name.
        print('################# Set First Name ####################')
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['first_name']))).send_keys(combined_first_names)

        # set the surname.
        print('################# Set Last Name ####################')
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['last_name']))).send_keys(last_name)

        # set username
        print('################# Set User Name ####################')
        rand_4_digit_num = random.randint(1000,9999)
        user_concat = combined_first_names +"."+ last_name
        user_concat = user_concat.lower()
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['username']))).send_keys(user_concat)

        # set password
        print('################# Set Password ####################')
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        pw_length = 8


        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['password']))).send_keys(mypw)

        print('################# Set Confirm Password ####################')
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['confirm_password']))).send_keys(mypw)

        #click next button
        print('################# Click "Next" Buton ####################')
        for selector in selectors['next']:
            try:
                print(selector)
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                break
            except:
                pass
        time.sleep(WAIT*2)
        print('################# Phone Number ####################')
        phone_number_input = WebDriverWait(driver, WAIT*3).until(EC.presence_of_element_located((By.XPATH, selectors['phone_number'])))
        # time.sleep(WAIT*3)
        number = ""
        activationId = ""
        count = 0

        print('################ Get Virtual Phone Number from SMS_Activate ##############')
        while(count < REQUEST_MAX_TRY):
            # proxy = getProxy()
            res = requests.get(url=sms_activate_url,params = phone_request_params)
            # res = requests.get(url=sms_activate_url,params = phone_request_params, proxies = {'http':proxy, 'https':proxy})
            data = res.text
            print(data)
            if "ACCESS_NUMBER" in data:
                activationId = data.split(':')[1]
                number = data.split(':')[2]
                number = '+'+ number
                print(number)
                break
            count = count+1
            time.sleep(WAIT)
        if number == '':
            print("Cannot get virtual phone number: ", REQUEST_MAX_TRY, " times retry.")
            quit()
        
        phone_number_input.send_keys(number)

        #click next button
        print('################# Click "Next" Buton ####################')
        for selector in selectors['next']:
            try:
                print(selector)
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                break
            except:
                pass

        print('############################# Get SMS Code from SMS_Activate ###########################')
        time.sleep(WAIT)

        count_status = 0
        code = ''
        while(True):
        # while(count_status < REQUEST_MAX_TRY):
            status_param['id'] = activationId
            print(status_param)
            # proxy = getProxy()
            res_code = requests.get(url=sms_activate_url,params = status_param)
            # res_code = requests.get(url=sms_activate_url,params = status_param, proxies = {'http':proxy, 'https':proxy})
            data_code = res_code.text
            print(data_code)
            if "STATUS_OK" in data_code:
                code = data_code.split(':')[1]
                print(code)
                break

            count_status = count_status + 1
            time.sleep(WAIT*5)

        if code == '':
            print('Cannot receive code from sms_activate: ',REQUEST_MAX_TRY, " times retrial")
            quit()

        print('################# Verify Code ####################')  
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['code']))).send_keys(code)

        #click next button
        print('################# Click "Verify" Buton ####################')
        for selector in selectors['next']:
            try:
                print(selector)
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                break
            except:
                pass
        time.sleep(WAIT*5)
        print('################# Account Phone Number ####################')
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_phone_number']))).clear()

        print('################# Account Birthday ####################')   
        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_day']))).send_keys(birthday.split('/')[0])
        
        select_acc_month = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_month'])))

        acc_month = Select(select_acc_month)
        acc_month.select_by_value(birthday.split('/')[1])

        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_year']))).send_keys(birthday.split('/')[2])


        select_acc_gender = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_gender'])))

        acc_gender = Select(select_acc_gender)
        acc_gender.select_by_value('1')

        print('################# Click "Next" Buton ####################')
        for selector in selectors['next']:
            try:
                print(selector)
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                break
            except:
                pass
        print('################# Click "I agree" Buton ####################')
        time.sleep(WAIT)
        driver.execute_script("window.scrollTo(0, 800)") 
        time.sleep(WAIT)
        for selector in selectors['next']:
            try:
                print(selector)
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                break
            except:
                pass
        time.sleep(WAIT*10)
        f = open('user_details.txt', 'a')
        f.write(user_concat + "    " + mypw + "\n")
        f.close()
        driver.quit()

main()