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

# Time to wait for selectors.(second)
WAIT = 4

# Max Retry to get phone number from sms-activate.org
REQUEST_MAX_TRY = 10

# These are sample user data you will put in user.csv
first_name = "All" # First Name
last_name = "Soft1210" # Last Name
birthday = "12/30/1990" # Birthday

# Your SMS-Activate API key
api_key = "9b6b9eb50d0A3020c2710A17d9b7495b"
country_code = "175" #i.e, Austrailian country code, See country table in sms-activate. I often use Australian phone number and it works almost always.

sms_activate_url = "https://sms-activate.org/stubs/handler_api.php"
phone_request_params = {
    "api_key":api_key,
    "action":"getNumber",
    "country":country_code, 
    "service":"go",
}

status_param = {
    "api_key":api_key,
    "action":"getStatus"
}

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
    "code":'//input[@name="code"]',
    "acc_phone_number":'//input[@id="phoneNumberId"]',
    "acc_day":'//input[@name="day"]',
    "acc_month":'//select[@id="month"]',
    "acc_year":'//input[@name="year"]',
    "acc_gender":'//select[@id="gender"]'
}

# You can modify this method with your own proxy.
def getProxy():
    proxy_list = [
        "http://kIOLw:B52RK@60.242.64.183:2002",
        "http://kIOLw:B52RK@60.242.64.183:2003",
        "http://kIOLw:B52RK@60.242.64.183:2004",
        ]

    proxy = random.choice(proxy_list)

    if "2002" in proxy:
        url = "http://60.242.64.183/api/change_ip?index=2&rtoken=R2NbWa4IZxhnhJBUnk2FVUPbArIvJZ1QSbYNe8p1gJrmPhCbu4"
    if "2003" in proxy:
        url = "http://60.242.64.183/api/change_ip?index=3&rtoken=R2NbWa4IZxhnhJBUnk2FVUPbArIvJZ1QSbYNe8p1gJrmPhCbu4"
    if "2004" in proxy:
        url = "http://60.242.64.183/api/change_ip?index=4&rtoken=R2NbWa4IZxhnhJBUnk2FVUPbArIvJZ1QSbYNe8p1gJrmPhCbu4"

    return proxy

def getRandomeUserAgent():
    UAGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 YaBrowser/21.8.1.468 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Mozilla/5.0 (X11; CrOS x86_64 14440.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4807.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14467.0.2022) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4838.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.7.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.13 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14455.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4827.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.17 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14436.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4803.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14475.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14471.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.37.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14409.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4829.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14395.0.2021) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4765.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.14 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14484.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14450.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4817.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14473.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14324.72.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.91 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14454.0.2022) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4824.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14453.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4816.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14447.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4815.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14477.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14476.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4840.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.8.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.9 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.25.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.22 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.57.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.64 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.93 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.59.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.91.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.55 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.23.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.20 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.36.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.36 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.26 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14685.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4992.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14682.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.16 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.9.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.5 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14574.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4937.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14716.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14268.81.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.48 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.61.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.37.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.37 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.51.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.32 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.56 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.43.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.54 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14505.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4870.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.16.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.25 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.28.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.44 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14543.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4918.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.31.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.19 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.13 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14658.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4975.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.25.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36'
    ]
    agent = random.choice(UAGENTS)
    return agent

# This method is for chrome driver initialization. You can customize if you want.
def setDriver():
    
    # proxy = getProxy() # rotating proxy
    proxy = "socks5://login:password@176.103.246.143:12324" # fixed proxy
    user_agent = getRandomeUserAgent() # random user agent
    # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36" #fixed agent
    options = {
        # 'proxy': {
        #     'http': proxy,
        #     'https': proxy,
        #     'no_proxy': 'localhost,127.0.0.1' # excludes
        # },
        # 'ca_cert': './ca.crt',
        'exclude_hosts': ['google-analytics.com'],
        # 'verify_ssl': True
    }
    profile_path = ""
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
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
    # chrome_options.add_argument(r"--user-data-dir=C:\\Users\\nICE\\AppData\\Local\\Google\\Chrome\\User Data") #e.g. C:\Users\nICE\AppData\Local\Google\Chrome\User Data
    # chrome_options.add_argument(r'--profile-directory=Profile 11')
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options, seleniumwire_options=options)

    return driver

def main():

    with open("user.csv", 'r') as file:
      csvreader = csv.reader(file)
      for row in csvreader:
        try:
            print(row)
            if "Firstname" == row[0]:
                continue
            first_name = row[0]
            last_name = row[1]
            mypw = row[2]
            birthday = row[3]

            try:
                user_name_manual = row[4]
            except:
                user_name_manual = ""

            print('Start...')
            # get driver.
            
            driver = setDriver()

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

            
            username_try = 0

            # if the username exists, it retries REQUEST_MAX_TRY times.
            while username_try < REQUEST_MAX_TRY:
                time.sleep(WAIT*2)
                print("Username Retrial: ", username_try)
                # set the first name.
                print('################# Set First Name ####################')
                first_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['first_name'])))
                first_name_tag.clear()
                first_name_tag.send_keys(first_name)

                # set the surname.
                print('################# Set Last Name ####################')
                last_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['last_name'])))
                last_name_tag.clear()
                last_name_tag.send_keys(last_name)
                # set username
                print('################# Set User Name ####################')
                if user_name_manual == "":
                    rand_5_digit_num = random.randint(10000,99999)
                    user_name = first_name +"."+ last_name
                    user_name = user_name.lower() + str(rand_5_digit_num)
                else:
                    user_name = user_name_manual
                user_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['username'])))
                user_name_tag.clear()
                user_name_tag.send_keys(user_name)

                # set password
                print('################# Set Password ####################')
                passwd_tag =WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['password'])))
                passwd_tag.clear()
                passwd_tag.send_keys(mypw)

                print('################# Set Confirm Password ####################')
                confirmwd_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['confirm_password'])))
                confirmwd_tag.clear()
                confirmwd_tag.send_keys(mypw)

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

                print('################## Check if it needs phone verification on current ip address.')
                without_verification = False
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_day'])))
                    without_verification = True
                    print("No. It doesn't require.")
                    break
                except:
                    print("Yes. It requires")
                    pass
                print('################# Phone Number ####################')
                try:
                    phone_number_input = WebDriverWait(driver, WAIT*3).until(EC.presence_of_element_located((By.XPATH, selectors['phone_number'])))
                    time.sleep(WAIT)
                    break
                except:
                    username_try = username_try + 1
                    pass
            number = ""
            activationId = ""
            count = 0
            if without_verification == False:
                print('################ Get Virtual Phone Number from SMS_Activate ##############')
                while(count < REQUEST_MAX_TRY):
                    res = requests.get(url=sms_activate_url,params = phone_request_params)
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
                    raise Exception("Go to next account.")
                
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
                    res_code = requests.get(url=sms_activate_url,params = status_param)
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
                    raise Exception("Go to next account.")

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

            time.sleep(WAIT*2)
            print('################# Account Phone Number ####################')
            WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_phone_number']))).clear()

            print('################# Account Birthday ####################')   
            WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_day']))).send_keys(birthday.split('/')[1])
            
            select_acc_month = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selectors['acc_month'])))

            acc_month = Select(select_acc_month)
            acc_month.select_by_value(birthday.split('/')[0])

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
            time.sleep(WAIT*4)
            f = open('created_accounts.txt', 'a')
            f.write(user_name + "    " + mypw + "\n")
            f.close()
            driver.quit()
        except:
            driver.quit()

main()