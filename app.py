# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import random
import datetime
import requests
import csv
import string
from fp.fp import FreeProxy
from fake_useragent import UserAgent

# Option for Auto User info generation
AUTO_GENERATE_UERINFO = False
AUTO_GENERATE_NUMBER = 10

# Include Refer URL
INCLUDE_REFER_URL = False

# Time to wait for SELECTORS.(second)
WAIT = 4

# Max Retry to get phone number from sms-activate.org
REQUEST_MAX_TRY = 10

# Your SMS-Activate API key
API_KEY = "" #9b6b9eb50d0A30---------d9b7495b
COUNTRY_CODE = "175" #i.e, Austrailian country code, See country table in sms-activate. I often use Australian phone number and it works almost always.

sms_activate_url = "https://sms-activate.org/stubs/handler_api.php"
phone_request_params = {
    "api_key":API_KEY,
    "action":"getNumber",
    "country":COUNTRY_CODE, 
    "service":"go",
}

status_param = {
    "api_key":API_KEY,
    "action":"getStatus"
}

SELECTORS = {
    "create_account":[
        "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d LQeN7 FliLIb uRo0Xe TrZEUc Xf9GD']",
        "//*[@class='JnOM6e TrZEUc kTeh9 KXbQ4b']"
        ],
    'for_my_personal_use':[
        "//span[@class='VfPpkd-StrnGf-rymPhb-b9t22c']",
        ], 
    "first_name":"//*[@name='firstName']",
    "last_name":"//*[@name='lastName']",
    "username":"//*[@name='Username']",
    "password":"//*[@name='Passwd']",
    "confirm_password":"//*[@name='ConfirmPasswd']",
    "next":[
            "//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b']",
            "//button[contains(text(),'Next')]",
            "//button[contains(text(),'I agree')]"
    ],
    "phone_number":"//*[@id='phoneNumberId']",
    "code":'//input[@name="code"]',
    "acc_phone_number":'//input[@id="phoneNumberId"]',
    "acc_day":'//input[@name="day"]',
    "acc_month":'//select[@id="month"]',
    "acc_year":'//input[@name="year"]',
    "acc_gender":'//select[@id="gender"]',
    "username_warning":'//*[@class="jibhHc"]',
}
# https://webflow.com/made-in-webflow/fast , I tried to find the fast websites and you can add more.
SITE_LIST = [
    'https://google.com',
    'https://wizardrytechnique.webflow.io/',
    'https://www.rachelbavaresco.com/',
    'https://lightning-bolt.webflow.io/'
]
proxy_list = None
with open("./data/Proxy_DB.csv", 'r') as proxy_list_file:
    proxy_list = csv.reader(proxy_list_file)
    proxy_list = list(proxy_list)

def generatePassword():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for x in range(size))

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
    seleniumwire_options = {}
    seleniumwire_options['exclude_hosts'] = ['google-analytics.com']

    # Secure Connection
    # seleniumwire_options['verify_ssl'] = True

    # Set Proxy
    # proxy = getProxy() # Rotating proxy
    SOCKS_PROXY = "socks5://14ab1e7131541:39d813de77@176.103.246.143:12324" # Fixed proxy, i.e socks5://14ab1e7131541:39d813de77@176.103.246.143:12324
    # SOCKS_PROXY = "socks5://user:pass@ip:port" # Fixed proxy, i.e socks5://14ab1e7131541:39d813de77@176.103.246.143:12324
    # SOCKS_PROXY = 'socks5://158.69.225.110:59166'

    # https://pypi.org/project/free-proxy/
    try:
        random_proxy = FreeProxy(timeout=1).get()
        print('################ Use FreeProxy library to get HTTP proxy ################')
    except:
        print('################ Use Proxy DB to get HTTP proxy ################')
        random_proxy = "http://"+ random.choice(proxy_list)[0]

    HTTP_PROXY = random_proxy
    print(HTTP_PROXY)
    # HTTPS_PROXY = "https://user:pass@ip:port"

    # Proxy
    proxy_options = {}
    proxy_options['no_proxy']= 'localhost,127.0.0.1'

    ## Http proxy
    proxy_options['http'] = HTTP_PROXY

    ## Https proxy
    # proxy_options['https'] = HTTPS_PROXY

    ## Socks proxy
    # proxy_options['http'] = SOCKS_PROXY
    # proxy_options['https'] = SOCKS_PROXY

    seleniumwire_options['proxy'] = proxy_options
    # prox = Proxy()
    # prox.proxy_type = ProxyType.MANUAL
    # prox.socks_proxy = SOCKS_PROXY
    # prox.socks_version = 5
    # prox.http_proxy = HTTP_PROXY
    # print(SOCKS_PROXY)
    # prox.http_proxy = SOCKS_PROXY
    # prox.https_proxy = SOCKS_PROXY

    # capabilities = webdriver.DesiredCapabilities.CHROME
    # prox.add_to_capabilities(capabilities)

    # Set User Agent
    # user_agent = getRandomeUserAgent() # Random user agent
    # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36" # Fixed agent
    # Please refer to this https://github.com/fake-useragent/fake-useragent
    user_agent = UserAgent(fallback="Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36").random
    print(user_agent)
    # Set Browser Option
    options = ChromeOptions()
    # options = FirefoxOptions()

    prefs = {"profile.password_manager_enabled": False, "credentials_enable_service": False, "useAutomationExtension": False}
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("disable-popup-blocking")
    options.add_argument("disable-notifications")
    options.add_argument("disable-popup-blocking")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    # options.add_argument('--headless') # UI
    # options.add_argument("--incognito")
    # options.add_argument(r"--user-data-dir=C:\\Users\\Username\\AppData\\Local\\Google\\Chrome\\User Data")
    # options.add_argument(r'--profile-directory=ProfileName')
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options, seleniumwire_options=seleniumwire_options)
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = options, seleniumwire_options=seleniumwire_options)
    
    return driver

def main():
    user_number = 0
    i = 0

    if(AUTO_GENERATE_UERINFO):
        user_number = AUTO_GENERATE_NUMBER
        print('################ Open First_Name_DB.csv ################')
        try:
            first_name_file = open("./data/First_Name_DB.csv", 'r')
            first_names = csv.reader(first_name_file)
            first_names = list(first_names)
        except:
            print('################ Please check if First_Name_DB.csv exists ################')
            quit()

        print('################ Open Last_Name_DB.csv ################')
        try:
            last_name_file = open("./data/Last_Name_DB.csv", 'r')
            last_names = csv.reader(last_name_file)
            last_names = list(last_names)
        except:
            print('################ Please check if Last_Name_DB.csv exists ################')
            quit()
    else:
        print('################ Open User.csv ################')
        try:
            user_info_file = open("User.csv", 'r')
            user_infos = csv.reader(user_info_file)
            user_infos = list(user_infos)
            user_number = len(user_infos)
        except:
            print('################ Please check if User.csv exists ################')
            quit()

    while True:
        try:
            # Check if the count reach to the maxium users.
            
            if i == user_number:
                break

            i = i + 1
            print('################ User:', i,' ################')
            if AUTO_GENERATE_UERINFO:
                first_name = random.choice(first_names)[0]
                last_name = random.choice(last_names)[0]
                password = generatePassword()
                birthday = str(random.randint(1,12)) + "/" + str(random.randint(1,28)) + "/" +  str(random.randint(1980,1999))
                user_name_manual = ""
                print(first_name + "\t" + last_name + "\t" + password + '\t' + birthday)
            else:
                row = user_infos[i]
                if "Firstname" == row[0]:
                    continue

                first_name = row[0]
                last_name = row[1]
                password = row[2]
                birthday = row[3]
                print(first_name + "\t" + last_name + "\t" + password + '\t' + birthday)
            try:
                user_name_manual = row[4]
            except:
                user_name_manual = ""

            print('################ Initialize Chrome Driver ################')
            driver = setDriver()

            print('################ Random Refer website to bypass Google Bot Detection ################')
            if INCLUDE_REFER_URL:
                random_url = random.choice(SITE_LIST)
                driver.get(random_url)

            # 4 ways to go to account creation page.
            random_int = random.randint(1,4)
            if random_int ==  1:

                print('################ Creat a google account article ################')
                driver.get('https://support.google.com/accounts/answer/27441?hl=en')
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH,'//*[@id="hcfe-content"]/section/div/div[1]/article/section/div/div[1]/div/div[2]/a[1]'))).click()
                time.sleep(WAIT)
            elif random_int == 2:
                print('################ Go to account page ################')
                driver.get("https://accounts.google.com")

                time.sleep(WAIT)
                
                print('################ Click "Create account" ################')
                for selector in SELECTORS["create_account"]:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass
                print('################ Click "For my personal use" ################')
                for selector in SELECTORS["for_my_personal_use"]:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass

            elif random_int == 3:
                driver.get('https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp')
                time.sleep(WAIT)
            
            elif random_int == 4:
                driver.get('https://support.google.com/mail/answer/56256?hl=en')
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH,'//*[@id="hcfe-content"]/section/div/div[1]/article/section/div/div[1]/div/p[1]/a'))).click()
                time.sleep(WAIT)

            username_try = 0

            # if the username exists, it retries REQUEST_MAX_TRY times.
            while username_try < REQUEST_MAX_TRY:
                time.sleep(WAIT*2)
                print("################ Generate User Try: ", username_try+1, " ################")
                # set the first name.
                print('################ Set First Name ################')
                first_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['first_name'])))
                first_name_tag.clear()
                time.sleep(WAIT/2)
                first_name_tag.send_keys(first_name)

                # set the surname.
                print('################ Set Last Name ################')
                last_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['last_name'])))
                last_name_tag.clear()
                last_name_tag.send_keys(last_name)
                # set username
                print('################ Set User Name ################')
                if user_name_manual == "":
                    rand_5_digit_num = random.randint(10000,99999)
                    user_name = first_name +"."+ last_name
                    user_name = user_name.lower() + str(rand_5_digit_num)
                else:
                    user_name = user_name_manual
                user_name_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['username'])))
                user_name_tag.clear()
                time.sleep(WAIT/2)
                user_name_tag.send_keys(user_name)

                # set password
                print('################ Set Password ################')
                passwd_tag =WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['password'])))
                passwd_tag.clear()
                passwd_tag.send_keys(password)

                print('################ Set Confirm Password ################')
                confirmwd_tag = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['confirm_password'])))
                confirmwd_tag.clear()
                confirmwd_tag.send_keys(password)

                #click next button
                print('################ Click "Next" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass
                time.sleep(WAIT*2)
                print('################ Check Username Validation ################')
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['username_warning'])))
                    user_name_manual = ""
                    print("Invalid")
                    username_try = username_try + 1
                    continue
                except:
                    print("Valid")
                    pass
                print('################ Check Phone Verification ################')
                without_verification = False
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_day'])))
                    without_verification = True
                    print("No. It doesn't require.")
                    break
                except:
                    print("Yes. It requires")
                    pass
                print('################ Input Phone Number ################')
                try:
                    phone_number_input = WebDriverWait(driver, WAIT*3).until(EC.presence_of_element_located((By.XPATH, SELECTORS['phone_number'])))
                    time.sleep(WAIT)
                    break
                except:
                    username_try = username_try + 1
            number = ""
            activationId = ""
            count = 0
            if without_verification == False:
                print('################ Get Phone Number from SMS_Activate ################')
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
                    if "NO_BALANCE" in data:
                        print("Check your Balance in sms-activate.")
                        exit()
                    count = count+1
                    time.sleep(WAIT)
                if number == '':
                    print("################ Cannot get phone number: ", REQUEST_MAX_TRY, " times retrial. ################")
                    raise Exception("Go to next account.")
                
                phone_number_input.send_keys(number)

                #click next button
                print('################ Click "Next" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass

                print('################ Get SMS Code from SMS_Activate ################')
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
                        break

                    count_status = count_status + 1
                    time.sleep(WAIT*5)

                if code == '':
                    print('Cannot receive code from sms_activate: ',REQUEST_MAX_TRY, " times retrial")
                    raise Exception("Go to next account.")

                print('################ Verify Phone Code ################')  
                WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['code']))).send_keys(code)

                #click next button
                print('################ Click "Verify" Buton ################')
                for selector in SELECTORS['next']:
                    try:
                        WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                        break
                    except:
                        pass

            time.sleep(WAIT*2)
            print('################ Clear Account Phone Number ################')
            # WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_phone_number']))).clear()

            print('################ Account Birthday ################')
            # Date   
            WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_day']))).send_keys(birthday.split('/')[1])
            
            # Month
            select_acc_month = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_month'])))

            acc_month = Select(select_acc_month)
            acc_month.select_by_value(birthday.split('/')[0])

            # Year
            WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_year']))).send_keys(birthday.split('/')[2])

            select_acc_gender = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, SELECTORS['acc_gender'])))

            # Gender
            acc_gender = Select(select_acc_gender)
            acc_gender.select_by_value('1')

            print('################ Click "Next" Buton ################')
            for selector in SELECTORS['next']:
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                    break
                except:
                    pass
            print('################ Click "I agree" Buton ################')
            time.sleep(WAIT)

            # Scroll to click "I agree"
            driver.execute_script("window.scrollTo(0, 800)") 
            time.sleep(WAIT)
            for selector in SELECTORS['next']:
                try:
                    WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.XPATH, selector))).click()
                    break
                except:
                    pass
            time.sleep(WAIT*3)
            print('################ Save to Created.txt ################')
            f = open('Created.txt', 'a')
            f.write(user_name + "\t" + password + "\t" +birthday + "\t"+ number + "\n")
            f.close()

            driver.quit()
        except Exception as e:
            print(e)
            driver.quit()

    user_info_file.close()
main()