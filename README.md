# Auto-Gmail-Creator

## Description
Auto Google account creation

This script uses [sms-activate.org](https://sms-activate.org) api for phone verification but please note that they charge tiny money.

You don't need to download Chromedriver manually. The script does it automatically with webdriver manager. Is it helpful? But you need to use Chrome Browser in your PC in general.

I am trying to find best free sms activation service. If you have any idea, Please let me know.

Thanks.

1. Need to install Python 3.x.
2. Install Dependencies with "pip install -r requirements.txt"
    - selenium==4.8.2
    - selenium_wire==5.1.0
    - webdriver_manager==3.8.5
3. Run script 
    - Manual Entry for Gmail
        You edit the 'user.csv' with given type such as First name, Last name, Password, Birthday, Username(optional) from the second line.
        If the 5th parameter on user.csv is not passed by userBot generates username automatically adding FN + dot + LN + random 5 digits.(john.doe12345@gmail.com)
    - Proxy
        You can add your own proxy on line 175, then you need to remove comment from line 197-183.
        ```
        proxy = "socks5://login:password@176.103.246.143:12324" # fixed proxy

        'proxy': {
            'http': proxy,
            'https': proxy,
            'no_proxy': 'localhost,127.0.0.1' # excludes
        },
        ```
    - Headless (without UI)
        You can remote comment this line on 190.
        ```
            chrome_options.add_argument('--headless')
        ```

    - Profile (Optional)
        You can add your own profile if you want by specifying the path.
        ```
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument(r"--user-data-dir=C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data") #e.g. C:\Users\nICE\AppData\Local\Google\Chrome\User Data
        chrome_options.add_argument(r'--profile-directory=Profile 11')
        ```
    - Run script 
        ```python app.py``` or ```python3 app.py```

3. If an account is created successfully, it will be added to 'created_accounts.txt'.

## Images
- Editing the user.csv
    ![edit_user](./user.jpg)

- Bot will create chrome browser repeatedly for each gmail.
    ![auto-gmail-create-leostech](./gmail-create.jpg)

- You can visit [sms-activate.org](https://sms-activate.org) to see it's apis.
    ![sms-activate](./sms.jpg)

    ![auto-gmail-create](./country_code.jpg)

    ![auto-gmail-create](./country_table.jpg)
    

## Github

https://github.com/leostech

## Email

tr.soft.engineer@gmail.com

## Skype

https://join.skype.com/invite/H6S0RFA69GNK

## Telegram

https://t.me/softengineer1210

## Phone

+1 229 299 5932

If you like it, Please donate here. Thanks. :)

Ether: 0xb6c9ce60a5db371164c461ec6d3fcae01292eb55

