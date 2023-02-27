# Auto-Gmail-Creator

## Description
Latest Open Source Bulk Auto Google Gccount Regiteration script 2023

According to [Jonathan](https://www.quora.com/profile/Jonathan-Elder)'s desription ,only about five gmail addresses can be verified on a single phone number.
To avoid this limitation, I recommend to use SMS activation services.

This script uses [sms-activate.org](https://sms-activate.org) api for phone verification but please note that they charge tiny money.

You don't need to download Chromedriver manually. The script does it automatically with webdriver manager. Is it helpful? But you need to use Chrome Browser in your PC in general.

This is an Auto Gmail Creator script but you can refer this repo to learn Selenium & Scraping.

I am trying to find best free sms activation service. If you have any idea, Please let me know.

Thanks.

1. Need to install Python 3.x.
2. Install Dependencies with ```pip install -r requirements.txt```
    - requests==2.27.1
    - selenium==4.8.2
    - webdriver_manager==3.8.5
3. Run script 
    - Browser Choice
        You can use Chrome, Firefox by commenting 2 lines.
        ```
        #options = ChromeOptions()
        options = FirefoxOptions()

        #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options, desired_capabilities=capabilities)

        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = options, desired_capabilities=capabilities)
        ```
    - Manual Entry for Gmail
        You edit the 'user.csv' with given type such as First name, Last name, Password, Birthday, Username(optional) from the second line.
        If the 5th parameter on user.csv is not passed by userBot generates username automatically adding FN + dot + LN + random 5 digits.(john.doe12345@gmail.com)
    - Automatic Username with popular names.
        Thanks to [BourneXu](https://github.com/BourneXu/AutoCreateGmailAccount), I implemented the script to generate Random Popular Usernames.
        You can set this variant as "True" to use this functionality.
        ```
        AUTO_GENERATE_UERINFO = True
        ```
    - Proxy
        If you want to use socks proxy, please remove comment theses lines.
        [Free Proxy list](http://free-proxy.cz/en/proxylist/country/all/socks5/ping/all/2) is here
        ```
        SOCKS_PROXY = "socks5://user:pass@ip:port"
        HTTP_PROXY = "http://user:pass@ip:port"
        HTTPS_PROXY = "https://user:pass@ip:port"
        ```

    - Headless or With UI (Optional)
        You can remote comment this line on 190.
        ```
            options.add_argument('--headless')
        ```

    - Profile (Optional)
        You can add your own profile if you want by specifying the path.
        ```
        options.add_argument("--incognito")
        options.add_argument(r"--user-data-dir=C:\\Users\\Username\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument(r'--profile-directory=ProfileName')
        ```
    - Run script 
        ```python app.py``` or ```python3 app.py```

3. If an account is created successfully, it will be added to 'Created.txt'.

## Images
- Running
    ![auto-gmail-creator-leostech](./data/images/auto-gmail-creator-leostech.jpg)

- Edit user.csv
    With Notepad
    ![edit-user-notepad](./data/images/user-notepad-leostech.jpg)

    With Excel
    ![edit-user-excel](./data/images/user-excel-leostech.jpg)

- Bot will create chrome browser repeatedly for each gmail.
    ![auto-gmail-create-leostech](./data/images/gmail-create-leostech.jpg)

- You can visit [sms-activate.org](https://sms-activate.org) to see it's apis.
    ![sms-activate](./data/images/sms-leostech.jpg)

- To see the country code, you can hit here.
    ![auto-gmail-creator-leostech](./data/images/country-code-leostech.jpg)
    ![auto-gmail-creator-leostech](./data/images/country-table-leostech.jpg)

## Email

tr.soft.engineer@gmail.com

## Skype

https://join.skype.com/invite/H6S0RFA69GNK

## Telegram

https://t.me/softengineer1210

## Github

https://github.com/leostech

## Phone

+12292995932

If you like it, Please star this repo or folk or donate. Thanks. :)

Ether: 0xb6c9ce60a5db371164c461ec6d3fcae01292eb55

